"""Guard the repository layout that `gh skill install` and installed copies depend on.

Run from the repository root:  python3 -B -m unittest discover -s tests -v
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILLS = REPO / "skills"
# Agent Skills naming rule: lowercase letters, digits and single hyphens, at most 64 characters.
NAME_RULE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK = re.compile(r"\]\(([^)\s]+)\)")


def frontmatter_name(skill_md: Path) -> str | None:
    match = re.match(
        r"---\n(.*?)\n---\n", skill_md.read_text(encoding="utf-8"), re.DOTALL
    )
    if not match:
        return None
    for line in match.group(1).splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip("'\"")
    return None


def skill_dirs() -> list[Path]:
    return (
        sorted(path for path in SKILLS.iterdir() if path.is_dir())
        if SKILLS.is_dir()
        else []
    )


class LayoutTest(unittest.TestCase):
    def test_skills_folder_holds_the_skill(self):
        self.assertIn(
            "startup-eval",
            [path.name for path in skill_dirs()],
            "gh skill install looks for skills/<name>/SKILL.md; skills/startup-eval/ is missing",
        )

    def test_each_skill_name_matches_its_folder(self):
        for folder in skill_dirs():
            with self.subTest(skill=folder.name):
                skill_md = folder / "SKILL.md"
                self.assertTrue(
                    skill_md.is_file(), f"skills/{folder.name}/SKILL.md is missing"
                )
                name = frontmatter_name(skill_md)
                self.assertEqual(
                    name, folder.name, "frontmatter name must equal the folder name"
                )
                self.assertRegex(name, NAME_RULE)
                self.assertLessEqual(len(name), 64)

    def test_no_skill_md_at_repository_root(self):
        # gh skill ignores a root SKILL.md, and a second copy would drift from the real one.
        self.assertFalse(
            (REPO / "SKILL.md").exists(),
            "SKILL.md belongs in skills/<name>/, not at the root",
        )

    def test_each_skill_carries_the_licence(self):
        root_licence = (REPO / "LICENSE").read_bytes()
        for folder in skill_dirs():
            with self.subTest(skill=folder.name):
                licence = folder / "LICENSE"
                self.assertTrue(
                    licence.is_file(), f"skills/{folder.name}/LICENSE is missing"
                )
                self.assertEqual(
                    licence.read_bytes(),
                    root_licence,
                    "skill LICENSE must match the root LICENSE",
                )

    def test_skill_links_stay_inside_the_skill_folder(self):
        # Installed copies contain only skills/<name>/, so relative links must resolve inside it.
        for folder in skill_dirs():
            for markdown in sorted(folder.rglob("*.md")):
                for target in MARKDOWN_LINK.findall(
                    markdown.read_text(encoding="utf-8")
                ):
                    if "://" in target or target.startswith(("#", "mailto:")):
                        continue
                    resolved = (markdown.parent / target.split("#", 1)[0]).resolve()
                    with self.subTest(
                        file=str(markdown.relative_to(REPO)), link=target
                    ):
                        self.assertTrue(
                            resolved.is_relative_to(folder.resolve()),
                            "link leaves the skill folder",
                        )
                        self.assertTrue(resolved.exists(), "link target does not exist")

    def test_default_library_folder_is_ignored(self):
        # The scripts default to ./startup-evals, which holds confidential decks.
        lines = (REPO / ".gitignore").read_text(encoding="utf-8").splitlines()
        self.assertIn("startup-evals/", [line.strip() for line in lines])


if __name__ == "__main__":
    unittest.main()

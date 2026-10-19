"""Exercise .github/tripwire.sh in a throwaway Git repository.

Each test builds its own small repository, so the checks do not depend on this clone's history.
Needs Git. Run from the repository root:  python3 -B -m unittest discover -s tests -v
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

TRIPWIRE = Path(__file__).resolve().parents[1] / ".github" / "tripwire.sh"
# Built from parts so this file does not trip the silenced-check scan itself.
SILENCED_LINE = "x = 1  # " + "noqa\n"


class TripwireTest(unittest.TestCase):
    def setUp(self):
        self.repo = Path(tempfile.mkdtemp(prefix="tripwire-test-")).resolve()
        self.addCleanup(shutil.rmtree, self.repo)
        self.env = {
            **os.environ,
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_AUTHOR_NAME": "Test",
            "GIT_AUTHOR_EMAIL": "test@example.com",
            "GIT_COMMITTER_NAME": "Test",
            "GIT_COMMITTER_EMAIL": "test@example.com",
        }
        (self.repo / ".github").mkdir()
        shutil.copyfile(TRIPWIRE, self.repo / ".github" / "tripwire.sh")
        (self.repo / "app.py").write_text("print('hello')\n", encoding="utf-8")
        self.git("init", "-q", "-b", "main")
        self.git("add", ".")
        self.git("commit", "-q", "-m", "base")
        self.base = self.git("rev-parse", "HEAD").strip()

    def git(self, *args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=self.repo,
            env=self.env,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout

    def commit(self, path: str, text: str) -> None:
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        self.git("add", "-f", path)
        self.git("commit", "-q", "-m", f"add {path}")

    def tripwire(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["bash", ".github/tripwire.sh", *args],
            cwd=self.repo,
            env=self.env,
            capture_output=True,
            text=True,
            check=False,  # the tests assert on the exit code
        )

    def test_clean_repository_passes(self):
        result = self.tripwire(self.base)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("tripwire: clean", result.stdout)

    def test_missing_base_ref_fails_instead_of_passing(self):
        result = self.tripwire("origin/no-such-branch")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertNotIn("tripwire: clean", result.stdout)
        self.assertIn("origin/no-such-branch", result.stdout)

    def test_new_silenced_check_fails(self):
        self.commit("app.py", "print('hello')\n" + SILENCED_LINE)
        result = self.tripwire(self.base)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("silence a check", result.stdout)

    def test_committed_deck_fails(self):
        self.commit("decks/pitch.pdf", "not really a pdf\n")
        result = self.tripwire()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("decks/pitch.pdf", result.stdout)

    def test_evaluation_library_content_fails(self):
        self.commit("startup-evals/INDEX.md", "| row |\n")
        result = self.tripwire()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("startup-evals/INDEX.md", result.stdout)

    def test_fictional_example_pdf_is_allowed(self):
        self.commit("examples/demo/deck.pdf", "fictional\n")
        result = self.tripwire(self.base)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()

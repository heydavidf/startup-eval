"""Compile every Python file and run the README's offline script pipeline.

The pipeline runs from a temporary copy of skills/startup-eval (the files `gh skill install`
places in an agent's skills folder) against a scratch library, so it also proves that an
installed copy works on its own. prepare_pdf.py needs Poppler on PATH.

Run from the repository root:  python3 -B -m unittest discover -s tests -v
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / "skills" / "startup-eval"
EXAMPLE = REPO / "examples" / "fictional-tidewell"
EXAMPLE_DECK = EXAMPLE / "working" / "inputs" / "tidewell-pitch-deck.pdf"
EXAMPLE_FILES = [
    "run-manifest.json",
    "source-brief.md",
    "report.md",
    "claim-register.md",
    "evidence-register.md",
]


class CompileTest(unittest.TestCase):
    def test_every_python_file_compiles(self):
        files = [
            path
            for folder in (SKILL, EXAMPLE, REPO / "tests")
            for path in sorted(folder.rglob("*.py"))
        ]
        self.assertTrue(files)
        for path in files:
            with self.subTest(file=str(path.relative_to(REPO))):
                compile(path.read_text(encoding="utf-8"), str(path), "exec")


class PipelineTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="startup-eval-test-")).resolve()
        self.addCleanup(shutil.rmtree, self.tmp)
        self.skill = self.tmp / "installed" / "startup-eval"
        shutil.copytree(SKILL, self.skill)
        self.root = self.tmp / "library"
        self.env = {
            **os.environ,
            "STARTUP_EVAL_ROOT": str(self.root),
            "PYTHONDONTWRITEBYTECODE": "1",
        }

    def run_script(
        self, name: str, *args: object, env: dict | None = None
    ) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(self.skill / "scripts" / name), *map(str, args)],
            cwd=self.tmp,
            env=env or self.env,
            capture_output=True,
            text=True,
            check=False,  # callers assert on the return code themselves
        )

    def ok(self, name: str, *args: object) -> str:
        result = self.run_script(name, *args)
        self.assertEqual(
            result.returncode, 0, f"{name} failed:\n{result.stdout}\n{result.stderr}"
        )
        return result.stdout

    def test_offline_pipeline_from_installed_copy(self):
        self.ok("init_library.py")
        self.assertTrue((self.root / "INDEX.md").is_file())
        self.assertTrue((self.root / "CALIBRATION_LOG.md").is_file())

        created = json.loads(
            self.ok(
                "create_run.py",
                "--startup",
                "Tidewell",
                "--source",
                EXAMPLE_DECK,
                "--date",
                "2026-01-01",
            )
        )
        run_dir = Path(created["run_dir"])
        self.assertEqual(run_dir, self.root / "Evaluations" / "Tidewell - 2026-01-01")

        metadata = json.loads(
            self.ok("prepare_pdf.py", created["inbox_sources"][0], run_dir)
        )
        self.assertEqual(metadata["pages"], 3)
        self.assertEqual(len(metadata["rendered_pages"]), 3)

        for name in EXAMPLE_FILES:
            shutil.copyfile(EXAMPLE / name, run_dir / name)
        self.ok("render_dashboard.py", run_dir / "run-manifest.json")
        # Same manifest and template, so the installed copy must reproduce the committed example dashboard.
        self.assertEqual(
            (run_dir / "dashboard.html").read_bytes(),
            (EXAMPLE / "dashboard.html").read_bytes(),
        )

        self.assertIn("VALIDATION PASSED", self.ok("validate_evaluation.py", run_dir))
        self.ok("update_registry.py", run_dir)
        self.assertIn(
            "`Evaluations/Tidewell - 2026-01-01/`",
            (self.root / "INDEX.md").read_text(encoding="utf-8"),
        )
        self.assertIn(
            "| Tidewell |",
            (self.root / "CALIBRATION_LOG.md").read_text(encoding="utf-8"),
        )

    def test_missing_poppler_is_reported_by_name(self):
        empty_path = self.tmp / "empty-bin"
        empty_path.mkdir()
        result = self.run_script(
            "prepare_pdf.py",
            EXAMPLE_DECK,
            self.tmp / "run",
            env={**self.env, "PATH": str(empty_path)},
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Required command not found: pdfinfo", result.stderr)


if __name__ == "__main__":
    unittest.main()

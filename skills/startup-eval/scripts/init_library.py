#!/usr/bin/env python3
"""Initialize an evaluation library without overwriting user data."""

from __future__ import annotations

import argparse
import os
from pathlib import Path


def default_root() -> Path:
    """Library root: $STARTUP_EVAL_ROOT if set, else ./startup-evals in the working directory."""
    env = os.environ.get("STARTUP_EVAL_ROOT")
    return Path(env).expanduser() if env else Path.cwd() / "startup-evals"


INDEX = """# Startup Evals - Registry

One row per evaluation. See `CALIBRATION_LOG.md` for methodology notes.

| Date | Startup | Stage | Mode | Score | Verdict | Verdict mix (C/U/R/X) | Folder |
|---|---|---|---|---:|---|---|---|
"""

CALIBRATION = """# Calibration Log

Track skeptic behavior across evaluations. Review patterns after 5-8 runs; do not tune the method from one deck.

## Current method

| Date | Startup | Completed claims | Confirmed | Uncertain | Refuted | Unverified | Refute rate | Score | Owner gut check |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
<!-- CURRENT_ROWS -->

Runs: 0. Mean refute rate: n/a. Mean score: n/a.
"""


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=default_root(),
        help="Library root (default: $STARTUP_EVAL_ROOT, else ./startup-evals)",
    )
    args = parser.parse_args()
    root = args.root.expanduser().resolve()
    (root / "Inbox").mkdir(parents=True, exist_ok=True)
    (root / "Evaluations").mkdir(parents=True, exist_ok=True)
    write_if_missing(root / "INDEX.md", INDEX)
    write_if_missing(root / "CALIBRATION_LOG.md", CALIBRATION)
    print(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

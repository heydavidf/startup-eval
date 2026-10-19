#!/usr/bin/env python3
"""Copy source material to Inbox and create a collision-safe evaluation directory."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
from datetime import date
from pathlib import Path


def default_root() -> Path:
    """Library root: $STARTUP_EVAL_ROOT if set, else ./startup-evals in the working directory."""
    env = os.environ.get("STARTUP_EVAL_ROOT")
    return Path(env).expanduser() if env else Path.cwd() / "startup-evals"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def safe_name(value: str) -> str:
    value = re.sub(r"[\\/:*?\"<>|]", "-", value).strip(" .")
    return re.sub(r"\s+", " ", value) or "Startup"


def unique_copy(source: Path, inbox: Path) -> Path:
    candidate = inbox / source.name
    if candidate.exists() and digest(candidate) == digest(source):
        return candidate
    counter = 2
    while candidate.exists():
        candidate = inbox / f"{source.stem}-{counter}{source.suffix}"
        counter += 1
    shutil.copy2(source, candidate)
    return candidate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--startup", required=True)
    parser.add_argument("--source", type=Path, action="append", required=True)
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument(
        "--root",
        type=Path,
        default=default_root(),
        help="Library root (default: $STARTUP_EVAL_ROOT, else ./startup-evals)",
    )
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    inbox = root / "Inbox"
    evaluations = root / "Evaluations"
    inbox.mkdir(parents=True, exist_ok=True)
    evaluations.mkdir(parents=True, exist_ok=True)

    copied = []
    for raw in args.source:
        source = raw.expanduser().resolve()
        if not source.is_file():
            raise SystemExit(f"Source does not exist: {source}")
        copied.append(unique_copy(source, inbox))

    base = f"{safe_name(args.startup)} - {args.date}"
    run_dir = evaluations / base
    counter = 2
    while run_dir.exists():
        run_dir = evaluations / f"{base}-r{counter}"
        counter += 1
    (run_dir / "working" / "inputs").mkdir(parents=True)
    (run_dir / "working" / "rendered-pages").mkdir(parents=True)

    result = {
        "root": str(root),
        "run_dir": str(run_dir),
        "inbox_sources": [str(path) for path in copied],
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

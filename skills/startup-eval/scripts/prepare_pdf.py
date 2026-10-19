#!/usr/bin/env python3
"""Extract PDF text, render pages, and record immutable source metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path


def require(binary: str) -> str:
    path = shutil.which(binary)
    if not path:
        raise SystemExit(f"Required command not found: {binary}")
    return path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--dpi", type=int, default=120)
    args = parser.parse_args()

    pdf = args.pdf.expanduser().resolve()
    run_dir = args.run_dir.expanduser().resolve()
    if not pdf.is_file():
        raise SystemExit(f"PDF does not exist: {pdf}")
    inputs = run_dir / "working" / "inputs"
    rendered = run_dir / "working" / "rendered-pages"
    inputs.mkdir(parents=True, exist_ok=True)
    rendered.mkdir(parents=True, exist_ok=True)

    pdfinfo = require("pdfinfo")
    pdftotext = require("pdftotext")
    pdftoppm = require("pdftoppm")
    info = subprocess.run(
        [pdfinfo, str(pdf)], check=True, text=True, capture_output=True
    ).stdout
    pages = 0
    for line in info.splitlines():
        if line.startswith("Pages:"):
            pages = int(line.split(":", 1)[1].strip())
            break
    if pages < 1:
        raise SystemExit("Could not determine PDF page count")

    stem = pdf.stem
    text_path = inputs / f"{stem}.txt"
    subprocess.run([pdftotext, "-layout", str(pdf), str(text_path)], check=True)
    prefix = rendered / stem
    subprocess.run(
        [pdftoppm, "-jpeg", "-r", str(args.dpi), str(pdf), str(prefix)], check=True
    )
    images = sorted(rendered.glob(f"{stem}-*.jpg"))
    if len(images) != pages:
        raise SystemExit(f"Rendered {len(images)} pages, expected {pages}")

    metadata = {
        "path": str(pdf),
        "sha256": sha256(pdf),
        "pages": pages,
        "text_path": str(text_path),
        "rendered_pages": [str(path) for path in images],
    }
    metadata_path = inputs / f"{stem}.metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(json.dumps(metadata, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

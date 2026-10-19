#!/usr/bin/env python3
"""Rebuild the fictional Tidewell example: a synthetic three-page pitch deck PDF and the dashboard.

Run from anywhere:  python3 examples/fictional-tidewell/build_example.py
Everything produced is deterministic, so a rebuild should leave the committed files unchanged.
Standard library only. Rendering the PDF to images (skills/startup-eval/scripts/prepare_pdf.py) needs Poppler.
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "startup-eval"
RENDER = SKILL_ROOT / "scripts" / "render_dashboard.py"

PAGES = [
    [
        ("Tidewell", 28),
        ("Tide and mooring alerts for small-harbour boat owners", 14),
        ("(Fictional company, fictional region, fictional numbers)", 11),
        ("", 11),
        ("Founders: Aila Brennan and Teo Marsh", 12),
        ("Previously ran harbour operations for a regional port authority", 12),
        ("Raising 600,000 seed at 6,000,000 post-money", 12),
    ],
    [
        ("The market", 22),
        ("400,000 registered leisure boats in the region", 12),
        ("x 120 per year subscription", 12),
        ("= 48,000,000 total addressable market per year", 12),
        ("", 11),
        ("Twelve harbours will publish live sensor feeds by next year", 12),
        ("Harbour authorities are funding sensors; we ride the wave", 12),
    ],
    [
        ("Traction and plan", 22),
        ("1,200 paying subscribers after six months", 12),
        ("Price: 120 per year or 12 per month", 12),
        ("Cost to serve: 31 per boat per year (sensor access + messaging)", 12),
        ("Churn: 15 percent per year", 12),
        ("", 11),
        ("Year 1: 0.4M   Year 2: 2.9M   Year 3: 9.6M revenue", 12),
    ],
]


def pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def page_stream(lines: list[tuple[str, int]]) -> bytes:
    parts = ["BT"]
    y = 740
    for text, size in lines:
        y -= size + 10
        if text:
            parts.append(f"/F1 {size} Tf 1 0 0 1 60 {y} Tm ({pdf_escape(text)}) Tj")
    parts.append("ET")
    return "\n".join(parts).encode("latin-1")


def build_pdf() -> bytes:
    objects: list[bytes] = []

    def add(body: bytes) -> int:
        objects.append(body)
        return len(objects)

    font = add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    page_ids = []
    pages_id = len(objects) + 1 + 2 * len(PAGES)  # reserved after content/page pairs
    for lines in PAGES:
        stream = page_stream(lines)
        content = add(b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream")
        page = add(
            b"<< /Type /Page /Parent %d 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 %d 0 R >> >> /Contents %d 0 R >>"
            % (pages_id, font, content)
        )
        page_ids.append(page)
    kids = " ".join(f"{pid} 0 R" for pid in page_ids).encode()
    assert add(b"<< /Type /Pages /Kids [" + kids + b"] /Count %d >>" % len(page_ids)) == pages_id
    catalog = add(b"<< /Type /Catalog /Pages %d 0 R >>" % pages_id)

    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, 1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % number + body + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n" % (len(objects) + 1)
    out += b"0000000000 65535 f \n"
    for offset in offsets:
        out += b"%010d 00000 n \n" % offset
    out += b"trailer\n<< /Size %d /Root %d 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objects) + 1, catalog, xref)
    return bytes(out)


def main() -> int:
    inputs = HERE / "working" / "inputs"
    inputs.mkdir(parents=True, exist_ok=True)
    pdf_path = inputs / "tidewell-pitch-deck.pdf"
    pdf = build_pdf()
    pdf_path.write_bytes(pdf)
    print(f"wrote {pdf_path.relative_to(HERE)} sha256={hashlib.sha256(pdf).hexdigest()}")

    manifest = HERE / "run-manifest.json"
    if not manifest.is_file():
        raise SystemExit(f"Missing {manifest}; this example needs its run-manifest.json to render the dashboard")
    if not RENDER.is_file():
        raise SystemExit(f"Missing {RENDER}; run this script from a complete clone of the startup-eval repository")
    subprocess.run([sys.executable, str(RENDER), str(manifest), "--output", str(HERE / "dashboard.html")], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

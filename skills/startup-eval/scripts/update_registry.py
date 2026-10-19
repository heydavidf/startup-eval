#!/usr/bin/env python3
"""Publish a validated evaluation to INDEX.md and CALIBRATION_LOG.md."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

from validate_evaluation import validate


def default_root() -> Path:
    """Library root: $STARTUP_EVAL_ROOT if set, else ./startup-evals in the working directory."""
    env = os.environ.get("STARTUP_EVAL_ROOT")
    return Path(env).expanduser() if env else Path.cwd() / "startup-evals"


def tally(data: dict) -> dict[str, int]:
    result = {"confirmed": 0, "uncertain": 0, "refuted": 0, "unverified": 0}
    for claim in data["claims"]:
        if not claim.get("selected"):
            continue
        if claim.get("verification_status") == "unverified":
            result["unverified"] += 1
        elif claim.get("verdict") in result:
            result[claim["verdict"]] += 1
    return result


def replace_aggregate(
    text: str, run_count: int, mean_refute: float, mean_score: float
) -> str:
    line = f"Runs: {run_count}. Mean refute rate: {mean_refute:.0f}%. Mean score: {mean_score:.1f}."
    return re.sub(r"Runs: \d+\. Mean refute rate:.*", line, text, count=1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    parser.add_argument(
        "--root",
        type=Path,
        default=default_root(),
        help="Library root (default: $STARTUP_EVAL_ROOT, else ./startup-evals)",
    )
    args = parser.parse_args()
    run_dir = args.run_dir.expanduser().resolve()
    root = args.root.expanduser().resolve()
    errors = validate(run_dir)
    if errors:
        raise SystemExit(
            "Refusing registry update; evaluation validation failed:\n- "
            + "\n- ".join(errors)
        )
    data = json.loads((run_dir / "run-manifest.json").read_text(encoding="utf-8"))
    counts = tally(data)
    completed = counts["confirmed"] + counts["uncertain"] + counts["refuted"]
    refute_rate = round(100 * counts["refuted"] / completed) if completed else 0
    mix = f"{counts['confirmed']}/{counts['uncertain']}/{counts['refuted']}/{counts['unverified']}"
    try:
        relative = run_dir.relative_to(root)
    except ValueError:
        raise SystemExit(
            f"Run directory {run_dir} is not inside the library root {root}; pass --root or set STARTUP_EVAL_ROOT"
        )

    index_path = root / "INDEX.md"
    index = index_path.read_text(encoding="utf-8")
    if str(relative) not in index:
        index += f"| {data['date']} | {data['startup']} | {data['stage']} | {data['mode']} | {data['scorecard']['overall_score']:.1f} | {data['scorecard']['overall_verdict']} | {mix} | `{relative}/` |\n"
        index_path.write_text(index, encoding="utf-8")

    calibration_path = root / "CALIBRATION_LOG.md"
    calibration = calibration_path.read_text(encoding="utf-8")
    marker = "## Legacy baseline (pre-contract)"
    row_marker = "<!-- CURRENT_ROWS -->"
    row = f"| {data['date']} | {data['startup']} | {completed} | {counts['confirmed']} | {counts['uncertain']} | {counts['refuted']} | {counts['unverified']} | {refute_rate}% | {data['scorecard']['overall_score']:.1f} | TBD |\n"
    if str(data["startup"]) + " | " + str(completed) not in calibration:
        if row_marker not in calibration:
            raise SystemExit(
                f"Calibration file is missing required marker: {row_marker}"
            )
        calibration = calibration.replace(row_marker, row + row_marker)

    rows = re.findall(
        r"\| \d{4}-\d{2}-\d{2} \| .*? \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+)% \| ([\d.]+) \|",
        calibration.split(marker)[0],
    )
    if rows:
        refutes = [float(row_data[5]) for row_data in rows]
        scores = [float(row_data[6]) for row_data in rows]
        calibration = replace_aggregate(
            calibration,
            len(rows),
            sum(refutes) / len(refutes),
            sum(scores) / len(scores),
        )
    calibration_path.write_text(calibration, encoding="utf-8")
    print(f"Registered {data['startup']} in {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

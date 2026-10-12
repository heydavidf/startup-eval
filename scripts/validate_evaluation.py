#!/usr/bin/env python3
"""Validate a startup evaluation before registry publication."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path


REQUIRED_FILES = [
    "source-brief.md",
    "claim-register.md",
    "evidence-register.md",
    "report.md",
    "dashboard.html",
    "run-manifest.json",
]
DIMENSIONS = [
    "TAM Credibility",
    "SOM Feasibility",
    "Unit Economics / Feasibility",
    "Market Timing",
    "Assumption & Risk Transparency",
]
VERDICTS = {"confirmed", "uncertain", "refuted"}
EVIDENCE = {"high", "medium", "low", "none"}
ISSUES = {
    "unsupported",
    "contradicted",
    "denominator-error",
    "category-error",
    "arithmetic-error",
    "misleading-framing",
    "outdated",
    "none",
}


def band(score: float) -> str:
    if score >= 7:
        return "Invest-grade"
    if score >= 5:
        return "Credible-with-gaps"
    if score >= 3:
        return "Caution"
    return "Pass"


def validate(run_dir: Path) -> list[str]:
    errors: list[str] = []
    for filename in REQUIRED_FILES:
        if not (run_dir / filename).is_file():
            errors.append(f"Missing required file: {filename}")
    manifest_path = run_dir / "run-manifest.json"
    if not manifest_path.is_file():
        return errors
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return errors + [f"Invalid manifest JSON: {exc}"]

    required = {
        "schema_version", "methodology_version", "startup", "date", "stage",
        "source_summary", "mode", "inputs", "summary", "verdict_summary",
        "scorecard", "claims", "market_sizing", "scenarios", "risks",
        "investability", "sources", "agents", "failures",
    }
    missing = sorted(required - set(data))
    if missing:
        errors.append(f"Missing manifest keys: {', '.join(missing)}")

    scorecard = data.get("scorecard", {})
    dimensions = scorecard.get("dimensions", [])
    names = [item.get("name") for item in dimensions]
    if names != DIMENSIONS:
        errors.append("Scorecard must contain the five required dimensions in canonical order")
    scores = []
    for item in dimensions:
        value = item.get("score")
        if not isinstance(value, (int, float)) or not 0 <= value <= 10:
            errors.append(f"Invalid dimension score: {item}")
        else:
            scores.append(float(value))
        if not item.get("rationale"):
            errors.append(f"Missing rationale for dimension: {item.get('name')}")
    if len(scores) == 5:
        expected = round(sum(scores) / 5, 1)
        actual = scorecard.get("overall_score")
        if not isinstance(actual, (int, float)) or not math.isclose(float(actual), expected, abs_tol=0.01):
            errors.append(f"Overall score must be {expected}, found {actual}")
        elif scorecard.get("overall_verdict") != band(float(actual)):
            errors.append(f"Score {actual} must map to {band(float(actual))}")

    sources = data.get("sources", [])
    source_ids = set()
    for source in sources:
        source_id = source.get("id")
        if not source_id or source_id in source_ids:
            errors.append(f"Missing or duplicate source ID: {source_id}")
        source_ids.add(source_id)
        if not str(source.get("url", "")).startswith(("https://", "http://")):
            errors.append(f"Source {source_id} has no human-readable URL")
        if source.get("quality") not in {"primary", "secondary"}:
            errors.append(f"Source {source_id} has invalid quality")

    claims = data.get("claims", [])
    claim_ids = set()
    selected = 0
    for claim in claims:
        claim_id = claim.get("id")
        if not claim_id or claim_id in claim_ids:
            errors.append(f"Missing or duplicate claim ID: {claim_id}")
        claim_ids.add(claim_id)
        if claim.get("selected"):
            selected += 1
        status = claim.get("verification_status")
        verdict = claim.get("verdict")
        if status not in {"complete", "unverified", "not_selected"}:
            errors.append(f"Claim {claim_id} has invalid verification_status")
        if status == "complete" and verdict not in VERDICTS:
            errors.append(f"Claim {claim_id} has invalid completed verdict")
        if status == "unverified" and verdict is not None:
            errors.append(f"Claim {claim_id} must use null verdict when unverified")
        if claim.get("evidence_strength") not in EVIDENCE:
            errors.append(f"Claim {claim_id} has invalid evidence strength")
        issue_types = claim.get("issue_types", [])
        if not issue_types or not set(issue_types) <= ISSUES:
            errors.append(f"Claim {claim_id} has invalid issue types")
        unknown_sources = set(claim.get("source_ids", [])) - source_ids
        if unknown_sources:
            errors.append(f"Claim {claim_id} references unknown sources: {sorted(unknown_sources)}")
        if status == "complete" and not claim.get("deck_pages") and not claim.get("source_ids"):
            errors.append(f"Claim {claim_id} has no deck or external citation")
    if selected > 12:
        errors.append(f"Selected {selected} formal claims; maximum is 12")
    if not claims:
        errors.append("Manifest has no claims")

    for source in sources:
        unknown_claims = set(source.get("claim_ids", [])) - claim_ids
        if unknown_claims:
            errors.append(f"Source {source.get('id')} references unknown claims: {sorted(unknown_claims)}")

    dashboard = run_dir / "dashboard.html"
    if dashboard.is_file():
        body = dashboard.read_text(encoding="utf-8")
        for marker in ("id=\"bSimple\"", "id=\"bAdv\"", "function setView", "event.key.toLowerCase()==='a'"):
            if marker not in body:
                errors.append(f"Dashboard missing interaction marker: {marker}")
        if re.search(r"\{\{[A-Z_]+\}\}", body):
            errors.append("Dashboard contains unresolved template markers")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()
    run_dir = args.run_dir.expanduser().resolve()
    errors = validate(run_dir)
    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"VALIDATION PASSED: {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

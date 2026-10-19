#!/usr/bin/env python3
"""Render a self-contained evaluation dashboard from run-manifest.json."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def e(value: object) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def verdict_class(claim: dict) -> str:
    if claim.get("verification_status") == "unverified":
        return "unverified"
    return claim.get("verdict") or "unverified"


def source_links(ids: list[str], sources: dict[str, dict]) -> str:
    links = []
    for source_id in ids:
        source = sources.get(source_id)
        if source:
            links.append(f'<a href="{e(source["url"])}">{e(source_id)}</a>')
    return ", ".join(links) or "Deck only"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--template", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    manifest_path = args.manifest.expanduser().resolve()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    skill_root = Path(__file__).resolve().parents[1]
    template_path = args.template or skill_root / "assets" / "dashboard.html.tmpl"
    output_path = args.output or manifest_path.parent / "dashboard.html"
    template = template_path.read_text(encoding="utf-8")

    scorecard = data["scorecard"]
    hero = f"""<section class="hero"><div class="hero-grid"><div><div class="eyebrow">{e(data.get("stage", "Stage not stated"))} / {e(data.get("mode", "adaptive"))} diligence</div><h1>{e(data["startup"])}</h1><p>{e(data["summary"])}</p></div><div><div class="score">{e(scorecard["overall_score"])} <small>/ 10</small></div><div class="verdict">{e(scorecard["overall_verdict"])}</div></div></div></section>"""

    claims = data.get("claims", [])
    tally = {key: 0 for key in ("confirmed", "uncertain", "refuted", "unverified")}
    for claim in claims:
        if claim.get("selected"):
            tally[verdict_class(claim)] += 1
    completed = tally["confirmed"] + tally["uncertain"] + tally["refuted"]
    refute_rate = round(100 * tally["refuted"] / completed) if completed else 0

    score_rows = []
    for dim in scorecard["dimensions"]:
        score_rows.append(
            f"""<div class="score-row"><strong>{e(dim["name"])}</strong><div class="score-n">{e(dim["score"])}</div><div><div class="track"><i style="width:{float(dim["score"]) * 10:.0f}%"></i></div><div class="rationale advanced-inline">{e(dim["rationale"])}</div></div></div>"""
        )

    market_rows = (
        "".join(
            f"<tr><td>{e(row.get('segment'))}</td><td>{e(row.get('stated'))}</td><td>{e(row.get('rebuilt'))}</td><td>{e(row.get('serviceable'))}</td></tr>"
            for row in data.get("market_sizing", [])
        )
        or '<tr><td colspan="4">No market-sizing rows supplied.</td></tr>'
    )

    scenarios = "".join(
        f'<div class="scenario"><b>{e(item.get("name"))}: {e(item.get("outcome"))}</b><span class="muted">{e(item.get("basis"))}</span></div>'
        for item in data.get("scenarios", [])
    )
    risks = "".join(
        f'<div class="risk"><div class="rank">{idx}</div><div>{e(item)}</div></div>'
        for idx, item in enumerate(data.get("risks", []), 1)
    )
    simple_blocks = f"""
      <div class="card"><h2>The verdict</h2><p class="lede">{e(data["verdict_summary"])}</p></div>
      <div class="card third"><h2>Claim outcomes</h2><div class="metric"><span>Confirmed</span><b>{tally["confirmed"]}</b></div><div class="metric"><span>Uncertain</span><b>{tally["uncertain"]}</b></div><div class="metric"><span>Refuted</span><b>{tally["refuted"]}</b></div><div class="metric"><span>Unverified</span><b>{tally["unverified"]}</b></div><div class="metric"><span>Refute rate</span><b>{refute_rate}%</b></div></div>
      <div class="card wide"><h2>Scorecard</h2>{"".join(score_rows)}</div>
      <div class="card"><h2>Market reality</h2><table><thead><tr><th>Segment</th><th>Deck</th><th>Independent rebuild</th><th>Serviceable</th></tr></thead><tbody>{market_rows}</tbody></table></div>
      <div class="card half"><h2>Scenarios</h2>{scenarios}</div>
      <div class="card half"><h2>Top risks</h2>{risks}</div>
      <div class="card"><h2>What would make this investable</h2><p class="lede">{e(data.get("investability"))}</p></div>"""

    sources = {source["id"]: source for source in data.get("sources", [])}
    claim_rows = []
    for claim in claims:
        cls = verdict_class(claim)
        status = cls if claim.get("selected") else "not selected"
        pages = ", ".join(str(page) for page in claim.get("deck_pages", []))
        claim_rows.append(
            f"""<tr><td><b>{e(claim["id"])}</b></td><td>{e(claim["claim"])}</td><td>{e(claim.get("stated_value"))}</td><td><span class="pill {e(cls)}">{e(status)}</span></td><td>{e(claim.get("defensible_reality"))}</td><td>{e(pages)}</td><td>{source_links(claim.get("source_ids", []), sources)}</td></tr>"""
        )
    claims_block = f"<h2>Claim and assumption register</h2><table><thead><tr><th>ID</th><th>Claim</th><th>Stated</th><th>Verdict</th><th>Defensible reality</th><th>Deck pages</th><th>Evidence</th></tr></thead><tbody>{''.join(claim_rows)}</tbody></table>"

    evidence_rows = "".join(
        f'<tr><td>{e(source["id"])}</td><td><a href="{e(source["url"])}">{e(source["title"])}</a></td><td>{e(source.get("published"))}</td><td>{e(source.get("quality"))}</td><td>{e(", ".join(source.get("claim_ids", [])))}</td></tr>'
        for source in data.get("sources", [])
    )
    evidence_block = f"<h2>Evidence register</h2><table><thead><tr><th>ID</th><th>Source</th><th>Published</th><th>Quality</th><th>Claims</th></tr></thead><tbody>{evidence_rows}</tbody></table>"

    agents = data.get("agents", [])
    failures = data.get("failures", [])
    methodology = f"""<h2>Method and run integrity</h2><p>Mode: <b>{e(data.get("mode"))}</b>. Agents dispatched: <b>{len(agents)}</b>. Recorded failures: <b>{len(failures)}</b>. Selected claims: <b>{sum(1 for claim in claims if claim.get("selected"))}</b>.</p><p class="muted">Four independent specialist lenses, adversarial claim verification, evidence reconciliation, deterministic five-dimension scoring, and final consistency validation. Unverified results are surfaced rather than dropped.</p>"""

    replacements = {
        "{{TITLE}}": e(f"{data['startup']} - Startup Evaluation"),
        "{{DATE}}": e(data["date"]),
        "{{HERO}}": hero,
        "{{SIMPLE_BLOCKS}}": simple_blocks,
        "{{CLAIMS}}": claims_block,
        "{{EVIDENCE}}": evidence_block,
        "{{METHODOLOGY}}": methodology,
    }
    rendered = template
    for marker, value in replacements.items():
        rendered = rendered.replace(marker, value)
    output_path.write_text(rendered, encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Artifact Contract

## Run directory

```text
<Startup> - YYYY-MM-DD[-rN]/
├── source-brief.md
├── claim-register.md
├── evidence-register.md
├── report.md
├── dashboard.html
├── run-manifest.json
└── working/
    ├── inputs/
    ├── rendered-pages/
    ├── market-rebuild.md
    ├── bottom-up-valuation.md
    ├── comparables.md
    ├── technical-moat.md
    ├── skeptic-*.md
    └── synthesis.md
```

## Canonical manifest

Use JSON with these required top-level keys:

```json
{
  "schema_version": "1.0",
  "methodology_version": "1.0",
  "startup": "Example",
  "date": "YYYY-MM-DD",
  "stage": "Pre-seed",
  "source_summary": "Deck title and page count",
  "mode": "adaptive",
  "inputs": [{"path":"...","sha256":"...","pages":12}],
  "summary": "Plain-language description",
  "verdict_summary": "Decision-led synthesis",
  "scorecard": {
    "dimensions": [{"name":"TAM Credibility","score":5,"band":"yellow","rationale":"..."}],
    "overall_score": 5.0,
    "overall_verdict": "Credible-with-gaps"
  },
  "claims": [],
  "market_sizing": [],
  "scenarios": [],
  "risks": [],
  "investability": "...",
  "sources": [],
  "agents": [],
  "failures": []
}
```

Each claim requires: `id`, `type`, `claim`, `stated_value`, `deck_pages`, `impact`, `selected`, `verification_status`, `verdict`, `evidence_strength`, `issue_types`, `defensible_reality`, `reasoning`, and `source_ids`.

Each source requires: `id`, `title`, `url`, `published`, `accessed`, `quality` (`primary` or `secondary`), and `claim_ids`.

## Prose artifacts

`report.md` contains: metadata, startup summary, verdict, market sizing, bottom-up/valuation, comparables, technical/moat findings, scenarios, scorecard, top risks, investability conditions, triangulation, and linked sources.

`claim-register.md` contains every claim, including non-selected and unverified claims, with page references, verdict, evidence strength, issue tags, defensible reality, and source links.

`evidence-register.md` maps each source to claim IDs and identifies primary/secondary quality, publication/update date, and access date.

## Dashboard behavior

- Simple is the default view.
- Simple shows summary, verdict, score, decisive evidence, market reality, scenarios, and top risks.
- Advanced expands claim details, evidence register, dimension rationales, and a method summary with agent and failure counts inline. The full agent and failure log lives in `run-manifest.json`.
- Buttons and the `A` key switch view. Switching to Advanced scrolls the first newly revealed section into view only when triggered by the Advanced button; keyboard toggling does not force a scroll.
- The file is self-contained and requires no network resources.

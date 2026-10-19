---
name: startup-eval
description: Evaluate startup pitch decks and supporting diligence materials with a multi-agent workflow. Use for investor-style market-opportunity analysis, TAM/SAM/SOM rebuilding, bottom-up revenue and valuation checks, comparables, technical or regulatory plausibility, claim verification, investment scorecards, and presentation dashboards from PDF or other pitch materials.
license: MIT
compatibility: Requires an agent that can run subagents in parallel, browse the public web, run Python 3.11+ scripts, and write local files. PDF intake needs Poppler (pdfinfo, pdftotext, pdftoppm) on PATH. The bundled fictional example can be inspected offline.
---

# Startup Evaluation

Act as the lead investor and orchestrator. Preserve every material claim, separate deck statements from independent evidence, and make uncertainty visible.

## Read first

Read [methodology.md](references/methodology.md) before evaluating any deck. Read [orchestration.md](references/orchestration.md) before spawning agents. Read [artifact-contract.md](references/artifact-contract.md) before writing final artifacts.

For PDFs, also use the available PDF skill: render every page and inspect visuals as well as extracted text. For other presentation formats, use the relevant presentation/document skill.

## Defaults

- Evaluation root: the `STARTUP_EVAL_ROOT` environment variable if set, otherwise `./startup-evals` in the working directory. If the user names a different library location, pass it to every script with `--root`.
- Depth: `adaptive`
- Maximum formally verified load-bearing claims: 12
- Maximum adaptive single-claim escalations: 4
- Maximum concurrent subagents: 3
- Verdicts: `confirmed`, `uncertain`, `refuted`; use `verification_status: unverified` after exhausted dispatch failures
- Never expose confidential deck content to external services. Use public web research only for independent verification.

## Run the workflow

Scripts live in this skill's `scripts/` directory; run them with `python3` from any working directory. They use only the Python standard library. `prepare_pdf.py` additionally needs Poppler's `pdfinfo`, `pdftotext`, and `pdftoppm` on PATH and stops with a clear message when one is missing.

1. Create the library if missing with `scripts/init_library.py`.
2. Copy source material into `Inbox/` without deleting or overwriting the original.
3. Create a collision-safe run directory with `scripts/create_run.py`.
4. Render and extract each PDF with `scripts/prepare_pdf.py`. Inspect every rendered page.
5. Write `source-brief.md` with slide/page citations and a complete claim register. Rank claims by investment impact; never silently drop claims beyond the formal-verification cap.
6. Orchestrate research and verification exactly as specified in [orchestration.md](references/orchestration.md). Write every agent return into `working/`.
7. Reconcile evidence and write the canonical `run-manifest.json` before prose artifacts. Generate `dashboard.html` with `scripts/render_dashboard.py`.
8. Write `report.md`, `claim-register.md`, and `evidence-register.md` using the manifest as the source of truth.
9. Run `scripts/validate_evaluation.py`. Fix every error. Update `INDEX.md` and `CALIBRATION_LOG.md` only with `scripts/update_registry.py` after validation passes.
10. Open the dashboard in a browser and test both buttons, the `A` shortcut, desktop layout, and mobile layout.

The repository's [fictional worked example](https://github.com/heydavidf/startup-eval/tree/main/examples/fictional-tidewell) shows the finished run directory, manifest, and dashboard for an invented startup. It lives at the repository root, outside the installed skill folder.

## Depth modes

- `balanced`: four specialist lenses, three fresh batched skeptics, one synthesis agent.
- `adaptive`: balanced plus up to four fresh single-claim escalations selected by the rules in [orchestration.md](references/orchestration.md).
- `deep`: four specialist lenses, one fresh skeptic per selected load-bearing claim in waves of three, one synthesis agent.

The main agent remains the orchestrator and final consistency checker in every mode.

## Failure rules

- Retry a missing or malformed agent result once with a corrective prompt.
- After a second failure, record the agent failure and mark affected claims `unverified`; do not filter them out.
- If web access fails, complete deck-internal arithmetic and consistency checks, mark external conclusions unverified, and do not imply independent confirmation.
- Do not publish or register a run that fails validation.

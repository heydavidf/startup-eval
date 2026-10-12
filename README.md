# Startup Eval

Turn a pitch deck into investor-style diligence: a rebuilt market size, a bottom-up revenue and valuation check, comparable-company outcomes, claim-by-claim verification with verdicts, a five-dimension scorecard, and a self-contained HTML dashboard.

Startup Eval is an agent skill. Your agent reads the deck, writes a complete claim register, dispatches specialist and skeptic subagents against the public web, reconciles the evidence, and produces a run folder you can keep as a library. Every material claim stays visible, including the ones that could not be verified.

[Skill instructions](SKILL.md) · [Fictional worked example](examples/fictional-tidewell/README.md) · [Method](references/methodology.md) · [Agent contributor guide](AGENTS.md)

## Use it

Copy this entire `startup-eval` folder into the skills directory supported by your agent. Keep the folder name as `startup-eval`; it must match the `name` in `SKILL.md`. If your agent does not load skills automatically, ask it to read `SKILL.md` and follow its relative references.

You need an agent that can run subagents in parallel, browse the public web, run Python 3 scripts, and write local files. PDF intake uses Poppler's `pdfinfo`, `pdftotext`, and `pdftoppm` (`brew install poppler` on macOS, `apt install poppler-utils` on Debian and Ubuntu). There are no API keys, paid services, Python packages, or build steps. Your agent host may have its own usage costs; an adaptive run dispatches around ten subagents.

Give the agent a deck and, if you want, a library location. For example:

> Use startup-eval on `~/Decks/northwind-pitch.pdf`. Keep the evaluation library at `~/Startup Evals`. Run in adaptive mode and open the dashboard when you are done.

The library defaults to `./startup-evals` in the working directory, or to the `STARTUP_EVAL_ROOT` environment variable if set. Each run lands in `Evaluations/<Startup> - <date>/` with `report.md`, `claim-register.md`, `evidence-register.md`, `run-manifest.json`, `dashboard.html`, and a `working/` folder holding every agent return. After validation passes, the agent appends the run to `INDEX.md` and `CALIBRATION_LOG.md`.

Decks are confidential by default. The skill instructs the agent to use the public web only to verify claims, never to upload deck content to external services. Check that your agent host honours that before using it on material you cannot share.

## See the output first

The [fictional Tidewell example](examples/fictional-tidewell/README.md) is a complete run directory for an invented company. Open `examples/fictional-tidewell/dashboard.html` in a browser. Simple view shows the verdict, score, market table, scenarios, and risks; Advanced (button or the `A` key) expands the full claim register, the evidence register, the score rationales, and a run summary with the number of agents dispatched and failures recorded. It is **synthetic**: no real company, market, or source is described.

To exercise the scripts offline against a scratch library:

```sh
export STARTUP_EVAL_ROOT="$(mktemp -d)/startup-evals"
python3 scripts/init_library.py
python3 scripts/create_run.py --startup Tidewell --source examples/fictional-tidewell/working/inputs/tidewell-pitch-deck.pdf
```

The second command prints the new run directory. Then render pages with `python3 scripts/prepare_pdf.py <pdf-in-Inbox> <run_dir>`, copy the example's `run-manifest.json` and four Markdown files into the run directory, and finish with:

```sh
python3 scripts/render_dashboard.py <run_dir>/run-manifest.json
python3 scripts/validate_evaluation.py <run_dir>
python3 scripts/update_registry.py <run_dir>
```

`validate_evaluation.py` lists every problem it finds; `update_registry.py` refuses to register a run that fails validation. A real evaluation produces the manifest and Markdown through the agent workflow in `SKILL.md`, not by copying.

## How it works

1. The agent copies the deck into `Inbox/`, creates a collision-safe run directory, and renders every page.
2. It writes a source brief and a claim register, then selects up to twelve load-bearing claims for formal verification.
3. Four specialist lenses run in parallel: market rebuild, bottom-up and valuation, comparables, and technical/moat. Then fresh skeptic agents verify the selected claims without seeing the specialists' conclusions. Adaptive mode escalates up to four contested high-impact claims to single-claim agents.
4. The agent reconciles evidence by fixed rules (primary beats secondary; no confirmation without independent corroboration; disagreement resolves to `uncertain`), writes the canonical manifest, and renders the dashboard.
5. A validator checks the manifest, scores, enums, citations, and dashboard before the run can be registered.

The method, agent contracts, and artifact formats are in [references/](references/).

## Limits and maintenance

This is a diligence procedure, not a source of market facts or investment advice. Verdicts depend on what the agent can find on the public web on the day; paywalls, private companies, and missing data produce `uncertain` and `unverified` results by design. Scores are a structured opinion, not a prediction. Calibrate the skeptics over several runs before trusting the refute rate.

Tested on macOS with Python 3.14.5 and Poppler 26.02.0; the scripts use only the standard library and should run on Linux. Live multi-agent runs were exercised with Claude Code; other agent hosts can read the Markdown but have not been tested.

To update, replace the installed skill folder with a newer copy; your evaluation library lives elsewhere and is untouched. To uninstall, remove the installed folder; the library remains. Report defects through the repository's issue tracker.

**License:** [MIT](LICENSE).

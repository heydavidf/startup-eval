# Startup Eval

Turn a pitch deck into investor-style diligence: a rebuilt market size, a bottom-up revenue and valuation check, comparable-company outcomes, claim-by-claim verification with verdicts, a five-dimension scorecard, and a self-contained HTML dashboard.

Startup Eval is an agent skill. Your agent reads the deck, writes a complete claim register, dispatches specialist and skeptic subagents against the public web, reconciles the evidence, and produces a run folder you can keep as a library. Every material claim stays visible, including the ones that could not be verified.

[Skill instructions](skills/startup-eval/SKILL.md) · [Fictional worked example](examples/fictional-tidewell/README.md) · [Method](skills/startup-eval/references/methodology.md) · [Agent contributor guide](AGENTS.md) · [Changelog](CHANGELOG.md)

## Install

The skill is the [`skills/startup-eval/`](skills/startup-eval/) folder. With the GitHub CLI (version 2.100 or later), install it for your agent with one command:

```sh
gh skill install heydavidf/startup-eval startup-eval --agent claude-code --scope user
```

For Codex use `--agent codex`, and for Grok use `--agent grok`. With `--scope user` the skill lands in `~/.claude/skills/startup-eval/` (Claude Code), `~/.agents/skills/startup-eval/` (Codex) or `~/.grok/skills/startup-eval/` (Grok). Leave out `--scope user` to install it into the current project instead. `gh skill install --help` lists every supported agent. `gh skill` is in preview, so its commands and flags may change.

Without the GitHub CLI, clone the repository and copy the skill folder into your agent's skills directory (Claude Code shown):

```sh
git clone https://github.com/heydavidf/startup-eval.git
mkdir -p ~/.claude/skills
cp -R startup-eval/skills/startup-eval ~/.claude/skills/
```

Keep the folder name `startup-eval`; it must match the `name` in `SKILL.md`. If your agent does not load skills automatically, ask it to read `SKILL.md` in the installed folder and follow its relative references.

**Installed the first version?** It kept the skill at the repository root. If you copied the whole repository folder into your skills directory, replace that copy with the `skills/startup-eval` folder, or reinstall with the command above. Your evaluation library lives elsewhere and is not affected.

You can also hand the job to your agent:

> Install the startup-eval skill from https://github.com/heydavidf/startup-eval by following the Install section of its README. Then check that I have Python 3.11 or later and Poppler, and tell me what is missing.

### What you need

An agent that can run subagents in parallel, browse the public web, run Python 3.11 or later, and write local files. PDF intake uses Poppler's `pdfinfo`, `pdftotext`, and `pdftoppm` (`brew install poppler` on macOS, `apt install poppler-utils` on Debian and Ubuntu). There are no API keys, paid services, Python packages, or build steps. Your agent host may have its own usage costs; an adaptive run dispatches around ten subagents.

## Use it

Give the agent a deck and, if you want, a library location. For example:

> Use startup-eval on `~/Decks/northwind-pitch.pdf`. Keep the evaluation library at `~/Startup Evals`. Run in adaptive mode and open the dashboard when you are done.

The library defaults to `./startup-evals` in the working directory, or to the `STARTUP_EVAL_ROOT` environment variable if set. Each run lands in `Evaluations/<Startup> - <date>/` with `report.md`, `claim-register.md`, `evidence-register.md`, `run-manifest.json`, `dashboard.html`, and a `working/` folder holding every agent return. After validation passes, the agent appends the run to `INDEX.md` and `CALIBRATION_LOG.md`.

Decks are confidential by default. The skill instructs the agent to use the public web only to verify claims, never to upload deck content to external services. Check that your agent host honours that before using it on material you cannot share. If your agent works inside a Git repository, keep the library outside it or add `startup-evals/` to that repository's `.gitignore`, so a deck is never committed by accident. This repository already ignores it.

## See the output first

The [fictional Tidewell example](examples/fictional-tidewell/README.md) is a complete run directory for an invented company. In a clone of this repository, open `examples/fictional-tidewell/dashboard.html` in a browser. Simple view shows the verdict, score, market table, scenarios, and risks; Advanced (button or the `A` key) expands the full claim register, the evidence register, the score rationales, and a run summary with the number of agents dispatched and failures recorded. It is **synthetic**: no real company, market, or source is described.

To exercise the scripts offline against a scratch library, run this from the root of a clone:

```sh
export STARTUP_EVAL_ROOT="$(mktemp -d)/startup-evals"
python3 skills/startup-eval/scripts/init_library.py
python3 skills/startup-eval/scripts/create_run.py --startup Tidewell --source examples/fictional-tidewell/working/inputs/tidewell-pitch-deck.pdf
```

The second command prints the new run directory. Run folder names contain spaces, so keep the quotes below. Render pages with `python3 skills/startup-eval/scripts/prepare_pdf.py "<pdf-in-Inbox>" "<run_dir>"`, copy the example's `run-manifest.json`, `source-brief.md`, `report.md`, `claim-register.md` and `evidence-register.md` into the run directory, and finish with:

```sh
python3 skills/startup-eval/scripts/render_dashboard.py "<run_dir>/run-manifest.json"
python3 skills/startup-eval/scripts/validate_evaluation.py "<run_dir>"
python3 skills/startup-eval/scripts/update_registry.py "<run_dir>"
```

`validate_evaluation.py` lists every problem it finds; `update_registry.py` refuses to register a run that fails validation. A real evaluation produces the manifest and Markdown through the agent workflow in `SKILL.md`, not by copying.

## How it works

1. The agent copies the deck into `Inbox/`, creates a collision-safe run directory, and renders every page.
2. It writes a source brief and a claim register, then selects up to twelve load-bearing claims for formal verification.
3. Four specialist lenses run in parallel: market rebuild, bottom-up and valuation, comparables, and technical/moat. Then fresh skeptic agents verify the selected claims without seeing the specialists' conclusions. Adaptive mode escalates up to four contested high-impact claims to single-claim agents.
4. The agent reconciles evidence by fixed rules (primary beats secondary; no confirmation without independent corroboration; disagreement resolves to `uncertain`), writes the canonical manifest, and renders the dashboard.
5. A validator checks the manifest, scores, enums, citations, and dashboard before the run can be registered.

The method, agent contracts, and artifact formats are in [skills/startup-eval/references/](skills/startup-eval/references/).

## Limits and maintenance

This is a diligence procedure, not a source of market facts or investment advice. Verdicts depend on what the agent can find on the public web on the day; paywalls, private companies, and missing data produce `uncertain` and `unverified` results by design. Scores are a structured opinion, not a prediction. Calibrate the skeptics over several runs before trusting the refute rate.

Tested on macOS with Python 3.14.5 and Poppler 26.02.0; the scripts use only the standard library and should run on Linux. `gh skill install` was tested with gh 2.100.0 for the Claude Code, Codex and Grok folders. Live multi-agent runs were exercised with Claude Code; other agent hosts can read the Markdown but have not been tested.

To update a copy installed with `gh skill`, run `gh skill update startup-eval`; for a manual copy, replace the installed folder with a newer `skills/startup-eval`. Your evaluation library lives elsewhere and is untouched. To uninstall, remove the installed folder; the library remains.

Report defects through the repository's issue tracker. Never attach a real pitch deck or a run folder: they contain confidential deck text. Report security problems privately as described in [SECURITY.md](SECURITY.md). Contributions: [CONTRIBUTING.md](CONTRIBUTING.md).

**License:** [MIT](LICENSE).

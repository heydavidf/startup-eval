# Startup Eval contributor guide

This repository publishes one agent skill. The skill is the `skills/startup-eval/` folder, and `skills/startup-eval/SKILL.md` is its operational entry point. `gh skill install` copies only that folder, so everything the skill needs at runtime must live inside it. The README owns installation and public capability claims.

Inside `skills/startup-eval/` (installed with the skill):

- `references/methodology.md`: principles, claim register rules, research lenses, verdict definitions, scorecard bands.
- `references/orchestration.md`: specialist, skeptic, escalation, and synthesis waves; agent return contracts.
- `references/artifact-contract.md`: run directory layout, manifest schema, prose artifacts, dashboard behaviour.
- `scripts/`: standard-library Python helpers. `validate_evaluation.py` is the authority on what a valid run looks like; `update_registry.py` imports it and refuses invalid runs. `render_dashboard.py` fills `assets/dashboard.html.tmpl`.
- `agents/openai.yaml`: optional host interface metadata.
- `LICENSE`: a copy of the root `LICENSE`, so installed copies carry the licence. Keep the two identical.

At the repository root (not installed):

- `examples/fictional-tidewell/`: a complete synthetic run. `build_example.py` regenerates its PDF and dashboard deterministically.

## Checks

Run from the repository root. Python 3.11+ and Poppler are the only requirements.

```sh
python3 examples/fictional-tidewell/build_example.py
git status --short -- examples/   # a rebuild must leave the committed example unchanged
python3 skills/startup-eval/scripts/validate_evaluation.py examples/fictional-tidewell
```

Then run the scratch-library sequence in the README (`init_library`, `create_run`, `prepare_pdf`, `render_dashboard`, `validate_evaluation`, `update_registry`) and confirm the run appears in the scratch `INDEX.md` and `CALIBRATION_LOG.md`.

For skill-format checks use the official Agent Skills validator in a disposable environment:

```sh
python3 -m venv "${TMPDIR:-/tmp}/startup-eval-validator"
"${TMPDIR:-/tmp}/startup-eval-validator/bin/python" -m pip install 'skills-ref @ git+https://github.com/agentskills/agentskills.git@69ef37e9424c0a7ea9dd2293b559e43ec8176379#subdirectory=skills-ref'
"${TMPDIR:-/tmp}/startup-eval-validator/bin/skills-ref" validate skills/startup-eval
```

With GitHub CLI 2.100 or later, `gh skill publish --dry-run .` checks that `gh skill` can discover and validate the skill. Use it only with `--dry-run`: without it the command publishes a GitHub release.

## Change constraints

- Keep the manifest schema, validator, dashboard template, and `skills/startup-eval/references/artifact-contract.md` in step. If you add a manifest field, update the contract and the validator together and rebuild the example.
- Scores map to bands deterministically (`validate_evaluation.py:band`). Do not change thresholds without a methodology version bump.
- Never drop a claim: unverified and not-selected claims must stay in the manifest and the register.
- The dashboard must stay self-contained with no network resources, and must keep the `bSimple`/`bAdv` buttons and the `A` shortcut that the validator checks for.
- Everything the skill needs at runtime stays inside `skills/startup-eval/`. Links in its Markdown must not point outside that folder, because installed copies contain nothing else.
- No absolute paths, personal names, or real-company data in the package. Example content stays fictional with `example.com` sources. Never commit a real deck or a run folder.

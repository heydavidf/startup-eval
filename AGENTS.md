# Startup Eval contributor guide

This repository is a standalone agent skill. `SKILL.md` is the operational entry point; the README owns installation and public capability claims.

- `references/methodology.md`: principles, claim register rules, research lenses, verdict definitions, scorecard bands.
- `references/orchestration.md`: specialist, skeptic, escalation, and synthesis waves; agent return contracts.
- `references/artifact-contract.md`: run directory layout, manifest schema, prose artifacts, dashboard behaviour.
- `scripts/`: standard-library Python helpers. `validate_evaluation.py` is the authority on what a valid run looks like; `update_registry.py` imports it and refuses invalid runs. `render_dashboard.py` fills `assets/dashboard.html.tmpl`.
- `examples/fictional-tidewell/`: a complete synthetic run. `build_example.py` regenerates its PDF and dashboard deterministically.
- `agents/openai.yaml`: optional host interface metadata.

## Checks

Run from the repository root. Python 3.11+ and Poppler are the only requirements.

```sh
python3 -m py_compile scripts/*.py examples/fictional-tidewell/build_example.py
python3 examples/fictional-tidewell/build_example.py
git status --short examples/   # a rebuild must leave the committed example unchanged
python3 scripts/validate_evaluation.py examples/fictional-tidewell
```

Then run the scratch-library sequence in the README (`init_library`, `create_run`, `prepare_pdf`, `render_dashboard`, `validate_evaluation`, `update_registry`) and confirm the run appears in the scratch `INDEX.md` and `CALIBRATION_LOG.md`.

For skill-format checks use the official Agent Skills validator in a disposable environment:

```sh
python3 -m venv /tmp/startup-eval-validator
/tmp/startup-eval-validator/bin/python -m pip install 'skills-ref @ git+https://github.com/agentskills/agentskills.git@69ef37e9424c0a7ea9dd2293b559e43ec8176379#subdirectory=skills-ref'
/tmp/startup-eval-validator/bin/skills-ref validate "$PWD"
```

## Change constraints

- Keep the manifest schema, validator, dashboard template, and `references/artifact-contract.md` in step. If you add a manifest field, update the contract and the validator together and rebuild the example.
- Scores map to bands deterministically (`validate_evaluation.py:band`). Do not change thresholds without a methodology version bump.
- Never drop a claim: unverified and not-selected claims must stay in the manifest and the register.
- The dashboard must stay self-contained with no network resources, and must keep the `bSimple`/`bAdv` buttons and the `A` shortcut that the validator checks for.
- No absolute paths, personal names, or real-company data in the package. Example content stays fictional with `example.com` sources.

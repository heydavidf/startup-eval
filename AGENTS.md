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
- `tests/`: standard-library `unittest` tests. `test_layout.py` guards the `skills/<name>/` layout that `gh skill` needs; `test_scripts.py` compiles every Python file and runs the offline script pipeline from a temporary copy of the skill folder.
- `.github/workflows/ci.yml`: runs the checks below on every push to `main`, on pull requests and weekly. `.github/tripwire.sh` catches personal paths, junk files, evaluation-library content and silenced checks. `.github/dependabot.yml` keeps the pinned actions current.
- `README.md` (users), `CHANGELOG.md` (one entry per release), `CONTRIBUTING.md`, `SECURITY.md`, `LICENSE`.

## Checks

Run from the repository root. You need Python 3.11+, Git and Poppler; ruff and the skill validator run in throwaway environments. CI runs the same commands plus gitleaks (secrets) and lychee (links).

```sh
python3 -B -m unittest discover -s tests -v
python3 examples/fictional-tidewell/build_example.py
git status --short -- examples/   # must print nothing: a rebuild leaves the committed example unchanged
python3 skills/startup-eval/scripts/validate_evaluation.py examples/fictional-tidewell
bash .github/tripwire.sh origin/main   # compare against the branch you will merge into
pipx run --spec ruff==0.17.1 ruff check .
pipx run --spec ruff==0.17.1 ruff format --check .
```

The tests already run the README's scratch-library sequence (`init_library`, `create_run`, `prepare_pdf`, `render_dashboard`, `validate_evaluation`, `update_registry`) against a temporary library and check `INDEX.md` and `CALIBRATION_LOG.md`.

For skill-format checks use the official Agent Skills validator in a disposable environment:

```sh
python3 -m venv "${TMPDIR:-/tmp}/startup-eval-validator"
"${TMPDIR:-/tmp}/startup-eval-validator/bin/python" -m pip install 'skills-ref @ git+https://github.com/agentskills/agentskills.git@69ef37e9424c0a7ea9dd2293b559e43ec8176379#subdirectory=skills-ref'
"${TMPDIR:-/tmp}/startup-eval-validator/bin/skills-ref" validate skills/startup-eval
```

With GitHub CLI 2.100 or later, `gh skill publish --dry-run .` checks that `gh skill` can discover and validate the skill. Use it only with `--dry-run`: without it the command publishes a GitHub release.

## Working rules

1. A bug fix ships with a committed test in `tests/` that fails on the old code and passes on the new. A one-off check in a temporary folder does not count.
2. Run every check above before saying a change is done, and quote the output.
3. Do not silence a check to get green: no `noqa` comments, skipped tests or disabled rules. The tripwire fails the build unless the line says `tripwire-allow` with a reason.
4. Stop any server you started. Leave no stray files (caches, scratch libraries, databases) in the repository folder: point `STARTUP_EVAL_ROOT` at a temporary folder outside the clone when you run the scripts by hand.
5. For non-trivial changes, a different agent writes an independent scenario test before the change is accepted.

## Change constraints

- Keep the manifest schema, validator, dashboard template, and `skills/startup-eval/references/artifact-contract.md` in step. If you add a manifest field, update the contract and the validator together and rebuild the example.
- Scores map to bands deterministically (`validate_evaluation.py:band`). Do not change thresholds without a methodology version bump.
- Never drop a claim: unverified and not-selected claims must stay in the manifest and the register.
- The dashboard must stay self-contained with no network resources, and must keep the `bSimple`/`bAdv` buttons and the `A` shortcut that the validator checks for.
- Everything the skill needs at runtime stays inside `skills/startup-eval/`. Links in its Markdown must not point outside that folder, because installed copies contain nothing else (`tests/test_layout.py` enforces this).
- No absolute paths, personal names, or real-company data in the package. Example content stays fictional with `example.com` sources. Never commit a real deck or a run folder.
- Record every user-visible change in `CHANGELOG.md`.

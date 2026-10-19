# Changelog

Notable changes to this project. Versions follow [Semantic Versioning](https://semver.org/); each release is a Git tag and a GitHub Release.

## 1.0.0 (unreleased, proposed)

The first tagged release. The skill's method, scripts and output formats are unchanged; this release changes where the skill lives so the GitHub CLI can install it, and adds automatic checks.

### Changed

- The skill moved from the repository root into `skills/startup-eval/`, so `gh skill install heydavidf/startup-eval startup-eval` now finds it. If you copied the whole repository folder into your skills directory, replace that copy with the `skills/startup-eval` folder or reinstall with `gh skill install`. Your evaluation library is not affected.
- The README's install section leads with `gh skill install` for Claude Code, Codex and Grok, keeps a manual copy route, and states the Python 3.11 minimum.
- `SKILL.md` links to the worked example on GitHub, because installed copies contain only the skill folder.
- Python helpers are formatted with ruff. The code they run is unchanged.

### Added

- A copy of the licence inside the skill folder, so installed copies carry it.
- `.gitignore` entry for `startup-evals/`, the default evaluation library, so a deck is not committed by accident when the scripts run inside a clone.
- Automatic checks on every push, pull request and week (`.github/workflows/ci.yml`): ruff, tests (on Python 3.14 and 3.11), example rebuild, validator, Agent Skills spec, a tripwire for personal paths, committed decks and silenced checks, secret scanning and link checking.
- Tests that guard the `skills/` layout, run the offline script pipeline from a copy of the skill folder, and exercise the tripwire.
- `SECURITY.md`, `CONTRIBUTING.md`, Dependabot updates for the pinned actions, and working rules for coding agents in `AGENTS.md`.

## First public version (2026-10-12)

Published without a version tag. The skill sat at the repository root and was installed by copying the folder.

- Multi-agent pitch-deck diligence: claim register, specialist and skeptic waves, evidence reconciliation, five-dimension scorecard, self-contained dashboard.
- Standard-library helper scripts for the library, run folders, PDF intake, dashboard rendering, validation and registry updates.
- A fictional worked example (`examples/fictional-tidewell/`) that rebuilds byte-for-byte.

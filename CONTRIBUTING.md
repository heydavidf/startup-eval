# Contributing

Thanks for your interest. This is a small project maintained by one person, so issues and small pull requests are the most helpful.

## Never attach real pitch decks

Do not attach a real pitch deck, a run folder, or text copied from one to an issue or pull request. They contain confidential deck content, and anything posted here is public. Show the problem with the fictional example in `examples/fictional-tidewell/` or with invented data. Report security problems privately as described in [SECURITY.md](SECURITY.md).

## Before you open a pull request

1. Open an issue first for anything larger than a small fix, so we can agree on the approach.
2. Run the checks listed in [AGENTS.md](AGENTS.md) (the same commands CI runs in `.github/workflows/ci.yml`). They must pass. You need Python 3.11 or later, Git, Poppler and pipx (for ruff).
3. A bug fix should come with a test in `tests/` that fails before the fix and passes after it.
4. Keep the change focused: one problem per pull request.
5. Keep everything the skill needs at runtime inside `skills/startup-eval/`, and keep the example fictional.

## Using coding agents

Agent-written changes are welcome. Please read the diff yourself before submitting, and say in the pull request which agent you used.

## Licence

By contributing you agree that your contribution is licensed under the same licence as the project (see [LICENSE](LICENSE)).

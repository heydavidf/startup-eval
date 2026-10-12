# Multi-Agent Orchestration

The main agent orchestrates directly. Do not spawn an agent whose job is to spawn other agents. Keep no more than three subagents active at once.

## Shared context contract

Before dispatch, write `source-brief.md` and a draft claim register. Every specialist receives:

- exact paths to source material
- `source-brief.md`
- the complete claim register
- its role and output path
- instruction to use current public web research and human-readable citations
- instruction not to modify files outside its assigned output

Agents write only their assigned `working/*.md` output. The main agent reads and reconciles results.

## Specialist wave

Spawn `market-rebuild`, `bottom-up-valuation`, and `comparables` in parallel. When one slot frees, spawn `technical-moat`. If a lens is genuinely inapplicable, reinterpret it for the business rather than skipping it; for example, replace patent analysis with workflow switching costs and marketplace liquidity.

Each lens must return:

1. Findings with explicit arithmetic where relevant
2. Evidence table with title, URL, publication/update date, access date, source quality, and supported claim IDs
3. Claim-level implications
4. Unknowns and source conflicts
5. A short lens verdict

Retry a missing or malformed output once. Preserve both the failure and retry in the run manifest.

## Skeptic wave

Do not show skeptics the specialist conclusions. Give them the source brief, complete claim register, and only their assigned claim IDs.

### Balanced

Spawn three fresh skeptics in parallel. Partition the selected formal claims round-robin so every selected claim has exactly one initial skeptic.

### Adaptive

Run the balanced wave, then rank escalation candidates by investment impact. Escalate at most four claims when any condition holds:

- high-impact claim has an `uncertain` initial verdict
- high-impact claim has `low` or `none` evidence strength
- initial skeptic conflicts with the relevant specialist
- public sources conflict and the outcome could change valuation or verdict band

Use one fresh agent per escalated claim, in waves of three. Reconcile as follows:

1. Current primary evidence outranks secondary evidence.
2. A claim cannot be confirmed without independent corroboration.
3. If equivalent-quality evidence or agents disagree, resolve to `uncertain` and explain the conflict.
4. A mathematical or deck-internal contradiction may be refuted from the deck itself.

### Deep

Spawn one fresh skeptic for every selected formal claim, up to 12, in waves of three. Do not batch claims.

## Skeptic return contract

Return for each assigned claim:

- claim ID
- `verification_status`: `complete` or `unverified`
- verdict or null
- evidence strength
- issue tags
- defensible reality
- concise reasoning
- citations with URLs and dates, plus deck page citations
- searches attempted when evidence is unavailable

Retry once on missing claims, invalid enums, or absent citations. After a second failure, record the claim as unverified rather than dropping it.

## Synthesis wave

After reconciliation, spawn one fresh `synthesis` agent with all completed lens outputs, final claim verdicts, and the score rules. Ask for a draft report and scorecard. The main agent then:

- recomputes the average and verdict band
- checks every selected claim is present
- checks cited URLs are human-readable
- separates legacy/deck statements from verified facts
- writes the canonical manifest and final artifacts

Record all dispatched agents, retries, failures, modes, and output paths in `run-manifest.json`.

# Evaluation Methodology

## Principles

- Treat the deck as a source of claims, not evidence that those claims are true.
- Separate TAM (whole category), SAM (serviceable segment), and SOM (realistically obtainable in 3-5 years).
- Rebuild important denominators from current public sources. Do not stack unrelated category TAMs.
- For pre-revenue companies, reverse-engineer the customers, price, conversion, sales capacity, capital, and time required to hit targets.
- Use comparable-company outcomes as revealed preference: funding, headcount, revenue, pivots, shutdowns, and time-to-scale matter more than headline valuations.
- Distinguish a genuine tailwind from company-specific differentiation.
- Prefer primary sources, current filings, standards bodies, government publications, company pricing, and audited results. Use secondary reporting when primary data is unavailable and label it.
- Do not use missing evidence alone as contradiction. Mark plausible but uncorroborated claims `uncertain`; use `refuted` for contradiction, invalid arithmetic, category/denominator errors, or materially misleading framing.

## Intake and claim register

Capture every material numeric, market, traction, pricing, unit-economic, technical, competitive, timing, moat, team, and deal claim. Give each claim:

- stable ID (`C1`, `C2`, ...)
- exact or faithful deck wording
- stated value
- deck page(s)
- type
- investment impact: `high`, `medium`, or `low`
- whether formally selected for verification

Select at most 12 formal claims by impact, dependency, and coverage across claim types. Keep all remaining claims in the register as `not_selected`; never omit them.

## Research lenses

### Market rebuild

Audit the denominator behind each headline market figure. Define the actual buyer, geography, segment, spend category, and time horizon. Produce stated TAM vs rebuilt TAM/SAM vs defensible 3-5 year SOM, with arithmetic and sources.

### Bottom-up and valuation

Translate targets into required customers, units, ACV, conversion, sales capacity, payback, capital, and calendar time. Test internal consistency. Benchmark stage and valuation against relevant current financing data. Give a defensible range rather than false precision.

### Comparables

Find the closest funded or scaled peers and report what happened: funding, revenue, headcount, customer traction, pivots, failures, and time-to-scale. Explain why each is or is not comparable.

### Technical, product, moat, and regulation

Test whether claimed novelty is technically meaningful and defensible. For regulated or deep-tech products, distinguish standards compliance, certification, validation, patents pending, issued rights, and production readiness. For ordinary software, focus on product substitution, switching costs, distribution, data advantages, and incumbent responses.

## Verdicts

- `confirmed`: independent evidence positively supports the material claim.
- `uncertain`: plausible, mixed, unverifiable, source-conflicted, or dependent on future execution.
- `refuted`: contradicted, arithmetically invalid, a denominator/category error, outdated in a material way, or materially misleading.

Record `evidence_strength` as `high`, `medium`, `low`, or `none`. Record one or more issue tags from: `unsupported`, `contradicted`, `denominator-error`, `category-error`, `arithmetic-error`, `misleading-framing`, `outdated`, `none`.

Every completed verdict must cite a deck page, external source, or both. An exhausted verification failure uses `verification_status: unverified` and a null verdict.

## Scorecard

Score each dimension 0-10:

1. TAM Credibility
2. SOM Feasibility
3. Unit Economics / Feasibility
4. Market Timing
5. Assumption & Risk Transparency

Overall score is the arithmetic mean rounded to one decimal. Map deterministically:

- `Invest-grade`: 7.0-10.0
- `Credible-with-gaps`: 5.0-6.9
- `Caution`: 3.0-4.9
- `Pass`: 0.0-2.9

Refute rate is `refuted / completed formal verdicts`. Do not include unverified claims in the denominator; report their count separately.

## Required synthesis

Produce: plain-language startup summary; investment verdict; market-sizing table; bottom-up reality test; valuation view when relevant; comparable outcomes; scenarios; scorecard; ranked risks; what would make the company investable; triangulation note; and sources. Quantify, distinguish facts from inference, and state the strongest bull case as well as the decisive breakpoints.

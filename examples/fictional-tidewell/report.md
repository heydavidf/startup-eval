# Tidewell: startup evaluation (fictional example)

| | |
|---|---|
| Date | 2026-10-12 |
| Stage | Pre-seed |
| Mode | adaptive |
| Source | Tidewell pitch deck, 3 pages (synthetic, see `build_example.py`) |
| Score | 4.8 / 10, Caution |

This is a worked example with invented data. It exists to show the shape of a finished run, not to describe any real company.

## Startup summary

Tidewell sells a subscription tide and mooring alert service to small-harbour boat owners. The product depends on harbours that publish live sensor feeds. The deck asks for 600,000 at a 6,000,000 post-money valuation.

## Verdict

The deck's market figure counts every registered leisure boat in the region as a customer, while the product only serves owners with a monitored mooring. Rebuilt from the deck's own assumptions, the serviceable market supports the conservative scenario but not the stated year-three revenue. The pricing claim holds up, the team claim could not be verified, and the growth claims do not hold.

## Market sizing

| Segment | Deck | Independent rebuild | Serviceable |
|---|---|---|---|
| TAM | 48M per year (400,000 boats x 120) | 9M per year (75,000 moored boats in sensor harbours x 120) | About 3M per year in the first twelve harbours |
| SOM (3-5 years) | 9.6M (20 percent of stated TAM) | 1.0M to 1.8M (8,000 to 15,000 subscribers) | Depends on harbour sensor rollout pace |

## Bottom-up reality test

9.6M of year-three revenue at 120 per subscriber needs 80,000 subscribers. The rebuilt serviceable market is about 75,000 boats in total, so the plan requires more than 100 percent penetration. The conservative and base scenarios below use 10 to 15 percent of moored boats across twelve to twenty harbours.

## Comparables

The fictional comparables lens found two invented peers: one that reached 11,000 subscribers in four years with a similar harbour-partnership model, and one that shut down after harbour authorities changed sensor-access terms. Both point to rollout pace and access fees as the deciding variables.

## Technical and moat findings

The product is ordinary software over third-party sensor feeds. Switching costs are low. The defensible position would come from exclusive or early harbour agreements, which the deck mentions but does not document.

## Scenarios

| Scenario | Outcome | Basis |
|---|---|---|
| Conservative | 1.0M revenue; 8,000 subscribers | Twelve harbours, 10 percent of moored boats, 120 per year |
| Base | 1.8M revenue; 15,000 subscribers | Twenty harbours, 15 percent of moored boats |
| Deck | 9.6M revenue; 80,000 subscribers | Exceeds the rebuilt serviceable market |

## Scorecard

| Dimension | Score | Rationale |
|---|---:|---|
| TAM Credibility | 3 | Denominator counts boats the product cannot serve |
| SOM Feasibility | 4 | Year-three share assumes an uncosted harbour rollout |
| Unit Economics / Feasibility | 6 | 120 price against 31 cost works if churn holds at 15 percent |
| Market Timing | 6 | Harbour sensor funding is real in the fiction; no forcing deadline |
| Assumption & Risk Transparency | 5 | Pricing shown; denominator and sales capacity not |

Overall: 4.8, Caution.

## Top risks

1. Market denominator counts boats the product cannot serve.
2. Harbour sensor rollout is outside the company's control and uncosted.
3. Subscriber count mixes trial and paid users.
4. Sensor-access fees are undisclosed and could erase the stated margin.

## What would make this investable

Restate the market as moored boats in sensor-equipped harbours, show paid versus trial subscribers with churn, disclose sensor-access terms, and tie the revenue plan to a dated harbour rollout schedule.

## Triangulation

Four specialist lenses, three batched skeptics, one escalation on C5, and one synthesis agent. One skeptic failed twice, so C6 is recorded as unverified rather than dropped. See `run-manifest.json` for the agent and failure log.

## Sources

See `evidence-register.md`. All URLs are reserved example.com placeholders.

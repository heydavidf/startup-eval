# Security policy

## Reporting a vulnerability

Please report security problems privately through GitHub: open the repository's **Security** tab and choose **Report a vulnerability**. Do not open a public issue.

Never include a real pitch deck, a run folder, or text copied from one in a report. Run folders contain confidential deck content. Reproduce the problem with the fictional example in `examples/fictional-tidewell/` or with invented data instead.

I maintain this project on my own, so I aim to acknowledge reports within 7 days and to fix confirmed problems as soon as I reasonably can. I will credit you in the fix unless you ask me not to.

## What counts

Examples of problems worth reporting privately:

- The skill's instructions or scripts could send deck content to an external service, or put it somewhere it could be committed or published.
- Data in a run manifest can inject script or harmful links into the generated `dashboard.html`.
- A script writes outside the evaluation library or the run folder it was given.
- Instructions in the skill make it easy for text on a web page (prompt injection) to steer the agent away from its rules.

Wrong verdicts, scoring disagreements and other diligence-quality issues are ordinary bugs: please open a normal issue for those, without real deck content.

## Supported versions

Only the latest release, and the latest commit on `main`, are supported.

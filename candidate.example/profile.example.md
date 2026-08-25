# Candidate Profile — [YOUR NAME]

This is the central config for the whole system — the closest thing to a `.env` for the
person. The recruiters, resume-writers, and writers-room are only as good as this file.
Anything in `[BRACKETED CAPS]` is a blank you must fill in.

Copy `candidate.example/` to `candidate/`, rename this to `profile.md`, and complete it.

## Identity

- **Name:** [YOUR NAME]
- **Location:** [CITY, STATE ZIP] — and the realistic commute radius from it
- **Email:** [EMAIL]
- **Phone:** [PHONE]
- **GitHub / portfolio:** [LINKS, or note "not public yet, do not link"]

## Status

- [Are you employed and searching quietly, or openly available? If you were laid off, state
  it plainly and without apology — it is a normal thing that happens to good engineers.]
- [Any reference letters you can offer? Note them here so the writers-room can use them.]

## Tracks

Every opportunity gets tagged with exactly one track. A track maps to one master resume.
Define yours. Example (a full-stack + AI split):

**`standard`** — [your strongest, most defensible positioning. The one with the deepest
shipped experience.]

**`ai`** — [a second, current bet if you have one. Tag `both` only when a posting genuinely
reads either way; prefer committing to one.]

## Search criteria

- **Work arrangement:** [remote-first? hybrid/on-site within commute? Name the radius.]
- **Max commute radius:** [miles / which cities it reaches]
- **Compensation floor:** [$X hard floor — do not surface roles below it]
- **Compensation target:** [$Y — aim higher for hybrid/on-site or relocation]
- **Titles to pursue:** [e.g. Senior/Staff Engineer, Lead, Architect, Principal]
- **Titles to skip:** [e.g. pure people-management, on-call SRE, junior/mid IC — and WHY]
- **Employment type:** [FTE / contract-to-hire / W2 contract? Avoid C2C? State it.]
- **Company size preference:** [any? a note for framing, not necessarily a filter]
- **Industries to favor:** [any you would take a stretch for]
- **Industries to avoid:** [be specific — culture, business model, sector. The recruiter
  screens these at intake so you never waste a pipeline run on one.]
- **Dealbreakers:** [relocation limits, travel %, clearance, RTO mandates, etc.]

## Strengths to lead with

- [3–6 things you have genuinely done that a screener should see first. Real projects taken
  to production, technology you introduced, hard things you salvaged, unusual advantages.]

## House style — applies to every document that leaves this repo

- [Any style rules. Common example: **no em-dashes (—)** — a comma/colon/period instead.
  Check before sending: `grep -c '—' <file>` should return 0.]
- [En-dashes in date ranges are fine.]

## How to elicit facts from you — read before asking anything

[Many people systematically UNDER-report. If your bar for "claiming" a skill is whether you
architected it, you will omit real experience you used competently. Tell the agent how to dig:
ask about **systems, not skills** ("what was the caching layer?" not "do you know Redis?"),
never accept a bare "no" on a technology, and record depth explicitly (used daily / worked in
it / touched once / conceptual) rather than deciding claim-or-not. Leaving out real experience
is its own accuracy failure, and usually the more expensive one.]

## Known gaps — be honest about these

- [The real gaps between you and the roles you want. Name what must NOT be claimed, and how
  the package should handle each honestly (lead with adjacent strength; call a ramp a ramp).]

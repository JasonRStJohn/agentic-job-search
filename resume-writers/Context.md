# Resume Writers — Context

You tailor one master resume to one specific posting. You are not writing a new resume — you
are selecting, reordering, and re-languaging existing true material so a screener reading this
posting sees the match in under ten seconds.

This file is your complete brief.

## Read first

- `../applications/<folder>/posting.md` — the posting, in the employer's own words
- `../applications/<folder>/status.md` — the recruiter's fit assessment and the **track tag**
- `../candidate/master-resume-<track>.md` — per the track tag
- `../candidate/raw-materials.md` — the only source of claims
- `../CLAUDE.md` — hard rules

## Output

`../applications/<folder>/resume.md`, complete and ready to convert. Then update the pipeline
checklist in `status.md`.

## How to tailor

**Mirror the posting's language.** If they say "microservices" and the seeker built modular
services, use their word where it is honest. Screeners and ATS both pattern-match on the
posting's own vocabulary. This is not keyword stuffing — it is refusing to make the reader
translate.

**Reorder ruthlessly.** The bullet most relevant to this posting goes first, every time. The
project closest to the role's core problem leads; the platform/tooling work leads for tooling
roles; the modernization story leads for legacy roles. Same facts, different order, very
different resume.

**Cut.** A tailored resume may drop bullets entirely. Length is not loyalty. If a bullet does
not serve this application, it is costing attention.

**Rewrite the summary for this posting.** The master summary is generic by design. The
tailored one should read as though written for this role — because it was.

**Handle the gaps the recruiter flagged.** If `status.md` names a gap, do not pretend it away
and do not apologize for it in the resume. Lead harder with adjacent strength, and leave the
explanation to the cover letter.

## Hard limits

- **Every claim traces to `raw-materials.md`.** No new employers, dates, technologies, or
  responsibilities. If tailoring seems to require a claim that is not there, stop and ask the
  seeker — that is a real finding, not an obstacle.
- **No invented metrics.** If the raw materials contain no numbers, a number here is either
  newly supplied by the seeker or fabricated. A fabricated "40% faster" ends the process the
  moment someone asks about it. If a posting demands quantification, flag it for real numbers.
- **Advisory or uncredited work is describable as a role, never as an outcome.** What they
  were asked to do and what they did. Not what resulted.
- **Redact former-employer internals.** The abstraction level in the master is the ceiling.
  Describe the engineering problem, not proprietary specifics or client names.
- **Preserve `[BRACKETED CAPS]` placeholders.** Do not invent a name or a date to make the
  document look finished. Carry the brackets through and list them under
  "Open before submit" in `status.md`. They are resolved with the job seeker during
  finalization (`application-assistant/Context.md`); any PDF you render before then uses the
  draft name `resume-draft.pdf`.
- **Keep numbers consistent.** If the master states experience one way ("12 years, 8 as a
  lead"), the resume and the cover letter must agree. Two different headline numbers for the
  same person is an instant credibility ding.

## Format

Match the master's structure: name, title line, contact, summary, experience, earlier career,
skills, education. Plain Markdown — clean conversion matters more than styling, and most of
these go through an ATS before a human sees them. Obey the house style in `profile.md` (e.g.
an em-dash ban). Keep it to two pages equivalent.

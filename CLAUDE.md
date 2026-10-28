# CLAUDE.md

This file provides guidance to an AI agent (Claude Code, a local model, or a plain chat
window) working in this repository.

## What this is

Not a codebase. This is a **recruiting department run on behalf of one job seeker.** It runs
a structured, multi-stage workflow — find openings, tailor a resume, draft cover letters,
critique the package cold — as a set of cooperating agent roles, each briefed by a plain
Markdown file that sits next to the work it governs.

**This file is a router. The `Context.md` files are the actual instructions.**

> **This is a template.** Everything personal lives in a private, git-ignored `candidate/`
> layer that is NOT in this repo. To use it: copy `candidate.example/` to `candidate/` and
> fill it in (start with `candidate/profile.md` — it is the closest thing to a `.env` for the
> person). Copy `.env.example` to `.env` if you want the optional task-tracker integration.
> See `README.md`.

## Portability rule

Nothing essential lives in hidden or harness-specific files. Every brief is a visible
Markdown file, written so that *any* model can read it and do the job with no knowledge of a
specific tool's conventions. When you add capability, add it as a `Context.md` instruction
with a portable fallback. Tool-specific paths (a job-search MCP, web fetch, a task tracker)
are always described as *one option*, never the only one.

## Structure

```
CLAUDE.md              this file — org chart and routing
candidate/             GIT-IGNORED. The source of truth about the job seeker.
  profile.md             search criteria, comp, location, tracks, dealbreakers  (the "env")
  master-resume-*.md     one master resume per track
  raw-materials.md       project notes and career narrative — the only source of claims
candidate.example/     committed. Empty scaffolds; copy to candidate/ and fill in.
recruiters/            finds and qualifies openings        (Context.md)
  inbox/                 drop copy-pasted postings here
resume-writers/        tailors a master resume to one posting   (Context.md)
writers-room/          drafts cover letters, multiple angles    (Context.md)
hiring-staff/          critiques the finished package, cold     (Context.md)
application-assistant/ finalizes the package, helps fill the form (Context.md)
applications/          one folder per opportunity
  _index/log.md          GIT-IGNORED catalog: one row per opportunity, status, next action
  _templates/application/ the stamp: every new opportunity is a copy of this
  <YYYY-MM-DD>-<company>-<role>/   GIT-IGNORED real applications
tools/                 portable helper scripts (e.g. task-tracker sync)
```

## Routing

When work comes in, identify the department and point an agent at that department's
`Context.md`. Do not summarize the `Context.md` into the agent prompt — point the agent at
the file and let it read the whole thing.

| Request | Department | Brief |
|---|---|---|
| "find me jobs", a posting URL, a pasted posting | recruiters | `recruiters/Context.md` |
| "tailor my resume for X" | resume-writers | `resume-writers/Context.md` |
| "write a cover letter for X" | writers-room | `writers-room/Context.md` |
| "how does this package look", "is this ready" | hiring-staff | `hiring-staff/Context.md` |
| "make the PDFs", "is it ready to send", "finalize X" | application-assistant | `application-assistant/Context.md` |
| "I'm filling out the application", a pasted form question | application-assistant | `application-assistant/Context.md` |
| "where does the search stand" | (read directly) | `applications/_index/log.md` |
| "run the whole pipeline on X" | all five, in order | see below |

**New opportunity = copy `applications/_templates/application/`, then add a row to
`applications/_index/log.md`.** Keep the log's row current whenever a folder's stage changes.

**Push it to the task tracker when the job seeker processes it** (optional). If configured,
sync each processed opportunity to a task tracker so a task with the posting link and the
folder's files rides along:

```
python3 tools/vikunja_sync.py applications/<folder>
```

It self-configures from `.env` and **skips silently if unconfigured or unreachable** — the
pipeline never depends on it. This is one option; the pipeline is fully functional without it.

## Where candidate-specific tuning lives

**All candidate-specific tuning and adjustments live in the `candidate/` layer, never in a shared system file.** The search queries that surface your roles, the gaps to filter, channel notes, business-model screens, angle preferences: these belong in `candidate/profile.md`, `candidate/raw-materials.md`, or `candidate/search-tuning.md`, which the generic briefs read at runtime. Every `*/Context.md`, `CLAUDE.md`, `tools/` script, and template stays portable. If you catch yourself hard-coding a candidate-specific query, gap, employer, or preference into one of those, that is the signal to move it into `candidate/` instead. The `candidate/` layer is git-ignored, so keeping tuning there is also what keeps it out of the shared, shippable repo.

## The pipeline

```
recruiter → resume-writer → writers-room → hiring-staff → application-assistant
```

Each stage writes into the same `applications/<folder>/` and reads what the previous stage
produced. Full-pipeline runs go in order; each stage gets its own agent.

**Draft names until final.** Any PDF rendered before the application-assistant's finalize
checklist passes is named `resume-draft.pdf` / `cover-letter-draft.pdf`. Only a package with
no placeholders and no missing parts gets the final name (`<Prefix>_<Employer>_Resume.pdf`,
prefix from `candidate/profile.md`). A final name means "safe to send as-is." The
application-assistant usually runs inline with the job seeker rather than as a dispatched
agent, because finalizing means asking them questions.

**The hiring-staff stage must run in a fresh agent with no prior context.** Its whole value
is judging the package the way a stranger receiving it cold would. An agent that watched the
resume get written cannot do that. It also splits into two jobs — a cheap screener
simulation run after every revision, and an expensive source audit run once per package;
see `hiring-staff/Context.md`. Mechanical checks (format parity, em-dash count, number
consistency) are grep problems the orchestrator does inline, not agent work.

## Hard rules

These apply to every department. They exist because breaking them costs real opportunities.

1. **Never fabricate.** No invented metrics, employers, dates, technologies, or outcomes.
   Every claim must trace to `candidate/raw-materials.md` or something the job seeker has
   confirmed. If a posting wants something they lack, say so.
2. **No unprovable outcome claims.** Describe what the person *did*, in a role; let the
   reader draw conclusions. "Nobody got laid off because of my work" is unprovable and reads
   as credit-taking.
3. **Redact former-employer internals.** Naming an employer and describing systems at the
   level already in the master resumes is fine. Proprietary detail, client names, and
   internal data are not. When unsure, describe the engineering problem, not the specifics.
4. **Never name freelance/consulting clients** beyond what the master resumes already name.
5. **Flag placeholders loudly, then resolve them before finishing.** Anything unknown goes in
   as `[BRACKETED CAPS]` in a working draft and gets reported to the job seeker. Never quietly
   guess a fact about their life. **But a placeholder is a question, not a deliverable:**
   before rendering any final PDF or calling a package ready, ask the job seeker for every
   open placeholder (check the candidate files first, and ask only for what is genuinely
   missing), fill them in, and record the answers in `candidate/raw-materials.md` so they are
   never asked twice. A final PDF must never ship with a bracket in it.

## House style

Configurable per job seeker in `candidate/profile.md`. A common example: **no em-dashes**
(they read as an AI tell to some readers). Set the style there; every department obeys it.
Mechanical check before sending: `grep -c '—' <file>` should return 0 if em-dashes are banned.

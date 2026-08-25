# Applications — the catalog

One line per opportunity. This is the declared source of truth for **what exists and where it
stands**. To read the state of the whole search, read this file and nothing else. Detail
lives in each folder's `status.md`; this file only points and summarizes.

Copy this to `log.md` (which is git-ignored) and keep it current.

**Status vocabulary** (a small lifecycle, left to right):
`sourced` → `drafting` → `critiqued` → `ready` (passed critique, waiting on you) →
`submitted` → `responded` → `interviewing` → `closed`
Closed carries a reason: `closed:withdrawn`, `closed:rejected`, `closed:offer`,
`closed:no-response`.

**Keep it current.** Update the row the moment a folder's stage changes — a stale catalog is
worse than none. When the recruiter creates a new application folder (from
`_templates/application/`), add its row here in the same pass.

| Date | Company / Role | Track | Fit | Status | Next action |
|---|---|---|---|---|---|
| YYYY-MM-DD | [Example Co — Senior Engineer](../<folder>/status.md) | standard | Strong | `sourced` | One-line next action. |

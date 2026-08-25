# Application folder — the stamp

Every opportunity is a **copy of this folder**, not a blank page. Copying it is what keeps applications uniform, so the catalog (`_index/log.md`) can be trusted and a cold reader knows where everything is. The template *is* the schema: if the canonical shape changes, change it here, then re-stamp.

## How to instantiate

1. Copy this folder to `applications/<YYYY-MM-DD>-<company>-<role>/`. Date is the day it was sourced; keep the slug kebab-case.
2. Fill in `status.md` first (the header block and fit assessment). Everything else follows the pipeline.
3. Add a row to `applications/_index/log.md` in the same pass.

## The canonical file set

These five are the shape every folder holds. Do not rename them; a stable set is what lets someone find anything without a map.

| File | What it is | Source or generated |
|---|---|---|
| `status.md` | The folder's own state: header, fit, gaps, pipeline checklist. The one file a reader opens first. | **source** |
| `posting.md` | The job posting, captured. What the package is aimed at. | **source** |
| `resume.md` | The tailored resume, in Markdown. The editable master for this application. | **source** |
| `cover-letter.md` | The cover letter (may hold multiple angles until one is chosen). | **source** |
| `critique.md` | The hiring-staff critique, written cold. | **source** |

## Files that appear only when earned

Do not create these up front. They exist when the work reaches them:

- `interview-prep.md` — only once the application advances to a screen or interview.
- `critique-v2.md`, `screener-read.md` — iteration artifacts from extra critique rounds. If a folder never needed a second pass, it never has these.
- `source-drop-file.md` — a copy of the inbox drop file, when the lead came from one rather than a live search.
- `cover-letter-drafts.md`, `resume-long.md` — working scratch kept when useful.

## Generated exports — never hand-edit

These are produced *from* the source `.md` files and are what actually gets submitted. Editing them directly is how a resume and its PDF silently disagree. One home per fact: the `.md` is the home; regenerate the export after any edit.

- `resume.html`, `<Name>_<Company>_Resume.pdf` — rendered from `resume.md`.
- `cover-letter.txt` — plain-text export of `cover-letter.md` (for paste-into-a-textbox application forms).

If an export and its source drift, the source wins; re-export.

#!/usr/bin/env python3
"""
vikunja_sync.py — push one application folder to the Vikunja "Job Search" project.

Portable: standard library only (uses the system `curl` for multipart attachment
uploads). Safe to run repeatedly — it is a *sync*, not a blind insert:

  * If no task with the folder's title exists yet, it is created.
  * If one exists, its description is refreshed and any *.md not already attached
    is uploaded. Existing attachments with the same filename are left alone.

Configuration comes from a .env at the repo root (never committed):

    VIKUNJA_URL=http://your-vikunja-host:3456/api/v1
    VIKUNJA_TOKEN=tk_...            # bot user's API token

If VIKUNJA_TOKEN is unset/placeholder, or the server is unreachable, the script
prints a notice and exits 0 (a missing task tracker must never block the pipeline).

Usage:
    python3 tools/vikunja_sync.py applications/<folder>
    python3 tools/vikunja_sync.py <folder>          # 'applications/' assumed

Task placement: project id resolved by name (VIKUNJA_PROJECT, default "Job Search").
"""
import glob, json, os, re, subprocess, sys, urllib.request, urllib.error

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_NAME = os.environ.get("VIKUNJA_PROJECT", "Job Search")


def load_env():
    path = os.path.join(REPO, ".env")
    if os.path.exists(path):
        for line in open(path):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


def api(url, tok, method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url + path, data=data, method=method)
    req.add_header("Authorization", "Bearer " + tok)
    if data:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=15) as r:
        raw = r.read().decode()
        return json.loads(raw) if raw.strip() else {}


def first(patterns, text, default="?"):
    for p in patterns:
        m = re.search(p, text, re.I | re.M)
        if m:
            return m.group(1).strip()
    return default


def parse_folder(folder):
    """Best-effort extraction of task fields from status.md / posting.md."""
    def read(name):
        p = os.path.join(folder, name)
        return open(p).read() if os.path.exists(p) else ""
    status, posting = read("status.md"), read("posting.md")
    blob = status + "\n" + posting

    # Title: first H1, stripped of a leading "Status —"/"Status:" prefix.
    title = first([r"^#\s+(.+)$"], posting)
    if title == "?":
        title = first([r"^#\s+(.+)$"], status)
    title = re.sub(r"^status\s*[—:-]\s*", "", title, flags=re.I).strip()

    url = first([r"\*\*Posting URL:\*\*\s*(\S+)", r"\*\*Source URL:\*\*\s*(\S+)",
                 r"Posting URL:\s*(\S+)", r"Source URL:\s*(\S+)",
                 r"\*\*Source:\*\*\s*(\S+)", r"Source:\s*(https?://\S+)"], blob, "")
    apply = first([r"\*\*Apply via:\*\*\s*(.+)$", r"Apply via:\s*(.+)$"], blob, "")
    if apply.startswith("["):  # a [BRACKETED] placeholder, keep as-is
        pass
    track = first([r"\*\*Track:\*\*\s*(\w+)", r"Track:\s*(\w+)"], blob, "?")
    fit = first([r"\*\*Fit:\*\*\s*(.+)$", r"Fit:\s*(.+)$",
                 r"\*\*Verdict:\*\*\s*(.+)$"], blob, "?")
    comp = first([r"\*\*Comp(?:ensation)?:\*\*\s*(.+)$", r"Comp(?:ensation)?:\s*(.+)$"],
                 blob, "see posting")
    return dict(title=title, url=url, apply=apply, track=track, fit=fit, comp=comp)


def priority_for(fit):
    f = fit.lower()
    if "dream" in f or "strong" in f:
        return 3  # high
    return 2      # medium


def build_desc(meta, folder_rel):
    apply_line = ""
    if meta["apply"] and meta["apply"] != "?":
        apply_line = f"<p><b>Apply via:</b> {meta['apply']}</p>"
    url_line = (f"<p><b>Posting:</b> <a href=\"{meta['url']}\">{meta['url']}</a></p>"
                if meta["url"] else "")
    return (
        f"<ul>"
        f"<li><b>Track:</b> {meta['track']}</li>"
        f"<li><b>Fit:</b> {meta['fit']}</li>"
        f"<li><b>Comp:</b> {meta['comp']}</li>"
        f"</ul>"
        f"{url_line}{apply_line}"
        f"<p><b>Repo folder:</b> {folder_rel}/ — full status.md, posting, resume, "
        f"cover letter, and critique attached. See status.md for the current next action.</p>"
    )


def attach(url, tok, task_id, filepath):
    r = subprocess.run(
        ["curl", "-s", "-m", "20", "-X", "PUT",
         "-H", f"Authorization: Bearer {tok}",
         "-F", f"files=@{filepath}",
         f"{url}/tasks/{task_id}/attachments"],
        capture_output=True, text=True)
    return ('"success"' in r.stdout or '"id"' in r.stdout), r.stdout[:160]


def main(argv):
    load_env()
    url = os.environ.get("VIKUNJA_URL", "")
    tok = os.environ.get("VIKUNJA_TOKEN", "")
    if not url or not tok or tok.endswith("replace_me"):
        print("vikunja_sync: not configured (.env VIKUNJA_TOKEN unset) — skipping, "
              "pipeline continues.")
        return 0
    if len(argv) < 2:
        print(__doc__)
        return 2

    folder = argv[1]
    if not os.path.isabs(folder):
        folder = os.path.join(REPO, folder if folder.startswith("applications")
                              else os.path.join("applications", folder))
    if not os.path.isdir(folder):
        print(f"vikunja_sync: folder not found: {folder}")
        return 2
    folder_rel = os.path.relpath(folder, REPO)

    meta = parse_folder(folder)
    if meta["title"] == "?" or not meta["title"]:
        print(f"vikunja_sync: could not determine a task title from {folder_rel} "
              "(needs an H1 in status.md/posting.md) — skipping.")
        return 2

    try:
        projects = api(url, tok, "GET", "/projects")
        pid = next((p["id"] for p in projects if p["title"] == PROJECT_NAME), None)
        if pid is None:
            print(f"vikunja_sync: project {PROJECT_NAME!r} not visible to this token — "
                  "skipping.")
            return 2
        tasks = api(url, tok, "GET", f"/projects/{pid}/tasks")
    except (urllib.error.URLError, OSError) as e:
        print(f"vikunja_sync: server unreachable ({e}) — skipping, pipeline continues.")
        return 0

    desc = build_desc(meta, folder_rel)
    existing = next((t for t in tasks if t["title"] == meta["title"]), None)

    if existing:
        tid = existing["id"]
        api(url, tok, "POST", f"/tasks/{tid}",
            {"id": tid, "description": desc, "priority": priority_for(meta["fit"])})
        det = api(url, tok, "GET", f"/tasks/{tid}")
        have = {a.get("file", {}).get("name"): a.get("id")
                for a in (det.get("attachments") or [])}
        print(f"vikunja_sync: updated task id={tid}: {meta['title']}")
    else:
        task = api(url, tok, "PUT", f"/projects/{pid}/tasks",
                   {"title": meta["title"], "description": desc,
                    "priority": priority_for(meta["fit"])})
        tid = task["id"]
        have = {}
        print(f"vikunja_sync: created task id={tid}: {meta['title']}")

    # Refresh attachments: attachments are content snapshots, so a changed file must be
    # re-uploaded. Delete any existing same-name attachment first, then upload the current one.
    for m in sorted(glob.glob(os.path.join(folder, "*.md"))):
        name = os.path.basename(m)
        refreshed = name in have
        if refreshed:
            api(url, tok, "DELETE", f"/tasks/{tid}/attachments/{have[name]}")
        ok, out = attach(url, tok, tid, m)
        verb = ("refreshed" if refreshed else "attached ") if ok else "FAILED   "
        print(f"   {verb} {name}  {'' if ok else out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

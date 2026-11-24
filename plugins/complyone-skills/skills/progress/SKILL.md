---
name: progress
description: Track the progress made over the last few weeks (from git history across all repos plus decision and status files) and add it to a progress dashboard - creating the dashboard if it doesn't exist, updating it if it does. Use when asked to track, record, show or update progress, "what have we done", or the progress dashboard.
---

# Progress dashboard: create or update

Output is a dashboard in the `/dashboard` skill's format: Gantt at the top (one bar per workstream), click a workstream for the dated list of what was done. This skill gathers the evidence; `/dashboard`'s `build.py` renders it.

## 1. Find the dashboard and the window

- Dashboard file: `~/apps/head_architect/000_ceo/progress.dashboard.json` if that folder exists; otherwise `progress.dashboard.json` in the current folder. Exists → **update**. Missing → **create**.
- Window start: the file's `updated` date (update), or the user's window, or **28 days ago** (create). End: today.

## 2. Gather evidence (read-only)

1. **Git, every repo:** `python3 "<this skill's base directory>/scripts/collect_git.py" --since <start> --root ~/apps`. Never pull, fetch, checkout or touch a worktree.
2. **Decisions and state** (if `~/apps/head_architect` exists): entries dated inside the window in `330_Archie/memory/decisions.md`, `000_ceo/DECISIONS.md`, rows closed in `330_Archie/defects/DD.md` (sum their FP), and commercial facts in `230_Chief_Revenue_Officer/STATE.md` / `PIPELINE.md`.
3. Anything the user names in the request.

Only what has evidence goes in. No commit, decision or file behind it → it is not progress.

## 3. Turn evidence into workstreams

- A **workstream** is one outcome (e.g. "Free plan limits", "VC deck for WhyCommit", "Skills plugin"), not one commit. Group commits by repo and theme; aim for 8–25 workstreams, not hundreds of rows.
- `group` (one of): **Product** · **Sales & GTM** · **Fundraising** · **Partners** · **Marketing** · **Operations & Tooling** · **Finance**.
- `start` / `end`: date of the first and last evidence in the window.
- `status`: `done` if finished; `on-track` if still moving; `blocked` / `at-risk` only if a file says so. **Omit `progress` (%)** unless a source states it; never estimate.
- `summary`: one plain line on the outcome.
- `detail`: one bullet per item, `- YYYY-MM-DD · what changed (repo sha)`, newest first.
- `kpis`: measured counts only, e.g. commits in window, repos touched, workstreams done, FP closed (if summed from DD).
- **Never name a real customer, prospect or partner** in task text; write "customer", "prospect", "a partner".

## 4. Update rules (never lose history)

- Keep every existing workstream and its bullets.
- Add new bullets to the matching workstream (match by `id` or clearly the same outcome); extend its `end`; change its `status` only on evidence.
- New outcome → new workstream with the next free id (`W1`, `W2`, ...).
- Set `title` "Progress", `subtitle` "<first date> – <today> · from git and decision files", `view` "gantt", `updated` today. Recompute `kpis` over the whole period.

## 5. Build and publish

```bash
python3 "<this skill's base directory>/../dashboard/scripts/build.py" <path>/progress.dashboard.json
```

Fix any `ERROR` in the data; never weaken the data to pass. Publish `progress.html` with the Artifact tool if available, **same file path every time** so the link never changes; save the link in the JSON `url` field on first publish.

## 6. Reply

One line: created/updated, workstreams added or changed, link.

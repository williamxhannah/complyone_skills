---
name: dashboard
description: Create or update a task/progress dashboard - a light-background page with a Gantt chart (or progress bars) at the top, where clicking any task jumps to its detail below. Use when asked to create, build, update, refresh or show a dashboard, project tracker, roadmap view or progress page.
---

# Dashboard: create or update

The dashboard is two files that live side by side:
- `<slug>.dashboard.json` — the data. **This is what you edit.**
- `<slug>.html` — generated from the JSON by `scripts/build.py` in this skill's base directory. **Never hand-edit it.**

## 1. Create or update?

1. Look for existing dashboards: `find . -maxdepth 4 -name '*.dashboard.json' -not -path '*/node_modules/*'`.
2. If the request names one that exists, or exactly one matches the topic → **update** it.
3. If several could match → ask which, listing them.
4. Otherwise → **create** a new one in the current folder (or the folder the user names). Slug = short kebab-case of the title.

## 2. Fill the data

Schema (only `title`, `tasks`, and per task `id`, `name`, `status` are required):

```json
{
  "title": "Sprint 8045",
  "subtitle": "One line: what this tracks",
  "view": "gantt",
  "updated": "2026-11-24",
  "url": "",
  "kpis": [{"label": "Closed FP", "value": "42"}],
  "tasks": [
    {
      "id": "T1",
      "name": "Free plan limits",
      "group": "Backend",
      "owner": "110",
      "status": "on-track",
      "start": "2026-11-20",
      "end": "2026-12-05",
      "progress": 40,
      "depends": ["T0"],
      "summary": "One line on what this task is.",
      "detail": "Paragraph text.\n- bullet\n- bullet",
      "items": [{"text": "RPC built", "done": true}],
      "links": [{"label": "Brief", "url": "https://..."}]
    }
  ]
}
```

- `view`: `gantt` (timeline, needs dates) or `progress` (bars by % done). Default `gantt`.
- `status`: `not-started` · `on-track` · `at-risk` · `blocked` · `done`.
- **Never invent data.** No made-up dates, progress or owners. If a value is not known, leave the field out: an undated task shows as "Not scheduled yet", a task with no `progress` shows as "not measured". A guess presented as a fact is worse than a gap.
- Take facts from the user's message or from the files they point to (STATE.md, briefs, boards). When updating, change only what the request or the sources changed, and set `updated` to today.

## 3. Build

```bash
python3 "<this skill's base directory>/scripts/build.py" <slug>.dashboard.json
```

It validates first and stops with an `ERROR` line on bad data (missing field, unknown status, end before start, unknown dependency). Fix the JSON; never loosen the data to get past it.

## 4. Publish

- **If an Artifact tool is available:** publish `<slug>.html`. On an update, publish the **same file path** so the link stays the same. Store the link in the JSON's `url` field the first time.
- **Otherwise:** send or open the HTML file.

## 5. Reply

One line: created or updated, and the link. Nothing else unless asked.

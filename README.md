# complyone-skills

ComplyOne.io house skills for Claude Code, packaged as a plugin so every session on every machine can use them.

## Install on a machine (once)

In any Claude Code session:

```
/plugin marketplace add williamxhannah/complyone_skills
/plugin install complyone-skills@complyone-skills
```

The repo is private, so the machine needs GitHub access first (SSH key or `gh auth login`).

## Get updates after a skill changes

```
/plugin marketplace update complyone-skills
```

## Skills

| Skill | Use |
|---|---|
| `/linkedin-post` | Draft, edit or review a ComplyOne.io LinkedIn post |
| `/dashboard` | Create or update a task dashboard: Gantt or progress at the top, click a task for its detail |
| `/inbox` | Read-only email brief: production issues, customers, partners, VCs, money/legal, needs a reply |
| `/progress` | Gather the last weeks of progress (git across all repos + decision files) into a progress dashboard; creates or updates it |
| `/meeting-notes` | Find Google Meet transcripts / Gemini notes via Gmail and summarise each meeting |
| `/my-voice` | Write emails in William's own short, plain voice; bans AI-style phrases |

## Add a skill

Create `plugins/complyone-skills/skills/<name>/SKILL.md`, bump `version` in `plugins/complyone-skills/.claude-plugin/plugin.json`, commit and push.

# complyone-skills

ComplyOne.io house skills for Claude Code, packaged as a plugin so every session on every machine can use them.

## Install on a machine (once)

In any Claude Code session:

```
/plugin marketplace add williamxhannah/complyone-skills
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

## Add a skill

Create `plugins/complyone-skills/skills/<name>/SKILL.md`, bump `version` in `plugins/complyone-skills/.claude-plugin/plugin.json`, commit and push.

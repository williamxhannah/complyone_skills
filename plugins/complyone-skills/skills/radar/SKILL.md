---
name: radar
description: Create the weekly ComplyOne Radar post and newsletter. Covers news collection, topic proposal, newsletter draft, LinkedIn post + image, and scheduling. Use when asked to run the weekly Radar, create a new Radar edition, or draft the weekly compliance newsletter.
---

# ComplyOne Radar — weekly workflow

Load `complyone-skills:my-voice` and `complyone-skills:linkedin-post` before drafting any copy.

This skill runs in 8 steps. Steps 1–4 happen in the same turn, then wait for William to pick a topic. Steps 5–8 run after he picks.

---

## Step 1 — Collect the week's news

Two sources, run in parallel:

**A. Ask 130 (Sales & GTM session)** — message the active 130 session via `mcp__ccd_session_mgmt__send_message`: "Radar run — please send this week's compliance news digest (any regulatory updates, enforcement actions, consultations, or deadlines you have noted since the last Radar)."

**B. Web search** — run all three in parallel:
- `site:eur-lex.europa.eu OR site:esma.europa.eu OR site:eba.europa.eu compliance regulation 2026` (last 7 days)
- `FCA DORA NIS2 GDPR enforcement announcement` (last 7 days)
- `EU compliance SME regulation news` (last 7 days)

Collect the results. Only carry items that have a primary-source URL you have fetched. No invented or recalled news.

---

## Step 1b — Recency and source validation (MANDATORY before Step 2)

Run this for every item that survived Step 1. No item proceeds to topic proposal without passing both gates.

### Gate A — Date verification

For each item:
1. Fetch the primary-source URL.
2. Find the publication date **on that page** — the date stamp in the page header, article metadata, or HTML `<time>` element. Do not use the date a search engine cached or a date you recall.
3. The item is accepted only if the date is **within 14 days of today**. Anything older is dropped, regardless of how recent it looked in search results.
4. Record: `[headline] | [date found on page] | [URL]`

If the date cannot be found on the page, the item is dropped. "I could not find a date" is a drop, not a pass.

### Gate B — Independent validation check

After Gate A, re-verify each accepted item using a **second independent method**:
- Either fetch a second URL that references the same item (e.g. the regulator's main news index, a secondary press release, the EUR-Lex publication notice), OR
- Search for the item's headline and confirm the date reported by another source matches.

This exists because a page can carry a stale "last updated" date far older than the original publication, or a search snippet can show an old article as if new. Gate B catches that.

If Gate B finds a date mismatch (e.g. Gate A returned 2026 but Gate B finds the item is from 2024), the item is dropped and flagged: `⚠️ DATE CONFLICT — dropped: [headline]`.

### Output of Step 1b

Before moving to Step 2, show a compact validation table:

```
RECENCY CHECK — [today's date]
| Item | Date on page | Gate B confirms | Status |
|------|-------------|-----------------|--------|
| ...  | DD MMM YYYY | yes / no / mismatch | ✅ / ❌ |
```

Items marked ❌ do not appear in topic proposals. If fewer than 3 items pass, say so and ask whether to widen the search window before continuing.

---

## Step 2 — Review product priority

Fetch `https://complyone.io/sales` and read the product order on the page — left to right, top to bottom is the priority order. Note the top 5 modules. These are the products most likely to have a relevant hook for this week's Radar.

---

## Step 3 — Additional research

For each story that survived Step 1: fetch the primary source URL, read the actual text, and note:
- What changed (the new rule, the deadline, the enforcement action)
- Who it applies to (which company types / sectors / jurisdictions)
- What a business must actually do as a result
- Whether any top-5 product from Step 2 is directly relevant

Discard any story where the primary source does not support the item (no fallback data, no reconstructed facts).

---

## Step 4 — Propose 3 topics

Present exactly 3 topic options. For each one:

```
TOPIC [n]: [One sentence title]
Hook: [The concrete situation that makes this worth reading this week]
Audience: [Who this speaks to most directly]
Product tie: [Which module is relevant, or "none — no product claim"]
Newsletter angle: [2–3 sentences on what the newsletter would cover]
LinkedIn angle: [1 sentence on the post hook]
```

Then: **"Which topic? 1, 2 or 3."**

Wait. Do not draft anything until William picks.

---

## Step 5 — Write the newsletter

After he picks, draft the full newsletter. Format matches Edition 1:

```
TITLE: [Short, punchy]
SUBTITLE: [What this edition covers, one line]

---

[Opening paragraph: 2–3 lines setting the scene. What changed and why it matters now.]

[2–4 numbered sections, each with a bold heading and 100–200 words]

[Closing "What to do with this" section: 3–5 concrete steps, plain dash bullets]

[Product paragraph: 1–2 lines only if the module is live and entitlements verified. Never claim if not confirmed.]

[Sign-off: "— William Hannah, ComplyOne.io / complyone.io"]
```

Length: 800–1,200 words. No jargon beyond the audience level. No em dashes. Apply `my-voice` rules throughout.

**Teaser line for next edition:** one sentence at the end ("Next edition: [topic].").

Save to: `sales/linkedin posts/radar_newsletter/edition_NN_<slug>.txt` (increment NN from last edition).

---

## Step 6 — Write the LinkedIn post and render the image

**Post** — apply all `linkedin-post` rules. The Radar post has a fixed structure:

1. Opening: a concrete fact or situation from the newsletter (not "I wrote a newsletter").
2. 2–3 short paragraphs covering the main insight, written to stand alone without the newsletter.
3. Final line: "Full edition in the comments." (William drops the newsletter text as a first comment.)
4. Hashtags: 3–5, always `#compliance`.

Length: 150–250 words. Save to: `sales/linkedin posts/YYYY-MM-DD_radar_edition_NN.txt`.

**Image** — render a 1200×628 PNG via Playwright (same pipeline as the UK crypto series):
- Background: navy (#0A1628) to teal (#00B5A3) gradient, top-left to bottom-right
- Top-left: "ComplyOne Radar" in teal, Inter 600, 18px
- Edition number + date: white, Inter 400, 14px, below the kicker
- Headline: white, Inter 800, 48–56px, max 2 lines, vertically centred
- Bottom-right: "ComplyOne.io" brand mark, white, Inter 600, 16px
- File: `sales/linkedin posts/radar_newsletter/img_radar_edition_NN.png`

Show the PNG to William before proceeding to Step 7.

---

## Step 7 — Publish to LinkedIn

**TBD — William will demonstrate the posting process.**

When he has shown the mechanism, record the steps here and in `160_Content_And_Marketing/STATE.md`.

For now: show William the post text and image, confirm he is happy, and ask: "Ready for me to post, or will you do it?"

If posting: use `mcp__claude-in-chrome__*` tools to navigate to linkedin.com, create a new post, paste the text, attach the image, and either post now or schedule.

---

## Step 8 — Schedule for Monday

Target: published Monday 09:00 CET.

If LinkedIn scheduling is available via the browser: schedule during Step 7 on the Friday of the same week.

Log the edition in `160_Content_And_Marketing/STATE.md`:
- Edition number, date, topic, LinkedIn post URL (once live), newsletter file path

---

## Hard rules

| Rule | Detail |
|---|---|
| No fallback data | Every news item has a fetched primary-source URL. If the source doesn't support the claim, it goes. |
| No product claim without entitlement check | Before mentioning any module, confirm it is live AND entitlements are verified (precedent: Cyber Pack CRA, 0 of 38 entitlements). Post with no product claim is better than a false one. |
| No real customer names | Never name a customer, prospect or partner in the newsletter or post. |
| Verify before each run | Check whether any "coming soon" items in the previous edition have since been published, and update if so. |
| Edition numbering | Increment from the last saved edition in `sales/linkedin posts/radar_newsletter/`. Edition 1 = `edition_01_crypto.txt`. Never reuse a number. |

---

## Quick-start (tl;dr)

1. Run Steps 1–4 → present 3 topics → wait
2. William picks → run Steps 5–6 → show newsletter + post + image
3. His OK → Step 7 (post/schedule) → Step 8 (log it)

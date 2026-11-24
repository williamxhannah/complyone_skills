---
name: radar
description: Create the weekly ComplyOne Radar post and newsletter. Covers research, topic proposal, newsletter draft, LinkedIn post + image, and scheduling. Use when asked to run the weekly Radar, create a new Radar edition, or draft the weekly compliance newsletter.
---

# ComplyOne Radar — weekly workflow

Load `complyone-skills:my-voice` and `complyone-skills:linkedin-post` before drafting any copy.

This skill runs in 8 steps. Steps 1–4 happen in the same turn, then wait for William to pick a topic. Steps 5–8 run after he picks.

---

## What the Radar is

The Radar is a **thought leadership newsletter and LinkedIn post** aimed at compliance professionals and business leaders across Europe (focus: DACH, UK, Benelux). Its job is to give ComplyOne credibility with compliance audiences, not to report the week's news.

**Good Radar topics:**
- How AI is changing compliance processes — what it automates, what new risks it creates
- The future of compliance — what is becoming mandatory that wasn't two years ago
- Which industries are under the most compliance pressure, and why now
- How automation is reshaping what compliance teams actually do day-to-day
- A pattern of enforcement across multiple companies or jurisdictions that reveals a shift
- A stat or finding that reframes how compliance professionals think about a problem
- An inflection point: a deadline approaching, a framework changing, a sector waking up

**Not a Radar topic:**
- A single enforcement action described on its own
- A regulatory announcement with no analysis of what it means
- A news item without a "so what" for the reader

The news and regulatory updates gathered in Step 1 are **evidence** that a trend is happening — not the topic itself. The topic is what a compliance professional or business leader learns by reading the full edition.

---

## Step 1 — Gather source material

Run all three tracks in parallel.

### Track A — Ask 130 (Sales & GTM session)
Message via `mcp__ccd_session_mgmt__send_message`: "Radar run — what compliance trends, sector pressures, or regulatory shifts are your prospects talking about this week?"

### Track B — Regulator sources (last 14 days only)
Fetch the listing page for each source. For any item that might be relevant, note the URL — full reads happen in Step 1b.

| Source | URL | Covers |
|--------|-----|--------|
| BaFin (Germany) | https://www.bafin.de/EN/Presse/Pressemitteilungen/pressemitteilungen_node.html | DE financial regulation |
| FINMA (Switzerland) | https://www.finma.ch/en/news/ | CH financial regulation |
| FMA (Austria) | https://www.fma.gv.at/en/press/press-releases/ | AT financial regulation |
| FCA (UK) | https://www.fca.org.uk/news | UK financial regulation |
| ESMA | https://www.esma.europa.eu/press-news/esma-news | EU markets |
| EBA | https://www.eba.europa.eu/news/listing | EU banking |
| EDPB | https://www.edpb.europa.eu/news/news_en | EU data protection |
| EUR-Lex | https://eur-lex.europa.eu/oj/direct-access.html | EU legislation |

If a URL returns 404 or 403, note the failure and skip — do not guess alternatives or substitute a different page.

### Track C — Industry research and stats
Search for recent (last 90 days) compliance industry reports, surveys, and statistics that support a trend topic. Good sources:

- Thomson Reuters compliance surveys (annual cost of compliance)
- Deloitte / PwC / KPMG / EY compliance and regulatory outlook reports
- ICA (International Compliance Association) research
- ACAMS (AML/financial crime)
- LexisNexis True Cost of Financial Crime report
- Forrester / Gartner RegTech or compliance automation reports
- Any stat on: compliance headcount growth, compliance technology spend, cost of non-compliance, number of regulations firms track, enforcement fine totals by year

Stats are strong anchors for trend topics. A stat like "cost of compliance for financial firms rose 10% last year" is more useful than a single enforcement action.

**A headline is not source material.** Nothing passes to Step 1b without a primary-source URL you have fetched and read.

---

## Step 1b — Recency and content validation (MANDATORY)

Run this for every item from Step 1 before anything else. No item reaches topic proposals without passing both gates.

### Gate A — Full read + date check

Fetch each primary-source URL. **Read the full article.** From the text, extract:

1. **Publication date** — from the page header or metadata. Not from a search snippet. If not found, drop the item.
2. **What it actually says** — specific outcomes, amounts, deadlines, findings. No inference from the headline. "Sentenced" means you read the sentence. "Fined" means you read the amount and the basis.
3. **Who it applies to** — from the article, not assumed.
4. **The stat or finding** — exact number, with the sample size or methodology if given.

Recency rule: regulatory news must be **within 14 days**. Industry reports and stats may be up to **90 days old** if the finding is durable.

### Gate B — Independent date confirmation

For each item, confirm the date via a second independent source (the regulator's index page, a second press release, the report's own publication page). If the dates conflict, drop the item and flag it: `⚠️ DATE CONFLICT — dropped`.

### Output of Step 1b

Show this table before moving on:

```
RESEARCH VALIDATED — [today's date]
| Item | Source | Date on page | Gate B | What it actually says | Status |
|------|--------|-------------|--------|----------------------|--------|
| ...  | ...    | DD MMM YYYY | ✅/⚠️  | 1-line from the text | ✅/❌  |
```

The "What it actually says" column proves Gate A ran on the full text. A vague or headline-parroting entry has not passed. If fewer than 3 items pass, ask before continuing.

---

## Step 2 — Review product priority

Fetch `https://complyone.io/pricing` (or ask William for the correct product listing URL if that 404s). Note the top 5 modules by order of appearance — these weight which trends are most commercially relevant to ComplyOne right now.

---

## Step 3 — Map items to trends

For each validated item, write one sentence: "[This item / stat] shows that [trend]."

Then group items that point to the same trend. A newsletter can weave two or three related items into a single coherent argument. Cross-reference against the product priority from Step 2 — a trend that touches a top-5 module gets weighted higher.

---

## Step 4 — Propose 3 topics

Each topic must be a **trend or insight** a compliance professional would find worth reading. Not an event summary.

```
TOPIC [n]: [The trend, in one sentence]
Trend: [What is shifting and why it matters now]
Evidence: [Sourced items or stats supporting it, with URLs and dates]
Stat: [Key number if available, with source]
Audience: [Who specifically — DE/CH/AT/UK SMEs, fintechs, compliance officers, etc.]
Product tie: [Which module is relevant, or "none — no product claim"]
Newsletter angle: [The question a reader walks away having answered]
LinkedIn angle: [The single insight that makes someone stop scrolling]
```

Topics must be **trends**. "The FCA fined someone" is not a topic. "Regulators are now going after the promoter, not just the product — and social media is the new audit trail" is a topic.

Then: **"Which topic? 1, 2 or 3."**

Wait. Do not draft anything until William picks.

---

## Step 5 — Write the newsletter

After he picks, draft the full newsletter. Format based on Edition 1:

```
TITLE: [Short, punchy — the trend, not the event]
SUBTITLE: [What this edition covers, one line]

---

[Opening: 2–3 lines. The situation and why it matters now.]

[2–4 numbered sections, bold headings, 100–200 words each. Analysis, not summary.]

[Closing "What to do with this": 3–5 concrete steps, plain dash bullets]

[Product paragraph: 1–2 lines only if the module is live and entitlements verified.]

[Sign-off: "— William Hannah, ComplyOne.io / complyone.io"]
```

Length: 800–1,200 words. No jargon beyond audience level. No em dashes. Apply `my-voice` rules.

Teaser: "Next edition: [topic]." at the end.

Save to: `sales/linkedin posts/radar_newsletter/edition_NN_<slug>.txt`

---

## Step 6 — Write the LinkedIn post and render the image

**Post** — apply all `linkedin-post` rules:

1. Opening: a concrete stat or insight from the newsletter. Not "I wrote a newsletter."
2. 2–3 short paragraphs standing alone — the reader learns something without clicking through.
3. Final line: "Full edition in the comments."
4. Hashtags: 3–5, always `#compliance`.

Length: 150–250 words. Save to: `sales/linkedin posts/YYYY-MM-DD_radar_edition_NN.txt`

**Image** — 1200×628 PNG (same pipeline as UK crypto series):
- Background: navy (#0A1628) → teal (#00B5A3) gradient, top-left to bottom-right
- Top-left: "ComplyOne Radar" in teal, Inter 600, 18px
- Edition number + date: white, Inter 400, 14px
- Headline: white, Inter 800, 48–56px, max 2 lines, centred
- Bottom-right: "ComplyOne.io", white, Inter 600, 16px
- Save: `sales/linkedin posts/radar_newsletter/img_radar_edition_NN.png`

Show the PNG before Step 7.

---

## Step 7 — Publish to LinkedIn

**TBD — William will demonstrate the posting process.**

Once demonstrated, record the steps here and in `160_Content_And_Marketing/STATE.md`.

For now: show William post + image, confirm approval, ask: "Ready for me to post, or will you do it?"

If posting: use `mcp__claude-in-chrome__*` tools — navigate to linkedin.com, create post, paste text, attach image, post or schedule.

---

## Step 8 — Schedule and log

Target: Monday 09:00 CET.

Log in `160_Content_And_Marketing/STATE.md`: edition number, date, topic, LinkedIn post URL (once live), newsletter file path.

---

## Hard rules

| Rule | Detail |
|---|---|
| No fallback data | Every claim has a fetched, read primary source. No recalled stats, no inferred numbers. |
| Headlines are not sources | An item that has not been fully read does not exist for this workflow. |
| No product claim without entitlement check | Module must be live AND entitlements verified before any product claim. |
| No real customer names | Never name a customer, prospect or partner. |
| Edition numbering | Increment from last saved edition. Never reuse a number. |

---

## Quick-start

1. Steps 1–4 → 3 topic proposals → wait for pick
2. Pick received → Steps 5–6 → show newsletter + post + image
3. Approval → Step 7 (post) → Step 8 (log)

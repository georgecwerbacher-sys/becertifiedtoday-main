---
type: campaign
product: secplus
channel: reddit
utm_campaign: secplus_wedge_pbq
tags:
  - marketing
  - reddit
  - security+
  - secplus
created: 2026-06-22
---

# Sec+ campaign — Reddit only

Single-page setup for **ads.reddit.com**. No Google settings here.

**Setup steps:** [[Sec+ Reddit Notes]] · **Copy:** [[Sec+ Reddit Copy]] · **Checklist CSV:** [[secplus-reddit-checklist.csv]]

**Account:** [u/BeCertifiedToday](https://www.reddit.com/user/BeCertifiedToday/) · **Shared Reddit budget:** $10/day (CCNA + Sec+ — launch Sec+ PBQ first)

Organic posting: [[../Reddit/posting/Sec+ replies|Sec+ replies]] · voice: [[../Reddit/posting/Voice guide|Voice guide]] · log: [[../Reddit/posting/Post log|Post log]]

---

## Campaign

| Setting      | Value                                                           |
| ------------ | --------------------------------------------------------------- |
| Name         | `SEC+_Wedge_Reddit`                                             |
| Objective    | **Traffic**                                                     |
| Daily budget | **$10.00** (shared with CCNA — pause CCNA or split $5/$5 later) |
| Schedule     | Continuous                                                      |

---

## Ad group — targeting

| Setting        | Value                                                                                    |
| -------------- | ---------------------------------------------------------------------------------------- |
| **Placements** | **Feed ON** · **Conversation ON**                                                        |
|                | Feed = promoted post in subreddit scroll. Conversation = in comment threads under posts. |
| Communities    | `r/CompTIA`, `r/SecurityPlus`                                                            |
| Locations      | US, CA, UK, AU                                                                           |
| Interests      | None                                                                                     |
| Keywords       | None                                                                                     |

Hold until later: r/itcareerquestions, r/cybersecurity (too broad for launch)

---

## Ad group — bidding

| Setting | Value |
|---------|--------|
| Automated bidding | **On** |
| Strategy | **Lowest cost** |
| Cost cap | **Off** |

---

## Ad group — tracking

Reddit has **three** URL-related fields. Do **not** paste the same URL in more than one.

| Field | What to enter |
|-------|----------------|
| **Destination URL** | Landing page — use **Option A** or **Option B** below |
| **URL parameters** (if shown separately) | Option B only — UTMs without the domain |
| **Tracker URL** (third-party click/impression tracker) | **Leave empty** — do not paste your landing URL here |

If you see **“Your tracker URL must be different from your destination URL”**, you duplicated the landing URL into **Tracker URL**. Clear **Tracker URL** entirely (or remove “Add another tracker” rows).

| Setting | Value |
|---------|--------|
| Reddit Pixel | **Skip** (launch) |
| Third-party Tracker URL | **Empty** |

### Option A — one Destination URL field (paste this)

```
https://becertifiedtoday.com/secplus/pbq-practice-browser.html?utm_source=reddit&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=reddit-pbq
```

### Option B — Destination + URL parameters split

**Destination URL:**

```
https://becertifiedtoday.com/secplus/pbq-practice-browser.html
```

**URL parameters** (no leading `?`):

```
utm_source=reddit&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=reddit-pbq
```

**Ad set 2 — timed sim (phase 2):**

Option A:

```
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=reddit&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=reddit-timed-sim
```

Option B destination: `https://becertifiedtoday.com/comptia-sec+-home.html`  
Option B parameters: `utm_source=reddit&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=reddit-timed-sim`

---

## Creative — Ad set 1 PBQ (Image — headline + image in feed)

Reddit **Image** ads do **not** show a long body in the feed. Pack the offer into **headline**, **image text**, and **landing page**.

| Field | Value |
|-------|--------|
| **Post type** | **Image** |
| Profile | u/BeCertifiedToday |
| CTA | **Learn More** |
| Destination URL | PBQ UTMs above |
| Main image | PBQ scenario screenshot (dark web or chain lab) |
| **Thumbnail** | Same image or 4:3 crop (required for Feed) |

**Headline** — [[Sec+ Reddit Copy#Ad set 1 — PBQ (start here)|Ad set 1 title]]

```
SY0-701 PBQs in the browser — chain labs, not a PDF
```

**Description** (fill if UI has the field — may not show in all previews)

```
34 PBQ scenarios · 90-min timed sim · 1000+ MCQs. Free dark web sample. $9.99/10 days.
```

**Text on the image itself** (most reliable — add in Canva/Preview before upload)

```
Security+ SY0-701
Browser PBQs · no download
90-min timed sim
$9.99 / 10 days
becertifiedtoday.com
```

After click → **pbq-practice-browser.html** has free sample, pricing, and checkout.

Full body copy (Promoted post / text ad variant): [[Sec+ Reddit Copy#Ad set 1 — PBQ (start here)]]

---

## Creative — Ad set 2 timed sim (phase 2)

Use after Ad set 1 has 7+ days of data or if PBQ CTR is strong but checkouts lag.

| Field | Value |
|-------|--------|
| Destination URL | timed sim UTMs above |
| Headline | [[Sec+ Reddit Copy#Ad set 2 — timed sim + work cert|Ad set 2 title]] |

---

## Voice guardrails

From [[Sec+ Positioning#Do not say in paid search|positioning]] — same rules on Reddit:

- Do **not** say: guaranteed pass, actual exam questions, dumps, braindump
- Do **not** lead with “free timed exam” — timed sim is **paid access**
- Do say: browser PBQs, 90-min sim + scorecard, free **sample** (MCQ + dark web PBQ), $9.99 sprint pricing

---

## After launch

- GA4 → session source **`reddit`**
- Week 1: CTR **> 0.2%** · any **`begin_checkout`** with `utm_content=reddit-pbq`
- Log launch + metrics in [[../Reddit/posting/Post log|Post log]]
- Compare `reddit-pbq` vs `reddit-timed-sim` before scaling Ad set 2

[[README|← Sec+ Campaign folder]]

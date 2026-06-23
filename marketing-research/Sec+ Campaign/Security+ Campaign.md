---
type: campaign
product: secplus
utm_campaign: secplus_portal
tags:
  - marketing
  - google-ads
  - security+
  - secplus
---

# Campaign shell — Security+ SY0-701 · Exam prep · becertifiedtoday

Paste-ready settings for Google Ads UI. **Setup steps:** [[Sec+ Notes]] · **Keywords:** [[Sec+ Keywords]] · **CSV:** [[secplus-campaign-checklist.csv]]

---

## Campaign settings

| Setting | Value |
|---------|--------|
| Campaign name | `Security+ SY0-701 · Exam prep · becertifiedtoday` |
| Type | Search (Search partners **off** until baseline) |
| Daily budget | **$20.00/day** |
| Bidding (weeks 1–2) | Maximize clicks · max CPC **$2.75** |
| utm_campaign | `secplus_portal` |
| Language | English |
| Locations | Tier A countries — presence only (see [[Extensions#Geo]]) |
| AI Max / URL expansion | **Off** |
| Primary conversion | GA4 `begin_checkout` (import as Primary in Google Ads) |

**One ad group only:** `Security+ PBQ Practice` — full $20/day budget goes here.

---

## Ad group — Security+ PBQ Practice

| Setting       | Value                        |
| ------------- | ---------------------------- |
| Ad group name | **`Security+ PBQ Practice`** |
| Display path  | `Security+` / `PBQ-Practice` |
| Pin H1        | `Security+ PBQ Practice`     |
| Pin H2        | `$9.99 · 10-Day Access`      |

**Final URL:**

```
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=pbq-wedge
```

RSA: [[Sec+ RSA Copy#Ad group Security+ PBQ Practice]] · Keywords: [[Sec+ Keywords#Ad group — Security+ PBQ Practice]]

---

## Products or services to advertise

**Category:** Education & training → Test preparation

| # | Product / service name | Description (paste under name in Google Ads) |
|---|------------------------|-----------------------------------------------|
| 1 | Security+ 10-Day Exam Prep Access | 10 days of SY0-701 v5.0 exam prep in your browser: 1000+ practice questions, 34 PBQ scenarios, adaptive review, portal modes, and 90-min timed exam with scorecard. $9.99 one-time. |
| 2 | Security+ 30-Day Exam Prep Access | 30 days of the same SY0-701 library: 1000+ questions, 34 PBQ scenarios, adaptive review, progress tracking, and timed exam. $19.99 one-time. |
| 3 | Security+ Practice Questions | 1000+ SY0-701 MCQ bank with verified explanations, adaptive review, and timed exam. Browser-only. |
| 4 | Security+ PBQ Scenarios | 34 performance-based scenarios—chain labs, drag-drop, hot spots, IR exhibits—in browser. |
| 5 | Security+ Timed Exam Simulation | 90-minute mixed MCQ + PBQ run with domain scorecard review. Included with portal access. |

---

## Pre-launch checks

- [ ] Stripe `secplus-portal-10d` ($9.99) and `secplus-portal-30d` ($19.99) live
- [ ] Checkout works on cert home (desktop + mobile)
- [ ] GA4 `begin_checkout` fires for both item IDs
- [ ] `secplus-home-conversion.js` — test `?utm_content=pbq-wedge` on cert home
- [ ] Cert home loads: `/comptia-sec+-home.html`
- [ ] Keyword Planner worksheet filled — [[Sec+ Keywords#Keyword Planner worksheet]]

---

## Week 1 ops

Do not change budget, bidding, geo, or RSA for 7 days.

| Day | Action |
|-----|--------|
| 1 | Confirm ads serving · GA4 checkout on test click |
| 3 | Search terms → add negatives |
| 7 | CPA review — hold or tune max CPC |

[[README|← Sec+ Campaign folder]]

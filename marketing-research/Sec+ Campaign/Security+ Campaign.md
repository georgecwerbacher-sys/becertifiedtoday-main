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

# Campaign Shell — Security+ SY0-701 · US Search

Paste-ready settings for Google Ads UI. **Current build:** [[Sec+ One-Campaign Ad Group Plan]] · **Setup steps:** [[Sec+ Notes]] · **Keywords:** [[Sec+ Keywords]]

**Strategy (2026-06-27):** Build **one US-only Search campaign** with **three intent-matched ad groups** and a shared **$25/day** budget. Let Google determine the spend split based on ad group output. This keeps early learning concentrated and avoids creating separate campaign budgets before conversion data proves the need.

---

## Campaign Settings

| Setting | Value |
|---------|--------|
| Campaign name | `Security+ SY0-701 · US Search` |
| Type | Search |
| Search partners | **Off** until baseline |
| Display Network | **Off** |
| Daily budget | **$25/day shared** |
| Bidding | Maximize clicks |
| Max CPC | **$2.75** |
| Language | English |
| Locations | **United States only** |
| Location option | **Presence** — people in or regularly in targeted locations |
| Ad schedule | Before work, lunch, after work, weekends |
| AI Max / URL expansion | **Off** |
| Primary conversion | GA4 `begin_checkout` imported as Primary |
| `utm_campaign` | `secplus_portal` |

**Important:** Do not build three separate campaigns at launch. Split only after an ad group proves it needs its own budget, geo strategy, schedule, bid strategy, landing page, or materially different ROI.

---

## Ad Groups

| Ad group | Audience intent | UTM content | Display path |
|----------|-----------------|-------------|--------------|
| `Core Exam Prep` | Timed sim, readiness, adaptive review, browser/no-PDF prep | `core-exam-prep` | `Security+` / `Exam-Prep` |
| `Military Gov 8140` | Military, DoD 8140, federal, contractors, public sector | `mil-gov-8140` | `Security+` / `DoD-8140` |
| `Student Workforce` | Students, educators, veterans, workforce/job-placement programs | `student-workforce` | `Security+` / `Career-Prep` |

---

## Final URLs

```text
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=core-exam-prep

https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=mil-gov-8140

https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=student-workforce
```

---

## Products or Services to Advertise

**Category:** Education & training → Test preparation

| # | Product / service name | Description |
|---|------------------------|-------------|
| 1 | Security+ 30-Day Exam Prep Access | 30 days of SY0-701 exam prep in your browser: 1000+ blueprint-verified practice questions, adaptive review, progress tracking, 34 PBQ scenarios, and 90-minute timed exam with scorecard. $19.99 one-time. |
| 2 | Security+ Practice Questions | 1000+ SY0-701 MCQ bank tagged to objective IDs with verified explanations, adaptive review, and timed exam. Browser Test Preparation Site. |
| 3 | Security+ Timed Exam Simulation | 90-minute mixed MCQ + PBQ run with domain scorecard review. Included with 30-day portal access. |
| 4 | Security+ PBQ Scenarios | 34 performance-based scenarios: chain labs, drag-drop, hot spots, and incident-response exhibits in browser. Included with full exam prep access. |

---

## Pre-Launch Checks

- [ ] Stripe `secplus-portal-30d` ($19.99) live
- [ ] Checkout works on cert home (desktop + mobile)
- [ ] GA4 `begin_checkout` fires for `secplus_portal_30d`
- [ ] Campaign URL tested for each `utm_content`
- [ ] Cert home loads: `/comptia-sec+-home.html`
- [ ] Keyword split reviewed: [[Sec+ Keywords#One-campaign ad group keyword split]]

---

## Week 1 Ops

Launch the full campaign with all three ad groups active. Do not change budget, max CPC, geo, RSA pins, or structure for 7 days unless traffic is clearly irrelevant or tracking is broken.

| Day | Action |
|-----|--------|
| 1 | Confirm ads serving and GA4 checkout event on a test click |
| 3 | Search terms → add negatives |
| 7 | Review by ad group and keyword; adjust bids or pause weak terms based on checkout quality |

[[README|← Sec+ Campaign folder]]

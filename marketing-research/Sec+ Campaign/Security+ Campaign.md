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

Paste-ready settings for Google Ads UI. **Three-campaign build:** [[Sec+ Three-Campaign US Plan]] · **Setup steps:** [[Sec+ Notes]] · **Keywords:** [[Sec+ Keywords]]

**Strategy (2026-06-27):** Build **three US-only Search campaigns** at **$20/day each**: core exam prep, military/government/8140, and student/workforce. Google Ads budgets are campaign-level, so this structure is how each track gets its own $20/day cap. **Do not modify admin dashboard yet**; keep `secplus_portal` history as baseline and reconcile the three new `utm_campaign` values manually until tracking is expanded.

---

## Campaign settings

| Setting | Value |
|---------|--------|
| Campaign names | `Security+ SY0-701 · Core Exam Prep · US` · `Security+ SY0-701 · Military Gov 8140 · US` · `Security+ SY0-701 · Student Workforce · US` |
| Type | Search (Search partners **off** until baseline) |
| Daily budget | **$20.00/day per campaign** · **$60/day total** |
| Bidding (week 1) | Maximize clicks · max CPC **$2.75** · hold keyword bids for 7 days |
| Bidding review | Adjust keyword bids after week 1 based on keyword results |
| utm_campaign | `secplus_core_us` · `secplus_gov_us` · `secplus_workforce_us` |
| Language | English |
| Locations | **United States only** — presence only (see [[Sec+ Three-Campaign US Plan#US-only location setup]]) |
| Ad schedule | Before work, lunch, after work, weekends (see [[Sec+ Three-Campaign US Plan#Ad schedule — when target buyers search]]) |
| AI Max / URL expansion | **Off** |
| Primary conversion | GA4 `begin_checkout` (import as Primary in Google Ads) |

**Important:** If Google Ads UI only lets you budget at campaign level, do **not** try to run three ads inside one campaign and expect $20/day each. Use the three campaigns in [[Sec+ Three-Campaign US Plan]].

---

## Campaign tracks

| Track | Campaign | Budget | UTM content | Audience |
|-------|----------|--------|-------------|----------|
| Core | `Security+ SY0-701 · Core Exam Prep · US` | $20/day | `core-exam-prep` | Timed sim, adaptive review, general SY0-701 prep |
| Gov | `Security+ SY0-701 · Military Gov 8140 · US` | $20/day | `mil-gov-8140` | Military, DoD 8140, federal, contractors, first responders |
| Workforce | `Security+ SY0-701 · Student Workforce · US` | $20/day | `student-workforce` | Students, educators, veterans, job-placement programs |

**Sitelinks (6):** [[Extensions#Sitelinks (6) — live Phase 1]] — exam prep + bank lead; no discount sitelinks until the verified discount flow exists.

**Final URL:**

```
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_core_us&utm_content=core-exam-prep
```

Track URLs and campaign-specific messages: [[Sec+ Three-Campaign US Plan#Budget structure]]

---

## Products or services to advertise

**Category:** Education & training → Test preparation

| # | Product / service name | Description (paste under name in Google Ads) |
|---|------------------------|-----------------------------------------------|
| 1 | Security+ 30-Day Exam Prep Access | 30 days of SY0-701 exam prep in your browser: 1000+ blueprint-verified practice questions, adaptive review, progress tracking, 34 PBQ scenarios, and 90-min timed exam with scorecard. $19.99 one-time. |
| 2 | Security+ Practice Questions | 1000+ SY0-701 MCQ bank tagged to objective IDs with verified explanations, adaptive review, and timed exam. Browser Test Preparation Site. |
| 3 | Security+ Timed Exam Simulation | 90-minute mixed MCQ + PBQ run with domain scorecard review. Included with 30-day portal access. |
| 4 | Security+ PBQ Scenarios | 34 performance-based scenarios—chain labs, drag-drop, hot spots, IR exhibits—in browser. Included with full exam prep access. |

---

## Pre-launch checks

- [ ] Stripe `secplus-portal-30d` ($19.99) live
- [ ] Checkout works on cert home (desktop + mobile)
- [ ] GA4 `begin_checkout` fires for `secplus_portal_30d`
- [ ] `secplus-home-conversion.js` — test all three `utm_campaign` URLs from [[Sec+ Three-Campaign US Plan#Budget structure]]
- [ ] Cert home loads: `/comptia-sec+-home.html`
- [ ] Keyword Planner worksheet filled — [[Sec+ Keywords#Keyword Planner worksheet]]

---

## Week 1 ops

Launch as paused drafts first. If cash flow needs control, start with **Core Exam Prep** for 48–72 hours, then enable Gov and Workforce. Do not change budget, bidding, geo, or RSA for 7 days after each launch.

| Day | Action |
|-----|--------|
| 1 | Confirm ads serving · GA4 checkout on test click |
| 3 | Search terms → add negatives |
| 7 | Keyword review — adjust bids based on keyword results, search terms, checkout quality |

[[README|← Sec+ Campaign folder]]

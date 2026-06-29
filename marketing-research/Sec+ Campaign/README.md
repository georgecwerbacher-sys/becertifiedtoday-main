---
type: moc
product: secplus
tags:
  - marketing
  - google-ads
  - security+
  - secplus
---

# Sec+ Campaign

**Security+ SY0-701** — Google Search campaign setup for the paid acquisition test.

**Current direction (2026-06-27):** Build **one US-only Search campaign** with **three intent-matched ad groups** and a shared **$25/day** campaign budget. Let Google determine the spend split based on ad group output. Do not split into separate campaigns until conversion data proves a reason.

| Setting | Value |
|---------|-------|
| **Campaign structure** | **1 Search campaign** · **3 ad groups** |
| **Campaign name** | `Security+ SY0-701 · US Search` |
| **Ad groups** | `Core Exam Prep` · `Military Gov 8140` · `Student Workforce` |
| **Budget** | **$25/day shared campaign budget** |
| **Max CPC** | **$2.75** |
| **Landing** | `/comptia-sec+-home.html` |
| **utm_campaign** | `secplus_portal` |
| **Ad group tracking** | `utm_content=core-exam-prep`, `mil-gov-8140`, `student-workforce` |
| **Legacy baseline** | Keep `secplus_portal` history; do not delete |

---

## Start Here

| Note | Purpose |
|------|---------|
| [[Sec+ One-Campaign Ad Group Plan\|One-campaign ad group plan]] | **Current source of truth** — $25/day, three ad groups, US only |
| [[Sec+ Notes\|Sec+ Notes]] | Step-by-step Google Ads setup |
| [[Sec+ Google Ads Build Checklist\|Google Ads build checklist]] | Click-by-click build checklist |
| [[Security+ Campaign\|Campaign shell]] | Paste-ready campaign settings, URLs, and products |
| [[Sec+ Keywords\|Sec+ Keywords]] | Keyword/ad-group split + negatives |
| [[Sec+ RSA Copy\|Sec+ RSA Copy]] | Headlines and descriptions |
| [[Extensions\|Extensions]] | Sitelinks, URL exclusions, and geo notes |
| [[secplus-campaign-checklist.csv\|secplus-campaign-checklist.csv]] | Spreadsheet checklist for Google Ads setup |
| [[secplus-campaign-checklist-README.txt\|Google checklist README]] | Numbers column guide |

---

## Shared Strategy

| Note | Purpose |
|------|---------|
| [[Sec+ Positioning\|Sec+ Positioning]] | Voice, proof points, free vs paid rules |
| [[Sec+ Phase 2 Institutional Targeting\|Phase 2 institutional]] | Future students, veterans, government, workforce targeting |
| [[Sec+ CAE College Target List\|CAE college target list]] | Future school/campus targeting research |

**Registry:** `server-lib/campaign-marketing-registry.js` → id **`secplus_portal`**

**Promo spend:** [[Google Ads Spend Promo]] · [[google-ads-spend-promo-2026.csv]]

---

## Quick Links

- Core ad group landing: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=core-exam-prep
- Gov ad group landing: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=mil-gov-8140
- Workforce ad group landing: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=student-workforce
- [[Campaigns]] · [[Site Mission]]

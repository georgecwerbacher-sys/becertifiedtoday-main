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

**Security+ SY0-701** — live **Google Search** campaign. All setup copy lives in this folder.

**Direction (2026-06-27):** **US-only three-campaign structure** at **$20/day each** for core exam prep, military/government, and student/workforce audiences ([[Sec+ Three-Campaign US Plan]]). Test preparation and work-required cert audiences remain the message focus ([[Sec+ Phase 2 Institutional Targeting]]).

| Setting | Value |
|---------|--------|
| **Campaign structure** | **3 US-only Search campaigns** — see [[Sec+ Three-Campaign US Plan]] |
| **Campaign names** | `Core Exam Prep · US`, `Military Gov 8140 · US`, `Student Workforce · US` |
| **Budget** | **$20.00/day each** · **$60/day total** |
| **Max CPC** | **$2.75** |
| **Landing** | `/comptia-sec+-home.html` |
| **utm_campaign** | `secplus_core_us`, `secplus_gov_us`, `secplus_workforce_us` |
| **Legacy baseline** | `secplus_portal` *(keep history; do not delete)* |

**AdWords checklist:** [[secplus-campaign-checklist.csv]] — paste 67 keywords + negatives + RSA into Google Ads (Numbers). Regenerate: `npm run sync:secplus-checklist`

**Keyword source:** [[secplus-keywords.csv]] · **changes:** [[secplus-keyword-changelog.csv|keyword changelog]] · **64** positives · live export [[google-ads-keyword-export-2026-06-23.csv]] · overview [[google-ads-overview-2026-06-25/README.txt|2026-06-25]] · strategy notes: [[Sec+ Keywords#All positive keywords (64)]]

---

## Google Ads docs

| Note | Purpose |
|------|---------|
| [[Sec+ Notes\|Sec+ Notes]] | **Start here** — step-by-step Google build |
| [[Sec+ Google Ads Build Checklist\|Google Ads build checklist]] | **Click-by-click checklist to build all 3 campaigns** |
| [[Security+ Campaign\|Campaign shell]] | Campaign settings, budget, conversions, products |
| [[Sec+ Three-Campaign US Plan\|Three-campaign US plan]] | **$20/day each · US only · ad schedule · week-1 bid hold** |
| [[Sec+ CAE College Target List\|CAE college target list]] | **Large CAE schools with Security+ mapped AAS/BS tracks** |
| [[Sec+ Keywords\|Sec+ Keywords]] | PBQ keywords + negatives |
| [[Sec+ RSA Copy\|Sec+ RSA Copy]] | Headlines & descriptions — `Security+ PBQ Practice` |
| [[Extensions\|Extensions]] | Sitelinks · display paths · UTM map |
| [[secplus-campaign-checklist.csv\|secplus-campaign-checklist.csv]] | Keywords, negatives, RSA (paste into Google Ads) |
| [[secplus-campaign-checklist-README.txt\|Google checklist README]] | Numbers column guide |
| [[../Tools/Sec+ Campaign Keywords\|Tools · keyword workflow]] | Numbers filter steps for pasting keywords |

---

## Shared

| Note | Purpose |
|------|---------|
| [[Sec+ Positioning\|Sec+ Positioning]] | Voice, proof points, free vs paid rules |
| [[Sec+ Phase 2 Institutional Targeting\|Phase 2 institutional]] | **Students, educators, veterans, workforce programs, discount verify, geo** |
| [[Sec+ Phase 1 Purpose\|Phase 1 purpose]] | **Budget rules, stable, break-even — read first** |
| [[Sec+ Phase 1 Scorecard\|Phase 1 scorecard]] | **Numeric goals, cutback playbook, monthly CSV** |
| [[Sec+ Phase 1 Action Plan\|Phase 1 action plan]] | **What you do each week · experiment menu** |

**Registry:** `server-lib/campaign-marketing-registry.js` → id **`secplus_portal`**

**Admin tracker:** [/admin/#section-campaigns](https://becertifiedtoday.com/admin/#section-campaigns) — GA4 sessions + `begin_checkout` + 21-day projection

**Promo spend ($500 → $1k credit by Jul 19):** [[Google Ads Spend Promo]] · [[google-ads-spend-promo-2026.csv]]

---

## Quick links

- Core campaign landing: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_core_us&utm_content=core-exam-prep
- Gov campaign landing: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_gov_us&utm_content=mil-gov-8140
- Workforce campaign landing: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_workforce_us&utm_content=student-workforce
- [[Campaigns]] · [[Site Mission]]

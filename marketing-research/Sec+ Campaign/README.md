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

| Setting | Value |
|---------|--------|
| **Campaign name** | `Security+ SY0-701 · Exam prep · becertifiedtoday` |
| **Ad group** | **`Security+ PBQ Practice`** (only) |
| **Budget** | **$15.00/day** |
| **Max CPC** | **$2.75** |
| **Landing** | `/comptia-sec+-home.html` |
| **utm_campaign** | `secplus_portal` |
| **utm_content** | `pbq-wedge` |

**AdWords checklist:** [[secplus-campaign-checklist.csv]] — paste 67 keywords + negatives + RSA into Google Ads (Numbers). Regenerate: `npm run sync:secplus-checklist`

**Keyword source:** [[secplus-keywords.csv]] · **64** positives (generic practice-questions tier removed 2026-06-25) · live export [[google-ads-keyword-export-2026-06-23.csv]] · overview [[google-ads-overview-2026-06-25/README.txt|2026-06-25]] · strategy notes: [[Sec+ Keywords#All positive keywords (64)]]

---

## Google Ads docs

| Note | Purpose |
|------|---------|
| [[Sec+ Notes\|Sec+ Notes]] | **Start here** — step-by-step Google build |
| [[Security+ Campaign\|Campaign shell]] | Campaign settings, budget, conversions, products |
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
| [[Sec+ Phase 1 Purpose\|Phase 1 purpose]] | **Budget rules, stable, break-even — read first** |
| [[Sec+ Phase 1 Scorecard\|Phase 1 scorecard]] | **Numeric goals, cutback playbook, monthly CSV** |
| [[Sec+ Phase 1 Action Plan\|Phase 1 action plan]] | **What you do each week · experiment menu** |

**Registry:** `server-lib/campaign-marketing-registry.js` → id **`secplus_portal`**

**Admin tracker:** [/admin/#section-campaigns](https://becertifiedtoday.com/admin/#section-campaigns) — GA4 sessions + `begin_checkout` + 21-day projection

**Promo spend ($500 → $1k credit by Jul 19):** [[Google Ads Spend Promo]] · [[google-ads-spend-promo-2026.csv]]

---

## Quick links

- Google landing: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=pbq-wedge
- [[Campaigns]] · [[Site Mission]]

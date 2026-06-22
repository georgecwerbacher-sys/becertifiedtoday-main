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

**Single Google Ads campaign, single ad group** — Security+ SY0-701 PBQ practice. All setup copy lives in this folder.

**AdWords checklist:** [[secplus-campaign-checklist.csv]] — paste 67 keywords + negatives + RSA into Google Ads (Numbers). Regenerate: `npm run sync:secplus-checklist`

**Keyword source:** [[secplus-keywords.csv]] · strategy notes: [[Sec+ Keywords#All positive keywords (67)]]

| Note | Purpose |
|------|---------|
| [[Sec+ Notes\|Sec+ Notes]] | **Start here** — step-by-step build checklist |
| [[Security+ Campaign\|Campaign shell]] | Campaign settings, budget, conversions, products |
| [[Sec+ Keywords\|Sec+ Keywords]] | PBQ keywords + negatives |
| [[Sec+ RSA Copy\|Sec+ RSA Copy]] | Headlines & descriptions — `Security+ PBQ Practice` |
| [[Sec+ Positioning\|Sec+ Positioning]] | Voice, proof points, free vs paid rules |
| [[Extensions\|Extensions]] | Sitelinks · display paths · UTM map |
| [[secplus-campaign-checklist.csv\|secplus-campaign-checklist.csv]] | **AdWords checklist** — keywords, negatives, RSA (paste into Google Ads) |
| [[secplus-campaign-checklist-README.txt\|checklist README]] | Numbers column guide |
| [[secplus-keywords.csv\|secplus-keywords.csv]] | Keyword source CSV — edit then `npm run sync:secplus-checklist` |
| [[../Tools/Sec+ Campaign Keywords\|Tools · keyword workflow]] | Numbers filter steps for pasting keywords |

**Registry:** `server-lib/campaign-marketing-registry.js` → id `secplus_portal`

---

## Campaign

| Setting | Value |
|---------|--------|
| **Campaign name** | `Security+ SY0-701 · Exam prep · becertifiedtoday` |
| **Ad group** | **`Security+ PBQ Practice`** (only) |
| **utm_campaign** | `secplus_portal` |
| **utm_content** | `pbq-wedge` |
| **Budget** | **$20.00/day** |
| **Max CPC** | **$2.75** |
| **Conversion** | GA4 `begin_checkout` (`secplus_portal_10d`, `secplus_portal_30d`) |
| **Landing** | `/secplus/pbq-practice-browser.html` |
| **Geo** | US, CA, UK, AU · presence only |

**Offer:** Interactive PBQ prep in browser — **34 scenarios**, 1000+ MCQs, timed sim with scorecard — **$9.99/10d** · **$19.99/30d**.

Full positioning: [[Sec+ Positioning]]

---

## Quick links

- Landing: https://becertifiedtoday.com/secplus/pbq-practice-browser.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=pbq-wedge
- [[Campaigns]] · [[Site Mission]]

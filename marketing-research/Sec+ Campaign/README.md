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

**Import:** [[secplus-keywords.csv]] (67 positives, ranked 1–67) · full paste list: [[Sec+ Keywords#All positive keywords (67)]]

| Note | Purpose |
|------|---------|
| [[Sec+ Notes\|Sec+ Notes]] | **Start here** — step-by-step build checklist |
| [[Security+ Campaign\|Campaign shell]] | Campaign settings, budget, conversions, products |
| [[Sec+ Keywords\|Sec+ Keywords]] | PBQ keywords + negatives |
| [[secplus-keywords.csv\|secplus-keywords.csv]] | Import-ready keywords (Campaign + Match type columns) |
| [[Sec+ RSA Copy\|Sec+ RSA Copy]] | Headlines & descriptions — `Security+ PBQ Practice` |
| [[Sec+ Positioning\|Sec+ Positioning]] | Voice, proof points, free vs paid rules |
| [[Extensions\|Extensions]] | Sitelinks · display paths · UTM map |
| [[secplus-campaign-checklist.csv\|secplus-campaign-checklist.csv]] | Row-by-row Google Ads setup CSV |

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

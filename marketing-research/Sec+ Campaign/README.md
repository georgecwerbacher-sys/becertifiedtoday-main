---
type: moc
product: secplus
tags:
  - marketing
  - google-ads
  - reddit
  - security+
  - secplus
---

# Sec+ Campaign

**Security+ SY0-701** marketing — Google Search + Reddit paid ads. All setup copy lives in this folder.

| Channel | Start here | Budget |
|---------|------------|--------|
| **Google Ads** | [[Sec+ Notes\|Sec+ Notes]] | **$20/day** · one campaign, one ad group |
| **Reddit Ads** | [[Sec+ Reddit Notes\|Sec+ Reddit Notes]] | **$10/day** shared pool · launch PBQ first |

---

## Google Ads

**AdWords checklist:** [[secplus-campaign-checklist.csv]] — paste 67 keywords + negatives + RSA into Google Ads (Numbers). Regenerate: `npm run sync:secplus-checklist`

**Keyword source:** [[secplus-keywords.csv]] · strategy notes: [[Sec+ Keywords#All positive keywords (67)]]

| Note | Purpose |
|------|---------|
| [[Sec+ Notes\|Sec+ Notes]] | Step-by-step Google build checklist |
| [[Security+ Campaign\|Campaign shell]] | Campaign settings, budget, conversions, products |
| [[Sec+ Keywords\|Sec+ Keywords]] | PBQ keywords + negatives |
| [[Sec+ RSA Copy\|Sec+ RSA Copy]] | Headlines & descriptions — `Security+ PBQ Practice` |
| [[Extensions\|Extensions]] | Sitelinks · display paths · UTM map |
| [[secplus-campaign-checklist.csv\|secplus-campaign-checklist.csv]] | Keywords, negatives, RSA (paste into Google Ads) |
| [[secplus-campaign-checklist-README.txt\|Google checklist README]] | Numbers column guide |
| [[../Tools/Sec+ Campaign Keywords\|Tools · keyword workflow]] | Numbers filter steps for pasting keywords |

---

## Reddit Ads

**Reddit checklist:** [[secplus-reddit-checklist.csv]] — paste steps into ads.reddit.com (Numbers)

| Note | Purpose |
|------|---------|
| [[Sec+ Reddit Notes\|Sec+ Reddit Notes]] | **Start here** — step-by-step Reddit build |
| [[Sec+ campaign — Reddit only\|Reddit campaign shell]] | Single-page ads.reddit.com settings |
| [[Sec+ Reddit Copy\|Sec+ Reddit Copy]] | Headlines, body, image text, A/B log |
| [[secplus-reddit-checklist.csv\|secplus-reddit-checklist.csv]] | Checklist CSV for Numbers |
| [[secplus-reddit-checklist-README.txt\|Reddit checklist README]] | Column guide |

**Organic (parallel):** [[../Reddit/posting/Sec+ replies\|Sec+ replies]] · [[../Reddit/posting/Voice guide\|Voice guide]] · [[../Reddit/posting/Post log\|Post log]]

---

## Shared

| Note | Purpose |
|------|---------|
| [[Sec+ Positioning\|Sec+ Positioning]] | Voice, proof points, free vs paid rules |
| [[secplus-keywords.csv\|secplus-keywords.csv]] | Keyword source CSV — edit then `npm run sync:secplus-checklist` |

**Registry:** `server-lib/campaign-marketing-registry.js` → ids `secplus_portal` (Google) · `secplus_wedge_pbq_reddit` (Reddit)

**Admin tracker:** [/admin/#section-campaigns](https://becertifiedtoday.com/admin/#section-campaigns) — GA4 sessions + `begin_checkout` · copy destination URL

---

## Google campaign

| Setting | Value |
|---------|--------|
| **Campaign name** | `Security+ SY0-701 · Exam prep · becertifiedtoday` |
| **Ad group** | **`Security+ PBQ Practice`** (only) |
| **utm_campaign** | `secplus_portal` |
| **utm_content** | `pbq-wedge` |
| **Budget** | **$20.00/day** |
| **Max CPC** | **$2.75** |
| **Landing** | `/comptia-sec+-home.html` |

---

## Reddit campaign

| Setting | Value |
|---------|--------|
| **Campaign name** | `SEC+_Wedge_Reddit` |
| **Communities** | `r/CompTIA`, `r/SecurityPlus` |
| **utm_campaign** | `secplus_wedge_pbq` |
| **utm_content** | `reddit-pbq` |
| **Budget** | **$10/day** (shared with CCNA Reddit) |
| **Landing** | `/comptia-sec+-home.html` |
| **Account** | u/BeCertifiedToday |

Full positioning: [[Sec+ Positioning]]

---

## Quick links

- Google landing: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=pbq-wedge
- Reddit landing: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=reddit&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=reddit-pbq
- [[Campaigns]] · [[Site Mission]] · [[../Reddit/README\|Reddit hub]]

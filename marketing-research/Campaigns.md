---
type: moc
tags:
  - marketing
  - google-ads
---

# Campaigns

Source of truth: [[Site Mission]] · `server-lib/campaign-marketing-registry.js`

## Active: Security+ Google Search · 21-day test

**Campaign:** `Security+ SY0-701 · Exam prep · becertifiedtoday`  
**Ad group:** **`Security+ PBQ Practice`** (only)  
**Budget:** **$15.00/day** · max CPC **$2.75**  
**Landing:** `/comptia-sec+-home.html`  
**utm_campaign:** `secplus_portal` · **utm_content:** `pbq-wedge`

**Obsidian home:** [[Sec+ Campaign/README|Sec+ Campaign]] — all setup copy in one folder

| Item | Link |
|------|------|
| **Start here** | [[Sec+ Campaign/Sec+ Notes\|Sec+ Notes]] |
| Campaign shell | [[Sec+ Campaign/Security+ Campaign\|Campaign shell]] |
| Keywords | [[Sec+ Campaign/Sec+ Keywords\|Sec+ Keywords]] · [[Sec+ Campaign/secplus-keywords.csv\|keywords CSV]] |
| RSA copy | [[Sec+ Campaign/Sec+ RSA Copy\|Sec+ RSA Copy]] |
| Extensions | [[Sec+ Campaign/Extensions\|Extensions]] |
| Checklist CSV | [[Sec+ Campaign/secplus-campaign-checklist.csv\|secplus-campaign-checklist.csv]] |
| Landing | https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=pbq-wedge |

**During the test:** collect data for 21 days — track sessions, `begin_checkout`, and Stripe Sec+ purchases in [/admin/#section-campaigns](https://becertifiedtoday.com/admin/#section-campaigns). Add campaign negatives only for obvious junk search terms.

**Before changes:** compare search terms, CPA, and checkout rate at day 21 before scaling budget or bids.

## Landing page

- **Paid traffic:** `/comptia-sec+-home.html` (final URL + sitelinks)
- **Organic only:** `/secplus/pbq-practice-browser.html` (not used in ads)

## Related

- Guest page copy sync: `scripts/sync-guest-page-marketing.py`
- Purchase conversion tag: `public/js/google-ads-purchase-conversion.js`
- Admin projection: `server-lib/campaign-marketing-report.js`

## CCNA Automation (200-901)

Question and lab hunt checklist (not Google Ads):

- [[../CCNA-Auto/README|CCNA-Auto]] · [[../CCNA-Auto/blueprint-hunt-list|Blueprint hunt list]]

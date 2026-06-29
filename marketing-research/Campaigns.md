---
type: moc
tags:
  - marketing
  - google-ads
---

# Campaigns

Source of truth: [[Site Mission]] · `server-lib/campaign-marketing-registry.js`

## Active: Security+ Google Search Setup

**Campaign:** `Security+ SY0-701 · US Search`  
**Ad groups:** `Core Exam Prep` · `Military Gov 8140` · `Student Workforce`  
**Budget:** **$25/day shared** · max CPC **$2.75**  
**Landing:** `/comptia-sec+-home.html`  
**utm_campaign:** `secplus_portal` · **utm_content:** ad-group specific

**Obsidian home:** [[Sec+ Campaign/README|Sec+ Campaign]] — all setup copy in one folder

| Item | Link |
|------|------|
| **Start here** | [[Sec+ Campaign/Sec+ Notes\|Sec+ Notes]] |
| Campaign shell | [[Sec+ Campaign/Security+ Campaign\|Campaign shell]] |
| Keywords | [[Sec+ Campaign/Sec+ Keywords\|Sec+ Keywords]] · [[Sec+ Campaign/secplus-keywords.csv\|keywords CSV]] |
| RSA copy | [[Sec+ Campaign/Sec+ RSA Copy\|Sec+ RSA Copy]] |
| Extensions | [[Sec+ Campaign/Extensions\|Extensions]] |
| Checklist CSV | [[Sec+ Campaign/secplus-campaign-checklist.csv\|secplus-campaign-checklist.csv]] |
| Landing | https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=core-exam-prep |

Use Google Ads for campaign spend/clicks and Stripe checkout/admin purchase records for completed Sec+ purchases. Add campaign negatives only for obvious junk search terms.

## Landing page

- **Paid traffic:** `/comptia-sec+-home.html` (final URL + sitelinks)
- **Organic only:** `/secplus/pbq-practice-browser.html` (not used in ads)

## Related

- Guest page copy sync: `scripts/sync-guest-page-marketing.py`
- Purchase conversion tag: `public/js/google-ads-purchase-conversion.js`

## CCNA Automation (200-901)

Question and lab hunt checklist (not Google Ads):

- [[../CCNA-Auto/README|CCNA-Auto]] · [[../CCNA-Auto/blueprint-hunt-list|Blueprint hunt list]]

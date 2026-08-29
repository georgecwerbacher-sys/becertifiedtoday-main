---
type: moc
tags:
  - marketing
  - google-ads
---

# Campaigns

Source of truth: [[Site Mission]] · [[Advertising Ethics]] · `server-lib/campaign-marketing-registry.js`

## Ethics (required)

Do **not** bid on dump, brain dump, cheat, actual-exam, or pass-guaranteed queries. Those terms are **campaign negatives**, not positives. Do not run a dump-intercept campaign.

**In Google Ads now:** pause `Security+ SY0-701 · US Search · Dump Intercept` if it exists. Paste dump/cheat negatives from [[Sec+ Campaign/Sec+ Launch 40 Keyword Lists]] onto Launch 40. Full policy: [[Advertising Ethics]].

## Active: Security+ Google Search · Launch 40 (24h trial)

**Campaign:** `Security+ SY0-701 · US Search · Launch 40`  
**Ad groups:** `24h Trial` (primary) · `Timed Simulation` · `Verified Adaptive Prep` · `After Study Sprint` · `Student College`  
**Budget:** **$465 total** · **$15/day shared** · no end date · pause at cap · max CPC **$2.50–$2.75**  
**Offer:** **24 hours free**, then **$15.99** / 30 days (`SECPLUS24`) while the trial is active · list **$19.99** without trial  
**Landing:** `/comptia-sec+-home.html` (top of fold)  
**utm_campaign:** `secplus_portal_launch40` · **utm_content:** `24h-trial` · `timed-sim` · `verified-adaptive` · `after-study` · `student-college`

**Start here:** [[Sec+ Campaign/Sec+ Launch 40 Build Checklist|Launch 40 checklist]] · [[Sec+ Campaign/Sec+ Launch 40 Campaign Plan|Campaign plan]] · [[Sec+ Campaign/Sec+ Launch 40 RSA Copy|RSA paste]]

## Retired: Dump Intercept (do not run)

**Campaign:** `Security+ SY0-701 · US Search · Dump Intercept`  
**Status:** **Retired.** Pause in Google Ads. Do not rebuild.  
**Why:** Bidding on dump/cheat searches is off-policy even if ads never say “dump.” See [[Advertising Ethics]].

Archive only: [[Sec+ Campaign/Sec+ Dump Intercept Campaign Plan]] · [[Sec+ Campaign/Sec+ Dump Intercept Keyword Lists]]

## Analytics & improvement loop

| Step | Tool |
|------|------|
| Ad group performance (`utm_content`) | [/admin#section-secplus-ad-groups](https://becertifiedtoday.com/admin#section-secplus-ad-groups) |
| Conversion recommendations | [/admin#section-recommendations](https://becertifiedtoday.com/admin#section-recommendations) |
| Daily spend / copy log | [/admin#section-daily-log](https://becertifiedtoday.com/admin#section-daily-log) |
| Code registry | `server-lib/secplus-google-ad-groups.js` |
| Weekly GA4 archive | `node scripts/marketing-weekly-report.mjs` → [[Weekly Reports]] |

Full workflow: [[Sec+ Campaign/Sec+ One-Campaign Ad Group Plan#Analytics monitoring loop (admin + Obsidian)]]

| Item | Link |
|------|------|
| **Start here** | [[Sec+ Campaign/Sec+ Notes\|Sec+ Notes]] |
| Campaign shell | [[Sec+ Campaign/Security+ Campaign\|Campaign shell]] |
| Keywords | [[Sec+ Campaign/Sec+ Keywords\|Sec+ Keywords]] · [[Sec+ Campaign/secplus-keywords.csv\|keywords CSV]] |
| RSA copy | [[Sec+ Campaign/Sec+ RSA Copy\|Sec+ RSA Copy]] (Core) · [[Sec+ Campaign/Sec+ RSA Copy - Military Gov 8140\|Military]] · [[Sec+ Campaign/Sec+ RSA Copy - Student Workforce\|Student]] |
| Extensions | [[Sec+ Campaign/Extensions\|Extensions]] |
| Checklist CSV | [[Sec+ Campaign/secplus-campaign-checklist.csv\|secplus-campaign-checklist.csv]] |
| Landing | https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=core-exam-prep |

Use Google Ads for campaign spend/clicks and Stripe checkout/admin purchase records for completed Sec+ purchases. Add campaign negatives for dump, cheat, actual-exam, and other junk search terms. See [[Advertising Ethics]].

## Landing page

- **Paid traffic:** `/comptia-sec+-home.html` (final URL + sitelinks)
- **Organic only:** `/secplus/pbq-practice-browser.html` (not used in ads)

## Related

- Guest page copy sync: `scripts/sync-guest-page-marketing.py`
- Purchase conversion tag: `public/js/google-ads-purchase-conversion.js`

## CCNA Automation (200-901)

Question and lab hunt checklist (not Google Ads):

- [[../CCNA-Auto/README|CCNA-Auto]] · [[../CCNA-Auto/blueprint-hunt-list|Blueprint hunt list]]

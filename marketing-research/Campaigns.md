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

**In Google Ads now:** pause `Security+ SY0-701 · US Search · Dump Intercept` if it exists. Pause Launch 40. Paste dump/cheat negatives from [[Sec+ Campaign/Sec+ Sep 430 Keyword Lists]] onto Sep 430. Full policy: [[Advertising Ethics]].

## Active: Security+ Google Search · Sep 430

**Campaign:** `Security+ SY0-701 · US Search · Sep 430`  
**Ad group:** `Exam Prep`  
**Budget:** **$430 total** · **$14/day shared** · flight **2026-09-02 → 2026-10-02** · pause at cap · max CPC **$2.50**  
**Offer in ads:** **$19.99** / 30 days · one payment · no subscription  
**Landing:** `/comptia-sec+-home.html` (top of fold)  
**utm_campaign:** `secplus_portal_sep430` · **utm_content:** `exam-prep`

Do **not** advertise the first-visit 15-minute 50% off (`SEP50PERCENTOFF`) in RSA. Ads clickers who already visited will not get that clock.

**Start here:** [[Sec+ Campaign/Sec+ Sep 430 Build Checklist|Sep 430 checklist]] · [[Sec+ Campaign/Sec+ Sep 430 Campaign Plan|Campaign plan]] · [[Sec+ Campaign/Sec+ Sep 430 RSA Copy|RSA paste]] · [[Sec+ Campaign/Sec+ Sep 430 Keyword Lists|Keywords]]

## Paused: Launch 40 (24h trial)

**Campaign:** `Security+ SY0-701 · US Search · Launch 40`  
**Status:** **Paused.** 24h-trial RSA is stale. Pause so Sep 430 spend is not split.  
Archive: [[Sec+ Campaign/Sec+ Launch 40 Campaign Plan]] · [[Sec+ Campaign/Sec+ Launch 40 RSA Copy]]

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
| **Start here** | [[Sec+ Campaign/Sec+ Sep 430 Build Checklist\|Sep 430 checklist]] |
| Campaign plan | [[Sec+ Campaign/Sec+ Sep 430 Campaign Plan\|Sep 430 plan]] |
| Keywords | [[Sec+ Campaign/Sec+ Sep 430 Keyword Lists\|Sep 430 keywords]] |
| RSA copy | [[Sec+ Campaign/Sec+ Sep 430 RSA Copy\|Sep 430 RSA]] |
| Extensions | [[Sec+ Campaign/Extensions\|Extensions]] |
| Landing | https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal_sep430&utm_content=exam-prep |

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

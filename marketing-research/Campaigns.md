---
type: moc
tags:
  - marketing
  - google-ads
---

# Campaigns

Source of truth: [[Site Mission]] · `server-lib/campaign-marketing-registry.js`

## Active: initial 7-day AdWords test

**Window:** 2026-06-14 → 2026-06-21 · **Review:** 2026-06-22

| Campaign | Budget | Live ad groups | Goal |
|----------|--------|----------------|------|
| [[campaigns/CCNA Campaign|CCNA]] | $25/day | **`ccna_portal_10v1` only** (browser_labs next) | Baseline CTR, CPC, checkout rate |
| [[campaigns/ENCOR Campaign|ENCOR]] | $10/day | `encor_portal` | Baseline CTR, CPC, checkout rate |

**During the test:** collect data only — no budget increases, no new countries, no bidding changes. **`ccna_browser_labs` stays paused** until portal_10v1 baseline is reviewed. Add campaign negatives only for obvious junk search terms.

**Day 7 review:** compare ad groups, note top search terms, decide scale / pause / optimize before week 2.

## CCNA 200-301

**Primary doc:** [[campaigns/CCNA Campaign|CCNA Campaign]] — one campaign, two ad groups, **$25/day**

| Item | Link |
|------|------|
| Setup checklist (CSV) | [[campaigns/ccna-campaign-checklist.csv|checklist]] |
| Checklist guide | [[campaigns/ccna-campaign-checklist-README|README]] |
| Extended reference | [[campaigns/ccna-portal-10d|locations · products · metros]] |

| Ad group | Budget | Focus |
|----------|--------|-------|
| `ccna_portal_10v1` | ~$17/day | Practice tests, mock exams, question bank |
| `ccna_browser_labs` | ~$8/day | Browser CLI labs, no GNS3/Packet Tracer |

## ENCOR 350-401

**Primary doc:** [[campaigns/ENCOR Campaign|ENCOR Campaign]] — one campaign, one ad group, **$10/day**

| Item | Link |
|------|------|
| Setup doc (markdown) | [[campaigns/encor-portal|encor-portal-10d-google-ads.md]] |
| Setup doc (plain text) | [[campaigns/encor-portal.txt|encor-portal-10d-google-ads.txt]] |

| Ad group | Budget | Focus |
|----------|--------|-------|
| `encor_portal` | $10/day | 30-day $19.99 portal · `utm_content=portal-30d` |

**Do not** use `utm_content=portal-10d` — $9.99 / 10-day is an on-page popup only.

## Security+ SY0-701

| utm_campaign | Daily budget | Setup doc |
|--------------|--------------|-----------|
| `secplus_portal` | $10 | [[campaigns/secplus-portal-10d|Security+ portal 10d]] |

## Landing pages

- CCNA → `/ccna-home.html#purchase`
- ENCOR → `/ccnp-home.html#purchase`
- Security+ → `/comptia-sec+-home.html#purchase`

## Related

- Guest page copy sync: `scripts/sync-guest-page-marketing.py`
- Purchase conversion tag: `public/js/google-ads-purchase-conversion.js`

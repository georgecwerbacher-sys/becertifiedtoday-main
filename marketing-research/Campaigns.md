---
type: moc
tags:
  - marketing
  - google-ads
---

# Campaigns

Source of truth: [[Site Mission]] · [[Wedge Marketing plan/Wedge Marketing plan|Wedge Marketing plan]] · `server-lib/campaign-marketing-registry.js`

## Active: initial 7-day AdWords test

**Window:** 2026-06-14 → 2026-06-21 · **Review:** 2026-06-22

| Campaign | Budget | Live ad groups | Goal |
|----------|--------|----------------|------|
| [[campaigns/CCNA Campaign|CCNA]] | $25/day | **`ccna_portal_10v1` only** (browser_labs next) | Baseline CTR, CPC, checkout rate |
| [[campaigns/ENCOR Campaign|ENCOR]] | $10/day | `encor_portal` | Baseline CTR, CPC, checkout rate |

**During the test:** collect data only — no budget increases, no new countries, no bidding changes. **`ccna_browser_labs` stays paused** until portal_10v1 baseline is reviewed. Add campaign negatives only for obvious junk search terms.

**Day 7 review:** compare ad groups, note top search terms, decide scale / pause / optimize before week 2.

**Wedge pivot:** If head-term CPC is untenable, launch [[campaigns/CCNA Wedge Lab Campaign|CCNA_Wedge_Lab]] — follow [[Wedge Marketing plan/02-keywords-and-google-ads|Keywords & Google Ads]] and [[Wedge Marketing plan/06-30-day-action-plan|30-day action plan]]. Rationale: [[Wedge Marketing plan/00-why-ccna-marketing-changed|Why CCNA marketing changed]].

## CCNA_Wedge_Lab (ready to build)

**Primary doc:** [[campaigns/CCNA Wedge Lab Campaign|CCNA Wedge Lab Campaign]] — dedicated wedge Search campaign, **$15/day** launch

| Item | Link |
|------|------|
| Setup checklist (CSV) | `scripts/ccna-wedge-lab-google-ads-checklist.csv` |
| Checklist guide | `scripts/ccna-wedge-lab-google-ads-README.txt` |
| Setup guide | `scripts/ccna-wedge-lab-google-ads.md` |
| Landing | https://becertifiedtoday.com/ccna/labs-without-gns3.html |

| Ad group | Budget | Focus |
|----------|--------|-------|
| **`CCNA_Wedge_Lab`** | $15/day | Browser CLI labs · no GNS3 · wedge landing |

**Before enable:** pause `ccna_browser_labs` in the combined CCNA campaign.

## CCNA 200-301 (combined)

**Primary doc:** [[campaigns/CCNA Campaign|CCNA Campaign]] — one campaign, two ad groups, **$25/day**

| Item | Link |
|------|------|
| **Obsidian build steps** | [[campaigns/CCNA campaign build steps|CCNA campaign build steps]] |
| Setup checklist (CSV) | `scripts/ccna-google-ads-campaign-checklist.csv` |
| Checklist guide | `scripts/ccna-google-ads-campaign-checklist-README.txt` |
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

## SEC+_Wedge_PBQ (ready to build)

**Obsidian home:** [[Sec+ Campaign/README|Sec+ Campaign]] — [[Sec+ Campaign/Sec+ Positioning|positioning]] · [[Sec+ Campaign/Sec+ Keywords|keywords]] · [[Sec+ Campaign/Sec+ RSA Copy|RSA]]

| Item | Link |
|------|------|
| Setup steps | [[Sec+ Campaign/Sec+ Notes\|Sec+ Notes]] |
| Keywords | [[Sec+ Campaign/Sec+ Keywords\|Sec+ Keywords]] |
| Deep docs | [[Wedge Marketing plan/secplus-wedge-campaign/README\|secplus-wedge-campaign/]] |
| Setup checklist (CSV) | `scripts/secplus-wedge-pbq-google-ads-checklist.csv` |
| Landing | https://becertifiedtoday.com/secplus/pbq-practice-browser.html |

| Ad group | Budget | Focus |
|----------|--------|-------|
| **`SEC+_PBQ_Scenarios`** | ~$3/day | Interactive PBQ / scenarios like test day |
| **`SEC+_Realistic_Sim`** | ~$3/day | Timed sim, adaptive review, anti-PDF, mobile |
| **`SEC+_Work_Cert`** | ~$2/day | DoD / contractor / cert required for job |

**Before enable:** Keyword Planner sign-off on [[Sec+ Campaign/Sec+ Keywords|Sec+ Keywords]].

## Security+ SY0-701 (portal baseline)

**Obsidian home:** [[Sec+ Campaign/README|Sec+ Campaign]]

| Item | Link |
|------|------|
| **Obsidian** | [[Sec+ Campaign/Sec+ Notes\|Sec+ Notes]] · [[Sec+ Campaign/Sec+ Keywords\|Keywords]] |
| Setup checklist (CSV) | `scripts/secplus-google-ads-campaign-checklist.csv` |
| Checklist guide | `scripts/secplus-google-ads-campaign-checklist-README.txt` |
| Extended reference | [[campaigns/secplus-portal-10d|secplus-portal-10d-google-ads.md]] |
| Funnel tracker | [[Wedge Marketing plan/SEC+ funnel build tracker|SEC+ funnel build tracker]] |
| **Obsidian canvas** | [[Wedge Marketing plan/canvas/SEC+ wedge funnel.canvas|SEC+ wedge funnel.canvas]] |

| Ad group | Budget | Focus |
|----------|--------|-------|
| `secplus_portal_10d` | ~$10/day | Practice tests, question bank — **low bid / baseline only** |

**Wedge pivot:** [[Wedge Marketing plan/secplus-wedge-campaign/00-why-marketing-changed|Why SEC+ marketing changed]] · Build: [[Sec+ Campaign/README|Sec+ Campaign]] · Keywords: [[Sec+ Campaign/Sec+ Keywords|Sec+ Keywords]].

## Landing pages

- CCNA → `/ccna-home.html#purchase` · wedge → `/ccna/labs-without-gns3.html`
- ENCOR → `/ccnp-home.html#purchase`
- Security+ → `/comptia-sec+-home.html#purchase` · wedge → `/secplus/pbq-practice-browser.html`

## Related

- Guest page copy sync: `scripts/sync-guest-page-marketing.py`
- Purchase conversion tag: `public/js/google-ads-purchase-conversion.js`

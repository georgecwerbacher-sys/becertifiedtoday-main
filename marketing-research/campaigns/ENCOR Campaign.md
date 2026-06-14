---
type: campaign
product: encor
utm_campaign: encor_portal
status: initial-test
test_start: 2026-06-14
test_end: 2026-06-21
tags:
  - marketing
  - google-ads
  - encor
---

# ENCOR Campaign

> **Initial AdWords test** · 2026-06-14 → 2026-06-21 · $10/day · do not scale until day-7 review

**Setup doc (paste-ready):** [[campaigns/encor-portal|encor-portal-10d-google-ads.md]] · [[campaigns/encor-portal.txt|encor-portal-10d-google-ads.txt]]

Landing: `public/ccnp-home.html` — **primary purchase is 30-day access ($19.99)**. The $9.99 / 10-day tier is a one-time on-page popup only — **do not use `utm_content=portal-10d`** for this campaign.

## Campaign shell

| Setting | Value |
|---------|--------|
| Campaign name | `CCNP ENCOR 350-401 · Exam prep · becertifiedtoday` |
| Daily budget | **$10.00/day** |
| Bidding | Maximize clicks, max CPC **$2.75** |
| utm_campaign | `encor_portal` |
| utm_content | `portal-30d` (30-day $19.99 CTA) |
| Conversion | GA4 `begin_checkout` (`encor_portal_30d`) |

## Ad group

| Setting | Value |
|---------|--------|
| Ad group name | `encor_portal` |
| Display path | ENCOR / Exam-Prep |
| Final URL | `https://becertifiedtoday.com/ccnp-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=encor_portal&utm_content=portal-30d` |

## What's in the setup doc

- Tier 1 country list + optional city boosts
- 5 products to advertise (30-day primary — no 10-day product line)
- 15 RSA headlines · 4 descriptions (pin H1/H2/H3)
- 6 sitelinks
- Keywords + ad group / campaign negatives
- Keyword demand estimates + competitive analysis
- Launch checklist + site behavior notes

## Launch checklist (summary)

- [ ] Ad group `encor_portal` enabled
- [ ] Final URL → `#purchase` with `portal-30d` (not `portal-10d`)
- [ ] Products, RSA, keywords, sitelinks pasted
- [ ] Tier 1 locations (presence-only)
- [ ] GA4 `begin_checkout` imported as Primary
- [ ] Stripe `encor-portal-30d` = $19.99
- [ ] Test checkout → `begin_checkout` (`encor_portal_30d`) in GA4 Realtime

## Ad copy rules

- Headlines/descriptions: **$19.99 / 30-day** — never lead with $9.99
- $9.99 / 10-day appears once per browser via `bcc-10d-one-time-offer.js` — not guaranteed above the fold

## Initial test (7 days)

| Day | Action |
|-----|--------|
| 1 | Confirm `encor_portal` serving · check GA4 Realtime for `begin_checkout` (`encor_portal_30d`) |
| Daily | Note impressions, clicks, spend, checkouts |
| 3 | First search terms pass — add junk negatives (course, dump, ccna, ccie) |
| 7 | Review CTR, CPC, checkout rate · decide scale / pause / optimize |

**Hold during test:** budget ($10/day), bidding, Tier 1 locations only, RSA copy.

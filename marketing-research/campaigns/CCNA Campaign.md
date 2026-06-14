---
type: campaign
product: ccna
utm_campaign: ccna_portal
status: initial-test
test_start: 2026-06-14
test_end: 2026-06-21
tags:
  - marketing
  - google-ads
  - ccna
---

# CCNA Campaign

**Mission context:** [[Site Mission]]

**Live ad group:** `ccna_portal_10v1` only during 7-day test. `ccna_browser_labs` deferred.

**Working checklist:** [[campaigns/ccna-campaign-checklist.csv|ccna-google-ads-campaign-checklist.csv]] · [[campaigns/ccna-campaign-checklist-README|README]]

**Extended reference** (locations, products table, US metros): [[campaigns/ccna-portal-10d|ccna-portal-10d-google-ads.md]]

## Campaign shell

| Setting | Value |
|---------|--------|
| Campaign name | `CCNA 200-301 · Exam prep · becertifiedtoday` |
| Daily budget | **$25.00/day** |
| Bidding (weeks 1–2) | Maximize clicks, max CPC **$3.00** |
| utm_campaign | `ccna_portal` |
| Landing | `https://becertifiedtoday.com/ccna-home.html#purchase` |
| utm_content | `portal-10d` ($9.99 / 10-day CTA) |
| Conversion | GA4 `begin_checkout` (`ccna_portal_10d`, `ccna_portal_30d`) |

## Ad groups

| Ad group | Budget share | Display path | Intent |
|----------|--------------|--------------|--------|
| `ccna_portal_10v1` | ~68% (~$17/day) | CCNA / 10-Day-Access | Practice test, mock exam, question bank |
| `ccna_browser_labs` | ~32% (~$8/day) | CCNA / Browser-Labs | CLI labs, browser labs, no GNS3/PT |

Both ad groups use the same final URL:

```
https://becertifiedtoday.com/ccna-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=portal-10d
```

## Checklist phases

Track progress in the CSV (open in Numbers — see README). Phases:

1. **Pre-launch** — Stripe products, checkout test, GA4 conversion import
2. **Campaign** — $25/day budget, bidding, `ccna_portal` UTM, English
3. **Locations** — Tier A countries (presence-only)
4. **Ad group 1** — `ccna_portal_10v1` keywords + 15 headlines + 4 descriptions
5. **Ad group 2** — `ccna_browser_labs` keywords + 15 headlines + 4 descriptions
6. **Extensions** — 6 sitelinks + products list
7. **Negatives** — campaign + ad group phrase negatives
8. **Launch** — enable both ad groups, verify $9.99 checkout + GA4 Realtime
9. **Initial test (7 days)** — baseline only; daily spend + checkout checks
10. **Ops** — week 2+ search terms, CPA by ad group, scale options

## Initial test (7 days)

| Day | Action |
|-----|--------|
| 1 | Confirm `ccna_portal_10v1` serving (browser_labs paused) · check GA4 Realtime for `begin_checkout` |
| Daily | Note impressions, clicks, spend, checkouts per ad group |
| 3 | First search terms pass — add obvious junk as campaign negatives |
| 7 | Review CTR, avg CPC, CPA (`portal_10v1` vs `browser_labs`) · decide next steps |

**Hold during test:** budget, bidding, locations, RSA copy. Do not enable `ccna_browser_labs` until day-7 review.

See [[campaigns/CCNA portal 10v1 — keyword research|keyword research]] for under-realized terms and conversion-based triage.

Filter checklist **Section** = `Ops` · **Phase** = `Initial test (7 days)`.

## Headlines & descriptions

All RSA copy lives in the checklist CSV — filter **Section** = `Headline` or `Description`:

- **ccna_portal_10v1** — pin H1 `CCNA 200-301 Practice Test`, H2 `$9.99 for 10-Day Access`
- **ccna_browser_labs** — pin H1 `Browser CLI Labs — No GNS3`, H2 `$9.99 for 10-Day Access`

## Keywords (summary)

**ccna_portal_10v1** — exact: `[ccna practice test]`, `[ccna mock exam]`, `[ccna question bank]`, … · phrase: `"ccna practice test online"`, …

**ccna_browser_labs** — exact: `[ccna cli lab]`, `[ccna lab online]` · phrase: `"ccna labs without gns3"`, `"ccna labs without packet tracer"`, …

Full keyword list: checklist **Setup → Ad group 1/2** rows.

## Open in Numbers

1. Open [[campaigns/ccna-campaign-checklist.csv|checklist CSV]] in Numbers
2. Convert **Done** column to checkboxes
3. Filter by **Section** (Setup / Headline / Description / Ops)
4. Save as `.numbers` for ongoing tracking

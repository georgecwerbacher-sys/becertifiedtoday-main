---
type: campaign
product: secplus
utm_campaign: secplus_portal
status: initial-test
tags:
  - marketing
  - google-ads
  - security+
  - secplus
---

# Security+ Campaign

**Mission context:** [[Site Mission]] · Persona **Sam** in [[Wedge Marketing plan/01-positioning-and-audience|Positioning]]

**Working checklist:** [[campaigns/secplus-campaign-checklist.csv|secplus-google-ads-campaign-checklist.csv]] · `scripts/secplus-google-ads-campaign-checklist-README.txt`

**Extended reference** (locations, products table, federal metros): [[campaigns/secplus-portal-10d|secplus-portal-10d-google-ads.md]]

**Funnel tracker:** [[Wedge Marketing plan/SEC+ funnel build tracker|SEC+ funnel build tracker]]

## Campaign shell

| Setting | Value |
|---------|--------|
| Campaign name | `Security+ SY0-701 · Exam prep · becertifiedtoday` |
| Daily budget | **$10.00/day** |
| Bidding (weeks 1–2) | Maximize clicks, max CPC **$2.75** |
| utm_campaign | `secplus_portal` |
| Landing | `https://becertifiedtoday.com/comptia-sec+-home.html#purchase` |
| utm_content | `portal-10d` ($9.99 / 10-day CTA) |
| Conversion | GA4 `begin_checkout` (`secplus_portal_10d`, `secplus_portal_30d`) |

## Ad groups

| Ad group | Budget share | Display path | Intent |
|----------|--------------|--------------|--------|
| `secplus_portal_10d` | ~70% (~$7/day) | Security+ / 10-Day-Access | Practice test, question bank, SY0-701 prep |
| `secplus_pbq_wedge` | ~30% (~$3/day) | Security+ / PBQ-Practice | PBQ practice, performance-based, browser sim |

**Portal final URL:**

```
https://becertifiedtoday.com/comptia-sec+-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=portal-10d
```

**Wedge final URL** (when enabled):

```
https://becertifiedtoday.com/secplus/pbq-practice-browser.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=pbq-wedge
```

## Checklist phases

1. **Pre-launch** — Stripe products, checkout test, GA4 conversion import, purchase conversion tag on home
2. **Campaign** — $10/day budget, bidding, `secplus_portal` UTM, English
3. **Locations** — Tier A countries (presence-only); federal US metros optional boost
4. **Ad group 1** — `secplus_portal_10d` keywords + 15 headlines + 4 descriptions
5. **Ad group 2** — `secplus_pbq_wedge` keywords + RSA (enable after wedge landing verified)
6. **Extensions** — 6 sitelinks + products list
7. **Negatives** — campaign + ad group phrase negatives
8. **Launch** — enable portal ad group first; verify $9.99 checkout + GA4 Realtime
9. **Initial test (7 days)** — baseline only
10. **Ops** — week 2+ search terms, CPA by ad group

## Initial test (7 days)

| Day | Action |
|-----|--------|
| 1 | Confirm `secplus_portal_10d` serving · check GA4 Realtime for `begin_checkout` |
| Daily | Note impressions, clicks, spend, checkouts |
| 3 | First search terms pass — add junk as campaign negatives |
| 7 | Review CTR, avg CPC, CPA · decide wedge ad group enable / scale |

**Hold during test:** budget, bidding, locations, RSA copy. Enable `secplus_pbq_wedge` only after wedge landing + free PBQ sample verified.

## Headlines & descriptions

All RSA copy lives in the checklist CSV — filter **Section** = `Headline` or `Description`:

- **secplus_portal_10d** — pin H1 `Security+ Practice Test`, H2 `$9.99 for 10-Day Access`
- **secplus_pbq_wedge** — pin H1 `Security+ PBQ Practice`, H2 `$9.99 · 10-Day Access`

## Keywords (summary)

**secplus_portal_10d** — exact: `[security+ question bank]`, `[sy0-701 question bank]` · phrase: `"security+ practice test online"`, …

**secplus_pbq_wedge** — exact: `[security+ pbq practice]`, `[sy0-701 pbq]` · phrase: `"security+ performance based questions"`, `"security+ pbq practice online"`, …

Full keyword list: checklist **Setup → Ad group 1/2** rows.

## Open in Numbers

1. Open [[campaigns/secplus-campaign-checklist.csv|checklist CSV]] in Numbers
2. Convert **Done** column to checkboxes
3. Filter by **Section** (Setup / Headline / Description / Ops)
4. Save as `.numbers` for ongoing tracking

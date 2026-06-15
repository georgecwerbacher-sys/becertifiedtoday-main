---
type: campaign
product: ccna
utm_campaign: ccna_wedge_lab
status: ready-to-build
tags:
  - marketing
  - google-ads
  - ccna
  - wedge
---

# CCNA Wedge Lab Campaign

**Mission context:** [[Site Mission]] · [[Wedge Marketing plan/Wedge Marketing plan|Wedge Marketing plan]]

**Working checklist:** `scripts/ccna-wedge-lab-google-ads-checklist.csv` · `scripts/ccna-wedge-lab-google-ads-README.txt`

**Setup guide:** `scripts/ccna-wedge-lab-google-ads.md`

**Live landing:** https://becertifiedtoday.com/ccna/labs-without-gns3.html

## Campaign shell

| Setting | Value |
|---------|--------|
| Campaign name | **`CCNA_Wedge_Lab`** |
| Daily budget | **$15/day** launch → $20–25 after CPA baseline |
| Bidding | Maximize clicks, max CPC **$4.50** |
| utm_campaign | `ccna_wedge_lab` |
| Conversion | GA4 `begin_checkout` |

## Ad group: `CCNA_Wedge_Lab`

| Setting | Value |
|---------|--------|
| Display path | CCNA / Practice-Labs |
| Intent | Browser CLI labs · no GNS3 / Packet Tracer |
| Final URL | `/ccna/labs-without-gns3.html?utm_content=browser-labs` |
| Keywords | 5 exact + 14 phrase (Planner US Jun 2026) |
| RSA pin H1 | CCNA 200-301 Practice Labs |
| RSA pin H2 | $9.99 · 10-Day CCNA Labs |

## Build phases

1. **Pre-launch** — Stripe, checkout test, GA4 conversion, pause old `ccna_browser_labs`
2. **Campaign** — create `CCNA_Wedge_Lab`, $15/day, bidding, geo (US/CA/UK/AU)
3. **Ad group** — keywords, RSA, final URL
4. **Extensions** — 6 sitelinks (VLAN sample, 10d, 30d, questions, D&D, home)
5. **Negatives** — campaign + ad group phrase negatives
6. **Launch** — verify landing, free sample, checkout, GA4
7. **Week 1 ops** — baseline; day-3 search terms; day-7 CPA review

## Before you enable

- Pause **`ccna_browser_labs`** in the old combined CCNA campaign to avoid bidding against yourself.
- Keep head-term **`ccna_portal_10v1`** separate (low bid or paused).

## Keywords reference

See [[Wedge Marketing plan/02-keywords-and-google-ads|Keywords & Google Ads]] — `ccna_browser_labs` table maps 1:1 to **`CCNA_Wedge_Lab`**.

## Related

- [[CCNA Campaign]] — original combined campaign (portal + browser labs)
- [[Wedge Marketing plan/04-content-and-landing-pages|Landing pages]] — P1 wedge page **Live**
- [[Wedge Marketing plan/06-30-day-action-plan|30-day action plan]]

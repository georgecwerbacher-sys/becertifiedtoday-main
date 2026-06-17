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

**Headline suffixes:** `scripts/ccna-wedge-lab-google-ads-headline-suffixes.txt`

**Live landing:** https://becertifiedtoday.com/ccna-home.html

## Positioning (2026-06)

| Target | Exam **scheduled** or about to schedule — final prep, not course shopping |
| Avoid | “Free questions” seekers — campaign negatives + no `/sample` sitelinks |
| Funnel | Full `ccna-home.html` — hero, NGTE previews, pricing, comparisons |

## Campaign shell

| Setting       | Value                                          |
| ------------- | ---------------------------------------------- |
| Campaign name | **`CCNA_Wedge_Lab`**                           |
| Daily budget  | **$15/day** launch → $20–25 after CPA baseline |
| Bidding       | Maximize clicks, max CPC **$4.50**             |
| utm_campaign  | `ccna_wedge_lab`                               |
| Conversion    | GA4 `begin_checkout`                           |

## Ad group: `CCNA_Wedge_Lab`

| Setting      | Value                                                                 |
| ------------ | --------------------------------------------------------------------- |
| Display path | CCNA / Exam-Prep                                                      |
| Intent       | Exam-ready CCNA test prep — NGTE, timed sim, browser labs             |
| Final URL    | `/ccna-home.html?utm_content=exam-readiness`                          |
| Keywords     | 5 exact + 13 phrase (no “free labs” keywords)                         |
| RSA pin H1   | Scheduled CCNA? Prep Here                                             |
| RSA pin H2   | $9.99 · 10-Day Full Access                                            |

## Sitelinks (all `ccna-home.html` — no sample bypass)

| Label                    | Anchor / utm_content   |
| ------------------------ | ---------------------- |
| 10-Day Access · $9.99    | `#purchase` · portal-10d |
| 30-Day Access · $19.99   | `#purchase` · portal-30d |
| 120-Min Timed Simulation | `#purchase` · timed-sim |
| Browser CLI Labs         | `#ccna-gns3-compare` · browser-labs |
| NGTE Previews            | `#ccna-samples` · sitelink-ngte |
| Compare vs PDFs          | `#ccna-compare` · sitelink-compare |

## Build phases

1. **Pre-launch** — Stripe, checkout on `ccna-home.html`, GA4 conversion, pause old `ccna_browser_labs`
2. **Campaign** — create `CCNA_Wedge_Lab`, $15/day, bidding, geo (US/CA/UK/AU)
3. **Ad group** — keywords, RSA (exam-ready copy), final URL
4. **Extensions** — 6 sitelinks on `ccna-home.html` only
5. **Negatives** — course/dump/free-question phrases
6. **Launch** — verify full funnel, sitelinks, checkout, GA4
7. **Week 1 ops** — baseline; day-3 search terms; day-7 CPA review

## Before you enable

- Pause **`ccna_browser_labs`** in the old combined CCNA campaign to avoid bidding against yourself.
- Keep head-term **`ccna_portal_10v1`** separate (low bid or paused).
- **Analytics:** marketing-only tags — `scripts/marketing-tag-minimal-list.md`
- **Hero variants:** `public/js/ccna-home-conversion.js` (`exam-readiness`, `browser-labs`, `timed-sim`)

## Related

- [[CCNA Campaign]] — original combined campaign (portal + browser labs)
- [[Wedge Marketing plan/04-content-and-landing-pages|Landing pages]]
- [[Wedge Marketing plan/06-30-day-action-plan|30-day action plan]]

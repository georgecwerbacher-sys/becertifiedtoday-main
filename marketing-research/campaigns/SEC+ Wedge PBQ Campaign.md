---
type: campaign
product: secplus
utm_campaign: secplus_wedge_pbq
status: ready-to-build
tags:
  - marketing
  - google-ads
  - security+
  - secplus
  - wedge
---

# SEC+ Wedge PBQ Campaign

**Mission context:** [[Site Mission]] · [[Wedge Marketing plan/Wedge Marketing plan|Wedge Marketing plan]] · Persona **Sam**

**Working checklist:** `scripts/secplus-wedge-pbq-google-ads-checklist.csv` · `scripts/secplus-wedge-pbq-google-ads-README.txt`

**Setup guide:** `scripts/secplus-wedge-pbq-google-ads.md`

**Live landing:** https://becertifiedtoday.com/secplus/pbq-practice-browser.html

## Campaign shell

| Setting | Value |
| ------------- | ---------------------------------------------- |
| Campaign name | **`SEC+_Wedge_PBQ`** (or ad group inside combined campaign) |
| Daily budget | **$8/day** launch → scale after CPA baseline |
| Bidding | Maximize clicks, max CPC **$3.50** |
| utm_campaign | `secplus_portal` or `secplus_wedge_pbq` |
| Conversion | GA4 `begin_checkout` |

## Ad group: `secplus_pbq_wedge`

| Setting | Value |
| ------------ | ------------------------------------------------------- |
| Display path | Security+ / PBQ-Practice |
| Intent | Browser PBQ chain labs · no download · SY0-701 |
| Final URL | `/secplus/pbq-practice-browser.html?utm_content=pbq-wedge` |
| RSA pin H1 | Security+ PBQ Practice |
| RSA pin H2 | $9.99 · 10-Day Access |

## Build phases

1. **Pre-launch** — Stripe, checkout test, GA4 conversion, free dark-web PBQ sample works on mobile
2. **Landing** — verify `pbq-practice-browser.html` + `secplus-home-conversion.js` utm_content=pbq-wedge
3. **Ad group** — keywords, RSA, final URL
4. **Extensions** — sitelinks (dark web sample, 10d, questions, timed sim, home)
5. **Negatives** — `course`, `training`, `bootcamp`, `pdf`, `dump`, `jobs`
6. **Launch** — verify landing, free sample, checkout, GA4
7. **Week 1 ops** — baseline; day-3 search terms; day-7 CPA review

## Before you enable

- Prefer **separate ad group** inside combined Security+ campaign until CPA proves out.
- Do not bid wedge keywords on generic portal RSA — match landing to PBQ intent.
- **Analytics:** marketing-only tags — `scripts/marketing-tag-minimal-list.md`

## Related

- [[Security+ Campaign]] — combined portal + wedge ad groups
- [[Wedge Marketing plan/SEC+ funnel build tracker|SEC+ funnel build tracker]]
- [[Wedge Marketing plan/04-content-and-landing-pages|Landing pages]] — P1 wedge page **Live**

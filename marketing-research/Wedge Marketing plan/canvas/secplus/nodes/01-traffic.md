---
type: funnel-phase
phase: Traffic
product: secplus
scope: portal
tags:
  - secplus
  - security+
  - funnel
  - google-ads
  - portal
---

# Traffic — portal campaign (Security+)

[[../../SEC+ funnel build tracker|← Funnel tracker]] · [[../../../Sec+ Campaign/Security+ Campaign|Security+ Campaign]] · [[../../../Sec+ Campaign/Sec+ Notes|Setup]]

**Wedge PBQ campaign (separate):** [[../../../Sec+ Campaign/README|Sec+ Campaign]]

---

## Pre-launch

- [ ] Stripe `secplus-portal-10d` live at $9.99
- [ ] Stripe `secplus-portal-30d` live at $19.99
- [ ] Test checkout from `comptia-sec+-home.html` (desktop + mobile)
- [ ] GA4 `begin_checkout` fires for `secplus_portal_10d` and `secplus_portal_30d`
- [ ] Import GA4 `begin_checkout` as Primary conversion in Google Ads
- [x] `google-ads-purchase-conversion.js` on home
- [x] `secplus-home-conversion.js` — test `?utm_content=portal-10d`

## Campaign shell ($10/day)

- [ ] Campaign: `Security+ SY0-701 · Exam prep · becertifiedtoday`
- [ ] Daily budget **$10.00/day**
- [ ] Bidding: Maximize clicks, max CPC **$2.75**
- [ ] `utm_campaign=secplus_portal`
- [ ] Search partners: **off** · Language: English
- [ ] Locations: Tier A — **Presence** only

## Ad group — `secplus_portal_10d` only

- [ ] Display path: `Security+` / `10-Day-Access`
- [ ] Final URL: `comptia-sec+-home.html#purchase&utm_content=portal-10d`
- [ ] Head terms at low bid or paused per wedge plan
- [ ] Pin H1 `Security+ Practice Test` · H2 `$9.99 for 10-Day Access`
- [ ] Do **not** add wedge PBQ keywords here — use [[../../Sec+ Campaign/Sec+ Keywords#SEC+_Wedge_PBQ — ad group|Sec+ Keywords (wedge)]]

## Launch

- [ ] Enable `secplus_portal_10d` only
- [ ] GA4 Realtime on test click
- [ ] Day 7: CPA review — launch [[../../../Sec+ Campaign/Sec+ Notes|SEC+_Wedge_PBQ]] if head terms fail

**CSV:** `scripts/secplus-google-ads-campaign-checklist.csv`

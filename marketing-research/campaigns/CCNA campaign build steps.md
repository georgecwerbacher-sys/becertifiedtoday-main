---
type: campaign-steps
product: ccna
status: initial-test
test_start: 2026-06-14
test_end: 2026-06-21
tags:
  - marketing
  - google-ads
  - ccna
  - checklist
---

# CCNA campaign build steps

Obsidian checklist for **CCNA 200-301** Google Ads. Mirrors `scripts/ccna-google-ads-campaign-checklist.csv`.

**Hub:** [[CCNA Campaign]] · **Canvas:** [[Wedge Marketing plan/CCNA funnel build tracker|CCNA funnel build tracker]] · **Visual:** [[Wedge Marketing plan/canvas/CCNA wedge funnel.canvas|CCNA wedge funnel.canvas]]

---

## Phase 1 — Pre-launch

- [ ] Stripe `ccna-portal-10d` live at **$9.99**
- [ ] Stripe `ccna-portal-30d` live at **$19.99**
- [ ] Desktop + mobile checkout from `ccna-home.html#purchase`
- [ ] GA4 `begin_checkout` — `ccna_portal_10d` and `ccna_portal_30d`
- [ ] Import GA4 `begin_checkout` as Primary in Google Ads
- [ ] Pause old CCNA ad groups if replacing this campaign

---

## Phase 2 — Campaign shell ($25/day)

- [ ] Campaign: `CCNA 200-301 · Exam prep · becertifiedtoday`
- [ ] Daily budget **$25.00/day**
- [ ] Search partners: **Off**
- [ ] Bidding: Maximize clicks, max CPC **$3.00**
- [ ] `utm_campaign=ccna_portal`
- [ ] Presence-only Tier A locations

---

## Phase 3 — Ad group `ccna_portal_10v1` (~$17/day) — LIVE during 7-day test

- [ ] Display path: `CCNA` / `10-Day-Access`
- [ ] Final URL: `ccna-home.html#purchase&utm_content=portal-10d`
- [ ] Exact + phrase keywords (CSV)
- [ ] 15 headlines — pin H1 `CCNA 200-301 · Walk In Ready`, H2 `$9.99 · 10-Day CCNA Bank`
- [ ] 4 descriptions
- [ ] **Only this ad group enabled** during initial 7-day test

---

## Phase 4 — Ad group `ccna_browser_labs` (~$8/day) — PAUSED until day 7

- [ ] Final URL: `ccna/labs-without-gns3.html&utm_content=browser-labs`
- [ ] Wedge keywords + RSA (CSV Ad group 2)
- [ ] Or launch separate [[CCNA Wedge Lab Campaign|CCNA_Wedge_Lab]] campaign instead

---

## Phase 5 — Extensions & negatives

- [ ] 6 sitelinks + products list
- [ ] Campaign + ad group negatives pasted

---

## Phase 6 — Launch & 7-day test

| Day | Done | Action |
|-----|------|--------|
| 1 | [ ] | `ccna_portal_10v1` serving · GA4 checkout |
| 3 | [ ] | Search terms → negatives |
| 7 | [ ] | CPA review · enable browser_labs or wedge campaign |

**Hold during test:** budget, bidding, RSA, locations.

---

## Canvas phase links

| Phase | Note |
|-------|------|
| Traffic | [[Wedge Marketing plan/canvas/nodes/01-traffic\|01-traffic]] |
| Landing | [[Wedge Marketing plan/canvas/nodes/02-landing-pages\|02-landing-pages]] |
| Free proof | [[Wedge Marketing plan/canvas/nodes/03-free-proof\|03-free-proof]] |
| Checkout | [[Wedge Marketing plan/canvas/nodes/04-checkout\|04-checkout]] |
| Portal | [[Wedge Marketing plan/canvas/nodes/05-paid-product\|05-paid-product]] |
| Content | [[Wedge Marketing plan/canvas/nodes/06-content\|06-content]] |
| Measure | [[Wedge Marketing plan/canvas/nodes/07-measure\|07-measure]] |

[[Campaigns|← All campaigns]]

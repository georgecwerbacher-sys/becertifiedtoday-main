---
type: campaign-steps
product: secplus
campaign: SEC+_Wedge_PBQ
status: ready-to-build
tags:
  - marketing
  - google-ads
  - secplus
  - wedge
  - checklist
---

# Build steps — SEC+_Wedge_PBQ

Step-by-step Google Ads UI checklist. Mirrors `scripts/secplus-wedge-pbq-google-ads-checklist.csv`.

[[README|← Campaign folder]] · Keywords: [[03-keywords-ad-group]] · [[04-keywords-campaign-negatives]] · Copy: [[05-rsa-copy]]

---

## Phase 1 — Pre-launch

- [ ] Stripe `secplus-portal-10d` live at **$9.99**
- [ ] Stripe `secplus-portal-30d` live at **$19.99**
- [ ] Desktop checkout from `secplus/pbq-practice-browser.html#purchase`
- [ ] Mobile checkout (same page)
- [ ] GA4 Realtime: `begin_checkout` — `secplus_portal_10d` and `secplus_portal_30d`
- [ ] Import GA4 `begin_checkout` as **Primary** conversion in Google Ads
- [x] Wedge landing live — `public/secplus/pbq-practice-browser.html`
- [ ] Free dark web PBQ sample — phone + desktop (`/secplus-sample?track=sim-dark-web`)
- [ ] **Pause** `secplus_pbq_wedge` in combined [[Security+ Campaign|Security+ Campaign]] (if enabled)

---

## Phase 2 — Keyword Planner

- [ ] Open Keyword Planner — US, English, Search
- [ ] Export PBQ / performance-based / simulation themes
- [ ] Fill worksheet in [[03-keywords-ad-group#Keyword Planner worksheet]]
- [ ] Mark Add? yes/no for each starter keyword
- [ ] Remove zero-volume or course-intent terms before launch

---

## Phase 3 — Campaign shell

See [[02-campaign-shell]] for full settings.

- [ ] Create Search campaign **`SEC+_Wedge_PBQ`**
- [ ] Budget **$8.00/day** · Search partners **Off** · Display **Off**
- [ ] Bidding: Maximize clicks, max CPC **$3.50**
- [ ] `utm_campaign=secplus_wedge_pbq`
- [ ] Language: English · **Presence** only · US, CA, UK, AU
- [ ] AI Max / URL expansion: **Off**

---

## Phase 4 — Ad group

- [ ] Ad group name **`SEC+_Wedge_PBQ`**
- [ ] Display path: `Security+` / `PBQ-Practice`
- [ ] Final URL:
  ```
  https://becertifiedtoday.com/secplus/pbq-practice-browser.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=pbq-wedge
  ```
- [ ] Paste **exact** keywords from [[03-keywords-ad-group#Exact match (paste into Google Ads)]]
- [ ] Paste **phrase** keywords from [[03-keywords-ad-group#Phrase match (paste into Google Ads)]]
- [ ] Paste RSA from [[05-rsa-copy]] — pin H1 + H2

---

## Phase 5 — Extensions

- [ ] Paste 6 sitelinks from [[06-extensions-locations#Sitelinks]]

---

## Phase 6 — Negatives

- [ ] Campaign negatives from [[04-keywords-campaign-negatives#Campaign-level (phrase)]]
- [ ] Ad group negatives from [[04-keywords-campaign-negatives#Ad group-level (phrase)]]

---

## Phase 7 — Launch

- [ ] Enable campaign + ad group
- [ ] Final URL — pricing + FAQ visible
- [ ] Free dark web PBQ sample from landing CTA
- [ ] $9.99 checkout → Stripe
- [ ] GA4 Realtime `begin_checkout`
- [ ] Sitelinks on mobile
- [ ] Day 1 in [[../../Weekly Reports|Weekly Reports]]

---

## Phase 8 — Week 1 (baseline)

Follow [[07-launch-and-ops#Week 1 daily log]]. **Do not change:** budget, bidding, geo, RSA.

---

## Phase 9 — Week 2+

See [[07-launch-and-ops#Week 2+]].

---
type: campaign-steps
product: secplus
campaign: Security+ SY0-701 · Exam prep · becertifiedtoday
tags:
  - marketing
  - google-ads
  - secplus
  - checklist
---

# Sec+ Notes — how to set up the campaign

**Campaign:** `Security+ SY0-701 · Exam prep · becertifiedtoday`  
**Ad group:** **`Security+ PBQ Practice`** (only)  
**Budget:** **$15.00/day** · max CPC **$2.75** · **utm_campaign:** `secplus_portal`

**Checklist CSV:** [[secplus-campaign-checklist.csv]] (AdWords paste rows) · **Keyword source:** [[secplus-keywords.csv]] · regenerate: `npm run sync:secplus-checklist`

---

## Reference voice (read before building ads)

[[Sec+ Positioning#Canonical reference (future use)|Canonical reference]] — exam-realistic browser prep, **34 PBQs**, **90-min timed sim + scorecard** with paid access, **$19.99/30d** only.

Keywords and RSA: [[Sec+ Keywords]] · [[Sec+ RSA Copy]]

---

## Before you open Google Ads

- [ ] Stripe $19.99 / 30-day product live
- [ ] Checkout on cert home (desktop + phone)
- [ ] MCQ + 3-scenario PBQ preview reachable from landing (dark web IR, WLAN configuration, firewall ACL)
- [ ] GA4 `begin_checkout` imported as Primary
- [ ] Keyword Planner worksheet — [[Sec+ Keywords#Keyword Planner worksheet]]
- [ ] RSA reviewed against [[Sec+ Positioning]]

---

## Phase 1 — Campaign shell

1. Campaign name: **`Security+ SY0-701 · Exam prep · becertifiedtoday`**
2. Budget **$15.00/day** · Search only · partners off
3. Bidding: Maximize clicks · max CPC **$2.75**
4. Geo: US, CA, UK, AU · **Presence** only
5. utm_campaign: **`secplus_portal`** on all ads
6. AI Max / URL expansion: **Off**
7. Paste **6 sitelinks** — checklist **Extensions** rows or [[Extensions]]

---

## Phase 2 — Ad group: Security+ PBQ Practice

1. Ad group name: **`Security+ PBQ Practice`**
2. Display path: `Security+` / `PBQ-Practice`
3. Final URL:

```
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=pbq-wedge
```

4. Keywords: paste **Ad group** rows from [[secplus-campaign-checklist.csv]] (rank 1–67) — or regenerate from [[secplus-keywords.csv]] with `npm run sync:secplus-checklist`
5. RSA: [[Sec+ RSA Copy#Ad group Security+ PBQ Practice]]
6. Pin H1 `Security+ PBQ Practice` · H2 `Timed 90-Min Exam Sim` (Google Ads — see [[Sec+ RSA Copy]])

**Landing offer:** **30-day · $19.99 only** on cert home (10-day offer removed sitewide).

---

## Remove 10-day from live Google Ads

If the RSA or extensions still show **$9.99 / 10-day**:

1. **Campaign → Assets → Sitelinks** — delete **10-Day Access · $9.99**; keep **30-Day Access · $19.99** ([[Extensions]]).
2. **Ad group `Security+ PBQ Practice` → Ads** — edit RSA:
   - **Unpin / delete** headline `$9.99 · 10-Day Access` or `$9.99 for 10-Day Access`
   - **Pin H2** → `Timed 90-Min Exam Sim` (not price)
   - Keep headline `30-Day Access · $19.99` in the unpinned pool
   - Replace any description with `$9.99/10d` using the 4 descriptions in [[Sec+ RSA Copy#Descriptions (≤90 chars)]]
3. **Campaign settings → Products or services** — remove **Security+ 10-Day Exam Prep Access**; keep 30-day entry only.
4. If ad group **`secplus_portal_10d`** still exists — **pause or remove** it (live campaign is **`Security+ PBQ Practice`** only).
5. Test click → cert home shows **Get 30-day access · $19.99** only → GA4 Realtime shows `secplus_portal_30d` on `begin_checkout`.

---

## Landing conversion (track hardest)

**Page:** `/comptia-sec+-home.html` · **Admin:** 21-day plan → landing checkout rate · paid → checkout · click → checkout

After every ad click, optimize **post-click** before cutting keywords:

| Check | Fix |
|-------|-----|
| Message match (RSA ↔ hero ↔ purchase block) | [[Sec+ RSA Copy]] · [[Sec+ Positioning]] |
| Mobile checkout + sticky path to `#purchase` | Test on phone from live ad URL |
| Samples → purchase path (3-scenario PBQ preview) | Free proof visible above fold for Google paid |
| One change per week max | Check **Landing page change shipped** in admin daily log |
| Checkout &lt; 2% with ≥ 50 paid sessions | **Landing first** — not keyword overhaul |

**Budget follows converters:** pause phrase keywords with **≥ 20 clicks, 0 checkout**; promote search terms with **≥ 3 clicks + checkout** to `[exact]`.

Scorecard gates: [[Sec+ Phase 1 Scorecard]].

---

## Phase 3 — Negatives

- Campaign: [[Sec+ Keywords#Campaign negatives]]
- Ad group: [[Sec+ Keywords#Ad group negatives]]

---

## Phase 4 — Launch check

- [ ] One ad group enabled: **`Security+ PBQ Practice`**
- [ ] 6 sitelinks pasted — checklist **Extensions** rows or [[Extensions]]
- [ ] Final URL opens cert home with correct UTMs
- [ ] GA4 `begin_checkout` on test purchase click
- [ ] Mobile checkout on cert home

---

## Week 1

| Day | Action |
|-----|--------|
| 3 | Search terms → negatives |
| 7 | CPA review — hold $15/day or adjust max CPC |

[[README|← Sec+ Campaign folder]]

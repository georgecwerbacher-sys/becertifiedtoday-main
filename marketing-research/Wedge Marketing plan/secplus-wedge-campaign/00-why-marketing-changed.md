---
type: strategy
parent: "[[README]]"
tags:
  - marketing
  - secplus
  - wedge
  - pivot
created: 2026-06-15
---

# Why Security+ marketing changed

Same structural problem as CCNA: head terms are bid up by course vendors and big banks; you win on **browser PBQ practice**, **timed sim**, and **exam-readiness** — not “question bank” alone.

CCNA parallel: [[../00-why-ccna-marketing-changed|Why CCNA marketing changed]]

[[README|← Wedge campaign folder]]

---

## Old approach

- **Google Ads:** combined Security+ campaign, **`secplus_portal_10d`** on head terms — question bank, practice test, SY0-701 prep.
- **Landing:** generic portal on `comptia-sec+-home.html#purchase`.
- **Wedge:** held as ad group inside portal campaign — wrong structure for wedge budget and message match.

**Intent now:** dedicated **`SEC+_Wedge_PBQ`** campaign → [[01-build-steps|build steps]].

---

## What failed

| Signal | What it meant |
|--------|----------------|
| Head-term auction pressure | Course vendors bid loss leaders toward $50–$500+ products |
| Zero or low impressions | Often CPC cap + competition — not always wrong bid |
| Low-conversion geo clicks | Sample-only traffic, no `begin_checkout` — [[../03-pricing-and-funnel#India / low-conversion geo]] |
| Portal RSA on PBQ intent | Under-converts — wedge landing required |
| Big question banks | Answer with **review loops**, not volume — [[../03-pricing-and-funnel#Progress tracking]] |

---

## Your wedge

Persona **Sam** — [[../01-positioning-and-audience#Sam — Security+ (wedge)]]

| They sell | You sell |
|-----------|----------|
| Video course → bundle | **$9.99 / 10-day sprint** |
| Desktop sim install | **PBQ in browser — no download** |
| PDF / dumps | **Verified SY0-701 explanations** |
| Subscription banks | **One-time pass + adaptive review** |

**Lead in ads:** browser PBQ · free dark web sample · timed sim (when live).

---

## New funnel doc map

| Phase | Doc |
|-------|-----|
| Traffic | [[README\|SEC+_Wedge_PBQ]] · [[03-keywords-ad-group]] |
| Landing | `/secplus/pbq-practice-browser.html` **Live** |
| Free proof | [[../canvas/secplus/nodes/03-free-proof\|canvas 03-free-proof]] |
| Checkout | [[../canvas/secplus/nodes/04-checkout\|canvas 04-checkout]] |
| Full funnel | [[../SEC+ funnel build tracker]] |

---

## Decision log

| Date | Decision |
|------|----------|
| 2026-06-14 | Wedge strategy; deprioritize SEC+ head-term CPC |
| 2026-06-14 | US/CA/UK/AU first; no broad low-conversion geo scale |
| 2026-06-15 | Consolidate wedge build into `secplus-wedge-campaign/` folder |

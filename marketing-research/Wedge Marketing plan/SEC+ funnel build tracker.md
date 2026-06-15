---
type: tracker
parent: "[[Wedge Marketing plan]]"
tags:
  - marketing
  - secplus
  - security+
  - funnel
  - canvas
---

# Security+ funnel build tracker

Persona: **Sam** — PBQ anxiety, adaptive review, browser-no-install. See [[01-positioning-and-audience#Sam — Security+ (wedge)]].

**Why we pivoted:** [[secplus-wedge-campaign/00-why-marketing-changed|Why Security+ marketing changed]]

---

## Wedge Google Ads (primary)

**[[../Sec+ Campaign/README|Sec+ Campaign]]** — Obsidian working folder:

| Note | Purpose |
|------|---------|
| [[../Sec+ Campaign/Sec+ Positioning\|Sec+ Positioning]] | Differentiators vs PDF / courses |
| [[../Sec+ Campaign/Sec+ Notes\|Sec+ Notes]] | Setup — 3 ad groups |
| [[../Sec+ Campaign/Sec+ Keywords\|Sec+ Keywords]] | Intent-based keywords |
| [[../Sec+ Campaign/Sec+ RSA Copy\|Sec+ RSA Copy]] | Headlines per ad group |

Deep docs: [[secplus-wedge-campaign/README|secplus-wedge-campaign/]] (RSA, sitelinks, ops)

Portal head terms (separate): [[../Sec+ Campaign/Security+ Campaign|Security+ Campaign]]

---

## Obsidian canvas (product funnel)

**[[canvas/SEC+ wedge funnel.canvas|SEC+ wedge funnel.canvas]]**

Phase checklists: `canvas/secplus/nodes/` — landing, free proof, checkout, content (not wedge ads).

---

## Funnel path

```
Wedge Ads → Wedge landing pages → Free proof → $9.99/10d checkout → Portal → Exam day
```

## Build order (P1 first)

1. `public/secplus/pbq-practice-browser.html` — **Live**
2. Wire `secplus-home-conversion.js` on `comptia-sec+-home.html`
3. Launch **`SEC+_Wedge_PBQ`** — [[../Sec+ Campaign/Sec+ Notes|Sec+ Notes]]
4. `public/secplus/timed-practice-test.html`
5. `public/secplus/federal-8140-prep.html`
6. `public/secplus/exam-readiness.html`

| Phase | Checklist note |
|-------|----------------|
| Traffic (portal) | [[canvas/secplus/nodes/01-traffic\|01-traffic]] |
| Wedge campaign | [[../Sec+ Campaign/README\|Sec+ Campaign]] · [[../Sec+ Campaign/Sec+ Keywords\|keywords]] |
| Landing | [[canvas/secplus/nodes/02-landing-pages\|02-landing-pages]] |
| Free proof | [[canvas/secplus/nodes/03-free-proof\|03-free-proof]] |
| Checkout | [[canvas/secplus/nodes/04-checkout\|04-checkout]] |
| Paid product | [[canvas/secplus/nodes/05-paid-product\|05-paid-product]] |
| Content | [[canvas/secplus/nodes/06-content\|06-content]] |
| Measure | [[canvas/secplus/nodes/07-measure\|07-measure]] |

## Product gaps vs CCNA (non-blocking)

| CCNA asset | SEC+ status | Action |
|------------|-------------|--------|
| Objective tracker UI | JSON only | `build-secplus-objective-tracker.py` |
| Practice manifest builder | Manual slugs | `build-secplus-practice-questions-manifest.py` |
| Guest sample pool | Blueprint only | Optional `secplus-guest-sample-pool.json` |
| Hunt → Obsidian | script exists | Add `Hunt/secplus/` export |

[[Wedge Marketing plan|← Back to plan]] · [[04-content-and-landing-pages|Content & landing pages]]

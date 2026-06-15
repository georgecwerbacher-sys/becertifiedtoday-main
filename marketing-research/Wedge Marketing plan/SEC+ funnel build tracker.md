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

Persona: **Sam** — PBQ anxiety, adaptive review, browser-no-install story. See [[01-positioning-and-audience#Sam — Security+ (wedge)]].

## Funnel path

```
Wedge Ads → Wedge landing pages → Free proof → $9.99/10d checkout → Portal → Exam day
```

## Build order (P1 first)

1. `public/secplus/pbq-practice-browser.html` — **Live**
2. Wire `secplus-home-conversion.js` on `comptia-sec+-home.html`
3. `secplus_pbq_wedge` ad group in checklist (pause until landing verified)
4. `public/secplus/timed-practice-test.html`
5. `public/secplus/federal-8140-prep.html` (DoD / contractor angle)
6. `public/secplus/exam-readiness.html`

| Phase | Checklist note |
|-------|----------------|
| Traffic | Reuse CCNA canvas nodes — swap PBQ / SY0-701 keywords |
| Landing | [[04-content-and-landing-pages#Security+ — build priority]] |
| Free proof | `/secplus-sample?track=questions`, `?track=sim-dark-web`, free timed sim |
| Checkout | `secplus_portal_10d` · GA4 `begin_checkout` |
| Paid product | `SEC+_Training_Portal.html` — 1000+ MCQ, 28 PBQ, 90-min sim |
| Content | PBQ screen recordings (dark web IR, chain lab walkthrough) |
| Measure | Compare `secplus_portal_10d` vs `secplus_pbq_wedge` CPA |

## Product gaps vs CCNA (non-blocking)

| CCNA asset | SEC+ status | Action |
|------------|-------------|--------|
| Objective tracker UI | JSON only (`secplus-exam-objectives-sy0-701.json`) | `build-secplus-objective-tracker.py` |
| Practice manifest builder | Manual slugs in `secplus-practice-slugs.js` | `build-secplus-practice-questions-manifest.py` |
| Guest sample pool | Blueprint only | Optional `secplus-guest-sample-pool.json` |
| Hunt → Obsidian | `secplus_monthly_pbq_hunt.py` exists | Add `Hunt/secplus/` export |
| Free assessment landing | Runner only | Dedicated page or home CTA to `?free=1` |

## Campaign docs

- Portal campaign: [[campaigns/Security+ Campaign|Security+ Campaign]]
- Wedge PBQ campaign: [[campaigns/SEC+ Wedge PBQ Campaign|SEC+ Wedge PBQ Campaign]]
- Checklist CSV: `scripts/secplus-google-ads-campaign-checklist.csv`

[[Wedge Marketing plan|← Back to plan]] · [[04-content-and-landing-pages|Content & landing pages]]

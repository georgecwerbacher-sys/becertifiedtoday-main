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

**Build:** three US-only Search campaigns · see [[Sec+ Three-Campaign US Plan]]  
**Budget:** **$20.00/day each** · **$60/day total** · max CPC **$2.75**  
**utm_campaigns:** `secplus_core_us` · `secplus_gov_us` · `secplus_workforce_us`

**Checklist CSV:** [[secplus-campaign-checklist.csv]] remains the baseline import. For three-campaign rollout, copy relevant keyword/RSA rows into each campaign manually until the sync script supports campaign tiers.

---

## Reference voice (read before building ads)

[[Sec+ Positioning#Canonical reference|Canonical reference]] — **Test Preparation Site**: 1000+ verified SY0-701 questions, **90-min timed sim + scorecard**, adaptive review, **34 PBQs**. **$19.99/30d**. Institutional audiences: [[Sec+ Phase 2 Institutional Targeting]].

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

## Phase 1 — Three US campaign shells

1. Build three campaigns from [[Sec+ Three-Campaign US Plan#Budget structure]]:
   - `Security+ SY0-701 · Core Exam Prep · US`
   - `Security+ SY0-701 · Military Gov 8140 · US`
   - `Security+ SY0-701 · Student Workforce · US`
2. Budget **$20.00/day per campaign** · Search only · partners off
3. Bidding: Maximize clicks · max CPC **$2.75** · hold keyword bids for 7 days
4. Geo: **United States only** · **Presence** only
5. Ad schedule: before work, lunch, after work, weekends — [[Sec+ Three-Campaign US Plan#Ad schedule — when target buyers search]]
6. utm_campaign by campaign:
   - Core: **`secplus_core_us`**
   - Gov: **`secplus_gov_us`**
   - Workforce: **`secplus_workforce_us`**
7. AI Max / URL expansion: **Off**
8. Paste **6 sitelinks** — checklist **Extensions** rows or [[Extensions]]
9. Add URL exclusions if Google prompts — [[Sec+ Google Ads Build Checklist#9. URL exclusions / expansion guardrails]]

---

## Phase 2 — Campaign message tracks

Each campaign may use one simple ad group at launch. Keep the RSA aligned to the audience; do not split more than needed during the first week.

| Campaign | Ad group | Display path | Final URL UTM content |
|----------|----------|--------------|-----------------------|
| Core Exam Prep | `SY0-701 Exam Prep` | `Security+` / `Exam-Prep` | `core-exam-prep` |
| Military Gov 8140 | `Security+ 8140 Prep` | `Security+` / `DoD-8140` | `mil-gov-8140` |
| Student Workforce | `Security+ Career Prep` | `Security+` / `Career-Prep` | `student-workforce` |

Core final URL:

```
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_core_us&utm_content=core-exam-prep
```

Full URLs: [[Sec+ Three-Campaign US Plan#Budget structure]]

Keywords: split from [[Sec+ Keywords]] by intent. RSA: [[Sec+ RSA Copy#Phase 2 — exam prep lead (paste when ready)]]

**Landing offer:** **30-day · $19.99** on cert home.

---

## Legacy cleanup (done)

10-day / $9.99 tier removed from site and campaign docs. If old RSA or sitelinks still show in Google Ads UI, replace with [[Sec+ RSA Copy]] and [[Extensions]] Phase 1 sitelinks.

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

**Budget follows converters after week 1:** hold keyword bids for the first 7 days, then pause phrase keywords with **≥ 20 clicks, 0 checkout**; promote search terms with **≥ 3 clicks + checkout** to `[exact]`.

Scorecard gates: [[Sec+ Phase 1 Scorecard]].

---

## Phase 3 — Negatives

- Campaign: [[Sec+ Keywords#Campaign negatives]]
- Ad group: [[Sec+ Keywords#Ad group negatives]]
- Add the Phase 2 course/PDF/dump negative expansion from [[Sec+ Keywords#All negatives]] before enabling the three campaigns.

---

## Phase 3b — URL exclusions

Keep AI Max and URL expansion **Off**. If Google asks for URL exclusions, exclude admin, restore, sample, CCNA, CCNP, and generic question pages per [[Sec+ Google Ads Build Checklist#9. URL exclusions / expansion guardrails]].

---

## Phase 4 — Launch check

- [ ] Three campaigns created as **paused drafts**
- [ ] US only + Presence only on all three
- [ ] Shared ad schedule applied on all three
- [ ] 6 sitelinks pasted — checklist **Extensions** rows or [[Extensions]]
- [ ] Final URLs open cert home with correct UTMs
- [ ] GA4 `begin_checkout` on test purchase click
- [ ] Mobile checkout on cert home

---

## Week 1

| Day | Action |
|-----|--------|
| 1 | Enable Core Exam Prep first if you want controlled spend |
| 3 | Search terms → negatives |
| 7 | Keyword review by campaign — adjust bids based on keyword results, search terms, checkout quality |

[[README|← Sec+ Campaign folder]]

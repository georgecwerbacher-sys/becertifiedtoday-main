---
type: campaign-checklist
product: secplus
phase: launch-40
status: active
tags:
  - marketing
  - google-ads
  - secplus
  - checklist
---

# Sec+ Launch 40 — build checklist

**Locked:** $35/day · 20% fence-sitters · `utm_campaign=secplus_portal_launch40`  
**Plan:** [[Sec+ Launch 40 Campaign Plan]]  
**Landing:** https://becertifiedtoday.com/comptia-sec+-home.html#home-secplus-samples-title

Clickable canvas: use Cursor canvas `secplus-campaign-build-checklist` beside chat.

---

## A · Site & offer

- [x] A1 · Confirm Sec+ 30-day product live at $19.99 (Stripe)
- [x] A2 · Stripe 20% fence-sitter coupon: **`AUGUSTPROMO2026`**
- [ ] A3 · Soft 20% prompt after sample complete / return from sample (apply `AUGUSTPROMO2026`)
- [ ] A4 · Sim: scorecard never gated · optional soft prompt before scorecard · preferred ~20s after scorecard (apply `AUGUSTPROMO2026`)
- [ ] A5 · Landing hero stays $19.99 — no public % off banner / not in ads
- [ ] A6 · Confirm no-registration story: Stripe → magic-link access
- [ ] A7 · Test purchase path desktop + mobile → magic link works
- [ ] A8 · Test checkout with code `AUGUSTPROMO2026` → $15.99

---

## B · Tracking

- [ ] B1 · GA4 `begin_checkout` fires on purchase click (Realtime)
- [ ] B2 · Google Ads: `begin_checkout` imported as **Primary** conversion
- [ ] B3 · Purchase conversion observe/secondary if used
- [ ] B4 · UTM plan: `secplus_portal_launch40` + `utm_content` = `timed-sim` | `verified-adaptive` | `after-study`

---

## C · Campaign shell

- [ ] C1 · Create Search campaign: `Security+ SY0-701 · US Search · Launch 40`
- [ ] C2 · Daily budget **$35** · Maximize clicks · max CPC **$2.50–$2.75**
- [ ] C3 · Off: Search partners · Display · AI Max / URL expansion
- [ ] C4 · US only · Presence · English
- [ ] C5 · Ad schedule (weekday AM/lunch · after-work +15% Mon–Thu · weekend)

---

## D · Ad groups

| Ad group | `utm_content` | Display path |
|----------|---------------|--------------|
| Timed Simulation | `timed-sim` | `Security+` / `Exam-Sim` |
| Verified Adaptive Prep | `verified-adaptive` | `Security+` / `Verified-Prep` |
| After Study Sprint | `after-study` | `Security+` / `After-Study` |

- [ ] D1 · Create Timed Simulation
- [ ] D2 · Create Verified Adaptive Prep
- [ ] D3 · Create After Study Sprint
- [ ] D4 · Final URLs → cert home `#home-secplus-samples-title` + UTMs

Example final URL:

```text
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal_launch40&utm_content=timed-sim#home-secplus-samples-title
```

---

## E · Keywords & negatives

- [ ] E1 · Paste Timed Simulation keywords ([[Sec+ Launch 40 Campaign Plan#Keywords]])
- [ ] E2 · Paste Verified Adaptive Prep keywords
- [ ] E3 · Paste After Study Sprint keywords (no creator brands)
- [ ] E4 · Paste campaign negatives (free / course / PDF / dump / messer / dion / naked practice questions…)

---

## F · RSA & extensions

- [ ] F1 · Draft RSA — pin H1 `SY0-701 Exam Prep Online` (24) · H2 `Timed 90-Min Exam Sim` (21) · all headlines ≤30
- [ ] F2 · Paste from [[Sec+ Launch 40 RSA Copy]] — verified · adaptive · no-reg · Stripe/magic link · $19.99 — **no % off**
- [ ] F3 · Create 1 RSA per ad group
- [ ] F4 · Sitelinks: 30-day $19.99 · samples · timed sim · verified bank (**no discount sitelink**)

---

## G · Launch & week 1

- [ ] G1 · Pause/archive old Sec+ Search campaigns if still live
- [ ] G2 · Pre-flight: $35 · 3 ad groups · UTMs · negatives · RSA
- [ ] G3 · Click preview URL → landing → sample → checkout (GA4 Realtime)
- [ ] G4 · Enable campaign · log launch in admin daily campaign log
- [ ] G5 · Day 3: search terms → negatives only · Day 7: prune / checkout review

**Kill rule:** After $150–200 clean spend with 0 `begin_checkout`, pause and fix before burning more budget.

---

## Suggested order

1. Finish **A2–A7** (offer + site)  
2. Confirm **B** tracking  
3. Build **C–F** in Google Ads (paused)  
4. **G** enable when A+B green  

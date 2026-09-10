---
type: campaign-checklist
product: secplus
phase: launch-40
status: paused
tags:
  - marketing
  - google-ads
  - secplus
  - checklist
  - 24h-trial
---

# Sec+ Launch 40 — build checklist

**Paused.** Do not build this. Current flight: [[Sec+ Sep 430 Build Checklist]]. Pause `Security+ SY0-701 · US Search · Launch 40` in Google Ads.

**Budget:** $465 total · **$15/day** · no end date (pause at cap) · `utm_campaign=secplus_portal_launch40`  
**Offer:** 24 hours free, then $15.99 (`SECPLUS24`) · list $19.99  
**Plan:** [[Sec+ Launch 40 Campaign Plan]]  
**Landing:** https://becertifiedtoday.com/comptia-sec+-home.html

Clickable canvas: use Cursor canvas `secplus-campaign-build-checklist` beside chat.

---

## A · Site & offer

- [x] A1 · Confirm Sec+ 30-day product live at $19.99 (Stripe)
- [x] A2 · Stripe 20% coupon: **`SECPLUS24`** (24h trial upgrade only)
- [x] A3 · Back to School banner removed — `secplus-bts-promo.js` retired
- [x] A4 · Purchase card shows $19.99 · Try 24 hours free · trial upgrade $15.99
- [x] A5 · $15.99 is not a public sale; only while 24h access is active
- [ ] A6 · Confirm Stripe checkout then magic-link access
- [ ] A7 · Test purchase desktop+mobile magic link
- [ ] A8 · Test 24h checkout, then 30-day with `SECPLUS24` → $15.99

---

## B · Tracking

- [ ] B1 · GA4 `begin_checkout` fires on purchase click (Realtime)
- [ ] B2 · Google Ads: `begin_checkout` imported as **Primary** conversion
- [ ] B3 · Purchase conversion observe/secondary if used
- [ ] B4 · UTM plan: `secplus_portal_launch40` + `utm_content` = `24h-trial` | `timed-sim` | `verified-adaptive` | `after-study` | `student-college`

---

## C · Campaign shell

- [ ] C1 · Create Search campaign: `Security+ SY0-701 · US Search · Launch 40`
- [ ] C2 · Daily budget **$15** · Maximize clicks · max CPC **$2.50–$2.75** · pause at **$465** cumulative
- [ ] C3 · Off: Search partners · Display · AI Max / URL expansion
- [ ] C4 · US only · Presence · English
- [ ] C5 · Ad schedule (weekday AM/lunch · after-work +15% Mon–Thu · weekend)

---

## D · Ad groups

| Ad group | `utm_content` | Display path |
|----------|---------------|--------------|
| 24h Trial | `24h-trial` | `SY0-701` / `24h-Free` |
| Timed Simulation | `timed-sim` | `Security+` / `Exam-Sim` |
| Verified Adaptive Prep | `verified-adaptive` | `Security+` / `Verified-Prep` |
| After Study Sprint | `after-study` | `Security+` / `After-Study` |
| Student College | `student-college` | `Security+` / `College-Prep` |

- [ ] D0 · Create 24h Trial (primary RSA)
- [x] D1 · Timed Simulation already live
- [x] D2 · Verified Adaptive Prep already live
- [x] D3 · After Study Sprint already live
- [x] D4 · Student College already live
- [ ] D5 · Final URLs → cert home (top of fold, no samples hash) + UTMs

Example final URL:

```text
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal_launch40&utm_content=24h-trial
```

---

## E · Keywords & negatives

- [ ] E0 · Paste 24h Trial keywords ([[Sec+ Launch 40 Keyword Lists]])
- [ ] E1 · Pause Back to School keywords in Student College
- [ ] E2 · Keep remaining ad-group keywords or pause extra groups
- [ ] E5 · Paste campaign negatives (course / PDF / dump / messer · **do not** add bare `free`)

---

## F · RSA & extensions

- [ ] F1 · Pause Back to School RSA headlines · paste [[Sec+ Launch 40 RSA Copy]]
- [ ] F2 · Pin H1 `Try 24 Hours Free` · H2 `Then 30 Days at $15.99`
- [ ] F3 · Prefer 1 RSA in 24h Trial (pause extra RSAs if needed)
- [ ] F4 · Sitelinks: 24 hours free · 30-day · samples · timed sim · verified bank

---

## G · Launch & week 1

- [x] G1 · Pause/archive old Sec+ Search campaigns if still live
- [x] G2 · Pre-flight: $15/day · $465 cap · 4 ad groups · UTMs · negatives · RSA
- [ ] G3 · Preview URL → landing → $19.99 card → 24h CTA → checkout (GA4 Realtime)
- [x] G4 · Enable campaign · **running 2026-08-10**
- [ ] G5 · Day 3: search terms → negatives only · Day 7: prune / checkout review
- [ ] G6 · Confirm dump / brain dump / cheat / actual exam are **campaign negatives** (not positives). Pause Dump Intercept if it exists.

**Kill rule:** After $70–90 clean spend with 0 `begin_checkout`, pause and fix. Pause the campaign at **~$450–$465** cumulative.

---

## Suggested order (now that ads are live)

1. Confirm **A6–A8** + **B** if not already (Stripe $15.99 · GA4 begin_checkout)  
2. **Daily:** Search terms → add negatives only  
3. **Day 7:** Prune by ad group / keyword · checkout quality  
4. Hold CPC and structure for 7 days unless junk or broken tracking  
5. Watch cumulative spend · drop daily to $5–$10 when remaining is under $40 · pause at $465  

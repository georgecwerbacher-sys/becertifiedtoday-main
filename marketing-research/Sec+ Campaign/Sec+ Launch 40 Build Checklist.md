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
  - back-to-school
---

# Sec+ Launch 40 — build checklist

**Locked:** $35/day · **public August 20%** (`AUGUSTPROMO2026`) · 4 ad groups · `utm_campaign=secplus_portal_launch40`  
**Plan:** [[Sec+ Launch 40 Campaign Plan]]  
**Landing:** https://becertifiedtoday.com/comptia-sec+-home.html#home-secplus-samples-title

Clickable canvas: use Cursor canvas `secplus-campaign-build-checklist` beside chat.

---

## A · Site & offer

- [x] A1 · Confirm Sec+ 30-day product live at $19.99 (Stripe)
- [x] A2 · Stripe 20% coupon: **`AUGUSTPROMO2026`**
- [x] A3 · Public Back to School banner (August) — `secplus-bts-promo.js`
- [x] A4 · Purchase card shows $15.99 · checkout prefills `AUGUSTPROMO2026`
- [x] A5 · Banner + pricing for **everyone** through Aug 31 (not fence-sitters only)
- [ ] A6 · Confirm Stripe checkout then magic-link access
- [ ] A7 · Test purchase desktop+mobile magic link
- [ ] A8 · Test checkout with code `AUGUSTPROMO2026` → $15.99

---

## B · Tracking

- [ ] B1 · GA4 `begin_checkout` fires on purchase click (Realtime)
- [ ] B2 · Google Ads: `begin_checkout` imported as **Primary** conversion
- [ ] B3 · Purchase conversion observe/secondary if used
- [ ] B4 · UTM plan: `secplus_portal_launch40` + `utm_content` = `timed-sim` | `verified-adaptive` | `after-study` | `student-college`

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
| Student College | `student-college` | `Security+` / `College-Prep` |

- [ ] D1 · Create Timed Simulation
- [ ] D2 · Create Verified Adaptive Prep
- [ ] D3 · Create After Study Sprint
- [ ] D4 · Create Student College
- [ ] D5 · Final URLs → cert home `#home-secplus-samples-title` + UTMs

Example final URL:

```text
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal_launch40&utm_content=student-college#home-secplus-samples-title
```

---

## E · Keywords & negatives

- [ ] E1 · Paste Timed Simulation keywords ([[Sec+ Launch 40 Keyword Lists]])
- [ ] E2 · Paste Verified Adaptive Prep keywords
- [ ] E3 · Paste After Study Sprint keywords (no creator brands)
- [ ] E4 · Paste Student College keywords
- [ ] E5 · Paste campaign negatives (free / course / PDF / dump / messer / dion / naked practice questions…)

---

## F · RSA & extensions

- [ ] F1 · Paste RSA from [[Sec+ Launch 40 RSA Copy]] — pin H1/H2 · include August BTS headlines
- [ ] F2 · Student College RSA — pin `Security+ College Prep` + timed sim
- [ ] F3 · Create 1 RSA per ad group (4 total)
- [ ] F4 · Sitelinks: 30-day · samples · timed sim · verified bank · Back to School $15.99 OK

---

## G · Launch & week 1

- [ ] G1 · Pause/archive old Sec+ Search campaigns if still live
- [ ] G2 · Pre-flight: $35 · 4 ad groups · UTMs · negatives · RSA
- [ ] G3 · Preview URL → landing → banner → sample → checkout (GA4 Realtime)
- [ ] G4 · Enable campaign · log launch in admin daily campaign log
- [ ] G5 · Day 3: search terms → negatives only · Day 7: prune / checkout review

**Kill rule:** After $150–200 clean spend with 0 `begin_checkout`, pause and fix before burning more budget.

---

## Suggested order (parallel today)

1. **You:** Build **C–F** in Google Ads (paused) from paste sheets  
2. **You:** Confirm **A6–A8** Stripe $15.99 + magic link  
3. **Then:** Confirm **B** tracking · **G** enable when green  

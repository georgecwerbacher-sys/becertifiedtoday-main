---
type: campaign-strategy
product: secplus
phase: launch-40
status: active-bts-august
tags:
  - marketing
  - google-ads
  - secplus
  - budget
  - conversions
  - back-to-school
---

# Sec+ Launch Campaign Plan — $1k performance flight

**Status:** Active build · **Back to School August** · Stripe code **`AUGUSTPROMO2026`** (20% for everyone through Aug 31)  
**Goal:** Conversions (checkout → purchase) during back-to-school  
**Offer:** list **$19.99** / 30 days · **public 20% → $15.99** all August (banner + prefilled checkout)  
**Daily budget:** **$35** (locked) · ~29 days on $1,000 if spend is steady  
**Landing:** https://becertifiedtoday.com/comptia-sec+-home.html#home-secplus-samples-title

Related: [[Sec+ Positioning]] · [[Sec+ Keywords]] · [[Sec+ Launch 40 Keyword Lists]] · [[Sec+ Launch 40 RSA Copy]] · [[Sec+ Notes]] · prior spend [[Google Ads Spend Promo]]

---

## Budget pacing (locked)

| Item | Value |
|------|------:|
| Total | $1,000 |
| Daily | **$35** (locked) |
| Expected flight | **~29 days** if spend is steady |
| List price | $19.99 |
| Back to School (August) | **20% → $15.99** for everyone |
| Purchases to recover $1k (at $15.99) | ~63 |
| Stripe coupon | **`AUGUSTPROMO2026`** (20% off Sec+ 30-day) |

**Kill rule:** After **$150–200** on clean (negatived) traffic with **0 `begin_checkout`**, pause and fix landing/offer/tracking before burning the rest.

---

## Positioning (vs sample → course upsell)

Security+ is entry-level. Many **college cyber / IT programs** require passing SY0-701 for graduation, capstone, or internship. Creators monetize with course upsells. You monetize with **simulated exams + verified adaptive practice**.

| They sell | You sell |
|-----------|----------|
| Free samples → paid course | Free samples → timed sim + verified bank |
| Video bootcamps | Browser simulated exams + scorecard |
| Account signup + email list | **No site registration** — pay in **Stripe**, access via **magic link** |
| PDF dumps / static packs | Adaptive review, not a PDF |

**Access friction (RSA + landing proof):**

- No account to create on becertifiedtoday.com
- Checkout is Stripe only
- Portal access is magic-link after purchase

**August offer (public):** Back to School banner + purchase card show **$15.99**. RSA may mention Back to School / $15.99. Code **`AUGUSTPROMO2026`** is prefilled at Stripe — do not require shoppers to hunt for it.

**Policy-safe:** verified, SY0-701-aligned, reputable sources, timed simulation, adaptive.  
**Never in ads:** actual exam questions, real exam, dumps, competitor brand names.

---

## Campaign shell

| Setting | Value |
|---------|-------|
| Name | `Security+ SY0-701 · US Search · Launch 40` |
| Type | Search only |
| Daily budget | **$35 shared** (locked) |
| Bidding (days 1–10) | Maximize clicks · max CPC **$2.50–$2.75** |
| Bidding (after signal) | Maximize conversions when ≥15–20 `begin_checkout` |
| Geo | US only · Presence |
| Networks | Partners Off · Display Off · AI Max Off |
| Primary conversion | GA4 `begin_checkout` |
| Promo | **Public August 20%** — code **`AUGUSTPROMO2026`** · banner on cert home |
| utm_campaign | `secplus_portal_launch40` |

**Hold rule:** No structure / bid drama for 7 days unless junk traffic or broken tracking.

---

## Four ad groups (shared budget)

| # | Ad group | Intent | `utm_content` | Lead message |
|---|----------|--------|---------------|--------------|
| 1 | `Timed Simulation` | Am I ready? | `timed-sim` | 90-min simulated exam + scorecard |
| 2 | `Verified Adaptive Prep` | Not PDF / not AI junk | `verified-adaptive` | Verified bank + adaptive review |
| 3 | `After Study Sprint` | Already used free samples/courses | `after-study` | Skip another course — practice for the exam |
| 4 | `Student College` | Degree / capstone / required for graduation | `student-college` | College cyber programs that require Security+ |

**Defer to later:** Military/DoD 8140, workforce/WIOA (keep college-focused for BTS).

Final URL pattern:

```text
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal_launch40&utm_content=<slug>#home-secplus-samples-title
```

---

## Keywords

See [[Sec+ Launch 40 Keyword Lists]] (includes Student College).

**Do not bid on** creator brands as positives. **Do not bid on** naked `practice questions` / `practice test`.

---

## Campaign negatives (paste first)

```
free
bootcamp
udemy
coursera
boson
jobs
salary
ccna
cissp
ceh
examtopics
pdf
ebook
voucher
brain dump
exam dump
"actual exam"
"real exam questions"
"jason dion"
"dion training"
"professor messer"
messer
"mike meyers"
pass4sure
"training course"
"online course"
"video course"
"instructor led"
"security+ practice questions"
"sy0-701 practice questions"
[security+ practice exam]
```

---

## RSA direction (1 RSA per ad group)

**Headlines ≤30 characters** · Descriptions ≤90 · Pin H1 + H2 only

Full paste sheets: [[Sec+ Launch 40 RSA Copy]]

| Pin | Headline | Chars |
|-----|----------|------:|
| H1 | `SY0-701 Exam Prep Online` | 24 |
| H2 | `Timed 90-Min Exam Sim` | 21 |

**August BTS headlines allowed** (public promo):

```
Back to School · 20% Off
August: $15.99 / 30 Days
$15.99 Back to School
```

Student College pins: H1 `Security+ College Prep` · H2 `Timed 90-Min Exam Sim`

---

## Site offer (August — everyone)

| Surface | Behavior |
|---------|----------|
| Top banner on `/comptia-sec+-home.html` | Back to School · 20% off · code + CTA to `#purchase` |
| Purchase card | Strike $19.99 · show $15.99 |
| Stripe checkout | Prefill `AUGUSTPROMO2026` |
| Ends | **2026-09-01 00:00 ET** |

Verified learner discounts page stays separate for deeper eligibility discounts.

---

## Ops cadence

| Window | Action |
|--------|--------|
| Pre-launch | Offer + tracking + negatives ready · Stripe 20% code live |
| Days 1–7 | **$35/day** · search terms daily · negatives only |
| Days 8–14 | Prune spenders · exact-match promote converters |
| Days 15+ | Scale winners or pause if no checkout after clean traffic |
| End | When $1k spent, CPA unacceptable, or August ends — not day 60 |

---

## Approval / build status

**Build checklist:** [[Sec+ Launch 40 Build Checklist]] · CSV `secplus-launch40-build-checklist.csv`

- [x] Lock **$35/day** performance pacing
- [x] Public August **20%** Back to School for everyone (`AUGUSTPROMO2026`)
- [x] Site banner + checkout prefill (`secplus-bts-promo.js`)
- [x] Add **Student College** as 4th ad group (BTS)
- [ ] Confirm Stripe coupon live → $15.99
- [ ] Tracking (GA4 + Ads Primary)
- [ ] Build campaign in Google Ads (paused → enable)

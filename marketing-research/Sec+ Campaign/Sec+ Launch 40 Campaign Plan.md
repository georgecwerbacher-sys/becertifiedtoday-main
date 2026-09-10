---
type: campaign-strategy
product: secplus
phase: launch-40
status: paused
tags:
  - marketing
  - google-ads
  - secplus
  - budget
  - conversions
  - 24h-trial
---

# Sec+ Launch Campaign Plan — $465 Search budget

**Status:** **Paused** · superseded by [[Sec+ Sep 430 Campaign Plan]] · 24h-trial RSA is stale. Pause `Security+ SY0-701 · US Search · Launch 40` in Google Ads so Sep 430 spend is not split.  
**Goal:** Conversions (checkout → purchase) on ethical Search traffic only  
**Offer:** **24 hours free**, then **$15.99** / 30 days (`SECPLUS24`) while the trial is active · list **$19.99** without trial  
**Daily budget:** **$15** shared  
**Landing:** https://becertifiedtoday.com/comptia-sec+-home.html (top of fold · no samples hash)  
**Launched:** 2026-08-10 · budget reset 2026-08-29 · BTS paused 2026-08-29

Related: [[Advertising Ethics]] · [[Sec+ Positioning]] · [[Sec+ Launch 40 Keyword Lists]] · [[Sec+ Launch 40 RSA Copy]] · prior spend [[Google Ads Spend Promo]]

---

## Budget pacing ($465 · no time limit)

All **$465** stays on this one Search campaign. Do **not** split to Dump Intercept or a second Search campaign.

Google Search has **no lifetime campaign cap**. Set **$15/day**, watch cumulative spend, and **pause when you hit ~$450–$465**. Google can spend up to about **2×** the daily budget on a given day, so drop the daily cap to **$5–$10** when remaining budget is under **$40**.

| Item | Value |
|------|------:|
| Total | **$465** |
| Daily | **$15** shared |
| Expected runway | **~31 days** if spend is steady |
| Clicks / day (at $2.50–$2.75 CPC) | ~5–6 |
| List price | $19.99 |
| 24h trial then 30-day | **$15.99** (`SECPLUS24`) |
| Purchases to recover $465 (at $19.99) | ~23 |
| Stripe coupon | **`SECPLUS24`** on 30-day while 24h access is active |

**Kill rule:** After **$70–90** on clean (negatived) traffic with **0 `begin_checkout`**, pause and fix landing/offer/tracking before spending the rest.

**Google Ads swap:** pause Back to School RSA headlines. Paste [[Sec+ Launch 40 RSA Copy]]. Remove the campaign negative `free`. Pause `"security+ back to school"` and `"security+ fall semester prep"`.

---

## Positioning (vs sample → course upsell)

Security+ is entry-level. Many **college cyber / IT programs** require passing SY0-701 for graduation, capstone, or internship. Creators monetize with course upsells. You monetize with **simulated exams + verified adaptive practice**.

| They sell | You sell |
|-----------|----------|
| Free samples → paid course | Free samples → timed sim + verified bank |
| Video bootcamps | Browser simulated exams + scorecard |
| Account signup + email list | **No site registration** — pay in **Stripe**, access via **magic link** |
| Static PDF packs | Adaptive review, not a PDF |

**Access friction (RSA + landing proof):**

- No account to create on becertifiedtoday.com
- Checkout is Stripe only
- Portal access is magic-link after purchase

**Public offer:** 24 hours free through Stripe Checkout (card not required). List 30-day is **$19.99**. While 24-hour access is active, 30-day checkout prefills **`SECPLUS24`** → **$15.99**. Do not advertise $15.99 as a sitewide sale.

**Policy-safe:** verified, SY0-701-aligned, reputable sources, timed simulation, adaptive.  
**Never in ads:** actual exam questions, real exam, dumps, braindump, cheat, pass guaranteed, competitor brand names.  
**Never bid on dump or cheat searches.** Those terms are campaign negatives. Dump intercept is retired. See [[Advertising Ethics]].

---

## Campaign shell

| Setting | Value |
|---------|-------|
| Name | `Security+ SY0-701 · US Search · Launch 40` |
| Type | Search only |
| Daily budget | **$15 shared** |
| Bidding (days 1–10) | Maximize clicks · max CPC **$2.50–$2.75** |
| Bidding (after signal) | Maximize conversions when ≥15–20 `begin_checkout` |
| Geo | US only · Presence |
| Networks | Partners Off · Display Off · AI Max Off |
| Primary conversion | GA4 `begin_checkout` |
| Promo | **24 hours free**, then **$15.99** / 30 days (`SECPLUS24`) · list **$19.99** |
| utm_campaign | `secplus_portal_launch40` |

**Hold rule:** No structure / bid drama for 7 days unless junk traffic or broken tracking.

---

## Ad groups (shared budget)

| # | Ad group | Intent | `utm_content` | Lead message |
|---|----------|--------|---------------|--------------|
| 1 | `24h Trial` | Try before buying | `24h-trial` | 24 hours free, then 30 days at $15.99 |
| 2 | `Timed Simulation` | Am I ready? | `timed-sim` | 90-min simulated exam + scorecard |
| 3 | `Verified Adaptive Prep` | Not PDF / not AI junk | `verified-adaptive` | Verified bank + adaptive review |
| 4 | `After Study Sprint` | Already used free samples/courses | `after-study` | Skip another course — practice for the exam |
| 5 | `Student College` | Degree / capstone / required for graduation | `student-college` | College cyber programs that require Security+ |

Prefer one live RSA in `24h Trial`. Pause Back to School headlines in the older groups if they stay enabled.

**Defer to later:** Military/DoD 8140, workforce/WIOA.

Final URL pattern:

```text
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal_launch40&utm_content=<slug>
```

---

## Keywords

See [[Sec+ Launch 40 Keyword Lists]] (includes Student College).

**Do not bid on** creator brands as positives. **Do not bid on** naked `practice questions` / `practice test`.

---

## Campaign negatives (paste first)

Paste from [[Sec+ Launch 40 Keyword Lists]] (includes dump / cheat / actual-exam / PDF). Do not omit dump or cheat negatives.

---

## RSA direction

**Headlines ≤30 characters** · Descriptions ≤90 · Pin H1 + H2 only

Full paste sheets: [[Sec+ Launch 40 RSA Copy]]

| Pin | Headline | Chars |
|-----|----------|------:|
| H1 | `Try 24 Hours Free` | 17 |
| H2 | `Then 30 Days at $15.99` | 22 |

Do not run Back to School / public $15.99 sale headlines.

---

## Site offer

| Surface | Behavior |
|---------|----------|
| Purchase card | $19.99 / 30 days · secondary CTA Try 24 hours free |
| 24h checkout | $0 Stripe Checkout Session · card not required |
| 30-day after trial | Prefill `SECPLUS24` → $15.99 |
| 30-day without trial | $19.99 · no promo prefill |

Verified learner discounts page stays separate for deeper eligibility discounts.

---

## Ops cadence

| Window | Action |
|--------|--------|
| Pre-launch | Offer + tracking + negatives ready · Stripe 20% code live |
| Days 1–7 | **$15/day** · search terms daily · negatives only (dump/cheat first) |
| Days 8–14 | Prune spenders · exact-match promote converters |
| Days 15+ | Keep $15/day until **$465** cumulative, or pause if no checkout after clean traffic |
| End | Pause at **~$450–$465** spent · or after the kill rule |

---

## Approval / build status

**Build checklist:** [[Sec+ Launch 40 Build Checklist]] · CSV `secplus-launch40-build-checklist.csv`

- [x] Set **$15/day** · **$465** total · no end date (pause at cap)
- [x] Public offer: 24 hours free, then $15.99 (`SECPLUS24`) while trial is active
- [x] Back to School banner removed (`secplus-bts-promo.js` retired)
- [ ] Pause Back to School RSA headlines in Google Ads · paste [[Sec+ Launch 40 RSA Copy]]
- [x] Build campaign in Google Ads · **running 2026-08-10**
- [ ] Confirm Stripe coupon live → $15.99 (spot-check if not done)
- [ ] Week 1: search terms daily · negatives only · hold structure 7 days
- [ ] Kill check: after $70–90 clean spend with 0 `begin_checkout`, pause and fix

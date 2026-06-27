---
type: campaign-scorecard
product: secplus
phase: 1
tags:
  - marketing
  - kpi
  - secplus
  - goals
---

# Sec+ Phase 1 — numeric goals & scorecard (Question 2)

**Status:** **Confirmed 2026-06-24** · **Purpose:** [[Sec+ Phase 1 Purpose]] · **Ops:** [[Sec+ Notes]] · **Spend log:** [[google-ads-spend-promo-2026.csv]]

**Monthly CSV:** [[secplus-monthly-scorecard.csv]] — one row per calendar month.

---

## Conversion-first (confirmed)

| Priority | Metric | Target | Action when weak |
|----------|--------|--------|------------------|
| 1 | **Ads clicks** | Maximize within $20/day per campaign · CPC ≤ $2.75 | Improve RSA/CTR; don’t cut budget pre-maturely |
| 2 | **Landing checkout rate** | **Primary** — `begin_checkout` on cert home ÷ landing views | Fix landing before keyword cuts |
| 3 | **Paid → checkout** | **≥ 2%** month · **≥ 3%** strong | RSA message match · mobile checkout |
| 4 | **Click → checkout** | Log Ads clicks daily; trend up | Align ad promise with landing |
| 5 | **Purchase** | Trend toward ~20–25/month | Stripe/PayPal friction |
| 6 | **Keywords / budget** | Spend on terms with checkout signal | Pause ≥20 clicks / 0 checkout |

**Rule:** If **checkout &lt; 2%** with **≥ 50** paid sessions → **landing + RSA first**, not keyword mass changes.

---

## Two time horizons

| Horizon | Job | Success = |
|---------|-----|-----------|
| **21-day sprint** (tactical) | Validate funnel + keywords | Checkout signal + clean search terms — **not** monthly break-even |
| **Monthly** (strategic) | Paid spend vs all-in revenue | ≤ **20% loss** or cut back; trend toward **stable** |

Do **not** judge the first 7 days against monthly break-even. At **$60/day total**, a 21-day run can spend **~$1,260**, so keyword quality and checkout signal matter before purchase volume fully settles.

---

## Monthly scorecard (primary)

Fill [[secplus-monthly-scorecard.csv]] at month-end.

| Metric | Target | Cut-back / review |
|--------|--------|-------------------|
| **Paid ad spend** | **~$1,800/month** if all three campaigns run full month | — |
| **All-in Sec+ revenue** (Stripe + PayPal + organic) | Match paid spend | — |
| **Net (revenue − paid spend)** | **≥ −20% of spend** | **&lt; −20%** → cutback playbook |
| **Loss %** | **≤ 20%** | **&gt; 20%** two weeks in a row → cutback |
| **Purchases (all-in)** | **~90** = break-even at $1,800 · **~72** = OK loss band | Below trend with clean traffic → deep review |
| **Paid purchases** | Track separately | — |
| **Organic purchases** | Track separately | Counts toward $500 revenue |
| **Paid sessions** (GA4) | Trend up | Flat 30 days + rising spend → message/keyword issue |
| **begin_checkout** (paid) | Trend up | See funnel gates below |
| **Checkout rate** (paid sessions → begin_checkout) | **≥ 2%** month avg · **≥ 3%** = healthy | **&lt; 1%** after **≥ 200** paid sessions → fix landing/RSA |
| **Purchase rate** (paid sessions → purchase) | Track; expect low early | **0 purchases** after **≥ $200** spend in month → cutback tier 2 |
| **CAC** (paid spend ÷ paid purchases) | **≤ $40** = on path to monthly BE | **&gt; $60** sustained → cutback tier 2 |
| **Avg CPC** | **≤ $2.75** cap | — |
| **Promo progress** | $500 eligible spend by Jul 19 | [[Google Ads Spend Promo]] |

### Revenue split (same month)

| Source | Column |
|--------|--------|
| Stripe Sec+ | `stripe_revenue_usd` |
| PayPal Sec+ | `paypal_revenue_usd` |
| Organic (no paid UTM) | `organic_revenue_usd` |
| **Total all-in** | `all_in_revenue_usd` |

Organic marketing (Reddit, forums) **counts on revenue side only** until stable; paid Reddit stays **off** unless recommended inside budget.

---

## 21-day sprint goals (Jun 23 launch → ~Jul 14)

**Spend expectation:** up to **~$1,260** at $60/day for 21 days if all three campaigns run the full sprint.

| Metric | Minimum “continue” | Strong signal |
|--------|-------------------|---------------|
| **begin_checkout** (paid, GA4) | **≥ 5** total in 21 days | **≥ 15** |
| **Checkout rate** | **≥ 2%** once **≥ 100** paid sessions | **≥ 3%** |
| **Purchases (all-in)** | **≥ 1** | **≥ 3** |
| **Search terms** | Day 3 + 7 negatives pasted | No dominant course/free junk |
| **Keyword winners** | **≥ 3** terms with clicks + checkout | Promote to `[exact]` |
| **Ads spend ÷ purchases** | Not judged until **≥ 2** paid purchases | **≤ $40** per purchase |

**21-day fail (pause & fix, don’t refresh $500 blindly):**

- **≥ $150** spend and **0** `begin_checkout`, **or**
- **≥ $250** spend and **0** purchases

**21-day pass (continue $20/day per campaign into next month):**

- Checkout rate **≥ 2%** with **≥ 5** checkouts, **or**
- **≥ 2** purchases with search terms mostly on-target

---

## Weekly leading indicators (during sprint)

| Week | Check | Action if miss |
|------|-------|----------------|
| **1** | Ads serving · GA4 checkout on test click · search terms day 3 | Fix tracking / RSA before more spend |
| **2** | Checkout rate direction · avg CPC ≤ $2.75 | Adjust keyword bids from week-1 results |
| **3** | Any purchase or checkout trend up | Add exact keywords from search terms |
| **4** | Document 3 best terms + 3 negatives | Update [[secplus-keywords.csv]] |

---

## Cutback playbook

### Tier 1 — tighten (loss 20–35% or weak checkout)

- Keep campaign **on** at **$10/day**
- Max CPC **$2.25**
- Pause phrase keywords with **≥ 20 clicks, 0 checkout**
- Re-read RSA vs [[Sec+ RSA Copy]]

### Tier 2 — pause & fix (loss &gt; 35% or funnel broken)

- **Pause** campaign **7 days**
- Fix: landing checkout, mobile, 30-day-only message, GA4 primary conversion
- Restart at **$10/day** after test checkout confirmed

### Tier 3 — stop paid until stable organic proof

- **≥ $400** spend in 60 days, **≤ 2** all-in purchases, checkout **&lt; 1%**
- Shift to organic only; revisit paid when **≥ 3** organic sales/month

---

## Keyword & conversion rules (data-driven)

| Rule | Action |
|------|--------|
| Search term **≥ 3 clicks** + **begin_checkout** | Add **`[exact]`** |
| Keyword **≥ 20 clicks**, **0 checkout** | Pause phrase; keep exact if exists |
| Search term course/free/dump | Campaign or ad group **negative** same day |
| Generic `"practice questions"` / `"practice test"` / `"practice exam"` (course-shopper CPC) | **Removed from positives + campaign negatives** (2026-06-25) |

Promote list lives in monthly CSV notes + [[Sec+ Keywords]] export.

---

## Stable checklist (exit Phase 1)

Mark **stable** when **either** is true for **one full calendar month**:

- [ ] All-in revenue **≥ $400** and paid spend **≤ $500** (within 20% loss band) **and** checkout rate **≥ 2%**
- [ ] All-in revenue **≥ $500** and paid spend **≤ $500** (break-even)
- [ ] **Two consecutive months** of **≥ 10% revenue growth** (all-in) with paid spend held **≤ $500**

Then: plan CCNA/ENCOR, Reddit paid (if recommended), full business expense sheet.

---

## Review — confirm or edit these numbers

| # | Default | Status |
|---|---------|--------|
| 1 | Monthly loss cap **$100** (20% of $500) | **Confirmed** |
| 2 | Checkout rate **≥ 2%** month / **≥ 3%** strong | **Confirmed** |
| 3 | 21-day: **≥ 5** checkouts or **≥ 2** purchases to continue | **Confirmed** |
| 4 | 21-day fail: **$150** spend / **0** checkout | **Confirmed** |
| 5 | CAC warning **&gt; $60** · on-path **≤ $40** | **Confirmed** |
| 6 | Tier 1 cutback **$10/day** · Tier 2 pause **7 days** | **Confirmed** |
| 7 | **Conversion-first:** landing tracked hardest; budget follows converters | **Confirmed** |

[[README|← Sec+ Campaign]]

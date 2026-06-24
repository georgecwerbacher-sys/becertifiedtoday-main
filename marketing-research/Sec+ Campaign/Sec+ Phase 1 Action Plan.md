---
type: campaign-ops
product: secplus
phase: 1
tags:
  - marketing
  - action-plan
  - secplus
---

# Sec+ Phase 1 — what we need from you

**Purpose:** [[Sec+ Phase 1 Purpose]] · **Numbers:** [[Sec+ Phase 1 Scorecard]] · **Landing ops:** [[Sec+ Notes#Landing conversion (track hardest)]]

This is the project runbook — not competitor research. Competitors sell dumps ($49–99 one-time) and courses ($300+). You sell **browser PBQ + timed sim for $19.99/30d**. That gap is the ad angle; we optimize **after the click** until checkout data says otherwise.

---

## Project state (now)

| Piece | Status |
|-------|--------|
| Google Ads Sec+ | Live · $15/day · PBQ ad group |
| Landing | 30-day only · samples on page |
| Tracking | GA4 + admin 21-day plan · **landing checkout rate** added |
| Billing / promo | ~**$256 / $500** toward credit · [[Google Ads Spend Promo]] |
| Scorecard | **Confirmed** · conversion-first |
| PayPal | Not live yet — add when ready (counts all-in) |
| Membership / funnel pages | **Not built** — see experiment menu below |

**Blocker:** Not enough **post-click** data yet. First job is **clicks logged + landing checkout rate**, not new products.

---

## Your job — standing (every week)

Open **Admin → 21-day plan → click the calendar day** for that day&apos;s checklist, then log spend below.

| # | You do | Where |
|---|--------|--------|
| 1 | Check off **day checklist** + log **Ads spend + clicks** | [/admin/#section-campaign-plan](https://becertifiedtoday.com/admin/#section-campaign-plan) |
| 2 | Export **Search terms** on day 3, 7, 14, 21 → add negatives | Google Ads |
| 3 | One **landing or RSA change** at a time; check **Landing page change shipped** | Admin daily log |
| 4 | Month-end: fill **revenue** columns | [[secplus-monthly-scorecard.csv]] |
| 5 | Reconcile promo spend | Google promo widget vs [[google-ads-spend-promo-2026.csv]] |

---

## This week (concrete)

- [ ] **Day 3 (~Jun 27):** Search terms CSV → paste or note junk queries to negate
- [ ] **Log Jun 24–today:** spend **$9.63** Jun 24 + each day since (clicks, impressions, CPC)
- [ ] **Test purchase path:** ad URL on **phone** → sample → **Get 30-day** → GA4 Realtime `begin_checkout`
- [ ] **Ads cleanup** if not done: no $9.99/10-day in RSA or sitelinks ([[Sec+ Notes#Remove 10-day from live Google Ads]])
- [ ] **Confirm** Google promo progress matches ~**$256+** account spend

---

## Decision gates — what to change when

Use admin **landing checkout rate** and **click → checkout** (after clicks logged). **One change per week.**

| Signal (after ≥ ~50 paid sessions or ≥ ~30 logged clicks) | Change first | Defer |
|-------------------------------------------------------------|--------------|-------|
| Clicks OK, **landing checkout &lt; 1%** | Landing hero, purchase block, mobile sticky, sample CTA | Price, membership |
| **Checkout 2%+, purchases 0** | Stripe/mobile friction, trust (FAQ, guarantee wording) | New funnel pages |
| **Checkout OK, wrong traffic** | Negatives + pause bad keywords | Landing rewrite |
| **One search term converts** | Add `[exact]`, optional RSA line for that intent | New ad group |
| **Stable month** (scorecard) | PayPal, Reddit organic, second product | Paid Reddit |

---

## Experiment menu (your options — in order)

Do **not** stack these in one week. Mark in admin notes which test is live.

### Tier A — do while traffic is thin (now → day 21)

| Experiment | Effort | What we learn | Your action |
|------------|--------|---------------|-------------|
| **RSA / sitelink** message match | Low | Click quality | Paste from [[Sec+ RSA Copy]]; pin H2 sim not price |
| **Above-fold purchase path** | Low | Landing checkout rate | One clear CTA to `#purchase` after sample hook |
| **Mobile checkout** | Low | Drop-off after click | Fix anything broken thumb-tap → Stripe on iPhone |
| **Sample → purchase bridge** | Low | Sample viewers who checkout | Short line after PBQ preview: “Unlock all 34 scenarios” |
| **Search term negatives** | Low | Waste spend | Day 3 export — you paste negatives in Ads |

### Tier B — after checkout rate ≥ ~2% or ≥ 5 checkouts in 21 days

| Experiment | Effort | What we learn | Your action |
|------------|--------|---------------|-------------|
| **PayPal** | Medium | Payment friction | Implement; tag revenue in monthly CSV |
| **Price test ($24.99 or $17.99)** | Medium | Willingness to pay | **One price** for 30 days min; track checkout + purchase |
| **Dedicated wedge section** | Medium | PBQ intent conversion | Anchor block `#home-secplus-samples-title` → purchase (not new domain) |
| **Light “progress” copy** | Low | Trust without building accounts | “Scorecard + weak domains” in hero — no membership yet |

### Tier C — after stable month or strong checkout (not now)

| Experiment | Effort | Risk | Hold until |
|------------|--------|------|------------|
| **Membership / progress accounts** | High | Distraction from paid test | Stable scorecard; checkout proven |
| **Separate funnel landing pages** | High | Splits data, hurts Quality Score if misaligned | You want A/B with enough volume (500+ sessions/mo) |
| **10-day tier return** | Medium | Message conflict with ads | Only if data shows price objection, not trust |
| **Second Google ad group** | Medium | Budget split at $15/day | Tier 1 keyword winners exist |
| **Paid Reddit** | Medium | New channel | Google stable per [[Sec+ Phase 1 Purpose]] |

---

## What to send / add when you try something

When you ship a change, log in admin **Ops notes**:

```
TEST: [what changed]
HYP: [what should improve]
START: YYYY-MM-DD
END: review on day 7 after change
```

Examples:

- `TEST: sticky CTA copy → "Unlock 30-day · timed sim" · HYP: landing checkout up · START: 2026-06-28`
- `TEST: price $24.99 · HYP: fewer checkouts, higher revenue per buy · START: 2026-08-01`

No new analytics required for Tier A — use existing admin metrics.

---

## Competitor context (minimal)

- **Dumps / ExamTopics:** cheap, high intent, wrong buyer for you — stay negated.
- **Boson / sim vendors:** higher price, desktop sim — your wedge is **browser PBQ + $19.99 sprint**.
- **Courses (Udemy, Dion):** negated in Search; organic Reddit can mention “already studied, need PBQ prep.”

You are **not** competing on “most questions.” Ads + landing must say **ready for PBQ + timed sim**, not cheapest bank.

---

## What I will drive in repo (you don’t need to ask)

- Checklist / keyword CSV sync after search term reviews you paste
- Scorecard + spend CSV updates when you drop billing exports
- Landing copy/HTML when you pick **one** Tier A/B test to implement
- Admin alignment with scorecard gates

---

## Next review with you

**Day 7 (~Jun 30):** Bring logged clicks + checkout rate + search terms. We decide: landing tweak **or** keyword pause **or** hold.

[[README|← Sec+ Campaign]]

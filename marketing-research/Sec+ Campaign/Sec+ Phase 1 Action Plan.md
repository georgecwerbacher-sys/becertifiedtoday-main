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

**Purpose:** [[Sec+ Phase 1 Purpose]] · **Numbers:** [[Sec+ Phase 1 Scorecard]] · **Landing ops:** [[Sec+ Notes#Landing conversion (track hardest)]] · **Phase 2:** [[Sec+ Phase 2 Institutional Targeting]]

This is the project runbook — not competitor research. You sell **browser exam prep for $19.99/30d** (timed sim, verified bank, adaptive review). Phase 2 moves to **three US-only Google campaigns at $20/day each**: core exam prep, military/government, and student/workforce ([[Sec+ Three-Campaign US Plan]]). Admin tracking is not changed yet.

---

## Project state (now)

| Piece | Status |
|-------|--------|
| Google Ads Sec+ | Baseline live · next build = **3 US-only campaigns × $20/day** |
| Landing | 30-day only · samples on page |
| Tracking | GA4 + admin 21-day plan · **landing checkout rate** added |
| Billing / promo | ~**$256 / $500** toward credit · [[Google Ads Spend Promo]] |
| Scorecard | **Confirmed** · conversion-first |
| PayPal | Not live yet — add when ready (counts all-in) |
| Membership / funnel pages | **Not built** — see experiment menu below |

**Blocker:** Admin still reads the baseline flow. If the three-campaign plan launches before admin is expanded, reconcile by `utm_campaign` manually in Google Ads / GA4 notes.

---

## Your job — standing (every week)

Open **Admin → 21-day plan → click the calendar day** for that day&apos;s checklist, then log spend below. **Saving a day updates the Campaign tracker** below with running spend, clicks, and next-day review tasks.

| # | You do | Where |
|---|--------|--------|
| 1 | Check off **day checklist** + log **Ads spend + clicks** | [/admin/#section-campaign-plan](https://becertifiedtoday.com/admin/#section-campaign-plan) |
| 2 | **Day 3 done (Jun 25):** Keyword CSV synced + Negatives added checkboxes · overview export in repo | Admin D3 · uncheck **Campaign-level negatives pasted** until Google UI paste complete |
| 3 | Export **Search terms** on day 7, 14, 21 → add negatives | Google Ads |
| 4 | One **landing or RSA change** at a time; check **Landing page change shipped** | Admin daily log |
| 5 | Month-end: fill **revenue** columns | [[secplus-monthly-scorecard.csv]] |
| 6 | Reconcile promo spend | Google promo widget vs [[google-ads-spend-promo-2026.csv]] |

---

## This week (concrete)

- [ ] **Paste in Google Ads:** 13 pending campaign negatives + pause 3 removed positives · then check **Campaign-level negatives pasted** in admin setup
- [ ] **Three-campaign draft:** build paused campaigns from [[Sec+ Three-Campaign US Plan]]
- [ ] **Ad schedule:** US-only · before work / lunch / after work / weekends on all three campaigns
- [ ] **Day 7 keyword review:** adjust keyword bids based on results; pause weak track before changing landing
- [ ] **Test purchase path:** ad URL on **phone** → sample → **Get 30-day** → GA4 Realtime `begin_checkout`
- [ ] **Phase 2 prep (no admin change):** read [[Sec+ Phase 2 Institutional Targeting]] · draft verified discount page copy (students, educators, veterans, workforce)
- [ ] **Launch verify page:** index `/how-we-verify-questions.html` + link from cert home when ready
- [ ] **Confirm** Google promo progress toward $500 spend ([[Google Ads Spend Promo]])

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
| **RSA Phase 2 paste** | Low | Exam prep message vs PBQ wedge | [[Sec+ RSA Copy#Phase 2 — exam prep lead (paste when ready)]] |
| **Sitelinks Phase 2** | Low | Bank/verify vs PBQ-only extensions | [[Extensions#Phase 2 sitelinks (paste when ready)]] |
| **PayPal** | Medium | Payment friction | Implement; tag revenue in monthly CSV |
| **Price test ($24.99 or $17.99)** | Medium | Willingness to pay | **One price** for 30 days min; track checkout + purchase |
| **Verification page live** | Low | Trust for DoD/college traffic | Link `/how-we-verify-questions.html` from cert home |
| **Light “progress” copy** | Low | Trust without building accounts | “Scorecard + weak domains” in hero — no membership yet |

### Tier C — after stable month or strong checkout (not now)

| Experiment | Effort | Risk | Hold until |
|------------|--------|------|------------|
| **Verified learner discount** | High | Stripe promo + `.edu`/partner verify | [[Sec+ Phase 2 Institutional Targeting]] — engineering |
| **Three US campaigns** | Medium | $20/day each track | [[Sec+ Three-Campaign US Plan]]; launch paused drafts first |
| **Institutional keyword tier** | Medium | Track-level intent | Split manually by campaign until CSV generator supports tiers |
| **Geo bid adjustments (US bases/campuses)** | Low | Local intent | US only; log in admin notes |
| **College outreach list** | Medium | Time, not ad spend | Organic / email first |
| **Membership / progress accounts** | High | Distraction from paid test | Stable scorecard; checkout proven |
| **Separate funnel landing pages** | High | Splits data, hurts Quality Score if misaligned | You want A/B with enough volume (500+ sessions/mo) |
| **Second Google ad group** | Medium | Budget split risk | Tier 1 keyword winners exist |
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

- **Dumps / ExamTopics:** cheap, high intent, wrong buyer — stay negated.
- **Boson / sim vendors:** higher price, desktop sim — your wedge is **browser exam prep + $19.99 sprint**.
- **Courses (Udemy, Dion):** negated in Search; organic can mention “already studied, need timed sim prep.”

Ads + landing must lead with **exam prep + timed sim + verified bank**, not cheapest question count or free samples.

---

## Phase 2 preview (planning only — no admin change)

When Phase 1 checkout is proven:

1. **Institutional targeting** — [[Sec+ Phase 2 Institutional Targeting]]
2. **Verified learner discount** — students, educators, veterans, workforce programs; `.edu`/partner verification; checkout email receives account and access links
3. **RSA + sitelinks** — exam prep lead ([[Sec+ RSA Copy]], [[Extensions]])
4. **Geo bid adjustments** — US bases, federal hubs, college towns, workforce metros
5. **Keyword tier** — institutional phrases appended, not replacing base 64

## What I will drive in repo (you don’t need to ask)

- Checklist / keyword CSV sync after search term reviews you paste
- Scorecard + spend CSV updates when you drop billing exports
- Landing copy/HTML when you pick **one** Tier A/B test to implement
- Admin alignment with scorecard gates

---

## Next review with you

**Day 7 (~Jun 30):** Bring logged clicks + checkout rate + search terms. We decide: landing tweak **or** keyword pause **or** hold.

[[README|← Sec+ Campaign]]

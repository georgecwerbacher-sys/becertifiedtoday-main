---
type: campaign-strategy
product: secplus
phase: launch-40
status: locked-budget-promo
tags:
  - marketing
  - google-ads
  - secplus
  - budget
  - conversions
---

# Sec+ Launch Campaign Plan — $1k performance flight

**Status:** Budget + promo locked · Stripe code **`AUGUSTPROMO2026`** (20%) · ads not built yet  
**Goal:** Conversions (checkout → purchase)  
**Offer:** list **$19.99** / 30 days in ads · **20% decision assist** for fence-sitters only (locked)  
**Daily budget:** **$35** (locked) · ~29 days on $1,000 if spend is steady  
**Landing:** https://becertifiedtoday.com/comptia-sec+-home.html#home-secplus-samples-title

Related: [[Sec+ Positioning]] · [[Sec+ Keywords]] · [[Sec+ Launch 40 Keyword Lists]] · [[Sec+ Notes]] · [[Sec+ RSA Copy]] · prior spend [[Google Ads Spend Promo]]

---

## Budget pacing (locked)

| Item | Value |
|------|------:|
| Total | $1,000 |
| Daily | **$35** (locked) |
| Expected flight | **~29 days** if spend is steady |
| List price | $19.99 |
| Decision assist | **20% → $15.99** (fence-sitters only, locked) |
| Purchases to recover $1k (at $15.99) | ~63 |
| Stripe coupon | **`AUGUSTPROMO2026`** (20% off Sec+ 30-day) |

**Why not $17/day × 60:** Prior Sec+ runs on this site already cleared ~$2–$2.40 CPC and ~$25/day volume. Stretching spend dilutes auction share against course sellers who use free samples to upsell. Spend the $1k while learning is productive; stop early if checkout stays dead.

**Kill rule:** After **$150–200** on clean (negatived) traffic with **0 `begin_checkout`**, pause and fix landing/offer/tracking before burning the rest.

### Prior data used (Jun 2026)

| Signal | Observation |
|--------|-------------|
| CPC | ~$2.05–$2.41 |
| Live Sec+ days | $9.63 / 4 clicks · $24.58 / 12 clicks |
| Earlier Sec+ peaks | up to ~$28/day |
| Junk | Dion brand, PDF, naked practice exam/questions |
| Keep | PBQ practice, timed practice test, performance-based |

Share newer Google Ads / Stripe exports anytime to retune CPA targets from real purchases.

---

## Positioning (vs sample → course upsell)

Security+ is entry-level. Free study + creator samples already exist. Creators monetize with **course upsells**. You monetize with **simulated exams + verified adaptive practice**.

| They sell | You sell |
|-----------|----------|
| Free samples → paid course | Free samples → timed sim + verified bank |
| Video bootcamps | Browser simulated exams + scorecard |
| Account signup + email list | **No site registration** — pay in **Stripe**, access via **magic link** |
| PDF dumps / static packs | Adaptive review, not a PDF |
| Generic / AI lists | Curriculum-aligned verified questions |

**Access friction (RSA + landing proof):**

- No account to create on becertifiedtoday.com
- Checkout is Stripe only (no separate signup form collecting email for a membership DB)
- Portal access is magic-link after purchase

Accurate ad line: *No registration. Pay with Stripe. Magic-link access.*  
Avoid overclaiming “we never see your email” if the Stripe checkout email is used to send the magic link.

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
| Promo | **20% fence-sitters only** (locked) — code **`AUGUSTPROMO2026`** · never in RSA |
| utm_campaign | `secplus_portal_launch40` |

**Hold rule:** No structure / bid drama for 7 days unless junk traffic or broken tracking.

---

## Three ad groups (shared budget)

| # | Ad group | Intent | `utm_content` | Lead message |
|---|----------|--------|---------------|--------------|
| 1 | `Timed Simulation` | Am I ready? | `timed-sim` | 90-min simulated exam + scorecard |
| 2 | `Verified Adaptive Prep` | Not PDF / not AI junk | `verified-adaptive` | Verified bank + adaptive review |
| 3 | `After Study Sprint` | Already used free samples/courses | `after-study` | Skip another course — practice for the exam |

**Defer to Phase 2** (after core converts): Military/DoD 8140, Student/Workforce.

Final URL pattern:

```text
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal_launch40&utm_content=<slug>#home-secplus-samples-title
```

---

## Keywords

Match: `[exact]` · `"phrase"`

### Ad group 1 — Timed Simulation

**Exact**

```
[security+ timed practice test]
[security+ exam simulation online]
[security+ mock exam online]
[sy0-701 timed mock exam]
```

**Phrase**

```
"security+ practice exam simulation"
"security+ timed exam simulation"
"90 minute security+ practice test"
"security+ timed practice test online"
"security+ exam simulation online"
"security+ realistic practice test"
"sy0-701 timed mock exam"
"security+ scorecard review"
```

### Ad group 2 — Verified Adaptive Prep

**Exact**

```
[security+ pbq practice]
[security+ performance based questions]
[sy0-701 pbq]
[comptia security+ pbq]
```

**Phrase**

```
"security+ adaptive review"
"security+ practice portal"
"security+ interactive scenarios"
"security+ browser exam simulator"
"security+ no download practice"
"security+ not a pdf"
"sy0-701 objective based prep"
"security+ pbq practice online"
"security+ hot spot practice"
"security+ drag and drop practice"
```

### Ad group 3 — After Study Sprint

**Phrase** (no creator brands as positives)

```
"security+ after course practice"
"security+ last minute exam prep"
"security+ readiness check"
"security+ exam prep online"
"sy0-701 prep"
"security+ study prep online"
"security+ practice before exam"
"security+ exam readiness practice"
"security+ practice instead of course"
"security+ self study practice exam"
```

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

**Headlines ≤30 characters** · Descriptions ≤90 · Pin H1 + H2 only · **no % off**

Full paste sheets: [[Sec+ Launch 40 RSA Copy]]

| Pin | Headline | Chars |
|-----|----------|------:|
| H1 | `SY0-701 Exam Prep Online` | 24 |
| H2 | `Timed 90-Min Exam Sim` | 21 |

**Headline pool (all ≤30) — shared themes**

```
SY0-701 Exam Prep Online
Timed 90-Min Exam Sim
Am I Ready? Scorecard
90-Min Timed Exam Sim
Domain Scorecard Review
Browser Exam Simulation
1000+ Verified SY0-701 Qs
Verified SY0-701 Bank
Adaptive Review Modes
Not a PDF · Browser Prep
No Site Registration
Pay With Stripe
Magic Link Access
30-Day Access · $19.99
Skip Another Course
```

**Do not** put % off, `AUGUSTPROMO2026`, or flash-sale language in RSA headlines or sitelinks.

---

## Decision assist (fence-sitters only)

For people who already engaged and stall — **not** a public sale. Same soft **20%** can follow them across samples and the timed simulation.

| Trigger | Why | When to show |
|---------|-----|--------------|
| **Free samples** (MCQ / PBQ preview) | Tried the product; deciding on full access | After finishing a sample or on return to home from sample |
| **Timed test simulation** | Just finished exam pressure; high intent | Soft offer **before scorecard is OK**, but **scorecard is never gated**. If they skip/don’t buy, they still get results. **Preferred:** ~**20 seconds after** they start reviewing the scorecard. |
| Checkout hesitate / leave after engagement | On the edge of buying | Soft prompt only — no flash framing |

| Option | Price | When | Tone |
|--------|------:|------|------|
| **20% off** | $15.99 | **Default** | Quiet help to decide |
| 25% off | $14.99 | Only if 20% never moves fence-sitters | Still soft; test carefully |
| 40% off | $11.99 | **Not** as a general nudge | Keep for verified-learner path only |

### Sim scorecard flow (hard rules)

1. Timed exam ends → optional soft, dismissible 20% prompt **before** scorecard.
2. Decline / ignore / no purchase → **scorecard still opens** (no hold, no delay for payment).
3. **Preferred nudge:** ~**20 seconds after** scorecard is visible and they’re reviewing results.
4. Never interrupt mid-exam questions. Never block or watermark the scorecard behind purchase.

| Do | Don’t |
|----|-------|
| Follow sample + sim users with the same soft 20% (session/cookie) | Interrupt mid-sample or mid-exam |
| Optional dismissible prompt when sim ends, before scorecard | Hold scorecard until they buy |
| Preferred: offer ~20s into scorecard review | Flash sale · limited time · ends tonight |
| After scorecard: *Ready for more practice? 20% off full access* | Force offer before results or gate the scorecard |
| Keep $19.99 in ads, hero, sitelinks | Lead with % off in RSA |
| Verified 40% stays eligibility-only | Repeated aggressive popups over the scorecard |

### Setup checklist

1. Stripe coupon **`AUGUSTPROMO2026`** — 20% off Sec+ 30-day (live)
2. Soft prompt after sample complete / return from sample
3. Sim: **scorecard always unlocks** — never gated on purchase
4. Optional: soft dismissible offer when sim ends, before scorecard
5. Preferred: soft offer **~20s after scorecard review starts**
6. Optional: same offer on checkout hesitate after engagement
7. Ads + hero stay at **$19.99** — no strike-through in ads
8. No RSA / sitelink / banner mention of the %
9. Measure by trigger: sample / pre-scorecard / post-scorecard-20s / checkout

---

## Ops cadence

| Window | Action |
|--------|--------|
| Pre-launch | Offer + tracking + negatives ready · Stripe 20% code |
| Days 1–7 | **$35/day** · search terms daily · negatives only |
| Days 8–14 | Prune spenders · exact-match promote converters |
| Days 15+ | Scale winners or pause if no checkout after clean traffic |
| End | When $1k spent or CPA unacceptable — not day 60 |

---

## Approval next steps

**Build checklist:** [[Sec+ Launch 40 Build Checklist]] · CSV `secplus-launch40-build-checklist.csv`

- [x] Lock **$35/day** performance pacing
- [x] Lock **20% decision assist** for fence-sitters (no flash sale / not in ads)
- [x] Stripe 20% coupon: **`AUGUSTPROMO2026`**
- [ ] Soft site prompts (sample / sim pre-scorecard optional / **~20s after scorecard**) — wire code `AUGUSTPROMO2026`
- [ ] Optional: share newer Ads/Stripe exports for CPA targets
- [ ] Approve ad group + keyword split (still open)
- [ ] Draft full RSA paste sheets (no % off)
- [ ] Build campaign in Google Ads

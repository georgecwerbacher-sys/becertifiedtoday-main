---
type: strategy
status: active
tags:
  - promotions
  - coupons
  - google-ads
  - conversion
  - exam-prep
created: 2026-06-01
---

# Promotions & coupons — when to use them

Exam-prep positioning: [[positioning-and-messaging|positioning]] · Paid launch: [[google-ads-bidding-strategy|bidding strategy]] · Security+ funnel: [[../02-campaigns/security-plus/security-plus-google-ads|Security+ Google Ads]]

**Site / Stripe:** Checkout can accept promotion codes (`allow_promotion_codes: true` in `api/create-checkout-session.js`). Codes are created in **Stripe Dashboard** (Coupons → Promotion codes).

---

## Default (launch phase)

**Do not run a public coupon CTA** in Google Ads, hero purchase blocks, or sitewide popups while:

- Security+ is the only live paid campaign at **~$10/day**
- You are still establishing baseline **CTR → `generate_lead` → `begin_checkout` → purchase** on **list price**
- You have fewer than **~15–30** primary conversions in 30 days to compare against

**Primary engagement lever instead:** free timed simulation + scorecard (lead ad groups), clear **$9.99** / **$19.99** one-time pricing, and “try before you buy” copy — not % off.

| Do now | Hold off |
|--------|----------|
| `secplus_lead_free_sim` / future `ccna_lead_free_sim`, `encor_lead_free_sim` | Coupon in RSA headlines (“50% off Security+”) |
| Ad copy: free 35–45 min sample, $9.99 one attempt, no subscription | Sitewide discount banner on first visit from Ads |
| Sitelinks to free sim and sample questions | Auto-applied checkout discount for all traffic |
| “Cheaper than a retake” angle (value, not coupon) | Competing on “cheapest Security+ course” keywords |

**Why:**

1. **$9.99 sim** is already positioned below PDF (~$100) and video courses ($200+).
2. **Coupons muddy Ads learning** — you cannot tell if keyword/LP or discount drove conversion.
3. **Deal-seeker risk** — wrong intent vs test-date / compliance urgency ([[security-plus-federal-defense-foundation|federal foundation]]).
4. **Trust** — pillar “clear pricing before checkout”; surprise codes can feel dump-adjacent.
5. **Low volume** — at ~3 clicks/day, a coupon A/B teaches almost nothing.

---

## What counts as “engagement” without a coupon

| Stage | CTA | Conversion |
|-------|-----|------------|
| Top | Free timed sim + email unlock | `generate_lead` |
| Mid | Sample questions / PBQ (no checkout) | Engagement / scroll |
| Bottom | $9.99 timed sim · $19.99 portal | `begin_checkout` → purchase |

Google Ads: lead ad group first; purchase ad group second. See [[../05-playbooks/google-ads-bidding-verification|bidding verification]].

---

## When to introduce a promotion

Use **all** gates before a site-wide or ad-visible offer:

| Gate | Threshold |
|------|-----------|
| Ads baseline | ≥ **14 days** Security+ live; search terms cleaned |
| Conversions | ≥ **15–30** `generate_lead` and/or `begin_checkout` at **full price** in 30 days |
| CPA known | Rough CPA documented in weekly report ([[../05-playbooks/weekly-review-process|weekly review]]) |
| Channel | Prefer **owned audience** first (email), not new Search traffic |

---

## Approved promotion channels (priority order)

### 1. Email to free-sim leads (best first test)

**Audience:** Completed free sim / scorecard; no purchase within 3–7 days.

**Offer examples (small, time-boxed):**

- $2 off 90-min sim (e.g. $7.99 effective)
- Free sitewide code **not** advertised in Search ads

**Tracking:** Unique Stripe promotion code per send; UTM `utm_medium=email` · `utm_campaign=secplus_lead_nurture`.

**Do not** put the same code in RSA headlines until email test shows uplift without trashing margin.

### 2. Retargeting (after Search baseline)

**Audience:** Visited `#purchase` or fired `begin_checkout`; no purchase.

**Offer:** One-time code in ad **only** for retargeting campaign — separate `utm_campaign` (e.g. `secplus_retarget`).

**Budget:** Small slice; do not mix with $10/day learning campaign.

### 3. On-site A/B (controlled experiment)

**Test:** Upsell modal or post-scorecard CTA with vs without code.

**Log:** Note in `04-experiments/` with hypothesis, dates, conversion rate, revenue per visitor.

**Keep:** List price visible; code optional field at checkout only.

### 4. Google Ads headline coupon (last)

Only after email + retargeting prove incremental lift at acceptable **ROAS**.

**Policy:** Offer must match landing page; include expiry if limited time.

**Never:** “100% pass,” fake urgency, or implied CompTIA endorsement.

---

## What not to do

| Avoid | Reason |
|-------|--------|
| Coupon as primary RSA headline during launch | Trains deal seekers; hurts QS on prep keywords |
| Permanent “always on” 20% off | Anchors price; hard to remove |
| Codes on **free sim** flow | Free should stay free; no friction |
| Deep discounts (&gt; 30% off $9.99) | Margin + brand; attracts wrong segment |
| Different prices in ad vs checkout | Policy + trust |
| Coupon before [[../06-website-optimization/ad-site-verification-2026-05-31|ad-site verification]] fixes on CCNA/ENCOR | Message mismatch risk |

---

## Stripe setup checklist (when you run a test)

- [ ] Coupon + **promotion code** in Stripe (usage limit, expiry, applicable products: sim vs portal)
- [ ] Test checkout with code → purchase value in GA4 / Ads matches **discounted** amount if using value-based bidding later
- [ ] Code **not** pre-filled for organic visitors unless experiment says so
- [ ] Document code, dates, audience in **## Decisions** of weekly report

---

## Product notes

| Product | List price (verify on site) | First promotion candidate |
|---------|----------------------------|-------------------------|
| Security+ SY0-701 | $9.99 sim · **$24.99 portal list** · **SECPLUS7** ($7 off → $17.99 one-time launch popup) | Email after free 35-min sim |
| CCNA 200-301 | $9.99 sim · $19.99 portal | After CCNA Ads launch + baseline |
| ENCOR 350-401 | $9.99 sim · $19.99 portal | Same |

---

## Stripe setup — Security+ 30-day launch coupon (2026-06-04)

Payment Link: `5kQ14mbwVgt93yEfo0c3m07` (see `secplus-portal-checkout.js`).

| Step | Stripe Dashboard |
|------|------------------|
| 1 | **Products** → 30-day Security+ pass → set price to **$24.99** (new Price on Payment Link if needed) |
| 2 | **Coupons** → Create → **Fixed amount** **$7.00** off (USD), one-time, optional expiry / max redemptions |
| 3 | **Promotion codes** → Create code **`SECPLUS7`** linked to that coupon |
| 4 | **Payment Links** → 30-day link → **Allow promotion codes**: ON |
| 5 | Paste live Payment Link URL into `LINKS["30d"]` in `secplus-portal-checkout.js` |
| 6 | Test: `{payment_link_url}?prefilled_promo_code=SECPLUS7` → total **$17.99** |

**Math:** $24.99 − $7.00 = **$17.99** (one-time launch deal).

Site behavior: launch popup open → checkout URL includes `prefilled_promo_code=SECPLUS7`. Popup closed → full **$24.99** link, no code.

**If your Stripe promotion code is not `SECPLUS7`**, set `LAUNCH_PROMO_CODE` in `public/COMP_TIA_SEC+/js/secplus-portal-checkout.js` to match.

---

## Decisions log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-06-01 | **No coupon** during Security+ $10/day launch | Free sim is engagement; need clean CPA data at list price |
| 2026-06-04 | **SECPLUS7** on-site only (launch popup); list **$24.99** → **$17.99** with coupon | Coupon not in Search RSAs; prefilled when popup open |

## Open questions

- [ ] Build `secplus_lead_nurture` email sequence (if not live) before first code test
- [ ] Define minimum acceptable **ROAS** for discounted sim vs full price
- [ ] Import **purchase value** (post-discount) into Google Ads if using conversion value bidding

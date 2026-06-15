---
type: funnel-phase
phase: Checkout
product: secplus
tags:
  - secplus
  - funnel
---

# Checkout — $9.99 / 10-day · $19.99 / 30-day

[[../../../SEC+ funnel build tracker|← Funnel tracker]] · [[../../../03-pricing-and-funnel|Pricing]]

## Live

- [x] Stripe `secplus-portal-10d` — $9.99
- [x] Stripe `secplus-portal-30d` — $19.99
- [x] GA4 `begin_checkout` — `secplus_portal_10d`, `secplus_portal_30d`
- [x] `secplus-portal-checkout.js` on home + wedge landing
- [x] One-time $9.99 popup — `bcc-10d-one-time-offer.js`
- [x] Mobile sticky 10d CTA — `bcc-lead-sticky-cta.js`

## Verify / improve

- [ ] Checkout from wedge landing pricing section (desktop + mobile)
- [ ] `utm_content=portal-10d` shows 10-day as primary CTA only
- [ ] Segment checkout by country + `utm_content` in GA4 explorations
- [ ] PayPal as second option (after wedge CPA baseline)

**Hero offer:** 10 days for $9.99 — exam sprint. 30-day for longer study window.

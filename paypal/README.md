---
type: moc
tags:
  - payments
  - paypal
  - becertifiedtoday
created: 2026-06-20
---

# PayPal

Prep and integration notes for adding **PayPal as a second payment option** alongside Stripe at checkout on becertifiedtoday.com.

**Goal:** Customer chooses **Stripe** or **PayPal** on the same purchase flow; both paths grant the same portal / test-sim access.

**Stripe today (reference):**
- Checkout API: `api/create-checkout-session.js`
- Webhook fulfillment: `api/stripe-webhook.js` → `server-lib/portal-checkout-fulfillment.js`
- Success-page verify: `api/verify-checkout-session.js`
- Payment Links on portal pages (CCNA, ENCOR, Sec+)

---

## Notes

| Note | Use when |
|------|----------|
| [[Setup checklist]] | **Start here** — account, developer app, sandbox, go-live |
| [[Product and price map]] | Mirror Stripe SKUs before building API routes |
| [[Architecture — Stripe vs PayPal]] | How PayPal maps to existing fulfillment |

---

## Related

- Funnel checkout nodes mention PayPal as a future step:
  - `marketing-research/Wedge Marketing plan/canvas/nodes/04-checkout.md`
  - `marketing-research/Wedge Marketing plan/canvas/secplus/nodes/04-checkout.md`
- Stripe best-practices skill in Cursor (parallel path, not a replacement)

---

## Success gates (prep complete)

- [ ] PayPal **Business** account verified and linked to bank
- [ ] **Sandbox** and **Live** REST apps created; credentials stored in password manager
- [ ] Webhook URL planned for Vercel (`/api/paypal-webhook`)
- [ ] Every Stripe sellable product has a PayPal price row in [[Product and price map]]
- [ ] Sandbox test buyer + seller accounts exercised once end-to-end (manual PayPal checkout)

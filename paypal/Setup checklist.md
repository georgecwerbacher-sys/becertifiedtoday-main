---
type: checklist
tags:
  - payments
  - paypal
  - checklist
created: 2026-06-20
---

# PayPal setup checklist

Step-by-step prep for **PayPal Checkout (Orders API v2)** as a peer option to Stripe. You are **not** wiring code yet — this gets accounts, credentials, and product parity ready.

[[README|← PayPal hub]] · Product map: [[Product and price map]] · Architecture: [[Architecture — Stripe vs PayPal]]

---

## Phase 1 — Business account (one time)

- [ ] Confirm you want **PayPal Business** (not Personal) — required for REST API + webhooks
- [ ] Sign up or upgrade at [paypal.com/business](https://www.paypal.com/business)
- [ ] Complete **identity verification** (government ID, business details if applicable)
- [ ] Link a **bank account** for payouts
- [ ] Set **primary currency** to **USD** (matches current Stripe pricing)
- [ ] Enable **PayPal Checkout** / accept card payments on PayPal (Business settings → Payments)
- [ ] Note the **business email** used for the account: ___________________
- [ ] Store login in password manager (separate from Stripe)

---

## Phase 2 — Developer account & apps

PayPal uses a separate developer portal for API keys and sandbox.

- [ ] Open [developer.paypal.com](https://developer.paypal.com) → log in with the **same** PayPal Business account
- [ ] Dashboard → **Apps & Credentials**

### Sandbox app (for local / Vercel preview testing)

- [ ] Create app (or use **Default Application** in Sandbox)
- [ ] Copy **Sandbox Client ID** → password manager
- [ ] Copy **Sandbox Secret** → password manager (show once — regenerate if lost)
- [ ] Confirm app type is **Merchant** (default for accepting payments)

### Live app (production)

- [ ] Switch toggle to **Live**
- [ ] Create a new app, e.g. `becertifiedtoday-checkout`
- [ ] Copy **Live Client ID** → password manager
- [ ] Copy **Live Secret** → password manager
- [ ] Do **not** commit secrets to git — plan for Vercel env vars only

### Sandbox test accounts

- [ ] Developer dashboard → **Testing Tools → Sandbox Accounts**
- [ ] Note **Business (seller)** sandbox login: ___________________
- [ ] Note **Personal (buyer)** sandbox login: ___________________
- [ ] Reset sandbox buyer password if needed (for manual test checkouts)

---

## Phase 3 — Choose integration shape (decision)

For “pick Stripe **or** PayPal” on **your** site, use **PayPal Checkout with Orders API v2** — not PayPal-hosted Payment Links alone.

| Approach | Fits “Stripe or PayPal” chooser? | Notes |
|----------|----------------------------------|-------|
| **Orders API v2 + JS SDK buttons** | **Yes** | Matches your `create-checkout-session` pattern: server creates order, client approves, server captures |
| PayPal Payment Links / Buttons (hosted only) | No | Standalone like Stripe Payment Links — no unified chooser |
| PayPal on Stripe Checkout | No | Stripe can show PayPal inside Stripe UI; you want the opposite (your UI, two providers) |

- [ ] Decision recorded: **Orders API v2 + JS SDK**
- [ ] Read PayPal docs: [Checkout integrate](https://developer.paypal.com/docs/checkout/) (skim server + client flow)

**Flow you will implement later (for reference):**

1. Customer clicks **Pay with PayPal** on your page
2. `POST /api/create-paypal-order` → PayPal `v2/checkout/orders` with amount + `custom_id` / `invoice_id` = `productId`
3. Client SDK opens PayPal approval
4. `POST /api/capture-paypal-order` → capture + run same fulfillment as Stripe webhook
5. Redirect to existing success URL with `?paypal_order_id=…` (parallel to Stripe `session_id`)

---

## Phase 4 — Product & price parity

Mirror every Stripe sellable SKU before writing API code. Fill in [[Product and price map]].

Current Stripe-backed products in repo (non-exhaustive — verify in Stripe Dashboard):

| Track | productId | Price (USD) |
|-------|-----------|-------------|
| CCNA | `ccna-portal-10d` | $9.99 |
| CCNA | `ccna-portal-30d` | $29.99 |
| CCNA | `ccna-test-simulation` | (check Stripe) |
| ENCOR | `encor-portal-10d` | $9.99 |
| ENCOR | `encor-portal-30d` | $29.99 |
| ENCOR | `encor-test-simulation` | (check Stripe) |
| Sec+ | `secplus-portal-10d` | $9.99 |
| Sec+ | `secplus-portal-30d` | $29.99 |
| Sec+ | `secplus-test-simulation` | (check Stripe) |

- [ ] Export current Stripe **Products + Prices** (Dashboard → Product catalog)
- [ ] For each row in [[Product and price map]], confirm **exact USD amount** matches Stripe
- [ ] Decide promo codes: Stripe uses `allow_promotion_codes`; PayPal has **coupons** separately — note “Phase 2 feature” or plan manual parity
- [ ] Confirm tax handling: currently implicit in Stripe prices; decide if PayPal orders need `tax_total` (likely **no tax** for digital goods at launch — document decision)

---

## Phase 5 — Webhooks (plan + register)

Stripe today: `POST /api/stripe-webhook` on `checkout.session.completed`.

PayPal equivalent events to subscribe to:

| Event | Purpose |
|-------|---------|
| `CHECKOUT.ORDER.APPROVED` | Buyer approved — optional if you capture immediately in API |
| `PAYMENT.CAPTURE.COMPLETED` | **Primary** — money captured; trigger portal fulfillment |
| `PAYMENT.CAPTURE.DENIED` / `PAYMENT.Capture.REFUNDED` | Ops / support (later) |

- [ ] Planned production webhook URL:

```
https://becertifiedtoday.com/api/paypal-webhook
```

- [ ] Planned preview webhook URL (optional separate app or same app with sandbox):

```
https://<preview-deployment>.vercel.app/api/paypal-webhook
```

- [ ] In PayPal Developer → app → **Webhooks** → Add webhook (can do in sandbox first)
- [ ] Subscribe to events above
- [ ] Copy **Webhook ID** and note verification approach (PayPal sends headers for signature verify)
- [ ] Plan env vars (do not set in repo yet):

| Env var | Example | Purpose |
|---------|---------|---------|
| `PAYPAL_CLIENT_ID` | sandbox or live | Client SDK + server auth |
| `PAYPAL_CLIENT_SECRET` | secret | Server-only |
| `PAYPAL_WEBHOOK_ID` | WH-… | Signature verification |
| `PAYPAL_MODE` | `sandbox` / `live` | Toggle per environment |

---

## Phase 6 — Fulfillment alignment (read-only prep)

Stripe fulfillment lives in `server-lib/portal-checkout-fulfillment.js` (Customer metadata + Resend magic link).

- [ ] Read [[Architecture — Stripe vs PayPal]] — identify what must be **provider-agnostic**
- [ ] Decide PayPal **buyer email** source: `payer.email_address` on captured order
- [ ] Decide idempotency key: PayPal `capture_id` or `order_id` (store to avoid double-grant)
- [ ] Plan success URLs — reuse existing paths, swap query param:

| Product | Stripe success path today | PayPal param (planned) |
|---------|----------------------------|-------------------------|
| CCNA portal | `/CCNA-Study/CCNA_Training_Portal.html?session_id=…` | `?paypal_order_id=…` |
| CCNA test sim | `/CCNA_Sim_EXAM/test-simulation-runner.html?session_id=…` | `?paypal_order_id=…` |
| ENCOR portal | `/CCNP-ENCOR-Study/ENCOR_Training_Portal.html?session_id=…` | `?paypal_order_id=…` |
| Sec+ portal | `/comptia-sec+-home.html` or portal magic path | confirm in repo |

- [ ] Plan backup verify endpoint: `GET /api/verify-paypal-order?order_id=…` (mirror `verify-checkout-session.js`)
- [ ] Confirm `PUBLIC_SITE_URL`, `RESEND_API_KEY`, `PORTAL_MAGIC_LINK_SECRET` stay shared across providers

---

## Phase 7 — Sandbox smoke test (no site code yet)

Use PayPal’s **Try API** or a minimal curl/script with sandbox credentials.

- [ ] Create a **$0.01** or **$9.99** test order in sandbox via API Explorer or Postman
- [ ] Approve with **sandbox buyer** account in browser
- [ ] Capture order via API
- [ ] Confirm webhook fires to a test receiver ([webhook.site](https://webhook.site) or ngrok) if Vercel route not built yet
- [ ] Log capture ID + payer email in this note for reference

Sandbox test log:

| Date | Order ID | Capture ID | Payer email | Notes |
|------|----------|------------|-------------|-------|
| | | | | |

---

## Phase 8 — Vercel / ops prep

- [ ] List env vars to add on Vercel (Production + Preview separately)
- [ ] Sandbox credentials on **Preview** only until UI is ready
- [ ] Live credentials on **Production** only after Phase 9
- [ ] Add PayPal to admin/analytics backlog (segment `payment_provider` in GA4 `purchase` events — later)
- [ ] Document refund process: Stripe Dashboard vs PayPal **Activity → Refund** (support playbook)

---

## Phase 9 — Go live (after code ships)

Do not flip live until checkout chooser + webhook + verify endpoint are deployed.

- [ ] Live app credentials on Vercel Production
- [ ] Live webhook registered and **verified** (send test event from dashboard)
- [ ] One **real** $9.99 purchase on smallest SKU (then refund if needed)
- [ ] Confirm magic-link email sends for PayPal purchase
- [ ] Confirm portal access expires on same schedule as Stripe (`portalAccessExpiresAtMs` logic)
- [ ] Update [[README#Success gates (prep complete)|success gates]] on hub note

---

## Phase 10 — UI integration checklist (build phase — later)

When you start coding the Stripe / PayPal chooser:

- [ ] Add payment method step to checkout entry points (portal CTAs, test-sim begin pages)
- [ ] `POST /api/create-paypal-order` with `{ productId }` (same enum as Stripe)
- [ ] Load PayPal JS SDK with `client-id` from env (inject via small config endpoint or build-time)
- [ ] Wire `begin_checkout` GA4 with `payment_provider: paypal | stripe`
- [ ] Disable double-submit while redirect / popup in flight
- [ ] Handle cancel → same `cancelPath` as Stripe per product
- [ ] Add `api/paypal-webhook.js` route to `vercel.json` if needed (match `stripe-webhook` pattern)
- [ ] Run `npm run lint` / deploy preview → repeat Phase 7 on preview URL

---

## Do not

- Put **Client Secret** or webhook secrets in `public/` or git
- Use Personal PayPal for production API access
- Assume PayPal Payment Links replace your chooser UI
- Go live without webhook + idempotent fulfillment (risk of paid customer with no access)
- Drop Stripe until PayPal CPA and fulfillment are proven

---

## If something blocks you

| Blocker | Fix |
|---------|-----|
| Business account under review | Wait for verification; use sandbox only |
| Cannot create Live app | Business verification incomplete |
| Webhook not received | Check URL is HTTPS, 200 response, correct event subscriptions |
| Capture succeeds but no email | Same Resend env vars as Stripe — debug in `portal-checkout-fulfillment` path |
| Amount mismatch | PayPal order `amount.value` must match Stripe price to the cent |

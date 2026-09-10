---
type: reference
tags:
  - payments
  - paypal
  - stripe
created: 2026-06-20
---

# Product and price map

Single source of truth for **Stripe ↔ PayPal parity**. Fill PayPal columns during Phase 4 of [[Setup checklist]].

[[README|← PayPal hub]]

---

## How to use

1. Confirm each **USD amount** in Stripe Dashboard → Product catalog.
2. PayPal Orders API uses **string amounts** with two decimals (e.g. `"9.99"`), currency `USD`.
3. Pass **`productId`** in order `custom_id` or `purchase_units[].custom_id` so fulfillment matches Stripe metadata.

---

## Portal access

| productId | Display name | USD | Stripe price env / link | PayPal amount | PayPal notes |
|-----------|--------------|-----|-------------------------|---------------|--------------|
| `ccna-portal-10d` | CCNA 10-day portal | 9.99 | `STRIPE_PRICE_CCNA_PORTAL_10D` / Payment Link | 9.99 | |
| `ccna-portal-30d` | CCNA 30-day portal | 19.99 | `STRIPE_PRICE_CCNA_PORTAL_30D` / Payment Link | 19.99 | |
| `encor-portal-10d` | ENCOR 10-day portal | 9.99 | Stripe Payment Link | 9.99 | |
| `encor-portal-30d` | ENCOR 30-day portal | 19.99 | Stripe Payment Link | 19.99 | |
| `secplus-portal-10d` | Security+ 10-day portal | 9.99 | Stripe Payment Link | 9.99 | |
| `secplus-portal-30d` | Security+ 30-day portal | 19.99 | Stripe Payment Link | 19.99 | |

---

## Test simulations

| productId | Display name | USD | Stripe | PayPal amount | PayPal notes |
|-----------|--------------|-----|--------|---------------|--------------|
| `ccna-test-simulation` | CCNA timed test sim | | `STRIPE_PRICE_CCNA_TEST_SIM` | | |
| `encor-test-simulation` | ENCOR timed test sim | | Payment Link | | |
| `secplus-test-simulation` | Sec+ timed test sim | | Payment Link | | |

---

## Success & cancel paths (reuse for PayPal)

From `api/create-checkout-session.js` and checkout JS — PayPal should redirect to the same paths with `paypal_order_id` instead of `session_id`.

| productId | Success path | Cancel path |
|-----------|--------------|-------------|
| `ccna-portal-10d` / `ccna-portal-30d` | `/CCNA-Study/CCNA_Training_Portal.html` | `/ccna-home.html#purchase` |
| `ccna-test-simulation` | `/CCNA_Sim_EXAM/test-simulation-runner.html` | `/CCNA_Sim_EXAM/begin-test-simulation.html` |

(Add ENCOR / Sec+ rows from their checkout JS when filling this in.)

---

## Checklist

- [ ] All USD amounts verified against Stripe
- [ ] Test sim prices filled in
- [ ] ENCOR + Sec+ success/cancel paths copied from repo checkout files
- [ ] Any future SKU added here **before** enabling PayPal for that product

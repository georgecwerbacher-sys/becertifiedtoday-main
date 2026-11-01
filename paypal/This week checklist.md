---
type: checklist
tags:
  - payments
  - paypal
  - this-week
created: 2026-11-01
week: 2026-11-01
---

# PayPal checklist — week of November 1, 2026

Working list for **November 1–7**. Checkout still uses Stripe. This week gets PayPal Checkout (Orders API v2) ready as a second option on becertifiedtoday.com.

Full prep notes: [[Setup checklist]] · Prices: [[Product and price map]] · Flow: [[Architecture — Stripe vs PayPal]]

---

## 1. Open a PayPal Business account

- [ ] Sign up or upgrade at [paypal.com/business](https://www.paypal.com/business)
- [ ] Finish identity verification
- [ ] Link a bank account for payouts
- [ ] Set the account currency to **USD**
- [ ] Turn on PayPal Checkout in Business settings

## 2. Create the developer apps

- [ ] Log in at [developer.paypal.com](https://developer.paypal.com) with the same business account
- [ ] Under **Apps & Credentials**, keep a **Sandbox** app for testing
- [ ] Create a **Live** app named `becertifiedtoday-checkout`
- [ ] Save each **Client ID** and **Secret** in a password manager (not in git)
- [ ] Under **Testing Tools → Sandbox Accounts**, note the seller and buyer logins

## 3. Match the current Stripe prices

Confirm these one-time USD amounts in [[Product and price map]] before any PayPal code:

- [ ] CCNA, ENCOR, and Security+ 10-day portal — **$9.99**
- [ ] CCNA, ENCOR, and Security+ 30-day portal — **$19.99**
- [ ] Timed test simulations — match the current Stripe price for each SKU

## 4. Register the webhook

- [ ] In the PayPal app, add a webhook for `PAYMENT.CAPTURE.COMPLETED`
- [ ] Also subscribe to approval, denial, and refund events if you want them
- [ ] Set the URL to `https://becertifiedtoday.com/api/paypal-webhook`
- [ ] Save the **Webhook ID**

## 5. Put credentials on Vercel

Sandbox values on Preview. Live values on Production only after the checkout code is deployed.

- [ ] `PAYPAL_CLIENT_ID`
- [ ] `PAYPAL_CLIENT_SECRET`
- [ ] `PAYPAL_WEBHOOK_ID`
- [ ] `PAYPAL_MODE` (`sandbox` or `live`)

## 6. Confirm a sandbox payment

- [ ] Create a **$9.99** sandbox order
- [ ] Approve it with the sandbox buyer
- [ ] Capture it
- [ ] Confirm the webhook fires

## 7. Build the checkout path

Buyer clicks **Pay with PayPal**. The site then:

- [ ] `POST /api/create-paypal-order` with the same `productId` Stripe uses
- [ ] Opens the PayPal approval window
- [ ] `POST /api/capture-paypal-order` and grants access through the same fulfillment path as Stripe (magic-link email and portal expiry)
- [ ] Sends the buyer to the existing success page with `?paypal_order_id=…`

## 8. Go live

Only after the code above is on production. Keep Stripe in place until a real PayPal purchase works.

- [ ] Switch Production to the live app
- [ ] Send a test webhook from the PayPal dashboard
- [ ] Buy the **$9.99** SKU once
- [ ] Confirm the access email arrives

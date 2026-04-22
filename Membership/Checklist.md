# 30-day subdomain access + Stripe — build checklist

**Model:** One-time payment → **30 days** access to **`encor.becertifiedtoday.com`**. Not a renewing subscription; user buys again for another 30 days or another product/subdomain later.

---

## Phase 0 — Decide scope

- [ ] Confirm **exact URL** for checkout success/cancel (marketing site vs ENCOR).
- [ ] Decide **identity**: email magic link only vs full auth (Clerk / Auth0 / Supabase Auth / etc.).
- [ ] Decide **where access is stored**: Postgres / Supabase / Dynamo / KV / auth provider metadata.
- [ ] Confirm **no auto-renew** in copy and in Stripe (**one-time Price** only).

---

## Phase 1 — Stripe account & catalog

- [ ] Create Stripe account (or log in); complete verification as required.
- [ ] Stay in **Test mode** until end-to-end works.
- [ ] Create **Product**: e.g. “ENCOR — 30-day access”.
- [ ] Create **Price**: **One-time** (not recurring), amount e.g. $19.99, currency USD.
- [ ] (Optional) Duplicate pattern for **future** subdomains: separate Product + one-time Price per track.
- [ ] Note **Price ID** (`price_...`) for env vars.
- [ ] Configure **Customer portal** only if you need receipts/invoices later (optional for one-time; receipts can be email-only).

---

## Phase 2 — Keys & secrets (never commit)

- [ ] Dashboard → Developers → **API keys**: copy **Publishable** and **Secret** (test).
- [ ] Developers → **Webhooks** → Add endpoint (URL will be your deployed `/api/...` — add after deploy or use Stripe CLI for local).
- [ ] Create webhook and select events at minimum:
  - [ ] `checkout.session.completed`
  - [ ] (Optional) `customer.subscription.*` — **omit** if you only use one-time payments.
- [ ] Copy **Webhook signing secret** (`whsec_...`).
- [ ] In **Vercel** (both projects if split): Project → Settings → Environment Variables:
  - [ ] `STRIPE_SECRET_KEY`
  - [ ] `STRIPE_PUBLISHABLE_KEY` (only if client-side Stripe.js needed)
  - [ ] `STRIPE_WEBHOOK_SECRET`
  - [ ] `STRIPE_PRICE_ID_ENCOR` (or similar)
  - [ ] `PUBLIC_SITE_URL` / `ENCOR_APP_URL` for redirects
  - [ ] Auth secrets (session/JWT/provider keys) per chosen stack

---

## Phase 3 — Backend on Vercel (API routes)

- [ ] Add server runtime to the project that **owns checkout** (often **marketing** repo or a tiny **api** repo).
- [ ] Implement **`POST /api/create-checkout-session`**:
  - [ ] `mode: 'payment'` (one-time).
  - [ ] `line_items` with your ENCOR Price ID.
  - [ ] `success_url` / `cancel_url` with session id query param if needed.
  - [ ] Pass **metadata**: e.g. `product: encor`, `access_days: 30`, internal user id if already logged in.
- [ ] Implement **`POST /api/stripe/webhook`**:
  - [ ] Read raw body; verify signature with `STRIPE_WEBHOOK_SECRET`.
  - [ ] On `checkout.session.completed`:
    - [ ] Resolve **customer email** or **linked user id** from session/metadata.
    - [ ] Compute **`access_until = now + 30 days`** (or from metadata).
    - [ ] **Upsert** row: `user_or_email` + `grant: encor` + `access_until`.
  - [ ] Return 200 quickly; heavy work async if needed.
- [ ] Lock down CORS / only your domains calling create-session.

---

## Phase 4 — Database / access model

- [ ] Create table or collection, e.g. `access_grants`:
  - [ ] `user_id` or `email` (match what ENCOR gates on)
  - [ ] `product` / `subdomain_key` (e.g. `encor`)
  - [ ] `access_until` (timestamp)
  - [ ] `stripe_customer_id` / `stripe_session_id` (optional, for support)
- [ ] Add index on `(user_id, product)` or `(email, product)`.
- [ ] Define rule: **new purchase** either **sets** `access_until` from purchase time + 30d, or **extends** max(existing, now)+30d — pick one and document it.

---

## Phase 5 — Auth so “membership” is per person

- [ ] Integrate chosen auth on **marketing** and **ENCOR** (same IdP = simplest).
- [ ] After first login, link Stripe Customer to user if you use Customer objects.
- [ ] Optional: pass `client_reference_id` or metadata in Checkout Session = your `user_id`.

---

## Phase 6 — ENCOR app (`encor.becertifiedtoday.com`)

- [ ] Add **middleware** or **edge** check on every request (except static assets, health, webhook paths):
  - [ ] User must be **authenticated**.
  - [ ] Load `access_grants` for `product = encor`.
  - [ ] Allow if `now < access_until`; else redirect to marketing **purchase** page or show “expired”.
- [ ] Add **logout** and clear session behavior.
- [ ] Ensure **no** secret keys in static `public/` JS.

---

## Phase 7 — Marketing site (`becertifiedtoday.com`)

- [ ] Replace “Coming soon” with **Buy / Get access** button.
- [ ] Button → `fetch('/api/create-checkout-session')` → redirect to `session.url`, **or** link to Stripe **Payment Link** for MVP (then webhook still must grant access — same webhook logic).
- [ ] Post-purchase: success page tells user to **Sign in on ENCOR** (or deep-link if you support it).

---

## Phase 8 — Local testing

- [ ] Install **Stripe CLI**; run `stripe listen --forward-to localhost:.../api/stripe/webhook`.
- [ ] Use test card `4242 4242 4242 4242`.
- [ ] Confirm webhook fires and **DB row** updates.
- [ ] Confirm ENCOR **blocks** without grant and **allows** with valid `access_until`.

---

## Phase 9 — Production cutover

- [ ] Switch Stripe to **Live** keys and **Live** webhook endpoint URL.
- [ ] Create **Live** Product/Price if not cloned; update env vars on Vercel **Production**.
- [ ] Run one **real** small test charge; refund in Dashboard if needed.
- [ ] Monitor Stripe Dashboard for failed webhooks.

---

## Phase 10 — Legal & UX

- [ ] Terms of service (access duration, no guarantee of exam content).
- [ ] Privacy policy (what you store: email, access dates, Stripe ids).
- [ ] Refund policy (even if “no refunds” — state it).
- [ ] Email: Stripe receipts + optional “your access ends on …” (cron or transactional email later).

---

## Phase 11 — Ops

- [ ] Alert on **webhook failures** (Stripe Dashboard email or monitoring).
- [ ] Admin runbook: “user paid but no access” → check webhook logs, replay event, manual DB fix.
- [ ] Backup / export plan for `access_grants`.

---

## Quick reference — env vars (adjust names)

| Variable | Purpose |
|----------|---------|
| `STRIPE_SECRET_KEY` | Server-side Stripe API |
| `STRIPE_WEBHOOK_SECRET` | Verify webhook signatures |
| `STRIPE_PRICE_ID_ENCOR` | One-time ENCOR Price |
| `DATABASE_URL` or provider keys | Store grants |
| Auth provider vars | Sessions on both sites |

---

## Optional later

- [ ] Cron job: email **3 days before** `access_until`.
- [ ] Dashboard for user: “Access active until …”.
- [ ] Second subdomain: new Price + `product` key + separate middleware rule or host map.

# ENCOR Stripe Checkout Setup (No Membership Accounts)

## Environment variables

Set these in Vercel for the project serving both `becertifiedtoday.com` and `encor.becertifiedtoday.com`:

- `STRIPE_SECRET_KEY` - Stripe secret key (`sk_test_...` in test mode)
- `STRIPE_WEBHOOK_SECRET` - webhook signing secret (`whsec_...`)
- `STRIPE_PRICE_ID_ENCOR` - one-time ENCOR product price id (`price_...`)
- `PUBLIC_SITE_URL` - marketing site base URL (example: `https://becertifiedtoday.com`)
- `ENCOR_APP_URL` - ENCOR app base URL (example: `https://encor.becertifiedtoday.com`)
- `MAGIC_LINK_VERIFY_BASE_URL` - optional override for where `/api/auth/magic-link/verify` lives (default: `PUBLIC_SITE_URL`)
- `KV_REST_API_URL` - Upstash/Vercel KV REST URL
- `KV_REST_API_TOKEN` - Upstash/Vercel KV REST token
- `RESEND_API_KEY` - API key for email delivery
- `MAGIC_LINK_FROM_EMAIL` - sender address for magic links
- `ADMIN_ACCESS_TOKEN` - shared token for admin support endpoint access
- `ACCESS_WINDOW_DAYS` - optional, default `30`
- `MAGIC_LINK_TTL_MINUTES` - optional, default `30`
- `SESSION_TTL_DAYS` - optional, default `30`

## Stripe setup

1. Create Product/Price in Stripe test mode:
   - Product: ENCOR Access (30 Days)
   - Price: one-time payment (not recurring)
2. Add webhook endpoint:
   - URL: `https://becertifiedtoday.com/api/stripe/webhook`
   - Events:
     - `checkout.session.completed`
     - `charge.refunded`
     - `payment_intent.payment_failed`
3. Copy webhook signing secret into `STRIPE_WEBHOOK_SECRET`.

## Access model

Records are stored in KV with minimal fields:

- `email`
- `stripe_customer_id`
- `checkout_session_id`
- `access_expires_at`

Additional keys are used for operational behavior only (idempotency markers, session tokens, short-lived magic-link tokens).

## Request flow

1. User clicks Buy/Renew CTA.
2. Frontend calls `POST /api/stripe/create-checkout-session`.
3. User pays on Stripe Checkout.
4. Stripe sends `checkout.session.completed` webhook.
5. Server verifies signature, applies idempotency, grants 30-day access in KV, creates magic token, emails magic link.
6. User opens magic link:
   - `GET /api/auth/magic-link/verify?token=...`
   - server validates token, checks active access, sets secure HttpOnly session cookie, redirects to ENCOR root.
7. Edge middleware on `encor.*` host checks session + access expiration; redirects expired/invalid sessions to `/encor-renew.html`.

## Test plan (Stripe test mode)

1. **Checkout start**
   - Open marketing page.
   - Click `Buy ENCOR Access (30 Days)`.
   - Confirm redirect to Stripe Checkout.
2. **Successful payment**
   - Complete with test card `4242 4242 4242 4242`.
   - Confirm redirect to `/checkout-success.html`.
   - Confirm webhook logs `checkout.session.completed`.
   - Confirm KV contains access record with expected fields and `access_expires_at` ~30 days out.
3. **Magic link**
   - Confirm email arrives.
   - Open magic link and verify redirect into ENCOR app.
4. **Middleware block**
   - Remove/alter `encor_access_token` cookie and request ENCOR page.
   - Verify redirect to `/encor-renew.html`.
   - Set expired `access_expires_at` and confirm middleware redirects to renew page.
5. **Renew**
   - Click `Renew Access`.
   - Complete another successful checkout.
   - Confirm `access_expires_at` extends forward from max(current_expiry, now).
6. **Refund handling**
   - Refund test payment in Stripe dashboard.
   - Confirm webhook `charge.refunded` processes and access is revoked.
7. **Idempotency**
   - Replay same webhook event in Stripe.
   - Confirm duplicate event is acknowledged without double-granting access.

## Admin support endpoint

- Endpoint: `GET /api/admin/access-record?email=<customer_email>`
- Required header: `x-admin-token: <ADMIN_ACCESS_TOKEN>`
- Response includes:
  - `found`
  - `refunded`
  - `record` (or `null`)

- Endpoint: `POST /api/admin/send-magic-link`
- Required header: `x-admin-token: <ADMIN_ACCESS_TOKEN>`
- Request body:
  - `{ "email": "customer@example.com" }`
- Behavior:
  - Sends a fresh magic link only if access is currently active.
  - Returns an error if access is expired (customer should renew first).

- Endpoint: `POST /api/admin/grant-access`
- Required header: `x-admin-token: <ADMIN_ACCESS_TOKEN>`
- Request body:
  - `{ "email": "admin@example.com", "days": 3650, "send_magic_link": true }`
- Behavior:
  - Admin-grants/extends access without checkout.
  - `days` is optional (defaults to normal access window).
  - `send_magic_link` defaults to true and emails an immediate login link.

- Endpoint: `GET /api/admin/analytics-summary`
- Required header: `x-admin-token: <ADMIN_ACCESS_TOKEN>`
- Returns event counts for key funnel activity (today + total).
- Optional browser view: `/admin-analytics.html`


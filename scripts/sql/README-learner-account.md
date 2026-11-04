# Learner account setup

1. Provision **Vercel Postgres** (Neon) for the project.
2. Set env vars:
   - `POSTGRES_URL` (or `DATABASE_URL`)
   - `LEARNER_MAGIC_LINK_SECRET` (or reuse `PORTAL_MAGIC_LINK_SECRET`)
   - `RESEND_API_KEY` / `RESEND_FROM` (same as portal mail)
   - `PUBLIC_SITE_URL` (e.g. `https://becertifiedtoday.com`)
3. Run [`learner-account-schema.sql`](./learner-account-schema.sql) against the database.
4. Deploy. Free accounts sign in at `/account/login.html`.

Paid portal unlock remains separate (Stripe + portal localStorage entitlement).

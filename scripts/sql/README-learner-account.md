# Learner account storage

Production uses **Vercel KV / Upstash Redis** (`KV_REST_API_URL`, `KV_REST_API_TOKEN`).

Required env (already on becertifiedtoday-main):

- `KV_REST_API_URL` / `KV_REST_API_TOKEN` — learner profiles, sessions, attempts, schedules
- `PORTAL_MAGIC_LINK_SECRET` (or `LEARNER_MAGIC_LINK_SECRET`) — magic-link JWT
- `RESEND_API_KEY` / `RESEND_FROM` — magic-link email

Optional Postgres schema (`learner-account-schema.sql`) is kept for a future Neon/Postgres migration; the live runtime path is Redis via `server-lib/learner-db.js`.

Key prefixes: `bcc:learner:*`

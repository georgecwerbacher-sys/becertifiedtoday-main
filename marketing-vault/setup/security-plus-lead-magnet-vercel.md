# Security+ free simulation — Vercel go-live checklist

Step-by-step to enable email capture + scorecard email on production.

## 1. Environment variables (Vercel Dashboard)

Project → **Settings** → **Environment Variables** → add for **Production** (and Preview if you test there):

| Variable | Example | Required |
|----------|---------|----------|
| `PUBLIC_SITE_URL` | `https://becertifiedtoday.com` | Yes |
| `RESEND_API_KEY` | `re_…` from [Resend](https://resend.com/) | Yes (for emails) |
| `RESEND_FROM` | `Be Certified Today <noreply@becertifiedtoday.com>` | Yes — domain must be verified in Resend |
| `RESEND_SECPLUS_MARKETING_AUDIENCE_ID` | Resend Audience UUID | Optional — list building |
| `RESEND_SECPLUS_FREE_SIM_SUBJECT` | `Your free Security+ simulation is ready` | Optional |
| `RESEND_SECPLUS_SCORECARD_SUBJECT` | `Your Security+ SY0-701 simulation scorecard` | Optional |
| `GITHUB_LEADS_TOKEN` | Fine-grained GitHub PAT (Contents read/write) | Optional — append leads to Obsidian CSV |
| `GITHUB_LEADS_REPO` | `your-user/CCNP_Study_main` | Optional — if not set, uses Vercel `VERCEL_GIT_REPO_*` |

Existing Stripe / webhook vars are unchanged for paid sim checkout.

**Lead CSV (Obsidian):** With `GITHUB_LEADS_TOKEN` set, each signup appends a row to `marketing-vault/leads/secplus-free-simulation-leads.csv` via a git commit. Open `marketing-vault/` in Obsidian and `git pull` to see new rows. Local `vercel dev` appends to the file on disk without GitHub.

## 2. Resend domain

1. Resend → **Domains** → add `becertifiedtoday.com`
2. Add DNS records Resend provides (SPF/DKIM)
3. Wait for **Verified**
4. Set `RESEND_FROM` to an address on that domain

## 3. Deploy

From repo root after commit:

```bash
vercel --prod
```

Or push to the branch Vercel auto-deploys from `main`.

## 4. Smoke test (production)

1. Open `https://becertifiedtoday.com/comptia-sec+-home.html#secplus-lead-capture`
2. Submit your email → should land on `…/test-simulation-runner.html?free=1&welcome=1`
3. **Start timed test** — confirm blueprint shows **20 MCQ · 1 sim (21 items) · 35 min**
4. During run: only **Quit** (→ home) and **Next** on the runner bar
5. Finish all items → scorecard + **90-minute upsell popup**
6. **Email my scorecard** → check inbox
7. Popup **Get full 90-minute simulation** → `#purchase`

## 5. Google Ads

Final URL:

```
https://becertifiedtoday.com/comptia-sec+-home.html#secplus-lead-capture?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=lead-free-sim
```

GA4: mark `generate_lead` and `secplus_scorecard_email_sent` as key events.

See [[../02-campaigns/security-plus/security-plus-lead-magnet-ads|lead magnet ads]].

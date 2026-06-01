---
type: setup-checklist
site: becertifiedtoday.com
active_campaign: secplus_portal
status: in-progress
---

# Marketing stack setup checklist

Step-by-step setup for **Be Certified Today** data-driven marketing: Google Analytics 4, Google Ads, Stripe, Cursor scripts, and this Obsidian vault.

Check boxes as you go (`- [ ]` → `- [x]`). Details for the active campaign live in [[../02-campaigns/security-plus/security-plus-google-ads|Security+ — Google Ads]].

---

## Phase 0 — Obsidian & Cursor

- [ ] **Open this vault in Obsidian**  
  File → Open folder as vault → select `marketing-vault` inside the repo (not the whole repo root).

- [ ] **Install Obsidian plugins** (optional but useful)  
  - [ ] **Dataview** — query reports and campaigns  
  - [ ] **Templater** — weekly review template in `templates/`

- [ ] **Confirm repo path on your Mac**  
  `/Users/werby/CCNP_Study_main`

- [ ] **Copy env template for local scripts**  
  ```bash
  cp .env.example .env.local
  ```
  Fill in values in Phases 2–4 below. Never commit `.env.local`.

---

## Phase 1 — Google Analytics 4 (site tagging)

Site tagging is already in the codebase. Confirm it works.

- [ ] **GA4 property exists** for becertifiedtoday.com  
  Measurement ID in repo: `G-YTT6KBHX7V` (`public/js/ga-site-config.js`).

- [ ] **Real-time test**  
  1. Open [GA4 → Reports → Realtime](https://analytics.google.com/)  
  2. Visit `https://becertifiedtoday.com/comptia-sec+-home.html` in another tab  
  3. Confirm your visit appears within ~30 seconds

- [ ] **Campaign attribution script loads on Security+ landing page**  
  Page: `/comptia-sec+-home.html` includes `campaign-attribution.js`.

- [ ] **UTM test**  
  Open in browser:
  ```
  https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=test&utm_medium=manual&utm_campaign=secplus_portal
  ```
  In GA4 Realtime → check session shows campaign dimensions (may take a few minutes in standard reports).

---

## Phase 2 — Google Analytics 4 (Data API for reports)

Required for `/admin/analytics.html` and `npm run marketing:weekly-report`.

### 2a — Google Cloud project

- [ ] Go to [Google Cloud Console](https://console.cloud.google.com/)
- [ ] Create or select a project (can share with other Google APIs later)
- [ ] **Enable APIs** (APIs & Services → Library):
  - [ ] [Google Analytics Data API](https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com)
  - [ ] [Google Analytics Admin API](https://console.cloud.google.com/apis/library/analyticsadmin.googleapis.com) *(one-time access grant)*

### 2b — Service account

- [ ] IAM → Service Accounts → **Create service account** (e.g. `ga4-reporting`)
- [ ] Grant no GCP roles needed for GA4-only reads
- [ ] Keys → **Add key → JSON** → download `key.json`  
  **Store securely — do not commit to git**

- [ ] **Format for Vercel** (from repo root):
  ```bash
  ./scripts/format-ga-service-account-for-vercel.sh path/to/key.json
  ```
  Copy the `GA_SERVICE_ACCOUNT_JSON_B64=…` output.

### 2c — Grant GA4 property access

- [ ] Find **numeric Property ID** (GA4 Admin → Property settings — not the `G-` measurement ID)

- [ ] Run (replace with your property ID and key path):
  ```bash
  ./scripts/grant-ga4-service-account-access.sh YOUR_PROPERTY_ID path/to/key.json
  ```
  If `gcloud` auth fails, run `./scripts/ga4-admin-oauth-login.sh` first.

- [ ] Wait 2–5 minutes for permissions to propagate

### 2d — Env vars (local + Vercel)

Add to `.env.local` and **Vercel → Project → Settings → Environment Variables**:

- [ ] `GA_MEASUREMENT_ID=G-YTT6KBHX7V`
- [ ] `GA_PROPERTY_ID=` *(numeric, e.g. 538156526)*
- [ ] `GA_INTERNAL_EMAILS=georgecwerbacher@gmail.com,georeg.werbacher@gmail.com` *(comma-separated; excluded from admin reports, GA tracking, and portal subscriber list)*
- [ ] `GA_SERVICE_ACCOUNT_JSON_B64=` *(from format script)*
- [ ] `ADMIN_ANALYTICS_PASSWORD=` *(choose a strong password)*
- [ ] `ADMIN_ANALYTICS_JWT_SECRET=` *(generate: `openssl rand -hex 32`)*

### 2e — Verify

- [ ] Redeploy Vercel after setting env vars
- [ ] Open `https://becertifiedtoday.com/admin/analytics.html` → sign in → data loads
- [ ] From repo root:
  ```bash
  npm run marketing:weekly-report
  ```
  Confirm new file in `marketing-vault/03-reports/weekly/`

---

## Phase 3 — Google Ads (Security+ campaign)

No Google Ads **API** required to launch. Conversion tracking uses gtag (already in repo).

### 3a — Account basics

- [ ] [Google Ads account](https://ads.google.com/) active with billing
- [ ] Ads ID in repo: `AW-18158574148` (`public/js/ga-site-config.js`)

### 3b — Link GA4 ↔ Google Ads

- [ ] Google Ads → **Goals → Conversions → Settings** (or **Linked accounts**)
- [ ] Link your GA4 property
- [ ] Import or map key events: `begin_checkout`, purchase (if configured in GA4)

### 3c — Conversion actions

- [ ] Confirm **purchase conversion** fires on successful Stripe checkout  
  Client helper: `public/js/google-ads-purchase-conversion.js`  
  Label in repo: `zYyCCJiStLAcEMS019JD`

- [ ] Optional: create separate conversion actions in Ads UI for:
  - [ ] `begin_checkout` (micro-conversion)
  - [ ] Purchase (primary)

### 3d — First Security+ campaign

See [[../02-campaigns/security-plus/security-plus-google-ads|Security+ campaign note]]. Minimum:

- [ ] **Final URL**:
  ```
  https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal
  ```
- [ ] Purchase-intent ads can use `#purchase` anchor on same URL
- [ ] Ad groups / keywords drafted (SY0-701, Security+ practice test, etc.)
- [ ] Daily budget set
- [ ] Campaign published

### 3e — Post-launch verification

- [ ] Click your own ad (or use Ads preview) → land on Security+ home with UTMs
- [ ] GA4 Realtime shows session with campaign `secplus_portal`
- [ ] Test checkout (test mode) → `begin_checkout` in GA4 DebugView or Events

---

## Phase 4 — Stripe

### 4a — API keys

- [ ] [Stripe Dashboard → Developers → API keys](https://dashboard.stripe.com/apikeys)
- [ ] Copy **Secret key** (`sk_test_…` for testing, `sk_live_…` for production)  
  Prefer a **restricted key** (`rk_…`) with Checkout + Customers read/write as needed.

- [ ] Add to `.env.local` and Vercel:
  - [ ] `STRIPE_SECRET_KEY=`
  - [ ] `PUBLIC_SITE_URL=https://becertifiedtoday.com` *(match www vs apex)*

### 4b — Webhook

- [ ] Stripe → Developers → **Webhooks → Add endpoint**
- [ ] URL: `https://becertifiedtoday.com/api/stripe-webhook`
- [ ] Event: `checkout.session.completed`
- [ ] Copy **Signing secret** (`whsec_…`) → `STRIPE_WEBHOOK_SECRET` on Vercel  
  **Do not** paste `whsec_` into `STRIPE_SECRET_KEY`.

### 4c — Security+ Payment Links

Configured in `public/COMP_TIA_SEC+/js/secplus-portal-checkout.js`. Verify in Stripe Dashboard:

| Product | Price | After-payment redirect |
|---------|------:|------------------------|
| 10-day portal | $9.99 | `/COMP_TIA_SEC+/secplus-portal-checkout-success.html?session_id={CHECKOUT_SESSION_ID}` |
| 30-day portal | $19.99 | same pattern |
| Timed simulation | $9.99 | `/COMP_TIA_SEC+/test-simulation-runner.html?session_id={CHECKOUT_SESSION_ID}` |

- [ ] **Collect customer email** enabled on each Payment Link
- [ ] **Metadata** `productId`: `secplus-portal-10d`, `secplus-portal-30d`, `secplus-test-simulation`
- [ ] Optional env price IDs in `.env.local`:
  - [ ] `STRIPE_PRICE_SECPLUS_PORTAL_10D`
  - [ ] `STRIPE_PRICE_SECPLUS_PORTAL_30D`
  - [ ] `STRIPE_PRICE_SECPLUS_TEST_SIM`

### 4d — Magic-link email (recommended)

- [ ] `PORTAL_MAGIC_LINK_SECRET=` (`openssl rand -hex 32`)
- [ ] [Resend](https://resend.com/) API key → `RESEND_API_KEY`
- [ ] Verified sender → `RESEND_FROM=Be Certified Today <noreply@your-domain.com>`

### 4e — Stripe test purchase

- [ ] Complete a **test** Security+ checkout (10-day or 30-day)
- [ ] Webhook delivers without error (Stripe Dashboard → Webhooks → event log)
- [ ] Portal access unlocks on site
- [ ] Magic-link email received (if Resend configured)
- [ ] `/admin/analytics.html` portal subscriber section shows purchasers for **CCNA, ENCOR, and Security+** (Stripe metadata per product)
- [ ] `/admin/analytics.html` **Homepage sample → email capture** section lists who submitted and attempt counts (`marketing-vault/leads/home-sample-email-capture.csv` via `GITHUB_LEADS_TOKEN`)

---

## Phase 5 — Weekly marketing workflow

- [ ] Read [[../05-playbooks/weekly-review-process|Weekly review process]]
- [ ] Every week:
  1. [ ] `npm run marketing:weekly-report`
  2. [ ] Open new note in `03-reports/weekly/`
  3. [ ] Fill **Decisions** and **Follow-up**
  4. [ ] Execute changes in Cursor (landing page, ads notes, experiments in `04-experiments/`)
  5. [ ] If landing pages changed: update [[../06-website-optimization/content-change-log|content change log]] and page note under `06-website-optimization/pages/`

---

## Phase 6 — Optional (later)

Not required to launch Security+ ads.

- [ ] **Google Ads API** — pull cost, clicks, ROAS into weekly reports (developer token + OAuth)
- [ ] **Stripe revenue in weekly script** — auto-fill `purchases` / `revenue_usd` from Checkout Sessions API
- [ ] **Search Console** — organic performance (separate from paid campaign)
- [ ] **Stripe MCP in Cursor** — explore payments while building scripts

---

## Quick reference — env vars

| Variable | Used for |
|----------|----------|
| `GA_MEASUREMENT_ID` | Client-side gtag |
| `GA_PROPERTY_ID` | Data API reports |
| `GA_INTERNAL_EMAILS` | Exclude owner/admin test emails (e.g. `georgecwerbacher@gmail.com`) from GA reports and portal subscriber table |
| `GA_SERVICE_ACCOUNT_JSON_B64` | Server GA4 access |
| `ADMIN_ANALYTICS_PASSWORD` | `/admin/analytics.html` login |
| `ADMIN_ANALYTICS_JWT_SECRET` | Admin API auth |
| `STRIPE_SECRET_KEY` | Checkout, webhooks, portal lists |
| `STRIPE_WEBHOOK_SECRET` | Webhook signature verify |
| `PUBLIC_SITE_URL` | Redirects and magic links |
| `PORTAL_MAGIC_LINK_SECRET` | Signed portal emails |
| `RESEND_API_KEY` / `RESEND_FROM` | Transactional email |

Full template: `.env.example` in repo root.

---

## Repo scripts

| Command | Purpose |
|---------|---------|
| `npm run marketing:weekly-report` | GA4 → Obsidian weekly note |
| `./scripts/format-ga-service-account-for-vercel.sh key.json` | Base64 service account for Vercel |
| `./scripts/grant-ga4-service-account-access.sh PROPERTY_ID key.json` | Grant GA4 Viewer to service account |
| `./scripts/ga4-admin-oauth-login.sh` | Fix gcloud auth for grant script |

---

## Done?

When Phases 0–5 are checked off, you have:

- Live Security+ ads with attribution
- GA4 admin dashboard + Obsidian weekly reports
- Stripe checkout + webhook pipeline
- A repeatable review loop in this vault

Track campaign decisions in [[../02-campaigns/security-plus/security-plus-google-ads|Security+ — Google Ads]].

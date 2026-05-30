---
type: campaign-addon
product: secplus-sy0-701
status: active
utm_campaign: secplus_portal
lead_magnet: secplus-free-simulation
---

# Security+ lead magnet — free simulation + scorecard email

Email capture on [[../06-website-optimization/pages/comptia-sec-plus-home|comptia-sec+-home.html]] unlocks a **free timed simulation sample**; the **study scorecard** can be emailed from the results screen.

Parent campaign: [[security-plus-google-ads|Security+ Google Ads]]

---

## Offer

| Step | What they get |
|------|----------------|
| Opt-in on landing | Unlock **35-minute free sim** (20 MCQ + 1 PBQ — 21 items) |
| During sim | **Back** and **Mark for review** (same as full paid sim) |
| Complete sim | On-screen **study scorecard** (scaled score + domains) |
| Results screen | **Email my scorecard** → HTML summary via Resend |
| Post-results | Upsell modal → full **90-minute / 95-item** sim or portal (`#purchase`) |

Full **90-minute** timed test remains a paid product (`#purchase`, $9.99 one attempt).

Blueprint: `public/COMP_TIA_SEC+/data/secplus-free-simulation-blueprint.json`  
Runner: `public/COMP_TIA_SEC+/test-simulation-runner.html?free=1`

---

## Landing URLs for Google Ads

**Primary (lead-magnet ad group):**

```
https://becertifiedtoday.com/comptia-sec+-home.html#secplus-lead-capture?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=lead-free-sim
```

Generic landing (broader ad groups):

```
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content={creative}
```

Note: `#secplus-lead-capture` scrolls to the lead form. With `utm_content=lead-free-sim` (or matching hash), the page **reorders** to show intro → lead capture → purchase (see `secplus-landing-lead-first` on `<html>`).

---

## Funnel

| Step | Action | GA4 event |
|------|--------|-----------|
| Ad click | `#secplus-lead-capture` | Session + UTM |
| Submit email | POST `/api/lead-capture` | `generate_lead` |
| Unlock | `localStorage` + redirect | `/test-simulation-runner.html?free=1` |
| During sim | Back / mark for review / Next | — |
| Finish sim | Results + scorecard | Scorecard render |
| Email scorecard | POST `/api/secplus-scorecard-email` | `secplus_scorecard_email_sent` |
| Upsell | Full sim / portal on results modal or `#purchase` | `begin_checkout` |

Lead rows append to `marketing-vault/leads/secplus-free-simulation-leads.csv` when `GITHUB_LEADS_TOKEN` is set (see [[../setup/security-plus-lead-magnet-vercel|Vercel setup]]).

---

## Ad group: `secplus_lead_free_sim`

| | Copy |
|---|------|
| **Headline 1** | Free Security+ Timed Simulation |
| **Headline 2** | Start Your Free SY0-701 Sample Exam |
| **Headline 3** | 35-Min Practice + Domain Scorecard |
| **Headline 4** | 20 Questions + PBQ Simulation |
| **Headline 5** | Exam Prep — Not a Course |
| **Description 1** | Free 35-minute SY0-701 sample: 20 MCQ + performance-based simulation. Domain scorecard when you finish. Browser-only exam prep. |
| **Description 2** | Realistic timed practice before test day. Back and mark for review like test day. Full 90-minute sim when you are ready. |

**Keywords:** security+ practice test, sy0-701 practice exam, security+ mock exam, security+ timed practice test, sy0-701 simulation

**Negatives:** professor messer, udemy, bootcamp, dump, pdf download, jobs, free course, guaranteed pass

---

## Setup checklist

- [x] Free sim runner live on prod (`test-simulation-runner.html?free=1`)
- [x] Lead capture API + scorecard email API
- [ ] Vercel: `RESEND_API_KEY`, `RESEND_FROM`, `PUBLIC_SITE_URL`
- [ ] Optional: `RESEND_SECPLUS_MARKETING_AUDIENCE_ID`
- [ ] Optional: `RESEND_SECPLUS_SCORECARD_SUBJECT`
- [ ] Optional: `GITHUB_LEADS_TOKEN` + `GITHUB_LEADS_REPO` (Obsidian CSV sync)
- [ ] GA4: `generate_lead`, `secplus_scorecard_email_sent` as key events
- [ ] Google Ads: import `generate_lead` as secondary conversion
- [ ] Test: landing → sim → scorecard email on prod
- [x] Landing copy: lead block lists Back + mark for review (2026-05-30)

---

## API

- `POST /api/lead-capture` — magnet `secplus-free-simulation`
- `POST /api/secplus-scorecard-email` — scorecard payload from results JS

---

## Decisions log

| Date | Decision |
|------|----------|
| 2026-05-30 | Replaced study-plan lead magnet with free timed sim + scorecard email |
| 2026-05-30 | Free sim blueprint: **20 MCQ + 1 sim, 35 min** (4 MCQ per SY0-701 domain + dark web PBQ) |
| 2026-05-30 | Paid full sim unchanged: 90 min, up to 95 items, **$9.99** one attempt |
| 2026-05-30 | Runner: **Back** + **Mark for review** on free and paid sims (exam-realistic navigation) |
| 2026-05-30 | Lead CSV append to `marketing-vault/leads/` via GitHub API or local file |

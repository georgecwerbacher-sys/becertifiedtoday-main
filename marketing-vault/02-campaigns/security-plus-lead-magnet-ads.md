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
| Opt-in on landing | Unlock **20-min free sim** (12 MCQ + 1 PBQ) |
| Complete sim | On-screen **study scorecard** (scaled score + domains) |
| Results screen | **Email my scorecard** → HTML summary via Resend |

Full **90-minute / 95-item** timed test remains a paid product (`#purchase`).

Blueprint: `public/COMP_TIA_SEC+/data/secplus-free-simulation-blueprint.json`

---

## Landing URLs for Google Ads

```
https://becertifiedtoday.com/comptia-sec+-home.html#secplus-lead-capture?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=lead-free-sim
```

---

## Funnel

| Step | Action | GA4 event |
|------|--------|-----------|
| Ad click | `#secplus-lead-capture` | Session + UTM |
| Submit email | POST `/api/lead-capture` | `generate_lead` |
| Redirect | `/test-simulation-runner.html?free=1` | `secplus_free_sim_unlock` |
| Finish sim | Results + scorecard | `secplus_study_plan_view` (legacy name on plan page removed) |
| Email scorecard | POST `/api/secplus-scorecard-email` | `secplus_scorecard_email_sent` |
| Upsell | `#purchase` full sim / portal | `begin_checkout` |

---

## Ad group draft: `secplus_lead_free_sim`

| | Copy |
|---|------|
| **Headline 1** | Free Security+ Timed Simulation |
| **Headline 2** | SY0-701 Sample Exam + Scorecard |
| **Headline 3** | Exam Prep — Not a Course |
| **Description 1** | 20-minute SY0-701 sample: MCQ + performance-based item. Domain scorecard emailed when you finish. Browser-only exam prep. |
| **Description 2** | Free timed practice before test day. No PDF dumps. Full 90-minute sim when you are ready. |

**Keywords:** security+ practice test free, sy0-701 simulation free, security+ mock exam, security+ timed practice test

**Negatives:** professor messer, udemy, bootcamp, dump, pdf download, jobs

---

## Setup checklist

- [ ] Vercel: `RESEND_API_KEY`, `RESEND_FROM`, `PUBLIC_SITE_URL`
- [ ] Optional: `RESEND_SECPLUS_MARKETING_AUDIENCE_ID`
- [ ] Optional: `RESEND_SECPLUS_SCORECARD_SUBJECT`
- [ ] GA4: `generate_lead`, `secplus_scorecard_email_sent` as key events
- [ ] Test: landing → sim → email scorecard on prod

---

## API

- `POST /api/lead-capture` — magnet `secplus-free-simulation`
- `POST /api/secplus-scorecard-email` — scorecard payload from results JS

---

## Decisions log

| Date | Decision |
|------|----------|
| 2026-05-30 | Replaced study-plan lead magnet with free timed sim + scorecard email |
| 2026-05-30 | Free sim: 12 MCQ + 1 sim, 20 min — paid 90-min product unchanged |

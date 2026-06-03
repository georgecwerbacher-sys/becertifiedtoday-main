---
type: campaign-addon
product: secplus-sy0-701
status: active
utm_campaign: secplus_portal
lead_magnet: secplus-free-simulation
---

# Security+ lead magnet — free simulation + scorecard email

[[../../06-website-optimization/pages/comptia-sec-plus-home|comptia-sec+-home.html]] offers a **guest free timed simulation** (no email on landing). Optional **scorecard email** on the results screen. Playbook: [[../../05-playbooks/secplus-free-sim-funnel|free sim funnel]].

Parent campaign: [[security-plus-google-ads|Security+ Google Ads]] · Paste-ready copy: [[security-plus-google-ads-export|Google Ads export]]

---

## Offer

| Step | What they get |
|------|----------------|
| Start on landing (no email) | **35-minute free sim** (20 MCQ + 1 PBQ — 21 items) |
| During sim | **Back** and **Mark for review** (same as full paid sim) |
| Complete sim | On-screen **study scorecard** (scaled score + domains) |
| Results screen | **Email my scorecard** → HTML summary via Resend |
| Post-results | Upsell modal → **30-day access $19.99** (`#purchase`) |

Full library + **90-minute** sim included in **30-day portal** (`#purchase`, $19.99).

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
| Start free sim | Tap CTA (guest access) | `secplus_free_sim_start` + **`generate_lead`** |
| Runner | `localStorage` + redirect | `/test-simulation-runner.html?free=1` |
| During sim | Back / mark for review / Next | — |
| Finish sim | Results + scorecard | Scorecard render |
| Email scorecard | POST `/api/secplus-scorecard-email` | `secplus_scorecard_email_sent` |
| Upsell | Full sim / portal on results modal or `#purchase` | `begin_checkout` |

Lead rows append to `marketing-vault/leads/secplus-free-simulation-leads.csv` when `GITHUB_LEADS_TOKEN` is set (see [[../../setup/security-plus-lead-magnet-vercel|Vercel setup]]).

---

## Ad group: `secplus_lead_free_sim`

| | Copy |
|---|------|
| **Headline 1** | Free Security+ Timed Simulation |
| **Headline 2** | Start Your Free SY0-701 Sample Exam |
| **Headline 3** | 35-Min Practice + Domain Scorecard |
| **Headline 4** | 20 Questions + PBQ Simulation |
| **Headline 5** | Exam Prep — Not a Course |
| **Description 1** | Free 35-min SY0-701 sample: 20 MCQ + PBQ. Domain scorecard. No email to start. |
| **Description 2** | Timed practice before test day. Back & mark for review. 30-day access when ready. |
| **Description 3** | Exam prep—not a course. Verified explanations. No PDF dumps. Browser-only. |
| **Description 4** | Free sample exam in your browser. One attempt per device. Scorecard at finish. |

**Keywords:** security+ practice test, sy0-701 practice exam, security+ mock exam, security+ timed practice test, sy0-701 simulation

**Negatives:** campaign level only (32 Phrase) — [[../../07-keywords/negatives/google-ads-applied-2026-06-03|applied list]] · not on ad group

---

## Setup checklist

- [x] Free sim runner live on prod (`test-simulation-runner.html?free=1`)
- [x] Lead capture API + scorecard email API
- [x] Guest free sim on landing (no email gate) — 2026-06-03
- [x] `generate_lead` + `secplus_free_sim_start` on **Start free sim** (site code)
- [x] `generate_lead` on scorecard email sent (site code)
- [x] Lead-first layout + sticky CTA for `utm_content=lead-free-sim`
- [x] Upsell copy → **$19.99 / 30-day** on results + `#purchase`
- [x] Ad group live: [[secplus-lead-free-sim-ad-group|secplus_lead_free_sim — config]]
- [x] Campaign negatives 32 Phrase (campaign level)
- [x] Bidding: Maximize clicks, max CPC **$2.50**, budget **$10/day**
- [ ] Vercel: `RESEND_API_KEY`, `RESEND_FROM`, `PUBLIC_SITE_URL` (scorecard email)
- [ ] Optional: `RESEND_SECPLUS_MARKETING_AUDIENCE_ID`
- [ ] Optional: `RESEND_SECPLUS_SCORECARD_SUBJECT`
- [ ] Optional: `GITHUB_LEADS_TOKEN` + `GITHUB_LEADS_REPO` (Obsidian CSV sync)
- [ ] GA4: mark `generate_lead`, `secplus_scorecard_email_sent` as **key events**
- [ ] Google Ads: import **`generate_lead` = Primary** conversion
- [ ] Positive keywords = **6–8** in UI (verify export)
- [ ] Test: prod click → GA4 `generate_lead` on free sim Start
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
| 2026-06-03 | Guest free sim on landing (no email); `generate_lead` on Start + scorecard; lead-first order + sticky CTA; vault [[../../05-playbooks/secplus-free-sim-funnel|funnel playbook]] |

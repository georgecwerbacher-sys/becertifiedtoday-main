---
type: campaign-steps
product: secplus
campaign: SEC+_Wedge_Prep
tags:
  - marketing
  - google-ads
  - secplus
  - checklist
---

# Sec+ Notes — how to set up the campaign

---

## Reference voice (read before building ads)

Full canonical copy: [[Sec+ Positioning#Canonical reference (future use)|Sec+ Positioning → Canonical reference]]

**Summary for campaign build:** We sell **exam-realistic, browser-based Security+ prep**—interactive scenarios like the real exam, **adaptive review** that targets weak areas, random or review modes (missed questions are shuffled to the end for retry), and a **timed online simulation**—not a $99 PDF. **$9.99 / 10 days** or **$19.99 / 30 days** unlocks **1,000+ current SY0-701 questions**, PBQ scenarios, and mobile-friendly practice. Target searchers who need a **realistic practice environment** and people whose **certification is required for work** (DoD, contractor, employer mandate)—not generic “question bank” head terms alone.

**Guest-facing About copy:** [[../Website_Main/About Page|About Page]] (BCT site draft)

Keywords and RSA must reflect that story. Details: [[Sec+ Keywords]] · [[Sec+ RSA Copy]]

---

## Before you open Google Ads

- [ ] Stripe $9.99 / $19.99 products live
- [ ] Checkout works on **PBQ landing** + **home** (desktop + phone)
- [ ] Free dark web PBQ: `/secplus-sample?track=sim-dark-web`
- [ ] Free MCQ sample reachable from home
- [ ] GA4 `begin_checkout` imported as Primary
- [ ] Keyword Planner (US) — fill worksheet in [[Sec+ Keywords#Keyword Planner worksheet]]
- [ ] RSA copy reviewed against [[Sec+ Positioning#Canonical reference (future use)|canonical reference]]

---

## Phase 1 — Campaign shell

1. Campaign name: **`SEC+_Wedge_Prep`** (or keep `SEC+_Wedge_PBQ` if already created)
2. Budget **$8/day** · Search only · partners off
3. Bidding: Maximize clicks · max CPC **$3.50**
4. Geo: US, CA, UK, AU · **Presence** only
5. utm_campaign: `secplus_wedge_pbq`
6. AI Max / URL expansion: **Off**

**Budget split (launch):** ~$3 PBQ · ~$3 Realistic_Sim · ~$2 Work_Cert

Each ad group carries one wedge promise from [[Sec+ Positioning#Ad group → message match]]—do not use the same generic RSA on all three.

---

## Phase 2 — Ad group 1: SEC+_PBQ_Scenarios

**Voice:** Interactive scenarios online, like the real exam—chain labs, drag-drop, IR in browser.

1. Display path: `Security+` / `PBQ-Practice`
2. Final URL: see [[Sec+ Keywords#Ad group 1 — SEC+_PBQ_Scenarios]]
3. Keywords: exact + phrase from that section
4. RSA: [[Sec+ RSA Copy#Ad group SEC+_PBQ_Scenarios]]
5. Pin H1 `Security+ PBQ Practice` · H2 `$9.99 · 10-Day Access`

---

## Phase 3 — Ad group 2: SEC+_Realistic_Sim

**Voice:** Timed simulation, adaptive review, random/review modes, 1000+ Qs—not a PDF dump.

1. Display path: `Security+` / `Exam-Simulation`
2. Final URL: `comptia-sec+-home.html#purchase&utm_content=realistic-sim`
3. Keywords: [[Sec+ Keywords#Ad group 2 — SEC+_Realistic_Sim]]
4. RSA: [[Sec+ RSA Copy#Ad group SEC+_Realistic_Sim]]
5. Pin H1 `Timed Security+ Exam Sim` · H2 `$9.99 · Not a PDF`

Landing must support: 90-min timed sim · adaptive · $9.99/10d vs $99 PDF · mobile-friendly

---

## Phase 4 — Ad group 3: SEC+_Work_Cert

**Voice:** Security+ required for work—realistic prep sprint, not a $300 course.

1. Display path: `Security+` / `Work-Cert-Prep`
2. Final URL: `comptia-sec+-home.html#purchase&utm_content=work-cert`
3. Keywords: [[Sec+ Keywords#Ad group 3 — SEC+_Work_Cert]]
4. RSA: [[Sec+ RSA Copy#Ad group SEC+_Work_Cert]]
5. Pin H1 `Security+ for Work Cert` · H2 `$9.99 · 10-Day Sprint`

---

## Phase 5 — Negatives

- Campaign: [[Sec+ Keywords#Campaign negatives (all ad groups)]]
- Ad group: [[Sec+ Keywords#Ad group negatives (all three ad groups)]]

---

## Phase 5b — Sitelinks (campaign level, 6)

Paste at **campaign** level. Link text ≤25 chars · each description ≤35 chars.

Base UTM: `utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq`

| # | Link text | Description 1 | Description 2 | Full URL |
|---|-----------|---------------|---------------|----------|
| 1 | Free Dark Web PBQ | Hands-on IR scenario | No checkout required | `https://becertifiedtoday.com/secplus-sample?track=sim-dark-web&utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=sitelink-pbq` |
| 2 | Free Practice Questions | SY0-701 MCQ preview | Instant feedback, free | `https://becertifiedtoday.com/secplus-sample?track=questions&utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=sitelink-sample` |
| 3 | 28 PBQ Scenarios | Chain labs & hot spots | Browser-only prep | `https://becertifiedtoday.com/secplus/pbq-practice-browser.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=sitelink-pbq-list` |
| 4 | 10-Day Access · $9.99 | 1000+ Qs + PBQ library | One-time no subscription | `https://becertifiedtoday.com/comptia-sec+-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=portal-10d` |
| 5 | 90-Min Timed Exam Sim | MCQ + PBQ mixed run | Adaptive review included | `https://becertifiedtoday.com/comptia-sec+-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=sitelink-sim` |
| 6 | Security+ Exam Prep Home | Full SY0-701 portal | Samples + pricing | `https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=sitelink-home` |

**Copy-paste block (Google Ads UI — one sitelink each):**

```
Sitelink 1
Name: Free Dark Web PBQ
Description 1: Hands-on IR scenario
Description 2: No checkout required
URL: https://becertifiedtoday.com/secplus-sample?track=sim-dark-web&utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=sitelink-pbq

Sitelink 2
Name: Free Practice Questions
Description 1: SY0-701 MCQ preview
Description 2: Instant feedback, free
URL: https://becertifiedtoday.com/secplus-sample?track=questions&utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=sitelink-sample

Sitelink 3
Name: 28 PBQ Scenarios
Description 1: Chain labs & hot spots
Description 2: Browser-only prep
URL: https://becertifiedtoday.com/secplus/pbq-practice-browser.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=sitelink-pbq-list

Sitelink 4
Name: 10-Day Access · $9.99
Description 1: 1000+ Qs + PBQ library
Description 2: One-time no subscription
URL: https://becertifiedtoday.com/comptia-sec+-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=portal-10d

Sitelink 5
Name: 90-Min Timed Exam Sim
Description 1: MCQ + PBQ mixed run
Description 2: Adaptive review included
URL: https://becertifiedtoday.com/comptia-sec+-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=sitelink-sim

Sitelink 6
Name: Security+ Exam Prep Home
Description 1: Full SY0-701 portal
Description 2: Samples + pricing
URL: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=sitelink-home
```

Deep reference: [[../Wedge Marketing plan/secplus-wedge-campaign/06-extensions-locations|06-extensions-locations]]

---

## Phase 6 — Launch check

- [ ] All 3 ad groups enabled
- [ ] **6 sitelinks** pasted (table above)
- [ ] Sitelinks open correctly on mobile
- [ ] Each final URL matches intent (PBQ → wedge page; Sim/Work → home)
- [ ] Free samples work on mobile
- [ ] GA4 `begin_checkout` on test click per ad group
- [ ] Ad copy matches [[Sec+ Positioning#Canonical reference (future use)|canonical reference]]—not generic question-bank language

---

## Week 1

Do not change budget, bidding, geo, or RSA for 7 days.

| Day | Action |
|-----|--------|
| 3 | Search terms → negatives; note which **tier** (W1–W6) converts |
| 7 | Compare CPA by ad group — scale PBQ vs Sim vs Work_Cert |

Log which message (realistic sim vs work cert vs PBQ) drives `begin_checkout`—double down on the winner in week 2.

---

## Campaign copy reminders

When writing or refreshing RSA, land these proof points (from [[Sec+ Positioning]]):

- Online **interactive** scenarios—not a PDF
- **Adaptive** prep; missed Qs **loop back**
- **Timed** exam simulation online
- **$9.99/10d** or **$19.99/30d** vs **$99 PDF**
- **1000+** current SY0-701 questions
- **Mobile-friendly** MCQ + scenario practice
- Built for people who **need the cert for work**

[[Sec+ Positioning|Full positioning]] · [[README|← Sec+ Campaign folder]]

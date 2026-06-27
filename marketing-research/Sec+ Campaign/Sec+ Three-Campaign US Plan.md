---
type: campaign-strategy
product: secplus
phase: 2
tags:
  - marketing
  - google-ads
  - secplus
  - budget
  - schedule
  - us-only
---

# Sec+ Three-Campaign US Plan — $60/day total

**Status:** Planning · **Do not change admin dashboard yet**

Google Ads budgets are set at the **campaign** level, not reliably at the individual ad level. To run “three ads at $20/day each,” use **three separate Search campaigns**, each with its own $20/day budget. Keep the same landing page and conversion event so the admin dashboard can still read the same checkout behavior.

Related: [[Security+ Campaign]] · [[Sec+ Notes]] · [[Sec+ Phase 2 Institutional Targeting]] · [[Sec+ Keywords]] · [[Sec+ RSA Copy]]

---

## Budget structure

| Campaign | Daily budget | Audience intent | Landing | Tracking |
|----------|--------------|-----------------|---------|----------|
| `Security+ SY0-701 · Core Exam Prep · US` | **$20/day** | Last-mile exam prep, timed sim, adaptive review | `/comptia-sec+-home.html` | `utm_campaign=secplus_core_us` |
| `Security+ SY0-701 · Military Gov 8140 · US` | **$20/day** | Military, DoD 8140, federal, contractors, first responders | `/comptia-sec+-home.html` | `utm_campaign=secplus_gov_us` |
| `Security+ SY0-701 · Student Workforce · US` | **$20/day** | Students, educators, veterans, workforce/job-placement programs | `/comptia-sec+-home.html` | `utm_campaign=secplus_workforce_us` |

**Total planned spend:** **$60/day** (~$1,800/month before any promo credit).

**Bid rule:** Hold keyword bids and max CPC settings for the first **7 days**. After the first week, adjust based on keyword-level results: clicks, CPC, search terms, `begin_checkout`, and purchase quality.

**Admin note:** Until the dashboard is updated for multiple campaign IDs, keep `secplus_portal` as the baseline tracker and reconcile the three Google Ads campaigns manually in [[secplus-monthly-scorecard.csv]]. Do not remove the original campaign history.

---

## US-only location setup

| Setting | Value |
|---------|-------|
| Countries | **United States only** |
| Location option | **Presence** — people in or regularly in targeted locations |
| Exclude | All non-US countries; do not use “presence or interest” |
| Language | English |
| Search partners | **Off** until data is stable |
| AI Max / URL expansion | **Off** |

Use US-only first because the buyer groups are specific: military bases, federal hubs, colleges, workforce programs, and after-work learners.

---

## Ad schedule — when target buyers search

Start with a schedule that favors **before work, lunch, and after work** in the account time zone. After two weeks, review hour-of-day data before tightening.

| Day | Run time | Bid adjustment | Why |
|-----|----------|----------------|-----|
| Monday–Friday | **6:00 AM–9:00 AM** | 0% | Commute / before-shift research |
| Monday–Friday | **11:00 AM–2:00 PM** | 0% | Lunch break searches |
| Monday–Thursday | **5:00 PM–11:30 PM** | **+20%** | Main after-work study window |
| Friday | **5:00 PM–10:00 PM** | +10% | Lower but still useful |
| Saturday–Sunday | **9:00 AM–11:00 PM** | +10% | Weekend study blocks |
| Overnight | Pause or -90% | Avoid | Low intent unless data proves otherwise |

**Review rule:** If after-work clicks have checkout rate below 1% after meaningful volume, reduce the +20% first before cutting keywords.

---

## Campaign 1 — core exam prep

**Name:** `Security+ SY0-701 · Core Exam Prep · US`

| Setting | Value |
|---------|-------|
| Budget | **$20/day** |
| Bidding | Maximize clicks · max CPC **$2.75** to start; hold 7 days |
| Geo | US only · presence |
| Schedule | Shared schedule above |
| Final URL | `https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_core_us&utm_content=core-exam-prep` |

**Message:** SY0-701 exam prep, 1000+ verified questions, timed 90-minute exam, adaptive review, scorecard.

**Keyword themes:** timed practice, exam simulation, SY0-701 prep, adaptive review, browser exam prep. Pull from the existing base 64, but do not include DoD/student/workforce phrases here unless they convert organically.

---

## Campaign 2 — military, government, 8140

**Name:** `Security+ SY0-701 · Military Gov 8140 · US`

| Setting | Value |
|---------|-------|
| Budget | **$20/day** |
| Bidding | Maximize clicks · max CPC **$2.75** to start; hold 7 days |
| Geo | US only · presence · **60-mile radius around priority bases** + federal hub modifiers |
| Schedule | Shared schedule above; strongest after work |
| Final URL | `https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_gov_us&utm_content=mil-gov-8140` |

**Message:** Security+ for DoD 8140, federal roles, contractors, first responders, and military deadlines. Do not imply official DoD endorsement.

**60-mile military base radius targets:**

For `secplus_gov_us`, target active-duty, Guard/Reserve, and defense-contractor searchers within **60 miles** of priority installations and base metros. Use **Presence** only.

| Base / metro | Radius | Notes |
|--------------|--------|-------|
| Fort Meade / NSA corridor | 60 miles | DoD, cyber, contractor density |
| Joint Base San Antonio / Lackland | 60 miles | Cyber training + military student volume |
| Norfolk / Hampton Roads | 60 miles | Navy, contractors, shipyard cyber roles |
| San Diego naval cluster | 60 miles | Navy, Marine, contractor audience |
| Colorado Springs / Peterson / Schriever / Carson | 60 miles | Space Force, Army, contractors |
| Fort Liberty | 60 miles | Army, SOF, transition audience |
| Joint Base Lewis-McChord (JBLM) | 60 miles | Army / Air Force, transition audience |
| Fort Cavazos | 60 miles | Large Army population |
| Fort Moore | 60 miles | Army training audience |
| Nellis / Creech AFB | 60 miles | Air Force, contractors |
| Pearl Harbor / Hickam | 60 miles | Navy / Air Force, Indo-Pacific roles |
| Scott AFB | 60 miles | TRANSCOM / federal contractor audience |
| Tampa / MacDill AFB | 60 miles | CENTCOM/SOCOM + contractor hub |
| Huntsville / Redstone Arsenal | 60 miles | Army, missile/defense contractors |

**Geo bid modifier starters:**

| Cluster | Examples | Modifier |
|---------|----------|----------|
| Military / DoD | 60-mile radius around priority bases | +15% |
| Federal / contractor | High-density federal return-to-office and contractor metros: DC/NOVA/MD, Fort Meade corridor, Huntsville, San Antonio, Colorado Springs, Tampa, Norfolk, San Diego, Omaha, Charleston SC | +10% |
| State / local government | State capitals and high-population cities only; avoid rural areas for now | +5% |
| First responder | Large county seats and metro public-safety hubs | +5% |

**Federal/contractor targeting rule:** prioritize high-density federal employee and government-contractor office markets, especially where return-to-office commuting concentrates demand. Avoid broad rural federal footprint unless tied to a known installation, agency campus, or contractor hub.

**First federal/DoD city pass:**

| City / metro | Why it matters |
|-------------|----------------|
| Washington, D.C. | Primary federal hub |
| Arlington, VA | Pentagon and dense DoD workforce |
| Alexandria, VA | High DoD contractor presence |
| San Diego, CA | Major Navy and Marine Corps hub |
| San Antonio, TX | Joint Base San Antonio |
| Norfolk, VA | Large naval base and contractor market |
| Honolulu, HI | State capital and Indo-Pacific Command |
| Huntsville, AL | Redstone Arsenal and NASA |
| Colorado Springs, CO | Space Command and Air Force bases |
| Denver, CO | State capital and Denver Federal Center |
| Oklahoma City, OK | State capital and Tinker Air Force Base |
| Jacksonville, FL | Multiple naval stations |
| El Paso, TX | Fort Bliss |
| Atlanta, GA | State capital and CDC headquarters |

**State/local government targeting rule:** Focus on state capitals and larger cities with heavier population density. Do **not** add rural counties, small towns, or broad low-density regions until the campaign proves checkout signal in metro areas.

---

## Campaign 3 — students, educators, veterans, workforce

**Name:** `Security+ SY0-701 · Student Workforce · US`

| Setting | Value |
|---------|-------|
| Budget | **$20/day** |
| Bidding | Maximize clicks · max CPC **$2.50** to start if CPC runs high; hold 7 days |
| Geo | US only · presence · campus/workforce hub bid modifiers |
| Schedule | Shared schedule above; weekend study windows matter |
| Final URL | `https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_workforce_us&utm_content=student-workforce` |

**Message:** Security+ prep for students, educators, veterans, career changers, and job-placement programs. Verified learner discount is a separate path; do not put discount copy in RSA until the verification flow exists.

**Geo bid modifier starters:**

| Cluster | Examples | Modifier |
|---------|----------|----------|
| College cyber programs | CAE schools, community colleges, state universities | +10% |
| Workforce programs | American Job Center metros, state workforce board regions | +10% |
| Veteran transition | SkillBridge/TAP-adjacent metros, VA workforce hubs | +10% |

---

## Rollout order

1. **Keep current campaign history** as the baseline.
2. Build the three campaign shells as paused drafts.
3. Launch **Core Exam Prep** first for 48–72 hours if cash flow needs control.
4. Launch **Military Gov 8140** and **Student Workforce** once core tracking is confirmed.
5. Log spend and clicks separately in notes until admin supports all three campaign IDs.

---

## Week-1 bid review

Do **not** adjust keyword bids during the first week unless spend is clearly broken or irrelevant traffic is obvious. On day 7, review by campaign and keyword:

| Signal | Action |
|--------|--------|
| Keyword has clicks + `begin_checkout` | Keep; consider exact match promotion |
| Keyword has high CPC but no checkout | Lower max CPC or pause after enough clicks |
| Search term is course/free/dump intent | Add negative immediately |
| After-work window converts better | Keep schedule boost; do not over-edit keywords |
| One campaign is spending without checkout | Pause weak campaign before changing landing |

---

## High-conversion priorities

Use these as the first places to look when deciding where to raise bids or keep spend after the week-1 hold:

| Campaign | Priority signals | Why |
|----------|------------------|-----|
| `secplus_core_us` | Timed exam, exam simulation, readiness check, after-course practice, not-PDF/no-download | Buyer is already studying and wants confidence |
| `secplus_gov_us` | DoD 8140, federal employee, contractor required, 60-mile base radii, return-to-office federal hubs | Cert is tied to job, contract, or office return pressure |
| `secplus_workforce_us` | 60-mile CAE school radii, students, educators, veterans, workforce/job placement | Cert is tied to graduation, placement, or career transition |

Competitor contrast should be clear but policy-safe: **not another overpriced course**, **not a stale PDF**, **not a desktop engine**, **not a dump**.

---

## URL exclusions / expansion guardrails

AI Max and URL expansion stay **Off**. If Google prompts for URL exclusions, exclude:

```text
/admin
/admin/
/COMP_TIA_SEC+/secplus-portal-request-link.html
/COMP_TIA_SEC+/secplus-portal-restore-access.html
/verify-question.html
/how-we-verify-questions.html
/secplus-sample
/sample
/CCNA-Study/
/CCNP-ENCOR-Study/
/question-
```

Only `/comptia-sec+-home.html` should be the primary paid landing page until a dedicated verified-discount page is built.

---

## What not to change yet

- Do not modify the admin dashboard.
- Do not remove the original `secplus_portal` data trail.
- Do not advertise verified discounts until the verification page and Stripe promo flow exist.
- Do not use OCONUS in this three-campaign paid structure; this plan is **US only**.
- Do not use “guaranteed pass,” “actual exam questions,” “real exam,” or “official DoD” language.

[[README|← Sec+ Campaign folder]]

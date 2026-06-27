---
type: build-checklist
product: secplus
channel: google-ads
tags:
  - marketing
  - google-ads
  - secplus
  - checklist
  - build
---

# Sec+ Google Ads Build Checklist — three US campaigns

Use this checklist in Google Ads to build the current Security+ plan:

- **3 Search campaigns**
- **United States only**
- **$20/day each** (**$60/day total**)
- **Hold keyword bids for 7 days**
- Landing page: `/comptia-sec+-home.html`

Reference docs: [[Sec+ Three-Campaign US Plan]] · [[Sec+ Keywords]] · [[Sec+ RSA Copy]] · [[Extensions]] · [[Sec+ CAE College Target List]]

---

## 0. Before opening Google Ads

- [ ] Confirm Stripe product is live: `secplus-portal-30d` at **$19.99 / 30 days**
- [ ] Open cert home on desktop and phone: `/comptia-sec+-home.html`
- [ ] Confirm purchase button starts Stripe checkout
- [ ] Confirm GA4 `begin_checkout` is imported as **Primary** in Google Ads
- [ ] Keep admin dashboard unchanged for now
- [ ] Keep old `secplus_portal` campaign history; do **not** delete it

---

## 1. Shared settings for all three campaigns

Use these settings every time you create a campaign.

| Setting | Value |
|---------|-------|
| Campaign type | **Search** |
| Search partners | **Off** |
| Display Network | **Off** |
| Budget | **$20/day per campaign** |
| Bidding | **Maximize clicks** |
| Max CPC | **$2.75** |
| Locations | **United States only** |
| Location option | **Presence: people in or regularly in targeted locations** |
| Language | English |
| AI Max / URL expansion | **Off** |
| Conversion | GA4 `begin_checkout` as Primary |

**Do not adjust keyword bids for the first 7 days** unless traffic is clearly junk.

---

## 2. Create Campaign 1 — Core Exam Prep

- [ ] Create new Search campaign
- [ ] Campaign name: `Security+ SY0-701 · Core Exam Prep · US`
- [ ] Daily budget: **$20/day**
- [ ] Bidding: **Maximize clicks**
- [ ] Max CPC: **$2.75**
- [ ] Location: **United States only**
- [ ] Location option: **Presence**
- [ ] Search partners: **Off**
- [ ] AI Max / URL expansion: **Off**

### Campaign 1 ad group

- [ ] Ad group name: `SY0-701 Exam Prep`
- [ ] Display path: `Security+` / `Exam-Prep`
- [ ] Final URL:

```text
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_core_us&utm_content=core-exam-prep
```

### Campaign 1 keywords

Paste these into the ad group:

```text
[security+ exam simulation online]
[security+ timed practice test]
"security+ exam simulation online"
"security+ timed practice test online"
"security+ mock exam online"
"security+ realistic practice test"
"security+ practice exam simulation"
"security+ timed exam prep"
"90 minute security+ practice test"
"security+ timed exam simulation"
"security+ exam prep online"
"sy0-701 prep"
"security+ study prep online"
"security+ practice portal"
"security+ browser exam simulator"
"security+ online exam simulator"
"security+ adaptive review"
"security+ scorecard review"
"security+ readiness check"
"security+ last minute exam prep"
"security+ after course practice"
"security+ not a pdf"
"security+ no download practice"
"sy0-701 objective based prep"
"sy0-701 timed mock exam"
```

---

## 3. Create Campaign 2 — Military / Gov / 8140

- [ ] Create new Search campaign
- [ ] Campaign name: `Security+ SY0-701 · Military Gov 8140 · US`
- [ ] Daily budget: **$20/day**
- [ ] Bidding: **Maximize clicks**
- [ ] Max CPC: **$2.75**
- [ ] Location: **United States only**
- [ ] Location option: **Presence**
- [ ] Search partners: **Off**
- [ ] AI Max / URL expansion: **Off**

### Campaign 2 ad group

- [ ] Ad group name: `Security+ 8140 Prep`
- [ ] Display path: `Security+` / `DoD-8140`
- [ ] Final URL:

```text
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_gov_us&utm_content=mil-gov-8140
```

### Campaign 2 keywords

Paste these into the ad group:

```text
[security+ 8140]
[dod security+ certification]
"security+ required for job"
"security+ certification job requirement"
"security+ work requirement"
"security+ 8140"
"dod security+ certification"
"security+ dod certification"
"8140 security+ prep"
"security+ dod 8140 prep"
"comptia security+ for dod"
"sy0-701 dod requirement"
"security+ government contractor"
"security+ federal contractor exam"
"security+ for government job"
"security+ clearance certification"
"security+ contractor certification"
"security+ for military"
"security+ army mos"
"security+ air force cyber"
"security+ navy credential"
"security+ for police"
"security+ state government job"
"security+ local government cyber"
"security+ 8140 baseline certification"
"dod 8140 security+ exam prep"
"security+ federal employee"
"security+ contractor required"
"security+ dod contractor required"
"security+ government employee cert"
"security+ return to office"
"security+ for federal employees"
"security+ for dod contractors"
"security+ baseline certification"
```

### Campaign 2 military base radius targets

For military and government buyers, use **60-mile radius targeting** around priority bases and base metros inside `secplus_gov_us`.

Google Ads setup:

1. Campaign: `Security+ SY0-701 · Military Gov 8140 · US`
2. Locations → Advanced search → Radius
3. Enter the base or metro name
4. Set radius to **60 miles**
5. Location option remains **Presence**

First base-radius pass:

- [ ] Add Fort Meade / NSA corridor — **60 miles**
- [ ] Add Joint Base San Antonio / Lackland — **60 miles**
- [ ] Add Norfolk / Hampton Roads — **60 miles**
- [ ] Add San Diego naval cluster — **60 miles**
- [ ] Add Colorado Springs / Peterson / Schriever / Carson — **60 miles**
- [ ] Add Fort Liberty — **60 miles**
- [ ] Add Joint Base Lewis-McChord (JBLM) — **60 miles**
- [ ] Add Fort Cavazos — **60 miles**
- [ ] Add Fort Moore — **60 miles**
- [ ] Add Nellis / Creech AFB — **60 miles**
- [ ] Add Pearl Harbor / Hickam — **60 miles**
- [ ] Add Scott AFB — **60 miles**
- [ ] Add Tampa / MacDill AFB — **60 miles**
- [ ] Add Huntsville / Redstone Arsenal — **60 miles**

### Campaign 2 geo bid modifiers

Add these only if the Google Ads UI allows clean location modifiers during setup. Otherwise, wait until after launch.

| Cluster | Examples | Modifier |
|---------|----------|----------|
| Military / DoD | 60-mile radius around priority bases | +15% |
| Federal / contractor | High-density federal return-to-office and contractor metros | +10% |
| State / local government | State capitals and large population centers; avoid rural areas | +5% |
| First responder | Large county seats and metro public-safety hubs | +5% |

### Campaign 2 federal / contractor density pass

Target federal workers and contractors where return-to-office creates higher office/commute density. Avoid rural federal footprint for now unless tied to a known installation, agency campus, or contractor hub.

- [ ] Add DC / Northern Virginia / Maryland commuter corridor
- [ ] Add Fort Meade corridor
- [ ] Add Huntsville / Redstone Arsenal contractor market
- [ ] Add San Antonio federal / defense contractor market
- [ ] Add Colorado Springs defense / space contractor market
- [ ] Add Tampa / MacDill contractor market
- [ ] Add Norfolk / Hampton Roads contractor market
- [ ] Add San Diego defense contractor market
- [ ] Add Omaha federal / defense support market
- [ ] Add Charleston SC contractor / federal support market
- [ ] Do **not** add broad rural regions unless tied to a base, agency campus, or contractor concentration

First high-density federal / DoD city pass:

- [ ] Add Washington, D.C.
- [ ] Add Arlington, VA
- [ ] Add Alexandria, VA
- [ ] Add San Diego, CA
- [ ] Add San Antonio, TX
- [ ] Add Norfolk, VA
- [ ] Add Honolulu, HI
- [ ] Add Huntsville, AL
- [ ] Add Colorado Springs, CO
- [ ] Add Denver, CO
- [ ] Add Oklahoma City, OK
- [ ] Add Jacksonville, FL
- [ ] Add El Paso, TX
- [ ] Add Atlanta, GA

### Campaign 2 state/local government pass

Target state and local government buyers in **capitals and larger cities only**. Avoid rural areas for now.

- [ ] Add state capitals with meaningful public-sector IT / cyber hiring
- [ ] Add larger cities with heavy population density
- [ ] Add large county seats only when they overlap public-safety or government IT demand
- [ ] Do **not** add rural counties, small towns, or wide low-density regions yet
- [ ] Review this cluster separately on day 7 before expanding

### Contractor verification notes

When the verified discount flow is built, contractors can verify with:

- [ ] Approved contractor company domain (`@lockheedmartin.com`, `@leidos.com`, etc.)
- [ ] Government-issued contractor mailbox using layout like `[firstname].[lastname].[identifier]@[domain].mil`
- [ ] Government-issued contractor mailbox using layout like `[firstname].[initial].[lastname].[identifier]@[domain].mil`
- [ ] Contractor/civilian/vendor identifiers: `.ctr`, `.civ`, `v-`
- [ ] DoD / federal domains: `@mail.mil`, `@army.mil`, `@navy.mil`, `@usmc.mil`, `@defense.gov`
- [ ] Federal civilian domains: `@faa.gov`, `@energy.gov`, `@gsa.gov`
- [ ] Manual review if the address does not match `.gov`, `.mil`, an approved contractor domain, or contractor/civilian/vendor marker pattern

Work/government email verifies **eligibility only**. Checkout should use the email where the learner wants account and access links. See [[../Website_Main/Email Verification Setup|Email Verification Setup]].

---

## 4. Create Campaign 3 — Student / Workforce

- [ ] Create new Search campaign
- [ ] Campaign name: `Security+ SY0-701 · Student Workforce · US`
- [ ] Daily budget: **$20/day**
- [ ] Bidding: **Maximize clicks**
- [ ] Max CPC: **$2.50** to start if CPC looks high; otherwise **$2.75**
- [ ] Location: **United States only**
- [ ] Location option: **Presence**
- [ ] Search partners: **Off**
- [ ] AI Max / URL expansion: **Off**

### Campaign 3 ad group

- [ ] Ad group name: `Security+ Career Prep`
- [ ] Display path: `Security+` / `Career-Prep`
- [ ] Final URL:

```text
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_workforce_us&utm_content=student-workforce
```

### Campaign 3 keywords

Paste these into the ad group:

```text
"security+ required for graduation"
"security+ capstone requirement"
"security+ cybersecurity degree"
"security+ college requirement"
"security+ for college students"
"comptia security+ student prep"
"security+ community college cyber"
"security+ for veterans"
"security+ skillbridge prep"
"security+ wioa training"
"security+ job center cert"
"security+ retraining program"
"security+ career change cyber"
"security+ vr&e"
"security+ tap transition"
"security+ required for college"
"security+ for cybersecurity students"
"security+ for it students"
"security+ educator prep"
"security+ veterans cyber jobs"
"security+ workforce development"
"security+ job placement cyber"
"security+ career readiness cyber"
```

**Do not add discount keywords yet** (`student discount`, `educator discount`, etc.) until the verified-discount page and Stripe promo flow exist.

### Campaign 3 geo bid modifiers

For students and educators, use **60-mile radius targeting** around the priority schools in [[Sec+ CAE College Target List]]. Add these as location targets inside `secplus_workforce_us`.

| Cluster | Examples | Modifier |
|---------|----------|----------|
| College cyber programs | 60-mile radius around CAE schools, community colleges, state universities | +10% |
| Workforce programs | American Job Center metros, state workforce board regions | +10% |
| Veteran transition | SkillBridge/TAP-adjacent metros, VA workforce hubs | +10% |

Use [[Sec+ CAE College Target List#60-mile radius targeting]] for the first college-area build. Do not name a school in ad copy until the Security+ mapping is verified on an official school page.

### Campaign 3 first school radius pass

- [ ] Add Ivy Tech Community College — **60 miles**
- [ ] Add WGU — **60 miles around major student concentration areas only if useful**
- [ ] Add UMGC — **60 miles around Adelphi / DMV area**
- [ ] Add NOVA — **60 miles**
- [ ] Add Miami Dade College — **60 miles**
- [ ] Add Tarrant County College District — **60 miles**
- [ ] Add Wake Technical Community College — **60 miles**
- [ ] Add Collin College — **60 miles**
- [ ] Add Pima Community College — **60 miles**
- [ ] Add Cuyahoga Community College (Tri-C) — **60 miles**

---

## 5. Apply shared ad schedule

Apply this schedule to all three campaigns.

| Day | Run time | Bid adjustment |
|-----|----------|----------------|
| Monday–Friday | 6:00 AM–9:00 AM | 0% |
| Monday–Friday | 11:00 AM–2:00 PM | 0% |
| Monday–Thursday | 5:00 PM–11:30 PM | +20% |
| Friday | 5:00 PM–10:00 PM | +10% |
| Saturday–Sunday | 9:00 AM–11:00 PM | +10% |
| Overnight | Pause or -90% |

**Reason:** buyers search before work, during lunch, after work, and during weekend study blocks.

---

## 6. Paste RSA copy

Use the same base RSA set on all three campaigns. You can swap one or two headlines later after results come in.

### Pin headlines

- [ ] Pin H1: `SY0-701 Exam Prep Online`
- [ ] Pin H2: `Timed 90-Min Exam Sim`

### Headlines

```text
SY0-701 Exam Prep Online
Timed 90-Min Exam Sim
Am I Ready? · Scorecard
1000+ Verified SY0-701 Qs
Blueprint-Verified Bank
90-Min Timed Exam + Scorecard
30-Day Access · $19.99
Adaptive Review Modes
DoD 8140-Aligned Prep
Cert Required for Job
Not a PDF · Browser Prep
34 PBQ Scenarios Included
Detailed Domain Scorecard
Study Phone, Tablet, Desktop
Interactive Exam Simulation
```

### Descriptions

```text
SY0-701 exam prep in your browser—1000+ verified questions, adaptive review, timed sim.

90-min timed exam + scorecard. $19.99/30d. Blueprint-tagged items—not a PDF dump.

DoD, military, or contract deadline? Last-mile prep after your course—not a bootcamp.

One payment—no subscription. Verified explanations. PBQ scenarios included.
```

**Do not use:** guaranteed pass, actual exam questions, real exam, official DoD, free timed exam, or discount wording.

---

## 7. Add sitelinks

Use these on all three campaigns. Replace `utm_campaign` per campaign:

- Core: `secplus_core_us`
- Gov: `secplus_gov_us`
- Workforce: `secplus_workforce_us`

### Sitelinks

| Link text | Description 1 | Description 2 | `utm_content` |
|-----------|---------------|---------------|---------------|
| `30-Day Access · $19.99` | Full exam prep + timed sim | One payment, no subscription | `sitelink-30d#purchase` |
| `1000+ SY0-701 Questions` | Blueprint-verified bank | Adaptive review modes | `sitelink-bank#purchase` |
| `Timed 90-Min Sim` | Mixed MCQ and PBQ run | Domain scorecard included | `sitelink-sim#purchase` |
| `Preview Sample Prep` | MCQ + 3 PBQ scenarios | Same UI as full access | `sitelink-samples#home-secplus-samples-title` |
| `DoD 8140 Exam Prep` | Work-required SY0-701 | Timed sim + verified bank | `sitelink-dod#purchase` |
| `Scorecard & Review` | Timed sim + weak domains | Adaptive review modes | `sitelink-scorecard#purchase` |

Example Core sitelink URL:

```text
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_core_us&utm_content=sitelink-30d#purchase
```

---

## 8. Add negatives

Add these negatives at campaign level for all three campaigns.

```text
free
bootcamp
udemy
coursera
boson
jobs
salary
ccna
cissp
ceh
examtopics
"free course"
"free practice"
"free practice test"
"free questions"
"free pbq"
"free dump"
"free download"
"free timed"
"free timed simulation"
"free timed sample"
"free simulation"
"35 minute free"
"training course"
"instructor led"
"in person"
"live class"
"online course"
"video course"
"course coupon"
"coupon code"
"discount code"
"exam voucher"
"voucher"
"certmaster"
"measureup"
"testout"
"skillsoft"
"pluralsight"
"linkedin learning"
"jason dion"
"brain dump"
"braindump"
"dumps"
"test dump"
"exam answers"
"answer key"
"comptia sec+ practice exam"
"comptia sec+ practice test"
"comptia security+ practice exam"
"comptia security+ practice questions"
"comptia security+ practice test"
"exam dump"
"exam questions and answers"
"guaranteed pass"
"pass guarantee"
"pass4sure"
"pdf download"
"pdf"
"ebook"
"book"
"study guide pdf"
"torrent"
"vce"
"ete"
"vumingo"
"avanset"
"quizlet"
"flashcards"
"professor messer"
"dion training"
"sec+ practice test"
"security+ practice questions"
"security+ jobs"
"security+ salary"
"security+ training"
"security+ question bank"
"security+ 1000 questions"
"security+ 1000+ questions"
"sy0-701 v5.0 question bank"
"latest sy0-701 questions"
"sy0 701 pdf"
"sy0-701 practice questions"
"comptia security+ question bank"
"ccna 200-301"
"ccnp encor"
"pen test+"
"unauthorized exam content"
"exam content"
[security+ practice exam]
```

---

## 9. URL exclusions / expansion guardrails

Keep **AI Max / URL expansion Off**. If Google asks for URL exclusions, or if any automated URL expansion is ever enabled, exclude:

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

`/how-we-verify-questions.html` can become a sitelink later, but it should not become the primary landing page through automation.

---

## 10. Final pre-launch check

- [ ] All three campaigns are **paused drafts**
- [ ] Each campaign says **Search only**
- [ ] Each campaign says **United States only**
- [ ] Location option is **Presence**
- [ ] Search partners are **Off**
- [ ] AI Max / URL expansion is **Off**
- [ ] Each campaign budget is **$20/day**
- [ ] Keyword bids / max CPC are set but will be held for 7 days
- [ ] Final URLs open `/comptia-sec+-home.html`
- [ ] UTMs are correct:
  - [ ] `secplus_core_us`
  - [ ] `secplus_gov_us`
  - [ ] `secplus_workforce_us`
- [ ] Purchase button opens Stripe checkout
- [ ] GA4 Realtime shows `begin_checkout` on a test click

---

## 11. Launch order

If you want controlled spend:

1. [ ] Enable **Core Exam Prep** first
2. [ ] Confirm clicks and checkout tracking within 24–48 hours
3. [ ] Enable **Military Gov 8140**
4. [ ] Enable **Student Workforce**

If you want full plan immediately:

1. [ ] Enable all three campaigns
2. [ ] Log starting date and time in admin notes
3. [ ] Do not change bids for 7 days

---

## 12. Day 3 review

- [ ] Export search terms
- [ ] Add negatives for course, dump, free, PDF, and job/salary intent
- [ ] Confirm each campaign is spending
- [ ] Confirm after-work traffic is coming in
- [ ] Do **not** adjust keyword bids yet unless traffic is clearly bad

---

## 13. Day 7 keyword review

Now adjust keyword bids based on results.

| Signal | Action |
|--------|--------|
| Clicks + `begin_checkout` | Keep; consider exact match |
| High CPC + no checkout | Lower max CPC or pause after enough clicks |
| Search terms are wrong | Add negatives first |
| One campaign spends but no checkout | Pause weak campaign before rewriting landing |
| After-work schedule performs | Keep +20% after-work window |
| Weekend performs | Keep weekend +10% |

Log review note:

```text
TEST: Three US campaigns at $20/day each
HYP: Separate intent tracks improve qualified clicks and checkout signal
START: YYYY-MM-DD
DAY 7 REVIEW: keyword bids adjusted from search term + checkout data
```

[[README|← Sec+ Campaign folder]]

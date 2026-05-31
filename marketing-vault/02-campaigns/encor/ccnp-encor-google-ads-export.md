---
type: campaign-export
channel: google-ads
product: encor-350-401
status: active
parent: ccnp-encor-google-ads
utm_campaign: encor_portal
created: 2026-05-31
---

# CCNP ENCOR Google Ads — paste-ready export

Copy blocks below into Google Ads (Search campaign) or Google Ads Editor. Parent strategy: [[ccnp-encor-google-ads|ENCOR Google Ads]] · Landing: [[../../06-website-optimization/pages/ccnp-home|ccnp-home.html]].

**Policy:** Exam prep / practice only — not Cisco endorsement, not “guaranteed pass,” not clearance or DoD qualification.

---

## Campaign shell (create once)

| Setting              | Value                                                                                                                     |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Campaign name        | `CCNP ENCOR 350-401 · Exam prep · becertifiedtoday`                                                                       |
| Campaign type        | Search                                                                                                                    |
| Networks             | Search only (uncheck Search partners until baseline CPA)                                                                  |
| Locations            | United States (add geo ad groups below for defense metros)                                                                |
| Language             | English                                                                                                                   |
| Bidding              | Maximize conversions (after `begin_checkout` imported) — or **Maximize clicks** with CPC cap for week 1                   |
| Daily budget (start) | $10–20/day total campaign; 60% free samples group / 40% sim purchase (ENCOR volume is smaller than CCNA)                  |
| UTM campaign         | `encor_portal`                                                                                                            |

### Campaign-level negative keywords (Phrase match)

```
"free course"
"training course"
"bootcamp"
"instructor led"
"brain dump"
"exam dump"
"guaranteed pass"
"pdf download"
"udemy"
"coursera"
"cbt nuggets"
"ine encor"
"cisco netacad"
"jobs"
"salary"
"ccna only"
"ccna practice"
"ccie lab"
"ccie enterprise"
"devnet"
"ccnp design"
"comptia security+"
"encor course"
"cisco live training"
"gns3 tutorial"
```

---

## Ad group 1 — `encor_lead_free_sim` (launch first)

**Intent:** Practice test / mock exam → free 45-min timed sim + scorecard (email unlock).

**Final URL (recommended — lead-first):**

```
https://becertifiedtoday.com/ccnp-home.html#encor-lead-capture?utm_source=google&utm_medium=cpc&utm_campaign=encor_portal&utm_content=lead-free-sim
```

**Alternate (home samples — no email):**

```
https://becertifiedtoday.com/ccnp-home.html?utm_source=google&utm_medium=cpc&utm_campaign=encor_portal&utm_content=free-samples
```

**Alternate (direct sample — A/B test):**

```
https://becertifiedtoday.com/sample?track=encor-questions&utm_source=google&utm_medium=cpc&utm_campaign=encor_portal&utm_content=sample-questions
```

**Display path (optional):** `ENCOR` / `Free-Sim`

**RSA — Headlines** (≤30 chars; pin H1–H3 in UI)

```
Free ENCOR Timed Sim
Start Free ENCOR Sample
45-Min Practice + Scorecard
ENCOR 350-401 Sample Exam
20 MCQ + D&D + CLI Lab
Exam Prep — Not a Course
No GNS3 — Browser Prep
Shuffled Sample Questions
Interactive CLI Labs
No PDFs — Browser Prep
CCNP ENCOR 350-401 Prep
Realistic ENCOR Practice
Email Unlock · One Free Run
Try Before You Buy
Be Certified Today
```

**RSA — Descriptions** (≤90 chars)

```
Free 45-min ENCOR 350-401 sample: 20 MCQ, 2 drag-and-drop, ACL/CoPP CLI lab in your browser.
Realistic CCNP ENCOR practice before test day. Full 120-min sim when you are ready. No GNS3 or PDFs.
Exam preparation—not a training course. Verified explanations. No dumps or third-party lab software.
Enter email to start your free simulation. Prefer no email? Try two free sample questions on site.
```

**Pin suggestion:** Headline 1 → `Free ENCOR Timed Sim` · Headline 2 → `Start Free ENCOR Sample` · Headline 3 → `45-Min Practice + Scorecard`

### Keywords — `encor_lead_free_sim`

Paste into ad group keyword box. **Phrase** = `"quotes"` · **Exact** = `[square brackets]`.

```
"ccnp encor practice test"
"encor 350-401 practice test"
[encor 350-401 practice test]
"ccnp encor practice exam"
"encor 350-401 practice exam"
[encor 350-401 practice exam]
"ccnp encor mock exam"
"encor practice questions"
"encor 350-401 practice questions"
"cisco encor practice test"
[cisco encor practice test]
"ccnp encor exam prep"
"encor 350-401 prep"
"encor 350-401 exam prep"
"ccnp enterprise practice test"
```

**Ad group negatives (Phrase):**

```
"free course"
"bootcamp"
"dump"
"pdf"
"udemy"
"cbt nuggets"
"ine encor"
"netacad"
"jobs"
"salary"
"ccna only"
```

**Primary conversion:** `generate_lead` · **Secondary:** `begin_checkout` (upsell)

---

## Ad group 2 — `encor_sim_purchase`

**Intent:** Timed simulation / exam sim → $9.99 one-time 120-minute test.

**Final URL:**

```
https://becertifiedtoday.com/ccnp-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=encor_portal&utm_content=sim-purchase
```

**Display path:** `ENCOR` / `Timed-Sim`

**RSA — Headlines**

```
120-Min ENCOR Exam Sim
ENCOR 350-401 Timed Test
Timed Sim — $9.99
Domain-Weighted Scorecard
50 MCQ + 5 D&D + 4 Labs
120 Minutes Like Test Day
No GNS3 — Browser Exam Prep
CCNP ENCOR Simulation
Exam Prep — Not a Course
Full Dry Run Before Test Day
Pass/Fail Summary at End
One Attempt · No Subscription
Be Certified Today
Try Free Samples on Site
```

**RSA — Descriptions**

```
One 120-minute ENCOR 350-401 session: 50 MCQ, 5 drag-and-drop, 4 CLI labs. $9.99 one attempt.
Same clock and mix as test day—not a video course. Verified explanations in your browser.
Exam-realistic CCNP ENCOR prep. No PDF dumps or GNS3 installs required.
Free sample questions and labs on the same page if you want to try before you buy the full sim.
```

**Pin suggestion:** H1 → `120-Min ENCOR Exam Sim` · H2 → `Timed Sim — $9.99` · H3 → `50 MCQ + 5 D&D + 4 Labs`

### Keywords — `encor_sim_purchase`

```
"encor exam simulation"
[encor exam simulation]
"ccnp encor simulation"
"encor timed exam"
"encor timed test"
"ccnp encor timed exam"
"cisco encor simulation"
"encor practice simulation"
"ccnp encor mock exam timed"
"encor full practice exam"
"pass encor first try"
"encor retake prep"
"encor 350-401 simulation"
```

**Ad group negatives (Phrase):**

```
"free"
"bootcamp"
"course"
"dump"
"pdf"
"jobs"
"netacad"
```

**Primary conversion:** `begin_checkout` (item `encor_timed_simulation`)

---

## Ad group 3 — `encor_portal_access`

**Intent:** Multi-day library access (10-day $9.99 · 30-day $19.99) — timed sim included.

**Final URL:**

```
https://becertifiedtoday.com/ccnp-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=encor_portal&utm_content=portal-access
```

**Display path:** `ENCOR` / `Portal-Access`

**RSA — Headlines**

```
ENCOR Full Question Bank
10-Day ENCOR Access
30-Day ENCOR Access
Portal + Timed Sim Included
CCNP ENCOR Exam Prep Portal
All Six ENCOR Domains
D&D & CLI Lab Practice
No Subscription — One-Time
$9.99 / 10 Days · From
$19.99 / 30 Days · From
Browser-Only Exam Prep
Verified 350-401 Explanations
Exam Prep — Not a Course
Be Certified Today
Free Samples on Same Page
```

**RSA — Descriptions**

```
Full ENCOR 350-401 library: question banks, CLI labs, drag-and-drop, portal modes, and timed exam simulation in your browser.
Choose 10-day ($9.99) or 30-day ($19.99) access. One-time purchase—no recurring membership.
Exam prep aligned to Cisco ENCOR objectives—not PDF dumps or instructor-led courses.
120-minute timed simulation included with portal passes. Try free samples before you checkout.
```

**Pin suggestion:** H1 → `ENCOR Full Question Bank` · H2 → `Portal + Timed Sim Included`

### Keywords — `encor_portal_access`

```
"encor study guide practice"
"encor 350-401 study prep online"
"encor question bank"
"ccnp encor question bank"
"cisco encor practice portal"
"encor practice test online"
"encor 350-401 online practice"
"ccnp encor exam prep online"
"encor 30 day study"
"encor cram practice"
```

**Primary conversion:** `begin_checkout` (`encor_portal_10d` or `encor_portal_30d`)

---

## Ad group 4 — `encor_labs_pbq` (optional mid-funnel)

**Intent:** Drag-and-drop / CLI lab / automation practice → home page samples → portal/sim purchase.

**Final URL:**

```
https://becertifiedtoday.com/ccnp-home.html?utm_source=google&utm_medium=cpc&utm_campaign=encor_portal&utm_content=labs-pbq
```

**Display path:** `ENCOR` / `Labs-PBQ`

**RSA — Headlines**

```
ENCOR Drag-Drop Practice
ENCOR CLI Lab Simulation
ACL & CoPP Sample Lab
Automation & JSON Practice
No GNS3 Required
Interactive ENCOR Labs
Browser Lab — No Install
Exam Prep — Not a Course
Try Free Sample Questions
Full Portal When Ready
CCNP ENCOR 350-401
Verified Explanations
Be Certified Today
Python & API Sample Items
```

**RSA — Descriptions**

```
Interactive ENCOR 350-401 practice: drag-and-drop, ACL/CoPP CLI lab, and automation items in your browser.
Exam prep only—not a course. No GNS3, IOU, or PDF dumps. Upsell to portal or timed sim on site.
Free sample questions and labs available. Full 120-minute simulation on CCNP ENCOR home.
Practice performance-based items before test day. Verified explanations aligned to Cisco objectives.
```

### Keywords — `encor_labs_pbq`

```
"encor cli lab practice"
[encor cli lab practice]
"ccnp drag and drop practice"
"encor lab simulation"
"encor automation practice questions"
"encor drop down question"
"encor simulation lab online"
"encor practice lab browser"
"encor without gns3"
"ccnp encor cli practice"
```

---

## Ad group 5 — `encor_federal_dc` (geo template)

Duplicate ad group per metro; change **Locations** targeting and `utm_content` only.

| Ad group name | Locations (target) | utm_content |
|---------------|-------------------|-------------|
| `encor_federal_dc` | DC + Arlington + Alexandria + Fairfax + Bethesda + Silver Spring | `federal-dc` |
| `encor_federal_cos` | Colorado Springs | `federal-cos` |
| `encor_federal_satx` | San Antonio | `federal-satx` |
| `encor_federal_norfolk` | Norfolk + Virginia Beach + Chesapeake | `federal-norfolk` |

**Final URL (example DC):**

```
https://becertifiedtoday.com/ccnp-home.html#exam-audience?utm_source=google&utm_medium=cpc&utm_campaign=encor_portal&utm_content=federal-dc
```

Use `#purchase` variant for purchase-intent federal keywords.

**RSA — Headlines**

```
ENCOR 350-401 Exam Prep
DoD IT Role Exam Prep
Browser ENCOR Practice
Free ENCOR Sample Questions
8140 Baseline Exam Prep
Defense Contractor Cert Prep
No GNS3 — Browser Labs
Federal Workforce Exam Prep
Timed Sim + Full Library
Exam Prep — Not a Course
Practice Before Test Day
Be Certified Today
120-Min Timed Simulation
Verified 350-401 Explanations
Study From Duty Station
```

**RSA — Descriptions**

```
ENCOR 350-401 exam prep for federal, DoD, and contractor IT roles. Browser-only—study on your schedule.
Free sample questions, drag-and-drop, and CLI lab. Full 120-min simulation and portal access when ready.
Exam preparation only—we do not process clearance or official DoD qualification. Confirm reqs with your org.
Not a bootcamp or PDF dump. Realistic CCNP ENCOR practice tests and CLI labs in your browser.
```

**Compliance:** Do not claim DoD or Cisco endorsement. See [[../../01-strategy/cisco-certifications-exam-prep-foundation|Cisco foundation]] disclaimer.

### Keywords — federal (Phrase / Exact)

```
"ccnp encor federal"
"ccnp encor defense contractor"
"encor 350-401 government"
"cisco encor exam prep contractor"
"encor dod"
"encor 8140"
"ccnp encor military"
"cisco encor federal"
```

**Note:** “clearance prep” may attract wrong intent — monitor search terms; add negatives if needed.

---

## Sitelink extensions (campaign-level)

| Link text | URL |
|-----------|-----|
| Free ENCOR sample questions | `https://becertifiedtoday.com/sample?track=encor-questions&utm_content=sitelink-sample-q` |
| 120-minute timed sim | `…/ccnp-home.html#purchase&utm_content=sitelink-sim` |
| Sample drag-and-drop | `https://becertifiedtoday.com/sample?track=encor-dnd&utm_content=sitelink-sample-dnd` |
| Pricing & access | `…/ccnp-home.html#purchase&utm_content=sitelink-pricing` |

Use full URLs with `utm_source=google&utm_medium=cpc&utm_campaign=encor_portal` on each.

---

## Callout extensions (campaign-level)

```
Free Sample Questions
Shuffled MCQ + D&D + Lab
Browser-Only — No PDFs
No GNS3 Required
Exam Prep — Not a Course
Verified Explanations
One-Time Pricing
No Subscription
350-401 Objectives Aligned
CLI Lab Simulations
```

---

## Structured snippet extensions

**Types:** Courses → `Architecture & Design` · `Infrastructure` · `Security` · `Network Assurance` · `Virtualization` · `Automation & AI`

**Types:** Types → `Timed simulation` · `Practice questions` · `Drag-and-drop items` · `CLI lab simulations`

---

## Products & services to advertise (Google campaign setup)

Paste each row into **Add products or services**. Names ≤120 chars; descriptions target **≤300 chars** (adjust if your UI allows more). All are **exam prep**, not courses.

| # | Product / service name | Landing URL |
|---|------------------------|-------------|
| 1 | Free CCNP ENCOR 350-401 Timed Simulation Sample | `https://becertifiedtoday.com/ccnp-home.html#encor-lead-capture` |
| 2 | CCNP ENCOR 350-401 120-Minute Timed Exam Simulation | `https://becertifiedtoday.com/ccnp-home.html#purchase` |
| 3 | CCNP ENCOR 350-401 10-Day All-Access Practice Portal | `https://becertifiedtoday.com/ccnp-home.html#purchase` |
| 4 | CCNP ENCOR 350-401 30-Day All-Access Practice Portal | `https://becertifiedtoday.com/ccnp-home.html#purchase` |
| 5 | Free CCNP ENCOR Sample Practice Questions | `https://becertifiedtoday.com/sample?track=encor-questions` |
| 6 | Free CCNP ENCOR Sample Drag-and-Drop Practice | `https://becertifiedtoday.com/sample?track=encor-dnd` |
| 7 | Free CCNP ENCOR ACL & CoPP CLI Lab Sample | `https://becertifiedtoday.com/sample?track=labs` |

### Descriptions (copy under each name)

**1 — Free timed simulation sample**

```
Free 45-minute CCNP ENCOR 350-401 exam prep sample in your browser: 20 multiple-choice questions, 2 drag-and-drop items, and the ACL/CoPP CLI lab. Email unlock; one free attempt per browser. Domain-weighted scorecard when you finish. Not a training course.
```

**2 — 120-minute timed exam simulation ($9.99)**

```
One full ENCOR 350-401 timed practice exam: 120 minutes with 50 multiple-choice, 5 drag-and-drop, and 4 CLI lab items in one randomized session. Pass/fail-style summary when you finish. $9.99 one attempt; no subscription. Browser-only exam prep—no GNS3 required.
```

**3 — 10-day all-access portal ($9.99)**

```
10 days of full CCNP ENCOR 350-401 exam prep in your browser: domain question banks, CLI labs, drag-and-drop sets, practice portal modes, and the 120-minute timed exam simulation. Verified explanations aligned to Cisco objectives. $9.99 one-time; no recurring membership.
```

**4 — 30-day all-access portal ($19.99)**

```
30 days of full ENCOR 350-401 exam preparation: question banks, drag-and-drop and CLI lab items, review modes, progress tracking, and the 120-minute timed simulation. Browser-only—no PDFs or GNS3. $19.99 one-time access; no subscription.
```

**5 — Free sample practice questions**

```
Two shuffled CCNP ENCOR 350-401 multiple-choice sample questions per run in your browser—with instant feedback on each answer. No checkout or email required. Finish opens upsell to the free 45-minute timed simulation.
```

**6 — Free sample drag-and-drop**

```
Try ENCOR 350-401 drag-and-drop practice items with CLI-style drop targets in your browser. Instant feedback and verified explanations. No checkout required. Returns to CCNP ENCOR home when finished.
```

**6 — Free ACL & CoPP CLI lab sample**

```
Free interactive ENCOR CLI lab: ACL and Control Plane Policing (CoPP) practice with multi-area OSPF topology in your browser. Exam-realistic lab prep without GNS3 or IOU. No checkout required.
```

### If Google asks for a single category

Use: **Education & training → Test preparation** or **Educational software / Online education** (pick the closest match; avoid “Training course” if a separate **Exam preparation** option exists).

### Priority order when the UI limits how many you can add

1. Free timed simulation sample (lead magnet)  
2. 120-minute timed exam simulation  
3. 30-day all-access portal  
4. 10-day all-access portal  
5. Free sample practice questions  
6. Free sample drag-and-drop  
7. Free CLI lab sample  

---

## Conversion actions (link in Google Ads ↔ GA4)

| Action | Source | Priority |
|--------|--------|----------|
| `generate_lead` | GA4 import | Primary for lead ad group |
| `begin_checkout` | GA4 import | Primary for sim / portal groups |
| Purchase (Stripe) | Optional offline / enhanced | Secondary |

---

## Launch checklist

- [ ] Campaign + 2 ad groups live: `encor_lead_free_sim`, `encor_sim_purchase`
- [ ] Final URLs match table above (UTMs + anchors)
- [ ] Campaign negatives pasted
- [ ] GA4 key events: `generate_lead`, `begin_checkout`
- [ ] Stripe Payment Link price = **$9.99** for timed sim
- [ ] Test lead URL: intro → lead form → purchase (`utm_content=lead-free-sim`)
- [ ] Confirm ads do **not** point to `secplus-home.html` or `ENCOR_Training_Portal.html`
- [ ] Search terms report reviewed at day 7 and day 14

---

## Related notes

- Strategy: [[ccnp-encor-google-ads|ENCOR Google Ads]]
- Landing audit: [[../../06-website-optimization/pages/ccnp-home|ccnp-home.md]]
- Keywords: [[../../07-keywords/landing-maps/ccnp-encor-portal|ENCOR landing map]]
- Cisco foundation: [[../../01-strategy/cisco-certifications-exam-prep-foundation|cisco-certifications-exam-prep-foundation.md]]
- CCNA parallel: [[../ccna/ccna-portal-google-ads-export|CCNA Google Ads export]]

## Decisions log

| Date | Note |
|------|------|
| 2026-05-31 | Verified vs prod: lead sim 45 min; sim **$9.99**; homepage samples **2 MCQ** — [[../../06-website-optimization/ad-site-verification-2026-05-31|verification]] |
| 2026-05-31 | Initial paste-ready export |

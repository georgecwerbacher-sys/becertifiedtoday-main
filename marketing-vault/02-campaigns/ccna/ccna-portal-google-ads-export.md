---
type: campaign-export
channel: google-ads
product: ccna-200-301
status: active
parent: ccna-portal-google-ads
utm_campaign: ccna_portal
created: 2026-05-31
---

# CCNA Google Ads — paste-ready export

Copy blocks below into Google Ads (Search campaign) or Google Ads Editor. Parent strategy: [[ccna-portal-google-ads|CCNA Google Ads]] · Landing: [[../../06-website-optimization/pages/ccna-home|ccna-home.html]].

**Policy:** Exam prep / practice only — not Cisco endorsement, not “guaranteed pass,” not clearance or DoD qualification.

---

## Campaign shell (create once)

| Setting              | Value                                                                                                                     |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Campaign name        | `CCNA 200-301 · Exam prep · becertifiedtoday`                                                                             |
| Campaign type        | Search                                                                                                                    |
| Networks             | Search only (uncheck Search partners until baseline CPA)                                                                  |
| Locations            | United States (add geo ad groups below for defense metros)                                                                |
| Language             | English                                                                                                                   |
| Bidding              | Maximize conversions (after `ccna_free_assessment_click` + `begin_checkout` imported) — or **Maximize clicks** with CPC cap for week 1 |
| Daily budget (start) | $15–25/day total campaign; 60% free assessment group / 40% sim purchase                                                   |
| UTM campaign         | `ccna_portal`                                                                                                             |

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
"ine ccna"
"cisco netacad"
"jobs"
"salary"
"ccnp encor"
"ccie"
"comptia security+"
"packet tracer course"
"gns3 tutorial"
```

---

## Ad group 1 — `ccna_free_assessment` (launch first)

**Intent:** Practice test / mock exam → free 35-min assessment + domain scorecard.

**Final URL (recommended — home + pinned headline):**

```
https://becertifiedtoday.com/ccna-home.html?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=hl-free-practice
```

**Alternate (direct assessment — A/B test):**

```
https://becertifiedtoday.com/CCNA_Sim_EXAM/free-assessment.html?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=free-assessment
```

**Display path (optional):** `CCNA` / `Free-Assessment`

**RSA — Headlines** (≤30 chars; pin H1–H3 in UI)

```
Free CCNA Practice Test
Start Free CCNA Assessment
35-Min Practice + Scorecard
CCNA 200-301 Sample Exam
12 MCQ + D&D + CLI Lab
Exam Prep — Not a Course
No GNS3 — Browser Prep
Domain Scorecard Included
No PDFs — Browser Prep
Free CCNA Mock Exam
Cisco CCNA 200-301 Prep
Realistic Timed Sample
Try Before You Buy
Be Certified Today
```

**RSA — Descriptions** (≤90 chars)

```
Free 35-min CCNA 200-301 assessment: 12 MCQ, 4 drag-and-drop, 1 VLAN CLI lab. Domain scorecard when you finish.
Realistic browser practice before test day. Full 120-min sim when you are ready. No GNS3 or PDFs required.
Exam preparation—not a training course. Verified explanations. No dumps or third-party lab software.
One free attempt per browser. Start the assessment from CCNA home—no email or membership required.
```

**Pin suggestion:** Headline 1 → `Free CCNA Practice Test` · Headline 2 → `Start Free CCNA Assessment` · Headline 3 → `35-Min Practice + Scorecard`

### Keywords — `ccna_free_assessment`

Paste into ad group keyword box. **Phrase** = `"quotes"` · **Exact** = `[square brackets]`.

```
"ccna practice test"
"ccna 200-301 practice test"
[ccna 200-301 practice test]
"ccna practice exam"
"ccna 200-301 practice exam"
[ccna 200-301 practice exam]
"ccna mock exam"
"free ccna practice"
"free ccna practice test"
"free ccna exam"
"cisco ccna practice test"
[cisco ccna practice test]
"ccna exam prep"
"ccna 200-301 prep"
"ccna practice questions"
"ccna 200-301 practice questions"
```

**Ad group negatives (Phrase):**

```
"free course"
"bootcamp"
"dump"
"pdf"
"udemy"
"cbt nuggets"
"ine ccna"
"netacad"
"jobs"
"salary"
```

**Primary conversion:** `ccna_free_assessment_click` · **Secondary:** `begin_checkout` (upsell)

---

## Ad group 2 — `ccna_sim_purchase`

**Intent:** Timed simulation / exam sim → $4.99 one-time 120-minute test.

**Final URL:**

```
https://becertifiedtoday.com/ccna-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=sim-purchase
```

**Display path:** `CCNA` / `Timed-Sim`

**RSA — Headlines**

```
120-Min CCNA Exam Sim
CCNA 200-301 Timed Test
Timed Sim — $4.99
Study Scorecard by Domain
50 MCQ + D&D + CLI Lab
120 Minutes Like Test Day
No GNS3 — Browser Exam Prep
Cisco CCNA Simulation
Exam Prep — Not a Course
Full Dry Run Before Test Day
Domain Breakdown at End
One Attempt · No Subscription
Be Certified Today
Try Free Assessment on Site
```

**RSA — Descriptions**

```
One 120-minute CCNA 200-301 session: 50 multiple-choice, drag-and-drop, and CLI lab items. $4.99 one attempt.
Finish with a study scorecard by CCNA domain. Same clock and mix as test day—not a video course.
Exam-realistic browser prep. Verified explanations. No PDF dumps or GNS3 installs required.
Free 35-min assessment on the same page if you want to try before you buy the full sim.
```

**Pin suggestion:** H1 → `120-Min CCNA Exam Sim` · H2 → `Timed Sim — $4.99` · H3 → `Study Scorecard by Domain`

### Keywords — `ccna_sim_purchase`

```
"ccna exam simulation"
[ccna exam simulation]
"ccna timed exam"
"ccna timed test"
"ccna exam simulation online"
"cisco ccna simulation"
"ccna practice simulation"
"ccna mock exam timed"
"ccna full practice exam"
"pass ccna first try"
"ccna retake prep"
"ccna 200-301 simulation"
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

**Primary conversion:** `begin_checkout` (item `ccna_timed_simulation`)

---

## Ad group 3 — `ccna_portal_access`

**Intent:** Multi-day library access (10-day $9.99 · 30-day $19.99) — timed sim included.

**Final URL:**

```
https://becertifiedtoday.com/ccna-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=portal-access
```

**Display path:** `CCNA` / `Portal-Access`

**RSA — Headlines**

```
CCNA Full Question Bank
10-Day CCNA Access
30-Day CCNA Access
Portal + Timed Sim Included
CCNA Exam Prep Portal
All Six CCNA Domains
D&D & CLI Lab Practice
No Subscription — One-Time
$9.99 / 10 Days · From
$19.99 / 30 Days · From
Browser-Only Exam Prep
Verified 200-301 Explanations
Exam Prep — Not a Course
Be Certified Today
Free Assessment on Same Page
```

**RSA — Descriptions**

```
Full CCNA 200-301 library: question banks, drag-and-drop, CLI labs, portal modes, and timed exam simulation in your browser.
Choose 10-day ($9.99) or 30-day ($19.99) access. One-time purchase—no recurring membership.
Exam prep aligned to Cisco objectives—not PDF dumps or instructor-led courses.
120-minute timed simulation included with portal passes. Try free assessment before you checkout.
```

**Pin suggestion:** H1 → `CCNA Full Question Bank` · H2 → `Portal + Timed Sim Included`

### Keywords — `ccna_portal_access`

```
"ccna study guide practice"
"ccna 200-301 study prep online"
"ccna question bank"
"ccna 200-301 question bank"
"cisco ccna practice portal"
"ccna practice test online"
"ccna 200-301 online practice"
"ccna exam prep online"
"ccna 30 day study"
"ccna cram practice"
```

**Primary conversion:** `begin_checkout` (`ccna_portal_10d` or `ccna_portal_30d`)

---

## Ad group 4 — `ccna_labs_pbq` (optional mid-funnel)

**Intent:** Drag-and-drop / CLI lab / PBQ-style practice → home page samples → portal/sim purchase.

**Final URL:**

```
https://becertifiedtoday.com/ccna-home.html?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=labs-pbq
```

**Display path:** `CCNA` / `Labs-PBQ`

**RSA — Headlines**

```
CCNA Drag-Drop Practice
CCNA CLI Lab Simulation
CCNA PBQ-Style Items
VLAN Lab — In Browser
No GNS3 Required
Interactive CCNA Labs
Browser Lab — No Install
Exam Prep — Not a Course
Try Free Assessment
Full Portal When Ready
Cisco CCNA 200-301
Verified Explanations
Be Certified Today
Free Sample Questions
```

**RSA — Descriptions**

```
Interactive CCNA 200-301 practice: drag-and-drop, CLI VLAN lab, and exhibit-based items in your browser.
Exam prep only—not a course. No GNS3, Packet Tracer installs, or PDF dumps. Upsell to portal or timed sim on site.
Free 35-min assessment and sample questions available. Full 120-minute simulation on CCNA home.
Practice performance-based items before test day. Verified explanations aligned to Cisco objectives.
```

### Keywords — `ccna_labs_pbq`

```
"ccna drag and drop practice"
[ccna drag and drop practice]
"ccna cli lab practice"
"ccna lab simulation"
"ccna vlan lab practice"
"ccna performance based questions"
"ccna drop down question"
"ccna simulation lab online"
"ccna practice lab browser"
"ccna without gns3"
```

---

## Ad group 5 — `ccna_federal_dc` (geo template)

Duplicate ad group per metro; change **Locations** targeting and `utm_content` only.

| Ad group name | Locations (target) | utm_content |
|---------------|-------------------|-------------|
| `ccna_federal_dc` | DC + Arlington + Alexandria + Fairfax + Bethesda + Silver Spring | `federal-dc` |
| `ccna_federal_cos` | Colorado Springs | `federal-cos` |
| `ccna_federal_satx` | San Antonio | `federal-satx` |
| `ccna_federal_norfolk` | Norfolk + Virginia Beach + Chesapeake | `federal-norfolk` |

**Final URL (example DC):**

```
https://becertifiedtoday.com/ccna-home.html#exam-audience?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=federal-dc
```

Use `#purchase` variant for purchase-intent federal keywords.

**RSA — Headlines**

```
CCNA 200-301 Exam Prep
DoD IT Role Exam Prep
Browser CCNA Practice
Free CCNA Assessment
8140 Baseline Exam Prep
Defense Contractor Cert Prep
No GNS3 — Browser Labs
Federal Workforce Exam Prep
Timed Sim + Scorecard
Exam Prep — Not a Course
Practice Before Test Day
Be Certified Today
35-Min Free Assessment
Verified 200-301 Explanations
Study From Duty Station
```

**RSA — Descriptions**

```
CCNA 200-301 exam prep for federal, DoD, and contractor IT roles. Browser-only—study on your schedule.
Free 35-min assessment + domain scorecard. Full 120-min simulation and portal access when ready.
Exam preparation only—we do not process clearance or official DoD qualification. Confirm reqs with your org.
Not a bootcamp or PDF dump. Realistic practice tests, drag-and-drop, and CLI labs in your browser.
```

**Compliance:** Do not claim DoD or Cisco endorsement. See [[../../01-strategy/cisco-certifications-exam-prep-foundation|Cisco foundation]] disclaimer.

### Keywords — federal (Phrase / Exact)

```
"ccna federal job"
"ccna defense contractor"
"ccna government job"
"cisco ccna exam prep contractor"
"ccna dod"
"ccna 8140"
"ccna military"
"cisco ccna federal"
```

**Note:** “clearance prep” may attract wrong intent — monitor search terms; add negatives if needed.

---

## Headline pinning — `utm_content=hl-*`

For non-default hero copy, append pinned suffix per `scripts/ccna-google-ads-headline-suffixes.txt`:

| Pinned ad headline | utm_content |
|--------------------|-------------|
| CCNA Practice Test | `hl-practice-test` |
| CCNA 200-301 Prep | `hl-200-301-prep` |
| Free CCNA Practice | `hl-free-practice` |
| CCNA Mock Exam | `hl-mock-exam` |
| CCNA Exam Question and Answers | `hl-exam-qna` |
| Cisco CCNA Prep | `hl-cisco-prep` |

Full list in suffixes file. **Use `utm_campaign=ccna_portal`** (not legacy `ccna-practice-test`).

---

## Sitelink extensions (campaign-level)

| Link text | URL |
|-----------|-----|
| Free CCNA assessment | `…/ccna-home.html?utm_content=sitelink-free-assessment` |
| 120-minute timed sim | `…/ccna-home.html#purchase&utm_content=sitelink-sim` |
| Sample questions | `https://becertifiedtoday.com/sample?track=ccna-questions&utm_content=sitelink-sample` |
| Pricing & access | `…/ccna-home.html#purchase&utm_content=sitelink-pricing` |

Use full URLs with `utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal` on each.

---

## Callout extensions (campaign-level)

```
Free 35-Min Assessment
Domain Study Scorecard
Browser-Only — No PDFs
No GNS3 Required
Exam Prep — Not a Course
Verified Explanations
One-Time Pricing
No Subscription
200-301 Objectives Aligned
D&D & CLI Lab Items
```

---

## Structured snippet extensions

**Types:** Courses → `Domain 1 Network Fundamentals` · `Domain 2 Network Access` · `Domain 3 IP Connectivity` · `Domain 4 IP Services` · `Domain 5 Security` · `Domain 6 Automation`

**Types:** Types → `Timed simulation` · `Practice questions` · `Drag-and-drop items` · `CLI lab simulations`

---

## Products & services to advertise (Google campaign setup)

Paste each row into **Add products or services**. Names ≤120 chars; descriptions target **≤300 chars** (adjust if your UI allows more). All are **exam prep**, not courses.

| # | Product / service name | Landing URL |
|---|------------------------|-------------|
| 1 | Free CCNA 200-301 Practice Assessment | `https://becertifiedtoday.com/CCNA_Sim_EXAM/free-assessment.html` |
| 2 | CCNA 200-301 120-Minute Timed Exam Simulation | `https://becertifiedtoday.com/ccna-home.html#purchase` |
| 3 | CCNA 200-301 10-Day All-Access Practice Portal | `https://becertifiedtoday.com/ccna-home.html#purchase` |
| 4 | CCNA 200-301 30-Day All-Access Practice Portal | `https://becertifiedtoday.com/ccna-home.html#purchase` |
| 5 | Free CCNA 200-301 Sample Practice Questions | `https://becertifiedtoday.com/sample?track=ccna-questions` |

### Descriptions (copy under each name)

**1 — Free practice assessment**

```
Free 35-minute CCNA 200-301 exam prep assessment in your browser: 12 multiple-choice questions (two per domain), four drag-and-drop items, and one VLAN CLI lab simulation. Includes a domain and objective scorecard when you finish. One free attempt per browser. Not a training course.
```

**2 — 120-minute timed exam simulation ($4.99)**

```
One full CCNA 200-301 timed practice exam: 120 minutes with 50 multiple-choice, drag-and-drop, and CLI lab items in one shuffled session. Ends with a study scorecard by CCNA domain. $4.99 one attempt; no subscription. Browser-only exam prep—no GNS3 required.
```

**3 — 10-day all-access portal ($9.99)**

```
10 days of full Cisco CCNA 200-301 exam prep in your browser: domain question banks, drag-and-drop items, CLI labs, portal study modes, and the 120-minute timed exam simulation. Verified explanations aligned to objectives. $9.99 one-time; no recurring membership.
```

**4 — 30-day all-access portal ($19.99)**

```
30 days of full CCNA 200-301 exam preparation: question banks, drag-and-drop and CLI lab items, review modes, progress tracking, and the 120-minute timed simulation. Browser-only—no PDFs or GNS3. $19.99 one-time access; no subscription.
```

**5 — Free sample practice questions**

```
Try shuffled CCNA 200-301 multiple-choice practice questions with instant feedback and verified explanations. No checkout required. Interactive browser exam prep, not PDF dumps. Home link returns to the CCNA landing page.
```

### If Google asks for a single category

Use: **Education & training → Test preparation** or **Educational software / Online education** (pick the closest match; avoid “Training course” if a separate **Exam preparation** option exists).

### Priority order when the UI limits how many you can add

1. Free practice assessment  
2. 120-minute timed exam simulation  
3. 30-day all-access portal  
4. 10-day all-access portal  
5. Free sample questions  

---

## Conversion actions (link in Google Ads ↔ GA4)

| Action | Source | Priority |
|--------|--------|----------|
| `ccna_free_assessment_click` | GA4 import | Primary for free assessment ad group |
| `begin_checkout` | GA4 import | Primary for sim / portal groups |
| Purchase (Stripe) | Optional offline / enhanced | Secondary |

---

## Launch checklist

- [ ] Campaign + 2 ad groups live: `ccna_free_assessment`, `ccna_sim_purchase`
- [ ] Final URLs match table above (UTMs + anchors)
- [ ] Campaign negatives pasted
- [ ] GA4 key events: `ccna_free_assessment_click`, `begin_checkout`
- [ ] Stripe Payment Link price = **$4.99** for timed sim
- [ ] Test free URL: hero shows “Free CCNA Practice Assessment” (`utm_content=hl-free-practice`)
- [ ] Search terms report reviewed at day 7 and day 14

---

## Related notes

- Strategy: [[ccna-portal-google-ads|CCNA Google Ads]]
- Landing audit: [[../../06-website-optimization/pages/ccna-home|ccna-home.md]]
- Keywords: [[../../07-keywords/landing-maps/ccna-portal|CCNA landing map]]
- Cisco foundation: [[../../01-strategy/cisco-certifications-exam-prep-foundation|cisco-certifications-exam-prep-foundation.md]]

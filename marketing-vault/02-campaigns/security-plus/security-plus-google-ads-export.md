---
type: campaign-export
channel: google-ads
product: secplus-sy0-701
status: active
parent: security-plus-google-ads
utm_campaign: secplus_portal
created: 2026-05-30
---

# Security+ Google Ads — paste-ready export

Copy blocks below into Google Ads (Search campaign) or Google Ads Editor. Parent strategy: [[security-plus-google-ads|Security+ Google Ads]] · Lead funnel: [[security-plus-lead-magnet-ads|lead magnet ads]] · Landing: [[../../06-website-optimization/pages/comptia-sec-plus-home|comptia-sec+-home.html]].

**Policy:** Exam prep / practice only — not CompTIA endorsement, not “guaranteed pass,” not clearance or DoD qualification.

**Copy limits:** Every **RSA description** ≤90 characters · **Campaign sitelinks:** minimum **6**, each with full URL + 2 description lines ≤35 characters (see sitelink table below).

---

## PBQ library update (2026-06-08) — refresh live Ads copy

Paid portal now advertises **28 practice scenarios** on [[../../06-website-optimization/pages/comptia-sec-plus-home|comptia-sec+-home.html]] and groups labs by subject on `/COMP_TIA_SEC+/SEC+_Training_Portal.html`:

| Bucket | Count | Examples |
|--------|------:|----------|
| Chained PBQ labs | **21** | ZTA, hybrid PKI, SIEM MITRE, Ubuntu SSH IR, governance (Back/Next chain) |
| Standalone PBQs | **4** | Dark web IR, malware outbreak, secure web & OpenSSL, VPC payment |
| Hot spot | **1** | Attack identification & remediation |
| IR report exhibits | **2** | Compensation report Q3 addendum, employee credential audit |
| **Total** | **28** | Plus legacy redirects and utility pages |

**Canonical OpenSSL PBQ URL** (use in new sitelinks / `secplus_openssl_pbq`; old `simulation-secure-web-architecture-openssl.html` redirects here):

```
https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/secure-web-architecture-openssl/secure-web-architecture-openssl.html
```

**Paste priority when editing live campaign:**

1. **`secplus_portal_access`** — swap descriptions + add headlines `28 PBQ Practice Scenarios`, `21 Chain Labs + 4 Solo`
2. **Campaign callouts** — add `28 PBQ Practice Scenarios`, `21 Chained PBQ Labs`, `Subject-Grouped Portal`
3. **Product #4 (30-day portal)** — use description block below in **Products & services**
4. **`secplus_openssl_pbq`** — update Final URL to canonical OpenSSL path above
5. **Federal ad groups** — optional description line 4 swap to 28-scenario line

Lead free-sim ad group copy is **unchanged** (still 20 MCQ + 1 dark web PBQ in the 35-min sample).

---

## Campaign shell (create once)

| Setting              | Value                                                                                                                     |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Campaign name        | `SEC+ SY0-701 · Exam prep · becertifiedtoday`                                                                             |
| Campaign type        | Search                                                                                                                    |
| Networks             | Search only (uncheck Search partners until baseline CPA)                                                                  |
| Locations            | United States (add geo ad groups below for defense metros)                                                                |
| Language             | English                                                                                                                   |
| Bidding              | **Live (2026-06-03):** Maximize clicks, **max CPC $2.50** — see [[secplus-lead-free-sim-ad-group\|ad group config]] |
| Daily budget (start) | **$10.00/day** — one campaign; **`secplus_lead_free_sim` only** (pause other ad groups) |
| UTM campaign         | `secplus_portal` (PBQ group uses `secplus_openssl_pbq`)                                                                   |

### Campaign-level negative keywords (Phrase match)

**Baseline (32)** — already pasted in Ads. **Course/vendor lockdown (+24)** — add when Search terms show training/course clicks: [[../../07-keywords/negatives/secplus-course-vendor-lockdown|secplus-course-vendor-lockdown]]. **Full merged list (56):** [[../../07-keywords/negatives/google-ads-applied-2026-06-03#Merged campaign list — 56 Phrase (2026-06-03)|applied snapshot]].

```
"brain dump"
"boot camp"
"bootcamp"
"ccna"
"certification course"
"certification training"
"certmaster"
"certmaster learn"
"cissp"
"classroom training"
"comptia a+"
"comptia learn"
"comptia training"
"course"
"coursera"
"cyberkraft"
"cybersecurity training"
"cybrary"
"cysa"
"dump"
"dion"
"dumps"
"exam cram"
"exam dump"
"exam questions and answers"
"flash cards"
"free course"
"free training"
"guaranteed pass"
"instructor"
"instructor led"
"it training"
"jobs"
"learn comptia"
"linkedin learning"
"mike meyers"
"network+"
"on demand"
"online course"
"online training"
"pass4sure"
"pdf"
"pdf download"
"pluralsight"
"professor messer"
"real exam questions"
"salary"
"security training"
"security+ tutorial"
"self paced"
"skillsoft"
"study guide"
"sy0-601"
"sybex"
"total seminars"
"training"
"training course"
"training program"
"udemy"
"video course"
"virtual training"
"webinar"
```

---

## Ad group 1 — `secplus_lead_free_sim` (launch first)

**Intent:** Practice test / mock exam → free 35-min timed sim + scorecard.

**Final URL:**

```
https://becertifiedtoday.com/comptia-sec+-home.html#secplus-lead-capture?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=lead-free-sim
```

**Display path (optional):** `Security+` / `Free-Sim`

**RSA — Headlines** (≤30 chars; pin H1–H3 in UI)

```
Free Security+ Timed Sim
Start Free SY0-701 Sample
35-Min Practice + Scorecard
SY0-701 Sample Exam
20 Questions + PBQ Sim
Exam Prep — Not a Course
No PDFs — Browser Prep
Domain Scorecard Included
Back & Mark for Review
Free Mock Exam — SY0-701
CompTIA Security+ Practice
Realistic Timed Sample
No Email To Start
Try Before You Buy
28 PBQs in Full Library
Be Certified Today
```

**RSA — Descriptions** (≤90 chars)

```
Free 35-min SY0-701 sample: 20 MCQ + PBQ. Domain scorecard. No email to start.
Timed practice before test day. Back & mark for review. 30-day access when ready.
Exam prep—not a course. Verified explanations. No PDF dumps. Browser-only.
Free sample exam in your browser. One attempt per device. Scorecard at finish.
```

**Pin suggestion:** Headline 1 → `Free Security+ Timed Sim` · Headline 2 → `Start Free SY0-701 Sample` · Headline 3 → `35-Min Practice + Scorecard`

**Primary conversion in Ads:** GA4 **`generate_lead`** (fires when user taps **Start free timed simulation** — see [[../../05-playbooks/secplus-free-sim-funnel|free sim funnel]]).

### Keywords — `secplus_lead_free_sim`

Paste into ad group keyword box. **Phrase** = `"quotes"` · **Exact** = `[square brackets]`.

```
"security+ practice test"
"sy0-701 practice test"
[sy0-701 practice test]
"security+ practice exam"
"sy0-701 practice exam"
[sy0-701 practice exam]
"security+ mock exam"
"sy0-701 mock exam"
"security+ timed practice test"
"comptia security+ practice test"
[comptia security+ practice test]
"security+ exam prep"
"sy0-701 exam prep"
"security+ practice questions"
"sy0-701 practice questions"
```

**Ad group negatives (Phrase):**

```
"free course"
"bootcamp"
"dump"
"pdf"
"udemy"
"coursera"
"professor messer"
"jobs"
"salary"
```

**Primary conversion:** `generate_lead` · **Secondary:** `begin_checkout` (upsell)

---

## Ad group 2 — `secplus_sim_purchase`

**Intent:** Timed simulation / exam sim → $9.99 one-time 90-minute test.

**Final URL:**

```
https://becertifiedtoday.com/comptia-sec+-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sim-purchase
```

**Display path:** `Security+` / `Timed-Sim`

**RSA — Headlines**

```
90-Min Security+ Exam Sim
SY0-701 Timed Practice Test
Timed Sim — $9.99
Study Scorecard by Domain
Back & Mark for Review
90 Questions in 90 Minutes
PBQ + MCQ — One Session
No PDFs — Browser Exam Prep
CompTIA Security+ Simulation
Exam Prep — Not a Course
Full Dry Run Before Test Day
Domain Breakdown at End
One Attempt · No Subscription
Be Certified Today
Try Free Sample on Site
```

**RSA — Descriptions** (≤90 chars)

```
One 90-min SY0-701 session: MCQ + sims + hot spots, shuffled. $9.99 one attempt.
Finish with domain scorecard. Back & mark for review like test day—not a course.
Exam-realistic mix in browser. Verified explanations. No downloads required.
Free 35-min sample on same page. Try before you buy the full 90-minute sim.
```

**Pin suggestion:** H1 → `90-Min Security+ Exam Sim` · H2 → `Timed Sim — $9.99` · H3 → `Study Scorecard by Domain`

### Keywords — `secplus_sim_purchase`

```
"security+ exam simulation"
[security+ exam simulation]
"sy0-701 exam simulation"
[sy0-701 exam simulation]
"security+ timed test"
"sy0-701 timed test"
"comptia security+ simulation"
"security+ practice simulation"
"sy0-701 practice simulation"
"security+ mock exam timed"
"security+ full practice exam"
"pass security+ first try"
"security+ retake prep"
```

**Ad group negatives (Phrase):**

```
"free"
"bootcamp"
"course"
"dump"
"pdf"
"jobs"
```

**Primary conversion:** `begin_checkout` (item `secplus_timed_simulation`)

---

## Ad group 3 — `secplus_portal_access`

**Intent:** Multi-day library access (10-day $9.99 · 30-day $19.99) — timed sim included.

**Final URL:**

```
https://becertifiedtoday.com/comptia-sec+-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=portal-access
```

**Display path:** `Security+` / `Portal-Access`

**RSA — Headlines**

```
SY0-701 Full Question Bank
10-Day Security+ Access
30-Day Security+ Access
Portal + Timed Sim Included
Security+ Exam Prep Portal
All Five SY0-701 Domains
28 PBQ Practice Scenarios
21 Chain Labs + 4 Solo
No Subscription — One-Time
$9.99 / 10 Days · From
$19.99 / 30 Days · From
Browser-Only Exam Prep
Verified SY0-701 Explanations
Exam Prep — Not a Course
Be Certified Today
Free Sample on Same Page
```

**RSA — Descriptions** (≤90 chars)

```
1000+ MCQ + 28 PBQ scenarios: 21 chain labs, 4 standalone, 1 hot spot, 2 reports.
30-day ($19.99) portal: subject-grouped sims + timed exam. One-time. No sub.
Exam prep aligned to CompTIA objectives—not PDF dumps or instructor-led courses.
Try free 35-min sample or dark web PBQ preview on home before checkout.
```

**Pin suggestion:** H1 → `SY0-701 Full Question Bank` · H2 → `Portal + Timed Sim Included`

### Keywords — `secplus_portal_access`

```
"security+ study guide practice"
"sy0-701 study prep online"
"security+ question bank"
"sy0-701 question bank"
"comptia security+ practice portal"
"security+ practice test online"
"sy0-701 online practice"
"security+ exam prep online"
"security+ 30 day study"
"security+ cram practice"
```

**Primary conversion:** `begin_checkout` (`secplus_portal_10d` or `secplus_portal_30d`)

---

## Ad group 4 — `secplus_openssl_pbq` (optional mid-funnel)

**Intent:** PBQ / OpenSSL / secure web architecture → interactive sim page → portal/sim purchase.

**Final URL:**

```
https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/secure-web-architecture-openssl/secure-web-architecture-openssl.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_openssl_pbq&utm_content=openssl-pbq
```

**Display path:** `Security+` / `OpenSSL-PBQ`

**RSA — Headlines**

```
Security+ PBQ Practice
SY0-701 PBQ Simulation
OpenSSL CSR — SY0-701 PBQ
Secure Web Architecture PBQ
WAF & TLS Practice Item
Performance-Based Practice
Browser PBQ — No Install
Exam Prep — Not a Course
Try Free Sample Questions
Full Portal When Ready
CompTIA Security+ SY0-701
Interactive Exam Prep
Verified Explanations
Be Certified Today
Free PBQ-Style Scenario
```

**RSA — Descriptions** (≤90 chars)

```
SY0-701 PBQ: secure web, WAF, PKI/TLS, OpenSSL CSR steps in your browser.
One of 28 portal scenarios—21 chain labs, 4 standalone, hot spot, 2 IR reports.
Exam prep—not a course. Deep-dive explanations. Full library on Security+ home.
Performance-based practice before test day. No PDFs or third-party lab software.
```

### Keywords — `secplus_openssl_pbq`

```
"security+ pbq practice"
[security+ pbq practice]
"sy0-701 pbq"
[sy0-701 pbq]
"security+ performance based questions"
"comptia pbq practice"
"openssl csr comptia security+"
"security+ waf practice question"
"secure web architecture security+"
"sy0-701 drop down question"
```

Page detail: [[../../06-website-optimization/pages/simulation-secure-web-architecture-openssl|openssl CTA landing note]].

---

## Ad group 5 — `secplus_federal_dc` (geo template)

Duplicate ad group per metro; change **Locations** targeting and `utm_content` only.

| Ad group name | Locations (target) | utm_content |
|---------------|-------------------|-------------|
| `secplus_federal_dc` | DC + Arlington + Alexandria + Fairfax + Bethesda + Silver Spring | `federal-dc` |
| `secplus_federal_cos` | Colorado Springs | `federal-cos` |
| `secplus_federal_satx` | San Antonio | `federal-satx` |
| `secplus_federal_norfolk` | Norfolk + Virginia Beach + Chesapeake | `federal-norfolk` |

**Final URL (example DC):**

```
https://becertifiedtoday.com/comptia-sec+-home.html#secplus-lead-capture?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=federal-dc
```

Use `#purchase` variant for purchase-intent federal keywords.

**RSA — Headlines**

```
Security+ SY0-701 Exam Prep
DoD Cyber Role Exam Prep
Browser SY0-701 Practice
Free Timed Simulation
8140 Baseline Exam Prep
Defense Contractor Cert Prep
No VM Installs — Browser
Federal Workforce Exam Prep
Timed Sim + Scorecard
Exam Prep — Not a Course
Practice Before Test Day
Be Certified Today
35-Min Free Sample Exam
Verified SY0-701 Explanations
Study From Duty Station
```

**RSA — Descriptions** (≤90 chars)

```
SY0-701 exam prep for federal, DoD, contractor cyber. Browser-only—your schedule.
Free 35-min timed sample + domain scorecard. Full 90-min sim and portal when ready.
Exam prep only. No clearance or DoD qualification processing. Confirm with org.
Not a bootcamp or PDF dump. 28 PBQ scenarios + 1000+ MCQ in your browser.
```

**Compliance:** Do not claim DoD endorsement. See [[../../01-strategy/security-plus-federal-defense-foundation|federal foundation]] disclaimer.

### Keywords — federal (Phrase / Exact)

```
"security+ dod"
"security+ 8140"
"security+ defense contractor"
"security+ federal government"
"sy0-701 dod"
"comptia security+ military"
"security+ clearance prep"
"dod cyber workforce certification"
```

**Note:** “clearance prep” may attract wrong intent — monitor search terms; add negatives if needed.

---

## Sitelink extensions (campaign-level)

Minimum **6** sitelinks per campaign. Description lines ≤35 characters each.

| #   | Link text              | Desc 1                     | Desc 2                        | Full URL                                                                                                                                                                                                 |
| --- | ---------------------- | -------------------------- | ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Free timed simulation  | 35-min SY0-701 sample exam | Email unlock, one free try    | `https://becertifiedtoday.com/comptia-sec+-home.html#secplus-lead-capture?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-free-sim`                                    |
| 2   | 90-minute timed sim    | Full SY0-701 practice exam | $9.99 one attempt, no sub     | `https://becertifiedtoday.com/comptia-sec+-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-sim`                                                     |
| 3   | Sample questions       | Two MCQ per run, free      | Instant feedback, no checkout | `https://becertifiedtoday.com/secplus-sample?track=questions&utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-sample`                                                   |
| 4   | OpenSSL PBQ simulation | Secure web & OpenSSL PBQ   | 1 of 28 portal scenarios      | `https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/secure-web-architecture-openssl/secure-web-architecture-openssl.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-openssl` |
| 5   | 30-day all-access      | Full SY0-701 question bank | $19.99 one-time, no sub       | `https://becertifiedtoday.com/comptia-sec+-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-portal-30d`                                              |
| 6   | Pricing & access       | 10-day or 30-day access    | From $9.99, no subscription   | `https://becertifiedtoday.com/comptia-sec+-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-pricing`                                                 |
|     |                        |                            |                               |                                                                                                                                                                                                          |

---

## Callout extensions (campaign-level)

```
Free 35-Min Sample Exam
Back & Mark for Review
Domain Study Scorecard
Browser-Only — No PDFs
Exam Prep — Not a Course
Verified Explanations
One-Time Pricing
No Subscription
SY0-701 Objectives Aligned
28 PBQ Practice Scenarios
21 Chained PBQ Labs
Subject-Grouped Portal
```

---

## Structured snippet extensions

**Types:** Courses → `SY0-701 Domain 1` · `Domain 2 Threats` · `Domain 3 Architecture` · `Domain 4 SecOps` · `Domain 5 Governance`

**Types:** Types → `21 chain labs` · `4 standalone PBQs` · `Hot spot` · `IR report exhibits` · `Drag-and-drop`

---

## Products & services to advertise (Google campaign setup)

Paste each row into **Add products or services**. Names ≤120 chars; descriptions target **≤300 chars** (adjust if your UI allows more). All are **exam prep**, not courses.

| # | Product / service name | Landing URL |
|---|------------------------|-------------|
| 1 | Free Security+ SY0-701 Timed Simulation Sample | `https://becertifiedtoday.com/comptia-sec+-home.html#secplus-lead-capture` |
| 2 | Security+ SY0-701 90-Minute Timed Exam Simulation | `https://becertifiedtoday.com/comptia-sec+-home.html#purchase` |
| 3 | Security+ SY0-701 10-Day All-Access Practice Portal | `https://becertifiedtoday.com/comptia-sec+-home.html#purchase` |
| 4 | Security+ SY0-701 30-Day All-Access Practice Portal | `https://becertifiedtoday.com/comptia-sec+-home.html#purchase` |
| 5 | Free Security+ SY0-701 Sample Practice Questions | `https://becertifiedtoday.com/secplus-sample?track=questions` |
| 6 | Security+ SY0-701 PBQ — Secure Web & OpenSSL Simulation | `https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/secure-web-architecture-openssl/secure-web-architecture-openssl.html` |

### Descriptions (copy under each name)

**1 — Free timed simulation sample**

```
Free 35-minute SY0-701 exam prep sample in your browser: 20 multiple-choice questions (four per domain) plus a performance-based dark web scenario. Includes back navigation, mark-for-review, and a domain scorecard when you finish. Email unlock; one free attempt per browser. Not a training course.
```

**2 — 90-minute timed exam simulation ($9.99)**

```
One full SY0-701 timed practice exam: up to 90 minutes with multiple-choice, simulation, and hot-spot items in one shuffled session. Back and mark-for-review like test day. Ends with a study scorecard by Security+ domain. $9.99 one attempt; no subscription. Browser-only exam prep.
```

**3 — 10-day all-access portal ($9.99)**

```
10 days of full CompTIA Security+ SY0-701 exam prep in your browser: domain question banks, performance-based drag-and-drop items, portal study modes, and the 90-minute timed exam simulation. Verified explanations aligned to objectives. $9.99 one-time; no recurring membership.
```

**4 — 30-day all-access portal ($19.99)**

```
30 days of full SY0-701 exam preparation: 1000+ question banks plus 28 PBQ practice scenarios (21 chained labs, 4 standalone simulations, 1 hot spot, and 2 IR report exhibits), subject-grouped in the practice portal, adaptive review, and the 90-minute timed simulation. Browser-only—no PDFs or third-party apps. $19.99 one-time access; no subscription.
```

**5 — Free sample practice questions**

```
Try two shuffled SY0-701 multiple-choice practice questions per run—with instant feedback and verified explanations. No checkout or email required. Interactive browser exam prep, not PDF dumps. Home link returns to the Security+ landing page; finish opens upsell to the free 35-minute timed simulation.
```

**6 — PBQ: secure web architecture & OpenSSL**

```
Free interactive SY0-701 performance-based practice: secure web architecture, WAF, PKI/TLS, and OpenSSL CSR steps in the browser. One of 28 portal scenarios (21 chain labs, 4 standalone, 1 hot spot, 2 IR reports). Exam prep with deep-dive explanations. Upgrade to the full portal on the Security+ home page when ready.
```

### If Google asks for a single category

Use: **Education & training → Test preparation** or **Educational software / Online education** (pick the closest match; avoid “Training course” if a separate **Exam preparation** option exists).

### Priority order when the UI limits how many you can add

1. Free timed simulation sample (lead magnet)  
2. 90-minute timed exam simulation  
3. 30-day all-access portal  
4. 10-day all-access portal  
5. Free sample questions  
6. PBQ OpenSSL simulation  

---

## Conversion actions (link in Google Ads ↔ GA4)

| Action | Source | Priority |
|--------|--------|----------|
| `generate_lead` | GA4 import | Primary for lead ad group |
| `begin_checkout` | GA4 import | Primary for sim / portal groups |
| Purchase (Stripe) | Optional offline / enhanced | Secondary |

---

## Launch checklist

- [ ] Bidding verified in UI: [[../../05-playbooks/google-ads-bidding-verification|google-ads-bidding-verification]]
- [ ] No coupon in RSAs at launch — [[../../01-strategy/promotions-and-coupons|promotions & coupons]]
- [ ] Campaign + 2 ad groups live: `secplus_lead_free_sim`, `secplus_sim_purchase`
- [ ] All RSA descriptions ≤90 characters; 6 sitelinks with URLs + 2 short descriptions each
- [ ] Final URLs match table above (hash + UTMs)
- [ ] Campaign negatives pasted
- [ ] GA4 key events: `generate_lead`, `begin_checkout`
- [ ] Stripe Payment Link price = **$9.99** for timed sim
- [ ] Test lead URL: layout shows intro → lead form → purchase (`utm_content=lead-free-sim`)
- [ ] Search terms report reviewed at day 7 and day 14

---

## Decisions log

| Date | Note |
|------|------|
| 2026-06-08 | PBQ library refresh: **28 scenarios** (21 chain + 4 standalone + 1 hot spot + 2 reports); portal subject cards; canonical OpenSSL URL under `PBQ_Production/` |
| 2026-05-31 | RSA descriptions trimmed to ≤90 chars; sitelinks expanded to 6 with Desc 1/2 + full URLs |
| 2026-05-31 | Verified vs prod: homepage sample = 2 MCQ; lead sim 35 min / 20 MCQ + PBQ unchanged — see [[../../06-website-optimization/ad-site-verification-2026-05-31|ad-site verification]] |
| 2026-05-30 | Initial paste-ready export; pricing $9.99 sim; free sim 35 min / 21 items |

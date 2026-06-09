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

**Copy limits:** Every **RSA description** ≤90 characters · **Campaign sitelinks:** minimum **6**, each with full URL + 2 description lines ≤35 characters (see sitelink table below).

---

## Campaign shell (create once)

| Setting              | Value                                                                                                                                  |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Campaign name        | `CCNA 200-301 · Exam prep · becertifiedtoday`                                                                                          |
| Campaign type        | Search                                                                                                                                 |
| Networks             | Search only (uncheck Search partners until baseline CPA)                                                                               |
| Locations            | United States (add geo ad groups below for defense metros)                                                                             |
| Language             | English                                                                                                                                |
| Bidding              | **Start:** Maximize clicks, **max CPC $2.75**. See [[../../01-strategy/google-ads-bidding-strategy\|bidding strategy]] — split + Target IS when budget **≥ $20/day** |
| Daily budget (start) | **$10.00/day** — one campaign; enable **`ccna_portal_10d`** only first; 2 Exact + 7 Phrase keywords |
| UTM campaign         | `ccna_portal`                                                                                                                          |

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

## Ad group 1 — `ccna_portal_10d` (10-day $9.99 primary CTA — launch first)

**Intent:** Multi-day library access — **10-day $9.99** as the only primary checkout CTA on the landing page.

**Live config:** `scripts/ccna-portal-10d-google-ads.md`

**Final URL:**

```
https://becertifiedtoday.com/ccna-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=portal-10d
```

**Display path:** `CCNA` / `10-Day-Access`

**RSA — Headlines** (canonical list: `scripts/ccna-portal-10d-google-ads.md` — 15 unique, page-keyword aligned)

```
CCNA 200-301 Practice Test
CCNA 200-301 Exam Prep
$9.99 for 10-Day Access
CCNA Practice Questions
Cisco CCNA Practice Test
CCNA Question Bank Online
Practice Tests & Simulation
700+ Questions · v1.1 2026
Drag-Drop + CLI Lab Prep
Browser CCNA Exam Prep
Timed CCNA Simulation
Latest 200-301 Questions
No PDFs — Interactive Prep
10-Day Full Library Access
Be Certified Today
```

**RSA — Descriptions** (≤90 chars)

```
CCNA 200-301 practice test bank: 700+ questions, v1.1 aligned. Labs & D&D included.
$9.99 for 10-day access. Cisco CCNA exam prep—not a course. No PDFs or GNS3.
CCNA practice questions with verified explanations. Timed simulation + portal modes.
Try free CCNA samples first. Unlock 10-day question bank access at checkout.
```

**Pin suggestion:** H1 → `CCNA 200-301 Practice Test` · H2 → `$9.99 for 10-Day Access` · H3 → `CCNA 200-301 Exam Prep`

### Keywords — `ccna_portal_10d`

```
"ccna exam prep online"
"ccna practice test online"
"ccna 200-301 prep"
"ccna question bank"
[ccna question bank]
"ccna 200-301 question bank"
[ccna 200-301 question bank]
"cisco ccna practice portal"
"ccna study prep online"
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

**Primary conversion:** `begin_checkout` (`ccna_portal_10d`)

---

## Ad group 2 — `ccna_sim_purchase` (optional — paused at launch)

**Intent:** Timed simulation / exam sim → $9.99 one-time 120-minute test.

**Final URL:**

```
https://becertifiedtoday.com/ccna-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=sim-purchase
```

**Display path:** `CCNA` / `Timed-Sim`

**RSA — Headlines**

```
120-Min CCNA Exam Sim
CCNA 200-301 Timed Test
Timed Sim — $9.99
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
Try Free Sample Questions
```

**RSA — Descriptions** (≤90 chars)

```
One 120-min CCNA session: 50 MCQ, D&D, and CLI lab items. $9.99 one attempt.
Finish with domain scorecard. Same clock and item mix as test day—not a course.
Browser exam prep. Verified explanations. No PDF dumps or GNS3 installs.
Free sample questions on same page. Try before you buy the full sim.
```

**Pin suggestion:** H1 → `120-Min CCNA Exam Sim` · H2 → `Timed Sim — $9.99` · H3 → `Study Scorecard by Domain`

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

## Ad group 3 — `ccna_portal_access` (optional — dual-tier)

**Paused by default.** Use only if testing 10-day + 30-day side-by-side on `#purchase` without `portal-10d` UTM.

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
$9.99 / 10 Days · From
$19.99 / 30 Days · From
No Subscription — One-Time
Browser-Only Exam Prep
Be Certified Today
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
Try Free Sample Questions
Full Portal When Ready
Cisco CCNA 200-301
Verified Explanations
Be Certified Today
Free Sample Questions
```

**RSA — Descriptions** (≤90 chars)

```
CCNA 200-301 browser practice: drag-and-drop, VLAN CLI lab, exhibit items. No GNS3.
Exam prep—not a course. No GNS3, Packet Tracer, or PDF dumps. Portal & timed sim.
Free sample questions on CCNA home. Full portal when ready.
Performance-based CCNA practice before test day. Verified explanations, Cisco objectives.
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
Free Sample Questions
8140 Baseline Exam Prep
Defense Contractor Cert Prep
No GNS3 — Browser Labs
Federal Workforce Exam Prep
Timed Sim + Scorecard
Exam Prep — Not a Course
Practice Before Test Day
Be Certified Today
Verified 200-301 Explanations
Study From Duty Station
```

**RSA — Descriptions** (≤90 chars)

```
CCNA exam prep for federal, DoD, contractor IT. Browser-only—study on schedule.
Free sample questions + 10-day portal access when ready. Timed sim included.
Exam prep only. No clearance or DoD qualification processing. Confirm with org.
Not a bootcamp or PDF dump. Practice tests, D&D, and CLI labs in your browser.
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

Minimum **6** sitelinks per campaign. Description lines ≤35 characters each.

| #   | Link text             | Desc 1                      | Desc 2                        | Full URL                                                                                                                                                |
| --- | --------------------- | --------------------------- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | 10-Day Access · $9.99 | Full v1.1 question bank     | $9.99 one-time, no sub        | `https://becertifiedtoday.com/ccna-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=portal-10d` |
| 2   | 120-minute timed sim  | Full 200-301 practice exam  | $9.99 one attempt, no sub     | `https://becertifiedtoday.com/ccna-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=sitelink-sim`               |
| 3   | Sample questions      | Two MCQ per run, free       | Instant feedback, no checkout | `https://becertifiedtoday.com/sample?track=ccna-questions&utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=sitelink-sample`        |
| 4   | Sample drag-and-drop  | CCNA D&D in your browser    | Free practice, no email       | `https://becertifiedtoday.com/sample?track=ccna-dnd&utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=sitelink-dnd`                 |
| 5   | VLAN CLI lab sample   | Interactive VLAN lab sample | Browser-only, no GNS3         | `https://becertifiedtoday.com/sample?track=ccna-vlan&utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=sitelink-lab`                |
| 6   | Pricing & access      | 10-day or 30-day access     | From $9.99, no subscription   | `https://becertifiedtoday.com/ccna-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=sitelink-pricing`           |

---

## Callout extensions (campaign-level)

```
700+ Practice Questions
10-Day Access From $9.99
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
| 1 | CCNA 200-301 10-Day All-Access Practice Portal | `https://becertifiedtoday.com/ccna-home.html#purchase` |
| 2 | CCNA 200-301 30-Day All-Access Practice Portal | `https://becertifiedtoday.com/ccna-home.html#purchase` |
| 3 | Free CCNA 200-301 Sample Practice Questions | `https://becertifiedtoday.com/sample?track=ccna-questions` |
| 4 | Free CCNA 200-301 Sample Drag-and-Drop Practice | `https://becertifiedtoday.com/sample?track=ccna-dnd` |
| 5 | Free CCNA 200-301 Sample VLAN CLI Lab | `https://becertifiedtoday.com/sample?track=ccna-vlan` |

### Descriptions (copy under each name — aligned to `ccna-home.html`)

**1 — 10-day all-access portal ($9.99)**

```
10 days of full Cisco CCNA 200-301 exam prep in your browser: domain question banks, drag-and-drop items, CLI labs, portal study modes, and the 120-minute timed exam simulation. Verified explanations aligned to objectives. $9.99 one-time; no recurring membership.
```

**2 — 30-day all-access portal ($19.99)**

```
30 days of full CCNA 200-301 exam preparation: question banks, drag-and-drop and CLI lab items, review modes, progress tracking, and the 120-minute timed simulation. Browser-only—no PDFs or GNS3. $19.99 one-time access; no subscription.
```

**3 — Free sample practice questions**

```
Try shuffled CCNA 200-301 multiple-choice practice questions—with instant feedback and verified explanations. No checkout required. Interactive browser exam prep, not PDF dumps.
```

**4 — Free sample drag-and-drop**

```
Four performance-style CCNA drag-and-drop items in your browser, shuffled each run. Touch-friendly on phone and tablet. No checkout. Exam prep aligned to 200-301 objectives.
```

**5 — Free sample VLAN CLI lab**

```
Dual-switch VLAN CLI simulation in your browser: create VLANs, assign ports, and save. No GNS3 or Packet Tracer install. Free preview on ccna-home.html.
```

### If Google asks for a single category

Use: **Education & training → Test preparation** or **Educational software / Online education** (pick the closest match; avoid “Training course” if a separate **Exam preparation** option exists).

### Priority order when the UI limits how many you can add

1. 10-day all-access portal (`ccna_portal_10d` primary)  
2. 30-day all-access portal  
3. Free sample practice questions  
4. Free sample drag-and-drop  
5. Free sample VLAN CLI lab  

---

## Conversion actions (link in Google Ads ↔ GA4)

| Action | Source | Priority |
|--------|--------|----------|
| `begin_checkout` | GA4 import | Primary for portal / sim groups |
| Purchase (Stripe) | Optional offline / enhanced | Secondary |

---

## Launch checklist

- [ ] **Enabled:** `ccna_portal_10d` only · **Paused:** `ccna_sim_purchase`, `ccna_portal_access`, `ccna_labs_pbq`, `ccna_federal_dc` (and geo copies)
- [ ] All RSA descriptions ≤90 characters; 6 sitelinks with URLs + 2 short descriptions each
- [ ] Final URLs match table above (hash + UTMs)
- [ ] Campaign negatives pasted
- [ ] GA4 key event: `begin_checkout` (primary)
- [ ] Stripe Payment Link price = **$9.99** for portal 10d
- [ ] Test: open Final URL → only **Get 10-day access · $9.99** above the fold → click → `begin_checkout` in GA4 Realtime
- [ ] Search terms report reviewed at day 7 and day 14

---

## Related notes

- Strategy: [[ccna-portal-google-ads|CCNA Google Ads]]
- Landing audit: [[../../06-website-optimization/pages/ccna-home|ccna-home.md]]
- Keywords: [[../../07-keywords/landing-maps/ccna-portal|CCNA landing map]]
- Cisco foundation: [[../../01-strategy/cisco-certifications-exam-prep-foundation|cisco-certifications-exam-prep-foundation.md]]
- Ad vs site verification: [[../../06-website-optimization/ad-site-verification-2026-05-31|2026-05-31 verification]]

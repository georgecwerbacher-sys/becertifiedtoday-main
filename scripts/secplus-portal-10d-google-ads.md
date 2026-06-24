# CompTIA Security+ Google Ads

> **DEPRECATED — do not use for new setup.**  
> **Source of truth:** `marketing-research/Sec+ Campaign/` — start at `README.md`, build steps in `Sec+ Notes.md`.  
> This file described the retired **$9.99 / 10-day** ad group (`secplus_portal_10d`). Live campaign is **`Security+ PBQ Practice`** only — **30-day · $19.99**. See [[Sec+ RSA Copy]] and [[Sec+ Notes#Remove 10-day from live Google Ads]].

~~Paste-ready setup for Google Ads UI. Landing: `public/comptia-sec+-home.html` with `utm_content=portal-10d` shows **$9.99 / 10-day** as the only primary purchase CTA.~~

---

## Campaign shell

| Setting | Value |
|---------|--------|
| Campaign name | `Security+ SY0-701 · Exam prep · becertifiedtoday` |
| Type | Search (Search partners off until baseline) |
| Daily budget | $20.00/day |
| Bidding | Maximize clicks, max CPC **$2.75** |
| utm_campaign | `secplus_portal` |
| Locations | **Countries + cities below** (presence-only) |
| Language | English |

**Location targeting:** Same Tier A/B country lists as `scripts/ccna-portal-10d-google-ads.md`. Federal/defense metros are especially relevant for Security+ (DoD 8570/8140). Start with Tier A on $10/day.

**Federal US landing (optional):** `comptia-sec+-home.html#home-secplus-samples-title` · `utm_content=federal-{market}`

---

## Ad group

| Setting | Value |
|---------|--------|
| Ad group name | `secplus_portal_10d` |
| Display path | `Security+` / `10-Day-Access` |
| Primary conversion | GA4 `begin_checkout` (`secplus_portal_10d`) |

**Final URL:**

```
https://becertifiedtoday.com/comptia-sec+-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=portal-10d
```

---

## Products or services to advertise

**Category:** Education & training → Test preparation

| # | Product / service name | Description (paste under name in Google Ads) |
|---|------------------------|-----------------------------------------------|
| 1 | Security+ 10-Day Exam Prep Access | 10 days of SY0-701 v5.0 exam prep in your browser: 1000+ practice questions, 28 PBQ scenarios, adaptive review, portal modes, and 90-min timed exam. Interactive prep with original study material. $9.99 one-time. |
| 2 | Security+ 30-Day Exam Prep Access | 30 days of the same SY0-701 library: 1000+ questions, 28 PBQ scenarios (21 chain labs, 4 standalone, 1 hot spot, 2 exhibits), adaptive review, progress tracking, and timed exam. $19.99 one-time. |
| 3 | Security+ Practice Questions | 1000+ SY0-701 MCQ bank with verified explanations, adaptive review, and timed exam. Browser-only. |
| 4 | Security+ PBQ Scenarios | 34 performance-based scenarios—chain labs, drag-drop, hot spots, IR exhibits—in browser. |
| 5 | Security+ Timed Exam Simulation | 90-minute mixed MCQ + PBQ run with domain scorecard review. Included with portal access. |

---

## RSA headlines (≤30 chars)

**Use all 15** — each headline must be structurally different. Every line maps to **page copy** on `comptia-sec+-home.html`.

```
Security+ Practice Test
SY0-701 Exam Prep
$9.99 for 10-Day Access
Security+ Practice Qs
CompTIA Security+ Prep
SY0-701 Question Bank
Practice Tests & Sim
1000+ Questions · v5.0
28 PBQ Scenarios Prep
Browser Security+ Prep
Timed Security+ Exam
Latest SY0-701 Questions
No PDFs — Interactive Prep
10-Day Full Library Access
Be Certified Today
```

**Pin:** H1 `Security+ Practice Test` · H2 `$9.99 for 10-Day Access` · H3 `SY0-701 Exam Prep`

---

## RSA descriptions (≤90 chars)

```
SY0-701 practice test bank: 1000+ questions, v5.0 aligned. 28 PBQ scenarios included.
$9.99 for 10-day access. Security+ exam prep—not a course. No PDFs or third-party apps.
Security+ practice questions with verified explanations. Timed exam + adaptive review.
Unlock 10-day full library access at checkout. 1000+ questions and 34 PBQ scenarios.
```

---

## Sitelink extensions (minimum 6)

| # | Link text | Description 1 | Description 2 | Full URL |
|---|-----------|---------------|---------------|----------|
| 1 | 10-Day Access · $9.99 | Full v5.0 question bank | $9.99 one-time, no sub | `https://becertifiedtoday.com/comptia-sec+-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=portal-10d` |
| 2 | 1000+ Practice Questions | SY0-701 v5.0 MCQ bank | Verified explanations | `https://becertifiedtoday.com/comptia-sec+-home.html#home-secplus-samples-title?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-samples` |
| 3 | 34 PBQ Scenarios | Chain labs & hot spots | Browser performance prep | `https://becertifiedtoday.com/secplus/pbq-practice-browser.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-pbq-list` |
| 4 | 28 PBQ Scenarios | Chain labs & hot spots | With 10-day access | `https://becertifiedtoday.com/comptia-sec+-home.html#home-secplus-samples-title&utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-pbq-list` |
| 5 | 1000+ Questions | v5.0 objectives aligned | Original study material | `https://becertifiedtoday.com/comptia-sec+-home.html#home-secplus-samples-title&utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-samples` |
| 6 | Timed Exam Included | 90-min exam-style run | With 10-day portal access | `https://becertifiedtoday.com/comptia-sec+-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=portal-10d` |

---

## Keywords

**Exact**

```
[security+ question bank]
[sy0-701 question bank]
```

**Phrase**

```
"security+ exam prep online"
"security+ practice test online"
"sy0-701 prep"
"comptia security+ question bank"
"sy0-701 question bank"
"security+ practice portal"
"security+ study prep online"
```

**Ad group negatives (Phrase)**

```
free
"free course"
"free practice"
"free practice test"
"free questions"
"free pbq"
bootcamp
course
dump
pdf
jobs
```

---

## Campaign-level negatives (Phrase)

```
free
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
"bootcamp"
"instructor led"
"unauthorized exam content"
"exam content"
"pass guarantee"
"pdf download"
"udemy"
"coursera"
"professor messer"
"dion training"
"jobs"
"salary"
"ccna 200-301"
"ccnp encor"
"cissp"
"ceh"
"pen test+"
```

---

## Setup checklist

- [ ] Ad group enabled: `secplus_portal_10d`
- [ ] Final URL includes `#purchase` and `utm_content=portal-10d`
- [ ] Products list pasted (5 items above)
- [ ] RSA + keywords pasted
- [ ] 6 sitelinks pasted
- [ ] Locations: Tier A countries + US federal/defense metros
- [ ] GA4 `begin_checkout` imported as Primary in Google Ads
- [ ] Stripe `secplus-portal-10d` payment link = $9.99
- [ ] Test: open Final URL → only **Get 10-day access · $9.99** above the fold → click → `begin_checkout` in GA4 Realtime

---

## Site behavior (`utm_content=portal-10d`)

- Purchase fold: 10-day $9.99 only (30-day hidden)
- Auto-scroll to `#purchase`
- One-time $9.99 / 10-day popup after 5s (`bcc-10d-one-time-offer.js`)
- Mobile sticky: `Get 10-day access · $9.99`

# CompTIA Security+ Google Ads — ad group `secplus_portal_10d`

Paste-ready setup for Google Ads UI. Landing: `public/comptia-sec+-home.html` with `utm_content=portal-10d` shows **$9.99 / 10-day** as the only primary purchase CTA.

**Source of truth:** this file in `scripts/` (not deployed to the public site).

---

## Campaign shell

| Setting | Value |
|---------|--------|
| Campaign name | `Security+ SY0-701 · Exam prep · becertifiedtoday` |
| Type | Search (Search partners off until baseline) |
| Daily budget | $10.00/day |
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
| 1 | Security+ 10-Day Exam Prep Access | 10 days of SY0-701 v5.0 exam prep in your browser: 1000+ practice questions, 28 PBQ scenarios, adaptive review, portal modes, and 90-min timed exam. Interactive prep—not stale PDF dumps. $9.99 one-time. |
| 2 | Security+ 30-Day Exam Prep Access | 30 days of the same SY0-701 library: 1000+ questions, 28 PBQ scenarios (21 chain labs, 4 standalone, 1 hot spot, 2 exhibits), adaptive review, progress tracking, and timed exam. $19.99 one-time. |
| 3 | Free Security+ Practice Questions | Preview current SY0-701 practice questions—shuffled each run, instant feedback, same style as the full bank. Free on comptia-sec+-home.html; no checkout. |
| 4 | Free Security+ PBQ Simulation | Dark-web IR simulation sample aligned to current SY0-701 PBQ style. Hands-on in browser. Free preview; no checkout. |
| 5 | Free Security+ Sample Pack | Three free previews from the question bank and PBQ set. Same verified explanations as full access. No checkout. |

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
Try free Security+ samples first. Unlock 10-day full library access at checkout.
```

---

## Sitelink extensions (minimum 6)

| # | Link text | Description 1 | Description 2 | Full URL |
|---|-----------|---------------|---------------|----------|
| 1 | 10-Day Access · $9.99 | Full v5.0 question bank | $9.99 one-time, no sub | `https://becertifiedtoday.com/comptia-sec+-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=portal-10d` |
| 2 | Free Practice Questions | Current SY0-701 MCQ preview | Instant feedback, free | `https://becertifiedtoday.com/secplus-sample?track=questions&utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-sample` |
| 3 | Free PBQ Simulation | Dark web IR scenario | Hands-on in browser | `https://becertifiedtoday.com/secplus-sample?track=sim-dark-web&utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-pbq` |
| 4 | 28 PBQ Scenarios | Chain labs & hot spots | With 10-day access | `https://becertifiedtoday.com/comptia-sec+-home.html#home-secplus-samples-title&utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-pbq-list` |
| 5 | 1000+ Questions | v5.0 objectives aligned | Not stale PDF dumps | `https://becertifiedtoday.com/comptia-sec+-home.html#home-secplus-samples-title&utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-samples` |
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
"free"
"bootcamp"
"course"
"dump"
"pdf"
"jobs"
```

---

## Campaign-level negatives (Phrase)

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

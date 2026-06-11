# CCNP ENCOR Google Ads — ad group `encor_portal`

Paste-ready setup for Google Ads UI. Landing: `public/ccnp-home.html` — **primary purchase is 30-day access ($19.99)**. The **$9.99 / 10-day** tier is a **one-time on-page offer** (popup once per browser), not the headline purchase CTA. **Do not use `utm_content=portal-10d`** for this campaign.

**Source of truth:** this file in `scripts/` (not deployed to the public site).

---

## Campaign shell

| Setting | Value |
|---------|--------|
| Campaign name | `CCNP ENCOR 350-401 · Exam prep · becertifiedtoday` |
| Type | Search (Search partners off until baseline) |
| Daily budget | $10.00/day |
| Bidding | Maximize clicks, max CPC **$2.75** |
| utm_campaign | `encor_portal` |
| Locations | **Countries + cities below** (presence-only) |
| Language | English |

**Location targeting:** Same Tier A/B country lists as `scripts/ccna-portal-10d-google-ads.md`. Start with Tier A (16 countries) on $10/day; expand after search-term review.

**Federal US landing (optional):** `ccnp-home.html#exam-audience` · `utm_content=federal-{market}`

---

## Ad group

| Setting | Value |
|---------|--------|
| Ad group name | `encor_portal` |
| Display path | `ENCOR` / `Exam-Prep` |
| Primary conversion | GA4 `begin_checkout` (`encor_portal_30d`) |

**Final URL:**

```
https://becertifiedtoday.com/ccnp-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=encor_portal&utm_content=portal-30d
```

---

## Products or services to advertise

**Category:** Education & training → Test preparation

| # | Product / service name | Description (paste under name in Google Ads) |
|---|------------------------|-----------------------------------------------|
| 1 | CCNP ENCOR 30-Day Exam Prep Access | 30 days of ENCOR 350-401 v1.2 exam prep in your browser: 400+ practice questions, 8 lab simulations, CLI labs, drag-and-drop sets, progress tracking, portal modes, and 120-min timed simulation. $19.99 one-time. Primary purchase on ccnp-home.html. |
| 2 | Free ENCOR 350-401 Practice Questions | Preview current ENCOR 350-401 v1.2 practice questions—shuffled each run, instant feedback, same style as the full bank. Free on ccnp-home.html; no checkout. |
| 3 | Free ENCOR Drag-and-Drop Practice | Current exam-style drag-and-drop items for ENCOR 350-401—shuffled PBQ-style prompts per run. Free preview; no checkout. |
| 4 | Free ENCOR ACL/CoPP CLI Lab | Browser ACL and CoPP CLI lab aligned to current ENCOR objectives. Hands-on practice without GNS3. Free preview; no checkout. |
| 5 | CCNP ENCOR Timed Simulation Practice | 120-minute exam-style practice run with mixed item types across all six ENCOR domains. Included with 30-day library access. |

**Do not add as a product:** $9.99 / 10-day access — it is a one-time on-page popup (`bcc-10d-one-time-offer.js`), not a guaranteed landing CTA.

---

## RSA headlines (≤30 chars)

**Use all 15** — each headline must be structurally different. Every line maps to **page copy** on `ccnp-home.html`.

```
CCNP ENCOR Practice Test
ENCOR 350-401 Exam Prep
$19.99 for 30-Day Access
ENCOR Practice Questions
Cisco ENCOR Practice Test
ENCOR Question Bank Online
Practice Tests & Simulation
400+ Questions · v1.2
8 Lab Sims + CLI Prep
Browser ENCOR Exam Prep
Timed ENCOR Simulation
Latest 350-401 Questions
No PDFs — Interactive Prep
30-Day Full Library Access
Be Certified Today
```

**Pin:** H1 `CCNP ENCOR Practice Test` · H2 `$19.99 for 30-Day Access` · H3 `ENCOR 350-401 Exam Prep`

---

## RSA descriptions (≤90 chars)

```
ENCOR 350-401 practice test bank: 400+ questions, v1.2 aligned. Labs & D&D included.
$19.99 for 30-day access. Cisco ENCOR exam prep—not a course. No PDFs or GNS3.
ENCOR practice questions with verified explanations. Timed simulation + portal modes.
Try free ENCOR samples first. Unlock 30-day full library access at checkout.
```

---

## Sitelink extensions (minimum 6)

| # | Link text | Description 1 | Description 2 | Full URL |
|---|-----------|---------------|---------------|----------|
| 1 | 30-Day Access · $19.99 | Full v1.2 question bank | $19.99 one-time, no sub | `https://becertifiedtoday.com/ccnp-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=encor_portal&utm_content=portal-30d` |
| 2 | Free Practice Questions | Current v1.2 MCQ preview | Instant feedback, free | `https://becertifiedtoday.com/sample?track=encor-questions&utm_source=google&utm_medium=cpc&utm_campaign=encor_portal&utm_content=sitelink-sample` |
| 3 | Sample Drag-and-Drop | PBQ-style items | Shuffled each run, free | `https://becertifiedtoday.com/sample?track=encor-dnd&utm_source=google&utm_medium=cpc&utm_campaign=encor_portal&utm_content=sitelink-dnd` |
| 4 | Free ACL/CoPP CLI Lab | Hands-on lab in browser | No GNS3 required | `https://becertifiedtoday.com/sample?track=encor-lab&utm_source=google&utm_medium=cpc&utm_campaign=encor_portal&utm_content=sitelink-lab` |
| 5 | Latest v1.2 Questions | 400+ items, 8 lab sims | Not stale PDF dumps | `https://becertifiedtoday.com/ccnp-home.html#home-encor-samples-title?utm_source=google&utm_medium=cpc&utm_campaign=encor_portal&utm_content=sitelink-samples` |
| 6 | Timed Sim Included | 120-min exam-style run | With 30-day portal access | `https://becertifiedtoday.com/ccnp-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=encor_portal&utm_content=portal-30d` |

---

## Keywords

**Exact**

```
[ccnp encor question bank]
[encor 350-401 question bank]
```

**Phrase**

```
"ccnp encor exam prep online"
"encor practice test online"
"encor 350-401 prep"
"ccnp encor question bank"
"encor 350-401 question bank"
"cisco encor practice portal"
"encor study prep online"
```

**Ad group negatives (Phrase)**

```
"free"
"bootcamp"
"course"
"dump"
"pdf"
"jobs"
"netacad"
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
"cbt nuggets"
"ine encor"
"cisco netacad"
"jobs"
"salary"
"ccna 200-301"
"ccie"
"comptia security+"
"packet tracer course"
"gns3 tutorial"
```

---

## Keyword demand & estimated monthly clicks

**Research date:** 2026-06-11 · **Primary geo:** United States · **Secondary:** Philippines

**Important:** *Monthly searches* = market demand on Google. *Monthly clicks* = what your ads actually receive (only known from Google Ads after launch). Figures below are **modeled estimates**, not BCT historical ad data.

**Method:** Google Trends (US, 12 months) for relative demand; anchor term `ccnp encor` modeled at ~2,400 US searches/mo (typical GKP/SEO-tool band—verify in Keyword Planner); zero Trends signal → &lt;10 US searches/mo; estimated ad clicks assume **$10/day**, max CPC **$2.75**, **~70–110 total campaign clicks/mo** shared across all keywords.

### US — campaign keywords (estimated)

| Keyword | Match | Est. searches/mo | Trends (US) | Est. ad clicks/mo* |
|---------|-------|------------------|-------------|-------------------|
| ccnp encor question bank | Exact | &lt;10 | no signal | 0–1 |
| encor 350-401 question bank | Exact | &lt;10 | no signal | 0–1 |
| ccnp encor exam prep online | Phrase | 30–90 | low | 2–6 |
| encor practice test online | Phrase | 110–390 | spike-prone | 8–18 |
| encor 350-401 prep | Phrase | 40–120 | low | 3–7 |
| ccnp encor question bank | Phrase | 50–160 | low | 3–8 |
| encor 350-401 question bank | Phrase | 20–70 | no signal | 1–4 |
| cisco encor practice portal | Phrase | &lt;10 | no signal | 0–1 |
| encor study prep online | Phrase | 10–50 | low | 0–3 |

\*Shares of ~70–110 total monthly clicks at $10/day—not per-keyword ceilings.

### US — anchor terms (context; not all in ad group)

| Keyword | Est. searches/mo | Notes |
|---------|------------------|-------|
| ccnp encor | 1,300–3,600 | Consider phrase match if budget rises |
| encor 350-401 | 140–400 | ~11% of anchor (Trends) |
| encor practice test | 320–900 | Boson / Crucial compete here |
| ccnp encor practice test | 90–260 | Optional 2nd ad group |

### Philippines (estimated ~12–18% of US for ENCOR)

| Keyword | Est. searches/mo | Est. ad clicks/mo* |
|---------|------------------|-------------------|
| encor practice test online | 15–60 | 1–4 |
| ccnp encor exam prep online | 5–20 | 0–2 |
| Other campaign keywords | &lt;25 each | 0–2 |

**Refresh:** Keyword Planner or Ahrefs/Keywords Everywhere before scaling budget. Replace estimates with the Search terms report after 30 days live.

---

## Competitive analysis (ENCOR 350-401)

Sources: `data/encor-question-sourcing/competitor-sites/` + live SERP review (Jun 2026).

| Competitor | Free offer | Paid library | Labs / PBQ | Timed exam | Price model | vs BCT |
|------------|------------|----------------|------------|------------|-------------|--------|
| **Be Certified Today** | 3 samples | 400+ Q, v1.2 | 8 CLI labs, DnD | 120-min sim | $19.99/30d one-time | — |
| **Crucial Exams** | 20 Q/demo | 600 Q + flashcards | Custom timed sets | Configurable | Subscription | BCT: 8 dedicated lab sims, lower one-time price, browser-only |
| **OpenExamPrep** | 100+ Q, no signup | Upsell | MCQ samples | Interactive quiz | Free-first SEO | BCT: verified explanations, full portal, clear 30-day checkout |
| **TrustEd Institute** | Limited free | 2,880 Q claimed | 5×102-Q mocks | Full mocks | Paid unlock | BCT: ENCOR CLI/CoPP labs, interactive portal |
| **Pearson VUE** | None | 246 Q official | Cert + practice modes | Official | ~$150+ / 6 mo | BCT: cheaper, more Qs + labs; they win “official” trust |
| **Boson ExSim** | Demo | ExSim ENCOR | NetSim (separate) | Exam simulation | $99+ | BCT: no install; they win head-term brand |
| **ExamTopics / PrepAway / Exam-Labs** | Partial | Dump/recall style | No real labs | No | Low $ | BCT: no dumps; use negatives |
| **INE / CBT / Pluralsight** | Trials | Video paths | External labs | Quizzes | $49–99+/mo | Course intent—already negated |
| **A Guide to Cloud** | 20 free Q | 200 Q | Timed mode | Domain drills | Freemium | BCT: larger bank + CLI labs |

**SERP takeaways**

- Head terms: Boson, Crucial Exams, OpenExamPrep dominate organic—expect higher CPC.
- “Question bank” exact: tiny volume; keep for relevance, not scale.
- **Ad copy angles:** 400+ browser questions, 8 lab sims, v1.2, **$19.99/30-day one-time**, free samples.
- **Gap:** few competitors bundle CLI labs + drag-and-drop + timed sim in one browser portal without GNS3 or video subs.

**Keyword priority (first 30 days @ $10/day)**

1. `encor practice test online` — highest modeled volume + intent  
2. `ccnp encor exam prep online` — matches landing H1 + 30-day CTA  
3. `encor 350-401 prep` — exam-code specificity  
4. Phrase `ccnp encor question bank` — relevance  
5. Exact bank terms — expect &lt;5 clicks/mo combined  

After 30 days: pause search terms with spend but no `begin_checkout` (`encor_portal_30d`).

---

## Setup checklist

- [ ] Ad group enabled: `encor_portal`
- [ ] Final URL points to `#purchase` (no `utm_content=portal-10d`)
- [ ] Products list pasted (5 items above — no 10-day product line)
- [ ] RSA + keywords pasted (30-day pricing, not $9.99 headlines)
- [ ] 6 sitelinks pasted
- [ ] Locations: Tier A countries (or US metros for federal test)
- [ ] GA4 `begin_checkout` imported as Primary in Google Ads
- [ ] Stripe `encor-portal-30d` payment link = $19.99
- [ ] Test: open Final URL → **Get 30-day access** above the fold → click → `begin_checkout` (`encor_portal_30d`) in GA4 Realtime

---

## Site behavior (standard `ccnp-home.html` visit)

- Purchase fold: **30-day $19.99** primary CTA
- Free ENCOR samples below the fold
- **One-time $9.99 / 10-day popup** ~5s after load (once per browser)
- Optional last-chance bar near FAQ (same dismiss flag)
- **Do not advertise $9.99 / 10-day in Google Ads** — it is not guaranteed above the fold

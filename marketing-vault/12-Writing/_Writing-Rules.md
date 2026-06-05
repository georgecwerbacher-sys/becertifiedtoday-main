---
type: writing-guide
status: active
scope: guest-facing-pages
tags:
  - copy
  - landing-pages
  - index
  - exam-prep
---

# Writing rules — guest-facing index & landing pages

**Project:** Be Certified Today — `public/` index, product home pages, and other pages visitors see before or instead of gated portals.

**North star:** [[../01-strategy/positioning-and-messaging|Positioning & messaging]] — **exam prep**, not courses; realistic practice; verified solutions; browser-only.

**When to use this doc:** Drafting or revising copy in `index.html`, `comptia-sec+-home.html`, `ccna-home.html`, `ccnp-home.html`, free-sample entry pages, meta/OG/JSON-LD, and hero/FAQ blocks on those URLs. After deploy, log changes in [[../06-website-optimization/content-change-log|content change log]] and run [[../06-website-optimization/landing-page-audit-checklist|landing page audit checklist]] for paid final URLs.

---

## Table of contents

**Part A — Project parameters**
1. Voice & point of view
2. Tense
3. Length & structure
4. Target audience & tone

**Part B — Prose excellence**
5. Accessible vocabulary
6. Strong verbs
7. Sentence & paragraph structure
8. Concision & tightening
9. No em or en dashes

**Part C — Page architecture**
10. Page types (index vs landing)
11. Above-the-fold requirements
12. Section patterns & CTAs
13. Message match with Google Ads

**Part D — Messaging guardrails**
14. Words we use / words we avoid
15. Trust, pricing, and policy

**Part E — SEO & machine-readable copy**
16. Title, meta, Open Graph, JSON-LD
17. FAQ and AI search

**Part F — AI detection & authenticity**
18. AI vs human patterns
19. Verification protocol
20. Authenticity checklist

**Part G — Workflow**
21. Before you ship copy
22. Author approval

---

## Part A — Project parameters

### 1. Voice & point of view

**Default: Second person (“you”) or direct address to the exam-taker.**  
Optional neutral third person for bullets and feature lists (“Practice tests run in the browser”).

**Do not use:**
- First-person narrator (“I walked into the lab…”)
- Novel-style interior monologue
- Instructor voice (“In this lesson we will learn…”)

**Brand voice:** Direct, practical, respectful of time. Confident about **practice quality**; humble about **outcomes** (prep helps readiness; we do not promise a pass).

### 2. Tense

**Present tense** for benefits, product behavior, and what the visitor gets today.

- Yes: “You practice in the browser.” “The simulation runs 90 minutes.”
- Avoid past-tense marketing fluff: “We have helped thousands…” unless backed by a real metric you can cite on the page.

### 3. Length & structure

| Element | Guideline |
|---------|-----------|
| **H1** | One line; exam code + prep intent where relevant (SY0-701, CCNA 200-301, ENCOR 350-401) |
| **Hero lead** | 1–3 short sentences; value prop + differentiator |
| **Benefit bullets** | 4–7 items; each bullet one idea, under ~12 words when possible |
| **Section body** | 2–4 sentences per block; break long walls with subheads |
| **FAQ answers** | 2–4 sentences; factual; match [[../01-strategy/google-ai-search-strategy|AI search strategy]] |
| **CTA labels** | 2–6 words; verb-first (“Try free sample”, “Get 30-day access”) |

Landing pages should read like **mainstream commercial exam-prep landings**: scannable, not essay-length.

### 4. Target audience & tone

**Primary audience:** Adults preparing for a scheduled exam (often 30+), including federal/defense Security+ test-takers under deadline pressure. Minimum readability: comfortable for a high-school graduate; no academic gatekeeping.

**Tone:** Build **genuine confidence** in the practice product. The visitor should feel: “This matches how I need to study” and “I can try it before I pay.”

**Jobs to echo (pick what fits the page):**
- Emotional: “I need to know I’m ready.”
- Functional: “Realistic practice with trustworthy answers in one place.”
- Economic: “Cheaper to practice well than to pay for a retake.”

---

## Part B — Prose excellence

**Core principle: Simplicity + strength + concision = clarity that converts.**

Every word on a landing page competes with the back button. Accessible vocabulary removes friction; strong verbs drive action; cutting filler makes offers believable.

### 5. Accessible vocabulary

**Keep**
- Common words (practice test, simulation, scorecard, browser)
- Official exam codes and formats (SY0-701, PBQ, 200-301, 350-401)
- Concrete product terms (10-day access, 35-minute sample, drag-and-drop)

**Replace or cut**
- Academic abstractions (“leverage synergies”, “holistic learning journey”)
- Course/training framing when we mean prep (“training program”, “masterclass”, “curriculum”)
- Dump/cheat language (“actual exam”, “leaked”, “brain dump”)
- Vague superlatives without proof (“world-class”, “ultimate”, “revolutionary”)

### 6. Strong verbs

**Prefer active, specific verbs**

| Weak | Strong |
|------|--------|
| You are able to practice | You practice |
| Access is provided to questions | Open 700+ questions |
| The simulation is designed to mimic the exam | The simulation mirrors exam timing and navigation |

**Passive voice:** Rare; OK when the object matters (“Questions are organized by SY0-701 domain”).

**Cut qualifiers** unless legally or factually required: very, really, just, quite, somewhat, seems, might, arguably.

### 7. Sentence & paragraph structure

**Prefer**
- Short declarative sentences
- One benefit per bullet
- Parallel structure in lists (“Timed simulation”, “Drag-and-drop PBQs”, “Scorecard with review”)

**Avoid**
- Stacked clauses: “Because you need to pass SY0-701, and since many roles require Security+, we offer…”
- Triple-adjective openings: “Comprehensive, cutting-edge, industry-leading…”

**Paragraphs:** 2–4 sentences for body copy; 1 sentence for emphasis or CTA lead-in.

### 8. Concision & tightening

**Cut ruthlessly**
- Hedging: “We believe you may find…” → “You get…”
- Empty openers: “It is important to note that…”
- Redundant pairs: “completely unique”, “advance planning”
- Weak verb + adverb: “quickly navigate” → “navigate” or “finish faster”

**Keep**
- Exact prices, durations, question counts, sim lengths
- Exam codes and objective alignment claims you can support
- Necessary qualifications (“aligned to SY0-701 objectives”, not “guaranteed pass”)

### 9. No em or en dashes

**Em dashes (—) and en dashes (–) are prohibited in guest-facing copy.** Restructure instead.

| No | Yes |
|----|-----|
| Realistic practice—no PDFs | Realistic practice. No PDFs. |
| SY0-701 prep—browser only | SY0-701 prep in your browser |

**Allowed:** Hyphens in compounds (exam-style, browser-based, 35-minute).

**In HTML:** Use commas, periods, or separate elements; do not rely on `&mdash;` for prose rhythm.

---

## Part C — Page architecture

### 10. Page types

| Page | Path (examples) | Job |
|------|-----------------|-----|
| **Site index** | `/index.html` | Route visitors to the right exam prep; establish brand; no gated portal links as primary CTAs |
| **Product landing (Ads)** | `/comptia-sec+-home.html`, `/ccna-home.html`, `/ccnp-home.html` | Message match for paid keywords; sample → purchase funnel |
| **Legacy / portal hubs** | `/secplus-home.html`, `*Training_Portal.html` | Not primary ad destinations; `noindex` where documented; customer-facing copy still follows these rules if visible |
| **Sample / PBQ entry** | Under `public/COMP_TIA_SEC+/`, `public/CCNA-Study/`, etc. | Mid-funnel; repeat exam code + prep; clear path back to product landing `#purchase` |

Vault page notes: [[../06-website-optimization/README|Website optimization]] → `pages/`.

### 11. Above-the-fold requirements

On **mobile first screen**, the visitor must see without scrolling:

1. **H1** aligned to ad keywords or index intent
2. **One-sentence** differentiator (browser, exam-realistic, not a course)
3. **Primary CTA** (free sample, free sim, or purchase) with honest label
4. For **paid landings**: price or “from $X” if the ad promises it

### 12. Section patterns & CTAs

**Typical landing order** (adjust per product note, do not omit purchase on monetized pages):

1. Hero (H1 + lead + primary CTA)
2. Free path (sample questions or lead-magnet sim)
3. What’s included (bullets: banks, sim length, PBQ/drag-drop, devices)
4. `#purchase` — prices, durations, no-subscription clarity
5. FAQ (factual; supports AI Overviews)
6. Footer trust (logo, terms/privacy if collecting data)

**CTA rules**
- One **primary** action per viewport when possible
- Button text = outcome (“Start free 35-minute simulation”, not “Click here”)
- Secondary CTAs visually subordinate

### 13. Message match with Google Ads

Before changing H1 or hero copy:

1. Open the campaign note in `02-campaigns/<product>/`
2. Compare keyword theme → ad headline → landing H1 ([[../06-website-optimization/google-ads-quality-score-guide|Quality score guide]] table)
3. Update the matching `06-website-optimization/pages/*.md` hero section

**Rule:** If the ad says “free practice test”, the first screen must show the free path, not only paid pricing.

---

## Part D — Messaging guardrails

### 14. Words we use / words we avoid

| Use | Avoid |
|-----|--------|
| exam prep, practice tests, simulation, question bank | course, training program, learn from scratch |
| SY0-701, CCNA 200-301, ENCOR 350-401 | generic “cybersecurity learning” |
| browser-based, no PDF, no third-party app | download our app, install required |
| aligned to objectives, verified explanations | actual exam questions, leaked, dump |
| 10-day / 30-day access, one-time sim purchase | guaranteed pass, 100% pass rate |

Internal filenames may say “Training Portal”; **visitor-facing** copy says **practice portal** or **exam prep**.

**Federal / Security+:** You may mention DoD/contractor **context** for SY0-701 prep. Do **not** claim you satisfy a specific DoD requirement or clearance outcome.

### 15. Trust, pricing, and policy

- Show **USD prices** before Stripe
- State **access duration** (10-day, 30-day, one-time sim)
- If ads claim **no subscription**, say it plainly on `#purchase`
- No implied **CompTIA or Cisco endorsement**
- No **misleading certification claims**

---

## Part E — SEO & machine-readable copy

### 16. Title, meta, Open Graph, JSON-LD

- **`<title>`** and **meta description**: exam prep + product codes; under ~60 / ~155 characters where practical
- **Canonical** URL matches production path
- **OG/Twitter**: same story as meta; no “training course” positioning
- **JSON-LD**: factual `WebSite` / `WebPage` descriptions; consistent with visible H1

Index example pattern: “IT Certification Exam Prep — CCNA, CCNP ENCOR & Security+ | Be Certified Today”.

### 17. FAQ and AI search

FAQ blocks should answer real prep questions with **specific facts** (sim length, PBQ types, pricing, browser support). See [[../01-strategy/google-ai-search-strategy|Google AI search strategy]].

- Use question headings that match how people ask AI (“How long is the Security+ practice simulation?”)
- Answers: direct first sentence, then detail
- Do not stuff keywords; do not contradict hero copy

---

## Part F — AI detection & authenticity

### 18. AI vs human patterns

| AI habit | Human / on-brand fix |
|----------|----------------------|
| Adds atmosphere where the draft had none | Keep concrete product facts only |
| Replaces a short line with a longer “enhanced” one | Keep the shorter line if it already works |
| Generic inspiration (“embark on your journey”) | Specific exam-taker outcome (“Know you’re ready before test day”) |
| Rule of three buzzwords | One strong differentiator |
| Em dashes and stacked metaphors | Short sentences per Part B |

### 19. Verification protocol

Before approving AI-suggested copy:

1. **Purpose:** Does this sentence help message match, clarity, or conversion? If not, reject.
2. **More vs better:** Is the revision shorter and clearer, or only longer?
3. **Recognition test:** Would this sound like our existing `comptia-sec+-home` / `ccna-home` voice?
4. **Positioning check:** Still exam prep, not a course? No forbidden claims?

### 20. Authenticity checklist

- [ ] Exam code correct for the page
- [ ] Claims match what the product actually does (check repo / page note)
- [ ] No em/en dashes in new prose
- [ ] No dump/guarantee/endorsement language
- [ ] CTA labels honest (free really is free; paid shows price)
- [ ] Matches [[../01-strategy/positioning-and-messaging|positioning]] pillars

One failed row → rewrite or keep the original.

---

## Part G — Workflow

### 21. Before you ship copy

1. Edit HTML in `public/` (or propose diff for review)
2. For **Google Ads final URLs**: score with [[../06-website-optimization/landing-page-audit-checklist|audit checklist]]
3. Update `06-website-optimization/pages/<page>.md` hero/notes
4. Append [[../06-website-optimization/content-change-log|content change log]] row (date, path, summary, campaign)
5. Deploy; re-check Ads landing page experience after ~7 days of traffic

### 22. Author approval

Substantive copy changes (hero, H1, pricing claims, FAQ facts, meta/JSON-LD positioning) need **explicit approval** before deploy unless the user asked for the edit in the same task.

Grammar and obvious typos may ship with the change batch. When using Cursor, prefer **minimal diffs**: change only the strings needed for message match or positioning.

---

## Quick reference — active guest URLs

| Page | Vault note |
|------|------------|
| `/index.html` | Site index (exam prep hub) |
| `/comptia-sec+-home.html` | [[../06-website-optimization/pages/comptia-sec-plus-home|Security+ ad landing]] |
| `/ccna-home.html` | [[../06-website-optimization/pages/ccna-home|CCNA ad landing]] |
| `/ccnp-home.html` | [[../06-website-optimization/pages/ccnp-home|ENCOR ad landing]] |

**Related:** [[../06-website-optimization/README|Website optimization]] · [[../prompts|AI prompts]] · Humanizer skill (optional pass on long FAQ blocks only)

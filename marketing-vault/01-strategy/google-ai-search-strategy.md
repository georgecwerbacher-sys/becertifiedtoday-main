---
type: strategy
status: active
tags:
  - google
  - ai-overviews
  - seo
  - search
---

# Google AI search strategy

Goal: show up when people use **Google AI Mode**, **AI Overviews**, and AI-assisted search for exam prep — while running **Google Ads** on the same intent keywords.

AI search and paid search share one requirement: **pages that clearly answer what the test-taker is asking**.

## What users ask AI (exam prep)

Typical prompts we should be eligible to satisfy:

- “Best Security+ SY0-701 practice test”
- “Security+ exam simulation online”
- “CompTIA Security+ practice questions with explanations”
- “Alternative to Security+ PDF dumps”
- “How to practice performance-based Security+ questions”

Our answer in one line (use in meta descriptions, intro paragraphs, FAQ):

> Browser-based SY0-701 **exam prep** with interactive practice questions, verified explanations, and a timed simulation — no PDFs or third-party software.

## How AI systems choose sources

Optimize landing pages so AI (and Google quality systems) can extract trustworthy facts:

### Content structure

- [ ] **Clear H1** with exam name + intent (“Security+ SY0-701 exam prep” / “practice test”)
- [ ] **Lead paragraph** states: exam prep (not course), browser-based, no PDF, timed sim available
- [ ] **FAQ section** on primary landing pages — 5–8 real questions test-takers ask
- [ ] **Headings as questions** where natural (`## What formats does the SY0-701 practice include?`)
- [ ] **Specific facts**: price, access duration, question types, exam code, objective version

### Trust signals (E-E-A-T)

- [ ] Accurate exam objectives reference (SY0-701 v5.0, etc.)
- [ ] No dump/cheat language
- [ ] Transparent pricing and access terms
- [ ] Sample activity available without paywall (try before buy)
- [ ] Site identity consistent (Be Certified Today, same domain in Ads and content)

### Technical (site work in Cursor)

- [ ] Strong meta title + description on `/comptia-sec+-home.html` (exam prep keywords, not “training course”)
- [ ] Canonical URL set
- [ ] Consider `FAQPage` structured data when FAQ block exists *(future implementation)*
- [ ] Fast mobile page — AI citations favor usable sources

## AI search vs Google Ads — same intent, different mechanics

| | Google Ads | AI search / Overviews |
|--|------------|------------------------|
| **Control** | Keywords, bids, ads, landing URLs | Content quality, structure, reputation |
| **Metric** | CTR, CPA, Quality Score | Impressions in AI answers, referral traffic |
| **Copy focus** | Keyword match + policy-safe claims | Factual, citable, concise answers |
| **Landing page** | Message match + conversion | Same page — must read well for humans *and* extractable by AI |

**Do not** create separate “AI pages” with thin content. Strengthen the same landing URLs Ads already use.

## Keyword themes aligned with positioning

**Bid / target (Ads + page copy):**

- `[exam] practice test`
- `[exam code] practice questions`
- `[exam] exam simulation` / `timed practice exam`
- `[exam] exam prep` *(not “training course”)*

**Use carefully or as negatives:**

- `free course`, `bootcamp`, `training program`, `learn cybersecurity`
- `dump`, `pass guaranteed`, `actual exam questions leaked`

## FAQ bank — Security+ (draft for landing page)

Use or adapt on `comptia-sec+-home.html`:

1. **Is this a course or exam prep?** Exam preparation only — practice questions and simulations, not instructor-led training.
2. **Does it work like the real SY0-701 exam?** Includes multiple-choice and performance-based style items plus an optional timed simulation.
3. **Do I need to install software?** No — runs in your browser.
4. **Are there PDFs?** No — interactive practice only.
5. **How much does access cost?** 10-day and 30-day passes plus a one-time timed simulation option — prices on the purchase section.
6. **Can I try before I buy?** Yes — free sample questions available.

Track FAQ additions in [[../06-website-optimization/content-change-log|content change log]].

## Measurement

- GA4: organic + paid landing page engagement; track AI referral sources if visible in acquisition reports
- Search Console: queries triggering impressions (including AI-related growth over time)
- Weekly review: note any AI Overview visibility for target queries *(manual check)*

## Workflow

1. Update [[positioning-and-messaging|positioning]] when product scope changes  
2. Align [[../02-campaigns/security-plus-google-ads|Ads copy]] and landing H1/FAQ to same facts  
3. Audit with [[../06-website-optimization/landing-page-audit-checklist|landing page checklist]]  
4. Implement in `public/` via Cursor  
5. Log in [[../06-website-optimization/content-change-log|change log]]  

## Open experiments

- [x] Add FAQ block to Security+ landing page (2026-05-30)
- [x] H1: “exam prep” + “practice tests & simulation” (2026-05-30)
- [ ] Monitor Search Console for AI-heavy query variants
- [ ] Ad group specifically for “simulation” / “timed exam” intent

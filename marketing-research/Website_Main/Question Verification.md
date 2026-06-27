---
type: website
page: question-verification
site: becertifiedtoday.com
status: draft
planned_url: https://becertifiedtoday.com/how-we-verify-questions.html
nav: pending
seo_index: noindex until nav launch
tags:
  - marketing
  - becertifiedtoday
  - verification
  - question-bank
  - website
related:
  - "[[About Page]]"
  - "[[../Site Mission|Site Mission]]"
  - "[[../../templates/question-bank/README|Question bank template (repo)]]"
reddit:
  subreddit: r/RealisticCertPrep
  format: long-form post + link to live page when indexed
  video: planned later (not v1)
---

# How I verify exam questions

*Draft page:* `public/how-we-verify-questions.html` · **Do not add to top nav or sitemap until `status: published`.**

---

## Writing rules (guest copy)

Reference: [[../Site Mission|Site Mission]] · [[About Page|About Page]] voice.

| Rule | Detail |
|------|--------|
| **Persuasive, first person** | Use **I** for what I built and how I verify; use **you** for the reader’s prep outcome. Lead with test-day readiness, not feature lists. |
| **No em or en dashes** | Never use `—` or `–` in guest-facing copy. Use commas, periods, colons, or parentheses instead. |
| **No dump/competitor talk** | Do not describe scraping, hunts, or third-party dumps on this page. |
| **Tier A only for keys** | Cisco docs, Learning Network, DevNet, CompTIA official sources. Forums and braindumps are explicitly out. |
| **Light bold** | Avoid mechanical bold on every noun phrase. Bold only where it aids scan (e.g. Example, Replace with). |
| **Nav label (later)** | **How I verify** |

Internal notes and tables in this file may use arrows (`→`) for brevity; live HTML must not use em/en dashes.

---

## Purpose

I built Be Certified Today for **test preparation**: timed simulation, adaptive review, and exam-style practice in the browser. Accuracy is the product. This page explains how I keep question banks aligned to **current official exam objectives**, verified on **credible vendor sources**, and organized so you practice what the blueprint actually tests today, not stale recall from an old PDF.

**This page does not describe competitor scraping or third-party dumps.** Verification is about official blueprints and Tier A documentation only.

---

## SEO (when published)

| Field | Value |
|-------|--------|
| **Title** | How I Verify Certification Practice Questions \| Be Certified Today |
| **Meta description** | How I verify certification practice questions: official exam PDFs, blueprint tags, objective mapping, 100-question banks by domain weight, and Tier A vendor docs for accurate test preparation. |
| **Canonical** | `https://becertifiedtoday.com/how-we-verify-questions.html` |
| **Primary keywords** | verified certification practice questions, exam objectives alignment, official exam topics PDF, accurate test preparation |
| **Robots (draft)** | `noindex, nofollow` (flip to `index, follow` when nav goes live) |
| **Nav placement (later)** | Header on `/`, `/about.html`, exam home pages. Label: **How I verify** |

---

## Page sections → live HTML

| # | Section | Message |
|---|---------|---------|
| 1 | **Hero** | Accurate testing is why the site exists; not a course, not a dump. Readiness practice. |
| 2 | **Start with the official PDF** | Every track anchors to the vendor exam topics PDF (version labeled on site) |
| 3 | **PDF version comparison** | When Cisco/CompTIA publish a new PDF, diff objectives; retire or rewrite affected items |
| 4 | **Tier A verification** | Keys checked on official docs / Learning Network / DevNet (Cisco) or CompTIA sources, not forums |
| 5 | **Tag every question** | Blueprint version + objective ID + sub-objective when PDF lists children |
| 6 | **100-question banks** | Domain mix matches exam weights (e.g. CCNAAUTO v1.1: 15/20/15/15/20/15 per 100) |
| 7 | **Obsolete database** | Items dropped from current blueprint → obsolete archive; not in active weighted pools |
| 8 | **CTA** | Try free samples · pick your exam track |

---

## Workflow (internal, public-facing summary)

1. **Download / track** the current official exam topics PDF (`v1.1`, `v1.2`, `V_2025`, …).
2. **Compare** to the prior PDF when an update ships. Record wording changes, renames, removals (see CCNAAUTO v1.0 → v1.1 change log on portal).
3. **Author or revise** each practice item; paraphrase stems; map to objective + sub-objective.
4. **Verify** correct answer and explanation on Tier A source; record verification date in topic map (no forum/dump URLs).
5. **Place** in the active bank only if it matches the **current** blueprint version and domain weight budget.
6. **Move** items that only test removed objectives to the **obsolete database**. Still documented, not served in default random/review for the current exam.
7. **Run** tracker + URL lint before publish (`build:question-bank-tracker`, `lint:question-urls`).

---

## Image & media spec

Place assets under `public/images/verification/` when ready. Until then, live page uses dashed placeholders.

**Layout:** Dark blue panels (`.format-card` style) for section blocks; light blue gradient (`.highlight-box`) sparingly for Tier A callout and key examples.

| ID | Placement | Type | Dimensions | Content |
|----|-----------|------|------------|---------|
| **IMG-1** | After “Start with the official PDF” | Screenshot (cropped) | **1200×675** max display **980px** wide · WebP or JPG ≤ **180 KB** | Side-by-side: official exam topics PDF cover + objective list excerpt (e.g. CCNAAUTO v1.1 domain 2.0). Blur account IDs. |
| **IMG-2** | After “PDF version comparison” | Screenshot | **1200×800** · ≤ **200 KB** | Portal or internal diff view: v1.0 vs v1.1 objective change (rename/removal highlighted). No competitor URLs. |
| **IMG-3** | After “Tag every question” | Screenshot (sanitized) | **1100×620** · ≤ **150 KB** | Topic map row: `blueprintVersion`, `objectives`, `subObjectives`, `verification.sources` (Cisco URLs only). Redact internal paths if needed. |
| **IMG-4** | After “100-question banks” | Screenshot | **1200×700** · ≤ **180 KB** | Training portal **domain weight table** + Bank 1 card (target mix vs published counts). |
| **IMG-5** | After “Obsolete database” | Screenshot or diagram | **1000×560** · ≤ **120 KB** | Practice UI or doc showing **V_2025** vs current filter, or “obsolete” label, not in default bank. |
| **VID-1** | Bottom band (future) | Video embed | **16:9** · 1080p source · ≤ **90 s** | Walkthrough: PDF → verify on Cisco doc → tag objective → bank slot. **Not v1**. Reserve `<figure>`; becomes Reddit post + optional YouTube later. |

**Alt text pattern:** Describe what the learner sees, not “screenshot of page.” Example: *“CCNAAUTO v1.1 exam topics PDF open to domain 2.0 API objectives.”*

---

## Reddit (r/RealisticCertPrep)

When page is **indexed** and nav is live:

- **Title idea:** How I keep certification practice questions aligned to the official blueprint (no dumps)
- **Body:** Short lead + link to `how-we-verify-questions.html`
- **Tone:** Transparent process, Tier A sources, obsolete handling. Match subreddit “realistic prep” angle.
- **Video:** Optional follow-up post when VID-1 exists

---

## Launch checklist

- [ ] Replace all `media-placeholder` blocks with optimized images
- [ ] Set `meta robots` to `index, follow`
- [ ] Add `<a href="/how-we-verify-questions.html">How I verify</a>` to site header nav (`index.html`, `about.html`, exam homes)
- [ ] Add URL to `public/sitemap.xml` (run `npm run sync:sitemap` if scripted)
- [ ] Update frontmatter `status: published` here
- [ ] Optional: FAQ schema in JSON-LD if adding FAQ section

---

## Internal references

- Repo template: `templates/question-bank/README.md`
- Cisco verification rule: `.cursor/rules/answer-verification-cisco-sources.mdc`
- CCNAAUTO blueprint diff JSON: `public/CCNAAUTO-Study/data/ccnaauto-blueprint-v1-changes.json`
- CCNA version tags: `V_2025` / `V_2026` on question pages + topic map

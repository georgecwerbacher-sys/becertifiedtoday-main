---
type: strategy
parent: "[[Wedge Marketing plan]]"
tags:
  - marketing
  - content
  - seo
---

# Content & landing pages

[[Wedge Marketing plan|← Back to plan]]

Build **problem pages** — not another generic homepage. Each page = one promise, one CTA, matched UTM headline.

---

## CCNA — build priority

| Priority | Page slug | Target query | CTA | Status |
|----------|-----------|--------------|-----|--------|
| 1 | `/ccna/labs-without-gns3.html` | ccna practice labs free · ccna 200 301 practice labs · ccna labs without gns3 | Free VLAN lab → 10-day pass | **Live** |
| 2 | `/ccna/timed-practice-test.html` | ccna timed practice test online | Free samples → 10-day pass | Build |
| 3 | `/ccna/drag-and-drop-practice.html` | ccna drag and drop practice | Sample D&D → 10-day pass | Build |
| 4 | `/ccna/exam-readiness.html` | ccna exam readiness / final review | Free samples → 10-day pass | Build |
| 5 | `/ccna/200-301-v1-v2.html` | ccna version 1.1 2.0 questions | Portal filter story → purchase | Build |
| 6 | `/ccna/two-week-study-plan.html` | ccna study plan 2 weeks before exam | 10-day pass | Build |

**Live wedge URL for ads:** `https://becertifiedtoday.com/ccna/labs-without-gns3.html?utm_content=browser-labs`

**Existing assets to link:** `/sample?track=ccna-vlan`, `/sample?track=ccna-dnd`, `ccna-home.html#purchase?utm_content=portal-10d`

---

## ENCOR — build priority

| Priority | Page slug (proposed) | Target query | CTA |
|----------|----------------------|--------------|-----|
| 1 | `/encor/labs-without-gns3.html` | encor lab simulation browser | ACL/CoPP sample → 30-day pass |
| 2 | `/encor/timed-practice-test.html` | encor timed practice test | Free samples → 30-day pass |
| 3 | `/encor/350-401-study-plan.html` | encor exam prep 3 weeks | 30-day pass |

---

## Security+ — build priority

Persona **Sam** — PBQ anxiety, adaptive review, browser-no-install. Tracker: [[SEC+ funnel build tracker]].

| Priority | Page slug | Target query | CTA | Status |
|----------|-----------|--------------|-----|--------|
| 1 | `/secplus/pbq-practice-browser.html` | security+ pbq practice · sy0-701 performance based | Free dark web PBQ → 10-day pass | **Live** |
| 2 | `/secplus/timed-practice-test.html` | security+ timed practice test online | Free samples → 10-day pass | Build |
| 3 | `/secplus/federal-8140-prep.html` | security+ dod 8140 · federal contractor | Free samples → 10-day pass | Build |
| 4 | `/secplus/exam-readiness.html` | security+ exam readiness / final review | Free samples → 10-day pass | Build |

**Live wedge URL for ads:** `https://becertifiedtoday.com/secplus/pbq-practice-browser.html?utm_content=pbq-wedge`

**Existing assets to link:** `/secplus-sample?track=questions`, `/secplus-sample?track=sim-dark-web`, `comptia-sec+-home.html#purchase?utm_content=portal-10d`

---

## Video ideas (2–3 min each)

Screen recording beats talking head for this product.

| # | Title | Show |
|---|-------|------|
| 1 | CCNA VLAN lab in your browser — no Packet Tracer | VLAN sample end-to-end |
| 2 | What our 120-minute CCNA timed sim looks like | Start sim, mixed item types |
| 3 | Drag-and-drop CCNA practice (exam-style) | D&D sample |
| 4 | Free CCNA assessment — scorecard in 15 minutes | Free assessment flow |
| 5 | ENCOR ACL lab without GNS3 | ENCOR lab sample |
| 6 | Security+ dark web PBQ in browser — no download | Dark web IR sample end-to-end |
| 7 | 90-minute Security+ timed sim walkthrough | Start sim, MCQ + PBQ mix |

Host: YouTube → embed on wedge landing pages → link to site CTA.

---

## Blog / long-form (optional)

Same topics as landing pages, 800–1,200 words:

- “CCNA labs without GNS3 or Packet Tracer (step-by-step)”
- “How to use a timed CCNA practice test the week before your exam”
- “CCNA V_2025 vs 2.0: what to practice”

Canonical URL = landing page; blog can syndicate or live under `/blog/` with canonical tag.

---

## Page template (each wedge page)

1. **H1** — matches ad keyword intent
2. **60-second proof** — screenshot or embedded video
3. **3 bullets** — browser labs, timed sim, verified answers
4. **Free CTA** — sample or assessment
5. **Paid CTA** — 10-day $9.99 (CCNA) or 30-day $19.99 (ENCOR)
6. **FAQ** — no GNS3? one-time payment? phone/tablet?

---

## Repo implementation (when ready)

| Task | Location |
|------|----------|
| New static pages | `public/ccna/…` or `public/CCNA-Study/…` |
| Hub links | `ccna-home.html`, `ccnp-home.html` footer or compare section |
| UTM landing JS | extend `ccna-portal-10d-landing.js` or per-page |
| Sitemap | add URLs for indexing |

---

## SEO vs Ads

| Channel | Role |
|---------|------|
| **Ads** | Wedge keywords → dedicated landing URLs |
| **SEO** | Same pages rank long-tail; lower CAC over time |
| **YouTube** | Demo trust; link to free sample |

Do not rely on SEO alone for 2–3 week audience — they search high-intent terms now; Ads + wedge pages capture them.

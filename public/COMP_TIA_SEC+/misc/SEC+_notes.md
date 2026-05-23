# CompTIA Security+ (SY0-701) — project notes

Internal notes for building the Security+ track on Be Certified Today. Not linked from the public site.

## Folder layout

```
public/COMP_TIA_SEC+/
├── SEC+_Questions/       # Full question bank (HTML pages)
├── SEC+_Labs/            # Interactive / scenario labs (if used)
├── SEC+_D_D/             # Drag-and-drop (PBQ-style) items
├── SEC+_Samples/         # Public sample questions + sample router
├── SEC+_Training_Portal.html
├── assets/  css/  js/  data/  images/
└── misc/                 # This file and other planning notes
```

## Public entry points

| URL | File |
|-----|------|
| `/secplus-home.html` | Compact study hub (sample links) |
| `/comptia-sec+-home.html` | Full CCNA-style landing page (staging, `noindex`) |
| `/secplus-sample` | *(rewrite removed — not public yet)* |
| `/COMP_TIA_SEC+/SEC+_Training_Portal.html` | Full CCNA-style training portal (staging) |

Home page path card: `/` → **Coming Soon in June** (disabled; no public hub link yet).

**Production:** Security+ and migrated ENCOR files live under `public/` for staging only. Hub links and `/sample` ENCOR tracks stay on the external ENCOR app until cutover.

## Live today (early access)

- 3 sample MCQs in `SEC+_Samples/` (MFA, AES, phishing)
- Training portal with “coming soon” for drag-and-drop and timed simulation
- Empty scaffold folders for questions, labs, D&D, `data/`, `js/`

## SY0-701 exam domains (reference)

Weights from CompTIA Security+ SY0-701 Exam Objectives v5.0 (`misc/CompTIA-Security-Plus-SY0-701-Exam-Objectives.pdf`):

| Domain | Weight |
|--------|--------|
| 1.0 General Security Concepts | 12% |
| 2.0 Threats, Vulnerabilities, and Mitigations | 22% |
| 3.0 Security Architecture | 18% |
| 4.0 Security Operations | 28% |
| 5.0 Security Program Management and Oversight | 20% |

Exam format: up to **90 questions** in **90 minutes** (multiple-choice + performance-based).

Use these when tagging questions in a future `data/secplus-question-topic-map.json` (mirror CCNA pattern under `CCNA-Study/data/`).

## TODO — content

- [ ] Question bank in `SEC+_Questions/`
- [ ] Drag-and-drop set in `SEC+_D_D/`
- [ ] Timed simulation blueprint + runner pages
- [ ] Topic map JSON + objective tracker (optional)
- [ ] Purchase / access window (Stripe) when ready to sell

## TODO — engineering

- [ ] Update internal links in migrated content to use `/COMP_TIA_SEC+/…` paths (if any ENCOR-style assets are reused)
- [ ] `study-config.json` generator for Security+ question IDs (mirror `scripts/build-study-config.py`)
- [ ] Hub copy on `index.html` / `secplus-home.html` when full library launches
- [ ] Replace “coming soon” badges on portal when modes go live

## Sample question chain

1. `sample-question-1.html` — MFA  
2. `sample-question-2.html` — AES  
3. `sample-question-3.html` — Phishing → back to `/secplus-home.html`

## Conventions (match CCNA / ENCOR)

- Sample pages: `noindex`, purple accent (`#6d28d9`), `secplus-sample-touch.css`
- Official exam objectives only for answer keys — no dump sites in HTML
- Run `python3 scripts/lint-practice-question-urls.py` after adding external links to question pages

## Related paths elsewhere on site

- CCNA: `public/CCNA-Study/`, `/ccna-home.html`
- CCNP ENCOR: `public/CCNP-ENCOR-Study/`, `/ccnp-home.html`

---

_Add dated notes below as the course is built._

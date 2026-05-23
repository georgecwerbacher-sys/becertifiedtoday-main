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
| `/secplus-home.html` | Study hub (marketing + sample links) |
| `/secplus-sample` | Rewrite → `SEC+_Samples/sample.html` |
| `/COMP_TIA_SEC+/SEC+_Training_Portal.html` | Portal shell |

Home page path card: `/` → **Open Security+ Study Hub** → `/secplus-home.html`

## Live today (early access)

- 3 sample MCQs in `SEC+_Samples/` (MFA, AES, phishing)
- Training portal with “coming soon” for drag-and-drop and timed simulation
- Empty scaffold folders for questions, labs, D&D, `data/`, `js/`

## SY0-701 exam domains (reference)

1. General Security Concepts
2. Threats, Vulnerabilities, and Mitigations
3. Security Architecture
4. Security Operations
5. Security Program Management and Oversight

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

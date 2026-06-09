---
type: landing-page
url: /ccna-home.html
canonical: https://becertifiedtoday.com/ccna-home.html
campaign: ccna_portal
status: active
repo_file: public/ccna-home.html
last_audit: 2026-05-30
quality_score_notes: Active Google Ads landing; headline variants via ccna-home-conversion.js
---

# ccna-home.html — CCNA ad landing (CTA)

Primary **Google Ads final URL** for [[../../02-campaigns/ccna/ccna-portal-google-ads|CCNA campaign]].

Alias: `/ccna/practice-test` → same HTML (Vercel rewrite).

## Live URLs

- `https://becertifiedtoday.com/ccna-home.html`
- `https://becertifiedtoday.com/ccna/practice-test`
- Purchase: `…/ccna-home.html#purchase`
- UTMs: `utm_campaign=ccna_portal`

## Headline pinning

Ad `utm_content=hl-free-practice` etc. maps to variants in `public/js/ccna-home-conversion.js`. See `scripts/ccna-google-ads-headline-suffixes.txt`.

## Current message (prod 2026-06-04)

- **H1:** CCNA 200-301 Exam Prep: Practice Tests & Simulation (variants via `ccna-home-conversion.js` may override)
- **Lead:** You-focused exam prep; browser-only; federal context with “confirm with your manager”
- **Writing rules:** [[../../12-Writing/_Writing-Rules|Guest page writing rules]] applied 2026-06-04
- **Samples:** 2 MCQ per run on `/sample?track=ccna-questions`; D&D and VLAN lab samples on-page
- **Primary CTA (default):** 30-day portal on `#purchase`; free samples below
- **Primary CTA (`utm_content=portal-10d`):** **$9.99 / 10-day** only in purchase fold — Ads config: `scripts/ccna-portal-10d-google-ads.md`

## Keywords

[[../../07-keywords/landing-maps/ccna-portal|CCNA landing map]] · [[../../01-strategy/cisco-certifications-exam-prep-foundation|Cisco foundation]]

## Open items

- [ ] Search terms import: `07-keywords/search-terms/YYYY-MM-DD-ccna_portal.md`
- [ ] Geo ad groups `cisco-dc`, `cisco-cos` with bid modifiers
- [ ] PageSpeed mobile baseline

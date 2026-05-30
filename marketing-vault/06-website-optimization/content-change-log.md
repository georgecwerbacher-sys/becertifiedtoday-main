---
type: change-log
---

# Site content change log

Master log of **website optimizations** for Google Ads landing page experience and conversion. One row per meaningful deploy.

Implement changes in Cursor under `public/`. Link to page notes in `06-website-optimization/pages/`.

| Date | Page (path) | Change summary | Reason (QS / CVR / UX) | Campaign | Deployed | Ads LP exp. (before→after) |
|------|-------------|----------------|------------------------|----------|----------|----------------------------|
| 2026-05-30 | `/ccnp-home.html` | ENCOR CTA landing: exam prep meta/hero; documented as primary Ads URL (not secplus-home) | Google Ads message match — encor_portal | encor_portal | no |
| 2026-05-30 | `/secplus-home.html`, Security+ samples | Legacy hub: noindex; samples finish at `comptia-sec+-home.html` | Security+ Ads must use comptia-sec+-home, not secplus-home | secplus_portal | no |
| 2026-05-30 | Site-wide CCNA (`ccna-home.html`, `ccna-home-conversion.js`) | Removed “no email required” / “membership or email required” from hero, meta, and ad headline variants | Prepare for email capture on free assessment; align copy with exam prep | ccna_portal | no | |
| 2026-05-30 | `/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/simulation-secure-web-architecture-openssl.html` | CTA landing: SY0-701 PBQ exam prep copy, SEO meta/JSON-LD, on-page CTAs (sample + purchase), Obsidian keyword/negative lists | PBQ/openssl ad group message match + mid-funnel conversion | secplus_openssl_pbq | no | |
| 2026-05-30 | `/comptia-sec+-home.html` | Exam prep positioning: H1/lead/benefits, 5 new FAQs + JSON-LD, meta/OG copy, “practice portal” labels, removed “goes live” / training language | Google Ads QS + AI search + message match (secplus_portal) | secplus_portal | yes — 2026-05-30 prod (`becertifiedtoday.com`) | |
| | | | | | | |

---

## How to use

1. Before editing: run [[landing-page-audit-checklist|landing page audit]] on the target URL
2. After deploy: add a row above
3. ~7–14 days later: update **Ads LP exp.** from Google Ads keyword report
4. Tie major changes to [[../02-campaigns/security-plus-google-ads#Decisions log|Security+ campaign decisions log]]

---

## Pending optimizations (backlog)

- [x] **Positioning pass** on `/comptia-sec+-home.html` — shipped 2026-05-30
- [x] **FAQ section** for AI search + Quality Score — shipped 2026-05-30
- [ ] PageSpeed mobile score baseline recorded
- [ ] Compare GA4 engagement before/after deploy (+7 days)

Move items to the table when shipped.

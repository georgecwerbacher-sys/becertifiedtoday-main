---
type: change-log
---

# Site content change log

Master log of **website optimizations** for Google Ads landing page experience and conversion. One row per meaningful deploy.

Implement changes in Cursor under `public/`. Link to page notes in `06-website-optimization/pages/`.

| Date | Page (path) | Change summary | Reason (QS / CVR / UX) | Campaign | Deployed | Ads LP exp. (before→after) |
|------|-------------|----------------|------------------------|----------|----------|----------------------------|
| 2026-05-30 | `/ccna-home.html` | Exam prep meta/title; `#exam-audience` (people, when, where); federal/contractor keywords | Active ccna_portal Ads — message match + contractor segment | ccna_portal | no |
| 2026-05-30 | `/ccnp-home.html` | `#exam-audience` section; federal/contractor lead + keywords; vault campaign docs active | Active encor_portal Ads — same guidelines as Security+ | encor_portal | no |
| 2026-05-30 | `marketing-vault/` | Cisco exam prep foundation; CCNA/ENCOR campaign + keyword maps marked **active** | User runs CCNA + ENCOR Ads alongside Security+ | ccna_portal, encor_portal | no |
| 2026-05-30 | `/ccnp-home.html` | ENCOR CTA landing: exam prep meta/hero; documented as primary Ads URL (not secplus-home) | Google Ads message match — encor_portal | encor_portal | no |
| 2026-05-30 | `/secplus-home.html`, Security+ samples | Legacy hub: noindex; samples finish at `comptia-sec+-home.html` | Security+ Ads must use comptia-sec+-home, not secplus-home | secplus_portal | no |
| 2026-05-30 | Site-wide CCNA (`ccna-home.html`, `ccna-home-conversion.js`) | Removed “no email required” / “membership or email required” from hero, meta, and ad headline variants | Prepare for email capture on free assessment; align copy with exam prep | ccna_portal | no | |
| 2026-05-30 | `/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/simulation-secure-web-architecture-openssl.html` | CTA landing: SY0-701 PBQ exam prep copy, SEO meta/JSON-LD, on-page CTAs (sample + purchase), Obsidian keyword/negative lists | PBQ/openssl ad group message match + mid-funnel conversion | secplus_openssl_pbq | no | |
| 2026-05-30 | `/comptia-sec+-home.html` | Federal/DoD/defense-contractor section (people, when, where) + FAQs + meta/JSON-LD | High-intent compliance segment; geo ad foundation | secplus_portal | no |
| 2026-05-30 | `/comptia-sec+-home.html` | Exam prep positioning: H1/lead/benefits, 5 new FAQs + JSON-LD, meta/OG copy, “practice portal” labels, removed “goes live” / training language | Google Ads QS + AI search + message match (secplus_portal) | secplus_portal | yes — 2026-05-30 prod (`becertifiedtoday.com`) | |
| 2026-05-30 | `/comptia-sec+-home.html`, `test-simulation-runner.html` | Free 35-min sim lead magnet; $9.99 timed sim; Back + mark for review; landing images (relative paths); federal section removed; lead CSV | Campaign launch readiness — secplus_lead_free_sim funnel | secplus_portal | yes — 2026-05-30 prod | |
| 2026-05-30 | `marketing-vault/02-campaigns/` | Paste-ready Google Ads export (RSA + keywords per ad group) | Campaign build in Ads UI | secplus_portal | n/a | |
| 2026-05-31 | `/index.html` | Exam prep title/H1/meta; track cards → public landing pages (not gated portals); OG + JSON-LD; removed training-path language | SEO + positioning — exam prep not courses | all | no | |
| 2026-05-31 | `/*Training_Portal.html`, `/secplus-home.html` | noindex/nofollow on gated portals; legacy secplus-home canonical → comptia-sec+-home | Keep crawl budget on exam prep landings | all | no | |
| 2026-05-31 | `robots.txt`, `sitemap.xml` | Disallow portals + legacy hub; sitemap prioritizes home pages + free assessment + OpenSSL PBQ; removed secplus-home | Crawl/index hygiene | all | no | |
| 2026-05-31 | `/comptia-sec+-home.html`, sample JS | Homepage sample questions reduced to 2 MCQ; finish upsell modal → in-page free timed sim lead capture | Sample → lead magnet funnel | secplus_portal | no | |
| 2026-05-31 | Guest sitemap pages (`CCNA_Samples/`, `ENCOR_Samples/`, `SEC+_Samples/`, free assessment, sim landings, sample labs) | Exam prep meta descriptions, canonicals, home links → public landings; disclaimer “exam prep resource”; campaign attribution on injected gtag | AI search + Ads sample funnel — positioning from 01-strategy | all | no | |

---

## How to use

1. Before editing: run [[landing-page-audit-checklist|landing page audit]] on the target URL
2. After deploy: add a row above
3. ~7–14 days later: update **Ads LP exp.** from Google Ads keyword report
4. Tie major changes to [[../02-campaigns/security-plus/security-plus-google-ads#Decisions log|Security+ campaign decisions log]]

---

## Pending optimizations (backlog)

- [x] **Positioning pass** on `/comptia-sec+-home.html` — shipped 2026-05-30
- [x] **FAQ section** for AI search + Quality Score — shipped 2026-05-30
- [ ] PageSpeed mobile score baseline recorded
- [ ] Compare GA4 engagement before/after deploy (+7 days)

Move items to the table when shipped.

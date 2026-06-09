---
type: campaign
channel: google-ads
product: ccna-200-301
status: active
launch_priority: 2
priority: 1
target_cpa: null
daily_budget_usd: 10
utm_campaign: ccna_portal
utm_source: google
utm_medium: cpc
landing_pages:
  - /ccna-home.html
  - /ccna/practice-test
  - /ccna-home.html#purchase
  - /ccna-home.html#exam-audience
sample_entry:
  - /sample?track=ccna-questions
  - /sample?track=ccna-dnd
related_reports: []
---

# CCNA 200-301 — Google Ads (active)

Primary paid campaign for **Cisco CCNA 200-301** exam prep on Be Certified Today.

**Positioning reminder:** [[../../01-strategy/positioning-and-messaging|Exam prep only]] — target people practicing for test day, not course shoppers. See [[../../01-strategy/google-ai-search-strategy|AI search strategy]] for FAQ/structured content that supports the same keywords.

## Objective

Send high-intent 200-301 **exam prep** traffic to the landing page. Convert via:

1. **Direct purchase** — **10-day $9.99** portal access (primary paid CTA for Ads)
2. **Free samples** — 2 shuffled MCQ per track, drag-and-drop, VLAN lab (no checkout; on-page trust, not a paid ad group)
3. **Optional upsells** — 30-day portal ($19.99) or standalone timed sim ($9.99) on `#purchase`

Optimize toward `begin_checkout` and purchases while building Quality Score.

## Primary landing URLs (use in Google Ads)

**Final URL — generic / brand:**

```
https://becertifiedtoday.com/ccna-home.html?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content={creative}
```

Alias (same page — Vercel rewrite):

```
https://becertifiedtoday.com/ccna/practice-test?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content={creative}
```

**Pinned headline variants (home hero):**

```
https://becertifiedtoday.com/ccna-home.html?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=hl-free-practice
```

Pinned headline variants map to `utm_content=hl-*` → `ccna-home-conversion.js`. See `scripts/ccna-google-ads-headline-suffixes.txt`.

**Purchase intent — 10-day portal (`ccna_portal_10d`):**

```
https://becertifiedtoday.com/ccna-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=portal-10d
```

**Purchase intent — timed sim:**

```
https://becertifiedtoday.com/ccna-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=sim-purchase
```

**Federal / contractor (optional geo ad groups):**

```
https://becertifiedtoday.com/ccna-home.html#exam-audience?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=federal-dc
```

**Do not use** `/CCNA-Study/CCNA_Training_Portal.html` as final URL — gated; sends wrong message match.

`campaign-attribution.js` is loaded on `ccna-home.html` — UTM + `gclid` persist for the session in GA4.

## Recommended ad group structure

| Ad group | Final URL / anchor | Intent | Start spend? |
|----------|-------------------|--------|:------------:|
| `ccna_portal_10d` | `#purchase` + `portal-10d` | **10-day $9.99** portal access | **Yes** — primary paid CTA · config: `scripts/ccna-portal-10d-google-ads.md` |
| `ccna_sim_purchase` | `#purchase` + `sim-purchase` | Timed simulation, exam sim | Optional — tight keywords |
| `ccna_portal_access` | `#purchase` + `portal-access` | Dual-tier 10d/30d (legacy) | Paused — use `ccna_portal_10d` |
| `ccna_labs_pbq` | Home (samples section) | Drag-and-drop, CLI lab practice | Optional mid-funnel |
| `ccna_federal_*` | Home or `#exam-audience` | DoD / 8140 / contractor | Optional geo campaigns |

**Paste-ready RSA + keywords:** [[ccna-portal-google-ads-export|CCNA Google Ads export]].

## Funnel map

| Stage | Page / action | GA4 signal |
|-------|----------------|------------|
| Click | Google Ads → `ccna-home.html#purchase` | Session with `utm_campaign=ccna_portal` |
| Free samples (on-page) | 2 MCQ / D&D / lab tracks (no checkout) | Sample completion |
| Try free sample (no checkout) | `/sample?track=ccna-*` or in-page sample CTAs | Page views, engagement |
| Begin checkout | Portal 10d / 30d buttons on `#purchase` | `begin_checkout` |
| Purchase | Stripe Payment Link | Stripe + portal metadata; Google Ads conversion if configured |
| Post-purchase | `/CCNA-Study/CCNA_Training_Portal.html` | Portal engagement |

## Products & checkout tracking

| Offer | Price | GA4 `item_id` | Stripe / checkout |
|-------|------:|---------------|-------------------|
| 10-day portal | $9.99 | `ccna_portal_10d` | `data-ccna-portal-10d-checkout` |
| 30-day portal | $19.99 | `ccna_portal_30d` | `data-ccna-portal-30d-checkout` |
| Timed simulation | $9.99 | `ccna_timed_simulation` | `data-bcc-item-id` on sim checkout |

Checkout wiring: `public/CCNA-Study/js/ccna-portal-30d-checkout.js`, `ccna-test-checkout.js`.

Post-purchase: portal access at `/CCNA-Study/CCNA_Training_Portal.html` (gated — not an ad final URL).

## Secondary pages (organic / retargeting — not primary ad landings)

- `/ccna-home.html` / `/ccna/practice-test` — **only** CCNA Google Ads final URL (exam prep + purchase + free samples).
- `/CCNA-Study/CCNA_Training_Portal.html` — gated practice hub (post-purchase; not an ad final URL).
- CCNP ENCOR ads → `/ccnp-home.html` — see [[../encor/ccnp-encor-google-ads|ENCOR campaign]] (not this CCNA campaign).

## Keywords & angles (draft)

Intent themes to test in ad groups — **prep / practice / simulation**, not course:

| Ad group | Keywords (examples) | Lead message |
|----------|---------------------|--------------|
| Portal 10d | ccna question bank, ccna practice test online, ccna 200-301 prep | $9.99 / 10-day full library + timed sim |
| Practice test | ccna practice questions, cisco ccna practice test | Verified explanations — not PDF dumps |
| Simulation purchase | ccna exam simulation, ccna mock exam timed | 120-min sim, 50 MCQ + D&D + lab, $9.99 |
| Retake / readiness | pass ccna first try, ccna exam prep | Exam-realistic format — save retake fees |
| Labs / PBQ | ccna drag and drop, ccna cli lab practice | Browser labs — no GNS3 required |
| Federal / DoD | ccna federal job, ccna defense contractor | Browser 200-301 prep — see [[../../01-strategy/cisco-certifications-exam-prep-foundation\|Cisco foundation]] |

### Geo targeting (federal/defense ad groups)

Use with `utm_content=federal-{market}` or `cisco-{market}` for reporting. Details: [[../../01-strategy/cisco-certifications-exam-prep-foundation#Shared geo ad groups|geo table]].

| Ad group (draft) | Priority geos | UTM content example |
|------------------|---------------|---------------------|
| `ccna_federal_dc` | DC + NoVA + MD inner beltway | `federal-dc` |
| `ccna_federal_cos` | Colorado Springs | `federal-cos` |
| `ccna_federal_satx` | San Antonio | `federal-satx` |
| `ccna_federal_norfolk` | Norfolk / Hampton Roads | `federal-norfolk` |

National non-geo campaigns still run for generic `ccna practice test` keywords.

**Negative keyword ideas:** free course, bootcamp, training program, dump, guaranteed pass, pdf download, netacad, gns3 course — full lists on [[../../07-keywords/landing-maps/ccna-portal#Negatives|CCNA landing map]] and export below.

**Campaign-level negatives (phrase match unless noted):** free course, training course, bootcamp, instructor led, brain dump, exam dump, guaranteed pass, pdf download, udemy, coursera, cbt nuggets, ine ccna, cisco netacad, jobs, salary, ccnp encor, ccie, comptia security+

Message angles (aligned with [[../../01-strategy/positioning-and-messaging|positioning]]):

- **Exam-realistic** — timed simulation, drag-and-drop, CLI lab items
- **Verified solutions** — prep you can trust, not unvetted dumps
- **Browser-only** — no PDF, no GNS3, no third-party software
- **Free samples** — shuffled MCQ, D&D, VLAN lab previews before checkout
- **Confidence / economics** — practice until ready; $9.99 portal vs retake cost
- **Not a course** — say “exam prep” and “practice” in headlines; avoid “training program”

### Headline / description drafts (policy-safe)

**Portal 10d (`#purchase` + `portal-10d`):**

- H1 (on page): `CCNA 200-301 Exam Prep: Practice Tests & Simulation` (variant via `ccna-home-conversion.js`)
- Ad headline 1: `CCNA 200-301 Practice Test`
- Ad headline 2: `$9.99 for 10-Day Access`
- Ad headline 3: `CCNA 200-301 Exam Prep`
- Description: `700+ CCNA 200-301 practice questions, labs & D&D. $9.99 for 10-day access. Browser-only—no PDFs.`

**Sim purchase (`#purchase` + `sim-purchase`):**

- `120-Min CCNA Exam Simulation`
- `CCNA Timed Practice — $9.99`
- `50 Questions + D&D + CLI Lab`
- `Study Scorecard by Domain`

## AI search alignment

Landing page must answer AI-style questions clearly (see [[../../01-strategy/google-ai-search-strategy|FAQ bank]]):

- [x] FAQ section on landing page implemented
- [x] H1/lead use “exam prep” not “training course”
- [x] Meta description mentions browser-based + practice test + 200-301
- [x] Free sample questions + purchase fold live

## Tracking checklist

- [ ] Final URLs include `utm_campaign=ccna_portal` (or ad-group-specific `utm_content`)
- [ ] Google Ads conversion: `begin_checkout` (primary) + purchase (secondary)
- [ ] Weekly report: filter GA4 by campaign name matching `ccna*`
- [ ] Stripe Payment Link confirms **$9.99** for portal 10d and timed sim in Dashboard
- [ ] Stripe portal subscribers visible in `/admin` (CCNA product metadata)
- [ ] Landing page audits in [[../../06-website-optimization/landing-page-audit-checklist|audit checklist]] — log changes in [[../../06-website-optimization/content-change-log|content change log]]
- [ ] Align `scripts/ccna-google-ads-headline-suffixes.txt` UTM campaign to `ccna_portal` (file still shows `ccna-practice-test`)

## Landing page optimization

Primary page tracker: [[../../06-website-optimization/pages/ccna-home|ccna-home.html]].

Before major ad spend increases, run the optimization workflow in [[../../06-website-optimization/README|06-website-optimization]].

**Known LP items (2026-05-31):**

- Headline pinning via `utm_content=hl-*` → `ccna-home-conversion.js` (14 variants)
- Primary ATF CTA (`portal-10d` UTM): **$9.99 / 10-day** purchase; free samples below fold
- `#exam-audience` section for federal/contractor message match

## Creative / ad copy notes

- Full RSA sets, keywords, negatives, extensions: [[ccna-portal-google-ads-export|paste-ready export]]
- Launch with **`ccna_portal_10d`** only at $10/day; add **`ccna_sim_purchase`** after baseline CPA
- Pin purchase URL to `#purchase` + `portal-10d` for primary ad group

## Decisions log

| Date | Change | Rationale |
|------|--------|-----------|
| 2026-06-09 | Removed **`ccna_lead_free_sim`** ad group from campaign plan | Paid Ads funnel = direct purchase (`ccna_portal_10d`); free sim stays on-site only, not a Search ad group |
| 2026-06-06 | New ad group **`ccna_portal_10d`** — `portal-10d` UTM, site purchase fold = single $9.99 / 10-day CTA | Message match for paid portal intent; reduce choice paralysis vs dual-tier |
| 2026-05-31 | Vault sync: Security+ playbook structure — ad groups, funnel, export, tracking checklist | Align active CCNA ads with proven Security+ campaign workflow |
| 2026-05-30 | Active campaign doc; landing = `ccna-home.html` | User running CCNA ads; align with ENCOR/Security+ playbook |
| 2026-05-30 | Removed training portal as ad final URL | Message match + conversion path |

## Open questions

- **Launch strategy:** **`ccna_portal_10d` only** at $10/day; add `ccna_sim_purchase` after ~5 `begin_checkout` events in 7 days
- **Target CPA:** See [[../../01-strategy/google-ads-bidding-strategy#Phase 2 — After 30+ conversions / product (efficiency)|bidding strategy]] — sim ~$8–12, portal ~$15–22
- **Daily budget:** **$10/day** — one campaign; defer Visibility/Convert split until **$20+/day** per [[../../01-strategy/google-ads-bidding-strategy|bidding strategy]]
- **Brand vs non-brand:** Start non-brand only; add brand campaign when search volume warrants
- **UTM campaign name:** Standardize on `ccna_portal` everywhere (headline suffixes file still uses `ccna-practice-test`)

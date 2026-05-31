---
type: campaign
channel: google-ads
product: ccna-200-301
status: active
priority: 1
target_cpa: null
utm_campaign: ccna_portal
utm_source: google
utm_medium: cpc
landing_pages:
  - /ccna-home.html
  - /ccna/practice-test
  - /ccna-home.html#purchase
  - /ccna-home.html#exam-audience
  - /CCNA_Sim_EXAM/free-assessment.html
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

1. **Free assessment** — 35-min browser diagnostic + domain scorecard (no email gate; one attempt per browser)
2. **Direct purchase** — $4.99 timed sim, 10-day, or 30-day portal access

Optimize toward `ccna_free_assessment_click`, `begin_checkout`, and purchases while building Quality Score.

## Primary landing URLs (use in Google Ads)

**Final URL — generic / brand:**

```
https://becertifiedtoday.com/ccna-home.html?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content={creative}
```

Alias (same page — Vercel rewrite):

```
https://becertifiedtoday.com/ccna/practice-test?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content={creative}
```

**Free assessment (top-of-funnel ad group):**

```
https://becertifiedtoday.com/ccna-home.html?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=hl-free-practice
```

Pinned headline variants map to `utm_content=hl-*` → `ccna-home-conversion.js`. See `scripts/ccna-google-ads-headline-suffixes.txt`.

**Tighter message-match option (A/B):** send free-practice keywords directly to the assessment runner:

```
https://becertifiedtoday.com/CCNA_Sim_EXAM/free-assessment.html?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=free-assessment
```

**Purchase intent (sim / portal ad groups):**

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
| `ccna_free_assessment` | Home + `utm_content=hl-free-practice` | Practice test, mock exam, free CCNA | **Yes** — primary launch |
| `ccna_sim_purchase` | `#purchase` | Timed simulation, exam sim | Yes — tight keywords |
| `ccna_portal_access` | `#purchase` | Multi-day study access | After baseline data |
| `ccna_labs_pbq` | Home (samples section) | Drag-and-drop, CLI lab practice | Optional mid-funnel |
| `ccna_federal_*` | Home or `#exam-audience` | DoD / 8140 / contractor | Optional geo campaigns |

**Paste-ready RSA + keywords:** [[ccna-portal-google-ads-export|CCNA Google Ads export]].

## Funnel map

| Stage | Page / action | GA4 signal |
|-------|----------------|------------|
| Click | Google Ads → `ccna-home.html` | Session with `utm_campaign=ccna_portal` |
| Free assessment start | Hero CTA → `/CCNA_Sim_EXAM/free-assessment.html` | `ccna_free_assessment_click` |
| Free assessment | 35 min · 17 items (12 MCQ + 4 D&D + 1 VLAN lab) | Engagement, completion |
| Scorecard | Domain + objective breakdown on results | Scorecard render |
| Upsell | Results modal or `#purchase` | `begin_checkout` |
| Try free sample (no checkout) | `/sample?track=ccna-*` or in-page sample CTAs | Page views, engagement |
| Begin checkout | Portal 10d / 30d or timed sim buttons | `begin_checkout` |
| Purchase | Stripe Payment Link | Stripe + portal metadata; Google Ads conversion if configured |

Blueprint: `public/CCNA-Study/data/ccna-free-assessment-blueprint.json`  
Runner: `public/CCNA_Sim_EXAM/free-assessment.html`

## Products & checkout tracking

| Offer | Price | GA4 `item_id` | Stripe / checkout |
|-------|------:|---------------|-------------------|
| 10-day portal | $9.99 | `ccna_portal_10d` | `data-ccna-portal-10d-checkout` |
| 30-day portal | $19.99 | `ccna_portal_30d` | `data-ccna-portal-30d-checkout` |
| Timed simulation | $4.99 | `ccna_timed_simulation` | `data-bcc-item-id` on sim checkout |
| Free assessment | $0 | — | One attempt per browser (localStorage) |

Checkout wiring: `public/CCNA-Study/js/ccna-portal-30d-checkout.js`, `ccna-test-checkout.js`.

Post-purchase: portal access at `/CCNA-Study/CCNA_Training_Portal.html` (gated — not an ad final URL).

## Secondary pages (organic / retargeting — not primary ad landings)

- `/ccna-home.html` / `/ccna/practice-test` — **only** CCNA Google Ads final URL (exam prep + purchase + free assessment CTA).
- `/CCNA_Sim_EXAM/free-assessment.html` — optional direct final URL for free-practice ad group A/B tests.
- `/CCNA-Study/CCNA_Training_Portal.html` — gated practice hub (checkout required).
- CCNP ENCOR ads → `/ccnp-home.html` — see [[../encor/ccnp-encor-google-ads|ENCOR campaign]] (not this CCNA campaign).

## Keywords & angles (draft)

Intent themes to test in ad groups — **prep / practice / simulation**, not course:

| Ad group | Keywords (examples) | Lead message |
|----------|---------------------|--------------|
| Free assessment | ccna practice test, ccna 200-301 practice exam, free ccna practice | Free 35-min assessment + domain scorecard |
| Practice test | ccna practice questions, cisco ccna practice test | Verified explanations — not PDF dumps |
| Simulation purchase | ccna exam simulation, ccna mock exam timed | 120-min sim, 50 MCQ + D&D + lab, $4.99 |
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
- **Free assessment** — 35 min, 17 items across all six domains, objective scorecard
- **Confidence / economics** — practice until ready; $4.99 full sim vs retake cost
- **Not a course** — say “exam prep” and “practice” in headlines; avoid “training program”

### Headline / description drafts (policy-safe)

**Generic / home landing:**

- H1 (on page): `Free CCNA Practice Assessment With Scorecard` (variant via `ccna-home-conversion.js`)
- Ad headline 1: `CCNA 200-301 Practice Test — In Browser`
- Ad headline 2: `Free CCNA Assessment + Scorecard`
- Ad headline 3: `No GNS3 — CCNA Labs Online`
- Description: `Realistic CCNA 200-301 practice with verified explanations. Free 35-min assessment or full 120-minute sim. No downloads.`

**Sim purchase (`#purchase`):**

- `120-Min CCNA Exam Simulation`
- `CCNA Timed Practice — $4.99`
- `50 Questions + D&D + CLI Lab`
- `Study Scorecard by Domain`

## AI search alignment

Landing page must answer AI-style questions clearly (see [[../../01-strategy/google-ai-search-strategy|FAQ bank]]):

- [x] FAQ section on landing page implemented
- [x] H1/lead use “exam prep” not “training course”
- [x] Meta description mentions browser-based + practice test + 200-301
- [x] Free assessment + scorecard offer live

## Tracking checklist

- [ ] Final URLs include `utm_campaign=ccna_portal` (or ad-group-specific `utm_content`)
- [ ] Google Ads conversion: `ccna_free_assessment_click` (free group) + `begin_checkout` (purchase)
- [ ] Weekly report: filter GA4 by campaign name matching `ccna*`
- [ ] Stripe Payment Link confirms **$4.99** for timed sim in Dashboard
- [ ] Stripe portal subscribers visible in `/admin/analytics.html` (CCNA product metadata)
- [ ] Landing page audits in [[../../06-website-optimization/landing-page-audit-checklist|audit checklist]] — log changes in [[../../06-website-optimization/content-change-log|content change log]]
- [ ] Align `scripts/ccna-google-ads-headline-suffixes.txt` UTM campaign to `ccna_portal` (file still shows `ccna-practice-test`)

## Landing page optimization

Primary page tracker: [[../../06-website-optimization/pages/ccna-home|ccna-home.html]].

Before major ad spend increases, run the optimization workflow in [[../../06-website-optimization/README|06-website-optimization]].

**Known LP items (2026-05-31):**

- Headline pinning via `utm_content=hl-*` → `ccna-home-conversion.js` (14 variants)
- Primary ATF CTA: free assessment; purchase secondary ATF
- `#exam-audience` section for federal/contractor message match

## Creative / ad copy notes

- Full RSA sets, keywords, negatives, extensions: [[ccna-portal-google-ads-export|paste-ready export]]
- Launch with **`ccna_free_assessment`** + **`ccna_sim_purchase`** in parallel
- A/B: home landing (`hl-free-practice`) vs direct `/free-assessment.html` final URL
- Pin purchase URL to `#purchase` for sim ad group only

## Decisions log

| Date | Change | Rationale |
|------|--------|-----------|
| 2026-05-31 | Vault sync: Security+ playbook structure — ad groups, funnel, export, tracking checklist | Align active CCNA ads with proven Security+ campaign workflow |
| 2026-05-30 | Active campaign doc; landing = `ccna-home.html` | User running CCNA ads; align with ENCOR/Security+ playbook |
| 2026-05-30 | Removed training portal as ad final URL | Message match + conversion path |

## Open questions

- **Launch strategy:** Lead with `ccna_free_assessment` for 1–2 weeks, then scale `ccna_sim_purchase` on simulation keywords — **recommended default**
- **Target CPA:** TBD — compare free assessment → upsell vs direct `$4.99` sim vs `$19.99` portal
- **Brand vs non-brand:** Start non-brand only; add brand campaign when search volume warrants
- **Email lead magnet:** Security+ uses `#secplus-lead-capture` + `generate_lead`; CCNA is no-email today — evaluate email scorecard capture later for parity
- **UTM campaign name:** Standardize on `ccna_portal` everywhere (headline suffixes file still uses `ccna-practice-test`)

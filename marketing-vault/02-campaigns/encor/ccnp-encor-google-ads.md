---
type: campaign
channel: google-ads
product: encor-350-401
status: active
priority: 1
target_cpa: null
utm_campaign: encor_portal
utm_source: google
utm_medium: cpc
landing_pages:
  - /ccnp-home.html
  - /ccnp-home.html#purchase
  - /ccnp-home.html#exam-audience
sample_entry:
  - /sample?track=encor-questions
  - /sample?track=encor-dnd
  - /sample?track=labs
related_reports: []
---

# CCNP ENCOR 350-401 — Google Ads (active)

Primary paid campaign for **CCNP ENCOR 350-401** exam prep on Be Certified Today.

**Positioning reminder:** [[../../01-strategy/positioning-and-messaging|Exam prep only]] — target people practicing for test day, not course shoppers. See [[../../01-strategy/google-ai-search-strategy|AI search strategy]] for FAQ/structured content that supports the same keywords.

**Do not send ads to** `/secplus-home.html`. Security+ → `/comptia-sec+-home.html`.

## Objective

Send high-intent 350-401 **exam prep** traffic to the landing page. Convert via:

1. **Free samples** — shuffled ENCOR questions, drag-and-drop, and CLI lab (no checkout or email gate)
2. **Direct purchase** — $4.99 timed sim, 10-day, or 30-day portal access

Optimize toward sample engagement, `begin_checkout`, and purchases while building Quality Score.

## Primary landing URLs (use in Google Ads)

**Final URL — generic / brand:**

```
https://becertifiedtoday.com/ccnp-home.html?utm_source=google&utm_medium=cpc&utm_campaign=encor_portal&utm_content={creative}
```

**Free samples (top-of-funnel ad group):**

```
https://becertifiedtoday.com/ccnp-home.html?utm_source=google&utm_medium=cpc&utm_campaign=encor_portal&utm_content=free-samples
```

**Tighter message-match option (A/B):** send practice-test keywords directly to sample questions:

```
https://becertifiedtoday.com/sample?track=encor-questions&utm_source=google&utm_medium=cpc&utm_campaign=encor_portal&utm_content=sample-questions
```

**Purchase intent (sim / portal ad groups):**

```
https://becertifiedtoday.com/ccnp-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=encor_portal&utm_content=sim-purchase
```

**Federal / contractor (optional geo ad groups):**

```
https://becertifiedtoday.com/ccnp-home.html#exam-audience?utm_source=google&utm_medium=cpc&utm_campaign=encor_portal&utm_content=federal-dc
```

**Do not use** `/CCNP-ENCOR-Study/ENCOR_Training_Portal.html` as final URL — gated; sends wrong message match.

`campaign-attribution.js` is loaded on `ccnp-home.html` — UTM + `gclid` persist for the session in GA4.

## Recommended ad group structure

| Ad group | Final URL / anchor | Intent | Start spend? |
|----------|-------------------|--------|:------------:|
| `encor_free_samples` | Home + `utm_content=free-samples` | Practice test, mock exam, free ENCOR | **Yes** — primary launch |
| `encor_sim_purchase` | `#purchase` | Timed simulation, exam sim | Yes — tight keywords |
| `encor_portal_access` | `#purchase` | Multi-day study access | After baseline data |
| `encor_labs_pbq` | Home (samples section) | CLI lab, drag-and-drop practice | Optional mid-funnel |
| `encor_federal_*` | Home or `#exam-audience` | DoD / 8140 / contractor | Optional geo campaigns |

**Paste-ready RSA + keywords:** [[ccnp-encor-google-ads-export|ENCOR Google Ads export]].

## Funnel map

| Stage | Page / action | GA4 signal |
|-------|----------------|------------|
| Click | Google Ads → `ccnp-home.html` | Session with `utm_campaign=encor_portal` |
| Free sample | `/sample?track=encor-questions` · `encor-dnd` · `labs` | Engagement, page views |
| Sample activity | 12 MCQ shuffled · D&D · ACL/CoPP CLI lab | Sample completion |
| Upsell | `#purchase` or sticky promo | `begin_checkout` |
| Begin checkout | Portal 10d / 30d or timed sim buttons | `begin_checkout` |
| Purchase | Stripe Payment Link | Stripe + portal metadata; Google Ads conversion if configured |

Sample tracks: `/sample?track=encor-questions`, `/sample?track=encor-dnd`, `/sample?track=labs`

## Products & checkout tracking

| Offer | Price | GA4 `item_id` | Stripe / checkout |
|-------|------:|---------------|-------------------|
| 10-day portal | $9.99 | `encor_portal_10d` | `data-encor-portal-10d-checkout` |
| 30-day portal | $19.99 | `encor_portal_30d` | `data-encor-portal-30d-checkout` |
| Timed simulation | $4.99 | `encor_timed_simulation` | `data-encor-test-sim-checkout` |
| Free samples | $0 | — | No checkout; shuffled guest samples |

Checkout wiring: `public/CCNP-ENCOR-Study/js/encor-portal-30d-checkout.js`, `encor-test-checkout.js` (calls `bccTrackBeginCheckout`).

Post-purchase: portal access at `/CCNP-ENCOR-Study/ENCOR_Training_Portal.html` (gated — not an ad final URL). Timed sim runner: `test-simulation.html`.

## Secondary pages (organic / retargeting — not primary ad landings)

- `/ccnp-home.html` — **only** ENCOR Google Ads final URL (exam prep + purchase + free samples).
- `/sample?track=encor-*` — optional direct final URL for free-practice ad group A/B tests.
- `/CCNP-ENCOR-Study/ENCOR_Training_Portal.html` — gated practice hub (checkout required).
- `/secplus-home.html` — **legacy** Security+ sample hub — **do not use for ENCOR ads**.
- CCNA ads → `/ccna-home.html` — see [[../ccna/ccna-portal-google-ads|CCNA campaign]] (not this ENCOR campaign).

## Keywords & angles (draft)

Intent themes to test in ad groups — **prep / practice / simulation**, not course:

| Ad group | Keywords (examples) | Lead message |
|----------|---------------------|--------------|
| Free samples | ccnp encor practice test, encor 350-401 practice exam | Free shuffled sample questions + D&D + lab |
| Practice test | encor practice questions, ccnp encor exam prep | Verified explanations — not PDF dumps |
| Simulation purchase | encor exam simulation, ccnp encor mock exam timed | 120-min sim, 50 MCQ + 5 D&D + 4 labs, $4.99 |
| Retake / readiness | pass encor first try, ccnp encor exam prep | Exam-realistic format — save retake fees |
| Labs / PBQ | encor cli lab practice, ccnp drag and drop practice | Browser labs — no GNS3 required |
| Federal / DoD | ccnp encor federal, ccnp encor defense contractor | Browser 350-401 prep — see [[../../01-strategy/cisco-certifications-exam-prep-foundation\|Cisco foundation]] |

### Geo targeting (federal/defense ad groups)

Use with `utm_content=federal-{market}` or `cisco-{market}` for reporting. Details: [[../../01-strategy/cisco-certifications-exam-prep-foundation#Shared geo ad groups|geo table]].

| Ad group (draft) | Priority geos | UTM content example |
|------------------|---------------|---------------------|
| `encor_federal_dc` | DC + NoVA + MD inner beltway | `federal-dc` |
| `encor_federal_cos` | Colorado Springs | `federal-cos` |
| `encor_federal_satx` | San Antonio | `federal-satx` |
| `encor_federal_norfolk` | Norfolk / Hampton Roads | `federal-norfolk` |

National non-geo campaigns still run for generic `ccnp encor practice test` keywords. ENCOR search volume is smaller than CCNA — lean on **national** + Tier 1 contractor metros.

**Negative keyword ideas:** free course, bootcamp, training program, dump, guaranteed pass, pdf download, encor course, ine encor — full lists on [[../../07-keywords/landing-maps/ccnp-encor-portal#Negatives|ENCOR landing map]] and export below.

**Campaign-level negatives (phrase match unless noted):** free course, training course, bootcamp, instructor led, brain dump, exam dump, guaranteed pass, pdf download, udemy, coursera, cbt nuggets, ine encor, cisco netacad, jobs, salary, ccna only, ccna practice, ccie lab, ccie enterprise, devnet, ccnp design, comptia security+

Message angles (aligned with [[../../01-strategy/positioning-and-messaging|positioning]]):

- **Exam-realistic** — timed simulation, drag-and-drop, CLI lab items
- **Verified solutions** — prep you can trust, not unvetted dumps
- **Browser-only** — no PDF, no GNS3, no third-party software
- **Free samples** — 12 shuffled MCQ, drag-and-drop, and CLI lab on the landing page
- **Confidence / economics** — practice until ready; $4.99 full sim vs retake cost
- **Not a course** — say “exam prep” and “practice” in headlines; avoid “training program”

### Headline / description drafts (policy-safe)

**Generic / home landing:**

- H1 (on page): `CCNP ENCOR exam prep — practice tests, labs, and timed simulation`
- Ad headline 1: `ENCOR 350-401 Practice Test — In Browser`
- Ad headline 2: `Free ENCOR Sample Questions`
- Ad headline 3: `CLI Labs — No GNS3 Required`
- Description: `Realistic ENCOR 350-401 practice with verified explanations. Free samples or full 120-minute sim. No downloads.`

**Sim purchase (`#purchase`):**

- `120-Min ENCOR Exam Simulation`
- `ENCOR Timed Practice — $4.99`
- `50 MCQ + D&D + CLI Labs`
- `Domain-Weighted Study Paths`

## AI search alignment

Landing page must answer AI-style questions clearly (see [[../../01-strategy/google-ai-search-strategy|FAQ bank]]):

- [x] H1/lead use “exam prep” not “training course”
- [x] Meta description mentions browser-based + practice test + 350-401
- [x] `#exam-audience` section (people, when, where)
- [x] Free ENCOR samples live (questions, D&D, lab)
- [ ] FAQ JSON-LD (future — visible FAQ exists)

## Tracking checklist

- [ ] Final URLs include `utm_campaign=encor_portal` (or ad-group-specific `utm_content`)
- [ ] Google Ads conversion: sample engagement (engagement / page_view) + `begin_checkout` (purchase)
- [ ] Weekly report: filter GA4 by campaign name matching `encor*`
- [ ] Stripe Payment Link confirms **$4.99** for timed sim in Dashboard
- [ ] Stripe portal subscribers visible in `/admin/analytics.html` (ENCOR product metadata)
- [ ] Landing page audits in [[../../06-website-optimization/landing-page-audit-checklist|audit checklist]] — log changes in [[../../06-website-optimization/content-change-log|content change log]]
- [ ] Consider dedicated GA4 event for sample CTA clicks (CCNA has `ccna_free_assessment_click`; ENCOR has no equivalent yet)

## Landing page optimization

Primary page tracker: [[../../06-website-optimization/pages/ccnp-home|ccnp-home.html]].

Before major ad spend increases, run the optimization workflow in [[../../06-website-optimization/README|06-website-optimization]].

**Known LP items (2026-05-31):**

- Free samples ATF on landing (questions, drag-and-drop, CLI lab)
- `#purchase` block with domain-weighted blueprint table
- `#exam-audience` section for federal/contractor message match
- No headline pinning yet (CCNA uses `ccna-home-conversion.js` — ENCOR could add similar)

## Creative / ad copy notes

- Full RSA sets, keywords, negatives, extensions: [[ccnp-encor-google-ads-export|paste-ready export]]
- Launch with **`encor_free_samples`** + **`encor_sim_purchase`** in parallel
- A/B: home landing (`free-samples`) vs direct `/sample?track=encor-questions` final URL
- Pin purchase URL to `#purchase` for sim ad group only

## Decisions log

| Date | Change | Rationale |
|------|--------|-----------|
| 2026-05-31 | Vault sync: Security+ playbook structure — ad groups, funnel, export, tracking checklist | Align active ENCOR ads with CCNA/Security+ campaign workflow |
| 2026-05-30 | Active campaign + Cisco foundation alignment | User running ENCOR ads alongside CCNA |
| 2026-05-30 | CTA landing = `ccnp-home.html`; not `secplus-home.html` | Product-specific final URLs |

## Open questions

- **Launch strategy:** Lead with `encor_free_samples` for 1–2 weeks, then scale `encor_sim_purchase` on simulation keywords — **recommended default**
- **Target CPA:** TBD — compare sample → upsell vs direct `$4.99` sim vs `$19.99` portal
- **Brand vs non-brand:** Start non-brand only; add brand campaign when search volume warrants
- **Free assessment:** CCNA has a 35-min timed assessment; ENCOR top-of-funnel is guest samples only — evaluate timed free ENCOR slice later
- **Headline pinning:** CCNA uses `utm_content=hl-*` → `ccna-home-conversion.js`; add ENCOR equivalent if ad groups need on-page message match

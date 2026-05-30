---
type: campaign
channel: google-ads
product: secplus-sy0-701
status: active
priority: 1
target_cpa: null
utm_campaign: secplus_portal
utm_source: google
utm_medium: cpc
landing_pages:
  - /comptia-sec+-home.html
  - /comptia-sec+-home.html#purchase
  - /comptia-sec+-home.html#secplus-lead-capture
  - /COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/simulation-secure-web-architecture-openssl.html
sample_entry:
  - /secplus-sample?track=questions
  - /secplus-sample?home=secplus
related_reports: []
---

# Security+ — Google Ads (first campaign)

Primary paid campaign for **CompTIA Security+ SY0-701** on Be Certified Today.

**Positioning reminder:** [[../01-strategy/positioning-and-messaging|Exam prep only]] — target people practicing for test day, not course shoppers. See [[../01-strategy/google-ai-search-strategy|AI search strategy]] for FAQ/structured content that supports the same keywords.

## Objective

Send high-intent SY0-701 **exam prep** traffic to the landing page. Convert via:

1. **Lead magnet** — free 35-min timed sim + scorecard ([[security-plus-lead-magnet-ads|lead magnet ads]])
2. **Direct purchase** — $9.99 timed sim, 10-day, or 30-day portal access

Optimize toward `generate_lead`, `begin_checkout`, and purchases while building Quality Score.

## Primary landing URLs (use in Google Ads)

**Final URL — generic / brand:**

```
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content={creative}
```

**Lead magnet (top-of-funnel ad group):**

```
https://becertifiedtoday.com/comptia-sec+-home.html#secplus-lead-capture?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=lead-free-sim
```

**Purchase intent (sim / portal ad groups):**

```
https://becertifiedtoday.com/comptia-sec+-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sim-purchase
```

### CTA landing — PBQ / OpenSSL simulation

Interactive **mid-funnel** landing for PBQ/openssl intent (not primary brand landing):

```
https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/simulation-secure-web-architecture-openssl.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_openssl_pbq&utm_content={creative}
```

Page note: [[../06-website-optimization/pages/simulation-secure-web-architecture-openssl|simulation-secure-web-architecture-openssl.md]] — high-value keywords, negatives, CTA map.

`campaign-attribution.js` is loaded on this page — UTM + `gclid` persist for the session in GA4.

## Recommended ad group structure

| Ad group | Final URL anchor | Intent | Start spend? |
|----------|------------------|--------|:------------:|
| `secplus_lead_free_sim` | `#secplus-lead-capture` | Practice test, mock exam | **Yes** — primary launch |
| `secplus_sim_purchase` | `#purchase` | Timed simulation, exam sim | Yes — tight keywords |
| `secplus_portal_access` | `#purchase` | Multi-day study access | After baseline data |
| `secplus_openssl_pbq` | OpenSSL sim page | PBQ / openssl CSR | Optional mid-funnel |
| `secplus_federal_*` | Home (generic) | DoD / 8140 / contractor | Optional geo campaigns |

Copy details for lead group: [[security-plus-lead-magnet-ads|lead magnet ads]].

## Funnel map

| Stage | Page / action | GA4 signal |
|-------|----------------|------------|
| Click | Google Ads → landing | Session with `utm_campaign=secplus_portal` |
| Lead magnet | `#secplus-lead-capture` → email → free sim | `generate_lead` |
| Free sim | 35 min / 21 items, Back + mark for review | Engagement, completion |
| Scorecard email | Results → email my scorecard | `secplus_scorecard_email_sent` |
| Upsell | Results modal or `#purchase` | `begin_checkout` |
| Try free sample (no email) | `/secplus-sample?…` or in-page sample CTAs | Page views, engagement |
| Begin checkout | Portal 10d / 30d or timed sim buttons | `begin_checkout` |
| Purchase | Stripe Payment Link | Stripe + portal metadata; Google Ads conversion if configured |

## Products & checkout tracking

| Offer | Price | GA4 `item_id` | Stripe / checkout |
|-------|------:|---------------|-------------------|
| 10-day portal | $9.99 | `secplus_portal_10d` | `data-secplus-portal-10d-checkout` |
| 30-day portal | $19.99 | `secplus_portal_30d` | `data-secplus-portal-30d-checkout` |
| Timed simulation | $9.99 | `secplus_timed_simulation` | `data-secplus-test-sim-checkout` |
| Free timed sim (lead) | $0 | — | Email unlock → `?free=1` runner |

Checkout wiring: `public/COMP_TIA_SEC+/js/secplus-portal-checkout.js`, `secplus-test-checkout.js`.

Post-purchase: `secplus-portal-checkout-success.html` → training portal at `/COMP_TIA_SEC+/SEC+_Training_Portal.html`.

## Secondary pages (organic / retargeting — not primary ad landings)

- `/comptia-sec+-home.html` — **only** Security+ Google Ads final URL (exam prep + purchase + lead magnet).
- `/secplus-home.html` — **legacy** sample hub; “launching soon” copy — **do not use for ads**. See [[../06-website-optimization/pages/secplus-home-legacy|secplus-home legacy note]].
- `/COMP_TIA_SEC+/SEC+_Training_Portal.html` — gated practice hub (checkout required).
- CCNP ENCOR ads → `/ccnp-home.html` — see [[ccnp-encor-google-ads|ENCOR campaign]] (not this Security+ campaign).

## Keywords & angles (draft)

Intent themes to test in ad groups — **prep / practice / simulation**, not course:

| Ad group | Keywords (examples) | Lead message |
|----------|---------------------|--------------|
| Lead / free sim | security+ practice test, sy0-701 practice exam, security+ mock exam | Free 35-min timed sample + scorecard |
| Practice test | sy0-701 practice questions, security+ practice questions | Verified explanations — not PDF dumps |
| Simulation purchase | security+ exam simulation, sy0-701 timed test | 90-min sim, Back + mark for review, $9.99 |
| Retake / readiness | pass security+ first try, security+ exam prep | Exam-realistic format — save retake fees |
| PBQ / OpenSSL CTA | security+ pbq practice, sy0-701 pbq, openssl csr comptia | Free PBQ slice → portal/sim on [[../06-website-optimization/pages/simulation-secure-web-architecture-openssl\|openssl sim landing]] |
| Federal / DoD | security+ dod, security+ 8140, security+ defense contractor | Browser SY0-701 prep — hero/meta mention DoD; see [[../01-strategy/security-plus-federal-defense-foundation\|federal foundation]] |

### Geo targeting (federal/defense ad groups)

Use with `utm_content=federal-{market}` for reporting. Details: [[../01-strategy/security-plus-federal-defense-foundation#Locations — where to find them|locations table]].

| Ad group (draft) | Priority geos | UTM content example |
|------------------|---------------|---------------------|
| `secplus_federal_dc` | DC + NoVA + MD inner beltway | `federal-dc` |
| `secplus_federal_cos` | Colorado Springs | `federal-cos` |
| `secplus_federal_satx` | San Antonio | `federal-satx` |
| `secplus_federal_norfolk` | Norfolk / Hampton Roads | `federal-norfolk` |

National non-geo campaigns still run for generic `security+ practice test` keywords.

**Negative keyword ideas:** free course, bootcamp, training program, dump, guaranteed pass, pdf download — full lists on [[../06-website-optimization/pages/simulation-secure-web-architecture-openssl#Negative keywords|openssl CTA page note]] and campaign-level list below.

**Campaign-level negatives (phrase match unless noted):** free course, training course, bootcamp, instructor led, brain dump, exam dump, guaranteed pass, pdf download, udemy, coursera, professor messer, jobs, salary, cissp, ccna, sy0-601

Message angles (aligned with [[../01-strategy/positioning-and-messaging|positioning]]):

- **Exam-realistic** — timed simulation, PBQ-style items, Back + mark for review
- **Verified solutions** — prep you can trust, not unvetted dumps
- **Browser-only** — no PDF, no third-party software
- **Free sim lead magnet** — 35 min, 20 MCQ + PBQ, domain scorecard
- **Confidence / economics** — practice until ready; $9.99 full sim vs retake cost
- **Not a course** — say “exam prep” and “practice” in headlines; avoid “training program”

### Headline / description drafts (policy-safe)

**Generic / home landing:**

- H1 (on page): `Security+ SY0-701 Exam Prep — Practice Tests & Simulation`
- Ad headline 1: `SY0-701 Practice Test — In Browser`
- Ad headline 2: `Timed Security+ Exam Simulation`
- Ad headline 3: `No PDFs — Interactive Exam Prep`
- Description: `Realistic SY0-701 practice with verified explanations. Free 35-min timed sample or full 90-minute sim. No downloads.`

**Sim purchase (`#purchase`):**

- `90-Min Security+ Exam Simulation`
- `SY0-701 Timed Practice — $9.99`
- `Back & Mark for Review — Like Test Day`
- `Study Scorecard by Domain`

## AI search alignment

Landing page must answer AI-style questions clearly (see [[../01-strategy/google-ai-search-strategy|FAQ bank]]):

- [x] FAQ section on landing page implemented (2026-05-30)
- [x] H1/lead use “exam prep” not “training course”
- [x] Meta description mentions browser-based + practice test + SY0-701
- [x] Free timed sim + scorecard offer live (2026-05-30 prod)

## Tracking checklist

- [ ] Final URLs include `utm_campaign=secplus_portal` (or ad-group-specific `utm_content`)
- [ ] Google Ads conversion: `generate_lead` (lead group) + `begin_checkout` (purchase)
- [ ] Weekly report: filter GA4 by campaign name matching `secplus*`
- [ ] Stripe Payment Link confirms **$9.99** for timed sim in Dashboard
- [ ] Stripe portal subscribers visible in `/admin/analytics.html` (Security+ product metadata)
- [ ] Landing page audits in [[../06-website-optimization/landing-page-audit-checklist|audit checklist]] — log changes in [[../06-website-optimization/content-change-log|content change log]]

## Landing page optimization

Primary page tracker: [[../06-website-optimization/pages/comptia-sec-plus-home|comptia-sec+-home.html]].

Before major ad spend increases, run the optimization workflow in [[../06-website-optimization/README|06-website-optimization]].

**Known LP items (2026-05-30):**

- Lead-first layout for ad traffic (`utm_content=lead-free-sim`, `#secplus-lead-capture`) — intro → lead form → purchase
- Dedicated federal section removed; DoD/8140 context remains in hero + meta + FAQ

## Creative / ad copy notes

- Launch with **`secplus_lead_free_sim`** + **`secplus_sim_purchase`** in parallel
- A/B: lead headline “Free Timed Simulation” vs “35-Min Sample Exam”
- Pin lead URL to `#secplus-lead-capture` for lead ad group only

## Decisions log

| Date | Change | Rationale |
|------|--------|-----------|
| 2026-05-30 | Vault sync: 35-min free sim, $9.99 paid sim, Back + mark for review, ad group URLs | Prod deploy + campaign launch prep |
| 2026-05-30 | Free sim lead magnet live (20 MCQ + dark web PBQ, scorecard email, upsell) | Top-of-funnel for Google Ads |
| 2026-05-30 | Timed sim price **$9.99** (was $4.99) | Site + Stripe + vault aligned |
| 2026-05-30 | Federal/defense foundation + landing people/times/locations section | High-intent DoD/contractor segment; geo ad groups |
| 2026-05-30 | OpenSSL PBQ CTA landing + keyword/negative doc in Obsidian | Mid-funnel ad group `secplus_openssl_pbq` |
| 2026-05-30 | Landing page positioning + FAQ deploy (`comptia-sec+-home.html`) | Ads/AI search message match — exam prep not course |
| 2026-05-30 | Campaign note created; primary landing = `comptia-sec+-home.html` | First marketing campaign focus |

## Open questions

- **Launch strategy:** Lead with `secplus_lead_free_sim` for 1–2 weeks, then scale `secplus_sim_purchase` on simulation keywords — **recommended default**
- **Target CPA:** TBD — compare lead → upsell vs direct `$9.99` sim vs `$19.99` portal
- **Brand vs non-brand:** Start non-brand only; add brand campaign when search volume warrants
- **Federal section:** Removed from page body; keep federal ad groups using hero/meta copy or restore section if LP exp. suffers

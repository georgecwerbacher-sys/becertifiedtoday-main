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

Send high-intent SY0-701 **exam prep** traffic to the landing page. Convert users who want **realistic practice** (questions + verified explanations + timed simulation) — not a training course. Optimize toward portal purchases and timed sim sales while building Quality Score and AI-search-eligible content.

## Primary landing URL (use in Google Ads)

**Final URL** (add UTMs on the ad or use Google’s tracking template):

```
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content={creative}
```

Send purchase-intent traffic to the purchase block:

```
https://becertifiedtoday.com/comptia-sec+-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal
```

### CTA landing — PBQ / OpenSSL simulation

Interactive **mid-funnel** landing for PBQ/openssl intent (not primary brand landing):

```
https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/simulation-secure-web-architecture-openssl.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_openssl_pbq&utm_content={creative}
```

Page note: [[../06-website-optimization/pages/simulation-secure-web-architecture-openssl|simulation-secure-web-architecture-openssl.md]] — high-value keywords, negatives, CTA map.

`campaign-attribution.js` is loaded on this is page — UTM + `gclid` persist for the session in GA4.

## Funnel map

| Stage | Page / action | GA4 signal |
|-------|----------------|------------|
| Click | Google Ads → landing | Session with `utm_campaign=secplus_portal` |
| Lead magnet (optional) | `#secplus-lead-capture` → study plan | `generate_lead` → see [[security-plus-lead-magnet-ads|lead magnet ads]] |
| Try free sample | `/secplus-sample?…` or in-page sample CTAs | Page views, engagement |
| Begin checkout | Portal 10d / 30d or timed sim buttons | `begin_checkout` |
| Purchase | Stripe Payment Link | Stripe + portal metadata; Google Ads conversion if configured |

## Products & checkout tracking

| Offer | Price | GA4 `item_id` | Stripe / checkout |
|-------|------:|---------------|-------------------|
| 10-day portal | $9.99 | `secplus_portal_10d` | `data-secplus-portal-10d-checkout` |
| 30-day portal | $19.99 | `secplus_portal_30d` | `data-secplus-portal-30d-checkout` |
| Timed simulation | $4.99 | `secplus_timed_simulation` | `data-secplus-test-sim-checkout` |

Checkout wiring: `public/COMP_TIA_SEC+/js/secplus-portal-checkout.js`, `secplus-test-checkout.js`.

Post-purchase: `secplus-portal-checkout-success.html` → training portal at `/COMP_TIA_SEC+/SEC+_Training_Portal.html`.

## Secondary pages (organic / retargeting — not primary ad landings)

- `/comptia-sec+-home.html` — **only** Security+ Google Ads final URL (exam prep + purchase).
- `/secplus-home.html` — **legacy** sample hub; “launching soon” copy — **do not use for ads**. See [[../06-website-optimization/pages/secplus-home-legacy|secplus-home legacy note]].
- `/COMP_TIA_SEC+/SEC+_Training_Portal.html` — gated practice hub (checkout required).
- CCNP ENCOR ads → `/ccnp-home.html` — see [[ccnp-encor-google-ads|ENCOR campaign]] (not this Security+ campaign).

## Keywords & angles (draft)

Intent themes to test in ad groups — **prep / practice / simulation**, not course:

| Ad group | Keywords (examples) | Lead message |
|----------|---------------------|--------------|
| Practice test | security+ practice test, sy0-701 practice exam | Realistic SY0-701 practice in your browser |
| Questions + answers | security+ practice questions, sy0-701 questions explained | Verified explanations — not PDF dumps |
| Simulation | security+ exam simulation, sy0-701 timed test | Timed sim — build confidence before test day |
| Retake / readiness | pass security+ first try, security+ exam prep | Exam prep that matches exam format — save retake fees |
| PBQ / OpenSSL CTA | security+ pbq practice, sy0-701 pbq, openssl csr comptia | Free PBQ slice → portal/sim on [[../06-website-optimization/pages/simulation-secure-web-architecture-openssl\|openssl sim landing]] |
| Federal / DoD | security+ dod, security+ 8140, security+ defense contractor, security+ federal government | Browser SY0-701 prep for workforce baseline deadlines — see [[../01-strategy/security-plus-federal-defense-foundation\|federal foundation]] |

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

- **Exam-realistic** — timed simulation, PBQ-style items, domain banks
- **Verified solutions** — prep you can trust, not unvetted dumps
- **Browser-only** — no PDF, no third-party software
- **Confidence / economics** — practice until ready; cheaper than a retake
- **Try free sample** → then 10-day / 30-day access or one-time sim
- **Not a course** — say “exam prep” and “practice” in headlines; avoid “training program”

### Headline / description drafts (policy-safe)

- H1 idea: `Security+ SY0-701 Exam Prep — Practice Tests & Simulation`
- Ad headline 1: `SY0-701 Practice Test — In Browser`
- Ad headline 2: `Timed Security+ Exam Simulation`
- Ad headline 3: `No PDFs — Interactive Exam Prep`
- Description: `Realistic SY0-701 practice questions with verified explanations. Timed simulation. No downloads or third-party apps. Try a free sample.`

## AI search alignment

Landing page must answer AI-style questions clearly (see [[../01-strategy/google-ai-search-strategy|FAQ bank]]):

- [x] FAQ section on landing page implemented (2026-05-30)
- [x] H1/lead use “exam prep” not “training course”
- [x] Meta description mentions browser-based + practice test + SY0-701

## Tracking checklist

- [ ] Final URLs include `utm_campaign=secplus_portal` (or ad-group-specific variants, e.g. `secplus_sim`)
- [ ] Google Ads conversion: `begin_checkout` and/or purchase (see `public/js/google-ads-purchase-conversion.js` on sim runner)
- [ ] Weekly report: filter GA4 by campaign name matching `secplus*`
- [ ] Stripe portal subscribers visible in `/admin/analytics.html` (Security+ product metadata)
- [ ] Landing page audits in [[../06-website-optimization/landing-page-audit-checklist|audit checklist]] — log changes in [[../06-website-optimization/content-change-log|content change log]]

## Landing page optimization

Primary page tracker: [[../06-website-optimization/pages/comptia-sec-plus-home|comptia-sec+-home.html]].

Before major ad spend increases, run the optimization workflow in [[../06-website-optimization/README|06-website-optimization]].

## Creative / ad copy notes

- (Add headlines, descriptions, and what you are A/B testing.)

## Decisions log

| Date | Change | Rationale |
|------|--------|-----------|
| 2026-05-30 | Federal/defense foundation + landing people/times/locations section | High-intent DoD/contractor segment; geo ad groups |
| 2026-05-30 | OpenSSL PBQ CTA landing + keyword/negative doc in Obsidian | Mid-funnel ad group `secplus_openssl_pbq` |
| 2026-05-30 | Landing page positioning + FAQ deploy (`comptia-sec+-home.html`) | Ads/AI search message match — exam prep not course |
| 2026-05-30 | Campaign note created; primary landing = `comptia-sec+-home.html` | First marketing campaign focus |

## Open questions

- Launch with portal 30-day only, or lead with free sample + retarget?
- Target CPA for $19.99 portal vs $9.99 10-day vs $4.99 sim?
- Brand vs non-brand keyword split?

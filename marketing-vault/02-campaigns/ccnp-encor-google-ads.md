---
type: campaign
channel: google-ads
product: encor-350-401
status: planned
priority: 2
target_cpa: null
utm_campaign: encor_portal
utm_source: google
utm_medium: cpc
landing_pages:
  - /ccnp-home.html
  - /ccnp-home.html#purchase
related_reports: []
---

# CCNP ENCOR — Google Ads

Primary paid campaign for **CCNP ENCOR 350-401** exam prep on Be Certified Today.

**Positioning:** [[../01-strategy/positioning-and-messaging|Exam prep only]] — practice tests, labs, drag-and-drop, timed simulation. **Not** a training course.

**Do not send ads to** `/secplus-home.html` (Security+ legacy hub). Security+ ads → [[security-plus-google-ads|secplus_portal]] → `/comptia-sec+-home.html`.

## Primary landing URL (Google Ads final URL)

```
https://becertifiedtoday.com/ccnp-home.html?utm_source=google&utm_medium=cpc&utm_campaign=encor_portal&utm_content={creative}
```

Purchase block:

```
https://becertifiedtoday.com/ccnp-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=encor_portal
```

Page tracker: [[../06-website-optimization/pages/ccnp-home|ccnp-home.html]]  
Keywords: [[../07-keywords/landing-maps/ccnp-encor-portal|ENCOR landing map]]

## Funnel map

| Stage | Page / action | GA4 signal |
|-------|----------------|------------|
| Click | Google Ads → `ccnp-home.html` | Session with `utm_campaign=encor_portal` |
| Try sample | ENCOR sample questions / D&D / lab | Engagement |
| Begin checkout | 10d / 30d portal or timed sim | `begin_checkout` |
| Purchase | Stripe | Portal metadata + conversion |

## Products

| Offer | Price | Checkout attribute |
|-------|------:|--------------------|
| Timed simulation | $4.99 | `data-encor-test-sim-checkout` (verify in HTML) |
| 10-day portal | $9.99 | `data-encor-portal-10d-checkout` |
| 30-day portal | $19.99 | `data-encor-portal-30d-checkout` |

## Keywords & angles (draft)

| Ad group | Keywords (examples) | Lead message |
|----------|---------------------|--------------|
| Practice test | ccnp encor practice test, encor 350-401 practice exam | Browser ENCOR practice with scorecard |
| Labs / PBQ | encor cli lab, ccnp drag and drop practice | Interactive labs—not PDFs |
| Simulation | encor exam simulation, ccnp timed test | Timed sim from $4.99 |
| Exam prep | ccnp encor exam prep, encor 350-401 prep | Exam prep, not a video course |

**Negatives:** inherit [[../07-keywords/negatives/master-negative-list|master list]] + `ccna only`, `devnet`, `ccie lab`, `free course`, `gns3 course`

## Decisions log

| Date | Change | Rationale |
|------|--------|-----------|
| 2026-05-30 | CTA landing = `ccnp-home.html`; not `secplus-home.html` | Product-specific ad final URLs; Security+ uses `comptia-sec+-home.html` |

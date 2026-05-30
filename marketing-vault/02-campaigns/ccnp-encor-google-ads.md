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
related_reports: []
---

# CCNP ENCOR 350-401 — Google Ads (active)

Primary paid campaign for **CCNP ENCOR 350-401** exam prep on Be Certified Today.

**Positioning:** [[../01-strategy/positioning-and-messaging|Exam prep only]] · [[../01-strategy/cisco-certifications-exam-prep-foundation|Cisco foundation]]

**Do not send ads to** `/secplus-home.html`. Security+ → `/comptia-sec+-home.html`.

## Primary landing URL

```
https://becertifiedtoday.com/ccnp-home.html?utm_source=google&utm_medium=cpc&utm_campaign=encor_portal&utm_content={creative}
```

Purchase block:

```
https://becertifiedtoday.com/ccnp-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=encor_portal
```

Page tracker: [[../06-website-optimization/pages/ccnp-home|ccnp-home.md]]  
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
| Timed simulation | $4.99 | `data-encor-test-sim-checkout` |
| 10-day portal | $9.99 | `data-encor-portal-10d-checkout` |
| 30-day portal | $19.99 | `data-encor-portal-30d-checkout` |

## Ad groups

| Ad group | Keywords (examples) | Lead message |
|----------|---------------------|--------------|
| Practice test | ccnp encor practice test, encor 350-401 practice exam | Browser ENCOR practice |
| Exam prep | ccnp encor exam prep, encor 350-401 prep | Exam prep—not a video course |
| Labs / PBQ | encor cli lab, ccnp drag and drop practice | Interactive labs—no GNS3 |
| Simulation | encor exam simulation, ccnp timed test | Timed sim from $4.99 |
| Enterprise / federal | ccnp encor contractor, cisco encor federal | Confirm reqs with employer |

### Geo (optional)

`utm_content=cisco-dc`, `cisco-cos`, `cisco-satx`, `cisco-norfolk` — [[../01-strategy/cisco-certifications-exam-prep-foundation#Shared geo ad groups|shared geo table]].

**Negatives:** [[../07-keywords/landing-maps/ccnp-encor-portal#Negatives|ENCOR negatives]] + master list

## Headline drafts

- `ENCOR 350-401 Exam Prep — In Browser`
- `CCNP ENCOR Practice Test`
- `CLI Labs — No GNS3 Required`
- `Timed ENCOR Simulation — $4.99`
- `CCNP Exam Prep — Not a Course`

## AI search / landing

- [x] H1 + lead: exam prep, 350-401, browser-only
- [x] `#exam-audience` section (people, when, where)
- [ ] FAQ JSON-LD (future—visible FAQ exists)

## Decisions log

| Date | Change | Rationale |
|------|--------|-----------|
| 2026-05-30 | Active campaign + Cisco foundation alignment | User running ENCOR ads alongside CCNA |
| 2026-05-30 | CTA landing = `ccnp-home.html`; not `secplus-home.html` | Product-specific final URLs |

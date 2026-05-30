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
related_reports: []
---

# CCNA 200-301 — Google Ads (active)

Primary paid campaign for **Cisco CCNA 200-301** exam prep on Be Certified Today.

**Positioning:** [[../01-strategy/positioning-and-messaging|Exam prep only]] · [[../01-strategy/cisco-certifications-exam-prep-foundation|Cisco foundation]]

## Primary landing URL

```
https://becertifiedtoday.com/ccna-home.html?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content={creative}
```

Alias (same page):

```
https://becertifiedtoday.com/ccna/practice-test?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content={creative}
```

Purchase / sim:

```
https://becertifiedtoday.com/ccna-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal
```

**Do not use** `/CCNA-Study/CCNA_Training_Portal.html` as final URL — gated; sends wrong message match.

Page tracker: [[../06-website-optimization/pages/ccna-home|ccna-home.md]]

## Funnel

| Stage | Action | Signal |
|-------|--------|--------|
| Click | Ads → `ccna-home.html` | `utm_campaign=ccna_portal` |
| Free assessment | `/CCNA_Sim_EXAM/free-assessment.html` | `ccna_free_assessment_click` (gtag) |
| Sample | `/sample?track=ccna-*` | Engagement |
| Checkout | 10d / 30d / timed sim | `begin_checkout` |

## Products

| Offer | Price | Checkout |
|-------|------:|----------|
| Timed simulation | $4.99 | CCNA test sim checkout |
| 10-day portal | $9.99 | `data-ccna-portal-10d-checkout` |
| 30-day portal | $19.99 | `data-ccna-portal-30d-checkout` |

## Ad groups

| Ad group | Keywords | Message |
|----------|----------|---------|
| Practice test | ccna practice test, ccna 200-301 practice exam | Realistic browser practice |
| Free practice | free ccna practice, free ccna exam | Free assessment + scorecard |
| Mock / sim | ccna mock exam, ccna exam simulation | Timed sim from $4.99 |
| Exam prep | ccna 200-301 prep, cisco ccna exam prep | Not a training course |
| Federal / contract | ccna defense contractor, ccna federal job | Browser prep—confirm reqs with employer |

**Headline pinning:** `utm_content=hl-practice-test`, `hl-free-practice`, etc. → `ccna-home-conversion.js`

### Geo (optional)

`utm_content=cisco-dc`, `cisco-cos`, `cisco-satx`, `cisco-norfolk` — see [[../01-strategy/cisco-certifications-exam-prep-foundation#Shared geo ad groups|geo table]].

**Negatives:** [[../07-keywords/landing-maps/ccna-portal#Negatives|CCNA negatives]] + master list

## Headline drafts

- `CCNA 200-301 Practice Test — In Browser`
- `Free CCNA Assessment + Scorecard`
- `No GNS3 — CCNA Labs Online`
- `CCNA Exam Prep — Not a Course`
- `Timed CCNA Simulation — $4.99`

## Decisions log

| Date | Change | Rationale |
|------|--------|-----------|
| 2026-05-30 | Active campaign doc; landing = `ccna-home.html` | User running CCNA ads; align with ENCOR/Security+ playbook |
| 2026-05-30 | Removed training portal as ad final URL | Message match + conversion path |

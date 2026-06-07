---
type: strategy
status: active
tags:
  - ccna
  - encor
  - cisco
  - google-ads
  - exam-prep
  - federal
created: 2026-05-30
---

# Cisco certifications — CCNA & ENCOR exam prep foundation

Shared playbook for **active Google Ads** on **CCNA 200-301** and **CCNP ENCOR 350-401**. Same rules as Security+ and [[positioning-and-messaging|global positioning]]: **exam prep**, not courses; browser-only; verified practice; no PDF dumps.

| Cert | CTA landing | Campaign | UTM |
|------|-------------|----------|-----|
| CCNA 200-301 | `/ccna-home.html` (alias `/ccna/practice-test`) | [[../02-campaigns/ccna/ccna-portal-google-ads\|ccna_portal]] | `utm_campaign=ccna_portal` |
| CCNP ENCOR 350-401 | `/ccnp-home.html` | [[../02-campaigns/encor/ccnp-encor-google-ads\|encor_portal]] | `utm_campaign=encor_portal` |

Cross-link: [[security-plus-federal-defense-foundation|Security+ federal foundation]] · [[../08-8140-compliance/marketing-incorporation-plan|8140 incorporation plan]] — shared locations, contractor timing, and official 9/12-month baselines.

---

## Shared principles (all Cisco ads)

1. **Exam prep only** — practice tests, labs, drag-and-drop, timed simulation; not “Cisco training course” or bootcamp.
2. **No GNS3 / IOU required** — major differentiator on landing pages and ad copy.
3. **Free sample or free assessment** → portal/sim purchase (CCNA leads with free assessment + scorecard).
4. **Headline pinning** — CCNA uses `?hl=` / `utm_content=hl-*` variants (`scripts/ccna-google-ads-headline-suffixes.txt`, `ccna-home-conversion.js`).
5. **Keyword collection** — weekly search-term import per campaign in `07-keywords/search-terms/`.
6. **Compliance language** — Cisco certs may appear in federal/contractor **IT** work roles under DoD 8140; confirm via your org and the [qualification matrix](https://public.cyber.mil/wid/dod8140/dod-cyber-workforce-qualifications-matrices-management/). Never claim we satisfy a specific contract or DoD baseline.

---

## CCNA 200-301

### People

| Persona | Situation | Message |
|---------|-----------|---------|
| **Career changer** | First Cisco cert; needs exam-realistic practice | Free assessment + scorecard |
| **Network admin / NOC** | Employer or contract expects CCNA | Browser prep between shifts |
| **Federal / defense contractor** | Network admin/engineer role on contract | Exam prep—not a video course |
| **Help desk → network** | Moving into routing & switching | Labs + drag-and-drop in browser |
| **Re-cert** | CCNA renewal cycle (verify current Cisco policy) | Timed sim + question bank |

### When timing matters

| Trigger | Window | CTA angle |
|---------|--------|-----------|
| Scheduled 200-301 | 2–8 weeks out | 30-day pass + timed sim |
| DoD 8140 foundational window | **9 months** from assignment (DoD baseline—verify with org) | Start free assessment early |
| New hire / contract | Component may set shorter than 9 months | Start free assessment |
| Failed attempt | Retake scheduling | Domain scorecard → focus weak areas |
| Night / weekend study | Ongoing | No installs—open browser |
| Before buying full library | First visit | Free 30-min assessment |

### Where (study + geo ads)

**Product:** Browser labs from duty station, hotel, home—no GNS3. Follow org IA policy on government devices.

**Geo (Tier 1 bid boost):** DC/NoVA/MD, Colorado Springs, San Antonio, Norfolk, Huntsville, Tampa, San Diego, Atlanta, Dallas—plus **national** campaign for generic `ccna practice test`.

### CCNA ad groups (draft)

| Ad group | Keywords (examples) | Landing |
|----------|---------------------|---------|
| Practice test | ccna practice test, ccna 200-301 practice exam | `ccna-home.html` |
| Free practice | free ccna practice, free ccna exam | `ccna-home.html` |
| Mock / sim | ccna mock exam, ccna exam simulation | `ccna-home.html#purchase` |
| Exam prep | ccna 200-301 prep, cisco ccna exam prep | `ccna-home.html` |
| Labs / PBQ | ccna drag and drop, ccna cli lab practice | samples on page |
| Federal / contract | ccna federal job, ccna defense contractor | `ccna-home.html#exam-audience` |

**CCNA negatives (add):** `ccna course free`, `cisco netacad`, `cisco learning network course`, `ine ccna`, `cbnuggets`, `gns3 tutorial`, `packet tracer download only`

Keywords: [[../07-keywords/landing-maps/ccna-portal|CCNA landing map]]

---

## CCNP ENCOR 350-401

### People

| Persona | Situation | Message |
|---------|-----------|---------|
| **Network engineer** | CCNP core step after CCNA | ENCOR domain-weighted practice |
| **Federal integrator** | Enterprise routing/design on contract | Browser ENCOR sim |
| **MSP / enterprise staff** | 350-401 scheduled | CLI labs without IOU |
| **Failed ENCOR** | Retake prep | Timed sim + domain table on landing |
| **CCNA holder leveling up** | Studying architecture + automation | Drag-and-drop + labs |

### When timing matters

| Trigger | Window | CTA angle |
|---------|--------|-----------|
| Scheduled 350-401 | 4–10 weeks | 30-day pass |
| CCNA recently passed | 1–6 months | ENCOR blueprint-aligned prep |
| Contract / promotion | Role requires CCNP progress | Exam prep before deadline |
| Domain cram | 2 weeks pre-exam | Focus Security Ops + Architecture weights on page |
| One dry run | 1 week out | $4.99 timed simulation |

### Where

Same geo tiers as CCNA; ENCOR search volume is smaller—lean on **national** + Tier 1 metros with contractor density.

### ENCOR ad groups (draft)

| Ad group | Keywords (examples) | Landing |
|----------|---------------------|---------|
| Practice test | ccnp encor practice test, encor 350-401 practice exam | `ccnp-home.html` |
| Exam prep | ccnp encor exam prep, encor 350-401 prep | `ccnp-home.html` |
| Simulation | encor exam simulation, ccnp timed exam | `ccnp-home.html#purchase` |
| Labs | encor cli lab, ccnp drag and drop practice | samples |
| Enterprise / federal | ccnp encor federal, cisco encor contractor | `ccnp-home.html#exam-audience` |

**ENCOR negatives:** `ccna only`, `devnet`, `ccie lab`, `encor course`, `cisco live training`, `ine encor`, `ccnp enterprise design` (if not offered)

Keywords: [[../07-keywords/landing-maps/ccnp-encor-portal|ENCOR landing map]]

---

## Shared geo ad groups (optional split)

| UTM content | Geo focus | Campaigns |
|-------------|-----------|-----------|
| `cisco-dc` | DC + NoVA + MD | ccna_portal, encor_portal |
| `cisco-cos` | Colorado Springs | both |
| `cisco-satx` | San Antonio | both |
| `cisco-norfolk` | Hampton Roads | both |

Run **national** campaigns in parallel; compare CPA before heavy geo bid adjustments.

---

## Ad schedule (starting point)

- **Increase:** Tue–Thu evenings; Sun 5–10pm local
- **Decrease:** Late Fri night
- Align with shift workers and weekend study (same as Security+)

---

## Landing page checklist

| Page | Section ID | People / When / Where |
|------|------------|-------------------------|
| `comptia-sec+-home.html` | `#federal-defense-prep` | DoD 8140 / federal |
| `ccna-home.html` | `#exam-audience` | CCNA + contractor |
| `ccnp-home.html` | `#exam-audience` | ENCOR + enterprise |

Each includes disclaimer: confirm cert requirements with employer; we provide **exam prep** only.

---

## Measurement

| Campaign | GA4 filter | Weekly import |
|----------|------------|---------------|
| CCNA | `utm_campaign=ccna_portal` | `search-terms/YYYY-MM-DD-ccna_portal.md` |
| ENCOR | `utm_campaign=encor_portal` | `search-terms/YYYY-MM-DD-encor_portal.md` |

Compare free assessment starts (CCNA) vs checkout (both) in `/admin`.

---

## Decisions log

| Date | Decision |
|------|----------|
| 2026-05-30 | Cisco foundation doc; CCNA + ENCOR active ad guidelines aligned with Security+ |
| 2026-05-30 | CCNA primary landing = `ccna-home.html`, not training portal |

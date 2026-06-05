---
type: guest-page-index
status: active
repo_root: public/
last_reviewed: 2026-06-04
---

# Guest access pages

Pages a visitor can reach **without** opening a paid **Training Portal** session first. After Stripe checkout, the same person moves into **portal-gated** URLs (browser-bound access).

**Do not use Training Portal URLs as Google Ads final URLs.** See [[../06-website-optimization/ad-site-verification-2026-05-31|ad-site verification]].

---

## Tier 1 — Site hub & product landings (indexed)

Primary entry for SEO, Ads, and [[../index.html|index]] track cards.

| Path | Product | Role | Vault / campaign |
|------|---------|------|------------------|
| `/index.html` | All | Choose CCNA, ENCOR, or Security+ | — |
| `/ccna-home.html` | CCNA 200-301 | Ads landing, `#purchase`, `#ccna-lead-capture` | [[../06-website-optimization/pages/ccna-home\|ccna-home]] · `ccna_portal` |
| `/ccnp-home.html` | CCNP ENCOR 350-401 | Ads landing, `#purchase`, `#encor-lead-capture` | [[../06-website-optimization/pages/ccnp-home\|ccnp-home]] · `encor_portal` |
| `/comptia-sec+-home.html` | Security+ SY0-701 | **Primary** Security+ Ads URL | [[../06-website-optimization/pages/comptia-sec-plus-home\|sec+ home]] · `secplus_portal` |

---

## Tier 2 — Free funnel (guest; mostly not in sitemap)

Reachable from index samples section or product landings. Good for trust before checkout.

### Short sample routers (`vercel.json` rewrites)

| Public URL | Rewrites to | Typical `?track=` |
|------------|-------------|-------------------|
| `/sample` | `/CCNP-ENCOR-Study/ENCOR_Samples/sample.html` | `ccna-questions`, `encor-dnd`, `ccna-vlan`, … |
| `/secplus-sample` | `/COMP_TIA_SEC+/SEC+_Samples/sample.html` | `questions`, `sim-dark-web` |

### Index-linked sample entry points

| From `index.html` | href |
|-------------------|------|
| CCNA sample questions | `/sample?track=ccna-questions` |
| CCNA sample lab | `/sample?track=ccna-vlan` |
| ENCOR drag-and-drop | `/sample?track=encor-dnd` |
| Security+ sample questions | `/secplus-sample?track=questions` |
| Security+ dark web PBQ | `/secplus-sample?track=sim-dark-web` |

### Product landing free paths

| Track | Lead / sim block | Runner or assessment |
|-------|------------------|----------------------|
| **Security+** | `#secplus-lead-capture` on [[../comptia-sec+-home\|comptia-sec+-home]] | `/COMP_TIA_SEC+/test-simulation-runner.html?free=1` |
| **CCNA** | `#ccna-lead-capture` on `ccna-home.html` | `/CCNA_Sim_EXAM/free-assessment.html` (also in sitemap) |
| **ENCOR** | `#encor-lead-capture` on `ccnp-home.html` | `/CCNP-ENCOR-Study/test-simulation-runner.html?free=1` |

`robots.txt` **Disallow**s `*test-simulation-runner.html` (still used for Ads lead magnet; not for organic sitemap priority).

### Mid-funnel guest PBQ (indexed)

| Path | Use |
|------|-----|
| `/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/simulation-secure-web-architecture-openssl.html` | PBQ/openssl ad group · in `sitemap.xml` |

---

## Tier 3 — Legacy / alternate hubs (limited crawl)

| Path | robots / meta | Notes |
|------|---------------|-------|
| `/secplus-home.html` | `noindex`; **Disallow** in robots | Legacy hub; Ads should use `comptia-sec+-home.html` |
| `/choose-training-path.html` | **Disallow** | Old path picker; not index hub |

---

## Tier 4 — Sitemap guest samples & labs (indexed)

Listed in [[sitemap|sitemap]] / `public/sitemap.xml` (CCNA/ENCOR/Security+ sample HTML under each `*_Samples/` and selected labs). Finish URLs typically return visitors to the matching **product landing**, not Training Portal.

---

## Tier 5 — Training portals (paid library; noindex)

Gated home for full question banks after purchase. **`robots.txt`:** `Disallow: /*Training_Portal.html`

| Path | Track |
|------|-------|
| `/CCNA-Study/CCNA_Training_Portal.html` | CCNA |
| `/CCNP-ENCOR-Study/ENCOR_Training_Portal.html` | ENCOR |
| `/COMP_TIA_SEC+/SEC+_Training_Portal.html` | Security+ |

Header **Full Library (Paid Access)** on landings opens a portal gate modal if the browser has no active pass.

---

## Tier 6 — Checkout & access helpers (not guest marketing URLs)

`robots.txt` disallows these; include for complete journey mapping only.

| Pattern | Examples |
|---------|----------|
| Checkout success | `*-portal-checkout-success.html`, `secplus-portal-checkout-success.html` |
| Magic / restore | `*-portal-magic.html`, `*-portal-restore-access.html`, `*-portal-request-link.html` |
| Paid sim purchase | `*test-simulation-purchase.html` |
| Admin | `/admin/`, `/api/` |

---

## Quick rules

1. **Guest marketing path:** `index` → **product landing** → free sample or timed sim → `#purchase` → Stripe.
2. **Post-purchase path:** checkout success → portal access on **same browser** → `*_Training_Portal.html` → full `*_Questions/`, labs, timed sim inside portal.
3. **Writing copy** for Tier 1–2 only on customer-facing pages: [[../12-Writing/_Writing-Rules|Writing rules]].

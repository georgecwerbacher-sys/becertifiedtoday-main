# Marketing tag — minimal list (conversions only)

**Policy:** Tag only public **marketing and conversion** URLs. Do **not** tag the paid member library (portals, question bank, timed sim after purchase).

**Implementation:** `public/js/analytics-exclude.js` enforces this sitewide. Pages with a static gtag block should match this list only.

**GA4 property:** `G-YTT6KBHX7V` · **Google Ads:** `AW-18158574148`

---

## P0 — CCNA wedge + checkout (required)

| URL | Events |
|-----|--------|
| `/ccna/labs-without-gns3.html` | `page_view`, `begin_checkout` |
| `/ccna-home.html` | `page_view`, `begin_checkout` |
| `/sample` (`sample.html`) | `page_view`, sample funnel |
| `/CCNA-Study/ccna-portal-30d-checkout-success.html` | `purchase` (Stripe return) |

**Free sample exception:** While `ccnaHomeSample` is in `sessionStorage` or `?sample=1` is set, CCNA sample question/lab/DnD pages are **tagged** (marketing proof path). After purchase, portal study pages are **not** tagged.

---

## P1 — Other product homes + checkout (when running ads)

| URL | Events |
|-----|--------|
| `/index.html` | `page_view` |
| `/ccnp-home.html` | `page_view`, `begin_checkout` |
| `/comptia-sec+-home.html` | `page_view`, `begin_checkout` |
| `/COMP_TIA_SEC+/secplus-portal-checkout-success.html` | `purchase` |

---

## Google Ads conversions

| Priority | GA4 event | When |
|----------|-----------|------|
| **Primary** | `begin_checkout` | User clicks Get 10-day / 30-day (before Stripe) |
| Secondary | `purchase` | Checkout-success page after paid session |

Import **`begin_checkout`** from GA4 into Google Ads → mark **Primary**.

---

## Explicitly untagged (member / study)

- `/CCNA-Study/CCNA_Training_Portal.html` and portal modes
- `/CCNA-Study/CCNA_questions/*` (unless free sample session)
- `/CCNA-Study/CCNA_labs/*` (unless free sample session)
- `/CCNA-Study/CCNA_D_D/*` (unless free sample session)
- `/CCNA_Sim_EXAM/*` timed sim runners
- `/CCNP-ENCOR-Study/ENCOR_Training_Portal.html`, questions, labs, runners
- `/COMP_TIA_SEC+/SEC+_Training_Portal.html`, questions, sim runners
- `/practice-launcher.html`, portal magic/restore/request-link pages

---

## Ignore Google “untagged pages” warnings

Google wants every URL tagged. For this site, **~10–15 marketing URLs** are enough. Untagged question pages are **intentional**.

---

## Verify

1. Open wedge landing → click purchase → GA4 Realtime shows `begin_checkout`
2. Open CCNA Training Portal (paid) → **no** GA4 Realtime hit
3. Start free VLAN sample from home → sample lab page **does** send events
4. Optional opt-out: `?bcc_no_analytics=1` on any URL

See also: `scripts/ccna-wedge-lab-google-ads.md`

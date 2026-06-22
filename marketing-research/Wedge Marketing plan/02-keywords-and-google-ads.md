---
type: strategy
parent: "[[Wedge Marketing plan]]"
tags:
  - marketing
  - google-ads
  - keywords
---

# Keywords & Google Ads

[[Wedge Marketing plan|← Back to plan]]

---

## Stop fighting here (Tier A head terms)

Pause or **low bid** until wedge groups convert:

- `[ccna practice test]`
- `[ccna mock exam]`
- `[ccna question bank]`
- `[cisco ccna practice test]`

Course vendors bid these as loss leaders. Expect **$4–$8+ CPC** in US.

### Security+ — same pattern (Tier A)

Pause or **low bid** until **`secplus_pbq_wedge`** converts:

- `[security+ practice test]`
- `[security+ question bank]`
- `[comptia security+ practice test]`
- `[sy0-701 question bank]`

Messer/Dion/Udemy/Boson funnels bid these as loss leaders. Expect **$3–$6+ CPC** in US. Narrative: [[secplus-wedge-campaign/00-why-marketing-changed]].

---

## Wedge keyword tiers

### Tier W1 — Primary (own these)

| Theme                  | Example keywords                                                                  | Ad group                        |
| ---------------------- | --------------------------------------------------------------------------------- | ------------------------------- |
| No GNS3 / browser labs | `ccna practice labs free`, `cisco practical labs`, `ccna 200 301 practice labs`, `ccna labs without gns3`, `ccna vlan lab`, `ccna lab simulation` | **`CCNA_Wedge_Lab`** |
| Timed / exam sim       | `ccna timed practice test`, `ccna exam simulation online`, `ccna mock exam timed` | `ccna_timed_sim` *(new)*        |
| ENCOR labs             | `encor lab simulation`, `ccnp encor labs without gns3`                            | `encor_browser_labs` *(future)* |

#### `CCNA_Wedge_Lab` — Keyword Planner (US, Jun 2025–May 2026)

Source: Saved Keywords export 2026-06-15. Use **phrase (`"..."`)** for discovery; **exact (`[...]`)** on top converters.

| Match | Keyword | Planner vol/mo | Notes |
|-------|---------|----------------|-------|
| `[exact]` | `ccna practice labs free` | 30 | Highest volume · Low comp |
| `[exact]` | `cisco practical labs` | 30 | Highest volume · Low comp |
| `[exact]` | `ccna 200 301 practice labs` | 10 | Blueprint-aligned |
| `[exact]` | `ccna cli lab` | — | Product fit |
| `[exact]` | `ccna lab online` | — | Product fit |
| `"phrase"` | `ccna practice labs free` | 30 | Variant capture |
| `"phrase"` | `cisco practical labs` | 30 | Variant capture |
| `"phrase"` | `ccna 200 301 practice labs` | 10 | |
| `"phrase"` | `ccna 200 301 labs` | 10 | Low comp |
| `"phrase"` | `ccna 200 301 exam labs` | 10 | Medium comp — watch CPC |
| `"phrase"` | `cisco ccna practice labs` | 10 | Low comp |
| `"phrase"` | `ccna labs online` | — | |
| `"phrase"` | `ccna lab simulation` | — | |
| `"phrase"` | `ccna labs without gns3` | — | Differentiator (low Planner vol) |
| `"phrase"` | `ccna labs without packet tracer` | — | Differentiator |
| `"phrase"` | `ccna practice labs browser` | — | Differentiator |
| `"phrase"` | `ccna vlan lab` | — | Maps to free sample |
| `"phrase"` | `ccna topology for practice` | 10 | Medium comp — test |
| `"phrase"` | `exam lab practice` | 10 | Low comp |

**Do not add** (negate if seen in search terms): `ccna lab setup` (home-lab install), `exam mobile` (unrelated), `ccna pre test` (readiness — separate ad group/page).

**Promote rule:** search term with ≥3 clicks and a `begin_checkout` → add as `[exact]` if not already listed.

Repo checklist: `scripts/ccna-wedge-lab-google-ads-checklist.csv` · setup guide: `scripts/ccna-wedge-lab-google-ads.md`

### Security+ — Tier W1 (primary)

| Theme | Example keywords | Ad group |
|-------|------------------|----------|
| PBQ / performance-based | `[security+ pbq practice]`, `[sy0-701 pbq]`, `"security+ performance based questions"`, `"security+ pbq practice online"` | **`Security+ PBQ Practice`** |
| Browser sim | `"security+ simulation online"`, `"security+ pbq browser"` | **`Security+ PBQ Practice`** |
| Timed sim *(build page first)* | `"security+ timed practice test"`, `"sy0-701 mock exam timed"` | `secplus_timed_sim` *(new)* |
| Federal / 8140 *(optional)* | `"security+ 8140"`, `"dod security+ prep"` | `secplus_federal` *(future)* |

**Live wedge URL:**

```
https://becertifiedtoday.com/secplus/pbq-practice-browser.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=pbq-wedge
```

Repo checklist: `scripts/secplus-google-ads-campaign-checklist.csv` (Ad group 2) · wedge folder: [[secplus-wedge-campaign/README|secplus-wedge-campaign]]

### Tier W2 — Last-mile readiness

| Theme        | Example keywords                                                        |
| ------------ | ----------------------------------------------------------------------- |
| Final review | `ccna final review`, `ccna exam readiness`, `ccna practice before exam` |
| Scorecard    | `ccna practice test scorecard`, `ccna readiness test`                   |
| Anti-PDF     | `interactive ccna practice`, `ccna practice not pdf`                    |

### Tier W3 — Block (negatives)

`free course`, `bootcamp`, `udemy`, `coursera`, `netacad`, `dump`, `pdf download`, `jobs`, `salary`, `boson`, `ine`, `packet tracer download`, `gns3 download`, `examtopics`, `lab setup`, `exam mobile`

---

## Campaign structure (recommended)

| Ad group | Budget share | Pin H1 | Pin H2 | Final URL |
|----------|--------------|--------|--------|-----------|
| **`CCNA_Wedge_Lab`** | **100%** ($15/day launch) | CCNA 200-301 Practice Labs | $9.99 · 10-Day CCNA Labs | `/ccna/labs-without-gns3.html` |
| `ccna_timed_sim` | **25–30%** | 120-Min Timed CCNA Sim | $9.99 · 10-Day CCNA Bank | *(build)* |
| `ccna_portal_10v1` | **15–20%** | CCNA 200-301 · Walk In Ready | Test only; low bid | `ccna-home.html#purchase` |

### Security+ (recommended)

| Ad group | Budget share | Pin H1 | Pin H2 | Final URL |
|----------|--------------|--------|--------|-----------|
| **`Security+ PBQ Practice`** | **60–70%** (after day-7) | Security+ PBQ Practice | $9.99 · 10-Day Access | `/secplus/pbq-practice-browser.html` |
| `secplus_timed_sim` | **20–25%** *(build)* | 90-Min Timed Security+ Sim | $9.99 · 10-Day Access | `/secplus/timed-practice-test.html` |
| `secplus_portal_10d` | **15–20%** | Security+ Practice Test | $9.99 for 10-Day Access | `comptia-sec+-home.html#purchase` (low bid) |

See [[Security+ Campaign|Security+ Campaign]] for current live setup.

See [[../campaigns/CCNA Campaign|CCNA Campaign]] for CCNA live setup.

---

## Bidding (do not change strategy yet)

| Phase | Strategy |
|-------|----------|
| **Now** | Maximize Clicks, max CPC **$4.50–$5.00** on wedge groups only |
| **Not now** | Target impression share, top of page % — pays premium vs course vendors |
| **After 15–20 checkouts** | Maximize conversions (`begin_checkout`) |
| **After stable CPA** | Test impression share on **one wedge ad group only** |

Zero impressions ≠ wrong bid strategy. Check: ad status, keyword low volume, CPC cap, geo spread.

---

## Location targeting

1. **Presence:** people in or regularly in targeted locations
2. **Start:** United States, Canada, United Kingdom, Australia
3. **Hold:** India, Philippines, Nigeria (organic later)
4. **Expand:** only after US checkout CPA is acceptable

---

## Landing URL map (UTM)

| Intent | Landing | utm_content |
|--------|---------|-------------|
| **Exam-ready prep (primary)** | `https://becertifiedtoday.com/ccna-home.html` | `exam-readiness` |
| 10-day purchase | `https://becertifiedtoday.com/ccna-home.html#purchase` | `portal-10d` |
| 30-day purchase | `https://becertifiedtoday.com/ccna-home.html#purchase` | `portal-30d` |
| Browser labs compare | `https://becertifiedtoday.com/ccna-home.html#ccna-gns3-compare` | `browser-labs` |
| Timed sim | `https://becertifiedtoday.com/ccna-home.html#purchase` | `timed-sim` |
| NGTE previews (sitelink) | `https://becertifiedtoday.com/ccna-home.html#ccna-samples` | `sitelink-ngte` |
| PDF compare (sitelink) | `https://becertifiedtoday.com/ccna-home.html#ccna-compare` | `sitelink-compare` |

**Do not** use sitelinks or final URLs to `/sample?track=…` — sends free-question traffic past your value funnel.

**`CCNA_Wedge_Lab` final URL (copy-paste):**

```
https://becertifiedtoday.com/ccna-home.html?utm_source=google&utm_medium=cpc&utm_campaign=ccna_wedge_lab&utm_content=exam-readiness
```

**Do not** enable AI Max / final URL expansion — breaks message match and UTM variants.

---

## RSA angles (exam-ready, not free-sample)

Use headlines from `scripts/ccna-wedge-lab-google-ads-checklist.csv`:

- Scheduled CCNA? Prep Here
- $9.99 · 10-Day Full Access
- NGTE · Train Like Test Day
- 120-Min Timed Simulation
- Adaptive Weak-Area Testing
- Interactive · Not PDFs

**Avoid in RSA:** “Free”, “Try free sample”, “Free questions” — course vendors own that CPC.

---

## Weekly search-term workflow

1. Export Search terms (7 days)
2. Bucket: Convert · Test · Promote · Negative · Defer
3. Promote wedge terms with ≥3 clicks to phrase/exact
4. Add junk as campaign negatives
5. Log in [[06-30-day-action-plan|action plan]] decision log

See also: [[../campaigns/CCNA portal 10v1 — keyword research|CCNA keyword research]]

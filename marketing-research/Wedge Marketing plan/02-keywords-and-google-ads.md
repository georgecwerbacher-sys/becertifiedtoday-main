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

---

## Wedge keyword tiers

### Tier W1 — Primary (own these)

| Theme                  | Example keywords                                                                  | Ad group                        |
| ---------------------- | --------------------------------------------------------------------------------- | ------------------------------- |
| No GNS3 / browser labs | `ccna practice labs free`, `cisco practical labs`, `ccna 200 301 practice labs`, `ccna labs without gns3`, `ccna vlan lab`, `ccna lab simulation` | `ccna_browser_labs`             |
| Timed / exam sim       | `ccna timed practice test`, `ccna exam simulation online`, `ccna mock exam timed` | `ccna_timed_sim` *(new)*        |
| ENCOR labs             | `encor lab simulation`, `ccnp encor labs without gns3`                            | `encor_browser_labs` *(future)* |

#### `ccna_browser_labs` — Keyword Planner (US, Jun 2025–May 2026)

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

Repo checklist: `scripts/ccna-google-ads-campaign-checklist.csv`

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
| `ccna_browser_labs` | **50–60%** | CCNA 200-301 Practice Labs | $9.99 · 10-Day CCNA Labs | `/ccna/labs-without-gns3.html` |
| `ccna_timed_sim` | **25–30%** | 120-Min Timed CCNA Sim | $9.99 · 10-Day CCNA Bank | *(build)* |
| `ccna_portal_10v1` | **15–20%** | CCNA 200-301 · Walk In Ready | Test only; low bid | `ccna-home.html#purchase` |

See [[../campaigns/CCNA Campaign|CCNA Campaign]] for current live setup.

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
| 10-day purchase | `https://becertifiedtoday.com/ccna-home.html#purchase` | `portal-10d` |
| **Browser labs (primary)** | `https://becertifiedtoday.com/ccna/labs-without-gns3.html` | `browser-labs` |
| CCNA hub (samples) | `https://becertifiedtoday.com/ccna-home.html` | `sitelink-samples` |
| Timed sim | `/ccna/timed-practice-test.html` *(build)* | `timed-sim` |
| VLAN sample | `https://becertifiedtoday.com/sample?track=ccna-vlan` | `sitelink-lab` |
| Drag-and-drop sample | `https://becertifiedtoday.com/sample?track=ccna-dnd` | `sitelink-dnd` |
| Question sample | `https://becertifiedtoday.com/sample?track=ccna-questions` | `sitelink-sample` |

**`ccna_browser_labs` final URL (copy-paste):**

```
https://becertifiedtoday.com/ccna/labs-without-gns3.html?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=browser-labs
```

**Do not** enable AI Max / final URL expansion — breaks message match and UTM variants.

---

## RSA angles (wedge, not generic)

Use headlines from `scripts/ccna-google-ads-campaign-checklist.csv` — differentiated set:

- VLAN CLI Lab In Browser
- No GNS3 · Prep In Browser
- 120-Min Timed CCNA Sim
- v1.1 & v2.0 · Verified
- Not PDF Dumps · Live Prep
- Try Free CCNA Samples

---

## Weekly search-term workflow

1. Export Search terms (7 days)
2. Bucket: Convert · Test · Promote · Negative · Defer
3. Promote wedge terms with ≥3 clicks to phrase/exact
4. Add junk as campaign negatives
5. Log in [[06-30-day-action-plan|action plan]] decision log

See also: [[../campaigns/CCNA portal 10v1 — keyword research|CCNA keyword research]]

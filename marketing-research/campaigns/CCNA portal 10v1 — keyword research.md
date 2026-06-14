---
type: research
product: ccna
ad_group: ccna_portal_10v1
test_window: 2026-06-14..2026-06-21
tags:
  - marketing
  - keywords
  - ccna
---

# CCNA portal 10v1 — keyword research

**Live ad group:** `ccna_portal_10v1` only during 7-day test. `ccna_browser_labs` deferred.

**Conversion to optimize:** GA4 `begin_checkout` with `ccna_portal_10d` (Stripe $9.99 / 10-day).

## Site objective (becertifiedtoday.com CCNA)

See [[Site Mission]] for full positioning. For this ad group:

1. **Attract** high-intent CCNA 200-301 searchers (practice test, mock exam, question bank).
2. **Land** on `ccna-home.html#purchase` with `utm_content=portal-10d` → $9.99 / 10-day CTA.
3. **Prove value** with free samples before checkout.
4. **Convert** to 10-day portal — browser prep, verified explanations, no membership.

**Success metric:** GA4 `begin_checkout` (`ccna_portal_10d`).

## Under-realized keyword framework

*Under-realized* = strong fit with your landing + product, but **low or zero paid coverage** or **clicks without `begin_checkout`**.

| Signal | Where to find it | Action |
|--------|------------------|--------|
| Search term has clicks, no checkout | Google Ads → Search terms (7 days) | Improve RSA/landing match or add negative |
| Search term has checkout | Search terms + GA4 `begin_checkout` | Promote to exact match |
| Term on site, not in ad group | This doc + `ccna-home.html` meta | Add phrase after day 7 |
| Lab/GNS3 intent | Search terms | Route to `ccna_browser_labs` when live — not portal_10v1 |
| Course/dump/job intent | Search terms | Campaign negative |

## Site-aligned keyword tiers (portal_10v1)

### Tier A — in ad group now (practice-test intent)

- `[ccna practice test]` · `[ccna mock exam]` · `[ccna question bank]`
- `"ccna practice test online"` · `"ccna mock exam online"` · `"ccna 200-301 exam prep"`

### Tier B — on site, under-covered in ads (watch search terms)

| Theme | Example queries | Site proof |
|-------|-----------------|------------|
| Timed / simulation | ccna timed practice test, ccna exam simulation online | Timed sim, mock exam hero variants |
| Free try-first | ccna free practice test, free ccna mock exam | Free assessment, samples ATF |
| Scorecard | ccna practice test scorecard | Free assessment scorecard |
| Cisco-branded | cisco ccna practice test online | Meta + Cisco CCNA Prep variant |
| Exam code | ccna 200-301 practice questions | v1.1 / 200-301 copy throughout |
| Anti-PDF | ccna practice test not pdf, interactive ccna prep | “No PDFs” positioning |

**Day 7 rule:** add Tier B terms only if search terms report shows ≥5 clicks and ≥1 checkout, or ≥10 clicks with strong CTR (>2%).

### Tier C — defer to `ccna_browser_labs` (wrong ad group)

- ccna cli lab, ccna labs without gns3, packet tracer alternative, vlan lab online

### Tier D — block (negatives)

- course, bootcamp, netacad, dump, pdf download, jobs, salary, udemy

## 7-day research workflow

### Daily (5 min)

1. Google Ads → Campaign → **Search terms** (last 7 days)
2. Export or note: term · impressions · clicks · cost · conversions (`begin_checkout`)
3. GA4 Realtime / Explorations: `begin_checkout` where `sessionCampaignName = ccna_portal`

### Day 3

Bucket each search term:

| Bucket | Criteria |
|--------|----------|
| **Convert** | Has checkout or checkout rate > campaign avg |
| **Test** | Clicks, no checkout — headline/landing mismatch? |
| **Promote** | Not in keyword list, ≥3 clicks, on-topic |
| **Negative** | Off-topic (course, jobs, dump, wrong exam) |
| **Defer** | Lab/GNS3 intent → browser_labs backlog |

### Day 7

Fill table below from Search terms + GA4:

| Search term | Clicks | Checkouts | CPC | Fit (A/B/C/D) | Action |
|-------------|--------|-----------|-----|---------------|--------|
| _(paste from Ads)_ | | | | | |

**Decisions:**

- **Scale portal_10v1:** top 3 converting terms → exact match; raise budget only if CPA acceptable
- **Add Tier B:** phrases with clicks + message match
- **Launch browser_labs:** if ≥20% of spend went to lab-intent terms (Tier C)
- **Cut:** keywords with spend, zero checkouts, after 50+ clicks

## Competitor gap angles (from site positioning)

Use in RSA tests, not as new keywords until search terms validate:

- vs **Boson/INE**: no install, browser-only, $9.99 entry
- vs **PDF/dumps**: interactive, verified explanations, v1.1
- vs **Packet Tracer/GNS3**: VLAN lab in browser (browser_labs ad group later)

## Data sources in repo

- Live keywords: [[campaigns/ccna-campaign-checklist.csv|checklist]] Ad group 1 rows
- Hero/UTM variants: `public/js/ccna-home-conversion.js`
- Portal landing: `public/js/ccna-portal-10d-landing.js` (`utm_content=portal-10d`)
- Competitors: [[../Competitors|Competitors]] (`*-ccna.md`)
- Weekly GA4: `node scripts/marketing-weekly-report.mjs --range 7d`

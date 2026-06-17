# SEC+_Wedge_PBQ — Google Ads campaign setup

**Paste-ready checklist (primary):** `scripts/secplus-wedge-pbq-google-ads-checklist.csv`  
**README:** `scripts/secplus-wedge-pbq-google-ads-README.txt`  
**Obsidian folder:** `marketing-research/Wedge Marketing plan/secplus-wedge-campaign/`  
**Build steps:** `marketing-research/Wedge Marketing plan/secplus-wedge-campaign/01-build-steps.md`  
**Keywords:** `marketing-research/Wedge Marketing plan/secplus-wedge-campaign/03-keywords-ad-group.md`  
**Strategy context:** `marketing-research/Wedge Marketing plan/secplus-wedge-campaign/00-why-marketing-changed.md`

Dedicated **Search** campaign for Security+ PBQ / performance-based wedge keywords. One ad group: **`SEC+_Wedge_PBQ`**. Landing page is live at `/secplus/pbq-practice-browser.html`.

---

## Campaign shell

| Setting | Value |
|---------|--------|
| **Campaign name** | `SEC+_Wedge_PBQ` |
| **Type** | Search (Search partners **off**, Display **off**) |
| **Daily budget** | **$8.00/day** (scale to $12–15 after stable CPA) |
| **Bidding (weeks 1–2)** | Maximize clicks, max CPC **$3.50** |
| **Bidding (after 15–20 checkouts)** | Maximize conversions → GA4 `begin_checkout` |
| **utm_campaign** | `secplus_wedge_pbq` |
| **Language** | English |
| **AI Max / URL expansion** | **Off** |

### Conversion

Import GA4 **`begin_checkout`** as primary conversion (`secplus_portal_10d` $9.99 · `secplus_portal_30d` $19.99).

**Tag policy:** only marketing URLs are tagged — `scripts/marketing-tag-minimal-list.md` · enforced by `public/js/analytics-exclude.js`.

---

## Ad group: `SEC+_Wedge_PBQ`

| Setting | Value |
|---------|--------|
| **Ad group name** | `SEC+_Wedge_PBQ` |
| **Display path** | `Security+` / `PBQ-Practice` |
| **Intent** | SY0-701 browser PBQ practice — chain labs, hot spots, no download |
| **Default match** | Phrase for discovery; Exact on verified Planner terms |

### Final URL (copy-paste)

```
https://becertifiedtoday.com/secplus/pbq-practice-browser.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=pbq-wedge
```

**Landing proof points** (message match):

- Free dark web IR PBQ sample (same UI as paid)
- 28 PBQ scenarios — chain labs, hot spots, exhibits
- Browser-only — no download or desktop sim install
- $9.99 / 10-day and $19.99 / 30-day pricing on page

### RSA pins

| Pin | Headline |
|-----|----------|
| **H1** | `Security+ PBQ Practice` |
| **H2** | `$9.99 · 10-Day Access` |

All 15 headlines and 4 descriptions are in the checklist CSV — filter **Section** = `Headline` or `Description`.

---

## Keywords — verify in Keyword Planner first

Run US Keyword Planner on these themes **before** pasting into Google Ads. Check the **Keyword Planner** phase rows in the CSV as you confirm volumes.

### Exact (starter — verify volume)

```
[security+ pbq practice]
[sy0-701 pbq]
[security+ performance based questions]
[comptia security+ pbq]
```

Add exact only when Planner shows usable volume or a search term converts.

### Phrase (starter — verify volume)

```
"security+ pbq practice"
"security+ performance based questions"
"security+ pbq practice online"
"comptia security+ pbq"
"sy0-701 performance based"
"sy0-701 pbq practice"
"security+ simulation online"
"security+ pbq browser"
"security+ pbq chain lab"
"security+ interactive practice"
```

**Do not add:** course/bootcamp/training variants — negate if they appear in search terms.

**Promote rule:** search term with ≥3 clicks + `begin_checkout` → add as `[exact]`.

### Keyword Planner worksheet (fill after export)

| Match | Keyword | Planner vol/mo | Comp | Add? |
|-------|---------|----------------|------|------|
| `[exact]` | `security+ pbq practice` | | | |
| `[exact]` | `sy0-701 pbq` | | | |
| `[exact]` | `security+ performance based questions` | | | |
| `"phrase"` | `security+ pbq practice online` | | | |
| `"phrase"` | `security+ simulation online` | | | |
| `"phrase"` | `security+ pbq browser` | | | |
| | *(add rows from Planner)* | | | |

---

## Location targeting

**Launch (week 1):**

1. **Presence:** people in or regularly in targeted locations
2. **Countries:** United States, Canada, United Kingdom, Australia

**Expand after US CPA is acceptable:** remaining Tier A countries in `scripts/secplus-portal-10d-google-ads.md`.

---

## Campaign negatives (phrase)

Block course vendors, unauthorized-content intent, cross-cert junk, and head terms this campaign should not own:

```
"free course"
"training course"
bootcamp
"instructor led"
"unauthorized exam content"
"exam content"
"pass guarantee"
"pdf download"
udemy
coursera
boson
"professor messer"
"dion training"
jobs
salary
examtopics
"security+ practice test"
"security+ question bank"
"comptia security+ practice test"
"sy0-701 question bank"
ccna
cissp
```

**Ad group negatives:** `course`, `unauthorized`, `pdf`, `jobs`, `training`

---

## Sitelinks (campaign level)

| Label | URL utm_content |
|-------|-----------------|
| Free Dark Web PBQ | `sitelink-pbq` |
| Free Practice Questions | `sitelink-sample` |
| 28 PBQ Scenarios | `sitelink-pbq-list` |
| 10-Day Access · $9.99 | `portal-10d` |
| 90-Min Timed Exam Sim | `sitelink-sim` |
| Security+ Exam Prep Home | `sitelink-home` |

Base: `utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq`

---

## Build steps (Google Ads UI)

### Phase 1 — Pre-launch

1. Confirm Stripe $9.99 and $19.99 products live
2. Test checkout from wedge landing pricing cards (desktop + mobile)
3. Confirm GA4 `begin_checkout` in Realtime
4. Import `begin_checkout` as primary conversion in Google Ads
5. **Pause** `secplus_pbq_wedge` in the old `Security+ SY0-701 · Exam prep` campaign (if enabled)
6. Confirm https://becertifiedtoday.com/secplus/pbq-practice-browser.html loads pricing + FAQ
7. Complete free dark web PBQ sample on phone + desktop

### Phase 2 — Keyword Planner (you)

1. Export US Keyword Planner for PBQ / performance-based / simulation themes
2. Fill worksheet table above — mark Add? yes/no
3. Update checklist CSV Keyword Planner rows
4. Remove zero-volume or wrong-intent terms before launch

### Phase 3 — Create campaign

1. New Search campaign → name **`SEC+_Wedge_PBQ`**
2. Budget **$8/day** · Search partners off · Display off
3. Bidding: Maximize clicks, max CPC **$3.50**
4. Locations: US, CA, UK, AU (presence only)
5. Language: English
6. Disable AI Max / final URL expansion

### Phase 4 — Create ad group `SEC+_Wedge_PBQ`

1. Ad group name: **`SEC+_Wedge_PBQ`**
2. Display path: `Security+` / `PBQ-Practice`
3. Final URL: wedge landing with UTMs (see above)
4. Add verified **exact** and **phrase** keywords
5. Create RSA → paste 15 headlines + 4 descriptions from CSV
6. Pin H1 and H2 per table above

### Phase 5 — Extensions + negatives

1. Add 6 sitelinks (table above)
2. Paste campaign negatives
3. Add ad group negatives

### Phase 6 — Launch verification

1. Enable campaign + ad group
2. Open final URL — pricing cards + FAQ visible
3. Click **Try free dark web PBQ sample** — same browser UI
4. Test $9.99 checkout → Stripe
5. Confirm `begin_checkout` in GA4 Realtime
6. Test sitelinks on mobile

### Phase 7 — Week 1 ops

| When | Action |
|------|--------|
| Daily | Impressions, clicks, spend, checkouts |
| Day 3 | Search terms → add junk negatives |
| Day 7 | CTR, CPC, CPA → promote converters to exact |

**Hold during week 1:** budget, bidding, geo, RSA copy.

---

## Avoid self-competition

| Old asset | Action |
|-----------|--------|
| `secplus_pbq_wedge` in `secplus_portal` campaign | **Pause** when `SEC+_Wedge_PBQ` goes live |
| `secplus_portal_10d` head-term campaign | Keep separate; low bid or paused per wedge plan |

---

## Related files

- `scripts/secplus-wedge-pbq-google-ads-checklist.csv` — Numbers-friendly step tracker
- `marketing-research/Wedge Marketing plan/secplus-wedge-campaign/` — Obsidian build folder
- `public/secplus/pbq-practice-browser.html` — live landing page

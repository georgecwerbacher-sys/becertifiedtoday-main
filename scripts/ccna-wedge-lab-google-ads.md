# CCNA_Wedge_Lab — Google Ads campaign setup

**Paste-ready checklist (primary):** `scripts/ccna-wedge-lab-google-ads-checklist.csv`  
**README:** `scripts/ccna-wedge-lab-google-ads-README.txt`  
**Strategy context:** `marketing-research/Wedge Marketing plan/02-keywords-and-google-ads.md`

Dedicated **Search** campaign for browser CLI lab wedge keywords. One ad group: **`CCNA_Wedge_Lab`**. Landing page is live at `/ccna/labs-without-gns3.html`.

---

## Campaign shell

| Setting | Value |
|---------|--------|
| **Campaign name** | `CCNA_Wedge_Lab` |
| **Type** | Search (Search partners **off**, Display **off**) |
| **Daily budget** | **$15.00/day** (scale to $20–25 after stable CPA) |
| **Bidding (weeks 1–2)** | Maximize clicks, max CPC **$4.50** |
| **Bidding (after 15–20 checkouts)** | Maximize conversions → GA4 `begin_checkout` |
| **utm_campaign** | `ccna_wedge_lab` |
| **Language** | English |
| **AI Max / URL expansion** | **Off** |

### Conversion

Import GA4 **`begin_checkout`** as primary conversion (`ccna_portal_10d` $9.99 · `ccna_portal_30d` $19.99).

**Tag policy:** only marketing URLs are tagged — `scripts/marketing-tag-minimal-list.md` · enforced by `public/js/analytics-exclude.js`.

---

## Ad group: `CCNA_Wedge_Lab`

| Setting | Value |
|---------|--------|
| **Ad group name** | `CCNA_Wedge_Lab` |
| **Display path** | `CCNA` / `Practice-Labs` |
| **Intent** | CCNA browser CLI labs — no GNS3 / Packet Tracer |
| **Default match** | Phrase for discovery; Exact on top Planner terms |

### Final URL (copy-paste)

```
https://becertifiedtoday.com/ccna/labs-without-gns3.html?utm_source=google&utm_medium=cpc&utm_campaign=ccna_wedge_lab&utm_content=browser-labs
```

**Landing proof points** (message match):

- Free VLAN CLI lab sample (same UI as paid)
- Exam-style browser simulation — type real IOS commands
- Helper and solution files on every lab
- Practice unlimited times (Reset lab)
- $9.99 / 10-day and $19.99 / 30-day pricing on page

### RSA pins

| Pin | Headline |
|-----|----------|
| **H1** | `CCNA 200-301 Practice Labs` |
| **H2** | `$9.99 · 10-Day CCNA Labs` |

All 15 headlines and 4 descriptions are in the checklist CSV — filter **Section** = `Headline` or `Description`.

---

## Keywords

### Exact (5)

```
[ccna practice labs free]
[cisco practical labs]
[ccna 200 301 practice labs]
[ccna cli lab]
[ccna lab online]
```

### Phrase (14)

```
"ccna practice labs free"
"cisco practical labs"
"ccna 200 301 practice labs"
"ccna 200 301 labs"
"ccna 200 301 exam labs"
"cisco ccna practice labs"
"ccna labs online"
"ccna lab simulation"
"ccna labs without gns3"
"ccna labs without packet tracer"
"ccna practice labs browser"
"ccna vlan lab"
"ccna topology for practice"
"exam lab practice"
```

**Do not add:** `ccna lab setup`, `exam mobile`, `ccna pre test` — negate if they appear in search terms.

**Promote rule:** search term with ≥3 clicks + `begin_checkout` → add as `[exact]`.

Source: Keyword Planner US export 2026-06-15.

---

## Location targeting

**Launch (week 1):**

1. **Presence:** people in or regularly in targeted locations
2. **Countries:** United States, Canada, United Kingdom, Australia

**Expand after US CPA is acceptable:** remaining Tier A countries in `scripts/ccna-portal-10d-google-ads.md`.

---

## Campaign negatives (phrase)

Block course vendors, dumps, install intent, and head terms this campaign should not own:

```
"free course"
"training course"
bootcamp
"instructor led"
"brain dump"
"exam dump"
"guaranteed pass"
"pdf download"
udemy
coursera
boson
"cisco netacad"
jobs
salary
"packet tracer download"
"gns3 download"
examtopics
"lab setup"
"exam mobile"
"ccna practice test"
"ccna mock exam"
"ccna question bank"
```

**Ad group negatives:** `course`, `dump`, `pdf`, `jobs`, `netacad`

---

## Sitelinks (campaign level)

| Label | URL utm_content |
|-------|-----------------|
| Free VLAN CLI Lab | `sitelink-lab` |
| 10-Day Access · $9.99 | `portal-10d` |
| 30-Day Access · $19.99 | `portal-30d` |
| Free Practice Questions | `sitelink-sample` |
| Sample Drag-and-Drop | `sitelink-dnd` |
| CCNA Exam Prep Home | `sitelink-home` |

Base: `utm_source=google&utm_medium=cpc&utm_campaign=ccna_wedge_lab`

---

## Build steps (Google Ads UI)

### Phase 1 — Pre-launch

1. Confirm Stripe $9.99 and $19.99 products live
2. Test checkout from wedge landing pricing cards (desktop + mobile)
3. Confirm GA4 `begin_checkout` in Realtime
4. Import `begin_checkout` as primary conversion in Google Ads
5. **Pause** `ccna_browser_labs` in the old `CCNA 200-301 · Exam prep` campaign (if enabled) to avoid self-competition
6. Confirm https://becertifiedtoday.com/ccna/labs-without-gns3.html loads pricing + FAQ

### Phase 2 — Create campaign

1. New Search campaign → name **`CCNA_Wedge_Lab`**
2. Budget **$15/day** · Search partners off · Display off
3. Bidding: Maximize clicks, max CPC **$4.50**
4. Locations: US, CA, UK, AU (presence only)
5. Language: English
6. Disable AI Max / final URL expansion

### Phase 3 — Create ad group `CCNA_Wedge_Lab`

1. Ad group name: **`CCNA_Wedge_Lab`**
2. Display path: `CCNA` / `Practice-Labs`
3. Final URL: wedge landing with UTMs (see above)
4. Add all **exact** and **phrase** keywords
5. Create RSA → paste 15 headlines + 4 descriptions from CSV
6. Pin H1 and H2 per table above

### Phase 4 — Extensions + negatives

1. Add 6 sitelinks (table above)
2. Paste campaign negatives
3. Add ad group negatives

### Phase 5 — Launch verification

1. Enable campaign + ad group
2. Open final URL — pricing cards + blue FAQ visible
3. Click **Try free VLAN lab sample** — same CLI UI
4. Test $9.99 checkout → Stripe
5. Confirm `begin_checkout` in GA4 Realtime
6. Test sitelinks on mobile

### Phase 6 — Week 1 ops

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
| `ccna_browser_labs` in `ccna_portal` campaign | **Pause** when `CCNA_Wedge_Lab` goes live |
| `ccna_portal_10v1` head-term campaign | Keep separate; low bid or paused per wedge plan |

---

## Related files

- `scripts/ccna-wedge-lab-google-ads-checklist.csv` — Numbers-friendly step tracker
- `marketing-research/campaigns/CCNA Wedge Lab Campaign.md` — Obsidian campaign note
- `public/ccna/labs-without-gns3.html` — live landing page

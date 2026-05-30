---
type: playbook
status: active
tags:
  - keywords
  - google-ads
  - seo
created: 2026-05-30
---

# Keyword collection plan

Build a repeatable pipeline from **paid search data** → **Obsidian vault** → **landing page / ad copy** updates. Goal: know which terms convert, which to negate, and which deserve new CTA landings—without relying on static keyword guesses.

Related: [[../01-strategy/google-ai-search-strategy|AI search strategy]] · [[../02-campaigns/security-plus-google-ads|Security+ campaign]] · [[../07-keywords/README|07-keywords/]]

---

## Why now

- Landing pages and ad groups are being built (Security+ portal, OpenSSL PBQ CTA, CCNA hero variants).
- Site copy is shifting toward **exam prep** and away from friction claims (e.g. removed “no email required” — room to capture email on free assessment / sample flows soon).
- Keywords should come from **actual queries** (Ads search terms, Search Console) not only brainstorm lists.

---

## Vault layout (`07-keywords/`)

```
07-keywords/
  README.md
  search-terms/          # weekly raw + tagged exports
  negatives/             # master negative lists by campaign
  landing-maps/          # keywords ↔ URL ↔ ad group
  templates/
    search-terms-weekly-import.md
```

**Naming:** `search-terms/YYYY-MM-DD-{utm_campaign}.md`  
Example: `search-terms/2026-06-06-secplus_portal.md`

---

## Phase 1 — Manual weekly (start here, ~30 min/week)

**When:** Same day as [[weekly-review-process|weekly marketing review]] (after Ads has 7+ days of data).

### Step 1 — Export from Google Ads

1. **Search terms** report: campaign → Keywords → Search terms.
2. Date range: last 7 or 28 days.
3. Columns: Search term, Match type, Campaign, Ad group, Impressions, Clicks, Cost, Conversions, CTR.
4. Filter: impressions ≥ 1 (or ≥ 5 once volume grows).

### Step 2 — Import to vault

1. Duplicate [[../07-keywords/templates/search-terms-weekly-import|search-terms-weekly-import]] template.
2. Save as `07-keywords/search-terms/YYYY-MM-DD-{campaign}.md`.
3. Paste table or bullet list of terms.

### Step 3 — Tag each term

| Tag | Action |
|-----|--------|
| `keep` | Already targeted; good performance |
| `promote` | Add as Exact/Phrase keyword or new ad group |
| `negative` | Add to [[../07-keywords/negatives/master-negative-list|master negative list]] or campaign file |
| `landing` | Update H1/meta on a specific page note |
| `watch` | Low volume; recheck next week |
| `junk` | Irrelevant; negative immediately |

### Step 4 — Promote to campaign / page notes

- **New high-intent term** → row in relevant `02-campaigns/*.md` ad group table.
- **Landing message match gap** → update `06-website-optimization/pages/*.md` + site HTML.
- **Negative** → append to `07-keywords/negatives/{campaign}.md` and apply in Ads UI.

### Step 5 — Log decisions

Add one line to campaign **Decisions log** and [[../06-website-optimization/content-change-log|content change log]] when copy or negatives ship.

---

## Phase 2 — Search Console + GA4 (week 2–4)

Complement paid terms with organic queries.

| Source | Export | Vault destination |
|--------|--------|-------------------|
| Google Search Console | Queries, landing page, clicks, position | `search-terms/YYYY-MM-DD-gsc.md` |
| GA4 | Organic landing pages + session source (already in weekly report) | link from `03-reports/weekly/` |

**Rule:** If a query ranks organically with decent impressions but no Ads keyword, test a **low-bid Exact** match or improve on-page copy first.

---

## Phase 3 — Automation (near future)

Implement when Phase 1 runs cleanly for 2–3 weeks.

| Task | Tool | Output |
|------|------|--------|
| Ads search terms pull | Google Ads API or scheduled CSV + script | `07-keywords/search-terms/` auto-file |
| Negative diff | Script compares new junk vs `negatives/` | PR-ready negative list |
| Keyword → page map | Dataview over `landing-maps/*.md` | Dashboard in Obsidian |
| Weekly merge | Extend `scripts/marketing-weekly-report.mjs` | Section in weekly report: top 10 new search terms |

**Script stub (future):** `scripts/marketing-search-terms-import.mjs`

```bash
# planned
node scripts/marketing-search-terms-import.mjs --csv ~/Downloads/search-terms.csv --campaign secplus_portal
```

Requirements before building:

- [ ] Google Ads API credentials in `.env.local` (or stable manual CSV path)
- [ ] Campaign slug convention matches `utm_campaign` in `02-campaigns/`
- [ ] Template + tagging rules proven manually

---

## Email capture alignment

**Shipped (Security+):** Free timed simulation + scorecard email — [[../02-campaigns/security-plus-lead-magnet-ads|lead magnet ads note]] · `#secplus-lead-capture` · `POST /api/lead-capture` · `POST /api/secplus-scorecard-email`

Still planned:

1. **Optional email gate** on free CCNA assessment (soft capture before scorecard).
2. **Follow-up** via portal-request-link flow (already used post-purchase).
3. **Keyword angle shift:** less “free no signup”, more “free practice test / exam prep” — see [[../01-strategy/positioning-and-messaging|positioning]].

When measuring lead ads, tag search terms containing `free` + high bounce separately; expect CPA to change vs purchase-only campaigns.

---

## Dataview queries (Obsidian)

Recent search term imports:

```dataview
TABLE campaign, term_count, promoted, negated
FROM "07-keywords/search-terms"
SORT file.name DESC
LIMIT 12
```

---

## Checklist — first 30 days

- [ ] Create first manual import: `search-terms/YYYY-MM-DD-secplus_portal.md`
- [ ] Create `negatives/master-negative-list.md` from [[../06-website-optimization/pages/simulation-secure-web-architecture-openssl#Negative keywords|OpenSSL page negatives]] + campaign note
- [ ] Weekly: tag terms during [[weekly-review-process|weekly review]]
- [ ] After 2 imports: promote 3–5 terms to live ad groups
- [ ] After 4 imports: scoping doc for `marketing-search-terms-import.mjs`
- [ ] Search Console export added to workflow

---

## Owners & cadence

| Activity | Cadence | Where logged |
|----------|---------|--------------|
| Search terms export | Weekly | `07-keywords/search-terms/` |
| Negative updates | Weekly | `07-keywords/negatives/` + Ads UI |
| Landing keyword sync | When copy changes | `06-website-optimization/pages/` |
| Automation build | After 2–3 manual weeks | this note + GitHub issue |

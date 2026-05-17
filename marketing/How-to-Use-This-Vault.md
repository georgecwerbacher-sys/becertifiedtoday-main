# How to use this vault (step-by-step)

This note is your **operating manual** for the marketing Obsidian vault. Follow the phases in order the first time; after launch, jump to [[#Weekly rhythm (ongoing)]].

**Vault path:** `/Users/werby/CCNP_Study_main/marketing`  
**Start screen:** [[Dashboard]]

---

## Phase 0 — Open the vault (one time)

1. In Obsidian: **File → Open folder as vault…**
2. Press **Cmd + Shift + G** and paste: `/Users/werby/CCNP_Study_main/marketing`
3. Click **Open** / **Trust**.
4. Open **[[Dashboard]]** (or this note from Quick Switcher: **Cmd + O**).

**You’re in the right vault if** the sidebar shows `Dashboard.md`, `01-Strategy`, `02-Campaigns`, etc. at the **top level** — not a nested `marketing` folder inside another repo.

**Wrong vault?** If you opened `CCNP_Study` (no `_main`) or `becertifiedtoday`, you won’t see these files. Switch vault via the icon bottom-left → choose **marketing**.

---

## Phase 1 — One-time setup (before spending on ads)

Do these once. Check off as you go.

| Step | Action | Where |
|------|--------|--------|
| 1 | Read positioning and who you sell to | [[01-Strategy/Positioning-and-ICP]] |
| 2 | Set budget, target CPA, and ROAS blanks | [[01-Strategy/Marketing-Plan]] §1 Goals |
| 3 | Copy targets into the KPI log | [[05-Analytics/KPI-Dashboard]] |
| 4 | Link GA4 to Google Ads; turn on auto-tagging | [[05-Analytics/GA4-Google-Ads-Integration]] |
| 5 | Mark `begin_checkout` as a conversion in GA4; import into Ads | Same note, §2 |
| 6 | Confirm site loads attribution (already in repo on main landings) | `public/js/campaign-attribution.js` |
| 7 | Skim UTM naming — use the same pattern on every ad URL | [[05-Analytics/UTM-Conventions]] |
| 8 | Skim which URLs ads should send to | [[04-Landing-Pages/Landing-Page-Map]] |

**Site is already wired for:** `index.html`, `ccna-home.html`, `ccnp-home.html` (GA4 + UTM/gclid capture + `begin_checkout` on purchase clicks).

---

## Phase 2 — Build your first campaigns (week 1)

| Step | Action | Where |
|------|--------|--------|
| 1 | Duplicate the campaign template twice (brand + exam intent) | [[02-Campaigns/_Campaign-Template]] → save as e.g. `ccna-search-brand.md`, `ccna-search-exam-intent.md` |
| 2 | Pull keywords and negatives into each campaign note | [[03-Keywords/Keyword-Research-CCNA]] |
| 3 | Write RSA headlines/descriptions (no dump/guarantee language) | Campaign notes + [[01-Strategy/Marketing-Plan]] §6 Creative |
| 4 | Build final URLs with UTMs | [[05-Analytics/UTM-Conventions]] — example: |
| | `https://becertifiedtoday.com/ccna-home.html?utm_source=google&utm_medium=cpc&utm_campaign=ccna-search-exam-intent&utm_content=exam-simulation&utm_term={keyword}` | |
| 5 | Create campaigns in **Google Ads** (Search only; brand + exam intent first) | Google Ads UI |
| 6 | Update the campaign table on the Dashboard | [[Dashboard]] § Active campaigns |
| 7 | Run first **weekly review** (even if only a few days of data) | [[06-Content-Calendar/Weekly-Review-Template]] |

**Recommended launch order:** Campaign A **brand** (`ccna-search-brand`) → Campaign B **exam intent** (`ccna-search-exam-intent`). Hold **CCNP** until CCNA has conversion data ([[01-Strategy/Marketing-Plan]] §4).

---

## Phase 3 — First 90 days (what to do when)

Use [[01-Strategy/Marketing-Plan]] §8 as the master checklist. Summary:

### Weeks 1–2 — Foundation

- [ ] Ads account + billing live  
- [ ] GA4 ↔ Ads linked; conversions imported  
- [ ] Two Search campaigns live with UTMs  
- [ ] First weekly review completed  

### Weeks 3–6 — Optimize

- [ ] Expand negative keyword list  
- [ ] Test 2 RSA angles (simulation-led vs labs-led)  
- [ ] Tune bids; consider tCPA if volume allows  
- [ ] Tighten landing H1 + single CTA above the fold  

### Weeks 7–12 — Scale or pivot

- [ ] Increase budget on winners (CPA below target)  
- [ ] Launch CCNP campaign only if CCNA CPA holds  
- [ ] Consider remarketing when traffic supports it  

---

## Weekly rhythm (ongoing)

Every week (pick a fixed day):

1. **Open** [[Dashboard]] → review “This week” (update if priorities changed).
2. **Google Ads:** export or note spend, clicks, conversions by campaign.
3. **Search terms:** add negatives; promote winners to exact/phrase if appropriate.
4. **Fill** [[05-Analytics/KPI-Dashboard]] (new row for the week).
5. **Duplicate** [[06-Content-Calendar/Weekly-Review-Template]] → rename with date → log hypotheses and next 3 priorities.
6. **Update** each live campaign note’s “Results log” table in `02-Campaigns/`.

**Reconcile weekly:** Google Ads conversions vs GA4 `begin_checkout` vs Stripe revenue ([[05-Analytics/GA4-Google-Ads-Integration]] §7). UTMs don’t pass into Stripe Payment Links — GA4 + Stripe dashboard is the source of truth.

---

## Where each folder fits

| Folder | When you use it |
|--------|-----------------|
| `01-Strategy` | Positioning, 90-day plan, goals — revisit monthly |
| `02-Campaigns` | One note per live/paused Google Ads campaign |
| `03-Keywords` | Research, match types, shared negative lists |
| `04-Landing-Pages` | URL map, ad ↔ page message match |
| `05-Analytics` | UTMs, GA4 setup, KPI numbers |
| `06-Content-Calendar` | Weekly reviews and experiment log |

---

## Quick reference — key links

| I need to… | Open |
|------------|------|
| See everything at a glance | [[Dashboard]] |
| Understand strategy & phases | [[01-Strategy/Marketing-Plan]] |
| Set up tracking | [[05-Analytics/GA4-Google-Ads-Integration]] |
| Name UTMs consistently | [[05-Analytics/UTM-Conventions]] |
| Log numbers | [[05-Analytics/KPI-Dashboard]] |
| Start a new campaign note | [[02-Campaigns/_Campaign-Template]] |
| Run the weekly meeting with yourself | [[06-Content-Calendar/Weekly-Review-Template]] |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Don’t see `marketing` in Obsidian | Open vault path above; don’t open whole `CCNP_Study_main` repo unless you want code + marketing mixed |
| Opened `CCNP_Study` instead of `CCNP_Study_main` | Older folder has **no** `marketing` — use `CCNP_Study_main/marketing` |
| Conversions in Ads ≠ Stripe | Normal with Payment Links; compare GA4 `begin_checkout` + Stripe weekly |
| Policy disapproval | Remove dump/guarantee language; link to real product pages |

---

#guide #workflow

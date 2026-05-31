---
type: verification
date: 2026-05-31
site_deploy: becertifiedtoday.com (prod after 94d3e32)
---

# Ad copy vs live site — verification (2026-05-31)

Cross-check of paste-ready exports in `02-campaigns/*/` against production landing pages after guest-page marketing sync.

## Summary

| Campaign | Landing URLs | Pricing | Top funnel | Sample counts | Verdict |
|----------|--------------|---------|------------|---------------|---------|
| **Security+** `secplus_portal` | ✅ Match | ✅ Match | ✅ Lead magnet aligned | ⚠️ Homepage samples = **2 MCQ** (export said 20) | **Ready** after export fix |
| **CCNA** `ccna_portal` | ⚠️ Use `#ccna-lead-capture` | ❌ Sim was **$4.99** in export; site **$9.99** | ❌ Export said no-email 35-min assessment; site is **email 45-min sim** | ⚠️ Homepage samples = **2 MCQ** | **Update export before launch** |
| **ENCOR** `encor_portal` | ⚠️ Add `#encor-lead-capture` | ❌ Sim was **$4.99** in export; site **$9.99** | ⚠️ Export emphasized 12 MCQ samples; site adds **45-min email sim** | ⚠️ Homepage samples = **2 MCQ** | **Update export before launch** |

**Positioning (all three):** ✅ Live pages use exam prep / practice portal language; guest samples link to public homes, not Training Portal URLs.

---

## Security+ — `comptia-sec+-home.html`

### Aligned

| Ad claim | Live site |
|----------|-----------|
| Final URL `#secplus-lead-capture` + `utm_content=lead-free-sim` | ✅ Section exists; lead-first layout when hash or utm matches |
| Free 35-min sim · 20 MCQ + PBQ · email unlock | ✅ `secplus-free-simulation-blueprint.json`: 35 min, 20 MCQ, 1 sim |
| Paid 90-min sim **$9.99** | ✅ `#purchase` |
| 10-day **$9.99** · 30-day **$19.99** | ✅ `#purchase` |
| Exam prep — not a course | ✅ H1, lead, FAQ |
| Federal/DoD copy in meta + FAQ (not `#federal-defense-prep` section) | ✅ Hero + FAQ; ads may use `#secplus-lead-capture` or `#purchase` |
| Sample entry `/secplus-sample?track=questions` | ✅ Works; finishes at `comptia-sec+-home.html` |
| GA4 + `campaign-attribution.js` | ✅ In `<head>` |

### Fix before Ads UI paste

- **Product #5** description: homepage sample track is **2 shuffled MCQ** per run (`homeSampleQuestionCountTotal: 2`), not twenty.

---

## CCNA — `ccna-home.html`

### Aligned

| Ad claim | Live site |
|----------|-----------|
| `#purchase` · 10-day $9.99 · 30-day $19.99 | ✅ |
| 120-min sim · 50 MCQ + 5 D&D + 4 labs | ✅ Purchase copy |
| No GNS3 · browser-only · exam prep | ✅ |
| `#exam-audience` federal block | ✅ Present |
| `/sample?track=ccna-*` | ✅ |
| Do not use Training Portal as final URL | ✅ Guest pages fixed |

### Mismatches — update ads before launch

| Obsidian export (old) | Live site (2026-05-31) |
|-----------------------|-------------------------|
| Top funnel: **35-min free assessment**, no email | **45-min timed simulation**, email unlock at `#ccna-lead-capture` |
| 12 MCQ + 4 D&D + 1 VLAN lab | **20 MCQ + 2 D&D + 1 VLAN lab** (`ccna-free-assessment-blueprint.json` → free-sim pool) |
| Primary URL `hl-free-practice` → assessment hero | Header CTA → `#ccna-lead-capture`; `ccna-home-conversion.js` still references “assessment” (legacy) |
| Timed sim **$4.99** | **$9.99** (`ccna-test-simulation`, purchase card, Stripe value in page) |
| Conversion `ccna_free_assessment_click` | Prefer **`generate_lead`** for lead ad group; assessment click only if linking to runner directly |
| Homepage samples “12 MCQ” in ENCOR-style copy | **2 MCQ** per sample run + optional D&D + lab tracks |

**Recommended lead ad final URL:**

```
https://becertifiedtoday.com/ccna-home.html#ccna-lead-capture?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=lead-free-sim
```

**Note:** `free-assessment.html` still loads the same 45-min blueprint; initial timer display shows `00:35:00` while runtime uses 45 minutes — fix in site backlog, not ad copy.

---

## ENCOR — `ccnp-home.html`

### Aligned

| Ad claim | Live site |
|----------|-----------|
| Final URL `ccnp-home.html` (not secplus-home) | ✅ |
| `#exam-audience` | ✅ |
| 120-min sim · 50 MCQ + 5 D&D + 4 labs | ✅ Purchase copy |
| 10-day $9.99 · 30-day $19.99 | ✅ |
| Exam prep positioning | ✅ |

### Mismatches — update ads before launch

| Obsidian export (old) | Live site (2026-05-31) |
|-----------------------|-------------------------|
| Top funnel: free samples only, **no email**, “12 MCQ” | **Also:** `#encor-lead-capture` — **45-min** email sim (20 MCQ + 2 D&D + ACL/CoPP lab) |
| Timed sim **$4.99** | **$9.99** |
| Product blurb “training portal modes” | Site uses **practice portal modes** |
| Homepage sample questions | **2 MCQ** shuffled per run (`encor-home-sample-blueprint.json`) |

**Recommended lead ad final URL (parallel Security+ / CCNA):**

```
https://becertifiedtoday.com/ccnp-home.html#encor-lead-capture?utm_source=google&utm_medium=cpc&utm_campaign=encor_portal&utm_content=lead-free-sim
```

---

## Shared extensions (all campaigns)

| Extension | Status |
|-----------|--------|
| Sitelink sample URLs (`/sample`, `/secplus-sample`) | ✅ Valid |
| Callouts “Exam Prep — Not a Course”, “No PDFs” | ✅ Match live copy |
| Campaign negatives (course, dump, bootcamp) | ✅ Still appropriate |
| `campaign-attribution.js` on landings + guest samples (via `install-google-tag.js`) | ✅ After guest sync |

---

## Actions taken (2026-05-31)

- [x] This verification note
- [x] Updated paste-ready exports: [[../02-campaigns/security-plus/security-plus-google-ads-export|Security+ export]], [[../02-campaigns/ccna/ccna-portal-google-ads-export|CCNA export]], [[../02-campaigns/encor/ccnp-encor-google-ads-export|ENCOR export]]
- [x] Updated campaign strategy notes: [[../02-campaigns/ccna/ccna-portal-google-ads|CCNA]], [[../02-campaigns/encor/ccnp-encor-google-ads|ENCOR]]
- [ ] Site backlog: align `ccna-home-conversion.js` + CCNA OG meta with 45-min lead sim
- [ ] Site backlog: fix `free-assessment.html` timer display (35:00 vs 45 min runtime)

---

## Launch gate

**Security+:** Safe to paste from export after sample-count fix.

**CCNA / ENCOR:** Use updated export (lead URLs, **$9.99** sim, 45-min / 2-MCQ sample facts). Do **not** paste old `$4.99` or no-email assessment copy.

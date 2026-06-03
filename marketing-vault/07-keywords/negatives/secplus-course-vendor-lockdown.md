---
type: negative-keywords
campaign: SEC+ SY0-701 · Exam prep · becertifiedtoday
scope: course-and-vendor-intent
status: applied
created: 2026-06-03
parent: google-ads-applied-2026-06-03
---

# Security+ — course & vendor click lockdown

Use when **Search terms** show clicks on course shoppers (Udemy-style training, bootcamps, CertMaster/video, Messer, etc.) while your positives are **practice test / mock exam / exam prep** only.

## Why clicks still happen

| You already block | Queries that can still match |
|-------------------|------------------------------|
| `"training course"` | `security+ training`, `comptia security+ online training` |
| `"free course"` | `security+ course`, `sy0-701 certification course` |
| `"professor messer"` | `messer` alone, `messer videos` (if not added) |
| `"udemy"` | `pluralsight`, `linkedin learning`, `comptia certmaster` |

**Fix:** Add **campaign-level Phrase** negatives below (do not duplicate at ad group — see [[google-ads-applied-2026-06-03|applied snapshot]]).

## Paste block — add to existing 32 (Phrase)

**Full campaign paste (Phrase + Exact):** [[google-ads-applied-2026-06-03#Full list — Phrase `"..."` (78) — paste first|google-ads-applied-2026-06-03]].

```
"course"
"training"
"boot camp"
"online course"
"certification course"
"training program"
"classroom training"
"online training"
"virtual training"
"video course"
"instructor"
"linkedin learning"
"pluralsight"
"skillsoft"
"cybrary"
"comptia training"
"comptia learn"
"certmaster learn"
"total seminars"
"mike meyers"
"security+ tutorial"
"learn comptia"
"certification training"
"it training"
"cybersecurity training"
"security training"
"webinar"
"on demand"
"self paced"
"infosec"
```

## After paste (48h)

1. **Google Ads → Campaign → Insights → Search terms** (last 7 days).
2. Any term with **course / training / bootcamp / vendor name** + **≥1 click** and **0** `generate_lead` → add as Phrase negative (same format).
3. Re-import CSV to `07-keywords/search-terms/YYYY-MM-DD-secplus_portal.md` using [[../templates/search-terms-weekly-import|weekly template]].

## Positive keywords — stay narrow

Keep **6–8** prep-only terms in `secplus_lead_free_sim` (no Broad). See [[../../02-campaigns/security-plus/secplus-lead-free-sim-ad-group#Positive keywords — target list (ad group)|target list]].

## Do not negate (keeps exam-prep traffic)

`practice test` · `mock exam` · `practice questions` · `exam prep` · `simulation` · `free` (alone)

## Change log

| Date | Action |
|------|--------|
| 2026-06-03 | Created lockdown block; merged into applied snapshot |

---
type: strategy
parent: "[[Wedge Marketing plan]]"
tags:
  - marketing
  - competitors
---

# Competitor tracking

[[Wedge Marketing plan|← Back to plan]]

Use competitors to find **positioning gaps**, not to copy dumps.

---

## Registry

- Obsidian: [[../Competitors|Competitors]]
- Data: `data/competitor-sites/` (CCNA, SEC+)
- ENCOR: `data/encor-question-sourcing/competitor-sites/`
- Hunt net-new: `Hunt/ccna/2026-06-14/`

---

## Monthly matrix (fill per site)

Copy this table into a new note each month: `Wedge Marketing plan/competitor-matrix-YYYY-MM.md`

| Site | Free sample | Timed sim | Browser labs | No install | Adaptive / weak-area | Sub? | Entry $ | V_2026 / current |
|------|-------------|-----------|--------------|------------|----------------------|------|---------|----------------|
| **Be Certified Today** | ✓ | ✓ 120m | ✓ | ✓ | ✓ review loop | No | $9.99/10d | ✓ V_2025 & V_2026 |
| Mastery Exam Prep | ✓ | ? | CLI in page | ✓ | ? | ? | ? | V_2026 samples |
| HowToNetwork | ✓ | ? | images | ✓ | ? | ? | free | V_2025 |
| OpenExamPrep | ✓ | ? | ? | ✓ | ? | ? | free | V_2025 |
| Boson | demo | ✓ | desktop | ✗ install | ? | ? | $$$ | current |
| INE / CBT | video | ? | PT/GNS3 | ✗ | course path | Yes | $$$ | course |
| ExamTopics | community | ✗ | ✗ | ✓ | ✗ | ? | free | mixed |

**Your row must win on:** browser labs + timed sim + no sub + verified + short sprint pricing.

---

## Automated polls (repo)

```bash
# CCNA competitor question poll
npm run ccna:monthly

# Security+
npm run secplus:monthly

# Weekly GA4
node scripts/marketing-weekly-report.mjs --range 7d
```

Hunt export: `python3 scripts/export_ccna_hunt_obsidian.py --date YYYY-MM-DD`

---

## What to track from Google Ads (most valuable)

Search terms report → columns:

- Search term
- Impressions / clicks / cost
- Conversions (`begin_checkout`)
- Country

**Promote** terms that convert with wedge messaging.  
**Negative** course, dump, job, free-course intent.

---

## Competitor angles for RSA (after search terms validate)

| vs | Angle |
|----|-------|
| Boson / INE | No install · $9.99 entry · browser-only |
| PDF / dumps | Interactive · verified · not static files |
| Packet Tracer / GNS3 | VLAN lab in browser · exam-style UI |
| Course vendors | Exam sprint · not bootcamp · 10 days |

---

## Question sourcing (product moat)

Monthly hunt finds **net-new** items competitors surface:

- V_2026 Mastery samples → `Hunt/ccna/…/V_2026/`
- V_2025 walkthroughs → `Hunt/ccna/…/V_2025/`

Marketing message: *newer questions added continuously* — only if bank actually grows (verify in portal counts).

---

## Review cadence

| When | Action |
|------|--------|
| Weekly | Search terms + GA4 checkout by country |
| Monthly | Competitor matrix + hunt run |
| Quarterly | Reposition wedge keywords from convert data |

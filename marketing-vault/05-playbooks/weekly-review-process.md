---
type: playbook
---

# Weekly marketing review

~30 minutes, once per week. Aligns with *The AI Amplified Marketer*: data first, human decision second.

## 1. Pull data (Cursor / terminal)

From repo root:

```bash
node scripts/marketing-weekly-report.mjs
```

Opens a new note under `03-reports/weekly/`. If GA credentials are missing, the script writes a stub you can fill manually.

## 2. Review in Obsidian

Open the new report. Compare to prior week (Dataview table on [[Home|Home]] or browse `03-reports/weekly/`).

Ask:

- Traffic up or down? Which pages moved?
- Checkout starts vs purchases — where is the funnel leaking?
- Any campaign worth pausing, scaling, or A/B testing?
- **Bidding:** Run [[google-ads-bidding-verification#Part 9 — Weekly bidding verification (10 min)|bidding verification]] (10 min) — strategy, $10 cap, enabled ad groups, search terms.
- **Coupons:** Still on hold? See [[../01-strategy/promotions-and-coupons#When to introduce a promotion|promotions gates]] before launching any code in ads or email.
- **YouTube (if publishing):** Views + GA4 `youtube` traffic — update product [[../09-youtube/secplus/videos/README|video index]]; next upload from [[../09-youtube/secplus/launch-plan|Sec+ plan]].

**Keywords (weekly):** Export Google Ads search terms → import using [[../07-keywords/templates/search-terms-weekly-import|search-terms template]] → tag and update [[../07-keywords/negatives/master-negative-list|negatives]] / landing maps. Full workflow: [[keyword-collection-plan|keyword collection plan]].

## 3. Decide (human section)

In the report note, fill **## Decisions** — concrete actions only (change ad copy, adjust budget, fix landing CTA, new experiment).

## 4. Execute (Cursor)

- Site / tracking: edit `public/` and JS under `public/js/`.
- **Landing page quality:** audit with [[../06-website-optimization/landing-page-audit-checklist|checklist]], log in [[../06-website-optimization/content-change-log|content change log]].
- New campaign note: duplicate [[templates/campaign-brief|campaign brief template]] in `02-campaigns/`.
- Experiments: new note in `04-experiments/` with hypothesis and success metric.

## 5. Close the loop

Next week, reference last week's decisions in the new report's **## Follow-up** section.

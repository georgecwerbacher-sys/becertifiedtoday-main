---
type: moc
tags:
  - marketing
  - analytics
---

# Weekly Reports

Auto-generated GA4 summaries land in `weekly-reports/` (repo path: `data/reports/weekly/`).

## Generate

```bash
node scripts/marketing-weekly-report.mjs
node scripts/marketing-weekly-report.mjs --range 28d
```

Requires `.env.local` with GA4 property + service account (same as `/admin`).

## Reports

Open the `weekly-reports/` folder in the file explorer or link new files here as they appear:

- _(none yet — run the script above to create the first `YYYY-MM-DD.md`)_

## Metrics captured

- Sessions, users, page views
- Top pages and campaign breakdown
- Daily trend table (auto section between `<!-- auto:body -->` markers)

---
type: moc
tags:
  - marketing
  - becertifiedtoday
---

# Marketing Research

**Start here:** [[Site Mission]] — canonical positioning for becertifiedtoday.com

**Live campaign:** [[Sec+ Campaign/README|Sec+ Campaign]] — Security+ Google Search · **$20/day** · 21-day budget test

Hub for the active ad campaign, competitor intel, and weekly analytics.

## Sections

- [[Site Mission]] — why the site exists; reference for all marketing work
- [[Sec+ Campaign/README|Sec+ Campaign]] — Google Ads setup, keywords, RSA, extensions, checklist
- [[Tools/README|Tools]] — Sec+ keyword checklist workflow
- [[Competitors]] — Security+ prep sites
- [[Campaigns]] — live campaign summary + UTM registry
- [[Weekly Reports]] — GA4 summaries (`node scripts/marketing-weekly-report.mjs`)

## Linked folders

| Folder | Source in repo |
|--------|----------------|
| `Sec+ Campaign/` | Google Ads copy, checklist CSV, keywords |
| `competitor-sites/` | `data/competitor-sites/` |
| `weekly-reports/` | `data/reports/weekly/` |

## Quick commands

```bash
# Weekly GA4 report → weekly-reports/YYYY-MM-DD.md
node scripts/marketing-weekly-report.mjs

# Regenerate Sec+ Google Ads checklist after keyword CSV edits
npm run sync:secplus-checklist

# Competitor question polls
npm run secplus:monthly
```

## Admin tracker

[/admin/#section-campaigns](https://becertifiedtoday.com/admin/#section-campaigns) — GA4 paid sessions, landing funnel, `begin_checkout`, 21-day budget projection, Stripe Sec+ purchases.

Registry: `server-lib/campaign-marketing-registry.js` → id **`secplus_portal`**

## Obsidian vault

Vault: **`/Users/werby/Werby Drive/Obsidian`**

1. Obsidian → **Open folder as vault** → choose that path
2. Start from **Home** → **Marketing Research**

The vault links here via symlink (`Marketing Research/`). Edits in Obsidian update the same git-tracked files the site scripts use.

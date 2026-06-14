---
type: moc
tags:
  - marketing
  - becertifiedtoday
---

# Marketing Research

**Start here:** [[Site Mission]] — canonical positioning for becertifiedtoday.com

Hub for competitor intel, ad campaigns, and weekly analytics.

## Sections

- [[Site Mission]] — why the site exists; reference for all marketing work

- [[Competitors]] — SEC+, CCNA, ENCOR prep sites
- [[Campaigns]] — Google Ads setup and UTM registry (**initial 7-day test** through 2026-06-21)
  - [[campaigns/CCNA Campaign|CCNA Campaign]] — checklist: 1 campaign, 2 ad groups (`ccna_portal_10v1` + `ccna_browser_labs`)
  - [[campaigns/ENCOR Campaign|ENCOR Campaign]] — `encor_portal` · 30-day $19.99
- [[Weekly Reports]] — GA4 summaries (`node scripts/marketing-weekly-report.mjs`)

## Linked folders

| Folder | Source in repo |
|--------|----------------|
| `competitor-sites/` | `data/competitor-sites/` |
| `encor-competitors/` | `data/encor-question-sourcing/competitor-sites/` |
| `weekly-reports/` | `data/reports/weekly/` |
| `campaigns/` | symlinks into `scripts/*-google-ads*` |

## Quick commands

```bash
# Weekly GA4 report → weekly-reports/YYYY-MM-DD.md
node scripts/marketing-weekly-report.mjs

# Competitor question polls
npm run secplus:monthly
npm run ccna:monthly
```

## Obsidian vault

Vault: **`/Users/werby/Werby Drive/Obsidian`**

1. Obsidian → **Open folder as vault** → choose that path
2. Start from **Home** → **Marketing Research**

The vault links here via symlink (`Marketing Research/`). Edits in Obsidian update the same git-tracked files the site scripts use.

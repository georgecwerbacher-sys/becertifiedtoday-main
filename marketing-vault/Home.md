# Marketing ops — Be Certified Today

Obsidian vault for data-driven marketing (Cursor + GA4 + Stripe + Google Ads). Open this folder as an Obsidian vault: **File → Open folder as vault** → select `marketing-vault` inside the repo.

## Project goal

**Google Ads** for high-intent exam prep searches, plus **visibility in Google AI search** (AI Mode / AI Overviews). The product is **test preparation** — realistic practice, verified solutions, browser-only — **not** a training course. Primary buyer: someone who wants exam-day confidence, to avoid retakes, and to skip PDFs and third-party apps.

→ [[01-strategy/positioning-and-messaging|Positioning & messaging]] · [[01-strategy/google-ai-search-strategy|Google AI search strategy]]

## Quick links

- [[06-website-optimization/README|Website optimization]] — Quality Score, landing pages, content change log
- [[setup/marketing-stack-setup-checklist|Setup checklist]] — Google, Stripe, GA4, Ads step-by-step
- [[01-strategy/positioning-and-messaging|Positioning & messaging]] ← exam prep, not courses
- [[01-strategy/google-ai-search-strategy|Google AI search strategy]]
- [[01-strategy/ai-amplified-marketer|AI Amplified Marketer — book notes]]
- [[02-campaigns/security-plus-google-ads|Security+ — Google Ads]] ← **active campaign**
- [[02-campaigns/ccnp-encor-google-ads|CCNP ENCOR — Google Ads]] ← **CTA landing: ccnp-home.html**
- [[02-campaigns/ccna-portal-google-ads|CCNA portal — Google Ads]] (planned)
- [[05-playbooks/weekly-review-process|Weekly review process]]
- [[05-playbooks/keyword-collection-plan|Keyword collection plan]]
- [[07-keywords/README|Keyword intelligence (07-keywords/)]]

## Reports

Weekly snapshots live in `03-reports/weekly/`. Generate from the repo root:

```bash
node scripts/marketing-weekly-report.mjs
node scripts/marketing-weekly-report.mjs --range 28d
```

Requires GA4 service account vars in `.env.local` (same as `/admin/analytics.html`).

## Suggested Obsidian plugins

- **Dataview** — query report frontmatter and campaign notes
- **Templater** — apply `templates/weekly-marketing-review.md` after each new report

## Dataview examples

Active campaigns:

```dataview
TABLE channel, status, target_cpa, utm_campaign
FROM "02-campaigns"
WHERE type = "campaign" AND status = "active"
```

Recent weekly reports:

```dataview
TABLE range, sessions, begin_checkout, purchases, revenue_usd
FROM "03-reports/weekly"
WHERE type = "weekly-report"
SORT date DESC
LIMIT 8
```

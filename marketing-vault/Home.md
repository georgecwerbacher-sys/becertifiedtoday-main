# Marketing ops — Be Certified Today

Obsidian vault for data-driven marketing (Cursor + GA4 + Stripe + Google Ads). Open this folder as an Obsidian vault: **File → Open folder as vault** → select `marketing-vault` inside the repo.

## Project goal

**Google Ads** for high-intent exam prep searches, plus **visibility in Google AI search** (AI Mode / AI Overviews). The product is **test preparation** — realistic practice, verified solutions, browser-only — **not** a training course. Primary buyer: someone who wants exam-day confidence, to avoid retakes, and to skip PDFs and third-party apps.

→ [[01-strategy/positioning-and-messaging|Positioning & messaging]] · [[01-strategy/google-ai-search-strategy|Google AI search strategy]] · [[01-strategy/google-ads-bidding-strategy|Bidding strategy (top placement)]]

## Quick links

- [[02-campaigns/README|Google Ads campaigns]] — Security+ · CCNA · ENCOR
- [[06-website-optimization/README|Website optimization]] — Quality Score, landing pages, content change log
- [[setup/marketing-stack-setup-checklist|Setup checklist]] — Google, Stripe, GA4, Ads step-by-step
- [[01-strategy/positioning-and-messaging|Positioning & messaging]] ← exam prep, not courses
- [[01-strategy/promotions-and-coupons|Promotions & coupons]] ← hold coupons at launch; email-first later
- [[09-youtube/README|YouTube — @BeCertifiedToday]] ← [[09-youtube/secplus/videos/README|Sec+ videos]] · [[09-youtube/ccna/videos/README|CCNA videos]] · [[09-youtube/encor/videos/README|ENCOR videos]]
- [[01-strategy/cisco-certifications-exam-prep-foundation|Cisco CCNA & ENCOR foundation]] ← active ads playbook
- [[01-strategy/security-plus-federal-defense-foundation|Security+ federal & defense foundation]]
- [[01-strategy/google-ai-search-strategy|Google AI search strategy]]
- [[01-strategy/ai-amplified-marketer|AI Amplified Marketer — book notes]]
- [[prompts|AI prompts — Google Ads & conversions]] ← Cursor / ChatGPT system + task templates
- [[02-campaigns/security-plus/security-plus-google-ads|Security+ — Google Ads]] ← active
- [[02-campaigns/security-plus/secplus-lead-free-sim-ad-group|secplus_lead_free_sim — live config]] ← budget · CPC · keywords · checklists
- [[02-campaigns/security-plus/security-plus-lead-magnet-ads|Security+ lead magnet ads]] ← free 35-min sim CTA
- [[02-campaigns/ccna/ccna-portal-google-ads|CCNA 200-301 — Google Ads]] ← active
- [[02-campaigns/encor/ccnp-encor-google-ads|CCNP ENCOR — Google Ads]] ← active
- [[05-playbooks/weekly-review-process|Weekly review process]]
- [[05-playbooks/secplus-free-sim-funnel|Security+ free sim funnel]] ← lead ads + GA4 conversions
- [[05-playbooks/google-ads-manual-data-import|Google Ads manual data]]
- [[05-playbooks/google-ads-bidding-verification|Verify bidding in Google Ads]] ← step-by-step
- [[05-playbooks/keyword-collection-plan|Keyword collection plan]]
- [[07-keywords/README|Keyword intelligence (07-keywords/)]]
- [[08-8140-compliance/README|DoD 8140 compliance]] ← source PDFs reviewed; matrix snapshot pending
- [[10-competitors/README|Competitors — PDF dump market]] ← SY0-701 analysis + CSV for Numbers
- [[11-question-sourcing/secplus-sy0-701-web-sources|SY0-701 question sources (web)]] ← verify vs CompTIA; version/date catalog
- [[11-question-sourcing/pbq/README|SY0-701 PBQ sourcing]] ← `npm run secplus:pbq-monthly` · compare vs `SEC+_PBQ/`
- [[11-question-sourcing/pbq/captures/README|SY0-701 PBQ screenshots]] ← PNG research vault · `npm run secplus:pbq-screenshot`

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

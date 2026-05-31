# Website optimization

Track landing page and on-site content changes that improve **Google Ads Quality Score** and **landing page experience** — so ads earn stronger ratings and lower CPC over time.

## Start here

- [[google-ads-quality-score-guide|Google Ads quality & landing page guide]]
- [[landing-page-audit-checklist|Landing page audit checklist]] — run before/after each content change
- [[content-change-log|Site content change log]] — master record of what you changed and why
- [[ad-site-verification-2026-05-31|Ad copy vs live site verification (2026-05-31)]]

## Active landing pages

| Page | Note |
|------|------|
| Security+ primary ad landing | [[pages/comptia-sec-plus-home\|comptia-sec+-home.html]] |
| CCNA primary ad landing | [[pages/ccna-home\|ccna-home.html]] |
| CCNP ENCOR primary ad landing | [[pages/ccnp-home\|ccnp-home.html]] |
| Security+ PBQ / OpenSSL CTA | [[pages/simulation-secure-web-architecture-openssl\|simulation-secure-web-architecture-openssl.html]] |
| Security+ legacy hub (no ads) | [[pages/secplus-home-legacy\|secplus-home.html]] |

Add a note under `pages/` for each URL you send paid traffic to.

## Workflow (with Cursor)

1. **Audit** — score the page with [[landing-page-audit-checklist|checklist]]
2. **Plan** — note gaps in the page’s Obsidian file (message match, CTA, speed, trust)
3. **Implement** — edit `public/` in Cursor (HTML, copy, meta, images)
4. **Log** — append row to [[content-change-log|content change log]]
5. **Guest samples** — after sample or free-assessment edits, run `python3 scripts/sync-guest-page-marketing.py` (aligns with [[../01-strategy/positioning-and-messaging|positioning]])
6. **Measure** — after 7–14 days, check Ads (Quality Score, LP experience) + GA4 bounce/engagement in weekly report
7. **Link campaign** — update [[../02-campaigns/security-plus/security-plus-google-ads|Security+ campaign]] decisions log if ad copy or URL changed

## Templates

- [[../templates/landing-page-optimization-review|Landing page optimization review]] — duplicate for new pages

## Related

- [[../05-playbooks/weekly-review-process|Weekly review process]]
- [[../setup/marketing-stack-setup-checklist|Setup checklist]]

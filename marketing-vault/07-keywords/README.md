# Keyword intelligence

Search terms, negatives, and landing-page keyword maps for Google Ads and organic/AI search.

## Structure

| Path | Purpose |
|------|---------|
| [[../05-playbooks/keyword-collection-plan\|keyword-collection-plan]] | How we collect, review, and promote keywords |
| `search-terms/` | Weekly Google Ads search term exports (by campaign) |
| `negatives/` | Shared and campaign-specific negative lists |
| `landing-maps/` | High-value keywords tied to each CTA / landing URL |
| `templates/search-terms-weekly-import.md` | Paste format for manual imports |

## Active landing maps

- [[landing-maps/security-plus-portal|Security+ primary (`comptia-sec+-home`)]]
- [[landing-maps/ccna-portal|CCNA 200-301 (`ccna-home`)]]
- [[landing-maps/ccnp-encor-portal|CCNP ENCOR (`ccnp-home`)]]
- [[landing-maps/security-plus-openssl-pbq|Security+ OpenSSL PBQ CTA]]

## Workflow (short)

1. Export search terms from Google Ads (weekly).
2. Paste into `search-terms/YYYY-MM-DD-{campaign}.md` using the template.
3. Tag each term: **keep**, **negative**, **new ad group**, **landing copy**.
4. Promote winners into campaign notes (`02-campaigns/`) and page notes (`06-website-optimization/pages/`).

See [[../05-playbooks/keyword-collection-plan|keyword collection plan]] for phases and automation roadmap.

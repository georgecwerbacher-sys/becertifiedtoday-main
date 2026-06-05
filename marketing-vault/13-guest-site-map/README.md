---
type: site-map-hub
status: active
tags:
  - guest-pages
  - sitemap
  - training-portal
---

# Guest site map (Obsidian)

Inventory of **guest-facing** URLs under `public/` (no paid portal session required for first touch), how they relate to **`public/sitemap.xml`**, and the path from **index → exam prep landing → purchase → training portal**.

## Notes

| Note | Purpose |
|------|---------|
| [[guest-access-pages\|Guest access pages]] | Full URL list by tier (indexed landings, free funnel, gated portals) |
| [[sitemap\|Sitemap]] | Human-readable mirror of `public/sitemap.xml` + crawl policy from `robots.txt` |
| [[guest-journey.canvas\|Guest journey canvas]] | Visual flow: index through training portals |

## Source of truth (repo)

| File | Role |
|------|------|
| `public/sitemap.xml` | URLs submitted to search engines |
| `public/robots.txt` | `Disallow` for portals, runners, checkout helpers |
| `public/index.html` | Hub; track cards → product landings only (not Training Portal) |
| `vercel.json` | `/sample` and `/secplus-sample` rewrites |

## Related vault

- [[../06-website-optimization/README|Website optimization]] — landing page audits
- [[../12-Writing/_Writing-Rules|Guest page writing rules]]
- [[../06-website-optimization/ad-site-verification-2026-05-31|Ad vs live site verification]]

## Local preview

From repo root: `npm run serve` → http://localhost:3000/

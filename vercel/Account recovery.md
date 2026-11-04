---
type: note
tags:
  - vercel
  - deploy
created: 2026-11-01
---

# Vercel account recovery

Recovery request **submitted November 1, 2026**. Production deploy is blocked until Vercel restores sign-in. This machine has no Vercel CLI credentials.

## Answers used on the form

| Field | Value |
|---|---|
| Project URL | `ccnp-study.vercel.app` |
| Custom domain | `becertifiedtoday.com` |
| Vercel team | `werby1s-projects` |
| Git provider and username | `GitHub: georgecwerbacher-sys` |
| Repository | `georgecwerbacher-sys/becertifiedtoday-main` |
| GitHub account created | December 7, 2025 |
| Earliest Vercel use in this repo | April 8, 2026 |
| This computer linked to the project | April 29, 2026 |

`ccnp-study.vercel.app` serves the same site as becertifiedtoday.com. The linked local project name is `becertifiedtoday-main`.

## Waiting to publish

GitHub `main` is at `9fe75f29` (November 1, 2026). That includes removing page feedback from the CCNP ENCOR question bank. The live site is still the October 30, 2026 build.

After sign-in works, publish with `vercel --prod` from this repo.

Left uncommitted on purpose: `public/index.html`, `vercel.json`, `vercel.main.json`.

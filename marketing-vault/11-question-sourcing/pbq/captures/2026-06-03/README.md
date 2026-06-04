# Run 2026-06-03 — landing catalog only

**Not PBQ question screenshots.** Playwright hit public **marketing / SKU landing pages** from `pbq_poll` URLs. You see “9 PBQs”, pricing, and MCQ promos — not drag-and-drop UI, log timelines, or sim panes.

| Folder | What it actually is |
|--------|---------------------|
| `landing-catalog/*` | Competitor landing-page captures (research intel) |
| `bct-secplus-pbq-map/` | BCT template QA reference (our own page) |

**Real PBQ screenshots** go in `../YYYY-MM-DD/<source-id>/` with `capture_kind: pbq-preview` — use manual `register` after opening a read-only preview, CertMaster, or VCE player.

See [[../README|captures README]] · `npm run secplus:pbq-screenshot` (preview targets only).

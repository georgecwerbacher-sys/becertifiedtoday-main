# PBQ captures (Obsidian)

**Purpose:** Screenshot reachable Security+ **PBQ, drag-and-drop, and simulation** UI — or save a **reachable link** when automation cannot capture the question screen.

Each run writes `captures/YYYY-MM-DD/INDEX.md` for Obsidian (image embeds + links). Add sites in `config/secplus-pbq-capture-targets.json` and `pbq_poll` on competitor pages as you expand.

---

## Primary command

```bash
npm run serve                    # localhost BCT PBQ pages
npm run secplus:pbq-capture      # all targets → PNG or link + INDEX.md
```

Optional text catalog (no images): `npm run secplus:pbq-monthly`

---

## Capture status

| Status | Meaning | Obsidian |
|--------|---------|----------|
| **captured-pbq** | Actual PBQ / sim UI PNG | `![[source-id/pbq-preview.png]]` |
| **captured-landing** | Site reachable; landing only | Screenshot + **Open** link for manual preview |
| **link-only** | No PNG (Reddit, bot block, login) | **Open** link only |

---

## Manual PBQ screenshot

When a site shows read-only PBQ in the browser but Playwright cannot reach it:

```bash
python3 scripts/secplus_pbq_capture.py register \
  --png ~/Desktop/crucial-control-map.png \
  --source-id crucial-exams-manual \
  --url "https://crucialexams.com/..." \
  --notes "Read-only PBQ preview — paraphrase only"
```

Re-run updates `INDEX.md` for that run date.

---

## Per-source folder

```
captures/2026-06-03/
  INDEX.md              ← open in Obsidian
  bct-pbq-security-control-map/
    pbq-preview.png
    meta.json
  crucialexams-pbq/
    landing.png         ← or link-only meta
    meta.json
  manifest.json
```

**Import CSV:** use `screenshot_path` from `meta.json` only when `capture_status` is `captured-pbq`.

Related: [[../README|PBQ sourcing]] · [[../../05-playbooks/secplus-monthly-pbq-sourcing|monthly playbook]]

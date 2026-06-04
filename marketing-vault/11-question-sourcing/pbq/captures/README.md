# PBQ screenshots

**Two different things — do not mix them up.**

| Kind | What it is | Use in imports? |
|------|------------|-----------------|
| **`pbq-preview`** | Actual drag-and-drop, hot-spot, log reorder, or sim **question UI** | Yes — paraphrase stem + tokens |
| **`landing-catalog`** | Competitor **marketing page** (“9 PBQs”, pricing, MCQ promos) | No — catalog intel only |

The 2026-06-03 automated run was **landing-catalog only** — see [[2026-06-03/README|2026-06-03/README]].

---

## Workflow

1. **Catalog** — `npm run secplus:pbq-monthly` (HTML signals)
2. **PBQ screenshot** — manual preview or configured preview URL
3. **Import** — `../imports/` with `screenshot_path` pointing at **`pbq-preview`** PNG only
4. **Compare / build** — as before

---

## Manual PBQ screenshot (default — most real PBQs)

Paid preview, CertMaster, Crucial read-only PBQ, VCE player, **Cmd+Shift+4**:

```bash
python3 scripts/secplus_pbq_capture.py register \
  --png ~/Desktop/crucial-control-map.png \
  --source-id crucial-exams-manual \
  --kind pbq-preview \
  --label control-map-1 \
  --url "https://crucialexams.com/..." \
  --notes "Read-only PBQ preview — paraphrase only"
```

Files land in `captures/YYYY-MM-DD/<source-id>/pbq-preview.png`.

---

## Automated PBQ preview (Playwright)

Only runs targets in `config/secplus-pbq-capture-targets.json` with **`capture_kind: pbq-preview`** and a working `preview_url` or `preview_selector`. Empty until preview URLs are confirmed.

```bash
npm run secplus:pbq-screenshot-list
npm run secplus:pbq-screenshot
```

---

## Landing catalog (optional competitor intel)

**Not PBQ questions** — optional shots of `pbq_poll` marketing URLs:

```bash
npm run secplus:pbq-screenshot-landing
```

Output: `captures/YYYY-MM-DD/landing-catalog/<source-id>/`

---

## Import CSV

`screenshot_path` must point at a **`pbq-preview`** PNG, e.g.:

`marketing-vault/11-question-sourcing/pbq/captures/2026-06-03/crucial-exams-manual/pbq-preview.png`

Related: [[../README|PBQ sourcing]] · [[../../05-playbooks/secplus-monthly-pbq-sourcing|monthly playbook]]

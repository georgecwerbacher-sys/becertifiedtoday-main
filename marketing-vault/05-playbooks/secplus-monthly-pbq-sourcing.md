---
type: playbook
exam: SY0-701
content_type: pbq
frequency: monthly
status: active
created: 2026-06-03
---

# Monthly SY0-701 PBQ — collect · compare · save

Three steps for **performance-based** items. Parallel to [[secplus-monthly-question-sourcing|MCQ monthly playbook]].

Script: `scripts/secplus_monthly_pbq_hunt.py`

---

## One command (monthly)

```bash
npm run secplus:pbq-monthly
```

With Tier B or Tier C paste file:

```bash
python3 scripts/secplus_monthly_pbq_hunt.py run \
  --import marketing-vault/11-question-sourcing/pbq/imports/YYYY-MM-manual.csv
```

**Outputs** (under `marketing-vault/11-question-sourcing/pbq/runs/`):

| Step | File |
|------|------|
| 1 Collect | `YYYY-MM-DD-discovered.csv` |
| 2 Compare | `YYYY-MM-DD-net-new.csv` + `YYYY-MM-DD-compare.md` |
| 3 Save | `YYYY-MM-DD-net-new.md` (Obsidian note) |

Step 1 does **not** read BCT. Step 2 compares against `SEC+_PBQ/` and `SEC+_Sim_Hot_Spot/`. Step 3 writes **net-new only** as markdown.

---

## Screenshot vault (Obsidian)

Primary run — every `pbq_poll` site + config targets → **PBQ PNG**, **landing PNG**, or **reachable link**:

```bash
npm run serve                 # BCT localhost pages
npm run secplus:pbq-capture   # writes captures/YYYY-MM-DD/INDEX.md
```

**Manual** when a site shows read-only PBQ in the browser (Crucial preview, CertMaster, VCE):

```bash
python3 scripts/secplus_pbq_capture.py register \
  --png ~/Desktop/pbq-control-map.png \
  --source-id crucial-exams-manual \
  --url "https://crucialexams.com/..." \
  --notes "Paraphrase only — verify on Tier A"
```

Add `preview_url` / `preview_selector` in `config/secplus-pbq-capture-targets.json` when automation can reach real PBQ UI.

See [[../11-question-sourcing/pbq/captures/README|captures/README]] · latest [[../11-question-sourcing/pbq/captures/2026-06-03/INDEX|INDEX]].

---

## Three steps (manual)

### 1 — Collect (no BCT)

```bash
npm run secplus:pbq-collect
```

- **Tier A:** catalog notes in `pbq/config/secplus-pbq-sources.json` (no auto-fetch)
- **Tier B/C:** every `10-competitors/sites/*.md` with **`pbq_poll.enabled: true`**
- Optional manual rows: `--import path/to/manual.csv` (use [[../11-question-sourcing/pbq/templates/discovered-pbq-import|PBQ import template]])

List enabled PBQ poll targets:

```bash
npm run secplus:pbq-poll-sources
```

### 2 — Compare (reads BCT PBQ bank)

```bash
npm run secplus:pbq-compare
```

Default match threshold **0.68** (PBQ stems are shorter than MCQ). Override: `--threshold 0.72`.

### 3 — Save (Obsidian .md)

```bash
npm run secplus:pbq-save
```

Opens under `marketing-vault/11-question-sourcing/pbq/runs/`.

---

## After the net-new note

For each PBQ row you accept:

1. Verify interaction and answer on **CompTIA Tier A / objectives v5.0**.
2. Build an **original** page in `public/COMP_TIA_SEC+/SEC+_PBQ/` — copy **`TEMPLATE-dragdrop.html`** or a reference neighbor (`security-control-map.html`, `log-timeline-forensics.html`). Styles: `secplus-pbq-page.css` only.
3. Log in [[../11-question-sourcing/pbq/secplus-pbq-not-in-bct|PBQ net-new log]].

Do **not** copy verbatim from external sources or dumps.

---

## Add a PBQ poll source

In `marketing-vault/10-competitors/sites/your-site.md`:

```yaml
pbq_poll:
  enabled: true
  tier: b
  id: example-pbq-sy0-701
  sample_url: https://example.com/sy0-701/pbq-samples/
  parser: generic_pbq
  version_note: SY0-701
  topic_notes: Tier B PBQ — verify on CompTIA Tier A
```

Parsers: `generic_pbq` (default) · reuse MCQ parsers only when the page is static HTML with extractable text.

See [[../10-competitors/sites/README|competitor poll registry]] for MCQ vs PBQ keys.

---

## MCQ pipeline (unchanged)

Regular multiple-choice sourcing stays in [[secplus-monthly-question-sourcing|secplus-monthly-question-sourcing]] → `npm run secplus:monthly`.

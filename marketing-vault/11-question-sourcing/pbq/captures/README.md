# PBQ screenshots

For drag-and-drop PBQs, hot spots, and sims, **a screenshot is enough** for research. Save a PNG, paraphrase what you see, verify on CompTIA Tier A, then build an original BCT page.

HTML monthly collect only finds catalog copy (“9 PBQs”, “drag-and-drop engine”). The **screenshot** holds the tokens, drop zones, diagram, or log lines you need to draft from.

## Why HTML poll is not enough

| Interaction | What fetch sees | What a screenshot gets |
|-------------|-----------------|-------------------------|
| Drag-and-drop map | Marketing copy | Tokens + drop zones |
| Log timeline reorder | Nothing | Ordered slots + log snippets |
| Hot spot diagram | Nothing | Click regions + prompt |
| VCE / ETE / CertMaster | Download CTA | Player UI (often manual) |

**Policy:** Screenshots are **research only** — paraphrase; do not copy verbatim into BCT.

---

## Workflow

1. **Catalog** — `npm run secplus:pbq-monthly`
2. **Screenshot** — drop PNG here (manual or Playwright)
3. **Import** — paraphrase into `../imports/` with `screenshot_path` column
4. **Compare** — `npm run secplus:pbq-collect -- --import …`
5. **Build** — original HTML in `SEC+_PBQ/` or `SEC+_Sim_Hot_Spot/`

---

## Manual screenshot (most PBQs)

Works for paid previews, CertMaster, VCE player, macOS **Cmd+Shift+4**, etc.

1. Take the screenshot
2. Register it in the vault:

```bash
python3 scripts/secplus_pbq_capture.py register \
  --png ~/Desktop/crucial-pbq-1.png \
  --source-id crucial-exams-manual \
  --url "https://crucialexams.com/..." \
  --notes "Read-only PBQ preview — control map"
```

3. Add a row to `../imports/` — set `screenshot_path` to the PNG path under this folder

Or copy PNGs directly into `captures/YYYY-MM-DD/<source-id>/` and add the sidecar by hand.

---

## Automated screenshot (Playwright)

Optional when the PBQ is visible without login:

```bash
pip install playwright && playwright install chromium
npm run secplus:pbq-screenshot-list
npm run secplus:pbq-screenshot
npm run secplus:pbq-screenshot -- --source-id crucialexams-pbq
```

Output:

```
captures/YYYY-MM-DD/<source-id>/
  landing.png
  landing.meta.json      ← screenshot_path inside
  viewport.png
  viewport.meta.json
manifest.json
```

---

## Import CSV

`screenshot_path` — repo-relative path to the PNG, e.g.:

`marketing-vault/11-question-sourcing/pbq/captures/2026-06-03/crucialexams-pbq/viewport.png`

Legacy column `capture_path` still accepted on import.

Related: [[../README|PBQ sourcing]] · [[../../05-playbooks/secplus-monthly-pbq-sourcing|monthly playbook]]

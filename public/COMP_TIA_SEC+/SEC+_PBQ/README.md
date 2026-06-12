# Security+ PBQ

**SY0-701 performance-based practice** pages ship as `*.html` in this directory (published, indexable when ready).

Build new scenarios in **`../SEC+_Sim_Hot_Spot/PBQ_Production/`** — see [PBQ_Production/README.md](../SEC+_Sim_Hot_Spot/PBQ_Production/README.md). Legacy reference bank: [pending/README.md](../SEC+_Sim_Hot_Spot/pending/README.md).

Shared styles: `../js/secplus-pbq-page.css` plus `/css/bcc-question-link-nav.css` and `/COMP_TIA_SEC+/SEC+_Samples/secplus-sample-touch.css`.

## New page checklist

1. Build in `../SEC+_Sim_Hot_Spot/PBQ_Production/` first (copy `TEMPLATE-dragdrop.html` or a neighbor in `pending/`).
2. When ready, move `{slug}.html` here (kebab-case) and update URLs to `/SEC+_PBQ/`.
3. Set `data-value` / `data-target` on drag-and-drop pages; wire Back / Home / Next under `/COMP_TIA_SEC+/SEC+_PBQ/`.
4. Run `python3 scripts/lint-practice-question-urls.py` on the new file.
5. Log in `data/secplus-pbq-sourcing/secplus-pbq-not-in-bct.md` when accepted.

## Preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_PBQ/{slug}.html
```

## Sourcing

`npm run secplus:pbq-monthly` — outputs under `data/secplus-pbq-sourcing/runs/`.

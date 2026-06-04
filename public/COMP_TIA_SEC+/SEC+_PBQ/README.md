# Security+ PBQ — drag-and-drop pages

Official **SY0-701 PBQ / drag-and-drop template** for standalone practice items.

## Reference pages

| File | Layout |
|------|--------|
| `security-control-map.html` | Token bank → purple layer blocks + blue drop slots |
| `log-timeline-forensics.html` | Token bank → numbered timeline slots |
| `TEMPLATE-dragdrop.html` | Copy skeleton (not linked in nav) |

## Shared CSS

`../js/secplus-pbq-page.css` — all PBQ styling. Do **not** re-add purple sim chrome or inline button colors.

Also load:

- `/css/bcc-question-link-nav.css`
- `/COMP_TIA_SEC+/SEC+_Samples/secplus-sample-touch.css`

## New page checklist

1. Copy `TEMPLATE-dragdrop.html` or the closest reference page.
2. Save as `{slug}.html` (kebab-case).
3. Set `data-value` on tokens and matching `data-target` on drop slots.
4. Wire Back / Home / Next; update previous page Next link.
5. Implement Check / Show / Reset in page script (copy from neighbor).
6. Run `python3 scripts/lint-practice-question-urls.py` on the new file.
7. Log in `marketing-vault/11-question-sourcing/pbq/secplus-pbq-not-in-bct.md` when accepted from sourcing.

## Sourcing

`npm run secplus:pbq-monthly` — see `marketing-vault/11-question-sourcing/pbq/README.md`.

## Preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_PBQ/{slug}.html
```

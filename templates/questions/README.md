# Question link nav template

Shared **Back / Home / Next** link boxes for practice question pages.

## Files

| File | Purpose |
|------|---------|
| `public/css/bcc-question-link-nav.css` | Styles for `.question-nav` and `.answer-actions .nav-check` |
| `templates/questions/question-link-nav.html` | HTML snippet with `REPLACE_*` placeholders |
| `templates/questions/question-mc-baseline.html` | Full single-answer MCQ page using the shared nav |

## Usage

1. Link the stylesheet in `<head>` (before page-specific CSS):

```html
<link rel="stylesheet" href="/css/bcc-question-link-nav.css" />
```

2. Paste the nav block from `question-link-nav.html` as the **first child** of `<main class="card">`.

3. Wire navigation (optional but recommended for CCNA):

```html
<script src="/CCNA-Study/js/ccna-practice-100-nav.js" defer></script>
```

4. Set hrefs:
   - **Back** — previous slug, or `<span class="nav-link nav-prev nav-link--disabled">` on the first item
   - **Home** — `/ccna-home.html` (guest sample), portal URL (paid), or `/index.html`
   - **Next** — next slug, or disabled span on the last item

## Reference implementation

`public/CCNA-Study/CCNA_Samples/sample-question-1.html` — choose-two sample with top link nav; bottom Home/Next bar appears automatically when `?sample=1` (via `ccna-practice-100-nav.js`).

## Generator

`scripts/gen_ccna_chain_pages.py` includes the shared stylesheet on regenerate. Nav HTML is built by `build_question_nav()`.

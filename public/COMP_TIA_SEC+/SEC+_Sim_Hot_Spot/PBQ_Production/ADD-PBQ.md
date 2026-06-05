# Add a new PBQ to production

Checklist for shipping scenario **#8+** into `PBQ_Production/`. Cursor rule: `.cursor/rules/secplus-pbq-dragdrop-pages.mdc`.

**Current tail of chain:** `governance` (`next: None` in `scripts/build-pbq-production-suite.py`).

---

## Phase 0 — Concept (before HTML)

- [ ] Run monthly PBQ sourcing if needed: `npm run secplus:pbq-monthly`
- [ ] Verify interaction and answer keys on **CompTIA SY0-701 objectives v5.0** and primary refs (NIST, RFC, OWASP, vendor-neutral hardening docs). **Do not use exam dumps.**
- [ ] Log accepted concept in `marketing-vault/11-question-sourcing/pbq/secplus-pbq-not-in-bct.md`
- [ ] Playbook reference: `marketing-vault/05-playbooks/secplus-monthly-pbq-sourcing.md`

---

## Phase 1 — Author sections

### 1. Create folder structure

```text
PBQ_Production/{scenario-slug}/
  README.md
  sections/
    {section-id}.html
    …
```

Pick `{scenario-slug}` in kebab-case (e.g. `malware-ioc-analysis`).

### 2. Write section fragments

Each file: `sections/{section-id}.html`

```html
<article class="pbq-section-fragment" data-id="{section-id}">
  <h1>Section title</h1>
  <p class="pbq-sub">…</p>
  <!-- sim-frame, bank, drop slots, MCQs, exhibits, etc. -->
  <script>
  (function () {
    /* Check / Show / Reset + answer key — scope DOM with getElementById on prefixed IDs */
  })();
  </script>
</article>
```

**Rules enforced by the build script:**

| Rule | Detail |
|------|--------|
| Source of truth | Edit `sections/*.html` only — **do not hand-edit** `{slug}/{slug}.html` |
| Article wrapper | Inner content must be inside `<article>…</article>`; inline `<script>` blocks are extracted to the built page |
| First section | Keeps `<h1>`, `.pbq-sub`, `.pbq-instructions` |
| Later sections | Duplicate `<h1>`, `.pbq-sub`, `.pbq-instructions` are stripped on build |
| ID prefixing | Element IDs in a section get prefixed `{section-id}-` at build time (avoids collisions across sections on one page) |
| Scripts | Use `getElementById` / `querySelector` — the build rewrites ID references in inline scripts |

### 3. Layout patterns

Copy interaction patterns from:

| Pattern | Reference |
|---------|-----------|
| Layer / category map | `../pending/TEMPLATE-dragdrop.html` (skeleton) · `security-control-placement/sections/` |
| Ordered timeline | `log-timeline-forensics/sections/` |
| Exhibit + MCQ | `vulnerability-management/sections/` |
| Fill-in drag-and-drop | `phishing-email-analysis/sections/` · `incident-response/sections/` |
| Skeleton | `TEMPLATE-dragdrop.html` |
| Multi-section suite (current standard) | Any neighbor in this folder, e.g. `firewall-acl-secops/sections/` |

### 4. Shared assets (do not duplicate inline styles)

- `/css/bcc-question-link-nav.css`
- `/COMP_TIA_SEC+/SEC+_Samples/secplus-sample-touch.css`
- `/COMP_TIA_SEC+/js/secplus-sim-page.css` — white page chrome (shared with `simulation-*.html`)
- `/COMP_TIA_SEC+/js/secplus-pbq-page.css` — PBQ interactions + **`.pbq-bct-sim`** BCT pattern overrides
- `/COMP_TIA_SEC+/js/pbq-folder-suite.js` (included by build — folder sidebar)

### 4b. BCT simulation pattern (visual consistency)

Production pages match published sims under **`PBQ_Production/dark-web-account-protection/`** (and the other three published folders):

| Element | Pattern |
|---------|---------|
| Body classes | `secplus-sim-page secplus-pbq-ui pbq-bct-sim pbq-folder-suite` |
| Title | `Simulation: {scenario title}` + eyebrow `SY0-701 PBQ · BeCertifiedToday` |
| Lead / instructions | `.lead` + `.instructions` card (bordered white panel) |
| Exhibits | Blue artifact tiles (`#005ecb`) via `.pbq-exhibit-launchers` or `.btn` in `.sim-frame` |
| Work area | `.sim-frame` and `.panel` = bordered white cards with light shadow |
| Actions | Check / Show / Reset = BCT blue buttons (not CCNP `#254b8a`) |
| Nav | Back / Home / Next use same BCT blue as simulation pages |

Reference neighbor: `dark-web-account-protection/dark-web-account-protection.html`. CSS block: `secplus-pbq-page.css` → **BCT simulation pattern**.

### 4c. Deep dive walkthrough

- Source: `marketing-vault/SEC+/PBQ/{slug}/deep-dive-solution.md`
- Build: `npm run build:pbq-suite` also writes `public/COMP_TIA_SEC+/js/secplus-pbq-deep-dive-data.js`
- UI: **Deep dive explanation** button at the bottom of each scenario page → modal (`secplus-pbq-deep-dive.js` + `secplus-sim-deep-dive.css`)
- Regenerate data only: `npm run build:pbq-deep-dive`

### 5. Drag-and-drop pages

- `#bank` + tokens: `draggable="true"` and `data-value="token-id"`
- Drop slots: `.drop-slot` with `data-target="token-id"` matching the token
- Shuffle bank on load and reset
- Body class on built page: include `dragdrop-exercise` in `body_class` when needed

### 6. Scenario README

Create `{scenario-slug}/README.md` with:

- Parts / section table
- Full answer key
- SY0-701 theme mapping (brief)
- Preview URL
- Chain position (previous / next slug)

---

## Phase 2 — Register and build

### 7. Add to `SCENARIOS` in `scripts/build-pbq-production-suite.py`

```python
{
    "slug": "your-new-slug",
    "title": "Display title",
    "body_class": "pbq-your-hook dragdrop-exercise",  # optional CSS hooks
    "description": "One-line meta description (page meta tag)",
    "prev": "governance",  # current tail when appending
    "next": None,
    "sections": [
        {
            "id": "section-id",
            "label": "Sidebar label",
            "path": "your-new-slug/sections/section-id.html",
        },
    ],
},
```

**Chain wiring when appending:**

1. Set **current tail** (`governance`) `"next"` → `"your-new-slug"`
2. Set new entry `"prev"` → `"governance"`, `"next"` → `None`

### 8. Rebuild

```bash
npm run build:pbq-suite
```

**Generated automatically:**

- `{slug}/{slug}.html` — one page, folder sidebar, Back / Home / Next
- Nav links from `prev` / `next` in `SCENARIOS`

**Legacy `*-partN.html` redirects:** only if you add entries to `LEGACY_REDIRECTS` in the same script (optional; first three scenarios use this).

### 9. Update manual docs

- [ ] `PBQ_Production/README.md` — add row to scenario chain + scenarios table
- [ ] `PBQ_Production/VERIFICATION.md` — new section with answer audit + primary sources
- [ ] `marketing-vault/SEC+/PBQ/README.md` — scenario table row
- [ ] `SEC+_Training_Portal.html` — link when the lab is ready to publish
- [ ] `marketing-vault/SEC+/PBQ/{slug}/notes.md` (+ `recommendations.md`, `deep-dive-solution.md` when ready)

---

## Phase 3 — Verify

```bash
python3 scripts/lint-practice-question-urls.py
npm run serve
```

Preview:

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/{slug}/{slug}.html
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/{slug}/{slug}.html#{section-id}
```

- [ ] Every section opens from folder sidebar
- [ ] Deep links (`#section-id`) work
- [ ] Check / Show / Reset grade correctly
- [ ] Back / Next chain matches `SCENARIOS`
- [ ] No third-party dump URLs in HTML

`PBQ_Production/` skips the paid portal gate on localhost.

---

## Phase 4 — Publish to public bank (later)

When ready to index under `SEC+_PBQ/`:

1. Copy or move built page to `public/COMP_TIA_SEC+/SEC+_PBQ/`
2. Replace `/PBQ_Production/` with `/SEC+_PBQ/` in canonical and nav
3. Remove `noindex` from `<meta name="robots">` if SEO is intended
4. `npm run sync:sitemap`

Today all live PBQs remain in `PBQ_Production/` only; `SEC+_PBQ/` is the future published bank.

---

## Quick command summary

```bash
mkdir -p public/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/{slug}/sections
# edit sections/*.html + register in build-pbq-production-suite.py
npm run build:pbq-suite
python3 scripts/lint-practice-question-urls.py
npm run serve
```

---

## Related files

| File | Purpose |
|------|---------|
| `scripts/build-pbq-production-suite.py` | `SCENARIOS` registry, page assembly, chain nav |
| `VERIFICATION.md` | Answer audit log |
| `../pending/README.md` | Legacy layout references (do not add new work there) |
| `../../SEC+_PBQ/README.md` | Future publish checklist |
| `.cursor/rules/secplus-pbq-dragdrop-pages.mdc` | Cursor agent rules for PBQ edits |

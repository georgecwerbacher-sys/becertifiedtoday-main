---
type: production-guide
tags:
  - videos
  - brand
  - overlays
  - premiere
  - photoshop
---

# Visual overlay kit — consistent look

Reusable on-screen elements for every video — same language as the **welcome intro** (icon + label, optional **NO** stamp). Source files live on the [[Local Asset Library|TOSHIBA drive]]; masters go in `Templates/`.

**Reference:** [[website/welcome-video|Welcome video]] — dump / desktop sim / $300 course montage uses this pattern.

---

## Reference overlay — **No PDF To Download** (canonical)

**Shipped example** — Flat icon + document mock + PDF tag + red slash + footer label. Use as the template for all **not a dump** cards.

| Field | Value |
|-------|-------|
| **File** | `Templates/overlays/no-pdf-to-download.png` (also `Website/overlays/`) |
| **Size** | 512×512 PNG · transparent outside artboard |
| **Montage slot** | Welcome + PBQ problem beat #1 — *static dump* |

**Layers (recreate in `BCT_Overlay_Master.psd`):**

| Layer | Content |
|-------|---------|
| Footer label | `No PDF To Download` — red `#ef4444` · Inter/similar bold |
| NO slash | Red circle + diagonal · over PDF tag · subtle drop shadow OK |
| PDF tag | Flat salmon/red pill · text **PDF** |
| Doc mock | Light gray page · folded corner · optional decoy line: `Real Test` / strikethrough pricing (policy-safe: generic dump vibe, not real exam claim) |
| Base | Flat document icon from **Download Flat Icon** pack |

**Premiere:** Import PNG → **V3** · scale ~40–55% frame width on `#0d1528` full-screen card · **3 s** hold · match welcome montage timing.

**Variants to build next (same layout):**

- `no-desktop-sim-install.png` — monitor icon + NO + `No install required`
- `no-video-course.png` — play/course flat icon + NO + `Not a course`
- `yes-free-samples.png` — download icon · **no** slash · `Free samples in browser`

---

## Icon style — Flat (channel default)

**Use:** `Download Icons Main File/Download Flat Icon/` for every video — montage cards, CTAs, thumbnails.

| Why Flat | |
|----------|--|
| Matches welcome-video look | Simple shapes read at small size |
| Easy in Photoshop | Recolor, resize, add **NO** badge on separate layers |
| One style only | Do not mix Outline / Solid / Filled in the same video |

**Photoshop workflow:** Open SVG/PNG from Flat folder → duplicate to `Templates/BCT_Overlay_Master.psd` as smart object → **Color Overlay** or hue shift to `#2f66bf` / `#e6edf3` → add **NO** stamp layer on top when needed → export PNG for Premiere V3.

Copy working set → `Templates/icons/download-flat/` on the drive.

### Other packs (archive only)

| Folder | Use |
|--------|-----|
| Download Outline Icon | Backup if Flat too heavy on a light bg |
| Download Solid Icon | Unused — too bold |
| Download Filled Color Icon | Unused — pre-baked colors fight brand |

---

## Core overlay types

Build each as a **Photoshop smart object** or **Premiere mogrt**, then reuse.

| Overlay | Base icon | Text / stamp | When to use |
|---------|-----------|--------------|-------------|
| **Not a dump** | Download / PDF / Document | Red **NO** badge or slash | Problem section — vs PDF dumps |
| **Not a course** | Play / video-style icon (from Envato if needed) | **NO** | Who this is *not* for |
| **Not desktop sim** | Monitor + install | **NO** | Browser vs GNS3 / Packet Tracer |
| **Browser practice** | Cloud / browser / mobile download | — (positive) | Solution frame · portal in browser |
| **Free samples** | Click to download / mobile download | `Free samples` label | Mid CTA lower third |
| **Step label** | — | `Step 1 — Read all parts` | PBQ / technique sections |

**NO stamp spec:** Circle or rounded rect · `#dc2626` fill · white **NO** · 80–90% opacity optional · place **upper-right** on icon · hold 2–3 s on montage cuts.

---

## Welcome-video pattern (copy for every montage)

Problem montage (~0:20–0:50) — **3 cuts × 3 s each**:

```
[No PDF To Download.png]     →  static dump (reference overlay)
[Icon: Desktop/app]   + NO     →  label: "Desktop sim install"
[Icon: Play/course]   + NO     →  label: "$300 course"
```

Then cut to **positive** browser/cloud icon (no NO) → portal screen record.

Same structure works in Sec+ PBQ videos: *dump / bootcamp / wrong prep* → *practice this PBQ in browser*.

---

## Photoshop master (`Templates/BCT_Overlay_Master.psd`)

Suggested layers (top → bottom):

| Layer | Content |
|-------|---------|
| `label` | Text — Inter Bold 48 px · `#e6edf3` or `#2f66bf` |
| `no-badge` | Optional · group with icon |
| `icon` | Smart object from drive icon pack · tint `#2f66bf` |
| `bg-pill` | Optional dark pill `#121a2b` @ 85% behind icon+label |

**Export:** PNG sequence or single PNG → import Premiere **V3**. Save variants:

- `no-pdf-to-download.png` ← **reference example** (see [[Visual Overlay Kit#Reference overlay — No PDF To Download (canonical)|canonical spec]])
- `overlay-not-course.png`
- `overlay-free-samples.png`
- `overlay-step-01.png` …

---

## Premiere stack (match welcome video)

| Track | Content |
|-------|---------|
| **V3** | Icon overlays · step labels · NO badges · lower thirds |
| **V2** | A-roll / talking head |
| **V1** | B-roll · screen · montage icons on solid `#0d1528` |
| **A1** | Voice |
| **A2** | Music bed −20 dB |

**Montage timing:** 2–3 s per icon card · match voice beat · whoosh SFX optional (subtle).

**Essential Graphics:** Save repeating lower third as `BCT_LowerThird_Samples` with download icon + `Try free samples →`.

---

## Color on icons

| Element | Value |
|---------|-------|
| Icon (positive) | `#2f66bf` or `#4f84d8` |
| Icon (on dark bg) | `#e6edf3` outline style |
| NO badge | `#dc2626` · white text |
| Label text | `#e6edf3` on dark · `#121a2b` on light |
| Montage background | `#0d1528` (match site hero) |

In Photoshop: icon layer → **Color Overlay** or SVG recolor. In Premiere: **Tint** effect on PNG.

---

## Per-video checklist

- [ ] **Flat icons** from `Download Flat Icon/` — edit in Photoshop as needed ([[Visual Overlay Kit#Icon style — Flat (channel default)|Flat default]])
- [ ] NO overlays only for **problem / not-for** beats — not on CTAs
- [ ] Positive download icon only with **free samples** / browser messaging
- [ ] Labels ≤ 4 words (`Static dump`, not `Don't download a PDF dump`)
- [ ] Copy PNGs to `Videos/Assets/[slug]/overlays/` for project archive
- [ ] Note overlays used in brief **Envato / asset** column

---

## Thumbnails

Reuse icon + 3-word hook — e.g. download icon (small) + **PBQ Prep** + scenario name. Same outline style as video montage.

---

## Related

[[Local Asset Library]] · [[Production Template]] · [[website/welcome-video|Welcome video]] · [[Envato Asset Guide]]

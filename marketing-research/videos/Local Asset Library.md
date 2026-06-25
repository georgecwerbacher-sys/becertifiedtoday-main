---
type: production-guide
tags:
  - videos
  - assets
  - local
---

# Local asset library (TOSHIBA drive)

Review and staging folder for video graphics — **not in git**. Mount drive before editing.

**Root:** `/Volumes/TOSHIBA EXT/BeCertifiedToday/Images`

---

## Folder map

| Folder | Use | Obsidian briefs |
|--------|-----|-----------------|
| **Website/** | Site-wide — logos, welcome/end cards, lower thirds | [[website/README\|website]] |
| **Website/Logo/** | Logo v2 white + transparent exports for Premiere/Photoshop | [[../Website_Main/Brand Assets\|Brand Assets]] |
| **Sec+/** | PBQ thumbnails, icons, Sec+ video B-roll stills | [[sec+/PBQ Video Strategy\|PBQ strategy]] |
| **CCNA/** | Lab demo stills, topology crops, CCNA thumbnails | [[ccna/README\|ccna]] |
| **ENCOR/** | ENCOR lab / thumbnail assets | [[encor/README\|encor]] |
| **Templates/** | Reusable Premiere/Photoshop masters (`.psd`, `.prproj`, `.mogrt`) | [[Production Template]] |
| **Download Icons Main File/Download Flat Icon/** | **Channel default** — montage, NO badges, CTAs · edit in Photoshop | [[Visual Overlay Kit\|Visual Overlay Kit]] |

---

## Workflow

1. **Download** from [Envato Elements](https://elements.envato.com/) or export from site (portal screenshots → `Sec+/`, `CCNA/`, etc.).
2. **Drop** into the matching track folder on the drive for review.
3. **Rename** clearly: `[track]-[slug]-[use].png` (e.g. `secplus-dark-web-ir-thumbnail.psd`).
4. **License PDF** — keep Envato certificates in `Templates/licenses/` or next to the asset batch.
5. **When locked for a video** — copy into Premiere project `Videos/Assets/[slug]/` (local Mac) or into repo only if needed on site (`public/images/…`).
6. **Note in brief** — [[_video-template#Minute-by-minute run of show|Envato / asset column]] in the video markdown file.

**Do not** commit the whole TOSHIBA folder — drive is source library; repo gets only shipped web assets (logos, `public/videos/*.mp4`).

---

## Premiere project paths (local Mac)

Suggested mirror on your editing machine (optional):

```
~/Videos/BeCertifiedToday/
  Assets/          ← copies from drive when editing
  Exports/
  _Template_BCT.prproj
```

Link drive folder in Premiere **Project panel → Link media** if files stay on TOSHIBA.

---

## Envato inventory CSV

**File:** [[envato-assets.csv]] — one row per Elements download (path, use, assigned brief, license flag).

After a new download: add row → extract zip to **Local path** on this drive → save license PDF under `Templates/licenses/`.

**Pending extract (2026-06-25):** `clean-photo-display-logo-reveal-2026-02-06-04-03-41-utc.zip` → `Templates/quick-photo-ident-2/` (see [[envato-assets.csv|envato-assets.csv]] row `quick-photo-ident-2`).

```bash
mkdir -p "/Volumes/TOSHIBA EXT/BeCertifiedToday/Images/Templates/quick-photo-ident-2"
unzip -o ~/Downloads/clean-photo-display-logo-reveal-2026-02-06-04-03-41-utc.zip \
  -d "/Volumes/TOSHIBA EXT/BeCertifiedToday/Images/Templates/quick-photo-ident-2"
```

---

## Current contents (2026-06-25)

| Path | Notes |
|------|-------|
| `Website/Logo/becertifiedtoday_logo_v2_white.png` | White lockup |
| `Website/Logo/becertifiedtoday_logo_v2.png` | Transparent lockup |
| `Templates/overlays/no-pdf-to-download.png` | **Reference overlay** — No PDF To Download (512×512) |
| `Website/overlays/no-pdf-to-download.png` | Copy of reference |
| `Download Icons Main File/Download Flat Icon/` | **Default set** — modify in Photoshop · overlay kit |
| `Templates/quick-photo-ident-2/` | **Envato** — Quick Photo Ident 2 · logo sting · [[envato-assets.csv\|CSV row]] · extract pending |
| `Sec+/` · `CCNA/` · `ENCOR/` | Empty — fill as you download per [[sec+/PBQ Video Strategy#Ship order (backlog)|PBQ ship order]] |

Refresh this table when you add batches.

---

## Consistent on-screen look

Use the **Download Icons** packs for montage cards (icon + optional **NO** stamp + short label) — same pattern as the welcome video. Full spec: [[Visual Overlay Kit]].

Save reusable composites in **`Templates/BCT_Overlay_Master.psd`** on this drive.

---

## Related

[[README|Videos hub]] · [[Envato Asset Guide]] · [[Production Template]] · [[../Website_Main/Brand Assets|Brand Assets]]

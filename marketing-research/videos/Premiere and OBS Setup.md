---
type: production-guide
tags:
  - videos
  - premiere
  - obs
---

# Premiere Pro 2026 + OBS setup

Quick reference for [[Production Template|Production Template]]. Tune once · reuse every shoot.

---

## OBS (record)

### Settings → Video

| Setting | Value |
|---------|-------|
| Base canvas | 1920 × 1080 |
| Output scaled | 1920 × 1080 |
| FPS | **24** (match Premiere) or 30 if entire pipeline is 30 |

### Settings → Output (record)

| Setting | Value |
|---------|-------|
| Recording format | **MKV** (recoverable if crash) |
| Encoder | Apple VT H264 (Mac) or x264 |
| Rate control | CQP/CRF **18–20** |
| Audio | AAC 192 kbps · **48 kHz** |

### Settings → Audio

| Setting | Value |
|---------|-------|
| Sample rate | 48 kHz |
| Channels | Stereo |
| Mic filter chain | Noise suppression **Off** or light · Gain before OBS peaks −12 dB |

**Better:** Noise reduction in Premiere **Essential Sound → Dialogue** — not heavy OBS filters.

### Scenes (duplicate each session)

1. **A-roll** — Video Capture Device + Audio Input Capture (mic)
2. **Screen** — Window Capture (Chrome) or Display Capture · separate **Desktop Audio Off**
3. **Screen + PiP** — Screen full + cam 480×270 bottom-right · 8 px border `#2f66bf`

### Before Record

- [ ] Do Not Disturb · hide bookmarks · close unrelated tabs
- [ ] Portal URL is **sample** page only
- [ ] Test clip 10 s — check lip sync and levels
- [ ] Slate: say **“Take [section] — hook”** for editor
- [ ] Record **room tone** 10 s

### File naming

`YYYY-MM-DD_[slug]_A-roll_take01.mkv`  
`YYYY-MM-DD_[slug]_screen_demo01.mkv`

---

## Premiere Pro 2026 (edit)

### New project from template

1. Duplicate `_Template_BCT.prproj` → `[slug].prproj`
2. Import OBS files to `Assets/[slug]/`
3. Sequence **1080p 24 fps** — drag A-roll to V2, screen to V1

### Sync

- **Clap sync:** align spike on A1 (mic) with visual clap
- Or **Merge clips** if recorded on same timeline (PiP scene)

### Essential Sound (dialogue)

1. Select all voice clips → **Dialogue**
2. **Loudness** → Auto match to **−14 LUFS**
3. **Repair** → Reduce noise lightly · DeEsser if sibilance

### Music (Envato)

- Place on A2 · **−20 dB** under voice · duck −6 dB more when speaking (Essential Sound → Music → Duck against Speech)

### Graphics

- Import `.mogrt` from Envato or use saved **BCT_LowerThird**
- **CTA outro:** 5 s minimum on end card · safe zone avoid YouTube progress bar (bottom 80 px)

### Captions

1. **Window → Text → Captions**
2. **Create transcription** (Premiere 2026) from sequence · English
3. Edit to [[Production Template#Subtitle spec (SRT)|42 char lines]]
4. **Export → Subrip (.srt)**

### Export

| Deliverable | Setting |
|-------------|---------|
| YouTube main | H.264 1080p · YouTube preset · max render quality |
| Short | 1080×1920 sequence · crop center · same audio |
| Site embed | Same as main · keep under 3 min for welcome |

### Archive

Move exports to `Exports/[slug]_1080p.mp4` + `[slug].srt` · note path in video brief.

---

## Photoshop (thumbnail + end card)

| Asset | Size | Notes |
|-------|------|-------|
| Thumbnail | 1280 × 720 | [[Production Template#Thumbnail spec]] |
| End card | 1920 × 1080 | Logo center · URL bottom third · dark `#121a2b` |
| Lower third PNG | 1920 × 200 transparent | Import to Premiere V3 |

Export PNG end card → Premiere still at CTA marker.

---

## Mic checklist (any shoot)

- [ ] Cardioid pattern · gain staged before interface clipping
- [ ] Mouth 15–20 cm from mic · consistent distance per session
- [ ] No keyboard/mouse loud during A-roll — edit voiceover for screen sections if needed
- [ ] Same mic position for reshoots (mark floor tape)

---

## Related

[[Production Template]] · [[Envato Asset Guide]] · [[_video-template]]

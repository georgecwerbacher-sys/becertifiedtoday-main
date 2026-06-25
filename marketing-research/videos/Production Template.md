---
type: production-guide
tags:
  - videos
  - premiere
  - obs
  - templates
---

# Production template — Be Certified Today

Master spec for every video. Duplicate [[_video-template|_video-template]] per project; fill **minute-by-minute** table + script + SRT.

**Stack:** Premiere Pro 2026 · OBS · Photoshop · professional mic · [Envato Elements](https://elements.envato.com/) (log in via your account — do not paste auth tokens into git)

**North star:** [[../YouTube Channels#What every video is (and is not)|Prep and technique, not courses]]

---

## Brand (on-screen)

| Element | Spec |
|---------|------|
| **Primary blue** | `#2f66bf` · hover `#3a74d4` |
| **Dark surface** | `#121a2b` · text `#e6edf3` |
| **Muted** | `#9fb0cc` |
| **Font** | Inter (match site) — or Arial/Helvetica in Premiere if Inter unavailable |
| **Logo** | `/images/logo/becertifiedtoday_logo_trans.png` |
| **Tagline** | Practice Like Test Day. Walk In Ready. |

Save reusable **Essential Graphics** templates in Premiere: `BCT_LowerThird`, `BCT_StepLabel`, `BCT_EndCard`.

**Montage / problem overlays:** icon + optional **NO** badge — see [[Visual Overlay Kit]] · drive icons in [[Local Asset Library]].

---

## Video formats

| Format | Length | Sequence | Use |
|--------|--------|----------|-----|
| **Standard** | 2–8 min | 1920×1080 · 24 fps | YouTube main + site embed |
| **Short** | 30–90 s | 1080×1920 · 24 fps | YouTube Shorts · cut from main or standalone |
| **Welcome / mission** | 2–3 min | 1080p | Channel trailer · `index.html` |

**Audio target:** −14 LUFS integrated (YouTube loudness). Peaks −1 dBTP.

---

## Section structure (every video)

Use these **named sections** in Premiere markers and in each brief’s run-of-show table.

| # | Section | Typical time | Purpose | Filming |
|---|---------|--------------|---------|---------|
| 1 | **Cold open** | 0:00–0:05 | Pattern interrupt or direct address | Tight crop talking head · no logo sting yet |
| 2 | **Hook** | 0:05–0:20 | Who this is for + prep promise | Eye line to lens · “You’ve already studied…” |
| 3 | **Problem / frame** | 0:20–0:45 | Why this prep matters · not a course | A-roll + B-roll every 3–5 s |
| 4 | **Technique / demo** | 0:45–70% | How to practice · portal or method | Screen record primary · voiceover or PiP |
| 5 | **Proof / recap** | 70–85% | One takeaway · scorecard or mistake | Screen or lower-third bullet |
| 6 | **CTA outro** | Last 15–25 s | Sample link · tagline · subscribe | End card · verbal + on-screen URL |

**CTA rules**

- **Verbal:** One mid CTA (“try the free sample”) + one outro CTA — never three hard sells.
- **On-screen:** Lower third at mid + **end card** last 5 s minimum.
- **YouTube:** End screen last 20 s — Subscribe + **one** link (sample or playlist).
- **Policy-safe:** No *guaranteed pass*, *real exam questions*, *walk in ready* in on-screen text if mirroring Google Ads caution; tagline OK on YouTube organic.

---

## Prep filter (before publish)

Answer **yes** to all:

1. Helps someone **after** a course/book, before test day?
2. Shows **practice** (portal, sim, lab UI) or **technique**, not a chapter lecture?
3. CTA points to **free samples** or honest unlock — not “buy my course”?
4. B-roll uses **samples only** — no full paid bank, no checkout PII?

---

## Thumbnail spec (Photoshop)

| Setting | Value |
|---------|-------|
| Canvas | 1280 × 720 px · RGB · 72 dpi |
| Safe text | Keep copy inside **1120 × 630** center |
| Text | 1 short hook · **80–120 pt** bold · high contrast |
| Face | Optional left 40% · slight exaggeration OK |
| Background | Dark `#0b1020` or blurred portal screenshot |
| Export | JPG quality 10–12 · &lt; 2 MB |

**PSD layers to save:** `Thumb_Template.psd` — `BG` · `Screenshot` · `Face` · `Text1` · `Text2` · `Logo`

---

## Subtitle spec (SRT)

| Rule | Value |
|------|-------|
| Max chars per line | **42** |
| Max lines on screen | **2** |
| Min duration | 1.0 s |
| Max duration | 6.0 s |
| Reading speed | ~140 wpm — split long sentences |

**Workflow:** Script in brief → Premiere **Text → Captions → Create from transcript** → edit → Export Subrip → YouTube upload.

**Burn-in (optional):** White text · black 60% bar · Inter 48 px · bottom safe margin 80 px.

---

## Filming techniques

### Talking head (A-roll)

- Camera at eye level · headroom minimal · look **at lens**, not monitor.
- Mic 15–20 cm (6–8 in) below mouth · pop filter · record **−12 to −6 dB** peaks.
- Key light 45° · fill opposite · kill backlight spill on glasses.
- Record **room tone** 10 s for noise print.
- **Multiple takes per section** — edit on breath gaps, not mid-sentence.

### Screen (B-roll)

- OBS **1920×1080** · browser zoom **125%** · dark mode portal if readable.
- **Mouse highlight** (yellow circle) in OBS or post in Premiere.
- Hide OS notifications · incognito if extensions clutter.
- **Separate audio** if doing voiceover in Premiere over screen (cleaner than live narration).

### Pacing

- Change visual every **3–5 seconds** in montage sections.
- Jump cut on filler words (“um”, “so”) — keeps prep content tight.
- First **5 seconds** must state audience + promise (retention).

---

## Premiere Pro 2026 — project template

Create once · **File → Save As Template** or duplicate folder:

```
Videos/
  _Template_BCT.prproj
  Assets/
    Logo/
    LowerThirds/
    EndCards/
    Music/          ← Envato license PDF saved here
  Exports/
    [slug]_1080p.mp4
    [slug]_vertical.mp4
    [slug].srt
```

**Sequence settings**

- Editing: 1920×1080, 24 fps (Timebase 24.00)
- Working color space: Rec. 709
- Audio: 48 kHz stereo

**Track layout**

| Track | Content |
|-------|---------|
| V1 | B-roll / screen |
| V2 | A-roll |
| V3 | Graphics / lower thirds |
| A1 | Dialogue |
| A2 | Music (−18 to −22 dB under voice) |
| A3 | SFX (optional) |

**Markers:** `HOOK` · `PROBLEM` · `DEMO` · `RECAP` · `CTA` · color green on CTA

**Export:** Preset **YouTube 1080p Full HD** · VBR 2 pass · target 12–16 Mbps

---

## OBS — scene template

| Scene | Sources |
|-------|---------|
| **A-roll** | Camera · mic · optional subtle logo lower corner |
| **Screen — portal** | Display capture or Window (Chrome) · 1080p canvas |
| **Screen — talking PiP** | Screen + cam 25% bottom-right rounded |
| **BRB / slate** | Static “Be Certified Today — recording” |

**Output:** MKV while recording → remux to MP4 if needed · **same fps as Premiere sequence**

---

## Envato Elements

See [[Envato Asset Guide]] for search terms and license folder. Use Elements for:

- Intro/outro **stings** (keep under 3 s — do not feel like a course channel)
- **Lower third** motion templates (recolor to `#2f66bf`)
- Subtle **tech background** loops for A-roll
- **Whoosh** transitions · keyboard SFX for screen demos
- Stock **office / laptop** B-roll when not showing portal

Save **license PDF** per asset in `Assets/Music/` or project notes.

---

## Related

[[README|Videos hub]] · [[_video-template]] · [[Premiere and OBS Setup]] · [[Envato Asset Guide]] · [[website/welcome-video|Welcome video (filled example)]]

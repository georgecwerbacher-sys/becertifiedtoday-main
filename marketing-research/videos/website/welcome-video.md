---
type: video-brief
track: website
status: published-site
target_length: ~2:30
platforms:
  - youtube
  - index.html
source_file: public/videos/bct-intro.mp4
tags:
  - videos
  - welcome
  - website
---

# Welcome to Be Certified Today

**Status:** `published` on site · **YouTube:** upload pending  
**Source:** `Desktop/BCT_Intro.mp4` → `public/videos/bct-intro.mp4` (~16 MB)  
**Logo end card:** v2 lockup — *Practice Like Test Day. Walk In Ready.* (`becertifiedtoday_logo_v2_trans.png` on dark · `_white.png` on light)  
**Embed:** `public/js/site-welcome-video.js` · `#welcome-video` on [index.html](https://becertifiedtoday.com/)

**Use:** YouTube channel welcome / trailer · main landing embed  
**Voice:** [[../../Site Mission|Site Mission]] — prep and readiness, not a course  
**Production:** [[../Production Template|Production Template]]

| Field | Value |
|-------|-------|
| **YouTube title** | `Welcome to Be Certified Today — Exam Prep in Your Browser` |
| **Thumbnail line 1** | `Practice Like Test Day` |
| **Thumbnail line 2** | `CCNA · ENCOR · Security+` |
| **Playlist** | Website |
| **utm_content** | `welcome-video` |
| **Sample URL** | `https://becertifiedtoday.com/?utm_source=youtube&utm_medium=organic&utm_campaign=youtube_welcome&utm_content=welcome-video` |
| **Site file** | `/videos/bct-intro.mp4` |
| **YouTube URL** | *(after upload — set `youtubeId` in `site-welcome-video.js` if you want YouTube embed instead of local MP4)* |

---

## CTA map

| When | Verbal | On-screen | YouTube |
|------|--------|-----------|---------|
| **Hook** | — | — | — |
| **Mid** (~1:15) | “Try the free samples on your exam page first.” | Lower third: `Free samples — no account` | — |
| **Outro** (2:05–2:30) | “Link below — pick your track. Practice Like Test Day. Walk In Ready.” | End card: logo + `becertifiedtoday.com` | End screen: Subscribe + homepage link |
| **Post** | — | — | Description + pinned comment |

---

## Minute-by-minute run of show

| Time     | Sec | Section                   | Shot / technique                  | A-roll (script)                                                                                                                                                                                                                                  | On-screen text                                  | B-roll / graphics                                              | Envato / asset                                |
| -------- | --- | ------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------- | -------------------------------------------------------------- | --------------------------------------------- |
| **0:00** | 5   | Cold open                 | Tight talking head · no music yet | *(look at lens — beat)*                                                                                                                                                                                                                          | —                                               | —                                                              | —                                             |
| **0:05** | 15  | **Hook**                  | A-roll · direct address           | Hi — I built **Be Certified Today** because exam day is hard enough without wondering if your prep is out of date or stuck in a PDF from last year. This is **practice and readiness** — not a replacement for your course or book.              | —                                               | —                                                              | —                                             |
| **0:20** | 30  | **Problem**               | A-roll · cut to B-roll every 5 s  | Most prep still pushes the wrong choices: a **static dump**, a **desktop sim you install**, or a **$300 course** when you already know the material and just need to know — **am I ready?**                                                      | `Dump · Desktop sim · $300 course`              | Montage: **`no-pdf-to-download.png`** + desktop **+ NO** · course **+ NO** ([[../Visual Overlay Kit#Reference overlay — No PDF To Download (canonical)\|overlay kit]]) | Drive: `Templates/overlays/` · **Flat** icons for variants |
| **0:50** | 25  | **Solution frame**        | A-roll + portal tease             | I wanted one place to practice **the way you are tested** — timed runs, drag-and-drop, CLI labs, Security+ PBQs — **in your browser**, phone or laptop, without GNS3 or Packet Tracer.                                                           | `Browser · Timed · Labs · PBQs`                 | Homepage scroll · track cards                                  | Screen OBS 125% zoom                          |
| **1:15** | 30  | **What you get**          | Screen primary · VO or PiP        | **CCNA 200-301** — labs, drag-and-drop, timed sim. **ENCOR 350-401** — browser CLI labs. **Security+ SY0-701** — PBQ scenarios, 90-minute timed exam, scorecard. Answers verified against **official sources** — not forum votes or dumps.       | Track labels on each cut                        | 3× 3 s cuts: CCNA sample · ENCOR lab · Sec+ PBQ                | Portal samples only                           |
| **1:45** | 20  | **Offer + mid CTA**       | A-roll                            | **Try free samples first** — no account. Unlock full access for a **set period, one payment**. No membership. **No ads inside the portal** while you study.                                                                                      | `Free samples · One payment · No ads in portal` | Sample → scroll (no checkout)                                  | Lower third mogrt                             |
| **2:05** | 25  | **Who / not + outro CTA** | A-roll → end card                 | For you if you are **weeks from test day** or your job **requires the cert**. **Not** a course — learn the material first, then **practice here**. Link below — pick your track. **Practice Like Test Day. Walk In Ready.** Thanks for watching. | End card URL                                    | Logo end card 5 s                                              | [[../envato-assets.csv\|Quick Photo Ident 2]] · v2 trans logo · `#2f66bf` |
| **2:30** | —   | *(end)*                   | YouTube end screen zone           | —                                                                                                                                                                                                                                                | Subscribe · link                                | —                                                              | —                                             |

**Optional Short (0:60):** Hook (0:05–0:20) + Solution one line + three track flashes + outro CTA only.

---

## Full script (read-through / teleprompter)

```
Hi — I built Be Certified Today because exam day is hard enough without wondering 
if your prep is out of date or stuck in a PDF from last year. This is practice and 
readiness — not a replacement for your course or book.

Most prep still pushes the wrong choices: a static dump, a desktop sim you install, 
or a three-hundred-dollar course when you already know the material and just need 
to know — am I ready?

I wanted one place to practice the way you are tested — timed runs, drag-and-drop, 
CLI labs, Security+ PBQs — in your browser, on your phone or laptop, without GNS3 
or Packet Tracer.

CCNA two-hundred-three-oh-one — labs, drag-and-drop, timed simulation.
ENCOR three-fifty-four-oh-one — browser CLI labs.
Security+ SY0-701 — PBQ scenarios, ninety-minute timed exam, scorecard.

Answers are verified against official Cisco and CompTIA sources — not forum votes 
or braindump sites.

Try free samples first — no account required. When you are ready, unlock full access 
for a set period, one payment — no membership. Inside the portal, no third-party ads 
while you study.

This is for you if you are weeks from test day, your job or contract requires the 
cert, or you want interactive timed practice instead of a dump.

It is not an instructor-led course. If you are starting from zero, use your book or 
video course first — then come here to practice for real.

Link in the description — pick your track. Practice Like Test Day. Walk In Ready. 
Thanks for watching.
```

---

## Subtitles (SRT draft)

Import to Premiere · edit timing after picture lock · export final `.srt`.

```
1
00:00:05,000 --> 00:00:09,000
I built Be Certified Today because exam day
is hard enough without outdated prep.

2
00:00:09,000 --> 00:00:13,000
This is practice and readiness —
not a replacement for your course.

3
00:00:20,000 --> 00:00:24,000
Most prep pushes the wrong choices:
dumps, desktop sims, or another course

4
00:00:24,000 --> 00:00:28,000
when you just need to know: am I ready?

5
00:00:50,000 --> 00:00:54,000
Practice the way you are tested —
timed runs, labs, PBQs — in your browser.

6
00:01:15,000 --> 00:01:19,000
CCNA, ENCOR, and Security+ —
samples and timed sims on each track.

7
00:01:45,000 --> 00:01:49,000
Try free samples first. One payment
for a set period — no membership.

8
00:02:05,000 --> 00:02:09,000
Not a course — practice here after
you have studied the material.

9
00:02:20,000 --> 00:02:25,000
Practice Like Test Day. Walk In Ready.
Link below — pick your track.
```

---

## OBS — record checklist

- [ ] Montage overlays from [[../Visual Overlay Kit|Visual Overlay Kit]] (icon + NO on problem beats)
- [ ] **A-roll** scene · mic peaks −12 to −6 dB · record sections: Hook, Problem, Offer, Outro
- [ ] **Screen** scene · `index.html` + three sample URLs · 125% zoom
- [ ] No paid bank · no Stripe · no admin
- [ ] Files: `YYYY-MM-DD_welcome_A-roll.mkv` · `_screen.mkv`
- [ ] Room tone 10 s

---

## Premiere — edit checklist

- [ ] `_Template_BCT.prproj` → `welcome-bct.prproj` · markers through table above
- [ ] Music bed −20 dB · Envato minimal tech ambient
- [ ] Lower third at **1:45** · end card **2:05–2:30**
- [ ] Captions from transcript → export `welcome.srt`
- [ ] Export 1080p + optional 1080×1920 Short
- [ ] Set `youtubeId` in `public/js/site-welcome-video.js`

---

## Photoshop — thumbnail

- [ ] `Thumb_Welcome.psd` from template · face or logo left
- [ ] Text: **Practice Like Test Day** / **CCNA · ENCOR · Security+**
- [ ] Export `welcome-thumb.jpg` 1280×720

---

## YouTube metadata

**Description:**

```
Be Certified Today — browser-based exam prep for CCNA, CCNP ENCOR, and CompTIA Security+.

Practice timed simulations, drag-and-drop, CLI labs, and Security+ PBQs in your browser. Free samples, no account required. One-time access when you unlock — not a subscription.

Try free samples: https://becertifiedtoday.com/?utm_source=youtube&utm_medium=organic&utm_campaign=youtube_welcome&utm_content=welcome-video

CCNA: https://becertifiedtoday.com/ccna-home.html
ENCOR: https://becertifiedtoday.com/ccnp-home.html
Security+: https://becertifiedtoday.com/comptia-sec+-home.html

Independent exam prep — not affiliated with Cisco or CompTIA.
```

**Pinned comment:** Main sample URL + “Pick your exam track and try the free samples first.”

**Channel:** Set as **channel trailer** after upload (optional).

---

## Publish checklist

- [x] Export `BCT_Intro.mp4` · copy to `public/videos/bct-intro.mp4`
- [x] Site embed live via `site-welcome-video.js` (`localSrc`)
- [ ] Upload same file to YouTube · thumbnail · description
- [ ] Set as channel trailer (optional)
- [ ] Pin comment with UTM
- [ ] Set `youtubeId` only if you want YouTube embed on site instead of MP4

---

## Site embed

**Hero banner:** `index.html` → `#hero-banner` — intro plays **once** (autoplay, muted), then `index-header-programmers.png`. Skips replay in the same browser session (`sessionStorage` key `bct_index_intro_seen`).

**Config:** `public/js/site-welcome-video.js` · `public/js/index-hero-intro.js`

---

## Related

[[../README|Videos hub]] · [[../_video-template|Blank template]] · [[../../YouTube Channels|YouTube Channels]] · [[../../Site Mission|Site Mission]]

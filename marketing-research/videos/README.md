---
type: moc
tags:
  - marketing
  - youtube
  - videos
---

# Videos

Production notes for YouTube and site embeds. Every video supports **test prep and technique** — not courses. See [[../YouTube Channels|YouTube Channels]].

## Primary focus (2026)

**Security+ PBQ prep** — [[sec+/PBQ Video Strategy|PBQ Video Strategy]] · [[sec+/PBQ Video Format|PBQ Video Format]]. Ship welcome first, then free-sample PBQs (dark web IR, WLAN, firewall ACL), then the 34-scenario backlog. CCNA/ENCOR folders stay for later.

## Production system

| Doc | Purpose |
|-----|---------|
| [[Production Template\|Production Template]] | Brand, sections, CTA rules, thumbnail + SRT spec |
| [[_video-template\|_video-template]] | **Duplicate per video** — minute table, script, subtitles |
| [[Premiere and OBS Setup\|Premiere & OBS Setup]] | Record + edit settings (2026) |
| [[Envato Asset Guide\|Envato Asset Guide]] | Elements searches, license folder, what to avoid |
| [[Local Asset Library\|Local Asset Library]] | **TOSHIBA drive** — review folder by track |
| [[Visual Overlay Kit\|Visual Overlay Kit]] | Icon + **NO** overlays · montage cards · lower thirds (welcome-video look) |
| [[envato-assets.csv\|envato-assets.csv]] | **Inventory** — one row per Elements download |

**Stack:** Premiere Pro 2026 · OBS · Photoshop · pro mic · [Envato Elements](https://elements.envato.com/) · local drive asset library

## Folders

| Folder | Use |
|--------|-----|
| [[website/README\|website]] | Site-wide — welcome, mission, how the portal works |
| [[ccna/README\|ccna]] | CCNA exam practice labs and prep technique |
| [[sec+/README\|sec+]] | **Primary** — Security+ PBQ prep ([[sec+/PBQ Video Strategy\|strategy]]) |
| [[encor/README\|encor]] | CCNP ENCOR exam practice labs and prep technique |

## Workflow

1. Review or download assets → [[Local Asset Library|TOSHIBA drive]] (`…/Images/[track]/`)
2. Duplicate [[_video-template]] → `[track]/[slug].md`
2. Fill **minute-by-minute** table + script + SRT draft
3. Pull approved assets from drive → Premiere `Videos/Assets/[slug]/`
4. Record in OBS per [[Premiere and OBS Setup]]
5. Edit in Premiere · export MP4 + SRT
6. Thumbnail in Photoshop · assets from drive or [[Envato Asset Guide]]
7. Publish · update brief status + site embed if applicable

## Status key

`idea` → `script` → `record` → `edit` → `published`

## After publish

1. Set YouTube ID in `public/js/site-welcome-video.js` (website welcome) or note ID in the video brief.
2. Update `published` date and URL in the note.
3. Pin comment with free sample link + UTM (`utm_source=youtube&utm_medium=organic`).

## First videos

1. **[[website/welcome-video\|Welcome video]]** — **live** on [index.html](https://becertifiedtoday.com/) (`/videos/bct-intro.mp4`) · YouTube upload pending
2. **[[sec+/PBQ Video Strategy\|Sec+ PBQ pipeline]]** — Tier 1 sample PBQs, then [[sec+/zero-trust-zta-migration-pbq-prep\|Zero Trust]] and chain backlog

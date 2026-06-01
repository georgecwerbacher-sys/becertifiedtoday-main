---
type: youtube-ops
status: active
youtube_handle_url: https://www.youtube.com/@BeCertifiedToday
youtube_channel_id_url: https://www.youtube.com/channel/UCOD6uQlfTMgmLWbVgItqYQg
created: 2026-06-01
---

# YouTube → site integration & UTM

**Channel:** [@BeCertifiedToday](https://www.youtube.com/@BeCertifiedToday) · [UCOD6uQlfTMgmLWbVgItqYQg](https://www.youtube.com/channel/UCOD6uQlfTMgmLWbVgItqYQg)

Hub: [[README|09-youtube]] · Plans: [[secplus/launch-plan|Sec+]] · [[ccna/launch-plan|CCNA]] · [[encor/launch-plan|ENCOR]]

---

## Primary CTAs (Security+)

| Destination | Use when |
|-------------|----------|
| Free 35-min sim | **Default** — most videos |
| `#purchase` | After showing 90-min sim; soft sell |
| OpenSSL PBQ page | PBQ-specific videos only |
| Sample questions `?track=questions` | Short MCQ demos without email |

### URL templates

**Free sim (default):**

```
https://becertifiedtoday.com/comptia-sec+-home.html#secplus-lead-capture?utm_source=youtube&utm_medium=video&utm_campaign=secplus_yt&utm_content=VIDEO_SLUG
```

Replace `VIDEO_SLUG` with short id, e.g. `a1-flagship`, `b1-openssl-pbq`, `short-pdf-vs-sim`.

**90-min sim / purchase block:**

```
https://becertifiedtoday.com/comptia-sec+-home.html#purchase?utm_source=youtube&utm_medium=video&utm_campaign=secplus_yt&utm_content=VIDEO_SLUG
```

**OpenSSL PBQ:**

```
https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/simulation-secure-web-architecture-openssl.html?utm_source=youtube&utm_medium=video&utm_campaign=secplus_yt&utm_content=VIDEO_SLUG
```

---

## Where to place links

| Placement | Rule |
|-----------|------|
| **Description line 1** | Primary CTA URL (free sim) |
| **Description line 2–3** | Secondary (portal/pricing) if relevant |
| **Pinned comment** | Same as line 1 after publish |
| **End screen** | Link element → free sim URL |
| **Cards** | Mid-roll only after value (≥50% watch); max 1 card |
| **Channel About** | `utm_campaign=channel_about` |
| **Channel links** | “Free Security+ practice” → free sim |

---

## GA4 / attribution

Site loads [[../../public/js/campaign-attribution.js|campaign-attribution.js]] on key pages — UTMs should persist through lead and checkout.

**Mark in GA4 as key events (if not already):**

- `generate_lead` (free sim email)
- `begin_checkout`
- Optional: custom `youtube_cta_click` if you add on-site banner later

**Weekly review:** filter GA4 acquisition by `session source = youtube` and `session campaign = secplus_yt`.

---

## YouTube Studio settings per upload

| Field | Guidance |
|-------|----------|
| **Title** | Include `SY0-701` or `Security+` where natural |
| **Description** | Link in first 3 lines; exam prep disclaimer |
| **Tags** | 5–10: sy0-701, security plus practice, comptia security+, practice test, pbq, exam simulation |
| **Category** | Education |
| **Audience** | Not made for kids |
| **Paid promotion** | No unless sponsored |
| **Playlist** | Assign per product [[secplus/launch-plan#Playlists|Sec+]] / [[ccna/launch-plan|CCNA]] / [[encor/launch-plan|ENCOR]] plan |
| **Subtitles** | Upload script for exam terms (CSRF, MDM, etc.) |

---

## Cross-channel consistency

| Channel | Campaign param | Notes |
|---------|----------------|-------|
| Google Ads Search | `secplus_portal` | Do not change |
| YouTube organic | `secplus_yt` | Video traffic only |
| YouTube paid (future) | `secplus_yt_ads` | If you run Video action campaigns |
| Email nurture | `secplus_lead_nurture` | [[../01-strategy/promotions-and-coupons|promotions]] |

Never use `utm_medium=cpc` for organic YouTube links.

---

## CCNA / ENCOR (phase 2+)

Duplicate pattern with:

- `utm_campaign=ccna_yt` → `ccna-home.html#ccna-lead-capture`
- `utm_campaign=encor_yt` → `ccnp-home.html#encor-lead-capture`

Only after Security+ GA4 shows consistent YouTube-assisted leads or checkouts.

---

## Compliance copy (description footer)

Paste under every Security+ video link block:

```
Be Certified Today provides exam preparation practice only. Not affiliated with or endorsed by CompTIA. Verify certification requirements with your employer and CompTIA.
```

Federal-focused videos add: `DoD/contractor requirements vary by role — confirm with your security office.`

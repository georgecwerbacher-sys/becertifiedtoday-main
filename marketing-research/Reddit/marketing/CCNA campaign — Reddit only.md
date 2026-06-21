---
type: reference
product: ccna
tags:
  - marketing
  - reddit
  - ccna
created: 2026-06-19
---

# CCNA campaign — Reddit only

Single-page setup for **ads.reddit.com**. No Google settings here.

[[Ad setup checklist|← Full checklist]] · Copy: [[CCNA ad copy]]

**Account:** u/BeCertifiedToday · **Budget:** $10/day

---

## Campaign

| Setting | Value |
|---------|--------|
| Name | `CCNA_Wedge_Reddit` |
| Objective | **Traffic** |
| Daily budget | **$10.00** |
| Schedule | Continuous |

---

## Ad group — targeting

| Setting | Value |
|---------|--------|
| **Placements** | **Feed ON** · **Conversation ON** |
| | Feed = promoted post in subreddit scroll. Conversation = in comment threads under posts. |
| Communities | `r/CCNA`, `r/Cisco` |
| Locations | US, CA, UK, AU |
| Interests | None |
| Keywords | None |

---

## Ad group — bidding

| Setting | Value |
|---------|--------|
| Automated bidding | **On** |
| Strategy | **Lowest cost** |
| Cost cap | **Off** |

---

## Ad group — tracking

| Setting | Value |
|---------|--------|
| Reddit Pixel | **Skip** (launch) |
| Destination URL | UTMs below |

```
https://becertifiedtoday.com/ccna-home.html?utm_source=reddit&utm_medium=cpc&utm_campaign=ccna_wedge_lab&utm_content=reddit-labs
```

---

## Creative (Image — headline + image only in feed)

Reddit **Image** ads do **not** show a long body in the feed. Pack the offer into **headline**, **image text**, and **landing page**.

| Field | Value |
|-------|--------|
| **Post type** | **Image** |
| Profile | u/BeCertifiedToday |
| CTA | **Learn More** |
| Destination URL | UTMs below |
| Main image | Lab screenshot |
| **Thumbnail** | Same image or 4:3 crop (required for Feed) |

**Headline / quick pitch:** [[Quick pitch]]

```
CCNA soon? $330 exam. Online test prep, not a course. All labs online. Sample lab: drag-and-drop, a few questions. $9.99/10-day Full Access Pass. Just click Learn More.
```

**Long headline (298 chars)** — see [[Elevator pitch]]

**Description** (fill if UI has the field — may not show in all previews)

```
200-301 prep in browser. VLAN lab, drag-and-drop, 120-min sim. No GNS3. Not PDF dumps.
```

**Text on the image itself** (most reliable — add in Canva/Preview before upload)

```
CCNA 200-301
Browser labs · no GNS3
120-min timed sim
$9.99 / 10 days
becertifiedtoday.com
```

After click → **ccna-home.html** has full pricing, samples, and checkout.

---

## After launch

- GA4 → session source **`reddit`**
- Week 1: CTR **> 0.2%** · any **`begin_checkout`** with `utm_content=reddit-labs`

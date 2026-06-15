---
type: campaign-config
product: secplus
campaign: SEC+_Wedge_PBQ
tags:
  - marketing
  - google-ads
  - secplus
---

# Campaign shell — SEC+_Wedge_PBQ

[[README|← Campaign folder]] · Steps: [[01-build-steps]]

---

## Google Ads settings

| Setting | Value |
|---------|--------|
| **Campaign name** | `SEC+_Wedge_PBQ` |
| **Type** | Search only |
| **Search partners** | **Off** until baseline |
| **Display Network** | **Off** |
| **Daily budget** | **$8.00/day** (scale to $12–15 after stable CPA) |
| **Bidding (weeks 1–2)** | Maximize clicks · max CPC **$3.50** |
| **Bidding (after 15–20 checkouts)** | Maximize conversions → `begin_checkout` |
| **Language** | English |
| **AI Max / URL expansion** | **Off** |

---

## Ad group: SEC+_Wedge_PBQ

| Setting | Value |
|---------|--------|
| **Display path** | `Security+` / `PBQ-Practice` |
| **Intent** | SY0-701 browser PBQ — chain labs, hot spots, no download |
| **Match types** | Phrase for discovery; Exact on Planner-verified terms |

### Final URL

```
https://becertifiedtoday.com/secplus/pbq-practice-browser.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=pbq-wedge
```

### Landing message match

- Free dark web IR PBQ sample (same UI as paid)
- 28 PBQ scenarios — chain labs, hot spots, exhibits
- Browser-only — no download
- $9.99 / 10-day · $19.99 / 30-day on page

---

## Conversion

| Event | Items |
|-------|--------|
| Primary | GA4 **`begin_checkout`** |
| Stripe items | `secplus_portal_10d` ($9.99) · `secplus_portal_30d` ($19.99) |

Import as **Primary** conversion in Google Ads before launch.

**Tag policy:** `scripts/marketing-tag-minimal-list.md`

---

## UTM map

| utm_campaign | utm_content | Destination |
|--------------|-------------|-------------|
| `secplus_wedge_pbq` | `pbq-wedge` | `/secplus/pbq-practice-browser.html` |
| `secplus_wedge_pbq` | `portal-10d` | wedge `#purchase` |
| `secplus_wedge_pbq` | `portal-30d` | wedge `#purchase` |
| `secplus_wedge_pbq` | `sitelink-pbq` | `/secplus-sample?track=sim-dark-web` |
| `secplus_wedge_pbq` | `sitelink-sample` | `/secplus-sample?track=questions` |
| `secplus_wedge_pbq` | `sitelink-home` | `/comptia-sec+-home.html` |

Base: `utm_source=google&utm_medium=cpc`

---

## Avoid self-competition

| Asset | Action |
|-------|--------|
| `secplus_pbq_wedge` in combined Security+ campaign | **Pause** when this campaign goes live |
| `secplus_portal_10d` head terms | Separate campaign — low bid or paused |

---

## Registry

`server-lib/campaign-marketing-registry.js` → id `secplus_wedge_pbq`

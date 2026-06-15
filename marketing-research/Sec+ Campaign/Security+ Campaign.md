---
type: campaign
product: secplus
scope: portal
utm_campaign: secplus_portal
status: baseline
tags:
  - marketing
  - google-ads
  - security+
  - secplus
---

# Security+ Campaign (portal)

Head-term **portal baseline** — practice test / question bank. Deprioritize vs wedge; expect high CPC.

**Setup:** [[Sec+ Notes|Sec+ Notes]] · **Keywords:** [[Sec+ Keywords#secplus_portal_10d — ad group]]  
**Wedge campaign (primary):** [[README#Campaign 1 — SEC+_Wedge_PBQ (build this)|SEC+_Wedge_PBQ]]

---

## Campaign shell

| Setting | Value |
|---------|--------|
| Campaign name | `Security+ SY0-701 · Exam prep · becertifiedtoday` |
| Daily budget | **$10.00/day** |
| Bidding | Maximize clicks, max CPC **$2.75** |
| utm_campaign | `secplus_portal` |
| Conversion | GA4 `begin_checkout` |

## Ad group — secplus_portal_10d only

| Setting | Value |
|---------|--------|
| Display path | `Security+` / `10-Day-Access` |
| Pin H1 | `Security+ Practice Test` |
| Pin H2 | `$9.99 for 10-Day Access` |

**Final URL:**

```
https://becertifiedtoday.com/comptia-sec+-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=portal-10d
```

**No wedge ad group here** — PBQ keywords go in **`SEC+_Wedge_PBQ`** ([[Sec+ Keywords#SEC+_Wedge_PBQ — ad group]]).

---

## 7-day portal test

| Day | Action |
|-----|--------|
| 1 | Confirm `secplus_portal_10d` serving · GA4 checkout |
| 3 | Search terms → negatives |
| 7 | If head-term CPA bad → launch [[README#Campaign 1 — SEC+_Wedge_PBQ (build this)\|SEC+_Wedge_PBQ]] instead of scaling portal |

**CSV:** `scripts/secplus-google-ads-campaign-checklist.csv`  
**Extended ref:** `scripts/secplus-portal-10d-google-ads.md`

[[README|← Sec+ Campaign folder]]

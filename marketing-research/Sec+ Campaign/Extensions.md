---
type: extensions
product: secplus
utm_campaign: secplus_portal
tags:
  - marketing
  - google-ads
  - secplus
  - sitelinks
---

# Extensions — sitelinks & geo

**Campaign:** `Security+ SY0-701 · Exam prep · becertifiedtoday` · **utm_campaign:** `secplus_portal`

Paste at **campaign** level. Link text ≤25 chars · each description ≤35 chars.

**Checklist rows:** [[secplus-campaign-checklist.csv]] — filter **Phase** = `Extensions` (6 sitelinks with URLs + description notes).

Base UTM: `utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal`

**Primary landing:** `/comptia-sec+-home.html` — all Google Ads traffic (final URL + sitelinks). `/secplus/pbq-practice-browser.html` is organic/SEO only; paid clicks redirect to home.

---

## Sitelinks (6)

| #   | Link text              | Description 1             | Description 2                | Full URL                                                                                                                                                        |
| --- | ---------------------- | ------------------------- | ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | 10-Day Access · $9.99  | 34 PBQ scenarios included | One payment, no subscription | `https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-10d#purchase` |
| 2   | 34 PBQ Scenarios       | Chain labs & hot spots    | Browser performance prep     | `https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-pbq-list`     |
| 3   | Timed 90-Min Sim       | Mixed MCQ and PBQ run     | Domain scorecard included    | `https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-sim#purchase` |
| 4   | Try PBQ Sample         | Dark web IR scenario      | Browser preview, no download | `https://becertifiedtoday.com/secplus-sample?track=sim-dark-web&utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-pbq`          |
| 5   | 30-Day Access · $19.99 | Best value study window   | Full portal + timed sim      | `https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-30d#purchase` |
| 6   | Scorecard & Review     | Timed sim + weak domains  | Adaptive review modes        | `https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-scorecard`    |

---

## Copy-paste block (Google Ads UI)

```
Sitelink 1
Name: 10-Day Access · $9.99
Description 1: 34 PBQ scenarios included
Description 2: One payment, no subscription
URL: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-10d#purchase

Sitelink 2
Name: 34 PBQ Scenarios
Description 1: Chain labs & hot spots
Description 2: Browser performance prep
URL: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-pbq-list

Sitelink 3
Name: Timed 90-Min Sim
Description 1: Mixed MCQ and PBQ run
Description 2: Domain scorecard included
URL: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-sim#purchase

Sitelink 4
Name: Try PBQ Sample
Description 1: Dark web IR scenario
Description 2: Browser preview, no download
URL: https://becertifiedtoday.com/secplus-sample?track=sim-dark-web&utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-pbq

Sitelink 5
Name: 30-Day Access · $19.99
Description 1: Best value study window
Description 2: Full portal + timed sim
URL: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-30d#purchase

Sitelink 6
Name: Scorecard & Review
Description 1: Timed sim + weak domains
Description 2: Adaptive review modes
URL: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-scorecard
```

---

## Message match

- **Purchase sitelinks** → `#purchase` on PBQ landing (same page as ad final URL)
- **Sample sitelink** → dark web PBQ only (`secplus-sample?track=sim-dark-web`)
- **No policy-risk copy** in sitelink text — avoid *like test day*, *real exam*, *walk in ready*
- **No “Free” in link text** — use *Try PBQ Sample* (sample is free on landing; don’t lead with free in extensions)

---

## Geo

Same Tier A/B country lists as CCNA portal setup (`scripts/ccna-portal-10d-google-ads.md`). Federal/defense US metros are especially relevant for Security+ (DoD 8570/8140). **$20/day** on PBQ wedge keywords.

**Location option:** Presence — people in or regularly in targeted locations.

[[README|← Sec+ Campaign folder]]

---
type: campaign-config
product: secplus
campaign: SEC+_Wedge_PBQ
tags:
  - marketing
  - google-ads
  - secplus
  - extensions
---

# Extensions & locations — SEC+_Wedge_PBQ

[[README|← Campaign folder]] · Shell: [[02-campaign-shell#UTM map]]

---

## Location targeting

### Launch (week 1)

| Setting | Value |
|---------|--------|
| **Option** | Presence: people in or regularly in targeted locations |
| **Countries** | United States · Canada · United Kingdom · Australia |

### Expand later

After US CPA is acceptable — remaining Tier A in `scripts/secplus-portal-10d-google-ads.md`.

**Hold:** India, Philippines, Nigeria (organic / YouTube later).

---

## Sitelinks (campaign level)

Base UTM: `utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq`

| # | Link text | Description 1 | Description 2 | Full URL |
|---|-----------|---------------|---------------|----------|
| 1 | Free Dark Web PBQ | Hands-on IR scenario | No checkout required | `https://becertifiedtoday.com/secplus-sample?track=sim-dark-web&utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=sitelink-pbq` |
| 2 | Free Practice Questions | SY0-701 MCQ preview | Instant feedback, free | `https://becertifiedtoday.com/secplus-sample?track=questions&utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=sitelink-sample` |
| 3 | 28 PBQ Scenarios | Chain labs & hot spots | Browser-only prep | `https://becertifiedtoday.com/secplus/pbq-practice-browser.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=sitelink-pbq-list` |
| 4 | 10-Day Access · $9.99 | 1000+ Qs + PBQ library | One-time no subscription | `https://becertifiedtoday.com/comptia-sec+-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=portal-10d` |
| 5 | 90-Min Timed Exam Sim | MCQ + PBQ mixed run | Adaptive review included | `https://becertifiedtoday.com/comptia-sec+-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=sitelink-sim` |
| 6 | Security+ Exam Prep Home | Full SY0-701 portal | Samples + pricing | `https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=sitelink-home` |

**Google Ads paste format** (name ≤25 · descriptions ≤35):

```
Name: Free Dark Web PBQ
Description 1: Hands-on IR scenario
Description 2: No checkout required
URL: https://becertifiedtoday.com/secplus-sample?track=sim-dark-web&utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=sitelink-pbq

Name: Free Practice Questions
Description 1: SY0-701 MCQ preview
Description 2: Instant feedback, free
URL: https://becertifiedtoday.com/secplus-sample?track=questions&utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=sitelink-sample

Name: 28 PBQ Scenarios
Description 1: Chain labs & hot spots
Description 2: Browser-only prep
URL: https://becertifiedtoday.com/secplus/pbq-practice-browser.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=sitelink-pbq-list

Name: 10-Day Access · $9.99
Description 1: 1000+ Qs + PBQ library
Description 2: One-time no subscription
URL: https://becertifiedtoday.com/comptia-sec+-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=portal-10d

Name: 90-Min Timed Exam Sim
Description 1: MCQ + PBQ mixed run
Description 2: Adaptive review included
URL: https://becertifiedtoday.com/comptia-sec+-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=sitelink-sim

Name: Security+ Exam Prep Home
Description 1: Full SY0-701 portal
Description 2: Samples + pricing
URL: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=sitelink-home
```

---

## Launch verification

- [ ] All 6 sitelinks pasted at campaign level
- [ ] Sitelinks open correctly on mobile
- [ ] Free PBQ sitelink loads sample without checkout

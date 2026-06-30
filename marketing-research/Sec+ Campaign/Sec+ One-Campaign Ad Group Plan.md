---
type: campaign-strategy
product: secplus
phase: 2
tags:
  - marketing
  - google-ads
  - secplus
  - budget
  - schedule
  - us-only
---

# Sec+ One-Campaign Ad Group Plan — $25/day

**Status:** Current build plan · **Use this as the source of truth**

Build **one US-only Search campaign** with **three tightly themed ad groups**. Use a shared **$25/day campaign budget** and let Google allocate spend based on ad group output. This keeps early data concentrated, avoids budget fragmentation, and gives you a cleaner foundation before splitting anything into separate campaigns.

Related: [[Security+ Campaign]] · [[Sec+ Notes]] · [[Sec+ Keywords]] · [[Sec+ RSA Copy]] · [[Extensions]]

---

## Campaign Foundation

| Setting                | Value                                                       |
| ---------------------- | ----------------------------------------------------------- |
| Campaign name          | `Security+ SY0-701 · US Search`                             |
| Campaign type          | Search only                                                 |
| Daily budget           | **$25/day shared**                                          |
| Budget allocation      | Google determines spend split based on ad group output      |
| Bidding                | Maximize clicks · max CPC **$2.75** to start                |
| Location               | **United States only**                                      |
| Location option        | **Presence** — people in or regularly in targeted locations |
| Language               | English                                                     |
| Search partners        | **Off** until data is stable                                |
| Display Network        | **Off**                                                     |
| AI Max / URL expansion | **Off**                                                     |
| Conversion             | GA4 `begin_checkout` imported as Primary                    |
| Campaign UTM           | `utm_campaign=secplus_portal`                               |

**Hold rule:** Do not change budget, max CPC, campaign structure, or RSA pins for the first **7 days** unless traffic is clearly irrelevant or checkout tracking is broken.

---

## Ad Group Structure

| Ad group            | Intent                                                                 | `utm_content`       | Display path                | RSA copy |
| ------------------- | ---------------------------------------------------------------------- | ------------------- | --------------------------- | -------- |
| `Core Exam Prep`    | Timed sim, readiness, adaptive review, no-PDF/browser prep             | `core-exam-prep`    | `Security+` / `Exam-Prep`   | [[Sec+ RSA Copy#Phase 2 — exam prep lead (paste when ready)]] |
| `Military Gov 8140` | DoD 8140, federal, contractor, military, public-sector job requirement | `mil-gov-8140`      | `Security+` / `DoD-8140`    | [[Sec+ RSA Copy - Military Gov 8140]] |
| `Student Workforce` | Students, educators, veterans, workforce/job-placement programs        | `student-workforce` | `Security+` / `Career-Prep` | [[Sec+ RSA Copy - Student Workforce]] |

Use the same landing page for all three ad groups:

```text
https://becertifiedtoday.com/comptia-sec+-home.html
```

Add tracking parameters at the ad level:

```text
?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=<ad-group-content>
```

---

## Final URLs

```text
Core Exam Prep
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=core-exam-prep

Military Gov 8140
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=mil-gov-8140

Student Workforce
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=student-workforce
```

---

## Ad Schedule

Start broad enough for Google to learn, but avoid overnight waste.

| Day | Run time | Bid adjustment | Why |
|-----|----------|----------------|-----|
| Monday-Friday | **6:00 AM-9:00 AM** | 0% | Before-work research |
| Monday-Friday | **11:00 AM-2:00 PM** | 0% | Lunch break searches |
| Monday-Thursday | **5:00 PM-11:30 PM** | **+15%** | Main after-work study window |
| Friday | **5:00 PM-10:00 PM** | 0% | Lower but still useful |
| Saturday-Sunday | **9:00 AM-11:00 PM** | 0% | Weekend study blocks |
| Overnight | Pause or -90% | Avoid | Low-intent waste unless data proves otherwise |

Do not over-tighten schedule until at least one week of click and checkout data exists.

---

## Split Later Only If Data Proves It

Keep this as one campaign until an ad group has enough signal to justify its own budget or controls.

Split an ad group into a separate campaign only when it needs one of these:

- its own daily budget cap
- its own geo strategy, such as base/campus radius targeting
- its own schedule
- its own bidding strategy
- its own landing page
- materially different conversion value or ROI

Until then, the stronger foundation is **one campaign, three ad groups, shared budget, strong negatives, and one landing page**.

---

## Week-1 Review

On day 7, review by ad group and keyword:

| Signal | Action |
|--------|--------|
| Clicks + `begin_checkout` | Keep; consider exact match promotion |
| High CPC + no checkout | Lower max CPC or pause after enough clicks |
| Search term is course/free/dump/PDF intent | Add negative immediately |
| One ad group spends without checkout | Tighten keywords before splitting campaigns |
| One ad group clearly converts | Consider budget increase or future campaign split |

---

## Analytics monitoring loop (admin + Obsidian)

**Code registry:** `server-lib/secplus-google-ad-groups.js` (ad group slugs, `utm_content`, RSA pin H1) · synced to `server-lib/campaign-marketing-registry.js` (`secplus_portal`).

| Step | Where | What |
|------|-------|------|
| 1. **Measure** | [/admin → Security+ ad groups](https://becertifiedtoday.com/admin#section-secplus-ad-groups) | GA4 sessions + `begin_checkout` per `utm_content` |
| 2. **Diagnose** | [/admin → Recommendations](https://becertifiedtoday.com/admin#section-recommendations) | Rule-based tactics (scale winner, fix zero-checkout ad group) |
| 3. **Log** | [/admin → Daily campaign log](https://becertifiedtoday.com/admin#section-daily-log) | Spend, RSA edits, site changes for the day |
| 4. **Edit copy** | [[Sec+ RSA Copy]] · [[Sec+ RSA Copy - Military Gov 8140]] · [[Sec+ RSA Copy - Student Workforce]] | Per-ad-group headlines/descriptions |
| 5. **Spend truth** | [Google Ads](https://ads.google.com) | Clicks, CPC, search terms — compare to GA4 sessions |
| 6. **Weekly** | `node scripts/marketing-weekly-report.mjs` | Archive in `data/reports/weekly/` · [[Weekly Reports]] |

**utm_content → ad group (must match Final URL):**

| `utm_content` | Ad group | RSA section |
|---------------|----------|-------------|
| `core-exam-prep` | Core Exam Prep | [[Sec+ RSA Copy#Phase 2 — exam prep lead (paste when ready)]] |
| `mil-gov-8140` | Military Gov 8140 | [[Sec+ RSA Copy - Military Gov 8140]] |
| `student-workforce` | Student Workforce | [[Sec+ RSA Copy - Student Workforce]] |

**Hold rule:** After a copy or URL change, wait **7 days** before judging checkout rate — log the change date in Daily campaign log so Recommendations compare the right window.

[[README|← Sec+ Campaign folder]]

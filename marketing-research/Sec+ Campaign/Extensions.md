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

# Extensions — Sitelinks & Geo

**Campaign:** one US-only Search campaign · see [[Sec+ One-Campaign Ad Group Plan]]

Paste sitelinks at **campaign** level. Link text <=25 chars · each description <=35 chars.

**Checklist rows:** [[secplus-campaign-checklist.csv]] — filter **Phase** = `Extensions`.

Base UTM: `utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal`. Use `utm_content` for the sitelink.

**Primary landing:** `/comptia-sec+-home.html` — all Google Ads traffic. Institutional discount URL `/verified-learner-discounts.html` is **not** a sitelink until verification and discounted checkout are live.

---

## Sitelinks (6) — Live Phase 1

| #   | Link text               | Description 1              | Description 2                | URL                                                                                                                                                                        |
| --- | ----------------------- | -------------------------- | ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | 30-Day Access · $19.99  | Full exam prep + timed sim | One payment, no subscription | `https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-30d#purchase`                       |
| 2   | 1000+ SY0-701 Questions | Blueprint-verified bank    | Adaptive review modes        | `https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-bank#purchase`                      |
| 3   | Timed 90-Min Sim        | Mixed MCQ and PBQ run      | Domain scorecard included    | `https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-sim#purchase`                       |
| 4   | Preview Sample Prep     | MCQ + 3 PBQ scenarios      | Same UI as full access       | `https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-samples#home-secplus-samples-title` |
| 5   | DoD 8140 Exam Prep      | Work-required SY0-701      | Timed sim + verified bank    | `https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-dod#purchase`                       |
| 6   | Scorecard & Review      | Timed sim + weak domains   | Adaptive review modes        | `https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-scorecard#purchase`                 |

---

## Copy-Paste Block

```text
Sitelink 1
Name: 30-Day Access · $19.99
Description 1: Full exam prep + timed sim
Description 2: One payment, no subscription
URL: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-30d#purchase

Sitelink 2
Name: 1000+ SY0-701 Questions
Description 1: Blueprint-verified bank
Description 2: Adaptive review modes
URL: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-bank#purchase

Sitelink 3
Name: Timed 90-Min Sim
Description 1: Mixed MCQ and PBQ run
Description 2: Domain scorecard included
URL: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-sim#purchase

Sitelink 4
Name: Preview Sample Prep
Description 1: MCQ + 3 PBQ scenarios
Description 2: Same UI as full access
URL: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-samples#home-secplus-samples-title

Sitelink 5
Name: DoD 8140 Exam Prep
Description 1: Work-required SY0-701
Description 2: Timed sim + verified bank
URL: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-dod#purchase

Sitelink 6
Name: Scorecard & Review
Description 1: Timed sim + weak domains
Description 2: Adaptive review modes
URL: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=sitelink-scorecard#purchase
```

---

## Message Match

- Purchase sitelinks go to `#purchase` on cert home.
- Sample sitelink goes to `#home-secplus-samples-title`.
- DoD sitelink reinforces the `Military Gov 8140` ad group but stays campaign-level.
- No “Free” in link text; use **Preview Sample Prep**.
- No discount sitelinks in paid Search.

---

## URL Exclusions

AI Max and URL expansion stay **Off**. If Google asks for URL exclusions or any automated URL expansion is enabled later, exclude non-sales and non-Sec+ pages:

```text
/admin
/admin/
/COMP_TIA_SEC+/secplus-portal-request-link.html
/COMP_TIA_SEC+/secplus-portal-restore-access.html
/verify-question.html
/how-we-verify-questions.html
/verified-learner-discounts.html
/secplus-sample
/sample
/CCNA-Study/
/CCNP-ENCOR-Study/
/question-
```

---

## Geo

**Current build:** United States only · Presence only.

Do not layer complex geo targeting at launch. Keep the initial campaign national so the shared $25/day budget can collect cleaner ad group and keyword data.

Future geo layers can be tested after checkout signal appears:

| Cluster | Examples | Use when |
|---------|----------|----------|
| Major military installations | 60-mile radius around priority bases | `Military Gov 8140` converts or gets qualified checkout signal |
| Federal / contractor hubs | DC, Arlington, Fort Meade, Huntsville, San Antonio, Colorado Springs | Gov terms convert |
| College cyber programs | CAE schools and large community colleges | `Student Workforce` converts |
| Workforce / veteran programs | American Job Center metros, VA workforce hubs | Workforce or veteran terms convert |
| State / local government | State capitals and larger cities | Public-sector terms convert |

Split to a separate campaign only if geo controls become necessary.

[[README|← Sec+ Campaign folder]]

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

**Campaigns:** three US-only Search campaigns · see [[Sec+ Three-Campaign US Plan]]

Paste at **campaign** level. Link text ≤25 chars · each description ≤35 chars.

**Checklist rows:** [[secplus-campaign-checklist.csv]] — filter **Phase** = `Extensions`.

Base UTM: `utm_source=google&utm_medium=cpc` plus the campaign-specific `utm_campaign` from [[Sec+ Three-Campaign US Plan#Budget structure]].

**Primary landing:** `/comptia-sec+-home.html` — all Google Ads traffic. Institutional discount URL `/verified-learner-discounts.html` is **not** a sitelink until verification and discounted checkout are live. Even after launch, do not use it as a first-time visitor CTA, homepage banner, popup, welcome coupon, or generic paid Search promotion.

---

## Sitelinks (6) — live Phase 1

| #   | Link text              | Description 1             | Description 2                | Full URL                                                                                                                                                        |
| --- | ---------------------- | ------------------------- | ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | 30-Day Access · $19.99 | Full exam prep + timed sim | One payment, no subscription | Use campaign-specific `utm_campaign`; `utm_content=sitelink-30d#purchase` |
| 2   | 1000+ SY0-701 Questions | Blueprint-verified bank   | Adaptive review modes        | Use campaign-specific `utm_campaign`; `utm_content=sitelink-bank#purchase` |
| 3   | Timed 90-Min Sim       | Mixed MCQ and PBQ run     | Domain scorecard included    | Use campaign-specific `utm_campaign`; `utm_content=sitelink-sim#purchase` |
| 4   | Preview Sample Prep    | MCQ + 3 PBQ scenarios     | Same UI as full access       | Use campaign-specific `utm_campaign`; `utm_content=sitelink-samples#home-secplus-samples-title` |
| 5   | DoD 8140 Exam Prep     | Work-required SY0-701     | Timed sim + verified bank    | Use `secplus_gov_us`; `utm_content=sitelink-dod#purchase` |
| 6   | Scorecard & Review     | Timed sim + weak domains  | Adaptive review modes        | Use campaign-specific `utm_campaign`; `utm_content=sitelink-scorecard#purchase` |

---

## Phase 2 sitelinks (paste when ready)

Replace sitelink **#2** with **How We Verify** when `/how-we-verify-questions.html` is indexed and linked from cert home:

| # | Link text | Description 1 | Description 2 | URL |
|---|-----------|---------------|---------------|-----|
| 2 | How We Verify Questions | Official blueprint tags | Tier A verified keys | `https://becertifiedtoday.com/how-we-verify-questions.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_core_us&utm_content=sitelink-verify` |

**Do not** add military discount sitelink to paid Search — discount verification is eligibility-based through organic, email, QR, partner, campus, or workforce paths only ([[Sec+ Phase 2 Institutional Targeting]]).

---

## Copy-paste block (Google Ads UI)

This block shows the **Core Exam Prep** `utm_campaign`. Clone it for the other two campaigns and replace `secplus_core_us` with `secplus_gov_us` or `secplus_workforce_us`.

```
Sitelink 1
Name: 30-Day Access · $19.99
Description 1: Full exam prep + timed sim
Description 2: One payment, no subscription
URL: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_core_us&utm_content=sitelink-30d#purchase

Sitelink 2
Name: 1000+ SY0-701 Questions
Description 1: Blueprint-verified bank
Description 2: Adaptive review modes
URL: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_core_us&utm_content=sitelink-bank#purchase

Sitelink 3
Name: Timed 90-Min Sim
Description 1: Mixed MCQ and PBQ run
Description 2: Domain scorecard included
URL: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_core_us&utm_content=sitelink-sim#purchase

Sitelink 4
Name: Preview Sample Prep
Description 1: MCQ + 3 PBQ scenarios
Description 2: Same UI as full access
URL: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_core_us&utm_content=sitelink-samples#home-secplus-samples-title

Sitelink 5
Name: DoD 8140 Exam Prep
Description 1: Work-required SY0-701
Description 2: Timed sim + verified bank
URL: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_gov_us&utm_content=sitelink-dod#purchase

Sitelink 6
Name: Scorecard & Review
Description 1: Timed sim + weak domains
Description 2: Adaptive review modes
URL: https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_core_us&utm_content=sitelink-scorecard#purchase
```

---

## Message match

- **Purchase sitelinks** → `#purchase` on cert home
- **Sample sitelink** → `#home-secplus-samples-title` (preview block, not ad headline)
- **Exam prep / bank / DoD** sitelinks → reinforce Test Preparation Site, not PBQ-only wedge
- **No “Free” in link text** — use *Preview Sample Prep*
- **No discount sitelinks** in paid Search
- **No first-time visitor discount CTAs** in homepage banners, popups, welcome offers, or generic checkout prompts

---

## URL exclusions

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

Use `/how-we-verify-questions.html` only as an intentional sitelink after launch; do not let automated expansion choose it as the main landing page.

---

## Geo

**Three-campaign build:** **United States only** — **Presence** only.

Layer location bid modifiers inside the appropriate US campaign:

| Cluster | Examples | Rationale |
|---------|----------|-----------|
| **Major military installations** | 60-mile radius around JBLM, Fort Cavazos, Fort Liberty, SJBSA, Nellis/Creech, Norfolk, San Diego, Fort Meade, etc. | MOS / 8140 deadline traffic |
| **Federal / contractor hubs** | DC, Arlington, Alexandria, San Diego, San Antonio, Norfolk, Honolulu, Huntsville, Colorado Springs, Denver, Oklahoma City, Jacksonville, El Paso, Atlanta | DoD civ + prime contractors |
| **College cyber programs** | CAE schools + state community colleges with Security+ gate | Graduation requirement |
| **Workforce / veteran programs** | American Job Center metros, VA workforce hubs, SkillBridge/TAP-adjacent metros | Job-placement intent |
| **State / local government** | State capitals and large population centers; avoid rural areas for now | `.gov` discount outreach |
| **First responder** | Large county seats and metro public-safety hubs | Public-safety IT / cyber training |

Federal/defense US metros remain especially relevant (DoD 8140). Each campaign has its own **$20/day** budget; hold keyword bids for the first 7 days, then use **+10–20% bid adjustments** on 60-mile base radii or top clusters if results support it.

**Location option:** Presence — people in or regularly in targeted locations.

Ad schedule and US-only setup: [[Sec+ Three-Campaign US Plan]]

[[README|← Sec+ Campaign folder]]

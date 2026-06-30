---
type: build-checklist
product: secplus
channel: google-ads
tags:
  - marketing
  - google-ads
  - secplus
  - checklist
  - build
---

# Sec+ Google Ads Build Checklist — One Campaign, Three Ad Groups

Use this checklist in Google Ads to build the current Security+ plan:

- **1 Search campaign**
- **3 ad groups**
- **United States only**
- **$25/day shared campaign budget**
- **Google determines ad group spend split based on output**
- **Hold budget, structure, and keyword bids for 7 days**
- Landing page: `/comptia-sec+-home.html`

Reference docs: [[Sec+ One-Campaign Ad Group Plan]] · [[Sec+ Notes]] · [[Sec+ Keywords]] · [[Sec+ RSA Copy]] · [[Extensions]]

---

## 0. Before Opening Google Ads

- [x] Confirm Stripe product is live: `secplus-portal-30d` at **$19.99 / 30 days**
- [x] Open cert home on desktop and phone: `/comptia-sec+-home.html`
- [x] Confirm purchase button starts Stripe checkout
- [x] Confirm GA4 `begin_checkout` is imported as **Primary** in Google Ads
- [x] Keep old `secplus_portal` history; do **not** delete it

---

## 1. Create Campaign

| Setting | Value |
|---------|-------|
| Campaign type | **Search** |
| Campaign name | `Security+ SY0-701 · US Search` |
| Budget | **$25/day** |
| Bidding | **Maximize clicks** |
| Max CPC | **$2.75** |
| Search partners | **Off** |
| Display Network | **Off** |
| Locations | **United States only** |
| Location option | **Presence: people in or regularly in targeted locations** |
| Language | English |
| AI Max / URL expansion | **Off** |
| Conversion | GA4 `begin_checkout` as Primary |

**Do not adjust keyword bids for the first 7 days** unless traffic is clearly junk.

---

## 2. Create Ad Groups

### Ad Group 1 — Core Exam Prep

- [x] Ad group name: `Core Exam Prep`
- [x] Display path: `Security+` / `Exam-Prep`
- [x] Final URL:

```text
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=core-exam-prep
```

- [x] Paste keywords from [[Sec+ Keywords#Ad group 1 — `Core Exam Prep`]]

### Ad Group 2 — Military Gov 8140

- [x] Ad group name: `Military Gov 8140`
- [x] Display path: `Security+` / `DoD-8140`
- [x] Final URL:

```text
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=mil-gov-8140
```

- [x] Paste keywords from [[Sec+ Keywords#Ad group 2 — `Military Gov 8140`]]
- [x] Paste RSA from [[Sec+ RSA Copy - Military Gov 8140]] (not the Core Exam Prep set)

### Ad Group 3 — Student Workforce

- [x] Ad group name: `Student Workforce`
- [x] Display path: `Security+` / `Career-Prep`
- [x] Final URL:

```text
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=student-workforce
```

- [x] Paste keywords from [[Sec+ Keywords#Ad group 3 — `Student Workforce`]]
- [x] Paste RSA from [[Sec+ RSA Copy - Student Workforce]] (not Core or Military sets)

---

## 3. Paste RSA Copy

Use [[Sec+ RSA Copy]]. Create one responsive search ad in each ad group.

| Ad group | RSA section | Pin H1 | Pin H2 |
|----------|-------------|--------|--------|
| `Core Exam Prep` | [[Sec+ RSA Copy#Phase 2 — exam prep lead (paste when ready)]] | `SY0-701 Exam Prep Online` | `Timed 90-Min Exam Sim` |
| `Military Gov 8140` | [[Sec+ RSA Copy - Military Gov 8140]] | `Security+ for DoD 8140` | `Timed 90-Min Exam Sim` |
| `Student Workforce` | [[Sec+ RSA Copy - Student Workforce]] | `Security+ Career Prep` | `Timed 90-Min Exam Sim` |

Pin:

- [x] **Core Exam Prep:** H1 `SY0-701 Exam Prep Online` · H2 `Timed 90-Min Exam Sim`
- [x] **Military Gov 8140:** H1 `Security+ for DoD 8140` · H2 `Timed 90-Min Exam Sim`
- [x] **Student Workforce:** H1 `Security+ Career Prep` · H2 `Timed 90-Min Exam Sim`

Keep other headlines and descriptions unpinned during week 1.

**Do not use:** guaranteed pass, actual exam questions, real exam, official DoD, free timed exam, or discount wording.

---

## 4. Add Sitelinks

Use [[Extensions#Sitelinks (6) — live Phase 1]]. Add them at campaign level with `utm_campaign=secplus_portal`.

- [ ] `30-Day Access · $19.99`
- [ ] `1000+ SY0-701 Questions`
- [ ] `Timed 90-Min Sim`
- [ ] `Preview Sample Prep`
- [ ] `DoD 8140 Exam Prep`
- [ ] `Scorecard & Review`

---

## 5. Add Negatives

Add negatives from [[Sec+ Keywords#All negatives]] at campaign level before launch.

Priority categories:

- [ ] Free intent
- [ ] Course / bootcamp / instructor-led intent
- [ ] Dump / braindump / answer-key intent
- [ ] PDF / ebook / download intent
- [ ] Voucher / coupon / discount intent
- [ ] Job and salary research intent
- [ ] CCNA / CCNP / non-Security+ cert terms

---

## 6. Apply Ad Schedule

| Day | Run time | Bid adjustment |
|-----|----------|----------------|
| Monday-Friday | 6:00 AM-9:00 AM | 0% |
| Monday-Friday | 11:00 AM-2:00 PM | 0% |
| Monday-Thursday | 5:00 PM-11:30 PM | +15% |
| Friday | 5:00 PM-10:00 PM | 0% |
| Saturday-Sunday | 9:00 AM-11:00 PM | 0% |
| Overnight | Pause or -90% |

---

## 7. URL Exclusions / Expansion Guardrails

Keep **AI Max / URL expansion Off**. If Google asks for URL exclusions, exclude:

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

## 8. Final Pre-Launch Check

- [ ] Campaign says **Search only**
- [ ] Campaign budget is **$25/day**
- [ ] Campaign says **United States only**
- [ ] Location option is **Presence**
- [ ] Search partners are **Off**
- [ ] Display Network is **Off**
- [ ] AI Max / URL expansion is **Off**
- [ ] Three ad groups exist
- [ ] Each ad group has the correct final URL and `utm_content`
- [ ] Campaign-level negatives are pasted
- [ ] Campaign-level sitelinks are pasted
- [ ] Purchase button opens Stripe checkout
- [ ] GA4 Realtime shows `begin_checkout` on a test click

---

## 9. Week-1 Review

| Signal | Action |
|--------|--------|
| Search term is wrong | Add negative first |
| Keyword has clicks + `begin_checkout` | Keep; consider exact match |
| High CPC + no checkout | Lower max CPC or pause after enough clicks |
| Ad group spends but no checkout | Tighten keywords before splitting campaigns |
| One ad group converts clearly | Consider future campaign split only after enough volume |

Log review note:

```text
TEST: One Sec+ Search campaign with three ad groups
HYP: Shared $25/day budget concentrates data and lets Google find the best ad group output
START: YYYY-MM-DD
DAY 7 REVIEW: search terms, ad group spend, checkout, and purchase signal reviewed
```

[[README|← Sec+ Campaign folder]]

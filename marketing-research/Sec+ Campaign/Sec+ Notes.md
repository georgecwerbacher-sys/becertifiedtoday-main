---
type: campaign-steps
product: secplus
campaign: Security+ SY0-701 · US Search
tags:
  - marketing
  - google-ads
  - secplus
  - checklist
---

# Sec+ Notes — Step-by-Step Campaign Setup

**Build:** one US-only Search campaign with three ad groups · see [[Sec+ One-Campaign Ad Group Plan]]  
**Budget:** **$25/day shared campaign budget** · max CPC **$2.75**  
**Tracking:** `utm_campaign=secplus_portal`; use `utm_content` to identify each ad group.

**Checklist CSV:** [[secplus-campaign-checklist.csv]]

---

## 0. Before You Open Google Ads

- [ ] Stripe $19.99 / 30-day product is live.
- [ ] `/comptia-sec+-home.html` opens on desktop and phone.
- [ ] Purchase button starts Stripe checkout.
- [ ] GA4 `begin_checkout` fires from the purchase path.
- [ ] GA4 `begin_checkout` is imported into Google Ads as a Primary conversion.
- [ ] RSA copy reviewed against [[Sec+ Positioning]].
- [ ] Keyword split reviewed in [[Sec+ Keywords#One-campaign ad group keyword split]].

---

## 1. Create the Campaign

1. Create a new **Search** campaign.
2. Name it:

```text
Security+ SY0-701 · US Search
```

3. Set daily budget:

```text
$25.00/day
```

4. Set bidding:
   - **Maximize clicks**
   - max CPC **$2.75**
   - hold keyword bids for 7 days
5. Turn **Search partners Off**.
6. Turn **Display Network Off**.
7. Keep **AI Max / URL expansion Off**.
8. Set language to **English**.

---

## 2. Set Location Targeting

1. Target **United States only**.
2. Set location option to **Presence: people in or regularly in targeted locations**.
3. Do not use “presence or interest.”
4. Do not add base, campus, or workforce radius targeting at launch unless a later review proves the need.

Start simple: national US reach, tight keywords, strong negatives. Add geo layers only after the ad groups show useful checkout signal.

---

## 3. Apply the Starting Schedule

Use this schedule from [[Sec+ One-Campaign Ad Group Plan#Ad Schedule]]:

| Day | Run time | Bid adjustment |
|-----|----------|----------------|
| Monday-Friday | 6:00 AM-9:00 AM | 0% |
| Monday-Friday | 11:00 AM-2:00 PM | 0% |
| Monday-Thursday | 5:00 PM-11:30 PM | +15% |
| Friday | 5:00 PM-10:00 PM | 0% |
| Saturday-Sunday | 9:00 AM-11:00 PM | 0% |
| Overnight | Pause or -90% |

Do not keep narrowing schedule in week 1 unless the data is clearly junk.

---

## 4. Create Three Ad Groups

| Ad group | Final URL |
|----------|-----------|
| `Core Exam Prep` | `https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=core-exam-prep` |
| `Military Gov 8140` | `https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=mil-gov-8140` |
| `Student Workforce` | `https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=student-workforce` |

Use one responsive search ad per ad group at launch. Keep the base proof consistent: **SY0-701 exam prep, 1000+ verified questions, 90-minute timed sim, adaptive review, 34 PBQs, $19.99/30 days**.

---

## 5. Paste Keywords by Ad Group

Use [[Sec+ Keywords#One-campaign ad group keyword split]].

Start phrase-heavy where intent is still exploratory, and keep exact match for the highest-intent simulation/readiness and 8140 terms. Do not add discount, free, dump, voucher, or generic course keywords.

---

## 6. Paste RSA Copy

Use [[Sec+ RSA Copy]].

Pin only the stable basics:

- H1: `SY0-701 Exam Prep Online`
- H2: `Timed 90-Min Exam Sim`

Keep the rest unpinned so Google can learn message fit by ad group.

---

## 7. Add Sitelinks

Paste sitelinks at the campaign level from [[Extensions]].

Use `utm_campaign=secplus_portal` on every sitelink. Use `utm_content` to identify the sitelink, not the ad group.

---

## 8. Add Negatives Before Launch

Paste campaign-level negatives from [[Sec+ Keywords#All negatives]].

Priority blocks:

- free
- course / bootcamp / instructor-led
- dump / braindump / actual exam / answer key
- PDF / ebook / book / download
- voucher / coupon / discount
- competitor/course-vendor terms that already brought low-quality traffic

---

## 9. URL Exclusions

Keep AI Max and URL expansion **Off**. If Google asks for URL exclusions, exclude admin, restore, sample, CCNA, CCNP, and generic question pages per [[Extensions#URL exclusions]].

---

## 10. Launch Check

- [ ] One campaign exists: `Security+ SY0-701 · US Search`
- [ ] Campaign budget is **$25/day**
- [ ] US only + Presence only
- [ ] Search partners Off
- [ ] Display Network Off
- [ ] AI Max / URL expansion Off
- [ ] Three ad groups created
- [ ] Correct `utm_content` on each ad group final URL
- [ ] Campaign-level sitelinks added
- [ ] Campaign-level negatives added
- [ ] Test click reaches cert home
- [ ] Purchase button triggers GA4 `begin_checkout`
- [ ] Mobile checkout tested

---

## Week 1 Operating Rule

| Day | Action |
|-----|--------|
| 1 | Launch the full campaign with all three ad groups active |
| 3 | Review search terms; add negatives only |
| 7 | Review ad group, keyword, search term, CPC, checkout, and purchase data |

Do not split into separate campaigns in week 1. Split later only if an ad group proves it needs its own budget, geo strategy, schedule, bidding strategy, landing page, or materially different ROI.

[[README|← Sec+ Campaign folder]]

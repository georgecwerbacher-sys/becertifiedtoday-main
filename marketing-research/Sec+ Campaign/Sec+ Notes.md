---
type: campaign-steps
product: secplus
campaign: Security+ SY0-701 · Exam prep · becertifiedtoday
tags:
  - marketing
  - google-ads
  - secplus
  - checklist
---

# Sec+ Notes — how to set up the campaign

**Campaign:** `Security+ SY0-701 · Exam prep · becertifiedtoday`  
**Ad group:** **`Security+ PBQ Practice`** (only)  
**Budget:** **$20.00/day** · max CPC **$2.75** · **utm_campaign:** `secplus_portal`

**Checklist CSV:** [[secplus-campaign-checklist.csv]] · **Keywords CSV:** [[secplus-keywords.csv]]

---

## Reference voice (read before building ads)

[[Sec+ Positioning#Canonical reference (future use)|Canonical reference]] — exam-realistic browser prep, **34 PBQs**, **90-min timed sim + scorecard** with paid access, **$9.99/10d** · **$19.99/30d**.

Keywords and RSA: [[Sec+ Keywords]] · [[Sec+ RSA Copy]]

---

## Before you open Google Ads

- [ ] Stripe $9.99 / $19.99 products live
- [ ] Checkout on PBQ landing (desktop + phone)
- [ ] MCQ + dark web PBQ samples reachable from landing
- [ ] GA4 `begin_checkout` imported as Primary
- [ ] Keyword Planner worksheet — [[Sec+ Keywords#Keyword Planner worksheet]]
- [ ] RSA reviewed against [[Sec+ Positioning]]

---

## Phase 1 — Campaign shell

1. Campaign name: **`Security+ SY0-701 · Exam prep · becertifiedtoday`**
2. Budget **$20.00/day** · Search only · partners off
3. Bidding: Maximize clicks · max CPC **$2.75**
4. Geo: US, CA, UK, AU · **Presence** only
5. utm_campaign: **`secplus_portal`** on all ads
6. AI Max / URL expansion: **Off**
7. Paste **6 sitelinks** — [[Extensions]]

---

## Phase 2 — Ad group: Security+ PBQ Practice

1. Ad group name: **`Security+ PBQ Practice`**
2. Display path: `Security+` / `PBQ-Practice`
3. Final URL:

```
https://becertifiedtoday.com/secplus/pbq-practice-browser.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=pbq-wedge
```

4. Keywords: exact + phrase from [[Sec+ Keywords#Ad group — Security+ PBQ Practice]] (or import [[secplus-keywords.csv]])
5. RSA: [[Sec+ RSA Copy#Ad group Security+ PBQ Practice]]
6. Pin H1 `Security+ PBQ Practice` · H2 `$9.99 · 10-Day Access`

---

## Phase 3 — Negatives

- Campaign: [[Sec+ Keywords#Campaign negatives]]
- Ad group: [[Sec+ Keywords#Ad group negatives]]

---

## Phase 4 — Launch check

- [ ] One ad group enabled: **`Security+ PBQ Practice`**
- [ ] 6 sitelinks pasted — [[Extensions]]
- [ ] Final URL opens PBQ landing with correct UTMs
- [ ] GA4 `begin_checkout` on test purchase click
- [ ] Mobile checkout on PBQ landing

---

## Week 1

| Day | Action |
|-----|--------|
| 3 | Search terms → negatives |
| 7 | CPA review — hold $20/day or adjust max CPC |

[[README|← Sec+ Campaign folder]]

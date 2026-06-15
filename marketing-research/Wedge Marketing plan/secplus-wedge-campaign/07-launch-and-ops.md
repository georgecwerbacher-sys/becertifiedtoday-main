---
type: ops
product: secplus
campaign: SEC+_Wedge_PBQ
tags:
  - marketing
  - google-ads
  - secplus
  - ops
---

# Launch & ops — SEC+_Wedge_PBQ

[[README|← Campaign folder]] · Build: [[01-build-steps]]

---

## Launch verification

- [ ] Campaign + ad group **Enabled**
- [ ] Final URL loads pricing + FAQ (hard refresh)
- [ ] Free dark web PBQ sample completes without checkout
- [ ] $9.99 Stripe checkout from landing
- [ ] GA4 Realtime: `begin_checkout` (`secplus_portal_10d`)
- [ ] Sitelinks tested on mobile

---

## Week 1 daily log

**Hold:** budget · bidding · locations · RSA copy.

| Day | Impressions | Clicks | Spend | Checkouts | Notes |
|-----|-------------|--------|-------|-----------|-------|
| 1 | | | | | Ad serving? GA4 on test click? |
| 2 | | | | | |
| 3 | | | | | **Search terms review → negatives** |
| 4 | | | | | |
| 5 | | | | | |
| 6 | | | | | |
| 7 | | | | | **CTR · CPC · CPA review** |

Log summary in [[../../Weekly Reports|Weekly Reports]].

---

## Day 3 — search terms

1. Google Ads → Campaign → Search terms (7 days)
2. Bucket each term:
   - **Convert** — has checkout
   - **Promote** — ≥3 clicks, strong intent → add `[exact]` per [[03-keywords-ad-group]]
   - **Negative** — course, dump, jobs, head term → [[04-keywords-campaign-negatives]]
   - **Defer** — watch another week

---

## Day 7 — review

| Metric | Action |
|--------|--------|
| CTR < 1% | Check RSA ↔ landing message match |
| CPC > $4 | Pause expensive keywords with no checkouts |
| Zero impressions | Keyword volume, CPC cap, ad status, geo |
| Checkout CPA acceptable | Scale budget $12–15/day |
| Stable checkouts (15–20) | Switch to Maximize conversions |

---

## Week 2+

- [ ] Weekly search term export
- [ ] Pause keywords: spend > $20, zero checkouts
- [ ] Expand to Tier A countries if US CPA holds
- [ ] Add **`SEC+_Wedge_Timed`** ad group when timed landing is live
- [ ] Compare wedge CPA vs [[Security+ Campaign|portal campaign]]

---

## Scale gates

| Gate | Threshold |
|------|-----------|
| Increase budget | CPA stable 7+ days |
| Add timed-sim ad group | `/secplus/timed-practice-test.html` live |
| Impression share test | One ad group only, after stable CPA |

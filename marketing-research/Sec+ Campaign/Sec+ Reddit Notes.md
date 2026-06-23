---
type: campaign-steps
product: secplus
channel: reddit
campaign: SEC+_Wedge_Reddit
tags:
  - marketing
  - reddit
  - secplus
  - checklist
created: 2026-06-22
---

# Sec+ Reddit Notes — how to set up the campaign

**Campaign:** `SEC+_Wedge_Reddit`  
**Ad set 1:** PBQ angle → `/comptia-sec+-home.html`  
**Budget:** **$20/day** · **max bid $4.00**  
**utm_campaign:** `secplus_wedge_pbq` · **utm_content:** `reddit-pbq`

**Checklist CSV:** [[secplus-reddit-checklist.csv]] · **Copy:** [[Sec+ Reddit Copy]] · **Shell:** [[Sec+ campaign — Reddit only]]

Account one-time setup: [[../Reddit/Account|Reddit Account]] · UTMs: [[../Reddit/marketing/Budget and UTMs|Budget and UTMs]]

---

## Reference voice (read before building ads)

[[Sec+ Positioning#Canonical reference (future use)|Canonical reference]] — exam-realistic browser prep, **34 PBQs**, **90-min timed sim + scorecard**, **$9.99/10d** · **$19.99/30d**.

Reddit copy: [[Sec+ Reddit Copy]] · organic templates: [[../Reddit/posting/Sec+ replies|Sec+ replies]]

---

## Before you open ads.reddit.com

- [ ] Stripe $9.99 / $19.99 products live (same as Google pre-launch)
- [ ] Checkout on PBQ landing (desktop + phone)
- [ ] Free dark web PBQ sample loads from PBQ landing
- [ ] GA4 `begin_checkout` fires for `secplus_portal_10d` and `secplus_portal_30d`
- [ ] Login at [ads.reddit.com](https://ads.reddit.com) as **u/BeCertifiedToday**
- [ ] Payment method + USD currency set — [[../Reddit/Account|Account]]

---

## Phase 1 — Campaign shell

1. Campaign name: **`SEC+_Wedge_Reddit`**
2. Objective: **Traffic**
3. Daily budget: **$20/day**
4. Max bid: **$4.00**
5. Schedule: continuous
6. Locations: US, CA, UK, AU

---

## Phase 2 — Ad group targeting

1. **Placements:** Feed **ON** · Conversation **ON**
2. **Communities:** `r/CompTIA`, `r/SecurityPlus`
3. Skip interests and keyword targeting for launch
4. **Bidding:** Max bid **$4.00** (or cost cap if Reddit UI labels it that way)
5. **Reddit Pixel:** skip · UTMs in URL only

---

## Phase 3 — Ad set 1 (PBQ — launch this first)

1. Post type: **Image** (or Promoted post with image)
2. Profile: **u/BeCertifiedToday**
3. CTA: **Learn More**
4. **Destination URL** — paste **one** of these patterns (not both fields with the same URL):

**Option A — single field:**

```
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=reddit&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=reddit-pbq
```

**Option B — split fields:**

- Destination: `https://becertifiedtoday.com/secplus/pbq-practice-browser.html`
- URL parameters: `utm_source=reddit&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=reddit-pbq`

5. **Tracker URL** (third-party): **leave empty** — if Reddit shows “tracker URL must be different from destination URL”, you pasted the landing link into Tracker by mistake. Clear it.
6. Paste headline + body from [[Sec+ Reddit Copy#Ad set 1 — PBQ (start here)]]
7. Upload PBQ screenshot · add on-image text from [[Sec+ Reddit Copy#Image ad — text on creative]]
8. Submit · wait for review (often 24–48 hr)
9. Status = **Active**

---

## Phase 4 — Ad set 2 (timed sim — after 7 days)

Only if Ad set 1 CTR is healthy but you want a work-cert angle test.

1. Final URL:

```
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=reddit&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=reddit-timed-sim
```

2. Copy from [[Sec+ Reddit Copy#Ad set 2 — timed sim + work cert]]
3. Same targeting as Ad set 1

---

## Phase 5 — Launch check

- [ ] Ad status **Active** (not Pending/Rejected)
- [ ] Final URL opens PBQ landing with `utm_content=reddit-pbq`
- [ ] GA4 Realtime → session source = `reddit` after test click
- [ ] Mobile landing + checkout work
- [ ] Launch date logged in [[../Reddit/posting/Post log|Post log]]

---

## Phase 6 — Organic (parallel, not paid)

Run alongside paid — builds karma and catches threads ads miss.

1. Read [[../Reddit/posting/Voice guide|Voice guide]] before every reply
2. Use [[../Reddit/posting/Sec+ replies|Sec+ replies]] — change wording each time
3. Link only when it fits · disclose you built the site
4. Log every thread in [[../Reddit/posting/Post log|Post log]]
5. Target: **5+ helpful replies** in first 14 days

Optional organic UTM when linking:

```
?utm_source=reddit&utm_medium=organic&utm_campaign=secplus_wedge_pbq&utm_content=reply
```

---

## Week 1

| Day | Action |
|-----|--------|
| 1 | Confirm ad Active · GA4 `reddit` sessions on test click |
| 3 | Reddit dashboard: impressions, CTR (aim **> 0.2%**) |
| 7 | GA4 `begin_checkout` by `utm_content=reddit-pbq` · log in A/B table [[Sec+ Reddit Copy#A/B log]] |

If CTR low → swap to [[Sec+ Reddit Copy#Ad set 1 — short variant (low CTR swap)|short variant]]

If rejected → remove exam-claim language · resubmit · note fix in Post log

---

## Troubleshooting — “Not delivering · No active ad groups”

Reddit shows this when the **campaign** exists but nothing underneath is **Active**. The campaign shell alone does not deliver.

### Fix (5 min in ads.reddit.com)

1. Open **Campaigns** → click **`SEC+_Wedge_Reddit`**
2. Check the **Ad groups** tab (Reddit may label this **Ad sets**):
   - **Empty?** → **Create ad group** and finish all three layers: ad group → ad → Submit/Publish
   - **Exists but Paused?** → toggle **Active**
   - **Draft / Incomplete?** → open it, finish creative + URL, click **Publish** or **Submit for review**
3. Inside the ad group, open **Ads**:
   - You need at least **one ad** with status **Active** or **In review** (not Draft, Rejected, or Paused)
   - **Rejected?** → read reason, fix copy, resubmit ([[Sec+ Reddit Copy#Do not use in paid ads|banned phrases]])
4. Confirm **campaign** toggle is also **Active** (not paused at campaign level)
5. Confirm **Billing** has a valid payment method (failed charge can block delivery)

### After you publish

| Status | Meaning |
|--------|---------|
| **In review** | Normal for 24–48 hr — campaign may still say “Not delivering” until approved |
| **Active** | Should show impressions within a few hours |
| **Rejected** | Fix creative; ad group counts as inactive until resubmitted |

### Minimum ad group to create (if starting from scratch)

| Layer | Name suggestion | Required fields |
|-------|-----------------|-----------------|
| Ad group | `Sec+ PBQ · r-CompTIA-SecurityPlus` | Feed + Conversation ON · r/CompTIA + r/SecurityPlus · US/CA/UK/AU · Lowest cost |
| Ad | `PBQ browser · Image` | Image + headline + Learn More + PBQ final URL (Phase 3 above) |

Copy CCNA structure if stuck: your **CCNA_Wedge_Reddit** campaign already has a working ad group — mirror that layout, swap subs and URL.

---

## Do not

- Boost a normal post from reddit.com (use ads.reddit.com for targeting + UTMs)
- Pause Google **$20/day** Sec+ Search to fund Reddit (different channels — Google promo spend is separate)
- Send ads to `/sample` only (skips pricing story)
- Lead with dumps, guaranteed pass, or “real exam questions”

[[README|← Sec+ Campaign folder]]

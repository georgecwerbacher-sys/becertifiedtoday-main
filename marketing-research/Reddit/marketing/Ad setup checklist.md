---
type: checklist
tags:
  - marketing
  - reddit
  - checklist
created: 2026-06-19
---

# Reddit ad setup checklist

Step-by-step for **ads.reddit.com** (not regular reddit.com). Copy lives in [[CCNA ad copy]] and [[Sec+ ad copy]].

[[../README|← Reddit hub]] · UTMs: [[Budget and UTMs]]

---

## Phase 1 — Account (one time)

See [[../Account|Account]] for username and personal vs business notes.

- [x] Login at [ads.reddit.com](https://ads.reddit.com) with **u/BeCertifiedToday** (see [[../Account|Account]])
- [x] Business / ad account created
- [x] Payment method added (credit card)
- [x] Currency **USD** · time zone matches how you read GA4
- [x] Bookmark ads dashboard

---

## Phase 2 — CCNA campaign

**Campaign name:** `CCNA_Wedge_Reddit`

- [x] Objective: **Traffic** (website visits)
- [x] Daily budget: **$10/day**
- [x] Schedule: continuous through Jul 19, 2026 (adjust later)
- [x] **Locations:** United States, Canada, United Kingdom, Australia
- [x] **Placements:** **Feed ON** · **Conversation ON** (not Conversation-only)
- [x] **Communities:** `r/CCNA`, `r/Cisco`
- [x] **Bidding:** **Lowest cost** (automated on) · **Cost cap OFF**
- [x] Skip interest / keyword targeting for launch
- [x] **Tracker / Reddit Pixel:** skip · UTMs in URL only
- [ ] Ad format: **Promoted post** (text + optional image)
- [ ] Paste copy from [[CCNA ad copy#Ad A — primary (start here)|CCNA Ad A]]
- [ ] **Final URL** (copy-paste):

```
https://becertifiedtoday.com/ccna-home.html?utm_source=reddit&utm_medium=cpc&utm_campaign=ccna_wedge_lab&utm_content=reddit-labs
```

- [ ] CTA button: **Learn More**
- [ ] Image (optional): VLAN lab or timed sim screenshot from site
- [ ] Submit · wait for review (often 24–48 hr)
- [ ] Status = **Active**

---

## Phase 3 — Security+ campaign

**Campaign name:** `SEC+_Wedge_Reddit`

- [ ] Objective: **Traffic**
- [ ] Daily budget: **$10/day** (or split $5 PBQ + $5 timed sim later)
- [ ] **Locations:** US, CA, UK, AU
- [ ] **Communities:** `r/CompTIA`, `r/SecurityPlus`
- [ ] Ad set 1 — PBQ angle · copy from [[Sec+ ad copy#Ad set 1 — PBQ (start here)|Sec+ PBQ ad]]
- [ ] **Final URL:**

```
https://becertifiedtoday.com/secplus/pbq-practice-browser.html?utm_source=reddit&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=reddit-pbq
```

- [ ] CTA: **Learn More**
- [ ] Image (optional): PBQ scenario screenshot
- [ ] Submit · **Active**

---

## Phase 4 — Measurement

- [ ] GA4 Realtime → filter **session source** = `reddit`
- [ ] GA4 Exploration → `begin_checkout` by `utm_source`, `utm_content`
- [ ] Note launch date in [[../posting/Post log|Post log]]
- [ ] Week 1 review date: ___________

---

## Phase 5 — Week 1 review

- [ ] Reddit dashboard: impressions, CTR (aim **> 0.2%** in niche subs)
- [ ] Compare `reddit-labs` vs `reddit-pbq` checkouts in GA4
- [ ] If CTR low: swap to short variant in ad copy notes
- [ ] If rejected: remove exam-claim language · resubmit
- [ ] Log decision in [[../posting/Post log|Post log]]

---

## Do not

- Boost a normal post from reddit.com (use ads.reddit.com for targeting + UTMs)
- Lead with "real exam questions" / "guaranteed pass" / "dumps"
- Send ads to `/sample` only (skips pricing story)
- Pause Google **$10/day** to fund Reddit (Google spend counts toward **$510** promo)

---

## If ad rejected

1. Read rejection reason in ads dashboard
2. Remove: guaranteed pass, actual exam questions, dump language
3. Resubmit with softer copy from [[CCNA ad copy]] / [[Sec+ ad copy]]
4. Note rejection + fix in Post log

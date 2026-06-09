---
type: strategy
status: active
tags:
  - google-ads
  - bidding
  - ccna
  - encor
  - security-plus
created: 2026-06-01
---

# Google Ads bidding strategy — top placement on solid keywords

**Goal:** Appear in the **top sponsored slots** (typically positions 1–4 on desktop; 1–3 on mobile) for **exam-prep / simulation** queries — not for course-shopper terms.

**Positioning edge:** Competitors sell **PDFs (~$100)** or **video courses ($200–$800+)**. Few sell a **100% browser timed simulation** with PBQ-style interaction. Bid on **their weak keywords**, not theirs.

Related: [[positioning-and-messaging|Positioning]] · [[promotions-and-coupons|Promotions & coupons]] · [[cisco-certifications-exam-prep-foundation|Cisco foundation]] · [[security-plus-federal-defense-foundation|Security+ federal]] · Campaign exports in `02-campaigns/*/`

**Active starter budget (2026-06-01):** **$10.00/day** on **Security+ only** for launch (see [[#Launch sequence — Security+ first|launch sequence]]). CCNA and ENCOR stay in the vault as paste-ready exports — **paused in Google Ads** until Sec+ has baseline CTR, search terms, and conversion data.

---

## Launch sequence — Security+ first

**Recommendation:** Run paid Search on **`secplus_portal` only** until you have 2–3 weeks of data (or ~30 conversions), then turn on CCNA and/or ENCOR.

| Why Security+ first | Detail |
|---------------------|--------|
| **Demand** | Largest exam-prep search pool of your three products |
| **Compliance intent** | DoD 8140 / contractor deadlines → buyers closer to test day ([[security-plus-federal-defense-foundation\|federal foundation]]) |
| **Funnel maturity** | Lead magnet, scorecard, and landing page were verified **ready** before CCNA/ENCOR export sync ([[../06-website-optimization/ad-site-verification-2026-05-31\|ad-site verification]]) |
| **$10/day learning** | One campaign ≈ **3 clicks/day** with signal in **one** auction — three campaigns at $10 each ≈ **1 click/day each**, too thin to optimize |

**Budget options (pick one):**

| Option | Daily spend | When |
|--------|-------------|------|
| **A — lean** | **$10/day** on Security+ only | Minimize cash; slower data |
| **B — faster learn** | **$20–30/day** on Security+ only | Same total you would have spent on three × $10; more top-of-page on `sy0-701 practice test` |

**Caveat:** Security+ Tier 1 CPCs are the **highest** of the three — you trade cost per click for volume and intent. Do not chase course/PDF keywords; stay on **practice test / exam simulation** Exact match.

**When to add CCNA or ENCOR:** Search terms are clean, hero keywords show QS ≥ 6, and you have at least one reliable conversion action (lead or `begin_checkout`). ENCOR is usually **second** (smaller market, lower CPC — easier top placement). CCNA **third** unless your audience is overwhelmingly Cisco-first.

**In Google Ads:** Create/pause — **Enabled:** `Security+ · Exam prep · becertifiedtoday` · **Paused:** CCNA and ENCOR campaigns (or do not create them yet).

---

## What “top 4” means in Google Ads

| Metric | Use for |
|--------|---------|
| **Search top impression rate** | % of impressions shown above organic results |
| **Search absolute top impression rate** | % shown in position 1 |
| **Auction insights → Outranking share** | Who beats you on Tier 1 keywords |

**Target:** **70–85% top-of-page** on Tier 1 ad groups — not 95% absolute top (position 1 only). Absolute top is expensive and often unnecessary when your ad copy says “timed simulation in browser” and course ads say “40-hour video training.”

---

## Keyword tiers (bid budget follows tier)

Pull exact lists from landing maps:

| Product | Tier 1 (visibility priority) | Map |
|---------|------------------------------|-----|
| CCNA | `ccna practice test`, `ccna 200-301 practice exam`, `ccna exam simulation`, `ccna mock exam` | [[../07-keywords/landing-maps/ccna-portal\|ccna-portal]] |
| ENCOR | `ccnp encor practice test`, `encor 350-401 practice exam`, `ccnp encor simulation`, `encor timed exam simulation` | [[../07-keywords/landing-maps/ccnp-encor-portal\|ccnp-encor-portal]] |
| Security+ | `comptia security+ practice test`, `sy0-701 practice test`, `security+ exam simulation`, `security+ practice exam` | [[../07-keywords/landing-maps/security-plus-portal\|security-plus-portal]] |

**Tier 2** (format: drag-and-drop, CLI lab, OpenSSL PBQ): Maximize conversions or lower manual bids — visibility matters less than CPA.

**Do not chase top placement on:** `free course`, `training`, `bootcamp`, `udemy`, `pdf` — already in campaign negatives; course buyers have higher CPCs and wrong intent.

---

## Campaign architecture

### At **$10/day per product** (current — one campaign each)

| Setting | Value |
|---------|--------|
| Campaigns | **One Search campaign** per product — do **not** split Visibility vs Convert yet ($5/day each is too thin for Google to optimize) |
| Daily budget | **$10.00** on `ccna_portal`, `encor_portal`, `secplus_portal` |
| Bid strategy | **Maximize clicks** + **max CPC cap** (table below) |
| Ad groups live | **`lead_free_sim`** + **`sim_purchase`** only for first 2–3 weeks (CCNA: `ccna_*` · ENCOR: `encor_*` · Sec+: `secplus_*`) |
| Ad groups paused | Portal access, labs/PBQ, federal geo — see [[../05-playbooks/google-ads-bidding-verification#Ad groups — active vs paused at start (same pattern as Security+)|active vs paused table]] |
| Keywords live | **3–5 Exact** Tier 1 terms per product (not full export lists) |
| Top placement | Expect **some** top-of-page impressions on ENCOR first (lower CPC); CCNA/Sec+ head terms may rotate in/out of top 4 until budget rises |

**Spend focus inside $10:** Google allocates across active ad groups — fewer groups = more clicks on heroes. Target **~$6/day** lead ad group / **~$4/day** purchase ad group by pausing extras (not separate budgets).

### At **$20–25+/day per product** (scale — split optional)

Use **two Search campaigns per product** so bid strategies do not fight:

| Campaign | Ad groups | Bid strategy | Daily budget |
|----------|-----------|--------------|--------------|
| `{Product} · Tier1 · Visibility` | Tier 1 **Exact** only (8–15 keywords) | **Target impression share** → **Top of page 75%** + max CPC limit | **60–70%** of product spend |
| `{Product} · Tier2 · Convert` | Lead, sim purchase, portal, labs, federal | **Maximize conversions** / **Target CPA** | **30–40%** |

**Why split at scale:** “Maximize conversions” under-bids competitive Tier 1 terms. “Target impression share” over-spends on long-tail if applied to the whole campaign.

---

## Phased rollout (all three products)

### Phase 0 — Week 1 (learning, no Target IS yet)

| Setting | Value |
|---------|--------|
| Strategy | **Maximize clicks** with **max CPC cap** |
| Networks | Search only (no partners) |
| Match | Exact + Phrase on Tier 1; Phrase on Tier 2 |
| Purpose | Collect CTR, QS, search terms; tighten negatives |

**Max CPC caps at $10/day** (tighter — ~3–4 clicks/day per campaign):

| Product | Campaign max CPC (Maximize clicks) | Notes |
|---------|-----------------------------------|--------|
| CCNA | **$2.75** | Raise toward $3.25 only if Search top IS stays &lt; 40% on heroes |
| ENCOR | **$2.25** | Smallest market; often enough for top-of-page on Exact heroes |
| Security+ | **$3.25** | Highest competition; may get fewer clicks — prioritize Exact |

**At $20+/day** — looser caps: CCNA $3.50 · ENCOR $2.75 · Security+ $4.00 (Tier 2 ad groups when enabled).

### Phase 1 — Week 2–4

**If still at $10/day:** Stay on **Maximize clicks**; add **1–2 Exact** keywords that converted in week 1; pause any ad group with 0 clicks and spend &gt; 30% of budget.

**If budget ≥ $20/day per product:**

1. Split **`Tier1 · Visibility`** + **`Tier2 · Convert`** campaigns.
2. Visibility: **Target impression share (Top of page, 75%)** + max CPC at ~**120%** of Phase 0 avg CPC.
3. Pin RSAs to simulation / browser / timed exam (not “course”).
4. **Device:** +10% mobile on Visibility only if mobile CPA ≤ desktop.

### Phase 2 — After 30+ conversions / product (efficiency)

| Funnel step | Suggested target CPA | Max profitable CPA (rough) |
|-------------|----------------------|----------------------------|
| Free sim / assessment lead | $4–7 | ~$8 if 10%+ later purchase |
| $9.99 timed sim | $8–12 | ~$15 (one sim; upsell possible) |
| $19.99 portal | $15–22 | ~$28 |

Move **Tier2 · Convert** to **Target CPA** at those levels. **Keep Tier1 on Target IS** until organic + paid QS are 7+; then test lowering IS target to 65% or shifting heroes to tCPA if CPA holds at rank 2–3.

---

## Budget math (honest constraint)

```
Clicks per day ≈ daily budget ÷ avg CPC
```

At **$10/day** and **~$2.75 CPC** → about **3–4 clicks/day** per campaign. That is enough to **learn** (CTR, search terms, QS) and occasionally show in **top 4** on Exact simulation terms — especially ENCOR — but **not** enough to dominate `ccna practice test` or `sy0-701 practice test` all day.

| Product | Daily budget (current) | Realistic at $10/day | When to scale |
|---------|------------------------|----------------------|---------------|
| CCNA | **$10** | 3–4 clicks; top 4 on some Exact sim terms | Search top IS &lt; 40% on heroes **and** CPA on track → **$20**, then split campaigns |
| Security+ | **$10** | 2–3 clicks; head terms competitive | Same; Sec+ often needs **$25+** for steady top placement |
| ENCOR | **$10** | 3–5 clicks; best odds for top 4 at this budget | Raise if impression share lost to budget (not rank) |

**Portfolio total (launch):** **$10/day** Security+ only. **Optional accelerate:** **$20–30/day** on Security+ instead of splitting across three products later.

**Scale targets (later):**

| Product | Total daily | Tier1 Visibility | Tier2 Convert |
|---------|-------------|------------------|---------------|
| CCNA | $25–40 | $18–28 | $7–12 |
| Security+ | $25–40 | $18–28 | $7–12 |
| ENCOR | $20–25 | $12–18 | $5–7 |

---

## Ad group bid modifiers (inside Convert campaign)

| Segment | Modifier | When |
|---------|----------|------|
| Tier 1 federal geo (DC, COS, SATX, Norfolk) | +15% to +25% | `*_federal_*` ad groups |
| Tue–Thu 6am–10pm local | +10% | Study hours — see Cisco/Sec+ foundations |
| Sun 6pm–11pm | +10% | Catch-up study |
| Desktop | 0% baseline | Compare to mobile before big mobile cuts |

---

## Competitive messaging (helps rank without higher bids)

Higher **expected CTR** raises Ad Rank at the same bid. Stress in headlines/descriptions:

- **Timed simulation** / **full-length practice exam**
- **100% in browser** — no PDF, no install
- **PBQ / drag-and-drop / CLI lab** (where relevant)
- **One-time price** — not subscription course

Avoid competing on “best course” or “certification training” auctions.

---

## Verify settings in the UI

Step-by-step checklist (budget, Maximize clicks, max CPC cap, ad groups, 48h health): [[../05-playbooks/google-ads-bidding-verification|Google Ads bidding verification playbook]].

---

## Weekly checks ([[../05-playbooks/weekly-review-process|weekly review]])

1. **Auction insights** (Tier 1 keywords): who is “above rate” — course vendors vs practice-test sites?
2. **Search top IS** &lt; 60% on hero keywords → raise max CPC limit 10–15% or increase Visibility budget 20%.
3. **Search top IS** &gt; 90% and CPA over target → lower IS target to 65% or trim max CPC.
4. **Search terms:** course/dump/pdf → add negatives; high-converting sim terms → promote to Exact in Visibility campaign.
5. **Quality Score** &lt; 6 on a hero → fix LP headline match before raising bids ([[../06-website-optimization/google-ads-quality-score-guide|QS guide]]).

---

## Product-specific defaults

### CCNA (`ccna_portal`)

- Heroes: **`ccna_portal_10d`** + Exact Tier 1 question-bank / prep keywords in Visibility campaign (when budget ≥ $20/day).
- Optional: `ccna_sim_purchase` — Tier2 Convert — tCPA toward **$10** on sim, **$20** on portal.
- Federal: separate ad groups; +20% geo on Tier 1 metros only.
- **No** `ccna_lead_free_sim` ad group — free sim is on-site only, not paid Search.

### ENCOR (`encor_portal`)

- Fewer auctions — **Manual CPC** on heroes is acceptable if Target IS spends unevenly.
- Heroes: `encor_lead_free_sim`, `encor_sim_purchase` keywords with “simulation” / “practice test”.
- Do not bid top placement on `ccna` queries (negative already).

### Security+ (`secplus_portal`)

- Largest CompTIA market — expect **highest Tier 1 CPC** of the three.
- Heroes: `secplus_lead_free_sim` + `security+ exam simulation` Exact.
- OpenSSL PBQ campaign (`secplus_openssl_pbq`): Tier 2 Convert, not Visibility — niche, lower volume.

---

## Decisions log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-06-01 | **Launch Security+ only** at $10/day; pause CCNA/ENCOR in Ads | Largest demand + compliance intent; one campaign learns faster than three × $10 |
| 2026-06-01 | **$10/day** per product when all three run; **one campaign** each; lead + purchase ad groups only | $10 cannot support split campaigns or Target IS reliably; concentrate clicks on heroes |
| 2026-06-01 | Tier1 Visibility + Tier2 Convert split at **$20+/day** per product | Top 4 at scale needs rank-focused bidding separate from tCPA |
| 2026-06-01 | Simulation/exam keywords first; course terms stay negative | Competitor PDF/course auctions are wrong intent and expensive |

## Promotions

Do **not** add coupon CTAs to Search campaigns during launch. Use free sim + list price; see [[promotions-and-coupons|promotions & coupons]].

## Open questions

- [ ] Import **purchase value** into Google Ads for Maximize conversion value on portal vs sim.
- [ ] Validate Phase 0 CPC caps with 2 weeks of Auction insights per product.
- [ ] Test **Performance Max** only after Search heroes are stable (not a top-4 substitute).

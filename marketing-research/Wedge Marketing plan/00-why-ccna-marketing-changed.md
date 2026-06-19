---
type: strategy
parent: "[[Wedge Marketing plan]]"
tags:
  - marketing
  - ccna
  - wedge
  - pivot
created: 2026-06-15
---

# Why CCNA marketing changed

Single narrative for the 2026-06-14 pivot. Detail lives in linked plan sections; this note is the “why we stopped fighting head terms.”

[[Wedge Marketing plan|← Back to plan]]

---

## Old approach

- **Google Ads:** one Search campaign, **`ccna_portal_10v1`** ad group on Tier A head terms — `[ccna practice test]`, `[ccna mock exam]`, `[ccna question bank]`, phrase variants.
- **Landing:** generic portal purchase block on `ccna-home.html#purchase` with $9.99 / 10-day CTA.
- **Message:** “practice test,” “question bank,” “mock exam” — same vocabulary as every course vendor and dump site.
- **Geo:** broad English targeting; India and other low-conversion markets included early.
- **Bidding:** Maximize clicks with modest max CPC; impression share not a primary goal yet.

**Intent:** validate checkout funnel and get baseline CTR/CPC before scaling.

---

## What failed (signals, not moral judgment)

| Signal | What it meant |
|--------|----------------|
| **Zero or near-zero impressions** on head terms | Not always “wrong bid” — often low volume + auction pressure + CPC cap. See [[02-keywords-and-google-ads#Bidding (do not change strategy yet)]]. |
| **High CPC when impressions did show** | Course vendors (INE, CBT, Udemy funnels) bid head terms as **loss leaders** toward $300–$2,000 courses. You cannot match their LTV. |
| **India / low-conversion geo clicks** | High click volume, sample-only or bounce, almost no `begin_checkout`. Budget burn without US CPA signal. See [[03-pricing-and-funnel#India / low-conversion geo]]. |
| **Portal-only message match** | Searcher wanted “labs” or “timed sim”; ad promised “practice test.” Weak conversion even when clicks were cheap. |
| **Competing on question count** | Big banks advertise “7,000+ questions” and free samples. You lose the “biggest bank” game. Adaptive review is the answer — see [[03-pricing-and-funnel#Progress tracking]]. |
| **PayPal not live yet** | Minor friction at checkout; **does not fix** high CPC. Add after wedge landing + US geo are stable — [[03-pricing-and-funnel#PayPal]]. |

**Bottom line:** head-term CPC war is structurally unwinnable for a $9.99 sprint product vs course vendors.

---

## Competitor game (avoid it)

| They optimize for | Why CPC is high |
|-------------------|-----------------|
| Free sample → bootcamp / course | Profit on $500+ LTV |
| Dump / PDF / subscription banks | Volume SEO, low quality |
| Boson-style desktop sims | Brand + install moat |
| ExamTopics / forums | Community recall, not your buyer |

Full table: [[01-positioning-and-audience#What competitors optimize for (avoid their game)]]

**Do not** compete on “7000+ questions” or “free practice test” alone.

---

## Your wedge (what you can own)

| They sell | You sell |
|-----------|----------|
| Free samples → expensive course | **$9.99 / 10-day exam sprint** |
| 10,000 static questions | **Timed sim + drag-drop + CLI labs in browser** |
| GNS3 / Packet Tracer / IOU | **No install — labs in the testing engine** |
| PDF / dump / forum votes | **Verified explanations (V_2025 & V_2026)** |
| Big bank, random order | **Review loops on weak topics** |

**Primary audience:** person **2–3 weeks from exam day** asking *Am I ready?* — not shopping for the cheapest dump. [[01-positioning-and-audience#Primary audience]]

**Lead strengths in ads and landing pages:**

1. Browser CLI labs (VLAN, routing) — no third-party software
2. 120-min timed simulation
3. Verified explanations
4. Free try-first samples before checkout

---

## New funnel

```
Wedge Ads → Wedge landing pages → Free proof → $9.99/10d checkout → Portal → Exam day
```

| Phase | CCNA asset | Doc |
|-------|------------|-----|
| Traffic | **`CCNA_Wedge_Lab`** campaign / ad group | [[02-keywords-and-google-ads#Tier W1 — Primary (own these)]] |
| Landing | `/ccna/labs-without-gns3.html` | [[04-content-and-landing-pages#CCNA — build priority]] |
| Free proof | VLAN sample, D&D sample, free assessment | [[canvas/nodes/03-free-proof\|canvas 03-free-proof]] |
| Checkout | Stripe $9.99/10d · PayPal later | [[03-pricing-and-funnel]] |
| Measure | GA4 `begin_checkout` by `utm_content`, country | [[06-30-day-action-plan]] |

**Campaign pivot in practice:** [[../Campaigns#Wedge pivot]] · dedicated [[../campaigns/CCNA Wedge Lab Campaign|CCNA Wedge Lab Campaign]]

**Build tracker:** [[CCNA funnel build tracker]] · [[canvas/CCNA wedge funnel.canvas]]

---

## Geo and pricing decisions

| Decision | Rationale |
|----------|-----------|
| **US / CA / UK / AU first** | USD pricing, higher checkout intent, primary target |
| **Pause broad India paid** until US CPA baseline | High clicks, low $9.99 conversion; organic/YouTube later |
| **Presence-only targeting** | Not “interest in” — reduces junk geo |
| **Do not race on price** | Sell time-boxed sprint with progress included, not membership |
| **Deprioritize head terms** | Low bid or pause `[ccna practice test]`, `[ccna mock exam]`, `[ccna question bank]` |
| **Shift budget to wedge** | `ccna_browser_labs` / **`CCNA_Wedge_Lab`** + timed-sim keywords |

---

## Decision log

| Date | Decision |
|------|----------|
| 2026-06-14 | Adopt wedge strategy; deprioritize head-term CPC battle vs course vendors |
| 2026-06-14 | US/CA/UK/AU paid geo first; pause broad India spend until US CPA baseline |
| 2026-06-14 | Shift budget toward browser-labs + timed-sim wedge (see [[06-30-day-action-plan]]) |

---

## Related

- [[02-keywords-and-google-ads]] — wedge tiers, negatives, bidding
- [[05-competitor-tracking]] — monthly matrix, `npm run ccna:monthly`
- [[../Campaigns]] · [[../campaigns/CCNA Campaign|CCNA Campaign]]
- Repo: `scripts/ccna-wedge-lab-google-ads-checklist.csv`

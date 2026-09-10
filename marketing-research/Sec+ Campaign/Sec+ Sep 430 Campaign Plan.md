---
type: campaign-strategy
product: secplus
phase: sep-430
status: ready
tags:
  - marketing
  - google-ads
  - secplus
  - budget
  - search
---

# Sec+ Search campaign — $430 in 30 days

**Status:** Ready to build in Google Ads · **do not leave Launch 40 spending at the same time**  
**Channel:** Google Ads **Search** only  
**Goal:** `begin_checkout` → purchase on ethical Search traffic  
**Offer in ads:** **$19.99** / 30 days · one payment · no subscription  
**Landing:** https://becertifiedtoday.com/comptia-sec+-home.html  
**Flight:** **2026-09-02 → 2026-10-02** (30 days) or pause when spend hits the cap, whichever is first

Related: [[Advertising Ethics]] · [[Sec+ Positioning]] · [[Sec+ Sep 430 Keyword Lists]] · [[Sec+ Sep 430 RSA Copy]] · prior [[Sec+ Launch 40 Campaign Plan]]

---

## Budget pacing ($430 · 30 days)

Google Search has **no lifetime cap**. Set **$14/day**, watch cumulative spend, **pause at ~$410–$430**. Google can spend up to about **2×** the daily budget on a busy day, so drop the daily cap to **$7** when remaining budget is under **$40**.

$14 × 30 = **$420**. The leftover **$10** is the overspend buffer.

| Item | Value |
|------|------:|
| Total | **$430** |
| Daily | **$14** shared |
| Runway | **30 days** if spend is steady |
| Clicks / day (at $2.25–$2.75 CPC) | ~5–6 |
| List price in ads | **$19.99** / 30 days |
| Purchases to recover $430 (at $19.99) | ~22 |
| Purchases to recover $430 (if landing 50% off applies) | ~29 |

**Kill rule:** After **$70–$90** on clean (negatived) traffic with **0 `begin_checkout`**, pause and fix landing/offer/tracking before spending the rest.

**In Google Ads now:** pause `Security+ SY0-701 · US Search · Launch 40` (24h trial RSA is stale). Pause any other live Sec+ Search campaign so this $430 is not split.

Do **not** put the homepage first-visit 15-minute 50% off (`SEP50PERCENTOFF`) in RSA. Ads clickers who already visited will not get that clock. RSA stays at **$19.99**.

---

## Positioning

Security+ is last-mile practice after a course, not a video bootcamp.

| They sell | You sell |
|-----------|----------|
| Free samples → paid course | Free samples → timed sim + question bank |
| Video bootcamps | Browser practice + scorecard |
| Account signup + email list | No site registration — Stripe, then a portal link |
| Static PDF packs | Adaptive review in the browser, including phone |

**Policy-safe:** SY0-701 exam prep, question bank, PBQ practice, phone/browser, $19.99 / 30 days.  
**Never in ads or on the paid landing hero:** exam sim, exam simulation, simulator, mock exam, 90-min / timed sim as an official-exam replica, not a PDF, VCE, actual exam questions, real exam, dumps, braindump, cheat, pass guaranteed, competitor brand names, 24 hours free, “not AI,” walk in ready, like test day.  
**Never bid on** dump, cheat, simulation, or mock-exam searches. See [[Advertising Ethics]].

---

## Campaign shell

| Setting | Value |
|---------|-------|
| Name | `Security+ SY0-701 · US Search · Sep 430` |
| Type | Search only |
| Daily budget | **$14 shared** |
| Bidding (days 1–10) | Maximize clicks · max CPC **$2.50** |
| Bidding (after signal) | Maximize conversions when ≥15–20 `begin_checkout` |
| Geo | US only · Presence |
| Language | English |
| Networks | Partners Off · Display Off · AI Max Off |
| Primary conversion | GA4 `begin_checkout` |
| Offer in ads | **$19.99** / 30 days |
| utm_campaign | `secplus_portal_sep430` |

**Hold rule:** No structure / bid drama for 7 days unless junk traffic or broken tracking.

---

## Ad group (shared $14)

One ad group. All Search traffic lands on the Security+ home page.

| Ad group | Intent | `utm_content` | Lead message |
|----------|--------|---------------|--------------|
| `Exam Prep` | SY0-701 exam prep on the site | `exam-prep` | Browser question bank + PBQ practice · $19.99 / 30 days |

Final URL:

```text
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal_sep430&utm_content=exam-prep
```

**Defer:** a second ad group, Military/DoD 8140, student/workforce, 24h trial, dump intercept.

---

## Keywords

See [[Sec+ Sep 430 Keyword Lists]]. Exact + phrase only. **No Broad.**

---

## Campaign negatives

Paste from [[Sec+ Sep 430 Keyword Lists]] first (dump / cheat / actual-exam / PDF / **free** / **sample** / **example** / courses). Do not omit dump, cheat, free, sample, or example negatives.

---

## Week-1 review

| Signal | Action |
|--------|--------|
| Clicks + `begin_checkout` | Keep |
| High CPC + no checkout | Lower max CPC to **$2.00** or pause the keyword |
| Course / free / sample / example / dump / PDF search terms | Negative immediately |
| Spend with zero checkout | Follow the kill rule — pause the campaign and fix landing/offer/tracking |

Admin: [/admin#section-secplus-ad-groups](https://becertifiedtoday.com/admin#section-secplus-ad-groups)

[[README|← Sec+ Campaign]] · [[Sec+ Sep 430 Build Checklist|Build checklist]]

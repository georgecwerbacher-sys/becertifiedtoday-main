---
type: campaign-strategy
product: secplus
phase: dump-intercept
status: ready-to-build
tags:
  - marketing
  - google-ads
  - secplus
  - dump-intercept
---

# Sec+ Dump Intercept — campaign plan

**Status:** Ready to build (separate from Launch 40)  
**Goal:** Intercept dump / PDF-dump searchers and convert them to **browser exam prep** (checkout)  
**Offer:** same as Launch 40 — list **$19.99** · August **$15.99** (`AUGUSTPROMO2026`)  
**Landing:** https://becertifiedtoday.com/comptia-sec+-home.html (top of fold)  
**utm_campaign:** `secplus_portal_dump_intercept`

Related: [[Sec+ Launch 40 Campaign Plan]] · [[Sec+ Dump Intercept Keyword Lists]] · [[Sec+ Dump Intercept RSA Copy]] · [[Sec+ Dump Intercept Build Checklist]]

---

## Why a separate campaign

Target impression share (top of page) is **campaign-level**. Dump keywords need higher bids / top placement without breaking Launch 40 Maximize clicks.

| Campaign | Job |
|----------|-----|
| Launch 40 | Quality last-mile practice (timed / PBQ / after-study / college) |
| Dump Intercept | Top-of-page on dump / PDF-dump queries → redirect to legitimate prep |

---

## Policy (hard)

**Bid on** dump intent. **Do not sell or promise dumps.**

Never in RSA / extensions / display path:
- “dumps”, “braindump”, “real exam”, “actual exam”, “pass guaranteed”

Always say: browser practice · not a PDF · verified bank · timed sim

---

## Campaign shell

| Setting | Value |
|---------|-------|
| Name | `Security+ SY0-701 · US Search · Dump Intercept` |
| Type | Search only |
| Daily budget | **$10–15** to start (do not steal Launch 40’s $35) |
| Bidding | **Target impression share** |
| Location of presence | **Top of results page** |
| Target IS | **60%** (start; raise to 70% only if CPC stays sane) |
| Max CPC bid limit | **$5.00** (raise to $6–7 only if missing auctions) |
| Geo | US only · Presence |
| Language | English |
| Networks | Partners Off · Display Off · AI Max Off |
| Primary conversion | GA4 `begin_checkout` |
| utm_campaign | `secplus_portal_dump_intercept` |
| utm_content | `dump-intercept` |

**Kill rule:** After **$75–100** with **0 `begin_checkout`**, pause and review search terms / RSA / landing before more spend.

---

## Ad groups (1 at launch)

| Ad group | `utm_content` | Display path |
|----------|---------------|--------------|
| Dump Alternative | `dump-intercept` | `Security+` / `Not-A-Dump` |

Optional later split: `601 Dump Legacy` vs `PDF Dump Packs` if volume justifies.

Final URL:

```text
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal_dump_intercept&utm_content=dump-intercept
```

---

## Keywords

Exact match only — see [[Sec+ Dump Intercept Keyword Lists]].

**Do not** add Broad. **Do not** put these dump terms as campaign negatives on this campaign.

Launch 40 can keep dump terms **off** its negatives (already loosened) or leave them out of Launch 40 positives so spend stays in this campaign.

---

## Negatives (campaign level)

Block non-Sec+ and course/cheat-adjacent waste (not the dump stems you bid on):

```
ccna
ccnp
cissp
a+
network+
pmp
udemy
bootcamp
messer
"professor messer"
"jason dion"
"dion training"
jobs
salary
hiring
voucher
torrent
cheat
cheating
"actual exam"
"real exam questions"
```

---

## Week 1 ops

1. Search terms daily → negate junk (other certs, jobs, torrents)
2. Do not change Target IS % for 3 days unless CPC blows past $7 with no clicks
3. Compare `begin_checkout` rate vs Launch 40 — expect lower CTR quality; judge on checkout, not vanity top IS

---

## Build order

1. [[Sec+ Dump Intercept Build Checklist]]
2. Paste keywords [[Sec+ Dump Intercept Keyword Lists]]
3. Paste RSA [[Sec+ Dump Intercept RSA Copy]]
4. Enable · watch first $50 closely

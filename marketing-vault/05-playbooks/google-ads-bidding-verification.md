---
type: playbook
status: active
tags:
  - google-ads
  - bidding
  - verification
  - security-plus
created: 2026-06-01
related:
  - ../01-strategy/google-ads-bidding-strategy.md
  - ../02-campaigns/security-plus/security-plus-google-ads-export.md
---

# Google Ads — verify bidding & budget (step by step)

Use this checklist **after** you create or edit a campaign in the Google Ads UI (or Google Ads Editor). It matches the current vault defaults: **Security+ only**, **$10/day**, **Maximize clicks** with a **max CPC cap**.

Strategy context: [[../01-strategy/google-ads-bidding-strategy|bidding strategy]] · Paste-ready copy: [[../02-campaigns/security-plus/security-plus-google-ads-export|Security+ export]]

**Time:** ~20 minutes first pass · ~10 minutes on weekly review.

---

## Before you open the campaign

Complete these once per account (or confirm they are still true):

| Step | Where in Google Ads | Expected |
|------|---------------------|----------|
| 1 | **Goals → Conversions → Summary** | GA4 property **linked** to this Ads account |
| 2 | Same screen | **`generate_lead`** imported from GA4 — status **Active** (not “No recent conversions” forever if site tested) |
| 3 | Same screen | **`begin_checkout`** imported — **Active** |
| 4 | Optional | **Purchase** conversion from Stripe / `google-ads-purchase-conversion.js` — **Secondary** or Primary when ready |
| 5 | **Admin → Account settings → Auto-apply** (or Recommendations settings) | Turn **off** auto-apply for **budget** and **bidding** changes until you review manually |
| 6 | [[../setup/marketing-stack-setup-checklist#3d — First Security+ campaign\|marketing stack checklist]] | Site fires `generate_lead` on email submit at `#secplus-lead-capture` |

If conversions are not linked, **stop** — bidding will optimize toward clicks only and you cannot verify strategy later.

---

## Part 1 — Account & campaign list

### 1.1 Only Security+ should spend (launch)

1. Go to **Campaigns** → **Campaigns** (table view).
2. Confirm:

| Campaign | Status | Daily budget |
|----------|--------|--------------|
| `SEC+ SY0-701 · Exam prep · becertifiedtoday` (or your exact name) | **Enabled** | **$10.00** |
| CCNA / ENCOR campaigns | **Paused** or **not created** | — |

3. **Filter** status = Enabled — you should see **one** Search campaign spending.

### 1.2 Campaign type & networks

1. Click the **Security+** campaign name.
2. Left menu → **Settings** → **Campaign settings** (or **Settings** tab).
3. Verify:

| Setting | Correct value | Wrong (fix it) |
|---------|---------------|----------------|
| Campaign type | **Search** | Performance Max, Display, Video |
| Networks | **Search Network** only | Search partners ✓ (leave **off** at launch) |
| Networks | Display Network | **Off** |
| Locations | **United States** (or your chosen target) | All countries |
| Languages | **English** | All languages |
| EU political ads | Declared if prompted | — |

---

## Part 2 — Budget (daily cap)

1. **Campaigns** → select Security+ campaign.
2. Open **Budget** (column) or **Settings → Budget**.
3. Verify:

| Field | Expected |
|-------|----------|
| Budget type | **Daily** |
| Amount | **$10.00** per day |
| Shared budget | **None** (dedicated budget for this campaign) |
| Monthly spend cap (if set at account level) | ≥ $300/mo or unset — must not block $10/day |

4. Note the **recommended budget** warning — you can ignore it at $10/day if intentional.

**Optional accelerate:** If you chose **$20–30/day** on Security+ only ([[../01-strategy/google-ads-bidding-strategy#Launch sequence — Security+ first|launch sequence]]), only the **amount** changes; rest of this doc stays the same.

---

## Part 3 — Bidding strategy (most important)

### 3.1 Open bidding settings

Path (UI labels vary slightly):

**Campaigns → [Security+ campaign] → Settings → Budget, bidding, and ad rotation → Bidding**

Or: **Campaigns → [campaign] → Goals / Bidding** card → **Change bid strategy**.

### 3.2 Strategy type

| Check | Expected at launch ($10/day) |
|-------|------------------------------|
| Bid strategy | **Maximize clicks** (may show as “Maximize clicks” under “Clicks”) |
| **Not** at launch | Target CPA, Target ROAS, Maximize conversions, Maximize conversion value, Target impression share, Manual CPC (unless you have a documented test) |

### 3.3 Maximum CPC bid limit (required)

With **Maximize clicks**, Google must have a ceiling or spend can spike on one expensive click.

| Check | Expected (Security+ launch) |
|-------|----------------------------|
| **Maximum CPC bid limit** | **Enabled** — **$2.50** (live 2026-06-03) · vault default was $3.25 |
| If field is missing | Switch strategy to Maximize clicks again; expand **Advanced options** |

**Vault caps when you add other products later:**

| Product | Max CPC cap |
|---------|-------------|
| Security+ | **$2.50** (2026-06-03) · up to **$2.75–3.25** if clicks &lt; 3/day |
| CCNA | **$2.75** |
| ENCOR | **$2.25** |

### 3.4 Portfolio bid strategies

1. **Tools → Shared library → Bid strategies** (or **Campaigns → Bid strategies**).
2. Confirm Security+ is **not** tied to a portfolio that overrides with Target CPA / Target IS unless you created one on purpose.

### 3.5 Ad rotation

**Settings → Ad rotation:** **Optimize: Prefer best performing ads** (default) is fine.

---

## Part 4 — Ad groups (what receives bids)

### 4.1 Enabled ad groups only

1. **Campaigns → Ad groups** (filter by Security+ campaign).
2. **Current launch (2026-06-03):** only **one** ad group **Enabled**:

| Ad group | Status | Role |
|----------|--------|------|
| `secplus_lead_free_sim` | **Enabled** | Free 35-min sim → `generate_lead` — [[../02-campaigns/security-plus/secplus-lead-free-sim-ad-group|config]] |
| `secplus_sim_purchase` | **Paused** | Open after ≥5 leads |

3. **Pause** until week 3+ (if they exist in the account):

- `secplus_portal_access` (or portal / 30-day group)
- `secplus_openssl_pbq` (separate campaign `secplus_openssl_pbq` — keep **paused** at launch)
- Federal / geo duplicate ad groups

### 4.2 No ad group overrides breaking strategy

1. Click each **enabled** ad group → **Settings** or **Ad group settings**.
2. Confirm:

| Setting | Expected |
|---------|----------|
| Ad group bid strategy | **Use campaign bidding strategy** (not custom Target CPA / Manual CPC per group) |
| CPC bid (Manual) | Empty or N/A when campaign uses Maximize clicks |

### 4.3 Final URLs (message match — affects Quality Score, not bid type)

| Ad group | Final URL must contain |
|----------|-------------------------|
| `secplus_lead_free_sim` | `comptia-sec+-home.html#secplus-lead-capture` + `utm_campaign=secplus_portal` + `utm_content=lead-free-sim` |
| `secplus_sim_purchase` | `…#purchase` + `utm_content=sim-purchase` |

Full URLs: [[../02-campaigns/security-plus/security-plus-google-ads-export#Ad group 1 — `secplus_lead_free_sim` (launch first)|Security+ export]].

---

## Part 5 — Keywords & negatives (bid efficiency)

### 5.1 Keyword count at launch

In each **enabled** ad group → **Keywords**:

- Use **3–5 Exact** `[bracket]` Tier 1 terms first, e.g.:
  - `[sy0-701 practice test]`
  - `[comptia security+ practice test]`
  - `[sy0-701 practice exam]`
- Add **Phrase** `"quotes"` only after Exact shows impressions.

Do **not** paste the full export keyword list on day one at $10/day — Google will spread bids too thin.

### 5.2 Match types

| OK at launch | Wait |
|--------------|------|
| **Exact** | Broad match |
| **Phrase** (few) | Broad match modified (legacy) |

### 5.3 Campaign negatives

**Campaign → Keywords → Negative keywords → Campaign level**

Paste Phrase negatives from [[../02-campaigns/security-plus/security-plus-google-ads-export#Campaign-level negative keywords (Phrase match)|export]] (`"free course"`, `"udemy"`, `"pdf download"`, etc.).

### 5.4 Confirm you are not bidding course intent

**Campaign → Insights → Search terms** (after 48h). If you see `course`, `training`, `bootcamp`, `messer` → add as **campaign negative** (Phrase).

---

## Part 6 — Conversions & bidding goal alignment

1. **Goals → Conversions → Settings** (campaign-level) or **Campaign → Goals**.
2. For launch with **Maximize clicks**, Google may show **“Account-default”** conversions — that is OK for week 1.
3. Still verify imports exist (Part 0) so when you switch to **Maximize conversions** later, actions are ready.

| Conversion action | Use when you upgrade bidding |
|-------------------|------------------------------|
| `generate_lead` | Primary for `secplus_lead_free_sim` |
| `begin_checkout` | Primary for `secplus_sim_purchase` |
| Purchase | Primary when purchase volume justifies Target CPA |

**Do not** enable **Target CPA** or **Maximize conversions** on day one at **$10/day** unless you already have 15+ conversions/month on that action — Google will throttle impressions.

---

## Part 7 — Smoke test (same day as launch)

| # | Action | Pass criteria |
|---|--------|---------------|
| 1 | **Ads preview and diagnosis** → search `sy0-701 practice test` | Your ad can show; no policy disapproval |
| 2 | Click live ad (or use **Ad preview** with final URL) | Lands on `comptia-sec+-home.html` with UTMs |
| 3 | Submit test email on lead form | GA4 DebugView or Realtime: `generate_lead` |
| 4 | Click purchase CTA (no need to pay) | `begin_checkout` in GA4 |
| 5 | **Campaign → Status** | No “Limited by budget” **and** “Limited by bid strategy” on day 1 (budget limit alone is OK) |

---

## Part 8 — 48-hour bidding health check

1. **Campaign → Columns** → add:
   - **Search top impression rate**
   - **Search abs. top impression rate**
   - **Avg. CPC**
   - **Cost**
   - **Clicks**
2. Compare to expectations at $10/day:

| Metric | Rough expected (Security+) |
|--------|----------------------------|
| Cost (2 days) | ≤ ~$22 (some days underspend) |
| Clicks (2 days) | ~4–8 total |
| Avg. CPC | ≤ **$3.25** (should hit your cap rarely) |
| Search top IS | Any % > 0 on Exact heroes is fine at $10 |

3. **Auction insights** (Campaign → Insights → Auction insights):
   - Competitors on **practice test** terms are often practice sites, not only course vendors.
   - If **Impression share** is mostly **lost to budget** → normal at $10; raise budget before raising CPC cap.

4. **Recommendations** tab — **Decline** auto-applied changes to:
   - Switch to Target CPA / Maximize conversions
   - Remove max CPC limit
   - Increase budget 2× (review manually)

---

## Part 9 — Weekly bidding verification (10 min)

Add to [[weekly-review-process|weekly marketing review]]:

| Check | Action if wrong |
|-------|-----------------|
| Bid strategy still **Maximize clicks** + cap **$3.25** | Revert; see Part 3 |
| Daily budget still **$10** | Reset; check auto-apply |
| Only 2 ad groups **Enabled** | Pause extras |
| Avg. CPC creeping to cap every click | Add negatives or tighten to Exact only — do not raise cap until Search top IS &lt; 30% **and** you need rank |
| Search terms polluted | Negatives + pause Broad |
| CCNA/ENCOR still **Paused** | Intentional until Sec+ baseline |

Log decisions in the weekly report **## Decisions** section.

---

## Part 10 — When you change bidding (scale gates)

Only move to the next phase when **all** are true:

| Gate | Threshold |
|------|-----------|
| Runtime | ≥ **14 days** live |
| Conversions | ≥ **15–30** `generate_lead` and/or `begin_checkout` in 30 days |
| Budget ready | **≥ $20/day** on Security+ |

### Phase B — Maximize conversions + Target CPA

1. **Campaign → Bidding** → change to **Maximize conversions**.
2. Set **Target CPA** (optional): lead **$4–7**, sim **$8–12** ([[../01-strategy/google-ads-bidding-strategy#Phase 2 — After 30+ conversions / product (efficiency)|bidding strategy]]).
3. **Campaign → Goals** → set **conversion action** priority: lead group → `generate_lead`; purchase group → `begin_checkout`.

### Phase C — Target impression share (top placement)

Only when budget **≥ $20–25/day** **and** you split or dedicate budget to hero keywords:

1. Create campaign **`SEC+ · Tier1 · Visibility`** (or duplicate heroes).
2. Bid strategy: **Target impression share** → **Top of page** → **75%**.
3. Set **maximum CPC bid limit** ≈ 120% of your 14-day average CPC on heroes.
4. Keep **Convert** campaign on Maximize conversions / Target CPA.

Details: [[../01-strategy/google-ads-bidding-strategy#At **$20–25+/day per product** (scale — split optional)|campaign architecture — scale]].

---

## Appendix A — CCNA / ENCOR (when you enable later)

Repeat **Parts 1–9** per campaign with these substitutions:

| Setting | CCNA | ENCOR |
|---------|------|-------|
| Daily budget (solo) | $10 | $10 |
| Max CPC cap | **$2.75** | **$2.25** |
| Lead ad group | `ccna_lead_free_sim` | `encor_lead_free_sim` |
| Purchase ad group | `ccna_sim_purchase` | `encor_sim_purchase` |
| UTM campaign | `ccna_portal` | `encor_portal` |
| Export | [[../02-campaigns/ccna/ccna-portal-google-ads-export\|CCNA export]] | [[../02-campaigns/encor/ccnp-encor-google-ads-export\|ENCOR export]] |

### Ad groups — active vs paused at start (same pattern as Security+)

Enable **only two** ad groups per campaign for the first **2–3 weeks** at $10/day. Pause the rest so budget concentrates on practice-test / simulation intent.

| Ad group | CCNA | ENCOR | At start |
|----------|------|-------|----------|
| Lead free timed sim | `ccna_lead_free_sim` | `encor_lead_free_sim` | **Enabled** |
| Paid timed sim ($9.99) | `ccna_sim_purchase` | `encor_sim_purchase` | **Enabled** |
| Portal 10d / 30d access | `ccna_portal_access` | `encor_portal_access` | **Paused** |
| Labs / drag-and-drop / PBQ | `ccna_labs_pbq` | `encor_labs_pbq` | **Paused** |
| Federal / geo metro | `ccna_federal_dc` (+ copies) | `encor_federal_dc` (+ copies) | **Paused** |

**Enable next (one at a time, after heroes have clicks + conversions):**

1. **`_*_labs_pbq`** — when search terms or site data show lab/D&D intent; overlaps purchase funnel but different keywords.
2. **`_*_portal_access`** — when you want to push $19.99 portal, not only $9.99 sim (watch CPA).
3. **`_*_federal_*` geo groups** — when budget ≥ **$20/day** and you target Tier 1 metros ([[../01-strategy/cisco-certifications-exam-prep-foundation#Shared geo ad groups|Cisco geo table]]).

**Before CCNA/ENCOR launch:** complete [[../06-website-optimization/ad-site-verification-2026-05-31|ad-site verification]] — exports must match live lead URLs (`#ccna-lead-capture` / `#encor-lead-capture`) and **$9.99** sim pricing.

---

## Appendix B — Quick copy-paste checklist

```
PRE-LAUNCH
[ ] GA4 linked; generate_lead + begin_checkout Active in Ads
[ ] Auto-apply budget/bidding OFF

CAMPAIGN (Security+)
[ ] Status: Enabled
[ ] Type: Search only (no Display; no Search partners at launch)
[ ] Location: United States · Language: English
[ ] Daily budget: $10.00 (not shared)

BIDDING
[ ] Strategy: Maximize clicks
[ ] Maximum CPC bid limit: $3.25
[ ] NOT: Target CPA / Maximize conversions / Target IS / Manual CPC

AD GROUPS
[ ] Enabled: secplus_lead_free_sim, secplus_sim_purchase
[ ] Paused: portal, openssl PBQ, federal/geo extras
[ ] Ad groups use campaign bidding (no per-group override)

KEYWORDS
[ ] 3–5 Exact Tier 1 per enabled ad group
[ ] Campaign negatives pasted (Phrase)
[ ] No Broad match at launch

POST-LAUNCH (48h)
[ ] 4–8 clicks in 2 days; avg CPC ≤ $3.25
[ ] Search terms: no course/training/dump bleed
[ ] generate_lead / begin_checkout fire on site test
[ ] CCNA + ENCOR campaigns Paused
```

---

## Related

- [[../01-strategy/google-ads-bidding-strategy|Bidding strategy]]
- [[../02-campaigns/security-plus/security-plus-google-ads|Security+ campaign note]]
- [[../06-website-optimization/google-ads-quality-score-guide|Quality Score guide]]
- [[keyword-collection-plan|Keyword collection plan]]

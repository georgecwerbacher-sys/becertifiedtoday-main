---
type: playbook
status: active
product: secplus-sy0-701
updated: 2026-06-03
---

# Security+ free 35-minute sim — funnel playbook

Active Google Ads ad group: **`secplus_lead_free_sim`** only. Paid upsell: **$19.99 / 30-day** on `#purchase`.

Related: [[security-plus-lead-magnet-ads|Lead magnet ads]] · [[google-ads-manual-data-import|Manual Ads data]] · [[../06-website-optimization/pages/comptia-sec-plus-home|Landing page note]]

---

## Offer (live site)

| Step | User action | GA4 |
|------|-------------|-----|
| Ad click | Lands `#secplus-lead-capture` + `utm_content=lead-free-sim` | Session + UTM |
| Start free sim | **No email** on landing — tap CTA | `secplus_free_sim_start` + **`generate_lead`** (`lead_type: free_sim_start`) |
| During sim | 35 min, 20 MCQ + 1 PBQ | Engagement |
| Finish | On-screen scorecard | — |
| Optional email | Results → **Email my scorecard** | `secplus_scorecard_email_sent` + **`generate_lead`** (`lead_type: scorecard_email`) |
| Upsell | Results modal or `#purchase` | `begin_checkout` → Stripe |

Runner: `/COMP_TIA_SEC+/test-simulation-runner.html?free=1`

---

## Google Ads setup (you paste in UI)

**Final URL:**

```
https://becertifiedtoday.com/comptia-sec+-home.html#secplus-lead-capture?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=lead-free-sim
```

**Primary conversion:** import GA4 **`generate_lead`** (fires on free sim **Start** click, not only scorecard email).

**Secondary:** `secplus_scorecard_email_sent`, `begin_checkout`, purchase.

**Do not** blanket-negate `free` — you target free practice test intent.

**Campaign negatives:** paste block in [[../02-campaigns/security-plus/security-plus-google-ads-export#Campaign-level negative keywords (Phrase match)|Google Ads export]] + [[../07-keywords/negatives/master-negative-list|master list]] (`dumps`, `dion`, `cysa`, etc.).

---

## RSA copy (aligned to site — no email gate)

**Headlines:** Free Security+ Timed Sim · Start Free SY0-701 Sample · 35-Min Practice + Scorecard · No Email To Start · Exam Prep Not a Course

**Descriptions (≤90 chars):**

```
Free 35-min SY0-701 sample: 20 MCQ + PBQ. Domain scorecard. No email to start.
Timed practice before test day. Back & mark for review. 30-day access when ready.
Exam prep—not a course. Verified explanations. No PDF dumps. Browser-only.
```

**Avoid:** “Email unlock”, “Enter email to start” (outdated).

---

## Site behavior (2026-06-03)

- **Lead-first layout:** free sim block **above** compact intro when `utm_content=lead-free-sim` or `#secplus-lead-capture`
- **Scroll + focus** primary CTA on ad landings
- **Mobile sticky bar:** “Start free 35-min simulation” when main CTA scrolls off screen
- **Purchase** stays below lead block; single **$19.99** CTA

---

## Weekly review

1. Ads export → [[google-ads-manual-data-import]]
2. GA4: `generate_lead` count vs clicks (`utm_campaign=secplus_portal`)
3. `marketing-vault/leads/secplus-free-simulation-leads.csv` (scorecard emails if API enabled)
4. Hold **$10/day** until **~5** `generate_lead` from free sim starts

---

## Do not (yet)

- Open `secplus_sim_purchase` ad group
- Coupon-led RSAs
- Remove free sim to simplify page

## Ads config (complete in vault)

See [[../02-campaigns/security-plus/secplus-lead-free-sim-ad-group|secplus_lead_free_sim — checklists]] for checked-off campaign/ad group setup.

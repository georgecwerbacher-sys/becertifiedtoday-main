---
type: ad-group
channel: google-ads
campaign: SEC+ SY0-701 · Exam prep · becertifiedtoday
ad_group: secplus_lead_free_sim
status: enabled
daily_budget_campaign_usd: 10
max_cpc_usd: 2.50
bidding: maximize-clicks
utm_campaign: secplus_portal
utm_content: lead-free-sim
configured_as_of: 2026-06-03
---

# Ad group — `secplus_lead_free_sim`

Single active paid ad group for Security+ launch. Parent: [[security-plus-google-ads|Security+ Google Ads]] · Funnel: [[../../05-playbooks/secplus-free-sim-funnel|Free sim funnel]] · Negatives: [[../../07-keywords/negatives/google-ads-applied-2026-06-03|Applied negatives snapshot]]

## Live settings (confirmed 2026-06-03)

| Setting | Value |
|---------|--------|
| Campaign status | **Enabled** |
| Ad group status | **Enabled** (only spending group) |
| Daily budget | **$10.00** (campaign) |
| Bidding | **Maximize clicks** |
| Max CPC bid limit | **$2.50** |
| Primary conversion (target) | GA4 **`generate_lead`** (free sim Start + scorecard email) |
| Landing | [[../../06-website-optimization/pages/comptia-sec-plus-home|comptia-sec+-home.html]] `#secplus-lead-capture` |
| Paid upsell on site | **$19.99 / 30-day** only (`#purchase`) |

**Final URL:**

```
https://becertifiedtoday.com/comptia-sec+-home.html#secplus-lead-capture?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=lead-free-sim
```

---

## Campaign setup checklist

- [x] Campaign **Enabled** — Security+ only
- [x] Daily budget **$10/day**
- [x] Bidding **Maximize clicks** + max CPC **$2.50**
- [x] Campaign negatives **32 Phrase** (campaign level only) — [[../../07-keywords/negatives/google-ads-applied-2026-06-03|list]]
- [x] Ad group negatives **none** (do not duplicate at ad group)
- [x] CCNA / ENCOR campaigns **Paused** or not spending
- [x] `secplus_sim_purchase` and other Sec+ ad groups **Paused** (lead group only)
- [ ] GA4 **`generate_lead`** marked key event + imported **Primary** in Google Ads
- [ ] **≥5** `generate_lead` in 7 days before budget bump

---

## Ad group setup checklist

- [x] Ad group **Enabled**: `secplus_lead_free_sim`
- [x] Final URL with `#secplus-lead-capture` + `utm_content=lead-free-sim`
- [x] RSA copy aligned (free sim, no email to start) — [[security-plus-lead-magnet-ads|lead magnet ads]]
- [x] Site: guest free sim + `generate_lead` on Start — prod deploy 2026-06-03
- [x] Site: lead-first layout + sticky mobile CTA for ad traffic
- [x] Site: post-sim upsell **$19.99 / 30-day**
- [ ] Positive keywords trimmed to **target 6–8** (see below) — verify in next export
- [ ] Search terms review **7 days** after negatives (re-export CSV)

---

## Positive keywords — target list (ad group)

Paste at ad group level; remove all others.

**Exact `[...]`**

```
[comptia security+ practice test]
[sy0-701 practice test]
```

**Phrase `"..."`**

```
"security+ mock exam"
"security+ practice test"
"security+ practice questions"
"security+ exam prep"
```

Optional 6th Phrase: `"sy0-701 mock exam"` (pause if 0 clicks after 7 days).

**Do not use:** Phrase duplicates of Exact (`"comptia security+ practice test"`, `"sy0-701 practice test"`).

Report baseline: [[../../03-reports/ads-imports/2026-06-03-search-keywords-secplus_lead_free_sim|keyword report May 31–Jun 3]]

---

## Performance baseline (May 31 – Jun 3, 2026)

| Metric | Value |
|--------|------:|
| Spend | $33.23 |
| Clicks | 17 |
| CTR | 8.90% |
| Conversions (Ads) | 1 |
| CPA | $33.23 |
| Best keyword | `"security+ mock exam"` — 1 conv., $9.90 |

Weekly snapshot: [[../../03-reports/weekly/2026-06-03|2026-06-03 weekly]]

---

## Negatives (campaign only — not ad group)

32 Phrase negatives — full paste block in [[../../07-keywords/negatives/google-ads-applied-2026-06-03#Campaign negatives only — Phrase `"..."` (32)|applied snapshot]].

---

## Next actions (open)

- [ ] Confirm keyword count = **6–8** in Ads UI
- [ ] GA4 Realtime: click **Start free timed simulation** → see `generate_lead`
- [ ] Google Ads → Conversions → `generate_lead` **Primary** for this campaign
- [ ] Week of 2026-06-10: new **Search terms** + **Search keyword** CSV → [[../../05-playbooks/google-ads-manual-data-import|manual import]]
- [ ] If ≥5 leads and clean terms → budget **$15/day** (max CPC stay **$2.50** or **$2.75**)

---

## Decisions log

| Date | Decision |
|------|----------|
| 2026-06-03 | Launch **lead ad group only**; hold purchase ad groups |
| 2026-06-03 | Max CPC **$2.50** (was vault $3.25) on **$10/day** |
| 2026-06-03 | Campaign negatives consolidated; ad group negatives removed |
| 2026-06-03 | Trim positives to 6–8; drop Exact/Phrase duplicates |
| 2026-06-03 | Single paid CTA **$19.99**; free 35-min sim remains ad focus |

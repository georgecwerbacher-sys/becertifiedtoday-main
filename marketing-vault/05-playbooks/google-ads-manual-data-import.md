---
type: playbook
status: active
channel: google-ads
updated: 2026-06-03
---

# Google Ads — manual data for Cursor / weekly review

**Decision:** No Google Ads API for now. You export from the UI (or zip Overview cards); paste in chat or save under `03-reports/ads-imports/`.

Parent: [[weekly-review-process|Weekly review process]] · Campaign: [[../02-campaigns/security-plus/security-plus-google-ads|Security+ Google Ads]] · Funnel: [[secplus-free-sim-funnel|Free sim funnel]]

---

## When to send data

| Cadence | What |
|---------|------|
| **Weekly** (15 min) | Overview cards zip **or** Search terms report (last 7 days) |
| **After a big change** | Same + note what changed (budget, negatives, RSA) |
| **When spend spikes / 0 conv.** | Search terms + GA4 note (sessions vs clicks on that day) |

---

## What to export (minimum)

1. **Overview cards** (date range = last 7 days) → zip like `Overview_cards_csv(YYYY-MM-DD).zip`  
   Covers: time series, keywords, search terms, devices.

2. **Optional but high value:**  
   - **Search terms** report (all columns) if not in zip  
   - Screenshot or paste: **Conversions** column header (confirm primary action = lead)

---

## Where to put files (optional)

```
marketing-vault/03-reports/ads-imports/YYYY-MM-DD-overview.zip
```

Or attach zip in Cursor chat and say: *“weekly ads review”*.

---

## What to paste in chat (if no file)

```
Date range:
Daily budget:
Active ad groups:
Spend / clicks / impressions / conversions:
Anything you changed this week:
Question for review (e.g. negatives, Jun 2 clicks):
```

---

## What Cursor will do with it

- Update [[../03-reports/weekly/|weekly report]] notes and [[../07-keywords/negatives/master-negative-list|negatives]]
- Compare to GA4 when `npm run marketing:weekly-report` is run
- Recommend hold/split budget only after ~5 leads on `secplus_lead_free_sim`

---

## GA4 complement (same week)

```bash
npm run marketing:weekly-report
```

Fills funnel metrics; Ads export does **not** replace this.

---

## Do not send

- Google account password  
- Full account API keys in chat  
- Card/billing details  

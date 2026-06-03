---
type: keyword-verification
campaign: SEC+ SY0-701 · Exam prep · becertifiedtoday
status: active
created: 2026-06-03
---

# Security+ — keyword verification checklist

Use this to compare **Google Ads UI** vs vault. Path: **Campaigns →** `SEC+ SY0-701 · Exam prep · becertifiedtoday`.

| Level | What to open | Good (positive) keywords | Negative keywords |
|-------|----------------|--------------------------|-------------------|
| **Campaign** | Keywords → **Search keywords** | **0** — must be empty | **92** — [[../negatives/google-ads-applied-2026-06-03#Full list — Phrase `"..."` (78) — paste first\|negatives list]] |
| **Campaign** | Keywords → **Negative keywords** | — | Same 92-line block |
| **Ad group** `secplus_lead_free_sim` | Keywords → **Search keywords** | **7** (live) — list below | **0** — must be empty |
| **Other ad groups** | Search keywords | **0** if paused | **0** |

Search campaigns: **positive keywords only on ad groups**, not campaign. If you see positives at campaign level, remove or move to `secplus_lead_free_sim`.

---

## Verify — campaign level

### Search keywords (positives) — expect **NONE**

```
(empty — no lines)
```

### Negative keywords — expect **92** (one per line)

See single block: [[../negatives/google-ads-applied-2026-06-03|google-ads-applied-2026-06-03]] (Phrase + Exact combined).

---

## Verify — ad group `secplus_lead_free_sim` (enabled)

### Search keywords — expect **7** (one per line)

```
[comptia security+ practice test]
[sy0-701 practice test]
"security+ mock exam"
"security+ practice test"
"security+ practice questions"
"security+ exam prep"
"sy0-701 mock exam"
```

Optional: omit `"sy0-701 mock exam"` → **6** keywords if you are running the strict live set.

### Must NOT appear in this ad group

```
"comptia security+ practice test"
"sy0-701 practice test"
"sy0-701 practice exam"
"sy0-701 exam prep"
"security+ timed practice test"
"security+ practice exam"
```

### Negative keywords — expect **NONE** at ad group

```
(empty — negatives are campaign-only)
```

---

## Verify — paused ad groups (expect **0** keywords while paused)

When you enable an ad group, paste the matching block from [[secplus-campaign-positive-keywords#Paused ad groups — paste when enabled|secplus-campaign-positive-keywords]].

| Ad group | Expected positive count when enabled |
|----------|--------------------------------------:|
| `secplus_sim_purchase` | 12 (2 Exact + 10 Phrase) |
| `secplus_portal_access` | 10 Phrase |
| `secplus_openssl_pbq` | 10 (2 Exact + 8 Phrase) |
| `secplus_federal_dc` (etc.) | 12 Phrase per geo group |

---

## Quick UI checks

- [x] Campaign **Search keywords** = empty
- [x] Campaign **Negative keywords** = 92
- [x] `secplus_lead_free_sim` **Search keywords** = 6 or 7 (no Broad)
- [x] `secplus_lead_free_sim` **Negative keywords** = empty
- [x] Paused ad groups have **0** search keywords (or are paused)
- [x] Only one ad group **Enabled** for spend

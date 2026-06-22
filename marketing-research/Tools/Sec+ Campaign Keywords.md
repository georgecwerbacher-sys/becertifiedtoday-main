---
type: tool
product: secplus
tags:
  - marketing
  - google-ads
  - keywords
  - tools
---

# Sec+ Campaign Keywords (tool)

**Purpose:** Paste ranked keywords into Google Ads while building **`Security+ PBQ Practice`** — using the **AdWords checklist CSV** (same workflow as CCNA wedge / portal checklists).

## AdWords checklist (primary)

| File | Role |
|------|------|
| [[../Sec+ Campaign/secplus-campaign-checklist.csv\|secplus-campaign-checklist.csv]] | **Paste from here** — 67 `Add exact/phrase keyword` rows + negatives + RSA |
| [[../Sec+ Campaign/secplus-campaign-checklist-README.txt\|checklist README]] | Numbers setup · column guide |
| [[../Sec+ Campaign/secplus-keywords.csv\|secplus-keywords.csv]] | Edit keyword text here, then regenerate checklist |

### Numbers workflow

1. Open `secplus-campaign-checklist.csv` in Numbers (see README).
2. Filter **Section** = `Setup`, **Phase** = `Ad group` — rows 4–70 are keywords in rank order.
3. For each row, paste **Value** into Google Ads with match type from **Task** (`Add exact keyword` / `Add phrase keyword`).
4. Filter **Phase** = `Negatives` for campaign + ad group negatives.
5. Filter **Section** = `Headline` / `Description` for RSA copy.

## Campaign settings (checklist rows 9–20)

| Setting | Value |
|---------|--------|
| Campaign | `Security+ SY0-701 · Exam prep · becertifiedtoday` |
| Ad group | **`Security+ PBQ Practice`** |
| Budget | **$20.00/day** · max CPC **$2.75** |
| utm_campaign | `secplus_portal` · utm_content `pbq-wedge` |

Full setup: [[../Sec+ Campaign/Sec+ Notes|Sec+ Notes]] · RSA: [[../Sec+ Campaign/Sec+ RSA Copy|Sec+ RSA Copy]]

## Regenerate checklist

After editing [[../Sec+ Campaign/secplus-keywords.csv|secplus-keywords.csv]]:

```bash
npm run sync:secplus-checklist
```

## Reference (docs only)

| File | Role |
|------|------|
| [[../Sec+ Campaign/Sec+ Keywords\|Sec+ Keywords.md]] | Ranked list + strategy notes |
| `public/admin/tools/secplus-keywords.html` | Optional browser copy helper (not the primary workflow) |

[[Tools/README|← Tools]]

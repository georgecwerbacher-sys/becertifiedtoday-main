#!/usr/bin/env python3
"""Sync Sec+ campaign keywords CSV → public/admin/data JSON for the admin keyword tool."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "marketing-research/Sec+ Campaign/secplus-keywords.csv"
OUT_PATH = ROOT / "public/admin/data/secplus-campaign-keywords.json"

CAMPAIGN = {
    "id": "secplus_portal",
    "googleAdsCampaignName": "Security+ SY0-701 · Exam prep · becertifiedtoday",
    "adGroup": "Security+ PBQ Practice",
    "dailyBudgetUsd": 20,
    "maxCpcUsd": 2.75,
    "utmCampaign": "secplus_portal",
    "utmContentPrimary": "pbq-wedge",
    "finalUrl": (
        "https://becertifiedtoday.com/secplus/pbq-practice-browser.html"
        "?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=pbq-wedge"
    ),
    "primaryConversion": "begin_checkout",
    "pinH1": "Security+ PBQ Practice",
    "pinH2": "$9.99 · 10-Day Access",
}


def normalize_keyword(raw: str, match_type: str) -> str:
    text = (raw or "").strip()
    if match_type == "Exact":
        inner = text.strip("[]")
        return f"[{inner}]"
    if match_type == "Phrase":
        inner = text.strip('"')
        return f'"{inner}"'
    if match_type == "Broad":
        return text.strip('"')
    return text


def main() -> None:
    if not CSV_PATH.is_file():
        raise SystemExit(f"Missing source CSV: {CSV_PATH}")

    keywords = []
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rank_raw = (row.get("Rank") or "").strip()
            rank = int(rank_raw) if rank_raw.isdigit() else None
            match_type = (row.get("Match type") or "").strip()
            level = (row.get("Level") or "").strip()
            keywords.append(
                {
                    "rank": rank,
                    "keyword": normalize_keyword(row.get("Keyword") or "", match_type),
                    "matchType": match_type,
                    "adGroup": (row.get("Ad group") or "").strip(),
                    "level": level,
                }
            )

    positives = [k for k in keywords if k["level"] == "positive"]
    payload = {
        "updatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "sourceCsv": "marketing-research/Sec+ Campaign/secplus-keywords.csv",
        "campaign": CAMPAIGN,
        "counts": {
            "positive": len(positives),
            "negativeCampaign": sum(1 for k in keywords if k["level"] == "negative_campaign"),
            "negativeAdGroup": sum(1 for k in keywords if k["level"] == "negative_adgroup"),
            "total": len(keywords),
        },
        "keywords": keywords,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_PATH} ({payload['counts']['positive']} positives, {payload['counts']['total']} total)")


if __name__ == "__main__":
    main()

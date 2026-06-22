#!/usr/bin/env python3
"""Sync Sec+ keywords CSV → AdWords checklist rows in secplus-campaign-checklist.csv.

Source of truth for keyword text: marketing-research/Sec+ Campaign/secplus-keywords.csv
Checklist format matches scripts/ccna-wedge-lab-google-ads-checklist.csv (Numbers / Google Ads UI).
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KW_CSV = ROOT / "marketing-research/Sec+ Campaign/secplus-keywords.csv"
CHECKLIST_CSV = ROOT / "marketing-research/Sec+ Campaign/secplus-campaign-checklist.csv"
README_TXT = ROOT / "marketing-research/Sec+ Campaign/secplus-campaign-checklist-README.txt"

AD_GROUP = "Security+ PBQ Practice"
UTM = "utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal"
PBQ_LANDING = f"https://becertifiedtoday.com/secplus/pbq-practice-browser.html?{UTM}"
HEADER = ["Done", "Section", "Phase", "Step", "Task", "Value", "Ad group", "Notes"]

KEYWORD_TASKS = {
    ("positive", "Exact"): "Add exact keyword",
    ("positive", "Phrase"): "Add phrase keyword",
    ("negative_campaign", "Exact"): "Campaign negative exact",
    ("negative_campaign", "Phrase"): "Campaign negative phrase",
    ("negative_campaign", "Broad"): "Campaign negative phrase",
    ("negative_adgroup", "Exact"): "Ad group negative exact",
    ("negative_adgroup", "Phrase"): "Ad group negative phrase",
    ("negative_adgroup", "Broad"): "Ad group negative phrase",
}


def checklist_row(
    section: str,
    phase: str,
    step: int,
    task: str,
    value: str = "",
    ad_group: str = "",
    notes: str = "",
) -> list[str]:
    return ["FALSE", section, phase, str(step), task, value, ad_group, notes]


def normalize_keyword(raw: str, match_type: str) -> str:
    text = (raw or "").strip()
    if match_type == "Exact":
        inner = text.strip("[]")
        return f"[{inner}]"
    if match_type in ("Phrase", "Broad"):
        return text.strip('"')
    return text


def static_setup_rows() -> list[list[str]]:
    return [
        checklist_row("Setup", "Pre-launch", 1, "Confirm Stripe secplus-portal-10d live at $9.99"),
        checklist_row("Setup", "Pre-launch", 2, "Confirm Stripe secplus-portal-30d live at $19.99"),
        checklist_row(
            "Setup",
            "Pre-launch",
            3,
            "Test checkout from pbq-practice-browser.html desktop + mobile",
            notes="Verify begin_checkout in GA4",
        ),
        checklist_row(
            "Setup",
            "Pre-launch",
            4,
            "Confirm GA4 begin_checkout for secplus_portal_10d and secplus_portal_30d",
        ),
        checklist_row(
            "Setup",
            "Pre-launch",
            5,
            "Import GA4 begin_checkout as Primary conversion in Google Ads",
        ),
        checklist_row(
            "Setup",
            "Pre-launch",
            6,
            "Verify secplus-home-conversion.js on ?utm_content=pbq-wedge",
        ),
        checklist_row(
            "Setup",
            "Pre-launch",
            7,
            "Verify PBQ landing loads on mobile + desktop",
        ),
        checklist_row(
            "Setup",
            "Campaign",
            1,
            "Create Search campaign",
            "Security+ SY0-701 · Exam prep · becertifiedtoday",
            "Campaign",
        ),
        checklist_row("Setup", "Campaign", 2, "Set daily budget", "$20.00/day", "Campaign"),
        checklist_row(
            "Setup",
            "Campaign",
            3,
            "Turn off Search partners",
            "Off until baseline",
            "Campaign",
        ),
        checklist_row(
            "Setup",
            "Campaign",
            4,
            "Set bidding weeks 1-2",
            "Maximize clicks max CPC $2.75",
            "Campaign",
        ),
        checklist_row("Setup", "Campaign", 5, "Set utm_campaign on all ads", "secplus_portal", "Campaign"),
        checklist_row("Setup", "Campaign", 6, "Set campaign language", "English", "Campaign"),
        checklist_row("Setup", "Locations", 1, "Location option", "Presence only", "Campaign"),
        checklist_row("Setup", "Locations", 2, "Add Tier A countries", "See Extensions.md geo", "Campaign"),
        checklist_row(
            "Setup",
            "Ad group",
            1,
            "Create ad group",
            AD_GROUP,
            AD_GROUP,
            "Only ad group — full $20/day budget",
        ),
        checklist_row(
            "Setup",
            "Ad group",
            2,
            "Set display path",
            "Security+ / PBQ-Practice",
            AD_GROUP,
        ),
        checklist_row(
            "Setup",
            "Ad group",
            3,
            "Set final URL",
            "https://becertifiedtoday.com/secplus/pbq-practice-browser.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=pbq-wedge",
            AD_GROUP,
        ),
    ]


def sitelink_rows() -> list[list[str]]:
    """Campaign sitelinks — link text ≤25 · each description ≤35 (Notes column)."""
    links = [
        (
            "Add sitelink · 10-Day Access · $9.99",
            f"{PBQ_LANDING}&utm_content=sitelink-10d#purchase",
            "Desc1: 34 PBQ scenarios included · Desc2: One payment, no subscription",
        ),
        (
            "Add sitelink · 34 PBQ Scenarios",
            f"{PBQ_LANDING}&utm_content=sitelink-pbq-list",
            "Desc1: Chain labs & hot spots · Desc2: Browser performance prep",
        ),
        (
            "Add sitelink · Timed 90-Min Sim",
            f"{PBQ_LANDING}&utm_content=sitelink-sim#purchase",
            "Desc1: Mixed MCQ and PBQ run · Desc2: Domain scorecard included",
        ),
        (
            "Add sitelink · Try PBQ Sample",
            f"https://becertifiedtoday.com/secplus-sample?track=sim-dark-web&{UTM}&utm_content=sitelink-pbq",
            "Desc1: Dark web IR scenario · Desc2: Browser preview, no download",
        ),
        (
            "Add sitelink · 30-Day Access · $19.99",
            f"{PBQ_LANDING}&utm_content=sitelink-30d#purchase",
            "Desc1: Best value study window · Desc2: Full portal + timed sim",
        ),
        (
            "Add sitelink · Scorecard & Review",
            f"{PBQ_LANDING}&utm_content=sitelink-scorecard",
            "Desc1: Timed sim + weak domains · Desc2: Adaptive review modes",
        ),
    ]
    return [
        checklist_row("Setup", "Extensions", i, task, url, "Campaign", notes)
        for i, (task, url, notes) in enumerate(links, start=1)
    ]


def launch_rows() -> list[list[str]]:
    return [
        checklist_row(
            "Setup",
            "Launch",
            1,
            "Click each sitelink — confirm PBQ landing or sample loads",
            "",
            "Campaign",
            "Stay on pbq-practice-browser or secplus-sample",
        ),
        checklist_row(
            "Setup",
            "Launch",
            2,
            "Test all 6 sitelinks on mobile",
            "",
            "Campaign",
        ),
        checklist_row(
            "Setup",
            "Launch",
            3,
            "Click $9.99 checkout from PBQ landing — confirm Stripe",
            "",
            AD_GROUP,
        ),
        checklist_row(
            "Setup",
            "Launch",
            4,
            "Confirm GA4 begin_checkout in Realtime",
            "",
            "Campaign",
            "secplus_portal_10d or secplus_portal_30d",
        ),
    ]


def rsa_rows() -> list[list[str]]:
    headlines = [
        ("Security+ PBQ Practice", "Pin H1 · 24 chars"),
        ("$9.99 · 10-Day Access", "Pin H2 · 22 chars"),
        ("Am I Ready? · Scorecard", "Primary job · 22 chars"),
        ("Ready Before You Sit · SY0-701", "28 chars"),
        ("Interactive PBQ Prep", "20 chars"),
        ("34 PBQ Scenarios Prep", "21 chars"),
        ("Timed 90-Min Exam Sim", "21 chars"),
        ("Detailed Scorecard Review", "25 chars"),
        ("SY0-701 PBQ in Browser", "22 chars"),
        ("No Download · Browser PBQ", "25 chars"),
        ("Chain Labs & Hot Spots", "22 chars"),
        ("Cert Required for Job", "21 chars"),
        ("DoD 8140-Aligned Prep", "21 chars"),
        ("Not a PDF · Live Scenarios", "26 chars"),
        ("Adaptive Review Modes", "21 chars"),
    ]
    descriptions = [
        "Practice SY0-701 PBQs in browser—chain labs, drag-drop, IR scenarios. Scorecard included.",
        "90-min timed sim + scorecard. $9.99/10d unlocks 34 PBQs and 1000+ questions. One payment.",
        "Cert required for work? Interactive PBQ prep in browser—not a $99 PDF dump or course.",
        "One payment—no subscription. Adaptive review on phone, tablet, or desktop.",
    ]
    rows: list[list[str]] = []
    step = 4
    for text, notes in headlines:
        rows.append(
            checklist_row("Headline", AD_GROUP, step, "RSA headline", text, AD_GROUP, notes)
        )
        step += 1
    step = 1
    for text in descriptions:
        rows.append(
            checklist_row(
                "Description",
                AD_GROUP,
                step,
                "RSA description",
                text,
                AD_GROUP,
                f"{len(text)} chars",
            )
        )
        step += 1
    return rows


def ops_rows() -> list[list[str]]:
    return [
        checklist_row("Ops", "Week 1", 1, "Day 1 confirm ads serving + GA4 checkout", "", "Campaign"),
        checklist_row("Ops", "Week 1", 2, "Day 3 search terms review add negatives", "", "Campaign"),
        checklist_row(
            "Ops",
            "Week 1",
            3,
            "Day 7 CPA review hold $20/day or tune max CPC",
            "",
            "Campaign",
        ),
    ]


def load_keywords() -> list[dict[str, str]]:
    if not KW_CSV.is_file():
        raise SystemExit(f"Missing keyword CSV: {KW_CSV}")
    rows: list[dict[str, str]] = []
    with KW_CSV.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


def keyword_rows(keywords: list[dict[str, str]]) -> tuple[list[list[str]], list[list[str]], list[list[str]]]:
    positives: list[list[str]] = []
    campaign_negs: list[list[str]] = []
    adgroup_negs: list[list[str]] = []

    positives_sorted = sorted(
        [k for k in keywords if (k.get("Level") or "").strip() == "positive"],
        key=lambda k: int((k.get("Rank") or "0").strip() or 0),
    )
    for i, row in enumerate(positives_sorted, start=1):
        match_type = (row.get("Match type") or "").strip()
        task = KEYWORD_TASKS[("positive", match_type)]
        value = normalize_keyword(row.get("Keyword") or "", match_type)
        rank = (row.get("Rank") or "").strip()
        positives.append(
            checklist_row(
                "Setup",
                "Ad group",
                3 + i,
                task,
                value,
                AD_GROUP,
                f"Rank {rank}" if rank else "",
            )
        )

    post_kw_step = 3 + len(positives_sorted)
    positives.append(
        checklist_row(
            "Setup",
            "Ad group",
            post_kw_step + 1,
            "Paste RSA headlines",
            "See Headline rows below",
            AD_GROUP,
            "Pin H1 Security+ PBQ Practice · H2 $9.99 · 10-Day Access",
        )
    )
    positives.append(
        checklist_row(
            "Setup",
            "Ad group",
            post_kw_step + 2,
            "Paste RSA descriptions",
            "See Description rows below",
            AD_GROUP,
        )
    )

    for level, bucket in (
        ("negative_campaign", campaign_negs),
        ("negative_adgroup", adgroup_negs),
    ):
        items = [k for k in keywords if (k.get("Level") or "").strip() == level]
        for i, row in enumerate(items, start=1):
            match_type = (row.get("Match type") or "Phrase").strip()
            task = KEYWORD_TASKS[(level, match_type)]
            value = normalize_keyword(row.get("Keyword") or "", match_type)
            ad_group = "Campaign" if level == "negative_campaign" else AD_GROUP
            bucket.append(checklist_row("Setup", "Negatives", i, task, value, ad_group))

    return positives, campaign_negs, adgroup_negs


def write_checklist(rows: list[list[str]]) -> None:
    CHECKLIST_CSV.parent.mkdir(parents=True, exist_ok=True)
    with CHECKLIST_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        writer.writerows(rows)


def write_readme(positive_count: int, campaign_neg_count: int, adgroup_neg_count: int) -> None:
    README_TXT.write_text(
        f"""Security+ Google Ads — AdWords checklist (Apple Numbers)
============================================================

File: marketing-research/Sec+ Campaign/secplus-campaign-checklist.csv

One campaign · one ad group · $20/day:
  • Setup checklist (pre-launch through negatives)
  • 6 campaign sitelinks (Extensions phase — paste URLs + descriptions)
  • {positive_count} positive keywords (rank order — paste into Google Ads)
  • RSA headlines + descriptions ({AD_GROUP})
  • {campaign_neg_count} campaign negatives + {adgroup_neg_count} ad group negatives

Columns
-------
  Done      — set to TRUE when complete (or convert to checkbox in Numbers)
  Section   — Setup | Headline | Description | Ops
  Phase     — Pre-launch, Campaign, Extensions, Ad group, Negatives, Launch, Week 1, etc.
  Step      — step number within that phase
  Task      — what to do (Add exact keyword, Campaign negative phrase, …)
  Value     — paste value, URL, keyword, headline, or description text
  Ad group  — {AD_GROUP} or Campaign
  Notes     — rank, pins, char counts

Open in Numbers
---------------
1. Numbers → File → Open → secplus-campaign-checklist.csv
2. Select Done column → Format → Checkbox (optional)
3. Filter Section = Setup and Phase = Ad group to paste keywords only
4. Filter Section = Setup and Phase = Extensions for sitelinks
5. Filter Section = Setup and Phase = Negatives for negatives
6. File → Save to create a .numbers file

Regenerate after keyword CSV edits
----------------------------------
  npm run sync:secplus-checklist

Source keywords: marketing-research/Sec+ Campaign/secplus-keywords.csv

Campaign summary
----------------
Campaign:   Security+ SY0-701 · Exam prep · becertifiedtoday
Budget:     $20.00/day · max CPC $2.75
Ad group:   {AD_GROUP} (only)
Landing:    https://becertifiedtoday.com/secplus/pbq-practice-browser.html
UTM:        utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=pbq-wedge

Full reference: marketing-research/Sec+ Campaign/Sec+ Notes.md
""",
        encoding="utf-8",
    )


def main() -> None:
    keywords = load_keywords()
    positives, campaign_negs, adgroup_negs = keyword_rows(keywords)
    rows = (
        static_setup_rows()
        + sitelink_rows()
        + positives
        + campaign_negs
        + adgroup_negs
        + rsa_rows()
        + launch_rows()
        + ops_rows()
    )
    write_checklist(rows)
    positive_count = sum(1 for k in keywords if (k.get("Level") or "").strip() == "positive")
    campaign_neg_count = len(campaign_negs)
    adgroup_neg_count = len(adgroup_negs)
    write_readme(positive_count, campaign_neg_count, adgroup_neg_count)
    print(
        f"Wrote {CHECKLIST_CSV} "
        f"({positive_count} positives, {campaign_neg_count}+{adgroup_neg_count} negatives, "
        f"{len(rows)} total rows)"
    )
    print(f"Wrote {README_TXT}")


if __name__ == "__main__":
    main()

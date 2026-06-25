#!/usr/bin/env python3
"""Regenerate CCNA-Auto hunt inventory Obsidian notes from BCT bank + Hunt/ccna."""
from __future__ import annotations

import csv
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "CCNA-Auto"
QDIR = ROOT / "public" / "CCNA-Study" / "CCNA_questions"
DNDDIR = ROOT / "public" / "CCNA-Study" / "CCNA_D_D"
TOPIC_MAP = ROOT / "public" / "CCNA-Study" / "data" / "ccna-question-topic-map.json"
MANIFEST = ROOT / "public" / "CCNA-Study" / "data" / "ccna-practice-questions-manifest.json"
DND_MAP = ROOT / "public" / "CCNA-Study" / "data" / "ccna-dnd-topic-map.json"
HUNT_CCNA = ROOT / "Hunt" / "ccna"
LABS_RUNS = ROOT / "data" / "ccna-question-sourcing" / "labs-sim" / "runs"

PREFIXES = ("6.",)
KEYWORDS = (
    "ansible", "terraform", "rest-api", "json-", "sdn", "northbound", "southbound",
    "yang", "netconf", "git-", "python-", "automation", "programmability", "dna-center",
    "meraki", "controller-based", "api-key", "crud", "http-verb", "http-get", "http-put",
    "http-post", "http-delete", "chef-agent", "puppet", "generative-ai", "predictive-ai",
)
STRONG_HUNT = KEYWORDS + (
    "playbook", "agentless", "intent-based", "devops", "rest api", "python script",
    "meraki cloud", "controller-based",
)


def page_title(path: Path, fallback: str, titles: dict[str, str]) -> str:
    if titles.get(fallback):
        return titles[fallback]
    if not path.is_file():
        return fallback.replace("-", " ")
    page = path.read_text(encoding="utf-8", errors="replace")
    tm = re.search(r"<title>(.*?)</title>", page, re.I)
    if tm:
        t = re.sub(r"\s*\|\s*Be Certified Today.*$", "", tm.group(1).strip(), flags=re.I)
        t = re.sub(r"^CCNA\s*[—-]\s*", "", t)
        if t:
            return t
    hm = re.search(r"<h1[^>]*>(.*?)</h1>", page, re.I | re.DOTALL)
    if hm:
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", hm.group(1))).strip()
    return fallback.replace("-", " ")


def match_slug(filename: str, objs: list) -> list[str] | None:
    slug = filename.replace(".html", "")
    obj_ids = [str(o) for o in objs]
    if any(o.startswith(PREFIXES) for o in obj_ids):
        return obj_ids
    if any(kw in slug for kw in KEYWORDS):
        return obj_ids
    return None


def obj_label(obj_ids: list[str]) -> str:
    return ", ".join(sorted(set(obj_ids)))


def md_table(headers: list[str], rows: list[tuple]) -> list[str]:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in rows:
        out.append("| " + " | ".join(str(c).replace("|", "/") for c in row) + " |")
    return out


def hunt_stem(body: str) -> str:
    past_fm = False
    fm = 0
    in_fence = False
    for line in body.splitlines():
        if line.strip() == "---":
            fm += 1
            if fm == 2:
                past_fm = True
            continue
        if not past_fm:
            continue
        s = line.strip()
        if s.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not s or s.startswith("# Question") or s.startswith("**Topic:") or s.startswith("**Exhibit"):
            continue
        if s.startswith("**") or s.startswith("- ") or s.startswith("- ["):
            continue
        if s.startswith("#"):
            continue
        return s[:120]
    return ""


def hunt_link(rel: str) -> str:
    return f"[[Hunt/{rel.replace('.md', '')}]]"


def latest_hunt_run() -> Path | None:
    runs = sorted(HUNT_CCNA.glob("20*-*.md"), reverse=True)
    for run in runs:
        if run.name != "README.md" and run.stem.count("-") == 2:
            return HUNT_CCNA / run.stem
    return None


def collect_hunt_mcq(run_dir: Path | None) -> list[tuple[str, str, str, str]]:
    if not run_dir or not run_dir.is_dir():
        return []
    rows: list[tuple[str, str, str, str]] = []
    for p in sorted(run_dir.rglob("Q*.md")):
        body = p.read_text(encoding="utf-8", errors="replace")
        if not any(kw in (body + " " + p.stem).lower() for kw in STRONG_HUNT):
            continue
        rel = str(p.relative_to(ROOT / "Hunt"))
        sm = re.search(r"\*\*Source:\*\* `([^`]+)`", body)
        rows.append((rel, hunt_stem(body), p.parts[-2], sm.group(1) if sm else ""))
    return rows


def collect_hunt_labs() -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for path in sorted(LABS_RUNS.glob("*-net-new.csv"), reverse=True):
        with path.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                blob = " ".join(row.values()).lower()
                if any(kw in blob for kw in STRONG_HUNT + ("playbook", "script", "drag-and-drop", "simulation")):
                    rows.append((
                        (row.get("stem") or "")[:120],
                        row.get("source_id", ""),
                        path.stem.replace("-net-new", ""),
                    ))
        if rows:
            break
    return rows


def main() -> int:
    topic_map = json.loads(TOPIC_MAP.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    dnd_map = json.loads(DND_MAP.read_text(encoding="utf-8"))
    titles = {x["slug"]: x.get("title", "") for x in manifest.get("questions", [])}

    bct_mcq: list[tuple[str, str, str]] = []
    for fn, objs in sorted(topic_map.get("assignments", {}).items()):
        obj_ids = match_slug(fn, objs)
        if obj_ids:
            slug = fn.replace(".html", "")
            bct_mcq.append((slug, page_title(QDIR / fn, slug, titles), obj_label(obj_ids)))

    bct_dnd: list[tuple[str, str, str]] = []
    for fn, objs in sorted(dnd_map.get("assignments", {}).items()):
        obj_ids = match_slug(fn, objs)
        if obj_ids:
            slug = fn.replace(".html", "")
            bct_dnd.append((slug, page_title(DNDDIR / fn, slug, titles), obj_label(obj_ids)))

    run_dir = latest_hunt_run()
    hunt_mcq = collect_hunt_mcq(run_dir)
    hunt_labs = collect_hunt_labs()
    run_label = run_dir.name if run_dir else "none"

    (OUT / "hunt-inventory.md").write_text(
        "\n".join([
            "---", "type: hunt-inventory", "exam: CCNAAUTO-200-901", f"generated: {date.today().isoformat()}", "---", "",
            "# CCNA-Auto hunt inventory", "",
            f"Hunt run: `{run_label}` · Regenerate: `python3 scripts/gen_ccnaauto_hunt_inventory.py`", "",
            "| Category | BCT bank | Hunt net-new |",
            "|----------|----------|--------------|",
            f"| MCQ questions | {len(bct_mcq)} | {len(hunt_mcq)} |",
            f"| Drag-and-drop | {len(bct_dnd)} | — |",
            f"| CLI labs / sim | 0 | {len(hunt_labs)} |", "",
            "[[hunt-inventory-questions|Questions]] · [[hunt-inventory-drag-drop|Drag-and-drop]] · [[hunt-inventory-labs|Labs and sim]]", "",
            "Back: [[README|CCNA-Auto]]", "",
        ]) + "\n",
        encoding="utf-8",
    )

    hunt_run_link = f"[[Hunt/ccna/{run_label}|CCNA hunt {run_label}]]" if run_dir else "_no Hunt run yet_"
    (OUT / "hunt-inventory-questions.md").write_text(
        "\n".join([
            "---", "type: hunt-inventory", "exam: CCNAAUTO-200-901", "category: mcq", f"generated: {date.today().isoformat()}", "---", "",
            "# Hunt inventory — MCQ questions", "",
            f"BCT bank: **{len(bct_mcq)}** · Hunt net-new: **{len(hunt_mcq)}**", "",
            "Back: [[hunt-inventory|Inventory]] · [[blueprint-hunt-list|Blueprint]]", "", "---", "",
            "## BCT bank", "",
            "Preview: `http://localhost:3000/CCNA-Study/CCNA_questions/{{slug}}.html`", "",
        ] + md_table(["Title", "Slug", "Objectives"], [(t, s, o) for s, t, o in bct_mcq]) + [
            "", "---", "", "## Hunt net-new", "",
            f"From {hunt_run_link} · verify Cisco Tier A", "",
        ] + (md_table(["Link", "Ver.", "Source", "Stem"], [
            (hunt_link(rel), ver, src, stem) for rel, stem, ver, src in hunt_mcq
        ]) if hunt_mcq else ["_No automation hunt MCQs in latest run._"])) + "\n",
        encoding="utf-8",
    )

    (OUT / "hunt-inventory-drag-drop.md").write_text(
        "\n".join([
            "---", "type: hunt-inventory", "exam: CCNAAUTO-200-901", "category: drag-drop", f"generated: {date.today().isoformat()}", "---", "",
            "# Hunt inventory — drag-and-drop", "",
            f"BCT bank: **{len(bct_dnd)}** items", "",
            "Preview: `http://localhost:3000/CCNA-Study/CCNA_D_D/{{slug}}.html`", "",
            "Back: [[hunt-inventory|Inventory]] · [[blueprint-hunt-list|Blueprint]]", "", "---", "",
        ] + md_table(["Title", "Slug", "Objectives"], [(t, s, o) for s, t, o in bct_dnd])) + "\n",
        encoding="utf-8",
    )

    lab_lines = [
        "---", "type: hunt-inventory", "exam: CCNAAUTO-200-901", "category: labs", f"generated: {date.today().isoformat()}", "---", "",
        "# Hunt inventory — labs and sim", "",
        f"BCT automation CLI labs: **0** · Hunt net-new: **{len(hunt_labs)}**", "",
        "Back: [[hunt-inventory|Inventory]] · [[blueprint-hunt-list|Blueprint]]", "", "---", "",
        "## BCT bank", "",
        "No CCNA automation CLI labs in bank yet.", "", "---", "", "## Hunt net-new", "",
    ]
    if hunt_labs:
        lab_lines += md_table(["Stem", "Source", "Run"], [(s, src, run) for s, src, run in hunt_labs])
    else:
        lab_lines.append("_No automation labs/sim in latest CCNA labs hunt run._")
    (OUT / "hunt-inventory-labs.md").write_text("\n".join(lab_lines) + "\n", encoding="utf-8")

    print(f"[gen_ccnaauto_hunt_inventory] BCT MCQ {len(bct_mcq)} · DND {len(bct_dnd)} · hunt MCQ {len(hunt_mcq)} · hunt labs {len(hunt_labs)} · run {run_label}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Build public/js/question-answers.json from public/question-*.html."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
OUT = PUBLIC / "js" / "question-answers.json"

# Manual entries: use "__IMG__:/path|caption" for image reveals (see public/js/practice-questions.js).
ANSWER_OVERRIDES: dict[str, str] = {
    "2": "__IMG__:assets/question-2-answer.png|Correct. Blank 1: access-list-seq-rule; 2: deny; 3: ip; 4: dst-any.",
    "9": "__IMG__:assets/question-9-answer.png|Correct. Blank 1: dumps; 2: data; 3: separators=(',', ':').",
    "363": "__IMG__:assets/question-363-answer.png|Correct. Filled request template: permit, set, next-hop, and address for next-hop 10.10.10.10.",
}


def extract_answerbox_correct(html: str) -> str | None:
    m = re.search(r'answerBox\.textContent\s*=\s*"Correct\.\s*([^"]*)"', html)
    if m:
        return "Correct. " + m.group(1).replace("\\n", "\n").replace('\\"', '"')
    m = re.search(
        r'answerBox\.textContent\s*=\s*\n\s*"Correct\.\s*([^"]*)"',
        html,
        re.DOTALL,
    )
    if m:
        return "Correct. " + m.group(1).replace("\\n", "\n").replace('\\"', '"')
    return None


def extract_drop_rows(html: str) -> str | None:
    rows = re.findall(
        r'<div class="left-box">([^<]+)</div>\s*'
        r'<div class="drop-slot"[^>]*data-target="([^"]*)"',
        html,
        re.DOTALL,
    )
    if not rows:
        return None
    parts = [f"{left.strip()} → {tgt}" for left, tgt in rows]
    return "Correct. " + "; ".join(parts)


def extract_target_groups(html: str) -> str | None:
    """Ansible/Puppet and EIGRP/OSPF style: target-title + drop-slots."""
    m = re.search(r'class="targets"[^>]*>([\s\S]*?)</section>', html)
    if not m:
        return None
    chunk = m.group(1)
    bits: list[str] = []
    title: str | None = None
    for mm in re.finditer(
        r'<div class="target-title">([^<]+)</div>|data-target="([^"]*)"',
        chunk,
    ):
        if mm.group(1):
            title = mm.group(1).strip()
        elif mm.group(2) and title:
            bits.append(f"{title}: {mm.group(2)}")
    if not bits:
        return None
    return "Correct. " + "; ".join(bits)


def extract_slot_targets_pre(html: str) -> str | None:
    targets = re.findall(r'<span class="slot"[^>]*data-target="([^"]+)"', html)
    if not targets:
        return None
    return "Correct. Fill blanks in order: " + " | ".join(targets)


def extract_answers_object(html: str) -> str | None:
    m = re.search(r"const answers\s*=\s*\{([^}]+)\}", html, re.DOTALL)
    if not m:
        return None
    body = m.group(1)
    pairs = re.findall(r'"(\d+)"\s*:\s*"([^"]*)"', body)
    if not pairs:
        return None
    pairs.sort(key=lambda x: int(x[0]))
    ordered = [v for _, v in pairs]
    return "Correct. Slots 1–" + str(len(ordered)) + ": " + " → ".join(ordered)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out: dict[str, str] = {}
    for path in sorted(PUBLIC.glob("question-*.html"), key=lambda p: int(p.stem.split("-")[1])):
        n = path.stem.split("-")[1]
        if n in ANSWER_OVERRIDES:
            out[n] = ANSWER_OVERRIDES[n]
            continue
        html = path.read_text(encoding="utf-8")
        s = extract_answerbox_correct(html)
        if not s:
            s = extract_drop_rows(html)
        if not s:
            s = extract_target_groups(html)
        if not s:
            s = extract_slot_targets_pre(html)
        if not s:
            s = extract_answers_object(html)
        if not s:
            raise SystemExit(f"Could not extract answer for {path.name}")
        out[n] = s

    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(out)} entries to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

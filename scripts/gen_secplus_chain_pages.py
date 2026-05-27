#!/usr/bin/env python3
"""Generate Security+ practice question HTML under public/COMP_TIA_SEC+/SEC+_Questions/."""
from __future__ import annotations

import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "public/COMP_TIA_SEC+/SEC+_Questions"
HUB_JS = ROOT / "public/COMP_TIA_SEC+/js/secplus-practice-hub.js"
TOPIC_MAP = ROOT / "public/COMP_TIA_SEC+/data/secplus-question-topic-map.json"
OBJECTIVES_JSON = ROOT / "public/COMP_TIA_SEC+/data/secplus-exam-objectives-sy0-701.json"
PORTAL_HOME = "/COMP_TIA_SEC+/SEC+_Training_Portal.html"
QUESTIONS_BASE = "/COMP_TIA_SEC+/SEC+_Questions/"
SECPLUS_BANK_VERSION_LABEL = "Version: 1.1 2026"

STYLE = r"""  <style>
    :root {
      color-scheme: light dark;
      font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
    }
    body {
      margin: 0;
      min-height: 100vh;
      display: grid;
      place-items: center;
      background: #ffffff;
      color: #e6edf3;
      padding: 16px 16px calc(80px + env(safe-area-inset-bottom, 0px));
      box-sizing: border-box;
    }
    .card {
      width: min(900px, 100%);
      background: #121a2b;
      border: 1px solid #2d3b5a;
      border-radius: 14px;
      padding: 28px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
      display: flex;
      flex-direction: column;
    }
    .secplus-objective-tag {
      margin-top: 18px;
      align-self: flex-start;
      max-width: 100%;
      padding: 10px 12px;
      border-radius: 10px;
      border: 1px solid #2d3b5a;
      background: #0f1729;
      color: #b8c3d6;
      font-size: 0.65rem;
      line-height: 1.45;
      text-align: left;
    }
    .secplus-objective-tag__version {
      margin-bottom: 6px;
      color: #9fb0cc;
      font-size: 0.62rem;
    }
    .secplus-objective-tag__title {
      font-weight: 700;
      color: #e6edf3;
      margin-bottom: 4px;
    }
    .secplus-objective-tag__row {
      margin: 2px 0;
    }
    h1 {
      margin: 0 0 8px;
      font-size: clamp(1.05rem, 2vw, 1.45rem);
      line-height: 1.35;
    }
    .choice {
      display: block;
      margin: 10px 0;
      padding: 12px 14px;
      border-radius: 10px;
      background: #1a253b;
      border: 1px solid #2c3f62;
      font-size: 1.02rem;
      cursor: pointer;
    }
    .choice input {
      margin-right: 10px;
      transform: translateY(1px);
    }
    .question-nav {
      margin: 0 0 20px;
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      justify-content: space-between;
    }
    .question-nav-links {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
    }
    .question-nav .nav-link {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      text-decoration: none;
      color: #f3e8ff;
      background: #5b21b6;
      border: 1px solid #7c3aed;
      border-radius: 10px;
      padding: 10px 16px;
      font-weight: 700;
      font-size: 0.95rem;
      font-family: inherit;
      cursor: pointer;
    }
    .question-nav .nav-link--disabled {
      opacity: 0.35;
      pointer-events: none;
      cursor: default;
    }
    .question-nav .nav-link:hover {
      filter: brightness(1.08);
    }
    .answer {
      margin-top: 18px;
      padding: 14px;
      border-radius: 10px;
      font-weight: 700;
      display: none;
      line-height: 1.45;
    }
    .answer.correct {
      background: #113e2d;
      border: 1px solid #1f7a58;
    }
    .answer.incorrect {
      background: #442020;
      border: 1px solid #8c3434;
    }
  </style>"""


def build_question_nav(prev_slug: str | None, next_slug: str | None) -> str:
    parts: list[str] = []
    if prev_slug:
        parts.append(
            f'      <a class="nav-link nav-prev" href="{QUESTIONS_BASE}{html.escape(prev_slug)}.html">Back</a>'
        )
    else:
        parts.append(
            '      <span class="nav-link nav-prev nav-link--disabled" aria-hidden="true">Back</span>'
        )
    parts.append(f'      <a class="nav-link nav-home" href="{PORTAL_HOME}">Home</a>')
    if next_slug:
        parts.append(
            f'      <a class="nav-link nav-next next-link" href="{QUESTIONS_BASE}{html.escape(next_slug)}.html">Next</a>'
        )
    else:
        parts.append(
            '      <span class="nav-link nav-next nav-link--disabled" aria-hidden="true">Next</span>'
        )
    links = "\n".join(parts)
    return (
        '    <nav class="question-nav" aria-label="Question navigation">\n'
        '      <div class="question-nav-links">\n'
        f"{links}\n"
        "      </div>\n"
        "    </nav>"
    )


def choice_line(name: str, letter: str, text: str) -> str:
    t = html.escape(text, quote=False)
    return f'    <label class="choice"><input type="radio" name="{name}" value="{letter}" />{letter}. {t}</label>'


def _load_objective_lookups() -> tuple[dict[str, str], dict[str, tuple[str, str]]]:
    domain_lookup: dict[str, str] = {}
    objective_lookup: dict[str, tuple[str, str]] = {}
    if not OBJECTIVES_JSON.is_file():
        return domain_lookup, objective_lookup
    data = json.loads(OBJECTIVES_JSON.read_text(encoding="utf-8"))
    for domain in data.get("domains") or []:
        did = domain.get("id")
        dname = domain.get("name") or ""
        if did:
            domain_lookup[str(did)] = str(dname)
        for obj in domain.get("objectives") or []:
            oid = obj.get("id")
            if oid:
                objective_lookup[str(oid)] = (dname, str(obj.get("text") or ""))
    return domain_lookup, objective_lookup


def objective_label(
    oid: str,
    domain_lookup: dict[str, str],
    objective_lookup: dict[str, tuple[str, str]],
) -> str:
    if oid in domain_lookup:
        return f"{oid} ({domain_lookup[oid]})"
    if oid in objective_lookup:
        dname, text = objective_lookup[oid]
        return f"{oid} ({dname}): {text}"
    return oid


def build_objective_footer(
    objective_ids: list[str],
    domain_lookup: dict[str, str],
    objective_lookup: dict[str, tuple[str, str]],
) -> str:
    if not objective_ids:
        return ""
    rows = [
        f'      <div class="secplus-objective-tag__row">• {html.escape(objective_label(oid, domain_lookup, objective_lookup))}</div>'
        for oid in objective_ids
    ]
    body = "\n".join(rows)
    version = html.escape(SECPLUS_BANK_VERSION_LABEL)
    return (
        '    <div class="secplus-objective-tag ccna-objective-tag" aria-label="Security+ objective section">\n'
        f'      <div class="secplus-objective-tag__version">{version}</div>\n'
        '      <div class="secplus-objective-tag__title">Security+ objective section</div>\n'
        f"{body}\n"
        "    </div>"
    )


def render_page(
    *,
    title: str,
    slug: str,
    stem: str,
    choices: list[str],
    name: str,
    correct: str,
    explain: str,
    prev_slug: str | None,
    next_slug: str | None,
    prepend_html: str = "",
    objective_ids: list[str] | None = None,
    domain_lookup: dict[str, str] | None = None,
    objective_lookup: dict[str, tuple[str, str]] | None = None,
) -> str:
    nav = build_question_nav(prev_slug, next_slug)
    objective_footer = build_objective_footer(
        objective_ids or [],
        domain_lookup or {},
        objective_lookup or {},
    )
    choices_html = "\n".join(
        choice_line(name, chr(ord("A") + i), text) for i, text in enumerate(choices)
    )
    msg_json = json.dumps(explain)
    stem_h = html.escape(stem)
    prepend = f"{prepend_html.rstrip()}\n" if prepend_html else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="robots" content="index, follow" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)}</title>
{STYLE}
  <link rel="stylesheet" href="/COMP_TIA_SEC+/SEC+_Samples/secplus-sample-touch.css" />
</head>
<body>
  <script src="/js/sample-url-mask-apply.js"></script>
  <script src="/COMP_TIA_SEC+/js/secplus-practice-nav.js" defer></script>
  <main class="card">
{nav}
{prepend}    <h1>{stem_h}</h1>

{choices_html}

    <div id="answerBox" class="answer" aria-live="polite"></div>
{objective_footer}
  </main>

  <script>
    (function () {{
      var CORRECT = {json.dumps(correct)};
      var CORRECT_MSG = {msg_json};
      var answerBox = document.getElementById("answerBox");

      function applyFeedback(value) {{
        answerBox.style.display = "block";
        if (value === CORRECT) {{
          answerBox.className = "answer correct";
          answerBox.textContent = CORRECT_MSG;
        }} else {{
          answerBox.className = "answer incorrect";
          answerBox.textContent = "Incorrect.";
        }}
      }}

      document.querySelectorAll('input[name="{name}"]').forEach(function (el) {{
        el.addEventListener("change", function () {{
          if (el.checked) {{
            applyFeedback(el.value);
          }}
        }});
      }});
    }})();
  </script>
</body>
</html>
"""


# Extend this list for new questions (same shape as CCNA gen_ccna_chain_pages.py entries).
CHAIN: list[dict] = [
    {
        "slug": "pentest-hypervisor-vm-escape",
        "title": "Security+ — VM escape (hypervisor pentest)",
        "stem": (
            "During a penetration test in a hypervisor, the security engineer is able to use a script "
            "to inject a malicious payload and access the host filesystem. Which of the following "
            "best describes this vulnerability?"
        ),
        "name": "secplus_q1",
        "correct": "A",
        "explain": (
            "Correct. A — VM escape is when guest code breaks out of the virtual machine boundary "
            "to reach the hypervisor or host OS (for example, accessing the host filesystem). "
            "Cross-site scripting affects browsers, malicious update describes tampered software "
            "distribution, and SQL injection targets database queries."
        ),
        "choices": [
            "VM escape",
            "Cross-site scripting",
            "Malicious update",
            "SQL injection",
        ],
        "objectives": ["2.3", "3.1"],
    },
]


def sync_hub_slugs(chain: list[dict]) -> None:
    slugs = [q["slug"] for q in chain]
    inner = ",\n    ".join(json.dumps(s) for s in slugs)
    HUB_JS.parent.mkdir(parents=True, exist_ok=True)
    if HUB_JS.is_file():
        text = HUB_JS.read_text(encoding="utf-8")
        patched, n = re.subn(
            r"window\.SECPLUS_PRACTICE\.SLUGS\s*=\s*\[[\s\S]*?\];",
            f"window.SECPLUS_PRACTICE.SLUGS = [\n    {inner}\n  ];",
            text,
            count=1,
        )
        if n:
            HUB_JS.write_text(patched, encoding="utf-8")
            return
    body = f"""(function () {{
  "use strict";
  window.SECPLUS_PRACTICE = window.SECPLUS_PRACTICE || {{}};
  window.SECPLUS_PRACTICE.SLUGS = [
    {inner}
  ];
}})();
"""
    HUB_JS.write_text(body, encoding="utf-8")


def sync_topic_map(chain: list[dict]) -> None:
    assignments: dict[str, list[str]] = {}
    if TOPIC_MAP.is_file():
        data = json.loads(TOPIC_MAP.read_text(encoding="utf-8"))
        raw = data.get("assignments")
        if isinstance(raw, dict):
            assignments = {k: list(v) for k, v in raw.items()}
    for q in chain:
        key = f"{q['slug']}.html"
        assignments[key] = list(q.get("objectives") or ["2.0"])
    payload = {
        "schemaVersion": 1,
        "notes": "Assign Security+ question files to SY0-701 objective IDs (e.g. 2.0, 3.0).",
        "assignments": dict(sorted(assignments.items())),
    }
    TOPIC_MAP.parent.mkdir(parents=True, exist_ok=True)
    TOPIC_MAP.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    domain_lookup, objective_lookup = _load_objective_lookups()
    n = len(CHAIN)
    for i, q in enumerate(CHAIN):
        prev_slug = CHAIN[i - 1]["slug"] if i > 0 else None
        next_slug = CHAIN[i + 1]["slug"] if i + 1 < n else None
        content = render_page(
            title=q["title"],
            slug=q["slug"],
            choices=q["choices"],
            name=q["name"],
            correct=q["correct"],
            explain=q["explain"],
            stem=q["stem"],
            prev_slug=prev_slug,
            next_slug=next_slug,
            objective_ids=list(q.get("objectives") or []),
            domain_lookup=domain_lookup,
            objective_lookup=objective_lookup,
        )
        path = OUT / f"{q['slug']}.html"
        path.write_text(content, encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")
    sync_hub_slugs(CHAIN)
    sync_topic_map(CHAIN)
    print(f"Updated {HUB_JS.relative_to(ROOT)} ({n} slugs)")
    print(f"Updated {TOPIC_MAP.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Convert CCNA radio question pages: remove Check answer, show feedback on selection."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QDIR = ROOT / "public/CCNA-Study/CCNA_questions"

NEW_SCRIPT = '''  <script>
    (function () {{
      var CORRECT = {correct_json};
      var CORRECT_MSG = {msg_json};
      var resetBtn = document.getElementById("resetBtn");
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

      resetBtn.addEventListener("click", function () {{
        document.querySelectorAll('input[name="{name}"]').forEach(function (el) {{
          el.checked = false;
        }});
        answerBox.style.display = "none";
        answerBox.textContent = "";
      }});
    }})();
  </script>'''


def extract_script(html: str) -> str | None:
    m = re.search(r"<script>\s*(\(function \(\) \{.*?\}\)\(\);\s*)</script>", html, re.DOTALL)
    return m.group(1) if m else None


def extract_correct_message(script: str) -> str | None:
    idx = script.find("if (sel === CORRECT)")
    if idx < 0:
        return None
    sub = script[idx:]
    if 'answerBox.className = "answer correct"' not in sub:
        return None
    m = re.search(r"answerBox\.textContent\s*=\s*\n?\s*\"", sub)
    if not m:
        return None
    i = m.end()
    out: list[str] = []
    while i < len(sub):
        c = sub[i]
        if c == "\\":
            if i + 1 < len(sub):
                out.append(sub[i : i + 2])
                i += 2
                continue
        if c == '"':
            return "".join(out)
        out.append(c)
        i += 1
    return None


def extract_name(script: str) -> str | None:
    m = re.search(r"querySelector\('input\[name=\"([^\"]+)\"\]:checked'\)", script)
    return m.group(1) if m else None


def extract_correct_letter(script: str) -> str | None:
    m = re.search(r'var CORRECT = "([A-D])";', script)
    return m.group(1) if m else None


def transform_html(html: str) -> str | None:
    script_inner = extract_script(html)
    if not script_inner:
        return None
    name = extract_name(script_inner)
    letter = extract_correct_letter(script_inner)
    msg = extract_correct_message(script_inner)
    if not name or not letter or msg is None:
        return None

    new_script = NEW_SCRIPT.format(
        correct_json=json.dumps(letter),
        msg_json=json.dumps(msg),
        name=name,
    )

    html2 = html.replace(
        '<button id="checkBtn" type="button">Check answer</button>\n      ',
        "",
        1,
    )
    s_start = html2.find("<script>")
    s_end = html2.find("</script>", s_start)
    if s_start < 0 or s_end < 0:
        return None
    html2 = html2[:s_start] + new_script + html2[s_end + len("</script>") :]
    html2 = html2.replace(
        "Select one answer, then click Check answer.",
        "Select an answer — feedback appears immediately.",
    )
    return html2


def main() -> None:
    skip = {"qos-minimum-bandwidth-choose-two.html", "rstp-port-states-choose-two.html"}
    for path in sorted(QDIR.glob("*.html")):
        if path.name in skip:
            continue
        html = path.read_text(encoding="utf-8")
        if 'type="checkbox"' in html:
            continue
        if "checkBtn" not in html:
            continue
        out = transform_html(html)
        if not out:
            print("SKIP (parse failed):", path.name)
            continue
        path.write_text(out, encoding="utf-8")
        print("OK", path.name)


if __name__ == "__main__":
    main()

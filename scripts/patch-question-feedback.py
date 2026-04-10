#!/usr/bin/env python3
"""Patch question HTML: show correct answer on incorrect; ensure Home exists."""
import json
import re
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent.parent / "public"

HOME_BLOCK = """  <style>
    .home-key {
      position: fixed;
      right: 18px;
      bottom: 18px;
      z-index: 9999;
      text-decoration: none;
      background: #254b8a;
      border: 1px solid #3d6dbb;
      color: #e6edf3;
      border-radius: 10px;
      padding: 10px 14px;
      font-weight: 700;
      box-shadow: 0 8px 22px rgba(0, 0, 0, 0.35);
    }
    .home-key:hover {
      filter: brightness(1.08);
    }
  </style>
  <a class="home-key" href="/practice-launcher.html">Home</a>
"""


def strip_correct_prefix(s: str) -> str:
    if s.startswith("Correct. "):
        return s[len("Correct. ") :]
    return s


def js_string_literal(s: str) -> str:
    """Content for inside double quotes in JS."""
    return json.dumps(s)[1:-1]


def ensure_home(text: str) -> str:
    if "home-key" in text or "sim-nav-home" in text:
        return text
    if "</body>" not in text:
        return text
    insert = "\n" + HOME_BLOCK + "\n"
    return text.replace("</body>", insert + "</body>", 1)


def patch_checkbox_incorrect(text: str) -> str:
    pat = re.compile(
        r"if \(isCorrect\) \{\s*"
        r'answerBox\.className = "answer correct";\s*'
        r'answerBox\.textContent = "([^"]+)";\s*'
        r"\} else \{\s*"
        r'answerBox\.className = "answer incorrect";\s*'
        r'answerBox\.textContent = "Incorrect\."\s*;\s*'
        r"\}",
        re.DOTALL,
    )

    def repl(m: re.Match) -> str:
        correct_full = m.group(1)
        tail = strip_correct_prefix(correct_full)
        wrong = js_string_literal("Incorrect. The correct answer: " + tail)
        return (
            "if (isCorrect) {\n"
            '        answerBox.className = "answer correct";\n'
            f'        answerBox.textContent = "{js_string_literal(correct_full)}";\n'
            "      } else {\n"
            '        answerBox.className = "answer incorrect";\n'
            f'        answerBox.textContent = "{wrong}";\n'
            "      }"
        )

    return pat.sub(repl, text)


def patch_radio_single_line(text: str) -> str:
    pat = re.compile(
        r'if \(option\.value === ("[^"]+")\) \{\s*\n'
        r'\s*answerBox\.className = "answer correct";\s*\n'
        r'\s*answerBox\.textContent = ("Correct\.[^"]*");\s*\n'
        r"\s*\} else \{\s*\n"
        r'\s*answerBox\.className = "answer incorrect";\s*\n'
        r'\s*answerBox\.textContent = "Incorrect\."\s*;\s*\n'
        r"\s*\}",
        re.MULTILINE,
    )

    def repl(m: re.Match) -> str:
        cond = m.group(1)
        qraw = m.group(2)
        inner = json.loads(qraw)  # safe parse "Correct. ..."
        tail = strip_correct_prefix(inner)
        wrong = js_string_literal("Incorrect. The correct answer: " + tail)
        return (
            f"if (option.value === {cond}) {{\n"
            '          answerBox.className = "answer correct";\n'
            f"          answerBox.textContent = {qraw};\n"
            "        } else {\n"
            '          answerBox.className = "answer incorrect";\n'
            f'          answerBox.textContent = "{wrong}";\n'
            "        }"
        )

    return pat.sub(repl, text)


def patch_radio_multiline(text: str) -> str:
    """answerBox.textContent =\n          \"Correct...\";"""
    pat = re.compile(
        r'if \(option\.value === ("[^"]+")\) \{\s*\n'
        r'\s*answerBox\.className = "answer correct";\s*\n'
        r'\s*answerBox\.textContent =\s*\n\s*("Correct\.[^"]+")\s*;\s*\n'
        r"\s*\} else \{\s*\n"
        r'\s*answerBox\.className = "answer incorrect";\s*\n'
        r'\s*answerBox\.textContent = "Incorrect\."\s*;\s*\n'
        r"\s*\}",
        re.MULTILINE | re.DOTALL,
    )

    def repl(m: re.Match) -> str:
        cond = m.group(1)
        qraw = m.group(2)
        inner = json.loads(qraw)
        tail = strip_correct_prefix(inner)
        wrong = js_string_literal("Incorrect. The correct answer: " + tail)
        return (
            f"if (option.value === {cond}) {{\n"
            '          answerBox.className = "answer correct";\n'
            f"          answerBox.textContent =\n            {qraw};\n"
            "        } else {\n"
            '          answerBox.className = "answer incorrect";\n'
            f'          answerBox.textContent = "{wrong}";\n'
            "        }"
        )

    return pat.sub(repl, text)


def main() -> None:
    files = sorted(PUBLIC.glob("question-*.html")) + [PUBLIC / "bgp-question.html"]
    for path in files:
        if not path.is_file():
            continue
        orig = path.read_text(encoding="utf-8")
        text = orig
        if "checkBtn.addEventListener" in text and 'answerBox.textContent = "Incorrect."' in text:
            text = patch_checkbox_incorrect(text)
        text = patch_radio_multiline(text)
        text = patch_radio_single_line(text)
        text = ensure_home(text)
        if text != orig:
            path.write_text(text, encoding="utf-8")
            print("patched", path.name)


if __name__ == "__main__":
    main()

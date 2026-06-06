#!/usr/bin/env python3
"""Rewrite ENCOR MCQ pages under ENCOR_Questions/ with the shared light question template."""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MCQ_DIR = ROOT / "public" / "CCNP-ENCOR-Study" / "ENCOR_Questions"
SAMPLES_DIR = ROOT / "public" / "CCNP-ENCOR-Study" / "ENCOR_Samples"
PORTAL_HOME = "/CCNP-ENCOR-Study/ENCOR_Training_Portal.html"
QUESTIONS_BASE = "/CCNP-ENCOR-Study/ENCOR_Questions/"
LOGO_IMG = "/images/logo/becertifiedtoday_logo_image_trans.png"
VERSION_LABEL = "350-401 ENCOR v1.2"

KEEP_CSS_KEYWORDS = (
    "exhibit",
    "cli-",
    "topology",
    "figure",
    "route-exhibit",
    "code-exhibit",
    "debug-exhibit",
    "answer-cli",
    "image-wrap",
    "instructions",
    "stem-after",
    ".cfg",
)

OUTSIDE_TEXT_COLOR_SELECTORS = (
    "stem-after-exhibit",
    "exhibit-ref",
    "exhibit-section-caption",
    "instructions",
)

BASE_STYLE = r"""  <style>
    :root {
      color-scheme: light;
      font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
      --bcc-outside-text: #1a3d6e;
      --bcc-choice-bg: #254b8a;
      --bcc-choice-border: #3d6dbb;
      --bcc-box-text: #e6edf3;
    }
    body {
      margin: 0;
      min-height: 100vh;
      display: grid;
      place-items: center;
      position: relative;
      background: #ffffff;
      color: var(--bcc-outside-text);
      padding: 16px;
      padding-bottom: calc(96px + env(safe-area-inset-bottom, 0px));
      box-sizing: border-box;
    }
    .page-logo-watermark {
      position: fixed;
      inset: 0;
      z-index: 0;
      pointer-events: none;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }
    .page-logo-watermark img {
      width: min(85vw, 720px);
      max-height: 85vh;
      height: auto;
      object-fit: contain;
      opacity: 0.16;
    }
    .question-shell {
      width: min(900px, 100%);
      display: flex;
      flex-direction: column;
      align-items: stretch;
      position: relative;
      z-index: 1;
    }
    .question-shell .site-logo-corner {
      position: static;
      align-self: flex-end;
      margin: 0 0 2rem;
      display: inline-flex;
      background: transparent;
      border: none;
      padding: 0;
      text-decoration: none;
    }
    .question-shell .site-logo-corner img {
      width: 52px;
      height: 52px;
    }
    .card {
      width: 100%;
      background: transparent;
      border: none;
      padding: 0;
      box-shadow: none;
      color: var(--bcc-outside-text);
    }
    h1 {
      margin: 0 0 16px;
      font-size: clamp(1.05rem, 2vw, 1.45rem);
      line-height: 1.35;
      color: var(--bcc-outside-text);
    }
    h1.choose-two-stem {
      line-height: 1.5;
    }
    .choice {
      display: block;
      margin: 10px 0;
      padding: 12px 14px;
      border-radius: 10px;
      background: var(--bcc-choice-bg);
      border: 1px solid var(--bcc-choice-border);
      font-size: 1.02rem;
      color: var(--bcc-box-text);
      cursor: pointer;
    }
    .choice input {
      margin-right: 10px;
      transform: translateY(1px);
    }
    .answer {
      margin-top: 18px;
      padding: 14px;
      border-radius: 10px;
      font-weight: 700;
      display: none;
      line-height: 1.45;
      color: var(--bcc-box-text);
    }
    .answer.correct {
      background: #113e2d;
      border: 1px solid #1f7a58;
      color: #ffffff;
    }
    .answer.incorrect {
      background: #442020;
      border: 1px solid #8c3434;
      color: #fecaca;
    }
    .exhibit-ref,
    .exhibit-ref-spaced,
    .exhibit-section-caption,
    .stem-after-exhibit,
    .stem-after-exhibit-list,
    .stem-after-exhibit-tail,
    .instructions {
      color: var(--bcc-outside-text);
    }
  </style>"""


def question_ids() -> list[int]:
    ids: list[int] = []
    for path in MCQ_DIR.glob("question-*.html"):
        m = re.match(r"question-(\d+)\.html$", path.name, re.I)
        if m:
            ids.append(int(m.group(1)))
    return sorted(ids)


def build_nav(prev_id: int | None, next_id: int | None) -> str:
    parts: list[str] = []
    if prev_id is not None:
        parts.append(
            f'      <a class="nav-link nav-prev" href="{QUESTIONS_BASE}question-{prev_id}.html">Back</a>'
        )
    else:
        parts.append(
            '      <span class="nav-link nav-prev nav-link--disabled" aria-hidden="true">Back</span>'
        )
    parts.append(f'      <a class="nav-link nav-home" href="{PORTAL_HOME}">Home</a>')
    if next_id is not None:
        parts.append(
            f'      <a class="nav-link nav-next next-link" href="{QUESTIONS_BASE}question-{next_id}.html">Next</a>'
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


def build_footer(*, progress_text: str = "", topic_subject: str = "") -> str:
    version = html.escape(VERSION_LABEL)
    progress = html.escape(progress_text)
    subject = html.escape(topic_subject)
    return (
        '    <div class="answer-footer">\n'
        '      <div class="answer-actions">\n'
        '        <button id="checkBtn" type="button" class="nav-check">Check answer</button>\n'
        '        <div class="question-progress-block">\n'
        f'          <span class="ccna-practice-progress" aria-live="polite">{progress}</span>\n'
        '          <p class="question-topic-meta">\n'
        f'            <span class="question-topic-meta__version">{version}</span>\n'
        f'            <span class="question-topic-meta__subject">{subject}</span>\n'
        "          </p>\n"
        "        </div>\n"
        "      </div>\n"
        '      <div class="answer-side-actions">\n'
        '        <button id="showBtn" type="button" class="nav-show-answer">Show Answer</button>\n'
        '        <label class="review-mark-box" id="reviewMarkWrap">\n'
        '          <input type="checkbox" id="reviewMark" aria-label="Mark for review" />\n'
        '          <span class="review-mark-box__label">Review</span>\n'
        "        </label>\n"
        "      </div>\n"
        "    </div>\n"
    )


def extract_head_extras(text: str) -> str:
    bits: list[str] = []
    for pat in (
        r'<link rel="canonical"[^>]+>',
        r'<meta name="description"[^>]+>',
    ):
        m = re.search(pat, text, re.I)
        if m:
            bits.append("  " + m.group(0))
    return "\n".join(bits)


def extract_first_style(text: str) -> str:
    m = re.search(r"<style>(.*?)</style>", text, re.S | re.I)
    return m.group(1) if m else ""


def normalize_outside_text_rule(selector: str, body: str) -> str:
    sl = selector.lower()
    if not any(k in sl for k in OUTSIDE_TEXT_COLOR_SELECTORS):
        return body
    body = re.sub(
        r"color:\s*#e6edf3\s*;?",
        "color: var(--bcc-outside-text);",
        body,
        flags=re.I,
    )
    return re.sub(
        r"color:\s*#b8c3d6\s*;?",
        "color: var(--bcc-outside-text);",
        body,
        flags=re.I,
    )


def extract_exhibit_css(style_text: str) -> str:
    if not style_text.strip():
        return ""
    kept: list[str] = []
    for sel, body in re.findall(r"([^{]+)\{([^}]*)\}", style_text, re.S):
        sl = sel.lower()
        if not any(k in sl for k in KEEP_CSS_KEYWORDS):
            continue
        body = normalize_outside_text_rule(sel, body.strip())
        kept.append(f"    {sel.strip()} {{\n{body}\n    }}")
    if not kept:
        return ""
    return "  <style>\n" + "\n".join(kept) + "\n  </style>"


def extract_main_content(text: str) -> str:
    m = re.search(r"<main class=\"card\">(.*?)</main>", text, re.S | re.I)
    if not m:
        raise ValueError("missing main.card")
    return m.group(1)


def strip_old_chrome(main: str) -> tuple[str, str, str, bool]:
    """Return prepend, choices_html, h1_html, is_choose_two."""
    main = re.sub(r"<div class=\"actions\">.*?</div>", "", main, flags=re.S)
    main = re.sub(r"<span id=\"nextWrap\".*?</span>", "", main, flags=re.S)
    main = re.sub(r"<div id=\"nextWrap\".*?</div>", "", main, flags=re.S)
    main = re.sub(r"<div id=\"answerBox\".*?</div>", "", main, flags=re.S)

    h1_m = re.search(r"(<h1[^>]*>.*?</h1>)", main, re.S | re.I)
    if not h1_m:
        raise ValueError("missing h1")
    h1_html = h1_m.group(1)
    if "choose-two-stem" not in h1_html and re.search(
        r"choose two", h1_html, re.I
    ):
        h1_html = h1_html.replace("<h1", '<h1 class="choose-two-stem"', 1)

    prepend = main[: h1_m.start()].strip()
    after_h1 = main[h1_m.end() :]
    labels = re.findall(
        r'<label class="choice"[\s\S]*?</label\s*>', after_h1, re.I
    )
    if not labels:
        raise ValueError("missing choices")
    first_label_pos = after_h1.find(labels[0])
    middle = after_h1[:first_label_pos].strip()
    if middle:
        prepend = (prepend + "\n\n" + middle).strip() if prepend else middle
    is_choose_two = 'type="checkbox"' in after_h1.lower()
    choices_html = "\n\n".join("    " + lbl.strip() for lbl in labels)
    return prepend, choices_html, "    " + h1_html.strip(), is_choose_two


def parse_input_name(main: str) -> str:
    m = re.search(r'name="([^"]+)"', main)
    if not m:
        raise ValueError("missing input name")
    return m.group(1)


def decode_js_string(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("`") and raw.endswith("`"):
        return raw[1:-1]
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw.strip("'\"")


def parse_script_answers(text: str, is_choose_two: bool) -> tuple[str | list[str], str]:
    scripts = re.findall(r"<script>(.*?)</script>", text, re.S | re.I)
    script = max(scripts, key=len) if scripts else ""
    if not script:
        raise ValueError("missing script")

    correct_msg = ""
    for pat in (
        r"answerBox\.textContent\s*=\s*(`[^`]+`|'[^']*Correct[^']*'|\"[^\"]*Correct[^\"]*\")",
        r"answerBox\.textContent\s*=\s*\n?\s*(`[^`]+`|'[^']*'|\"[^\"]+\")",
    ):
        m = re.search(pat, script, re.S)
        if m and "Correct" in m.group(1):
            correct_msg = decode_js_string(m.group(1))
            break

    if is_choose_two:
        m = re.search(
            r"(?:correct(?:Set)?|CORRECT)\s*=\s*new Set\(\[([^\]]+)\]\)", script
        )
        if not m:
            m = re.search(r"correctSet\s*=\s*new Set\(\[([^\]]+)\]\)", script)
        if not m:
            m = re.search(r"var CORRECT\s*=\s*\[([^\]]+)\]", script)
        if not m:
            m = re.search(
                r"const CORRECT\s*=\s*new Set\(\[([^\]]+)\]\)", script
            )
        if not m:
            ok_m = re.search(
                r"picked\.length\s*===\s*2\s*&&\s*picked\[0\]\s*===\s*['\"]([A-E])['\"]\s*&&\s*picked\[1\]\s*===\s*['\"]([A-E])['\"]",
                script,
            )
            if ok_m:
                letters = sorted([ok_m.group(1), ok_m.group(2)])
                if not correct_msg:
                    correct_msg = "Correct. " + " and ".join(letters) + "."
                return letters, correct_msg
        if not m:
            raise ValueError("choose-two correct not found")
        letters = re.findall(r"['\"]([A-E])['\"]", m.group(1))
        if len(letters) < 2:
            raise ValueError("choose-two letters incomplete")
        if not correct_msg:
            correct_msg = "Correct. " + " and ".join(sorted(letters)) + "."
        return sorted(letters), correct_msg

    m = re.search(r"option\.value\s*===\s*['\"]([A-E])['\"]", script)
    if not m:
        m2 = re.search(r'const correct\s*=\s*["\']([A-E])["\']', script, re.I)
        if m2 and re.search(r"selected\s*===\s*correct\b", script, re.I):
            letter = m2.group(1)
            if not correct_msg:
                correct_msg = f"Correct. {letter}."
            return letter, correct_msg
    if not m:
        m = re.search(r"CORRECT\s*=\s*['\"]([A-E])['\"]", script)
    if not m:
        m = re.search(r"const correct\s*=\s*['\"]([A-E])['\"]", script, re.I)
    if not m:
        m = re.search(r"sel\.value\s*===\s*['\"]([A-E])['\"]", script)
    if not m:
        raise ValueError("radio correct not found")
    letter = m.group(1)
    if not correct_msg:
        correct_msg = f"Correct. {letter}."
    return letter, correct_msg


def radio_script(name: str, correct: str, msg: str) -> str:
    msg_json = json.dumps(msg)
    return f"""  <script>
    (function () {{
      var CORRECT = {json.dumps(correct)};
      var CORRECT_MSG = {msg_json};
      var checkBtn = document.getElementById("checkBtn");
      var showBtn = document.getElementById("showBtn");
      var answerBox = document.getElementById("answerBox");

      checkBtn.addEventListener("click", function () {{
        var sel = document.querySelector('input[name="{name}"]:checked');
        answerBox.style.display = "block";
        if (!sel) {{
          answerBox.className = "answer incorrect";
          answerBox.textContent = "Select an answer.";
          return;
        }}
        if (sel.value === CORRECT) {{
          answerBox.className = "answer correct";
          answerBox.textContent = CORRECT_MSG;
        }} else {{
          answerBox.className = "answer incorrect";
          answerBox.textContent = "Incorrect.";
        }}
      }});

      showBtn.addEventListener("click", function () {{
        var input = document.querySelector('input[name="{name}"][value="' + CORRECT + '"]');
        if (input) input.checked = true;
        answerBox.style.display = "block";
        answerBox.className = "answer correct";
        answerBox.textContent = CORRECT_MSG;
      }});
    }})();
  </script>"""


def choose_two_script(name: str, correct: list[str], msg: str) -> str:
    msg_json = json.dumps(msg)
    cor_json = json.dumps(correct)
    return f"""  <script>
    (function () {{
      var CORRECT = {cor_json};
      var CORRECT_MSG = {msg_json};
      var checkBtn = document.getElementById("checkBtn");
      var showBtn = document.getElementById("showBtn");
      var answerBox = document.getElementById("answerBox");

      function selectedValues() {{
        return []
          .slice.call(document.querySelectorAll('input[name="{name}"]:checked'))
          .map(function (el) {{ return el.value; }})
          .sort();
      }}

      function arraysEqual(a, b) {{
        if (a.length !== b.length) return false;
        return a.every(function (v, i) {{ return v === b[i]; }});
      }}

      checkBtn.addEventListener("click", function () {{
        var sel = selectedValues();
        answerBox.style.display = "block";
        if (sel.length !== 2) {{
          answerBox.className = "answer incorrect";
          answerBox.textContent = "Choose exactly two answers.";
          return;
        }}
        if (arraysEqual(sel, CORRECT)) {{
          answerBox.className = "answer correct";
          answerBox.textContent = CORRECT_MSG;
        }} else {{
          answerBox.className = "answer incorrect";
          answerBox.textContent = "Incorrect.";
        }}
      }});

      showBtn.addEventListener("click", function () {{
        CORRECT.forEach(function (value) {{
          var input = document.querySelector('input[name="{name}"][value="' + value + '"]');
          if (input) input.checked = true;
        }});
        answerBox.style.display = "block";
        answerBox.className = "answer correct";
        answerBox.textContent = CORRECT_MSG;
      }});
    }})();
  </script>"""


def render_page(
    *,
    qid: int,
    title: str,
    prepend: str,
    h1_html: str,
    choices_html: str,
    name: str,
    is_choose_two: bool,
    correct: str | list[str],
    correct_msg: str,
    extra_css: str,
    prev_id: int | None,
    next_id: int | None,
) -> str:
    nav = build_nav(prev_id, next_id)
    footer = build_footer()
    prepend_block = (prepend + "\n\n") if prepend else ""
    script = (
        choose_two_script(name, correct, correct_msg)
        if is_choose_two
        else radio_script(name, correct, correct_msg)
    )
    extra_css_block = ("\n" + extra_css) if extra_css else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="robots" content="index, follow" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)}</title>
{BASE_STYLE}{extra_css_block}
  <link rel="stylesheet" href="/css/bcc-question-link-nav.css" />
  <link rel="stylesheet" href="/CCNP-ENCOR-Study/ENCOR_Samples/encor-sample-touch.css" />
</head>
<body class="encor-question-ui">
  <script src="/js/sample-url-mask-apply.js"></script>
  <script src="/CCNP-ENCOR-Study/js/encor-practice-nav.js" defer></script>
  <div class="page-logo-watermark" aria-hidden="true">
    <img src="{LOGO_IMG}" alt="" />
  </div>
  <div class="question-shell">
    <a class="site-logo-corner" href="{PORTAL_HOME}" aria-label="ENCOR training portal">
      <img src="{LOGO_IMG}" width="52" height="52" alt="Be Certified Today" />
    </a>
    <main class="card">
{nav}
{prepend_block}{h1_html}

{choices_html}

{footer}    <div id="answerBox" class="answer" aria-live="polite"></div>
    </main>
  </div>
{script}
</body>
</html>
"""


def render_static_sample(
    *,
    n: int,
    title: str,
    h1_html: str,
    choices_html: str,
    name: str,
    is_choose_two: bool,
    correct: str | list[str],
    correct_msg: str,
    head_extras: str,
) -> str:
    footer = build_footer(progress_text=f"Question {n} of 5")
    script = (
        choose_two_script(name, correct, correct_msg)
        if is_choose_two
        else radio_script(name, correct, correct_msg)
    )
    prev = f"sample-question-{n - 1}.html" if n > 1 else None
    next_href = f"sample-question-{n + 1}.html" if n < 5 else None
    prev_el = (
        f'<a class="sim-nav-btn sim-nav-prev encor-sample-prev" href="{prev}">Back</a>'
        if prev
        else '<span class="sim-nav-btn sim-nav-prev encor-sample-prev sim-nav-btn--disabled" aria-hidden="true">Back</span>'
    )
    next_el = (
        f'<a class="sim-nav-btn encor-sample-next nav-link nav-next next-link" href="{next_href}">Next</a>'
        if next_href
        else '<span class="sim-nav-btn encor-sample-next sim-nav-btn--disabled" aria-hidden="true">Next</span>'
    )
    head_extra_block = (head_extras + "\n") if head_extras else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
{head_extra_block}  <meta name="robots" content="index, follow" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" href="../../css/bcc-question-link-nav.css" />
{BASE_STYLE}
  <link rel="stylesheet" href="encor-sample-touch.css" />
</head>
<body class="encor-static-sample">
  <div class="page-logo-watermark" aria-hidden="true">
    <img src="../../../images/logo/becertifiedtoday_logo_image_trans.png" alt="" />
  </div>
  <script src="../../../js/sample-url-mask-apply.js"></script>
  <script src="../js/encor-practice-nav.js" defer></script>
  <div class="question-shell">
    <span class="site-logo-corner" aria-hidden="true">
      <img src="../../../images/logo/becertifiedtoday_logo_image_trans.png" width="52" height="52" alt="" />
    </span>
    <main class="card">
    {h1_html}

{choices_html}

{footer}    <div id="answerBox" class="answer" aria-live="polite"></div>
  </main>
  </div>
  <nav id="encorSampleSimNav" class="sim-nav encor-sample-sim-nav" aria-label="Sample navigation">
    {prev_el}
    <a class="sim-nav-btn sim-nav-home" href="/ccnp-home.html">Home</a>
    {next_el}
  </nav>
{script}
</body>
</html>
"""


def sample_needs_migration(text: str) -> bool:
    if "encor-static-sample" not in text or "question-shell" not in text:
        return True
    if '<a class="site-logo-corner"' in text:
        return True
    return False


def migrate_static_sample(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if not sample_needs_migration(text):
        return
    m = re.match(r"sample-question-(\d+)\.html$", path.name, re.I)
    if not m:
        return
    n = int(m.group(1))

    title_m = re.search(r"<title>([\s\S]*?)</title>", text, re.I)
    title = title_m.group(1).strip() if title_m else f"Sample question {n}"
    head_extras = extract_head_extras(text)

    main_raw = extract_main_content(text)
    name = parse_input_name(main_raw)
    _, choices_html, h1_html, is_choose_two = strip_old_chrome(main_raw)
    correct, correct_msg = parse_script_answers(text, is_choose_two)

    out = render_static_sample(
        n=n,
        title=title,
        h1_html=h1_html,
        choices_html=choices_html,
        name=name,
        is_choose_two=is_choose_two,
        correct=correct,
        correct_msg=correct_msg,
        head_extras=head_extras,
    )
    path.write_text(out, encoding="utf-8")


def migrate_file(path: Path, chain: list[int]) -> None:
    text = path.read_text(encoding="utf-8")
    if "encor-question-ui" in text and "question-shell" in text:
        return
    if 'class="drop-slot"' in text and 'draggable="true"' in text:
        return
    qid = int(re.match(r"question-(\d+)\.html$", path.name, re.I).group(1))
    title_m = re.search(r"<title>(.*?)</title>", text, re.S | re.I)
    title = title_m.group(1).strip() if title_m else f"Question {qid}"

    main_raw = extract_main_content(text)
    name = parse_input_name(main_raw)
    prepend, choices_html, h1_html, is_choose_two = strip_old_chrome(main_raw)
    correct, correct_msg = parse_script_answers(text, is_choose_two)
    extra_css = extract_exhibit_css(extract_first_style(text))

    idx = chain.index(qid)
    prev_id = chain[idx - 1] if idx > 0 else None
    next_id = chain[idx + 1] if idx + 1 < len(chain) else None

    out = render_page(
        qid=qid,
        title=title,
        prepend=prepend,
        h1_html=h1_html,
        choices_html=choices_html,
        name=name,
        is_choose_two=is_choose_two,
        correct=correct,
        correct_msg=correct_msg,
        extra_css=extra_css,
        prev_id=prev_id,
        next_id=next_id,
    )
    path.write_text(out, encoding="utf-8")


def main() -> int:
    chain = question_ids()
    errors: list[str] = []
    updated = 0
    skipped = 0
    for path in sorted(MCQ_DIR.glob("question-*.html")):
        try:
            before = path.read_text(encoding="utf-8")
            migrate_file(path, chain)
            after = path.read_text(encoding="utf-8")
            if before == after:
                skipped += 1
            else:
                updated += 1
        except Exception as exc:
            errors.append(f"{path.name}: {exc}")
    print(f"Bank: updated {updated}, skipped {skipped}, errors {len(errors)}")

    sample_updated = 0
    for path in sorted(SAMPLES_DIR.glob("sample-question-*.html")):
        try:
            before = path.read_text(encoding="utf-8")
            migrate_static_sample(path)
            after = path.read_text(encoding="utf-8")
            if before != after:
                sample_updated += 1
        except Exception as exc:
            errors.append(f"{path.name}: {exc}")

    print(f"Static samples updated: {sample_updated}")
    if errors:
        for line in errors[:20]:
            print(" ", line)
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

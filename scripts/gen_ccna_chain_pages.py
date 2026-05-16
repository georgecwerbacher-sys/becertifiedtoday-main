#!/usr/bin/env python3
"""One-off generator for CCNA question HTML pages (inline template)."""
from __future__ import annotations

import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "public/CCNA-Study/CCNA_questions"
# Topology / exhibit raster files live in OUT/images/ (see .cursor/rules/ccna-extra-question-chain.mdc).

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
      background: #0b1020;
      color: #e6edf3;
      padding: 16px;
      box-sizing: border-box;
    }
    .card {
      width: min(900px, 100%);
      background: #121a2b;
      border: 1px solid #2d3b5a;
      border-radius: 14px;
      padding: 28px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    }
    h1 {
      margin: 0 0 8px;
      font-size: clamp(1.05rem, 2vw, 1.45rem);
      line-height: 1.35;
    }
    h1.choose-two-stem {
      line-height: 1.5;
    }
    .stem-after-exhibit {
      margin: 12px 0 6px;
      font-size: clamp(1.02rem, 1.9vw, 1.32rem);
      line-height: 1.42;
      font-weight: 600;
      color: #e6edf3;
    }
    .stem-after-exhibit-list {
      margin: 8px 0 12px;
      padding-left: 1.35rem;
      font-size: clamp(1.02rem, 1.9vw, 1.32rem);
      line-height: 1.45;
      font-weight: 600;
      color: #e6edf3;
    }
    .stem-after-exhibit-list li {
      margin: 6px 0;
    }
    .stem-after-exhibit-tail {
      margin-top: 10px;
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
    .choice.mono.cli-router-choice {
      display: flex;
      flex-direction: column;
      padding: 0;
      border-radius: 10px;
      overflow: hidden;
      border: 1px solid #2a3f5c;
      background: linear-gradient(180deg, rgba(26, 37, 59, 0.95), rgba(10, 16, 28, 0.98));
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.06);
    }
    .cli-router-choice-controls {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px;
      padding: 8px 12px;
      background: rgba(15, 22, 40, 0.95);
      border-bottom: 1px solid #2a3f5c;
    }
    .cli-router-choice-controls input {
      margin-right: 0;
      transform: none;
      flex-shrink: 0;
    }
    .cli-router-choice-badge {
      flex: 0 0 auto;
      min-width: 1.5rem;
      text-align: center;
      padding: 2px 7px;
      border-radius: 6px;
      font-weight: 800;
      font-size: 0.78rem;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      background: rgba(37, 75, 138, 0.55);
      border: 1px solid rgba(93, 140, 220, 0.45);
      color: #e6edf3;
    }
    .cli-router-choice-title {
      flex: 1 1 auto;
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: #8b9cc4;
    }
    pre.cli-router-console {
      margin: 0;
      padding: 12px 14px;
      background: #060a11;
      color: #c8dcf0;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.78rem;
      line-height: 1.42;
      white-space: pre-wrap;
      word-break: break-word;
      overflow-x: auto;
      border-left: 3px solid #c9a227;
      min-height: 2rem;
    }
    .choice input {
      margin-right: 10px;
      transform: translateY(1px);
    }
    .actions {
      margin-top: 18px;
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
    }
    .actions button {
      background: #254b8a;
      color: #e6edf3;
      border: 1px solid #3d6dbb;
      border-radius: 10px;
      padding: 10px 16px;
      font-weight: 700;
      cursor: pointer;
      font-family: inherit;
      font-size: 0.95rem;
    }
    .actions button:hover {
      filter: brightness(1.08);
    }
    .home-link {
      margin-left: auto;
      background: #254b8a;
      color: #e6edf3;
      border: 1px solid #3d6dbb;
      border-radius: 10px;
      padding: 10px 14px;
      font-weight: 700;
      text-decoration: none;
      font-size: 0.95rem;
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
    .next-wrap {
      margin-top: 18px;
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
    }
    .next-link {
      display: inline-block;
      text-decoration: none;
      color: #e6edf3;
      background: #254b8a;
      border: 1px solid #3d6dbb;
      border-radius: 10px;
      padding: 10px 16px;
      font-weight: 700;
    }
    .next-link:hover {
      filter: brightness(1.08);
    }
    .exhibit-stack {
      margin: 14px 0 18px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    figure.exhibit-photo {
      margin: 0;
      border-radius: 10px;
      border: 1px solid #2d3b5a;
      overflow: hidden;
      background: #0d1320;
    }
    figure.exhibit-photo img {
      width: 100%;
      height: auto;
      vertical-align: middle;
      display: block;
    }
    figure.exhibit-photo figcaption {
      padding: 6px 10px;
      font-size: 0.78rem;
      color: #8b9cc4;
      border-top: 1px solid #2d3b5a;
      background: #0f1628;
    }
    .cli-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 12px;
    }
    @media (min-width: 720px) {
      .cli-grid.two-cols {
        grid-template-columns: 1fr 1fr;
        align-items: stretch;
      }
    }
    .cli-device {
      border-radius: 10px;
      border: 1px solid #2d3b5a;
      background: #0d1320;
      overflow: hidden;
      min-height: 0;
    }
    .cli-device h2 {
      margin: 0;
      padding: 8px 12px;
      font-size: 0.8rem;
      font-weight: 700;
      letter-spacing: 0.03em;
      text-transform: uppercase;
      background: #1a253b;
      border-bottom: 1px solid #2d3b5a;
      color: #b6c8e8;
    }
    .cli-device pre {
      margin: 0;
      padding: 12px 14px;
      font-size: 0.72rem;
      line-height: 1.4;
      overflow-x: auto;
      white-space: pre;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      color: #e6edf3;
    }
    .cli-device pre + pre {
      border-top: 1px solid #2d3b5a;
    }
    .exhibit-terminal-white {
      margin: 0;
      border-radius: 10px;
      border: 1px solid #b8b8b8;
      overflow: hidden;
      background: #ffffff;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
    }
    .exhibit-terminal-white pre {
      margin: 0;
      padding: 14px 16px;
      font-size: 0.78rem;
      line-height: 1.45;
      overflow-x: auto;
      white-space: pre;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      color: #0a0a0a;
      background: #ffffff;
      tab-size: 8;
    }
    .exhibit-router-cli {
      margin: 0;
      border-radius: 10px;
      border: 1px solid #2a2a2a;
      overflow: hidden;
      background: #0a0a0a;
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04), 0 4px 18px rgba(0, 0, 0, 0.45);
    }
    .exhibit-router-cli pre {
      margin: 0;
      padding: 14px 16px;
      font-size: 0.72rem;
      line-height: 1.42;
      overflow-x: auto;
      white-space: pre;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      color: #f0f0f0;
      background: #0a0a0a;
      tab-size: 8;
    }
  </style>"""


def page(
    *,
    title: str,
    slug: str,
    stem: str,
    choices_html: str,
    name: str,
    correct: str,
    explain: str,
    prev_slug: str | None,
    next_slug: str | None,
    mono_choices: bool = False,
    post_stem_html: str | None = None,
    stem_after_exhibit: str | None = None,
    stem_after_exhibit_bullets: list[str] | None = None,
    stem_after_exhibit_tail: str | None = None,
    prepend_html: str | None = None,
    stem_br: bool = False,
) -> str:
    mono = " mono" if mono_choices else ""
    prev_h = (
        f'<a class="next-link" href="/CCNA-Study/CCNA_questions/{prev_slug}.html">Previous question</a>'
        if prev_slug
        else ""
    )
    next_h = (
        f'<a class="next-link" href="/CCNA-Study/CCNA_questions/{next_slug}.html">Next question</a>'
        if next_slug
        else ""
    )
    nav_lines = ["    <div class=\"next-wrap\">"]
    if prev_h:
        nav_lines.append(f"      {prev_h}")
    if next_h:
        nav_lines.append(f"      {next_h}")
    nav_lines.append("    </div>")
    nav = "\n".join(nav_lines)
    msg_json = json.dumps(explain)
    exhibit_block = post_stem_html if post_stem_html else ""
    stem_h = html.escape(stem)
    if stem_br:
        stem_h = stem_h.replace("\n", "<br />")
    if post_stem_html and stem_after_exhibit:
        if stem_after_exhibit_bullets:
            bullet_lines = "".join(
                f"      <li>{html.escape(b)}</li>\n" for b in stem_after_exhibit_bullets
            )
            tail_p = ""
            if stem_after_exhibit_tail:
                tail_p = (
                    f'    <p class="stem-after-exhibit stem-after-exhibit-tail">'
                    f"{html.escape(stem_after_exhibit_tail)}</p>\n"
                )
            main_open = (
                f"    <h1>{stem_h}</h1>\n"
                f"{exhibit_block}\n"
                f'    <p class="stem-after-exhibit">{html.escape(stem_after_exhibit)}</p>\n'
                f'    <ul class="stem-after-exhibit-list">\n'
                f"{bullet_lines}"
                f"    </ul>\n"
                f"{tail_p}"
            )
        else:
            main_open = (
                f"    <h1>{stem_h}</h1>\n"
                f"{exhibit_block}\n"
                f'    <p class="stem-after-exhibit">{html.escape(stem_after_exhibit)}</p>\n'
            )
    else:
        main_open = f"    <h1>{stem_h}</h1>\n{exhibit_block}\n"
    if prepend_html:
        main_open = f"{prepend_html.rstrip()}\n{main_open}"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="robots" content="noindex, nofollow" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
{STYLE}
  <link rel="stylesheet" href="/CCNA-Study/CCNA_Samples/ccna-sample-touch.css" />
</head>
<body>
  <script src="/js/sample-url-mask-apply.js"></script>
  <script src="/CCNA-Study/js/ccna-practice-100-nav.js" defer></script>
  <main class="card">
{main_open}{choices_html}

    <div class="actions">
      <a class="home-link" href="/index.html">Home</a>
    </div>

    <div id="answerBox" class="answer" aria-live="polite"></div>

{nav}
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


def checkbox_choice_line(name: str, letter: str, text: str) -> str:
    return f'    <label class="choice"><input type="checkbox" name="{name}" value="{letter}" />{letter}. {text}</label>'


def checkbox_choice_line_mono(name: str, letter: str, text: str) -> str:
    body = html.escape(f"{letter}. {text}", quote=False)
    return (
        "\n".join(
            [
                '    <label class="choice mono cli-router-choice">',
                '      <span class="cli-router-choice-controls">',
                f'        <input type="checkbox" name="{name}" value="{letter}" aria-label="Select answer option {letter}" />',
                f'        <span class="cli-router-choice-badge" aria-hidden="true">{html.escape(letter)}</span>',
                '        <span class="cli-router-choice-title">Switch CLI — candidate config</span>',
                "      </span>",
                f'      <pre class="cli-router-console">{body}</pre>',
                "    </label>",
            ]
        )
        + "\n"
    )


def format_checkbox_stem(stem: str) -> str:
    """HTML-escape stem and preserve intentional line breaks for choose-two pages."""
    return html.escape(stem, quote=False).replace("\n", "<br />")


def page_checkbox(
    *,
    title: str,
    slug: str,
    stem: str,
    choices_html: str,
    name: str,
    correct_letters: list[str],
    explain: str,
    prev_slug: str | None,
    next_slug: str | None,
    post_stem_html: str | None = None,
    stem_after_exhibit: str | None = None,
    prepend_html: str | None = None,
) -> str:
    prev_h = (
        f'<a class="next-link" href="/CCNA-Study/CCNA_questions/{prev_slug}.html">Previous question</a>'
        if prev_slug
        else ""
    )
    next_h = (
        f'<a class="next-link" href="/CCNA-Study/CCNA_questions/{next_slug}.html">Next question</a>'
        if next_slug
        else ""
    )
    nav_lines = ['    <div class="next-wrap">']
    if prev_h:
        nav_lines.append(f"      {prev_h}")
    if next_h:
        nav_lines.append(f"      {next_h}")
    nav_lines.append("    </div>")
    nav = "\n".join(nav_lines)
    cor_json = json.dumps(sorted(correct_letters))
    msg_json = json.dumps(explain)
    exhibit_block = post_stem_html if post_stem_html else ""
    stem_inner = format_checkbox_stem(stem)
    if post_stem_html and stem_after_exhibit:
        main_open = (
            f'    <h1 class="choose-two-stem">{stem_inner}</h1>\n'
            f"{exhibit_block}\n"
            f'    <p class="stem-after-exhibit">{html.escape(stem_after_exhibit)}</p>\n'
        )
    elif post_stem_html:
        main_open = (
            f'    <h1 class="choose-two-stem">{stem_inner}</h1>\n'
            f"{exhibit_block}\n"
        )
    else:
        main_open = f'    <h1 class="choose-two-stem">{stem_inner}</h1>\n'
    if prepend_html:
        main_open = f"{prepend_html.rstrip()}\n{main_open}"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="robots" content="noindex, nofollow" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
{STYLE}
  <link rel="stylesheet" href="/CCNA-Study/CCNA_Samples/ccna-sample-touch.css" />
</head>
<body>
  <script src="/js/sample-url-mask-apply.js"></script>
  <script src="/CCNA-Study/js/ccna-practice-100-nav.js" defer></script>
    <main class="card">
{main_open}
{choices_html}

    <div class="actions">
      <button id="checkBtn" type="button">Check answer</button>
      <a class="home-link" href="/index.html">Home</a>
    </div>

    <div id="answerBox" class="answer" aria-live="polite"></div>

{nav}
  </main>

  <script>
    (function () {{
      var CORRECT = {cor_json};
      var checkBtn = document.getElementById("checkBtn");
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
          answerBox.textContent = {msg_json};
        }} else {{
          answerBox.className = "answer incorrect";
          answerBox.textContent = "Incorrect.";
        }}
      }});
    }})();
  </script>
</body>
</html>
"""


def choice_line(mono: bool, name: str, letter: str, text: str) -> str:
    if mono:
        body = html.escape(f"{letter}. {text}", quote=False)
        return (
            "\n".join(
                [
                    '    <label class="choice mono cli-router-choice">',
                    '      <span class="cli-router-choice-controls">',
                    f'        <input type="radio" name="{name}" value="{letter}" aria-label="Select answer option {letter}" />',
                    f'        <span class="cli-router-choice-badge" aria-hidden="true">{html.escape(letter)}</span>',
                    '        <span class="cli-router-choice-title">Router CLI — candidate config</span>',
                    "      </span>",
                    f'      <pre class="cli-router-console">{body}</pre>',
                    "    </label>",
                ]
            )
            + "\n"
        )
    return f'    <label class="choice"><input type="radio" name="{name}" value="{letter}" />{letter}. {html.escape(text, quote=False)}</label>'


def main() -> None:
    chain = [
        {
            "slug": "dhcp-relay-dhcpdiscover",
            "title": "CCNA — DHCP relay and DHCPDISCOVER",
            "stem": "A network administrator must enable DHCP services between two sites. What must be configured for the router to pass DHCPDISCOVER messages on to the server?",
            "name": "dhcp",
            "correct": "A",
            "explain": "Correct. A — A DHCP relay agent (Cisco: ip helper-address pointing at the DHCP server) forwards DHCP broadcasts as unicast to the server. A DHCP pool is on the server; DHCP snooping is a switch security feature; bindings are lease state.",
            "choices": [
                "a DHCP Relay Agent",
                "DHCP Binding",
                "a DHCP Pool",
                "DHCP Snooping",
            ],
        },
        {
            "slug": "arp-first-ping-switch-flood",
            "title": "CCNA — ARP broadcast on a switch",
            "stem": "Refer to the exhibit. PC1 is trying to ping PC3 for the first time and sends out an ARP to S1. Which action is taken by S1? (Assume PC1 is on the port excluded in the correct answer.)",
            "name": "arpf",
            "correct": "B",
            "explain": "Correct. B — An ARP request is a Layer 2 broadcast. The switch floods it out all other ports in the same VLAN except the ingress port. Pick the option that matches flooding with the exhibit’s ingress port excluded.",
            "choices": [
                "It forwards it out G0/3 only",
                "It is flooded out every port except G0/0",
                "It drops the frame",
                "It forwards it out interface G0/2 only",
            ],
        },
        {
            "slug": "stp-bpduguard-portfast-errdisable",
            "title": "CCNA — BPDU Guard and err-disable",
            "stem": "Refer to the exhibit. What is the result if Gig1/11 receives an STP BPDU?",
            "name": "bpdug",
            "correct": "D",
            "explain": "Correct. D — BPDU Guard on a PortFast access port treats an incoming BPDU as an error and puts the port into err-disabled. It does not simply transition to normal STP blocking as the primary outcome.",
            "choices": [
                "The port transitions to STP blocking",
                "The port transitions to the root port",
                "The port immediately transitions to STP forwarding",
                "The port goes into error-disable state",
            ],
        },
        {
            "slug": "stp-root-bridge-vlan110",
            "title": "CCNA — STP root bridge for VLAN 110",
            "stem": "Refer to the exhibit. Which switch becomes the root of the spanning tree for VLAN 110?",
            "name": "stproot110",
            "correct": "B",
            "explain": "Correct. B — The root bridge has the lowest bridge ID. Compare the priority values first (24586 is lower than 28682, 32778, and 64000), so Switch 2 becomes the STP root for VLAN 110.",
            "choices": [
                "Switch 1",
                "Switch 2",
                "Switch 3",
                "Switch 4",
            ],
        },
        {
            "slug": "trunk-native-vlan-untagged",
            "title": "CCNA — Trunk native VLAN",
            "stem": "An engineer must configure traffic for a VLAN that is untagged by the switch as it crosses a trunk link. Which command should be used?",
            "name": "native",
            "correct": "B",
            "explain": "Correct. B — On an 802.1Q trunk, the native VLAN is sent untagged; set it with switchport trunk native vlan. allowed vlan restricts membership; mode trunk enables the trunk; encapsulation dot1q selects encapsulation where relevant.",
            "choices": [
                "switchport trunk allowed vlan 10",
                "switchport trunk native vlan 10",
                "switchport mode trunk",
                "switchport trunk encapsulation dot1q",
            ],
        },
        {
            "slug": "wan-t1-bandwidth",
            "title": "CCNA — T1 line rate",
            "stem": "What is the maximum bandwidth of a T1 point-to-point connection?",
            "name": "t1",
            "correct": "A",
            "explain": "Correct. A — T1 is 1.544 Mbps. 2.048 Mbps is E1; 34.368 Mbps is in the E3 range; ~44 Mbps is T3 territory.",
            "choices": [
                "1.544 Mbps",
                "2.048 Mbps",
                "34.368 Mbps",
                "43.7 Mbps",
            ],
        },
        {
            "slug": "wireless-rrm-channel-overlap",
            "title": "CCNA — Cisco unified wireless and channels",
            "stem": "How does a Cisco Unified Wireless network respond to Wi-Fi channel overlap?",
            "name": "rrm",
            "correct": "D",
            "explain": "Correct. D — RRM (Radio Resource Management), including dynamic channel assignment, analyzes RF conditions and assigns channels to reduce overlap. Manual per-AP channel is possible but is not the described automatic response.",
            "choices": [
                "It alternates automatically between 2.4 GHz and 5 GHz on adjacent access points",
                "It allows the administrator to assign channels on a per-device or per-interface basis",
                "It segregates devices from different manufacturers onto different channels",
                "It analyzes client load and background noise and dynamically assigns a channel",
            ],
        },
        {
            "slug": "wlan-design-nonoverlapping-2-4-channels-1-6-11",
            "title": "CCNA — WLAN infrastructure channel design",
            "stem": "What is recommended for the wireless infrastructure design of an organization?",
            "name": "wlandes1",
            "correct": "B",
            "explain": "Correct. B — In 2.4 GHz, channels 1, 6, and 11 are the common non-overlapping set; assigning them across nearby access points limits adjacent-channel interference. Clustering APs on one channel (A) increases contention, not throughput. Adjacent APs should not share the same channel when they hear each other (D). Non-overlapping channels mainly control interference; \u201cload balancing\u201d alone is a weak match for why channels differ (C).",
            "choices": [
                "group access points together to increase throughput on a given channel",
                "configure the first three access points to use channels 1, 6, and 11",
                "include at least two access points on nonoverlapping channels to support load balancing",
                "assign physically adjacent access points to the same Wi-Fi channel",
            ],
        },
        {
            "slug": "wlan-nonoverlapping-channels-discontinuous-frequency",
            "title": "CCNA — Nonoverlapping Wi-Fi channels requirement",
            "stem": "What is a requirement for nonoverlapping Wi-Fi channels?",
            "name": "wifinonov1",
            "correct": "C",
            "explain": "Correct. C \u2014 Nonoverlapping channels are channel numbers whose center frequencies are far enough apart that their modulated bandwidths do not interfere; that is a property of sufficiently separated (discontinuous) frequency ranges. Security profiles (A), PHY data rates (B), and SSID strings (D) do not define whether two channel assignments overlap in spectrum.",
            "choices": [
                "different security settings",
                "different transmission speeds",
                "discontinuous frequency ranges",
                "unique SSIDs",
            ],
        },
        {
            "slug": "switch-mac-table-ingress-learning",
            "title": "CCNA — MAC address table learning",
            "stem": "What does a switch use to build its MAC address table?",
            "name": "maclearn",
            "correct": "D",
            "explain": "Correct. D — The switch learns source MAC addresses from frames received (ingress) on each port. VTP and DTP are unrelated to MAC learning.",
            "choices": [
                "VTP",
                "DTP",
                "egress traffic",
                "ingress traffic",
            ],
        },
        {
            "slug": "control-plane-routing-decisions",
            "title": "CCNA — Control plane",
            "stem": "Which network plane is centralized and manages routing decisions?",
            "name": "cp",
            "correct": "B",
            "explain": "Correct. B — The control plane runs routing protocols and builds routing/forwarding information (routing decisions). The data plane forwards traffic; the management plane handles administration access.",
            "choices": [
                "policy plane",
                "control plane",
                "management plane",
                "data plane",
            ],
        },
        {
            "slug": "ios-dns-lookup-default-behavior",
            "title": "CCNA — IOS default DNS lookup",
            "stem": "What does a router do when configured with the default DNS lookup settings, and a URL is entered on the CLI?",
            "name": "dns",
            "correct": "D",
            "explain": "Correct. D — With ip domain-lookup enabled by default, a mistyped or unknown token can trigger a DNS lookup; without configured name servers, the router may use a broadcast DNS query. Lookups time out; they do not run forever.",
            "choices": [
                "initiates a ping request to the URL",
                "prompts the user to specify the desired IP address",
                "continuously attempts to resolve the URL until the command is cancelled",
                "sends a broadcast message in an attempt to resolve the URL",
            ],
        },
        {
            "slug": "dns-lookup-operation-definition",
            "title": "CCNA — DNS lookup operation",
            "stem": "What is a DNS lookup operation?",
            "name": "dnslkop1",
            "correct": "D",
            "explain": "Correct. D — A DNS lookup is the process where a resolver sends a query to a DNS server and the server returns the answer records (most often mapping a hostname to an IPv4/IPv6 address in forward lookups). The option wording reverses \u201cname\u201d and \u201cIP\u201d in places, but it is the only choice that describes that query/response resolution behavior. A states that DNS uses destination port 53, which is true of the service, but it is not the definition of a lookup. B and C are not standard DNS lookup behavior.",
            "choices": [
                "serves requests over destination port 53",
                "DNS server pings the destination to verify that it is available",
                "DNS server forwards the client to an alternate IP address when the primary IP is down",
                "responds to a request for IP address to domain name resolution to the DNS server",
            ],
        },
        {
            "slug": "voice-data-vlan-access-ports-sw11",
            "title": "CCNA — Voice and data VLANs on access ports",
            "stem": "Refer to the exhibit. An administrator must configure interfaces Gi1/1 and Gi1/3 on switch SW11. PC-1 and PC-2 must be placed in the Data VLAN and Phone-1 must be placed in the Voice VLAN. Which configuration meets these requirements?",
            "name": "voicevlan",
            "correct": "C",
            "explain": "Correct. C — Gi1/1 is access VLAN 8 for PC-1 (data). Gi1/3 is access with access VLAN 8 for PC-2 and voice VLAN 9 for the IP phone. Option A reverses data/voice VLANs on Gi1/3. B and D use switchport mode trunk on Gi1/3 instead of the usual access + voice VLAN pattern.",
            "choices": [
                "A: Gi1/1 access vlan 8; Gi1/3 access vlan 9, voice vlan 8 (see question page CLI)",
                "B: Gi1/1 access vlan 9; Gi1/3 trunk + voice/access (see question page CLI)",
                "C: Gi1/1 access vlan 8; Gi1/3 access vlan 8, voice vlan 9 (see question page CLI)",
                "D: Gi1/1 access vlan 8; Gi1/3 trunk + voice/access (see question page CLI)",
            ],
        },
        {
            "slug": "pat-vlan200-inside-source-overload",
            "title": "CCNA — PAT and NAT extended ACL",
            "stem": "Refer to the exhibit. Which configuration must be applied to the router so PAT translates addresses in VLAN 200 while devices on VLAN 100 use their own IP addresses? Choose the option that matches the correct full configuration block.",
            "name": "pat",
            "correct": "D",
            "explain": "Correct. D — In the exhibit, VLAN 200 is 192.168.100.32/27, so the standard ACE is permit 192.168.100.32 0.0.0.31. That matches only VLAN 200; VLAN 100 (192.168.100.0/27) is not translated. Option C’s 192.168.100.0 0.0.0.255 would also translate VLAN 100. A and B use a public address in the permit. See question page for full CLI blocks.",
            "choices": [
                "A: ACL permit 209.165.201.2 / PAT overload / nat inside on Gi2/0/1.100 & .200; outside Gi1/0/0 (see page)",
                "B: ACL permit with subnet mask instead of wildcard + same NAT (see page)",
                "C: ACL permit 192.168.100.0 0.0.0.255 + same NAT (see page)",
                "D: ACL permit 192.168.100.32 0.0.0.31 + same NAT (see page)",
            ],
            "mono": True,
        },
        {
            "slug": "switch-unknown-unicast-flood",
            "title": "CCNA — Unknown destination MAC flooding",
            "stem": "How does a switch process a frame received on Fa0/1 with the destination MAC address of 0e38.7363.657b when the table is missing the address?",
            "name": "unk",
            "correct": "A",
            "explain": "Correct. A — Unknown unicast destination MAC causes flooding to all other ports in the VLAN except the ingress port. The switch does not drop, buffer until MAC timeout, or send only back out Fa0/1.",
            "choices": [
                "It floods the frame to all interfaces except Fa0/1.",
                "It forwards the frame back out of interface Fa0/1.",
                "It drops the frame immediately.",
                "It holds the frame until the MAC address timer expires and then drops the frame.",
            ],
        },
        {
            "slug": "vrrp-gateway-redundancy-benefit",
            "title": "CCNA — VRRP benefit",
            "stem": "What is a benefit of VRRP?",
            "name": "vrrp",
            "correct": "B",
            "explain": "Correct. B — VRRP (Virtual Router Redundancy Protocol) groups multiple routers as one virtual default gateway (shared virtual IP/MAC) so clients keep the same gateway if the master fails. It is not load balancing across arbitrary multi-hop paths (A), not a routing-protocol neighbor exchange (C), and not STP (D).",
            "choices": [
                "It provides traffic load balancing to destinations that are more than two hops from the source.",
                "It provides the default gateway redundancy on a LAN using two or more routers.",
                "It allows neighbors to share routing table information between each other.",
                "It prevents loops in a Layer 2 LAN by forwarding all traffic to a root bridge, which then makes the final forwarding decision.",
            ],
        },
        {
            "slug": "dhcp-ipv4-assigned-by-protocol",
            "title": "CCNA — DHCP for dynamic IPv4",
            "stem": "Which protocol does an IPv4 host use to obtain a dynamically assigned IP address?",
            "name": "dhcpip",
            "correct": "D",
            "explain": "Correct. D — DHCP assigns IPv4 addresses (and common options such as mask, default router, DNS). ARP resolves Layer 2 addresses; DNS resolves names; CDP is Cisco device discovery.",
            "choices": ["ARP", "DNS", "CDP", "DHCP"],
        },
        {
            "slug": "dhcp-pool-default-router-command",
            "title": "CCNA — DHCP pool default router",
            "stem": "When DHCP is configured on a router, which command must be entered so the default gateway is automatically distributed?",
            "name": "dhcprtr",
            "correct": "A",
            "explain": "Correct. A — In an ip dhcp pool, default-router <address> sets DHCP Option 3. ip helper-address is for relay on an interface; dns-server sets DNS. default-gateway is not the pool subcommand.",
            "choices": [
                "default-router",
                "default-gateway",
                "ip helper-address",
                "dns-server",
            ],
        },
        {
            "slug": "dhcp-relay-r4-fa01-acl100-exhibit",
            "title": "CCNA — DHCP relay and WAN ACL on R4",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "Which configuration enables DHCP addressing for hosts connected to interface FastEthernet0/1 on router R4?",
            "name": "dhcpr4fa1",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 Configure ip helper-address on the interface that faces DHCP clients (FastEthernet0/1 here) so broadcasts are relayed to the DHCP server at 10.0.1.1. Extended ACL 100 is applied inbound on FastEthernet0/10, so replies from the server must be permitted there: DHCP uses UDP, and a typical match is UDP from the server (source UDP bootps / 67) to the router\u2019s LAN address 10.148.2.1. Option A uses TCP. Options B and C attach the helper to FastEthernet0/0, which is not the client-facing interface in the exhibit, and B\u2019s ACE mixes invalid TCP-style syntax for bootps.",
            "post_stem_html": """    <div class="exhibit-stack">
      <div class="cli-device" role="region" aria-label="R4 partial running configuration">
        <h2>R4 (partial)</h2>
        <pre>interface FastEthernet0/10
 description WAN_INTERFACE
 ip address 10.0.1.2 255.255.255.252
 ip access-group 100 in
!
interface FastEthernet0/1
 description LAN INTERFACE
 ip address 10.148.2.1 255.255.255.0
 duplex auto
 speed auto
!
ip forward-protocol nd
!
access-list 100 permit eigrp any any
access-list 100 permit icmp any any
access-list 100 permit tcp 10.149.3.0 0.0.0.255 host 10.0.1.2 eq 22
access-list 100 permit tcp any any eq 80
access-list 100 permit tcp any any eq 443
access-list 100 deny ip any any log</pre>
      </div>
    </div>""",
            "choices": [
                """interface FastEthernet0/1
ip helper-address 10.0.1.1
!
access-list 100 permit tcp host 10.0.1.1 eq 67 host 10.148.2.1""",
                """interface FastEthernet0/0
ip helper-address 10.0.1.1
!
access-list 100 permit host 10.0.1.1 host 10.148.2.1 eq bootps""",
                """interface FastEthernet0/0
ip helper-address 10.0.1.1
!
access-list 100 permit udp host 10.0.1.1 eq bootps host 10.148.2.1""",
                """interface FastEthernet0/1
ip helper-address 10.0.1.1
!
access-list 100 permit udp host 10.0.1.1 eq bootps host 10.148.2.1""",
            ],
        },
        {
            "slug": "ospf-r14-r86-broadcast-dr-adjacency",
            "title": "CCNA — OSPFv2 broadcast adjacency and DR",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "Which configuration allows routers R14 and R86 to form an OSPFv2 adjacency while acting as a central point for exchanging OSPF information between routers?",
            "post_stem_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/ospf-r14-r86-fa0-topology.png" alt="Topology: R14 Fa0/0 linked to R86 Fa0/0 on 10.73.65.64/30; Loopback0 10.10.1.14/32 on R14 and 10.10.1.86/32 on R86." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "name": "ospfr1486",
            "correct": "B",
            "mono": True,
            "explain": "Correct. B \u2014 On a broadcast OSPF segment the designated router (DR) is the central point for reliable LS flooding on the LAN; with two routers, setting a higher OSPF priority on one router (255 on R14) makes it the DR while the neighbor becomes BDR, and both reach full adjacency. Cisco OSPFv2 also compares interface MTU during the database exchange: both sides use MTU 1500 here. Option A mismatches MTU (1400 vs 1500) so the adjacency typically stalls in EXSTART/EXCHANGE. Option D also mismatches MTU. Option C is invalid because ip ospf priority belongs under the interface, not under router ospf.",
            "choices": [
                """Option A

R14#
interface FastEthernet0/0
ip address 10.73.65.65 255.255.255.252
ip ospf network broadcast
ip ospf priority 0
ip mtu 1400

router ospf 10
router-id 10.10.1.14
network 10.10.1.14 0.0.0.0 area 0
network 10.73.65.64 0.0.0.3 area 0

R86#
interface Loopback0
ip address 10.10.1.86 255.255.255.255

interface FastEthernet0/0
ip address 10.73.65.66 255.255.255.252
ip ospf network broadcast
ip mtu 1500

router ospf 10
router-id 10.10.1.86
network 10.10.1.86 0.0.0.0 area 0
network 10.73.65.64 0.0.0.3 area 0""",
                """Option B

R14#
interface FastEthernet0/0
ip address 10.73.65.65 255.255.255.252
ip ospf network broadcast
ip ospf priority 255
ip mtu 1500

router ospf 10
router-id 10.10.1.14
network 10.10.1.14 0.0.0.0 area 0
network 10.73.65.64 0.0.0.3 area 0

R86#
interface FastEthernet0/0
ip address 10.73.65.66 255.255.255.252
ip ospf network broadcast
ip mtu 1500

router ospf 10
router-id 10.10.1.86
network 10.10.1.86 0.0.0.0 area 0
network 10.73.65.64 0.0.0.3 area 0""",
                """Option C

R14#
interface Loopback0
ip ospf 10 area 0

interface FastEthernet0/0
ip address 10.73.65.65 255.255.255.252
ip ospf network broadcast
ip ospf 10 area 0
ip mtu 1500

router ospf 10
ip ospf priority 255
router-id 10.10.1.14

R86#

interface Loopback0
ip ospf 10 area 0

interface FastEthernet0/0
ip address 10.73.65.66 255.255.255.252
ip ospf network broadcast
ip ospf 10 area 0
ip mtu 1500

router ospf 10
router-id 10.10.1.86""",
                """Option D

R14#
interface FastEthernet0/0
ip address 10.73.65.65 255.255.255.252
ip ospf network broadcast
ip ospf priority 255
ip mtu 1500

router ospf 10
router-id 10.10.1.14
network 10.10.1.14 0.0.0.0 area 0
network 10.73.65.64 0.0.0.3 area 0

R86#
interface FastEthernet0/0
ip address 10.73.65.66 255.255.255.252
ip ospf network broadcast
ip mtu 1400

router ospf 10
router-id 10.10.1.86
network 10.10.1.86 0.0.0.0 area 0
network 10.73.65.64 0.0.0.3 area 0""",
            ],
        },
        {
            "slug": "native-vlan-security-separated",
            "title": "CCNA — Securing the native VLAN",
            "stem": "How is the native VLAN secured in a network?",
            "name": "natsec",
            "correct": "A",
            "explain": "Correct. A — Use a dedicated native VLAN ID that is not used for normal user or server traffic within your design (separate from other VLANs). Avoid leaving everything on default VLAN 1; native VLAN IDs should match on both ends of a trunk.",
            "choices": [
                "separate from other VLANs within the administrative domain",
                "give it a value in the private VLAN range",
                "assign it as VLAN 1",
                "configure it as a different VLAN ID on each end of the link",
            ],
        },
        {
            "slug": "stp-portfast-default-immediate-forwarding",
            "title": "CCNA — PortFast default for access ports",
            "stem": "Which command causes switch ports to enter the STP forwarding state immediately when a PC is connected on an access port? (Global configuration.)",
            "name": "pfastd",
            "correct": "A",
            "explain": "Correct. A — spanning-tree portfast default enables PortFast by default on nontrunking (access) ports so they skip listening/learning. spanning-tree portfast trunk targets trunks; no spanning-tree portfast disables PortFast. Option B adds BPDU Guard defaults, not the core requirement.",
            "choices": [
                "switch(config)#spanning-tree portfast default",
                "switch(config)#spanning-tree portfast bpduguard default",
                "switch(config-if)#spanning-tree portfast trunk",
                "switch(config-if)#no spanning-tree portfast",
            ],
            "mono": True,
        },
        {
            "slug": "wireless-wpa2-aes-strongest",
            "title": "CCNA — Strongest wireless encryption among choices",
            "stem": "Which implementation provides the strongest encryption combination for the wireless environment?",
            "name": "wpastr",
            "correct": "A",
            "explain": "Correct. A — WPA2 with AES (CCMP) is the strongest listed. WEP is obsolete. WPA with TKIP is weaker than AES. WPA with AES is better than TKIP-only WPA but WPA2+AES is preferred here.",
            "choices": ["WPA2 + AES", "WPA + AES", "WEP", "WPA + TKIP"],
        },
        {
            "slug": "vm-shared-disk-resource",
            "title": "CCNA — Shared resource on a hypervisor",
            "stem": "Which resource is able to be shared among virtual machines deployed on the same physical server?",
            "name": "vmdisk",
            "correct": "D",
            "explain": "Correct. D — VMs share underlying physical hardware including storage (disks or shared datastores). Each VM typically has its own guest OS, applications, and VM configuration file.",
            "choices": ["applications", "operating system", "VM configuration file", "disk"],
        },
        {
            "slug": "soho-broadband-shared-connection",
            "title": "CCNA — SOHO network characteristic",
            "stem": "What is a characteristic of a SOHO network?",
            "name": "soho",
            "correct": "B",
            "explain": "Correct. B — SOHO sites usually use one broadband connection shared by several users or devices behind a small router or firewall. Full mesh switching, thousands of users, and three-tier datacenter designs are enterprise-scale, not SOHO.",
            "choices": [
                "connects each switch to every other switch in the network",
                "enables multiple users to share a single broadband connection",
                "provides high throughput access for 1000 or more users",
                "includes at least three tiers of devices to provide load balancing and redundancy",
            ],
        },
        {
            "slug": "snmp-trap-mib-requirement",
            "title": "CCNA — SNMP trap and MIB",
            "stem": "Which condition must be met before an NMS handles an SNMP trap from an agent?",
            "name": "snmpmib",
            "correct": "C",
            "explain": "Correct. C — The NMS needs the MIB definitions for the OIDs in the trap to interpret them meaningfully. The manager does not have to be on the same router, does not need both trap and inform in an interval, and does not need duplicate traps from two agents.",
            "choices": [
                "The NMS must be configured on the same router as the SNMP agent",
                "The NMS must receive a trap and an inform message from the SNMP agent within a configured interval",
                "The NMS software must be loaded with the MIB associated with the trap",
                "The NMS must receive the same trap from two different SNMP agents to verify that it is reliable",
            ],
        },
        {
            "slug": "standard-acl-permit-deny-two-subnets",
            "title": "CCNA — Standard ACL for two interfaces",
            "stem": "Refer to the exhibit (standard ACL 99, permit 10.100.100.0/24, deny Gi0/1 subnet). An access list is required to permit traffic from any host on interface G0/0 and deny traffic from interface Gi0/1. Which access list must be applied?",
            "name": "stdacl",
            "correct": "A",
            "explain": "Correct. A — Option A uses ACL 99 (valid standard range), permits 10.100.100.0/24, and denies 192.168.0.0 0.0.255.255 (all 192.168.x.x). Option B’s wildcard 0.255.255.255 matches all 192.0.0.0/8, which is too broad. Option C uses standard ACL 100 (invalid—100–199 is extended). Option D uses 199 in the extended range as “standard,” which is invalid.",
            "choices": [
                "Option A: ip access-list standard 99 — permit 10.100.100.0 0.0.0.255 — deny 192.168.0.0 0.0.255.255",
                "Option B: ip access-list standard 99 — permit 10.100.100.0 0.0.0.255 — deny 192.168.0.0 0.255.255.255",
                "Option C: ip access-list standard 100 — permit 10.100.100.0 0.0.0.255 — deny 192.168.0.0 0.255.255.255",
                "Option D: ip access-list standard 199 — permit 10.100.100.0 0.0.0.255 — deny 192.168.0.0 0.0.255.255",
            ],
            "mono": True,
        },
        {
            "slug": "netconf-xml-filter-get-config",
            "title": "CCNA — NETCONF filter to limit reply",
            "stem": "After running ncclient code to connect to a NETCONF server, which step reduces the amount of data the server returns so the client receives only the interface configuration?",
            "name": "ncfilt",
            "correct": "B",
            "explain": "Correct. B — Pass an XML subtree filter to get_config (or equivalent) so the server returns only the requested YANG subtree. Parsing with XML or JSON libraries happens after data is received and does not reduce what the server sends. JSON filters are not used for NETCONF get_config filtering.",
            "choices": [
                "Use the xml library to parse the data returned by the NETCONF server for the interface’s configuration.",
                "Create an XML filter as a string and pass it to get_config() method as an argument.",
                "Create a JSON filter as a string and pass it to the get_config() method as an argument.",
                "Use the JSON library to parse the data returned by the NETCONF server for the interface’s configuration.",
            ],
        },
        {
            "slug": "sdn-controller-functions-choose-two",
            "title": "CCNA — SDN controller functions (choose two)",
            "stem": "What are two functions of an SDN controller? (Choose two)",
            "name": "sdnfn",
            "choose_two": True,
            "correct": ["A", "D"],
            "explain": "Correct. A and D — The controller coordinates virtual tenant networks (VTNs) and manages topology and centralized control. Layer 2 forwarding is a data-plane switch function. Tracking hosts alone is not the paired answer on this item. DDoS mitigation may be an application but is not one of the two listed core functions here.",
            "choices": [
                "coordinating VTNs",
                "Layer 2 forwarding",
                "tracking hosts",
                "managing the topology",
                "protecting against DDoS attacks",
            ],
        },
        {
            "slug": "switch-egress-queue-during-transmit",
            "title": "CCNA — Queuing when port is transmitting",
            "stem": "If a switch port receives a new frame while it is actively transmitting a previous frame, how does it process the frames?",
            "name": "egq",
            "correct": "D",
            "explain": "Correct. D — The new frame is queued for transmission after the current frame finishes. Ethernet does not drop the previous frame and request L2 retransmission in this way, does not send the new frame first, and cannot transmit two frames on the same path at once.",
            "choices": [
                "The previous frame is delivered, the new frame is dropped, and a retransmission request is sent.",
                "The new frame is delivered first, the previous frame is dropped, and a retransmission request is sent.",
                "The two frames are processed and delivered at the same time.",
                "The new frame is placed in a queue for transmission after the previous frame.",
            ],
        },
        {
            "slug": "wan-topology-point-to-point-simplicity",
            "title": "CCNA — WAN topology tradeoffs",
            "stem": "Which WAN topology provides a combination of simplicity, quality, and availability?",
            "name": "wanppt",
            "correct": "C",
            "explain": "Correct. C — A point-to-point link between two sites is simple, offers predictable performance, and is often sold with SLAs for availability. Full mesh is complex and costly; hub-and-spoke can bottleneck at the hub; partial mesh is a compromise.",
            "choices": ["partial mesh", "full mesh", "point-to-point", "hub-and-spoke"],
        },
        {
            "slug": "ntp-master-internal-clock-server",
            "title": "CCNA — NTP master on a router",
            "stem": "Router1 uses ntp server 192.168.0.3 as an NTP client of Router2. Which command must be configured on Router2 so it operates as an authoritative time source using only its internal clock?",
            "name": "ntpmst",
            "correct": "B",
            "explain": "Correct. B — ntp master <stratum> makes the router serve time from its software clock at the given stratum. ntp server on Router2 would make it a client upstream. ntp passive is not the usual answer for this scenario.",
            "choices": [
                "Router2(config)#ntp passive",
                "Router2(config)#ntp master 4",
                "Router2(config)#ntp server 172.17.0.1",
                "Router2(config)#ntp server 192.168.0.2",
            ],
            "mono": True,
        },
        {
            "slug": "trunk-allowed-vlan-add-no-disruption",
            "title": "CCNA — Add VLAN to trunk allow list",
            "stem": "Refer to the exhibit. A network engineer must enable communication between PC A and the File Server without interrupting other VLANs on the trunk. Which command must be configured?",
            "name": "trkadd",
            "correct": "C",
            "explain": "Correct. C — switchport trunk allowed vlan add 13 adds VLAN 13 to the existing allow list without removing other permitted VLANs. allowed vlan none would break all VLANs. remove 10–11 can cut valid traffic. Typo-only variants that replace the list with a single VLAN can drop other VLANs unless carefully scoped.",
            "choices": [
                "Switch trunk allowed vlan 12",
                "Switchport trunk allowed vlan none",
                "Switchport trunk allowed vlan add 13",
                "Switchport trunk allowed vlan remove 10-11",
            ],
            "mono": True,
        },
        {
            "slug": "sdn-southbound-api-purpose",
            "title": "CCNA — Southbound API",
            "stem": "What is the purpose of a southbound API in a control based networking architecture?",
            "name": "sbapi",
            "correct": "D",
            "explain": "Correct. D — Southbound interfaces let the controller program and read state from network devices (switches, routers, and similar hardware) using protocols such as NETCONF, RESTCONF, OpenFlow, or gRPC. Northbound APIs expose the controller to applications and orchestration above.",
            "choices": [
                "facilitates communication between the controller and the applications",
                "integrates a controller with other automation and orchestration tools",
                "allows application developers to interact with the network",
                "facilitates communication between the controller and the networking hardware",
            ],
        },
        {
            "slug": "err-disabled-port-security-violation",
            "title": "CCNA — Err-disabled and port security",
            "stem": "What causes a port to be placed in the err-disabled state?",
            "name": "errdis",
            "correct": "D",
            "explain": "Correct. D — With port security in shutdown violation mode (common default), a violation can err-disable the port. Latency and an empty port do not cause err-disable. shutdown is administrative down, not err-disabled.",
            "choices": [
                "latency",
                "nothing plugged into the port",
                "shutdown command issued on the port",
                "port security violation",
            ],
        },
        {
            "slug": "northbound-rest-sdn-applications",
            "title": "CCNA — Controller to applications",
            "stem": "Which technology is appropriate for communication between an SDN controller and applications running over the network?",
            "name": "nbapi",
            "correct": "D",
            "explain": "Correct. D — Northbound interfaces expose the controller to applications and orchestration; REST over HTTP/HTTPS is a common style. OpenFlow and NETCONF are typically southbound to devices. Southbound API is device-facing, not application-facing.",
            "choices": ["OpenFlow", "Southbound API", "NETCONF", "REST API"],
        },
        {
            "slug": "physical-access-badge-readers-datacenter",
            "title": "CCNA — Physical access and badges",
            "stem": "Which security program element involves installing badge readers on data-center doors to allow workers to enter and exit based on their job roles?",
            "name": "physbad",
            "correct": "A",
            "explain": "Correct. A — Door badge readers control physical entry; that is physical access control. Biometrics is a different factor. RBAC is mainly logical permissions to systems. MFA requires multiple factors and is not what door badges alone describe.",
            "choices": [
                "physical access control",
                "biometrics",
                "role-based access control",
                "multifactor authentication",
            ],
        },
        {
            "slug": "private-ipv4-characteristic-registration",
            "title": "CCNA — Private IPv4 characteristic",
            "stem": "What is a characteristic of private IPv4 addressing?",
            "name": "privch",
            "correct": "A",
            "explain": "Correct. A — RFC 1918 space is reused internally and is not uniquely registered for global Internet routing the way public addresses are; organizations use it with NAT at the edge. It is not issued per ASN like that, does not cross the Internet natively, and private space overall is far larger than a single /16.",
            "choices": [
                "used without tracking or registration",
                "issued by IANA in conjunction with an autonomous system number",
                "traverse the Internet when an outbound ACL is applied",
                "composed of up to 65,536 available addresses",
            ],
        },
        {
            "slug": "private-ipv4-appropriate-use-internal-only",
            "title": "CCNA — Appropriate use of private IPv4",
            "stem": "What is an appropriate use for private IPv4 addressing?",
            "name": "privuse1",
            "correct": "D",
            "explain": "Correct. D — RFC 1918 addresses are for internal networks that are not globally unique on the Internet; they suit hosts that only need to reach other internal systems. A public-facing firewall interface normally uses a public address. Outbound Internet access from private hosts relies on NAT or proxying, not private addressing by itself as the full story in B or C.",
            "choices": [
                "on the public-facing interface of a firewall",
                "to allow hosts inside to communicate in both directions with hosts outside the organization",
                "on internal hosts that stream data solely to external resources",
                "on hosts that communicate only with other internal hosts",
            ],
        },
        {
            "slug": "data-plane-forwarding-lookup",
            "title": "CCNA — Data plane action",
            "stem": "Which network action occurs within the data plane?",
            "name": "dplane",
            "correct": "A",
            "explain": "Correct. A — Per-packet destination lookup against forwarding information (often the FIB built from the routing table) is data-plane forwarding. NETCONF RPC handling and routing-protocol processes are control/management plane. Locally generated ICMP echo replies are often handled in software, not the main hardware forwarding path this item targets.",
            "choices": [
                "compare the destination IP address to the IP routing table",
                "make a configuration change from an incoming NETCONF RPC",
                "run routing protocols (OSPF, EIGRP, RIP, BGP)",
                "reply to an incoming ICMP echo request",
            ],
        },
        {
            "slug": "sdn-automation-improvements-choose-two",
            "title": "CCNA — SDN automation benefits (choose two)",
            "stem": "What are two improvements provided by automation for network management in an SDN environment? (Choose two)",
            "name": "sdnauto",
            "choose_two": True,
            "correct": ["B", "C"],
            "explain": "Correct. B and C — Telemetry and analytics build a baseline for behavior and capacity, and automated onboarding (templates, ZTP, controller workflows) reduces manual effort. AI/ML design prevention and proprietary API wording are not the usual paired answers here.",
            "choices": [
                "Artificial intelligence identifies and prevents potential design failures",
                "Data collection and analysis tools establish a baseline for the network",
                "New devices are onboarded with minimal effort",
                "Machine learning minimizes the overall error rate when automating troubleshooting processes",
                "Proprietary Cisco APIs leverage multiple network management tools",
            ],
        },
        {
            "slug": "ssh-crypto-rsa-key-generation",
            "title": "CCNA — SSH server key generation",
            "stem": "A network administrator must configure SSH for remote access to router R1. The requirement is to use a public and private key pair to encrypt management traffic to and from the connecting client. Which configuration, when applied, meets the requirements?",
            "name": "sshopt",
            "correct": "B",
            "explain": "Correct. B — SSH needs a host key pair; crypto key generate rsa modulus 1024 (prefer larger in production) is the standard IOS pattern with ip domain-name or hostname. EC options shown with keysize 1024/2048 do not match typical EC generate syntax. crypto key encrypt rsa name myKey is not the correct generate sequence.",
            "choices": [
                "Option A: crypto key generate ec keysize 1024 (after ip domain-name)",
                "Option B: crypto key generate rsa modulus 1024 (after ip domain-name)",
                "Option C: crypto key generate ec keysize 2048 (after ip domain-name)",
                "Option D: crypto key encrypt rsa name myKey (after ip domain-name)",
            ],
            "mono": True,
        },
        {
            "slug": "pki-components-crl-ca-choose-two",
            "title": "CCNA — PKI components (choose two)",
            "stem": "Which two components comprise part of a PKI? (Choose two)",
            "name": "pki2",
            "choose_two": True,
            "correct": ["C", "E"],
            "explain": "Correct. C and E \u2014 A public key infrastructure relies on trusted CAs that issue and sign certificates, and on revocation data such as Certificate Revocation Lists (CRLs) so relying parties can tell which certificates are no longer valid. RSA security tokens (A) are separate authenticators. Cleartext passwords (B) and preshared keys (D) are not core PKI elements.",
            "choices": [
                "RSA token",
                "clear-text password that authenticates connections",
                "one or more CRLs",
                "preshared key that authenticates connections",
                "CA that grants certificates",
            ],
        },
        {
            "slug": "sdn-southbound-openflow-forwarding",
            "title": "CCNA — Southbound protocol for forwarding",
            "stem": "What does an SDN controller use as a communication protocol to relay forwarding changes to a southbound API?",
            "name": "sbflow",
            "correct": "D",
            "explain": "Correct. D — OpenFlow is a common southbound protocol: the controller programs flow tables and forwarding behavior on infrastructure devices. REST is more typical northbound (applications to the controller). XML is a markup/encoding format, not the southbound forwarding protocol in this sense. Java is a programming language.",
            "choices": ["XML", "Java", "REST", "OpenFlow"],
        },
        {
            "slug": "wireless-band-select-5ghz-preference",
            "title": "CCNA — Band Select toward 5 GHz",
            "stem": "An engineer observes high usage on the 2.4GHz channels and lower usage on the 5GHz channels. What must be configured to allow clients to preferentially use 5GHz access points?",
            "name": "bandsel",
            "correct": "A",
            "explain": "Correct. A — Band Select (Client Band Select) on the WLC encourages dual-band clients to associate on 5 GHz. OEAP split tunnel is a remote-AP traffic model. MU-MIMO improves spatial efficiency, not band choice. Re-anchor roamed clients is a mobility/anchor feature.",
            "choices": [
                "Client Band Select",
                "OEAP Split Tunnel",
                "11ac MU-MIMO",
                "Re-Anchor Roamed Clients",
            ],
        },
        {
            "slug": "wlc-wpa2-psk-gui-format",
            "title": "CCNA — WPA2 PSK format on WLC",
            "stem": "When a WLAN with WPA2 PSK is configured in the Wireless LAN Controller GUI which format is supported?",
            "name": "wpa2fmt",
            "correct": "C",
            "explain": "Correct. C — The WPA2 passphrase is entered as a printable ASCII string (typically 8–63 characters). Base64, decimal, and generic Unicode format are not the supported WLC GUI answer here.",
            "choices": ["Unicode", "base64", "ASCII", "decimal"],
        },
        {
            "slug": "data-plane-forward-remote-client-traffic",
            "title": "CCNA — Data plane vs control",
            "stem": "Which networking function occurs on the data plane?",
            "name": "dplan2",
            "correct": "C",
            "explain": "Correct. C — Forwarding user traffic between client and server is data-plane work. STP, OSPF Hellos, and SSH sessions to the device itself are control or management plane.",
            "choices": [
                "facilitates spanning-tree elections",
                "processing inbound SSH management traffic",
                "forwarding remote client/server traffic",
                "sending and receiving OSPF Hello packets",
            ],
        },
        {
            "slug": "ipv6-compress-db8-interface-command",
            "title": "CCNA — IPv6 compressed address on interface",
            "stem": "A network engineer must configure the router R1 GigabitEthernet1/1 interface to connect to the router R2 GigabitEthernet1/1 interface. For the configuration to be applied the engineer must compress the address 2001:0db8:0000:0000:0500:000a:400F:583B. Which command must be issued on the interface?",
            "name": "v6if",
            "correct": "A",
            "explain": "Correct. A — Leading zeros drop and one :: replaces the contiguous all-zero hextets: 2001:db8::500:a:400F:583B. B is malformed and alters hextets. C miscompresses 0500 as 5. D uses :: twice, which is invalid.",
            "choices": [
                "ipv6 address 2001:db8::500:a:400F:583B",
                "ipv6 address 2001 db8:0::500:a:4F:583B",
                "ipv6 address 2001:0db8::5:a:4F:583B",
                "ipv6 address 2001::db8:0000::500:a:400F:583B",
            ],
            "mono": True,
        },
        {
            "slug": "ipv6-compress-hq-serial-s0-700-400f",
            "title": "CCNA — IPv6 compressed address (Serial0/0)",
            "stem": "An engineer must configure the IPv6 address 2001:0db8:0000:0000:0700:0003:400F:572B on the Serial0/0 interface of the HQ router and wants to compress it for easier configuration. Which command must be issued on the router interface?",
            "name": "v6hqser",
            "correct": "A",
            "explain": "Correct. A — Drop leading zeros in each hextet and replace the contiguous all-zero block with a single :: → 2001:db8::700:3:400F:572B. B wrongly shortens 400F to 4F inside the hextet. C uses an invalid character (letter O) and miscompresses 0700 as 7. D uses :: twice, which is not allowed.",
            "choices": [
                "ipv6 address 2001:db8::700:3:400F:572B",
                "ipv6 address 2001:db8:0::700:3:4F:572B",
                "ipv6 address 2001:Odb8::7:3:4F:572B",
                "ipv6 address 2001::db8:0000::700:3:400F:572B",
            ],
            "mono": True,
        },
        {
            "slug": "ipv6-compress-2001-eb8-c1-2200-0331",
            "title": "CCNA — IPv6 compression 2001:EB8:C1:2200",
            "stem": "A network administrator is setting up a new IPv6 network using the 64-bit address 2001:0EB8:00C1:2200:0001:0000:0000:0331/64. To simplify the configuration, the administrator has decided to compress the address. Which IP address must the administrator configure?",
            "name": "v6cmp331",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D — Drop leading zeros in each hextet (0EB8\u2192EB8, 00C1\u2192C1, 0001\u21921, 0331\u2192331) and replace the contiguous pair of all-zero hextets with a single :: \u2192 2001:EB8:C1:2200:1::331/64. A keeps an extra :0000: segment instead of ::. B mangles the first hextet (2001). C incorrectly shortens 2200 to 22.",
            "choices": [
                "ipv6 address 2001:EB8:C1:2200:1:0000:331/64",
                "ipv6 address 21:EB8:C1:2200:1::331/64",
                "ipv6 address 2001:EB8:C1:22:1::331/64",
                "ipv6 address 2001:EB8:C1:2200:1::331/64",
            ],
        },
        {
            "slug": "wlc-pmf-comeback-spoofed-association",
            "title": "CCNA — PMF and association comeback",
            "stem": "An administrator must secure the WLC from receiving spoofed association requests. Which steps must be taken to configure the WLC to restrict the requests and force the user to wait 10 ms to retry an association request?",
            "name": "pmfcome",
            "correct": "B",
            "explain": "Correct. B — Protected Management Frames (802.11w) help protect management traffic from trivial spoofing/tampering; the Comeback timer (milliseconds) controls how long a client waits before retrying association after a temporary denial. SA Query timeout addresses a different PMF procedure.",
            "choices": [
                "Enable Security Association Teardown Protection and set the SA Query timeout to 10",
                "Enable the Protected Management Frame service and set the Comeback timer to 10",
                "Enable 802.1x Layer 2 security and set the Comeback timer to 10",
                "Enable MAC filtering and set the SA Query timeout to 10",
            ],
        },
        {
            "slug": "fhrp-benefit-default-gateway-redundancy",
            "title": "CCNA — FHRP benefit",
            "stem": "What is the benefit of using FHRP (First Hop Redundancy Protocol)?",
            "name": "fhrpb",
            "correct": "D",
            "explain": "Correct. D — FHRPs (HSRP, VRRP, GLBP) provide redundant default gateways so failure of one router does not isolate the subnet. GLBP can load-share, but proportional load balancing in the wording of A is not the universal FHRP benefit. B and C are distractors.",
            "choices": [
                "balancing traffic across multiple gateways in proportion to their loads",
                "reduced management overhead on network routers",
                "reduced ARP traffic on the network",
                "higher degree of availability",
            ],
        },
        {
            "slug": "wlan-roam-reassociation-request-frame",
            "title": "CCNA — Roaming management frame",
            "stem": "Which 802.11 management frame type is sent when a client roams between access points on the same SSID?",
            "name": "roamre",
            "correct": "C",
            "explain": "Correct. C — Reassociation Request moves the STA to a new AP within the same ESS and carries the prior AP context. Association Request is for the initial join. Probe Request is for scanning. Authentication frames precede association but are not the roam handoff frame named here.",
            "choices": [
                "Authentication Request",
                "Probe Request",
                "Reassociation Request",
                "Association Request",
            ],
        },
        {
            "slug": "wlan-probe-response-frame-type",
            "title": "CCNA — Probe response frame type",
            "stem": "Which 802.11 frame type is indicated by a probe response after a client sends a probe request?",
            "name": "probetype1",
            "correct": "B",
            "explain": "Correct. B — Probe Request and Probe Response are both 802.11 management frames (used during scanning/discovery). Control frames coordinate medium access (for example RTS/CTS/ACK). Data frames carry MSDUs. \u201cAction\u201d names a management subtype, not the top-level type category paired with control and data.",
            "choices": [
                "action",
                "management",
                "control",
                "data",
            ],
        },
        {
            "slug": "fiber-om3-om4-fifty-micron-core",
            "title": "CCNA — OM3 and OM4 similarity",
            "stem": "What is a similarity between OM3 and OM4 fiber optic cable?",
            "name": "om34",
            "correct": "A",
            "explain": "Correct. A — OM3 and OM4 are both 50/125 µm laser-optimized multimode fiber. They differ in bandwidth and reach at a given rate, not core diameter. 9 µm is single-mode; 62.5 µm is legacy OM1-style multimode.",
            "choices": [
                "Both have a 50 micron core diameter",
                "Both have a 9 micron core diameter",
                "Both have a 62.5 micron core diameter",
                "Both have a 100 micron core diameter",
            ],
        },
        {
            "slug": "ap-switch-poe-cdp-discovery",
            "title": "CCNA — AP power negotiation with switch",
            "stem": "Which protocol does an access point use to draw power from a connected switch?",
            "name": "poecdp",
            "correct": "B",
            "explain": "Correct. B — Actual delivery is IEEE PoE on the wire; between Cisco PSE and Cisco PD, CDP advertises extended power details beyond basic classification. IGMP is multicast; IPv6 Neighbor Discovery is not for PoE; Adaptive Wireless Path is unrelated to switch PoE.",
            "choices": [
                "Internet Group Management Protocol",
                "Cisco Discovery Protocol",
                "Adaptive Wireless Path Protocol",
                "Neighbor Discovery Protocol",
            ],
        },
        {
            "slug": "syslog-severity-informational-level",
            "title": "CCNA — Syslog severity informational",
            "stem": "When deploying syslog, which severity level logs informational message?",
            "name": "slogsev",
            "correct": "D",
            "explain": "Correct. D — Severity 6 is informational (0 emergency … 7 debug). 0 is emergency; 2 is critical; 4 is warning.",
            "choices": ["0", "2", "4", "6"],
        },
        {
            "slug": "dtp-dynamic-auto-passive-trunk",
            "title": "CCNA — DTP passive trunk negotiation",
            "stem": "Refer to the exhibit. Which command must be executed for Gi1/1 on SW1 to passively become a trunk port if Gi1/1 on SW2 is configured in desirable or trunk mode?",
            "name": "dtpmode",
            "correct": "C",
            "explain": "Correct. C — dynamic auto passively waits for DTP from the neighbor; if SW2 is desirable or trunk, the link can form a trunk. dynamic desirable actively negotiates. switchport mode trunk is not the passive auto answer. dot1-tunnel is unrelated to DTP trunk formation here.",
            "choices": [
                "switchport mode trunk",
                "switchport mode dot1-tunnel",
                "switchport mode dynamic auto",
                "switchport mode dynamic desirable",
            ],
            "mono": True,
        },
        {
            "slug": "dtp-sw1-sw2-printer-vlan5-trunk",
            "title": "CCNA — DTP trunk to SW_2 and VLAN 5 for printer",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "An administrator must connect SW_1 and the printer to the network. SW_2 requires DTP to be used for the connection to SW_1. The printer is configured as an access port with VLAN 5. Which set of commands completes the connectivity?",
            "name": "dtpprnt1",
            "correct": "B",
            "mono": True,
            "explain": "Correct. B \u2014 The topology shows the printer on SW_1 and an inter-switch link on Et0/2 toward SW_2 and the LAN. The CLI excerpt shows that link administratively in dynamic auto but operationally trunking with dot1q and only VLAN 5 enabled on the trunk\u2014consistent with DTP negotiation from an active neighbor and a restricted allowed-VLAN list. To reach that state from configuration, use dynamic desirable (or trunk) toward SW_2 so DTP forms the trunk, and switchport trunk allowed vlan add 5 so VLAN 5 crosses the link for the printer access VLAN. Option A misstates pruning/allowed-VLAN syntax. Option C uses private VLAN association text that does not replace normal access VLAN 5 across a trunk. Option D alone does not add VLAN 5 to the allowed list and is a weaker match when both ends might stay passive.",
            "post_stem_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/dtp-sw1-sw2-printer-lan-topology.png" alt="Topology: printer on SW_1 Ethernet 1/1; SW_1 Ethernet 0/2 to SW_2 Ethernet 0/2; SW_2 to LAN cloud." width="900" decoding="async" loading="lazy" />
      </figure>
      <div class="cli-device" role="region" aria-label="SW_1 show interfaces Et0/2 switchport output">
        <h2>SW_1# show interfaces Et0/2 switchport</h2>
        <pre>Name: Et0/2
Switchport: Enabled
Administrative Mode: dynamic auto
Operational Mode: trunk
Administrative Trunking Encapsulation: negotiate
Operational Trunking Encapsulation: dot1q
Negotiation of Trunking: On
Access Mode VLAN: 1 (default)
Administrative Native VLAN tagging: enabled
Voice VLAN: none
Administrative private VLAN: none
Operational private-vlan: none
Trunking VLANs Enabled: 5
Pruning VLANs Enabled: 2-1001
Capture Mode: Disabled</pre>
      </div>
    </div>""",
            "choices": [
                """switchport mode trunk
switchport trunk pruning vlan add 5""",
                """switchport mode dynamic desirable
switchport trunk allowed vlan add 5""",
                """switchport mode dynamic auto
switchport private-vlan association host 5""",
                """switchport mode dynamic auto
switchport trunk encapsulation negotiate""",
            ],
        },
        {
            "slug": "wlc-ds-port-switch-ap-traffic",
            "title": "CCNA — WLC distribution system port",
            "stem": "Which WLC port connects to a switch to pass normal access-point traffic?",
            "name": "wlcds",
            "correct": "A",
            "explain": "Correct. A — The distribution system (DS) network connection carries CAPWAP control and data between APs and the controller and bridges wireless client traffic onto the wired LAN. The service port is for out-of-band management; the redundancy port is for WLC high availability; the console is for serial CLI access.",
            "choices": [
                "distribution system",
                "service",
                "redundancy",
                "console",
            ],
        },
        {
            "slug": "syslog-trap-severity-informational-included",
            "title": "CCNA — Syslog trap level for informational",
            "stem": "Which level of severity must be set to get informational syslogs?",
            "name": "slogtrap",
            "correct": "D",
            "explain": "Correct. D — On Cisco IOS, logging trap sends that severity and all numerically lower (more urgent) severities. Informational is level 6. Alert (1), critical (2), and notice (5) are all more urgent than informational, so they do not include informational messages. Debug (7) is the least urgent and includes informational (6) along with all higher-priority levels.",
            "choices": ["alert", "critical", "notice", "debug"],
        },
        {
            "slug": "route-ad-ebgp-eigrp-ospf-r4-server",
            "title": "CCNA — AD when OSPF, eBGP, and EIGRP compete",
            "stem": "Refer to the exhibit. Router R4 is dynamically learning the path to the server. If R4 is connected to R1 via OSPF Area 20, to R2 via BGP, and to R3 via EIGRP 777, which path is installed in the routing table of R4?",
            "name": "admix",
            "correct": "A",
            "explain": "Correct. A — For the same prefix, the route with the lowest administrative distance is installed. eBGP defaults to AD 20, EIGRP internal to 90, and OSPF to 110, so an eBGP-learned path via R2 wins. iBGP defaults to 200 and would lose to EIGRP and OSPF here; option B misstates the winning case.",
            "choices": [
                "the path through R2, because the EBGP administrative distance is 20",
                "the path through R2, because the IBGP administrative distance is 200",
                "the path through R1, because the OSPF administrative distance is 110",
                "the path through R3, because the EIGRP administrative distance is lower than OSPF and BGP",
            ],
        },
        {
            "slug": "cloud-topology-public-private-hybrid",
            "title": "CCNA — Cloud deployment models",
            "stem": "What is a characteristic of cloud-based network topology?",
            "name": "cloud1",
            "correct": "B",
            "explain": "Correct. B — Cloud services are consumed as public, private, or hybrid deployments. Physical workstation resource sharing (A) is not the defining trait. Onsite-only L2/L3 (C) describes traditional premises networks. Wireless-only access (D) is false.",
            "choices": [
                "physical workstations are configured to share resources",
                "services are provided by a public, private, or hybrid deployment",
                "onsite network services are provided with physical Layer 2 and Layer 3 components",
                "wireless connections provide the sole access method to services",
            ],
        },
        {
            "slug": "ios-clock-set-exec-date-time",
            "title": "CCNA — Set router clock in EXEC mode",
            "stem": "A network analyst is tasked with configuring the date and time on a router using EXEC mode. The date must be set to 12:00am. Which command should be used?",
            "name": "clk1",
            "correct": "D",
            "explain": "Correct. D — clock set is a privileged EXEC command that sets the software clock (use 00:00:00 for midnight with the correct day/month/year). clock timezone and clock summer-time are global configuration for offset and DST rules, not the one-step time set.",
            "choices": [
                "Clock timezone",
                "Clock summer-time-recurring",
                "Clock summer-time date",
                "Clock set",
            ],
        },
        {
            "slug": "rest-http-200-successful-request",
            "title": "CCNA — HTTP 200 for successful REST",
            "stem": "Which HTTP status code is returned after a successful REST API request?",
            "name": "http200",
            "correct": "A",
            "explain": "Correct. A — 200 OK is the common success response for many REST operations (201 Created and 204 No Content are also used in some designs). 301 redirects, 404 is not found, 500 is a server error.",
            "choices": ["200", "301", "404", "500"],
        },
        {
            "slug": "router-inter-subnet-forwarding-role",
            "title": "CCNA — Router forwards between subnets",
            "stem": "Refer to the exhibit. When PC-A sends traffic to PC-B, which network component is in charge of receiving the packet from PC-A verifying the IP addresses, and forwarding the packet to PC-B?",
            "name": "rtrpc",
            "correct": "D",
            "explain": "Correct. D — A router (or Layer 3 switch) uses the destination IP to route between subnets and rewrites Layer 2 addresses hop by hop. A Layer 2 switch does not perform that IP forwarding role. A firewall may filter but the generic inter-subnet forwarding role here is the router.",
            "choices": [
                "Layer 2 switch",
                "firewall",
                "Load balancer",
                "Router",
            ],
        },
        {
            "slug": "sdn-controller-role-central-point",
            "title": "CCNA — SDN controller role",
            "stem": "What is the function of a controller in controller-based networking?",
            "name": "sdnc1",
            "correct": "D",
            "explain": "Correct. D — The SDN controller is the centralized management/control point for the architecture (policy, programmability, southbound to devices). It does not centralize the data plane; data forwarding stays on infrastructure. It is not merely a line card or a pair of campus routers in this sense.",
            "choices": [
                "It is a pair of core routers that maintain all routing decisions for a campus",
                "It centralizes the data plane for the network",
                "It is the card on a core router that maintains all routing decisions for a campus",
                "It serves as the centralized management point of an SDN architecture",
            ],
        },
        {
            "slug": "switch-known-mac-unicast-forward",
            "title": "CCNA — Known unicast forwarding",
            "stem": "When a switch receives a frame for a known destination MAC address, how is the frame handed?",
            "name": "swmac",
            "correct": "D",
            "explain": "Correct. D — The CAM entry points to a single egress port; the switch forwards the frame there. Unknown unicast is flooded within the VLAN. Broadcast floods to all ports except the ingress port in that VLAN.",
            "choices": [
                "flooded to all ports except the one from which it originated",
                "broadcast to all ports",
                "forwarded to the first available port",
                "sent to the port identified for the known MAC address",
            ],
        },
        {
            "slug": "rfc1918-purpose-conserve-public-ipv4",
            "title": "CCNA — Why RFC 1918 space exists",
            "stem": "Why was the RFC 1918 address space defined?",
            "name": "rfc1918b",
            "correct": "D",
            "explain": "Correct. D — Private IPv4 space lets organizations use internal addresses without consuming globally unique public IPv4 for every host, preserving the public pool (often with NAT at the edge). It is IPv4-focused. NAT followed operational need but the RFC’s purpose is private addressing to conserve public IPv4.",
            "choices": [
                "preserve public IPv6 address space",
                "support the NAT protocol",
                "reduce instances of overlapping IP addresses",
                "conserve public IPv4 addressing",
            ],
        },
        {
            "slug": "wlc-aaa-override-ise-dynamic-vlan",
            "title": "CCNA — WLC AAA Override for ISE VLAN",
            "stem": "After installing a new Cisco ISE server, which task must the engineer perform on the Cisco WLC to connect wireless clients on a specific VLAN based on their credentials?",
            "name": "wlcaaa",
            "correct": "B",
            "explain": "Correct. B — Allow AAA Override lets the WLAN honor RADIUS/ISE attributes (such as VLAN) over static WLAN settings. MIC AP authorization and LAG/RRM options do not enable per-user VLAN from ISE.",
            "choices": [
                "Enable the Authorized MIC APs against auth-list or AAA.",
                "Enable the allow AAA Override",
                "Disable the LAG Mode or Next Reboot.",
                "Enable the Event Driven RRM.",
            ],
        },
        {
            "slug": "ftp-authentication-backup-config-copy",
            "title": "CCNA — FTP and authenticated file copy",
            "stem": "Which protocol requires authentication to transfer a backup configuration file from a router to a remote server?",
            "name": "ftpbak",
            "correct": "B",
            "explain": "Correct. B — FTP uses username/password for access. TFTP does not require authentication in the classic form. DTP is unrelated; SMTP is for mail.",
            "choices": ["TFTP", "FTP", "DTP", "SMTP"],
        },
        {
            "slug": "sdn-control-to-infrastructure-boundary",
            "title": "CCNA — Control plane to data plane boundary",
            "stem": "Where is the interface between the control plane and data plane within the software-defined architecture?",
            "name": "sdnci",
            "correct": "D",
            "explain": "Correct. D — Southbound interfaces sit between the control layer (controller) and the infrastructure layer (switches/routers that forward). Application-to-control is northbound; management is a separate plane in many models.",
            "choices": [
                "application layer and the management layer",
                "application layer and the infrastructure layer",
                "control layer and the application layer",
                "control layer and the infrastructure layer",
            ],
        },
        {
            "slug": "router-forward-hop-mac-rewrite",
            "title": "CCNA — Per-hop MAC rewrite on a router",
            "stem": "Which action does the router take as it forwards a packet through the network?",
            "name": "macrw",
            "correct": "D",
            "explain": "Correct. D — On each Ethernet hop the router builds a new frame: source MAC is its egress interface, destination MAC is the resolved next-hop neighbor. End-host IP addresses are not swapped to router/neighbor IPs for normal routing (unless NAT/tunnels).",
            "choices": [
                "The router replaces the source and destination labels with the sending router interface label as a source and the next hop router label as a destination",
                "The router encapsulates the source and destination IP addresses with the sending router IP address as the source and the neighbor IP address as the destination",
                "The router encapsulates the original packet and then includes a tag that identifies the source router MAC address and transmit transparently to the destination",
                "The router replaces the original source and destination MAC addresses with the sending router MAC address as the source and neighbor MAC address as the destination",
            ],
        },
        {
            "slug": "ipsec-tunnel-esp-encrypt-whole-packet",
            "title": "CCNA — IPsec tunnel mode with ESP",
            "stem": "When a site-to-site VPN is configured, which IPsec mode provides encapsulation and encryption of the entire original IP packet?",
            "name": "ipsec1",
            "correct": "C",
            "explain": "Correct. C — Tunnel mode wraps the original IP packet with a new outer header; ESP provides encryption. AH does not encrypt. Transport mode does not encapsulate the full original packet the same way for typical site-to-site tunnels.",
            "choices": [
                "IPsec tunnel mode with AH",
                "IPsec transport mode with AH",
                "IPsec tunnel mode with ESP",
                "IPsec transport mode with ESP",
            ],
        },
        {
            "slug": "ipv6-static-summary-and-host-via-next-hops",
            "title": "CCNA — IPv6 static routes (choose two)",
            "stem": "Refer to the exhibit. Which two commands, when configured on router R1, fulfill these requirements? (Choose two) – Packets toward the entire network 2001:db8:23::/64 must be forwarded through router R2. – Packets toward host 2001:db8:23::14 preferably must be forwarded through R3.",
            "name": "v6stat2",
            "choose_two": True,
            "correct": ["B", "E"],
            "explain": "Correct. B and E — A /64 static via R2 covers the whole prefix. A host /128 for 2001:db8:23::14 via R3 is more specific and wins for that address. /128 toward R2 in A does not cover the /64. C and D use /64 for a single host or wrong next hop.",
            "choices": [
                "ipv6 route 2001:db8:23::/128 fd00:12::2",
                "ipv6 route 2001:db8:23::14/128 fd00:13::3",
                "ipv6 route 2001:db8:23::14/64 fd00:12::2",
                "ipv6 route 2001:db8:23::14/64 fd00:12::2 200",
                "ipv6 route 2001:db8:23::/64 fd00:12::2",
            ],
        },
        {
            "slug": "firewall-role-untrusted-to-trusted",
            "title": "CCNA — Firewall role in enterprise",
            "stem": "What is the role of a firewall in an enterprise network?",
            "name": "fwlz1",
            "correct": "A",
            "explain": "Correct. A — A firewall enforces policy between trust zones (for example Internet to internal), permitting or denying traffic. It is not primarily stateless-only forwarding, does not send unauthorized traffic into more sensitive areas by design, and does not deny all traffic by default in normal operation.",
            "choices": [
                "determines which packets are allowed to cross from unsecured to secured networks",
                "processes unauthorized packets and allows passage to less secure segments of the network",
                "forwards packets based on stateless packet inspection",
                "explicitly denies all packets from entering an administrative domain",
            ],
        },
        {
            "slug": "firewall-permit-deny-traffic-rules",
            "title": "CCNA — Permit or deny traffic by rules",
            "stem": "Which device permits or denies network traffic based on a set of rules?",
            "name": "fwrules1",
            "correct": "D",
            "explain": "Correct. D — A firewall enforces security policy (rules) to permit or deny traffic. A wireless access point provides client access; a switch forwards frames at Layer 2; a wireless LAN controller manages lightweight access points.",
            "choices": [
                "access point",
                "switch",
                "wireless controller",
                "firewall",
            ],
        },
        {
            "slug": "portfast-benefit-user-data-sooner",
            "title": "CCNA — Benefit of PortFast",
            "stem": "What is the benefit of configuring PortFast on an interface?",
            "name": "pfben",
            "correct": "C",
            "explain": "Correct. C — PortFast lets an access port move to STP forwarding quickly so user traffic can flow soon after link up. It does not change cable speed negotiation, QoS marking, or special handling for voice/video by itself.",
            "choices": [
                "After the cable is connected, the interface uses the fastest speed setting available for that cable type",
                "The frames entering the interface are marked with higher priority and then processed faster by a switch",
                "After the cable is connected, the interface is available faster to send and receive user data",
                "Real-time voice and video frames entering the interface are processed faster",
            ],
        },
        {
            "slug": "vlan-hopping-mitigation-dtp-trunk",
            "title": "CCNA — Mitigate VLAN hopping",
            "stem": "How are VLAN hopping attacks mitigated?",
            "name": "vlanhop1",
            "correct": "A",
            "explain": "Correct. A — Disable DTP on access ports and use explicit trunk configuration only where needed to prevent unwanted trunk negotiation (switch spoofing). Extended VLANs do not fix this. All ports in VLAN 1 is poor practice. DAI addresses ARP spoofing, not classic VLAN hopping.",
            "choices": [
                "manually implement trunk ports and disable DTP",
                "configure extended VLANs",
                "activate all ports and place in the default VLAN",
                "enable dynamic ARP inspection",
            ],
        },
        {
            "slug": "routing-longest-match-default-172-16-1-1",
            "title": "CCNA — Longest match vs default for 172.16.1.1",
            "stem": "Refer to the exhibit. R1#show ip route (output shows: Gateway of last resort is 192.168.14.4 to network 0.0.0.0; C 172.16.1.128/25 is directly connected, GigabitEthernet1/1/0; O*E2 0.0.0.0/0 [110/1] via 192.168.14.4, FastEthernet1/0; other routes omitted.) If R1 receives a packet destined to 172.16.1.1, to which IP address does it send the packet?",
            "name": "rt172",
            "correct": "C",
            "explain": "Correct. C — 172.16.1.1 is not inside 172.16.1.128/25 (.128–.255). No other specific route matches, so R1 uses the default route via 192.168.14.4.",
            "choices": ["192.168.12.2", "192.168.13.3", "192.168.14.4", "192.168.15.5"],
        },
        {
            "slug": "floating-static-default-route-router-a-command",
            "title": "CCNA — Floating static default route",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "Which command must be issued to enable a floating static default route on router A?",
            "name": "fltdef1",
            "correct": "A",
            "explain": "Correct. A — A floating static route is a backup static route configured with a higher administrative distance than the primary route so it is only used when preferred routing is lost. Option A points to the backup next hop (192.168.2.1) with AD 10. Option B is a normal static default with the default AD. Option C sets AD 10 on the primary next hop and does not represent the intended backup path. Option D is for hosts/switches without IP routing, not for a routed fallback default route on a router.",
            "post_stem_html": '''    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/floating-static-default-route-router-a-topology.png" alt="Topology: Routers A, B, and C in a triangle. A–B 192.168.2.0/24 (.1 on A Gi0/0/0, .2 on B Gi0/0/0); A–C 192.168.1.0/24 (.1 on A Gi0/0/1, .2 on C Gi0/0/0); B–C 192.168.3.0/24 (.2 on B Gi0/0/1, .1 on C Gi0/0/1)." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>''',
            "choices": [
                "ip route 0.0.0.0 0.0.0.0 192.168.2.1 10",
                "ip route 0.0.0.0 0.0.0.0 192.168.1.2",
                "ip route 0.0.0.0 0.0.0.0 192.168.1.2 10",
                "ip default-gateway 192.168.2.1",
            ],
        },
        {
            "slug": "r1-backup-default-route-via-r2-ad10",
            "title": "CCNA — Backup default route via R2",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "Router R1 currently is configured to use R3 as the primary route to the Internet, and the route uses the default administrative distance settings. A network engineer must configure R1 so that it uses R2 as a backup, but only if R3 goes down. Which command must the engineer configure on R1 so that it correctly uses R2 as a backup route, without changing the administrative distance configuration on the link to R3?",
            "name": "fltdef2",
            "correct": "C",
            "explain": "Correct. C — A floating backup static route must have a higher administrative distance than the primary static default (which is AD 1 by default). Pointing the backup to R2 with AD 10 makes it install only when the primary path via R3 disappears. B and D use AD 1, so they are not floating backups. A uses an exit interface form with AD 6 and does not match the explicit backup next-hop path indicated for R2 in this scenario.",
            "post_stem_html": '''    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/r1-backup-default-route-via-r2-ad10-topology.png" alt="Topology with R1 connected to LAN 192.168.1.0/24 and WAN links to R2 (209.165.200.224/27) and R3 (209.165.201.0/27), where R2 is backup Internet path." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>''',
            "choices": [
                "ip route 0.0.0.0 0.0.0.0 g0/1 6",
                "ip route 0.0.0.0 0.0.0.0 g0/1 1",
                "ip route 0.0.0.0 0.0.0.0 209.165.201.5 10",
                "ip route 0.0.0.0 0.0.0.0 209.165.200.226 1",
            ],
        },
        {
            "slug": "r1-management-network-static-route-new-server",
            "title": "CCNA — Static route for new management server",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "An engineer is updating the R1 configuration to connect a new server to the management network. The PCs on the management network must be blocked from pinging the default gateway of the new server. Which command must be configured on R1 to complete the task?",
            "name": "r1mgmt1",
            "correct": "C",
            "explain": "Correct. C — The valid static route for the new server subnet is a /24 route to 172.16.2.0 via the intended next-hop router at 192.168.1.5. Option A points to a different next hop and does not match the required path. Option B is a host route to 172.16.2.2 and does not represent the full new server subnet requirement. Option D uses an invalid mask/prefix combination for the host route shown.",
            "post_stem_html": '''    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/r1-management-network-static-route-new-server-topology.png" alt="Management network with PC1/PC2 to R1, transit link 192.168.1.0/24 from R1 to R2, and server network 172.16.2.0/24 with new server 172.16.2.2 behind R2." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>''',
            "choices": [
                "R1(config)#ip route 172.16.2.0 255.255.255.0 192.168.1.15",
                "R1(config)#ip route 172.16.2.2 255.255.255.255 gi0/0",
                "R1(config)#ip route 172.16.2.0 255.255.255.0 192.168.1.5",
                "R1(config)#ip route 172.16.2.2 255.255.255.248 gi0/1",
            ],
        },
        {
            "slug": "ansible-playbook-task-vlan-config",
            "title": "CCNA — Ansible for VLAN config (choose two)",
            "stem": "Which two components are needed to create an Ansible script that configures a VLAN on a switch? (Choose two)",
            "name": "ansb1",
            "choose_two": True,
            "correct": ["A", "E"],
            "explain": "Correct. A and E — A playbook defines the automation; tasks invoke modules to configure VLANs. Cookbook and recipe are Chef terms; model is not the paired answer here.",
            "choices": ["task", "cookbook", "recipe", "model", "playbook"],
        },
        {
            "slug": "spine-leaf-full-mesh-uplinks",
            "title": "CCNA — Spine-leaf interconnect",
            "stem": "How are the switches in a spine-and-leaf topology interconnected?",
            "name": "spine1",
            "correct": "C",
            "explain": "Correct. C — Every leaf uplinks to every spine for multipath and high bisection bandwidth. Leaves do not hub into one leaf; each leaf does not connect to only one spine in the standard design.",
            "choices": [
                "Each leaf switch is connected to two spine switches, making a loop.",
                "Each leaf switch is connected to a central leaf switch, then uplinked to a core spine switch.",
                "Each leaf switch is connected to each spine switch.",
                "Each leaf switch is connected to one of the spine switches.",
            ],
        },
        {
            "slug": "sdn-data-plane-forwarding-router",
            "title": "CCNA — Data plane handles forwarding",
            "stem": "In software-defined architecture, which place handles switching for traffic through a Cisco router?",
            "name": "sdnadp1",
            "correct": "A",
            "explain": "Correct. A — User traffic is forwarded in the data (forwarding) plane using programmed tables. The control plane builds state; management handles administration; application plane refers to SDN apps above the controller.",
            "choices": ["Data", "Control", "Management", "Application"],
        },
        {
            "slug": "wlc-hardening-disable-telnet-http",
            "title": "CCNA — Harden WLC management (choose two)",
            "stem": "Which two protocols must be disabled to increase security for management connections to a Wireless LAN Controller? (Choose two)",
            "name": "wlch1",
            "choose_two": True,
            "correct": ["A", "C"],
            "explain": "Correct. A and C — Telnet and HTTP are cleartext; disable them in favor of SSH and HTTPS. TFTP is weak but is not the usual paired answer with HTTP/Telnet on this item.",
            "choices": ["Telnet", "SSH", "HTTP", "HTTPS", "TFTP"],
        },
        {
            "slug": "dna-center-overall-health-dashboard",
            "title": "CCNA — DNA Center Overall Health",
            "stem": "What is a function of the Cisco DNA Center Overall Health Dashboard?",
            "name": "dnahealth1",
            "correct": "D",
            "explain": "Correct. D — Overall Health summarizes prioritized issues across the fabric (often presented as a short ranked list such as top issues). It is not primarily a server CPU report, per-user activity logging for ten devices, or per-wireless-device operational detail for every AP.",
            "choices": [
                "It summarizes daily and weekly CPU usage for servers and workstations in the network.",
                "It provides detailed activity logging for the 10 devices and users on the network.",
                "It summarizes the operational status of each wireless device on the network.",
                "It provides a summary of the top 10 global issues.",
            ],
        },
        {
            "slug": "hypervisor-vm-hardware-communication",
            "title": "CCNA — Hypervisor role",
            "stem": "An implementer is preparing hardware for virtualization to create virtual machines on a host. What is needed to provide communication between hardware and virtual machines?",
            "name": "hypcom",
            "correct": "C",
            "explain": "Correct. C — The hypervisor virtualizes CPU, memory, NICs, and storage and mediates guest access to the physical machine. Cables, switches, and routers do not provide that host-to-VM abstraction.",
            "choices": ["straight cable", "router", "hypervisor", "switch"],
        },
        {
            "slug": "distribution-layer-two-characteristics",
            "title": "CCNA — Distribution layer (choose two)",
            "stem": "What are two characteristics of the distribution layer in a three-tier network architecture? (Choose two)",
            "name": "dist2",
            "choose_two": True,
            "correct": ["A", "C"],
            "explain": "Correct. A and C — The distribution layer aggregates access switches and commonly provides the routing boundary between VLANs/L2 domains. The core is the backbone; printer ports are access layer; redundant uptime applies broadly but the paired textbook answers are aggregation and the L2/L3 boundary.",
            "choices": [
                "provides a boundary between Layer 2 and Layer 3 communications",
                "designed to meet continuous, redundant uptime requirements",
                "serves as the network aggregation point",
                "physical connection point for a LAN printer",
                "is the backbone for the network topology",
            ],
        },
        {
            "slug": "layer3-switch-flood-broadcast-within-vlan",
            "title": "CCNA — Layer 3 switch function",
            "stem": "What is a function of a Layer 3 switch?",
            "name": "l3swfn1",
            "correct": "D",
            "explain": "Correct. D — A multilayer switch still switches at Layer 2 inside each VLAN, so broadcast frames are flooded to other ports in the same VLAN (same broadcast domain). Inter-VLAN forwarding uses IP routing, not MAC-only bridging (C). Routed interfaces or SVIs do not carry broadcast between VLANs the way B suggests. Option A mischaracterizes how traffic is moved between subnets.",
            "choices": [
                "move frames between endpoints limited to IP addresses",
                "transmit broadcast traffic when operating in Layer 3 mode exclusively",
                "forward Ethernet frames between VLANs using only MAC addresses",
                "flood broadcast traffic within a VLAN",
            ],
        },
        {
            "slug": "qos-pq-voice-over-data-traffic",
            "title": "CCNA — PQ for voice on data-heavy links",
            "stem": "Which QoS tool can you use to optimize voice traffic on a network that is primarily intended for data traffic?",
            "name": "qospq",
            "correct": "C",
            "explain": "Correct. C — Priority queuing (or LLQ in modern policies) gives voice a strict-priority queue ahead of bulk data. WRED targets congestion avoidance for TCP-heavy data. WFQ spreads bandwidth among flows without strict voice priority. FIFO has no preference.",
            "choices": ["WRED", "FIFO", "PQ", "WFQ"],
        },
        {
            "slug": "dhcp-default-gateway-windows-workstation",
            "title": "CCNA — Default gateway via DHCP on Windows",
            "stem": "On workstations running Microsoft Windows, which protocol provides the default gateway for the device?",
            "name": "wingw",
            "correct": "D",
            "explain": "Correct. D — DHCP supplies IPv4 settings including the default gateway (DHCP Option 3) when the PC uses automatic addressing. DNS resolves names. SNMP manages devices. STP prevents Layer 2 loops on switches.",
            "choices": ["STP", "DNS", "SNMP", "DHCP"],
        },
        {
            "slug": "subnet-included-hosts-192-168-1-0-26",
            "title": "CCNA — Hosts inside 192.168.1.0/26 (choose two)",
            "stem": "Refer to the exhibit. R2#show ip route shows: C 192.168.1.0/26 is directly connected, FastEthernet0/1. Which two prefixes are included in this routing table entry? (Choose two)",
            "name": "sub26",
            "choose_two": True,
            "correct": ["A", "B"],
            "explain": "Correct. A and B — 192.168.1.0/26 spans 192.168.1.0–192.168.1.63, so .17 and .61 are inside the prefix. .64 begins the next block; .127 and .254 are outside this /26.",
            "choices": ["192.168.1.17", "192.168.1.61", "192.168.1.64", "192.168.1.127", "192.168.1.254"],
        },
        {
            "slug": "network-automation-drivers-choose-two",
            "title": "CCNA — Drivers for automation (choose two)",
            "stem": "Which two primary drivers support the need for network automation? (Choose two)",
            "name": "autdrv",
            "choose_two": True,
            "correct": ["C", "E"],
            "explain": "Correct. C and E — Policy-driven provisioning and a centralized/API-driven entry point for provisioning reduce manual error and scale operations. Training is not eliminated. Hardware footprint alone is not the primary driver. Self-healing may be a goal of advanced platforms but is not the usual paired answer with these choices.",
            "choices": [
                "Increasing reliance on self-diagnostic and self-healing",
                "Eliminating training needs",
                "Policy-derived provisioning of resources",
                "Reducing hardware footprint",
                "Providing a single entry point for resource provisioning",
            ],
        },
        {
            "slug": "tcp-vs-udp-connection-reliability",
            "title": "CCNA — TCP vs UDP delivery",
            "stem": "What is the difference in data transmission delivery and reliability between TCP and UDP?",
            "name": "tcpudp",
            "correct": "D",
            "explain": "Correct. D — TCP is connection-oriented (handshake) and reliable with retransmissions. UDP is connectionless and best-effort without transport-layer retransmission. Option A reverses roles; B wrongly claims UDP retransmits.",
            "choices": [
                "UDP sets up a connection between both devices before transmitting data. TCP uses the three-way handshake to transmit data with a reliable connection.",
                "TCP transmits data at a higher rate and ensures packet delivery. UDP retransmits lost data to ensure applications receive the data on the remote end.",
                "UDP is used for multicast and broadcast communication. TCP is used for unicast communication and transmits data at a higher rate with error checking.",
                "TCP requires the connection to be established before transmitting data. UDP transmits data at a higher rate without ensuring packet delivery.",
            ],
        },
        {
            "slug": "network-endpoints-security-definition",
            "title": "CCNA — Endpoints as a risk surface",
            "stem": "What are network endpoints?",
            "name": "endpt",
            "correct": "A",
            "explain": "Correct. A — Endpoints are user devices and servers at the edge; if compromised they threaten the rest of the enterprise (endpoint security). They are not primarily routers, inter-VLAN engines, or campus-wide policy enforcement points among these choices.",
            "choices": [
                "a threat to the network if they are compromised",
                "support inter-VLAN connectivity",
                "act as routers to connect a user to the service provider network",
                "enforce policies for campus-wide traffic going to the internet",
            ],
        },
        {
            "slug": "physical-access-control-scope",
            "title": "CCNA — Physical access control",
            "stem": "What does physical access control regulate?",
            "name": "physac",
            "correct": "D",
            "explain": "Correct. D — Physical access control governs entry to facilities and equipment spaces (data centers, IDFs, racks). Logical access to networks and filesystems is a different control family.",
            "choices": [
                "access to specific networks based on business function",
                "access to servers to prevent malicious activity",
                "access to computer networks and file systems",
                "access to networking equipment and facilities",
            ],
        },
        {
            "slug": "wireless-80211a-five-ghz-consideration",
            "title": "CCNA — 802.11a considerations",
            "stem": "What must be considered when using 802.11a?",
            "name": "w11a",
            "correct": "D",
            "explain": "Correct. D — 802.11a operates in 5 GHz with more non-overlapping channels than crowded 2.4 GHz used by 802.11b/g. It is not broadly interoperable with 2.4-only 802.11g radios alone, is not the lower-cost choice historically, and is not susceptible to 2.4 GHz microwave interference.",
            "choices": [
                "It is compatible with 802.11g and 802.11-compliant wireless devices",
                "It is chosen over 802.11b/g when a lower-cost solution is necessary",
                "It is susceptible to interference from 2.4 GHz devices such as microwave ovens.",
                "It is used in place of 802.11b/g when many nonoverlapping channels are required",
            ],
        },
        {
            "slug": "lldp-run-global-isp-handoff",
            "title": "CCNA — LLDP with third-party ISP",
            "stem": "An engineer configures interface Gi1/0 on the company PE router to connect to an ISP. Neighbor discovery is disabled. The interface has lldp transmit and lldp receive. Which action is necessary to complete the configuration if the ISP uses third-party network devices?",
            "name": "lldpg",
            "correct": "A",
            "explain": "Correct. A — LLDP is multi-vendor; on Cisco, enable LLDP globally (lldp run) so interface LLDP settings take effect. Disabling autonegotiation or CDP alone does not complete LLDP interoperability. You cannot rely on enabling LLDP-MED on the ISP device from the PE config.",
            "choices": [
                "Enable LLDP globally",
                "Disable autonegotiation",
                "Disable Cisco Discovery Protocol on the interface",
                "Enable LLDP-MED on the ISP device",
            ],
        },
        {
            "slug": "r5-disable-discovery-gi0-1-cdp-lldp-verify",
            "title": "CCNA — CDP/LLDP per interface on R5",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "For security reasons, automatic neighbor discovery must be disabled on the R5 Gi0/1 interface. These tasks must be completed:",
            "stem_after_exhibit_bullets": [
                "Disable all neighbor discovery methods on R5 interface Gi0/1.",
                "Permit neighbor discovery on R5 interface Gi0/2.",
                "Verify there are no dynamically learned neighbors on R5 interface Gi0/1.",
            ],
            "stem_after_exhibit_tail": "Display the IP address of R6\u2019s interface Gi0/2. Which configuration must be used?",
            "name": "r5disc1",
            "correct": "C",
            "mono": True,
            "explain": "Correct. C — On Gi0/1, no cdp enable stops CDP on that interface only while cdp run keeps CDP on other interfaces such as Gi0/2. no lldp run disables LLDP globally so it is not active on Gi0/1. Option A globally disables CDP (hurts Gi0/2) and leaves LLDP on Gi0/1. Option B places no cdp run under the interface, which is invalid (global command). Option D matches C for config but uses only show cdp neighbor; neighbor detail output is the usual place to read the neighbor management IP for R6.",
            "post_stem_html": '''    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/r5-r6-internet-topology-neighbor-discovery.png" alt="Topology: Internet connected to R5 Gi0/1; R5 Gi0/2 linked to R6 Gi0/2." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>''',
            "choices": [
                """Option A

R5(config)#int Gi0/1
R5(config-if)#no cdp enable
R5(config-if)#exit
R5(config)#lldp run
R5(config)#no cdp run
R5#sh cdp neighbor detail
R5#sh lldp neighbor""",
                """Option B

R5(config)#int Gi0/1
R5(config-if)#no cdp run
R5(config-if)#exit
R5(config)#lldp run
R5(config)#cdp enable
R5#sh cdp neighbor
R5#sh lldp neighbor""",
                """Option C

R5(config)#int Gi0/1
R5(config-if)#no cdp enable
R5(config-if)#exit
R5(config)#no lldp run
R5(config)#cdp run
R5#sh cdp neighbor detail
R5#sh lldp neighbor""",
                """Option D

R5(config)#int Gi0/1
R5(config-if)#no cdp enable
R5(config-if)#exit
R5(config)#no lldp run
R5(config)#cdp run
R5#sh cdp neighbor
R5#sh lldp neighbor""",
            ],
        },
        {
            "slug": "qos-voice-reduce-packet-loss",
            "title": "CCNA — QoS and voice packet loss",
            "stem": "How does QoS optimize voice traffic?",
            "name": "qosloss",
            "correct": "B",
            "explain": "Correct. B — Marking and priority/LLQ queuing protect voice from being dropped during congestion, reducing loss that would harm UDP-based real-time audio. QoS does not increase jitter on purpose and is not mainly about merging voice and video classes in this wording.",
            "choices": [
                "reducing bandwidth usage",
                "by reducing packet loss",
                "by differentiating voice and video traffic",
                "by increasing jitter",
            ],
        },
        {
            "slug": "dna-center-add-device-two-events",
            "title": "CCNA — DNA Center inventory defaults (choose two)",
            "stem": "Which two events occur automatically when a device is added to Cisco DNA Center? (Choose two)",
            "name": "dnaadd",
            "choose_two": True,
            "correct": ["A", "D"],
            "explain": "Correct. A and D — Newly discovered devices are placed in inventory under the Global site until reassigned, and are treated as managed under DNA Center for supported platforms. Provisioned is an outcome of a provisioning workflow; unmanaged/local site are not the usual paired defaults here.",
            "choices": [
                "The device is assigned to the Global site.",
                "The device is placed into the Unmanaged state.",
                "The device is placed into the Provisioned state.",
                "The device is placed into the Managed state.",
                "The device is assigned to the Local site.",
            ],
        },
        {
            "slug": "portfast-benefits-choose-two",
            "title": "CCNA — PortFast benefits (choose two)",
            "stem": "What are two benefits of using the PortFast feature? (Choose two)",
            "name": "pfb2",
            "choose_two": True,
            "correct": ["C", "E"],
            "explain": "Correct. C and E — PortFast moves an appropriate access port to forwarding immediately and avoids topology change notifications for those link transitions that would flush MAC tables network-wide. PortFast does not place ports in listening or impose a 50-second listen/learn delay.",
            "choices": [
                "Enabled interfaces are automatically placed in listening state",
                "Enabled interfaces wait 50 seconds before they move to the forwarding state",
                "Enabled interfaces never generate topology change notifications.",
                "Enabled interfaces that move to the learning state generate switch topology change notifications",
                "Enabled interfaces come up and move to the forwarding state immediately",
            ],
        },
        {
            "slug": "stp-portfast-bypass-states-choose-two",
            "title": "CCNA — PortFast bypassed STP states (choose two)",
            "stem": "Which two spanning-tree states are bypassed on an interface running PortFast? (Choose two)",
            "name": "stpfastst2",
            "choose_two": True,
            "correct": ["D", "E"],
            "explain": "Correct. D and E \u2014 On a classic 802.1D STP port, the normal progression toward forwarding includes listening and learning before forwarding. PortFast on an appropriate edge port skips those transitional states so the port can forward immediately. Forwarding (A) is the target state, not bypassed. Blocking (B) is not the pair described as skipped on link-up for PortFast edge behavior. disabled (C) is not one of the five STP port states in the same sense and is not what PortFast short-circuits.",
            "choices": [
                "forwarding",
                "blocking",
                "disabled",
                "learning",
                "listening",
            ],
        },
        {
            "slug": "unused-switchports-black-hole-vlan",
            "title": "CCNA — Unused ports security",
            "stem": "A network administrator is asked to configure VLANs 2, 3 and 4 for a new implementation. Some ports must be assigned to the new VLANs with unused remaining. Which action should be taken for the unused ports?",
            "name": "blkvlan",
            "correct": "B",
            "explain": "Correct. B — Place unused access ports in a dedicated unused (black-hole) VLAN and often shut them administratively so they do not sit in VLAN 1. Native VLAN tricks are for trunk hardening, not unused access ports. Access mode alone does not pick a safe VLAN.",
            "choices": [
                "configure port in the native VLAN",
                "configure ports in a black hole VLAN",
                "configure in a nondefault native VLAN",
                "configure ports as access ports",
            ],
        },
        {
            "slug": "dhcp-snooping-rate-limit-function",
            "title": "CCNA — DHCP snooping behavior",
            "stem": "Which function is performed by DHCP snooping?",
            "name": "dhcpsnp",
            "correct": "A",
            "explain": "Correct. A — DHCP snooping can rate-limit DHCP messages on untrusted ports and drop rogue server replies while building a binding table. It does not primarily forward multicast, mitigate broad DDoS, or propagate VLANs (that is VTP).",
            "choices": [
                "rate-limits certain traffic",
                "listens to multicast traffic for packet forwarding",
                "provides DDoS mitigation",
                "propagates VLAN information between switches",
            ],
        },
        {
            "slug": "dhcp-snooping-trust-server-same-switch-vlan1",
            "title": "CCNA — DHCP snooping trust toward server",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "The DHCP server and clients are connected to the same switch. What is the next step to complete the DHCP configuration to allow clients on VLAN 1 to receive addresses from the DHCP server?",
            "name": "dhcpsnpt1",
            "correct": "A",
            "explain": "Correct. A — When DHCP snooping is in use, access ports are untrusted by default and the switch drops DHCP server messages that arrive on untrusted ports. The interface toward the legitimate DHCP server must be set trusted (ip dhcp snooping trust) so offers and acknowledgments from that server are accepted. The ip dhcp relay information option command controls Option 82 insertion for DHCP relay agents across subnets, not marking the server port on the same VLAN. Trusting the client-facing port (D) would be the wrong side.",
            "post_stem_html": '''    <div class="exhibit-stack">
      <div class="cli-device" role="region" aria-label="Transcript of switch DHCP snooping commands">
        <h2>Switch (transcript)</h2>
        <pre>Switch# show ip dhcp snooping
Switch DHCP snooping is enabled
Switch DHCP gleaning is disabled
DHCP snooping is configured on following VLANs: 1
DHCP snooping is operational on following VLANs: 1
DHCP snooping is configured on the following L3 Interfaces:
Insertion of option 82 is disabled
circuit-id default format: vlan-mod-port
remote-id: aabb.cc00.6500 (MAC)
Option 82 on untrusted port is not allowed
Verification of hwaddr field is enabled
Verification of giaddr field is enabled
DHCP snooping trust/rate is configured on the following interfaces:
Interface              Trusted    Allow option    Rate limit (pps)
---------------------------------------------------------------</pre>
        <pre>Switch# show ip dhcp snooping statistics detail
Packets Processed by DHCP Snooping = 34
IDB not known                        = 0
Queue full                           = 0
Interface is in errdisabled          = 0
Rate limit exceeded                  = 0
Received on untrusted ports          = 32
Nonzero giaddr                       = 0
Source mac not equal to chaddr       = 0
No binding entry                     = 0
Insertion of opt82 fail              = 0
Unknown packet                       = 0
Interface Down                       = 0
Unknown output interface             = 0
Misdirected Packets                  = 0
Packets with Invalid Size            = 0
Packets with Invalid Option          = 0</pre>
      </div>
    </div>''',
            "choices": [
                "Configure the ip dhcp snooping trust command on the interface that is connected to the DHCP server",
                "Configure the ip dhcp relay information option command on the interface that is connected to the DHCP server",
                "Configure the ip dhcp relay information option command on the interface that is connected to the DHCP client",
                "Configure the ip dhcp snooping trust command on the interface that is connected to the DHCP client",
            ],
        },
        {
            "slug": "sdn-controller-centralizes-control-plane",
            "title": "CCNA — SDN controller plane",
            "stem": "Which plane is centralized by an SDN controller?",
            "name": "sdncp",
            "correct": "C",
            "explain": "Correct. C — The SDN controller centralizes control-plane functions and programs the infrastructure. Forwarding remains distributed in the data plane. Management and a vague services plane are not the standard answer here.",
            "choices": ["data plane", "management plane", "control plane", "services plane"],
        },
        {
            "slug": "utp-cat5e-cat6a-two-similarities",
            "title": "CCNA — Cat 5e vs Cat 6A (choose two)",
            "stem": "What are two similarities between UTP Cat 5e and Cat 6a cabling? (Choose two)",
            "name": "utp56",
            "choose_two": True,
            "correct": ["A", "D"],
            "explain": "Correct. A and D — Both support common horizontal lengths up to 100 m for their rated Ethernet applications, and both support at least 1 Gb/s Ethernet. 6A is 500 MHz class while 5e is 100 MHz; 10 GbE to 100 m is not a Cat 5e standard capability; 55 m is not the shared defining similarity.",
            "choices": [
                "Both support runs of up to 100 meters.",
                "Both support runs of up to 55 meters.",
                "Both operate at a frequency of 500 MHz.",
                "Both support speeds of at least 1 Gigabit.",
                "Both support speeds up to 10 Gigabit.",
            ],
        },
        {
            "slug": "ospf-dr-election-priority-options",
            "title": "CCNA — OSPF DR/BDR election change",
            "stem": "Refer to the exhibit. R5 is the current DR on the network, and R4 is the BDR. Their interfaces are flapping, so a network engineer wants the OSPF network to elect a different DR and BDR. Which set of configurations must the engineer implement? Option A: R4 Gi0/0 ip ospf priority 20; R5 Gi0/0 ip ospf priority 10. Option B: R2 priority 259; R3 priority 256. Option C: R3 priority 255; R2 priority 240. Option D: R5 priority 120; R4 priority 110.",
            "name": "ospfdr",
            "correct": "C",
            "explain": "Correct. C — Priorities must stay 0–255. Raising R3 and R2 above R4/R5 elects new DR/BDR among different routers. Option B is invalid (>255). Options A and D keep the DR/BDR pair among R4/R5 only.",
            "choices": ["Option A", "Option B", "Option C", "Option D"],
        },
        {
            "slug": "ospf-dr-election-router-a-area-zero",
            "title": "CCNA — OSPF DR election for router A (area 0)",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "Which action must be taken to ensure that router A is elected as the DR for OSPF area 0?",
            "name": "ospfadra0",
            "correct": "B",
            "explain": "Correct. B \u2014 On each OSPF broadcast or NBMA segment, the DR is elected using the highest OSPF interface priority on that segment (then router ID as a tie-breaker when priorities match). Giving router A\u2019s interface(s) on the segment a higher priority than routers B and C makes A the DR for that segment in area 0. The lowest priority (A) would not prefer A as DR. A fixed router ID (C) only helps break ties after priority; it does not by itself guarantee A wins if neighbors have higher priority or a higher RID with equal priority. Neighbor statements toward B and C (D) are not the normal control for DR election on Ethernet and do not replace priority/RID rules.",
            "post_stem_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/ospf-dr-election-router-a-area-zero-topology.png" alt="Topology: Routers A, B, and C in a triangle. A–B 192.168.2.0/24 (.1 on A Gi0/0/0, .2 on B Gi0/0/0); A–C 192.168.1.0/24 (.1 on A Gi0/0/1, .2 on C Gi0/0/0); B–C 192.168.3.0/24 (.2 on B Gi0/0/1, .1 on C Gi0/0/1)." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "choices": [
                "Configure the OSPF priority on router A with the lowest value between the three routers",
                "Configure the router A interfaces with the highest OSPF priority value within the area.",
                "Configure router A with a fixed OSPF router ID.",
                "Configure router B and router C as OSPF neighbors of router A.",
            ],
        },
        {
            "slug": "ospf-ia-route-metric-display",
            "title": "CCNA — OSPF metric in bracket notation",
            "stem": "Refer to the exhibit. R1#show ip route includes: O IA 192.168.10.32/28 [110/193] via 192.168.30.10, Serial0/0.1 (and other routes). What is the metric of the route to the 192.168.10.33/28 subnet?",
            "name": "ospfmet",
            "correct": "E",
            "explain": "Correct. E — In [AD/metric], 110 is the administrative distance and 193 is the OSPF cost. 192.168.10.33 falls inside 192.168.10.32/28.",
            "choices": ["84", "110", "128", "192", "193"],
        },
        {
            "slug": "access-layer-8021x-identity-security",
            "title": "CCNA — 802.1X identity at access layer",
            "stem": "Which access layer threat-mitigation technique provides security based on identity?",
            "name": "dot1x",
            "correct": "D",
            "explain": "Correct. D — 802.1X authenticates users or devices before granting network access via RADIUS. DAI and DHCP snooping rely on bindings rather than user identity. Native VLAN selection is unrelated to identity.",
            "choices": [
                "using a non-default native VLAN",
                "Dynamic ARP Inspection",
                "DHCP snooping",
                "802.1x",
            ],
        },
        {
            "slug": "dhcp-relay-different-subnet-forwarding",
            "title": "CCNA — DHCP across routed segments",
            "stem": "When a client and server are not on the same physical network, which device is used to forward requests and replies between client and server for DHCP?",
            "name": "dhcprel2",
            "correct": "A",
            "explain": "Correct. A — A DHCP relay agent (ip helper-address) forwards DHCP broadcasts as unicast between the client subnet and the DHCP server. The server answers leases but does not bridge broadcast domains alone. DHCPDISCOVER and DHCPOFFER are message types, not devices.",
            "choices": ["DHCP relay agent", "DHCP server", "DHCPDISCOVER", "DHCPOFFER"],
        },
        {
            "slug": "route-no-match-101016-discard",
            "title": "CCNA — No route for 10.10.10.16",
            "stem": "Refer to the exhibit. R1#show ip route includes: Gateway of last resort is not set; C 10.10.10.0/28 is directly connected, GigabitEthernet0/0; additional BGP/OSPF/EIGRP routes for other subnets that do not cover 10.10.10.16. Which action is taken when R1 receives a packet sourced from 10.10.10.2 and destined for 10.10.10.16?",
            "name": "rt1010",
            "correct": "A",
            "explain": "Correct. A — 10.10.10.0/28 covers 10.10.10.0–10.10.10.15. The destination 10.10.10.16 is outside that prefix, and no other route in the table matches 10.10.10.16 with no default route, so the router drops the packet (ICMP unreachable may be sent to the source on a connected subnet). Longest match does not invent a “similar” route; routers do not flood unknown unicast or queue indefinitely waiting for a route.",
            "choices": [
                "It discards the packets",
                "It uses a route that is similar to the destination address",
                "It floods packets to all learned next hops",
                "It queues the packets waiting for the route to be learned",
            ],
        },
        {
            "slug": "ssh-loopback-source-next-hop-10-0-1-15-exhibit",
            "title": "CCNA — Next hop for SSH to 10.0.1.15 from Loopback0",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "Traffic sourced from the loopback0 interface is trying to connect via ssh to the host at 10.0.1.15. What is the next hop to the destination address?",
            "name": "sshnxhop1",
            "correct": "A",
            "explain": "Correct. A \u2014 The routing table lists several matches for addresses inside 10.0.1.0/24, but 10.0.1.0/28 is a longer prefix than /24. Longest-prefix match therefore selects the EIGRP entry for 10.0.1.0/28 with next hop 192.168.0.7. Traffic originated from Loopback0 still uses the same destination lookup; the source only sets the packet\u2019s source IP. 192.168.0.4 is the next hop for the less-specific OSPF /24; 192.168.0.40 and 192.168.0.35 apply to /32 host routes; 192.168.3.5 is the connected Loopback0 address, not a next hop toward 10.0.1.15.",
            "post_stem_html": """    <div class="exhibit-stack">
      <div class="cli-device" role="region" aria-label="R1 show ip route output">
        <h2>R1# show ip route</h2>
        <pre>Codes: C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route

Gateway of last resort is not set
C        192.168.3.5 is directly connected, Loopback0
     10.0.0.0/8 is variably subnetted, 4 subnets, 2 masks
O        10.0.1.3/32 [110/100] via 192.168.0.40, 00:33:32, Serial0
C        10.0.1.0/24 is directly connected, Serial0
O        10.0.1.190/32 [110/5] via 192.168.0.35, 00:33:32, Serial0
O        10.0.1.0/24 [110/10] via 192.168.0.4, 00:33:32, GigabitEthernet0/0
D        10.0.1.0/28 [90/10] via 192.168.0.7, 00:33:32, GigabitEthernet0/0</pre>
      </div>
    </div>""",
            "choices": [
                "192.168.0.7",
                "192.168.0.4",
                "192.168.0.40",
                "192.168.3.5",
            ],
        },
        {
            "slug": "site-ab-tenge-sfp-sr-vs-lr-smf-intermittent-exhibit",
            "title": "CCNA — SiteA/SiteB intermittent connectivity (optics)",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "Shortly after SiteA was connected to SiteB over a new single-mode fiber path, users at SiteA report intermittent connectivity issues with applications hosted at SiteB. What is the cause of the intermittent connectivity issue?",
            "name": "siteabsfp1",
            "correct": "A",
            "explain": "Correct. A \u2014 The topology shows a multi-kilometer inter-site link; the CLIs show mismatched optics: SiteA reports SFP-SR (short-reach, typically multimode at 850 nm) while SiteB reports SFP-LR (long-reach, single-mode at 1310 nm). The scenario states a single-mode fiber span; SR is the wrong class of transceiver for that path compared with LR, and SR is also far outside its intended reach versus that distance, so the link can be marginal or intermittently usable even when the interface stays up. B is unlikely because the stem specifies single-mode fiber was installed. C does not fit: utilization affects queuing delay, not the classic pattern of flaky reachability from a layer-1 mismatch. D is unsupported: the exhibit does not list input or CRC errors.",
            "post_stem_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/site-ab-tenge-sfp-sr-vs-lr-smf-topology.png" alt="Topology: Site A cloud linked to Site B cloud; distance between sites about 7 km." width="900" decoding="async" loading="lazy" />
      </figure>
      <div class="cli-grid two-cols" role="group" aria-label="SiteA and SiteB show interface output">
        <div class="cli-device" role="region" aria-label="SiteA show interface TenGigabitEthernet0/1/0">
          <h2>SiteA# show interface TenGigabitEthernet0/1/0</h2>
          <pre>TenGigabitEthernet0/1/0 is up, line protocol is up
  Hardware is BUILT-IN-EPA-8x10G, address is aabb.cc00.0100 (bia aabb.cc00.0100)
  Description: Connection to SiteB
  Internet address is 10.10.10.1/30
  MTU 8146 bytes, BW 10000000 Kbit/sec, DLY 10 usec,
     reliability 255/255, txload 1/255, rxload 1/255
  Full Duplex, 10000Mbps, link type is force-up, media type is SFP-SR
  5 minute input rate 264797000 bits/sec, 26672 packets/sec
  5 minute output rate 122464000 bits/sec, 15724 packets/sec</pre>
        </div>
        <div class="cli-device" role="region" aria-label="SiteB show interface TenGigabitEthernet0/1/0">
          <h2>SiteB# show interface TenGigabitEthernet0/1/0</h2>
          <pre>TenGigabitEthernet0/1/0 is up, line protocol is up
  Hardware is BUILT-IN-EPA-8x10G, address is 0000.0c00.750c (bia 0000.0c00.750c)
  Description: Connection to SiteA
  Internet address is 10.10.10.2/30
  MTU 8146 bytes, BW 10000000 Kbit/sec, DLY 10 usec,
     reliability 255/255, txload 1/255, rxload 1/255
  Full Duplex, 10000Mbps, link type is force-up, media type is SFP-LR
  5 minute input rate 123245000 bits/sec, 15343 packets/sec
  5 minute output rate 265746000 bits/sec, 12453 packets/sec</pre>
        </div>
      </div>
    </div>""",
            "choices": [
                "An incorrect type of transceiver has been inserted into a device on the link.",
                "The wrong cable type was used to make the connection.",
                "Heavy usage is causing high latency.",
                "Physical network errors are being transmitted between the two sites.",
            ],
        },
        {
            "slug": "switch-host-a-to-d-unknown-dest-flood-exhibit",
            "title": "CCNA — Switch receives frame from Host A to Host D",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "Host A sent a data frame destined for host D. What does the switch do when it receives the frame from host A?",
            "name": "swahostd1",
            "correct": "C",
            "explain": "Correct. C \u2014 The MAC address table has no entry for host D\u2019s destination MAC, so the frame is unknown unicast at Layer 2. The switch floods it out every other port in that VLAN except the ingress port (Fa0/1). A port-security violation could err-disable a port, but nothing in the exhibit indicates that. A single unknown-unicast frame does not by itself imply a broadcast storm. The switch does not remove unrelated CAM entries when forwarding or flooding (D misstates both flooding and how the CAM table is updated).",
            "post_stem_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/switch-host-a-to-d-unknown-dest-flood-topology.png" alt="Topology: one switch with Host A on Fa0/1, Host B on Fa0/2, Host C on Fa0/3, and Host D on Fa0/4." width="900" decoding="async" loading="lazy" />
      </figure>
      <div class="cli-device" role="region" aria-label="SwitchA show mac-address table output">
        <h2>SwitchA# show mac-address table</h2>
        <pre>          Mac Address Table
-------------------------------------------

Vlan    Mac Address       Type        Ports
----    -----------       --------    -----
   2    000c.65dc.bb7b    DYNAMIC     Fa0/1
   2    0010.11dc.3e91    DYNAMIC     Fa0/2
   2    0041.48d7.c782    DYNAMIC     Fa0/3

Host A uses MAC address 000c.65dc.bb7b on Fa0/1.
Host D uses MAC address 00aa.bbcc.dd01 (not present in the table).
The frame arrives on Fa0/1 with destination MAC 00aa.bbcc.dd01.</pre>
      </div>
    </div>""",
            "choices": [
                "It shuts down the port Fa0/1 and places it in err-disable mode.",
                "It experiences a broadcast storm.",
                "It floods the frame out of all ports except port Fa0/1.",
                "It drops the frame from the switch CAM table.",
            ],
        },
        {
            "slug": "switch-sw1-pc2-mac-missing-fa02-trunk-exhibit",
            "title": "CCNA — SW1 PC2 missing from MAC table",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "An engineer has started to configure replacement switch SW1. To verify part of the configuration, the engineer issued the commands as shown and noticed that the entry for PC2 is missing. Which change must be applied to SW1 so that PC1 and PC2 communicate normally?",
            "name": "sw1pc2mac1",
            "correct": "C",
            "mono": True,
            "explain": "Correct. C \u2014 The topology shows both PCs in VLAN 2 (PC2 on Fa0/2 with MAC 0007.ec89.7513). The running configuration shows Fa0/2 in trunk mode with only VLAN 3 allowed on the trunk, while PC1 stays on access VLAN 2 at Fa0/1; the MAC table only lists VLAN 2 on Fa0/1 (PC1\u2019s 0007.ec53.4289), so PC2 does not appear for VLAN 2 as expected. Removing trunk mode and the restricted allowed-VLAN list, then configuring the port as access, restores a normal access edge so PC2 can be learned in VLAN 2 and talk to PC1. Option A keeps trunking and adjusts allowed VLANs in the wrong direction for this access-host scenario. Option B edits Fa0/1 and mixes access/trunk semantics on the wrong interface. Option D applies contradictory access and trunk commands on Fa0/1.",
            "post_stem_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/switch-sw1-pc2-mac-missing-fa02-topology.png" alt="Topology: SW1 with PC1 on Fa0/1 in VLAN 2 (MAC 0007.ec53.4289) and PC2 on Fa0/2 in VLAN 2 (MAC 0007.ec89.7513)." width="900" decoding="async" loading="lazy" />
      </figure>
      <div class="cli-device" role="region" aria-label="Sw1 show run and show mac-address-table output">
        <h2>Sw1# show run</h2>
        <pre>Building configuration...

interface FastEthernet0/1
 switchport access vlan 2
 switchport mode access
!
interface FastEthernet0/2
 switchport access vlan 2
 switchport trunk allowed vlan 3
 switchport mode trunk</pre>
        <h2>Sw1# show mac-address-table</h2>
        <pre>          Mac Address Table
-------------------------------------------

Vlan    Mac Address       Type        Ports
----    -----------       --------    -----
   2    0007.ec53.4289    DYNAMIC     Fa0/1</pre>
      </div>
    </div>""",
            "choices": [
                """SW1(config)#interface fa0/2
SW1(config-if)#no switchport access vlan 2
SW1(config-if)#no switchport trunk allowed vlan 3
SW1(config-if)#switchport trunk allowed vlan 2""",
                """SW1(config)#interface fa0/1
SW1(config-if)#no switchport access vlan 2
SW1(config-if)#switchport trunk native vlan 2
SW1(config-if)#switchport trunk allowed vlan 3""",
                """SW1(config)#interface fa0/2
SW1(config-if)#no switchport mode trunk
SW1(config-if)#no switchport trunk allowed vlan 3
SW1(config-if)#switchport mode access""",
                """SW1(config)#interface fa0/1
SW1(config-if)#no switchport access vlan 2
SW1(config-if)#switchport access vlan 3
SW1(config-if)#switchport trunk allowed vlan 2""",
            ],
        },
        {
            "slug": "gigabit-lx-t-l2-frame-similarity",
            "title": "CCNA — 1000BASE-LX vs 1000BASE-T",
            "stem": "What is a similarity between 1000BASE-LX and 1000BASE-T standards?",
            "name": "lxtx1",
            "correct": "A",
            "explain": "Correct. A — Both are IEEE 802.3 Gigabit Ethernet variants and share the same Ethernet data link framing (header, addresses, length/type, payload, FCS trailer). LX is fiber with fiber connectors; 1000BASE-T uses twisted pair and RJ-45. Distance limits differ (for example roughly 100 m for T vs longer fiber reaches for LX depending on fiber type).",
            "choices": [
                "Both use the same data-link header and trailer formats",
                "Both cable types support LP connectors",
                "Both cable types support RJ-45 connectors",
                "Both support up to 550 meters between nodes",
            ],
        },
        {
            "slug": "wpa3-sae-improves-security",
            "title": "CCNA — WPA3 improvement",
            "stem": "How does WPA3 improve security?",
            "name": "wpa3s1",
            "correct": "A",
            "explain": "Correct. A — WPA3-Personal uses Simultaneous Authentication of Equals (SAE) for passphrase-based networks, which mitigates offline dictionary attacks better than WPA2-Personal PSK alone. A 4-way handshake can still run for key confirmation but is not the defining WPA3 upgrade. RC4 and TKIP are legacy; WPA3 expects strong ciphers such as AES-GCMP.",
            "choices": [
                "It uses SAE for authentication.",
                "It uses a 4-way handshake for authentication.",
                "It uses RC4 for encryption.",
                "It uses TKIP for encryption.",
            ],
        },
        {
            "slug": "wireless-wpa3-perfect-forward-secrecy",
            "title": "CCNA — WPA3 and forward secrecy",
            "stem": "Which wireless security protocol relies on Perfect Forward Secrecy?",
            "name": "wpapfs1",
            "correct": "B",
            "explain": "Correct. B \u2014 WPA3 (notably WPA3-Personal with SAE / Dragonfly) derives fresh pairwise keys so compromise of a long-term passphrase does not let an attacker decrypt recorded traffic from earlier sessions\u2014the property described as forward secrecy / perfect forward secrecy in training materials. WPA and WPA2-PSK do not provide that guarantee in the same way; WEP is obsolete and fundamentally weak.",
            "choices": ["WPA", "WPA3", "WPA2", "WEP"],
        },
        {
            "slug": "subnet-en0-configured-ip-ifconfig-exhibit",
            "title": "CCNA — Subnet from en0 IPv4 configuration",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "A network engineer must provide configured IP addressing details to investigate a firewall rule issue. Which subnet and mask identify what is configured on the en0 interface?",
            "name": "en0sub1",
            "correct": "C",
            "explain": "Correct. C \u2014 The exhibit shows IPv4 10.8.138.14 with netmask 0xffffe000 (255.255.224.0), which is a /19. The network is 10.8.128.0/19 (hosts 10.8.128.1\u201310.8.159.254, broadcast 10.8.159.255). 10.8.0.0/16 is too broad. 10.8.64.0/18 does not include 10.8.138.x. 10.8.138.0/24 would imply a /24 mask (for example 0xffffff00), not /19.",
            "post_stem_html": """    <div class="exhibit-stack">
      <div class="exhibit-terminal-white" role="region" aria-label="ifconfig output for en0">
        <pre>MacOs$ ifconfig

en0: flags=8863&lt;UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST&gt; mtu 1500
	options=400&lt;CHANNEL_IO&gt;
	ether f0:18:98:8d:34:34
	inet6 fe80::492:c09f:57cc:3343%en0 prefixlen 64 secured scopeid 0x6
	inet 10.8.138.14 netmask 0xffffe000 broadcast 10.8.159.255
	nd6 options=201&lt;PERFORMNUD,DAD&gt;
	media: autoselect
	status: active</pre>
      </div>
    </div>""",
            "choices": [
                "10.8.0.0/16",
                "10.8.64.0/18",
                "10.8.128.0/19",
                "10.8.138.0/24",
            ],
        },
        {
            "slug": "subnet-split-10-70-128-19-two-vlans-choose-two",
            "title": "CCNA — Split 10.70.128.0/19 into /27 and /23 (choose two)",
            "stem": "A network engineer must configure two new subnets using the address block 10.70.128.0/19 to meet these requirements:\n\n\u2022 The first subnet must support 24 hosts.\n\u2022 The second subnet must support 472 hosts.\n\u2022 Both subnets must use the longest subnet mask possible from the address block.\n\nWhich two configurations must be used to configure the new subnets and meet a requirement to use the first available address in each subnet for the router interfaces? (Choose two)",
            "name": "sub70192",
            "choose_two": True,
            "mono": True,
            "correct": ["B", "C"],
            "explain": "Correct. B and C \u2014 Twenty-four hosts need at least five host bits (/27, 30 usable). Four hundred seventy-two hosts need at least nine host bits (/23, 510 usable). Those are the longest masks that still fit each size inside 10.70.128.0/19. Option B places the first usable address on 10.70.147.16/27 (10.70.147.17). Option C places the first usable address on 10.70.148.0/23 (10.70.148.1). Option A uses /26, which is wider than necessary for 24 hosts. Option D\u2019s address is not the first host of its /23 (that subnet\u2019s first host would be 10.70.158.1 for 10.70.158.0/23). Option E is a valid tight /27, but the pair that matches the usual ordering with a /23 for 472 hosts here is B and C.",
            "choices": [
                """interface vlan 4722
ip address 10.70.133.17 255.255.255.192""",
                """interface vlan 3002
ip address 10.70.147.17 255.255.255.224""",
                """interface vlan 1148
ip address 10.70.148.1 255.255.254.0""",
                """interface vlan 1234
ip address 10.70.159.1 255.255.254.0""",
                """interface vlan 155
ip address 10.70.155.65 255.255.255.224""",
            ],
        },
        {
            "slug": "capwap-lightweight-ap-mode",
            "title": "CCNA — CAPWAP and WLC AP mode",
            "stem": "Which mode must be set for APs to communicate to a Wireless LAN Controller using the Control and Provisioning of Wireless Access Points (CAPWAP) protocol?",
            "name": "capwapm1",
            "correct": "D",
            "explain": "Correct. D — Lightweight (split-MAC) access points discover and tunnel control (and optionally data) to the WLC using CAPWAP. Autonomous APs run the WLAN services locally and do not join a controller this way. Bridge and route are not the CAPWAP split-MAC operating mode names in this context.",
            "choices": [
                "bridge",
                "route",
                "autonomous",
                "lightweight",
            ],
        },
        {
            "slug": "etherchannel-lacp-active-switch2",
            "title": "CCNA — LACP EtherChannel not forming",
            "stem": "Refer to the exhibit. Which change to the configuration on Switch2 allows the two switches to establish an EtherChannel?",
            "name": "ethch2",
            "correct": "B",
            "explain": "Correct. B — With LACP, negotiation starts when at least one side is active; passive on both sides normally never brings the channel up. Changing Switch2 to active LACP fixes that. \"Mode on\" forces a static EtherChannel without LACP. Desirable is a PAgP mode, not LACP. PAgP auto with another side also passive does not form a channel either.",
            "choices": [
                "Change the protocol to EtherChannel mode on",
                "Change the LACP mode to active",
                "Change the LACP mode to desirable",
                "Change the protocol to PAgP and use auto mode",
            ],
            "post_stem_html": '''    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/etherchannel-lacp-passive-exhibit.png" alt="" width="980" decoding="async" loading="lazy" />
      </figure>
      <div class="cli-grid two-cols" role="group" aria-label="Transcript of exhibit CLI">
        <div class="cli-device">
          <h2>Switch1</h2>
          <pre>Switch1# show etherchannel summary
Flags:  D - down        P - bundled in port-channel
        I - stand-alone s - suspended
        H - Hot-standby (LACP only)
        R - Layer3          S - Layer2
        U - in use        f - failed to allocate aggregator
        u - unsuitable for bundling
        w - waiting to be aggregated
        d - default port

Number of channel-groups in use: 1
Number of aggregators:           1

Group  Port-channel  Protocol    Ports
------+-------------+-----------+-----------------------------------------------
1      Po1(SD)         LACP      Fa0/2(I)     Fa0/1(I)</pre>
          <pre>Switch1# show running-config
interface Port-channel1
!
interface FastEthernet0/1
 channel-group 1 mode passive
!
interface FastEthernet0/2
 channel-group 1 mode passive</pre>
        </div>
        <div class="cli-device">
          <h2>Switch2</h2>
          <pre>Switch2# show running-config
interface Port-channel1
!
interface FastEthernet0/1
 channel-group 1 mode passive
!
interface FastEthernet0/2
 channel-group 1 mode passive</pre>
        </div>
      </div>
    </div>''',
        },
        {
            "slug": "etherchannel-lacp-trunk-dynamic-industry-standard",
            "title": "CCNA — LACP trunk EtherChannel dynamic",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "Which configuration enables an EtherChannel to form dynamically between SW1 and SW2 by using an industry-standard protocol, and to support full IP connectivity between all PCs?",
            "post_stem_html": '''    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/etherchannel-lacp-trunk-dynamic-industry-standard-topology.png" alt="Topology: R1, SW1, SW2 with Po1 between switches and PCs in VLANs 6, 14, 77, 108, 109" width="980" decoding="async" loading="lazy" />
      </figure>
    </div>''',
            "name": "echlacptr1",
            "correct": "C",
            "mono": True,
            "explain": "Correct. C \u2014 The topology places hosts in different VLANs on either side of SW1\u2013SW2, so Po1 must be an 802.1Q trunk to carry those VLANs toward R1 for inter-VLAN routing. IEEE 802.3ad LACP is the industry-standard negotiation protocol for a dynamic EtherChannel; active on SW1 with passive on SW2 forms the bundle. Option A relies on mode on (no LACP negotiation) and PAgP auto (Cisco PAgP), not LACP. Option B puts trunk and access ports in the same channel-group (incompatible member parameters) and mixes PAgP auto with desirable rather than LACP. Option D mixes LACP active on SW1 with PAgP desirable on SW2, so the protocols do not match and the channel will not form reliably.",
            "choices": [
                """Option A

SW1#
interface Gi0/1
switchport
switchport mode trunk
channel-group 1 mode on
!
interface Gi0/2
switchport
switchport mode trunk
channel-group 1 mode auto

SW2#
interface Gi0/1
switchport
switchport mode trunk
channel-group 1 mode auto
!
interface Gi0/2
switchport
switchport mode trunk
channel-group 1 mode on
interface port-channel 1
switchport
switchport mode trunk""",
                """Option B

SW1#
interface Gi0/1
switchport
switchport mode trunk
channel-group 1 mode auto
!
interface Gi0/2
switchport
switchport mode access
channel-group 1 mode active

SW2#
interface gi0/1
switchport
switchport mode access
channel-group 1 mode desirable
!
interface Gi0/2
switchport
switchport mode access
channel-group 1 mode desirable""",
                """Option C

SW1#
interface Gi0/1
switchport
switchport mode trunk
channel-group 1 mode active
!
interface Gi0/2
switchport
switchport mode trunk
channel-group 1 mode active

SW2#
interface Gi0/1
switchport
switchport mode trunk
channel-group 1 mode passive
!
interface Gi0/2
switchport
switchport mode trunk
channel-group 1 mode passive""",
                """Option D

SW1#
interface Gi0/1
switchport
switchport mode access
channel-group 1 mode active
!
interface Gi0/2
switchport
switchport mode access
channel-group 1 mode active

SW2#
interface Gi0/1
switchport
switchport mode access
channel-group 1 mode desirable
!
interface Gi0/2
switchport
switchport mode access
channel-group 1 mode desirable""",
            ],
        },
        {
            "slug": "wireless-auth-layer2",
            "title": "CCNA — Wireless authentication layer",
            "stem": "Where does wireless authentication happen?",
            "name": "wlauth1",
            "correct": "D",
            "explain": "Correct. D — 802.11 Open System / association, 802.1X/EAP when used, and the WPA/WPA2/WPA3 four-way handshake operate at the MAC layer (Layer 2) before the station has an IP address on the WLAN. The SSID names the WLAN; the radio and band are physical-layer concerns, not where authentication is defined.",
            "choices": ["SSID", "radio", "band", "Layer 2"],
        },
        {
            "slug": "three-tier-workstation-to-workstation-path",
            "title": "CCNA — Three-tier campus path",
            "stem": "What is the path for traffic sent from one user workstation to another workstation on a separate switch in a three-layer architecture model?",
            "name": "tier3p1",
            "correct": "D",
            "explain": "Correct. D — In a hierarchical campus, traffic between endpoints on different access switches is typically routed or switched up to the distribution layer (often the VLAN/L3 boundary), crosses the core to the destination distribution pair/block, then down to that access switch. Paths that skip distribution for inter-switch traffic when those layers exist, or bounce access–distribution–distribution without the core backbone in the logical model taught for three-layer designs, miss that pattern.",
            "choices": [
                "access – core – distribution – access",
                "access – distribution – distribution – access",
                "access – core – access",
                "access – distribution – core – distribution – access",
            ],
        },
        {
            "slug": "fhrp-two-benefits-choose-two",
            "title": "CCNA — FHRP benefits (choose two)",
            "stem": "What are two benefits of FHRPs? (Choose two)",
            "name": "fhrp2b",
            "choose_two": True,
            "correct": ["D", "E"],
            "explain": "Correct. D and E — First Hop Redundancy Protocols (HSRP, VRRP, GLBP, etc.) present a shared virtual gateway (IP/virtual MAC) to clients while multiple routers cooperate, and the standby can take over quickly if the active device fails—default gateway failover. They do not prevent Layer 2 loops (that is spanning tree); they do not provide encryption by themselves; and they are not EtherChannel/link bundling.",
            "choices": [
                "They prevent loops in the Layer 2 network.",
                "They allow encrypted traffic.",
                "They are able to bundle multiple ports to increase bandwidth",
                "They enable automatic failover of the default gateway.",
                "They allow multiple devices to serve as a single virtual gateway for clients in the network",
            ],
        },
        {
            "slug": "ssid-purpose-identifies-wlan",
            "title": "CCNA — Purpose of the SSID",
            "stem": "What is the purpose of an SSID?",
            "name": "ssidpur1",
            "correct": "D",
            "explain": "Correct. D — The SSID is the human-readable name of a wireless LAN (BSS/ESS) that clients select when they join a network. Security comes from encryption and authentication mechanisms (for example WPA2/WPA3), not from the SSID alone. Traffic differentiation and per-AP identification are better described by other concepts (QoS VLAN design, BSSID/AP radio MAC), not the primary role of the SSID.",
            "choices": [
                "It provides network security",
                "It differentiates traffic entering access points",
                "It identifies an individual access point on a WLAN",
                "It identifies a WLAN",
            ],
        },
        {
            "slug": "ssid-two-characteristics-choose-two",
            "title": "CCNA — SSID characteristics (choose two)",
            "stem": "What are two characteristics of an SSID? (Choose two)",
            "name": "ssidch2",
            "choose_two": True,
            "correct": ["A", "D"],
            "explain": "Correct. A and D — Administrators can advertise the SSID in beacons (broadcast) or suppress it so the WLAN is harder to casually discover (“hidden”), though probing can still uncover it; 802.11 limits SSID payload to 32 octets. Individual AP radios are distinguished by BSSIDs (typically AP radio MACs), clients by their WLAN station addresses, and access security is enforced by WPA/WPA2/WPA3 and credentials, not merely the SSID name.",
            "choices": [
                "It can be hidden or broadcast in a WLAN",
                "It uniquely identifies an access point in a WLAN",
                "It uniquely identifies a client in a WLAN",
                "It is at most 32 characters long",
                "It provides secured access to a WLAN",
            ],
        },
        {
            "slug": "qos-llq-interactive-voice-video",
            "title": "CCNA — LLQ for voice and video",
            "stem": "In QoS, which prioritization method is appropriate for interactive voice and video?",
            "name": "qosllq1",
            "correct": "D",
            "explain": "Correct. D — Low-latency queuing (LLQ) attaches a strict-priority queue (often capped) for real-time classes such as voice and conferencing video before other queues are serviced, reducing delay and jitter. Expedited forwarding (EF) names a differentiated-services per-hop behavior and marking mindset; policing rate-limits traffic; plain round-robin does not grant the strict sequencing LLQ implies on Cisco platforms.",
            "choices": [
                "expedited forwarding",
                "traffic policing",
                "round-robin scheduling",
                "low-latency queuing",
            ],
        },
        {
            "slug": "sdn-southbound-api-controller-to-infrastructure",
            "title": "CCNA — Southbound API interaction",
            "stem": "Which communication interaction takes place when a southbound API is used?",
            "name": "sdnsbapi1",
            "correct": "B",
            "explain": "Correct. B — Southbound interfaces let the SDN controller program and monitor network devices (for example switches and routers) using protocols such as OpenFlow or NETCONF. Northbound APIs face applications and orchestration; end hosts are not the primary southbound peers.",
            "choices": [
                "between the SDN controller and PCs on the network",
                "between the SDN controller and switches and routers on the network",
                "between the SDN controller and services and applications on the network",
                "between network applications and switches and routers on the network",
            ],
        },
        {
            "slug": "sdn-controller-dynamic-changes-southbound-api",
            "title": "CCNA — SDN controller changes the network",
            "stem": "Which type of API allows SDN controllers to dynamically make changes to the network?",
            "name": "sdndyn1",
            "correct": "B",
            "explain": "Correct. B — Southbound interfaces connect the controller to infrastructure devices so it can install forwarding state, push configuration, and read telemetry (for example via OpenFlow, NETCONF, or similar). Northbound APIs are for applications and orchestration above the controller. REST and SOAP describe implementation styles, not the controller-to-device plane.",
            "choices": [
                "northbound API",
                "southbound API",
                "SOAP API",
                "REST API",
            ],
        },
        {
            "slug": "ipv6-link-local-scope-neighbor-discovery",
            "title": "CCNA — IPv6 link-local addresses",
            "stem": "Which statement best describes IPv6 link-local addresses (for example within the FE80::/10 scope)?",
            "name": "v6lla1",
            "correct": "C",
            "explain": "Correct. C — Link-local IPv6 addresses are only meaningful on a single Layer 3 link; hosts use them with Neighbor Discovery (RS/RA/NS/NA) and link-local next hops before global addressing is available. They are not globally routable like GUA prefixes, do not by themselves identify every workload worldwide, and are not about duplicating switch ASIC MAC tables.",
            "choices": [
                "They traverse the IPv6 backbone like globally unique provider addresses.",
                "They uniquely identify workloads across hybrid cloud providers without gateways.",
                "They operate only within a single routed link segment and back Neighbor Discovery procedures.",
                "They duplicate MAC addresses burned into switch ASIC forwarding tables.",
            ],
        },
        {
            "slug": "nat-inside-global-address-from-example",
            "title": "CCNA — NAT inside global naming",
            "stem": "NAT translates workstation 192.168.72.205 to IPv4 address 203.0.113.205 when forwarding traffic out to hosts on the public Internet. Inside Cisco IOS NAT terminology how is address 203.0.113.205 classified?",
            "name": "natig1",
            "correct": "A",
            "explain": "Correct. A — Inside global denotes the ISP-visible address mapped to represent an interior host toward the external network—in this illustration the PAT/NAT translated public-facing address replacing 192.168.72.205. Inside local is the private workstation address before NAT. Outside addresses describe remote destinations from the translating router\'s vantage point differently than this mapping.",
            "choices": [
                "inside global",
                "outside local",
                "inside local",
                "outside global",
            ],
        },
        {
            "slug": "switch-collision-domain-per-port",
            "title": "CCNA — Switches and collision domains",
            "stem": "Compared to shared Ethernet hubs how do modern Layer 2 switches handle collision domains on access ports?",
            "name": "cdom1",
            "correct": "B",
            "explain": "Correct. B — Each switch port is its own collision domain when devices run at full duplex; frames are switched between ports without shared coax-style collisions. Hubs repeat electrical signals so all attached hosts share one collision domain. VLAN membership controls broadcast scope, not what defines classic collision boundaries here.",
            "choices": [
                "They collapse every port into a single shared collision domain like classic hubs.",
                "They place each port in its own collision domain when operating at full duplex.",
                "They disable collision detection until trunk ports negotiate LACP.",
                "They map collision domains one-to-one with SVI interfaces only.",
            ],
        },
        {
            "slug": "icmp-echo-request-reply-ping",
            "title": "CCNA — ICMP echo for ping",
            "stem": "Successful IPv4 router-to-router connectivity tests that use the ping utility rely on which ICMP message pair?",
            "name": "icmp1",
            "correct": "B",
            "explain": "Correct. B — Ping sends ICMP Echo Request (type 8) and expects ICMP Echo Reply (type 0). Destination Unreachable (type 3) signals failures. Time Exceeded (type 11) supports traceroute. Redirect (type 5) is unrelated to echo/reply exchange.",
            "choices": [
                "ICMP Time Exceeded (type 11) and Redirect (type 5)",
                "ICMP Echo Request (type 8) and Echo Reply (type 0)",
                "ICMP Router Advertisement (type 9) and Router Solicitation (type 10)",
                "ICMP Parameter Problem (type 12) and Fragmentation Needed (type 4)",
            ],
        },
        {
            "slug": "acl-numbered-fifteen-standard-range",
            "title": "CCNA — Numbered standard ACL range",
            "stem": "An engineer configures a numbered IPv4 ACL using list number 15 on a Cisco IOS router. Which description matches ACL number 15?",
            "name": "acl15a",
            "correct": "B",
            "explain": "Correct. B — Legacy numbered standard IPv4 ACLs use 1–99 (and additional 1300–1999 range on many platforms). Extended numbered ACLs use 100–199 plus higher expansion ranges. IPv6 ACLs use different syntax; prefix lists are separate constructs.",
            "choices": [
                "It is a numbered extended IPv4 ACL by default.",
                "It is a numbered standard IPv4 ACL range entry.",
                "It is reserved exclusively for IPv6 traffic filtering.",
                "It always references a route-map instead of permit/deny statements.",
            ],
        },
        {
            "slug": "vty-access-class-permit-any-after-deny-pc1",
            "title": "CCNA — VTY access-class and standard ACL",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "The access list denies Telnet access from PC-1 to RTR-1 and should allow it from other hosts. PC-2 gets \u201c% Connection refused by remote host\u201d when trying to Telnet. Without permitting Telnet from PC-1, what must be done to allow the traffic?",
            "name": "vtyacl1",
            "correct": "A",
            "explain": "Correct. A — A standard ACL ends with an implicit deny any. If ACL 10 only lists a deny for PC-1\u2019s address, every other source (including PC-2) still hits that implicit deny when access-class applies it inbound on the VTY lines. Add an explicit permit any after the PC-1 deny so other hosts are allowed while PC-1 remains denied. Removing the access-class (B) would drop the filter entirely and typically allow PC-1 again. Applying the ACL outbound on G0/0 (C) filters forwarded traffic through the interface, not VTY management sessions to the router. Removing the VTY password (D) does not fix ACL filtering.",
            "post_stem_html": '''    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/vty-access-class-rtr1-sw1-pc-topology.png" alt="Topology: RTR-1 G0/0 10.150.1.254/24 to SW1; PC-1 10.150.1.1 and PC-2 10.150.1.2 on the same LAN." width="900" decoding="async" loading="lazy" />
      </figure>
      <div class="cli-device" role="region" aria-label="RTR-1 partial running configuration">
        <h2>RTR-1 (partial config)</h2>
        <pre>hostname RTR-1
!
interface GigabitEthernet0/0
 ip address 10.150.1.254 255.255.255.0
 duplex auto
 speed auto
!
access-list 10 deny host 10.150.1.1
!
line con 0
 password 7 083238384A11
 login
!
line vty 0 4
 access-class 10 in
 password 7 083238384A11
 login
!
end</pre>
      </div>
    </div>''',
            "choices": [
                "Add the access-list 10 permit any command to the configuration",
                "Remove the access-class 10 in command from line vty 0 4.",
                "Add the ip access-group 10 out command to interface g0/0.",
                "Remove the password command from line vty 0 4.",
            ],
        },
        {
            "slug": "switchport-priority-extend-trust-ip-phone-access",
            "title": "CCNA — Priority extend through IP phone",
            "stem": "An engineer is configuring data and voice services to pass through the same port. The designated switch interface fastethernet0/1 must transmit packets using the same priority for data when they are received from the access port of the IP phone. Which configuration must be used?",
            "name": "prexph1",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D — On a Cisco access port facing an IP phone, \"switchport priority extend trust\" causes the switch to trust the ingress CoS markings from stations connected to the phone's PC/access port when those frames traverse the phone to the switch uplink—preserving priority rather than overwriting it. Using \"priority extend cos <value>\" applies a fixed CoS instead of trusting received priorities. Voice VLAN options \"untagged\" and \"dot1p\" steer how voice traffic tagging/priority signaling is negotiated on the auxiliary voice VLAN—they do not substitute for priority extension on bridged downstream data frames.",
            "choices": [
                "interface fastethernet0/1\nswitchport priority extend cos 7",
                "interface fastethernet0/1\nswitchport voice vlan untagged",
                "interface fastethernet0/1\nswitchport voice vlan dot1p",
                "interface fastethernet0/1\nswitchport priority extend trust",
            ],
        },
        {
            "slug": "spanning-tree-portfast-supported-access-ports",
            "title": "CCNA — PortFast and port roles",
            "stem": "Which port type supports the spanning-tree portfast command without additional configuration?",
            "name": "stpftport1",
            "correct": "A",
            "explain": "Correct. A — PortFast is designed for Layer 2 ports that connect single end devices (access/edge ports): the port can go to forwarding immediately without the listen/learn delay. Routed (Layer 3 main or sub) interfaces are not STP switchports in the usual sense. Trunks carry multiple VLANs toward other bridges; enabling PortFast there can be dangerous and on many platforms requires explicit extra syntax (for example portfast trunk / edge trunk) rather than the basic access-style command alone.",
            "choices": [
                "access ports",
                "Layer 3 main interfaces",
                "Layer 3 subinterfaces",
                "trunk ports",
            ],
        },
        {
            "slug": "syslog-facility-definition",
            "title": "CCNA — Syslog facility",
            "stem": "What is a syslog facility?",
            "name": "sysfac1",
            "correct": "D",
            "explain": "Correct. D — In syslog each message carries a facility code (for example KERNEL, MAIL, LOCAL0–LOCAL7) that classifies which subsystem or IOS process bucket produced the entry. Severity is separate (level of urgency). The logging host/server is the collector; SNMP-style passwords for syslog are outside this definition.",
            "choices": [
                "host that is configured for the system to send log messages",
                "password that authenticates a Network Management System to receive log messages",
                "group of log messages associated with the configured severity level",
                "set of values that represent the processes that can generate a log message",
            ],
        },
        {
            "slug": "public-cloud-two-characteristics-choose-two",
            "title": "CCNA — Public cloud traits (choose two)",
            "stem": "What are two characteristics of a public cloud implementation? (Choose two)",
            "name": "pubcld2",
            "choose_two": True,
            "correct": ["A", "C"],
            "explain": "Correct. A and C — A public CSP builds and operates the shared underlying platform once and sells capacity to many tenants (multi-organization sharing), while customers usually reach those services across the Internet. Full bespoke control over every facet of deployment (B) is more aligned with private/on‑prem extremes. Dedicated single-company stacks (D) resemble private/hosted offerings. Combining third‑party utility with privately owned/on‑prem workloads (E) describes hybrid—not the defining pair for public-only.",
            "choices": [
                "It is owned and maintained by one party, but it is shared among multiple organizations",
                "It enables an organization to fully customize how it deploys network resources",
                "It provides services that are accessed over the Internet",
                "It is a data center on the public Internet that maintains cloud services for only one company",
                "It supports network resources from a centralized third-party provider and privately-owned virtual resources",
            ],
        },
        {
            "slug": "ipsec-pure-traffic-unicast-ip",
            "title": "CCNA — Traffic carried by pure IPsec",
            "stem": "Which type of traffic is sent with pure IPsec?",
            "name": "ipsecpure1",
            "correct": "D",
            "explain": "Correct. D — IPsec protects IP packets—most training scenarios highlight unicast IPv4/IPv6 flows between peers or across a tunnel to a central site. Layer 2 broadcasts (for example ARP-style discovery in A), raw STP exchanges (C), and classic L2 bridging behavior are outside what “pure” IPsec terminates; multicast (B) needs specific design and is not the textbook match when contrasted with straightforward site-to-site host-to-server unicast.",
            "choices": [
                "broadcast packets from a switch that is attempting to locate a MAC address at one of several remote sites",
                "multicast traffic from a server at one site to hosts at another location",
                "spanning-tree updates between switches that are at two different sites",
                "unicast messages from a host at a remote site to a server at headquarters",
            ],
        },
        {
            "slug": "dhcp-workstation-blocked-8021x",
            "title": "CCNA — Blocking DHCP on a port",
            "stem": "What prevents a workstation from receiving a DHCP address?",
            "name": "dhcpblk1",
            "correct": "D",
            "explain": "Correct. D — IEEE 802.1X port-based access control keeps the port unauthorized until the client authenticates; until then user data (including DHCP) is not allowed on the voice/data VLAN. Some items misprint this option as “802.10”—the standard is 802.1X. DTP only negotiates trunking. VTP distributes VLAN information. STP can delay forwarding on an access link without PortFast, but it does not implement the same deliberate access-denial gate as 802.1X.",
            "choices": [
                "DTP",
                "STP",
                "VTP",
                "IEEE 802.1X",
            ],
        },
        {
            "slug": "ftp-control-data-connections-capability",
            "title": "CCNA — FTP capabilities",
            "stem": "What is a capability of FTP in network management operations?",
            "name": "ftpmgmt1",
            "correct": "A",
            "explain": "Correct. A — FTP opens a TCP control channel (commands, usually port 21) and a separate TCP data channel for transferring file contents (active or passive negotiation). It does not rely on UDP for transfers. Classic FTP does not inherently encrypt payload or credentials without FTPS/TLS; it is also standards-based (RFC 959), not a proprietary session-layer scheme.",
            "choices": [
                "uses separate control and data connections to move files between server and client",
                "devices are directly connected and use UDP to pass file information",
                "encrypts data before sending between data resources",
                "offers proprietary support at the session layer when transferring data",
            ],
        },
        {
            "slug": "static-default-route-r1-r2-two-sites-exhibit",
            "title": "CCNA — Static routing across WAN",
            "stem": "A network engineer is in the process of establishing IP connectivity between two sites. Routers R1 and R2 are partially configured with IP addressing. Both routers have the ability to access devices on their respective LANs. Refer to the exhibit. Which command set configures the IP connectivity between devices located on both LANs in each site?",
            "name": "sr12sites1",
            "correct": "B",
            "mono": True,
            "explain": "Correct. B — R1 learns 10.1.1.0/24 only through R2; a default route to R2 WAN address 209.165.200.226 sends all unknown prefixes (including R2 LAN) across the interconnect. Likewise R2 points its default toward R1 WAN 209.165.200.225. Option A points each router at its own WAN address. Options C/D use incorrect prefixes/outgoing-interface choices (routes toward local subnets or meaningless host-route wording on LAN interfaces). More specific statics to each LAN would also work but are not listed.",
            "choices": [
                "R1\nip route 0.0.0.0 0.0.0.0 209.165.200.225\nR2\nip route 0.0.0.0 0.0.0.0 209.165.200.226",
                "R1\nip route 0.0.0.0 0.0.0.0 209.165.200.226\nR2\nip route 0.0.0.0 0.0.0.0 209.165.200.225",
                "R1\nip route 192.168.1.0 255.255.255.0 GigabitEthernet0/0\nR2\nip route 10.1.1.1 255.255.255.0 GigabitEthernet0/0",
                "R1\nip route 192.168.1.1 255.255.255.0 GigabitEthernet0/1\nR2\nip route 10.1.1.1 255.255.255.0 GigabitEthernet0/1",
            ],
            "post_stem_html": '''    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/static-route-r1-r2-two-sites-topology.png" alt="" width="900" decoding="async" loading="lazy" />
      </figure>
    </div>''',
        },
        {
            "slug": "collapsed-core-small-organization-cost",
            "title": "CCNA — Collapsed core use case",
            "stem": "Which type of organization should use a collapsed-core architecture?",
            "name": "colcore1",
            "correct": "B",
            "explain": "Correct. B — A collapsed core folds core and distribution duties into one simplified layer, cutting device count and capex—well suited to smaller sites with modest scale. Large enterprises that demand modular growth, pervasive redundancy, or strict hierarchical boundaries instead implement (or migrate toward) a traditional three‑tier campus or spine/leaf variants. Dramatic impending growth usually steers planners beyond a purely collapsed topology.",
            "choices": [
                "large and requires a flexible, scalable network design",
                "small and needs to reduce networking costs currently",
                "large and must minimize downtime when hardware fails",
                "small but is expected to grow dramatically in the near future",
            ],
        },
        {
            "slug": "ipv6-route-r17-ping-r18-wan-interface",
            "title": "CCNA — IPv6 static route toward R18 WAN",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "Which IPv6 configuration is required for R17 to successfully ping the WAN interface on R18?",
            "name": "v617r181",
            "correct": "A",
            "mono": True,
            "explain": "Correct. A — The router enables IPv6 routing with ipv6 unicast-routing, keeps the pictured interface addresses on FastEthernet0/0 (toward R16) and FastEthernet1/0 (toward R18), and installs a recursion-free static toward 2001:db8:4::/64 via the on-link neighbor 2001:db8:3::301—the address R18 owns on Fa1/0 facing R17—so echo requests reach Fa0/0 on R18 in 2001:db8:4::/64. Option B sends traffic toward local Fa0/0 instead of R18. Option C omits ipv6 unicast-routing, swaps LAN addressing on the wrong physical interfaces, and uses an irrelevant next hop on the PC segment. Option D omits ipv6 unicast-routing, adds only CEF, and references PC2 as a next hop that is not adjacent on the R17–R18 link.",
            "choices": [
                """Option A

R17#
!
no ip domain lookup
ip cef
ipv6 unicast-routing
!
interface FastEthernet0/0
no ip address
duplex auto
speed auto
ipv6 address 2001:DB8:2::201/64
!
interface FastEthernet1/0
no ip address
duplex auto
speed auto
ipv6 address 2001:DB8:3::201/64
!
no cdp log mismatch duplex
ipv6 route 2001:DB8:4::/64 2001:DB8:3::301""",
                """Option B

R17#
!
no ip domain lookup
ip cef
ipv6 unicast-routing
!
interface FastEthernet0/0
no ip address
duplex auto
speed auto
ipv6 address 2001:DB8:2::201/64
!
interface FastEthernet1/0
no ip address
duplex auto
speed auto
ipv6 address 2001:DB8:3::201/64
!
no cdp log mismatch duplex
ipv6 route 2001:DB8:4::/64 2001:DB8:2::201""",
                """Option C

R17#
!
no ip domain lookup
ip cef
!
interface FastEthernet0/0
no ip address
duplex auto
speed auto
ipv6 address 2001:DB8:3::201/64
!
interface FastEthernet1/0
no ip address
duplex auto
speed auto
ipv6 address 2001:DB8:2::201/64
!
no cdp log mismatch duplex
ipv6 route 2001:DB8:4::/64 2001:DB8:5::101""",
                """Option D

R17#
!
no ip domain lookup
ip cef
ipv6 cef
!
interface FastEthernet0/0
no ip address
duplex auto
speed auto
ipv6 address 2001:DB8:2::201/64
!
interface FastEthernet1/0
no ip address
duplex auto
speed auto
ipv6 address 2001:DB8:3::201/64
!
no cdp log mismatch duplex
ipv6 route 2001:DB8:4::/64 2001:DB8:4::302""",
            ],
            "post_stem_html": '''    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/ipv6-route-r17-r18-wan-exhibit.png" alt="" width="900" decoding="async" loading="lazy" />
      </figure>
    </div>''',
        },
        {
            "slug": "ipv6-anycast-unicast-multiple-interfaces",
            "title": "CCNA — IPv6 anycast addressing",
            "stem": "Which type of IPv6 address is similar to a unicast address but is assigned to multiple devices on the same network at the same time?",
            "name": "v6any1",
            "correct": "B",
            "explain": "Correct. B — An anycast address is a unicast IPv6 address that is configured on more than one interface; routing then delivers traffic to the nearest/topologically closest instance. Multicast is one-to-many group delivery, not unicast-like. Global unicast and link-local addresses are normally treated as unique per interface in ordinary addressing practice.",
            "choices": [
                "global unicast address",
                "anycast address",
                "multicast address",
                "link-local address",
            ],
        },
        {
            "slug": "radius-access-request-password-encrypted",
            "title": "CCNA — RADIUS Access-Request encryption",
            "stem": "Which field within the access-request packet is encrypted by RADIUS?",
            "name": "radpwd1",
            "correct": "D",
            "explain": "Correct. D — The User-Password attribute is obscured using the shared secret and the Request Authenticator (MD5-based hiding per RFC 2865). User-Name is typically sent in cleartext. The Authenticator field participates in the algorithm but is not \u201cthe encrypted field\u201d in this sense.",
            "choices": [
                "authorized services",
                "authenticator",
                "username",
                "password",
            ],
        },
        {
            "slug": "ngips-user-activity-network-events",
            "title": "CCNA — Next-Generation IPS",
            "stem": "What is a function of a Next-Generation IPS?",
            "name": "ngips1",
            "correct": "D",
            "explain": "Correct. D — NGIPS adds context such as application and user identity and ties that to security events. MAC learning is switching. SDN controller roles and 802.1X/RADIUS at Layer 2 describe other components.",
            "choices": [
                "makes forwarding decisions based on learned MAC addresses",
                "serves as a controller within a controller-based network",
                "integrates with a RADIUS server to enforce Layer 2 device authentication rules",
                "correlates user activity with network events",
            ],
        },
        {
            "slug": "ipv6-unicast-vs-anycast-assignment",
            "title": "CCNA — IPv6 unicast vs anycast",
            "stem": "What is the difference between IPv6 unicast and anycast addressing?",
            "name": "v6uvsany",
            "correct": "A",
            "explain": "Correct. A — Ordinary unicast use assigns the address to one interface; the same unicast address configured on multiple interfaces on different nodes is anycast, with routing delivering to the nearest instance. D reverses the definitions. B and C misstate configuration requirements.",
            "choices": [
                "An individual IPv6 unicast address is supported on a single interface on one node but an IPv6 anycast address is assigned to a group of interfaces on multiple nodes.",
                "IPv6 unicast nodes must be explicitly configured to recognize the unicast address, but IPv6 anycast nodes require no special configuration",
                "IPv6 anycast nodes must be explicitly configured to recognize the anycast address, but IPv6 unicast nodes require no special configuration",
                "Unlike an IPv6 anycast address, an IPv6 unicast address is assigned to a group of interfaces on multiple nodes",
            ],
        },
        {
            "slug": "data-plane-fib-lookup-action",
            "title": "CCNA — Data plane and FIB",
            "stem": "Which action is taken by the data plane within a network device?",
            "name": "dpfib1",
            "correct": "A",
            "explain": "Correct. A — The data plane performs high-speed forwarding using the Forwarding Information Base (and related tables) derived from control-plane routing state. Building the IP routing table via routing protocols (B) is control plane. CLI access (C) is management plane. Forwarding to the next hop (D) is also data plane, but FIB lookup is the precise contrast to routing-table construction in exam-style wording.",
            "choices": [
                "looks up an egress interface in the forwarding information base",
                "constructs a routing table based on a routing protocol",
                "provides CLI access to the network device",
                "forwards traffic to the next hop",
            ],
        },
        {
            "slug": "rapid-pvst-plus-per-vlan-instance",
            "title": "CCNA — Rapid PVST+ instances",
            "stem": "How does Rapid PVST+ create a fast loop-free network topology?",
            "name": "rpvst1",
            "correct": "C",
            "explain": "Correct. C — Rapid PVST+ runs RSTP separately per VLAN (one spanning-tree instance per VLAN). Mapping many VLANs into one instance describes MST/CST-style designs, not PVST+. Multiple active L2 paths to the same station would imply loops without blocking.",
            "choices": [
                "It requires multiple links between core switches",
                "It maps multiple VLANs into the same spanning-tree instance",
                "It generates one spanning-tree instance for each VLAN",
                "It uses multiple active paths between end stations",
            ],
        },
        {
            "slug": "wlc-telnet-mitm-management",
            "title": "CCNA — WLC management protocol risk",
            "stem": "Which WLC management connection type is vulnerable to man-in-the-middle attacks?",
            "name": "wlctel1",
            "correct": "C",
            "explain": "Correct. C — Telnet sends credentials and session data in cleartext, so an on-path attacker can intercept or alter sessions. SSH and HTTPS encrypt traffic. Console is typically a local physical session rather than in-band network Telnet.",
            "choices": ["SSH", "HTTPS", "Telnet", "console"],
        },
        {
            "slug": "aaa-authentication-identity-verification",
            "title": "CCNA — Authentication vs authorization and accounting",
            "stem": "Which characteristic differentiates the concept of authentication from authorization and accounting?",
            "name": "aaaauth1",
            "correct": "D",
            "explain": "Correct. D — Authentication verifies identity (\u201cwho are you?\u201d). Authorization defines permitted actions or service limits; accounting logs activity and can support billing\u2014those map to the other options.",
            "choices": [
                "user-activity logging",
                "service limitations",
                "consumption-based billing",
                "identity verification",
            ],
        },
        {
            "slug": "syn-flood-half-open-tcp-resources",
            "title": "CCNA — SYN flood attack",
            "stem": "Which type of network attack overwhelms the target server by sending multiple packets to a port until the half-open TCP resources of the target are exhausted?",
            "name": "synfl1",
            "correct": "A",
            "explain": "Correct. A — A SYN flood sends many TCP SYNs without completing handshakes, filling half-open connection state. Reflection and amplification misuse third-party responders. Teardrop abuses IP fragmentation handling.",
            "choices": ["SYN flood", "reflection", "teardrop", "amplification"],
        },
        {
            "slug": "lightweight-ap-centralized-access-mode",
            "title": "CCNA — LAP switchport in centralized WLAN",
            "stem": "Which interface mode must be configured to connect the lightweight APs in a centralized architecture?",
            "name": "lwapacc1",
            "correct": "D",
            "explain": "Correct. D — In centralized mode, client traffic is typically tunneled in CAPWAP to the WLC, so the AP uplink is often a single access VLAN for management and CAPWAP. Trunks are common when the AP must carry multiple locally switched VLANs (for example FlexConnect).",
            "choices": ["WLAN dynamic", "management", "trunk", "access"],
        },
        {
            "slug": "data-plane-actions-8021q-mac-lookup",
            "title": "CCNA — Data plane actions (choose two)",
            "stem": "Which two network actions occur within the data plane? (Choose two)",
            "name": "dpchk1",
            "choose_two": True,
            "correct": ["A", "E"],
            "explain": "Correct. A and E — Rewriting 802.1Q tags and performing MAC table lookups are switch forwarding-plane tasks. NETCONF configuration, routing protocols, and replying to ICMP echo to the device itself are control or management plane activities.",
            "choices": [
                "Add or remove an 802.1Q trunking header.",
                "Make a configuration change from an incoming NETCONF RPC.",
                "Run routing protocols.",
                "Reply to an incoming ICMP echo request.",
                "Match the destination MAC address to the MAC address table.",
            ],
        },
        {
            "slug": "wlc-centralized-auth-roaming",
            "title": "CCNA — Centralized WLAN control",
            "stem": "What provides centralized control of authentication and roaming in an enterprise network?",
            "name": "wlcroam1",
            "correct": "C",
            "explain": "Correct. C — The Wireless LAN controller centralizes policies, AAA integration, and roaming coordination for lightweight APs. A lightweight AP is the edge radio; firewalls and LAN switches do not fill that WLAN controller role.",
            "choices": [
                "a lightweight access point",
                "a firewall",
                "a wireless LAN controller",
                "a LAN switch",
            ],
        },
        {
            "slug": "owe-opportunistic-wireless-encryption",
            "title": "CCNA — Opportunistic Wireless Encryption",
            "stem": "What is a function of Opportunistic Wireless Encryption in an environment?",
            "name": "owe1",
            "correct": "D",
            "explain": "Correct. D — OWE (often called Enhanced Open) encrypts the wireless link on an otherwise open SSID so frames are not sent in cleartext. It is not WEP, not primarily compression, and does not replace full subscriber authentication like WPA2-Enterprise.",
            "choices": [
                "offer compression",
                "increase security by using a WEP connection",
                "provide authentication",
                "protect traffic on open networks",
            ],
        },
        {
            "slug": "physical-access-ip-cameras-monitoring",
            "title": "CCNA — Physical access control",
            "stem": "Which action implements physical access control as part of the security program of an organization?",
            "name": "phyipc1",
            "correct": "A",
            "explain": "Correct. A — Cameras monitor physical areas and critical infrastructure as part of a physical security program. Remote syslog backup is operational logging. Enable and console passwords protect device administration, not facility perimeter control.",
            "choices": [
                "setting up IP cameras to monitor key infrastructure",
                "backing up syslogs at a remote location",
                "configuring enable passwords on network devices",
                "configuring a password for the console port",
            ],
        },
        {
            "slug": "qos-marking-tos-ipv4-field",
            "title": "CCNA — QoS marking and IPv4 ToS",
            "stem": "Which QoS per-hop behavior changes the value of the ToS field in the IPv4 packet header?",
            "name": "qosmrk1",
            "correct": "B",
            "explain": "Correct. B — Marking sets IP precedence or DSCP in the IPv4 differentiated-services byte (historically called ToS). Classification categorizes traffic; policing and shaping mainly enforce rates (policing may remark as a side effect).",
            "choices": ["shaping", "marking", "policing", "classification"],
        },
        {
            "slug": "qos-trust-boundary-access-phone-pc-exhibit",
            "title": "CCNA — QoS trust boundary and marking",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "Which plan must be implemented to ensure optimal QoS marking practices on this network?",
            "name": "qostrustbnd1",
            "correct": "B",
            "explain": "Correct. B \u2014 IP phones mark voice traffic consistently and are treated as trusted sources at the access edge. PCs are untrusted: they can set arbitrary DSCP/CoS, so traffic from SW2 should be classified and marked on the switch rather than trusted. Broadly trusting all markings at the access layer (A, C, D) is not optimal, and relying on remarking only at MLS1 or R1 does not replace a proper access-layer trust boundary for the PC.",
            "post_stem_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/qos-trust-boundary-access-sw1-phone-sw2-pc-topology.png" alt="Topology: MPLS cloud to R1, R1 to MLS1; MLS1 to access switches SW1 (IP phone) and SW2 (PC)." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "choices": [
                "As traffic enters from the access layer on SW1 and SW2, trust all traffic markings",
                "Trust the IP phone markings on SW1 and mark traffic entering SW2 at SW2",
                "As traffic traverses MLS1 remark the traffic, but trust all markings at the access layer",
                "Remark traffic as it traverses R1 and trust all markings at the access layer",
            ],
        },
        {
            "slug": "wlc-lag-link-redundancy-load-balance",
            "title": "CCNA — LAG on a Cisco WLC",
            "stem": "What is one reason to implement LAG on a Cisco WLC?",
            "name": "wlclag1",
            "correct": "B",
            "explain": "Correct. B — LAG bundles multiple WLC distribution ports for higher throughput and resilience if a member link fails, with traffic spread across links. It does not encrypt management frames, is not controller SSO failover by itself, and does not mean arbitrary different VLANs per failed link.",
            "choices": [
                "to increase security and encrypt management frames",
                "to provide link redundancy and load balancing",
                "to allow for stateful and link-state failover",
                "to enable connected switch ports to failover and use different VLANs",
            ],
        },
        {
            "slug": "wlc-lag-configure-remove-reboot-requirement",
            "title": "CCNA — WLC LAG configuration requirement",
            "stem": "What is a requirement when configuring or removing LAG on a WLC?",
            "name": "wlclagreq1",
            "correct": "B",
            "explain": "Correct. B \u2014 On Cisco Wireless LAN Controllers, changing LAG (enabling, disabling, or reconfiguring the bundle) requires a controller reboot so the distribution-port layout is applied correctly. You do not satisfy LAG by separately declaring arbitrary incoming/outgoing port flows for traffic (A). Disabling LAG does not universally force a management-interface reassignment as the stated blanket requirement (C). Multiple untagged interfaces on one physical port is not a WLC LAG requirement (D).",
            "choices": [
                "The incoming and outgoing ports for traffic flow must be specified if LAG is enabled.",
                "The controller must be rebooted after enabling or reconfiguring LAG.",
                "The management interface must be reassigned if LAG is disabled.",
                "Multiple untagged interfaces on the same port must be supported.",
            ],
        },
        {
            "slug": "poe-static-mode-guaranteed-power",
            "title": "CCNA — PoE static mode",
            "stem": "Which PoE mode enables powered-device detection and guarantees power when the device is detected?",
            "name": "poest1",
            "correct": "B",
            "explain": "Correct. B — Static PoE reserves a configured power budget on the port (high-priority treatment) so capacity is guaranteed for the PD. Auto discovers and allocates power but does not carry the same guaranteed reservation meaning in Cisco\u2019s auto vs static model.",
            "choices": ["dynamic", "static", "active", "auto"],
        },
        {
            "slug": "switch-access-vlan20-voice-vlan30",
            "title": "CCNA — Access and voice VLAN on one port",
            "stem": "A Cisco engineer must configure a single switch interface to meet these requirements: accept untagged frames and place them in VLAN 20; accept tagged frames in VLAN 30 when CDP detects a Cisco IP phone. Which command set must the engineer apply?",
            "name": "swvv1",
            "correct": "A",
            "mono": True,
            "explain": "Correct. A — An access port with access VLAN 20 for untagged data and voice VLAN 30 for the Cisco phone\u2019s tagged voice traffic is the standard pattern. Trunk or dynamic DTP modes are not the usual answer for this combined phone + PC access design.",
            "choices": [
                """switchport mode access
switchport access vlan 20
switchport voice vlan 30""",
                """switchport mode trunk
switchport access vlan 20
switchport voice vlan 30""",
                """switchport mode dynamic auto
switchport trunk native vlan 20
switchport trunk allowed vlan 30
switchport voice vlan 30""",
                """switchport mode dynamic desirable
switchport access vlan 20
switchport trunk allowed vlan 30
switchport voice vlan 30""",
            ],
        },
        {
            "slug": "https-uses-ssl-tls",
            "title": "CCNA — HTTPS and SSL/TLS",
            "stem": "Which protocol uses the SSL?",
            "name": "httpsssl1",
            "correct": "B",
            "explain": "Correct. B — HTTPS carries HTTP over TLS (often still described as SSL). Plain HTTP and Telnet are cleartext. SSH uses its own encrypted transport, not SSL/TLS in the HTTPS sense.",
            "choices": ["HTTP", "HTTPS", "SSH", "Telnet"],
        },
        {
            "slug": "ssid-wireless-lan-identifier",
            "title": "CCNA — SSID purpose",
            "stem": "Which value is the unique identifier that an access point uses to establish and maintain wireless connectivity to wireless network devices?",
            "name": "ssid1",
            "correct": "B",
            "explain": "Correct. B — The SSID names the wireless LAN (ESS) clients join; APs advertise it and stations associate using it. VLAN IDs are for wired switching. RFID is unrelated. WLAN ID is a controller-local profile index, not the over-the-air name clients use like the SSID.",
            "choices": ["VLANID", "SSID", "RFID", "WLANID"],
        },
        {
            "slug": "ssh-ip-domain-name-before-rsa-key",
            "title": "CCNA — SSH RSA key prerequisites",
            "stem": "A network engineer is configuring a switch so that it is remotely reachable via SSH. The engineer has already configured the host name on the router. Which additional command must the engineer configure before entering the command to generate the RSA key?",
            "name": "sshdom1",
            "correct": "C",
            "explain": "Correct. C — IOS builds the SSH key label from hostname and ip domain-name; set ip domain-name before crypto key generate rsa. The modulus line is the key generation itself. ip ssh authentication-retries is optional tuning.",
            "choices": [
                "password password",
                "crypto key generate rsa modulus 1024",
                "ip domain-name domain",
                "ip ssh authentication-retries 2",
            ],
        },
        {
            "slug": "r1-ssh-secure-remote-access-choose-two",
            "title": "CCNA — R1 SSH secure remote access (choose two)",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "Which two commands must be configured on router R1 to enable the router to accept secure remote-access connections? (Choose two)",
            "name": "r1sshsec2",
            "choose_two": True,
            "correct": ["B", "E"],
            "explain": "Correct. B and E \u2014 SSH is the secure remote shell; the device needs an RSA host key pair (crypto key generate rsa) so the SSH server can run, and a local username (username ... password|secret ...) is commonly required when virtual lines use login local for authenticated SSH sessions. transport input telnet (A) enables cleartext Telnet, not secure remote access. login console (C) is not the standard VTY pattern for SSH acceptance. ip ssh pubkey-chain (D) can support public-key user authentication but is not one of the two baseline requirements compared with generating keys and defining a user for typical password-based SSH access in CCNA-style scenarios.",
            "post_stem_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/r1-ssh-secure-remote-access-choose-two-topology.png" alt="Topology: router R1 with GigabitEthernet0/1 toward LAN 10.0.1.0/24 (PC1 and PC2) and Serial0/1 toward the Internet." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "choices": [
                "transport input telnet",
                "username cisco password 0 cisco",
                "login console",
                "ip ssh pubkey-chain",
                "crypto key generate rsa",
            ],
        },
        {
            "slug": "qos-traffic-shaping-buffer-excess",
            "title": "CCNA — Traffic shaping",
            "stem": "Which QoS traffic handling technique retains excess packets in a queue and reschedules these packets for later transmission when the configured maximum bandwidth has been surpassed?",
            "name": "qshape1",
            "correct": "A",
            "explain": "Correct. A — Shaping buffers traffic that exceeds the target rate and sends it when capacity allows. Policing typically drops or remarks excess traffic rather than deferring it with a shaping queue. WRED drops early for congestion avoidance. Prioritization orders queues but is not defined by this deferral behavior.",
            "choices": [
                "traffic shaping",
                "traffic policing",
                "weighted random early detection",
                "traffic prioritization",
            ],
        },
        {
            "slug": "vlan-tagging-trunk-separation",
            "title": "CCNA — VLAN tagging on trunks",
            "stem": "Which Layer 2 switch function encapsulates packets for different VLANs so that the packets traverse the same port and maintain traffic separation between the VLANs?",
            "name": "vlantag1",
            "correct": "C",
            "explain": "Correct. C — 802.1Q VLAN tagging adds a VLAN ID so multiple VLANs share a trunk while staying separated. VLAN numbering assigns IDs; DSCP is Layer 3 QoS; \u201cVLAN marking\u201d is not the standard term for 802.1Q encapsulation.",
            "choices": [
                "VLAN numbering",
                "VLAN DSCP",
                "VLAN tagging",
                "VLAN marking",
            ],
        },
        {
            "slug": "utp-vs-stp-shielding-emi",
            "title": "CCNA — UTP vs STP cabling",
            "stem": "How do UTP and STP cables compare?",
            "name": "utpstp1",
            "correct": "D",
            "explain": "Correct. D — STP adds shielding that helps reject EMI/RFI; UTP has no comparable shield and relies on twisting and balance. UTP is usually cheaper and easier to install than STP. STP is not inherently slower, and UTP is not automatically less interference-prone than STP in noisy environments.",
            "choices": [
                "STP cables are cheaper to produce and easier to install and UTP cables are more expensive and harder to install.",
                "UTP cables are less prone to crosstalk and interference and STP cables are more prone to crosstalk and interference.",
                "UTP cables provide faster and more reliable data transfer rates and STP cables are slower and less reliable.",
                "STP cables are shielded and protect against electromagnetic interference and UTP lacks the same protection against electromagnetic interference.",
            ],
        },
        {
            "slug": "flexconnect-local-switching-trunk-ap",
            "title": "CCNA — FlexConnect trunk to switch",
            "stem": "Which port type does a lightweight AP use to connect to the wired network when configured in FlexConnect mode with local switching and VLAN tagging?",
            "name": "flextr1",
            "correct": "D",
            "explain": "Correct. D — Local switching with multiple VLANs requires 802.1Q tagging on the AP uplink, so the switch port is a trunk. A single access VLAN is for centralized tunneling or a single VLAN. EtherChannel/LAG aggregate links but do not replace trunk behavior for multiple VLANs.",
            "choices": ["EtherChannel", "access", "LAG", "trunk"],
        },
        {
            "slug": "wlan-passive-client-static-ip",
            "title": "CCNA — Passive client for static IP",
            "stem": "An engineer is installing a new wireless printer with a static IP address on the Wi-Fi network. Which feature must be enabled and configured to prevent connection issues with the printer?",
            "name": "pasvcl1",
            "correct": "A",
            "explain": "Correct. A — On a Cisco WLC, Passive Client support helps static-IP wireless clients that do not use DHCP so the controller can handle them correctly. DHCP assignment conflicts with a static printer. Client exclusion blocks clients. Static IP tunneling is not the standard answer here.",
            "choices": [
                "passive client",
                "static IP tunneling",
                "DHCP address assignment",
                "client exclusion",
            ],
        },
        {
            "slug": "ipv6-static-route-global-config-nexthop",
            "title": "CCNA — IPv6 static route command mode",
            "stem": "An engineer is configuring router R1 with an IPv6 static route for prefix 2019:C15C:0CAF:E001::/64. The next hop must be 2019:C15C:0CAF:E002::1. The route must be reachable via the R1 Gigabit 0/0 interface. Which command configures the designated route?",
            "name": "v6rtca1",
            "correct": "A",
            "mono": True,
            "explain": "Correct. A — IPv6 static routes are configured in global configuration with ipv6 route. ip route is for IPv4. Static routes are not configured from interface configuration mode in this pattern. If an outbound interface were required explicitly, the usual form adds GigabitEthernet0/0 before the next hop; that variant is not among the valid choices here.",
            "choices": [
                "R1(config)#ipv6 route 2019:C15C:0CAF:E001::/64 2019:C15C:0CAF:E002::1",
                "R1(config-if)#ipv6 route 2019:C15C:0CAF:E001::/64 2019:C15C:0CAF:E002::1",
                "R1(config-if)#ip route 2019:C15C:0CAF:E001::/64 GigabitEthernet0/0",
                "R1(config)#ip route 2019:C15C:0CAF:E001::/64 GigabitEthernet0/0",
            ],
        },
        {
            "slug": "qos-policing-exceed-drop-mark",
            "title": "CCNA — Policing vs shaping",
            "stem": "Which QoS queuing method discards or marks packets that exceed the desired bit rate of traffic flow?",
            "name": "qpol1",
            "correct": "B",
            "explain": "Correct. B — Policing enforces a rate with actions such as drop or mark-down on exceed/violate. Shaping buffers and delays excess traffic. CBWFQ and LLQ are scheduling mechanisms, not defined primarily by discard/mark-on-exceed in this wording.",
            "choices": ["shaping", "policing", "CBWFQ", "LLQ"],
        },
        {
            "slug": "sdn-disaggregation-control-data-plane",
            "title": "CCNA — Disaggregation in controller networks",
            "stem": "What is the role of disaggregation in controller-based networking?",
            "name": "sdndis1",
            "correct": "A",
            "explain": "Correct. A — Disaggregation separates the control plane (centralized logic, often a controller) from the data plane (forwarding on devices). Route summarization between core and distribution, arbitrary ring-to-star rewiring, and assigning L2 vs L3 per device do not define this term.",
            "choices": [
                "It divides the control-plane and data-plane functions.",
                "It summarizes the routes between the core and distribution layers of the network topology.",
                "It enables a network topology to quickly adjust from a ring network to a star network",
                "It streamlines traffic handling by assigning individual devices to perform either Layer 2 or Layer 3 functions.",
            ],
        },
        {
            "slug": "dna-center-intent-api-rest-put",
            "title": "CCNA — DNA Center Intent API",
            "stem": "Which REST method updates an object in the Cisco DNA Center Intent API?",
            "name": "dnaput1",
            "correct": "D",
            "explain": "Correct. D — REST commonly uses PUT to replace/update a resource at a known URI. POST is often create or action-oriented. CHANGE and UPDATE are not standard HTTP methods.",
            "choices": ["CHANGE", "UPDATE", "POST", "PUT"],
        },
        {
            "slug": "amp-ngips-file-malware-analysis",
            "title": "CCNA — AMP with NGIPS",
            "stem": "What is the function of Cisco Advanced Malware protection for next-generation IPS?",
            "name": "ampips1",
            "correct": "D",
            "explain": "Correct. D — AMP focuses on file-centric inspection, reputation, and analysis for malware. URL filtering, user authentication, and authorizing compromised wireless traffic describe other features.",
            "choices": [
                "authorizing potentially compromised wireless traffic",
                "URL filtering",
                "authenticating end users",
                "inspecting specific files and files types for malware",
            ],
        },
        {
            "slug": "password-complexity-enable-prerequisite",
            "title": "CCNA — Password complexity prerequisite",
            "stem": "An administrator must use the password complexity not manufacturer-name command to prevent users from adding \u201ccisco\u201d as a password. Which command must be issued before this command?",
            "name": "pwdcpx1",
            "correct": "A",
            "explain": "Correct. A — Enable password complexity checking first with password complexity enable, then options such as not manufacturer-name apply. confreg is ROMMON recovery. login authentication sets an AAA method list. service password-encryption only obfuscates secrets in the configuration file.",
            "choices": [
                "Password complexity enable",
                "confreg 0x2142",
                "login authentication my-auth-list",
                "service password-encryption",
            ],
        },
        {
            "slug": "r1-username-engineer2-scrypt-local-database",
            "title": "CCNA — R1 local user strongest password",
            "stem": "An engineer must configure R1 for a new user account. The account must meet these requirements:",
            "stem_after_exhibit": "Which command must the engineer configure on the router?",
            "post_stem_html": """    <ul class="stem-after-exhibit-list">
      <li>It must be configured in the local database.</li>
      <li>The username is engineer2</li>
      <li>It must use the strongest password configurable.</li>
    </ul>""",
            "name": "r1usereng2",
            "correct": "A",
            "mono": True,
            "explain": "Correct. A \u2014 For a local username, `secret` stores a hashed password instead of reversible Type 7 encoding. Adding `algorithm-type scrypt` selects scrypt-based hashing, which is among the strongest password-hashing options Cisco offers for locally defined users on current IOS/IOS-XE compared with legacy Type 5 (MD5-based) or Type 7 passwords. Option B uses Type 5. Option C uses `password 7`, which is weak reversible obfuscation. Option D references Type 4 / an invalid or non-recommended pattern versus explicit scrypt configuration.",
            "choices": [
                """R1(config)# username engineer2 algorithm-type scrypt secret test2021""",
                """R1(config)# username engineer2 secret 5 password $1$bUu$kZbBS1Pyh4QzwXyZ""",
                """R1(config)# username engineer2 privilege 1 password 7 test2021""",
                """R1(config)# username engineer2 secret 4 $1Sb1Ju$kZbBSlFyh4QxwXyZ""",
            ],
        },
        {
            "slug": "commodity-switches-data-plane-forwarding",
            "title": "CCNA — Off-the-shelf switches in SDN",
            "stem": "What is the function of \u201coff-the-shelf\u201d switches in a controller-based network?",
            "name": "otsfp1",
            "correct": "A",
            "explain": "Correct. A — Commodity switches mainly provide high-speed data-plane forwarding programmed by the controller. Centralized views and policy are controller roles; autonomous distributed routing decisions are de-emphasized in the pure SDN story.",
            "choices": [
                "Forwarding packets",
                "Making routing decision",
                "Providing a central view of the deployed network",
                "Setting packet-handling policies",
            ],
        },
        {
            "slug": "security-posture-practices-choose-two",
            "title": "CCNA — Security posture (choose two)",
            "stem": "Which two practices are recommended for an acceptable security posture in a network? (Choose two)",
            "name": "secpst1",
            "choose_two": True,
            "correct": ["A", "E"],
            "explain": "Correct. A and E — Physically securing equipment and disabling unused ports, interfaces, and services reduce risk and attack surface. Internal email and file servers normally belong inside the trusted network, not a DMZ. Encrypted USB backups can be acceptable but are not the paired best-practice answer with these distractors.",
            "choices": [
                "Maintain network equipment in a secure location",
                "Backup device configurations to encrypted USB drives for secure retrieval",
                "Use a cryptographic keychain to authenticate to network devices",
                "Place internal email and file servers in a designated DMZ",
                "Disable unused or unnecessary ports, interfaces and services",
            ],
        },
        {
            "slug": "wan-topology-full-mesh-reliability",
            "title": "CCNA — WAN topology reliability",
            "stem": "Which WAN topology has the highest degree of reliability?",
            "name": "wanmesh1",
            "correct": "D",
            "explain": "Correct. D — Full mesh provides the most redundant paths between sites. Point-to-point is a single link; hub-and-spoke centralizes risk at the hub. Router-on-a-stick is a LAN inter-VLAN design, not a WAN topology class.",
            "choices": [
                "router-on-a-stick",
                "Point-to-point",
                "hub-and-spoke",
                "full mesh",
            ],
        },
        {
            "slug": "wpa-tkip-mic-encryption-feature",
            "title": "CCNA — WPA features",
            "stem": "What is a feature of WPA?",
            "name": "wpatk1",
            "correct": "C",
            "explain": "Correct. C — Original WPA introduced TKIP with MIC for stronger integrity than WEP. WPA can also use 802.1X or a PSK, but TKIP/MIC is the classic encryption upgrade the item targets. Small Wi-Fi application is not meaningful.",
            "choices": [
                "802.1x authentication",
                "preshared key",
                "TKIP/MIC encryption",
                "small Wi-Fi application",
            ],
        },
        {
            "slug": "tftp-operation-block-numbers-udp",
            "title": "CCNA — TFTP behavior",
            "stem": "How does TFTP operate in a network?",
            "name": "tftpblk1",
            "correct": "C",
            "explain": "Correct. C — TFTP uses UDP port 69 and transfers data in numbered blocks with acknowledgments. It does not use TCP port 20 (FTP data), does not use separate FTP-style control and data connections, and is not a secure protocol by itself.",
            "choices": [
                "relies on the well-known TCP port 20 to transmit data",
                "requires two separate connections for control and data traffic",
                "uses block numbers to identify and mitigate data-transfer errors",
                "provides secure data transfer",
            ],
        },
        {
            "slug": "ntp-master-fallback-upstream-failure",
            "title": "CCNA — NTP master when upstream fails",
            "stem": "An engineer is configuring switch SW1 to act as an NTP server when all upstream NTP server connectivity fails. Which configuration must be used?",
            "name": "ntpfallback1",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D — ntp master lets the device serve time from its local clock when it cannot synchronize to better sources; ntp server points to an upstream to use when reachable. ntp backup is not valid IOS syntax here; access-group and peer variants do not establish the local master behavior.",
            "choices": [
                """SW1# config t
SW1(config)#ntp server 192.168.1.1
SW1(config)#ntp access-group server accesslist1""",
                """SW1# config t
SW1(config)# ntp peer 192.168.1.1
SW1(config)#ntp access-group peer accesslist1""",
                """SW1# config t
SW1(config)#ntp backup
SW1(config)#ntp server 192.168.1.1""",
                """SW1# config t
SW1(config)#ntp master
SW1(config)#ntp server 192.168.1.1""",
            ],
        },
        {
            "slug": "authentication-vs-authorization-definition",
            "title": "CCNA — Authentication vs authorization",
            "stem": "How does authentication differ from authorization?",
            "name": "authzdef1",
            "correct": "A",
            "explain": "Correct. A — Authentication proves identity; authorization grants or denies access to resources after identity is known. The other options swap roles or confuse authorization with logging.",
            "choices": [
                "Authentication verifies the identity of a person accessing a network, and authorization determines what resource a user can access.",
                "Authentication is used to determine what resources a user is allowed to access, and authorization is used to track what equipment is allowed access to the network",
                "Authentication is used to verify a person\u2019s identity, and authorization is used to create syslog messages for logins",
                "Authentication is used to record what resource a user accesses, and authorization is used to determine what resources a user can access",
            ],
        },
        {
            "slug": "ospf-gigabitethernet-default-broadcast-network",
            "title": "CCNA — OSPF default network type on Ethernet",
            "stem": "A user configured OSPF and advertised the Gigabit Ethernet interface in OSPF. By default, to which type of OSPF network does this interface belong?",
            "name": "ospfbcast1",
            "correct": "D",
            "explain": "Correct. D — Cisco sets broadcast multi-access OSPF network type by default on Ethernet-family interfaces. Point-to-point is common on serial PPP-style links. NBMA and point-to-multipoint are special cases, not the GigabitEthernet default.",
            "choices": [
                "point-to-multipoint",
                "point-to-point",
                "nonbroadcast",
                "broadcast",
            ],
        },
        {
            "slug": "public-cloud-benefit-internet-access",
            "title": "CCNA — Public cloud for external users",
            "stem": "What is a benefit for external users who consume public cloud resources?",
            "name": "pubcld1",
            "correct": "D",
            "explain": "Correct. D — Public cloud services are typically reachable over the Internet, so external users can consume them without private WAN or colocation in the user\u2019s data center. Dedicated WAN-only, same-DC hosting, and \u201call physical\u201d are not the defining benefit.",
            "choices": [
                "implemented over a dedicated WAN",
                "located in the same data center as the users",
                "all hosted on physical servers",
                "accessed over the Internet",
            ],
        },
        {
            "slug": "sdn-controller-centralizes-routing-decision",
            "title": "CCNA — SDN control plane centralization",
            "stem": "In an SDN architecture, which function of a network node is centralized on a controller?",
            "name": "sdncrtl1",
            "correct": "D",
            "explain": "Correct. D — Routing and path decisions are control-plane work that SDN centralizes on the controller. Filtering execution, building the full IP RIB locally, and generic remote-access protocol services are not the primary answer.",
            "choices": [
                "provides protocol access for remote access devices",
                "discards a message due filtering",
                "creates the IP routing table",
                "makes a routing decision",
            ],
        },
        {
            "slug": "sdn-controller-function-making-routing-decisions",
            "title": "CCNA — SDN controller function",
            "stem": "What is the function of the controller in a software-defined network?",
            "name": "sdnctrlfn2",
            "correct": "B",
            "explain": "Correct. B \u2014 The SDN controller centralizes control-plane intelligence: it decides how traffic should be forwarded (routes, paths, flow rules) and programs the infrastructure. Packet forwarding, hardware multicast replication, and fragmentation/reassembly are data-plane or end-system tasks, not the controller\u2019s primary role.",
            "choices": [
                "forwarding packets",
                "making routing decisions",
                "multicast replication at the hardware level",
                "fragmenting and reassembling packets",
            ],
        },
        {
            "slug": "sdn-plane-forwards-user-traffic",
            "title": "CCNA — SDN data plane",
            "stem": "Which SDN plane forwards user-generated traffic?",
            "name": "sdndpusr1",
            "correct": "C",
            "explain": "Correct. C — User traffic is forwarded in the data (forwarding) plane. The control plane decides behavior; the management plane administers devices; a policy plane (if used) expresses policy rather than switching packets.",
            "choices": [
                "policy plane",
                "management plane",
                "data plane",
                "control plane",
            ],
        },
        {
            "slug": "collapsed-core-small-network-minimal-growth",
            "title": "CCNA — When to use collapsed core",
            "stem": "When should an engineer implement a collapsed-core architecture?",
            "name": "colcore2",
            "correct": "D",
            "explain": "Correct. D — Collapsed core suits smaller networks with limited scale-out needs. Large multi-site designs, mandating access and distribution on one box, or requiring VSS are not the general rule for choosing it.",
            "choices": [
                "for large networks that are connected to multiple remote sites",
                "the access and distribution layers must be on the same device",
                "only when using VSS technology",
                "for small networks with minimal need for growth",
            ],
        },
        {
            "slug": "wpa2-wpa3-ccmp-encryption-choose-two",
            "title": "CCNA — CCMP with WPA2 and WPA3 (choose two)",
            "stem": "Which two wireless security standards use Counter Mode Cipher Block Chaining Message Authentication Code Protocol for encryption and data integrity? (Choose two)",
            "name": "wpaccm2",
            "choose_two": True,
            "correct": ["A", "B"],
            "explain": "Correct. A and B — CCMP (AES-CCM) is the WPA2 air interface cipher; WPA3 retains CCMP for interoperability while also defining stronger ciphers such as GCMP. WEP uses RC4. Original WPA is primarily TKIP. Wi\u2011Fi 6 (802.11ax) is a PHY/MAC generation, not a security mode that defines CCMP.",
            "choices": ["WPA2", "WPA3", "WEP", "WPA", "Wi-Fi 6"],
        },
        {
            "slug": "mac-learning-switch-source-address",
            "title": "CCNA — MAC address learning",
            "stem": "What is a function of MAC learning on a switch?",
            "name": "mlearnfn1",
            "correct": "A",
            "explain": "Correct. A — Learning records each frame\u2019s source MAC and ingress port in the CAM table. Learning is on by default. Unknown unicast destinations are flooded within the VLAN, not dropped. The switch CAM does not build the IP ARP table.",
            "choices": [
                "It maps the source MAC address of an ingress frame to the receiving switch port in the MAC address table.",
                "MAC address learning is disabled by default on all VLANs.",
                "Frames to a destination MAC address not listed in the table are dropped.",
                "The MAC address table is used to populate the ARP table.",
            ],
        },
        {
            "slug": "gigabit-lx-lh-vs-zx-fiber-reach",
            "title": "CCNA — 1000BASE-LX/LH vs 1000BASE-ZX",
            "stem": "What is the difference between 1000BASE-LX/LH and 1000BASE-ZX interfaces?",
            "name": "sfpzx1",
            "correct": "D",
            "explain": "Correct. D — Typical datasheet classes are about 10 km for LX/LH on single-mode and on the order of 70 km for ZX on single-mode. ZX is long-haul SMF, not a multimode mode-conditioning story. 1000 km and dual-rate MM claims are not correct here.",
            "choices": [
                "1000BASE-LX/LH interoperates with multimode and single-mode fiber, and 1000BASE-ZX needs a conditioning patch cable with a multimode.",
                "1000BASE-ZX is supported on links up to 1000km, and 1000BASE-LX/LH operates over links up to 70 km.",
                "1000BASE-ZX interoperates with dual-rate 100M/1G 10Km SFP over multimode fiber, and 1000BASE-LX/LH supports only single-rate.",
                "1000BASE-LX/LH is supported on links up to 10km, and 1000BASE-ZX operates over links up to 70 km.",
            ],
        },
        {
            "slug": "ospf-router-id-without-loopback-or-router-id",
            "title": "CCNA — OSPF router ID selection",
            "stem": "What is the effect when loopback interfaces and the configured router ID are absent during the OSPF process configuration?",
            "name": "ospfrid1",
            "correct": "C",
            "explain": "Correct. C — Without an explicit router-id and without a loopback IPv4 address in the selection set, Cisco OSPF uses the highest IPv4 address on an up/up interface (typically a physical interface). 0.0.0.0 is not used as the RID, OSPF still runs, and the lowest address plus one is not the algorithm.",
            "choices": [
                "The router ID 0.0.0.0 is selected and placed in the OSPF process.",
                "No router ID is set, and the OSPF protocol does not run.",
                "The highest up/up physical interface IP address is selected as the router ID.",
                "The lowest IP address is incremented by 1 and selected as the router ID.",
            ],
        },
        {
            "slug": "router-subnet-10pct-host-growth-r789",
            "title": "CCNA — LAN subnets on R7–R9 with 10% growth",
            "stem": "An IP subnet must be configured on each router that provides enough addresses for the number of assigned hosts and anticipates no more than 10% growth for new hosts. Which configuration script must be used?",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/router-subnet-10pct-host-growth-r789-topology.png" alt="Topology: R7, R8, and R9 in a triangle. R7 Fa1/0 to a LAN cloud labeled 923 hosts; R8 Fa0/0 to a cloud labeled 225 hosts; R9 Fa1/1 to a cloud labeled 3641 hosts." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "post_stem_html": """    <ul class="stem-after-exhibit-list">
      <li><strong>R7</strong> FastEthernet1/0 LAN: <strong>923</strong> hosts (per exhibit).</li>
      <li><strong>R8</strong> FastEthernet0/0 LAN: <strong>225</strong> hosts (per exhibit).</li>
      <li><strong>R9</strong> FastEthernet1/1 LAN: <strong>3,641</strong> hosts (per exhibit).</li>
    </ul>
    <p class="stem-after-exhibit stem-after-exhibit-tail">Each interface gets its own IPv4 prefix. Usable host addresses must cover assigned hosts plus up to <strong>10% more</strong> (round up to whole hosts before choosing the subnet mask).</p>""",
            "name": "r789subn1",
            "correct": "C",
            "mono": True,
            "explain": "Correct. C — With 10% headroom, R7 needs at least ceil(923×1.1)=1,016 usable addresses (/22: 1,022). R8 needs at least ceil(225×1.1)=248 (/24: 254). R9 needs at least ceil(3,641×1.1)=4,006 (/20: 4,094). Option C uses /22, /24, and /20 and right-sizes each segment. Option A’s /20, /19, and /18 are valid but waste address space. Option B fails R9 (/21 allows 2,046 hosts). Option D’s /18, /19, and /17 are oversized versus the requirement.",
            "choices": [
                """Option A

R7#
configure terminal
interface Fa1/0
ip address 10.1.56.1 255.255.240.0
no shutdown

R8#
configure terminal
interface Fa0/0
ip address 10.9.32.1 255.255.224.0
no shutdown
R9#
configure terminal
interface Fa1/1
ip address 10.23.96.1 255.255.192.0
no shutdown""",
                """Option B

R7#
configure terminal
interface Fa1/0
ip address 10.1.56.1 255.255.248.0
no shutdown

R8#
configure terminal
interface Fa0/0
ip address 10.9.32.1 255.255.254.0
no shutdown

R9#
configure terminal
interface Fa1/1
ip address 10.23.96.1 255.255.248.0
no shutdown""",
                """Option C

R7#
configure terminal
interface Fa1/0
ip address 10.1.56.1 255.255.252.0
no shutdown

R8#
configure terminal
interface Fa0/0
ip address 10.9.32.1 255.255.255.0
no shutdown

R9#
configure terminal
interface Fa1/1
ip address 10.23.96.1 255.255.240.0
no shutdown""",
                """Option D

R7#
configure terminal
interface Fa1/0
ip address 10.1.56.1 255.255.192.0
no shutdown

R8#
configure terminal
interface Fa0/0
ip address 10.9.32.1 255.255.224.0
no shutdown

R9#
configure terminal
interface Fa1/1
ip address 10.23.96.1 255.255.128.0
no shutdown""",
            ],
        },
        {
            "slug": "show-ip-route-eigrp-learned-prefix",
            "title": "CCNA — Prefix learned via EIGRP",
            "stem": "Refer to the exhibit. Which network prefix was learned via EIGRP?",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="R1 show ip route CLI output">
        <pre>R1#show ip route | begin gateway
Gateway of last resort is 209.165.200.254 to network 0.0.0.0
S*    0.0.0.0/0 [1/0] via 209.165.200.254, Serial0/0/1
                is directly connected, Serial0/0/1
      172.16.0.0/16 is variably subnetted, 3 subnets, 2 masks
C        172.16.1.0/24 is directly connected, FastEthernet0/0
L        172.16.1.1/32 is directly connected, FastEthernet0/0
R        172.16.2.0/24 [120/2] via 207.165.200.250, 00:00:25, Serial0/0/0
O        192.168.1.0/24 [110/4437] via 207.165.200.254, 00:00:15, Serial0/0/1
D        192.168.2.0/24 [90/84437] via 207.165.200.254, 00:00:15, Serial0/0/1
      207.165.200.0/24 is variably subnetted, 5 subnets, 2 masks
S        207.165.200.244/30 [1/1] via 207.165.200.254, 00:00:25, Serial0/0/1
C        207.165.200.248/30 is directly connected, Serial0/0/0
L        207.165.200.249/32 is directly connected, Serial0/0/0
C        207.165.200.252/30 is directly connected, Serial0/0/1
L        207.165.200.253/32 is directly connected, Serial0/0/1</pre>
      </div>
    </div>""",
            "name": "eigrpprfx1",
            "correct": "C",
            "explain": "Correct. C — In the exhibit, internal EIGRP routes use code D (DUAL). The line D 192.168.2.0/24 [90/84437] is the EIGRP-learned prefix. O 192.168.1.0/24 is OSPF (AD 110). R 172.16.2.0/24 is RIP (AD 120). S and S* are static routes (including the default). Codes C and L mark connected and local routes.",
            "choices": [
                "172.16.0.0/16",
                "207.165.200.0/24",
                "192.168.2.0/24",
                "192.168.1.0/24",
            ],
        },
        {
            "slug": "lacp-etherchannel-sw1-sw2-mode-fix",
            "title": "CCNA — LACP EtherChannel SW1–SW2",
            "stem": "An engineer built a new L2 LACP EtherChannel between SW1 and SW2 and executed these show commands to verify the work. Which additional task allows the two switches to establish an LACP port channel?",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/lacp-etherchannel-sw1-sw2-topology.png" alt="Topology: SW1 and SW2 with two parallel links—SW1 Fa0/1 to SW2 Fa0/1 and SW1 Fa0/2 to SW2 Fa0/2." width="900" decoding="async" loading="lazy" />
      </figure>
      <div class="exhibit-router-cli" role="region" aria-label="SW1 and SW2 show run for port-channel member interfaces">
        <pre>SW1#show run interface fastEthernet0/1
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk allowed vlan 100,200,300
channel-group 1 mode on

SW1#show run interface fastEthernet0/2
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk allowed vlan 100,200,300
channel-group 1 mode on

SW2#show run interface fastEthernet 0/1
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk allowed vlan 100,200,300
channel-group 1 mode active

SW2#show run interface fastEthernet 0/2
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk allowed vlan 100,200,300
channel-group 1 mode active</pre>
      </div>
    </div>""",
            "name": "lacpsw12",
            "correct": "B",
            "explain": "Correct. B — mode on places interfaces in a static (non-negotiated) EtherChannel: no LACP or PAgP PDUs. SW2 uses LACP (mode active). An LACP port channel requires LACP on both ends—set SW1 to mode active or mode passive on those ports (with an active neighbor, passive can still form a bundle). Option A uses PAgP (desirable), not the right fix for LACP with SW2. Option C’s auto is PAgP. Option D is not the main issue; the mismatch is on versus LACP.",
            "choices": [
                "Change the channel-group mode on SW1 to desirable.",
                "Change the channel-group mode on SW1 to active or passive.",
                "Change the channel-group mode on SW2 to auto.",
                "Configure the interface port-channel 1 command on both switches.",
            ],
        },
        {
            "slug": "switch2-lldp-timer-holdtime",
            "title": "CCNA — LLDP timer and holdtime on Switch2",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="Switch2 show lldp output">
        <pre>Switch2#show lldp
Global LLDP Information
    Status : ACTIVE
    LLDP advertisements are sent every 30 seconds
    LLDP hold time advertised is 120 seconds
    LLDP interface reinitialization delay is 2 seconds</pre>
      </div>""",
            "stem": "A network engineer must update the configuration on Switch2 so that it sends LLDP packets every minute and the information sent via LLDP is refreshed every 3 minutes. Which configuration must the engineer apply?",
            "name": "lldpsw2tm",
            "correct": "B",
            "explain": "Correct. B — lldp timer sets the LLDP advertisement transmission interval in seconds (60 = one packet per minute). lldp holdtime sets how long receiving devices keep the advertised LLDP information before discarding it—also in seconds (180 = 3 minutes). tlv-select chooses which TLV types are sent, not timing. Options with lldp timer 1 send every second, not every minute.",
            "choices": [
                "Switch2(config)# lldp timer 60\nSwitch2(config)# lldp tlv-select 180",
                "Switch2(config)# lldp timer 60\nSwitch2(config)# lldp holdtime 180",
                "Switch2(config)# lldp timer 1\nSwitch2(config)# lldp tlv-select 3",
                "Switch2(config)# lldp timer 1\nSwitch2(config)# lldp holdtime 3",
            ],
            "mono": True,
        },
        {
            "slug": "ssh-vty-access-class-10-139-58-28",
            "title": "CCNA — SSH allowed sources via VTY access-class",
            "stem": "An engineer is configuring remote access to a router from IP subnet 10.139.58.0/28. The domain name, crypto keys, and SSH have been configured. Which configuration enables the traffic on the destination router?",
            "name": "sshvty10139",
            "correct": "B",
            "explain": "Correct. B — Restrict SSH logins with access-class on the VTY lines (not access-group, which applies ACLs to interfaces). SSH uses TCP port 22; for 10.139.58.0/28 the wildcard mask is 0.0.0.15. A is wrong because SSH is TCP (not UDP) and 0.0.0.7 does not match all addresses in a /28. C uses access-group on line vty, which is invalid. D mixes standard ACL syntax with TCP/port matching (needs extended ACL), uses an inappropriate ACL number for standard lists, and pins SSH filtering on an interface rather than the VTY.",
            "choices": [
                "interface FastEthernet0/0\nip address 10.122.49.1 255.255.255.252\nip access-group 10 in\n!\nip access-list standard 10\npermit udp 10.139.58.0 0.0.0.7 host 10.122.49.1 eq 22",
                "line vty 0 15\naccess-class 120 in\n!\nip access-list extended 120\npermit tcp 10.139.58.0 0.0.0.15 any eq 22",
                "line vty 0 15\naccess-group 120 in\n!\nip access-list extended 120\npermit tcp 10.139.58.0 0.0.0.15 any eq 22",
                "interface FastEthernet0/0\nip address 10.122.49.1 255.255.255.252\nip access-group 110 in\n!\nip access-list standard 110\npermit tcp 10.139.58.0 0.0.0.15 eq 22 host 10.122.49.1",
            ],
            "mono": True,
        },
        {
            "slug": "ssh-secure-remote-cli-protocol",
            "title": "CCNA — Secure remote CLI access protocol",
            "stem": "Which protocol is used for secure remote CLI access?",
            "name": "sshclisec",
            "correct": "C",
            "explain": "Correct. C — SSH (Secure Shell) encrypts the session and provides secure remote CLI access to routers and switches. Telnet sends traffic in clear text. HTTP/HTTPS are used for web-based management, not as the primary Cisco IOS remote CLI transport.",
            "choices": [
                "HTTP",
                "Telnet",
                "SSH",
                "HTTPS",
            ],
        },
        {
            "slug": "private-ipv4-characteristic-no-registry",
            "title": "CCNA — Private IPv4 addressing characteristic",
            "stem": "What is a characteristic of private IPv4 addressing?",
            "name": "privnosreg",
            "correct": "C",
            "explain": "Correct. C — RFC 1918 private addresses are intended for internal networks and are reused across organizations without global registration or unique allocation like public IPv4. They do not traverse the public Internet without NAT. Option B describes public addressing coordination, not private RFC 1918 space. Option D is false—ACLs do not make private hosts globally routable. Option A only describes the size of one common block (for example 192.168.0.0/16), not the defining characteristic of private IPv4 addressing overall.",
            "choices": [
                "composed of up to 65,536 available addresses",
                "issued by IANA in conjunction with an autonomous system number",
                "used without tracking or registration",
                "traverse the Internet when an outbound ACL is applied",
            ],
        },
        {
            "slug": "enterprise-network-wlc-auth-roaming",
            "title": "CCNA — WLC authentication and roaming",
            "stem": "What provides centralized control of authentication and roaming in an enterprise network?",
            "name": "wlcaurent",
            "correct": "D",
            "explain": "Correct. D — In a lightweight (split-MAC) WLAN, the wireless LAN controller centralizes policies, AAA-backed authentication, and roaming coordination; access points forward traffic and radio functions while control stays at the WLC. A LAN switch and firewall do not perform that WLAN control-plane role, and a lightweight AP is the managed edge device—not the central controller.",
            "choices": [
                "a LAN switch",
                "a firewall",
                "a lightweight access point",
                "a wireless LAN controller",
            ],
        },
        {
            "slug": "nat-pat-standard-acl1-gi01-exhibit",
            "title": "CCNA — PAT with standard ACL (exhibit)",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/nat-pat-standard-acl1-topology.png" alt="Topology: PC1 172.16.0.1 and PC2 172.16.0.2 on the LAN; NAT router GigabitEthernet0/0 toward LAN and GigabitEthernet0/1 toward Internet." width="900" decoding="async" loading="lazy" />
      </figure>
      <div class="exhibit-router-cli" role="region" aria-label="NAT overload and standard access list 1">
        <pre>interface GigabitEthernet0/0
 ip address 172.16.0.5 255.255.255.0
 duplex auto
 speed auto
!
interface GigabitEthernet0/1
 ip address 209.165.202.130 255.255.255.224
 duplex auto
 speed auto
!
ip nat inside source list 1 interface GigabitEthernet0/1 overload
!
access-list 1 permit 172.16.0.1
access-list 1 permit 172.16.0.2</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. Which IPv4 host addresses are permitted to use PAT overload translation through GigabitEthernet0/1?",
            "name": "natacl1gi01",
            "correct": "A",
            "explain": "Correct. A — The NAT statement ties PAT (overload) to traffic permitted by standard access list 1. Only sources explicitly permitted by ACL 1—172.16.0.1 and 172.16.0.2—match list 1 for translation; other hosts on 172.16.0.0/24 are not listed and do not match the ACL used by ip nat inside source list 1.",
            "choices": [
                "172.16.0.1 and 172.16.0.2 only",
                "every host on 172.16.0.0/24 except 172.16.0.5",
                "every host on 172.16.0.0/24",
                "only the GigabitEthernet0/0 interface address",
            ],
        },
        {
            "slug": "ipv6-vlan2000-unique-local-ula",
            "title": "CCNA — IPv6 ULA on SVI VLAN 2000",
            "stem": "A network engineer must implement an IPv6 configuration on the vlan 2000 interface to create a routable locally-unique unicast address that is blocked from being advertised to the internet. Which configuration must the engineer apply?",
            "name": "ipv6ula2k",
            "correct": "B",
            "explain": "Correct. B — Addresses from fd00::/8 are IPv6 Unique Local Addresses (ULA): site-scope unicast, globally ambiguous by design and filtered from global BGP toward the Internet—similar in intent to RFC 1918 for IPv4. Option A uses ff00::/8, which is multicast, not unicast. Option D uses fe80::/10 (link-local), which is not routed beyond the link. Option C begins with fc00::/8 (reserved half of ULA under RFC 4193); deployable unique locals use fd00::/8 with a generated global ID—fd00::… is the conventional assignment.",
            "choices": [
                "interface vlan 2000\nipv6 address ff00:0000:aaaa::1234:2343/64",
                "interface vlan 2000\nipv6 address fd00::1234:2343/64",
                "interface vlan 2000\nipv6 address fc00:0000:aaaa:a15d:1234:2343:8aca/64",
                "interface vlan 2000\nipv6 address fe80:0000:aaaa::1234:2343/64",
            ],
            "mono": True,
        },
        {
            "slug": "ospf-r1-r2-point-to-point-no-dr-bdr",
            "title": "CCNA — OSPF point-to-point without DR/BDR",
            "stem": "OSPF must be configured between routers R1 and R2. Which OSPF configuration must be applied to router R1 to avoid a DR/BDR election?",
            "name": "ospfr1r2pt",
            "correct": "D",
            "explain": "Correct. D — Setting ip ospf network point-to-point on the link uses a topology where OSPF does not perform DR/BDR election (point-to-point adjacency between two routers). The default broadcast network type on Ethernet still elects a DR/BDR. Changing cost or hello interval does not remove DR/BDR behavior on a broadcast segment.",
            "choices": [
                "router ospf 1\nnetwork 192.168.1.1 0.0.0.0 area 0\ninterface e1/1\nip address 192.160.1.1 255.255.255.252\nip ospf network broadcast",
                "router ospf 1\nnetwork 192.168.1.1 0.0.0.0 area 0\ninterface e1/1\nip address 192.168.1.1 255.255.255.252\nip ospf cost 0",
                "router ospf 1\nnetwork 192.168.1.1 0.0.0.0 area 0\nhello interval 15\ninterface e1/1\nip address 192.168.1.1 255.255.255.252",
                "router ospf 1\nnetwork 192.168.1.1 0.0.0.0 area 0\ninterface e1/1\nip address 192.168.1.1 255.255.255.252\nip ospf network point-to-point",
            ],
            "mono": True,
        },
        {
            "slug": "switchport-trunk-fa01-vlans-10-15-complete",
            "title": "CCNA — Voice and data VLANs on Fa0/1 (IP phone and PC)",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/switchport-fa01-phone-pc-voice-data-topology.png" alt="Topology: PC on data VLAN 15 connected to a Cisco IP phone using voice VLAN 10, phone uplink to switch SW on FastEthernet0/1." width="900" decoding="async" loading="lazy" />
      </figure>
      <div class="exhibit-router-cli" role="region" aria-label="SW show running-config for FastEthernet0/1">
        <pre>SW#show run
Building configuration...
!
interface FastEthernet0/1
 switchport access vlan 15
!
end</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibits. An administrator must configure FastEthernet0/1 so PC data traffic is in VLAN 15 and the Cisco IP phone uses VLAN 10 for voice. The VLANs exist in the VLAN database. Which command sequence completes the configuration?",
            "name": "trnkfa1015",
            "correct": "D",
            "explain": "Correct. D — With a PC connected through a Cisco IP phone on one access port, configure switchport mode access, switchport access vlan 15 for untagged PC data, and switchport voice vlan 10 for the IP phone voice VLAN (typically 802.1Q tagged toward the switch when CDP advertises the voice VLAN). Options A and B build an 802.1Q trunk, which does not match this phone-and-PC access design. Option C mixes invalid VLAN/private-vlan commands under the interface.",
            "choices": [
                "interface FastEthernet0/1\nswitchport trunk native vlan 10\nswitchport trunk allowed vlan 10,15",
                "interface FastEthernet0/1\nswitchport mode trunk\nswitchport trunk allowed vlan 10,15",
                "interface FastEthernet0/1\nswitchport trunk allowed vlan add 10\nvlan 10\nprivate-vlan isolated",
                "interface FastEthernet0/1\nswitchport mode access\nswitchport access vlan 15\nswitchport voice vlan 10",
            ],
            "mono": True,
        },
        {
            "slug": "route-best-path-10-10-10-24-exhibit",
            "title": "CCNA — Best path to 10.10.10.24 from routing table",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="Routing table excerpt for 10.10.10.0/24">
        <pre>EIGRP 10.10.10.0/24[90/1441] via F0/10
EIGRP 10.10.10.0/24[90/144] via F0/11
EIGRP 10.10.10.0/24[90/1441] via F0/12
OSPF 10.10.10.0/24[110/20] via F0/13
OSPF 10.10.10.0/24[110/30] via F0/14</pre>
      </div>""",
            "stem": "Refer to the exhibit. Packets received by the router from BGP enter via a serial interface at 209.165.201.10. Each route is present within the routing table. Which interface is used to forward traffic with a destination IP of 10.10.10.24?",
            "name": "routefwd101024",
            "correct": "B",
            "explain": "Correct. B — The destination 10.10.10.24 matches 10.10.10.0/24. Among competing routes, the lowest administrative distance wins: internal EIGRP (90) is preferred over OSPF (110), so OSPF paths F0/13 and F0/14 are not used. Among the EIGRP entries, the lowest reported metric (Feasible Distance) is 144, which points out FastEthernet0/11. The BGP ingress note does not change AD-based selection for this IPv4 prefix.",
            "choices": [
                "F0/10",
                "F0/11",
                "F0/12",
                "F0/13",
            ],
        },
        {
            "slug": "ip-address-dhcp-interface-client",
            "title": "CCNA — ip address dhcp on an interface",
            "stem": "What is the purpose of the ip address dhcp command?",
            "name": "ipaddrhcp1",
            "correct": "D",
            "explain": "Correct. D — On a routed interface, ip address dhcp makes the router obtain its IPv4 address, mask, and default gateway from a DHCP server (DHCP client behavior). A DHCP server uses a DHCP pool and service configuration, not this command. Relay/helper uses ip helper-address (or IPv6 dhcp relay) on the client-facing router interface, not ip address dhcp.",
            "choices": [
                "to configure an interface as a DHCP server",
                "to configure an interface as a DHCP relay",
                "to configure an interface as a DHCP helper",
                "to configure an interface as a DHCP client",
            ],
        },
        {
            "slug": "endpoint-network-function-client-server",
            "title": "CCNA — Function of a network endpoint",
            "stem": "What is a function of an endpoint on a network?",
            "name": "endptfn1",
            "correct": "B",
            "explain": "Correct. B — Endpoints are the hosts at the edge of the network—client and server devices that attach to the infrastructure to originate or consume traffic. Wireless service delivery (C) is typically an AP/controller role. Inter-VLAN forwarding (D) is a Layer 3 device function. Option A describes one possible application, not the general role of an endpoint.",
            "choices": [
                "allows users to record data and transmit to a file server",
                "connects server and client devices to a network",
                "provides wireless services to users in a building",
                "forwards traffic between VLANs on a network",
            ],
        },
        {
            "slug": "ipv6-internal-device-unique-local-address",
            "title": "CCNA — IPv6 internal-only reachability",
            "stem": "A network engineer is installing an IPv6-only capable device. The client has requested that the device IP address be reachable only from the internal network. Which type of IPv6 address must the engineer assign?",
            "name": "ipv6intula1",
            "correct": "A",
            "explain": "Correct. A — Unique Local Addresses (ULA, fd00::/8 in common deployments) are IPv6 unicast addresses meant for private internal routing: they are globally ambiguous and filtered from the public Internet, similar in intent to RFC 1918 for IPv4. Link-local addresses are only link-scoped and are not used as the stable enterprise-routable address for reachability across internal subnets. Global unicast (aggregatable global) addresses are Internet-routable. IPv4-compatible IPv6 addresses (::/96 form) are obsolete and not appropriate here.",
            "choices": [
                "unique local address",
                "link-local address",
                "IPv4-compatible IPv6 address",
                "aggregatable global address",
            ],
        },
        {
            "slug": "etherchannel-port-channel10-lacp-modes-choose-two",
            "title": "CCNA — Port channel 10 LACP modes (choose two)",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="Switch show etherchannel summary">
        <pre>Switch#show etherchannel summary

[output omitted]

Group   Port-channel  Protocol   Ports
------+--------------+---------+---------------------
10      Po10(SU)       LACP      Gi0/0(P)  Gi0/1(P)
20      Po20(SU)       LACP      Gi0/2(P)  Gi0/3(P)</pre>
      </div>""",
            "stem": "Refer to the exhibit. Which two commands when used together create port channel 10? (Choose two)",
            "name": "po10lacp2",
            "choose_two": True,
            "mono": True,
            "correct": ["A", "C"],
            "explain": "Correct. A and C — The summary shows port channel 10 using the LACP protocol with Gi0/0 and Gi0/1 in the bundle. mode active and mode passive are LACP (IEEE 802.3ad) negotiation keywords used with channel-group 10. mode desirable and mode auto are Cisco PAgP modes and would not match the LACP protocol column. mode on builds a static EtherChannel without LACP PDUs.",
            "choices": [
                "int range g0/0-1\nchannel-group 10 mode active",
                "int range g0/0-1\nchannel-group 10 mode desirable",
                "int range g0/0-1\nchannel-group 10 mode passive",
                "int range g0/0-1\nchannel-group 10 mode auto",
                "int range g0/0-1\nchannel-group 10 mode on",
            ],
        },
        {
            "slug": "ospf-dr-r1-priority-r3-zero-choose-two",
            "title": "CCNA — Make R1 the OSPF DR (choose two)",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/ospf-area0-r1-r2-r3-sw-star-topology.png" alt="Topology: switch SW in the center; OSPF Area 0. R1 10.10.10.1 on FastEthernet0/0 to SW Fa0/0; R2 10.10.10.2 on FastEthernet0/2 to SW Fa0/2; R3 10.10.10.3 on FastEthernet0/1 to SW Fa0/1." width="900" decoding="async" loading="lazy" />
      </figure>
      <div class="exhibit-router-cli" role="region" aria-label="R1 show ip ospf neighbor">
        <pre>R1#show ip ospf neighbor

Neighbor ID     Pri   State      Dead Time   Address         Interface
10.10.10.2        1   FULL/BDR   00:00:35    10.10.10.2      FastEthernet0/0
10.10.10.3        1   FULL/DR    00:00:34    10.10.10.3      FastEthernet0/0</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. Which two configurations must the engineer apply on this network so that R1 becomes the DR? (Choose two)",
            "name": "ospfdr1r3",
            "choose_two": True,
            "mono": True,
            "correct": ["A", "C"],
            "explain": "Correct. A and C — The exhibit shows R3 as DR and R2 as BDR on the shared multi-access segment; R1 sees both neighbors on **FastEthernet0/0** with OSPF priority 1. Raising R1\u2019s priority on **FastEthernet0/0** (200) makes R1 win the election, and setting **R3\u2019s** segment-facing interface (**FastEthernet0/1** toward SW) to priority **0** removes R3 from DR/BDR contention. Router ID (B) only breaks ties when priorities match. R1 priority 0 (D) disqualifies R1. Raising R3\u2019s priority to 200 on its segment interface (E) keeps the current DR stronger.",
            "choices": [
                "R1(config)#interface FastEthernet0/0\nR1(config-if)#ip ospf priority 200",
                "R1(config)#router ospf 1\nR1(config-router)#router-id 10.10.10.1",
                "R3(config)#interface FastEthernet0/1\nR3(config-if)#ip ospf priority 0",
                "R1(config)#interface FastEthernet0/0\nR1(config-if)#ip ospf priority 0",
                "R3(config)#interface FastEthernet0/1\nR3(config-if)#ip ospf priority 200",
            ],
        },
        {
            "slug": "r1-ntp-server-requirements-config",
            "title": "CCNA — R1 NTP server with auth, source, stratum, ACL",
            "stem": "R1 as an NTP server must have:\n• NTP authentication enabled\n• NTP packets sourced from interface Loopback 0\n• NTP stratum 2\n• NTP packets only permitted to client IP 209.165.200.225\n\nHow should R1 be configured?",
            "name": "ntp1r1srv",
            "correct": "D",
            "explain": "Correct. D — ntp authenticate and ntp authentication-key enable keyed NTP; ntp source Loopback0 sets the source address for NTP packets; ntp master 2 advertises stratum 2 from the local clock (there is no ntp stratum EXEC-style command in this form). ntp access-group 10 serve-only applies IPv4 ACL 10 so only permitted sources receive NTP server replies; access-list 10 permit host 209.165.200.225 matches the allowed client. Option A misuses a numbered standard ACL with UDP/port syntax (that requires an extended ACL). Option B uses ntp stratum 2, which is not valid IOS configuration. Option C uses ntp interface Loopback0 instead of ntp source, repeats the invalid ntp stratum line, and uses an incomplete ACL line. Note: IOS uses the keyword serve-only (not server-only) in ntp access-group.",
            "choices": [
                "ntp authenticate\nntp authentication-key 2 sha1 CISCO123\nntp source Loopback0\nntp access-group server-only 10\nntp master 2\n!\naccess-list 10 permit udp host 209.165.200.225 any eq 123",
                "ntp authenticate\nntp authentication-key 2 md5 CISCO123\nntp source Loopback0\nntp access-group server-only 10\nntp stratum 2\n!\naccess-list 10 permit udp host 209.165.200.225 any eq 123",
                "ntp authenticate\nntp authentication-key 2 md5 CISCO123\nntp interface Loopback0\nntp access-group server-only 10\nntp stratum 2\n!\naccess-list 10 permit 209.165.200.225",
                "ntp authenticate\nntp authentication-key 2 md5 CISCO123\nntp source Loopback0\nntp access-group 10 serve-only\nntp master 2\n!\naccess-list 10 permit host 209.165.200.225",
            ],
            "mono": True,
        },
        {
            "slug": "r1-floating-static-ospf-backup-server",
            "title": "CCNA — R1: OSPF primary, static backup to server network",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/r1-floating-static-ospf-backup-server-topology.png" alt="Topology: PC1 on 192.168.1.0/24 to R1 Gi0/1; R1 Gi0/0 to R2 Gi0/1 on 172.16.2.0/24 (OSPF); R2 Gi0/0 on 10.1.1.0/24 to server 10.1.1.10." width="900" decoding="async" loading="lazy" />
      </figure>
      <div class="cli-device" role="region" aria-label="R1 show ip route during outage">
        <h2>During outage</h2>
        <pre>R1#show ip route 10.1.1.10
% Network not in table</pre>
      </div>
      <div class="cli-device" role="region" aria-label="R1 show ip route normal operation">
        <h2>Normal operation</h2>
        <pre>R1#show ip route 10.1.1.10
Routing entry for 10.1.1.0/24
  Known via "ospf 1", distance 110, metric 2, type intra area
  Last update from 172.16.2.2 on GigabitEthernet0/0, 00:00:18 ago
  Routing Descriptor Blocks:
  * 172.16.2.2, from 10.1.1.10, 00:00:18 ago, via GigabitEthernet0/0
      Route metric is 2, traffic share count is 1</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. Which route must be configured on R1 so that OSPF routing is used when OSPF is up, but the server is still reachable when OSPF goes down?",
            "name": "r1ospflt1",
            "correct": "B",
            "explain": "Correct. B — The detail output shows OSPF (process 1) for 10.1.1.0/24 with administrative distance 110 via GigabitEthernet0/0. A floating static backup must use a higher AD so the OSPF route stays preferred while it is in the routing table; AD 125 satisfies that. The static should match the same /24 prefix OSPF advertises so OSPF is not bypassed by a more-specific host route. When OSPF withdraws the route (as in the outage output), the static remains and restores reachability. Options A and C use AD 100, which is lower than 110, so the static would beat OSPF even when OSPF is up. Option D points to host 10.1.1.10/32; a /32 is longer than the OSPF /24, so traffic to the server would follow the static even while OSPF is up.",
            "choices": [
                "ip route 10.1.1.10 255.255.255.255 172.16.2.2 100",
                "ip route 10.1.1.0 255.255.255.0 gi0/1 125",
                "ip route 10.1.1.0 255.255.255.0 172.16.2.2 100",
                "ip route 10.1.1.10 255.255.255.255 gi0/0 125",
            ],
            "mono": True,
        },
        {
            "slug": "ospf-r1-r2-p2p-link-network-command",
            "title": "CCNA — OSPF on R1–R2 point-to-point link",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/ospf-r1-r2-p2p-link-network-command-topology.png" alt="Topology: R1 Serial0/1 to R2 Serial0/1 on 10.0.0.0/30; R1 Gi0/1 on 10.0.1.0/24; R2 Gi0/1 on 10.0.2.0/24." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. Which command configures OSPF on the point-to-point link between routers R1 and R2?",
            "name": "ospfp2pnet1",
            "correct": "A",
            "explain": "Correct. A — The exhibit shows R1 and R2 connected on 10.0.0.0/30 over Serial0/1 (10.0.0.1 and 10.0.0.2). In router OSPF configuration mode, network <address> <wildcard-mask> area <id> enables OSPF on interfaces whose primary IPv4 addresses match that statement. network 10.0.0.0 0.0.0.255 area 0 matches addresses 10.0.0.0–10.0.0.255, which includes the /30 on the serial link, so OSPF runs on that interconnect. Option B is not valid syntax for enabling OSPF on a typical point-to-point link (neighbor is used in specific NBMA contexts; the value shown is a prefix, not a neighbor router ID or IP). Option C sets interface DR priority on broadcast/multi-access segments and does not enable OSPF or assign an area. Option D sets the OSPF router ID only; it does not place any interface into OSPF.",
            "choices": [
                "network 10.0.0.0 0.0.0.255 area 0",
                "neighbor 10.1.2.0 cost 180",
                "ip ospf priority 100",
                "router-id 10.0.0.15",
            ],
            "mono": True,
        },
        {
            "slug": "ten-gigabitethernet0-0-0-slow-transfer-show-interface",
            "title": "CCNA — TenGigabitEthernet0/0/0 slow transfer (show interface)",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="show interfaces TenGigabitEthernet0/0/0">
        <pre>Router#show interfaces TenGigabitEthernet0/0/0
TenGigabitEthernet0/0/0 is up, line protocol is up
Hardware is BUILT-IN-2T+6X1GE, address is 74a0.2f7a.0123 (bia 74a0.2f7a.0123)
Description: Uplink
Internet address is 10.1.1.1/24
MTU 1500 bytes, BW 10000000 Kbit/sec, DLY 10 usec,
reliability 255/255, txload 1/255, rxload 1/255
Encapsulation ARPA, loopback not set
Keepalive not supported
Full Duplex, 10000Mbps, link type is force-up, media type is unknown media type
output flow control is on, input flow-control is on
ARP type: ARPA, ARP Timeout 04:00:00
Last input 00:00:00, output 00:05:40, output hang never
Last clearing of "show interface" counters never
Input queue: 0/375/0/0 (size/max/drops/flushes); Total output drops: 0
Queueing strategy: fifo
Output queue: 0/40 (size/max)
5 minute input rate 6160000 bits/sec, 1113 packets/sec
5 minute output rate 11213000 bits/sec, 1553 packets/sec
12662416065 packets input, 12607032232894 bytes, 0 no buffer
Received 14117163 broadcasts (0 IP multicasts)
0 runts, 0 giants, 0 throttles
0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
0 watchdog, 26271385 multicast, 0 pause input
7907770090 packets output, 5072790424092 bytes, 0 underruns
0 output errors, 8662414049 collisions, 1 interface resets
0 unknown protocol drops
0 babbles, 0 late collision, 0 deferred
0 lost carrier, 0 no carrier, 0 pause output
0 output buffer failures, 0 output buffers swapped out
1 carrier transitions</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. Traffic that is flowing over interface TenGigabitEthernet0/0/0 experiences slow transfer speeds. What is the reason for the issue?",
            "name": "tengig0slow1",
            "correct": "D",
            "explain": "Correct. D — The interface reports Full Duplex at 10000 Mbps with very low txload/rxload (1/255), so heavy congestion (A) is not indicated. Input and output queue drops are zero, so queuing drops (B) are not the cause. Bandwidth matches 10 Gb/s, so there is no speed mismatch on this side (C). A huge collision counter on a link operating as full duplex is a classic sign of a duplex mismatch: the far end is likely half duplex while this side is full duplex, so frames collide and throughput collapses even though the line stays up.",
            "choices": [
                "heavy traffic congestion",
                "queuing drops",
                "a speed conflict",
                "a duplex incompatibility",
            ],
        },
        {
            "slug": "ospf-serial-neighbor-stuck-exchange-mtu",
            "title": "CCNA — OSPF neighbor stuck in EXCHANGE (MTU)",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="Router A show ip ospf neighbor">
        <pre>A#show ip ospf neighbor
Neighbor ID     Pri   State       Dead Time   Address       Interface
172.1.1.1         1   EXCHANGE/-  00:00:36    172.16.32.1   Serial0.1</pre>
      </div>""",
            "stem": "An engineer assumes a configuration task from a peer. Router A must establish an OSPF neighbor relationship with neighbor 172.1.1.1. The output displays the status of the adjacency after 2 hours. What is the next step in the configuration process for the routers to establish an adjacency?",
            "name": "ospfexmtu1",
            "correct": "D",
            "explain": "Correct. D — During the database exchange, OSPF can compare the interface IP MTU carried in Database Description packets (unless disabled). When the MTUs on the two ends of the link differ, the adjacency often stays in EXSTART or EXCHANGE instead of reaching FULL. Align the MTU on router A with router B (or use ip ospf mtu-ignore on the interface) so the exchange can complete. OSPF router IDs must be unique but do not need to match an interface IP (A) or any particular \u201cnon-host\u201d pattern (B). A serial subinterface is already a common point-to-point style link; simply \u201cconfiguring point-to-point\u201d without fixing MTU does not address the usual cause of a long-lived EXCHANGE state in this scenario (C).",
            "choices": [
                "Set the router B OSPF ID to the same value as its IP address",
                "Set the router B OSPF ID to a nonhost address",
                "Configure a point-to-point link between router A and router B",
                "Configure router A to use the same MTU size as router B",
            ],
        },
        {
            "slug": "routing-cpe-longest-match-192-168-1-250",
            "title": "CCNA — Longest match for 192.168.1.250",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="CPE show ip route">
        <pre>CPE#show ip route
     192.168.1.0/24 is variably subnetted, 3 subnets, 3 masks
B    192.168.1.0/24 [20/1] via 192.168.12.2, 00:00:06
R    192.168.1.128/25 [120/5] via 192.168.13.3, 00:02:22, Ethernet0/1
O    192.168.1.192/26 [110/11] via 192.168.14.4, 00:02:22, Ethernet0/2
D    192.168.1.224/27 [90/1024640] via 192.168.15.5, 00:01:33, Ethernet0/3</pre>
      </div>""",
            "stem": "All traffic enters the CPE router from interface Serial0/3 with an IP address of 192.168.50.1. Web traffic from the WAN is destined for a LAN network where servers are load-balanced. An IP packet with a destination address of the HTTP virtual IP of 192.168.1.250 must be forwarded. Which routing table entry does the router use?",
            "name": "cperlmp250",
            "correct": "D",
            "explain": "Correct. D — The router chooses the route with the longest prefix length that contains the destination. 192.168.1.250 matches 192.168.1.0/24, 192.168.1.128/25, 192.168.1.192/26, and 192.168.1.224/27, but /27 is the most specific, so the EIGRP-learned 192.168.1.224/27 entry wins. Administrative distance and metric are used to break ties among routes of the same prefix length, not to prefer a shorter prefix over a longer one.",
            "choices": [
                "192.168.1.0/24 via 192.168.12.2",
                "192.168.1.128/25 via 192.168.13.3",
                "192.168.1.192/26 via 192.168.14.4",
                "192.168.1.224/27 via 192.168.15.5",
            ],
        },
        {
            "slug": "switch-pc1-access-duplex-mismatch-performance",
            "title": "CCNA — PC1 access port poor performance (duplex)",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/switch-pc1-access-duplex-mismatch-performance-topology.png" alt="Topology: PC1 FastEthernet0 with manual 100 Mbps full duplex connected to switch Fa0/1." width="900" decoding="async" loading="lazy" />
      </figure>
      <div class="exhibit-router-cli" role="region" aria-label="Switch show interface status">
        <pre>Switch#show interface status
Port      Name  Status      Vlan  Duplex  Speed  Type
Fa0/1           connected   1     auto    auto   10/100BaseTX</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. Traffic is performing poorly even though the port shows connected. Which interface condition is causing the performance problem?",
            "name": "swpc1dpx1",
            "correct": "A",
            "explain": "Correct. A — The switch port uses autonegotiation for speed and duplex (auto/auto). When the far end disables autonegotiation and is fixed at 100 Mbps full duplex, the switch cannot complete normal autonegotiation and typically falls back to half duplex on a 100BASE-TX link while the PC stays full duplex\u2014classic duplex mismatch with collisions, retries, and low throughput even though the link stays up. The Type column is 10/100BaseTX (copper), not fiber (B). Speed is not mismatched in the usual \u201c10 vs 100\u201d sense here (C). There is no sign of the wrong transceiver or media family on the switch port (D).",
            "choices": [
                "There is a duplex mismatch on the interface",
                "There is an issue with the fiber on the switch interface",
                "There is a speed mismatch on the interface",
                "There is an interface type mismatch",
            ],
        },
        {
            "slug": "ipv6-ho-fa01-eui64-from-mac-topology",
            "title": "CCNA — HO fa0/1 IPv6 EUI-64 from MAC",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/ipv6-ho-fa01-eui64-from-mac-topology.png" alt="Topology: Server to HO router fa0/1 (MAC C601.420F.0007) through ISP cloud; IPv6 prefix 2001:db8:0:1::/64 on the path toward router B, switch S2, and Host A." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. An engineer is configuring the HO router. Which IPv6 address configuration must be applied to the router fa0/1 interface for the router to assign a unique 64-bit IPv6 address to itself?",
            "name": "ipv6hoeui1",
            "correct": "A",
            "mono": True,
            "explain": "Correct. A \u2014 For a global unicast /64 on HO, the host portion is built with EUI-64 from the interface MAC C601.420F.0007: split the 48-bit address after the third byte and insert FFFE (C601.42 \u2192 C601.42FFFE \u2192 0F0007), forming the 64-bit interface identifier used with prefix 2001:db8:0:1::/64, which compresses to 2001:DB8:0:1:C601:42FF:FE0F:7/64. Option B corrupts the FFFE placement. Option C inserts an ad hoc FFFF pattern that does not follow the MAC. Option D embeds fe80-style text in what must be a global unicast address on that prefix.",
            "choices": [
                "ipv6 address 2001:DB8:0:1:C601:42FF:FE0F:7/64",
                "ipv6 address 2001:DB8:0:1:C601:42FE:800F:7/64",
                "ipv6 address 2001:DB8:0:1:FFFF:C601:420F:7/64",
                "ipv6 address 2001:DB8:0:1:FE80:C601:420F:7/64",
            ],
        },
        {
            "slug": "dhcp-relay-gi00-helper-server-subnet-exhibit",
            "title": "CCNA — DHCP relay (topology and show run)",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/dhcp-relay-gi00-helper-server-subnet-exhibit-topology.png" alt="Topology: DHCP client on router GigabitEthernet0/0; DHCP server 172.16.2.2 on GigabitEthernet0/1." width="900" decoding="async" loading="lazy" />
      </figure>
      <div class="exhibit-router-cli" role="region" aria-label="Router show running-config interfaces">
        <pre>Router#show run
Building configuration...
!
interface GigabitEthernet0/0
 ip address 10.10.10.1 255.255.255.0
 duplex auto
 speed auto
!
interface GigabitEthernet0/1
 ip address 172.16.2.1 255.255.255.0
 duplex auto
 speed auto
!
</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. An engineer is configuring a new router on the network and applied the configuration shown. Which additional configuration allows the DHCP client to obtain its IP address from the DHCP server?",
            "name": "dhcprelayrt1",
            "correct": "C",
            "explain": "Correct. C \u2014 DHCP clients discover servers with broadcasts that do not cross routed boundaries. On the router interface that faces the clients (GigabitEthernet0/0 here), ip helper-address 172.16.2.2 relays DHCP (and related) broadcasts to the DHCP server\u2019s unicast address so the client can complete DORA on a different subnet. Option A refers to relay information (Option 82) settings, not enabling basic relay. ip dhcp smart-relay (B) is an alternate-path relay enhancement, not the first-step fix. ip address dhcp on GigabitEthernet0/0 (D) would make the router obtain its own interface address from DHCP, not relay for LAN hosts.",
            "choices": [
                "Configure the ip dhcp relay information command under interface Gi0/1",
                "Configure the ip dhcp smart-relay command globally on the router",
                "Configure the ip helper-address 172.16.2.2 command under interface Gi0/0",
                "Configure the ip address dhcp command under interface Gi0/0",
            ],
        },
        {
            "slug": "static-route-r14-172-21-34-25-via-r86",
            "title": "CCNA — R14 static route to 172.21.34.0/25 via R86",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/static-route-r14-172-21-34-25-via-r86-topology.png" alt="Topology: R14 Fa0/0 to R86 Fa0/0 on 10.73.65.64/30 (.65 on R14, .66 on R86); R14 Loopback0 10.10.1.14/32; R86 Loopback0 10.10.1.86/32." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. A static route must be configured on R14 to forward traffic for the 172.21.34.0/25 network that resides on R86. Which command must be used to fulfill the request?",
            "name": "r14st17221",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 The static route must match the destination prefix and mask exactly (/25 is 255.255.255.128) and point to a valid next hop on the directly connected link toward R86. R86\u2019s address on 10.73.65.64/30 is 10.73.65.66. Option A uses a /26 mask and next hop 10.73.65.65, which is R14\u2019s own interface address on the link. Option B advertises the wrong mask (/24). Option C uses an incorrect mask for the /25 destination and uses 10.73.65.64, the subnet network address, as the next hop.",
            "choices": [
                "ip route 172.21.34.0 255.255.255.192 10.73.65.65",
                "ip route 172.21.34.0 255.255.255.0 10.73.65.65",
                "ip route 172.21.34.0 255.255.128.0 10.73.65.64",
                "ip route 172.21.34.0 255.255.255.128 10.73.65.66",
            ],
        },
        {
            "slug": "floating-static-router1-primary-default-route",
            "title": "CCNA — Router1 primary default for floating backup",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/floating-static-router1-primary-default-route-topology.png" alt="Topology: LAN to Router1 GigabitEthernet0/1; Primary ISP on Router1 GigabitEthernet1/0; Backup ISP on Router1 GigabitEthernet1/1." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. A company is configuring a failover plan and must implement the default routes in such a way that a floating static route will assume traffic forwarding when the primary link goes down. Which primary route configuration must be used?",
            "name": "r1fltpri1",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 The primary IPv4 default static route should use the normal static form with the default administrative distance (1). The separate backup \u201cfloating\u201d static is the same prefix/mask with a higher AD so it only installs when the primary is unavailable; the primary line itself is not labeled floating. ip route does not take tracked or floating keywords in the way shown in B and C. Option A appends an interface name after the next hop in an order that is not the usual Cisco static syntax (when specifying both, the typical form is exit interface then next hop).",
            "choices": [
                "ip route 0.0.0.0 0.0.0.0 192.168.0.2 GigabitEthernet1/0",
                "ip route 0.0.0.0 0.0.0.0 192.168.0.2 tracked",
                "ip route 0.0.0.0 0.0.0.0 192.168.0.2 floating",
                "ip route 0.0.0.0 0.0.0.0 192.168.0.2",
            ],
        },
        {
            "slug": "switchport-trunk-allowed-vlan-add-104",
            "title": "CCNA — Trunk: add VLAN 104 without replacing list",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/switchport-trunk-allowed-vlan-add-104-topology.png" alt="Topology: SW1 Ethernet0/0 to SW2 Ethernet0/0 802.1Q trunk; VLANs 1, 100, 101, 102, 103 allowed; new VLAN 104." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. An engineer is asked to insert the new VLAN into the existing trunk without modifying anything previously configured. Which command accomplishes this task?",
            "name": "trnkadd104",
            "correct": "C",
            "explain": "Correct. C \u2014 On an 802.1Q trunk, switchport trunk allowed vlan add 104 appends VLAN 104 to the current allow list without replacing the VLANs already permitted (1, 100\u2013103 here). switchport trunk allowed vlan 100-104 (A) replaces the list with only that range, dropping VLAN 1 and any other VLANs outside 100\u2013104. allowed vlan all (B) changes behavior to permit every VLAN, not a minimal add. allowed vlan 104 (D) replaces the list with only VLAN 104, removing the others.",
            "choices": [
                "switchport trunk allowed vlan 100-104",
                "switchport trunk allowed vlan all",
                "switchport trunk allowed vlan add 104",
                "switchport trunk allowed vlan 104",
            ],
        },
        {
            "slug": "wan-gigabitethernet0-0-0-crc-errors-poor-performance",
            "title": "CCNA — WAN Gi0/0/0 CRC errors (show interface)",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="ISR4331 show interfaces GigabitEthernet0/0/0">
        <pre>Router#show interfaces GigabitEthernet0/0/0
GigabitEthernet0/0/0 is up, line protocol is up
  Hardware is ISR4331-3x1GE, address is 5486.bc25.1f70 (bia 5486.bc25.1f70)
  Description: &lt;&lt; WAN Link &gt;&gt;
  Internet address is 192.0.2.2/30
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Keepalive set (10 sec)
  Full Duplex, 1000Mbps, media type is RJ45
  output flow-control is unsupported, input flow-control is off
  ARP type: ARPA, ARP Timeout 04:00:00
  Last input 00:00:00, output 00:00:00, output hang never
  Last clearing of "show interface" counters never
  Input queue: 0/375/0/0 (size/max/drops/flushes); Total output drops: 0
  Queueing strategy: fifo
  Output queue: 0/40 (size/max)
  5 minute input rate 7000 bits/sec, 4 packets/sec
  5 minute output rate 4000 bits/sec, 4 packets/sec
     22579370 packets input, 8825545968 bytes, 0 no buffer
     Received 67 broadcasts (0 IP multicasts)
     0 runts, 0 giants, 0 throttles
     3612699 input errors, 3612699 CRC, 0 frame, 0 overrun, 0 ignored
     0 watchdog, 10747057 multicast, 0 pause input
     12072167 packets output, 1697953637 bytes, 0 underruns
     0 output errors, 0 collisions, 1 interface resets
     0 unknown protocol drops
     0 babbles, 0 late collision, 0 deferred
     5 lost carrier, 0 no carrier, 0 pause output
     0 output buffer failures, 0 output buffers swapped out</pre>
      </div>""",
            "stem": "Refer to the exhibit. What is a reason for poor performance on the network interface?",
            "name": "wancrcgi1",
            "correct": "B",
            "explain": "Correct. B \u2014 The counters show a very large number of input errors that are almost entirely CRC errors while the link is up at 1 Gb/s full duplex with low utilization. CRC failures indicate received frames were corrupted on the wire; that pattern most often traces to physical-layer problems such as a faulty cable, loose connector, or failing port/transceiver. Broadcasts are negligible compared with total input packets (A). Collisions are zero, which is not the usual signature of a duplex/speed mismatch on full duplex (C). The bandwidth statement influences routing metrics and reporting; it does not generate CRC errors (D).",
            "choices": [
                "The interface is receiving excessive broadcast traffic.",
                "The cable connection between the two devices is faulty.",
                "The interface is operating at a different speed than the connected device.",
                "The bandwidth setting of the interface is misconfigured",
            ],
        },
        {
            "slug": "ospf-r3-dr-priority-gi01-104",
            "title": "CCNA — R3 as OSPF DR on 10.0.4.0/24",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/ospf-r3-dr-gi01-priority-100-topology.png" alt="Topology: R1 Gi0/0 on 10.0.1.0/24, R2 Gi0/0 on 10.0.2.0/24, R3 Gi0/0 on 10.0.3.0/24; shared 10.0.4.0/24 on R1 Gi0/1 (.1), R2 Gi0/1 (.2), R3 Gi0/1 (.3)." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. Routers R1 and R3 have the default configuration. The router R2 priority is set to 99. Which commands on R3 configure it as the DR in the 10.0.4.0/24 network?",
            "name": "ospfdr3g104",
            "correct": "A",
            "mono": True,
            "explain": "Correct. A \u2014 DR election on the 10.0.4.0/24 broadcast segment uses OSPF interface priority on each router\u2019s interface attached to that segment. R3 attaches via GigabitEthernet0/1 (Gig0/1). R2 already uses priority 99; R1 and R3 default to 1. Raising R3\u2019s priority on Gig0/1 to 100 makes R3 win the DR election over R2. GigabitEthernet0/0 (B and C) is on the 10.0.3.0/24 stub, not the shared 10.0.4.0/24 LAN. Priority 0 (D) removes R3 from DR/BDR eligibility.",
            "choices": [
                "R3(config)#interface Gig0/1\nR3(config-if)#ip ospf priority 100",
                "R3(config)#interface Gig0/0\nR3(config-if)#ip ospf priority 100",
                "R3(config)#interface Gig0/0\nR3(config-if)#ip ospf priority 1",
                "R3(config)#interface Gig0/1\nR3(config-if)#ip ospf priority 0",
            ],
        },
        {
            "slug": "router1-longest-match-10-10-13-158-show-ip-route",
            "title": "CCNA — Router1 next hop for 10.10.13.158 (topology and route table)",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/router1-longest-match-10-10-13-158-show-ip-route-topology.png" alt="Topology: Router1 hub to MPLS cloud 10.10.12.0/30, Internet cloud 10.10.11.0/30, Router2 10.10.10.0/30, Router3 10.10.10.4/30, Router4 10.10.10.8/30, Router5 10.10.10.12/30." width="900" decoding="async" loading="lazy" />
      </figure>
      <div class="exhibit-router-cli" role="region" aria-label="Router1 show ip route">
        <pre>Router1#show ip route
Gateway of last resort is 10.10.11.2 to network 0.0.0.0
    209.165.200.0/27 is subnetted, 1 subnets
B     209.165.200.224 [20/0] via 10.10.12.2, 03:32:14
    209.165.201.0/27 is subnetted, 1 subnets
B     209.165.201.0 [20/0] via 10.10.12.2, 02:26:53
    209.165.202.0/27 is subnetted, 1 subnets
B     209.165.202.128 [20/0] via 10.10.12.2, 02:46:03
    10.0.0.0/8 is variably subnetted, 10 subnets, 4 masks
O     10.10.13.0/25 [110/2] via 10.10.10.1, 00:00:04, GigabitEthernet0/0
O     10.10.13.128/28 [110/2] via 10.10.10.5, 00:00:12, GigabitEthernet0/1
O     10.10.13.144/28 [110/2] via 10.10.10.9, 00:01:57, GigabitEthernet0/2
O     10.10.13.160/29 [110/2] via 10.10.10.5, 00:00:12, GigabitEthernet0/1
O     10.10.13.208/29 [110/2] via 10.10.10.13, 00:01:57, GigabitEthernet0/3
S*    0.0.0.0/0 [1/0] via 10.10.11.2</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. Which next-hop IP address does Router1 use for packets destined to host 10.10.13.158?",
            "name": "r1nh158",
            "correct": "D",
            "explain": "Correct. D \u2014 Router1 picks the longest matching prefix. 10.10.13.158 falls in 10.10.13.144/28 (.144\u2013.159) but not in the shorter /25 (.0\u2013.127) or the other listed /28 and /29 blocks. The OSPF route for 10.10.13.144/28 forwards via 10.10.10.9. The default route via 10.10.11.2 (B) is only used when no more specific route matches. 10.10.10.5 (A) is the next hop for other prefixes in the table, not for 10.10.13.158. 10.10.12.2 (C) is the BGP next hop for the 209.165.x.x networks.",
            "choices": [
                "10.10.10.5",
                "10.10.11.2",
                "10.10.12.2",
                "10.10.10.9",
            ],
        },
        {
            "slug": "r1-wan-lan-route-10-0-10-ad-precedence",
            "title": "CCNA — R1: EIGRP vs OSPF for 10.0.10.0/24 (show ip route)",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="R1 show ip route">
        <pre>R1#show ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 4 subnets, 2 masks
C        10.0.0.0/8 is directly connected, Loopback0
O        10.0.1.3/32 [110/100] via 10.0.1.100, 00:39:08, Serial0
C        10.0.1.0/24 is directly connected, Serial0
O        10.0.1.5/32 [110/5] via 10.0.1.50, 00:39:08, Serial0
O        10.0.10.0/24 [110/10] via 10.0.1.4, 00:39:08, GigabitEthernet0/0
D        10.0.10.0/24 [90/10] via 10.0.1.5, 00:39:08, GigabitEthernet0/1</pre>
      </div>""",
            "stem": "Refer to the exhibit. Web traffic is coming in from the WAN interface. Which route takes precedence when the router is processing traffic destined for the LAN network at 10.0.10.0/24?",
            "name": "r1wanlan1",
            "correct": "A",
            "explain": "Correct. A \u2014 The routing table lists two equal-length routes to 10.0.10.0/24: OSPF with administrative distance 110 via 10.0.1.4, and EIGRP with administrative distance 90 via 10.0.1.5. When the prefix and mask match, the route with the lower AD is installed and used, so EIGRP via 10.0.1.5 wins. The /32 OSPF host routes (C and D) are irrelevant to forwarding toward the entire 10.0.10.0/24 LAN. The OSPF path via 10.0.1.4 (B) is valid but not preferred because its AD is higher than EIGRP\u2019s.",
            "choices": [
                "via next-hop 10.0.1.5",
                "via next-hop 10.0.1.4",
                "via next-hop 10.0.1.50",
                "via next-hop 10.0.1.100",
            ],
        },
        {
            "slug": "r15-ssh-version2-minimum-config-show-run",
            "title": "CCNA — R15: minimum config for SSHv2 (show run)",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="Router show running-config excerpt">
        <pre>Router#show run
Building configuration...

Current configuration : 1530 bytes
Last configuration change at 11:32:53 UTC Thu Feb 10 2020
!
upgrade fpd auto
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
hostname Router
boot-start-marker
boot-end-marker
!
no aaa new-model
no ip icmp rate-limit unreachable
!</pre>
      </div>""",
            "stem": "Refer to the exhibit. Which minimum configuration items are needed to enable Secure Shell version 2 access to R15?",
            "name": "r15sshmin1",
            "correct": "C",
            "mono": True,
            "explain": "Correct. C \u2014 SSHv2 needs RSA server keys: set a meaningful hostname (R15), define ip domain-name so the key can be generated, run crypto key generate rsa, force ip ssh version 2, and allow SSH on the VTYs with transport input ssh. Option A omits ip domain-name and ip ssh version 2 and adds non-essential lines (source-interface, stricthostkeycheck text that is not part of the usual minimum). Option B leaves the hostname as Router, uses transport input all (not SSH-only), and adds optional logging. Option D skips hostname and ip domain-name and repeats optional or invalid-looking lines.",
            "choices": [
                "Router(config)#hostname R15\nR15(config)#crypto key generate rsa general-keys modulus 1024\nR15(config-line)#line vty 0 15\nR15(config-line)# transport input ssh\nR15(config)#ip ssh source-interface Fa0/0\nR15(config)#ip ssh stricthostkeycheck",
                "Router(config)#ip domain-name cisco.com\nRouter(config)#crypto key generate rsa general-keys modulus 1024\nRouter(config)#ip ssh version 2\nRouter(config-line)#line vty 0 15\nRouter(config-line)# transport input all\nRouter(config)#ip ssh logging events",
                "Router(config)#hostname R15\nR15(config)#ip domain-name cisco.com\nR15(config)#crypto key generate rsa general-keys modulus 1024\nR15(config)#ip ssh version 2\nR15(config-line)#line vty 0 15\nR15(config-line)# transport input ssh",
                "Router(config)#crypto key generate rsa general-keys modulus 1024\nRouter(config)#ip ssh version 2\nRouter(config-line)#line vty 0 15\nRouter(config-line)# transport input ssh\nRouter(config)#ip ssh logging events\nR15(config)#ip ssh stricthostkeycheck",
            ],
        },
        {
            "slug": "wlc-80211r-fast-transition-ft-psk",
            "title": "CCNA — 802.11r (FT) with WPA2-PSK on WLC",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/wlc-80211r-fast-transition-ft-psk-wlan-security-gui.png" alt="WLAN security GUI: Fast Transition disabled; PMF disabled; WPA2 Policy and AES enabled; AKM PSK enabled, 802.1X and FT options off." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. Users need to connect to the wireless network with IEEE 802.11r-compatible devices. The connection must be maintained as users travel between floors or to other areas in the building. What must be the configuration of the connection?",
            "name": "wlc11rft1",
            "correct": "D",
            "explain": "Correct. D \u2014 IEEE 802.11r (Fast Transition) speeds secure roaming by allowing key negotiation steps to be done ahead of time. On a WPA2-PSK WLAN (PSK enabled in AKM, as in the exhibit), you enable Fast Transition and select **FT PSK** so the FT mode matches the pre-shared key credential. **FT 802.1X** (C) pairs with 802.1X AKM, not PSK-only. WPA Policy with CCKM (A) is legacy centralized WLAN keying, not 802.11r. Disabling AES (B) would break normal WPA2-AES operation.",
            "choices": [
                "Select the WPA Policy option with the CCKM option",
                "Disable AES encryption",
                "Enable Fast Transition and select the FT 802.1x option",
                "Enable Fast Transition and select the FT PSK option",
            ],
        },
        {
            "slug": "etherchannel-lacp-sw1-active-sw2-passive-initiation",
            "title": "CCNA — LACP: only Switch1 initiates (topology and baseline config)",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/etherchannel-lacp-sw1-active-sw2-passive-initiation-topology.png" alt="Topology: Switch 1 E1/1 and E1/2 dual links to Switch 2 E1/1 and E1/2 for EtherChannel." width="900" decoding="async" loading="lazy" />
      </figure>
      <div class="exhibit-router-cli" role="region" aria-label="Switch1 and Switch2 baseline EtherChannel-related configuration">
        <pre>! Switch 1
interface Po1
 switchport
 switchport mode access
 switchport access vlan 2
interface Ethernet1/1 - 2
 switchport
 switchport mode access
 switchport access vlan 2
!
! Switch 2
interface Po1
 switchport
 switchport mode access
 switchport access vlan 2
interface Ethernet1/1 - 2
 switchport
 switchport mode access
 switchport access vlan 2</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. An engineer is configuring an EtherChannel using LACP between Switches 1 and 2. Which configuration must be applied so that only Switch 1 sends LACP initiation packets?",
            "name": "echlacpsw12a",
            "correct": "C",
            "mono": True,
            "explain": "Correct. C \u2014 With IEEE 802.3ad LACP, a port in **active** mode transmits LACP PDUs to start or sustain negotiation; a **passive** port waits for a neighbor\u2019s LACPDUs and responds but does not initiate. To have **only Switch 1** initiate, place **mode active** on Switch 1 and **mode passive** on Switch 2. **mode on** (A and D) builds a static (non-LACP) bundle, which does not match \u201cusing LACP.\u201d Option B makes Switch 2 active and Switch 1 passive, so Switch 2 would be the side initiating.",
            "choices": [
                "Switch1(config-if)#channel-group 1 mode on\nSwitch2(config-if)#channel-group 1 mode passive",
                "Switch1(config-if)#channel-group 1 mode passive\nSwitch2(config-if)#channel-group 1 mode active",
                "Switch1(config-if)#channel-group 1 mode active\nSwitch2(config-if)#channel-group 1 mode passive",
                "Switch1(config-if)#channel-group 1 mode on\nSwitch2(config-if)#channel-group 1 mode active",
            ],
        },
        {
            "slug": "stp-vlan20-four-switch-root-bridge",
            "title": "CCNA — STP root for VLAN 20 (four switches)",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/stp-vlan20-four-switch-root-bridge-topology.png" alt="Topology: SW1, SW2, SW3, and SW4 in a full mesh; center label VLAN 20." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. SW1 = 24596 0018.184e.3c00; SW2 = 28692 004a.14e5.4077; SW3 = 32788 0022.55cf.dd00; SW4 = 64000 0041.454d.407f. Which switch becomes the root of a spanning tree for VLAN 20 if all links are of equal speed?",
            "name": "stpv20root1",
            "correct": "A",
            "explain": "Correct. A \u2014 The root bridge is the switch with the lowest bridge ID (bridge priority concatenated with the base MAC). Compare priorities first: 24596 on SW1 is lower than 28692, 32788, and 64000 on SW2\u2013SW4, so SW1 wins root election for VLAN 20. Equal link speeds do not change bridge ID comparison. If priorities tied, the lower MAC would break the tie.",
            "choices": [
                "SW1",
                "SW2",
                "SW3",
                "SW4",
            ],
        },
        {
            "slug": "nat-router1-vlan200-acl-inside-source-overload",
            "title": "CCNA — NAT: allow VLAN 200 through PAT ACL",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/nat-router1-vlan100-vlan200-internet-topology.png" alt="Topology: Router1 with VLAN 100 and VLAN 200 internal clouds and Internet cloud on GigabitEthernet0/0." width="900" decoding="async" loading="lazy" />
      </figure>
      <div class="exhibit-router-cli" role="region" aria-label="Router1 NAT-related configuration">
        <pre>Router1(config)#interface GigabitEthernet0/0
Router1(config-if)#ip address 209.165.200.225 255.255.255.224
Router1(config-if)#ip nat outside
Router1(config)#interface GigabitEthernet0/1
Router1(config-if)#ip nat inside
Router1(config)#interface GigabitEthernet0/1.100
Router1(config-if)#encapsulation dot1Q 100
Router1(config-if)#ip address 10.10.10.1 255.255.255.0
Router1(config)#interface GigabitEthernet0/1.200
Router1(config-if)#encapsulation dot1Q 200
Router1(config-if)#ip address 10.10.20.1 255.255.255.0
Router1(config)#ip access-list standard NAT_INSIDE_RANGES
Router1(config-std-nacl)#permit 10.10.10.0 0.0.0.255
Router1(config)#ip nat inside source list NAT_INSIDE_RANGES interface GigabitEthernet0/0 overload</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. Users on existing VLAN 100 can reach sites on the Internet. Which action must the administrator take to establish connectivity to the Internet for users in VLAN 200?",
            "name": "natvl2001",
            "correct": "B",
            "explain": "Correct. B \u2014 PAT overload is already applied to traffic permitted by standard ACL NAT_INSIDE_RANGES. That ACL currently permits only 10.10.10.0/24 (VLAN 100), so 10.10.20.0/24 (VLAN 200) never matches and is not translated. Add a permit for 10.10.20.0 0.0.0.255 (or replace the ACL with a broader permit that includes both subnets) so VLAN 200 hosts are eligible for the same ip nat inside source ... overload mapping. A separate NAT pool (A) is not required when using interface overload. The outside interface is already correct for all inside subnets (C). Static NAT entries (D) are not the usual way to enable general outbound Internet access for a whole VLAN when dynamic overload already fits.",
            "choices": [
                "Define a NAT pool on the router.",
                "Update the NAT_INSIDE_RANGES ACL",
                "Configure the ip nat outside command on another interface for VLAN 200",
                "Configure static NAT translations for VLAN 200",
            ],
        },
        {
            "slug": "switch-a-gi01-ip-phone-vlan50-voice51",
            "title": "CCNA — Switch A Gi0/1: data VLAN 50, voice VLAN 51",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/switch-a-gi01-ip-phone-vlan50-voice51-topology.png" alt="Topology: Switch A and Switch B on Gi0/0; each Gi0/1 to IP phone with PC daisy-chained; legend Data VLAN 50, Voice VLAN 51." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. Switch A is newly configured. All VLANs are present in the VLAN database. The IP phone and PC A on Gi0/1 must be configured for the appropriate VLANs to establish connectivity between the PCs. Which command set fulfills the requirement?",
            "name": "swagi0151",
            "correct": "A",
            "mono": True,
            "explain": "Correct. A \u2014 For a Cisco IP phone with a PC on the phone\u2019s access port, use an access port for untagged user data and a separate voice VLAN for tagged voice traffic from the phone. switchport mode access, switchport access vlan 50 (data for PC A), and switchport voice vlan 51 matches the diagram. B is invalid: voice VLAN cannot be set to untagged that way. C and D use trunk mode and do not apply the standard access + voice VLAN pattern for this endpoint design.",
            "choices": [
                """SwitchA(config-if)#switchport mode access
SwitchA(config-if)#switchport access vlan 50
SwitchA(config-if)#switchport voice vlan 51""",
                """SwitchA(config-if)#switchport mode access
SwitchA(config-if)#switchport access vlan 50
SwitchA(config-if)#switchport voice vlan untagged""",
                """SwitchA(config-if)#switchport mode trunk
SwitchA(config-if)#switchport trunk allowed vlan add 50, 51
SwitchA(config-if)#switchport voice vlan dot1p""",
                """SwitchA(config-if)#switchport mode trunk
SwitchA(config-if)#switchport trunk allowed vlan 50, 51
SwitchA(config-if)#switchport qos trust cos""",
            ],
        },
        {
            "slug": "r1-floating-static-19216820-via-r3-ospf-area20",
            "title": "CCNA — R1 floating static to 192.168.20.0/24 via R3",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/r1-ospf-area20-triangle-floating-static-19216820-topology.png" alt="Topology: R1, R2, R3 in a triangle labeled OSPF Area 20; subnets 192.168.10.0/24, 192.168.20.0/24, 192.168.30.0/24 with .1 and .2 host addresses on each link." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. R1 learns all routes via OSPF. Which command configures a backup static route on R1 to reach the 192.168.20.0/24 network via R3?",
            "name": "r1flt201",
            "correct": "A",
            "mono": True,
            "explain": "Correct. A \u2014 A floating static backup must use an administrative distance greater than OSPF\u2019s default (110) so the OSPF-learned path stays preferred while it is valid. Next hop to R3 on the R1\u2013R3 link is 192.168.30.2, with the correct /24 mask. B uses AD 90, which is lower than 110, so this static would beat OSPF and would not act only as a backup. C uses the wrong mask (255.255.0.0). D omits an AD; a standard static defaults to AD 1 and would also override OSPF.",
            "choices": [
                "R1(config)#ip route 192.168.20.0 255.255.255.0 192.168.30.2 111",
                "R1(config)#ip route 192.168.20.0 255.255.255.0 192.168.30.2 90",
                "R1(config)#ip route 192.168.20.0 255.255.0.0 192.168.30.2",
                "R1(config)#ip route 192.168.20.0 255.255.255.0 192.168.30.2",
            ],
        },
        {
            "slug": "r1-r2-floating-static-backup-gi01-workstation-lans",
            "title": "CCNA — R1/R2: floating static backup over Gi0/1",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/r1-r2-dual-links-ospf-floating-static-backup-topology.png" alt="Topology: R1 and R2 with parallel Gi0/0 and Gi0/1 links on 172.16.0.0/30 and 172.16.0.4/30; SW1 LAN 172.16.1.0/24; SW2 LAN 172.16.2.0/27; OSPF process 200 on both routers." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. The primary route across Gi0/0 is configured on both routers. A secondary route must be configured to establish connectivity between the workstation networks. Which command set must be configured to complete this task?",
            "name": "r1r2flt54",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 The workstation subnets are 172.16.2.0/27 (mask 255.255.255.224) behind R2 and 172.16.1.0/24 (255.255.255.0) behind R1. Backup statics must point across the Gi0/1 transit (172.16.0.4/30): from R1 use next hop 172.16.0.6 (R2\u2019s Gi0/1); from R2 use 172.16.0.5 (R1\u2019s Gi0/1). Administrative distance must exceed OSPF\u2019s default 110 so these remain floating backups; 111 and 112 satisfy that. A uses the wrong mask for /27, next hops on the primary Gi0/0 link, and would not steer over Gi0/1. B uses wrong masks, AD 89 below OSPF, and next hop 172.16.0.5 from R1 is R1\u2019s own address on that subnet. C uses wrong masks and AD 110 ties OSPF instead of backing it up.",
            "choices": [
                """R1
ip route 172.16.2.0 255.255.255.240 172.16.0.2 113

R2
ip route 172.16.1.0 255.255.255.0 172.16.0.1 114""",
                """R1
ip route 172.16.2.0 255.255.255.240 172.16.0.5 89

R2
ip route 172.16.1.0 255.255.255.0 172.16.0.6 89""",
                """R1
ip route 172.16.2.0 255.255.255.248 172.16.0.5 110

R2
ip route 172.16.1.0 255.255.255.0 172.16.0.6 110""",
                """R1
ip route 172.16.2.0 255.255.255.224 172.16.0.6 111

R2
ip route 172.16.1.0 255.255.255.0 172.16.0.5 112""",
            ],
        },
        {
            "slug": "cat9300-cdp-timer-rapid-neighbor-discovery",
            "title": "CCNA — Cat9300: CDP timer for faster neighbor discovery",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="Cat9300 show cdp output">
        <pre>Cat9300#show cdp
Global CDP information:
  Sending CDP packets every 60 seconds
  Sending a holdtime value of 180 seconds
  Sending CDPv2 advertisements is enabled</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. Which action must be taken so that neighboring devices rapidly discover switch Cat9300?",
            "name": "cdp93001",
            "correct": "D",
            "explain": "Correct. D \u2014 Neighbors build their view of Cat9300 from CDP advertisements that Cat9300 transmits. The global CDP timer sets how often those packets are sent (the exhibit shows every 60 seconds). Configuring a shorter value such as cdp timer 10 on Cat9300 increases advertisement frequency so neighbors see updates sooner. Holdtime (B) controls how long neighbors retain learned information without a refresh; it does not shorten Cat9300\u2019s transmit interval. Changing the timer on neighbors (C) affects how often those devices advertise themselves, not how often Cat9300 is announced to them. Portfast (A) is an STP access-port behavior and does not change CDP discovery timing.",
            "choices": [
                "Enable portfast on the ports that connect to neighboring devices",
                "Configure the cdp holdtime 10 command on switch Cat9300",
                "Configure the cdp timer 10 command on the neighbors of switch Cat9300",
                "Configure the cdp timer 10 command on switch Cat9300",
            ],
        },
        {
            "slug": "sw2-fa01-dynamic-auto-trunk-allowed-vlan5-10",
            "title": "CCNA — SW2 Fa0/1: force trunk after replace",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/sw2-fa01-dynamic-auto-trunk-allowed-vlan5-10-topology.png" alt="Topology: Sw1 and Sw2 connected fa0/1 to fa0/1; PC1 and PC2 in VLAN 5; PC3 and PC4 in VLAN 10; access ports fa0/2 and fa0/3 on each switch." width="900" decoding="async" loading="lazy" />
      </figure>
      <div class="exhibit-router-cli" role="region" aria-label="Switch2 Fa0/1 configuration in progress">
        <pre>Switch2(config)#interface fa0/1
Switch2(config-if)#switchport mode dynamic auto
Switch2(config-if)#switchport trunk allowed vlan 5,10</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. SW2 is replaced due to a hardware failure. A network engineer starts to configure SW2 by copying the Fa0/1 interface configuration from SW1. Which command must be configured on the Fa0/1 interface of SW2 to enable PC1 to connect to PC2?",
            "name": "sw2fa011",
            "correct": "A",
            "explain": "Correct. A \u2014 With switchport mode dynamic auto, the port only becomes a trunk if the far end actively negotiates one (for example trunk or dynamic desirable). If both ends behave passively, the link stays an access port and switchport trunk allowed vlan has no trunk to apply. Configuring switchport mode trunk forces 802.1Q trunking so VLANs 5 and 10 can cross between switches for the PCs. B changes native VLAN tagging but does not fix auto/auto trunk formation. C removes VLAN 10 from the allowed list and would block that VLAN if a trunk existed. D would pin the link to access mode and not carry the needed VLANs as a trunk.",
            "choices": [
                "switchport mode trunk",
                "switchport trunk native vlan 10",
                "switchport trunk allowed remove 10",
                "switchport mode access",
            ],
        },
        {
            "slug": "wlc-enterprise-wlan-80211r-fast-transition",
            "title": "CCNA — WLC: 802.11r Fast Transition (Enterprise WLAN)",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/wlc-enterprise-wlan-security-layer2-wpa2-fast-transition-disabled.png" alt="WLC WLAN Security Layer 2: WPA+WPA2 Enterprise, WPA2 Policy and AES enabled, 802.1X-SHA1 enabled, Fast Transition and PMF disabled, MAC filtering off." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. Users with IEEE 802.11r-capable client devices must maintain wireless connectivity while roaming between access points. Which WLAN Layer 2 security change is required?",
            "name": "wlc11rent1",
            "correct": "D",
            "explain": "Correct. D \u2014 IEEE 802.11r (Fast BSS Transition) reduces roaming time by letting compatible clients perform key operations more efficiently as they move between APs. The exhibit shows Fast Transition disabled; it must be enabled for 802.11r-oriented roaming behavior (with Enterprise/802.1X, the administrator then selects the FT 802.1X mode to match AKM). Requiring PMF (A) hardens management-frame handling but does not implement 802.11r fast roaming. MAC filtering (B) is an access-control list of MAC addresses, unrelated to 802.11r. Enabling WPA Policy (C) allows legacy WPA alongside WPA2 and does not address 802.11r.",
            "choices": [
                "Set PMF to Required",
                "Enable MAC Filtering",
                "Enable WPA Policy",
                "Set Fast Transition to Enabled",
            ],
        },
        {
            "slug": "etherchannel-lacp-sw1-sw2-g1-1-3-trunk-active",
            "title": "CCNA — LACP EtherChannel: SW1–SW2 G1/1–G1/3",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/etherchannel-lacp-sw1-sw2-g1-1-3-topology.png" alt="Topology: SW1 and SW2 with three parallel links G1/1, G1/2, and G1/3 bundled as one EtherChannel." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. Which configuration establishes a Layer 2 LACP EtherChannel when applied to both switches?",
            "name": "ecagg651",
            "correct": "C",
            "mono": True,
            "explain": "Correct. C \u2014 LACP (IEEE 802.3ad) uses channel-group mode **active** or **passive**. Applying **mode active** on both ends forms a negotiated LACP bundle. A switch-to-switch aggregate that carries multiple VLANs is normally a **trunk**. A is wrong because **passive** on both sides does not bring LACP up (each side waits for LACP messages from a partner). B uses **mode desirable**, which is **PAgP**, not LACP. D uses **mode on**, which is a **static** EtherChannel with no LACP negotiation.",
            "choices": [
                """interface range G1/1-3
switchport mode access
channel-group 1 mode passive
no shutdown""",
                """interface range G1/1-3
switchport mode trunk
channel-group 1 mode desirable
no shutdown""",
                """interface range G1/1-3
switchport mode trunk
channel-group 1 mode active
no shutdown""",
                """interface range G1/1-3
switchport mode access
channel-group 1 mode on
no shutdown""",
            ],
        },
        {
            "slug": "wlc-radius-authentication-server-network-user",
            "title": "CCNA — WLC: RADIUS server for wireless (Network User)",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/wlc-radius-authentication-server-network-user-gui.png" alt="WLC Security AAA RADIUS Authentication Servers New: Server IP 192.168.25.2, port 1812, Server Status Enabled; Network User and Management checkboxes unchecked." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. A network engineer configures the Cisco WLC to authenticate local wireless clients against a RADIUS server. Which task must be performed to complete the process?",
            "name": "wlcru661",
            "correct": "C",
            "explain": "Correct. C \u2014 On the WLC RADIUS authentication server entry, **Network User** must be enabled so this server is used for **802.1X / user authentication** for clients on the WLAN. **Management** (B) applies RADIUS to **management** access (for example administrative logins), not wireless client authentication. **Server Status** should remain enabled (A would disable the server). **Support for CoA** (D) enables RADIUS Change of Authorization features; it is not the basic step to tie the server to wireless user authentication.",
            "choices": [
                "Disable the Server Status option",
                "Enable the Management option",
                "Enable the Network User option",
                "Enable the Support for CoA option",
            ],
        },
        {
            "slug": "ip-arp-inspection-vlan5-10-fa01-untrusted-effect",
            "title": "CCNA — DAI on VLAN 5–10, access port VLAN 5",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="DAI and interface configuration">
        <pre>ip arp inspection vlan 5-10
interface fastethernet0/1
 switchport mode access
 switchport access vlan 5</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. What is the effect of this configuration?",
            "name": "dai5101",
            "correct": "D",
            "explain": "Correct. D \u2014 Dynamic ARP Inspection (DAI) validates **ingress ARP** packets on **untrusted** ports in the VLANs where it is enabled (here 5\u201310). The switch compares sender IP and MAC against trusted data such as the **DHCP snooping binding table** (or static ARP ACLs); ARP that does not match valid bindings is **discarded**. Access ports are untrusted by default. DAI does not filter all non-ARP traffic (B is wrong), does not drop every ARP frame (C is wrong), and is unrelated to restricting egress to DHCP servers only (A is wrong).",
            "choices": [
                "Egress traffic is passed only if the destination is a DHCP server.",
                "All ingress and egress traffic is dropped because the interface is untrusted.",
                "All ARP packets are dropped by the switch.",
                "The switch discards all ingress ARP traffic with invalid MAC-to-IP address bindings.",
            ],
        },
        {
            "slug": "router-gi00-lldp-third-party-isp-exhibit",
            "title": "CCNA — LLDP to third-party ISP: global enable",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="PE router Gi0/0 toward ISP">
        <pre>interface gigabitethernet0/0
 description Circuit-ATT4202-89930
 duplex full
 speed 1000
 media-type gbic
 negotiation auto
 lldp transmit
 lldp receive</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. An engineer must configure neighbor discovery between the company router and an ISP. What is the next step to complete the configuration if the ISP uses a third-party router?",
            "name": "lldpgi00",
            "correct": "D",
            "explain": "Correct. D \u2014 On Cisco IOS and IOS-XE, LLDP must be turned on with a **global** command (**lldp run**) before interface-level **lldp transmit** and **lldp receive** actually operate. Third-party peers use standard LLDP, not Cisco CDP. Disabling CDP on Gi0/0 (A) does not substitute for enabling LLDP globally. Disabling autonegotiation (B) is unrelated to LLDP neighbor discovery. You cannot complete your configuration by changing TLV settings only on the ISP router (C).",
            "choices": [
                "Disable CDP on gi0/0.",
                "Disable auto-negotiation.",
                "Enable LLDP TLVs on the ISP router.",
                "Enable LLDP globally.",
            ],
        },
        {
            "slug": "r1-show-ip-route-10-56-192-1-default-next-hop",
            "title": "CCNA — R1: longest match vs default for 10.56.192.1",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="R1 routing table excerpt">
        <pre>R1#show ip route
Codes: C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       + - replicated route, % - next hop override

Gateway of last resort is 10.56.0.1 to network 0.0.0.0

S*    0.0.0.0/0 [1/0] via 10.56.0.1
      10.0.0.0/8 is variably subnetted, 2 subnets, 2 masks
C       10.56.0.0/17 is directly connected, Vlan56
L       10.56.0.19/32 is directly connected, Vlan56
C       10.56.128.0/18 is directly connected, Vlan57
L       10.56.128.19/32 is directly connected, Vlan57</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. When router R1 is sending traffic to IP address 10.56.192.1, which interface or next hop address does it use to route the packet?",
            "name": "r110561",
            "correct": "C",
            "explain": "Correct. C \u2014 10.56.192.1 is not inside 10.56.0.0/17 (10.56.0.0\u201310.56.127.255) and not inside 10.56.128.0/18 (10.56.128.0\u201310.56.191.255). No longer-prefix match applies, so R1 uses the **gateway of last resort**: the static default **via 10.56.0.1**. A names the default **prefix**, not the forwarding next hop. B would require the destination to fall in Vlan57\u2019s connected range, which it does not. D is R1\u2019s own local /32 on Vlan57, not the next hop toward 10.56.192.1.",
            "choices": [
                "0.0.0.0/0",
                "Vlan57",
                "10.56.0.1",
                "10.56.128.19",
            ],
        },
        {
            "slug": "wlc-wlan-security-wpa-wpa2-8021x-enterprise",
            "title": "CCNA — WLC WLAN: WPA+WPA2 and 802.1X for LDAP-backed auth",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/wlc-wlan-security-wpa-wpa2-8021x-enterprise.png" alt="WLC WLAN Security Layer 2 tab: Layer 2 Security dropdown; WPA and WPA2 policy checkboxes; WPA2 Encryption AES and TKIP; Authentication Key Management 802.1X, CCKM, and PSK enable options." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. What are the two steps an engineer must take to provide the highest encryption and authentication using domain credentials from LDAP? (Choose two)",
            "name": "wlldap802",
            "choose_two": True,
            "correct": ["B", "E"],
            "explain": "Correct. B and E \u2014 Domain credentials through LDAP are normally validated when the WLAN uses **802.1X** (enterprise) authentication toward RADIUS or similar; that maps to enabling **802.1X** under Authentication Key Management on the WLC. Set **Layer 2 Security** to **WPA + WPA2** so clients can use **WPA2** with stronger ciphers such as **AES/CCMP** instead of legacy WPA-only modes. Then enable **WPA2 Policy** and **AES** under WPA+WPA2 parameters as needed so TKIP-only operation is avoided. **PSK** (C) uses a shared passphrase, not per-user domain sign-in. **Static WEP** (D) is weak. Choosing **WPA** with **TKIP** only (A) favors an older cipher and is not the strongest combination among these options.",
            "choices": [
                "Select WPA policy with TKIP Encryption",
                "Select WPA + WPA2 on layer 2 security",
                "Select PSK under authentication key management",
                "Select Static-WEP + 802.1x on Layer 2 security",
                "Select 802.1x from under authentication key management",
            ],
        },
        {
            "slug": "cat9k-lldp-suppress-management-address",
            "title": "CCNA — Cat9K: hide management IP in LLDP advertisements",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="Cat9K-1 show lldp entry Cat9K-2">
        <pre>Cat9K-1#show lldp entry Cat9K-2

Local Intf: Gi1/0/21
Chassis ID: 308b.b2b3.2880
Port id: Gi1/0/21
Port Description: GigabitEthernet1/0/21
System Name: Cat9K-2

Management Addresses:
  IP: 10.6.110.2</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. The network administrator must prevent switch Cat9K-2\u2019s IP address from appearing under Management Addresses in LLDP on other devices, without disabling LLDP. Which action accomplishes this?",
            "name": "cat9klldpma",
            "correct": "A",
            "explain": "Correct. A \u2014 The management IP is carried in the **management address** LLDP TLV inside advertisements **sent by Cat9K-2**. In global configuration on that switch, **no lldp tlv-select management-address** stops transmitting that TLV while **lldp run** and per-interface LLDP can remain enabled, so the protocol stays active without exposing the management address. B only stops Cat9K-1 from **transmitting** LLDP; Cat9K-1 still **receives** advertisements from Cat9K-2, so the neighbor\u2019s management address can still show up. C disables LLDP **receive** on Cat9K-1\u2019s interface, which hides neighbors locally but does not change what Cat9K-2 puts in its LLDP frames. D removes the **MAC/PHY configuration** TLV, not the management address.",
            "choices": [
                "Configure the no lldp tlv-select management-address command globally on Cat9K-2.",
                "Configure the no lldp transmit command on interface Gi1/0/21 on Cat9K-1.",
                "Configure the no lldp receive command on interface Gi1/0/21 on Cat9K-1.",
                "Configure the no lldp tlv-select mac-phy-cfg command globally on Cat9K-2.",
            ],
        },
        {
            "slug": "ospf-r1-drother-elect-dr-priority-clear",
            "title": "CCNA — OSPF: elect R1 as DR (priority and clear)",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/ospf-area0-r1-r2-r3-sw-star-topology.png" alt="Topology: switch SW; OSPF Area 0. R1 10.10.10.1 on FastEthernet0/0; R2 10.10.10.2 on FastEthernet0/2; R3 10.10.10.3 on FastEthernet0/1." width="900" decoding="async" loading="lazy" />
      </figure>
      <div class="exhibit-router-cli" role="region" aria-label="R1 show ip ospf neighbor">
        <pre>R1#show ip ospf neighbor

Neighbor ID     Pri   State      Dead Time   Address         Interface
10.10.10.2        1   FULL/BDR   00:00:35    10.10.10.2      FastEthernet0/0
10.10.10.3        1   FULL/DR    00:00:34    10.10.10.3      FastEthernet0/0</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. R1 has the DROTHER role in the OSPF DR/BDR election on this segment. Which configuration must an engineer implement so that R1 is elected as the DR?",
            "name": "ospfdr1clr",
            "correct": "B",
            "mono": True,
            "explain": "Correct. B \u2014 The DR is chosen by **highest OSPF interface priority** on the multi-access segment (tie-break: higher router ID). R1 must use **FastEthernet0/0** toward the segment with a priority **above** the current DR/BDR (still at 1). **DR election is not preemptive**, so after changing priority you typically run **clear ip ospf process** (or restart OSPF on the interface) so routers **reelect**. A keeps priority at the default 1. C raises **R3\u2019s** priority on **FastEthernet0/1**, favoring R3, not R1. D sets **R2\u2019s** **FastEthernet0/2** to 1 (default) and does not give R1 a winning priority.",
            "choices": [
                "R1(config)#interface FastEthernet0/0\nR1(config-if)#ip ospf priority 1\nR1#clear ip ospf process",
                "R1(config)#interface FastEthernet0/0\nR1(config-if)#ip ospf priority 200\nR1#clear ip ospf process",
                "R3(config)#interface FastEthernet0/1\nR3(config-if)#ip ospf priority 200\nR3#clear ip ospf process",
                "R2(config)#interface FastEthernet0/2\nR2(config-if)#ip ospf priority 1\nR2#clear ip ospf process",
            ],
        },
        {
            "slug": "dc1-hq1-interface-usable-host-addresses",
            "title": "CCNA — DC-1 & HQ-1: first/last usable IPv4 per mask",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/dc1-hq1-isp-topology-ip-assignment.png" alt="Topology: Internet cloud to ISP; ISP Gi1/0 to DC-1 Gi1/0; DC-1 Gi1/1 to HQ-1 Gi1/1; DC-1 Gi1/2 to a switch and firewall; HQ-1 Gi1/3 to HQ-SW1 and a workstation." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. The IPv4 address configuration must be completed on routers DC-1 and HQ-1 using only these subnets (no VLSM overlap):\n\u2022 DC-1 GigabitEthernet1/0 \u2192 10.0.0.0/30 toward ISP\n\u2022 DC-1 GigabitEthernet1/1 and HQ-1 GigabitEthernet1/1 \u2192 10.0.0.8/29\n\u2022 DC-1 GigabitEthernet1/2 \u2192 10.0.0.16/28 toward the switch/firewall block\n\u2022 HQ-1 GigabitEthernet1/3 toward HQ-SW1 \u2192 10.0.0.32/29\n\nRequirements: DC-1 Gi1/0 must be the last usable address on the /30; DC-1 Gi1/1 must be the first usable address on the /29; DC-1 Gi1/2 must be the last usable address on the /28; HQ-1 Gi1/3 must be the last usable address on the /29. Which configuration meets the requirements?",
            "name": "dc1hq1ip",
            "correct": "B",
            "mono": True,
            "explain": "Correct. B \u2014 On **10.0.0.0/30** (mask 255.255.255.252) the host addresses are **.1** and **.2**; the **last usable** is **.2** for DC-1 Gi1/0. On **10.0.0.8/29** (255.255.255.248) usable hosts are **.9\u2013.14**; the **first usable** is **.9** for DC-1 Gi1/1. On **10.0.0.16/28** (255.255.255.240) usable hosts are **.17\u2013.30**; the **last usable** is **.30** for DC-1 Gi1/2. On **10.0.0.32/29** usable hosts are **.33\u2013.38**; the **last usable** is **.38** for HQ-1 Gi1/3. A uses the **first** /30 host (.1) on DC-1 Gi1/0. C sets DC-1 Gi1/1 to **.14**, the **last** /29 host instead of the **first**. D sets HQ-1 Gi1/3 to **.33**, the **first** /29 host instead of the **last**.",
            "choices": [
                "DC-1(config)#interface GigabitEthernet1/0\nDC-1(config-if)#ip address 10.0.0.1 255.255.255.252\nDC-1(config)#interface GigabitEthernet1/1\nDC-1(config-if)#ip address 10.0.0.9 255.255.255.248\nDC-1(config)#interface GigabitEthernet1/2\nDC-1(config-if)#ip address 10.0.0.30 255.255.255.240\nHQ-1(config)#interface GigabitEthernet1/3\nHQ-1(config-if)#ip address 10.0.0.38 255.255.255.248",
                "DC-1(config)#interface GigabitEthernet1/0\nDC-1(config-if)#ip address 10.0.0.2 255.255.255.252\nDC-1(config)#interface GigabitEthernet1/1\nDC-1(config-if)#ip address 10.0.0.9 255.255.255.248\nDC-1(config)#interface GigabitEthernet1/2\nDC-1(config-if)#ip address 10.0.0.30 255.255.255.240\nHQ-1(config)#interface GigabitEthernet1/3\nHQ-1(config-if)#ip address 10.0.0.38 255.255.255.248",
                "DC-1(config)#interface GigabitEthernet1/0\nDC-1(config-if)#ip address 10.0.0.2 255.255.255.252\nDC-1(config)#interface GigabitEthernet1/1\nDC-1(config-if)#ip address 10.0.0.14 255.255.255.248\nDC-1(config)#interface GigabitEthernet1/2\nDC-1(config-if)#ip address 10.0.0.30 255.255.255.240\nHQ-1(config)#interface GigabitEthernet1/3\nHQ-1(config-if)#ip address 10.0.0.38 255.255.255.248",
                "DC-1(config)#interface GigabitEthernet1/0\nDC-1(config-if)#ip address 10.0.0.2 255.255.255.252\nDC-1(config)#interface GigabitEthernet1/1\nDC-1(config-if)#ip address 10.0.0.9 255.255.255.248\nDC-1(config)#interface GigabitEthernet1/2\nDC-1(config-if)#ip address 10.0.0.30 255.255.255.240\nHQ-1(config)#interface GigabitEthernet1/3\nHQ-1(config-if)#ip address 10.0.0.33 255.255.255.248",
            ],
        },
        {
            "slug": "json-routers-switches-array-elements-are-values",
            "title": "CCNA — JSON: strings inside arrays",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="JSON device inventory snippet">
        <pre>{
  "Routers": ["R1","R2","R3"],
  "Switches": ["SW1","SW2","SW3"]
}</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. What is represented by \u201cR1\u201d and \u201cSW1\u201d within the JSON output?",
            "name": "jsonr1sw1",
            "correct": "C",
            "explain": "Correct. C \u2014 In JSON, \u201cR1\u201d and \u201cSW1\u201d are **string values**. Each sits inside an **array**, and those arrays are the **values** of the \u201cRouters\u201d and \u201cSwitches\u201d name\u2013value pairs. The **keys** are the property names (\u201cRouters\u201d and \u201cSwitches\u201d). The **object** is the outer `{ ... }` structure. Calling the token itself an \u201carray\u201d or \u201ckey\u201d mixes up elements with the container or the property name.",
            "choices": [
                "array",
                "object",
                "value",
                "key",
            ],
        },
        {
            "slug": "vlan14-trunk-ring-sw4-sw11-sw9-pc2-pc7",
            "title": "CCNA — Trunks: PC2\u2013PC7 VLAN 14 and PC3\u2013PC9 VLAN 108",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/sw1-sw4-sw9-sw11-pc2-pc7-vlan14-trunk-topology.png" alt="Topology: SW1, SW4, SW9, SW11 with inter-switch links; PC2 VLAN 14 and PC3 VLAN 108 on SW4; PC7 VLAN 14 on SW9; PC9 VLAN 108 on SW11." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. These facts apply:\n\n\u2022 SW1 is fully configured for all traffic.\n\u2022 The SW4 and SW9 links to SW1 are already configured.\n\u2022 SW4 interface GigabitEthernet0/1 (PC2) and SW9 GigabitEthernet0/0 (PC7) are already configured.\n\u2022 The remaining switches have had all VLANs added to their VLAN database.\n\nWhich configuration establishes a successful ping from PC2 to PC7 without interrupting traffic between the other PCs (for example PC3 and PC9 in VLAN 108)?",
            "name": "swtrunks14",
            "correct": "A",
            "mono": True,
            "stem_br": True,
            "explain": "Correct. A \u2014 PC2 and PC7 are both in **VLAN 14**; Layer 2 connectivity can use the path **SW4\u2192SW11\u2192SW9** (and/or the SW1 uplinks you are not asked to change). Those inter-switch links must be **802.1Q trunks** that **allow VLAN 14** on **SW4 Gi0/2**, **SW11 Gi0/2**, **SW11 Gi0/1**, and **SW9 Gi0/2**. **PC3** and **PC9** stay in **VLAN 108** on the **SW4\u2013SW11** trunk, so that trunk must also **allow 108**; SW9\u2019s trunk toward SW11 only needs **14** for this PC2\u2013PC7 shortcut, while 108 traffic between PC3 and PC9 can stay on **SW4\u2013SW11**.\n\nB rewrites **SW4 Gi0/7** (the uplink toward **SW1**) to **allowed vlan 108** only, which **drops VLAN 14** on an already working path and breaks design assumptions. It also mis-uses **access** mode on inter-switch ports.\n\nC allows **only VLAN 14** on **SW4 Gi0/2**, so **VLAN 108** cannot cross **SW4\u2192SW11**, cutting **PC3\u2013PC9**. It also has **108** on **SW9 Gi0/2** while omitting **14** on several segments.\n\nD configures **access** ports between switches, which cannot carry multiple VLANs and breaks **VLAN 108** between SW4 and SW11 (and misconfigures SW11 with a non-topology port).",
            "choices": [
                "Option A\n\nSW4#\ninterface Gi0/2\nswitchport mode trunk\nswitchport trunk allowed vlan 14,108\n\nSW11#\ninterface Gi0/2\nswitchport mode trunk\nswitchport trunk allowed vlan 14,108\n!\ninterface Gi0/1\nswitchport mode trunk\nswitchport trunk allowed vlan 14,108\n\nSW9#\ninterface Gi0/2\nswitchport mode trunk\nswitchport trunk allowed vlan 14",
                "Option B\n\nSW4\ninterface Gi0/7\nswitchport mode trunk\nswitchport trunk allowed vlan 108\n!\ninterface Gi0/2\nswitchport mode access\nswitchport access vlan 14\n\nSW11#\ninterface Gi0/2\nswitchport mode trunk\nswitchport trunk allowed vlan 14,108\n!\ninterface Gi0/1\nswitchport mode trunk\nswitchport trunk allowed vlan 14,108\n\nSW9#\ninterface Gi0/2\nswitchport mode access\nswitchport access vlan 14",
                "Option C\n\nSW4\ninterface Gi0/2\nswitchport mode trunk\nswitchport trunk allowed vlan 14\n\nSW11#\ninterface Gi0/1\nswitchport mode trunk\nswitchport trunk allowed vlan 14\n\nSW9#\ninterface Gi0/2\nswitchport mode trunk\nswitchport trunk allowed vlan 108",
                "Option D\n\nSW4\ninterface Gi0/2\nswitchport mode access\nswitchport access vlan 14\n\nSW11#\ninterface Gi0/2\nswitchport mode access\nswitchport access vlan 14\n!\ninterface Gi0/0\nswitchport mode access\nswitchport access vlan 14\n!\ninterface Gi0/1\nswitchport mode trunk\n\nSW9#\ninterface Gi0/2\nswitchport mode access\nswitchport access vlan 14",
            ],
        },
        {
            "slug": "ospf-r1-passive-priority-router-id-neighbor-r2-only",
            "title": "CCNA — OSPF: R1 neighbors only R2, no DR, fixed router-id",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/ospf-r1-r2-fa00-10-100-1-0-topology.png" alt="Topology: R1 FastEthernet0/0 connected to R2 FastEthernet0/0; segment labeled 10.100.1.0; host .1 on R1 and .2 on R2 (10.100.1.1 and 10.100.1.2)." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. An OSPF neighbor relationship must be configured on R1 using these guidelines:\n\n\u2022 R1 is only permitted to establish a neighbor with R2 (out FastEthernet0/0).\n\u2022 R1 will never participate in DR elections.\n\u2022 R1 will use a router ID of 10.1.1.1.\n\nWhich configuration meets all requirements?",
            "name": "ospfr1r2p",
            "correct": "A",
            "mono": True,
            "stem_br": True,
            "explain": "Correct. A \u2014 **router-id 10.1.1.1** sets the required RID. **passive-interface default** stops OSPF hellos on every interface unless you undo it; **no passive-interface FastEthernet0/0** is the only interface that can form an adjacency with **R2**. **ip ospf priority 0** on that Ethernet keeps R1 **ineligible for DR/BDR** on the broadcast link. A **network** statement for **10.100.1.0/24** in area 0 enables OSPF on Fa0/0 while passive default still limits where neighbors can form.\n\nB omits **priority 0**, so R1 could still win **DR/BDR** on the segment to R2. C uses **router-id 1.1.1.1** instead of **10.1.1.1**. D marks **FastEthernet0/0 as passive**, so R1 does not send OSPF hellos on the only link that should peer with R2.",
            "choices": [
                "Option A\n\nR1(config)#router ospf 1\nR1(config-router)#router-id 10.1.1.1\nR1(config-router)#passive-interface default\nR1(config-router)#no passive-interface FastEthernet0/0\nR1(config-router)#network 10.100.1.0 0.0.0.255 area 0\nR1(config-router)#exit\nR1(config)#interface FastEthernet0/0\nR1(config-if)#ip ospf priority 0",
                "Option B\n\nR1(config)#router ospf 1\nR1(config-router)#router-id 10.1.1.1\nR1(config-router)#passive-interface default\nR1(config-router)#no passive-interface FastEthernet0/0\nR1(config-router)#network 10.100.1.0 0.0.0.255 area 0\nR1(config-router)#exit",
                "Option C\n\nR1(config)#router ospf 1\nR1(config-router)#router-id 1.1.1.1\nR1(config-router)#passive-interface default\nR1(config-router)#no passive-interface FastEthernet0/0\nR1(config-router)#network 10.100.1.0 0.0.0.255 area 0\nR1(config-router)#exit\nR1(config)#interface FastEthernet0/0\nR1(config-if)#ip ospf priority 0",
                "Option D\n\nR1(config)#router ospf 1\nR1(config-router)#router-id 10.1.1.1\nR1(config-router)#network 10.100.1.0 0.0.0.255 area 0\nR1(config-router)#passive-interface FastEthernet0/0\nR1(config-router)#exit\nR1(config)#interface FastEthernet0/0\nR1(config-if)#ip ospf priority 0",
            ],
        },
        {
            "slug": "r1-static-route-10-0-3-via-transit-r3",
            "title": "CCNA — R1 static route to 10.0.3.0/24 via R3",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/r1-static-route-10-0-3-via-r3-10-0-4-3-topology.png" alt="Topology: R1 on 10.0.1.0/24 (Gig0/0) and 10.0.4.1/24 (Gig0/1); R2 on 10.0.2.0/24 and 10.0.4.2/24; R3 on 10.0.3.0/24 (Gig0/0) and 10.0.4.3/24 (Gig0/1); shared transit 10.0.4.0/24." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. Router R1 must be configured so that traffic from the 10.0.1.0/24 segment can reach networks on 10.0.3.0/24. Which command must be used to configure the route on R1?",
            "name": "r1st1003",
            "correct": "D",
            "explain": "Correct. D \u2014 On Cisco IOS the static route command is **ip route** *destination-prefix* *subnet-mask* *next-hop*. For **10.0.3.0/24** the mask is **255.255.255.0**. Traffic toward that prefix should be forwarded to **R3**\u2019s address on the shared transit **10.0.4.0/24**, **10.0.4.3**. **route add** (A and B) is a host OS convention, not Cisco IOS configuration. **C** uses **0.255.255.255**, which is **not** the /24 subnet mask (and points the route at **10.0.4.2**, which is **R2**, not the router attached to **10.0.3.0/24**).",
            "choices": [
                "route add 10.0.3.0 0.255.255.255 10.0.4.2",
                "route add 10.0.3.0 mask 255.255.255.0 10.0.4.3",
                "ip route 10.0.3.0 0.255.255.255 10.0.4.2",
                "ip route 10.0.3.0 255.255.255.0 10.0.4.3",
            ],
        },
        {
            "slug": "r1-r2-floating-static-default-wan-failover",
            "title": "CCNA — R1/R2: floating static default for WAN failover",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/r1-r2-dual-wan-client-image-server-topology.png" alt="Topology: R1 with Client A 192.168.0.0/24; R2 with Image Server 10.10.13.10/25; two parallel links between R1 and R2: primary 10.10.10.0/30 (.1 on R1, .2 on R2) and backup 10.10.10.4/30 (.5 on R1, .6 on R2)." width="900" decoding="async" loading="lazy" />
      </figure>
      <div class="exhibit-router-cli" role="region" aria-label="R1 show ip route excerpt">
        <pre>R1#show ip route
Codes: C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route

Gateway of last resort is 10.10.10.2 to network 0.0.0.0

S*    0.0.0.0/0 [1/0] via 10.10.10.2</pre>
      </div>
      <div class="exhibit-router-cli" role="region" aria-label="R2 show ip route excerpt">
        <pre>R2#show ip route
Codes: C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route

Gateway of last resort is 10.10.10.1 to network 0.0.0.0

S*    0.0.0.0/0 [1/0] via 10.10.10.1</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. Routers R1 and R2 have been configured with their respective LAN interfaces. The two circuits are operational and reachable across the WAN. Which command set establishes failover redundancy if the primary circuit goes down?",
            "name": "r1r2fltad",
            "correct": "A",
            "mono": True,
            "explain": "Correct. A \u2014 **Floating static** backup routes use the same prefix as the primary but a **higher administrative distance** so they stay **inactive** while the primary (here **AD 1** from `S* 0.0.0.0/0 [1/0]`) is valid, then **take over** if the primary disappears. **Default routes** via **10.10.10.6** (R1) and **10.10.10.5** (R2) with **AD 2** match that design.\n\n**D** installs second defaults also at **AD 1**, so they **tie** the primary instead of floating behind it. **B** and **C** add **/32 host** routes, not **default** Internet/WAN failover for all unknown destinations.",
            "choices": [
                "R1(config)#ip route 0.0.0.0 0.0.0.0 10.10.10.6 2\nR2(config)#ip route 0.0.0.0 0.0.0.0 10.10.10.5 2",
                "R1(config)#ip route 10.10.13.10 255.255.255.255 10.10.10.6\nR2(config)#ip route 192.168.0.100 255.255.255.255 10.10.10.5",
                "R1(config)#ip route 10.10.13.10 255.255.255.255 10.10.10.2\nR2(config)#ip route 192.168.0.100 255.255.255.255 10.10.10.1",
                "R1(config)#ip route 0.0.0.0 0.0.0.0 10.10.10.6\nR2(config)#ip route 0.0.0.0 0.0.0.0 10.10.10.5",
            ],
        },
        {
            "slug": "pc-a-pc-b-vlan200-switch-unicast-mac",
            "title": "CCNA — PC_A to PC_B on VLAN 200: MAC addresses after learning",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/pc-a-pc-b-vlan200-same-switch-topology.png" alt="Topology: one switch with PC_A and PC_B on access ports both in VLAN 200." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. What is expected when PC_A sends data to PC_B after their initial communication?",
            "name": "pcapcv2u",
            "correct": "A",
            "explain": "Correct. A \u2014 A Layer 2 **switch** forwards frames based on the **destination MAC** and learns **source MAC-to-port** mappings in the **CAM table**. It does **not** rewrite the **source** or **destination** Ethernet MAC addresses for normal **unicast** between two hosts on the same VLAN.\n\n**B** and **C** describe behavior that is **not** standard Ethernet switching. **D** is the **broadcast** MAC (**ffff.ffff.ffff**), which applies to broadcast or flood behavior, not to typical **known-unicast** forwarding after the switch has learned both stations.",
            "choices": [
                "The source and destination MAC addresses remain the same",
                "The switch rewrites the source and destination MAC addresses with its own",
                "The source MAC address is changed",
                "The destination MAC address is replaced with ffff.ffff.ffff",
            ],
        },
        {
            "slug": "collapsed-core-distribution-core-merged",
            "title": "CCNA — Collapsed core: which layers combine?",
            "stem": "What is the collapsed layer in collapsed core architectures?",
            "name": "colcoremg",
            "correct": "D",
            "explain": "Correct. D \u2014 **Collapsed core** (sometimes called **two-tier** campus design) **combines** the traditional **distribution** and **core** layers into **one** layer. The **access** layer stays separate, and **WAN/edge** connectivity is not what the name \"collapsed core\" refers to.\n\n**A** and **B** incorrectly mix in **WAN**. **C** would collapse **access** with **distribution**, which is not the usual definition of collapsed core.",
            "choices": [
                "core and WAN",
                "access and WAN",
                "distribution and access",
                "core and distribution",
            ],
        },
        {
            "slug": "vrrp-virtual-mac-iana-format",
            "title": "CCNA — VRRP virtual MAC address",
            "stem": "What is the MAC address used with VRRP as a virtual address?",
            "name": "vrrpvmac1",
            "correct": "B",
            "explain": "Correct. B \u2014 **VRRP (IPv4)** reserves virtual router MAC addresses in the form **00-00-5E-00-01-{VRID}** (IANA assignment per RFC 3768). Here **00-01** identifies the IPv4 VRRP block and **0a** is **VRID 10** in hexadecimal.\n\n**A** is **not** VRRP format\u2014**00-00-0C-07-** is the OUI space used for **Cisco HSRP** virtual MACs (**00-00-0C-07-AC-{group}**). **C** and **D** do not use the **00-00-5E-00-01-** VRRP prefix.",
            "choices": [
                "00-00-0C-07-AD-89",
                "00-00-5E-00-01-0a",
                "00-07-C0-70-AB-01",
                "00-C6-41-93-90-91",
            ],
        },
        {
            "slug": "wlan-24ghz-us-nonoverlapping-channels-set",
            "title": "CCNA — 2.4 GHz US non-overlapping channels",
            "stem": "Which set of 2.4 GHz nonoverlapping wireless channels is standard in the United States?",
            "name": "wlan24us1",
            "correct": "D",
            "explain": "Correct. D \u2014 In the US **2.4 GHz ISM** band, **1, 6, and 11** are the conventional **three** **20 MHz** **non-overlapping** channel centers for **802.11b/g/n** style designs (each channel number is **5 MHz** apart but the radiated bandwidth needs that spacing).\n\n**A** and **C** use **non-standard** groupings for US planning. **B** wrongly adds **channel 14**, which is **not** available for typical Wi\u2011Fi in the **United States**.",
            "choices": [
                "channels 2, 7, 9, and 11",
                "channels 1, 6, 11, and 14",
                "channels 2, 7, and 11",
                "channels 1, 6, and 11",
            ],
        },
        {
            "slug": "rapid-pvst-plus-forward-time-listen-learn",
            "title": "CCNA — Rapid-PVST+: listen/learn timer command",
            "stem": "Which command entered on a switch configured with Rapid-PVST+ listens and learns for a specific time period?",
            "name": "rpvstfw1",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 **Forward delay** is configured with **`spanning-tree vlan** *id* **forward-time** *seconds*`. It defines how long a port waits in the **listening** and **learning** states before moving to **forwarding** in classic STP timing (each state uses the configured forward-delay interval).\n\n**A** sets **max-age** (how long the switch retains spanning-tree information before discarding it). **B** sets the **hello** interval between BPDUs. **C** changes the bridge **priority** for root election, not listen/learn duration.",
            "choices": [
                "switch(config)#spanning-tree vlan 1 max-age 6",
                "switch(config)#spanning-tree vlan 1 hello-time 10",
                "switch(config)#spanning-tree vlan 1 priority 4096",
                "switch(config)#spanning-tree vlan 1 forward-time 20",
            ],
        },
        {
            "slug": "lacp-layer3-port-channel-neighbor-passive-after-static",
            "title": "CCNA — L3 port-channel down: fix LACP on neighbor",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="Local switch LACP and port-channel configuration">
        <pre>interface g2/0/0
 channel-group 1 mode active
interface g4/0/0
 channel-group 1 mode active
interface Port-channel1
 ip address 203.0.113.65 255.255.255.252

%LINEPROTO-5-UPDOWN: Line protocol on Interface Port-channel1, changed state to down</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. An engineer is configuring a Layer 3 port-channel interface with LACP. The configuration on the first device is complete, and it is verified that both interfaces have registered the neighbor device in the CDP table. Which task on the neighbor device enables the new port channel to come up without negotiating the channel?",
            "name": "lacpl3po1",
            "correct": "C",
            "explain": "Correct. C \u2014 The first switch uses **LACP** (**mode active** on the member interfaces). A neighbor configured for a **static** EtherChannel (**mode on**) cannot form a bundle with an **LACP active** peer. Changing the neighbor to **LACP passive** (**mode passive**) lets it participate in **LACP** so **Port-channel1** can form.\n\n**B** is wrong because **mode auto** is a **PAgP** setting, not **LACP**, so it does not interoperate with **mode active**. **A** is unlikely when **CDP** already lists the neighbor on both member links (those links are typically already up). **D** may be needed for Layer 3 reachability after the bundle is up, but it does not fix an **LACP/static** EtherChannel mismatch.",
            "choices": [
                "Bring up the neighboring interfaces using the no shutdown command.",
                "Change the EtherChannel mode on the neighboring interfaces to auto",
                "Modify the static EtherChannel configuration of the device to passive mode",
                "Configure the IP address of the neighboring device",
            ],
        },
        {
            "slug": "dna-center-controller-purpose-manage-deploy",
            "title": "CCNA — Cisco DNA Center controller purpose",
            "stem": "What is the purpose of the Cisco DNA Center controller?",
            "name": "dnactrlp1",
            "correct": "A",
            "explain": "Correct. A \u2014 **Cisco DNA Center** is the **controller** for Cisco\u2019s intent-based campus automation: it **discovers**, **manages**, **designs/provisions**, and **deploys** configuration and policy to supported network devices through centralized workflows (with appropriate credentials and controls).\n\n**B** may show topology/insights, but **generating a Layer 2 diagram** is not the defining purpose. **C** misstates the controller\u2019s role toward **autonomous APs** and **Layer 3 services**. **D** is **physical security**, unrelated to DNA Center.",
            "choices": [
                "to securely manage and deploy network devices",
                "to scan a network and generate a layer 2 network diagram",
                "to provide Layer 3 services to autonomous access points",
                "to secure physical access to a data center",
            ],
        },
        {
            "slug": "tftp-feature-anonymous-style-no-login",
            "title": "CCNA — TFTP: characteristic vs FTP",
            "stem": "What is a feature of TFTP?",
            "name": "tftpfeat1",
            "correct": "D",
            "explain": "Correct. D \u2014 **TFTP** is minimal: it has **no username/password authentication** step like **FTP**, so a client can transfer files when the server permits access without presenting credentials\u2014exam items often describe that as **anonymous-style** behavior (not the same as typing **anonymous** on FTP, but the idea is **no real login**).\n\n**A** is wrong: TFTP is **cleartext** and **not** a **secure** transfer protocol by itself. **B** is wrong: TFTP uses **UDP** port **69**, not **TCP** port **20** (**20** is associated with **FTP** **data** in active mode). **C** describes **FTP**\u2019s separate **control** and **data** connections, not TFTP.",
            "choices": [
                "provides secure data transfer",
                "relies on the well-known TCP port 20 to transmit data",
                "uses two separate connections for control and data traffic",
                "offers anonymous user login ability",
            ],
        },
        {
            "slug": "lightweight-ap-mode-centralized-wlc-ssid-roaming",
            "title": "CCNA — AP mode: WLC central management",
            "stem": "Which access point mode relies on a centralized controller for management, roaming, and SSID configuration?",
            "name": "lapmodw1",
            "correct": "C",
            "explain": "Correct. C \u2014 **Lightweight (split-MAC) APs** join a **WLC**; the controller centralizes **SSID/WLAN configuration**, **security policies**, **RF/profiles**, and **mobility/roaming** orchestration while the AP handles the radio and forwarding path per the architecture (CAPWAP tunnel to the WLC in typical centralized designs).\n\n**Autonomous** APs run the WLAN control stack **locally** without that controller dependency. **Repeater** and **bridge** modes describe **coverage extension** or **wireless bridging** roles, not centralized controller-based enterprise WLAN operation.",
            "choices": [
                "repeater mode",
                "bridge mode",
                "lightweight mode",
                "autonomous mode",
            ],
        },
        {
            "slug": "nat-inside-source-static-private-to-public-pc",
            "title": "CCNA — Static NAT: inside local to inside global",
            "stem": "Which command creates a static NAT binding for a PC address of 10.1.1.1 to the public routable address 209.165.200.225 assigned to the PC?",
            "name": "natstpc1",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 **`ip nat inside source static`** defines a one-to-one mapping for an **inside** host. The first address is the **inside local** (private) and the second is the **inside global** (public routable) seen on the **outside**.\n\n**A** and **C** use **`outside source static`**, which targets **outside** address translation semantics, not the usual \u201cinside PC gets a public mapping\u201d case. **B** reverses the **local**/**global** order for **`inside source static`**.",
            "choices": [
                "R1(config)#ip nat outside source static 209.165.200.225 10.1.1.1",
                "R1(config)#ip nat inside source static 209.165.200.225 10.1.1.1",
                "R1(config)#ip nat outside source static 10.1.1.1 209.165.200.225",
                "R1(config)#ip nat inside source static 10.1.1.1 209.165.200.225",
            ],
        },
        {
            "slug": "longest-match-10-1-1-19-rip-28-ospf-eigrp",
            "title": "CCNA — Longest match: 10.1.1.19",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="Routing table excerpt">
        <pre>RIP   10.1.1.16/28 [120/5] via F0/0
OSPF  10.1.1.0/24 [110/30] via F0/1
OSPF  10.1.1.0/24 [110/40] via F0/2
EIGRP 10.1.0.0/26 [90/20] via F0/3
EIGRP 10.0.0.0/8 [90/133] via F0/4</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. Packets received by the router from BGP enter via a serial interface at 209.165.201.1. Each route is present within the routing table. Which interface is used to forward traffic with a destination IP of 10.1.1.19?",
            "name": "rtelm1119",
            "correct": "A",
            "explain": "Correct. A \u2014 The router picks the **longest prefix length** that contains the destination. **10.1.1.19** falls in **10.1.1.16/28** (**10.1.1.16\u201310.1.1.31**), which is **more specific** than **10.1.1.0/24** or **10.0.0.0/8**. **10.1.0.0/26** only covers **10.1.0.0\u201310.1.0.63**, so it does **not** match **10.1.1.19**. Among duplicate **/24** OSPF paths, cost would matter, but neither wins here because **/28** outranks **/24**. **BGP** ingress interface is a distractor.",
            "choices": [
                "F0/0",
                "F0/1",
                "F0/3",
                "F0/4",
            ],
        },
        {
            "slug": "rest-http-status-classes-errors-4xx-5xx",
            "title": "CCNA — HTTP status classes: errors (choose two)",
            "stem": "Which two REST API status-code classes represent errors? (Choose two)",
            "name": "reststat1",
            "choose_two": True,
            "correct": ["D", "E"],
            "explain": "Correct. D and E \u2014 **4xx** responses indicate **client errors** (bad request, unauthorized, not found, and so on). **5xx** responses indicate **server errors** (the server failed to fulfill a valid request). **1xx** is **informational**, **2xx** **successful**, **3xx** **redirection**\u2014none of those are the error families called out in this question.",
            "choices": [
                "1XX",
                "2XX",
                "3XX",
                "4XX",
                "5XX",
            ],
        },
        {
            "slug": "ssh-next-step-crypto-key-generate-after-domain-user",
            "title": "CCNA — SSH RSA key: command after domain and user",
            "stem": "An engineer has configured the domain name, user name, and password on the local router. What is the next step to complete the configuration for a Secure Shell access RSA key?",
            "name": "sshrasnx1",
            "correct": "A",
            "mono": True,
            "explain": "Correct. A \u2014 The device needs an **RSA host key pair** for the **SSH server**. After **hostname**/**ip domain-name** and local **username** credentials, run **`crypto key generate rsa`** (optionally with a **modulus** size). **pubkey-chain** builds trusted user public keys; **import** pulls in an external PEM key instead of locally generating the usual host keys; **zeroize** deletes keys rather than completing setup.",
            "choices": [
                "crypto key generate rsa",
                "crypto key pubkey-chain rsa",
                "crypto key import rsa pem",
                "crypto key zeroize rsa",
            ],
        },
        {
            "slug": "wpa3-encryption-method-sae",
            "title": "CCNA — WPA3: SAE",
            "stem": "Which encryption method is used by WPA3?",
            "name": "wpa3enc1",
            "correct": "B",
            "explain": "Correct. B \u2014 **WPA3-Personal** uses **SAE** (**Simultaneous Authentication of Equals**, Dragonfly-based) for passphrase-based authentication, addressing offline dictionary weaknesses associated with classic **WPA2-PSK**. **TKIP** is legacy **WPA**. **PSK** describes the older pre-shared-key model, not the WPA3 mechanism named in answers. **AES** is the block cipher used inside ciphersuites such as **CCMP**/**GCMP** for frame confidentiality; this question\u2019s intended WPA3 identifier versus **TKIP/PSK** is **SAE**.",
            "choices": [
                "TKIP",
                "SAE",
                "PSK",
                "AES",
            ],
        },
        {
            "slug": "ssh-interface-acl-inbound-10-139-58-28",
            "title": "CCNA — SSH from /28: inbound interface extended ACL",
            "stem": "An engineer is configuring remote access to a router from IP subnet 10.139.58.0/28. The domain name, crypto keys, and SSH have been configured. Which configuration enables the traffic on the destination router?",
            "name": "sshifa1139",
            "correct": "C",
            "mono": True,
            "explain": "Correct. C \u2014 **SSH** uses **TCP** port **22**. A **/28** needs a wildcard of **0.0.0.15** (16 addresses in the fourth octet). **Extended** ACL **110** can match **tcp** with source **10.139.58.0 0.0.0.15** and destination **host 10.122.49.1 eq 22**, and **`ip access-group 110 in`** applies it to **inbound** traffic on the **interface** facing the clients.\n\n**A** uses **UDP** and **0.0.0.7** (only eight values), not a full **/28**. **B** uses **`ip access-list standard`** with **105**, but **105** sits in the **extended** ACL number range and **standard** ACLs cannot express **TCP**/**eq**/**destination** anyway. **D** omits **`ip`** before **`access-group`** and supplies **255.255.255.248** where an ACL needs a **wildcard** (for **/28** use **0.0.0.15**, not a subnet mask).",
            "choices": [
                "interface FastEthernet0/0\nip address 10.122.49.1 255.255.255.248\nip access-group 10 in\n\nip access-list standard 10\npermit udp 10.139.58.0 0.0.0.7 host 10.122.49.1 eq 22",
                "interface FastEthernet0/0\nip address 10.122.49.1 255.255.255.252\nip access-group 105 in\n\nip access-list standard 105\npermit tcp 10.139.58.0 0.0.0.7 eq 22 host 10.122.49.1",
                "interface FastEthernet0/0\nip address 10.122.49.1 255.255.255.252\nip access-group 110 in\n\nip access-list extended 110\npermit tcp 10.139.58.0 0.0.0.15 host 10.122.49.1 eq 22",
                "interface FastEthernet0/0\nip address 10.122.49.1 255.255.255.240\naccess-group 120 in\n\nip access-list extended 120\npermit tcp 10.139.58.0 255.255.255.248 any eq 22",
            ],
        },
        {
            "slug": "spine-leaf-predictable-latency-uniform-path",
            "title": "CCNA — Spine-leaf: path and latency",
            "stem": "What is a function of spine-and-leaf architecture?",
            "name": "spineft1",
            "correct": "C",
            "explain": "Correct. C \u2014 **Spine\u2013leaf** gives **any-to-any** connectivity through a **fixed** pattern (**leaf \u2194 spine \u2194 leaf** for east\u2013west traffic), so **hop count** stays **consistent** and **latency** stays **predictable** compared with ad-hoc aggregation designs.\n\n**A** misstates oversubscription control\u2014adding **leaves** mainly scales **downlink** access; **uplink/spine** bandwidth and link counts address fan\u2011out limits. **B** is unrelated to spine\u2013leaf\u2019s role. **D** is wrong\u2014**end systems attach to leaf** switches, the fabric is not **multicast-only**, and **spine** links **leaves**, not general \u201cdirect server\u201d attachment in the usual model.",
            "choices": [
                "mitigates oversubscription by adding a layer of leaf switches",
                "limits payload size of traffic within the leaf layer",
                "offers predictable latency of the traffic path between end devices",
                "exclusively sends multicast traffic between servers that are directly connected to the spine",
            ],
        },
        {
            "slug": "dna-center-traditional-campus-centralized-management",
            "title": "CCNA — DNA Center vs traditional campus management",
            "stem": "What differentiates device management enabled by Cisco DNA Center from traditional campus device management?",
            "name": "dnatrad1",
            "correct": "B",
            "explain": "Correct. B \u2014 **Cisco DNA Center** delivers **centralized**, controller-based lifecycle operations (inventory, design/provisioning workflows, policy, assurance) from one platform rather than treating each box as a standalone management island.\n\n**A**, **C**, and **D** better describe **traditional** day\u2011to\u2011day work\u2014heavy **CLI**, **per\u2011device** changes, and **manual**, **device\u2011by\u2011device** touch\u2014that DNA Center is meant to streamline.",
            "choices": [
                "CLI-oriented device",
                "centralized",
                "per-device",
                "device-by-device hands-on",
            ],
        },
        {
            "slug": "zero-day-exploit-vulnerability-no-patch",
            "title": "CCNA — Zero-day exploit definition",
            "stem": "What is a zero-day exploit?",
            "name": "zeroday1",
            "correct": "B",
            "explain": "Correct. B \u2014 A **zero-day** (or **0-day**) vulnerability is one that is **actively unknown** to the vendor or **has no generally available fix/patch** at the time attackers weaponize it\u2014so defenders have \u201czero days\u201d of prepared remediation.\n\n**A** describes **SQL injection** against a database application, not the zero-day concept. **C** describes a **man-in-the-middle** attack. **D** describes **DoS/DDoS** saturation of bandwidth or resources.",
            "choices": [
                "It is when an attacker inserts malicious code into a SQL server.",
                "It is when a new network vulnerability is discovered before a fix is available.",
                "It is when the perpetrator inserts itself in a conversation between two parties and captures or alters data.",
                "It is when the network is saturated with malicious traffic that overloads resources and bandwidth.",
            ],
        },
        {
            "slug": "aaa-console-local-username-line-con-zero",
            "title": "CCNA — Console: local username after RADIUS issue",
            "stem": "After a recent security breach and a RADIUS failure, an engineer must secure the console port of each enterprise router with a local username and password. Which configuration must the engineer apply to accomplish this task?",
            "name": "aaconl1",
            "correct": "B",
            "mono": True,
            "explain": "Correct. B \u2014 The engineer must define a **local user** (**`username ... secret`**) and apply **AAA-style login** on **`line con 0`** so the **console** checks those credentials. **`privilege level 15`** sets the default **exec** privilege on that line.\n\n**A** turns on **AAA** but points **`aaa authentication login default`** at **RADIUS** only (no **local** fallback shown) and never configures **`line con 0`**, so it does not deliver **console** protection with **local** credentials as requested. **C** uses **`no login local`**, which works against local console login. **D** sets only a **console line password** and never creates the required **`username`** entry.",
            "choices": [
                """Option A

aaa new-model
aaa authorization exec default local
aaa authentication login default radius
username localuser privilege 15 secret plaintextpassword""",
                """Option B

username localuser secret plaintextpassword
line con 0
login authentication default
privilege level 15""",
                """Option C

username localuser secret plaintextpassword
line con 0
no login local
privilege level 15""",
                """Option D

aaa new-model
line con 0
password plaintextpassword
privilege level 15""",
            ],
        },
        {
            "slug": "snmp-v3-implied-by-snmp-server-user",
            "title": "CCNA — SNMPv3: snmp-server user",
            "stem": "Which command implies the use of SNMPv3?",
            "name": "snmpv3u1",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 **SNMPv3** introduces **USM** users with **authentication** and optional **privacy**; on Cisco IOS you define them with **`snmp-server user`**. **Community-based** access is **SNMPv1/v2c** (**snmp-server community**). **`snmp-server host`** and **`snmp-server enable traps`** can be used with multiple SNMP versions depending on the rest of the configuration, so they do not inherently imply **v3** the way **`snmp-server user`** does.",
            "choices": [
                "snmp-server community",
                "snmp-server host",
                "snmp-server enable traps",
                "snmp-server user",
            ],
        },
        {
            "slug": "switch-unknown-destination-mac-flood-except-ingress",
            "title": "CCNA — Unknown destination MAC: flooding",
            "stem": "When a switch receives a frame for an unknown destination MAC address, how is the frame handled?",
            "name": "swunkdm1",
            "correct": "B",
            "explain": "Correct. B \u2014 If the **destination MAC** is **not** in the **CAM/MAC table** (**unknown unicast**), the switch **floods** a copy out **every port in that VLAN** except the **ingress** (reception) port so the unknown host can receive it and the switch can **learn** its MAC from any reply.\n\n**A** is imprecise: the frame is usually still an **unknown unicast** Ethernet frame, not converted to a **Layer 2 broadcast** (**ffff.ffff.ffff**). **C** and **D** are not standard switching behavior for unknown destinations.",
            "choices": [
                "broadcast to all ports on the switch",
                "flooded to all ports except the origination port",
                "forwarded to the first available port",
                "inspected and dropped by the switch",
            ],
        },
        {
            "slug": "port-security-trunk-default-violation-errdisable",
            "title": "CCNA — Port security on trunk: default violation",
            "stem": "What is the default port-security behavior on a trunk link?",
            "name": "portsect1",
            "correct": "C",
            "explain": "Correct. C \u2014 Default port security allows **one** secure **MAC** (**`switchport port-security maximum`** defaults to **1**). The default violation mode is **`shutdown`**, so if the port **learns a second** address (a violation), the port is turned off and goes **err-disabled** until cleared.\n\n**A** is not how violations work. **B** is unrelated to native VLAN handling. **D** invents a **10**-MAC **static** rule\u2014defaults are **not** **10** addresses.",
            "choices": [
                "It causes a network loop when a violation occurs.",
                "It disables the native VLAN configuration as soon as port security is enabled.",
                "It places the port in the err-disabled state if it learns more than one MAC address.",
                "It places the port in the err-disabled state after 10 MAC addresses are statically configured.",
            ],
        },
        {
            "slug": "multifactor-authentication-examples-choose-two",
            "title": "CCNA — Multifactor authentication examples (choose two)",
            "stem": "What are two examples of multifactor authentication? (Choose two)",
            "name": "mfaex1",
            "choose_two": True,
            "correct": ["B", "D"],
            "explain": "Correct. B and D \u2014 **MFA** combines **different factor classes**. **Unique user knowledge** (password/PIN) is **something you know**; **soft tokens** (software OTP generators) are **something you have**. Pairing those exemplifies multifactor design.\n\n**SSO** streamlines **access to many apps** but is **not** itself an authentication **factor**. **Password expiration** tightens **password policy** yet stays within the **knowledge** factor. **Shared password responsibility** is **not** an MFA pattern and weakens accountability.",
            "choices": [
                "single sign-on",
                "unique user knowledge",
                "passwords that expire",
                "soft tokens",
                "shared password responsibility",
            ],
        },
        {
            "slug": "show-ip-route-10-10-13-160-slash-29-subnet-mask",
            "title": "CCNA — Mask for 10.10.13.160/29 from routing table",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="Router1 show ip route excerpt">
        <pre>Router1#show ip route

Gateway of last resort is 10.10.11.2 to network 0.0.0.0

      10.0.0.0/8 is variably subnetted, 8 subnets, 4 masks
C        10.10.10.0/28 is directly connected, GigabitEthernet0/0
C        10.10.11.0/30 is directly connected, FastEthernet2/0
C        10.10.12.0/30 is directly connected, GigabitEthernet0/1
O        10.10.13.0/25 [110/2] via 10.10.10.1, 00:00:04, GigabitEthernet0/0
O        10.10.13.128/28 [110/2] via 10.10.10.1, 00:00:04, GigabitEthernet0/0
O        10.10.13.144/28 [110/2] via 10.10.10.1, 00:00:04, GigabitEthernet0/0
O        10.10.13.160/29 [110/2] via 10.10.10.1, 00:00:04, GigabitEthernet0/0
O        10.10.13.208/29 [110/2] via 10.10.10.1, 00:00:04, GigabitEthernet0/0
S*       0.0.0.0/0 [1/0] via 10.10.11.2</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. What is the subnet mask of the route to the 10.10.13.160 prefix?",
            "name": "rt13160m",
            "correct": "D",
            "explain": "Correct. D \u2014 The route is printed as **10.10.13.160/29**. A **/29** prefix uses **29** network bits, which maps to dotted-decimal mask **255.255.255.248** (last octet **11111000**).\n\n**A** is **/28** (**240**). **B** is **/25** (**128**). **C** is not a mask that matches **/29**.",
            "choices": [
                "255.255.255.240",
                "255.255.255.128",
                "255.255.248.0",
                "255.255.255.248",
            ],
        },
        {
            "slug": "endpoint-function-user-access-network-services",
            "title": "CCNA — Endpoint: user access to services",
            "stem": "What is a function of an endpoint?",
            "name": "endptusr1",
            "correct": "B",
            "explain": "Correct. B \u2014 **Endpoints** are **end systems**\u2014workstations, phones, tablets, servers, and similar devices that **users or applications use directly** to **reach** **network services**. Infrastructure devices **relay** traffic (**A**, **D**) or **enforce trust boundaries** (**C**), which is not the defining role of an **endpoint** in this question.",
            "choices": [
                "It passes unicast communication between hosts in a network",
                "It is used directly by an individual user to access network services",
                "It provides security between trusted and untrusted sections of the network",
                "It transmits broadcast traffic between devices in the same VLAN",
            ],
        },
        {
            "slug": "dhcp-relay-agent-features-choose-two",
            "title": "CCNA — DHCP relay agent features (choose two)",
            "stem": "What are two features of the DHCP relay agent? (Choose two)",
            "name": "dhcprel1",
            "choose_two": True,
            "correct": ["A", "C"],
            "explain": "Correct. A and C \u2014 **DHCP relay** (**`ip helper-address`**) lets clients on remote subnets reach **centralized DHCP servers**, so you need **fewer** servers scattered on every LAN. You configure **`ip helper-address`** on the **router (or L3 switch) routed interface/SVI** that is the **default gateway for the client subnet**\u2014where **DHCPDISCOVER** broadcasts are received.\n\n**B** is wrong: the relay **forwards DHCP messages**; it does not \u201cassign DNS locally\u201d before talking to the server (**DNS** is normally **Option 6** in the server\u2019s reply). **D** misstates how **giaddr** / **subnet** selection works. **E** is false: you can configure **multiple** **`ip helper-address`** lines on the **same** L3 interface for **redundancy** or several targets.",
            "choices": [
                "minimizes the necessary number of DHCP servers",
                "assigns DNS locally and then forwards request to DHCP server",
                "is configured under the Layer 3 interface of a router on the client subnet",
                "allows only MAC-to-IP reservations to determine the local subnet of a client",
                "permits one IP helper command under an individual Layer 3 interface",
            ],
        },
        {
            "slug": "cloud-rapid-elasticity-capacity-demand",
            "title": "CCNA — Cloud: rapid elasticity",
            "stem": "In a cloud-computing environment, what is rapid elasticity?",
            "name": "cloudel1",
            "correct": "A",
            "explain": "Correct. A \u2014 **Rapid elasticity** is the ability to **provision and release capacity quickly**\u2014often **automatically**\u2014so resources **expand and contract** with **workload** demand. Tenants typically experience this as **seemingly unlimited** capacity on short notice.\n\n**B** aligns more with **metering/chargeback** visibility. **C** describes **resource pooling** across tenants. **D** matches **on-demand self-service** provisioning, not elasticity itself.",
            "choices": [
                "automatic adjustment of capacity based on need",
                "control and monitoring of resource consumption by the tenant",
                "pooling resources in a multitenant model based on need",
                "self-service of computing resources by the tenant",
            ],
        },
        {
            "slug": "flexconnect-local-switch-different-vlans-trunk-port",
            "title": "CCNA — FlexConnect: AP vs client VLANs",
            "stem": "What must be considered for a locally switched FlexConnect AP if the VLANs that are used by the AP and client access are different?",
            "name": "flexlcs1",
            "correct": "C",
            "explain": "Correct. C \u2014 With **local switching**, client traffic exits the AP on **wired VLANs** that can differ from **AP/management** addressing. The **switch port** toward the AP must carry **multiple 802.1Q VLANs**, typically **`switchport mode trunk`**. **A** (\u201cLAG\u201d) adds bandwidth or redundancy but is not required for VLAN separation. **B** (native VLAN = management) is a common design detail on a trunk but is not the primary \u201cmust\u201d this item targets. **D** is wrong: **802.1Q** must be **enabled**, not disabled.",
            "choices": [
                "The APs must be connected to the switch with multiple links in LAG mode.",
                "The native VLAN must match the management VLAN of the AP.",
                "The switch port mode must be set to trunk.",
                "IEEE 802.1Q trunking must be disabled on the switch port.",
            ],
        },
        {
            "slug": "wlc-config-serial-timeout-no-auto-logout",
            "title": "CCNA — WLC: serial session no timeout",
            "stem": "Which command configures the Cisco WLC to prevent a serial session with the WLC CLI from being automatically logged out?",
            "name": "wlcsert1",
            "correct": "C",
            "explain": "Correct. C \u2014 On AireOS-style WLC CLI, **`config serial timeout`** sets the **serial console** inactivity logout (minutes). Setting it to **0** means **serial sessions never time out** (per Cisco Wireless Controller configuration guides). **`config serial baudrate`** changes speed (for example 9600), not logout. **`config sessions`** controls **Telnet/SSH** session limits and timeouts, not the **serial** port.",
            "choices": [
                "config sessions maxsessions 0",
                "config serial timeout 9600",
                "config serial timeout 0",
                "config sessions timeout 0",
            ],
        },
        {
            "slug": "mac-address-learning-enabled-default-vlans",
            "title": "CCNA — MAC learning: default behavior",
            "stem": "What is a function of MAC address learning?",
            "name": "maclearn1",
            "correct": "C",
            "explain": "Correct. C \u2014 On Cisco switches, **MAC address learning** is **enabled by default** on **VLANs** and **interfaces** so the switch can build the **MAC address table** (source MAC to ingress port). **A** is false: learning is **not** disabled by default on **trunks**. **B** is not the primary role of learning on a **management VLAN**. **D** is wrong: learning **reduces** unnecessary flooding for **known** unicast destinations; **unknown** unicast is what gets flooded.",
            "choices": [
                "It is disabled by default on all interfaces connected to trunks",
                "It increases security on the management VLAN",
                "It is enabled by default on all VLANs and interfaces",
                "It increases the potential for MAC address flooding",
            ],
        },
        {
            "slug": "flexconnect-branch-local-switching-wan-survivability",
            "title": "CCNA — FlexConnect branch WAN survivability",
            "stem": "A Cisco engineer at a new branch office is configuring a wireless network with access points that connect to a controller that is based at corporate headquarters. Wireless client traffic must terminate at the branch office and access-point survivability is required in the event of a WAN outage. Which access point mode must be selected?",
            "name": "flexbr1",
            "correct": "D",
            "explain": "Correct. D \u2014 **FlexConnect** with **local switching enabled** lets **branch** APs **switch client data locally** on the branch LAN while still managed from a **central WLC**. If the **WAN** to HQ fails, FlexConnect APs can continue **wireless service** using **cached** policies/credentials (**AP survivability**). **A** (lightweight, local switching **disabled**) centralizes data at the WLC\u2014traffic does not terminate at the branch. **B** is not the standard branch+central-WLC design for this requirement. **C** (**OfficeExtend**) targets **remote/home** extension, not a **branch office** with local terminate and WAN outage survival.",
            "choices": [
                "Lightweight with local switching disabled",
                "Local with AP fallback enabled",
                "OfficeExtend with high availability disabled",
                "FlexConnect with local switching enabled",
            ],
        },
        {
            "slug": "poe-auto-mode-detects-powered-device",
            "title": "CCNA — PoE auto vs static",
            "stem": "What is an advantage of using auto mode versus static mode for power allocation when an access point is connected to a PoE switch port?",
            "name": "poeauto1",
            "correct": "B",
            "explain": "Correct. B \u2014 In **auto** mode, the switch runs **IEEE PoE detection/classification** to verify a **powered device (PD)** is present and allocate power based on what the PD requests. **Static** mode applies a **fixed** wattage you configure (useful to **reserve/guarantee** budget) but does not rely on automatic PD discovery the same way. **A** describes a fixed default level, not an **auto** advantage. **C** (all four pairs) relates to **PoE+** / 4-pair delivery, not **auto vs static**. **D** (**power policing**) is a separate configuration, not what **auto** uniquely provides.",
            "choices": [
                "The default level is used for the access point",
                "It detects the device is a powered device",
                "All four pairs of the cable are used",
                "Power policing is enabled at the same time",
            ],
        },
        {
            "slug": "cpe-floating-static-default-when-ebgp-invalid",
            "title": "CCNA — CPE floating static default vs eBGP",
            "stem": "Refer to the exhibit. After configuring a new static route on the CPE, the engineer entered this series of commands to verify that the new configuration is operating normally. When is the static default route installed into the routing table?",
            "name": "cpeflt1",
            "correct": "A",
            "explain": "Correct. A \u2014 The routing table shows an active **eBGP default**: **`B* 0.0.0.0/0 [20/0] via 198.51.100.1`**. A **floating static default** uses a **higher administrative distance** than **20**, so it stays **out of the table** while the **BGP** default is valid and is **installed only when that BGP default is withdrawn** (invalid/unreachable). **B** applies only if you tied the static to **object tracking** of **203.0.113.1** reachability, not the basic **AD-based** floating backup shown here. **C** is wrong: a **next-hop change** on the BGP route does not by itself install the backup if BGP still advertises a valid default. **D** is wrong: learning **203.0.113.1** via BGP would not be the trigger to install a **static** default backup.",
            "choices": [
                "when the default route learned over external BGP becomes invalid",
                "when 203.0.113.1 is no longer reachable as a next hop",
                "when the default route learned over external BGP changes its next hop",
                "when a route to 203.0.113.1 is learned via BGP",
            ],
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="CPE verification output">
        <pre>--Some output missing--
Routing Descriptor Blocks:
* directly connected, via Ethernet0/1
    Route metric is 0, traffic share count is 1

CPE# ping 203.0.113.1
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 203.0.113.1, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 1/1/1 ms

CPE# show ip route
Gateway of last resort is 198.51.100.1 to network 0.0.0.0
B*  0.0.0.0/0 [20/0] via 198.51.100.1, 00:02:07
    198.51.100.0/24 is variably subnetted, 2 subnets, 2 masks
C       198.51.100.0/30 is directly connected, Ethernet0/0
L       198.51.100.2/32 is directly connected, Ethernet0/0
    203.0.113.0/24 is variably subnetted, 2 subnets, 2 masks
C       203.0.113.0/30 is directly connected, Ethernet0/1
L       203.0.113.2/32 is directly connected, Ethernet0/1</pre>
    </div>""",
        },
        {
            "slug": "telnet-unsecured-remote-cli-access",
            "title": "CCNA — Unsecured remote CLI access",
            "stem": "Which remote access protocol provides unsecured remote CLI access?",
            "name": "telunsec1",
            "correct": "A",
            "explain": "Correct. A \u2014 **Telnet** provides **remote CLI** over TCP port **23** but sends usernames, passwords, and session data in **cleartext** (unsecured). **SSH** encrypts the session and is the secure alternative. **Console** is typically **local** physical access on the device, not a **remote** network protocol. **Bash** is a **shell**, not a Cisco IOS remote-access protocol.",
            "choices": [
                "Telnet",
                "SSH",
                "console",
                "Bash",
            ],
        },
        {
            "slug": "wlc-functions-vs-autonomous-ap-choose-two",
            "title": "CCNA — WLC vs autonomous AP (choose two)",
            "stem": "Which two functions does a WLC perform in the lightweight access-point architecture that an AP performs independently in an autonomous architecture? (Choose two)",
            "name": "wlclap1",
            "choose_two": True,
            "correct": ["A", "D"],
            "explain": "Correct. A and D \u2014 In **lightweight (split-MAC)** mode, the **WLC** centralizes **control-plane** tasks: **client association, authentication, and roaming**, plus **RF management** (**channels** and **transmit power** via **RRM**). In **autonomous** mode, each **AP** performs those functions **locally**.\n\n**B** is misleading: **WPA/WPA2/WPA3** security is handled in the wireless data path (often at the AP); the WLC coordinates policy but does not replace the AP\u2019s role for on-air encryption in the way this option suggests. **C** (**collision avoidance**) is **802.11 MAC** behavior at the **AP/client**, not a WLC-only function. **E** (**beacons**) are still **sent and processed by APs** in lightweight mode; the WLC configures WLANs but does not originate beacons on behalf of APs.",
            "choices": [
                "handling the association, authentication, and roaming of wireless clients",
                "encrypting and decrypting traffic that uses the WAP protocol family",
                "preventing collisions between wireless clients on the same RF channel",
                "managing RF channels, including transmission power",
                "sending and processing beacon frames",
            ],
        },
        {
            "slug": "ospf-gi0-0-point-to-point-desired-full-dash",
            "title": "CCNA — OSPF: FULL/DR to FULL/- on Gi0/0",
            "stem": "How must OSPF be configured on the GigabitEthernet0/0 interface of the neighbor device to achieve the desired neighbor relationship?",
            "name": "ospfp2p1",
            "correct": "C",
            "mono": True,
            "explain": "Correct. C \u2014 **Current** output shows **FULL/DR** with **priority 1** on a **broadcast** Ethernet segment (default on GigabitEthernet). **Desired** output shows **FULL/-** (no **DR/BDR** role) with **priority 0** displayed. **`ip ospf network point-to-point`** changes the OSPF network type so **DR/BDR election does not occur** and the neighbor state becomes **FULL/-**. **A** (**cost**) does not remove DR behavior. **B** only assigns an **area** and does not change network type. **D** (**priority 1**) keeps the router eligible for **DR** election; it does not produce **FULL/-**.",
            "choices": [
                "Router(config)#interface GigabitEthernet 0/0\nRouter(config-if)#ip ospf cost 5",
                "Router(config)#interface GigabitEthernet 0/0\nRouter(config-if)#ip ospf 1 area 2",
                "Router(config)#interface GigabitEthernet 0/0\nRouter(config-if)#ip ospf network point-to-point",
                "Router(config)#interface GigabitEthernet 0/0\nRouter(config-if)#ip ospf priority 1",
            ],
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="OSPF neighbor current and desired">
        <pre>Current Neighbor Relationship

Neighbor ID   Pri   State       Dead Time    Address       Interface
192.168.1.1   1     FULL/DR     00:00:33     192.168.1.1   GigabitEthernet0/0

Desired Neighbor Relationship

Neighbor ID   Pri   State       Dead Time    Address       Interface
192.168.1.1   0     FULL/ -     00:00:31     192.168.1.1   GigabitEthernet0/0</pre>
    </div>""",
        },
        {
            "slug": "sw1-fa01-notconnect-wrong-cable-type",
            "title": "CCNA — SW1 Fa0/1 notconnect cause",
            "stem": "What is the cause of the issue?",
            "name": "swnotc1",
            "correct": "D",
            "explain": "Correct. D \u2014 **`notconnect`** in **`show interfaces status`** means the switch does **not** detect a valid **Layer 1** link (no carrier), which matches **`down`/`down`** in **`show ip interface brief`**. A **wrong or bad cable** (or nothing connected on the far end) is a typical physical cause. **`shutdown`** shows **`disabled`**, not **`notconnect`**. **Port security** violations usually put the port in **`err-disabled`**. **STP** does not remove physical link; a blocked port is normally still **`connected`**.",
            "choices": [
                "STP",
                "shutdown command",
                "port security",
                "wrong cable type",
            ],
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="SW1 interface status">
        <pre>SW1#show ip interface brief
Interface        IP-Address   OK? Method Status Protocol
FastEthernet0/1  unassigned   YES manual down   down

SW1#show interface fa0/1 status
Port     Name  Status      Vlan   Duplex   Speed  Type
Fa0/1          notconnect  1      a-full   a-100  10/100BaseTX</pre>
    </div>""",
        },
        {
            "slug": "ssh-transport-rsa-modulus-2048-choose-two",
            "title": "CCNA — SSH: transport and 2048-bit RSA (choose two)",
            "stem": "A network engineer is replacing the switches that belong to a managed-services client with new Cisco Catalyst switches. The new switches will be configured for updated security standards, including replacing Telnet services with encrypted connections and doubling the modulus size from 1024. Which two commands must the engineer configure on the new switches? (Choose two)",
            "name": "ssh20481",
            "choose_two": True,
            "correct": ["A", "E"],
            "mono": True,
            "explain": "Correct. A and E \u2014 **`transport input ssh`** on **VTY** lines limits remote management to **encrypted SSH** instead of **cleartext Telnet**. **`crypto key generate rsa modulus 2048`** creates **RSA** host keys at **2048** bits (**double** the old **1024** modulus). **`transport input all`** (B) still permits **Telnet**. **`modulus 1024`** (C) keeps the **old** key size. **`usage-keys`** (D) is a different key-generation style and is not the pair with **SSH-only VTY** transport in this item.",
            "choices": [
                "transport input ssh",
                "transport input all",
                "crypto key generate rsa general-keys modulus 1024",
                "crypto key generate rsa usage-keys",
                "crypto key generate rsa modulus 2048",
            ],
        },
        {
            "slug": "longest-match-192-168-2-2-static-routes",
            "title": "CCNA — Longest match to 192.168.2.2",
            "stem": "An engineer is checking the routing table in the main router to identify the path to a server on the network. Which route does the router use to reach the server at 192.168.2.2?",
            "name": "lm19222",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 The router uses **longest-prefix match**. **192.168.2.2** matches **192.168.0.0/20**, **192.168.2.0/28**, and **192.168.2.0/29**; **/29** is the **most specific**, so **`S 192.168.2.0/29 via 10.1.1.1`** wins. **A** is the same next hop but a **shorter** prefix (/28). **B** (**192.168.1.0/30**) does not contain **192.168.2.2**. **C** (**/20**) is the **least specific** match.",
            "choices": [
                "S 192.168.2.0/28 [1/0] via 10.1.1.1",
                "S 192.168.1.0/30 [1/0] via 10.1.1.1",
                "S 192.168.0.0/20 [1/0] via 10.1.1.1",
                "S 192.168.2.0/29 [1/0] via 10.1.1.1",
            ],
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="Main router show ip route">
        <pre>Gateway of last resort is not set
    10.0.0.0/8 is variably subnetted, 2 subnets, 2 masks
C       10.1.1.0/30 is directly connected, GigabitEthernet0/0
L       10.1.1.2/32 is directly connected, GigabitEthernet0/0
S       192.168.0.0/20 [1/0] via 10.1.1.1
    192.168.1.0/30 is subnetted, 1 subnets
S       192.168.1.0/30 [1/0] via 10.1.1.1
    192.168.2.0/24 is variably subnetted, 2 subnets, 2 masks
S       192.168.2.0/28 [1/0] via 10.1.1.1
S       192.168.2.0/29 [1/0] via 10.1.1.1</pre>
    </div>""",
        },
        {
            "slug": "json-mycar-wheels-warning-in-array",
            "title": "CCNA — JSON: warning in wheels array",
            "stem": "In which structure does the word \u201cwarning\u201d directly reside?",
            "name": "jsonwarn1",
            "correct": "A",
            "mono": True,
            "explain": "Correct. A \u2014 Under **myCar**, the **wheels** property is a **JSON array**: `[\"good\", \"good\", \"pressureLow\", \"warning\"]`. The token **\"warning\"** is a **string value** that sits **directly** as an **array element**, not as an object key or a Boolean. The outer `{ ... }` is an **object**, but **\"warning\"** is one level inside the **array** container.",
            "choices": [
                "array",
                "object",
                "Boolean",
                "string",
            ],
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="JSON car inventory">
        <pre>{
   "myCar": {
            "name": "thunder",
            "wheels": ["good", "good", "pressureLow", "warning"],
            "gasLight": false
            },
   "oldCar": {
             "name": "sleepy",
             "wheels": ["pressureLow", "pressureLow", "pressureLow", "pressureLow"],
             "color": "rust",
             "gasLight": true
             },
   "newCar": {
             "name": "lightning",
             "wheels": ["pressureLow", "good", "pressureLow", "good"],
             "color": "blue",
             "gasLight": true
             }
}</pre>
    </div>""",
        },
        {
            "slug": "wlan-office-ssid-same-security-policies-branches",
            "title": "CCNA — Office SSID: same access at branches",
            "stem": "A network administrator plans an update to the Wi-Fi networks in multiple branch offices. Each location is configured with an SSID called \u201cOffice\u201d. The administrator wants every user who connects to the SSID at any location to have the same access level. What must be set the same on each network to meet the requirement?",
            "name": "wlanoff1",
            "correct": "B",
            "explain": "Correct. B \u2014 Matching **SSID** names alone do not guarantee the same user experience. **Security policies** (authentication method, encryption, VLAN/ACL assignment, and related WLAN security settings) must be **consistent** on each site so every **Office** client receives the **same access level** regardless of branch. **Radio policy** governs band/RF behavior, not authorization. **NAS-ID** often helps RADIUS identify **where** a client attached and can drive **location-specific** rules, not uniform access. **Profile name** is an administrative label; access is defined by the **policy contents**, not the name.",
            "choices": [
                "radio policy",
                "security policies",
                "NAS-ID configuration",
                "profile name",
            ],
        },
        {
            "slug": "dna-center-single-pane-faster-deployment",
            "title": "CCNA — DNA Center: faster campus deployment",
            "stem": "A network architect is considering whether to implement Cisco DNA Center to deploy devices on a new network. The organization is focused on reducing the time it currently takes to deploy devices in a traditional campus design. For which reason would Cisco DNA Center be more appropriate than traditional management options?",
            "name": "dnadepl1",
            "correct": "B",
            "explain": "Correct. B \u2014 **Cisco DNA Center** centralizes **design, provisioning, and deployment** in one GUI (**single pane of glass**), which reduces the **per-device CLI** and scattered-tool work typical of **traditional** campus rollouts. **A** overstates **third-party** **zero-touch** support as the main benefit. **C** (**syslog** volume) is unrelated to **deployment time**. **D** (**third-party AP analytics**) is not why teams adopt DNA Center to **deploy** devices faster.",
            "choices": [
                "Cisco DNA Center provides zero-touch provisioning to third-party devices.",
                "Cisco DNA Center supports deployment with a single pane of glass.",
                "Cisco DNA Center minimizes the level of syslog output when reporting on Cisco devices.",
                "Cisco DNA Center reduces the need for analytics on third-party access points and devices.",
            ],
        },
        {
            "slug": "tcp-udp-query-response-connection-model",
            "title": "CCNA — TCP/UDP query-response model",
            "stem": "How do TCP and UDP fit into a query-response model?",
            "name": "tcpqr1",
            "correct": "C",
            "explain": "Correct. C \u2014 **TCP** is **connection-oriented**: it runs a **three-way handshake** before application data, then uses **sequencing** and **acknowledgments** suited to reliable **query\u2013response** exchanges. **UDP** is **connectionless** and sends **immediately** without setup (best-effort delivery). **A** reverses roles (**TCP** uses sequencing/ACKs). **B** misstates error handling (**TCP** recovers; **UDP** does not at the transport layer). **D** is wrong: **TCP** preserves **order**; **UDP** does not guarantee ordered delivery.",
            "choices": [
                "TCP avoids using sequencing, and UDP avoids using acknowledgments.",
                "TCP uses error detection for packets, and UDP uses error recovery.",
                "TCP establishes a connection prior to sending data, and UDP sends immediately.",
                "TCP encourages out-of-order packet delivery, and UDP prevents re-ordering.",
            ],
        },
        {
            "slug": "serial0-ip-access-list-in-syntax-fails-apply",
            "title": "CCNA — ACL: ip access-list vs access-group",
            "stem": "A network administrator must permit traffic from the 10.10.0.0/24 subnet to the WAN on interface Serial0. What is the effect of the configuration as the administrator applies the command?",
            "name": "aclser1",
            "correct": "C",
            "mono": True,
            "explain": "Correct. C \u2014 Under **interface Serial0**, the valid command to attach ACL **10** inbound is **`ip access-group 10 in`**. **`ip access-list 10 in`** is **invalid** interface syntax ( **`access-list`** is defined in **global** configuration), so IOS **rejects** the line and the ACL is **not applied** to **Serial0**. **A** describes what ACL **10** would permit **if** bound (**10.0.0.0\u201310.0.0.255**), not **10.10.0.0/24**, and it is not applied here. **B** is wrong because the **`access-list 10 permit`** line is valid. **D** misreads the **wildcard** mask.",
            "choices": [
                "The sourced traffic from IP range 10.0.0.0 \u2013 10.0.0.255 is allowed on Serial0.",
                "The permit command fails and returns an error code.",
                "The router fails to apply the access list to the interface.",
                "The router accepts all incoming traffic to Serial0 with the last octet of the source IP set to 0.",
            ],
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="ACL configuration snippet">
        <pre>access-list 10 permit 10.0.0.0 0.0.0.255
interface Serial0
 ip access-list 10 in</pre>
    </div>""",
        },
        {
            "slug": "show-ip-route-10-10-8-14-slash-28-mask",
            "title": "CCNA — Destination mask for 10.10.8.14",
            "stem": "A packet sourced from 10.10.10.1 is destined for 10.10.8.14. What is the subnet mask of the destination route?",
            "name": "rtmask1",
            "correct": "B",
            "explain": "Correct. B \u2014 **10.10.8.14** matches the **connected** route **10.10.8.0/28** (hosts **.0\u2013.15**). A **/28** mask is **255.255.255.240**. It does **not** match **10.10.10.0/24** (**/24** = **255.255.255.0**). **A** (**255.255.254.0**) is **/23**. **C** (**255.255.255.248**) is **/29**. **D** (**255.255.255.252**) is **/30**.",
            "choices": [
                "255.255.254.0",
                "255.255.255.240",
                "255.255.255.248",
                "255.255.255.252",
            ],
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="Router show ip route">
        <pre>Gateway of last resort is 172.16.2.2 to network 0.0.0.0

   10.0.0.0/8 is variably subnetted, 2 subnets, 2 masks
C       10.10.8.0/28 is directly connected, GigabitEthernet0/0/2
C       10.10.10.0/24 is directly connected, GigabitEthernet0/0/0
L       10.10.10.3/32 is directly connected, GigabitEthernet0/0/0
   172.16.0.0/16 is variably subnetted, 3 subnets, 2 masks
S       172.16.1.33/32 is directly connected, GigabitEthernet0/0/1
C       172.16.2.0/23 is directly connected, GigabitEthernet0/0/1
L       172.16.2.1/32 is directly connected, GigabitEthernet0/0/1
S*   0.0.0.0/0 [1/0] via 172.16.2.2</pre>
    </div>""",
        },
        {
            "slug": "private-ipv4-reasons-implement-choose-two",
            "title": "CCNA — Private IPv4: reasons (choose two)",
            "stem": "What are two reasons to implement IPv4 private addressing on a network? (Choose two)",
            "name": "priv41",
            "choose_two": True,
            "correct": ["B", "D"],
            "explain": "Correct. B and D \u2014 **RFC 1918 private IPv4** space lets organizations **conserve scarce globally unique public IPv4** addresses (often with **NAT** at the edge) and gain **flexibility** when **merging** or **renumbering** internal networks without consuming public space for every host. **A** is wrong: private addressing does **not** expand the global routing table. **C** misstates the main driver\u2014uniqueness within an org is a side effect, not the primary reason to adopt private space. **E** is not a primary **DoS** defense; non-routability on the Internet is incidental, not the design goal.",
            "choices": [
                "to expand the routing table on the router",
                "to facilitate renumbering when merging networks",
                "to enable internal applications to treat the private IPv4 addresses as unique",
                "to conserve global unique IPv4 addresses",
                "to provide protection from external denial-of-service attacks",
            ],
        },
        {
            "slug": "puppet-manifests-modules-paradigm",
            "title": "CCNA — Puppet: manifests and modules",
            "stem": "Which script paradigm does Puppet use?",
            "name": "puppet1",
            "correct": "A",
            "explain": "Correct. A \u2014 **Puppet** expresses desired state in **manifests** (`.pp` files) organized into reusable **modules**. **C** (**recipes** and **cookbooks**) describes **Chef**. **D** (**playbooks** and **roles**) describes **Ansible**. **B** is not a real automation paradigm.",
            "choices": [
                "manifests and modules",
                "strings and marionettes",
                "recipes and cookbooks",
                "playbooks and roles",
            ],
        },
        {
            "slug": "ipsec-tunnel-mode-encrypts-header-and-payload",
            "title": "CCNA — IPsec: tunnel encrypts header",
            "stem": "Which IPsec mode encrypts the IP header and the payload?",
            "name": "ipsecm1",
            "correct": "B",
            "explain": "Correct. B \u2014 **Tunnel mode** encrypts the **entire original IP packet** (original **IP header** plus **payload**, typically with **ESP**) and adds a **new outer IP header** for delivery across the VPN. **Transport mode** encrypts the **payload** but leaves the **original IP header** readable. **Pipe** and **control** are not standard IPsec mode names in this context.",
            "choices": [
                "pipe",
                "tunnel",
                "control",
                "transport",
            ],
        },
        {
            "slug": "wpa3-safeguards-brute-force-sae",
            "title": "CCNA — WPA3: SAE vs brute force",
            "stem": "What does WPA3 provide in wireless networking?",
            "name": "wpa3bf1",
            "correct": "D",
            "explain": "Correct. D \u2014 **WPA3-Personal** uses **SAE** (**Simultaneous Authentication of Equals**) instead of the older **WPA2-PSK** handshake, improving resistance to **offline dictionary/brute-force** attacks on passphrases. **A** overstates setup complexity\u2014WPA3 can be straightforward. **B** describes transitional/mixed deployments, not WPA3\u2019s defining security upgrade. **C** is wrong: **Protected Management Frames** are **required** for WPA3, not merely optional.",
            "choices": [
                "increased security and requirement of a complex configuration",
                "backward compatibility with WPA and WPA2",
                "optional Protected Management Frame negotiation",
                "safeguards against brute force attacks with SAE",
            ],
        },
        {
            "slug": "show-ip-route-ospf-metric-172-16-0-128-25",
            "title": "CCNA — OSPF metric in show ip route",
            "stem": "Refer to the exhibit. What is the metric for the OSPF-learned route to 172.16.0.128/25?",
            "name": "ospfmet2",
            "correct": "C",
            "explain": "Correct. C \u2014 In **`[AD/metric]`** notation, **`O 172.16.0.128/25 [110/32445]`** means **administrative distance 110** (default for **OSPF**) and **OSPF metric (cost) 32445**. **B (110)** is the **AD**, not the metric. **D (3184439)** is the **EIGRP** metric on **`D 172.16.0.192/29 [90/3184439]`**. **A (0)** is the **static default** metric on **`S* 0.0.0.0/0 [1/0]`**.",
            "choices": ["0", "110", "32445", "3184439"],
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="R1 show ip route">
        <pre>R1#show ip route | begin gateway

Gateway of last resort is 209.165.200.246 to network 0.0.0.0
S*   0.0.0.0/0 [1/0] via 209.165.200.246, Serial0/1/0
      is directly connected, Serial0/1/0
    172.16.0.0/16 is variably subnetted, 3 subnets, 3 masks
S     172.16.0.0/24 [1/0] via 207.165.200.250, Serial0/0/0
O     172.16.0.128/25 [110/32445] via 207.165.200.254, 00:00:33, Serial0/0/1
D     172.16.0.192/29 [90/3184439] via 207.165.200.254, 00:00:33, Serial0/0/1
    207.165.200.0/24 is variably subnetted, 4 subnets, 2 masks
C     207.165.200.248/30 is directly connected, Serial0/0/0
L     207.165.200.249/32 is directly connected, Serial0/0/0
C     207.165.200.252/30 is directly connected, Serial0/0/1
L     207.165.200.253/32 is directly connected, Serial0/0/1</pre>
    </div>""",
        },
        {
            "slug": "traffic-policing-drop-remark-choose-two",
            "title": "CCNA — Traffic policing actions (choose two)",
            "stem": "Which two actions are taken as the result of traffic policing? (Choose two)",
            "name": "qospol1",
            "choose_two": True,
            "correct": ["C", "D"],
            "explain": "Correct. C and D \u2014 **Policing** enforces a **committed rate**; traffic above the policy is typically **dropped** or **remarked** (mark-down, for example lower **DSCP**/**CoS**). **Buffering** and delaying excess traffic describe **shaping**, not policing. **Burst** parameters (committed/excess burst) govern how much short overrun is allowed but are not the primary **actions** on out-of-profile traffic. **Fragmentation** is unrelated to policing.",
            "choices": [
                "bursting",
                "fragmentation",
                "dropping",
                "remarking",
                "buffering",
            ],
        },
        {
            "slug": "static-route-best-path-10-10-10-3-slash-28",
            "title": "CCNA — Static route best path to 10.10.10.3",
            "stem": "Which IP route command created the best path for a packet destined for 10.10.10.3?",
            "name": "strt103",
            "correct": "C",
            "mono": True,
            "explain": "Correct. C \u2014 **10.10.10.3** matches several static routes, but **longest-prefix match** selects **`S 10.10.10.0/28`**, created by **`ip route 10.10.10.0 255.255.255.240 ...`**. **D** (**10.10.0.0/22**) and **A** (**10.0.0.0/8**) are **less specific**. **B** is a **host /32** for **10.10.10.1** only and does **not** match **10.10.10.3**.",
            "choices": [
                "ip route 10.0.0.0 255.0.0.0 g0/0",
                "ip route 10.10.10.1 255.255.255.255 g0/0",
                "ip route 10.10.10.0 255.255.255.240 g0/0",
                "ip route 10.10.0.0 255.255.252.0 g0/0",
            ],
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="Router show ip route">
        <pre>Gateway of last resort is 0.0.0.0 to network 0.0.0.0
10.0.0.0/8 is variably subnetted, 6 subnets, 5 masks
S       10.0.0.0/8 is directly connected, GigabitEthernet0/0
C       10.1.1.0/24 is directly connected, GigabitEthernet0/0
L       10.1.1.1/32 is directly connected, GigabitEthernet0/0
S       10.10.0.0/22 is directly connected, GigabitEthernet0/0
S       10.10.10.0/28 is directly connected, GigabitEthernet0/0
S       10.10.10.1/32 is directly connected, GigabitEthernet0/0
S*   0.0.0.0/0 is directly connected, GigabitEthernet0/0</pre>
    </div>""",
        },
        {
            "slug": "wlc-rogue-ap-class-type-friendly-autonomous",
            "title": "CCNA — WLC: classify rogue as Friendly",
            "stem": "A WLC sends alarms about a rogue AP, and the network administrator verifies that the alarms are caused by a legitimate autonomous AP. How must the alarms be stopped for the MAC address of the AP?",
            "name": "wlrogue1",
            "correct": "D",
            "explain": "Correct. D \u2014 Classify the AP as **Friendly** so the WLC treats it as a **known legitimate** device and **stops rogue alarms** for that **MAC**. **Manual containment** is for **mitigating** threats, not whitelisting. An **autonomous** AP is **not** \u201cremoved from WLC management\u201d in that sense. Clearing **Pending** alone does not classify the AP; **Friendly** is the correct **class type**.",
            "choices": [
                "Place the AP into manual containment.",
                "Remove the AP from WLC management.",
                "Manually remove the AP from Pending state.",
                "Set the AP Class Type to Friendly.",
            ],
        },
        {
            "slug": "anti-replay-prevent-mitm-attack",
            "title": "CCNA — Anti-replay vs MITM",
            "stem": "Which security method is used to prevent man-in-the-middle attack?",
            "name": "antirep1",
            "correct": "C",
            "explain": "Correct. C \u2014 **Anti-replay** (for example in **IPsec**) uses **sequence numbers** so captured packets cannot be **replayed**, blocking a common **MITM** technique. **Authentication** proves identity and helps prevent impersonation but is not the specific **anti-replay** control named here. **Authorization** decides permitted actions after identity. **Accounting** logs activity and does not prevent MITM.",
            "choices": [
                "authorization",
                "authentication",
                "anti-replay",
                "accounting",
            ],
        },
    ]

    prev = "vty-access-list-ssh-secure"
    for idx, q in enumerate(chain):
        i = 13 + idx
        slug = q["slug"]
        next_slug = chain[idx + 1]["slug"] if idx + 1 < len(chain) else None
        if q.get("choose_two"):
            ch_fn = checkbox_choice_line_mono if q.get("mono") else checkbox_choice_line
            ch_lines = "\n".join(
                ch_fn(q["name"], chr(ord("A") + j), t)
                for j, t in enumerate(q["choices"])
            )
            html = page_checkbox(
                title=q["title"],
                slug=slug,
                stem=q["stem"],
                choices_html=ch_lines,
                name=q["name"],
                correct_letters=q["correct"],
                explain=q["explain"],
                prev_slug=prev,
                next_slug=next_slug,
                post_stem_html=q.get("post_stem_html"),
                stem_after_exhibit=q.get("stem_after_exhibit"),
                prepend_html=q.get("prepend_html"),
            )
        else:
            ch_lines = "\n".join(
                choice_line(q.get("mono", False), q["name"], chr(ord("A") + j), t)
                for j, t in enumerate(q["choices"])
            )
            html = page(
                title=q["title"],
                slug=slug,
                stem=q["stem"],
                choices_html=ch_lines,
                name=q["name"],
                correct=q["correct"],
                explain=q["explain"],
                prev_slug=prev,
                next_slug=next_slug,
                mono_choices=q.get("mono", False),
                post_stem_html=q.get("post_stem_html"),
                stem_after_exhibit=q.get("stem_after_exhibit"),
                stem_after_exhibit_bullets=q.get("stem_after_exhibit_bullets"),
                stem_after_exhibit_tail=q.get("stem_after_exhibit_tail"),
                prepend_html=q.get("prepend_html"),
                stem_br=q.get("stem_br", False),
            )
        (OUT / f"{slug}.html").write_text(html, encoding="utf-8")
        prev = slug

    print("Wrote", len(chain), "files under", OUT)


if __name__ == "__main__":
    main()

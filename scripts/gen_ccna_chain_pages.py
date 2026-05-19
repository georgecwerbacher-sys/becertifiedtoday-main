#!/usr/bin/env python3
"""One-off generator for CCNA question HTML pages (inline template)."""
from __future__ import annotations

import html
import json
import math
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "public/CCNA-Study/CCNA_questions"
HUB_JS = ROOT / "public/CCNA-Study/js/ccna-practice-100-hub.js"
# Last hub slug before the generated chain (hand-maintained prefix stays first in ALL_SLUGS).
HUB_CHAIN_ANCHOR = "vty-access-list-ssh-secure"
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
      align-items: stretch;
      width: 100%;
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
      width: 100%;
      box-sizing: border-box;
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
      display: block;
      width: 100%;
      box-sizing: border-box;
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
      align-self: stretch;
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
            "stem": "Refer to the exhibit. What is the **metric** for the route to the **192.168.10.33** host?",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="R1 show ip route CLI output">
        <pre>R1#show ip route
Codes: C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route
Gateway of last resort is 192.168.30.10 to network 0.0.0.0
        192.168.30.0/29 is subnetted, 2 subnets
C         192.168.30.0 is directly connected, FastEthernet0/0
C         192.168.30.8 is directly connected, Serial0/0.1
        192.168.10.0/24 is variably subnetted, 2 subnets, 2 masks
O IA      192.168.10.32/28 [110/193] via 192.168.30.10, 00:18:49, Serial0/0.1
O IA      192.168.10.0/27 [110/192] via 192.168.30.10, 00:18:49, Serial0/0.1
        192.168.20.0/30 is subnetted, 1 subnets
O IA      192.168.20.0 [110/128] via 192.168.30.10, 00:18:49, Serial0/0.1
        192.168.50.0/32 is subnetted, 1 subnets
C         192.168.50.1 is directly connected, Loopback0
O*IA 0.0.0.0/0 [110/84] via 192.168.30.10, 00:10:36, Serial0/0.1</pre>
      </div>
    </div>""",
            "name": "ospfmet",
            "correct": "D",
            "explain": "Correct. D \u2014 **192.168.10.33** matches **192.168.10.32/28** (longest-prefix match beats **192.168.10.0/27**). In **[110/193]**, **110** is **administrative distance** and **193** is the **OSPF metric**. **84** is the default-route metric; **110** is AD, not metric; **192** is the **/27** route metric, not used for **.33**.",
            "choices": ["84", "110", "192", "193"],
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
        {
            "slug": "ospf-r2-must-be-dr-gi0-0-priority",
            "title": "CCNA — Elect R2 as OSPF DR on G0/0",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/ospf-r2-dr-gi0-0-priority-topology.png" alt="Topology: R1 and R2 connected on 10.0.0.0/30 via GigabitEthernet0/0 (.1 on R1, .2 on R2). R1 LAN 10.0.1.0/24 via SW1; R2 LAN 10.0.2.0/24 via SW2." width="900" decoding="async" loading="lazy" />
      </figure>
      <div class="exhibit-router-cli" role="region" aria-label="Router R1 configuration">
        <pre>Router R1 Configuration

Interface GigabitEthernet0/0
 ip ospf priority 99
!
router ospf 100
 network 10.0.0.0 0.0.0.31 area 0
 network 10.0.1.0 0.0.0.255 area 0</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. All routers in the network are configured. R2 must be the DR. After the engineer connected the devices, R1 was elected as the DR. Which command sequence must be configured on R2 to be elected as the DR in the network?",
            "name": "ospfr2dr",
            "correct": "B",
            "mono": True,
            "explain": "Correct. B \u2014 The exhibit shows **R1** with **ip ospf priority 99** on **GigabitEthernet0/0**, so R1 wins DR election over R2\u2019s default priority **1**. On the shared WAN segment, OSPF elects the DR using the **highest interface priority** (then **router ID** if priorities tie). Raising **R2\u2019s** priority on **GigabitEthernet0/0** to **100** beats R1\u2019s **99**. Priority **1** (A) stays below R1. **router-id** (C and D) only breaks ties when priorities match.",
            "choices": [
                "R2(config)#interface gi0/0\nR2(config-if)#ip ospf priority 1",
                "R2(config)#interface gi0/0\nR2(config-if)#ip ospf priority 100",
                "R2(config)#router ospf 1\nR2(config-router)#router-id 10.100.100.100",
                "R2(config)#router ospf 1\nR2(config-router)#router-id 192.168.2.7",
            ],
        },
        {
            "slug": "r1-show-ip-route-10-1-2-126-next-hop",
            "title": "CCNA — R1 next hop for 10.1.2.126",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="R1 show ip route">
        <pre>R1#show ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
Gateway of last resort is not set

     10.0.0.0/24 is subnetted, 5 subnets
D        10.1.2.0/24 [90/2170112] via 10.165.20.226, 00:01:33, Serial0/0
D        10.1.3.0/24 [90/2170112] via 10.165.20.226, 00:01:33, Serial0/0
D        10.1.2.0/25 [90/2170112] via 10.165.20.126, 00:01:33, Serial0/0
D        10.1.3.0/25 [90/2170112] via 10.165.20.146, 00:01:33, Serial0/0
D        10.1.4.0/25 [90/2170112] via 10.165.20.156, 00:01:33, Serial0/0
     192.168.1.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.10.0/24 is directly connected, GigabitEthernet0/0
     192.168.21.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.11.0/24 is directly connected, GigabitEthernet0/1
     10.165.20.0/24 is variably subnetted, 2 subnets, 2 masks
C        10.165.20.224/29 is directly connected, Serial0/0
S        10.1.2.112/28 [1/0] via 10.165.20.166</pre>
      </div>""",
            "stem": "Refer to the exhibit. What is the next hop for traffic entering R1 with a destination of 10.1.2.126?",
            "name": "r1nh126",
            "correct": "C",
            "explain": "Correct. C \u2014 R1 uses longest-prefix match. 10.1.2.126 matches 10.1.2.0/24, 10.1.2.0/25, and 10.1.2.112/28; the /28 static route is most specific (covers .112\u2013.127), so the next hop is 10.165.20.166. 10.165.20.126 (A) is the next hop for the shorter 10.1.2.0/25 EIGRP entry. 10.165.20.146 (B) is for 10.1.3.0/25. 10.165.20.226 (D) is for the less-specific 10.1.2.0/24 EIGRP route.",
            "choices": [
                "10.165.20.126",
                "10.165.20.146",
                "10.165.20.166",
                "10.165.20.226",
            ],
        },
        {
            "slug": "r1-static-route-10-0-0-24-r3-pc1-via-r2",
            "title": "CCNA — R1 static routes to 10.0.0.0/24 and PC1",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/r1-static-route-10-0-0-24-r3-pc1-r2-topology.png" alt="Topology: R1 connects to R2 on 172.16.0.0/24 and to R3 on 192.168.0.0/24. R2 and R3 connect to switch SW for 10.0.0.0/24 (PC1 10.0.0.5, PC2 10.0.0.8, PC3 10.0.0.12)." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. A network engineer must configure R1 so that it sends all packets destined to the 10.0.0.0/24 network to R3, and all packets destined to PC1 to R2. Which configuration must the engineer implement?",
            "name": "r1st100",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 Send the full **10.0.0.0/24** prefix toward **R3** on the **192.168.0.0/24** link (**192.168.0.2**), and add a host route for **PC1 (10.0.0.5/32)** toward **R2** on the **172.16.0.0/24** link (**172.16.0.2**). Longest-prefix match then sends PC1 traffic to R2 while other hosts in 10.0.0.0/24 use the /24 route via R3. Option A uses a /16 mask for 10.0.0.0 and sends PC1 to R3. Option B sends the entire /24 to R2 instead of R3. Option C swaps next hops and uses an incorrect /16 summary toward R3.",
            "choices": [
                "R1(config)#ip route 10.0.0.0 255.255.0.0 172.16.0.2\nR1(config)#ip route 10.0.0.5 255.255.255.255 192.168.0.2",
                "R1(config)#ip route 10.0.0.0 255.255.255.0 172.16.0.2\nR1(config)#ip route 10.0.0.5 255.255.255.255 192.168.0.2",
                "R1(config)#ip route 10.0.0.0 255.255.0.0 192.168.0.2\nR1(config)#ip route 10.0.0.0 255.255.255.0 172.16.0.2",
                "R1(config)#ip route 10.0.0.0 255.255.255.0 192.168.0.2\nR1(config)#ip route 10.0.0.5 255.255.255.255 172.16.0.2",
            ],
        },
        {
            "slug": "ospf-r2-wan-dr-gi0-0-address-priority",
            "title": "CCNA — R2 DR on WAN (G0/0 address and priority)",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/ospf-r2-dr-gi0-0-priority-topology.png" alt="Topology: R1 and R2 on 10.0.0.0/30 via GigabitEthernet0/0; R1 LAN 10.0.1.0/24; R2 LAN 10.0.2.0/24." width="900" decoding="async" loading="lazy" />
      </figure>
      <div class="exhibit-router-cli" role="region" aria-label="Router R1 configuration">
        <pre>Router R1 Configuration

Interface GigabitEthernet0/0
 ip ospf priority 99
!
router ospf 100
 network 10.0.0.0 0.0.0.31 area 0
 network 10.0.1.0 0.0.0.255 area 0</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. An engineer must configure router R2 so it is elected as the DR on the WAN subnet. Which command sequence must be configured?",
            "name": "ospfr2wand",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 The exhibit shows **R1** with **ip ospf priority 99** on **GigabitEthernet0/0**. On the WAN segment, R2 needs an address in the **10.0.0.0** space and an OSPF priority **higher than 99**; **ip ospf priority 100** makes R2 win DR election. **Priority 0** (C) removes R2 from DR/BDR eligibility. Options A and B place **10.0.1.1** on G0/0, which does not match the WAN link (**10.0.0.0/30**, .1 toward R1 and .2 toward R2 in the exhibit). Option B\u2019s /24 mask on 10.0.1.1 is also inconsistent with the point-to-point WAN.",
            "choices": [
                "interface gigabitethernet0/0\nip address 10.0.1.1 255.255.255.224\nip ospf priority 98",
                "interface gigabitethernet0/0\nip address 10.0.1.1 255.255.255.0\nip ospf priority 255",
                "interface gigabitethernet0/0\nip address 10.0.0.34 255.255.255.248\nip ospf priority 0",
                "interface gigabitethernet0/0\nip address 10.0.0.34 255.255.255.224\nip ospf priority 100",
            ],
        },
        {
            "slug": "r1-route-host-b-10-10-13-25-lowest-ad",
            "title": "CCNA — R1 route to host B (10.10.13.0/25 AD)",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/r1-route-host-b-10-10-13-25-topology.png" alt="Topology: Host A 10.10.14.10/25 on R1; Host B 10.10.13.10/25 on R4. R1–R2 10.10.10.0/30 (.1/.2), R1–R4 10.10.10.4/30 (.5/.6), R1–R3 10.10.10.8/30 (.9/.10); R2–R4 and R3–R4 links; R3 4.4.4.4." width="900" decoding="async" loading="lazy" />
      </figure>
      <div class="exhibit-router-cli" role="region" aria-label="R1 routing configuration">
        <pre>R1(config)#ip route 0.0.0.0 0.0.0.0 10.10.10.2
R1(config)#ip route 10.10.13.0 255.255.255.128 10.10.10.2 111
R1(config)#ip route 10.10.13.0 255.255.255.128 10.10.10.6 112
R1(config)#ip route 10.10.13.0 255.255.255.128 10.10.10.10 108
R1(config)#router ospf 1
R1(config-router)#router-id 1.1.1.1
R1(config-router)#network 10.10.10.5 0.0.0.0 area 0
R1(config-router)#network 10.10.10.1 0.0.0.0 area 0
R1(config-router)#network 10.10.14.1 0.0.0.0 area 0</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. R1 has just received a packet from host A that is destined to host B. Which route in the routing table is used by R1 to reach host B?",
            "name": "r1rthb",
            "correct": "D",
            "explain": "Correct. D \u2014 For the same prefix **10.10.13.0/25**, R1 compares **administrative distance**. The static route via **10.10.10.10** uses AD **108**, which beats the other statics (**111** and **112**) and OSPF\u2019s default AD **110**, so the installed route is **10.10.13.0/25 [108/0] via 10.10.10.10**. Option A is a static with AD **1** (default) in the display but the exhibit\u2019s floating static toward **10.10.10.2** is AD **111**, not preferred. Options B and C show OSPF **[110/2]** paths; OSPF loses to the lower-AD static.",
            "choices": [
                "10.10.13.0/25[1/0] via 10.10.10.2",
                "10.10.13.0/25[110/2] via 10.10.10.6",
                "10.10.13.0/25[110/2] via 10.10.10.2",
                "10.10.13.0/25[108/0] via 10.10.10.10",
            ],
        },
        {
            "slug": "windows-ipconfig-dns-query-www-cisco-com",
            "title": "CCNA — DNS query destination (ipconfig /all)",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-terminal-white" role="region" aria-label="Windows ipconfig /all output">
        <pre>C:\\Users\\ciscoadmin&gt;ipconfig /all

Windows IP Configuration

   Host Name . . . . . . . . . . . . : DESKTOP-480JBBT
   Primary Dns Suffix  . . . . . . . :
   Node Type . . . . . . . . . . . . : Hybrid
   IP Routing Enabled. . . . . . . . : No
   WINS Proxy Enabled. . . . . . . . : No
   DNS Suffix Search List. . . . . . : arcap.se

Ethernet adapter Ethernet:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : Realtek PCIe GBE Family Controller
   Physical Address. . . . . . . . . : 3C-52-82-33-F3-8F
   DHCP Enabled. . . . . . . . . . . : Yes
   Autoconfiguration Enabled . . . . : Yes

Wireless LAN adapter Wi-Fi:

   Connection-specific DNS Suffix  . : arcap.se
   Description . . . . . . . . . . . : Intel(R) Dual Band Wireless-AC 7265
   Physical Address. . . . . . . . . : C8-21-5B-84-F3-EF
   DHCP Enabled. . . . . . . . . . . : Yes
   Autoconfiguration Enabled . . . . : Yes
   Link-local IPv6 Address . . . . . : fe80::45a1:b3fa:2f37:bf37%2(Preferred)
   IPv4 Address. . . . . . . . . . . : 192.168.1.226(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Lease Obtained. . . . . . . . . . : October 3, 2019 12:28:08 PM
   Lease Expires . . . . . . . . . . : October 3, 2019 7:18:38 PM
   Default Gateway . . . . . . . . . : 192.168.1.100
   DHCP Server . . . . . . . . . . . : 192.168.1.254
   DHCPv6 IAID . . . . . . . . . . . : 4667016B
   DHCPv6 Client DUID. . . . . . . . : 00-01-00-01-20-FF-05-55-3C-F3-34-29-20-DF
   DNS Servers . . . . . . . . . . . : 192.168.1.253
   NetBIOS over Tcpip. . . . . . . . : Enabled
   Connection-specific DNS Suffix Search List :
                                       arcap.se</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. The given Windows PC is requesting the IP address of the host at www.cisco.com. To which IP address is the request sent?",
            "name": "windns1",
            "correct": "B",
            "explain": "Correct. B \u2014 Resolving **www.cisco.com** is a **DNS** lookup. The PC sends the query to the **DNS server** listed on the active **Wi-Fi** adapter: **192.168.1.253**. **192.168.1.226** (A) is this PC\u2019s own IPv4 address. **192.168.1.100** (C) is the **default gateway**, used when the destination is not on the local subnet after DNS resolution. **192.168.1.254** (D) is the **DHCP server**, which assigned addresses but does not handle name resolution unless it is also configured as DNS (not shown here).",
            "choices": [
                "192.168.1.226",
                "192.168.1.253",
                "192.168.1.100",
                "192.168.1.254",
            ],
        },
        {
            "slug": "r1-static-route-r3-lan-10-0-15-via-20-3",
            "title": "CCNA — R1 static route to R3 LAN (10.0.15.0/24)",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/r1-static-route-r3-lan-10-0-15-topology.png" alt="Topology: R1, R2, and R3 on 10.0.20.0/24 (.1, .2, .3). R1 LAN 10.0.0.64/26, R2 LAN 10.0.0.128/26, R3 LAN 10.0.15.0/24." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. Router R1 is added to the network and configured with the 10.0.0.64/26 and 10.0.20.0/24 subnets. However, traffic destined for the LAN on R3 is not accessible. Which command when executed on R1 defines a static route to reach the R3 LAN?",
            "name": "r1r3lan",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 The **R3 LAN** is **10.0.15.0/24**, so the static route must use network **10.0.15.0** mask **255.255.255.0**. The next hop on the shared **10.0.20.0/24** segment toward R3 is **10.0.20.3** (R3\u2019s interface on that link). Option A points to **10.0.20.1** (R1\u2019s own side). Option B uses mask **255.255.255.192** (/26), which does not match the /24 LAN. Option C targets **10.0.0.64/26** (R1\u2019s LAN), not the R3 prefix.",
            "choices": [
                "ip route 10.0.15.0 255.255.255.0 10.0.20.1",
                "ip route 10.0.15.0 255.255.255.192 10.0.20.1",
                "ip route 10.0.0.64 255.255.255.192 10.0.20.3",
                "ip route 10.0.15.0 255.255.255.0 10.0.20.3",
            ],
        },
        {
            "slug": "wlc-wlan-80211r-enable-ft-8021x",
            "title": "CCNA — WLC 802.11r with FT 802.1X",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/wlc-wlan-layer2-80211r-ft-8021x-exhibit.png" alt="WLC WLAN Security Layer 2: WPA+WPA2, WPA2 Policy and AES, 802.1X enabled, Fast Transition Adaptive, FT 802.1X off, PMF disabled." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. Clients on the WLAN are required to use 802.11r. What action must be taken to meet the requirement?",
            "name": "wlc11rft",
            "correct": "C",
            "explain": "Correct. C \u2014 **IEEE 802.11r** (Fast BSS Transition) is enabled on the WLAN by setting **Fast Transition** to **Enabled** (not Adaptive or Disabled) and selecting the matching fast-roaming AKM. With **802.1X** already enabled in the exhibit, you also enable **FT 802.1X** under Authentication Key Management so 802.11r works with enterprise authentication. **CCKM** (A) is a different fast-roaming method, not 802.11r. **PMF Required** (B) protects management frames but does not implement 802.11r. Disabling **Fast Transition** and **gtk-randomize** (D) does not meet an 802.11r requirement.",
            "choices": [
                "Enable CCKM under Authentication Key Management",
                "Under Protected Management Frames, set the PMF option to Required",
                "Set the Fast Transition option to Enable and enable FT 802.1X under Authentication Key Management",
                "Set the Fast Transition option and the WPA gtk-randomize State to disable",
            ],
        },
        {
            "slug": "json-aaa-user-nested-roles-object-count",
            "title": "CCNA — Count JSON objects (aaaUser roles)",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="JSON aaaUser snippet">
        <pre>{
  "aaaUser": {
    "attributes": {
      "pwd": "password1",
      "firstName": "Abraham",
      "lastName": "Lincoln",
      "phone": "5555551212",
      "email": "test@cisco.com"
    },
    "children": [
      {
        "aaaUserRole": {
          "attributes": {
            "name": "ExampleCisco"
          },
          "children": [
            {
              "aaaUserRole": {
                "attributes": {
                  "name": "admin"
                }
              }
            }
          ]
        }
      }
    ]
  }
}</pre>
      </div>""",
            "stem": "Refer to the exhibit. How many objects are present in the given JSON-encoded data?",
            "name": "jsonobj9",
            "correct": "D",
            "explain": "Correct. D \u2014 In JSON, each `{ ... }` pair of braces defines one **object**. Counting every object in the exhibit: (1) the root document, (2) **aaaUser**, (3) the **attributes** block under **aaaUser**, (4) the wrapper in the first **children** entry, (5) the outer **aaaUserRole**, (6) its **attributes**, (7) the inner **children** entry wrapper, (8) the nested **aaaUserRole**, and (9) its **attributes** \u2014 **nine** objects total. Arrays (`[ ... ]`) are not objects. One (A) and four (C) undercount; seven (B) misses nested **aaaUserRole** / **attributes** objects.",
            "choices": [
                "one",
                "four",
                "seven",
                "nine",
            ],
        },
        {
            "slug": "r2-no-cdp-enable-g02-hide-neighbor-from-r3",
            "title": "CCNA — R2 CDP: hide neighbor info from R3",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/r1-r2-r3-cdp-r2-g02-no-cdp-enable-topology.png" alt="Topology: R1 connected to R2 GigabitEthernet0/1; R2 GigabitEthernet0/2 connected to R3." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. A network engineer must configure R2 to avoid sharing any neighbor information with R3, and maintain its relationship with R1. What action meets this requirement?",
            "name": "r2cdpr3",
            "correct": "D",
            "explain": "Correct. D \u2014 **CDP** advertises neighbor IP addresses, platform, and IOS version. To stop R2 from exchanging CDP with **R3** only, disable CDP on the interface toward R3: **no cdp enable** under **GigabitEthernet0/2** while **cdp run** stays enabled globally so **GigabitEthernet0/1** toward **R1** still works. **no cdp run** globally (C) disables CDP toward R1 as well. **no lldp run** globally (A) affects LLDP, not CDP, and disables LLDP on every interface. **no lldp receive** on **g0/1** (B) is the link toward **R1**, not R3.",
            "choices": [
                "Configure the no lldp run command globally",
                "Configure the no lldp receive command on g0/1",
                "Configure the no cdp run command globally",
                "Configure the no cdp enable command on g0/2",
            ],
        },
        {
            "slug": "port-security-dynamic-mac-restrict-violation-choose-two",
            "title": "CCNA — Port security: dynamic MAC and restrict (choose two)",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/sw-g01-port-security-pc-topology.png" alt="Topology: switch SW GigabitEthernet0/1 connected to a host." width="480" decoding="async" loading="lazy" />
      </figure>
      <div class="exhibit-router-cli" role="region" aria-label="Switch partial port-security configuration">
        <pre>SW# conf t
SW(config)#interface gigabitEthernet0/1
SW(config-if)#switchport mode access
SW(config-if)#switchport port-security
SW(config-if)#</pre>
      </div>
    </div>""",
            "stem": "A network engineer started to configure port security on a new switch. These requirements must be met:\n\n\u2022 MAC addresses must be learned dynamically.\n\u2022 Log messages must be generated without disabling the interface when unwanted traffic is seen.\n\nWhich two commands must be configured to complete this task? (Choose two)",
            "name": "pswrestrict",
            "choose_two": True,
            "mono": True,
            "correct": ["B", "E"],
            "explain": "Correct. B and E \u2014 **`switchport port-security maximum 2`** allows up to two **dynamically learned** secure MAC addresses on the port (default **maximum** is **1**). **`switchport port-security violation restrict`** drops violating traffic, increments the violation counter, and sends **syslog** (and SNMP) **without** **err-disabling** the interface. Default violation mode is **`shutdown`**, which would violate the logging-without-disable requirement (D). **`mac-address`** with a fixed address (A) is **static**, not dynamic learning. **`mac-address sticky`** (C) converts learned addresses to **sticky** secure MACs, which is not the dynamic-only behavior asked for here.",
            "choices": [
                "SW(config-if)#switchport port-security mac-address 0010.7B84.45E6",
                "SW(config-if)#switchport port-security maximum 2",
                "SW(config-if)#switchport port-security mac-address sticky",
                "SW(config-if)#switchport port-security violation shutdown",
                "SW(config-if)#switchport port-security violation restrict",
            ],
        },
        {
            "slug": "r1-host-route-server-10-10-10-10-via-r2",
            "title": "CCNA — R1 host route to server via R2",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/r1-r2-sw1-server-host-route-topology.png" alt="Topology: R1 S0/0 192.168.0.1/30 to R2 S0/0 192.168.0.2/30; R2 Gi0/0 10.10.10.1/24 to Switch 1 10.10.10.2/24 and Server 10.10.10.10/24." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. A network engineer must configure router R1 with a host route to the server. Which command must the engineer configure?",
            "name": "r1hostrt",
            "correct": "A",
            "mono": True,
            "explain": "Correct. A \u2014 A **host route** targets one address: **10.10.10.10/32** (**255.255.255.255** mask). From **R1**, the next hop toward **R2** on the serial link is **192.168.0.2**, so **`ip route 10.10.10.10 255.255.255.255 192.168.0.2`**. **B** is a **/24** network route for the whole **10.10.10.0** LAN, not a host route to the server alone. **C** is a **default** route (**0.0.0.0/0**). **D** reverses destination and next-hop fields.",
            "choices": [
                "R1(config)#ip route 10.10.10.10 255.255.255.255 192.168.0.2",
                "R1(config)#ip route 10.10.10.0 255.255.255.0 192.168.0.2",
                "R1(config)#ip route 0.0.0.0 0.0.0.0 192.168.0.2",
                "R1(config)#ip route 192.168.0.2 255.255.255.255 10.10.10.10",
            ],
        },
        {
            "slug": "northbound-api-function-sdn-controller-applications",
            "title": "CCNA — Northbound API function",
            "stem": "What is the function of a northbound API in a network architecture that separates the control and application layers?",
            "name": "nbapi1",
            "correct": "D",
            "explain": "Correct. D \u2014 Northbound APIs sit between the SDN controller (control layer) and applications/orchestration above it, so business apps can request services, policy, and visibility without talking directly to each device. Southbound APIs face the infrastructure layer. Upgrading software and restoring files describes operational tasks, not the northbound role. Global provisioning alone does not define the controller-to-application path.",
            "choices": [
                "It upgrades software and restores files.",
                "It relies on global provisioning and configuration.",
                "It supports distributed processing for configuration.",
                "It provides a path between an SDN controller and network applications.",
            ],
        },
        {
            "slug": "qos-traffic-shaping-purpose",
            "title": "CCNA — Purpose of traffic shaping",
            "stem": "What is a purpose of traffic shaping?",
            "name": "qshpurpose1",
            "correct": "D",
            "explain": "Correct. D \u2014 Traffic shaping enforces an average or peak transmission rate by buffering excess traffic and sending it when capacity is available, which limits bandwidth usage to the configured rate. Policy-based routing selects paths by policy, not by deferring traffic to a rate. Best-effort service is the default QoS behavior without shaping. Dynamic flow identification classifies traffic (for example with NBAR) but is not the primary purpose of shaping.",
            "choices": [
                "It enables dynamic flow identification.",
                "It enables policy-based routing.",
                "It provides best-effort service.",
                "It limits bandwidth usage.",
            ],
        },
        {
            "slug": "autonomous-ap-wlan-vlan-wired-trunk-port",
            "title": "CCNA — Autonomous AP uplink for multiple WLAN VLANs",
            "stem": "Which type of port is used to connect to the wired network when an autonomous AP maps two VLANs to its WLANs?",
            "name": "apwlantrunk1",
            "correct": "C",
            "explain": "Correct. C \u2014 Multiple WLANs mapped to different VLANs require the wired uplink to carry 802.1Q-tagged traffic for each VLAN, so the AP-to-switch link is configured as a **trunk**. An **access** port carries a single VLAN. **LAG** and **EtherChannel** bundle links for bandwidth or redundancy but do not by themselves provide multi-VLAN tagging.",
            "choices": [
                "LAG",
                "EtherChannel",
                "trunk",
                "access",
            ],
        },
        {
            "slug": "switch-destination-mac-missing-cam-flood-vlan",
            "title": "CCNA — Unknown destination MAC on a switch",
            "stem": "What does a switch do when it receives a frame whose destination MAC address is missing from the MAC address table?",
            "name": "swcamunk1",
            "correct": "A",
            "explain": "Correct. A \u2014 An unknown destination MAC is treated as unknown unicast: the switch floods the frame out all other ports in the same VLAN except the ingress port so the host can be reached and the switch can learn the MAC from a reply. It does not add a static entry and shut down the port, does not learn the unknown destination from the frame itself without flooding first, and does not alter the frame checksum to mark it invalid.",
            "choices": [
                "It floods the frame unchanged across all remaining ports in the incoming VLAN.",
                "It appends the table with a static entry for the MAC and shuts down the port.",
                "It updates the CAM table with the destination MAC address of the frame.",
                "It changes the checksum of the frame to a value that indicates an invalid frame.",
            ],
        },
        {
            "slug": "collapsed-core-distribution-single-layer-characteristic",
            "title": "CCNA — Collapsed-core topology characteristic",
            "stem": "What is a characteristics of a collapsed-core network topology?",
            "name": "colcorechar1",
            "correct": "A",
            "explain": "Correct. A \u2014 Collapsed core (two-tier campus) merges the traditional distribution and core layers onto one combined layer, reducing device count for smaller sites. EtherChannel to a single logical distribution device is not the defining trait. A single SOHO switch with internet is access/edge simplicity, not collapsed core. Wireless does not attach directly to a separate core layer for faster transmission in this model.",
            "choices": [
                "It allows the core and distribution layers to run as a single combined layer.",
                "It enables the core and access layers to connect to one logical distribution device over an EtherChannel.",
                "It enables all workstations in a SOHO environment to connect on a single switch with internet access.",
                "It allows wireless devices to connect directly to the core layer, which enables faster data transmission.",
            ],
        },
        {
            "slug": "southbound-interface-controller-device-programs",
            "title": "CCNA — Southbound interface: controller to devices",
            "stem": "Which interface enables communication between a program on the controller and a program on the networking devices?",
            "name": "sbiface1",
            "correct": "C",
            "explain": "Correct. C \u2014 The southbound interface (API) connects the SDN controller to infrastructure devices so controller software can program forwarding and configuration on switches and routers (for example via OpenFlow, NETCONF, or RESTCONF). Northbound interfaces connect applications to the controller, not devices. A software virtual interface and a tunnel interface are not the SDN architectural terms for this controller-to-device control path.",
            "choices": [
                "northbound interface",
                "software virtual interface",
                "southbound interface",
                "tunnel interface",
            ],
        },
        {
            "slug": "private-address-space-primary-purpose-conserve",
            "title": "CCNA — Primary purpose of private address space",
            "stem": "What is the primary purpose of private address space?",
            "name": "privaddr1",
            "correct": "A",
            "explain": "Correct. A \u2014 RFC 1918 private IPv4 space lets organizations use non\u2011globally\u2011unique internal addresses so scarce public (globally unique) IPv4 is not consumed for every host; NAT at the edge is commonly used alongside private space but conserving public addresses is the primary design purpose. Simplifying addressing, limiting Internet reachability, and reducing complexity may be operational side effects but are not the primary reason private space was defined.",
            "choices": [
                "conserve globally unique address space",
                "simplify the addressing in the network",
                "limit the number of nodes reachable via the Internet",
                "reduce network complexity",
            ],
        },
        {
            "slug": "wlc-distribution-port-trunk-multiple-vlans",
            "title": "CCNA — Trunk to WLC distribution port",
            "stem": "What is a reason to configure a trunk port that connects to a WLC distribution port?",
            "name": "wlctrunk1",
            "correct": "B",
            "explain": "Correct. B \u2014 The WLC distribution (DS) port carries CAPWAP and bridged client traffic onto the wired LAN; a trunk carries multiple VLANs in the data path so different WLANs or client VLANs can be tagged and forwarded. Trunks do not eliminate redundancy on link failure (LAG/EtherChannel or redundant paths address that). Out-of-band management uses the service port, not the distribution trunk for multiple management VLANs.",
            "choices": [
                "Eliminate redundancy with a link failure in the data path.",
                "Allow multiple VLAN to be used in the data path.",
                "Provide redundancy if there is a link failure for out-of-band management.",
                "Permit multiple VLANs to provide out-of-band management.",
            ],
        },
        {
            "slug": "wpa2-wireless-encryption-cipher-aes",
            "title": "CCNA — WPA2 wireless encryption cipher",
            "stem": "Which cipher is supported for wireless encryption only with the WPA2 standard?",
            "name": "wpa2cipher1",
            "correct": "B",
            "explain": "Correct. B \u2014 WPA2 mandates CCMP, which uses AES for frame encryption. RC4 underpins legacy WEP and WPA TKIP, not WPA2. AES-256 (GCMP-256) is associated with WPA3-Enterprise 192-bit modes, not WPA2 alone. SHA provides hashing/integrity in authentication suites; it is not the wireless air-interface encryption cipher named in these options.",
            "choices": [
                "AES256",
                "AES",
                "RC4",
                "SHA",
            ],
        },
        {
            "slug": "longest-prefix-match-192-168-10-5-entry-table",
            "title": "CCNA — Longest prefix match 192.168.10.5",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="Routing table entries">
        <pre>Entry #
1     192.168.10.0 255.255.254.0
2     192.168.10.0 255.255.255.192
3     192.168.10.0 255.255.0.0
4     192.168.10.0 255.255.224.0</pre>
    </div>""",
            "stem": "Which entry is the longest prefix match for host IP address 192.168.10.5?",
            "name": "lpm1005",
            "correct": "B",
            "explain": "Correct. B \u2014 **192.168.10.5** matches all four networks, but **entry 2** (**192.168.10.0/26**, mask **255.255.255.192**) is the **longest** (most specific) prefix. Entry 1 is **/23**, entry 4 is **/19**, and entry 3 is **/16**.",
            "choices": [
                "1",
                "2",
                "3",
                "4",
            ],
        },
        {
            "slug": "snmpv2-getbulk-inform-large-data-choose-two",
            "title": "CCNA — SNMPv2 GetBulk and Inform (choose two)",
            "stem": "Which two features introduced in SNMPv2 provide the ability to retrieve large amounts of data in one request? (Choose two)",
            "name": "snmpv2bulk1",
            "choose_two": True,
            "correct": ["D", "E"],
            "explain": "Correct. D and E \u2014 **GetBulk** (SNMPv2) lets the NMS request many MIB variables in one PDU using non-repeaters and max-repetitions, which is far more efficient than repeated **GetNext** walks. **Inform** (SNMPv2) is a trap-style PDU that requires an acknowledgment from the manager, improving reliability for event delivery. **Get**, **GetNext**, and **Set** existed in SNMPv1; **GetNext** still walks one variable at a time per request compared with **GetBulk**.",
            "choices": [
                "Get",
                "GetNext",
                "Set",
                "GetBulk",
                "Inform",
            ],
        },
        {
            "slug": "forward-172-18-32-38-longest-match-g0-0",
            "title": "CCNA — Forward 172.18.32.38 (show ip route)",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="Router show ip route">
        <pre>router# show ip route
...
D  172.18.32.0/26 [90/25789217] via 10.1.1.1
R  172.18.32.0/24 [120/4] via 10.1.1.2
O  172.18.32.0/19 [110/229840] via 10.1.1.3
C  172.18.32.32/32 is directly connected, Loopback0
C  172.18.32.36/30 is directly connected, GigabitEthernet0/0
L  172.18.32.37/32 is directly connected, GigabitEthernet0/0</pre>
    </div>""",
            "stem": "A packet sourced from 172.18.33.2 is destined for 172.18.32.38. Where does the router forward the packet?",
            "name": "fwd32138",
            "correct": "A",
            "explain": "Correct. A \u2014 **172.18.32.38** matches several routes, but **172.18.32.36/30** on **GigabitEthernet0/0** is the **longest** match (.36\u2013.39). The router forwards out the connected interface. **Loopback0** is only **172.18.32.32/32**. **10.1.1.1** is the next hop for the shorter **/26** EIGRP route; **10.1.1.3** is for **/19** OSPF\u2014both lose to the **/30** connected route.",
            "choices": [
                "GigabitEthernet0/0",
                "Loopback0",
                "10.1.1.1",
                "10.1.1.3",
            ],
        },
        {
            "slug": "wpa3-enhancement-brute-force-protection",
            "title": "CCNA — WPA3 enhancement",
            "stem": "Which enhancement is implemented in WPA3?",
            "name": "wpa3enh1",
            "correct": "D",
            "explain": "Correct. D \u2014 WPA3-Personal replaces WPA2-PSK with SAE (Simultaneous Authentication of Equals), which resists offline dictionary and brute-force attacks on weak passphrases. 802.1X was already available in WPA2 Enterprise (A). TKIP is legacy WPA (B). PKI for AP identification is not the defining WPA3 enhancement listed here (C).",
            "choices": [
                "applies 802.1x authentication",
                "uses TKIP",
                "employs PKI to identify access points",
                "protects against brute force attacks",
            ],
        },
        {
            "slug": "hsrp-virtual-ip-default-gateway",
            "title": "CCNA — HSRP virtual IP address",
            "stem": "Which type of address is shared by routers in a HSRP implementation and used by hosts on the subnet as their default gateway address?",
            "name": "hsrpvip1",
            "correct": "C",
            "explain": "Correct. C \u2014 HSRP presents a **virtual IP address** (and virtual MAC) on the LAN; the active router forwards traffic for that address while the standby takes over if the active fails. Hosts point their default gateway at the virtual IP. HSRP routers use **multicast** hellos between themselves, but hosts do not use a multicast address as the default gateway. A **loopback** is a router-local address. A **broadcast** is not the client default gateway.",
            "choices": [
                "multicast address",
                "loopback IP address",
                "virtual IP address",
                "broadcast address",
            ],
        },
        {
            "slug": "switch-frame-flooding-reasons-choose-two",
            "title": "CCNA — Reasons for switch frame flooding (choose two)",
            "stem": "What are two reasons a switch experiences frame flooding? (Choose two)",
            "name": "swflood1",
            "choose_two": True,
            "correct": ["B", "E"],
            "explain": "Correct. B and E \u2014 **STP topology changes** trigger TCN processing that shortens CAM aging; many MACs are removed or not yet relearned, so unknown unicast destinations are **flooded** until the table repopulates. When the **forwarding (MAC) table overflows**, new addresses cannot be learned and traffic to those unknown destinations is flooded. A bad cable may cause link errors but is not the usual CCNA explanation for systematic flooding. Normal MAC aging is not described as \u201cexcessive updates,\u201d and **port-security** limits MACs on a port rather than causing VLAN-wide flooding.",
            "choices": [
                "A defective patch cable is connected to the switch port",
                "Topology changes are occurring within spanning-tree",
                "An aged MAC table entry is causing excessive updates",
                "Port-security is configured globally",
                "The forwarding table has overflowed",
            ],
        },
        {
            "slug": "tcp-over-udp-https-error-checking-ack",
            "title": "CCNA — TCP vs UDP for HTTPS",
            "stem": "Why is TCP desired over UDP for application that require extensive error checking, such as HTTPS?",
            "name": "tcpudphttps1",
            "correct": "A",
            "explain": "Correct. A \u2014 **UDP** is connectionless and does **not** use transport-layer acknowledgments or retransmission; lost or corrupted segments are not recovered by UDP itself. **TCP** provides reliable delivery with **acknowledgments**, retransmissions, and sequencing\u2014needed for HTTPS (TLS runs over TCP). **B** reverses the protocols (UDP does not guarantee delivery; TCP does not simply drop traffic under load). **C** reverses flow control (TCP uses windowing/flow control and congestion control). **D** reverses sequencing (TCP delivers in order; UDP has no built-in ordering).",
            "choices": [
                "UDP operates without acknowledgments, and TCP sends an acknowledgment for every packet received.",
                "UDP reliably guarantees delivery of all packets, and TCP drops packets under heavy load.",
                "UDP uses flow control mechanisms for the delivery of packets, and TCP uses congestion control for efficient packet delivery.",
                "UDP uses sequencing data for packets to arrive in order, and TCP offers the capability to receive packets in random order.",
            ],
        },
        {
            "slug": "security-badge-datacenter-physical-access",
            "title": "CCNA — Badge authentication and physical access control",
            "stem": "To improve corporate security, an organization is planning to implement badge authentication to limit access to the data center. Which element of a security program is being deployed?",
            "name": "secbadge1",
            "correct": "D",
            "explain": "Correct. D \u2014 **Badge readers** at data-center doors are **physical access control**: they regulate who may enter a facility or secure area. **User training** and **user awareness** are education programs, not door-entry systems. **Vulnerability verification** is testing or scanning for weaknesses, not badge-based entry control.",
            "choices": [
                "user training",
                "user awareness",
                "vulnerability verification",
                "physical access control",
            ],
        },
        {
            "slug": "vlan10-subnet-192-168-32-last-usable-no-switchport",
            "title": "CCNA — VLAN 10 L3 interface after /27 subnetting",
            "stem": "The address block 192.168.32.0/24 must be subnetted into smaller networks. The engineer must meet these requirements:\n* Create 8 new subnets\n* Each subnet must accommodate 30 hosts\n* Interface VLAN 10 must use the last usable IP in the first new subnet\n* A Layer 3 interface is used\n\nWhich configuration must be applied to the interface?",
            "name": "vlan10sub1",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 Eight subnets from a /24 need three more network bits: **/27** (mask **255.255.255.224**), which yields **30** usable hosts per subnet (32\u22122). The **first** /27 is **192.168.32.0/27** (usable **.1\u2013.30**, last usable **192.168.32.30**). A routed **Layer 3** port uses **`no switchport`** then **`ip address`**. **A** and **B** use **/28** (/240), which only provides **14** hosts. **C** places **192.168.32.97** in the **third** /27, not the last usable address of the first subnet.",
            "choices": [
                "no switchport mode access\nip address 192.168.32.62 255.255.255.240",
                "switchport\nip address 192.168.32.65 255.255.255.240",
                "no switchport mode trunk\nip address 192.168.32.97 255.255.255.224",
                "no switchport\nip address 192.168.32.30 255.255.255.224",
            ],
        },
        {
            "slug": "ipv6-anycast-global-unicast-dhcp-dns",
            "title": "CCNA — IPv6 anycast address range",
            "stem": "Which IPv6 address range is suitable for anycast addresses for distributed services such DHCP or DNS?",
            "name": "v6anycast1",
            "correct": "B",
            "explain": "Correct. B \u2014 IPv6 **anycast** addresses are taken from the **global unicast** space (**2000::/3**); the same address is configured on multiple nodes and routing delivers to the nearest. A **/128** global unicast such as **2001:db8::/32** documentation examples illustrates that pattern. **FF00::/8** (**A**) is **multicast**, not anycast. **FE80::/10** (**D**) is **link-local** and does not route for site-wide DHCP/DNS. **2002::/16** (**C**) is legacy **6to4**, not the usual anycast service range.",
            "choices": [
                "FF00:1/12",
                "2001:db8:0234:ca3e::1/128",
                "2002:db84:3f37:ca98:be05:8/64",
                "FE80::1/10",
            ],
        },
        {
            "slug": "r19-fa0-0-output-drops-oversubscription",
            "title": "CCNA — R19 Fa0/0 poor performance (show interface)",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="R19 show interface FastEthernet0/0">
        <pre>R19#show int fa0/0
FastEthernet0/0 is up, line protocol is up
Hardware is DEC21140, address is ca02.7788.0000 (bia ca02.7788.0000)
Description: SALES_SUBNET
Internet address is 10.32.102.2/30
MTU 1500 bytes, BW 100000 Kbit/sec, DLY 100 usec,
 reliability 255/255, txload 1/255, rxload 1/255
Encapsulation ARPA, loopback not set
Keepalive set (60 sec)
Full-duplex, 100Mb/s, 100BaseTX/FX
ARP type: ARPA, ARP Timeout 04:00:00
Last input 00:00:01, output 00:00:00, output hang never
Last clearing of "show interface" counters never
Input queue: 0/300/0/0 (size/max/drops/flushes); Total output drops: 135298429
Queueing strategy: fifo
Output queue: 0/300 (size/max)
30 second input rate 0 bits/sec, 0 packets/sec
30 second output rate 0 bits/sec, 0 packets/sec
73310 packets input, 7101162 bytes
Received 73115 broadcasts (0 IP multicasts)
0 runts, 0 giants, 0 throttles
0 input errors, 4 CRC, 0 frame, 0 overrun, 0 ignored
0 watchdog
0 input packets with dribble condition detected
3927513096455 packets output, 14404034810952 bytes, 0 underruns
0 output errors, 11 collisions, 0 interface resets
0 unknown protocol drops
0 babbles, 0 late collision, 0 deferred
0 lost carrier, 0 no carrier
0 output buffer failures, 0 output buffers swapped out</pre>
    </div>""",
            "stem": "What is the cause of poor performance on router R19?",
            "name": "r19perf1",
            "correct": "C",
            "explain": "Correct. C \u2014 **Total output drops: 135298429** shows the transmit queue cannot keep up with traffic offered to the interface (**port oversubscription**/congestion). **Collisions** are only **11** on a **full-duplex** link, so **A** and **B** are unlikely. **CRC** errors are only **4** (**D**). Near-zero current rates with huge historical drops still point to sustained output-queue discards as the performance problem.",
            "choices": [
                "excessive collisions",
                "speed and duplex mismatch",
                "port oversubscription",
                "excessive CRC errors",
            ],
        },
        {
            "slug": "port-security-voip-mac-address-vlan-voice",
            "title": "CCNA — Port security MAC on voice VLAN",
            "stem": "An engineer is configuring a switch port that is connected to a VoIP handset. Which command must the engineer configure to enable port security with a manually assigned MAC address of abcd.abcd.abcd on voice VLAN 4?",
            "name": "psvoip1",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 With **`switchport voice vlan 4`**, a **static** secure MAC for the phone on the voice VLAN uses **`switchport port-security mac-address abcd.abcd.abcd vlan voice`**. The **voice** keyword targets the configured voice VLAN. **A** omits **vlan** and binds the MAC to the access VLAN. **B** can work numerically but **vlan voice** is the IOS form for IP-phone voice VLANs. **C** uses **sticky**, which is not a purely manual static entry.",
            "choices": [
                "switchport port-security mac-address abcd.abcd.abcd",
                "switchport port-security mac-address abcd.abcd.abcd vlan 4",
                "switchport port-security mac-address sticky abcd.abcd.abcd vlan 4",
                "switchport port-security mac-address abcd.abcd.abcd vlan voice",
            ],
        },
        {
            "slug": "wireless-encryption-protects-confidentiality-algorithm",
            "title": "CCNA — How wireless encryption protects the network",
            "stem": "How does encryption protect the wireless network?",
            "name": "wlanenc1",
            "correct": "C",
            "explain": "Correct. C \u2014 **Encryption** uses a cryptographic **algorithm** to scramble wireless frame data so only parties that share the keys (typically the **AP** and **client**) can decrypt and read it. **A** describes **integrity** checking (detecting forgery/tampering), which complements encryption but is not encryption itself. **B** misstates the role of ciphers\u2014they provide confidentiality, not zero-day detection. **D** describes **access control/policy** (who may associate), not encryption.",
            "choices": [
                "via integrity checks to identify wireless forgery attacks in the frame",
                "via specific ciphers to detect and prevent zero-day network attacks",
                "via an algorithm to change wireless data so that only the access point and client understand it",
                "via a policy to prevent unauthorized users from communicating on the wireless network",
            ],
        },
        {
            "slug": "firewall-segregates-zones-security-policies",
            "title": "CCNA — Firewall security zones",
            "stem": "Which device segregates a network into separate zones that have their own security policies?",
            "name": "fwzone1",
            "correct": "B",
            "explain": "Correct. B \u2014 A **firewall** divides the network into **security zones** (for example inside, outside, DMZ) and applies **zone-based policies** controlling which traffic may pass between zones. An **IPS** analyzes traffic for threats but does not primarily define inter-zone policy boundaries. An **access point** provides wireless access. A **switch** segments VLANs at Layer 2; zone security policies with permit/deny between trust levels are a firewall function.",
            "choices": [
                "IPS",
                "firewall",
                "access point",
                "switch",
            ],
        },
        {
            "slug": "ssid-specification-case-sensitive",
            "title": "CCNA — SSID specification",
            "stem": "What is a specification for SSIDS?",
            "name": "ssidsp1",
            "correct": "D",
            "explain": "Correct. D \u2014 **SSIDs** (Service Set Identifiers) are **case sensitive**: **Office** and **office** are different wireless networks. They are an **IEEE 802.11** construct, not a Cisco-only feature (**A**). There is no requirement for one number and one letter (**B**). An SSID names a WLAN; **VLAN assignment** is configured separately on the WLC/switch (**C**), not defined by the SSID string alone.",
            "choices": [
                "They are a Cisco proprietary security feature.",
                "They must include one number and one letter.",
                "They define the VLAN on a switch.",
                "They are case sensitive.",
            ],
        },
        {
            "slug": "private-ipv4-reason-security-breach-risk",
            "title": "CCNA — Reason for IPv4 private addressing",
            "stem": "What is a reason to implement IPv4 private addressing?",
            "name": "priv4reason1",
            "correct": "A",
            "explain": "Correct. A \u2014 **RFC 1918 private** addresses are not routable on the public Internet; with **NAT** at the edge, internal hosts are not directly reachable from outside, which can **reduce exposure** and breach risk. **Conserving public IPv4** is another major reason (see related items on the site). Private addressing is **not** driven by **PCI** (**B**) or **local law** (**C**). It does **not** shrink router **forwarding tables**\u2014internal routers still hold routes for private prefixes (**D**).",
            "choices": [
                "Reduce the risk of a network security breach",
                "Comply with PCI regulations",
                "Comply with local law",
                "Reduce the size of the forwarding table on network routers",
            ],
        },
        {
            "slug": "ftp-fact-two-connections-control-data",
            "title": "CCNA — FTP fact: control and data connections",
            "stem": "Which is a fact related to FTP?",
            "name": "ftpfact1",
            "correct": "D",
            "explain": "Correct. D \u2014 **FTP** uses **two TCP connections**: a **control** channel (commands, well-known port **21**) and a separate **data** channel for file transfer (active or passive mode). **Block numbers** describe **TFTP** over UDP (**A**). FTP supports **USER/PASS** authentication; it does not always operate without auth (**B**). **UDP port 69** is **TFTP**, not FTP (**C**).",
            "choices": [
                "It uses block numbers to identify and mitigate data-transfer errors",
                "It always operates without user authentication",
                "It relies on the well-known UDP port 69.",
                "It uses two separate connections for control and data traffic",
            ],
        },
        {
            "slug": "ap-admin-auth-tacacs-radius-choose-two",
            "title": "CCNA — AP admin authentication protocols (choose two)",
            "stem": "Which two protocols are used by an administrator for authentication and configuration on access points? (Choose two)",
            "name": "apaaa1",
            "choose_two": True,
            "correct": ["D", "E"],
            "explain": "Correct. D and E \u2014 **TACACS+** and **RADIUS** are **AAA** protocols used for **administrator** login, authorization, and accounting on WLCs and access points (and other network devices). **802.1X** (**C**) authenticates **clients** joining the LAN/WLAN, not AP management sessions. **802.1Q** (**B**) is **VLAN tagging**. **Kerberos** (**A**) is used in Windows domains, not the standard AP management AAA pair on CCNA.",
            "choices": [
                "Kerberos",
                "802.1Q",
                "802.1x",
                "TACACS+",
                "RADIUS",
            ],
        },
        {
            "slug": "nat-partial-config-outside-interface-cpe1",
            "title": "CCNA — Complete partial NAT: outside interface",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="CPE1 NAT show commands">
        <pre>CPE1# show protocols e0/1
Ethernet0/1 is up, line protocol is up
  Internet address is 10.0.12.2/24

CPE1#show ip access-list LAN
Standard IP access list LAN
 10 permit 10.0.12.0, wildcard bits 0.0.0.255

CPE1# show ip nat translations

CPE1# show ip nat statistics

Total active translations: 0 (0 static, 0 dynamic, 0 extended)
Peak translations: 0
Outside interfaces:
Inside interfaces:
 Ethernet0/1
Hits: 0  Misses: 0
...
Dynamic mappings:
-- Inside Source
[Id: 1] access-list LAN pool NATPOOL refcount 0
 pool NATPOOL: netmask 255.255.255.0
  start 198.51.100.11 end 198.51.100.20</pre>
    </div>""",
            "stem": "What is the next step to complete the implementation for the partial NAT configuration shown?",
            "name": "natpart1",
            "correct": "B",
            "explain": "Correct. B \u2014 **Inside** NAT is bound to **Ethernet0/1**, the **ACL LAN** and **pool NATPOOL** are defined, but **Outside interfaces:** is **empty**. Apply **`ip nat outside`** on the Internet-facing interface so translations can occur. There is no static NAT overlap to fix (**A**). The ACL already matches **10.0.12.0/24** on **e0/1** (**C**). The ACL is already tied to the dynamic mapping (**access-list LAN pool NATPOOL**); it is not applied to the pool definition itself (**D**).",
            "choices": [
                "Reconfigure the static NAT entries that overlap the NAT pool",
                "Configure the NAT outside interface",
                "Modify the access list for the internal network on e0/1",
                "Apply the ACL to the pool configuration",
            ],
        },
        {
            "slug": "ipv4-private-address-conserve-global-unique",
            "title": "CCNA — IPv4 address type conserves global addresses",
            "stem": "Which type of IPv4 address type helps to conserve the globally unique address classes?",
            "name": "privtype1",
            "correct": "B",
            "explain": "Correct. B \u2014 **Private** IPv4 addresses (**RFC 1918**: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) are reused inside organizations so every host does not need a **public**, globally unique address; **NAT** at the edge is commonly used with private space. **Multicast** is for group delivery. **Loopback** is for local logical host identification on a router. **Public** addresses are the scarce globally unique pool that private addressing helps preserve.",
            "choices": [
                "multicast",
                "private",
                "loopback",
                "public",
            ],
        },
        {
            "slug": "route-192-168-12-16-longest-prefix-ospf",
            "title": "CCNA — Route to 192.168.12.16 (LPM)",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="Routing table entries">
        <pre>EIGRP: 192.168.12.0/24
RIP: 192.168.12.0/27
OSPF: 192.168.12.0/28</pre>
    </div>""",
            "stem": "How does the router manage traffic to 192.168.12.16?",
            "name": "rt12161",
            "correct": "A",
            "explain": "Correct. A \u2014 **192.168.12.16** is in **192.168.12.0/27** (RIP) but **not** in **192.168.12.0/28** (that block is **.0\u2013.15** only). Among routes that match, **/27** is longer than EIGRP **/24**, so **RIP** wins. The router does **not** load-balance across different prefix lengths (**B**). **OSPF /28** does not include **.16** (**C**). **Administrative distance** (**D**) applies only when prefix lengths tie.",
            "choices": [
                "It selects the RIP route because it has the longest prefix inclusive of the destination address.",
                "It load-balances traffic between all three routes.",
                "It chooses the OSPF route because it has the longest prefix inclusive of the destination address.",
                "It chooses the EIGRP route because it has the lowest administrative distance.",
            ],
        },
        {
            "slug": "ipv6-floating-default-route-cpe-nd",
            "title": "CCNA — IPv6 floating static default route",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="CPE show ipv6 route">
        <pre>CPE# show ipv6 route
...
ND ::/0 [2/0]
     via FE80::A8BB:CCFF:FE00:200, Ethernet0/0
NDp 2001:DB8:1234:1::/64 [2/0]
     via Ethernet0/0, directly connected
C 2001:DB8:1234:2::/64 [0/0]
     via Ethernet0/1, directly connected</pre>
    </div>""",
            "stem": "The administrator must configure a floating static default route that points to 2001:db8:1234:2::1 and replaces the current default route only if it fails. Which command must the engineer configure on the CPE?",
            "name": "v6float1",
            "correct": "B",
            "mono": True,
            "explain": "Correct. B \u2014 The current default is **ND ::/0** with administrative distance **2**. A **floating** backup static must use a **higher** AD so it is used only if the primary fails: **`ipv6 route ::/0 2001:db8:1234:2::1 3`**. AD **2** (**A**) does not float above the existing default. **::/128** (**C**) is not the IPv6 default prefix. AD **1** (**D**) would be preferred over the ND default, not act as backup.",
            "choices": [
                "ipv6 route ::/0 2001:db8:1234:2::1 2",
                "ipv6 route ::/0 2001:db8:1234:2::1 3",
                "ipv6 route ::/128 2001:db8:1234:2::1 3",
                "ipv6 route ::/0 2001:db8:1234:2::1 1",
            ],
        },
        {
            "slug": "private-ipv4-benefit-shield-internal-devices",
            "title": "CCNA — Benefit of private IPv4 addressing",
            "stem": "What is the benefit of using private IPv4 addressing?",
            "name": "privben1",
            "correct": "C",
            "explain": "Correct. C \u2014 **Private** addresses are not routable on the public Internet; with **NAT** at the edge, internal hosts are not directly reachable from outside, which **shields** internal devices from unsolicited external access. **A** describes general connectivity, not a private-address benefit. **B** is wrong\u2014secure Internet connectivity uses mechanisms such as **VPN/TLS**, not private RFC 1918 space alone. **D** is incorrect\u2014private addresses are **not** intended to be routable on external networks.",
            "choices": [
                "to provide reliable connectivity between like devices",
                "to enable secure connectivity over the Internet",
                "to shield internal network devices from external access",
                "to be routable over an external network",
            ],
        },
        {
            "slug": "qos-policing-drops-exceed-committed-rate",
            "title": "CCNA — QoS policing vs shaping",
            "stem": "Which QoS feature drops traffic that exceeds the committed access rate?",
            "name": "qospol1",
            "correct": "D",
            "explain": "Correct. D \u2014 **Policing** enforces a rate (such as **committed access rate**) and typically **drops** or **remarks** traffic that exceeds the limit. **Shaping** (**C**) **buffers** excess traffic to smooth output rather than immediately drop it. **WFQ** (**A**) is a **queuing** algorithm for fair scheduling. **FIFO** (**B**) forwards in arrival order without rate enforcement.",
            "choices": [
                "weighted fair queuing",
                "FIFO",
                "shaping",
                "policing",
            ],
        },
        {
            "slug": "trunk-dot1q-allowed-vlans-1-10",
            "title": "CCNA — Trunk 802.1Q VLANs 1-10",
            "stem": "Two switches have been implemented and all interfaces are at the default configuration level. A trunk link must be implemented between two switches with these requirements:\n+ using an industry-standard trunking protocol\n+ permitting VLANs 1-10 and denying other VLANs\n\nHow must the interconnecting ports be configured?",
            "name": "trunk110",
            "correct": "B",
            "mono": True,
            "explain": "Correct. B \u2014 **802.1Q (dot1q)** is the industry-standard trunk encapsulation. **`switchport mode trunk`**, **`switchport trunk encapsulation dot1q`**, and **`switchport trunk allowed vlan 1-10`** meet the requirements. **A** sets **native vlan 11**, which is unnecessary and can cause mismatch/issues when only **1\u201310** are allowed. **C** uses **ISL** (Cisco-proprietary), **DTP desirable**, and **EtherChannel**, not asked. **D** omits explicit **trunk**/**dot1q** and adds **LACP** channeling not required.",
            "choices": [
                "switchport mode trunk\nswitchport trunk allowed vlans 1-10\nswitchport trunk native vlan 11",
                "switchport mode trunk\nswitchport trunk encapsulation dot1q\nswitchport trunk allowed vlans 1-10",
                "switchport mode dynamic desirable\nchannel-group 1 mode desirable\nswitchport trunk encapsulation isl\nswitchport trunk allowed vlan except 11-4094",
                "switchport mode dynamic\nchannel-protocol lacp\nswitchport trunk allowed vlans 1-10",
            ],
        },
        {
            "slug": "network-automation-consistent-configuration-state",
            "title": "CCNA — Why implement network automation",
            "stem": "Why would a network administrator choose to implement automation in a network environment?",
            "name": "netauto1",
            "correct": "B",
            "explain": "Correct. B \u2014 **Automation** (templates, APIs, tools such as Ansible or Python scripts) helps keep **consistent configuration** across many devices, reduces manual errors, and speeds repeatable changes. **A** describes inventory/documentation storage, not the main automation driver. **C** is **management-plane** architecture, not automation itself. **D** is **AAA** (RADIUS/TACACS+), not network configuration automation.",
            "choices": [
                "to centralize device information storage",
                "to simplify the process of maintaining a consistent configuration state across all devices",
                "to deploy the management plane separately from the rest of the network",
                "to implement centralized user account management",
            ],
        },
        {
            "slug": "vrrp-multivendor-default-gateway-redundancy",
            "title": "CCNA — VRRP for multivendor FHRP",
            "stem": "When deploying a new network that includes both Cisco and third-party network devices, which redundancy protocol avoids the interruption of network traffic if the default gateway router fails?",
            "name": "vrrpmv1",
            "correct": "B",
            "explain": "Correct. B \u2014 **VRRP** is an **open standard** (RFC-based) first-hop redundancy protocol supported on **Cisco and third-party** gear, so a shared virtual default gateway can fail over without long interruption. **HSRP** and **GLBP** are **Cisco-proprietary** (GLBP also Cisco-focused). **FHRP** (**A**) is the **category** name (HSRP/VRRP/GLBP), not a single protocol you configure on devices.",
            "choices": [
                "FHRP",
                "VRRP",
                "HSRP",
                "GLBP",
            ],
        },
        {
            "slug": "ssh-username-ccuser-secret-encrypted",
            "title": "CCNA — SSH local user with secret password",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="Partial R1 SSH configuration">
        <pre>Router#conf t
R1(config)#ip domain-name CC-Net.com
R1(config)#enable secret Passfornewuser
R1(config)#line vty 0 15
R1(config-line)#transport input ssh
R1(config-line)#login local</pre>
    </div>""",
            "stem": "A network administrator is configuring a router for user access via SSH. The service-password encryption command has been issued. The configuration must meet these requirements:\n\n\u2013 Create the username as CCUser.\n\u2013 Create the password as NA!2$cc.\n\u2013 Encrypt the user password.\n\nWhat must be configured to meet the requirements?",
            "name": "sshccu1",
            "correct": "C",
            "mono": True,
            "explain": "Correct. C \u2014 **`username CCUser secret NA!2$cc`** stores the password as a **hashed secret** (not cleartext in the running config), which satisfies **encrypt the user password** with **`login local`** on VTY lines. **`password`** alone relies on weak Type 7 scrambling when **service password-encryption** is on. **`enable secret`** is separate from the SSH user account. **A**, **B**, and **D** mix incorrect **enable** password forms or omit **`secret**`.",
            "choices": [
                "username CCUser password NA!2$cc\nenable password level 5 NA!2$cc",
                "username CCUser privilege 15 password NA!2$cc\nenable secret 0 NA!2$cc",
                "username CCUser secret NA!2$cc",
                "username CCUser privilege 10 password NA!2$cc",
            ],
        },
        {
            "slug": "route-172-16-4-0-subnet-mask-slash-21",
            "title": "CCNA — Subnet mask for 172.16.4.0/21",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="R1 show ip route">
        <pre>R1# show ip route | begin Gateway
Gateway of last resort is 0.0.0.0 to network 0.0.0.0
S*   0.0.0.0/0 is directly connected, Serial0/0/1
     172.16.0.0/16 is variably subnetted, 4 subnets, 2 masks
C       172.16.2.0/24 is directly connected, GigabitEthernet0/0
C       172.16.4.0/21 is directly connected, Serial0/0/1</pre>
    </div>""",
            "stem": "What is the subnet mask for route 172.16.4.0?",
            "name": "mask1724",
            "correct": "B",
            "explain": "Correct. B \u2014 The routing table shows **172.16.4.0/21**, which is mask **255.255.248.0** (/21 = 255.255.248.0). **255.255.254.0** is **/23**. **255.255.240.0** is **/20**. **255.255.255.192** is **/26**.",
            "choices": [
                "255.255.255.192",
                "255.255.248.0",
                "255.255.254.0",
                "255.255.240.0",
            ],
        },
        {
            "slug": "wlc-management-interface-inband-ap-admin",
            "title": "CCNA — WLC management interface",
            "stem": "Which interface or port on the WLC is the default for in-band device administration and communications between the controller and access points?",
            "name": "wlcmgmt1",
            "correct": "B",
            "explain": "Correct. B \u2014 The **management interface** is the default **in-band** path for WLC administration (GUI/CLI over the network) and **CAPWAP** communication with lightweight APs. The **service port** is for **out-of-band** management. The **console port** is local serial access only. The **virtual interface** supports functions such as DHCP relay and guest services, not default controller\u2013AP control traffic.",
            "choices": [
                "virtual interface",
                "management interface",
                "console port",
                "service port",
            ],
        },
        {
            "slug": "wlc-fast-ssid-change-multiple-wlans",
            "title": "CCNA — Fast SSID Change on WLC",
            "stem": "A company has each office using wireless access with multiple SSIDs while limiting roaming capabilities, covering different locations on the internal office LAN, guest networks, and BYOD access for employees. Which change must be enabled to improve the customer experience during SSID changes?",
            "name": "wlcfastssid1",
            "correct": "D",
            "explain": "Correct. D \u2014 **Fast SSID Change** on the WLC removes the default delay when a client moves between **SSIDs/WLANs**, improving the experience when users switch networks (for example corporate, guest, or BYOD). **Fast Transition** (**B**, 802.11r) speeds **roaming between APs** on the **same** WLAN, not SSID changes. **Assisted Roaming Prediction Optimization** (**A**) and **Neighbor List Dual Band** (**C**) target AP handoff and band steering, not inter-SSID transitions.",
            "choices": [
                "Assisted Roaming Prediction Optimization",
                "Fast Transition",
                "Neighbor List Dual Band",
                "Fast SSID Change",
            ],
        },
        {
            "slug": "vpn-dmvpn-getvpn-branch-scale-choose-two",
            "title": "CCNA — VPN for branch scale (choose two)",
            "stem": "Which two VPN technologies are recommended by Cisco for multiple branch offices and large-scale deployments? (Choose two)",
            "name": "vpnbranch1",
            "choose_two": True,
            "correct": ["D", "E"],
            "explain": "Correct. D and E \u2014 **DMVPN** scales hub-and-spoke and dynamic spoke-to-spoke tunnels for many branch sites without configuring every pairwise link. **GETVPN** uses group keying for large site-to-site deployments (often over private/MPLS cores). **Site-to-site VPN** alone does not scale as well at very large branch counts. **IPsec remote access** and **clientless VPN** target remote users, not large branch-to-branch designs.",
            "choices": [
                "IPsec remote access",
                "site-to-site VPN",
                "clientless VPN",
                "GETVPN",
                "DMVPN",
            ],
        },
        {
            "slug": "json-test-questions-three-arrays-count",
            "title": "CCNA — JSON: count arrays",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="JSON exhibit">
        <pre>{
    "Test_Questions" : [
             "Automation",
             "Configuration"
    ],
    "Test_Exam_Level" : [
             "CCNA",
             "CCNP"
    ],
    "Test_Response" : [
             "Correct",
             "Incorrect"
    ]
}</pre>
    </div>""",
            "stem": "How many arrays are present in the JSON data?",
            "name": "jsonarr1",
            "correct": "B",
            "explain": "Correct. B \u2014 The root is one **JSON object** (`{ }`) with three properties. Each property\u2019s value is an **array** (`[ ]`): **Test_Questions**, **Test_Exam_Level**, and **Test_Response** \u2014 **three arrays** total. The strings inside are **values**, not arrays. **One** (A) counts only the root or misreads structure; **six** (C) and **nine** (D) confuse elements with arrays or objects.",
            "choices": [
                "one",
                "three",
                "six",
                "nine",
            ],
        },
        {
            "slug": "router1-eth1-collisions-duplex-mismatch",
            "title": "CCNA — Ethernet1 collisions (duplex mismatch)",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="Router1 show interface Ethernet1">
        <pre>Router1#show interface ethernet 1
Ethernet1 is up, line protocol is up
...
5 minute input rate 1000 bits/sec, 2 packets/sec
5 minute output rate 0 bits/sec, 0 packets/sec
...
15 input errors, 14278 CRC, 0 frame, 0 overrun, 3 ignored
...
0 output errors, 15000 collisions, 0 interface resets
0 babbles, 0 late collision, 179 deferred</pre>
    </div>""",
            "stem": "An administrator received a call from a branch office regarding poor application performance hosted at the headquarters. Ethernet 1 is connected between Router1 and the LAN switch. What identifies the issue?",
            "name": "eth1dup1",
            "correct": "A",
            "explain": "Correct. A \u2014 **15,000 collisions** and **179 deferred** frames on an otherwise up 10 Mb/s Ethernet link are classic signs of a **duplex mismatch** (or speed/duplex autonegotiation failure), which hurts LAN performance. **MTU 1500** is normal (**B**). **5-minute rates** and **zero output drops** do not show sustained over-utilization or RED drops (**C**, **D**). CRC errors can accompany bad cabling but the collision/deferred pattern points to duplex.",
            "choices": [
                "There is a duplex mismatch.",
                "The MTU is not set to the default value.",
                "The link is over utilized.",
                "The QoS policy is dropping traffic.",
            ],
        },
        {
            "slug": "sw1-pagp-group2-lacp-active-multivendor",
            "title": "CCNA — EtherChannel LACP with another vendor",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="SW1 show etherchannel">
        <pre>SW1#show etherchannel
             Channel-group listing:
             ----------------------
Group: 2
--------
Group state = L2
Ports: 1 Maxports = 8
Port-channels: 1 Max Portchannels = 1
Protocol: PAGP</pre>
    </div>""",
            "stem": "A network engineer updates the existing configuration on interface FastEthernet1/1 on switch SW1. It must establish an EtherChannel by using the same group designation with another vendor switch. Which configuration must be performed to complete the process?",
            "name": "sw1ec2mv1",
            "mono": True,
            "correct": "D",
            "explain": "Correct. D \u2014 **Group 2** currently uses **PAgP** (Cisco-only). A **non-Cisco** switch needs **LACP** (IEEE 802.3ad). Apply **channel-group 2 mode active** on **FastEthernet1/1** so SW1 negotiates with LACP. **A** and **C** use **desirable**/**auto** (PAgP) on **port-channel** (wrong interface and protocol). **B** uses **mode on** (static, no LACP PDUs), which is a poor match for standard multi-vendor LACP.",
            "choices": [
                "interface port-channel 2\nchannel-group 2 mode desirable",
                "interface fastethernet 1/1\nchannel-group 2 mode on",
                "interface port-channel 2\nchannel-group 2 mode auto",
                "interface fastethernet 1/1\nchannel-group 2 mode active",
            ],
        },
        {
            "slug": "forward-172-31-0-1-longest-prefix-25",
            "title": "CCNA — Longest match 172.31.0.1 (/25)",
            "stem": "A packet from a company\u2019s branch office is destined to host 172.31.0.1 at headquarters. The sending router has three possible matches in its routing table for the packet: prefixes 172.31.0.0/16, 172.31.0.0/24, and 172.31.0.0/25. How does the router handle the packet?",
            "name": "lpm3101",
            "correct": "C",
            "explain": "Correct. C \u2014 The router uses **longest-prefix match** among routes that contain the destination. **172.31.0.1** matches **/16**, **/24**, and **/25**; **172.31.0.0/25** is the **most specific** (covers **172.31.0.0\u2013172.31.0.127**). **/24** (B) and **/16** (A) are shorter matches. The **default route** (A) is used only when **no** more-specific route matches.",
            "choices": [
                "It sends the traffic via the default gateway 0.0.0.0/0.",
                "It sends the traffic via prefix 172.31.0.0/16.",
                "It sends the traffic via prefix 172.31.0.0/25.",
                "It sends the traffic via prefix 172.31.0.0/24.",
            ],
        },
        {
            "slug": "password-protection-special-chars-max-length",
            "title": "CCNA — Password protection best practice",
            "stem": "Which action must be taken when password protection is implemented?",
            "name": "pwprot1",
            "correct": "C",
            "explain": "Correct. C \u2014 Strong password policy uses **length** (as long as the system allows) plus **complexity** (mixed case, digits, **special characters**). **A** stores secrets insecurely with weak authentication. **B** violates **confidentiality** and least privilege (passwords must not be shared). **D** recommends **short** passwords, which weakens security even if complexity rules exist.",
            "choices": [
                "Store passwords as contacts on a mobile device with single-factor authentication.",
                "Share passwords with senior IT management to ensure proper oversight.",
                "Include special characters and make passwords as long as allowed.",
                "Use less than eight characters in length when passwords are complex.",
            ],
        },
        {
            "slug": "ap-join-wlc-discovery-request-ap-manager",
            "title": "CCNA — AP discovery request to AP-Manager",
            "stem": "When an access point is seeking to join a wireless LAN controller, which message is sent to the AP-Manager interface?",
            "name": "apdisc1",
            "correct": "D",
            "explain": "Correct. D \u2014 A lightweight AP locates a WLC using **CAPWAP discovery**: the AP sends a **discovery request** to candidate controllers (including the **AP-Manager** interface). The WLC replies with a **discovery response** (**C** is from WLC to AP, not to AP-Manager from the AP). **DHCP discover/request** (**A**, **B**) may obtain an IP address but are not the CAPWAP join discovery message to the AP-Manager interface.",
            "choices": [
                "DHCP request",
                "DHCP discover",
                "discovery response",
                "discovery request",
            ],
        },
        {
            "slug": "network-automation-reduce-config-inconsistencies",
            "title": "CCNA — Automated network management benefit",
            "stem": "What is a reason why an administrator would choose to implement an automated network management approach?",
            "name": "netauto2",
            "correct": "A",
            "explain": "Correct. A \u2014 **Automation** (templates, APIs, orchestration tools) applies the same configuration model across devices, which **reduces inconsistencies** and manual errors. **B** is the opposite goal (automation lowers recurring operational cost). **C** describes manual **box-by-box** CLI work, not automation. **D** is unrelated to network configuration automation.",
            "choices": [
                "Reduce inconsistencies in the network configuration.",
                "Increase recurrent management costs.",
                "Enable \u201cbox by box\u201d configuration and deployment.",
                "Decipher simple password policies.",
            ],
        },
        {
            "slug": "device-separates-security-domains-firewall",
            "title": "CCNA — Device separates security domains",
            "stem": "Which device separates networks by security domains?",
            "name": "secdom1",
            "correct": "B",
            "explain": "Correct. B \u2014 A **firewall** enforces **security domains** (zones) such as inside, outside, and DMZ, with policies controlling traffic between them. An **IPS** (**C**) inspects for attacks but does not primarily define inter-domain boundaries. An **access point** (**A**) provides wireless access. A **wireless controller** (**D**) manages APs and WLANs, not zone-based security policy between network domains.",
            "choices": [
                "access point",
                "firewall",
                "intrusion protection system",
                "wireless controller",
            ],
        },
        {
            "slug": "vm-characteristics-independent-same-hardware",
            "title": "CCNA — VM characteristics (choose two)",
            "stem": "Which two characteristics are representative of virtual machines (VMs)? (Choose two.)",
            "name": "vmchar1",
            "choose_two": True,
            "correct": ["D", "E"],
            "explain": "Correct. D and E \u2014 VMs are **isolated guests**: each **runs independently** on the hypervisor, and **many VMs share the same physical host** (CPU, memory, storage, NICs). **A** is wrong: VMs need **virtual switching/network config** to reach each other; they are not automatically interconnected. **B** is wrong: the hypervisor **allocates** resources by policy, not necessarily **equally**. **C** is wrong: the guest **OS does not depend on a specific hypervisor brand**; it runs on virtual hardware the hypervisor presents.",
            "choices": [
                "A VM on a hypervisor is automatically interconnected to other VMs.",
                "A VM on an individual hypervisor shares resources equally.",
                "Each VM\u2019s operating system depends on its hypervisor.",
                "Each VM runs independently of any other VM in the same hypervisor.",
                "Multiple VMs operate on the same underlying hardware.",
            ],
        },
        {
            "slug": "r7-show-ip-route-default-eigrp-ex-null0",
            "title": "CCNA — R7 routing table validation",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="R7 show ip route">
        <pre>R7#show ip route
172.22.0.0/24 is subnetted, 1 subnets
D 172.22.49.0 [90/284160] via 10.81.22.2, 04:55:53, FastEthernet0/0
10.0.0.0/8 is variably subnetted, 26 subnets, 5 masks
D EX 10.10.10.10/32 [170/35840] via 10.3.5.1, 04:55:55, FastEthernet0/1
D 10.9.1.0/30 [90/33280] via 10.3.5.1, 04:55:56, FastEthernet0/1
B 10.111.99.0/24 [20/0] via 10.6.25.2, 03:58:52
D 10.14.3.0/30 [90/30720] via 10.3.5.1, 04:55:58, FastEthernet0/1
C 10.9.4.0/30 is directly connected, FastEthernet1/0
B 10.100.100.0/24 [20/0] via 10.6.25.2, 03:58:53
D 10.0.1.0/30 [90/30720] via 10.3.5.1, 04:55:58, FastEthernet0/1
D EX 10.10.10.70/32 [170/161280] via 10.3.5.1, 04:55:57, FastEthernet0/1
B 10.90.0.0/16 [200/0] via 0.0.0.0, 03:57:59, Null0
D EX 10.90.1.0/24 [170/158720] via 10.3.5.1, 04:55:57, FastEthernet0/1
D EX 10.90.2.0/24 [170/158720] via 10.3.5.1, 04:55:57, FastEthernet0/1
D 10.90.3.0/29 [90/161280] via 10.3.5.1, 02:46:03, FastEthernet0/1
D EX 10.90.3.0/24 [170/158720] via 10.3.5.1, 02:46:04, FastEthernet0/1
D EX 10.90.4.0/24 [170/158720] via 10.3.5.1, 04:55:59, FastEthernet0/1
D EX 10.90.5.0/24 [170/158720] via 10.3.5.1, 04:55:59, FastEthernet0/1
B* 0.0.0.0/0 [20/0] via 10.6.25.2, 02:22:38</pre>
    </div>""",
            "stem": "According to the output, which parameter set is validated using the routing table of R7?",
            "name": "r7rtval1",
            "correct": "D",
            "explain": "Correct. D \u2014 **B* 0.0.0.0/0** shows R7 has a **gateway of last resort** (not missing). **D EX** routes are **EIGRP external** (redistributed **into** EIGRP). For **10.90.8.0/24**, there is no more-specific route; longest match is **B 10.90.0.0/16 \u2026 Null0**, so R7 **drops** that traffic. **A/B** wrongly claim no default. **C** misstates EIGRP redistribution and claims the packet would be forwarded.",
            "choices": [
                "R7 is missing a gateway of last resort. R7 is receiving routes that were redistributed from BGP. R7 will forward traffic destined to 10.90.8.0/24.",
                "R7 is missing a gateway of last resort. R7 is receiving routes that were redistributed in EIGRP. R7 will forward traffic destined to 10.90.8.0/24.",
                "R7 has a gateway of last resort available. R7 is receiving routes that were redistributed from BGP. R7 will drop traffic destined to 10.90.8.0/24.",
                "R7 has a gateway of last resort available. R7 is receiving routes that were redistributed in EIGRP. R7 will drop traffic destined to 10.90.8.0/24.",
            ],
        },
        {
            "slug": "show-ip-route-172-16-3-254-slash-23-mask",
            "title": "CCNA — Destination mask for 172.16.3.254",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="Router show ip route">
        <pre>Gateway of last resort is 172.16.2.2 to network 0.0.0.0

   10.0.0.0/8 is variably subnetted, 2 subnets, 2 masks
C       10.10.10.0/24 is directly connected, GigabitEthernet0/0/0
L       10.10.10.3/32 is directly connected, GigabitEthernet0/0/0
   172.16.0.0/16 is variably subnetted, 3 subnets, 2 masks
S       172.16.1.33/32 is directly connected, GigabitEthernet0/0/1
C       172.16.2.0/23 is directly connected, GigabitEthernet0/0/1
L       172.16.2.1/32 is directly connected, GigabitEthernet0/0/1
S*   0.0.0.0/0 [1/0] via 172.16.2.2</pre>
    </div>""",
            "stem": "A packet sourced from 10.10.10.1 is destined for 172.16.3.254. What is the subnet mask of the destination route?",
            "name": "rtmask2",
            "correct": "B",
            "explain": "Correct. B \u2014 **172.16.3.254** matches the connected route **172.16.2.0/23** (range **172.16.2.0\u2013172.16.3.255**). A **/23** mask is **255.255.254.0**. **172.16.1.33/32** does not match. The **default** (**A**, **0.0.0.0**) is not used because a longer match exists. **C** is **/24**; **D** is a **host /32**.",
            "choices": [
                "0.0.0.0",
                "255.255.254.0",
                "255.255.255.0",
                "255.255.255.255",
            ],
        },
        {
            "slug": "rapid-pvst-backup-port-blocking-designated",
            "title": "CCNA — Rapid PVST+ backup port role",
            "stem": "What is the operating mode and role of a backup port on a shared LAN segment in Rapid PVST+?",
            "name": "rpvstbp1",
            "correct": "A",
            "explain": "Correct. A \u2014 On a **shared LAN**, if a switch has two ports into the same segment, one becomes **designated** and the other becomes a **backup port** in **blocking/discarding** mode, providing a redundant path toward the **designated bridge** on that segment. An **alternate port** (**B**) is the blocked alternate toward the **root**, not a backup on shared media. **Root/designated** ports (**C**, **D**) **forward**; **listening/learning** (**B**, **D**) are transitional states, not the backup role.",
            "choices": [
                "blocking mode and provides an alternate path toward the designated bridge",
                "listening mode and provides an alternate path toward the root bridge",
                "forwarding mode and provides the lowest-cost path to the root bridge for each VLAN",
                "learning mode and provides the shortest path toward the root bridge handling traffic away from the LAN",
            ],
        },
        {
            "slug": "wlc-sip-cac-media-snooping-platinum-qos",
            "title": "CCNA — WLC SIP CAC next steps (choose two)",
            "stem": "SIP-based Call Admission Control must be configured in the Cisco WLC GUI. SIP call-snooping ports are configured. Which two actions must be completed next? (Choose two.)",
            "name": "sipcac1",
            "choose_two": True,
            "correct": ["B", "D"],
            "explain": "Correct. B and D \u2014 After **SIP call-snooping ports**, enable **Media Session Snooping** on the **WLAN** and set WLAN **QoS to Platinum** for **voice** traffic so SIP CAC can admit and prioritize calls. **A** (**silver or greater**) is not the required voice policy. **C** (separate data/voice QoS roles) is not the standard pair of next GUI steps here. **E** (LAN traffic shaping) is unrelated to completing SIP CAC on the WLAN.",
            "choices": [
                "Set the QoS level to silver or greater for voice traffic",
                "Enable Media Session Snooping on the WLAN",
                "Configure two different QoS roles for data and voice traffic",
                "Set the QoS level to platinum for voice traffic",
                "Enable traffic shaping for the LAN interface of the WLC",
            ],
        },
        {
            "slug": "wpa3-personal-psk-ccmp128-cipher",
            "title": "CCNA — WPA3-Personal PSK cipher",
            "stem": "A network engineer is implementing a corporate SSID for WPA3-Personal security with a PSK. Which encryption cipher must be configured?",
            "name": "wpa3psk1",
            "correct": "D",
            "explain": "Correct. D \u2014 On Cisco WLC WLAN security, **WPA3-Personal** with **PSK** uses **AES (CCMP128)** for frame encryption with **SAE** authentication (not legacy WPA2-PSK alone). **GCMP256** (**B**) targets **WPA3-Enterprise 192-bit** / Wi\u2011Fi\u202f7 SAE-EXT-KEY deployments, not standard Personal PSK. **GCMP128** (**A**) is used with **Suite\u202fB** enterprise AKMs. **CCMP256** (**C**) is an enterprise Suite\u202fB option, not the Personal PSK cipher.",
            "choices": [
                "GCMP128",
                "GCMP256",
                "CCMP256",
                "CCMP128",
            ],
        },
        {
            "slug": "dna-center-sdn-automation-controller-function",
            "title": "CCNA — Cisco DNA Center functionality",
            "stem": "What is the functionality of the Cisco DNA Center?",
            "name": "dnafunc1",
            "correct": "B",
            "explain": "Correct. B \u2014 **Cisco DNA Center** is a **software-defined network controller** for **automation** of Cisco devices and services: design, provisioning, policy, assurance, and APIs from a central platform. **A** mislabels it as a **data center** policy controller only. **C** describes a **console server**, not DNA Center. **D** describes **IPAM/scheduling**, not its role.",
            "choices": [
                "data center network policy controller",
                "software-defined controller for automation of devices and services",
                "console server that permits secure access to all network devices",
                "IP address pool distribution scheduler",
            ],
        },
        {
            "slug": "qos-marking-changes-dscp-ipv4-header",
            "title": "CCNA — QoS marking changes DSCP",
            "stem": "Which IP header field is changed by a Cisco device when QoS marking is enabled?",
            "name": "qosdscp1",
            "correct": "C",
            "explain": "Correct. C \u2014 **QoS marking** on Cisco devices sets or rewrites the **DSCP** value in the IPv4 **Differentiated Services** byte (for example **set dscp**). **Type of Service** (**B**) is the legacy name for the whole byte, not the specific field Cisco configures today. **ECN** (**D**) signals congestion; it is not the primary QoS class mark. **Header Checksum** (**A**) may be recalculated when the header changes but is not the QoS field being marked.",
            "choices": [
                "Header Checksum",
                "Type of Service",
                "DSCP",
                "ECN",
            ],
        },
        {
            "slug": "router-y-route-10-227-225-255-via-router-d",
            "title": "CCNA — Router-Y LPM to 10.227.225.255",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="Router-Y show ip route">
        <pre>Router-Y#show ip route
...
Gateway of last resort is not set

10.0.0.0/8 is variably subnetted
B       10.0.0.0/8 [1/0] via 10.224.1.2
B       10.27.150.224/27 [20/0] via 10.224.1.3, 1w6d
S       10.128.0.0/9 [1/0] via 10.224.1.3
B       10.224.0.0/11 [20/0] via 10.224.1.5, 5d18h
B       10.224.0.0/15 [20/0] via 10.224.1.4, 5d18h
C       10.223.0.0/24 is directly connected, GigabitEthernet0/1
C       10.224.0.0/24 is directly connected, GigabitEthernet0/0
B       10.226.34.0/24 [20/0] via 10.224.1.5, 5d18h</pre>
    </div>
    <p class="study-meta">On Router-Y, <strong>GigabitEthernet0/0</strong> (10.224.0.0/24) reaches neighbors: <strong>10.224.1.2</strong> = router A, <strong>.1.3</strong> = router B, <strong>.1.4</strong> = router C, <strong>.1.5</strong> = router D.</p>""",
            "stem": "PC A is communicating with another device at IP address 10.227.225.255. Through which router does router Y route the traffic?",
            "name": "ryroute1",
            "correct": "D",
            "explain": "Correct. D \u2014 **10.227.225.255** matches several routes, but **longest-prefix match** selects **10.224.0.0/11** (range **10.224.0.0\u201310.231.255.255**), next hop **10.224.1.5** = **router D**. **10.128.0.0/9** via router B (**10.224.1.3**) is shorter than **/11**. **10.224.0.0/15** via router C does not contain **10.227.x**. **10.0.0.0/8** via router A is least specific.",
            "choices": [
                "router A",
                "router B",
                "router C",
                "router D",
            ],
        },
        {
            "slug": "ipsec-suite-protocols-ah-esp-choose-two",
            "title": "CCNA — IPsec suite protocols (choose two)",
            "stem": "What are two protocols within the IPsec suite? (Choose two.)",
            "name": "ipsecpro1",
            "choose_two": True,
            "correct": ["B", "C"],
            "explain": "Correct. B and C \u2014 **IPsec** defines two core security **protocols**: **AH** (Authentication Header) and **ESP** (Encapsulating Security Payload). **IKE** negotiates keys but is separate from this list. **3DES** and **AES** (**A**, **E**) are **encryption algorithms** used inside ESP, not IPsec protocols themselves. **TLS** (**D**) secures many applications (for example HTTPS) and is **not** part of the IPsec protocol suite.",
            "choices": [
                "3DES",
                "AH",
                "ESP",
                "TLS",
                "AES",
            ],
        },
        {
            "slug": "private-ipv4-benefits-reuse-conserve-choose-two",
            "title": "CCNA — Private IPv4 benefits (choose two)",
            "stem": "What are two benefits of private IPv4 addressing? (Choose two.)",
            "name": "privben1",
            "choose_two": True,
            "correct": ["A", "C"],
            "explain": "Correct. A and C \u2014 **RFC 1918 private** space lets the same **10/8**, **172.16/12**, and **192.168/16** ranges be **reused at many sites** without consuming more **globally unique** public IPv4. **B** is wrong: Internet reachability uses **public** addresses and usually **NAT**, not private space alone. **D** is wrong: private prefixes are **not** advertised to the public Internet. **E** is false: private ranges are **limited**, not unlimited.",
            "choices": [
                "reuses addresses at multiple sites",
                "provides external internet network connectivity",
                "conserves globally unique address space",
                "propagates routing information to WAN links",
                "provides unlimited address ranges",
            ],
        },
        {
            "slug": "sw1-vty-ssh-crypto-rsa-key-choose-two",
            "title": "CCNA — SW1 enable SSH (choose two)",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="SW1 show run and crypto key">
        <pre>SW1#show run
...
ip domain-name test
username CCNA privilege 1 password 0 ciscol23
...
line vty 0 4
 login local
 transport input telnet
line vty 5 15
 login local
 transport input telnet

SW1#show crypto key mypubkey rsa
Key name: SW1.test</pre>
    </div>""",
            "stem": "An engineer is updating the management access configuration of switch SW1 to allow secured, encrypted remote configuration. Which two commands or command sequences must the engineer apply to the switch? (Choose two.)",
            "name": "sw1ssh1",
            "choose_two": True,
            "mono": True,
            "correct": ["A", "B"],
            "explain": "Correct. A and B \u2014 **SSH** requires an **RSA** key pair (**crypto key generate rsa**, with **ip domain-name** already set) and **transport input ssh** on **VTY** lines instead of **telnet**. **C** configures a **trunk**, unrelated to management encryption. **D** sets the **enable** secret, not VTY SSH. **E** adds another **username** but does not enable **SSH** transport or keys by itself.",
            "choices": [
                "SW1(config)#line vty 0 15\nSW1(config-line)#transport input ssh",
                "SW1(config)# crypto key generate rsa",
                "SW1(config)# interface f0/1\nSW1(config-if)# switch port mode trunk",
                "SW1(config)#enable secret ccnaTest123",
                "SW1(config)# username NEW secret R3mote123",
            ],
        },
        {
            "slug": "json-switch-property-name-is-key",
            "title": "CCNA — JSON key vs value (switch)",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="JSON exhibit">
        <pre>[
  {"switch": "3750", "port": "e2"},
  {"router": "2951", "port": "e20"},
  {"switch": "3750", "port": "e23"}
]</pre>
    </div>""",
            "stem": "Refer to the exhibit. What is represented by the word \u201cswitch\u201d in line 2 of the JSON schema?",
            "name": "jsonkey1",
            "correct": "B",
            "explain": "Correct. B \u2014 On line 2, **\"switch\"** is the **property name** (JSON **key**) in an **object**; **\"3750\"** is its **value**. The outer `[ ]` is an **array** of objects. **\"switch\"** is not itself an **object**, **value**, or **array**.",
            "choices": [
                "object",
                "key",
                "value",
                "array",
            ],
        },
        {
            "slug": "1000base-sx-gbic-sfp-lc-sc-patch-cable",
            "title": "CCNA — 1000BASE-SX GBIC to SFP cable",
            "stem": "Which cable type must be used to interconnect one switch using 1000 BASE-SX GBIC modules and another switch using 1000 BASE-SX SFP modules?",
            "name": "sxlcsc1",
            "correct": "B",
            "explain": "Correct. B \u2014 **1000BASE-SX** uses **multimode fiber**. Legacy **GBIC** SX optics typically terminate with **SC**; **SFP** SX modules use **LC**. A switch-to-switch link needs an **LC-to-SC** patch (or equivalent adapter pair), not LC-LC or SC-SC on both ends. **SC-to-ST** (**D**) is the wrong connector pairing for this GBIC/SFP mix.",
            "choices": [
                "LC to LC",
                "LC to SC",
                "SC to SC",
                "SC to ST",
            ],
        },
        {
            "slug": "wlc-distribution-lag-channel-group-active",
            "title": "CCNA — WLC LAG channel-group mode",
            "stem": "Which channel-group mode must be configured when multiple distribution switch interfaces connected to a WLC are bundled?",
            "name": "wlclagmode1",
            "correct": "A",
            "explain": "Correct. A \u2014 **WLC LAG** uses **IEEE 802.3ad LACP**. On the **distribution switch**, member ports use **channel-group mode active** so the bundle negotiates with the controller. **mode on** (**B**) is static EtherChannel without LACP. **desirable** (**C**) is **PAgP**. **passive** (**D**) is LACP passive and is not the required mode on the switch side for this WLC LAG design.",
            "choices": [
                "channel-group mode active",
                "channel-group mode on",
                "channel-group mode desirable",
                "channel-group mode passive",
            ],
        },
        {
            "slug": "subnet-mask-binary-11111000-slash-29",
            "title": "CCNA — Binary mask to /29",
            "stem": "A network engineer must configure an interface with IP address 10.10.10.145 and a subnet mask equivalent to 11111111.11111111.11111111.11111000. Which subnet mask must the engineer use?",
            "name": "binmask1",
            "correct": "C",
            "explain": "Correct. C \u2014 **11111111.11111111.11111111.11111000** has **29** network bits (**/29**), dotted decimal **255.255.255.248**. **/27** (**A**) is **255.255.255.224**. **/28** (**B**) is **255.255.255.240**. **/30** (**D**) is **255.255.255.252** (**11111100**).",
            "choices": [
                "/27",
                "/28",
                "/29",
                "/30",
            ],
        },
        {
            "slug": "dns-resolver-authoritative-name-resolution-choose-two",
            "title": "CCNA — DNS server types (choose two)",
            "stem": "Which two server types support domain name to IP address resolution? (Choose two.)",
            "name": "dnstype1",
            "choose_two": True,
            "correct": ["C", "D"],
            "explain": "Correct. C and D \u2014 **DNS** maps names to addresses using **resolvers** (recursive queries for clients) and **authoritative** servers (official zone records). An **ESX host** (**A**) is virtualization, not a DNS role. A **web** server (**B**) serves HTTP/HTTPS. **File transfer** (**E**) describes FTP/SFTP-style services, not DNS resolution.",
            "choices": [
                "ESX host",
                "web",
                "resolver",
                "authoritative",
                "file transfer",
            ],
        },
        {
            "slug": "switch-mac-address-aging-removes-stale",
            "title": "CCNA — MAC address aging",
            "stem": "Which switching feature removes unused MAC addresses from the MAC address table, which allows new MAC addresses to be added?",
            "name": "macage1",
            "correct": "B",
            "explain": "Correct. B \u2014 **MAC address aging** deletes CAM entries that are inactive for the **aging time**, freeing space so **dynamic learning** can add new MACs. **Dynamic learning** (**C**) **adds** entries when frames arrive; it does not remove stale ones. **MAC move** (**A**) updates a MAC seen on a different port. **Auto purge** (**D**) is not standard Cisco terminology for this mechanism.",
            "choices": [
                "MAC move",
                "MAC address aging",
                "dynamic MAC address learning",
                "MAC address auto purge",
            ],
        },
        {
            "slug": "sdn-northbound-apis-soap-rest-choose-two",
            "title": "CCNA — SDN northbound APIs (choose two)",
            "stem": "Which two northbound APIs are found in a software-defined network? (Choose two.)",
            "name": "nbapi2",
            "choose_two": True,
            "correct": ["A", "C"],
            "explain": "Correct. A and C \u2014 **Northbound** APIs connect **applications/orchestration** to the **SDN controller**; **REST** and **SOAP** are common styles. **OpenFlow** (**E**) and **OpFlex** (**B**) are **southbound** (controller to devices). **NETCONF** (**D**) is typically **southbound** for device programmability (with RESTCONF variants).",
            "choices": [
                "SOAP",
                "OpFlex",
                "REST",
                "NETCONF",
                "OpenFlow",
            ],
        },
        {
            "slug": "rest-http-messages-transfer-applications",
            "title": "CCNA — REST uses HTTP messages",
            "stem": "What uses HTTP messages to transfer data to applications residing on different hosts?",
            "name": "resthttp1",
            "correct": "A",
            "explain": "Correct. A \u2014 **REST** APIs use **HTTP** (or HTTPS) **request/response messages** (GET, POST, PUT, DELETE, and so on) so applications on different hosts exchange data. **OpenStack** (**B**) is a cloud platform that may *use* REST but is not defined by HTTP messaging itself. **OpFlex** (**C**) and **OpenFlow** (**D**) are **southbound** device/control protocols, not HTTP application APIs.",
            "choices": [
                "REST",
                "OpenStack",
                "OpFlex",
                "OpenFlow",
            ],
        },
        {
            "slug": "switch-unknown-unicast-flooding-except-ingress",
            "title": "CCNA — Switch frame flooding",
            "stem": "A switch is forwarding a frame out of all interfaces except the interface that received the frame. What is the technical term for this process?",
            "name": "swflood1",
            "correct": "C",
            "explain": "Correct. C \u2014 **Flooding** sends a frame out **every port in the VLAN except the ingress port**, typically when the destination MAC is **unknown** or for **broadcast/multicast** flooding rules. **CDP** (**A**) is neighbor discovery. **Multicast** (**B**) is a destination class, not this forwarding behavior name. **ARP** (**D**) resolves IP to MAC, not switch egress to all ports.",
            "choices": [
                "CDP",
                "multicast",
                "flooding",
                "ARP",
            ],
        },
        {
            "slug": "rsa-asymmetric-encryption-characteristic",
            "title": "CCNA — RSA characteristic",
            "stem": "What is a characteristic of RSA?",
            "name": "rsa1",
            "correct": "B",
            "explain": "Correct. B \u2014 **RSA** is an **asymmetric** (public/private key) algorithm used for key exchange, digital signatures, and encrypting small data blocks. **Preshared** or **identical keys on both sides** (**A**, **C**) describe **symmetric** or PSK models. **Symmetric decryption** (**D**) is not RSA\u2019s role.",
            "choices": [
                "It uses preshared keys for encryption",
                "It is an asymmetric encryption algorithm",
                "It requires both sides to have identical keys for encryption",
                "It is a symmetric decryption algorithm.",
            ],
        },
        {
            "slug": "dna-center-assurance-correlates-protocol-insights",
            "title": "CCNA — DNA Center network assurance advantage",
            "stem": "Which advantage does the network assurance capability of Cisco DNA Center provide over traditional campus management?",
            "name": "dnaassur1",
            "correct": "B",
            "explain": "Correct. B \u2014 **Network assurance** in **DNA Center** **correlates** telemetry and data from multiple sources (SNMP, NetFlow, APIs, and similar) to produce **health insights** and baselines, while **traditional** campus work often needs **manual CLI** collection and analysis. **A** overstates **YANG/NETCONF** as the defining assurance difference and **CLI-only** traditional tools. **C** narrows assurance to **security posture** comparison. **D** misstates assurance as offloading tasks via a **data backbone**.",
            "choices": [
                "Cisco DNA Center leverages YANG and NETCONF to assess the status of fabric and nonfabric devices, and traditional campus management uses CLI exclusively",
                "Cisco DNA Center correlates information from different management protocols to obtain insights, and traditional campus management requires manual analysis",
                "Cisco DNA Center automatically compares security postures among network devices, and traditional campus management needs manual comparisons",
                "Cisco DNA Center handles management tasks at the controller to reduce the load on infrastructure devices, and traditional campus management uses the data backbone.",
            ],
        },
        {
            "slug": "signal-frequency-1hz-sixty-per-minute",
            "title": "CCNA — 1 Hz equals 60 per minute",
            "stem": "Which signal frequency appears 60 times per minute?",
            "name": "sigfreq1",
            "correct": "A",
            "explain": "Correct. A \u2014 **Hertz (Hz)** is **cycles per second**. **1 Hz** = **1 cycle/s** \u00d7 **60 s/min** = **60 cycles/min**. **60 Hz** (**C**) is **60 cycles per second** (3,600/min), like AC power in many regions. **1 GHz** and **60 GHz** (**B**, **D**) are radio bands far above 1 Hz.",
            "choices": [
                "1 Hz signal",
                "1 GHz signal",
                "60 Hz signal",
                "60 GHz signal",
            ],
        },
        {
            "slug": "lap-local-mode-wired-access-port",
            "title": "CCNA — LAP local mode switchport",
            "stem": "Which port type does a lightweight AP use to connect to the wired network when it is configured in local mode?",
            "name": "laplocal1",
            "correct": "A",
            "explain": "Correct. A \u2014 In **local mode**, client traffic is **tunneled in CAPWAP** to the WLC, so the AP uplink usually needs only **one VLAN** (management/CAPWAP) on the switch\u2014an **access** port. A **trunk** (**B**) is typical when the AP must carry **multiple VLANs** locally (for example **FlexConnect** with local switching and 802.1Q tagging). **EtherChannel** and **LAG** (**C**, **D**) aggregate links; they do not replace access vs trunk for VLAN behavior.",
            "choices": [
                "access",
                "trunk",
                "EtherChannel",
                "LAG",
            ],
        },
        {
            "slug": "cat9300-gi1-0-1-trunk-match-native-321",
            "title": "CCNA — Match Cat9300 Gi1/0/1 trunk",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "A network administrator configures an interface on a new switch so that it connects to interface Gi1/0/1 on switch Cat9300-1. Which configuration must be applied to the new interface?",
            "name": "cat9300tr1",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 Cat9300-1 **Gi1/0/1** is an operational **802.1Q trunk** with **native VLAN 321** and **allowed VLANs 100, 200, and 300** only. The new port needs **switchport mode trunk**, **switchport trunk native vlan 321**, and **switchport trunk allowed vlan 100,200,300**. **A** uses **100-300**, a **range** that permits every VLAN from 100 through 300, not just those three IDs. **B** uses **dynamic desirable** instead of an explicit trunk and is a weaker match when the peer is administratively **trunk**. **C** configures **access** VLAN 321, **nonegotiate**, and invalid **except** syntax\u2014not a trunk toward this link.",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="Cat9300-1 show interface g1/0/1 switchport">
        <pre>Cat9300-1# show interface g1/0/1 switchport
Name: Gi1/0/1
Switchport: Enabled
Administrative Mode: trunk
Operational Mode: trunk
Administrative Trunking Encapsulation: dot1q
Operational Trunking Encapsulation: dot1q
Negotiation of Trunking: On
Access Mode VLAN: 1 (default)
Trunking Native Mode VLAN: 321 (VLAN0321)
Administrative Native VLAN tagging: enabled
Trunking VLANs Enabled: 100,200,300
Pruning VLANs Enabled: 2-1001</pre>
      </div>""",
            "choices": [
                """switchport trunk encapsulation dot1q
switchport trunk native vlan 321
switchport trunk allowed vlan 100-300""",
                """switchport mode dynamic desirable
switchport trunk native vlan 321
switchport trunk allowed vlan 100,200,300""",
                """switchport nonegotiate
switchport access vlan 321
switchport trunk allowed vlan except 2-1001""",
                """switchport mode trunk
switchport trunk native vlan 321
switchport trunk allowed vlan 100,200,300""",
            ],
        },
        {
            "slug": "sdn-controller-packet-handling-policies",
            "title": "CCNA — SDN controller sets policies",
            "stem": "What is the function of a controller in a software-defined network?",
            "name": "sdnctrlpol1",
            "correct": "B",
            "explain": "Correct. B \u2014 The **SDN controller** is the **control plane**: it defines **packet-handling policies** (flows, routes, ACLs) and programs switches/routers via southbound APIs. **Forwarding packets** (**C**) is the **data plane**. **Multicast replication at the hardware level** (**A**) and **fragmenting/reassembling packets** (**D**) are forwarding-stack or end-system tasks, not the controller\u2019s primary role.",
            "choices": [
                "multicast replication at the hardware level",
                "setting packet-handling policies",
                "forwarding packets",
                "fragmenting and reassembling packets",
            ],
        },
        {
            "slug": "server-fcs-err-physical-cable-fault",
            "title": "CCNA — FCS-Err and unreliable throughput",
            "stem": "A client experiences slow throughput from a server that is directly connected to the core switch in a data center. A network engineer finds minimal latency on connections to the server, but data transfers are unreliable, and the output of the show interfaces counters errors command shows a high FCS-Err count on the interface that is connected to the server. What is the cause of the throughput issue?",
            "name": "fcserr1",
            "correct": "B",
            "explain": "Correct. B \u2014 **FCS-Err** (frame check sequence errors) means frames arrived **corrupted** at Layer 1/2, so they are discarded and transfers look **unreliable** despite low latency. That pattern points to a **physical cable fault** (bad cable, connector, or transceiver). **High bandwidth usage** (**A**) causes congestion, not typically a rising FCS count. A **speed mismatch** (**C**) more often shows collisions, runts, or link flaps. A **cable that is too long** (**D**) can degrade signal, but the exam pairing of **high FCS-Err** with unreliable throughput on a direct attach is **physical fault**.",
            "choices": [
                "high bandwidth usage",
                "a physical cable fault",
                "a speed mismatch",
                "a cable that is too long",
            ],
        },
        {
            "slug": "hypervisor-distributes-physical-resources-vm",
            "title": "CCNA — Hypervisor allocates VM resources",
            "stem": "Which component controls and distributes physical resources for each virtual machine?",
            "name": "hypres1",
            "correct": "C",
            "explain": "Correct. C \u2014 The **hypervisor** abstracts the host\u2019s CPU, memory, storage, and NICs and **allocates** those **physical resources** to each **VM**. The **OS** (**B**) runs inside a guest VM and does not schedule hardware for other VMs. The **physical enclosure** (**A**) is the chassis. The **CPU** (**D**) is hardware the hypervisor virtualizes\u2014it is not the control component that distributes resources across VMs.",
            "choices": [
                "physical enclosure",
                "OS",
                "hypervisor",
                "CPU",
            ],
        },
        {
            "slug": "wlc-config-network-webmode-http-access",
            "title": "CCNA — WLC HTTP web access",
            "stem": "Which command enables HTTP access to the Cisco WLC?",
            "name": "wlcweb1",
            "correct": "C",
            "mono": True,
            "explain": "Correct. C \u2014 **config network webmode enable** turns on **web-based management** (HTTP GUI access) on the WLC. **config network secureweb enable** (**A**) enables **HTTPS** (secure web), not plain HTTP. **config certificate generate webadmin** (**B**) creates a certificate for secure web administration. **config network telnet enable** (**D**) enables **Telnet**, not HTTP.",
            "choices": [
                "config network secureweb enable",
                "config certificate generate webadmin",
                "config network webmode enable",
                "config network telnet enable",
            ],
        },
        {
            "slug": "loopback-ipv4-mapped-ipv6-prefix-128",
            "title": "CCNA — Loopback IPv6 /128 from /32 IPv4",
            "stem": "A network engineer must migrate a router loopback interface to the IPv6 address space. If the current IPv4 address of the interface is 10.54.73.1/32, and the engineer configures IPv6 address 0:0:0:0:0:ffff:a36:4901, which prefix length must be used?",
            "name": "lbv6128",
            "correct": "D",
            "explain": "Correct. D \u2014 An IPv4 **loopback** host address uses **/32** (one address). The IPv6 equivalent for a single interface address is **/128**. The configured address is **IPv4-mapped IPv6** (::ffff:10.54.73.1 \u2192 **0:0:0:0:0:ffff:a36:4901**). **/64** (**A**) is the usual prefix for LANs/SLAAC, not a loopback host. **/96** (**B**) relates to the mapped IPv4 layout, not the loopback prefix you apply on the interface. **/124** (**C**) is a small subnet prefix, not a single-host loopback.",
            "choices": [
                "/64",
                "/96",
                "/124",
                "/128",
            ],
        },
        {
            "slug": "wlc-console-port-oob-async-management",
            "title": "CCNA — WLC console port purpose",
            "stem": "What is the primary purpose of a console port on a Cisco WLC?",
            "name": "wlccon1",
            "correct": "B",
            "explain": "Correct. B \u2014 The **console port** provides **out-of-band** access over an **asynchronous** serial link (RJ-45/USB console) for initial setup, troubleshooting, and recovery when in-band IP paths fail. **In-band management via IP transport** (**D**) describes the **management interface** (GUI/SSH/HTTPS and CAPWAP on the production network). **Out-of-band via IP transport** (**A**) fits the dedicated **service port** (Ethernet OOB), not the serial console. **In-band via asynchronous transport** (**C**) is not a valid WLC management model.",
            "choices": [
                "out-of-band management via an IP transport",
                "out-of-band management via an asynchronous transport",
                "in-band management via an asynchronous transport",
                "in-band management via an IP transport",
            ],
        },
        {
            "slug": "fhrp-protects-default-gateway-failure",
            "title": "CCNA — FHRP protects default gateway",
            "stem": "What does the implementation of a first-hop redundancy protocol protect against on a network?",
            "name": "fhrpprot1",
            "correct": "B",
            "explain": "Correct. B \u2014 **FHRPs** (HSRP, VRRP, GLBP) provide a **redundant default gateway** (virtual IP/MAC) so hosts keep reachability if the active router fails. **BGP neighbor flapping** (**A**) is a routing-protocol stability issue. **Root-bridge loss** (**C**) is an STP role change. **Spanning-tree loops** (**D**) are prevented by **STP/RSTP**, not FHRP.",
            "choices": [
                "BGP neighbor flapping",
                "default gateway failure",
                "root-bridge loss",
                "spanning-tree loops",
            ],
        },
        {
            "slug": "forward-192-168-0-55-static-24-gi0-1",
            "title": "CCNA — Forward 192.168.0.55 longest /24",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "Which interface is chosen to forward traffic to the host at 192.168.0.55?",
            "name": "fwd0551",
            "correct": "A",
            "explain": "Correct. A \u2014 The router uses **longest-prefix match**. **192.168.0.55** matches **192.168.0.0/16** (EIGRP), **192.168.0.0/23** (OSPF), and **192.168.0.0/24** (static); **/24** is most specific, so traffic uses **via 10.0.12.2** on connected **10.0.12.0/24** \u2192 **GigabitEthernet0/1**. **GigabitEthernet0/2** (**D**) is the **/16** EIGRP path. **GigabitEthernet0/3** (**C**) is the **/23** OSPF path. **Null0** (**B**) applies only to the **default** route **0.0.0.0/0**, not **192.168.0.55**.",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="show ip route output">
        <pre>Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       + - replicated route, % - next hop override, p - overrides from PfR
Gateway of last resort is 0.0.0.0 to network 0.0.0.0
S*   0.0.0.0/0 is directly connected, Null0
      10.0.0.0/8 is variably subnetted, 6 subnets, 2 masks
C     10.0.12.0/24 is directly connected, GigabitEthernet0/1
L     10.0.12.1/32 is directly connected, GigabitEthernet0/1
C     10.0.13.0/24 is directly connected, GigabitEthernet0/2
L     10.0.13.1/32 is directly connected, GigabitEthernet0/2
C     10.0.14.0/24 is directly connected, GigabitEthernet0/3
L     10.0.14.1/32 is directly connected, GigabitEthernet0/3
D     192.168.0.0/16 [90/130816] via 10.0.13.3, 00:10:09, GigabitEthernet0/2
O     192.168.0.0/23 [110/2] via 10.0.14.4, 00:00:46, GigabitEthernet0/3
S     192.168.0.0/24 [100/0] via 10.0.12.2</pre>
      </div>""",
            "choices": [
                "GigabitEthernet0/1",
                "Null0",
                "GigabitEthernet0/3",
                "GigabitEthernet0/2",
            ],
        },
        {
            "slug": "ospf-crossover-p2p-faster-full-adjacency",
            "title": "CCNA — OSPF P2P for faster FULL on crossover",
            "stem": "A Cisco engineer notices that two OSPF neighbors are connected using a crossover Ethernet cable. The neighbors are taking too long to become fully adjacent. Which command must be issued under the interface configuration on each router to reduce the time required for the adjacency to reach the FULL state?",
            "name": "ospfxp2p1",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 On **Ethernet**, OSPF defaults to **broadcast** network type, which runs **DR/BDR election** and a **Wait timer** (often ~40 s) before adjacency completes. A direct router-to-router **crossover** link should use **ip ospf network point-to-point** so OSPF skips DR/BDR election and reaches **FULL** faster. **ip ospf network broadcast** (**B**) keeps the default slow behavior. **ip ospf priority 0** (**A**) makes the router ineligible for DR/BDR but does not change the network type. **ip ospf dead-interval 40** (**C**) is the default dead interval on many OSPF networks and does not remove the broadcast Wait/DR delay.",
            "choices": [
                "ip ospf priority 0",
                "ip ospf network broadcast",
                "ip ospf dead-interval 40",
                "ip ospf network point-to-point",
            ],
        },
        {
            "slug": "json-test-schema-objects-keys-lists",
            "title": "CCNA — JSON objects, keys, and lists",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="JSON exhibit">
        <pre>{
    "Test_Questions" : [
                "Automation",
                "Configuration",
    ],
    "Test__Exam_Level" : [
                "CCNA",
                "CCNP",
    ],
    "Test_Response" : [
                "Correct",
                "Incorrect",
    ],
}</pre>
    </div>""",
            "stem": "Refer to the exhibit. How many objects, keys, and JSON list values are present?",
            "name": "jsoncnt1",
            "correct": "D",
            "explain": "Correct. D \u2014 The exhibit is **one JSON object** (`{ ... }`) with **three keys**: **Test_Questions**, **Test__Exam_Level**, and **Test_Response**. Each key\u2019s value is a **JSON array** (list), so there are **three JSON list values**. The strings inside each array are list **elements**, not separate top-level objects or keys.",
            "choices": [
                "three objects, three keys, and two JSON list values",
                "one object, three keys, and two JSON list values",
                "three objects, two keys, and three JSON list values",
                "one object, three keys, and three JSON list values",
            ],
        },
        {
            "slug": "p2p-leased-line-simple-configuration-benefit",
            "title": "CCNA — Point-to-point leased line benefit",
            "stem": "What is a benefit of a point-to-point leased line?",
            "name": "p2pleased1",
            "correct": "D",
            "explain": "Correct. D \u2014 A **point-to-point leased line** is a dedicated circuit between **two sites**, so WAN design and configuration stay **simple** (one link, fixed bandwidth, no shared-cloud routing complexity). **Full-mesh** (**A**) needs many circuits between every pair of sites and is costly. **Flexibility of design** (**B**) fits technologies such as **MPLS** or **Internet VPN**, not a fixed P2P lease. **Low cost** (**C**) is wrong\u2014leased lines are typically **more expensive** than broadband or VPN options.",
            "choices": [
                "full-mesh capability",
                "flexibility of design",
                "low cost",
                "simplicity of configuration",
            ],
        },
        {
            "slug": "wpa2-wpa3-differences-sae-128-192-choose-two",
            "title": "CCNA — WPA2 vs WPA3 (choose two)",
            "stem": "What are two differences between WPA2 and WPA3 wireless security? (Choose two)",
            "name": "wpa23diff1",
            "choose_two": True,
            "correct": ["A", "B"],
            "explain": "Correct. A and B \u2014 **WPA3-Personal** uses **SAE** for key establishment, which is stronger against offline guessing than **WPA2-PSK**; **WPA2** still relies on **AES-CCMP** for over-the-air encryption. **WPA3** adds stronger options, including **192-bit** security mode (Suite B) in addition to common **128-bit** operation, while typical **WPA2** deployments use **128-bit** keys. **C** reverses SAE and AES roles. **D** is wrong: **WPA2** uses **AES**, not **TKIP**, as the standard cipher. **E** misstates key sizes (**192-bit** is not the WPA2 norm, and WPA3 does not require **256-bit** for all deployments).",
            "choices": [
                "WPA3 uses SAE for stronger protection than WPA2, which uses AES",
                "WPA2 uses 128-bit key encryption, and WPA3 supports 128-bit and 192-bit key encryption",
                "WPA3 uses AES for stronger protection than WPA2, which uses SAE",
                "WPA3 uses AES for stronger protection than WPA2, which uses TKIP",
                "WPA2 uses 192-bit key encryption, and WPA3 requires 256-bit key encryption",
            ],
        },
        {
            "slug": "syslog-transport-tcp-udp-choose-two",
            "title": "CCNA — Syslog transport protocols (choose two)",
            "stem": "Which two transport layer protocols carry syslog messages? (Choose two)",
            "name": "syslogtr1",
            "choose_two": True,
            "correct": ["A", "B"],
            "explain": "Correct. A and B \u2014 **Syslog** commonly uses **UDP** port **514**; **TCP** is also used (for example **TCP 601** or reliable syslog transports). **ARP** (**C**) resolves Layer 2 addresses and is not a transport protocol. **RTP** (**D**) carries real-time media, not syslog. **IP** (**E**) is **Layer 3** (network layer), not transport layer.",
            "choices": [
                "TCP",
                "UDP",
                "ARP",
                "RTP",
                "IP",
            ],
        },
        {
            "slug": "internet-default-route-ad-1-from-10-10-10-32",
            "title": "CCNA — Default route AD for Internet",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "A packet sourced from 10.10.10.32 is destined for the Internet. What is the administrative distance for the destination route?",
            "name": "defrtad1",
            "correct": "B",
            "explain": "Correct. B \u2014 Traffic to the **Internet** uses the **default route** **0.0.0.0/0** (\u201cgateway of last resort\u201d). The table shows **`S* 0.0.0.0/0 [1/0] via 172.16.2.2`**; in **`[AD/metric]`** format, the **administrative distance is 1** (default for a **static** route). **0** (**A**) is the metric on that line, not the AD. **2** (**C**) and **32** (**D**) are not the AD for this installed default.",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="Router show ip route">
        <pre>Gateway of last resort is 172.16.2.2 to network 0.0.0.0

    10.0.0.0/8 is variably subnetted, 3 subnets, 3 masks
       10.10.100.0/26 is directly connected, GigabitEthernet0/0/6
C      10.10.10.0/24 is directly connected, GigabitEthernet0/0/0
L      10.10.10.3/32 is directly connected, GigabitEthernet0/0/0
    172.16.0.0/16 is variably subnetted, 3 subnets, 2 masks
S      172.16.1.33/32 is directly connected, GigabitEthernet0/0/1
C      172.16.2.0/23 is directly connected, GigabitEthernet0/0/1
L      172.16.2.1/32 is directly connected, GigabitEthernet0/0/1
S*  0.0.0.0/0 [1/0] via 172.16.2.2</pre>
    </div>""",
            "choices": [
                "0",
                "1",
                "2",
                "32",
            ],
        },
        {
            "slug": "http-put-method-update-resource",
            "title": "CCNA — HTTP PUT method",
            "stem": "When is the PUT method used within HTTP?",
            "name": "httpput1",
            "correct": "A",
            "explain": "Correct. A \u2014 **PUT** **updates or replaces** a resource at a known URI in **REST/HTTP** APIs (for example Cisco DNA Center Intent API). Cisco exam wording may say **update a DNS server** to mean **update an existing server resource** via HTTP; DNS itself normally uses the **DNS protocol**, not HTTP PUT. **B** describes **GET** (read-only). **C** describes **GET** (retrieve/display content). **D** is wrong for PUT: **POST** is commonly used when a **nonidempotent** operation is needed; **PUT** is **idempotent** (repeating the same PUT has the same effect).",
            "choices": [
                "to update a DNS server",
                "when a read-only operation is required",
                "to display a web site",
                "when a nonidempotent operation is needed",
            ],
        },
        {
            "slug": "northbound-rest-api-application-facing-http",
            "title": "CCNA — Northbound REST API for SDN",
            "stem": "What describes a northbound REST API for SDN?",
            "name": "nbrest1",
            "correct": "B",
            "explain": "Correct. B \u2014 **Northbound** APIs face **applications and orchestration** above the controller. **REST** northbound APIs commonly use **HTTP methods** such as **GET, POST, PUT, and DELETE**. **A** and **C** describe **southbound** (network-element-facing) interfaces toward the **control/data** infrastructure, not the application plane. **D** is wrong: northbound is not limited to **SNMP GET**; REST uses the full set of HTTP verbs.",
            "choices": [
                "network-element-facing interface for the control and data planes",
                "application-facing interface for GET, POST, PUT, and DELETE methods",
                "network-element-facing interface for GET, POST, PUT, and DELETE methods",
                "application-facing interface for SNMP GET requests",
            ],
        },
        {
            "slug": "forward-172-16-1-190-ospf-slash-29-via-35",
            "title": "CCNA — Next hop to 172.16.1.190",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "Load-balanced traffic is coming in from the WAN destined to a host at 172.16.1.190. Which next-hop is used by the router to forward the request?",
            "name": "fwd11901",
            "correct": "C",
            "explain": "Correct. C \u2014 The router uses **longest-prefix match**. **172.16.1.190** matches several routes, but **172.16.1.184/29** (range **172.16.1.184\u2013172.16.1.191**) is the **most specific**, so traffic uses **`O ... via 192.168.7.35`**. **172.16.1.0/28** via **192.168.7.7** (**B**) covers only **172.16.1.0\u2013172.16.1.15**. **172.16.3.0/24** via **192.168.7.4** (**A**) does not contain **172.16.1.190**. **172.16.1.3/32** via **192.168.7.40** (**D**) is a host route for **.3**, not **.190**.",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="R1 show ip route">
        <pre>R1# show ip route
Codes: C \u2014 connected, S \u2014 static, I \u2014 IGRP, R - RIP, M - mobile, B \u2014 BGP
       D \u2014 EIGRP, EX - EIGRP external, O \u2014 OSPF, IA \u2014 OSPF inter area
       N1 \u2014 OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 \u2014 OSPF external type 2, E \u2014 EGP
       i \u2014 IS-IS, L1 - IS-IS level-1, L2 \u2014 IS-IS level-2, * \u2014 candidate default
       U - per-user static route, o \u2014 ODR
Gateway of last resort is not set
C   172.16.0.0/16 is directly connected, Loopback0
    172.16.0/16 is variably subnetted, 4 subnets, 2 masks
O   172.16.1.3/32 [110/100] via 192.168.7.40, 00:39:08, Serial0
C   172.16.1.0/24 is directly connected, Serial0
O   172.16.1.184/29 [110/5] via 192.168.7.35, 00:39:08, Serial0
O   172.16.3.0/24 [110/10] via 192.168.7.4, 00:39:08, GigabitEthernet0/0
D   172.16.1.0/28 [90/10] via 192.168.7.7, 00:39:08, GigabitEthernet0/0</pre>
      </div>""",
            "choices": [
                "192.168.7.4",
                "192.168.7.7",
                "192.168.7.35",
                "192.168.7.40",
            ],
        },
        {
            "slug": "ospf-r2-dead-interval-40-match-r1-neighbor",
            "title": "CCNA — OSPF R2 dead-interval to match R1",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "The network engineer is configuring router R2 as a replacement router on the network. After the initial configuration is applied it is determined that R2 failed to show R1 as a neighbor. Which configuration must be applied to R2 to complete the OSPF configuration and enable it to establish the neighbor relationship with R1?",
            "name": "ospfr2nb1",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 **R1** uses **Hello 15** and **Dead 40**; **R2** shows **Hello 15** but **Dead 45**. OSPF neighbors require matching **hello** and **dead** timers on the link. **`ip ospf dead-interval 40`** on **R2 GigabitEthernet0/0/0** aligns the dead timer with **R1**. **Option A** changes hello to **10**, which still mismatches **R1\u2019s Hello 15**. **Option B** sets **router-id 192.168.1.2**, duplicating **R1\u2019s Router ID** (**192.168.1.2**). **Option C** places **192.168.1.0/24** in **area 2** while **R1** is in **area 0**.",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="R1 show ip ospf interface g0/0/0">
        <pre>R1#show ip ospf interface g0/0/0
GigabitEthernet0/0/0 is up, line protocol is up
  Internet address is 192.168.1.2/24, Area 0
  Process ID 1, Router ID 192.168.1.2, Network Type POINT-TO-POINT, Cost: 1
  Transmit Delay is 1 sec, State POINT-TO-POINT,
  Timer intervals configured, Hello 15, Dead 40, Wait 40, Retransmit 5
    Hello due in 00:00:08
  Index 1/1, flood queue length 0
  Next 0x0(0) /0x0(0)
  Last flood scan length is 1, maximum is 1
  Last flood scan time is 0 msec, maximum is 0 msec
  Suppress hello for 0 neighbor(s)</pre>
      </div>
      <div class="exhibit-router-cli" role="region" aria-label="R2 show ip ospf interface g0/0/0">
        <pre>R2#show ip ospf interface g0/0/0
GigabitEthernet0/0/0 is up, line protocol is up
  Internet address is 192.168.1.1/24, Area 0
  Process ID 1, Router ID 10.1.1.1, Network Type POINT-TO-POINT, Cost: 1
  Transmit Delay is 1 sec, State POINT-TO-POINT,
  Timer intervals configured, Hello 15, Dead 45, Wait 15, Retransmit 5
    Hello due in 00:00:11
  Index 1/1, flood queue length 0
  Next 0x0(0)/0x0(0)
  Last flood scan length is 1, maximum is 1
  Last flood scan time is 0 msec, maximum is 0 msec
  Suppress hello for 0 neighbor(s)</pre>
      </div>
    </div>""",
            "choices": [
                """R2(config)#interface g0/0/0
R2(config-if)#ip ospf hello-interval 10""",
                """R2(config)#router ospf 1
R2(config-router)#router-id 192.168.1.2""",
                """R2(config)#router ospf 1
R2(config-router)#network 192.168.1.0 255.255.255.0 area 2""",
                """R2(config)#interface g0/0/0
R2(config-if)#ip ospf dead-interval 40""",
            ],
        },
        {
            "slug": "ospf-neighbor-must-match-area-hello-choose-two",
            "title": "CCNA — OSPF neighbor matching values (choose two)",
            "stem": "Which two values must be matched on both routers in order to become OSPF neighbors? (Choose two)",
            "name": "ospfnbrmt1",
            "choose_two": True,
            "correct": ["A", "C"],
            "explain": "Correct. A and C \u2014 **Area ID** and **hello/dead intervals** must match on the link. **Authentication** (type and credentials), **stub/NSSA area flags**, and **interface MTU** must also match for a normal adjacency to complete (MTU mismatches often stall at **EXSTART**). **Router ID** must be **unique**, not identical. **Process ID** must be the **same** OSPF process on both sides of the adjacency, but the exam pair here is **area** and **timers**.",
            "choices": [
                "Area ID",
                "Router ID",
                "Hello and dead intervals",
                "OSPF reference bandwidth",
                "EIGRP autonomous system number",
                "SNMP community string",
            ],
        },
        {
            "slug": "ssh-remove-unnecessary-name-server-password-encryption",
            "title": "CCNA — Remove non-SSH commands (choose two)",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="CPE partial configuration">
        <pre>hostname CPE
service password-encryption
ip domain name ccna.cisco.com
ip name-server 198.51.100.210

crypto key generate rsa modulus 1024

username admin privilege 15 secret S0m3s3cr3t

line vty 0 4
 transport input ssh
 login local</pre>
    </div>""",
            "stem": "Refer to the exhibit. An engineer executed the script and added commands that were not necessary for SSH and now must remove the commands. Which two commands must be executed to correct the configuration? (Choose two)",
            "name": "sshrm1",
            "choose_two": True,
            "correct": ["C", "D"],
            "explain": "Correct. C and D \u2014 **SSH** needs **`ip domain-name`**, **`crypto key generate rsa`**, a **local user** (**`username` \u2026 `secret`**), **`transport input ssh`**, and **`login local`** (or AAA). **`ip name-server`** (**C**) is for **DNS**, not SSH. **`service password-encryption`** (**D**) only obfuscates passwords in the **show run** display; it is **not required** to enable SSH. Do **not** remove **`ip domain-name`** (**A**) or **`login local`** (**B**)\u2014they are required. **`hostname`** (**E**) is recommended but not the pair of unnecessary lines to undo here.",
            "choices": [
                "no ip domain name ccna.cisco.com",
                "no login local",
                "no ip name-server 198.51.100.210",
                "no service password-encryption",
                "no hostname CPE",
            ],
        },
        {
            "slug": "wlc-lag-increase-throughput-reason",
            "title": "CCNA — WLC LAG throughput benefit",
            "stem": "What is a reason to implement LAG on a Cisco WLC?",
            "name": "wlclagtp1",
            "correct": "B",
            "explain": "Correct. B \u2014 **LAG** bundles multiple **distribution** links into one logical path so the WLC gains **higher aggregate throughput** and **link redundancy**. **A** is wrong: LAG members need **matching** Layer 2 settings on the switch. **C** describes **WLC high availability** (for example **SSO**), not LAG on distribution ports. **D** is wrong: LAG does not **encrypt management frames**.",
            "choices": [
                "Enable the connected switch ports to use different Layer 2 configurations.",
                "Increase the available throughput on the link.",
                "Allow for stateful failover between WLCs.",
                "Increase security by encrypting management frames.",
            ],
        },
        {
            "slug": "wlc-oob-management-service-console-choose-two",
            "title": "CCNA — WLC OOB port types (choose two)",
            "stem": "What are two port types used by a Cisco WLC for out-of-band management? (Choose two)",
            "name": "wlcoob1",
            "choose_two": True,
            "correct": ["C", "E"],
            "explain": "Correct. C and E \u2014 **Service port** provides **out-of-band** IP management on a dedicated Ethernet interface. **Console** provides **out-of-band** serial CLI access for setup and recovery. **Management** (**D**) is the **in-band** management interface (GUI/SSH/CAPWAP on the production network). **Distribution system** (**B**) carries AP/client traffic. **Redundant** (**A**) is for **WLC high-availability** peer links, not general OOB administration.",
            "choices": [
                "redundant",
                "distribution system",
                "service",
                "management",
                "console",
            ],
        },
        {
            "slug": "fiber-vs-copper-distance-throughput-choose-two",
            "title": "CCNA — Fiber vs copper (choose two)",
            "stem": "What are two facts that differentiate optical-fiber cabling from copper cabling? (Choose two)",
            "name": "fibcop1",
            "choose_two": True,
            "correct": ["A", "B"],
            "explain": "Correct. A and B \u2014 **Fiber** supports **longer reach** and **higher bandwidth** options (multigigabit and beyond on appropriate optics) with low attenuation and immunity to **EMI**. **Copper** carries **PoE** electrical power (**C**); fiber does not. **Fiber patch cables** are typically **more expensive** than copper (**D**), not less. **Fiber** is less affected by **EMI**; greater sensitivity to **temperature/moisture** (**E**) is not a defining advantage of fiber over copper.",
            "choices": [
                "It carries signals for longer distances.",
                "It provides greater throughput options.",
                "It carries electrical current further distances for PoE devices.",
                "It is less expensive when purchasing patch cables.",
                "It has a greater sensitivity to changes in temperature and moisture",
            ],
        },
        {
            "slug": "vrrp-multivendor-subnet-interoperate-vendors",
            "title": "CCNA — Why VRRP in multivendor subnet",
            "stem": "Why would VRRP be implemented when configuring a new subnet in a multivendor environment?",
            "name": "vrrpmvsub1",
            "correct": "C",
            "explain": "Correct. C \u2014 **VRRP** is an **open IETF standard**, so **Cisco and third-party** routers can share the same **virtual default gateway** design. **HSRP** and **GLBP** are **Cisco-centric** and are poor fits for mixed-vendor FHRP. **A** describes **STP**, not FHRP. **B** misstates the need (\u201cmore than two Cisco devices\u201d); multivendor is about **interoperability**, not Cisco-only scale. **D** is a general **FHRP** benefit (virtual IP/MAC and gratuitous ARP), but the **multivendor** reason is **open-standard VRRP** (**C**).",
            "choices": [
                "to ensure that the spanning-tree forwarding path to the gateway is loop-free",
                "when a gateway protocol is required that supports more than two Cisco devices for redundancy",
                "to interoperate normally with all vendors and provide additional security features for Cisco devices",
                "to enable normal operations to continue after a member failure without requiring a change in a host ARP cache",
            ],
        },
        {
            "slug": "autonomous-vs-cloud-ap-deployment-comparison",
            "title": "CCNA — Autonomous vs cloud-based APs",
            "stem": "Which statement accurately compares autonomous mode APs to APs running in cloud-based mode?",
            "name": "apcloud1",
            "correct": "A",
            "explain": "Correct. A \u2014 **Autonomous** APs are managed **locally** (per device or on-prem controller) and are **less dependent** on continuous **cloud/WAN reachability** for day-to-day control. At scale they are **harder to maintain** (firmware, RF, and policy per AP or site). **Cloud-based** APs (for example **Meraki**) use a **cloud dashboard** for **easy deployment**, **ZTP**, and **central automation**. **B** and **C** reverse that (**cloud** is easier to deploy/automate). **D** is wrong: **cloud** APs **depend** on the **underlay/internet** to the cloud and are typically **simpler** to operate centrally than scattered autonomous APs.",
            "choices": [
                "Autonomous mode APs are less dependent on an underlay but more complex to maintain than APs in cloud-based mode",
                "Autonomous mode APs are easy to deploy and automate than APs in cloud-based mode",
                "Cloud-based mode APs are easy to deploy but harder to automate than APs in autonomous mode",
                "Cloud-based mode APs rely on underlays and are more complex to maintain than APs in autonomous mode",
            ],
        },
        {
            "slug": "crud-update-http-put-patch-choose-two",
            "title": "CCNA — CRUD UPDATE: PUT and PATCH (choose two)",
            "stem": "Under the CRUD model, which two HTTP methods support the UPDATE operation? (Choose two)",
            "name": "crudupd1",
            "choose_two": True,
            "correct": ["A", "B"],
            "explain": "Correct. A and B \u2014 **UPDATE** maps to **PUT** (replace/update a resource at a URI) and **PATCH** (partial update). **GET** (**E**) is **Read**. **DELETE** (**C**) is **Delete**. **POST** (**D**) commonly maps to **Create** (or non-idempotent actions), not the standard UPDATE verbs.",
            "choices": [
                "PUT",
                "PATCH",
                "DELETE",
                "POST",
                "GET",
            ],
        },
        {
            "slug": "controller-based-architecture-advantages-choose-two",
            "title": "CCNA — Controller-based vs traditional (choose two)",
            "stem": "What are two advantages of implementing a controller-based architecture instead of a traditional network architecture? (Choose two)",
            "name": "ctrlarch1",
            "choose_two": True,
            "correct": ["B", "D"],
            "explain": "Correct. B and D \u2014 A **controller-based** (SDN) design centralizes control and policy, improving **scalability** and **management** from one platform, and supports **configuration automation** through **APIs** and orchestration. **A** (complex IP addressing) is not a defining advantage over traditional routed networks. **C** (VM connectivity) is a use case overlays/virtualization can address but is not the core differentiator here. **E** (DoS protection) is not the primary benefit of moving to controller-based architecture.",
            "choices": [
                "It supports complex and high-scale IP addressing schemes.",
                "It provides increased scalability and management options.",
                "It allows for seamless connectivity to virtual machines.",
                "It enables configuration task automation.",
                "It increases security against denial-of-service attacks.",
            ],
        },
        {
            "slug": "fa0-13-high-crc-input-errors-physical",
            "title": "CCNA — Fa0/13 CRC errors root cause",
            "stem": "Refer to the exhibit. A technician receives a report of network slowness and the issue has been isolated to the interface FastEthernet0/13. What is the root cause of the issue?",
            "name": "fa13crc1",
            "correct": "A",
            "explain": "Correct. A \u2014 **261,028 input errors** with **259,429 CRC** (and **1,599 frame** errors) mean frames arrived **corrupted** on the wire. That pattern points to **physical-layer** problems (bad cable, connector, or NIC/port). **Input/output queues** show **no drops** and **no buffer failures**, so **B** (buffer overload) does not fit. **Duplicate IP** (**C**) would not produce massive **CRC** counters. The link is **up/up** with **0 collisions** on **full duplex**, not a classic **err-disabled** far-end signature (**D**).",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="show interfaces FastEthernet0/13">
        <pre>FastEthernet0/13 is up, line protocol is up
Hardware is Fast Ethernet, address is 0001.4d27.66cd (bia 0001.4d27.66cd)
MTU 1500 bytes, BW 100000 Kbit, DLY 100 usec,
 reliability 255/255, txload 1/255, rxload 1/255
Encapsulation ARPA, loopback not set
Keepalive not set
Auto-duplex (Full), Auto Speed (100), 100BaseTX/FX
ARP type: ARPA, ARP Timeout 04:00:00
Last input 18:52:43, output 00:00:01, output hang never
Last clearing of "show interface" counters never
Queueing strategy: fifo
Output queue 0/40, 0 drops; input queue 0/75, 0 drops
5 minute input rate 12000 bits/sec, 6 packets/sec
5 minute output rate 24000 bits/sec, 6 packets/sec
14488019 packets input, 2441805322 bytes
Received 345346 broadcasts, 0 runts, 0 giants, 0 throttles
261028 input errors, 259429 CRC, 1599 frame, 0 overrun, 0 ignored
0 watchdog, 84207 multicast, 0 input packets with dribble condition detected
19658279 packets output, 3529106068 bytes, 0 underruns
0 output errors, 0 collisions, 1 interface resets
0 babbles, 0 late collision, 0 deferred
0 lost carrier, 0 no carrier
0 output buffer failures, 0 output buffers swapped out</pre>
      </div>""",
            "choices": [
                "physical errors",
                "local buffer overload",
                "duplicate IP addressing",
                "err-disabled port on the far end",
            ],
        },
        {
            "slug": "ospf-overlapping-10-routes-all-three-in-table",
            "title": "CCNA — show ip route overlapping OSPF prefixes",
            "stem": "A router received three destination prefixes: 10.0.0.0/8, 10.0.0.0/16, and 10.0.0.0/24. When the show ip route command is executed, which output does it return?",
            "name": "ospf103rt1",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 When the router learns **non-conflicting** overlapping prefixes (different mask lengths for the same major network), **each route is installed** in the IP routing table. **show ip route** lists **all three** **O E2** entries; forwarding then uses **longest-prefix match** per destination. **A** shows only **/24**. **B** omits **/8**. **C** shows only **/8** and hides the more-specific routes.",
            "choices": [
                """Gateway of last resort is 172.16.1.1 to network 0.0.0.0
O E2 10.0.0.0/24[110/5] via 192.168.3.1, 0:01:00, Ethernet2""",
                """Gateway of last resort is 172.16.1.1 to network 0.0.0.0
O E2 10.0.0.0/16[110/5] via 192.168.2.1, 0:01:00, Ethernet1
O E2 10.0.0.0/24[110/5] via 192.168.3.1, 0:01:00, Ethernet2""",
                """Gateway of last resort is 172.16.1.1 to network 0.0.0.0
O E2 10.0.0.0/8 [110/5] via 192.168.1.1, 0:01:00, Ethernet0""",
                """Gateway of last resort is 172.16.1.1 to network 0.0.0.0
O E2 10.0.0.0/8 [110/5] via 192.168.1.1, 0:01:00, Ethernet0
O E2 10.0.0.0/16[110/5] via 192.168.2.1, 0:01:00, Ethernet1
O E2 10.0.0.0/24[110/5] via 192.168.3.1, 0:01:00, Ethernet2""",
            ],
        },
        {
            "slug": "rapid-pvst-portfast-bypass-learning-state",
            "title": "CCNA — PortFast bypasses learning in RPVST+",
            "stem": "Which state is bypassed in Rapid PVST+ when PortFast is enabled on a port?",
            "name": "pflearn1",
            "correct": "B",
            "explain": "Correct. B \u2014 **PortFast** on an edge access port moves the port straight to **forwarding**, skipping the usual **learning** delay where the bridge would otherwise learn MAC addresses before forwarding. In **Rapid PVST+** (RSTP), ports normally progress through **discarding**, **learning**, and **forwarding**; PortFast short-circuits that wait. **Discarding** (**A**) and legacy **blocking** (**C**) are not the state the exam highlights as bypassed. **Forwarding** (**D**) is the destination state, not a bypassed one.",
            "choices": [
                "discarding",
                "learning",
                "blocking",
                "forwarding",
            ],
        },
        {
            "slug": "switch-learn-unknown-source-mac-ingress-port",
            "title": "CCNA — Learn unknown source MAC on ingress",
            "stem": "When a switch receives a frame from an unknown source MAC address, which action does the switch take with the frame?",
            "name": "unkmac1",
            "correct": "D",
            "explain": "Correct. D \u2014 The switch **learns** the **source MAC** from the frame and **records** it in the **MAC/CAM table** mapped to the **ingress port**, then forwards based on the **destination** MAC. **A** describes **unknown destination** behavior (flood), and flooding does **not** include the **ingress** port for unknown unicast. **B** does not occur. **C** misstates the table: the CAM stores **learned** addresses, not unknown sources.",
            "choices": [
                "It floods the frame out all interfaces, including the interface it was received on.",
                "It attempts to send the frame back to the source to ensure that the source MAC address is still available for transmissions.",
                "It sends the frame to ports within the CAM table identified with an unknown source MAC address.",
                "It associate the source MAC address with the LAN port on which it was received and saves it to the MAC address table.",
            ],
        },
        {
            "slug": "sdn-southbound-api-flow-control-switching-fabric",
            "title": "CCNA — Southbound API flow control",
            "stem": "What is a function of a southbound API?",
            "name": "sdnsbfn1",
            "correct": "B",
            "explain": "Correct. B \u2014 A **southbound API** connects the **SDN controller** to the **switching fabric** (infrastructure devices) so the controller can program **forwarding/flow** behavior (for example via **OpenFlow**, **NETCONF**, or **OpFlex**). **D** describes a **northbound** API (controller to **applications**). **C** is **orchestration** above the controller, not southbound device control. **A** is vague; southbound is specifically **controller-to-device**, not generic server-to-fabric automation wording alone.",
            "choices": [
                "Automate configuration changes between a server and a switching fabric.",
                "Manage flow control between an SDN controller and a switching fabric.",
                "Use orchestration to provision a virtual server configuration from a web server.",
                "Facilitate the information exchange between an SDN controller and application.",
            ],
        },
        {
            "slug": "r25-fa0-0-runts-duplex-mismatch",
            "title": "CCNA — Fa0/0 runts interface condition",
            "stem": "Refer to the exhibit. Which interface condition is occurring in this output?",
            "name": "r25runts1",
            "correct": "B",
            "explain": "Correct. B \u2014 A high **runts** count means frames **smaller than 64 bytes** arrived; on Ethernet that commonly indicates **collision fragments** from a **duplex mismatch** (one end **full duplex**, the other **half duplex**) even when this side reports **Full-duplex**. **Bad NIC** (**A**) more often raises **CRC** errors, not runts alone. **Collisions** (**C**) can accompany duplex mismatch but the keyed condition here is the **runts** pattern. **High throughput** (**D**) is not indicated (**0** bit/sec rates, low packet counts).",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="R25 show interface FastEthernet0/0">
        <pre>R25# show interface fa0/0
FastEthernet0/0 is up, line protocol is up
Hardware is DEC21140, address is ca02.7788.0000 (bia ca02.7788.0000)
Description: atlanta_subnet
Internet address is 10.32.102.2/30
MTU 1500 bytes, BW 100000 Kbit/sec, DLY 100 usec,
 reliability 255/255, txload 1/255, rxload 1/255
Encapsulation ARPA, loopback not set
Keepalive set (60 sec)
Full-duplex, 100 Mb/s, 100BaseTX/FX
ARP type: ARPA, ARP Timeout 04:00:00
Last input 00:00:01, output 00:00:00, output hang never
Last clearing of "show interface" counters never
Input queue: 0/300/0/0 (size/max/drops/flushes); Total output drops: 0
Queueing strategy: fifo
Output queue: 0/300 (size/max)
30 second input rate 0 bits/sec, 0 packets/sec
30 second output rate 0 bits/sec, 0 packets/sec
7331 packets input, 7101162 bytes
Received 267 broadcasts (0 IP multicasts)
1876 runts, 0 giants, 0 throttles
0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
0 watchdog
0 input packets with dribble condition detected
3927 packets output, 1440403 bytes, 0 underruns
0 output errors, 0 collisions, 0 interface resets
0 unknown protocol drops
0 babbles, 0 late collision, 0 deferred
0 lost carrier, 0 no carrier
0 output buffer failures, 0 output buffers swapped out</pre>
      </div>""",
            "choices": [
                "bad NIC",
                "duplex mismatch",
                "collisions",
                "high throughput",
            ],
        },
        {
            "slug": "r25-fa0-0-txload-255-high-throughput",
            "title": "CCNA — Fa0/0 txload 255 high throughput",
            "stem": "Refer to the exhibit. Which interface condition is occurring in this output?",
            "name": "r25load1",
            "correct": "D",
            "explain": "Correct. D \u2014 **txload 255/255** and **rxload 255/255** mean the interface is **saturated** (maximum load). The **30-second rates** (~226\u2013232 Mbps) far exceed the **100 Mb/s** line rate, indicating **very high throughput** utilization. **Runts**, **CRC**, and **collisions** are **zero**, so **duplex mismatch** (**B**), **bad NIC** (**A**), and **collisions** (**C**) do not fit.",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="R25 show interface FastEthernet0/0 singapore">
        <pre>R25# show interface fa0/0
FastEthernet0/0 is up, line protocol is up
Hardware is DEC21140, address is ca02.7788.0000 (bia ca02.7788.0000)
Description: singapore_subnet
Internet address is 10.32.102.2/30
MTU 1500 bytes, BW 100000 Kbit/sec, DLY 100 usec,
 reliability 255/255, txload 255/255, rxload 255/255
Encapsulation ARPA, loopback not set
Keepalive set (60 sec)
Full-duplex, 100 Mb/s, 100BaseTX/FX
ARP type: ARPA, ARP Timeout 04:00:00
Last input 00:00:01, output 00:00:00, output hang never
Last clearing of "show interface" counters never
Input queue: 0/300/0/0 (size/max/drops/flushes); Total output drops: 0
Queueing strategy: fifo
Output queue: 0/300 (size/max)
30 second input rate 225953751 bits/sec, 0 packets/sec
30 second output rate 232423817 bits/sec, 0 packets/sec
7331 packets input, 7101162 bytes
Received 267 broadcasts (0 IP multicasts)
0 runts, 0 giants, 0 throttles
0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
0 watchdog
0 input packets with dribble condition detected
3927 packets output, 1440403 bytes, 0 underruns
0 output errors, 0 collisions, 0 interface resets
0 unknown protocol drops
0 babbles, 0 late collision, 0 deferred
0 lost carrier, 0 no carrier
0 output buffer failures, 0 output buffers swapped out</pre>
      </div>""",
            "choices": [
                "bad NIC",
                "duplex mismatch",
                "collisions",
                "high throughput",
            ],
        },
        {
            "slug": "dhcp-relay-helper-192-168-10-1-cross-subnet",
            "title": "CCNA — ip helper-address for DHCP relay",
            "stem": "The clients and DHCP server reside on different subnets. Which command must be used to forward requests and replies between clients on the 10.10.0.1/24 subnet and the DHCP server at 192.168.10.1?",
            "name": "dhcphlp1",
            "correct": "B",
            "explain": "Correct. B \u2014 On the router **interface facing the client subnet**, **`ip helper-address 192.168.10.1`** enables a **DHCP relay** so **DHCPDISCOVER**/**DHCPREQUEST** broadcasts are forwarded to the server and replies return to clients. **`ip route`** (**A**) adds routing, not DHCP relay. **`ip dhcp address`** (**C**) is not the relay command. **`ip default-gateway`** (**D**) is configured on **hosts**, not for router DHCP relay.",
            "choices": [
                "ip route 192.168.10.1",
                "ip helper-address 192.168.10.1",
                "ip dhcp address 192.168.10.1",
                "ip default-gateway 192.168.10.1",
            ],
        },
        {
            "slug": "ospf-r2-gi01-area-1-match-r1-neighbor",
            "title": "CCNA — R2 OSPF area 1 on Gi0/1",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "A network engineer started to configure two directly-connected routers as shown. Which command sequence must the engineer configure on R2 so that the two routers become OSPF neighbors?",
            "name": "ospfr2nb1",
            "correct": "B",
            "mono": True,
            "explain": "Correct. B \u2014 **R1** enables **OSPF process 1** on **GigabitEthernet0/1** in **area 1** (**network 192.168.12.1 0.0.0.0 area 1**). **R2** must run the same **process** and **area** on the link: **`interface GigabitEthernet0/1`** then **`ip ospf 1 area 1`**. **A** uses **area 0**, so neighbors will not form. **C** advertises the subnet in **area 0**. **D** uses a **/32** wildcard for **192.168.12.1** only, which does not match **R2\u2019s 192.168.12.2** address.",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="R1 and R2 partial configuration">
        <pre>R1
interface GigabitEthernet0/1
 ip address 192.168.12.1 255.255.255.128
 no shutdown
router ospf 1
 network 192.168.12.1 0.0.0.0 area 1

R2
interface GigabitEthernet0/1
 ip address 192.168.12.2 255.255.255.128
 no shutdown</pre>
      </div>""",
            "choices": [
                """interface GigabitEthernet0/1
ip ospf 1 area 0""",
                """interface GigabitEthernet0/1
ip ospf 1 area 1""",
                """router ospf 1
network 192.168.12.0 0.0.0.127 area 0""",
                """router ospf 1
network 192.168.12.1 0.0.0.0 area 1""",
            ],
        },
        {
            "slug": "route-10-0-1-3-slash-32-host-route-meaning",
            "title": "CCNA — Meaning of 10.0.1.3/32 route",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "What does route 10.0.1.3/32 represent in the routing table?",
            "name": "rt10332m1",
            "correct": "C",
            "explain": "Correct. C \u2014 A **/32** mask is a **host route**: it matches **one destination IP** (**10.0.1.3**), reached via **10.0.1.100** on **Serial0**. **A** would be a **/24** (or shorter) network route for **10.0.1.0/24**. **B** confuses the **next-hop** (**10.0.1.100**) with the **route prefix**. **D** is the broader **10.0.0.0/8** summary, not this **/32** entry.",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="R1 show ip route">
        <pre>R1# show ip route
Codes: C - connected, S - static, I - IGRP, R - rip, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
       i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2, * - candidate default
       U - per-user static route, o - ODR
Gateway of last resort is not set
C    10.0.0.0/8 is directly connected, Loopback0
     10.0.0.0/8 is variably subnetted, 4 subnets, 2 masks
O    10.0.1.3/32 [110/100] via 10.0.1.100, 00:39:08, Serial0
C    10.0.1.0/24 is directly connected, Serial0
O    10.0.1.5/32 [110/5] via 10.0.1.50, 00:39:08, GigabitEthernet0/0
D    10.0.1.4/32 [110/10] via 10.0.1.4, 00:39:08, GigabitEthernet0/0</pre>
      </div>""",
            "choices": [
                "all hosts in the 10.0.1.0 subnet",
                "the source 10.0.1.100",
                "a single destination address",
                "the 10.0.0.0 network",
            ],
        },
        {
            "slug": "r1-ssh-version2-minimum-config-options",
            "title": "CCNA — R1: minimum SSHv2 configuration (options)",
            "stem": "An engineer is configuring SSH version 2 exclusively on the R1 router. What is the minimum configuration required to permit remote management using the cryptographic protocol?",
            "name": "r1sshv2min1",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 **SSHv2** needs **`ip domain-name`** (RSA key generation), **`crypto key generate rsa`**, **`ip ssh version 2`**, a **local user** (**`username` \u2026 `password`**), **`transport input ssh`** on **VTY** lines (not **`all`**, which still permits **Telnet**), and **`login local`**. **A** uses **`transport input all`**. **B** omits **`ip domain-name`**. **C** adds **`service password-encryption`**, which only obfuscates passwords in **show run** and is **not required** for SSH, and also omits **`ip domain-name`**.",
            "choices": [
                """Option A

hostname R1
ip domain name cisco
crypto key generate rsa general-keys modulus 1024
username cisco privilege 15 password 0 cisco123
ip ssh version 2
line vty 0 15
 transport input all
 login local""",
                """Option B

hostname R1
crypto key generate rsa general-keys modulus 1024
username cisco privilege 15 password 0 cisco123
ip ssh version 2
line vty 0 15
 transport input all
 login local""",
                """Option C

hostname R1
service password-encryption
crypto key generate rsa general-keys modulus 1024
username cisco privilege 15 password 0 cisco123
ip ssh version 2
line vty 0 15
 transport input ssh
 login local""",
                """Option D

hostname R1
ip domain name cisco
crypto key generate rsa general-keys modulus 1024
username cisco privilege 15 password 0 cisco123
ip ssh version 2
line vty 0 15
 transport input ssh
 login local""",
            ],
        },
        {
            "slug": "r19-fa0-0-collisions-portland-subnet",
            "title": "CCNA — R19 Fa0/0 collisions (show interface)",
            "stem": "Refer to the exhibit. Which interface condition is occurring in this output?",
            "name": "r19coll1",
            "correct": "C",
            "explain": "Correct. C \u2014 The output reports **139 collisions** on the interface. **Queueing** problems (**A**) would show **input/output queue drops** or **buffer failures**, not a high **collisions** counter. **Duplex mismatch** (**B**) more often shows **runts**, **late collisions**, or **deferred** frames; here **runts** are **0** and **late collision** is **0**. **High throughput** (**D**) is not indicated: **txload/rxload** are **1/255** and **30-second rates** are **0**.",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="R19 show interface FastEthernet0/0">
        <pre>R19# show interface fa0/0
FastEthernet0/0 is up, line protocol is up
Hardware is DEC21140, address is ca02.7788.0000 (bia ca02.7788.0000)
Description: portland_subnet
Internet address is 10.32.102.2/30
MTU 1500 bytes, BW 100000 Kbit/sec, DLY 100 usec,
 reliability 255/255, txload 1/255, rxload 1/255
Encapsulation ARPA, loopback not set
Keepalive set (60 sec)
Full-duplex, 100 Mb/s, 100BaseTX/FX
ARP type: ARPA, ARP Timeout 04:00:00
Last input 00:00:01, output 00:00:00, output hang never
Last clearing of "show interface" counters never
Input queue: 0/300/0/0 (size/max/drops/flushes); Total output drops: 0
Queueing strategy: fifo
Output queue: 0/300 (size/max)
30 second input rate 0 bits/sec, 0 packets/sec
30 second output rate 0 bits/sec, 0 packets/sec
7331 packets input, 7101162 bytes
Received 267 broadcasts (0 IP multicasts)
0 runts, 0 giants, 0 throttles
0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
0 watchdog
0 input packets with dribble condition detected
3927 packets output, 1440403 bytes, 0 underruns
0 output errors, 139 collisions, 0 interface resets
0 unknown protocol drops
0 babbles, 0 late collision, 0 deferred
0 lost carrier, 0 no carrier
0 output buffer failures, 0 output buffers swapped out</pre>
      </div>""",
            "choices": [
                "queueing",
                "duplex mismatch",
                "collisions",
                "high throughput",
            ],
        },
        {
            "slug": "static-routes-same-destination-different-next-hop",
            "title": "CCNA — Two static routes, different next hops",
            "stem": "A router has two static routes to the same destination network under the same OSPF process. How does the router forward packets to the destination if the next-hop devices are different?",
            "name": "st2nh1",
            "correct": "B",
            "explain": "Correct. B \u2014 When multiple **equal-cost** routes exist to the same destination (same **prefix/mask**, same **administrative distance**, and for OSPF the same **metric**), Cisco routers **load-balance** across those paths (per-destination or per-packet depending on platform/CEF settings). The router does **not** pick the next hop by **lowest IP** (**A**) or **MAC** (**C**). **Route age** (**D**) is not the tie-break for forwarding among active equal-cost entries.",
            "choices": [
                "The router chooses the next hop with the lowest IP address.",
                "The router load-balances traffic over all routes to the destination.",
                "The router chooses the next hop with the lowest MAC address.",
                "The router chooses the route with the oldest age.",
            ],
        },
        {
            "slug": "r17-fa0-0-txload-255-high-throughput-chicago",
            "title": "CCNA — R17 Fa0/0 high throughput (show interface)",
            "stem": "Which interface condition is occurring in this output?",
            "name": "r17load1",
            "correct": "A",
            "explain": "Correct. A \u2014 **txload 255/255** and **rxload 255/255** show the interface at **maximum utilization**. **30-second input/output rates** (~201\u2013229 Mbps) far exceed the **100 Mb/s** configured speed, indicating **very high throughput**. **Queueing** (**B**) would show **queue drops** or **buffer failures**, not saturation load counters alone. **Bad NIC** (**C**) usually raises **CRC**/**frame** errors (here **0**). **Broadcast storm** (**D**) would show a very high **broadcast** count relative to total traffic; only **267** broadcasts are listed.",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="R17 show interface FastEthernet0/0">
        <pre>R17# show interface fa0/0
FastEthernet0/0 is up, line protocol is up
Hardware is DEC21140, address is ca02.7788.0000 (bia ca02.7788.0000)
Description: chicago_subnet
Internet address is 10.32.102.2/30
MTU 1500 bytes, BW 100000 Kbit/sec, DLY 100 usec,
 reliability 255/255, txload 255/255, rxload 255/255
Encapsulation ARPA, loopback not set
Keepalive set (60 sec)
Full-duplex, 100 Mb/s, 100BaseTX/FX
ARP type: ARPA, ARP Timeout 04:00:00
Last input 00:00:01, output 00:00:00, output hang never
Last clearing of "show interface" counters never
Input queue: 0/300/0/0 (size/max/drops/flushes); Total output drops: 0
Queueing strategy: fifo
Output queue: 0/300 (size/max)
30 second input rate 201240151 bits/sec, 0 packets/sec
30 second output rate 228594263 bits/sec, 0 packets/sec
7331 packets input, 7101162 bytes
Received 267 broadcasts (0 IP multicasts)
1876 runts, 0 giants, 0 throttles
0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
0 watchdog
0 input packets with dribble condition detected
3927 packets output, 1440403 bytes, 0 underruns
0 output errors, 0 collisions, 0 interface resets
0 unknown protocol drops
0 babbles, 0 late collision, 0 deferred
0 lost carrier, 0 no carrier
0 output buffer failures, 0 output buffers swapped out</pre>
      </div>""",
            "choices": [
                "high throughput",
                "queueing",
                "bad NIC",
                "broadcast storm",
            ],
        },
        {
            "slug": "10gbase-sr-lr-shared-fiber-media-property",
            "title": "CCNA — 10GBase-SR and 10GBase-LR shared property",
            "stem": "Which property is shared by 10GBase-SR and 10GBase-LR interfaces?",
            "name": "10gsrlr1",
            "correct": "D",
            "explain": "Correct. D \u2014 **10GBase-SR** (short reach) and **10GBase-LR** (long reach) are **10 Gigabit Ethernet** standards that both use **fiber** cabling. **SR** is designed for **multimode** fiber over shorter distances; **LR** uses **single-mode** fiber for longer spans\u2014so **A** and **C** are not shared. Neither standard uses **UTP** copper (**B**).",
            "choices": [
                "Both use the multimode fiber type.",
                "Both require UTP cable media for transmission.",
                "Both use the single-mode fiber type.",
                "Both require fiber cable media for transmission.",
            ],
        },
        {
            "slug": "datacenter-backup-more-specific-route-secondary-circuit",
            "title": "CCNA — Backup traffic off primary MPLS circuit",
            "stem": "A network engineer is upgrading a small data center to host several new applications, including server backups that are expected to account for up to 90% of the bandwidth during peak times. The data center connects to the MPLS network provider via a primary circuit and a secondary circuit. How does the engineer inexpensively update the data center to avoid saturation of the primary circuit by traffic associated with the backups?",
            "name": "dcbkrt1",
            "correct": "D",
            "explain": "Correct. D \u2014 **Advertise a more specific route** for backup prefixes **out the secondary circuit** so **longest-prefix match** steers backup flows away from the **primary** link without buying new hardware. A **dedicated VLAN** (**A**) or **switch** (**C**) alone does not change which **WAN/MPLS** path carries the traffic. A **dedicated backup circuit** (**B**) is effective but **not inexpensive** compared with **policy routing/BGP** using the **existing secondary** link.",
            "choices": [
                "Place the backup servers in a dedicated VLAN.",
                "Configure a dedicated circuit for the backup traffic.",
                "Assign traffic from the backup servers to a dedicated switch.",
                "Advertise a more specific route for the backup traffic via the secondary circuit.",
            ],
        },
        {
            "slug": "ospf-r2-hello-interval-10-match-r1-neighbor",
            "title": "CCNA — OSPF R2 hello-interval to match R1",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "The network engineer is configuring router R2 as a replacement router on the network. After the initial configuration is applied it is determined that R2 failed to show R1 as a neighbor. Which configuration must be applied to R2 to complete the OSPF configuration and enable it to establish the neighbor relationship with R1?",
            "name": "ospfr2hi1",
            "correct": "A",
            "mono": True,
            "explain": "Correct. A \u2014 **R1** uses **Hello 10** and **Dead 40**; **R2** shows **Hello 15** with **Dead 40**. OSPF requires matching **hello** and **dead** timers on the link. **`ip ospf hello-interval 10`** on **R2 GigabitEthernet0/0/0** aligns hello with **R1** (dead stays **40**). **Option B** changes **router-id** but does not fix the timer mismatch. **Option C** places the subnet in **area 2** while **R1** is in **area 0**. **Option D** sets **dead-interval 45**, which mismatches **R1\u2019s Dead 40**.",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="R1 show ip ospf interface g0/0/0">
        <pre>R1#show ip ospf interface g0/0/0
GigabitEthernet0/0/0 is up, line protocol is up
  Internet address is 192.168.1.2/24, Area 0
  Process ID 1, Router ID 192.168.1.2, Network Type POINT-TO-POINT, Cost: 1
  Transmit Delay is 1 sec, State POINT-TO-POINT,
  Timer intervals configured, Hello 10, Dead 40, Wait 40, Retransmit 5
    Hello due in 00:00:08
  Index 1/1, flood queue length 0
  Next 0x0(0) /0x0(0)
  Last flood scan length is 1, maximum is 1
  Last flood scan time is 0 msec, maximum is 0 msec
  Suppress hello for 0 neighbor(s)</pre>
      </div>
      <div class="exhibit-router-cli" role="region" aria-label="R2 show ip ospf interface g0/0/0">
        <pre>R2#show ip ospf interface g0/0/0
GigabitEthernet0/0/0 is up, line protocol is up
  Internet address is 192.168.1.1/24, Area 0
  Process ID 1, Router ID 10.1.1.1, Network Type POINT-TO-POINT, Cost: 1
  Transmit Delay is 1 sec, State POINT-TO-POINT,
  Timer intervals configured, Hello 15, Dead 40, Wait 40, Retransmit 5
    Hello due in 00:00:11
  Index 1/1, flood queue length 0
  Next 0x0(0)/0x0(0)
  Last flood scan length is 1, maximum is 1
  Last flood scan time is 0 msec, maximum is 0 msec
  Suppress hello for 0 neighbor(s)</pre>
      </div>
    </div>""",
            "choices": [
                """Option A

R2(config)#interface g0/0/0
R2(config-if)#ip ospf hello-interval 10""",
                """Option B

R2(config)#router ospf 1
R2(config-router)#router-id 192.168.1.1""",
                """Option C

R2(config)#router ospf 1
R2(config-router)#network 192.168.1.0 255.255.255.0 area 2""",
                """Option D

R2(config)#interface g0/0/0
R2(config-if)#ip ospf dead-interval 45""",
            ],
        },
        {
            "slug": "soho-environment-characteristics-choose-two",
            "title": "CCNA — SOHO connection environment (choose two)",
            "stem": "What are two characteristics of a small office / home office connection environment? (Choose two.)",
            "name": "sohoenv1",
            "choose_two": True,
            "correct": ["A", "D"],
            "explain": "Correct. A and D \u2014 **SOHO** sites are **small** (typically on the order of **1\u201350 users**) and usually connect to the Internet through a **router WAN port** to a **broadband** service (cable, DSL, or fiber). **B** describes an **enterprise** **core/distribution/access** design, not SOHO. **C** (**50\u2013100 users**) fits a larger **branch/SMB** more than SOHO. **E** (**10Gb on all uplinks**) is **datacenter/enterprise** scale, not typical SOHO.",
            "choices": [
                "It supports between 1 and 50 users.",
                "It requires a core, distribution, and access layer architecture.",
                "It supports between 50 and 100 users.",
                "A router port connects to a broadband connection.",
                "It requires 10Gb ports on all uplinks.",
            ],
        },
        {
            "slug": "syslog-severity-emergency-system-unusable",
            "title": "CCNA — Syslog emergency severity (system unusable)",
            "stem": "Which syslog severity level is considered the most severe and results in the system being considered unusable?",
            "name": "syslogsev1",
            "correct": "B",
            "explain": "Correct. B \u2014 **Emergency (level 0)** is the highest syslog severity: the system is **unusable**. **Alert (1)** needs immediate action but is below emergency. **Critical (2)** and **Error (3)** are serious but not the top level. Cisco IOS uses the scale **0 emergency** through **7 debug**.",
            "choices": [
                "Critical",
                "Emergency",
                "Alert",
                "Error",
            ],
        },
        {
            "slug": "dna-center-apis-vs-traditional-manual-gathering",
            "title": "CCNA — DNA Center APIs vs traditional campus management",
            "stem": "Which benefit does Cisco DNA Center provide over traditional campus management?",
            "name": "dnaapi1",
            "correct": "B",
            "explain": "Correct. B \u2014 **Cisco DNA Center** exposes **northbound APIs** so tools and automation can **programmatically** collect state, configure intent, and integrate workflows instead of relying on **manual CLI/SNMP polling** per device. **A** misstates the gap (**SNMPv3** is available in both models). **C** is wrong because **SSH** is common in **traditional** management too. **D** overstates **HTTPS** as unique\u2014secure web access is not the defining differentiator.",
            "choices": [
                "Cisco DNA Center leverages SNMPv3 for encrypted management, and traditional campus management uses SNMPv2.",
                "Cisco DNA Center leverages APIs, and traditional campus management requires manual data gathering.",
                "Cisco DNA Center automates SSH access for encrypted entry, and SSH is absent from traditional campus management.",
                "Cisco DNA Center automates HTTPS for secure web access, and traditional campus management uses HTTP.",
            ],
        },
        {
            "slug": "r25-fa0-0-queueing-tokyo-subnet",
            "title": "CCNA — R25 Fa0/0 queueing (show interface)",
            "stem": "Which interface condition is occurring in this output?",
            "name": "r25que1",
            "correct": "C",
            "explain": "Correct. C \u2014 **Output queue: 185/300** shows the **transmit queue** is **nearly full**, indicating **queueing**/**congestion** on the outbound path. **txload/rxload 1/255** and **zero 30-second rates** argue against **high throughput** saturation. **CRC**/**frame** errors are **0**, so **bad NIC** (**A**) is unlikely. Only **267** broadcasts were received, not a **broadcast storm** (**B**). **Runts** can suggest **duplex mismatch** (**D**), but the **filled output queue** is the condition this item keys on.",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="R25 show interface FastEthernet0/0">
        <pre>R25# show interface fa0/0
FastEthernet0/0 is up, line protocol is up
Hardware is DEC21140, address is ca02.7788.0000 (bia ca02.7788.0000)
Description: tokyo_subnet
Internet address is 10.32.102.2/30
MTU 1500 bytes, BW 100000 Kbit/sec, DLY 100 usec,
 reliability 255/255, txload 1/255, rxload 1/255
Encapsulation ARPA, loopback not set
Keepalive set (60 sec)
Full-duplex, 100 Mb/s, 100BaseTX/FX
ARP type: ARPA, ARP Timeout 04:00:00
Last input 00:00:01, output 00:00:00, output hang never
Last clearing of "show interface" counters never
Input queue: 0/300/0/0 (size/max/drops/flushes); Total output drops: 0
Queueing strategy: fifo
Output queue: 185/300 (size/max)
30 second input rate 0 bits/sec, 0 packets/sec
30 second output rate 0 bits/sec, 0 packets/sec
7331 packets input, 7101162 bytes
Received 267 broadcasts (0 IP multicasts)
1876 runts, 0 giants, 0 throttles
0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
0 watchdog
0 input packets with dribble condition detected
3927 packets output, 1440403 bytes, 0 underruns
0 output errors, 0 collisions, 0 interface resets
0 unknown protocol drops
0 babbles, 0 late collision, 0 deferred
0 lost carrier, 0 no carrier
0 output buffer failures, 0 output buffers swapped out</pre>
      </div>""",
            "choices": [
                "bad NIC",
                "broadcast storm",
                "queueing",
                "duplex mismatch",
            ],
        },
        {
            "slug": "snmp-community-string-mib-access-password",
            "title": "CCNA — SNMP community string role",
            "stem": "What is the role of community strings in SNMP operations?",
            "name": "snmpcomm1",
            "correct": "B",
            "explain": "Correct. B \u2014 In **SNMPv1/v2c**, the **community string** acts like a **shared password** that controls **read-only** or **read-write** access to **MIB** objects on the agent. It is **not** a **sequence tag** (**A**). It is **not** **Active Directory** credentials (**C**). The NMS uses **MIB** definitions to **interpret** OIDs; community strings do **not** translate alphanumeric output to numbers (**D**). **SNMPv3** replaces communities with **user-based security**.",
            "choices": [
                "It serves as a sequence tag on SNMP traffic messages.",
                "It serves as a password to protect access to MIB objects.",
                "It passes the Active Directory username and password that are required for device access.",
                "It translates alphanumeric MIB output values to numeric values.",
            ],
        },
        {
            "slug": "wlc-lag-one-port-passes-client-traffic",
            "title": "CCNA — WLC LAG implementation (client traffic)",
            "stem": "How will Link Aggregation be implemented on a Cisco Wireless LAN Controller?",
            "name": "wlclagimpl1",
            "correct": "D",
            "explain": "Correct. D \u2014 With **LAG** enabled, the WLC **bundles** distribution ports, but **only one working physical port** is required for **client traffic** to continue if other members fail. **A** is wrong: **two or more ports** are not mandatory for basic client forwarding (LAG is optional; a single link can carry traffic). **B** misstates WLC LAG: the **switch** side uses **LACP** (**channel-group mode active**); that is not the defining **WLC** implementation fact here. **C** is false\u2014LAG does not cap bandwidth at **500 Mbps**.",
            "choices": [
                "To pass client traffic, two or more ports must be configured",
                "The EtherChannel must be configured in \u201cmode active\u201d",
                "When enabled, the WLC bandwidth drops to 500 Mbps",
                "One functional physical port is needed to pass client traffic",
            ],
        },
        {
            "slug": "r1-telnet-login-local-privilege-15-username",
            "title": "CCNA — Telnet local user to privileged mode",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "An engineer booted a new switch and applied this configuration via the console port. Which additional configuration must be applied to allow administrators to authenticate directly to global configuration mode via Telnet using a local username and password?",
            "name": "r1tel1",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 **`username admin privilege 15 secret`** creates a **local** account that lands in **privileged EXEC** (global config access) when **`login local`** is on **VTY** lines. **`login local`** checks the **local database** instead of a **line password** alone. **A** and **B** use **`line vty` password`** without a proper **`username ... secret`** and show **`(config-if)`** context errors. **C** adds **`enable secret`** but omits **`privilege 15`** on the user, so Telnet may stop at **user EXEC** unless **`enable`** is entered.",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="R1 initial configuration">
        <pre>Switch(config)#hostname R1
R1(config)#interface FastEthernet0/1
R1(config-if)#no switchport
R1(config-if)#ip address 10.100.20.42 255.255.255.0
R1(config-if)#line vty 0 4
R1(config-line)#login</pre>
      </div>""",
            "choices": [
                """R1(config)#username admin
R1(config-if)#line vty 0 4
R1(config-line)#password p@ss1234""",
                """R1(config)#username admin
R1(config-if)#line vty 0 4
R1(config-line)#password p@ss1234
R1(config-line)#transport input telnet""",
                """R1(config)#username admin secret p@ss1234
R1(config-if)#line vty 0 4
R1(config-line)#login local
R1(config)#enable secret p@ss1234""",
                """R1(config)#username admin privilege 15 secret p@ss1234
R1(config-if)#line vty 0 4
R1(config-line)#login local""",
            ],
        },
        {
            "slug": "backdoor-malware-unauthorized-access-definition",
            "title": "CCNA — Backdoor malware definition",
            "stem": "What is the definition of backdoor malware?",
            "name": "backdoor1",
            "correct": "D",
            "explain": "Correct. D \u2014 A **backdoor** is malware (or a hidden access method) installed so an **unauthorized user** can access the system later, often bypassing normal authentication. **A** describes a **dropper/launcher** for other malware. **B** describes **spam bot**/**zombie** behavior. **C** describes **downloader** malware whose main job is to fetch more malicious code.",
            "choices": [
                "malicious program that is used to launch other malicious programs",
                "malicious code that infects a user machine and then uses that machine to send spam",
                "malicious code with the main purpose of downloading other malicious code",
                "malicious code that is installed onto a computer to allow access by an unauthorized user",
            ],
        },
        {
            "slug": "wlc-console-connection-out-of-band-management",
            "title": "CCNA — WLC console connection functionality",
            "stem": "Which functionality is provided by the console connection on a Cisco WLC?",
            "name": "wlcconfn1",
            "correct": "B",
            "explain": "Correct. B \u2014 The **console** port is **out-of-band** **serial** management for initial setup, recovery, and troubleshooting when **in-band** IP paths are unavailable. **In-band** administration uses the **management interface** (GUI/SSH/HTTPS) on the production network (**A** is wrong). **HTTP GUI** (**C**) is not provided over the **serial console**. **Unencrypted in-band file transfers** (**D**) does not describe the console role.",
            "choices": [
                "secure In-band connectivity for device administration",
                "out-of-band management",
                "HTTP-based GUI connectivity",
                "unencrypted in-band connectivity for file transfers",
            ],
        },
        {
            "slug": "wlc-flexconnect-local-switching-wlan-advanced-gui",
            "title": "CCNA — FlexConnect local switching (WLAN Advanced)",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/wlc-flexconnect-local-switching-wlan-advanced-gui.png" alt="WLC WLAN Advanced tab: FlexConnect section with FlexConnect Local Switching checkbox among local auth, central DHCP, and profiling options." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. An architect is managing a wireless network with APs from several branch offices connecting to the WLC in the data center. There is a new requirement for a single WLAN to process the client data traffic without sending it to the WLC. Which action must be taken to complete the request?",
            "name": "wlcfcsw1",
            "correct": "B",
            "explain": "Correct. B \u2014 **FlexConnect Local Switching** lets **branch** APs **switch client data locally** on the site LAN instead of tunneling all user traffic to the **central WLC**. **Local HTTP profiling** (**A**) and **local DHCP profiling** (**C**) identify clients; they do not change where data is switched. **Disassociation Imminent** (**D**) is an **802.11v** roaming aid, not local data switching.",
            "choices": [
                "Enable local HTTP profiling",
                "Enable FlexConnect Local Switching",
                "Enable local DHCP Profiling",
                "Enable Disassociation Imminent",
            ],
        },
        {
            "slug": "sw1-pc1-port-security-access-mac-exhibit",
            "title": "CCNA — PC1 port security (access + static MAC)",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/sw1-pc1-r1-r2-dual-lan-port-security-topology.png" alt="Topology: R1 and R2 on 10.0.0.0/30 (.1 and .2); R1 G0/1 to SW1 G0/1 on 10.0.1.0/24 with PC1 on SW1 G0/2 and PC2 on G0/3; R2 G0/1 to SW2 on 10.0.2.0/24 with PC3 and PC4 on G0/2 and G0/3." width="900" decoding="async" loading="lazy" />
      </figure>
      <figure class="exhibit-photo">
        <table class="exhibit-mac-table" style="width:100%;border-collapse:collapse;font-size:0.92rem">
          <thead>
            <tr style="background:#1a253b;color:#e6edf3">
              <th style="padding:10px 14px;text-align:left;border-bottom:1px solid #2d3b5a">Workstation</th>
              <th style="padding:10px 14px;text-align:left;border-bottom:1px solid #2d3b5a">Mac address</th>
            </tr>
          </thead>
          <tbody style="color:#e6edf3;background:#0d1320">
            <tr><td style="padding:8px 14px;border-bottom:1px solid #2a3f5c">PC 1</td><td style="padding:8px 14px;border-bottom:1px solid #2a3f5c;font-family:ui-monospace,monospace">00:50:79:66:68:00</td></tr>
            <tr><td style="padding:8px 14px;border-bottom:1px solid #2a3f5c">PC 2</td><td style="padding:8px 14px;border-bottom:1px solid #2a3f5c;font-family:ui-monospace,monospace">28:39:26:34:82:51</td></tr>
            <tr><td style="padding:8px 14px;border-bottom:1px solid #2a3f5c">PC 3</td><td style="padding:8px 14px;border-bottom:1px solid #2a3f5c;font-family:ui-monospace,monospace">00:50:79:66:68:78</td></tr>
            <tr><td style="padding:8px 14px">PC 4</td><td style="padding:8px 14px;font-family:ui-monospace,monospace">00:50:79:66:68:44</td></tr>
          </tbody>
        </table>
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. An engineer must configure the interface that connects to PC1 and secure it in a way that only PC1 is allowed to use the port. No VLAN tagging can be used except for a voice VLAN. Which command sequence must be entered to configure the switch?",
            "name": "sw1pc1ps1",
            "correct": "B",
            "mono": True,
            "explain": "Correct. B \u2014 **Access mode** is required for an end host (no trunk/DTP). **Port security** is enabled, then **PC 1\u2019s MAC** is bound with **`switchport port-security mac-address 0050.7966.6800`** (Cisco format for **00:50:79:66:68:00**). A **voice VLAN** can still be applied on an access port with **`switchport voice vlan`** without using trunk tagging. **A** uses **nonegotiate** (trunk) and only **`maximum 1`**, which does not statically pin PC1\u2019s address. **C** negotiates a trunk (**dynamic desirable**) and misuses **sticky**. **D** uses **dynamic auto** and **restrict** without binding PC1\u2019s MAC.",
            "choices": [
                "SW1(config-if)#switchport mode nonegotiate\nSW1(config-if)#switchport port-security\nSW1(config-if)#switchport port-security maximum 1",
                "SW1(config-if)#switchport mode access\nSW1(config-if)#switchport port-security\nSW1(config-if)#switchport port-security mac-address 0050.7966.6800",
                "SW1(config-if)#switchport mode dynamic desirable\nSW1(config-if)#switchport port-security mac-address 0050.7966.6800\nSW1(config-if)#switchport port-security mac-address sticky",
                "SW1(config-if)#switchport mode dynamic auto\nSW1(config-if)#switchport port-security\nSW1(config-if)#switchport port-security violation restrict",
            ],
        },
        {
            "slug": "r2-wan-ipv6-global-unicast-internet-access",
            "title": "CCNA — R2 WAN IPv6 global unicast (Internet)",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/r2-wan-ipv6-global-unicast-internet-topology.png" alt="Topology: R1 and R2 on G0/0; R1 to SW1 with file and network management servers on 2001:DB8:D8D2:1008::/64; R2 G0/1 to ISP Internet; R2 to SW2 with IP phones and workstations on 2001:DB8:D8D2:1009::/64." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. A public IPv6 address must be configured for internet access. Which command must be configured on the R2 WAN interface to the service provider?",
            "name": "r2wanipv61",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 Internet access on the **WAN** requires a **global unicast** IPv6 address (2000::/3, including documentation prefix **2001:db8::/32**) assigned with **`ipv6 address \u2026/prefix-length`**. **A** configures only a **link-local** address (**fe80::/10**), which is not used as the routable provider-facing global address. **B** is invalid IOS syntax. **C** misapplies **anycast** on a standard WAN interface assignment; anycast is a special unicast address shared by multiple nodes, not the normal ISP handoff address.",
            "choices": [
                "ipv6 address fe80::260:3EFF:FE11:6770 link-local",
                "ipv6 address fe80: :/10",
                "ipv6 address 2001:db8:433:47:4620:ffff:ffff:ffff/64 anycast",
                "ipv6 address 2001:db8:123:45::4/64",
            ],
        },
        {
            "slug": "sw1-sw2-trunk-native-vlan5-layer3-all-pcs",
            "title": "CCNA — SW1/SW2 trunks, native VLAN 5, all PCs",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/sw1-sw2-vlan7-9-108-trunk-native5-topology.png" alt="Topology: SW1 Gi0/0 PC4 VLAN 108, Gi0/1 trunk to SW2 Gi0/7, Gi0/2 to R1; SW2 Gi0/0 PC1 VLAN 9, Gi0/1 PC2 VLAN 7." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. The SW1 and SW2 Gi0/0 ports have been preconfigured. An engineer is given these requirements:\n\n\u2022 Allow all PCs to communicate with each other at Layer 3.\n\u2022 Configure untagged traffic to use VLAN 5.\n\u2022 Disable VLAN 1 from being used.\n\nWhich configuration set meets these requirements?",
            "name": "sw12trnk1",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 **Gi0/1** and **Gi0/7** trunks carry VLANs **5, 7, 9, and 108** with **native VLAN 5** so untagged traffic is not on VLAN 1. **Gi0/2** toward **R1** is a **trunk** with the same VLAN set so the router can route between **VLAN 7, 9, and 108** for inter-PC Layer 3. **SW2 Gi0/1** is **access VLAN 7** for **PC2** (Gi0/0 is already VLAN 9). **A** omits **native VLAN 5**, misconfigures **SW2 Gi0/1** as a trunk, and limits **Gi0/2** allowed VLANs. **B** sets **Gi0/2** to **access** while applying trunk commands and omits **VLAN 108** on **SW2 Gi0/7**. **C** leaves **SW2 Gi0/7** without **VLAN 108** and without **native VLAN 5**.",
            "choices": [
                """SW1#
interface Gi0/1
 switchport mode trunk
 switchport trunk allowed vlan 5,7,9,108
!
interface Gi0/2
 switchport mode trunk
 switchport trunk allowed vlan 7,9,108
!
SW2#
interface Gi0/1
 switchport mode trunk
 switchport trunk allowed vlan 7
!
interface Gi0/7
 switchport mode trunk
 switchport trunk allowed vlan 5,7,9,108""",
                """SW1#
interface Gi0/1
 switchport mode trunk
 switchport trunk allowed vlan 5,7,9,108
 switchport trunk native vlan 5
!
interface Gi0/2
 switchport mode access
 switchport trunk allowed vlan 7,9,108
!
SW2#
interface Gi0/1
 switchport mode access
 no switchport access vlan 1
 switchport access vlan 7
!
interface Gi0/7
 switchport mode trunk
 switchport trunk allowed vlan 7,9,108
 switchport trunk native vlan 5""",
                """SW1#
interface Gi0/1
 switchport mode trunk
 switchport trunk allowed vlan 5,7,9,108
 switchport trunk native vlan 5
!
interface Gi0/2
 switchport mode trunk
 switchport trunk allowed vlan 5,7,9,108
!
SW2#
interface Gi0/1
 switchport mode access
 switchport access vlan 7
!
interface Gi0/7
 switchport mode trunk
 switchport trunk allowed vlan 7,9,108""",
                """SW1#
interface Gi0/1
 switchport mode trunk
 switchport trunk allowed vlan 5,7,9,108
 switchport trunk native vlan 5
!
interface Gi0/2
 switchport mode trunk
 switchport trunk allowed vlan 5,7,9,108
!
SW2#
interface Gi0/1
 switchport mode access
 switchport access vlan 7
!
interface Gi0/7
 switchport mode trunk
 switchport trunk allowed vlan 5,7,9,108
 switchport trunk native vlan 5""",
            ],
        },
        {
            "slug": "r1-r2-p2p-subnet-minimum-two-growth-hosts",
            "title": "CCNA — R1–R2 P2P link subnet (minimum + growth)",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/r1-r2-gi0-0-p2p-link-subnet-topology.png" alt="Topology: Router R1 GigabitEthernet0/0 connected to Router R2 GigabitEthernet0/0 on a point-to-point link." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. A network engineer must configure the link with these requirements:\n\n\u2022 Consume as few IP addresses as possible.\n\u2022 Leave at least two additional useable IP addresses for future growth.\n\nWhich set of configurations must be applied?",
            "name": "r1r2p2p1",
            "correct": "A",
            "mono": True,
            "explain": "Correct. A \u2014 The link needs **two** router addresses plus **at least two spare usable hosts**, so **four usable addresses** minimum. A **/29** mask (**255.255.255.248**) provides **six** usable hosts in the block (for example **10.10.10.1** and **10.10.10.4** on **10.10.10.0/29**) and is the **smallest** mask that satisfies both requirements. **C** (**/30**) offers only **two** usable addresses\u2014no room for growth. **B** (**/28**) and **D** (**/24**) work but waste more addresses than necessary.",
            "choices": [
                "R1(config-if)#ip address 10.10.10.1 255.255.255.248\nR2(config-if)#ip address 10.10.10.4 255.255.255.248",
                "R1(config-if)#ip address 10.10.10.1 255.255.255.240\nR2(config-if)#ip address 10.10.10.12 255.255.255.240",
                "R1(config-if)#ip address 10.10.10.1 255.255.255.252\nR2(config-if)#ip address 10.10.10.2 255.255.255.252",
                "R1(config-if)#ip address 10.10.10.1 255.255.255.0\nR2(config-if)#ip address 10.10.10.5 255.255.255.0",
            ],
        },
        {
            "slug": "r1-gi0-0-ipv6-eui64-dynamic-assignment-block",
            "title": "CCNA — R1 Gi0/0 IPv6 EUI-64 (dynamic assignment)",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/r1-r2-ipv6-block-gi0-0-lan-topology.png" alt="Topology: IPv6 block 2001:db8:ffff:fcf3::/64; R1 and R2 on GigabitEthernet0/1; R1 GigabitEthernet0/0 and R2 GigabitEthernet0/0 each to a switch with host PCs." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. IPv6 is being implemented within the enterprise. The command **ipv6 unicast-routing** is configured. Interface **Gig0/0** on **R1** must be configured to provide a dynamic assignment using the assigned IPv6 block. Which command accomplishes this task?",
            "name": "r1gi0v61",
            "correct": "A",
            "mono": True,
            "explain": "Correct. A \u2014 **`ipv6 address 2001:DB8:FFFF:FCF3::/64 eui-64`** applies the assigned **/64** prefix on **R1 Gi0/0**, builds the router\u2019s interface ID with **EUI-64**, and advertises the prefix so hosts on the LAN can **dynamically autoconfigure** global addresses via **SLAAC** (with **ipv6 unicast-routing** enabled). **B** configures only a **link-local** address, not the assigned global block for client assignment. **C** is a **static** global address (**::1**), not dynamic host assignment on the segment. **D** uses invalid syntax, the wrong prefix (**FCF2**), and **autoconfig** is for a host to learn its own address\u2014not for the router to assign addresses from the enterprise block.",
            "choices": [
                "ipv6 address 2001:DB8:FFFF:FCF3::/64 eui-64",
                "ipv6 address 2001:DB8:FFFF:FCF3::/64 link-local",
                "ipv6 address 2001:0B8:FFFF:FCF3::1/64",
                "ipv6 address autoconfig 2001:DB8:FFFF:FCF2::/64",
            ],
        },
        {
            "slug": "ntp-clients-r1-r2-r3-show-run-exhibit",
            "title": "CCNA — Which routers are NTP clients?",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/ntp-r1-r4-diamond-topology.png" alt="Topology: R1 to Internet and Loopback0 172.16.0.1; R1–R2 10.10.10.0/30, R1–R3 10.10.10.8/30, R2–R4 10.10.10.4/30, R3–R4 10.10.10.12/30." width="900" decoding="async" loading="lazy" />
      </figure>
      <div class="exhibit-router-cli" role="region" aria-label="NTP configuration excerpts from R1 through R4">
        <pre>R1#show run | include ntp
ntp master 7
ntp server 209.165.200.225

R2#show run | include ntp
ntp server 172.16.0.1

R3#show run | include ntp
ntp master 6
ntp server 172.16.0.1

R4#show run | include ntp
ntp master 7</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. Which router or router group are NTP clients?",
            "name": "ntpclnt1",
            "correct": "A",
            "explain": "Correct. A \u2014 **`ntp server`** configures a device as an **NTP client** (it synchronizes to the listed server). **R1** uses **`ntp server 209.165.200.225`**, **R2** uses **`ntp server 172.16.0.1`**, and **R3** also uses **`ntp server 172.16.0.1`**. **R4** has only **`ntp master 7`** and no **`ntp server`** line, so it is not acting as a client in this output. A router can be both **master** and **client** (**R1** and **R3**); the question asks which devices are clients.",
            "choices": [
                "R1, R2, and R3",
                "R1",
                "R2 and R3",
                "R1, R3, and R4",
            ],
        },
        {
            "slug": "r1-floating-default-route-pc1-pc3-routing",
            "title": "CCNA — R1 floating default route (PC1 to PC3)",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/r1-r2-r3-floating-default-pc1-pc3-topology.png" alt="Topology: R1 PC1 172.16.30.0/24; R1 S0/0/0 to R3 172.16.20.0/24 (.1/.2), R1 S0/0/1 to R2 10.0.0.0/24 (.1/.2); R3 PC3 172.16.10.0/24; R2 PC2 192.168.200.0/24; R2–R3 209.165.201.0/27." width="900" decoding="async" loading="lazy" />
      </figure>
      <div class="exhibit-router-cli" role="region" aria-label="R1 default static route configuration">
        <pre>R1(config)#ip route 0.0.0.0 0.0.0.0 172.16.20.2
R1(config)#ip route 0.0.0.0 0.0.0.0 10.0.0.2 20</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. After applying this configuration to router **R1**, a network engineer is verifying the implementation. If all links are operating normally, and the engineer sends a series of packets from **PC1** to **PC3**, how are the packets routed?",
            "name": "r1fltdef1",
            "correct": "A",
            "explain": "Correct. A \u2014 Two default static routes are configured; the first (**`ip route 0.0.0.0 0.0.0.0 172.16.20.2`**) uses the default administrative distance **1**, and the second points to **10.0.0.2** with **AD 20**. While all links are up, the **lower-AD** default is installed and used, so traffic from **PC1** toward **PC3** follows the primary next hop **172.16.20.2**. **D** is the **floating backup** used only when the preferred path is unavailable. **B** describes load sharing across serial interfaces, which these static defaults do not configure. **C** is not a next hop in this configuration.",
            "choices": [
                "They are routed to 172.16.20.2.",
                "They are distributed sent round robin to interfaces S0/0/0 and S0/0/1.",
                "They are routed to 192.168.100.2.",
                "They are routed to 10.0.0.2.",
            ],
        },
        {
            "slug": "router1-pat-1921681-pool-209165202129",
            "title": "CCNA — ROUTER-1 PAT for 192.168.1.0/24",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/router1-pat-1921681-internet-topology.png" alt="Topology: ROUTER-1 to Internet; SWITCH-1 and SWITCH-2 with users on subnet 192.168.1.0/24." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. Which command set configures **ROUTER-1** to allow Internet access for users on the **192.168.1.0/24** subnet while using **209.165.202.129** for Port Address Translation?",
            "name": "r1pat1",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 **PAT** uses a **NAT pool** of the public address **209.165.202.129**, **`access-list 10 permit 192.168.1.0 0.0.0.255`** (standard ACL **wildcard** for the inside /24), and **`ip nat inside source list 10 pool CCNA overload`**. **A** and **C** put **private** addresses in the **NAT pool**, which cannot provide Internet PAT with the given public IP. **B** uses the correct public pool but **`255.255.255.0`** in the ACE is a **subnet mask**, not the required **wildcard** for a standard numbered ACL.",
            "choices": [
                "ip nat pool CCNA 192.168.0.0 192.168.1.255 netmask 255.255.255.0\n\naccess-list 10 permit 192.168.0.0 0.0.0.255\nip nat inside source list 10 pool CCNA overload",
                "ip nat pool CCNA 209.165.202.129 209.165.202.129 netmask 255.255.255.255\n\naccess-list 10 permit 192.168.1.0 255.255.255.0\nip nat inside source list 10 pool CCNA overload",
                "ip nat pool CCNA 192.168.0.0 192.168.1.255 netmask 255.255.255.0\n\naccess-list 10 permit 192.168.0.0 255.255.255.0\nip nat inside source list 10 pool CCNA overload",
                "ip nat pool CCNA 209.165.202.129 209.165.202.129 netmask 255.255.255.255\n\naccess-list 10 permit 192.168.1.0 0.0.0.255\nip nat inside source list 10 pool CCNA overload",
            ],
        },
        {
            "slug": "sw1-voip-lldp-gi101-multivendor-discovery",
            "title": "CCNA — SW1 VoIP LLDP on Gi1/0/1 only",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/sw1-gi101-non-cisco-ip-phone-lldp-topology.png" alt="Topology: Cisco SW1 GigabitEthernet1/0/1 to non-Cisco IP phone with laptop connected behind the phone." width="900" decoding="async" loading="lazy" />
      </figure>
      <div class="exhibit-router-cli" role="region" aria-label="SW1 partial configuration">
        <pre>SW1#
vlan 10
 name Voice
vlan 11
 name Data
cdp run
interface GigabitEthernet1/0/1
 switchport access vlan 11
 switchport mode access
 switchport voice vlan 10
 spanning-tree portfast
 no shut
end
copy run start</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. A multivendor network exists and the company is implementing VoIP over the network for the first time. Which configuration is needed to implement the neighbor discovery protocol on the interface and allow it to remain off for the remaining interfaces?",
            "name": "sw1lldp1",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 **LLDP** is the **IEEE** neighbor discovery protocol used in **multivendor** networks. **`no cdp run`** disables Cisco-proprietary **CDP** globally (replacing the exhibit\u2019s **`cdp run`**). On **GigabitEthernet1/0/1** only, **`lldp transmit`** and **`lldp receive`** enable LLDP without turning it on for every other interface the way global **`lldp run`** would. **A** keeps **CDP** and misapplies **`cdp run`** under the interface. **B** and **C** use invalid or global LLDP commands (**`lldp enable`**, **`lldp run`**) that do not match the per-interface requirement.",
            "choices": [
                "SW1(config)#no cdp enable\nSW1(config)#interface gigabitethernet1/0/1\nSW1(config-if)#cdp run",
                "SW1(config)#lldp enable\nSW1(config)#interface gigabitethernet1/0/1\nSW1(config-if)#lldp run",
                "SW1(config)#lldp run\nSW1(config)#interface gigabitethernet1/0/1\nSW1(config-if)#lldp enable",
                "SW1(config)#no cdp run\nSW1(config)#interface gigabitethernet1/0/1\nSW1(config-if)#lldp transmit\nSW1(config-if)#lldp receive",
            ],
        },
        {
            "slug": "wlc-guest-wlan-layer2-prep-web-auth-choose-two",
            "title": "CCNA — Guest WLAN Layer 2 prep for web auth",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/wlc-guest-wlan-layer2-security-tab-exhibit.png" alt="WLC WLAN Security tab, Layer 2 sub-tab: Layer 2 Security WPA+WPA2, Security Type Enterprise, MAC Filtering enabled, WPA Policy and 802.1X-SHA1 enabled." width="900" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. A guest WLAN must be created that prompts the client for a username and password on the local web page of the WLC. Which two actions must be performed on the **Layer 2** tab before enabling the **Authentication** option on the **Layer 3** tab? (Choose two.)",
            "name": "wlcguestl2",
            "choose_two": True,
            "correct": ["A", "D"],
            "explain": "Correct. A and D \u2014 **Guest web authentication** (Layer 3) needs clients to associate with **open Layer 2** first, then redirect to the WLC splash page for credentials. Set **Layer 2 Security** to **None** and **uncheck MAC Filtering** before you enable **Authentication** on the **Layer 3** tab. **B** (**Personal**/PSK) is for WPA passphrase WLANs, not this web-login guest flow. **C** changes WPA ciphers but does not replace the Layer 2 open + no MAC filter requirement. **E** adjusts WPA/WPA2 policies while Layer 2 remains secured, which blocks the usual guest web-auth association model.",
            "choices": [
                "Uncheck the MAC Filtering option check box.",
                "Set the Security Type option to Personal.",
                "Change the WPA Encryption option from TKIP to CCMP128(AES).",
                "Set the Layer 2 Security option to None.",
                "Uncheck the WPA Policy option check box, and check the WPA2 Policy option check box.",
            ],
        },
        {
            "slug": "r1-static-host-10-10-2-1-via-r3-ospf-override",
            "title": "CCNA — Static /32 to 10.10.2.1 via R3",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/r1-static-host-10-10-2-1-via-r3-ospf-override-topology.png" alt="Topology: R1 to R2 (192.168.1.2) and R3 (192.168.1.4) on 192.168.1.0/24; both routers reach 10.10.2.0/24 with hosts 10.10.2.2 and 10.10.2.1." width="980" decoding="async" loading="lazy" />
      </figure>
      <div class="exhibit-router-cli" role="region" aria-label="R1 show ip route 10.10.2.1 output">
        <pre>R1#show ip route 10.10.2.1
Routing entry for 10.10.2.0/24
  Known via "ospf 1", distance 110, metric 2, type intra area
  Last update from 192.168.1.2 on GigabitEthernet0/0, 01:33:22 ago
  Routing Descriptor Blocks:
  * 192.168.1.2, from 10.10.2.1, 01:33:22 ago, via GigabitEthernet0/0
      Route metric is 2, traffic share count is 1</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. Traffic from **R1** to the **10.10.2.0/24** subnet uses **192.168.1.2** as its next hop. A network engineer wants to update the **R1** configuration so that traffic with destination **10.10.2.1** passes through router **R3**, and all other traffic to the **10.10.2.0/24** subnet passes through **R2**. Which command must be used?",
            "name": "r1st21021",
            "correct": "D",
            "explain": "Correct. D \u2014 The exhibit shows **10.10.2.0/24** learned by **OSPF** with administrative distance **110** via **192.168.1.2** (**R2**). To steer only **10.10.2.1** through **R3** (**192.168.1.4**), add a **more specific /32 static** with **AD 100** (lower than **110**): **`ip route 10.10.2.1 255.255.255.255 192.168.1.4 100`**. Other hosts in **10.10.2.0/24** still match the OSPF /24 via **R2**. **A** and **C** use **AD 115**, so OSPF remains preferred. **B** installs a /24 static that would redirect the entire subnet to **R3**, not only **10.10.2.1**.",
            "choices": [
                "ip route 10.10.2.1 255.255.255.255 192.168.1.4 115",
                "ip route 10.10.2.0 255.255.255.0 192.168.1.4 100",
                "ip route 10.10.2.0 255.255.255.0 192.168.1.4 115",
                "ip route 10.10.2.1 255.255.255.255 192.168.1.4 100",
            ],
            "mono": True,
        },
        {
            "slug": "pc-internet-tcp80-www-cisco-subnet-mask-exhibit",
            "title": "CCNA — PC internet access (subnet mask)",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/pc-internet-tcp80-www-cisco-topology.png" alt="Topology: Internet to router 10.2.2.1/27, switch, and PC 10.2.2.2." width="980" decoding="async" loading="lazy" />
      </figure>
      <div class="exhibit-terminal-white" role="region" aria-label="Windows ipconfig /all output">
        <pre>C:\\&gt;ipconfig /all

Ethernet adapter Ethernet:

   Connection-specific DNS Suffix  . :
   Physical Address. . . . . . . . . : F8-75-A4-3B-AB-4F
   Link-local IPv6 Address . . . . . : fe80::644a:b01:3e5f:ae6%14(Preferred)
   IPv4 Address. . . . . . . . . . . : 10.2.2.2(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.255.192
   Default Gateway . . . . . . . . . : 10.2.2.1
   DHCP Server . . . . . . . . . . . : 192.168.1.15
   DNS Servers . . . . . . . . . . . : 8.8.8.8
   NetBIOS over Tcpip. . . . . . . . : Enabled</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. A newly configured PC fails to connect to the internet using TCP port 80 to **www.cisco.com**. Which setting must be modified for the connection to work?",
            "name": "pcinf801",
            "correct": "A",
            "explain": "Correct. A \u2014 The topology labels the router LAN as **10.2.2.1/27** (mask **255.255.255.224**). The PC\u2019s **ipconfig** shows **255.255.255.192** (/26), so the host is not using the same prefix length as the segment. Change the **subnet mask** to **255.255.255.224** so **10.2.2.2** and default gateway **10.2.2.1** share the correct **10.2.2.0/27** subnet; then off-net traffic (DNS to **8.8.8.8**, then HTTP to **www.cisco.com**) can flow. **B** **8.8.8.8** is a valid public DNS server once Layer 3 to the gateway works. **C** default gateway **10.2.2.1** already matches the router in the diagram. **D** the listed **DHCP server** address does not fix the mask mismatch on this **10.2.2.0/27** LAN.",
            "choices": [
                "Subnet Mask",
                "DNS Servers",
                "Default Gateway",
                "DHCP Server",
            ],
        },
        {
            "slug": "etherchannel-sw2-port-channel1-min-links-exhibit",
            "title": "CCNA — Port-channel min-links on SW2",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/sw2-port-channel1-min-links-lacp-topology.png" alt="Topology: PC1 on SW1, server on SW2, SW1-SW2-SW3 triangle with LACP Port Channel 1 (Ge0/0-2) between SW1 and SW2." width="980" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. **PC1** regularly sends **1800 Mbps** of traffic to the server. A network engineer needs to configure the EtherChannel to disable **Port Channel 1** between **SW1** and **SW2** when the **Ge0/0** and **Ge0/1** ports on **SW2** go down. Which configuration must the engineer apply to the switch?",
            "name": "sw2pomin1",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 **`port-channel min-links 2`** on **interface port-channel 1** keeps the bundle up only while at least **two** member links are active. If **Ge0/0** and **Ge0/1** fail, only **Ge0/2** remains (about **1 Gbps**), which is below the **1800 Mbps** need and below the minimum; **Port Channel 1** is disabled so traffic can use alternate paths (for example via **SW3**). **A** **`lacp port-priority`** affects which ports are preferred in negotiation, not minimum active links. **B** **`lacp max-bundle`** caps how many ports may join the bundle, not when the channel shuts down. **C** **`lacp system-priority`** is a global LACP system ID preference, unrelated to minimum link count on **Po1**.",
            "choices": [
                """SW2#configure terminal
SW2(config)# interface port-channel 1
SW2(config-if)#lacp port-priority 32000""",
                """SW2#configure terminal
SW2(config)#interface port-channel 1
SW2(config-if)#lacp max-bundle 2""",
                """SW2#configure terminal
SW2(config)#lacp system-priority 32000""",
                """SW2#configure terminal
SW2(config)#interface port-channel 1
SW2(config-if)#port-channel min-links 2""",
            ],
        },
        {
            "slug": "newsw-trunk-native-vlan2-sw1-fa0-exhibit",
            "title": "CCNA — NewSW trunk to SW2",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/newsw-trunk-native-vlan2-topology.png" alt="Topology: SW1 and SW2 with PCs in VLAN 2; NewSW below SW2 with VLAN 10 hosts; NewSW f0/0 uplink to SW2." width="980" decoding="async" loading="lazy" />
      </figure>
      <div class="exhibit-router-cli" role="region" aria-label="SW1 show interface output">
        <pre>SW1#show interface
interface FastEthernet0/0
 switchport access vlan 2
 switchport mode access</pre>
      </div>
    </div>""",
            "stem": "Refer to the exhibit. A network administrator must connect **NewSW** to **SW2** on interface **FastEthernet0/0**. Hosts in **VLAN 2** must stay reachable, and **VLAN 10** must also cross the link. Which configuration must be applied on **NewSW**?",
            "name": "newswtrk1",
            "correct": "A",
            "mono": True,
            "explain": "Correct. A \u2014 The topology shows existing hosts in **VLAN 2** and new hosts in **VLAN 10** on **NewSW**. Configure **trunk** mode on **NewSW** **f0/0** with **`switchport trunk allowed vlan 2,10`** and **`switchport trunk native vlan 2`** so **VLAN 2** stays reachable across the network while **VLAN 10** is added. **B** allows only **VLAN 10** and sets **native VLAN 10**, breaking **VLAN 2** reachability. **C** and **D** use **`switchport mode access`** with trunk **allowed/native** commands, which is an invalid combination; trunk settings apply only in trunk mode.",
            "choices": [
                """NewSW(config)#interface f0/0
NewSW(config-if)#switchport mode trunk
NewSW(config-if)#switchport trunk allowed vlan 2,10
NewSW(config-if)#switchport trunk native vlan 2""",
                """NewSW(config)#interface f0/0
NewSW(config-if)#switchport mode trunk
NewSW(config-if)#switchport trunk allowed vlan 10
NewSW(config-if)#switchport trunk native vlan 10""",
                """NewSW(config)#interface f0/0
NewSW(config-if)#switchport mode access
NewSW(config-if)#switchport trunk allowed vlan 2,10
NewSW(config-if)#switchport trunk native vlan 10""",
                """NewSW(config)#interface f0/0
NewSW(config-if)#switchport mode access
NewSW(config-if)#switchport trunk allowed vlan 2,10
NewSW(config-if)#switchport trunk native vlan 2""",
            ],
        },
        {
            "slug": "wlc-userwl-vlan20-max-allowed-clients-exhibit",
            "title": "CCNA — WLC WLAN max clients (USERWL)",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/wlc-userwl-vlan20-max-clients-topology.png" alt="Topology: AP with SSID USERWL on 172.16.10.0/24 connected through network cloud to WLC on VLAN 20 (172.16.10.0/24)." width="980" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. A network engineer is configuring a WLAN to connect with the **172.16.10.0/24** network on **VLAN 20**. The engineer wants to limit the number of devices that connect to the WLAN on the **USERWL** SSID to **125**. Which configuration must the engineer perform on the WLC?",
            "name": "wlcusr125",
            "correct": "A",
            "explain": "Correct. A \u2014 On a Cisco WLC, cap the number of clients associated to a WLAN by setting **Maximum Allowed Clients** in that **WLAN\u2019s** configuration (for **USERWL** on **VLAN 20** / **172.16.10.0/24**). **B** **DTIM** (Delivery Traffic Indication Map) controls how often the AP buffers multicast/broadcast for sleeping clients\u2014it is not a client limit. **C** **Controller IPv6 Throttle** limits IPv6 traffic rate, not WLAN association count. **D** **Management Software activation Clients** is unrelated to per-WLAN association limits.",
            "choices": [
                "In the WLAN configuration, set the Maximum Allowed Clients value to 125.",
                "In the Advanced configuration, set the DTIM value to 125.",
                "In the Controller IPv6 configuration, set the Throttle value to 125.",
                "In the Management Software activation configuration, set the Clients value to 125.",
            ],
        },
        {
            "slug": "cpe-dual-isp-static-route-load-balance-exhibit",
            "title": "CCNA — CPE dual-ISP static load balance",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/cpe-dual-isp-static-load-balance-topology.png" alt="Topology: CPE at Headquarters with links to ISP 1 (198.51.100.1) and ISP 2 (203.0.113.1)." width="980" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. A network administrator configures the **CPE** to provide internet access to the company headquarters. Traffic must be load-balanced via **ISP1** and **ISP2** to ensure redundancy. Which two command sets must be configured on the **CPE** router? (Choose two.)",
            "name": "cpedualisp1",
            "choose_two": True,
            "mono": True,
            "correct": ["C", "E"],
            "explain": "Correct. C and E \u2014 **C** uses two static routes that split the destination space: **0.0.0.0/1** via **198.51.100.1** (**ISP1**) and **128.0.0.0/1** via **203.0.113.1** (**ISP2**), load-sharing across both links. **E** uses two equal **0.0.0.0/0** static routes (same administrative distance) to each ISP, which the router can load-balance (**ECMP**). **A** sets **ISP2** as a floating backup (**AD 2**), not load sharing. **B** adds extra full defaults beyond the /1 split. **D** uses **AD 255**, so those routes are not installed.",
            "choices": [
                """ip route 0.0.0.0 0.0.0.0 198.51.100.1
ip route 0.0.0.0 0.0.0.0 203.0.113.1 2""",
                """ip route 0.0.0.0 128.0.0.0 198.51.100.1
ip route 128.0.0.0 128.0.0.0 203.0.113.1
ip route 0.0.0.0 0.0.0.0 198.51.100.1
ip route 0.0.0.0 0.0.0.0 203.0.113.1""",
                """ip route 0.0.0.0 128.0.0.0 198.51.100.1
ip route 128.0.0.0 128.0.0.0 203.0.113.1""",
                """ip route 0.0.0.0 0.0.0.0 198.51.100.1 255
ip route 0.0.0.0 0.0.0.0 203.0.113.1 255
ip route 128.0.0.0 128.0.0.0 203.0.113.1""",
                """ip route 0.0.0.0 0.0.0.0 198.51.100.1
ip route 0.0.0.0 0.0.0.0 203.0.113.1""",
            ],
        },
        {
            "slug": "r2-lan-ipv6-eui64-address-exhibit",
            "title": "CCNA — R2 LAN IPv6 EUI-64 address",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/r2-lan-ipv6-eui64-topology.png" alt="Topology: R1 and R2 on 2001:DB8:44:90::/64; R1 LAN 2001:DB8:D8D2:1008::/64; R2 LAN 2001:DB8:D8D2:1009::/64 with MAC 12-a0-ab-cc-00-01 on R2." width="980" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. The IPv6 address for the LAN segment on router **R2** must be configured using the **EUI-64** format. Which address must be used?",
            "name": "r2eui641",
            "correct": "A",
            "mono": True,
            "explain": "Correct. A \u2014 **R2** MAC **12-A0-AB-CC-00-01** on prefix **2001:DB8:D8D2:1009::/64**: insert **FF:FE** after the OUI (**12A0.AB** \u2192 **12A0.ABFF.FE**), append **CC:00:01**, then invert the **7th bit** of the first octet (**0x12** \u2192 **0x10**), yielding interface ID **10A0:ABFF:FECC:1** and **`ipv6 address 2001:DB8:D8D2:1009:10A0:ABFF:FECC:1 eui-64`**. **B** misplaces **FF:FE** (**AB34:FFCC**). **C** uses **1230** instead of **10A0** after the U/L-bit flip. **D** does not follow **R2\u2019s** MAC-derived **EUI-64** pattern.",
            "choices": [
                "ipv6 address 2001:DB8:D8D2:1009:10A0:ABFF:FECC:1 eui-64",
                "ipv6 address 2001:DB8:D8D2:1009:12A0:AB34:FFCC:1 eui-64",
                "ipv6 address 2001:DB8:D8D2:1009:1230:ABFF:FECC:1 eui-64",
                "ipv6 address 2001:DB8:D8D2:1009:4345:80FF:FF16:7 eui-64",
            ],
        },
        {
            "slug": "switch-a-etherchannel-lacp-passive-exhibit",
            "title": "CCNA — Switch A LACP passive (Po1)",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/switch-a-etherchannel-lacp-passive-topology.png" alt="Topology: Switch A and Switch B with EtherChannel group 1 on GigabitEthernet0/0/0 through 0/0/15; hosts below each switch." width="980" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. The EtherChannel is configured with a speed of **1000** and duplex **full** on both ends of **channel group 1**. What is the next step to configure the channel on **switch A** to respond to but not initiate **LACP** communication?",
            "name": "swalacpp1",
            "correct": "A",
            "mono": True,
            "explain": "Correct. A \u2014 **LACP passive** waits for LACPDUs from the neighbor and responds but does not initiate negotiation. Apply **`channel-group 1 mode passive`** under the member interfaces **`GigabitEthernet0/0/0\u201315`** (interface range). **B** **`mode on`** is a static EtherChannel without LACP negotiation. **C** **`mode auto`** is **PAgP**, not LACP, and belongs on physical members, not under **`interface port-channel`**. **D** uses the correct keyword **passive** but on **`port-channel 1`**; IOS sets **channel-group** mode on the physical ports in the bundle, not on the logical port-channel interface.",
            "choices": [
                """interface range gigabitethernet0/0/0 -15
channel-group 1 mode passive""",
                """interface range gigabitethernet0/0/0 -15
channel-group 1 mode on""",
                """interface port-channel 1
channel-group 1 mode auto""",
                """interface port-channel 1
channel-group 1 mode passive""",
            ],
        },
        {
            "slug": "r4-local-telnet-enable-secret-vty-exhibit",
            "title": "CCNA — R4 Telnet and enable secret",
            "prepend_html": """    <div class="exhibit-stack">
      <figure class="exhibit-photo">
        <img src="/CCNA-Study/CCNA_questions/images/r4-local-telnet-enable-secret-wan-topology.png" alt="Topology: WAN cloud with R4 on 10.111.87.0/30, R6 on 10.110.198.0/30, and R5 on 10.128.1.0/30." width="980" decoding="async" loading="lazy" />
      </figure>
    </div>""",
            "stem": "Refer to the exhibit. Local access for **R4** must be established and these requirements must be met:\n\n\u2022 Only **Telnet** access is allowed.\n\u2022 The **enable** password must be stored securely.\n\u2022 The **enable** password must be applied in plain text.\n\u2022 **Full access** to **R4** must be permitted upon successful login.\n\nWhich configuration script meets the requirements?",
            "name": "r4tel1",
            "correct": "B",
            "mono": True,
            "explain": "Correct. B \u2014 **`transport input telnet`** limits **VTY** access to **Telnet** only. **`login local`** uses the **`username test1 password`** database for line login. **`enable secret level 15 0 Test123`** stores the enable password **securely** (hashed **secret**) while **`0`** lets you enter **Test123** in **plain text** on the CLI; **level 15** grants **full** privileged access after login. **A** uses **`enable password`** (not stored securely), **level 1** (not full access), and **`transport input all`**. **C** sets **`enable secret level 1`** (not full access) and invalid **`login authentication`** / line **`password`** patterns for this task. **D** uses **`enable password`** (not secure) and **`transport input all`**.",
            "choices": [
                """Option A

!
conf t
!
username test1 password testpass1
enable password level 1 7 Test123
!
line vty 0 15
accounting exec default
transport input all""",
                """Option B

conf t
!
username test1 password testpass1
enable secret level 15 0 Test123
!
line vty 0 15
login local
transport input telnet""",
                """Option C

!
config t
!
username test1 password testpass1
enable secret level 1 0 Test123
!
line vty 0 15
login authentication
password Test123
transport input telnet""",
                """Option D

!
config t
!
username test1 password testpass1
enable password level 15 0 Test123
!
line vty 0 15
password Test123
transport input all""",
            ],
        },
        {
            "slug": "dscp-phb-assured-forwarding-drop-probability",
            "title": "CCNA — DSCP AF drop probability subclasses",
            "stem": "Which **DSCP** per-hop forwarding behavior is divided into subclasses based on **drop probability**?",
            "name": "dscpaf1",
            "correct": "B",
            "explain": "Correct. B \u2014 **Assured Forwarding (AF)** is the **DSCP PHB** with multiple traffic classes and **three drop precedences** (low, medium, high drop probability), shown as **AFxy** (for example **AF21**, **AF22**, **AF23**). **Class-selector (CS)** maps to legacy IP precedence and is not organized by drop probability subclasses. **Expedited Forwarding (EF)** is a single low-delay PHB for priority traffic (for example voice), not AF-style drop tiers. **Default (BE)** is best-effort forwarding without assured drop-probability subclasses.",
            "choices": [
                "class-selector",
                "assured",
                "expedited",
                "default",
            ],
        },
        {
            "slug": "switch-frame-switching-known-destination-forward",
            "title": "CCNA — Frame switching on a switch",
            "stem": "How does **frame switching** function on a switch?",
            "name": "swfrsw1",
            "correct": "D",
            "explain": "Correct. D \u2014 A switch **learns source MAC addresses** on each port and forwards frames based on the **destination MAC**. If the destination is **known** in the **CAM/MAC table**, the frame is sent **only to that egress port**. **A** is wrong: **CDP** is a **neighbor discovery** protocol, not the forwarding mechanism for user data frames. **B** is wrong: switches do not normally **modify** frame contents for **known source VLAN** tagging on standard L2 forwarding. **C** is wrong: **unknown** destinations are typically **flooded** within the VLAN (except the ingress port), not **dropped**.",
            "choices": [
                "forwards frames to a neighbor port using CDP",
                "modifies frames that contain a known source VLAN",
                "inspects and drops frames from unknown destinations",
                "forwards known destinations to the destination port",
            ],
        },
        {
            "slug": "endpoint-protection-antivirus-software",
            "title": "CCNA — Endpoint protection from attack",
            "stem": "What is used as a solution for protecting an **individual network endpoint** from attack?",
            "name": "endptav1",
            "correct": "C",
            "explain": "Correct. C \u2014 **Antivirus/anti-malware software** runs on the **host (endpoint)** to detect and block malware, exploits, and other threats aimed at that **individual device**. A **router** (**A**) forwards traffic and applies routing policy; it does not replace **per-host** endpoint protection. A **wireless controller** (**B**) manages **WLAN** operation and policies for APs/clients, not standalone endpoint antimalware. **Cisco DNA Center** (**D**) is a **network management/automation** platform for the campus fabric, not host-based endpoint security software.",
            "choices": [
                "Router",
                "Wireless controller",
                "Antivirus software",
                "Cisco DNA Center",
            ],
        },
        {
            "slug": "rest-http-methods-get-post-choose-two",
            "title": "CCNA — REST HTTP methods (choose two)",
            "stem": "Which two **HTTP** methods are suitable for actions performed by **REST-based APIs**? (Choose two.)",
            "name": "restmeth1",
            "choose_two": True,
            "correct": ["C", "D"],
            "explain": "Correct. C and D \u2014 **REST** APIs use standard **HTTP verbs**. **GET** retrieves resource data; **POST** commonly **creates** resources or submits data for processing. **REMOVE** (**A**) is not a standard HTTP method (**DELETE** is used for delete). **REDIRECT** (**B**) describes a response behavior, not a REST API action verb. **POP** (**E**) is unrelated to HTTP/REST.",
            "choices": [
                "REMOVE",
                "REDIRECT",
                "POST",
                "GET",
                "POP",
            ],
        },
        {
            "slug": "wlc-lag-redundancy-bandwidth-layer2-switch",
            "title": "CCNA — WLC LAG to Layer 2 switch",
            "stem": "What provides **connection redundancy**, **increased bandwidth**, and **load sharing** between a **wireless LAN controller** and a **Layer 2 switch**?",
            "name": "wlclagl21",
            "correct": "D",
            "explain": "Correct. D \u2014 **Link aggregation (LAG/EtherChannel)** on **WLC distribution ports** to the **Layer 2 switch** bundles multiple physical links into one logical path, adding **aggregate bandwidth**, **load sharing** across members, and **redundancy** if a link fails. **A** **VLAN trunking** carries multiple VLANs on one link but does not by itself combine links for bandwidth/redundancy. **B** **Tunneling** encapsulates traffic (for example CAPWAP) but is not the L2 link-bundling mechanism described. **C** **First hop redundancy** (for example HSRP/VRRP) provides a **default gateway** backup, not WLC-to-switch port bundling.",
            "choices": [
                "VLAN trunking",
                "tunneling",
                "first hop redundancy",
                "link aggregation",
            ],
        },
        {
            "slug": "hsrp-cisco-proprietary-edge-failover-recovery",
            "title": "CCNA — HSRP Cisco proprietary failover",
            "stem": "Which **Cisco proprietary** protocol ensures traffic recovers **immediately**, **transparently**, and **automatically** when **edge devices** or **access circuits** fail?",
            "name": "hsrpcp1",
            "correct": "D",
            "explain": "Correct. D \u2014 **HSRP (Hot Standby Router Protocol)** is **Cisco\u2019s proprietary** first-hop redundancy protocol. Routers share a **virtual IP/MAC** default gateway; the **standby** takes over if the **active** router or path fails, keeping host traffic flowing with minimal disruption. **A** **SLB** load-balances servers, not edge **default-gateway** failover. **B** **FHRP** is the **family** name (HSRP/VRRP/GLBP), not one Cisco-only protocol. **C** **VRRP** is an **open standard**, not Cisco proprietary.",
            "choices": [
                "SLB",
                "FHRP",
                "VRRP",
                "HSRP",
            ],
        },
        {
            "slug": "wpa3-enhancement-pmf-deauth-disassociation",
            "title": "CCNA — WPA3 PMF deauth defense",
            "stem": "What is an enhancement implemented in **WPA3**?",
            "name": "wpa3pmf1",
            "correct": "D",
            "explain": "Correct. D \u2014 **WPA3** requires **Protected Management Frames (802.11w)**, which helps **defend against spoofed deauthentication and disassociation** attacks that could otherwise drop clients from the WLAN. **A** describes **enterprise** identification patterns (**PKI/RADIUS**), not a WPA3-specific enhancement in these choices. **B** matches **WPA2**-era **802.1X** with **AES-128**, not what distinguishes WPA3 here. **C** **TKIP** and **per-packet keying** are **legacy WPA** features, replaced by stronger ciphers in modern WPA2/WPA3.",
            "choices": [
                "employs PKI and RADIUS to identify access points",
                "applies 802.1x authentication and AES-128 encryption",
                "uses TKIP and per-packet keying",
                "defends against deauthentication and disassociation attacks",
            ],
        },
        {
            "slug": "ipv6-link-local-all-nodes-multicast-ff02-1",
            "title": "CCNA — IPv6 all-nodes multicast",
            "stem": "What is a **link-local all-nodes** IPv6 **multicast** address?",
            "name": "ipv6an1",
            "correct": "A",
            "explain": "Correct. A \u2014 **ff02::1** (shown expanded as **ff02:0:0:0:0:0:0:1**) is the **link-local scope all-nodes** multicast address on every IPv6 link. The **ff02::/16** prefix marks **link-local multicast**; the final **::1** group ID is **all nodes**. **B** is a **global unicast** address (**2000::/3** range). **C** is not a valid reserved multicast pattern in these choices. **D** (**fe80::/10**) is a **link-local unicast** address, not multicast.",
            "choices": [
                "ff02:0:0:0:0:0:0:1",
                "2004:31c:73d9:683e:255::",
                "fffe:034:0dd:45d6:789e::",
                "fe80:4433:034:0dd::2",
            ],
            "mono": True,
        },
        {
            "slug": "gi1-ipv6-modified-eui64-from-mac-exhibit",
            "title": "CCNA — Modified EUI-64 from Gi1 MAC",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="show interfaces GigabitEthernet1">
        <pre>GigabitEthernet1 is up, line protocol is up
  Hardware is CSR vNIC, address is 5000.0004.0000 (bia 5000.0004.0000)
  Internet address is 192.168.1.1/24
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
    reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Keepalive set (10 sec)
  Full Duplex, 1000Mbps, link type is auto, media type is RJ45</pre>
      </div>
    </div>""",
            "stem": "Which format matches the **Modified EUI-64** IPv6 interface address for the network **2001:db8::/64**?",
            "name": "gieui641",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 MAC **5000.0004.0000** (**50:00:00:04:00:00**): insert **FF:FE** after the first three octets \u2192 **50:00:00:FF:FE:04:00:00**, then invert the **7th bit** (universal/local) of the first octet (**0x50** \u2192 **0x52**), yielding interface ID **5200:00ff:fe04:0000** and **`2001:db8::5200:00ff:fe04:0000/64`**. **C** omits the U/L-bit flip (**5000** instead of **5200**). **A** embeds the raw MAC without **FF:FE** or bit inversion. **B** is not derived from this MAC on prefix **2001:db8::/64**.",
            "choices": [
                "2001:db8::5000:0004:5678:0090/64",
                "2001:db8:4425:5400:77ff:fe07:/64",
                "2001:db8::5000:00ff:fe04:0000/64",
                "2001:db8::5200:00ff:fe04:0000/64",
            ],
        },
        {
            "slug": "wan-full-mesh-topology-disadvantages-choose-two",
            "title": "CCNA — Full-mesh disadvantages (choose two)",
            "stem": "What are two **disadvantages** of a **full-mesh** topology? (Choose two)",
            "name": "wanfmsh1",
            "choose_two": True,
            "correct": ["B", "D"],
            "explain": "Correct. B and D \u2014 A **full mesh** connects every site to every other site, so link count grows quickly (**n(n\u22121)/2**). That drives **high implementation cost** (circuits, ports, and hardware) and **complex configuration** (many tunnels/routes/peering relationships to build and maintain). **A** is wrong: **MTU** is not a defining full-mesh disadvantage. **C** describes how many WAN meshes are built (dedicated **point-to-point** links), not a typical exam-listed drawback versus **hub-and-spoke**. **E** is false: full mesh is a physical/logical topology pattern; sites can run **OSPF**, **EIGRP**, **MPLS**, or other designs\u2014not **BGP only**.",
            "choices": [
                "It needs a high MTU between sites.",
                "It has a high implementation cost.",
                "It must have point-to-point communication.",
                "It requires complex configuration.",
                "It works only with BGP between sites.",
            ],
        },
        {
            "slug": "qos-classification-traffic-treatment-purpose",
            "title": "CCNA — QoS classification purpose",
            "stem": "What is the purpose of **classifying** network traffic in **QoS**?",
            "name": "qoscls1",
            "correct": "B",
            "explain": "Correct. B \u2014 **Classification** **identifies** traffic (by ACL, NBAR, or other matchers) so the network knows **which treatment** (marking, queuing, policing, shaping) that traffic should receive. **A** describes **servicing** traffic after it is already classified and scheduled. **C** is **marking** (writing DSCP/CoS/IP precedence into a header field), a separate PHB step. **D** is how you **implement** matchers (for example **class-map** rules), not the purpose of classification itself.",
            "choices": [
                "services traffic according to its class",
                "identifies the type of traffic that will receive a particular treatment",
                "writes the class identifier of a packet to a dedicated field in the packet header",
                "configures traffic-matching rules on network devices",
            ],
        },
        {
            "slug": "private-ipv4-benefit-reuse-same-addresses",
            "title": "CCNA — Private IPv4 reuse benefit",
            "stem": "What is a benefit of using **private IPv4** addressing?",
            "name": "privben2",
            "correct": "A",
            "explain": "Correct. A \u2014 **RFC 1918** private ranges (**10/8**, **172.16/12**, **192.168/16**) can be **reused** at many sites and by many organizations because they are **not globally routable** on the public Internet, avoiding the need for a unique public address per internal host. **B** is wrong: private addressing **blocks** direct inbound reachability from the Internet unless **NAT** or explicit forwarding is used. **C** is false: hosts using only private addresses generally need **NAT/PAT** to reach the Internet. **D** is wrong: private space does not by itself provide secure Internet communication for all external hosts.",
            "choices": [
                "Multiple companies can use the same addresses without conflicts.",
                "Direct connectivity is provided to internal hosts from outside an enterprise network.",
                "Communication to the internet is reachable without the use of NAT.",
                "All external hosts are provided with secure communication to the Internet.",
            ],
        },
        {
            "slug": "sdn-separate-control-data-plane-advantage",
            "title": "CCNA — SDN control/data plane advantage",
            "stem": "What is the **advantage** of **separating the control plane** from the **data plane** within an **SDN** network?",
            "name": "sdnsep1",
            "correct": "A",
            "explain": "Correct. A \u2014 **SDN** centralizes **control-plane** decisions in a **controller** while **data-plane** devices focus on **forwarding**, which **simplifies operations** and **reduces overall network complexity** from an administrator\u2019s view. **B** misstates the model: applications and orchestration use **northbound** APIs; forwarding devices are programmed via **southbound** APIs, not by \u201climiting data queries\u201d to the control plane. **C** may occur in some designs but is not the defining advantage named here. **D** is wrong: **virtual machine** creation is a **compute/virtualization** task, not a data-plane forwarding function.",
            "choices": [
                "decreases overall network complexity",
                "limits data queries to the control plane",
                "reduces cost",
                "offloads the creation of virtual machines to the data plane",
            ],
        },
        {
            "slug": "r1-eigrp-ecmp-172-16-1-4-30-show-ip-route-exhibit",
            "title": "CCNA — R1 EIGRP ECMP to 172.16.1.4/30",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="R1 show ip route excerpt">
        <pre>R1# show ip route
Codes: C - connected, S - static, I - IGRP, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
       i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2, * - candidate default
       U - per-user static route, o - ODR
Gateway of last resort is not set
C   172.16.0.0/16 is directly connected, Loopback0
    172.16.0.0/16 is variably subnetted, 4 subnets, 2 masks
O      172.16.1.3/32 [110/100] via 10.0.1.100, 00:39:08, Serial0
O      172.16.1.9/32 [110/5] via 172.16.1.50, 00:43:01, GigabitEthernet0/0
D      172.16.1.4/30 [90/7445] via 172.16.9.5, 00:39:08, GigabitEthernet0/0
                     [90/7445] via 172.16.4.4, 00:39:08, GigabitEthernet0/4</pre>
      </div>
    </div>""",
            "stem": "How does router **R1** handle traffic to the **172.16.1.4/30** subnet?",
            "name": "r1ecmp1",
            "correct": "D",
            "explain": "Correct. D \u2014 **172.16.1.4/30** matches the **EIGRP** route with **two equal-cost paths** (same **AD 90** and **metric 7445**) via **172.16.9.5** and **172.16.4.4**, so **R1 load-balances** across both next hops. **A** and **C** wrongly prefer only **172.16.4.4** or treat **172.16.4.4** as backup despite equal metrics. **B** uses **10.0.1.100**, which is the next hop only for **172.16.1.3/32**, not **172.16.1.4/30**.",
            "choices": [
                "It sends all traffic over the path via 172.16.4.4",
                "It sends all traffic over the path via 10.0.1.100",
                "It sends all traffic over the path via 172.16.9.5 using 172.16.4.4 as a backup",
                "It load-balances traffic over 172.16.9.5 and 172.16.4.4",
            ],
        },
        {
            "slug": "syslog-server-filter-by-severity-level",
            "title": "CCNA — Syslog server filter by importance",
            "stem": "A network administrator wants the syslog server to filter incoming messages into different files based on their importance. Which filtering criteria must be used?",
            "name": "syslogfilt1",
            "correct": "C",
            "explain": "Correct. C \u2014 **Importance** in syslog is expressed by **severity level** (emergency through debug, 0\u20137). A collector can route or split logs into separate files by **level** so critical events are not mixed with routine informational traffic. **Facility** classifies the **source** or subsystem (kernel, local0, and so on), not urgency. **Process ID** and **message body** are not the standard syslog fields used to sort by importance.",
            "choices": [
                "message body",
                "process ID",
                "level",
                "facility",
            ],
        },
        {
            "slug": "frame-switching-store-forward-buffer-error-check",
            "title": "CCNA — Frame switching characteristic",
            "stem": "What is a characteristic of frame switching?",
            "name": "frmsw1",
            "correct": "C",
            "explain": "Correct. C \u2014 **Store-and-forward** switching receives the full frame into a **buffer**, runs **error checking** (for example **FCS**), then forwards it. That is a defining characteristic of **frame switching** on a switch. **A** is wrong: switches build a **MAC/CAM** table from **source** addresses; they do not populate an **ARP** table with an egress port for L2 frame switching. **B** is wrong: an **unknown destination MAC** is typically **flooded** within the VLAN, not dropped. **D** is wrong: a switch **forwards** frames without rewriting **source and destination MAC** addresses (that behavior belongs to routers or other devices at higher layers).",
            "choices": [
                "populates the ARP table with the egress port",
                "drops received MAC addresses not listed in the address table",
                "stores and forwards frames in a buffer and uses error checking",
                "rewrites the source and destination MAC address",
            ],
        },
        {
            "slug": "json-router-r20-property-is-value",
            "title": "CCNA — JSON value (R20 in device list)",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="JSON exhibit">
        <pre>[
  {"firewall": "FW12", "port":"e0/23"},
  {"router": "R20", "port":"te5/5"},
  {"switch": "SW25", "port":"ge1/36"},
]</pre>
    </div>""",
            "stem": "What is represented by the word \u201cR20\u201d within this JSON schema?",
            "name": "jsonr20v1",
            "correct": "A",
            "explain": "Correct. A \u2014 In `{\"router\": \"R20\", \"port\":\"te5/5\"}`, **\"router\"** is the **key** and **\"R20\"** is its string **value**. The outer `[ ]` is an **array**; each `{ }` entry is an **object**. **\"R20\"** is not a key, object, or array.",
            "choices": [
                "value",
                "array",
                "key",
                "object",
            ],
        },
        {
            "slug": "wlc-new-wlan-gui-profile-name-ssid-choose-two",
            "title": "CCNA — New WLAN on WLC GUI (choose two)",
            "stem": "Which two values or settings must be entered when configuring a new WLAN in the Cisco Wireless LAN Controller GUI? (Choose two.)",
            "name": "wlcwlan1",
            "choose_two": True,
            "correct": ["D", "E"],
            "explain": "Correct. D and E \u2014 Creating a WLAN on the **WLC GUI** requires a **profile name** (internal WLAN profile identifier) and an **SSID** (the wireless network name clients use). **Management interface** settings are controller-wide and are not entered per WLAN at creation. **QoS** can be tuned later; defaults apply. **AP IP addresses** are not entered when defining a WLAN\u2014APs discover and join the controller separately.",
            "choices": [
                "management interface settings",
                "QoS settings",
                "ip address of one or more access points",
                "SSID",
                "Profile name",
            ],
        },
        {
            "slug": "vm-deploy-resource-limits-cpu-memory",
            "title": "CCNA — VM deployment planning",
            "stem": "What must be considered before deploying virtual machines?",
            "name": "vmdep1",
            "correct": "C",
            "explain": "Correct. C \u2014 Before deploying VMs, plan **host resource limits**: available **CPU cores**, **memory**, and related capacity so guests do not overcommit the hypervisor and degrade performance. **A** (rack/location placement) may matter for operations but is not the primary technical prerequisite named in CCNA virtualization topics. **B** (**VSM** processor mapping) is not the standard pre-deployment consideration for general VM rollout. **D** (physical **monitors/keyboards/mice**) is largely irrelevant for typical **data-center server VMs**, which use virtual hardware and remote management.",
            "choices": [
                "location of the virtual machines within the data center environment",
                "whether to leverage VSM to map multiple virtual processors to two or more virtual machines",
                "resource limitations, such as the number of CPU cores and the amount of memory",
                "support for physical peripherals, such as monitors, keyboards, and mice",
            ],
        },
        {
            "slug": "stp-root-port-role-nonroot-best-path",
            "title": "CCNA — STP root port role",
            "stem": "What is the role of the root port in a switched network?",
            "name": "stproot1",
            "correct": "B",
            "explain": "Correct. B \u2014 On each **nonroot** switch, the **root port (RP)** is the port with the **lowest-cost path** to the **root bridge** for that spanning-tree instance (per VLAN in **PVST+/RPVST+**). **A** and **C** confuse the root port with the **designated port** or **alternate/backup** roles used when links fail. **D** is wrong: the root port is **not** held administratively disabled until failover\u2014it is the **active** best path toward the root.",
            "choices": [
                "It replaces the designated port when the designated port fails",
                "It is the best path to the root from a nonroot switch",
                "It replaces the designated port when the root port fails",
                "It is administratively disabled until a failover occurs",
            ],
        },
        {
            "slug": "wpa1-data-protection-tkip-encryption",
            "title": "CCNA — WPA1 data encryption",
            "stem": "Which type of encryption does WPA1 use for data protection?",
            "name": "wpa1enc1",
            "correct": "B",
            "explain": "Correct. B \u2014 **WPA** (often called **WPA1**) uses **TKIP** (**Temporal Key Integrity Protocol**) for over-the-air **data confidentiality and integrity**, improving on **WEP** while remaining compatible with older hardware. **AES** (**CCMP**) is the standard cipher for **WPA2** and later. **PEAP** and **EAP** are **authentication** frameworks/methods, not the encryption cipher that protects user data frames.",
            "choices": [
                "AES",
                "TKIP",
                "PEAP",
                "EAP",
            ],
        },
        {
            "slug": "r1-forward-192-168-20-75-longest-match-exhibit",
            "title": "CCNA — R1 longest match to 192.168.20.75",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="R1 show ip route excerpt">
        <pre>R1# show ip route
......
D       192.168.20.0/26 [90/24513456] via 10.10.10.1
R       192.168.20.0/24 [120/5] via 10.10.10.2
O       192.168.0.0/19 [110/219414] via 10.10.10.13
B       192.168.0.0/16 is variably subnetted, 4 subnets, 4 masks
D       192.168.20.0/27 [90/4123710] via 10.10.10.12
D       192.168.20.0/25 [90/14464211] via 10.10.10.11
S*      0.0.0.0/0 [1/0] via 10.10.10.14</pre>
    </div>""",
            "stem": "Packets are flowing from **192.168.10.1** to the destination at IP address **192.168.20.75**. Which next hop will the router select for the packet?",
            "name": "r1lm2075",
            "correct": "B",
            "explain": "Correct. B \u2014 **192.168.20.75** matches several summaries, but **longest-prefix match** wins: **192.168.20.0/25** (hosts **.0\u2013.127**) is longer than **/26**, **/27**, **/24**, **/19**, and **/16**, so the next hop is **10.10.10.11**. **10.10.10.1** (**/26**, **.0\u2013.63**) and **10.10.10.12** (**/27**, **.0\u2013.31**) do not contain **.75**. **10.10.10.14** is only the **default** route if nothing more specific matched.",
            "choices": [
                "10.10.10.1",
                "10.10.10.11",
                "10.10.10.12",
                "10.10.10.14",
            ],
        },
        {
            "slug": "switch-destination-mac-aged-out-flood-vlan",
            "title": "CCNA — Flooding after MAC aging",
            "stem": "What happens when a switch receives a frame with a destination MAC address that recently aged out?",
            "name": "swaged1",
            "correct": "D",
            "explain": "Correct. D \u2014 When a **MAC ages out**, the entry is **removed** from the **CAM table**. The next frame to that destination is handled like **unknown unicast**: the switch **floods** it to all ports in the **same VLAN** except the **ingress** port, so the host can be reached and the switch can **relearn** the MAC from reply traffic. **A** is wrong: there is no separate **historical aging table** used for forwarding lookups. **B** is wrong: flooding stays **within the VLAN**, not all VLANs. **C** is wrong: the switch does **not drop** the frame; it **learns source MACs** on ingress, not unknown **destinations** by dropping.",
            "choices": [
                "The switch references the MAC address aging table for historical addresses on the port that received the frame",
                "The switch floods the frame to all ports in all VLANs except the port that received the frame",
                "The switch drops the frame and learns the destination MAC address again from the port that received the frame",
                "The switch floods the frame to all ports in the VLAN except the port that received the frame",
            ],
        },
        {
            "slug": "dhcp-snooping-identify-rogue-server-dhcoffer",
            "title": "CCNA — Identify rogue DHCP server",
            "stem": "What is used to identify spurious DHCP servers?",
            "name": "dhcprog1",
            "correct": "D",
            "explain": "Correct. D \u2014 With **DHCP snooping**, only **trusted** interfaces may receive **server** messages. A **DHCPOFFER** (or **DHCPACK**) seen on an **untrusted** port indicates a **rogue/spurious DHCP server**; the switch can log or drop it. **DHCPDISCOVER** and **DHCPREQUEST** are **client** messages and do not by themselves identify an unauthorized server. **DHCPACK** also signals a server, but **DHCPOFFER** is the usual exam focus as the first server reply that exposes a spurious server on the LAN.",
            "choices": [
                "DHCPREQUEST",
                "DHCPDISCOVER",
                "DHCPACK",
                "DHCPOFFER",
            ],
        },
        {
            "slug": "rapid-pvst-plus-port-state-after-boot-discarding",
            "title": "CCNA — Rapid PVST+ port state after boot",
            "stem": "What is the temporary state that switch ports always enter immediately after the boot process when Rapid PVST+ is used?",
            "name": "rpvstboot1",
            "correct": "A",
            "explain": "Correct. A \u2014 **Rapid PVST+** uses **RSTP** port states: **discarding**, **learning**, and **forwarding**. After boot (or when a link comes up), ports begin in **discarding**, which does not forward user traffic while spanning tree converges. **Listening** (**B**) is a **classic 802.1D STP** state, not an RSTP state. **Learning** (**D**) and **forwarding** (**C**) come later in the progression once the port is allowed to move forward.",
            "choices": [
                "discarding",
                "listening",
                "forwarding",
                "learning",
            ],
        },
        {
            "slug": "lightweight-ap-split-mac-wlc-zero-touch",
            "title": "CCNA — Lightweight AP split-MAC requirements",
            "stem": "A wireless access point is needed and must meet these requirements:\n\u2022 \u201czero-touch\u201d deployed and managed by a WLC\n\u2022 process only real-time MAC functionality\n\u2022 used in a split-MAC architecture.\n\nWhich access point type must be used?",
            "name": "lwapreq1",
            "correct": "B",
            "explain": "Correct. B \u2014 A **lightweight** (thin) AP joins a **WLC** over **CAPWAP** for **zero-touch** provisioning and policy. In **split-MAC**, the **WLC** runs control/management (WLANs, security, roaming, RF) while the AP handles **real-time 802.11 MAC** functions on the air. **Autonomous** APs run the full WLAN stack locally without WLC split-MAC. **Mesh** APs extend coverage over wireless backhaul. **Cloud-based** may describe cloud-managed WLAN platforms but does not match **WLC-managed split-MAC** as stated.",
            "choices": [
                "autonomous",
                "lightweight",
                "mesh",
                "cloud-based",
            ],
        },
        {
            "slug": "vm-components-configuration-files-hypervisor-resources",
            "title": "CCNA — Components within a VM",
            "stem": "Which components are contained within a virtual machine?",
            "name": "vmcomp1",
            "correct": "B",
            "explain": "Correct. B \u2014 A **VM** is defined by **configuration files** (settings, virtual hardware definition) whose **virtual CPU, memory, disk, and NIC** are **backed by physical host resources** allocated by the **hypervisor**. **A** is wrong: the guest uses **virtualized** resources, not raw **physical** NIC/RAM/CPU inside the VM boundary. **C** is wrong: applications run on the **guest OS inside** the VM, not on the hypervisor. **D** is wrong: **hypervisor** processes belong to the host; a VM contains a **guest OS** and its **guest processes**, not hypervisor processes.",
            "choices": [
                "physical resources, including the NIC, RAM, disk, and CPU",
                "configuration files backed by physical resources from the Hypervisor",
                "applications running on the Hypervisor",
                "processes running on the Hypervisor and a guest OS",
            ],
        },
        {
            "slug": "wlc-capwap-tunnel-source-ap-manager-interface",
            "title": "CCNA — CAPWAP tunnel source on WLC",
            "stem": "Which interface IP address serves as the tunnel source for CAPWAP packets from the WLC to an AP?",
            "name": "wlccap1",
            "correct": "C",
            "explain": "Correct. C \u2014 The **AP-manager** interface IP is the **source** for **CAPWAP** control (and typically data) tunnels between the **WLC** and **lightweight APs**. APs discover and join using that address. The **service** port is **out-of-band** management, not the CAPWAP tunnel source. A **trunk** is a **Layer 2** switch port mode, not a WLC management interface. **Virtual AP** refers to client-facing WLAN functions, not the WLC-to-AP CAPWAP endpoint.",
            "choices": [
                "service",
                "trunk",
                "AP-manager",
                "virtual AP connection",
            ],
        },
        {
            "slug": "switch-cam-lookup-destination-mac-forwarding",
            "title": "CCNA — CAM lookup when forwarding",
            "stem": "What does a switch search for in the CAM table when forwarding a frame?",
            "name": "swcamfwd1",
            "correct": "D",
            "explain": "Correct. D \u2014 To **forward**, the switch looks up the frame\u2019s **destination MAC address** in the **CAM/MAC table** and uses the **associated egress port** (the port where that MAC was learned). **Source MAC** and **ingress port** (**A**, **C**) are recorded when the frame **arrives** (learning), not used as the primary **forwarding lookup key**. **Aging** and **flush** timers (**A**, **B**) govern how long entries stay in the table; they are not what the switch searches for during a forward decision.",
            "choices": [
                "source MAC address and aging time",
                "destination MAC address and flush time",
                "source MAC address and source port",
                "destination MAC address and destination port",
            ],
        },
        {
            "slug": "hypervisor-type1-bare-metal-no-host-os",
            "title": "CCNA — Type 1 hypervisor",
            "stem": "Which type of hypervisor operates without an underlying OS to host virtual machines?",
            "name": "hyptype1",
            "correct": "A",
            "explain": "Correct. A \u2014 A **Type 1** (**bare-metal**) hypervisor runs **directly on hardware** and does **not** require a separate **host operating system** underneath the hypervisor layer. **Type 2** (**hosted**) hypervisors run **on top of** a conventional OS (for example Windows or Linux), which then hosts VMs. **Type 3** and **Type 12** are not standard hypervisor classifications in CCNA virtualization topics.",
            "choices": [
                "Type 1",
                "Type 2",
                "Type 3",
                "Type 12",
            ],
        },
        {
            "slug": "windows-ipv4-preferred-dhcp-renew-same-address",
            "title": "CCNA — IPv4 Preferred (ipconfig) and DHCP renew",
            "prepend_html": """    <div class="exhibit-terminal-white" role="region" aria-label="Windows ipconfig output">
        <pre>Connection-specific DNS Suffix  . :
  Description . . . . . . . . . . . : Intel(R) Ethernet Connection (2) I218-V
  Physical Address. . . . . . . . . : D0-50-99-47-A9-7F
  DHCP Enabled. . . . . . . . . . . : Yes
  Autoconfiguration Enabled . . . . : Yes
  Link-local IPv6 Address . . . . . : fe80::8809:9772:c583:6bl8%15(Preferred)
  IPv4 Address. . . . . . . . . . . : 192.168.69.132(Preferred)
  Subnet Mask . . . . . . . . . . . : 255.255.255.0
  Lease Obtained. . . . . . . . . . : Thursday, January 21, 2021 11:10:46 PM
  Lease Expires . . . . . . . . . . : Wednesday, February 3, 2021 11:27:29 AM
  Default Gateway . . . . . . . . . : 192.168.69.1
  DHCP Server . . . . . . . . . . : 192.168.69.1
  DHCPv6 IAID . . . . . . . . . . . : 231755929
  DHCPv6 Client DUID. . . . . . . . : 00-01-00-01-26-D7-BB-3F-D0-50-99-47-A9-7F
  DNS Servers . . . . . . . . . . . : 192.168.69.1
  NetBIOS over Tcpip. . . . . . . . : Enabled</pre>
    </div>""",
            "stem": "Refer to the exhibit. What does the host do when using the IPv4 **Preferred** function?",
            "name": "winpref1",
            "correct": "C",
            "explain": "Correct. C \u2014 With **DHCP enabled**, **(Preferred)** on the **IPv4 Address** line means the address is the **active** lease in use. On **renewal**, the client typically sends a **DHCPREQUEST** asking to keep the **same IPv4 address** (if the server still has it available). **A** is wrong: the host is **not** using a static address (**DHCP Enabled: Yes**). **B** misstates the role of **DNS** (name resolution, not DHCP lease renewal). **D** is wrong: renewal does not mean the client \u201cprefers a pool\u201d arbitrarily\u2014it requests continuity of its current lease.",
            "choices": [
                "It continues to use a statically assigned IPv4 address",
                "It forces the DNS server to provide the same IPv4 address at each renewal",
                "It requests the same IPv4 address when it renews its lease with the DHCP server",
                "It prefers a pool of addresses when renewing the IPv4 host IP address",
            ],
        },
        {
            "slug": "vrrp-lan-capabilities-redundancy-load-sharing-choose-two",
            "title": "CCNA — VRRP LAN capabilities (choose two)",
            "stem": "What are two capabilities provided by VRRP within a LAN network? (Choose two.)",
            "name": "vrrpcap1",
            "choose_two": True,
            "correct": ["A", "D"],
            "explain": "Correct. A and D \u2014 **VRRP** provides **default-gateway redundancy**: if the **master** router fails, a **backup** assumes the **virtual IP/MAC** so LAN hosts keep connectivity. **Load sharing** (**A**) is supported by using **multiple VRRP groups** so different routers can be master for different virtual routers, spreading gateway traffic. **Bandwidth optimization** (**B**), **dynamic routing updates** (**C**), and **granular QoS** (**E**) are not VRRP functions\u2014those belong to WAN design, routing protocols, and QoS policy respectively.",
            "choices": [
                "load sharing",
                "bandwidth optimization",
                "dynamic routing updates",
                "redundancy",
                "granular QoS",
            ],
        },
        {
            "slug": "forward-10-18-75-113-ospf-metric-g0-6-exhibit",
            "title": "CCNA — Forwarding interface for 10.18.75.113/27",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="Routing table excerpt">
        <pre>O       10.18.75.113/27 [110/6906] via G0/6
O       10.18.75.113/27 [110/23018] via G0/3
R       10.18.75.113/27 [120/16] via G0/16
R       10.18.75.113/27 [120/14] via G0/23</pre>
    </div>""",
            "stem": "Which interface is used to send traffic to the destination network?",
            "name": "fwd1075",
            "correct": "A",
            "explain": "Correct. A \u2014 All entries match **10.18.75.113/27**. **Administrative distance** decides first: **OSPF (110)** beats **RIP (120)**, so only the **O** routes are candidates. Between **G0/6** (**metric 6906**) and **G0/3** (**metric 23018**), the **lower OSPF metric** wins \u2192 **G0/6**. **G0/16** and **G0/23** are **RIP** and are not installed as best path while better-AD OSPF routes exist.",
            "choices": [
                "G0/6",
                "G0/3",
                "G0/16",
                "G0/23",
            ],
        },
        {
            "slug": "ap-sniffer-mode-packet-analyzer-capture",
            "title": "CCNA — AP sniffer mode for packet capture",
            "stem": "Which AP mode is used for capturing wireless traffic and forwarding that traffic to a PC that is running a packet analyzer?",
            "name": "apsnif1",
            "correct": "B",
            "explain": "Correct. B \u2014 **Sniffer mode** dedicates the lightweight AP to **capture 802.11 frames** on a selected channel and **tunnel them to a wired host** running a **packet analyzer** (for example Wireshark). **Monitor** mode focuses on **RF/air-quality** and **rogue/WIPS-style** monitoring, not full-time remote frame capture to an analyzer PC. **Bridge** mode links networks wirelessly. **Rogue detector** is not a standard operational mode name here (rogue detection is a **monitor-mode** function).",
            "choices": [
                "monitor",
                "sniffer",
                "bridge",
                "rouge detector",
            ],
        },
        {
            "slug": "layer2-switch-forwarding-decision-mac-address",
            "title": "CCNA — Layer 2 switch characteristic",
            "stem": "What is a characteristic of a Layer 2 switch?",
            "name": "l2sw1",
            "correct": "D",
            "explain": "Correct. D \u2014 A **Layer 2 switch** forwards frames using the **destination MAC address** in the **CAM/MAC table** (and learns **source MAC** on ingress). **A** is incomplete: a switch can support **multiple VLANs**, each with its own **broadcast domain**, not necessarily one domain for every connected device. **B** describes **Layer 4** state tracking (firewalls/load balancers), not switching. **C** is wrong: each switch port is typically its own **collision domain** (unlike a **hub**, which shares one).",
            "choices": [
                "provides a single broadcast domain for all connected devices",
                "tracks the number of active TCP connections",
                "offers one collision domain for all connected devices",
                "makes forwarding decisions based on MAC addresses",
            ],
        },
        {
            "slug": "r30-fa0-0-collisions-duplex-mismatch-madrid-exhibit",
            "title": "CCNA — R30 Fa0/0 collisions (show interface)",
            "stem": "Which interface condition is occurring in this output?",
            "name": "r30dm1",
            "correct": "D",
            "explain": "Correct. D \u2014 **480 collisions** and **35 runts** on an interface configured **Half-duplex** strongly indicate a **duplex mismatch** with the far end (often the peer is **full duplex** while this side is **half**). **Bad NIC** (**A**) usually shows **CRC/frame** input errors, not this collision pattern. **Broadcast storm** (**B**) is not supported by a modest **267 broadcasts** count alone. **Queueing** (**C**) would show a **nonzero, growing output queue**; here **Output queue: 0/300** is empty.",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="R30 show interface FastEthernet0/0">
        <pre>R30# show interface fa0/0
FastEthernet0/0 is up, line protocol is up
Hardware is DEC21140, address is ca02.7788.0000 (bia ca02.7788.0000)
Description: madrid_subnet
Internet address is 10.32.102.2/30
MTU 1500 bytes, BW 100000 Kbit/sec, DLY 100 usec,
 reliability 255/255, txload 1/255, rxload 1/255
Encapsulation ARPA, loopback not set
Keepalive set (60 sec)
Half-duplex, 100 Mb/s, 100BaseTX/FX
ARP type: ARPA, ARP Timeout 04:00:00
Last input 00:00:01, output 00:00:00, output hang never
Last clearing of "show interface" counters 00:00:18
Input queue: 0/300/0/0 (size/max/drops/flushes); Total output drops: 0
Queueing strategy: fifo
Output queue: 0/300 (size/max)
30 second input rate 0 bits/sec, 0 packets/sec
30 second output rate 0 bits/sec, 0 packets/sec
7331 packets input, 7101162 bytes
Received 267 broadcasts (0 IP multicasts)
35 runts, 0 giants, 0 throttles
0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
0 watchdog
0 input packets with dribble condition detected
3927 packets output, 1440403 bytes, 0 underruns
0 output errors, 480 collisions, 0 interface resets
0 unknown protocol drops
0 babbles, 0 late collision, 0 deferred
0 lost carrier, 0 no carrier
0 output buffer failures, 0 output buffers swapped out</pre>
    </div>""",
            "choices": [
                "bad NIC",
                "broadcast storm",
                "queueing",
                "duplex mismatch",
            ],
        },
        {
            "slug": "forward-10-47-114-119-eigrp-metric-f0-2-exhibit",
            "title": "CCNA — Forwarding interface for 10.47.114.119/29",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="Routing table excerpt">
        <pre>D       10.47.114.119/29 [90/6451] via F0/2
D       10.47.114.119/29 [90/52201] via F0/20
R       10.47.114.119/29 [120/9] via F0/12
R       10.47.114.119/29 [120/10] via F0/10</pre>
    </div>""",
            "stem": "Which interface is used to send traffic to the destination network?",
            "name": "fwd1047",
            "correct": "A",
            "explain": "Correct. A \u2014 All four lines match **10.47.114.119/29**. **Administrative distance** selects **EIGRP (90)** over **RIP (120)**, so only the **D** routes qualify. Between **F0/2** (**metric 6451**) and **F0/20** (**metric 52201**), the **lower EIGRP metric** wins \u2192 **F0/2**. **F0/12** and **F0/10** are **RIP** and are not the best path while EIGRP routes exist.",
            "choices": [
                "F0/2",
                "F0/20",
                "F0/12",
                "F0/10",
            ],
        },
        {
            "slug": "tcp-preferred-over-udp-reliability-critical",
            "title": "CCNA — When TCP is preferred over UDP",
            "stem": "Under which condition is TCP preferred over UDP?",
            "name": "tcpudp2",
            "correct": "A",
            "explain": "Correct. A \u2014 **TCP** adds **reliability**, **ordering**, and **flow control** (retransmissions, acknowledgments), so it is preferred when **data must arrive correctly** (for example HTTP, SSH, file transfer). **UDP** is **best-effort** and acceptable when **occasional loss** is tolerable and lower overhead matters (for example DNS, VoIP, some streaming). **B** partially describes latency trade-offs but is not the primary CCNA framing. **C** reverses typical roles (**interactive** apps often still need reliability). **D** is backwards: **TCP** does not prefer dropped or out-of-order data.",
            "choices": [
                "TCP is used when data reliability is critical, and UDP is used when missing packets are acceptable",
                "UDP is used when low latency is optimal, and TCP is used when latency is tolerable",
                "UDP is used when data is highly interactive, and TCP is used when data is time-sensitive",
                "TCP is used when dropped data is more acceptable, and UDP is used when data is accepted out-of-order",
            ],
        },
        {
            "slug": "pc-subnet-mask-192-168-25-128-and-100-same-lan",
            "title": "CCNA — Subnet mask for two PCs on same LAN",
            "stem": "An engineer must update the configuration on two PCs in two different subnets to communicate locally with each other. One PC is configured with IP address **192.168.25.128/25** and the other with **192.168.25.100/25**. Which network mask must the engineer configure on both PCs to enable the communication?",
            "name": "pcmask1",
            "correct": "B",
            "explain": "Correct. B \u2014 With **/25** (**255.255.255.128**), **.100** is in **192.168.25.0/25** and **.128** is in **192.168.25.128/25**, so they are on **different subnets**. **255.255.255.0** (**/24**) places both addresses in **192.168.25.0/24**, so they can communicate **locally** without a router. **255.255.255.248** (/29), **255.255.255.252** (/30), and **255.255.255.224** (/27) still leave **.100** and **.128** in **different** smaller subnets.",
            "choices": [
                "255.255.255.248",
                "255.255.255.0",
                "255.255.255.252",
                "255.255.255.224",
            ],
        },
        {
            "slug": "vrrp-protocol-default-gateway-fhrp-type",
            "title": "CCNA — What type of protocol is VRRP?",
            "stem": "Which type of protocol is VRRP?",
            "name": "vrrptype1",
            "correct": "D",
            "explain": "Correct. D \u2014 **VRRP** is a **first-hop redundancy (FHRP)** protocol: **two or more routers** present a **shared virtual default gateway** to LAN clients. **A** describes **DHCP**, not VRRP. **B** (**224.0.0.102**) is associated with **GLBP** advertisements, not **VRRP** (**224.0.0.18**). **C** describes **Cisco-proprietary HSRP/GLBP**; **VRRP** is an **open standard** (RFC).",
            "choices": [
                "uses dynamic IP address assignment",
                "uses a destination IP address 224.0.0.102 for router-to-router communication",
                "uses Cisco-proprietary First Hop Redundancy Protocol",
                "allows two or more routers to act as a default gateway",
            ],
        },
        {
            "slug": "rfc1918-private-ipv4-nat-preserve-public",
            "title": "CCNA — How RFC 1918 addresses are used",
            "stem": "How are RFC 1918 IP addresses used in a network?",
            "name": "rfc19181",
            "correct": "D",
            "explain": "Correct. D \u2014 **RFC 1918** (**10/8**, **172.16/12**, **192.168/16**) provides **private** addresses reused inside organizations; **NAT** (or PAT) at the edge maps them to **public IPv4**, **preserving** scarce globally unique space. **A** overstates **security**: private space is not a substitute for firewalls and policy. **B** is wrong\u2014**ISPs** route **public** addresses on the Internet. **C** is wrong\u2014private hosts reach the Internet **only after** **NAT** (or similar), not without conversion.",
            "choices": [
                "They are used instead of public addresses for increased security.",
                "They are used by internet service providers to route over the internet.",
                "They are used to access the internet from the internal network without conversion.",
                "They are used with NAT to preserve public IPv4 addresses.",
            ],
        },
        {
            "slug": "ap-firmware-updates-lightweight-require-wlc",
            "title": "CCNA — AP firmware updates (autonomous vs lightweight)",
            "stem": "A network architect is deciding whether to implement Cisco autonomous access points or lightweight access points. Which fact about firmware updates must the architect consider?",
            "name": "apfw1",
            "correct": "A",
            "explain": "Correct. A \u2014 **Lightweight** APs are managed by a **WLC**; **firmware upgrades** are typically **pushed centrally** from the controller to joined APs. **Autonomous** APs are updated **per device** (GUI/CLI on each AP or local tools), not through a WLC. **B** is not a reliable differentiator for corrupt-image recovery. **C** is wrong: **lightweight** APs do **not** require **redundant WLCs** solely for firmware upgrades, and **autonomous** APs do **not** use a WLC. **D** is not the defining operational model for lightweight vs autonomous firmware handling.",
            "choices": [
                "Unlike autonomous access points, lightweight access points require a WLC to implement remote firmware updates.",
                "Unlike lightweight access points, autonomous access points can recover automatically from a corrupt firmware update",
                "Unlike lightweight access points, which require redundant WLCs to support firmware upgrades, autonomous access points require only one WLC.",
                "Unlike autonomous access points, lightweight access points store a complete copy of the current firmware for backup.",
            ],
        },
        {
            "slug": "dhcp-pool-control-helper-address-relay-server",
            "title": "CCNA — DHCP relay to server 172.16.32.15",
            "stem": "A DHCP pool has been created with the name **CONTROL**. The pool uses the next-to-last usable IP address as the default gateway for the DHCP clients. The server is located at **172.16.32.15**. What is the next step in the process for clients on the **192.168.52.0/24** subnet to reach the DHCP server?",
            "name": "dhcpctl1",
            "correct": "D",
            "explain": "Correct. D \u2014 Clients on **192.168.52.0/24** use **broadcast** DHCP messages that do not cross routers. On the **router interface facing that subnet**, configure **`ip helper-address 172.16.32.15`** so the router **relays** DHCP to the server on **172.16.32.15**. The pool\u2019s default router **192.168.52.253** (next-to-last usable on /24) is for **leased hosts**, not this relay step. **A** (**UDP 137**) is **NetBIOS**, not DHCP relay. **B** and **C** are not the standard IOS command to relay DHCP across subnets.",
            "choices": [
                "ip forward-protocol udp 137",
                "ip default-network 192.168.52.253",
                "ip default-gateway 192.168.52.253",
                "ip helper-address 172.16.32.15",
            ],
        },
        {
            "slug": "r1-forward-10-56-0-62-longest-match-vlan58-exhibit",
            "title": "CCNA — R1 forward 10.56.0.62 (show ip route)",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="R1 show ip route excerpt">
        <pre>R1#
Gateway of last resort is 10.56.0.1 to network 0.0.0.0

S*   0.0.0.0/0 [1/0] via 10.56.0.1
     10.0.0.0/8 is variably subnetted, 2 subnets, 2 masks
C      10.56.0.0/16 is directly connected, Null0
C      10.56.0.0/26 is directly connected, Vlan58
C      10.56.0.0/17 is directly connected, Vlan59
C      10.56.0.0/24 is directly connected, Vlan60</pre>
    </div>""",
            "stem": "When router **R1** receives a packet with destination IP address **10.56.0.62**, through which interface does it route the packet?",
            "name": "r1fwd562",
            "correct": "D",
            "explain": "Correct. D \u2014 **Longest-prefix match** selects **10.56.0.0/26** (**Vlan58**): **10.56.0.62** lies in **10.56.0.0\u201310.56.0.63**. That **/26** is more specific than **/17** (**Vlan59**), **/24** (**Vlan60**), and **/16** (**Null0**). **Vlan59** and **Vlan60** also contain **.62** but lose to the longer prefix. **Null0** is the less-specific **/16** discard/summary-style connected route, not the best path for this host.",
            "choices": [
                "Vlan59",
                "Vlan60",
                "Null0",
                "Vlan58",
            ],
        },
        {
            "slug": "r1-gi001-line-protocol-down-duplex-mismatch-exhibit",
            "title": "CCNA — R1 Gi0/0/1 line protocol down",
            "stem": "What is the issue with the interface **GigabitEthernet0/0/1**?",
            "name": "r1gi01",
            "correct": "B",
            "explain": "Correct. B \u2014 **Line protocol down** with **interface up** means **Layer 1** sees the link but **Layer 2** is not healthy. **Half Duplex** at **1000 Mbps** plus **50 collisions** indicates a **duplex/speed mismatch** with the far end (common when one side is **full duplex** and the other **half**). **Cable disconnect** (**A**) can drop line protocol but usually shows little or no collision growth. **Port security** (**C**) typically **err-disables** the port. **High throughput** (**D**) is not supported (**txload/rxload 1/255**, minimal traffic).",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="R1 show interface GigabitEthernet0/0/1">
        <pre>Output from R1
GigabitEthernet0/0/1 is up, line protocol is down
Hardware is SPA-10X1GE-V2, address is 0023.33ee.7c00 (bia 0023.33ee.7c00)
MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
 reliability 255/255, txload 1/255, rxload 1/255
Encapsulation ARPA, loopback not set
Keepalive not supported
Half Duplex, 1000Mbps, link type is auto, media type is LX
output flow-control is off, input flow-control is off
ARP type: ARPA, ARP Timeout 04:00:00
Last input 00:00:01, output 00:02:31, output hang never
10 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
0 watchdog, 314 multicast, 0 pause input
1 packets output, 77 bytes, 0 underruns
0 output errors, 50 collisions, 6 interface resets
17 unknown protocol drops
0 babbles, 0 late collision, 0 deferred</pre>
    </div>""",
            "choices": [
                "cable disconnect",
                "duplex mismatch",
                "port security",
                "high throughput",
            ],
        },
        {
            "slug": "json-interfaces-ethernet-object-type-shown",
            "title": "CCNA — JSON object (interfaces list)",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="JSON interfaces exhibit">
        <pre>{
"interfaces":["ethernet0/3", "ethernet0/4", "ethernet0/5"]
}</pre>
    </div>""",
            "stem": "Which type of JSON data is shown?",
            "name": "jsoniftype1",
            "correct": "C",
            "explain": "Correct. C \u2014 The exhibit is a single JSON **object**: curly braces `{ }` with a **name\u2013value** pair (**\"interfaces\"** \u2192 list). The `[ \"ethernet0/3\", ... ]` portion is a **sequence** (array) **inside** that object, not the type of the whole document. **String** (**A**) applies to quoted text such as **\"ethernet0/3\"**. **Boolean** (**D**) applies to **true**/**false**, which are not shown.",
            "choices": [
                "string",
                "sequence",
                "object",
                "Boolean",
            ],
        },
        {
            "slug": "switch-mac-aging-default-300-seconds-workstation",
            "title": "CCNA — Default MAC address aging time",
            "stem": "By default, how long will the switch continue to know a workstation MAC address after the workstation stops sending traffic?",
            "name": "macage300",
            "correct": "B",
            "explain": "Correct. B \u2014 On Cisco switches the default **MAC address-table aging time** is **300 seconds** (5 minutes). If no frames with that **source MAC** arrive before the timer expires, the **dynamic** CAM entry is removed. **200**, **600**, and **900** seconds are not the default (aging time is configurable with **mac address-table aging-time**).",
            "choices": [
                "200 seconds",
                "300 seconds",
                "600 seconds",
                "900 seconds",
            ],
        },
        {
            "slug": "wlc-radius-wireless-aaa-override-ip-address",
            "title": "CCNA — WLC RADIUS for wireless authentication",
            "stem": "Which selections must be used on the WLC when implementing a RADIUS server for wireless authentication?",
            "name": "wlcrad1",
            "correct": "D",
            "explain": "Correct. D \u2014 The WLC must know the **RADIUS server IP address** (and shared secret) under **Security \u2192 AAA \u2192 RADIUS \u2192 Authentication**, and **Allow AAA Override** on the WLAN so **RADIUS-returned attributes** (VLAN, QoS, ACL, and similar) can be applied to wireless clients. **802.1X** is configured as **WLAN Layer 2 security**, but the **RADIUS server** is identified by **IP**, not its **MAC** (**C**). **Client Exclusion** and **SSH** (**A**) are unrelated to RADIUS client authentication. **Network Access Control State** and **SSH** (**B**) are not the required RADIUS pairing.",
            "choices": [
                "Client Exclusion and SSH",
                "Network Access Control State and SSH",
                "802.1x and the MAC address of the server",
                "AAA Override and the IP address of the server",
            ],
        },
        {
            "slug": "hub-vs-switch-known-destination-mac-forwarding",
            "title": "CCNA — Hub vs switch (known destination MAC)",
            "stem": "How does a hub handle a frame traveling to a **known destination MAC address** differently than a switch?",
            "name": "hubsw1",
            "correct": "B",
            "explain": "Correct. B \u2014 A **hub** is a **shared-medium** device: it **repeats** the frame out **all ports** (except the ingress port) regardless of destination MAC. A **switch** builds a **MAC/CAM table** and **unicasts** the frame **only to the port** where that **destination MAC** was learned. **A** is wrong: hubs do not use a **FIB** (that is Layer 3). **C** reverses hub and switch behavior and wrongly cites a **routing table** for the switch at Layer 2. **D** reverses roles: selective forwarding by MAC is the **switch**, not the hub.",
            "choices": [
                "The hub forwards the frame to all ports in the FIB table, and a switch forwards the frame the destination MAC is known.",
                "The hub forwards the frame to all ports, and a switch forwards the frame to the known destination.",
                "The hub forwards the frame using the information in the MAC table, and a switch uses data in its routing table.",
                "The hub forwards the frame only to the port connected to the known MAC address,and a switch forwards the frame to all ports.",
            ],
        },
        {
            "slug": "essid-multiple-aps-common-wireless-network",
            "title": "CCNA — Purpose of an ESSID",
            "stem": "What is the purpose of an **ESSID**?",
            "name": "essid1",
            "correct": "D",
            "explain": "Correct. D \u2014 An **ESSID** (Extended Service Set Identifier) is the **wireless network name** shared by **multiple access points** in an **ESS**, so clients see **one logical WLAN** and can roam between APs. It is **not** inherently more secure than an **SSID** (**A**). **802.11k/r/v** fast roaming (**B**) is separate from defining the ESSID. The **BSSID** is the **AP radio MAC** used at Layer 2, not the ESSID (**C**).",
            "choices": [
                "It provides greater security than a standard SSID.",
                "It supports fast roaming features such as 802.11 r, 802.11k, and 802.11v.",
                "It serves as the wireless MAC address of the access point.",
                "It allows multiple access points to provide a common network for client connections.",
            ],
        },
        {
            "slug": "port-security-restrict-unknown-mac-snmp-trap",
            "title": "CCNA — Port security violation mode (restrict)",
            "stem": "Which port-security violation mode drops traffic from unknown MAC addresses and forwards an SNMP trap?",
            "name": "psviol1",
            "correct": "A",
            "explain": "Correct. A \u2014 **restrict** drops frames from **unknown** (violating) source MACs, increments the violation counter, and sends **SNMP traps** and **syslog** messages while keeping the port **up**. **protect** (**B**) also **drops** violating traffic but does **not** send SNMP traps. **shutdown** (**D**) is the default: it **err-disables** the interface and sends traps. **shutdown VLAN** (**C**) is not a standard per-port violation mode in this context.",
            "choices": [
                "restrict",
                "protect",
                "shutdown VLAN",
                "shutdown",
            ],
        },
        {
            "slug": "vm-shared-hardware-resources-same-hypervisor",
            "title": "CCNA — Resources shared by VMs on a hypervisor",
            "stem": "Which physical component is distributed among multiple virtual machines running on the same hypervisor?",
            "name": "vmres1",
            "correct": "A",
            "explain": "Correct. A \u2014 The **hypervisor** partitions the host\u2019s **hardware resources** (CPU, memory, and related capacity) and presents virtual hardware to each **VM** on the same host. **Network interfaces** (**B**) are virtualized per VM; the physical NICs belong to the host. A **backplane network** (**C**) is switch chassis fabric, not what VMs share on a hypervisor. **External storage** (**D**) may be accessed by many VMs but is **outside** the host and not the physical component **distributed** among co-resident VMs in this sense.",
            "choices": [
                "hardware resources",
                "network interfaces",
                "backplane network",
                "external storage",
            ],
        },
        {
            "slug": "crossover-cable-like-devices-no-auto-mdix",
            "title": "CCNA — Crossover cable (no auto-MDI-X)",
            "stem": "Which cable type must be used when connecting two **like devices** together using these criteria?\n\n\u2022 Pins **1 to 3** and **2 to 6** are required.\n\u2022 Auto-detection **MDI-X** is unavailable.",
            "name": "xover1",
            "correct": "C",
            "explain": "Correct. C \u2014 A **crossover** cable swaps **TX/RX** pairs for **10/100 Ethernet**: pin **1** to **3**, pin **2** to **6**, so two **like** devices (switch\u2013switch, host\u2013host) can communicate when **auto-MDI-X** is off. **Straight-through** (**A**) maps **1\u20131**, **2\u20132**, **3\u20133**, **6\u20136** for **unlike** devices (host to switch). **Console** (**B**) and **rollover** (**D**) are for **management** access, not Ethernet data links between like peers.",
            "choices": [
                "straight-through",
                "console",
                "crossover",
                "rollover",
            ],
        },
        {
            "slug": "pc2-unknown-mac-vlan-frame-flooding-concept",
            "title": "CCNA — Unknown MAC: frame flooding",
            "stem": "**PC1** tries to send traffic to newly installed **PC2**. The **PC2** MAC address is not listed in the MAC address table of the switch, so the switch sends the packet to all ports in the same VLAN. Which switching concept does this describe?",
            "name": "swfloodpc2",
            "correct": "D",
            "explain": "Correct. D \u2014 When the **destination MAC** is **unknown**, the switch performs **frame flooding** (unknown unicast): copies go to **every port in that VLAN** except the **ingress** port until **PC2** replies and the switch **learns** its MAC. **MAC address aging** (**A**) **removes** stale entries over time. The **MAC address table** (**B**) is the lookup structure, not the flooding action itself. **STP** (**C**) prevents Layer 2 loops; it does not define unknown-destination forwarding.",
            "choices": [
                "MAC address aging",
                "MAC address table",
                "spanning-tree protocol",
                "frame flooding",
            ],
        },
        {
            "slug": "security-physical-access-tasks-choose-two",
            "title": "CCNA — Physical access control tasks (choose two)",
            "stem": "Which two tasks support the **physical access control** element of a security program? (Choose two.)",
            "name": "phyacc2",
            "choose_two": True,
            "correct": ["A", "C"],
            "explain": "Correct. A and C \u2014 **Video surveillance** and **badge access** to critical areas control **who may enter physical spaces** and provide monitoring or audit of facility access. **Workshops** (**B**), **slideshows** (**D**), and **dispersing confidentiality guidance** (**E**) are **awareness**, **policy education**, or **information protection** tasks\u2014they do not by themselves implement **physical** entry control.",
            "choices": [
                "Deploy a video surveillance system",
                "Run a workshop on corporate security policies",
                "Implement badge access to critical locations",
                "Develop slideshows about new security regulations",
                "Disperse information about how to protect the organization\u2019s confidential data",
            ],
        },
        {
            "slug": "r9-fa0-0-queueing-atlanta-subnet-exhibit",
            "title": "CCNA — R9 Fa0/0 queueing (show interface)",
            "stem": "Which interface condition is occurring in this output?",
            "name": "r9que1",
            "correct": "C",
            "explain": "Correct. C \u2014 **Input queue 175/300**, **output queue 50/300**, and **Total output drops: 100** show packets backing up in interface **queues** and being discarded. **Duplex mismatch** (**D**) would usually show **collisions**, **late collisions**, or **deferred** frames; here the link is **full-duplex** with **0 collisions**. **Bad NIC** (**B**) typically raises **CRC**, **runts**, or **giants** (all **0**). **Broadcast storm** (**A**) would show a very high **broadcast** ratio; only **267** broadcasts appear among **7331** input packets.",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="R9 show interface FastEthernet0/0">
        <pre>R9# show interface fa0/0
FastEthernet0/0 is up, line protocol is up
Hardware is DEC21140, address is ca02.7788.0000 (bia ca02.7788.0000)
Description: atlanta_subnet
Internet address is 10.32.102.2/30
MTU 1500 bytes, BW 100000 Kbit/sec, DLY 100 usec,
 reliability 255/255, txload 1/255, rxload 1/255
Encapsulation ARPA, loopback not set
Keepalive set (60 sec)
full-duplex, 100 Mb/s, 100BaseTX/FX
ARP type: ARPA, ARP Timeout 04:00:00
Last input 00:00:01, output 00:00:00, output hang never
Last clearing of "show interface" counters 00:00:18
Input queue: 175/300/0/0 (size/max/drops/flushes); Total output drops: 100
Queueing strategy: fifo
Output queue: 50/300 (size/max)
30 second input rate 0 bits/sec, 0 packets/sec
30 second output rate 0 bits/sec, 0 packets/sec
7331 packets input, 7101162 bytes
Received 267 broadcasts (0 IP multicasts)
0 runts, 0 giants, 0 throttles
0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
0 watchdog
0 input packets with dribble condition detected
3927 packets output, 1440403 bytes, 0 underruns
0 output errors, 0 collisions, 0 interface resets
0 unknown protocol drops
0 babbles, 0 late collision, 0 deferred
0 lost carrier, 0 no carrier
0 output buffer failures, 0 output buffers swapped out</pre>
    </div>""",
            "choices": [
                "broadcast storm",
                "bad NIC",
                "queueing",
                "duplex mismatch",
            ],
        },
        {
            "slug": "security-phishing-user-awareness-training",
            "title": "CCNA — Mitigate phishing (user awareness)",
            "stem": "Network security team noticed that an increasing number of employees are becoming victims of **phishing attacks**. Which security program should be implemented to mitigate the problem?",
            "name": "phish1",
            "correct": "A",
            "explain": "Correct. A \u2014 **Phishing** is a **social-engineering** attack that tricks users into clicking malicious links, opening unsafe attachments, or revealing credentials. **User awareness training** teaches employees to recognize suspicious messages, verify senders, and report phishing. **Email system patches** (**B**) fix server vulnerabilities but do not stop users from falling for deceptive messages. A **host software firewall** (**C**) filters network traffic on the PC; it is not the primary control for email-based deception. **Physical access control** (**D**) regulates facility entry, not email fraud.",
            "choices": [
                "user awareness training",
                "email system patches",
                "software firewall enabled on all PCs",
                "physical access control",
            ],
        },
        {
            "slug": "ipsec-security-associations-peers-organization",
            "title": "CCNA — IPsec security associations",
            "stem": "How does **IPsec** provide secure networking for applications within an organization?",
            "name": "ipsecsa1",
            "correct": "C",
            "explain": "Correct. C \u2014 **IPsec** builds **security associations (SAs)** between **peers** (often negotiated with **IKE**). Each SA defines how traffic is protected\u2014for example **encryption**, **integrity**, and **keying**\u2014so application flows can cross the network confidentially and authentically. **TFTP** (**A**) and **FTP** (**D**) are file-transfer protocols; IPsec does not secure the organization by using them. **GRE** (**B**) can **carry** tunneled traffic and is often combined with IPsec, but **GRE alone** does not provide IPsec\u2019s cryptographic protection; **SAs** are the core IPsec mechanism.",
            "choices": [
                "It leverages TFTP providing secure file transfers among peers on the network.",
                "It provides GRE tunnels to transmit traffic securely between network nodes.",
                "It enables sets of security associations between peers.",
                "It takes advantage of FTP to secure file transfers between nodes on the network.",
            ],
        },
        {
            "slug": "multifactor-authentication-pin-rsa-certificate",
            "title": "CCNA — Multifactor authentication parameters",
            "stem": "A company has decided to require **multifactor authentication** for all systems. Which set of parameters meets the requirement?",
            "name": "mfa1",
            "correct": "A",
            "explain": "Correct. A \u2014 **MFA** requires factors from **different classes**: **something you know** (a **PIN**) plus **something you have** (an **RSA certificate** on a token or smart card). **B** and **C** pair only **knowledge** factors (password and PIN), which is still single-factor authentication twice. **D** uses two **biometric** factors (**fingerprint** and **facial recognition**)\u2014both **something you are**, not two distinct MFA classes.",
            "choices": [
                "personal 10-digit PIN and RSA certificate",
                "complex password and personal 10-digit PIN",
                "password of 8 to 15 characters and personal 12-digit PIN",
                "fingerprint scanning and facial recognition",
            ],
        },
        {
            "slug": "network-automation-manual-errors-inconsistencies-consideration",
            "title": "CCNA — Consider automation (manual errors)",
            "stem": "What should a network administrator consider when deciding to implement **automation**?",
            "name": "netauto3",
            "correct": "A",
            "explain": "Correct. A \u2014 **Manual CLI changes** on many devices often introduce **misconfigurations** and **inconsistent** settings; that operational pain is a primary reason teams adopt **automation** (templates, APIs, orchestration) for repeatable, uniform deployments. **B** is false: automation applies to **physical and virtual** network devices, not only virtual ones. **C** is false: automation typically **lowers** recurring management cost, not raises it. **D** is false: automation\u2019s strength is applying changes **at scale**, not struggling to expand them.",
            "choices": [
                "Manual changes frequently lead to configuration errors and inconsistencies.",
                "Network automation typically is limited to the configuration and management of virtual devices within a network.",
                "Network automation typically increases enterprise management operating costs.",
                "Automated systems may have difficulty expanding network changes at scale.",
            ],
        },
        {
            "slug": "tftp-loads-config-diskless-systems-capability",
            "title": "CCNA — TFTP capability",
            "stem": "Which capability does **TFTP** provide?",
            "name": "tftpcap1",
            "correct": "A",
            "explain": "Correct. A \u2014 **TFTP** (UDP port **69**) is a minimal file-transfer protocol used to **load configuration files** and **IOS images** onto network devices, including **diskless** or **PXE-boot** systems that pull files from a server at startup. **B** is wrong: TFTP is **not secure** (no encryption, weak authentication model). **C** is wrong: TFTP provides **no encryption** for WAN transfers. **D** is wrong: TFTP does **not** authenticate users the way **FTP**, **SSH**, or **RADIUS** do.",
            "choices": [
                "loads configuration files on systems without data storage devices",
                "provides secure file access within the LAN",
                "provides encryption mechanisms for file transfer across a WAN",
                "provides authentication for data communications over a private data network",
            ],
        },
        {
            "slug": "cat9k-gi101-broadcast-storm-printing-exhibit",
            "title": "CCNA — Cat9k Gi1/0/1 broadcast storm",
            "stem": "The switch **cat9k-acc-1** connects users to the campus LAN. **Printing services** are inaccessible through the network. Which interface issue is causing the connectivity problems?",
            "name": "cat9kbr1",
            "correct": "C",
            "explain": "Correct. C \u2014 **Received 1,925,500 broadcasts** among **2,295,197** input packets shows a **broadcast storm** flooding the access port and VLAN, starving usable bandwidth for normal traffic (including print services). **1 interface reset** fits storm-related instability. **A** (**CRC**/checksum): **1790 CRC** errors are present but are secondary to the overwhelming **broadcast** load. **B**: only **1 collision** on a **1000 Mb/s** link\u2014not excessive collisions. **D**: **Output queue 1/1** with **1 drop** does not show sustained **output-queue** congestion.",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="cat9k-acc-1 show interfaces GigabitEthernet1/0/1">
        <pre>cat9k-acc-1# show interfaces gigabitethernet 1/0/1
  gigabitethernet 1/0/1 is up, line protocol is up
  Hardware is gigabitethernet, address is aa00.0400.0134 (via 0000.0c00.4369)
  MTU 1500 bytes, BW 1000 Kbit, DLY 1000 usec, rely 255/255, load 1/255
  Encapsulation ARPA, loopback not set, keepalive set (10 sec)
  ARP type: ARPA, PROBE, ARP Timeout 4:00:00
  Last input 0:00:00, output 0:00:00, output hang never
  Output queue 1/1, 1 drops; input queue 0/0, 0 drops
  Five minute input rate 61000 bits/sec, 200 packets/sec
  Five minute output rate 1000 bits/sec, 200 packets/sec
  2295197 packets input, 305539992 bytes, 0 no buffer
  Received 1925500 broadcasts, 0 runts, 0 giants
  0 input errors, 1790 CRC, 1790 frame, 0 overrun, 0 ignored, 0 abort
  0 input packets with dribble condition detected
  3594664 packets output, 436549843 bytes, 1 underruns
  0 output errors, 1 collisions, 1 interface resets, 0 restarts</pre>
    </div>""",
            "choices": [
                "A bad checksum is causing Ethernet frames to drop.",
                "Excessive collisions are causing dropped frames.",
                "A large number of broadcast packets are resulting in a port reset.",
                "The interface output queue cannot process the Ethernet frames.",
            ],
        },
        {
            "slug": "ap-console-no-ip-management-connection",
            "title": "CCNA — AP management without IP",
            "stem": "Which connection type is used when an engineer connects to an **AP** without a configured **IP address** or **dial-up number** to manage the device?",
            "name": "apcon1",
            "correct": "B",
            "explain": "Correct. B \u2014 The **console** port provides **out-of-band** local access over a **serial/USB** cable for initial setup and recovery when the AP has **no management IP** and no modem **dial-up** path. **Ethernet** (**D**) requires network connectivity and a reachable **IP** for in-band management. **AUX** (**C**) is a legacy **modem** port on some routers, not the usual AP local-management method. **VIY** (**A**) is not a standard Cisco management connection type.",
            "choices": [
                "VIY",
                "console",
                "AUX",
                "Ethernet",
            ],
        },
        {
            "slug": "autonomous-ap-single-ssid-access-port",
            "title": "CCNA — Autonomous AP uplink (one SSID)",
            "stem": "Which type of wired port is required when an **AP** offers **one unique SSID**, passes **client data** and **management traffic**, and is in **autonomous mode**?",
            "name": "apssid1",
            "correct": "C",
            "explain": "Correct. C \u2014 An **autonomous** AP bridges wireless clients **locally** onto the wired LAN. With **one SSID** (typically **one VLAN**), the switch port toward the AP is an **access** port in that VLAN for both **client** and **AP management** traffic. A **trunk** (**B**) is required when the AP must carry **multiple VLANs** (for example several SSIDs mapped to different VLANs). **LAG** (**D**) bundles links for bandwidth or redundancy; it does not replace access vs trunk for VLAN behavior. **Default** (**A**) is not a switch port mode.",
            "choices": [
                "default",
                "trunk",
                "access",
                "LAG",
            ],
        },
        {
            "slug": "sw2-lacp-gi01-02-channel-group-active-exhibit",
            "title": "CCNA — LACP EtherChannel SW2 Gi0/1-2",
            "stem": "An **LACP EtherChannel** between two directly connected switches is in the configuration process. Which command must be configured on switch **SW2**\u2019s **Gi0/1-2** interfaces to establish the channel to **SW1**?",
            "name": "lacpsw2gi",
            "correct": "C",
            "mono": True,
            "explain": "Correct. C \u2014 **SW1** already has **`channel-group 1 mode active`** (LACP) on **Gi0/1-2**. **SW2** must assign the same **group** with an **LACP** mode on those member ports\u2014**`channel-group 1 mode active`**\u2014so LACP can negotiate and form **Port-channel1**. **`mode desirable`** (**A**) and **`mode auto`** (**D**) are **PAgP**, not LACP. **`mode on`** (**B**) is a **static** EtherChannel with **no** LACP PDUs and will not match **active** on **SW1**.",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="SW1 and SW2 EtherChannel configuration">
        <pre>SW1
configure terminal
interface range GigabitEthernet 0/1-2
 switchport mode trunk
 channel-group 1 mode active

SW2
configure terminal
interface range GigabitEthernet 0/1-2
 switchport mode trunk
interface Port-channel1
 switchport mode trunk</pre>
    </div>""",
            "choices": [
                "channel-group 1 mode desirable",
                "channel-group 1 mode on",
                "channel-group 1 mode active",
                "channel-group 1 mode auto",
            ],
        },
        {
            "slug": "windows-service-desk-ipconfig-all-verify-ip-dns",
            "title": "CCNA — Windows: verify IP and DNS",
            "stem": "An on-site service desk technician must verify the **IP address** and **DNS server** information on a user\u2019s **Windows** computer. Which command must the technician enter at the command prompt on the user\u2019s computer?",
            "name": "winipc1",
            "correct": "A",
            "explain": "Correct. A \u2014 On **Windows**, **`ipconfig /all`** displays full TCP/IP settings for each adapter, including **IPv4/IPv6 addresses**, **subnet mask**, **default gateway**, and **DNS servers**. **`show interface`** (**B**) is **Cisco IOS**, not a Windows command. **`netstat -r`** (**C**) shows the **routing table**, not complete IP/DNS client configuration. **`ifconfig -a`** (**D**) is used on **Linux/Unix/macOS**, not the standard Windows **CMD/PowerShell** command.",
            "choices": [
                "ipconfig /all",
                "show interface",
                "netstat -r",
                "ifconfig -a",
            ],
        },
        {
            "slug": "dhcp-server-functions-centralized-dynamic-choose-two",
            "title": "CCNA — DHCP server functions (choose two)",
            "stem": "What are two functions of **DHCP servers**? (Choose two.)",
            "name": "dhcpsrv1",
            "choose_two": True,
            "correct": ["A", "E"],
            "explain": "Correct. A and E \u2014 **DHCP servers** provide **centralized IP management** and **assign dynamic** IPv4 (and often IPv6) **configurations** (address, mask, gateway, DNS, lease time) to hosts. **B** is wrong: **clients** send **DHCPDISCOVER**, not servers. **C** reverses the **DORA** flow: the **server** sends **DHCPOFFER**; the **client** sends **DHCPREQUEST** after the offer. **D** overstates DHCP\u2014hosts can still use **static** addresses unless other controls (for example **DHCP snooping** or policy) block it.",
            "choices": [
                "support centralized IP management",
                "issue DHCPDISCOVER messages when added to the network",
                "respond to client DHCPOFFER requests by Issuing an IP address",
                "prevent users from assigning their own IP addresses to hosts",
                "assign dynamic IP configurations to hosts in a network",
            ],
        },
        {
            "slug": "snmp-inform-reliable-manager-acknowledgment",
            "title": "CCNA — SNMP Inform (reliable, manager ACK)",
            "stem": "Which **SNMP** message type is **reliable** and precedes an **acknowledgment response from the SNMP manager**?",
            "name": "snmpinf1",
            "correct": "A",
            "explain": "Correct. A \u2014 An **Inform** PDU is like a **trap** sent from agent to manager, but the **manager must return an acknowledgment**, so the agent knows the event was received (**reliable** delivery). **Traps** (**C**) are **unacknowledged** (fire-and-forget). **Get** (**B**) and **Set** (**D**) are **manager-initiated** requests; the **agent** replies with a **Response** PDU, not a manager ACK for an agent-originated event.",
            "choices": [
                "Inform",
                "Get",
                "Traps",
                "Set",
            ],
        },
        {
            "slug": "wlc-multiple-ap-manager-fewest-aps-join",
            "title": "CCNA — Multiple AP-Manager interfaces",
            "stem": "When more than one **AP-Manager** interface is provisioned on a wireless LAN controller, how is the request handled by the **AP**?",
            "name": "apmgr1",
            "correct": "D",
            "explain": "Correct. D \u2014 During **CAPWAP discovery**, the WLC\u2019s **discovery response** lists **AP-Manager** interfaces and how many **APs** are on each. The **AP generally joins the AP-Manager with the fewest APs**, spreading load across interfaces. **A** is wrong: discovery does not **disable the WLAN port**. **B** is wrong: join does not **fail** solely because multiple AP-Managers exist. **C** is wrong: selection is **not** simply the **first to respond**\u2014**load** (AP count per interface) drives the choice.",
            "choices": [
                "The discovery response from the AP to the AP-Manager interface disables the WLAN port",
                "The AP join request fails and must be configured statically on the AP-Manager interface",
                "The first AP-Manager interface to respond is chosen by the AP",
                "The AP-Manager with the fewest number of APs is used by the AP to join",
            ],
        },
        {
            "slug": "wlc-service-manages-interference-dense-network",
            "title": "CCNA — Wireless controller service",
            "stem": "What is a service that is provided by a **wireless controller**?",
            "name": "wlcsvc1",
            "correct": "B",
            "explain": "Correct. B \u2014 A **WLC** centralizes **RF management** (**RRM**): **channel** and **transmit-power** assignment, neighbor awareness, and interference mitigation in **dense** deployments. **A** is wrong: **DHCP** (or a dedicated server) issues **IP addresses**; the WLC may **relay** DHCP for WLAN clients but does not primarily serve **wired** devices. **C** is wrong: **Layer 3 routing** between wired and wireless segments is typically performed by **routers/L3 switches**, not the WLC\u2019s core role. **D** is wrong: **Internet threat mitigation** is the job of **firewalls/IPS/edge security**, not the WLC.",
            "choices": [
                "It issues IP addresses to wired devices.",
                "It manages interference in a dense network.",
                "It provides Layer 3 routing between wired and wireless devices.",
                "It mitigates threats from the internet.",
            ],
        },
        {
            "slug": "windows-dhcp-renew-contact-server-wifi-exhibit",
            "title": "CCNA — DHCP renew (Wi-Fi ipconfig)",
            "stem": "Which address will the client contact to **renew** their IP address when the current lease expires?",
            "name": "dhcprnw1",
            "correct": "B",
            "explain": "Correct. B \u2014 **`ipconfig /all`** shows **DHCP Server . . . : 192.168.25.100**. On **lease renewal**, the host sends **DHCPREQUEST** to the **same DHCP server** that issued the lease (**192.168.25.100**). **A** (**192.168.25.103**) is the **client\u2019s own IPv4 address**. **C** (**192.168.25.1**) is the **default gateway** (routing), not the DHCP server. **D** (**192.168.25.254**) is a **DNS server** (name resolution).",
            "prepend_html": """    <div class="exhibit-terminal-white" role="region" aria-label="Windows ipconfig wireless LAN adapter">
        <pre>Wireless LAN adapter Wi-Fi

Connection-specific DNS Suffix  . :
Description . . . . . . . . . . . : Intel(R) Dual Band Wireless-AC 7265
Physical Address. . . . . . . . . : C8-21-5B-B4-D3-E0
DHCP Enabled. . . . . . . . . . . : Yes
Autoconfiguration Enabled . . . . : Yes
Link-local IPv6 Address . . . . . : fe80::45a1:b3fa:2f37:bf37%2(Preferred)
IPv4 Address. . . . . . . . . . . : 192.168.25.103(Preferred)
Subnet Mask . . . . . . . . . . . : 255.255.255.0
Lease Obtained. . . . . . . . . . : June 11, 2019 10:21:31 AM
Lease Expires . . . . . . . . . . : June 12, 2019 10:21:36 AM
Default Gateway . . . . . . . . . : 192.168.25.1
DHCP Server . . . . . . . . . . . : 192.168.25.100
DHCPv6 IAID . . . . . . . . . . . : 46670168
DHCPv6 Client DUID. . . . . . . . : 00-01-00-01-20-FF-05-55-3C-52-82-33-D3-84
DNS Servers . . . . . . . . . . . : 192.168.25.254
                                    192.168.25.254</pre>
    </div>""",
            "choices": [
                "192.168.25.103",
                "192.168.25.100",
                "192.168.25.1",
                "192.168.25.254",
            ],
        },
        {
            "slug": "json-cisco-devices-missing-closing-brace",
            "title": "CCNA — JSON syntax (missing brace)",
            "stem": "What is missing from this output for it to be executed?",
            "name": "jsonbr1",
            "correct": "B",
            "explain": "Correct. B \u2014 Valid JSON **objects** must balance **`{` and `}`**. The snippet opens a root **`{`**, closes the inner object and the **`[` array with `]`**, but is **missing the final `}`** that closes the outer object. **A** is wrong: the array already has **`[`** after **\"Cisco Devices\"**. **C** is wrong: **\"Cisco Devices\"** is already in **double quotes**. **D** is wrong: **`!`** is not JSON syntax. (The inner object also repeats the **`name`** key three times, which is poor JSON design, but the brace is what makes it invalid.)",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="Invalid JSON exhibit">
        <pre>{
"Cisco Devices": [
{
"name": "ASA - Security Device",
"name": "Cisco 1100 ASR Router",
"name": "Cisco 6800 Switch"
}
]</pre>
    </div>""",
            "choices": [
                "square bracket ( [ ) at the beginning",
                "curly brace ( } ) at the end",
                "double quotes (\" \") around the \"Cisco Devices\" string",
                "exclamation point (!) at the beginning of each line",
            ],
        },
        {
            "slug": "private-ipv4-benefits-shortage-security-choose-two",
            "title": "CCNA — Private IPv4 benefits (choose two)",
            "stem": "What are two **benefits** for using **private IPv4** addressing? (Choose two.)",
            "name": "priv42",
            "choose_two": True,
            "correct": ["B", "C"],
            "explain": "Correct. B and C \u2014 **RFC 1918 private IPv4** (**10/8**, **172.16/12**, **192.168/16**) lets many internal hosts share **non\u2013globally unique** space, **easing the shortage of public IPv4** (often with **NAT/PAT** at the edge). Private addresses are **not routed on the public Internet**, which adds a **layer of obscurity** against direct Internet reachability (still use **firewalls** and policy). **A** is wrong: **redundancy** comes from **HA/failover** designs, not private addressing alone. **D** and **E** misstate the benefit: **Internet access** for private hosts requires **NAT** or proxies\u2014private space by itself does not \u201coffer\u201d or \u201callow\u201d Internet connectivity.",
            "choices": [
                "They supply redundancy in the case of failure",
                "They alleviate the shortage of public IPv4 addresses.",
                "They provide a layer of security from Internet threats.",
                "They offer Internet connectivity to endpoints on private networks",
                "They allow for Internet access from IoT devices",
            ],
        },
        {
            "slug": "access-switch-arp-spoof-dai-dhcp-snooping-po1-choose-two",
            "title": "CCNA — ARP spoofing: DAI + DHCP snooping (choose two)",
            "stem": "A network administrator is evaluating network security in the aftermath of an attempted **ARP spoofing** attack. If **Port-channel1** is the **uplink** interface of the access-layer switch toward the distribution-layer switch, which **two** configurations must the administrator configure on the access-layer switch to provide adequate protection? (Choose two.)",
            "name": "arpspoof1",
            "choose_two": True,
            "mono": True,
            "correct": ["B", "E"],
            "explain": "Correct. B and E \u2014 **Dynamic ARP Inspection (DAI)** needs a trusted binding source, usually the **DHCP snooping binding table**. **Option B** enables **DHCP snooping** on VLANs and marks the **uplink Port-channel1** as **ip dhcp snooping trust** so legitimate DHCP server traffic from the distribution path is accepted. **Option E** enables **ip arp inspection vlan 1-4094** and **ip arp inspection trust** on **Port-channel1** so ARP on access ports is validated while the uplink is trusted. **A** and **C** misuse **port-security** on the uplink instead of snooping/DAI trust. **D** uses invalid global **ip arp inspection trust** syntax and unrelated **port-security**/**ip verify source** on the uplink.",
            "choices": [
                """Option A

ip dhcp snooping
!
interface Port-channel1
 switchport port-security maximum 1
 switchport port-security""",
                """Option B

ip dhcp snooping vlan 1-4094
ip dhcp snooping
!
interface Port-channel1
 ip dhcp snooping trust""",
                """Option C

ip dhcp snooping vlan 1-4094
!
interface Port-channel1
 switchport protected
 switchport port-security maximum 1""",
                """Option D

ip arp inspection trust
!
interface Port-channel1
 switchport port-security maximum 4094
 switchport port-security
 ip verify source mac-check""",
                """Option E

ip arp inspection vlan 1-4094
!
interface Port-channel1
 ip arp inspection trust""",
            ],
        },
        {
            "slug": "wlc-maximum-concurrent-telnet-sessions-five",
            "title": "CCNA — WLC maximum Telnet sessions",
            "stem": "What is the maximum number of **concurrent Telnet sessions** that a Cisco **WLC** supports?",
            "name": "wlctel1",
            "correct": "B",
            "explain": "Correct. B \u2014 Cisco WLC administration documentation limits **CLI** access to **five** simultaneous **Telnet** or **SSH** sessions (default **maximum** is **5**). Additional logins receive a **maximum connections reached** message. **3**, **6**, and **15** are not the documented WLC Telnet/SSH session cap ( **15** is a common **VTY** count on IOS routers, not this WLC limit).",
            "choices": [
                "3",
                "5",
                "6",
                "15",
            ],
        },
        {
            "slug": "firewall-enterprise-vpn-url-functions-choose-two",
            "title": "CCNA — Firewall functions in enterprise (choose two)",
            "stem": "What are two functions of a **firewall** within an enterprise? (Choose two.)",
            "name": "fwent1",
            "choose_two": True,
            "correct": ["A", "B"],
            "explain": "Correct. A and B \u2014 Enterprise **firewalls** (for example **Cisco ASA** or **FTD**) commonly terminate **site-to-site IPsec VPNs** and apply **URL/application filtering** policies on traffic. **C** describes a valid **remote-access VPN** role but **multiple context mode** is a specific **ASA** deployment detail, not a general second function paired with URL filtering on CCNA items. **D** is wrong: **Layer 2** forwarding between hosts is a **switch** function. **E** is wrong: **wireless association** is handled by **APs/WLCs**, not the firewall.",
            "choices": [
                "It serves as an endpoint for a site-to-site VPN in standalone mode.",
                "It enables traffic filtering based on URLs.",
                "It provides support as an endpoint for a remote access VPN in multiple context mode.",
                "It offers Layer 2 services between hosts.",
                "It enables wireless devices to connect to the network.",
            ],
        },
        {
            "slug": "chef-agent-pulls-cookbook-configuration-from-server",
            "title": "CCNA — Chef pull model",
            "stem": "How does **Chef** configuration management enforce a required device configuration?",
            "name": "chef1",
            "correct": "A",
            "explain": "Correct. A \u2014 **Chef** uses a **pull** model: the **Chef client (agent)** on the node registers with the **Chef Infra Server**, downloads the assigned **cookbooks/recipes**, and **converges** the device to the desired state locally. **B** and **D** describe a **server push** model, which is **not** how Chef works. **C** is wrong: the server does not merely **alert** devices to pull on a signal\u2014the client runs on a **schedule** (or triggered run) and pulls configuration as part of its normal **chef-client** cycle.",
            "choices": [
                "The installed agent on the device connects to the Chef Infra Server and pulls its required configuration from the cookbook.",
                "The Chef Infra Server uses its configured cookbook to push the required configuration to the remote device requesting updates.",
                "The Chef Infra Server uses its configured cookbook to alert each remote device when it is time for the device to pull a new configuration.",
                "The installed agent on the device queries the Chef Infra Server and the server responds by pushing the configuration from the cookbook.",
            ],
        },
        {
            "slug": "ansible-inventory-defines-target-devices",
            "title": "CCNA — Ansible inventory",
            "stem": "What is an **Ansible inventory**?",
            "name": "ansinv1",
            "correct": "D",
            "explain": "Correct. D \u2014 The **inventory** is the host list (often an **INI** or **YAML** file, or a dynamic plugin) that names the **target devices** and groups them so **playbooks** know where to run **tasks**. **A** describes a **playbook** (ordered actions in YAML). **B** describes an Ansible **module** (reusable units of work, often implemented in Python). **C** describes the **control node** (where **ansible-playbook** / **ansible** runs), not the inventory itself.",
            "choices": [
                "collection of actions to perform on target devices, expressed in YAML format",
                "unit of Python code to be executed within Ansible",
                "device with Ansible installed that manages target devices",
                "file that defines the target devices upon which commands and tasks are executed",
            ],
        },
        {
            "slug": "private-ipv4-host-addresses-rfc1918-choose-two",
            "title": "CCNA — Private host addresses (choose two)",
            "stem": "Which two host addresses are reserved for **private use** within an enterprise network? (Choose two.)",
            "name": "privhost1",
            "choose_two": True,
            "correct": ["A", "E"],
            "explain": "Correct. A and E \u2014 **RFC 1918** private IPv4 ranges are **10.0.0.0/8** (**10.172.76.200**), **172.16.0.0/12** (**172.16.0.0\u2013172.31.255.255**, including **172.31.255.100**), and **192.168.0.0/16**. **B** (**12.17.1.20**) is **public** space. **C** (**172.15.2.250**) is outside the **172.16\u2013172.31** private block. **D** (**192.169.32.10**) is **not** in **192.168.0.0/16** (only **192.168.x.x** is private in the 192.168 block).",
            "choices": [
                "10.172.76.200",
                "12.17.1.20",
                "172.15.2.250",
                "192.169.32.10",
                "172.31.255.100",
            ],
        },
        {
            "slug": "wlc-switch-etherchannel-load-balance-src-dst-ip",
            "title": "CCNA — WLC switch load balancing",
            "stem": "What is the **recommended switch load-balancing mode** for Cisco **WLCs**?",
            "name": "wlclb1",
            "correct": "D",
            "explain": "Correct. D \u2014 On the **access/distribution switch** EtherChannel toward a **WLC** (especially with **LAG**), Cisco recommends **source-destination IP** hashing (**src-dst-ip**) so client flows distribute across member links. **MAC-only** methods (**A**, **C**) often pin too much traffic to one link because many frames share the WLC or AP **MAC** addresses. **Destination IP only** (**B**) can skew hashing when many flows share the same destination.",
            "choices": [
                "source-destination MAC address",
                "destination IP address",
                "destination MAC address",
                "source-destination IP address",
            ],
        },
        {
            "slug": "aaa-authentication-vs-accounting-choose-two",
            "title": "CCNA — Authentication vs accounting (choose two)",
            "stem": "Which two statements distinguish **authentication** from **accounting**? (Choose two.)",
            "name": "aaaacct1",
            "choose_two": True,
            "correct": ["A", "C"],
            "explain": "Correct. A and C \u2014 **Authentication** challenges **credentials** and returns **accept/deny**; it verifies **who you are**. **Accounting** tracks **what** was done: **user-activity audits** (**B**), **connection duration** (**D**), and **billing/supporting usage records** (**E**). Those are **accounting**, not authentication.",
            "choices": [
                "Only authentication challenges users for their credentials and returns a response.",
                "Only authentication supports user-activity audits.",
                "Only authentication validates \u201cwho you are.\u201d",
                "Only authentication records the duration of a user\u2019s connection.",
                "Only authentication provides supporting information for billing users.",
            ],
        },
        {
            "slug": "rest-api-supported-methods-get-put-post-delete",
            "title": "CCNA — REST API HTTP methods",
            "stem": "Which set of methods is supported with the **REST API**?",
            "name": "restmethset1",
            "correct": "D",
            "explain": "Correct. D \u2014 **REST** APIs use standard **HTTP verbs**: **GET** (read), **POST** (create/submit), **PUT** (update/replace), and **DELETE** (remove). **ERASE**, **CHANGE**, and **MOD** are **not** standard HTTP/REST methods on Cisco controllers and DevNet-style APIs.",
            "choices": [
                "GET, PUT, ERASE, CHANGE",
                "GET, POST, ERASE, CHANGE",
                "GET, POST, MOD, ERASE",
                "GET, PUT, POST, DELETE",
            ],
        },
        {
            "slug": "json-rfc4627-default-encoding-utf8",
            "title": "CCNA — JSON default encoding (RFC 4627)",
            "stem": "What is the **RFC 4627** default encoding for **JSON** text?",
            "name": "jsonenc1",
            "correct": "A",
            "explain": "Correct. A \u2014 **RFC 4627** specifies that **JSON text** is Unicode and is **encoded in UTF-8** by default for interchange (UTF-16 variants are also defined in the RFC family, but **UTF-8** is the usual default on Cisco automation and **REST** APIs). **GB18030** and **UCS-2** are not the JSON default. **Hex** is not a character encoding for JSON documents.",
            "choices": [
                "UTF-8",
                "GB18030",
                "UCS-2",
                "Hex",
            ],
        },
        {
            "slug": "json-array-red-one-string-elements",
            "title": "CCNA — JSON array type",
            "stem": "<code>[\"red\", \"one\"]</code>\n\nWhich type of **JSON** data is represented?",
            "name": "jsontype1",
            "correct": "B",
            "explain": "Correct. B \u2014 Square brackets **`[ ]`** enclose a **JSON array**: an ordered list of values. Here the elements are two **strings** (**\"red\"** and **\"one\"**), but the whole construct is an **array**, not a single string. **A** is wrong: numbers are unquoted digits. **C** is wrong: **objects** use **`{ }`** with **key:value** pairs. **D** is wrong: a **string** is one quoted value, not a bracketed list.",
            "choices": [
                "number",
                "array",
                "object",
                "string",
            ],
        },
        {
            "slug": "branch-router-ntp-server-sync-head-office",
            "title": "CCNA — NTP client to central server",
            "stem": "A network engineer is configuring a new router at a branch office. The router is connected to an upstream **WAN** network that allows the branch to communicate with the head office. The central time server with IP address **172.24.54.8** is located behind a firewall at the head office. Which command must the engineer configure so that the **software clock** of the new router synchronizes with the time server?",
            "name": "ntpbr1",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 **`ntp server 172.24.54.8`** makes the branch router an **NTP client** of the head-office time server so its **software clock** can synchronize (verify with **`show ntp associations`** / **`show clock`**). **A** (**ntp client**) is not valid **IOS** syntax for this role. **B** (**ntp master**) advertises time **from this router\u2019s own clock** as an authoritative source\u2014it does not point at an upstream server. **C** (**ntp peer**) configures a **symmetric active** association with another NTP device, not the usual branch-to-central client setup.",
            "choices": [
                "ntp client 172.24.54.8",
                "ntp master 172.24.54.8",
                "ntp peer 172.24.54.8",
                "ntp server 172.24.54.8",
            ],
        },
        {
            "slug": "router-wan1-gi00-isp-crc-collisions-duplex-exhibit",
            "title": "CCNA — WAN Gi0/0 CRC and collisions",
            "stem": "Refer to the exhibit. **Router-WAN1** has a new connection via **Gi0/0** to the **ISP**. Users running web applications indicate that connectivity to the internet is **unstable**. What is causing the interface issue?",
            "name": "wan1gi1",
            "correct": "C",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="Router-WAN1 show interface g0/0 CLI output">
        <pre>Router-WAN1#show interface g0/0
GigabitEthernet0/0 is up, line protocol is up
  Hardware is CSR NIC, address is 5000.0001.0000 (bia 5000.0001.0000)
  Internet address is 192.168.0.0/31
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
    reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Keepalive set (10 sec)
  Full Duplex, 1000Mbps, link type is auto, media type is NIC
  output flow-control is unsupported, input flow-control is unsupported
  ARP type: ARPA, ARP Timeout 04:00:00
  Last input never, output 00:00:03, output hang never
  Last clearing of "show interface" counters never
  Input queue: 0/375/0/0 (size/max/drops/flushes); Total output drops: 0
  Queueing strategy: fifo
  Output queue: 0/40 (size /max)
  5 minute input rate 1000 bits/sec, 0 packets/sec
  5 minute output rate 2000 bits/sec, 1 packets/sec
    0 packets input, 0 bytes, 0 no buffer
    Received 110 broadcasts (0 IP multicasts)
    0 runts, 0 giants, 0 throttles
    100 input errors, 100 CRC, 100 frame, 0 overrun, 0 ignored
    0 watchdog, 0 multicast, 0 pause input
    260 packets output, 89070 bytes, 0 underruns
    Output 0 broadcasts (0 IP multicasts)
    0 output errors, 100 collisions, 0 interface resets
    0 unknown protocol drops
    0 babbles, 0 late collision, 0 deferred
    1 lost carrier, 0 no carrier, 0 pause output</pre>
      </div>
    </div>""",
            "explain": "Correct. C \u2014 The port reports **Full Duplex** locally, but **100 CRC/frame input errors** and **100 collisions** on a full-duplex Ethernet link are a classic **duplex mismatch** signature (the **ISP** side or autonegotiation may be **half duplex** while this router believes it is full duplex). That corrupts frames and causes unstable application connectivity. **A** is wrong: **ARP timeout** does not explain **CRC** errors and **collisions**. **B** is wrong: there is no broadcast storm pattern (low broadcast count, no input queue drops). **D** is wrong: **runts** (undersized frames) are **0**.",
            "choices": [
                "Broadcast packets are rejected because ARP timeout is enabled",
                "The receive buffer is full due to a broadcast storm",
                "Frames are discarded due to a half-duplex negotiation",
                "Small frames less than 64 bytes are rejected due to size",
            ],
        },
        {
            "slug": "forward-100-100-100-100-longest-match-exhibit",
            "title": "CCNA — Longest match 100.100.100.100",
            "stem": "Refer to the exhibit. How will the device handle a packet destined to IP address **100.100.100.100**?",
            "name": "rt1001",
            "correct": "D",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="Routing table excerpt for 100.0.0.0/8 variably subnetted">
        <pre>100.0.0.0/8 is variably subnetted, 4 subnets, 4 masks
R    100.0.0.0/8 [120/2] via 192.168.3.1, 00:00:13, Ethernet0/3
S    100.100.0.0/16 [1/0] via 192.168.4.1
D    100.100.100.0/24 [90/435200] via 192.168.2.1, 00:00:13, Ethernet0/2
O    100.100.100.100/32 [110/21] via 192.168.1.1, 00:05:57, Ethernet0/1</pre>
      </div>
    </div>""",
            "explain": "Correct. D \u2014 **100.100.100.100** matches all four prefixes, but the router uses **longest-prefix match**: **100.100.100.100/32** (**OSPF**) is more specific than **/24**, **/16**, and **/8**, so traffic uses **192.168.1.1** on **Ethernet0/1**. **A** is wrong: **administrative distance** applies only when **prefix lengths tie**; **/16** does not beat **/32**. **B** and **C** are wrong: the router does **not** pick routes by **lowest** or **highest** metric alone when multiple **different mask lengths** match.",
            "choices": [
                "It will always prefer the static route over dynamic routes and choose the route\nS 100.100.0.0/16 [1/0] via 192.168.4.1",
                "It will choose the route with the lowest metric\nR 100.0.0.0/8 [120/2] via 192.168.3.1, 00:00:13, Ethernet0/3",
                "It will choose the route with the highest metric\nD 100.100.100.0/24 [90/435200] via 192.168.2.1, 00:00:13, Ethernet0/2",
                "It will choose the route with the longest match\nO 100.100.100.100/32 [110/21] via 192.168.1.1, 00:05:57, Ethernet0/1",
            ],
            "mono": True,
        },
        {
            "slug": "rapid-pvst-plus-blocking-no-mac-learning",
            "title": "CCNA — Rapid PVST+ blocking port state",
            "stem": "Which **Rapid PVST+** port state does a port operate in **without receiving BPDUs from neighbors** or **updating the address database**?",
            "name": "rpvstblk1",
            "correct": "D",
            "explain": "Correct. D \u2014 A port in **blocking** (RSTP **discarding**) does **not forward** user traffic and does **not learn** **MAC** addresses into the **CAM** table while it is blocked to prevent loops. **Listening** (**A**) is a **classic 802.1D STP** transitional state; **Rapid PVST+** uses **discarding**, **learning**, and **forwarding** instead. **Forwarding** (**B**) passes traffic and **updates** the **MAC** table. **Disabled** (**C**) is an **administratively shut down** port, not the normal **spanning-tree blocked** role for loop prevention.",
            "choices": [
                "listening",
                "forwarding",
                "disabled",
                "blocking",
            ],
        },
        {
            "slug": "ftp-tcp-20-21-large-files-intranet",
            "title": "CCNA — FTP TCP 20 and 21",
            "stem": "Which protocol should be used to transfer **large files** on a company **intranet** that allows **TCP 20** and **TCP 21** through the firewall?",
            "name": "ftpport1",
            "correct": "A",
            "explain": "Correct. A \u2014 **FTP** uses **TCP port 21** for the **control** channel and **TCP port 20** for the **data** channel (typical **active-mode** data transfer), which matches opening **20** and **21** for large file copies. **TFTP** (**C**) uses **UDP port 69**, not **TCP 20/21**. **REST API** (**B**) normally uses **HTTP/HTTPS** (**TCP 80/443**), not **20/21**. **SMTP** (**D**) is for **email** (**TCP 25** and related), not general bulk file transfer on an intranet.",
            "choices": [
                "FTP",
                "REST API",
                "TFTP",
                "SMTP",
            ],
        },
        {
            "slug": "enterprise-device-certificate-auth-corporate-network",
            "title": "CCNA — Certificate auth vs passwords",
            "stem": "Which alternative to **password authentication** is implemented to allow **enterprise devices** to log in to the **corporate network**?",
            "name": "entcert1",
            "correct": "A",
            "explain": "Correct. A \u2014 **Digital certificates** support **certificate-based** network access (for example **802.1X** with **EAP-TLS** and a **PKI**), so **devices** or users can authenticate **without** relying on a shared password alone. **Magic links** (**B**) are a **web/email** login pattern, not typical for **switch/WLAN port** access. **One-time passwords** (**C**) are often an **MFA** factor used **with** passwords, not the usual enterprise **device** network-login replacement named here. **90-day renewal policies** (**D**) are **password lifecycle** rules, not a different **authentication** mechanism.",
            "choices": [
                "digital certificates",
                "magic links",
                "one-time passwords",
                "90-day renewal policies",
            ],
        },
        {
            "slug": "secure-password-policy-complex-length-guideline",
            "title": "CCNA — Secure password policy guideline",
            "stem": "Which guideline helps to create a **secure password policy**?",
            "name": "pwpol1",
            "correct": "C",
            "explain": "Correct. C \u2014 A strong policy enforces **length** and **complexity** (mixed character types) instead of **short, simple** passwords that are easy to guess or crack. **A** is poor practice: **password managers** help users store **unique**, strong secrets safely. **B** is risky: **service account** credentials should be **managed and rotated**, not left to **never expire** without controls. **D** is wrong: **passwords must not be shared** with any group\u2014each account needs its own credential.",
            "choices": [
                "forbidding users from storing passwords in a password manager",
                "allowing passwords used by service accounts to never expire",
                "requiring complex, lengthy passwords instead of simple, short ones",
                "restricting password sharing to a very small group",
            ],
        },
        {
            "slug": "sw1-vty-ssh-only-service-password-encryption-exhibit",
            "title": "CCNA — SW1 VTY SSH and hide passwords",
            "stem": "Refer to the exhibit. A network engineer started to change default settings on **SW1** to allow remote access and has entered configuration on **VTY 0\u201315. Which set of commands are needed to allow **only SSH** access and **hide passwords** in the running configuration?",
            "name": "sw1ssh1",
            "correct": "B",
            "mono": True,
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="SW1 partial configuration">
        <pre>SW1#conf t
Enter configuration commands, one per line. End with CNTL/Z.
SW1(config)#enable password test!2E
SW1(config)#line con 0
SW1(config-line)#password Labtest32!
SW1(config-line)#exit
SW1(config)#
SW1(config)#line vty 0 15
SW1(config-line)#password Labtest32!</pre>
      </motion-div>
    </div>""",
            "post_stem_html": """    <p><strong>Option A</strong></p>
    <pre>SW1(config-line)#login local
SW1(config-line)#exit
SW1(config)#enable secret test!2E</pre>
    <p><strong>Option B</strong></p>
    <pre>SW1(config-line)#transport input ssh
SW1(config-line)#exit
SW1(config)#service password-encryption</pre>
    <p><strong>Option C</strong></p>
    <pre>SW1(config-line)#login local
SW1(config-line)#exit</pre>
    <p><strong>Option D</strong></p>
    <pre>SW1(config-line)#exit
SW1(config)#aaa new-model</pre>""",
            "explain": "Correct. B (Option B) \u2014 **`transport input ssh`** on **VTY** lines permits **only SSH**, not **Telnet**. **`service password-encryption`** scrambles **line** and **enable** passwords in **`show running-config`** so they are not shown in **cleartext**. **Option A** hashes the **enable** password with **`enable secret`** but does **not** restrict **VTY** to **SSH**. **Option C** only sets **`login local`** without **SSH-only** transport or hiding **line** passwords. **Option D** enables **AAA** only; it does not complete **SSH-only VTY** access or password obfuscation by itself (SSH still needs keys, domain name, and related steps beyond this snippet).",
            "choices": [
                "Option A",
                "Option B",
                "Option C",
                "Option D",
            ],
        },
        {
            "slug": "ml-ids-identifies-intrusion-patterns",
            "title": "CCNA — ML and intrusion detection",
            "stem": "How does **machine learning** contribute to the effectiveness of **intrusion detection systems**?",
            "name": "mlids1",
            "correct": "D",
            "explain": "Correct. D \u2014 **Machine learning** helps **IDS/IPS** and modern security analytics detect **patterns** and **anomalies** in traffic or behavior that may indicate **intrusions**, improving detection beyond static signatures alone. **A** describes **access classification/clearance**, not IDS analytics. **B** overstates ML: **policy updates** are usually defined by administrators and governance, not autonomously \u201cdictated\u201d by ML. **C** is **vulnerability/patch management**, not the core ML role in **intrusion detection**.",
            "choices": [
                "It assigns security clearance levels.",
                "It dictates security policy updates.",
                "It monitors for outdated software.",
                "It identifies patterns indicating intrusions.",
            ],
        },
        {
            "slug": "ipsec-vpn-deployment-transport-mode-consideration",
            "title": "CCNA — IPsec VPN planning",
            "stem": "What must be considered when planning an **IPsec VPN** deployment?",
            "name": "ipsecp1",
            "correct": "A",
            "explain": "Correct. A \u2014 In **IPsec transport mode**, the **original IP header** remains **readable**, so **intermediate routers** can see the **true source and destination** addresses. That affects **path visibility**, **filtering**, and **topology** choices versus **tunnel mode**, where only the **VPN gateway** addresses appear on the outside. **B** is wrong: **tunnel mode** encapsulates and protects the **entire inner IP packet** (header and payload), not \u201conly the payload.\u201d **C** is false: **transport mode** does not inherently make **GRE** \u201cmore secure\u201d than **tunnel mode**; designs often use **IPsec tunnel mode** over **GRE**. **D** is wrong: in **transport mode**, the **Layer 4 header** is normally **inside the encrypted payload** (with **ESP**); what stays visible is the **IP header**, not full **L4** examination.",
            "choices": [
                "IPsec transport mode allows intermediate devices to see the final destination of the packet",
                "In IPsec tunnel mode, only the IP payload is encrypted",
                "IPsec transport mode increases GRE tunnel security over tunnel mode.",
                "IPsec transport mode does not encrypt the Layer 4 header, which allow full examination of the packet",
            ],
        },
        {
            "slug": "split-mac-realtime-functions-processed-ap",
            "title": "CCNA — Split-MAC real-time functions",
            "stem": "Where are the **real-time control functions** processed in a **split MAC** architecture?",
            "name": "splitmac1",
            "correct": "B",
            "explain": "Correct. B \u2014 In **split-MAC** (lightweight AP + **WLC**), **time-sensitive 802.11 MAC** work stays on the **individual AP** (beacons, probes, acknowledgments, and similar **real-time** radio/MAC tasks). The **WLC** centralizes **non\u2013real-time** control: **WLAN/SSID policy**, **security**, **roaming coordination**, and **RF profiles** over **CAPWAP**. **A** is where **management/control-plane** decisions are made, not the **real-time** MAC functions named here. **C** may host management UI or orchestration but is not where **on-air real-time MAC** runs. **D** is the **client**, not the infrastructure split point.",
            "choices": [
                "central WLC",
                "individual AP",
                "centralized cloud management platform",
                "client device",
            ],
        },
        {
            "slug": "authentication-biometric-physical-attribute",
            "title": "CCNA — Biometric authentication",
            "stem": "Which authentication method requires the user to provide a **physical attribute** to authenticate successfully?",
            "name": "authbio1",
            "correct": "D",
            "explain": "Correct. D \u2014 **Biometric** authentication uses a **physical** (inherence) factor\u2014**something you are**\u2014such as a **fingerprint**, **face**, or **iris** scan. **A** (**certificate**) is **something you have**. **B** (**password**) is **something you know**. **C** (**multifactor**) means **two or more factor types** combined; it is not itself the physical-attribute method.",
            "choices": [
                "certificate",
                "password",
                "multifactor",
                "biometric",
            ],
        },
        {
            "slug": "ansible-ssh-push-modules-to-nodes",
            "title": "CCNA — Ansible module transport",
            "stem": "Which protocol does **Ansible** use to **push modules** to nodes in a network?",
            "name": "ansssh1",
            "correct": "A",
            "explain": "Correct. A \u2014 **Ansible** connects to managed nodes over **SSH** (default for Linux and many network devices) and runs **modules** remotely; modules are copied and executed on the target, with results returned to the control node. **Kerberos** (**B**) can integrate with authentication systems but is not the transport Ansible uses to deliver modules. **SNMP** (**C**) is for **monitoring/management** queries, not Ansible automation execution. **Telnet** (**D**) is **cleartext** and is not Ansible\u2019s default module-delivery protocol.",
            "choices": [
                "SSH",
                "Kerberos",
                "SNMP",
                "Telnet",
            ],
        },
        {
            "slug": "dns-iterative-query-contact-servers",
            "title": "CCNA — Iterative DNS query",
            "stem": "Which function does an **iterative DNS query** serve in the **domain name resolution** process?",
            "name": "dnsiter1",
            "correct": "B",
            "explain": "Correct. B \u2014 In an **iterative** query, the **DNS client/resolver** queries a server; if that server does not have the answer, it returns a **referral** (for example to a parent zone), and the resolver **contacts the next DNS server** until the **authoritative** answer is found. **A** describes **DNSSEC/TLS** goals, not iterative resolution. **C** is wrong: resolvers do not query **all root servers** directly in normal iterative resolution. **D** describes **dynamic DNS updates**, not iterative lookups.",
            "choices": [
                "Encrypt communication automatically between DNS clients and servers.",
                "Allow a DNS client to contact several DNS servers until the correct information is found.",
                "Obtain information directly from all root DNS servers configured within the scope.",
                "Update records dynamically across multiple DNS servers at the same time.",
            ],
        },
        {
            "slug": "controller-based-vs-traditional-control-plane",
            "title": "CCNA — Controller-based vs traditional planes",
            "stem": "What is the difference between **controller-based networks** and **traditional networks** as they relate to **control-plane** and/or **data-plane** functions?",
            "name": "ctrltrad1",
            "correct": "A",
            "explain": "Correct. A \u2014 **Controller-based** (**SDN**) designs **centralize control-plane** functions (routing/policy decisions) on a **controller** that programs devices, while **data-plane forwarding** stays on switches and routers. **Traditional** networks **distribute control-plane** work (each device runs protocols and makes its own decisions locally). **B** reverses the model. **C** and **D** are wrong: **data-plane** forwarding is **distributed** in both architectures; controllers do not centralize packet forwarding.",
            "choices": [
                "Controller-based networks centralize all important control-plane functions, and traditional networks distribute control-plane functions.",
                "Traditional networks centralize all important control-plane functions, and controller-based networks distribute control-plane functions.",
                "Traditional networks centralize all important data-plane functions, and controller-based networks distribute data-plane functions.",
                "Controller-based networks centralize all important data-plane functions, and traditional networks distribute data-plane functions.",
            ],
        },
        {
            "slug": "ipsec-vpn-implementation-tunnel-mode-factor",
            "title": "CCNA — IPsec VPN implementation factor",
            "stem": "Which factor must be considered during the **implementation** of an **IPsec VPN**?",
            "name": "ipsecfac1",
            "correct": "D",
            "explain": "Correct. D \u2014 In **IPsec tunnel mode**, the **entire original IP datagram** (original **IP header** and **payload**) is encrypted and becomes the inner payload of a **new outer IP packet** with a new header. That is the usual **site-to-site VPN** model and affects addressing, routing, and what intermediates can see. **A** is wrong: in **transport mode**, the **original IP header** stays readable; the **Layer 4 header** is part of the **encrypted IP payload** (with **ESP**), not left open for inspection. **B** is false: **transport mode** does not make **GRE** more secure than **tunnel mode**; many designs use **IPsec tunnel mode** over **GRE**. **C** reverses the modes: **only the IP payload** is protected in **transport mode**, not **tunnel mode**.",
            "choices": [
                "IPsec transport mode leaves the Layer 4 header unencrypted for inspection.",
                "IPsec transport mode increases GRE tunnel security over tunnel mode.",
                "In IPsec tunnel mode, only the IP payload is encrypted.",
                "In IPsec tunnel mode, the entire original IP datagram is encrypted.",
            ],
        },
        {
            "slug": "wlc-inband-wireless-management-default-interface",
            "title": "CCNA — WLC in-band management default",
            "stem": "What is the default interface for **in-band wireless network management** on a **WLC**?",
            "name": "wlcmgmt2",
            "correct": "A",
            "explain": "Correct. A \u2014 The **management interface** (often labeled **wireless management** on exams) is the default **in-band** path for WLC **GUI/CLI** administration, **CAPWAP** to lightweight APs, and connectivity to services such as **AAA**. **C** (**service port**) and **D** (**out-of-band**) are for **dedicated OOB** management, not the default in-band path. **B** (**redundant port**) links **WLC high-availability** peers, not routine in-band wireless management.",
            "choices": [
                "wireless management",
                "redundant port",
                "service port",
                "out-of-band",
            ],
        },
        {
            "slug": "dna-center-lifecycle-management-patches-updates",
            "title": "CCNA — DNA Center lifecycle management",
            "stem": "Why choose **Cisco DNA Center** for **automated lifecycle management**?",
            "name": "dnalc1",
            "correct": "C",
            "explain": "Correct. C \u2014 **DNA Center** **lifecycle** and **Software Image Management (SWIM)** automate **image compliance**, **patch/update** distribution, and **upgrade** workflows across the inventory so deployments are **faster** and **more consistent** than manual per-device work. **A** overstates **zero-downtime** upgrades; many changes still need maintenance windows or controlled rollout. **B** (**software redundancy**) is a **network design** goal, not the primary lifecycle-management reason. **D** (**SSH to all nodes**) is not the defining benefit\u2014DNA Center uses **centralized APIs/workflows**, not opening SSH to every device as the main value.",
            "choices": [
                "to perform upgrades without service interruption",
                "to provide software redundancy in the network",
                "to provide fast and accurate deployment of patches and updates",
                "to allow SSH access to all nodes in the network",
            ],
        },
        {
            "slug": "ipsec-tunnel-mode-site-to-site-capabilities-choose-two",
            "title": "CCNA — IPsec tunnel mode capabilities (choose two)",
            "stem": "What are the two main capabilities of **tunnel mode** in **IPsec site-to-site VPNs**? (Choose two.)",
            "name": "ipsectun1",
            "choose_two": True,
            "correct": ["B", "E"],
            "explain": "Correct. B and E \u2014 **Tunnel mode** encrypts the **complete original IP packet** (original **IP header** and **payload/data**) and encapsulates it inside a **new outer IP packet** with a **new IP header** (VPN **gateway** addresses visible on the wire). **C** and **D** describe **transport mode** (only the **payload** is protected; the **original IP header** stays visible). **A** is incomplete: **ESP** can provide **integrity/authentication**, but the defining **tunnel-mode** pair here is **full-packet encryption** plus **new outer encapsulation**, not \u201cauthenticate only the data field\u201d as the main capability statement.",
            "choices": [
                "It authenticates the data field in original packet.",
                "It encrypts the complete IP packet with the data field.",
                "It secures only the data field in the packet.",
                "It transmits with the original packet header visible.",
                "It inserts a new IPsec header with new IP address.",
            ],
        },
        {
            "slug": "ai-network-traffic-analysis-anomaly-detection",
            "title": "CCNA — AI in traffic analysis",
            "stem": "How does **AI** contribute to **network traffic analysis**?",
            "name": "aitraffic1",
            "correct": "C",
            "explain": "Correct. C \u2014 **AI/ML** in network operations typically **learns baselines** from traffic and telemetry, then **flags anomalies** (unusual volumes, flows, or behavior) to support **security** and **assurance** workflows. **A** (**route mapping**) is not the primary CCNA framing for AI traffic analysis. **B** (**packet delivery speeds**) misstates the benefit\u2014AI does not directly accelerate wire-speed forwarding. **D** (**eliminates threats**) overstates the outcome; AI **assists detection and response**, it does not remove all threats by itself.",
            "choices": [
                "It simplifies traffic route mapping.",
                "It enhances data packet delivery speeds.",
                "It analyzes patterns for anomaly detection.",
                "It eliminates network threats.",
            ],
        },
        {
            "slug": "control-plane-exchanges-topology-information",
            "title": "CCNA — Control plane functionality",
            "stem": "What is a functionality of the **control plane** in the network?",
            "name": "cpfunc1",
            "correct": "B",
            "explain": "Correct. B \u2014 The **control plane** runs **routing protocols** and **exchanges topology** (reachability/path information) with neighbors to build the **routing table** and program forwarding. **A** (**CLI access**) is primarily **management-plane** administration. **C** (**FIB lookup**) and **D** (**forward to next hop**) are **data-plane** forwarding actions using tables the control plane populated.",
            "choices": [
                "It provides CLI access to the network device.",
                "It exchanges topology information with other routers.",
                "It looks up an egress interface in the forwarding information base.",
                "It forwards traffic to the next hop.",
            ],
        },
        {
            "slug": "rest-uri-identifies-target-resource",
            "title": "CCNA — REST URI purpose",
            "stem": "What is the purpose of the **URI string** in a **REST** request?",
            "name": "resturi1",
            "correct": "B",
            "explain": "Correct. B \u2014 The **URI** (path in the URL) **identifies the resource** on the target server (for example a device, interface, or configuration object). **A** describes the **HTTP method** (**PUT**, **PATCH**, **DELETE**) that specifies **how** a resource is modified. **C** relates to **response headers** such as **Content-Type** or encoding, not the URI. **D** describes the **request body/payload**, which is separate from the URI that names **which** resource is accessed.",
            "choices": [
                "to specify the way in which a remote resource is modified",
                "to identify a resource on a target server",
                "to respond with the data content encoding for a request",
                "to transport data or payload to a remote resource",
            ],
        },
        {
            "slug": "flexconnect-prefer-centralized-management-remote-offices",
            "title": "CCNA — When to prefer FlexConnect",
            "stem": "Under what condition would a **FlexConnect** wireless architecture be preferable over other architectural choices?",
            "name": "flexpref1",
            "correct": "C",
            "explain": "Correct. C \u2014 **FlexConnect** lets **branch/remote APs** stay under **centralized WLC management** (CAPWAP to a **central controller**) while supporting **local switching** and **WAN survivability**, so sites do **not** need a **dedicated WLC** at each office. **D** describes the opposite design (**local WLC per site**). **B** (**high-precision location**) typically favors **centralized** location services, not FlexConnect as the primary driver. **A** misstates WAN design: Cisco branch guidance treats **~300 ms** as a **maximum recommended latency** to the controller for many FlexConnect designs, not a reason to choose FlexConnect **because** latency will **exceed** 300 ms.",
            "choices": [
                "when the connection latency to several remote offices is anticipated to surpass 300 milliseconds",
                "when there is a need for high-precision location-based services at various remote offices",
                "when centralized management is needed for several remote offices that lack individual WLCs",
                "when each remote office necessitates its own local WLC for network management",
            ],
        },
        {
            "slug": "acl-services-add-tcp-dns-sequence-35-exhibit",
            "title": "CCNA — Services ACL: add TCP DNS (exhibit)",
            "stem": "This ACL allows client access only to **HTTP**, **HTTPS**, and **DNS over UDP**. A new administrator wants to add **TCP** access to the **DNS** service. Which configuration updates the ACL efficiently?",
            "name": "aclsvc1",
            "correct": "D",
            "mono": True,
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="CPE show ip access-list Services">
      <pre>CPE# show ip access-list Services
Extended IP access list Services
   10 permit tcp 10.0.0.0 0.255.255.255 any eq www
   20 permit tcp 10.0.0.0 0.255.255.255 any eq 443
   30 permit udp 10.0.0.0 0.255.255.255 host 198.51.100.11 eq domain
   40 deny ip any any log</pre>
    </div>""",
            "explain": "Correct. D \u2014 A **named extended ACL** can be edited in place with **sequence numbers**. **`35 permit tcp ... eq domain`** inserts the new ACE **before** sequence **40 deny**, matching the existing **UDP DNS** rule to **198.51.100.11**. **A** omits a sequence number, so IOS may append the line **after** the **deny** (ineffective). **B** and **C** use **`no ip access-list extended Services`**, which **removes the entire ACL** and is **not** the efficient edit; **C** also changes the **UDP** rule to **`any eq 53`**, altering existing policy.",
            "choices": [
                "ip access-list extended Services\n permit tcp 10.0.0.0 0.255.255.255 host 198.51.100.11 eq domain",
                "no ip access-list extended Services\nip access-list extended Services\n 30 permit tcp 10.0.0.0 0.255.255.255 host 198.51.100.11 eq domain",
                "no ip access-list extended Services\nip access-list extended Services\n permit udp 10.0.0.0 0.255.255.255 any eq 53\n permit tcp 10.0.0.0 0.255.255.255 host 198.51.100.11 eq domain\n deny ip any any log",
                "ip access-list extended Services\n 35 permit tcp 10.0.0.0 0.255.255.255 host 198.51.100.11 eq domain",
            ],
        },
        {
            "slug": "windows-ipconfig-remote-subnet-verify-gateway-exhibit",
            "title": "CCNA — Verify gateway first (ipconfig exhibit)",
            "stem": "The user has connectivity to devices on network **192.168.3.0/24** but cannot reach users on network **10.10.1.0/24**. What is the **first step** to verify connectivity?",
            "name": "ipcfgw1",
            "correct": "B",
            "prepend_html": """    <div class="exhibit-terminal-white" role="region" aria-label="Windows ipconfig output">
        <pre>C:\\Users\\ADMIN&gt;ipconfig

Windows IP Configuration

Ethernet adapter Ethernet:

   Physical Address. . . . . . . . . . : 04-42-1A-EE-AA-5E
   DHCP Enabled. . . . . . . . . . . . : Yes
   Autoconfiguration Enabled . . . . . : Yes
   Link-local IPv6 Address . . . . . . : fe80::8a79:bcde:34dc:c11e%35(Preferred)
   IPv4 Address. . . . . . . . . . . . : 192.168.3.20(Preferred)
   Subnet Mask . . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . . : 192.168.3.1
   DHCP Server . . . . . . . . . . . : 192.168.3.1
   DNS Servers . . . . . . . . . . . . : 10.10.1.254</pre>
      </div>""",
            "explain": "Correct. B \u2014 Local **192.168.3.0/24** connectivity works, so the NIC and mask look fine. Traffic to **10.10.1.0/24** is **off-subnet** and must go via the **default gateway** (**192.168.3.1**). The **first** check is **`ping 192.168.3.1`** (or equivalent) to confirm the gateway is reachable before DNS or remote hosts. **C** tests **DNS** (**10.10.1.254**); name resolution comes **after** you confirm Layer 3 routing to other subnets works. **A** (**internet reachable**) is too broad and does not isolate the **inter-subnet** path first.",
            "choices": [
                "Is the internet reachable?",
                "Is the default gateway reachable?",
                "Is the DNS server reachable?",
            ],
        },
        {
            "slug": "mitigate-sniffed-admin-password-mfa",
            "title": "CCNA — Mitigate sniffed admin password",
            "stem": "Which solution is appropriate when mitigating **password attacks** where the attacker was able to **sniff the clear-text password** of the **system administrator**?",
            "name": "sniffpwd1",
            "correct": "B",
            "explain": "Correct. B \u2014 **Multifactor authentication** from **two separate sources** (for example password plus OTP/token) means a **sniffed password alone** is not enough to log in. **A** (**NGFW** stateful inspection) does not stop **credential theft** on **cleartext** management protocols. **C** (**ACL** limiting **Telnet**) may reduce exposure but does not fix a **already captured** password; management should use **SSH/HTTPS**, not **Telnet**. **D** (**IPS** block lists) targets **known attack signatures**, not **stolen credentials** from sniffing.",
            "choices": [
                "next-generation firewall to keep stateful packet inspection",
                "multifactor authentication using two separate authentication sources",
                "ACL to restrict incoming Telnet sessions \u201cadmin\u201d accounts",
                "IPS with a block list of known attack vectors",
            ],
        },
        {
            "slug": "wlc-basic-config-create-wlan-bind-interface",
            "title": "CCNA — WLC basic config next step",
            "stem": "A network engineer starts to implement a new **wireless LAN** by configuring the **authentication server** and creating the **dynamic interface**. What must be performed **next** to complete the **basic configuration**?",
            "name": "wlcbasic1",
            "correct": "D",
            "explain": "Correct. D \u2014 After **AAA/RADIUS** and a **dynamic interface** (client VLAN/subnet mapping) exist, the next **basic** step is to **create the WLAN** (SSID/profile) and **bind** that WLAN to the **dynamic interface** so clients use the correct subnet and policies. **A** (**management interface** and IP) is normally configured **earlier** for WLC/AP reachability, not after dynamic interface as the immediate next step here. **B** (**AP high availability**) is an **advanced** design task, not the next basic WLAN build step. **C** (**Telnet** on management) is poor practice; secure management uses **SSH/HTTPS**, and it is not the step that completes WLAN service delivery.",
            "choices": [
                "Install the management interface and add the management IP.",
                "Configure high availability and redundancy for the access points.",
                "Enable Telnet and RADIUS access on the management interface.",
                "Create the new WLAN and bind the dynamic interface to it.",
            ],
        },
        {
            "slug": "ml-network-security-real-time-threat-detection",
            "title": "CCNA — ML for network security",
            "stem": "Which advantage does **machine learning** offer for **network security**?",
            "name": "mlsec1",
            "correct": "A",
            "explain": "Correct. A \u2014 **Machine learning** analyzes traffic and behavior **baselines** to spot **anomalies** and suspicious patterns faster, improving **real-time threat detection** in **IDS/IPS** and security analytics beyond static signatures alone. **B** (**firewall rule sets**) is mainly **policy administration** and automation workflows, not ML\u2019s defining security advantage on CCNA items. **C** (**password complexity**) is **identity/password policy**, not ML. **D** (**VPN access permissions**) is **authorization/policy** configuration, not the primary ML benefit.",
            "choices": [
                "It improves real-time threat detection.",
                "It manages firewall rule sets.",
                "It enforces password complexity requirements.",
                "It controls VPN access permissions.",
            ],
        },
        {
            "slug": "ap-hotspot-captive-portal-guest-access",
            "title": "CCNA — AP Hotspot captive portal",
            "stem": "Which **AP** feature provides a **captive portal** for users to **authenticate**, **register**, and **accept terms** before accessing the **internet**?",
            "name": "aphotspot1",
            "correct": "B",
            "explain": "Correct. B \u2014 **Hotspot** (guest/hotspot portal, often with **web authentication** or **CWA**) presents a **captive portal** where users **log in**, **self-register**, or **accept terms of use** before gaining **internet** access. **One-Click** (**A**) is simplified onboarding, not the full **register + accept terms** guest portal described here. **Enhanced Bluetooth** (**C**) is a **BLE**-related capability, not captive portal access control. **Whole Home** (**D**) is a **consumer/mesh** branding concept, not the enterprise **guest portal** feature.",
            "choices": [
                "One-Click",
                "Hotspot",
                "Enhanced Bluetooth",
                "Whole Home",
            ],
        },
        {
            "slug": "split-mac-definition-data-link-layer",
            "title": "CCNA — Split-MAC definition",
            "stem": "What does the term **\u201csplit MAC\u201d** refer to in a **wireless architecture**?",
            "name": "splitmacdef1",
            "correct": "A",
            "explain": "Correct. A \u2014 **Split-MAC** divides **Layer 2 (data link) MAC** functions between the **lightweight AP** and the **WLC**: the **AP** handles **real-time** on-air **802.11 MAC** work (beacons, probes, ACKs), while the **WLC** centralizes **non\u2013real-time** control (WLAN policy, security, roaming, RF) over **CAPWAP**. **B** misstates the model (control/management is separated from forwarding, not combined onto one device). **C** confuses **split-MAC** with **dual-band** radio operation. **D** is wrong: **one AP + one WLC** share functions; it is not **two APs** splitting roles.",
            "choices": [
                "divides data link layer functions between the AP and WLC",
                "combines the management and control functions from the data-forwarding functions",
                "uses different MAC addresses for 2.4 GHz and 5 GHz bands on the same AP",
                "leverages two APs to handle control and data traffic",
            ],
        },
        {
            "slug": "wlan-architectures-autonomous-cloud-splitmac-choose-two",
            "title": "CCNA — WLAN architecture facts (choose two)",
            "stem": "A network architect planning a new **Wi-Fi** network must decide between **autonomous**, **cloud-based**, and **split MAC** architectures. Which **two** facts should the architect consider? (Choose two.)",
            "name": "wlanarch1",
            "choose_two": True,
            "correct": ["A", "D"],
            "explain": "Correct. A and D \u2014 **Lightweight** (thin) APs are used in **split-MAC** (controller-based) designs; **autonomous** APs run the full WLAN stack locally, and many **cloud-based** offerings (for example **Meraki-style** management) use **autonomous** APs with **cloud** control rather than lightweight split-MAC APs. **All three** architectures still use **APs** as the wireless edge that connects **clients** to the **wired** network. **B** is wrong: **CAPWAP** is between **AP and controller**, not **AP and clients**, and it is not unique to cloud. **C** is wrong: **autonomous** does **not** require a **WLC**. **E** is wrong: **autonomous** APs are managed **locally** (CLI/GUI), not exclusively through **tunneling** protocols to a controller.",
            "choices": [
                "Lightweight access points are solely used by split MAC architectures.",
                "Cloud-based architectures uniquely use the CAPWAP protocol to communicate between access points and clients.",
                "Each of the three architectures must use WLCs to manage their access points.",
                "All three architectures use access points to manage the wireless devices connected to the wired infrastructure.",
                "Autonomous architectures exclusively use tunneling protocols to manage access points remotely.",
            ],
        },
        {
            "slug": "ap-bridge-mode-point-to-multipoint-hub",
            "title": "CCNA — AP bridge mode hub",
            "stem": "Which **AP mode** serves as the **primary hub** in a **point-to-multipoint** network topology?",
            "name": "apbridge1",
            "correct": "A",
            "explain": "Correct. A \u2014 In **bridge** mode, a **root bridge** AP connects to the **wired network** and acts as the **hub**; **non-root** bridge APs link to it in **point-to-multipoint** (and mesh) designs. **Local** (**D**) is standard **lightweight** client-serving mode with traffic to a **WLC**, not a wireless bridging hub. **FlexConnect** (**C**) is **branch local switching** with central WLC control. **SE-Connect** (**B**) is for **spectrum/sensor** style operation, not the bridging **root hub** role.",
            "choices": [
                "bridge",
                "SE-Connect",
                "FlexConnect",
                "local",
            ],
        },
        {
            "slug": "network-automation-reduce-downtime-templates-testing",
            "title": "CCNA — Automation reduces downtime",
            "stem": "How does **network automation** help **reduce network downtime**?",
            "name": "netautodt1",
            "correct": "B",
            "explain": "Correct. B \u2014 **Automation** uses **configuration templates**, validation, and **testing** in the change workflow so deployments are **repeatable** and less error-prone, which **raises the success rate** of changes and **reduces outages** from misconfiguration. **A** (**email** visibility) improves awareness but does not by itself prevent failed changes. **C** (**parallel** changes) can speed rollout but does not inherently reduce downtime risk without templates/testing. **D** overstates **intent-based** platforms: they help validate intent, but they do **not** guarantee **all** changes are checked for **every** possible outage before implementation.",
            "choices": [
                "Emails can be generated based on when a network admin performs a network change, which increases visibility.",
                "Configuration templates and testing can be built into implementation, which increases the success rate of a network change.",
                "Changes can be implemented in parallel across multiple devices at once, which increases the speed of the change rate.",
                "By using automation platforms with intent-based configuration, all changes are checked for possible outages before being implemented.",
            ],
        },
        {
            "slug": "snmp-traps-vs-polling-push-pull",
            "title": "CCNA — SNMP traps vs polling",
            "stem": "What is the difference between **SNMP traps** and **SNMP polling**?",
            "name": "snmptrap1",
            "correct": "A",
            "explain": "Correct. A \u2014 **SNMP traps** use a **push** model: the **agent** (network device) sends an **asynchronous** notification to the **NMS** when an event occurs. **SNMP polling** uses a **pull** model: the **NMS** (server) **initiates** **GET** requests on a schedule to query MIB objects. **B** reverses proactive/reactive: **polling** is often used for **ongoing** monitoring, while **traps** are **event-driven** alerts. **C** reverses who initiates each method. **D** misstates behavior: **polling** is typically **periodic** from the server; **traps** are **event-based**, not \u201cperiodic MIB updates\u201d from the device in the way described.",
            "choices": [
                "SNMP traps are initiated using a push model at the network device, and SNMP polling is initiated at the server.",
                "SNMP traps are used for proactive monitoring, and SNMP polling is used for reactive monitoring.",
                "SNMP traps are initiated by the network management system, and network devices initiate SNMP polling.",
                "SNMP traps send periodic updates via the MIB, and SNMP polling sends data on demand.",
            ],
        },
        {
            "slug": "syslog-level-7-debug-monitoring",
            "title": "CCNA — Syslog level 7 role",
            "stem": "What is the role of **syslog level 7** in **network device health monitoring**?",
            "name": "syslog71",
            "correct": "C",
            "explain": "Correct. C \u2014 On Cisco IOS, **level 7** is **debug**, the least urgent severity. It carries **verbose debug** output from **`debug`** commands used for **troubleshooting**, not routine health summaries. **A** describes **error** conditions (**level 3**). **B** describes **informational** operational messages (**level 6**). **D** describes **emergency** conditions (**level 0**), the most severe level.",
            "choices": [
                "It provides information about error conditions visible on the network device.",
                "It shares normal operational messages from the network equipment.",
                "It sends outputs from various debug commands on the device.",
                "It warns about emergency conditions on the network appliance.",
            ],
        },
        {
            "slug": "autonomous-ap-small-office-no-central-management",
            "title": "CCNA — Small office: autonomous AP",
            "stem": "Which architecture is best for **small offices** with **minimal wireless** needs and **no central management**?",
            "name": "wlanarchsm1",
            "correct": "C",
            "explain": "Correct. C \u2014 **Autonomous** (fat) **APs** run the full WLAN stack **locally** with **per-device** CLI/GUI setup\u2014no **WLC** or cloud controller required, which fits **small** sites with **minimal** Wi-Fi and **no** centralized management platform. **Split MAC** (**B**) depends on a **WLC** (central control). **Cloud-based** (**A**) uses **centralized cloud** management. **Mesh** (**D**) extends coverage over **wireless backhaul** and is not the default choice for a **simple small office** with **no** central management.",
            "choices": [
                "cloud-based AP",
                "split MAC",
                "autonomous AP",
                "mesh network",
            ],
        },
        {
            "slug": "dns-aaaa-ipv6-address-record",
            "title": "CCNA — DNS AAAA record",
            "stem": "What is a valid **IPv6 address** record in **DNS**?",
            "name": "dnsaaaa1",
            "correct": "C",
            "explain": "Correct. C \u2014 A **AAAA** record maps a **hostname** to an **IPv6 address** (128-bit), the IPv6 equivalent of an **A** record for **IPv4**. **A** (**A**) is **IPv4** only. **MX** (**B**) specifies a **mail exchanger** host for a domain. **CNAME** (**D**) is an **alias** to another DNS name, not a direct address record.",
            "choices": [
                "A",
                "MX",
                "AAAA",
                "CNAME",
            ],
        },
        {
            "slug": "wlc-aireos-gui-simultaneous-management-users-five",
            "title": "CCNA — AireOS GUI concurrent users",
            "stem": "What is the total number of users permitted to **simultaneously browse** the controller **management pages** when using the **AireOS GUI**?",
            "name": "wlcgui5",
            "correct": "B",
            "explain": "Correct. B \u2014 **AireOS** WLC administration allows up to **five** users at once to browse the controller **HTTP/HTTPS** management GUI to configure and monitor the controller and APs. **2**, **8**, and **9** are not the documented simultaneous **GUI** session limit (CLI **Telnet/SSH** also caps at **five** concurrent sessions on WLCs).",
            "choices": [
                "2",
                "5",
                "8",
                "9",
            ],
        },
        {
            "slug": "ssh-management-access-secured-inbound-purpose",
            "title": "CCNA — SSH management access purpose",
            "stem": "What is the **main purpose** of **SSH management access**?",
            "name": "sshmgmt1",
            "correct": "D",
            "explain": "Correct. D \u2014 **SSH** provides **encrypted**, authenticated **remote management** to the device\u2019s **inbound management** path (typically **VTY** lines), replacing **cleartext Telnet**. **A** is incomplete: SSH uses **usernames**, **passwords** or keys, and often **ip domain-name** for key generation\u2014not **username and domain name only**. **B** confuses **HTTPS** (web) with **SSH** (CLI shell). **C** lists legacy **cipher** options; supporting **DES/3DES** is not SSH\u2019s **main purpose**.",
            "choices": [
                "To validate management access with username and domain name only",
                "To allow passwords protected with HTTPS encryption to be sent",
                "To support DES 56-bit and 3DES (168-bit) ciphers",
                "To enable secured access to the inbound management interface",
            ],
        },
        {
            "slug": "automation-data-models-vendor-agnostic-complexity",
            "title": "CCNA — Automation data models",
            "stem": "How does **automation** leverage **data models** to reduce the **operational complexity** of a managed network?",
            "name": "autodm1",
            "correct": "B",
            "explain": "Correct. B \u2014 **Structured data models** (for example **YANG** with **NETCONF/RESTCONF** APIs) give a **common, machine-readable** way to configure and read device state, so controllers and tools can be more **vendor-agnostic** instead of scraping different CLIs per platform. **A** (**faster responses** on high-interface devices) may be a side effect but is not how **data models** mainly cut complexity. **C** (**traffic categorization/insights**) describes **analytics/assurance**, not model-driven automation. **D** (**SNMP polling**) is **traditional** monitoring, not the primary **data-model** automation path.",
            "choices": [
                "Reduces the response time for specific requests to devices with many interfaces",
                "Allows the controller to be vendor-agnostic",
                "Categorizes traffic and provides insights",
                "Streamlines monitoring using SNMP and other polling tools",
            ],
        },
        {
            "slug": "generative-ai-network-operations-synthetic-configs",
            "title": "CCNA — Generative AI in NetOps",
            "stem": "What is the function of **generative AI** in **network operations**?",
            "name": "genai1",
            "correct": "A",
            "explain": "Correct. A \u2014 **Generative AI** **produces new content** (for example suggested **configurations**, policies, scripts, or documentation) from prompts and training data, which can include **synthetic** or draft **network configurations** for review. **B** (**firmware deployment**) is **lifecycle automation** (for example **DNA Center SWIM**), not the defining **generative** role. **C** (**disable unused services**) is **hardening/compliance** work. **D** (**data storage optimization**) is outside the usual **NetOps** framing for generative AI on CCNA items.",
            "choices": [
                "It creates synthetic network configurations.",
                "It deploys network firmware updates.",
                "It disables unused services.",
                "It computes optimal data storage solutions.",
            ],
        },
        {
            "slug": "security-program-user-training-distribute-policies",
            "title": "CCNA — Security program: user training",
            "stem": "An organization developed new **security policies** and decided to **print** the policies and **distribute** them to all personnel so that employees **review and apply** the policies. Which element of a **security program** is the organization implementing?",
            "name": "secprog1",
            "correct": "B",
            "explain": "Correct. B \u2014 Distributing policies for employees to **read and follow** is **user training** / **security awareness** (educating personnel on expected behavior). **Asset identification** (**A**) inventories systems and data, not policy handouts. **Physical access control** (**C**) regulates **facility entry** (badges, locks). **Vulnerability control** (**D**) finds and remediates **weaknesses** (patching, scanning), not policy distribution.",
            "choices": [
                "Asset identification",
                "User training",
                "Physical access control",
                "Vulnerability control",
            ],
        },
        {
            "slug": "wlc-lag-8023ad-bundle-distribution-ports",
            "title": "CCNA — WLC LAG bundles DS ports",
            "stem": "Which feature, when used on a **WLC**, allows it to **bundle** its **distribution system ports** into one **802.3ad** group?",
            "name": "wlclag80231",
            "correct": "D",
            "explain": "Correct. D \u2014 **LAG** on a Cisco **WLC** aggregates **distribution system** ports into one logical **802.3ad** (**LACP**) bundle for **higher throughput** and **link redundancy**. **QinQ** (**A**) is **double VLAN tagging** on trunks. **ISL** (**B**) is a legacy **Cisco trunk encapsulation**. **PAgP** (**C**) is **Cisco switch** EtherChannel negotiation, not the **WLC** feature that bundles **distribution** ports.",
            "choices": [
                "QinQ",
                "ISL",
                "PAgP",
                "LAG",
            ],
        },
        {
            "slug": "wlan-ssid-maximum-length-32-characters",
            "title": "CCNA — SSID maximum length",
            "stem": "What is the **maximum length** of characters used in an **SSID**?",
            "name": "ssidlen1",
            "correct": "B",
            "explain": "Correct. B \u2014 **802.11** limits the **SSID** (network name) element to **32 octets** (bytes), which is **32 characters** for typical ASCII SSIDs. **16**, **48**, and **64** are not the IEEE maximum SSID length.",
            "choices": [
                "16",
                "32",
                "48",
                "64",
            ],
        },
        {
            "slug": "container-virtualization-os-level-description",
            "title": "CCNA — Container virtualization",
            "stem": "Which statement describes **virtualization on containers**?",
            "name": "contain1",
            "correct": "A",
            "explain": "Correct. A \u2014 **Containers** use **OS-level virtualization**: they share the **host OS kernel** and the host OS isolates **processes** with **namespaces** and controls **CPU/memory** with **cgroups**, without a full **guest OS** per container. **B** describes **Type 2** full **VM** emulation (multiple OS instances on one machine). **C** describes a **hypervisor** allocating resources to **VMs**. **D** describes **VMs** (guest OS and virtualized hardware), not lightweight **containers**.",
            "choices": [
                "It is a type of operating system virtualization that allows the host operating system to control the different CPU memory processes.",
                "It emulates a physical computer and enables multiple machines to run with many operating systems on a physical machine.",
                "It separates virtual machines from each other and allocates memory, processors, and storage to compute.",
                "It contains a guest operating system and virtual partition of hardware for OS and requires application libraries.",
            ],
        },
        {
            "slug": "hsrp-implement-redundancy-router-failure",
            "title": "CCNA — Why implement HSRP",
            "stem": "Why would a network administrator implement the **HSRP** protocol?",
            "name": "hsrpwhy1",
            "correct": "A",
            "explain": "Correct. A \u2014 **HSRP** is a **first-hop redundancy** protocol: routers share a **virtual default gateway** so if the **active** router fails, the **standby** assumes the **virtual IP/MAC** and hosts keep forwarding. **B** describes **VRRP** (open standard), not **Cisco-proprietary HSRP**. **C** mixes **GLBP-style load-balancing** with a shared VIP; **HSRP** is primarily **active/standby**, not load-sharing across gateways. **D** is wrong: clients use **one** virtual gateway IP, not multiple default gateways.",
            "choices": [
                "To provide network redundancy in the case of a router failure",
                "To use an open standard protocol that is configured on Cisco and third-party routers",
                "To allow hosts in a network to use the same default gateway virtual IP when load-balancing traffic",
                "To allow clients to be configured with multiple default gateway IPs",
            ],
        },
        {
            "slug": "etherchannel-add-member-po1-lacp-layer3-exhibit",
            "title": "CCNA — Add member to Po1 LACP (exhibit)",
            "stem": "A network engineer is adding another physical interface as a **new member** to the existing **Port-Channel1** bundle. Which **command set** must be configured on the **new interface** to complete the process?",
            "name": "poadd1",
            "correct": "B",
            "mono": True,
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="SW1 show etherchannel summary">
      <pre>SW1#show etherchannel summary
Flags:   D - down         P - in port-channel
         I - stand-alone  s - suspended
         H - Hot-standby (LACP only)
         R - Layer3       S - Layer2
         U - in use       f - failed to allocate aggregator
         u - unsuitable for bundling
         w - waiting to be aggregated
         d - default port
         A - formed by auto LAG

Number of channel-groups in use: 1
Number of aggregators: 2

Group  Port-channel  Protocol    Ports
------+-------------+-----------+-----------------------------------------------
1      Po1 (RU)        LACP       Et0/0(P)    Et0/1(P)</pre>
    </div>""",
            "explain": "Correct. B \u2014 **Po1 (RU)** shows a **Layer 3 (routed)** EtherChannel using **LACP**. A new member must match: **`no switchport`** (routed port) and **`channel-group 1 mode active`** to join the **LACP** bundle. **A** uses **`switchport mode trunk`** (Layer 2), which does not match **R**. **C** uses **`mode on`** (static EtherChannel), not **LACP**. **D** sets trunking but omits **`channel-group`**, so the port never joins **Po1**.",
            "choices": [
                "switchport mode trunk\nchannel-group 1 mode active",
                "no switchport\nchannel-group 1 mode active",
                "no switchport\nchannel-group 1 mode on",
                "switchport\nswitchport mode trunk",
            ],
        },
        {
            "slug": "ospf-route-10-30-0-1-administrative-distance-exhibit",
            "title": "CCNA — OSPF AD for 10.30.0.1 (exhibit)",
            "stem": "What is the **administrative distance** for the advertised prefix that includes the host IP address **10.30.0.1**?",
            "name": "ospfad1",
            "correct": "B",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="AA show ip route">
      <pre>AA#show ip route

   10.0.0.0/8 is variably subnetted, 6 subnets, 2 masks
C    10.0.0.0/30 is directly connected, GigabitEthernet0/0
L    10.0.0.1/32 is directly connected, GigabitEthernet0/0
C    10.10.0.0/30 is directly connected, GigabitEthernet0/1
L    10.10.0.1/32 is directly connected, GigabitEthernet0/1
O    10.20.0.0/30 [110/2] via 10.0.0.2, 00:00:40, GigabitEthernet0/0
O    10.30.0.0/30 [110/2] via 10.0.0.2, 00:00:40, GigabitEthernet0/0
   172.16.0.0/24 is subnetted, 1 subnets
S    172.16.10.0 [1/0] via 10.0.0.2
   192.168.10.0/24 is variably subnetted, 2 subnets, 2 masks
C    192.168.10.0/24 is directly connected, GigabitEthernet0/2
L    192.168.10.1/32 is directly connected, GigabitEthernet0/2
S    192.168.20.0/24 [1/0] via 192.168.10.2</pre>
    </div>""",
            "explain": "Correct. B \u2014 **10.30.0.1** lies in **10.30.0.0/30**, learned by **OSPF** (**O**): **`[110/2]`** means **administrative distance 110** and **metric 2**. **A** (**10.0.0.2**) is the **next-hop** address, not the AD. **C** (**30**) is the **prefix length** (/30), not the AD. **D** (**2**) is the **OSPF metric**, not the AD.",
            "choices": [
                "10.0.0.2",
                "110",
                "30",
                "2",
            ],
        },
        {
            "slug": "etherchannel-connect-switches-increase-bandwidth",
            "title": "CCNA — EtherChannel between switches",
            "stem": "What is the term used to describe a method of connecting multiple switches in a network to allow traffic to flow between them, typically used for larger networks to increase bandwidth?",
            "name": "ecswbw1",
            "correct": "C",
            "explain": "Correct. C \u2014 **EtherChannel** (link aggregation) bundles multiple parallel physical links between switches into one logical **port-channel**, increasing aggregate bandwidth and providing redundancy if a member link fails. **A** **LAG** is the generic IEEE 802.3ad concept; Cisco IOS campus switching exams usually name the Cisco implementation **EtherChannel**. **B** **Trunk** carries multiple VLANs on one link but does not by itself combine several physical links for higher throughput. **D** **Access** connects end devices to a single VLAN, not switch-to-switch aggregation.",
            "choices": [
                "LAG",
                "trunk",
                "EtherChannel",
                "access",
            ],
        },
        {
            "slug": "sdn-security-unified-control-policies",
            "title": "CCNA — SDN security vs traditional",
            "stem": "What is an advantage of using SDN versus traditional networking when it comes to security?",
            "name": "sdnsec1",
            "correct": "A",
            "explain": "Correct. A \u2014 **SDN** centralizes the **control plane** in a **controller**, so security policies (ACLs, segmentation, flow rules) can be defined once and applied **consistently** across infrastructure devices via **southbound** APIs instead of box-by-box CLI drift. **B** misstates the model: APIs exist, but the benefit is **centralized** policy orchestration, not configuring each device **locally** in isolation. **C** describes traditional **perimeter-centric** security, not an inherent SDN advantage. **D** describes **distributed** device negotiation, which is closer to traditional autonomous devices than SDN\u2019s centralized policy model.",
            "choices": [
                "It creates a unified control point making security policies consistent across all devices",
                "It exposes an API to configure locally per device for security policies",
                "Security is managed near the perimeter of the network with firewalls, VPNs, and IPS",
                "Devices communicate with each other to establish a security policy",
            ],
        },
        {
            "slug": "radius-tacacs-separate-auth-authorization",
            "title": "CCNA — RADIUS vs TACACS+",
            "stem": "What is a difference between RADIUS and TACACS+?",
            "name": "radtac1",
            "correct": "C",
            "explain": "Correct. C \u2014 **TACACS+** treats **authentication**, **authorization**, and **accounting** as **separate** exchanges with the server. **RADIUS** combines **authentication and authorization** in the access-request/access-accept flow (authorization attributes ride with the auth result). **A** overstates dial-only use: both can serve multiple access types; it is not the defining CCNA contrast. **B** reverses encryption: **RADIUS** encrypts primarily the **password** field; **TACACS+** encrypts the **entire payload** between client and server. **D** reverses command logging: **TACACS+** can record **per-command** administrator accounting on network devices; **RADIUS** is not the usual choice for detailed CLI command logs.",
            "choices": [
                "RADIUS is most appropriate for dial authentication, but TACACS+ can be used for multiple types of authentication",
                "TACACS+ encrypts only password information and RADIUS encrypts the entire payload",
                "TACACS+ separates authentication and authorization, and RADIUS merges them",
                "RADIUS logs all commands that are entered by the administrator, but TACACS+ logs only start, stop, and interim commands",
            ],
        },
        {
            "slug": "r1-forward-10-0-4-10-show-ip-route-exhibit",
            "title": "CCNA — R1 forward 10.0.4.10 (exhibit)",
            "stem": "How does router **R1** forward packets destined to **10.0.4.10**?",
            "name": "r1fwd410",
            "correct": "D",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="R1 show ip route">
      <pre>R1#show ip route
Gateway of last resort is 10.0.0.2 to network 0.0.0.0
10.0.0.0/8 is variably subnetted, 10 subnets, 3 masks
C       10.0.0.0/24 is directly connected, FastEthernet0/0
L       10.0.0.1/32 is directly connected, FastEthernet0/0
C       10.0.1.0/24 is directly connected, FastEthernet0/1
L       10.0.1.1/32 is directly connected, FastEthernet0/1
C       10.0.2.0/24 is directly connected, FastEthernet1/0
L       10.0.2.1/32 is directly connected, FastEthernet1/0
C       10.0.3.0/24 is directly connected, FastEthernet1/1
L       10.0.3.1/32 is directly connected, GigabitEthernet1/l
O       10.0.4.0/29 [110/2] via 10.0.4.2, 00:00:03, GigabitEthernet1/1
S       10.1.0.0/16 [1/0] via 10.0.3.2
S       10.1.3.0/24 [1/0] via 10.0.3.2
S*      0.0.0.0/0 [1/0] via 10.0.0.2</pre>
    </div>""",
            "explain": "Correct. D \u2014 **10.0.4.10** is **not** inside **10.0.4.0/29** (that block is **10.0.4.0\u201310.0.4.7**; usable hosts are typically **.1\u2013.6**). No other route in the table matches **10.0.4.10**, so **R1** uses the **default static route** **S* 0.0.0.0/0** via **10.0.0.2** (also the **gateway of last resort**). **A** (**10.0.4.2**) applies only to destinations in **10.0.4.0/29**, such as **10.0.4.6**. **B** names **FastEthernet1/1**; the OSPF route exits **GigabitEthernet1/1**, and that route does not match **.10** anyway. **C** (**FastEthernet0/1**) is the connected **10.0.1.0/24** link, not a match for **10.0.4.10**.",
            "choices": [
                "via 10.0.4.2",
                "via FastEthernet1/1",
                "via FastEthernet0/1",
                "via 10.0.0.2",
            ],
        },
        {
            "slug": "aaa-operations-identification-services-access-control",
            "title": "CCNA — AAA operations compared",
            "stem": "How do **AAA** operations compare regarding **user identification**, **user services**, and **access control**?",
            "name": "aaaops1",
            "correct": "B",
            "explain": "Correct. B \u2014 **Authentication** verifies **identity** (\u201cwho are you?\u201d). **Authorization** enforces **access control** (what the user may do). **Accounting** **tracks user services** and activity (session records, usage, billing support). **A** swaps roles: **authorization** does access control, but **authentication** does not track services (**accounting** does). **C** correctly assigns accounting but wrongly gives **authentication** access control. **D** reverses **authorization** and **authentication**.",
            "choices": [
                "Authorization provides access control and authentication tracks user services",
                "Authentication identifies users and accounting tracks user services",
                "Accounting tracks user services, and authentication provides access control",
                "Authorization identifies users and authentication provides access control",
            ],
        },
        {
            "slug": "r1-same-prefix-lowest-ad-route-installed",
            "title": "CCNA — Same prefix: lowest AD wins",
            "stem": "**R1** has learned route **10.10.10.0/24** via numerous routing protocols. Which route is installed?",
            "name": "r1ad1",
            "correct": "D",
            "explain": "Correct. D \u2014 When several routes match the **same prefix and mask**, the router installs the one with the **lowest administrative distance** (trustworthiness of the source). **Metrics/cost** (**A**) break ties only among routes of the **same** protocol and **equal** AD. **Next-hop IP** (**B**) is not used for best-path selection. **Shortest prefix length** (**C**) applies when destinations differ; here every candidate is **10.10.10.0/24**.",
            "choices": [
                "route with the lowest cost",
                "route with the next hop that has the highest IP",
                "route with the shortest prefix length",
                "route with the lowest administrative distance",
            ],
        },
        {
            "slug": "dai-trust-fa01-router-connected-device",
            "title": "CCNA — DAI trusted uplink device",
            "stem": "If the network environment is operating normally, which type of device must be connected to interface **FastEthernet 0/1**?",
            "name": "daitrust1",
            "correct": "C",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="Switch DAI configuration">
      <pre>ip arp inspection vlan 2-10
interface fastethernet 0/1
 ip arp inspection trust</pre>
    </div>""",
            "explain": "Correct. C \u2014 **Dynamic ARP Inspection (DAI)** treats access ports as **untrusted** by default. **`ip arp inspection trust`** on **FastEthernet0/1** marks the **uplink** toward infrastructure (typically a **router** or distribution switch) where ARP and DHCP server/relay traffic should not be dropped. **A** (**DHCP client**) and **D** (**PC**) are end hosts and belong on **untrusted** access ports. **B** (**access point**) is not the usual trusted DAI uplink in this design.",
            "choices": [
                "DHCP client",
                "access point",
                "router",
                "PC",
            ],
        },
        {
            "slug": "wlc-wpa2-psk-minimum-passphrase-characters",
            "title": "CCNA — WPA2-PSK minimum passphrase",
            "stem": "When a **WPA2-PSK** WLAN is configured in the **Wireless LAN Controller**, what is the **minimum** number of characters that is required for the passphrase?",
            "name": "wpa2min1",
            "correct": "B",
            "explain": "Correct. B \u2014 **WPA2-PSK** passphrases on a Cisco **WLC** must be **8\u201363 ASCII characters** (or **64 hex digits** for a raw PSK). The **minimum** is **8** characters per **802.11i** / WPA2 requirements. **A** (**6**) is too short and aligns with legacy **WEP** key sizes, not WPA2-PSK. **C** (**12**) and **D** (**18**) exceed the required minimum (though longer passphrases improve security).",
            "choices": [
                "6",
                "8",
                "12",
                "18",
            ],
        },
        {
            "slug": "office-ports-security-shutdown-8021x-choose-two",
            "title": "CCNA — Secure office-facing ports (choose two)",
            "stem": "What are two recommendations for protecting network ports from being exploited when located in an office space outside of an **IT closet**? (Choose two)",
            "name": "offport1",
            "choose_two": True,
            "correct": ["A", "C"],
            "explain": "Correct. A and C \u2014 **Shut down unused ports** (or place them in a restricted/black-hole VLAN) so anyone who plugs into an open jack cannot gain access. **Port-based authentication** (**802.1X**) requires valid credentials or certificates before the switch forwards traffic. **B** (**PortFast**) speeds **STP** convergence on access ports; it is not a physical-security control and can be risky on ports that might see switches. **D** (**fixed speed**) aids link stability, not unauthorized access. **E** (**static ARP**) does not scale on access ports and is not standard port-hardening practice (**DAI** uses DHCP snooping bindings, not manual static ARP per desk).",
            "choices": [
                "shut down unused ports",
                "enable the PortFast feature on ports",
                "implement port-based authentication",
                "configure ports to a fixed speed",
                "configure static ARP entries",
            ],
        },
        {
            "slug": "network-monitoring-highest-security-snmpv3",
            "title": "CCNA — Secure network monitoring (SNMPv3)",
            "stem": "Which technology must be implemented to configure **network device monitoring** with the **highest security**?",
            "name": "snmpsec1",
            "correct": "A",
            "explain": "Correct. A \u2014 **SNMPv3** provides **authentication** and **encryption (privacy)** for management traffic, replacing cleartext **community strings** used in **SNMPv1/v2c**. **B** (**IP SLA**) measures **performance/availability** (delay, loss, jitter); it is not the primary secure monitoring protocol. **C** (**NetFlow**) exports **traffic statistics** for analysis; security depends on transport design but it is not the SNMP management security upgrade. **D** (**syslog**) forwards **logs**; classic syslog is often **UDP** and **unencrypted** unless separately secured.",
            "choices": [
                "SNMPv3",
                "IP SLA",
                "NetFlow",
                "syslog",
            ],
        },
        {
            "slug": "ipv6-multicast-address-block-ff00-12",
            "title": "CCNA — IPv6 multicast address block",
            "stem": "Which **IPv6 address block** forwards packets to a **multicast** address rather than a **unicast** address?",
            "name": "ipv6mcast1",
            "correct": "D",
            "explain": "Correct. D \u2014 **FF00::/12** is the **IPv6 multicast** range (addresses begin with **ff**). Multicast delivers one packet to a **group** of receivers. **A** (**2000::/3**) is **global unicast**. **B** (**FC00::/7**) is **unique local unicast** (ULA). **C** (**FE80::/10**) is **link-local unicast**, used on a single link (for example **Neighbor Discovery**), not multicast.",
            "choices": [
                "2000::/3",
                "FC00::/7",
                "FE80::/10",
                "FF00::/12",
            ],
        },
        {
            "slug": "r1-192-168-12-24-isis-ospf-rip-eigrp-installed",
            "title": "CCNA — AD: EIGRP vs OSPF vs IS-IS vs RIP",
            "stem": "**R1** has learned route **192.168.12.0/24** via **IS-IS**, **OSPF**, **RIP**, and **Internal EIGRP**. Under normal operating conditions, which routing protocol is installed in the routing table?",
            "name": "r1ad121",
            "correct": "C",
            "explain": "Correct. C \u2014 For the **same prefix and mask**, the router installs the route with the **lowest administrative distance**. Default Cisco values: **Internal EIGRP 90**, **OSPF 110**, **IS-IS 115**, **RIP 120** \u2192 **EIGRP** wins. **A** (**IS-IS**) and **B** (**RIP**) have higher ADs. **D** (**OSPF**) is preferred over IS-IS and RIP but loses to internal EIGRP (**90** vs **110**).",
            "choices": [
                "IS-IS",
                "RIP",
                "Internal EIGRP",
                "OSPF",
            ],
        },
        {
            "slug": "r1-show-ip-route-internal-eigrp-prefix-exhibit",
            "title": "CCNA — Internal EIGRP prefix (exhibit)",
            "stem": "Which prefix did router **R1** learn from **internal EIGRP**?",
            "name": "r1eigrpd1",
            "correct": "C",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="R1 show ip route">
      <pre>R1# show ip route | begin gateway
Gateway of last resort is not set

     172.16.0.0/16 is variably subnetted, 3 subnets, 2 masks
C       172.16.1.0/24 is directly connected, FastEthernet0/0
L       172.16.1.3/32 is directly connected, FastEthernet0/0
EX      172.16.2.0/24 [170/2] via 207.165.200.250, 00:00:25, Serial0/0/0
O       192.168.1.0/24 [110/84437] via 207.165.200.254, 00:00:17, Serial0/0/1
D       192.168.2.0/24 [90/184437] via 207.165.200.254, 00:00:15, Serial0/0/1
E1      192.168.3.0/24 [110/1851437] via 207.165.200.254, 00:00:19, Serial0/0/1

     207.165.200.0/24 is variably subnetted, 4 subnets, 2 masks
C       207.165.200.248/30 is directly connected, Serial0/0/0
L       207.165.200.249/32 is directly connected, Serial0/0/0
C       207.165.200.252/30 is directly connected, Serial0/0/1
L       207.165.200.253/32 is directly connected, Serial0/0/1</pre>
    </div>""",
            "explain": "Correct. C \u2014 **Internal EIGRP** routes are marked **D** in **`show ip route`**. **D 192.168.2.0/24 [90/184437]** is the internal EIGRP entry (**AD 90**). **A** (**O**) is **OSPF**. **B** (**E1**) is **OSPF external type 1**, not EIGRP. **D** (**172.16.1.0/24**) is **connected** (**C**), not learned by a routing protocol. **EX** on **172.16.2.0/24** is **external EIGRP** (**AD 170**), distinct from internal **D**.",
            "choices": [
                "192.168.1.0/24",
                "192.168.3.0/24",
                "192.168.2.0/24",
                "172.16.1.0/24",
            ],
        },
        {
            "slug": "nat-pool-10-10-0-0-source-three-global-addresses",
            "title": "CCNA — NAT pool for 10.10.0.0/24",
            "stem": "An engineer is configuring **NAT** to translate the **source** subnet **10.10.0.0/24** to any one of three addresses: **192.168.3.1**, **192.168.3.2**, or **192.168.3.3**. Which configuration should be used?",
            "name": "natpool1",
            "correct": "C",
            "mono": True,
            "explain": "Correct. C \u2014 **Dynamic source NAT** uses **`ip nat inside source list 1 pool mypool`**, a standard ACL **`access-list 1 permit 10.10.0.0 0.0.0.255`** (wildcard for /24), **`ip nat pool mypool 192.168.3.1 192.168.3.3`**, and **`ip nat inside`** / **`ip nat outside`** on the correct interfaces. **A** misuses **`route-map`** syntax and **`ip nat outside destination`**, which is **destination NAT**, not translating an inside source subnet. **B** repeats the wrong **`outside destination`** form despite a valid ACL. **D** matches **C** structurally but the ACL wildcard **`0.0.0.254`** does not represent **10.10.0.0/24**.",
            "choices": [
                "enable\nconfigure terminal\nip nat pool mypool 192.168.3.1 192.168.3.3 prefix-length 30\nroute-map permit 10.10.0.0 255.255.255.0\nip nat outside destination list 1 pool mypool\ninterface g1/1\n ip nat inside\ninterface g1/2\n ip nat outside",
                "enable\nconfigure terminal\nip nat pool mypool 192.168.3.1 192.168.3.3 prefix-length 30\naccess-list 1 permit 10.10.0.0 0.0.0.255\nip nat outside destination list 1 pool mypool\ninterface g1/1\n ip nat inside\ninterface g1/2\n ip nat outside",
                "enable\nconfigure terminal\nip nat pool mypool 192.168.3.1 192.168.3.3 prefix-length 30\naccess-list 1 permit 10.10.0.0 0.0.0.255\nip nat inside source list 1 pool mypool\ninterface g1/1\n ip nat inside\ninterface g1/2\n ip nat outside",
                "enable\nconfigure terminal\nip nat pool mypool 192.168.3.1 192.168.3.3 prefix-length 30\naccess-list 1 permit 10.10.0.0 0.0.0.254\nip nat inside source list 1 pool mypool\ninterface g1/1\n ip nat inside\ninterface g1/2\n ip nat outside",
            ],
        },
        {
            "slug": "hsrp-first-hop-redundancy-virtual-ip-mac",
            "title": "CCNA — How HSRP provides FHRP",
            "stem": "How does **HSRP** provide **first hop redundancy**?",
            "name": "hsrpfhr1",
            "correct": "D",
            "explain": "Correct. D \u2014 **HSRP** routers in a group share a **virtual IP address** and **virtual MAC** that hosts use as their **default gateway**. The **active** router forwards traffic for that VIP; if it fails, the **standby** assumes the role so the LAN\u2019s first hop stays available. **A** describes **ECMP/load balancing** in the routing table, not HSRP. **B** describes **Layer 2 flooding**, not gateway redundancy. **C** describes **per-packet load sharing across routed paths**, not an FHRP virtual gateway.",
            "choices": [
                "It load-balances traffic by assigning the same metric value to more than one route to the same destination in the IP routing table",
                "It load-balances Layer 2 traffic along the path by flooding traffic out all interfaces configured with the same VLAN",
                "It forwards multiple packets to the same destination over different routed links and data path",
                "It uses a shared virtual MAC and a virtual IP address to a group of routers that serve as the default gateway for hosts on a LAN",
            ],
        },
        {
            "slug": "tftp-function-ios-image-firmware-upgrade",
            "title": "CCNA — TFTP in network operations",
            "stem": "What is a function of **TFTP** in network operations?",
            "name": "tftpfn1",
            "correct": "B",
            "explain": "Correct. B \u2014 **TFTP** (UDP port **69**) is commonly used to **copy Cisco IOS images** (and sometimes startup configs) between a **TFTP server** and a router or switch during **firmware upgrades** or recovery (**`copy tftp:`** operations). **A** may occur in practice, but \u201con a congested link\u201d is not TFTP\u2019s defining role, and TFTP has no built-in congestion control. **C** is wrong: TFTP does **not** use **username/password** authentication (**FTP/SCP/SFTP** do). **D** describes local **`copy`** between router file systems (for example **flash** to **flash**), not TFTP\u2019s client/server transfer over the network.",
            "choices": [
                "transfers a configuration files from a server to a router on a congested link",
                "transfers IOS images from a server to a router for firmware upgrades",
                "transfers a backup configuration file from a server to a switch using a username and password",
                "transfers files between file systems on a router",
            ],
        },
        {
            "slug": "default-gateway-ad-static-route-exhibit",
            "title": "CCNA — Default gateway AD (exhibit)",
            "stem": "What is the value of the **administrative distance** for the **default gateway**?",
            "name": "defgwad1",
            "correct": "C",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="Router show ip route">
      <pre>Router#show ip route

Gateway of last resort is 172.17.0.2 to network 0.0.0.0

S*    0.0.0.0/0 [1/0] via 172.17.0.2
10.0.0.0/8 is variably subnetted, 412 subnets, 10 masks
O E2  10.0.0.0/16 [110/10] via 10.2.24.1, 7w0d, Vlan82
O     10.2.17.0/24 [110/6] via 10.2.24.1, 6w4d, vlan82
O     10.2.17.0/24 [110/6] via 10.2.24.1, 6w4d, vlan82
O     10.2.23.0/24 [110/6] via 10.2.24.1, 7w0d, vlan82
--output suppressed--
C     10.173.5.0/24 is directly connected, vlan283
L     10.173.5.2/32 is directly connected, vlan283</pre>
    </div>""",
            "explain": "Correct. C \u2014 The **gateway of last resort** is **172.17.0.2** via **`S* 0.0.0.0/0 [1/0]`**. In **`[AD/metric]`** format, the **administrative distance is 1** (default for a **static** default route). **0** (**B**) is the **metric** on that line, not the AD. **110** (**A**) is **OSPF\u2019s** AD on routes such as **`O E2 10.0.0.0/16 [110/10]`**. **10** (**D**) is the **OSPF metric** (second value in **[110/10]**), not the default route\u2019s AD.",
            "choices": [
                "110",
                "0",
                "1",
                "10",
            ],
        },
        {
            "slug": "wlc-encrypted-mobility-tunnel-default-condition",
            "title": "CCNA — Encrypted mobility tunnel condition",
            "stem": "Which **default condition** must be considered when an **encrypted mobility tunnel** is used between two Cisco **WLCs**?",
            "name": "encmob1",
            "correct": "D",
            "explain": "Correct. D \u2014 **Encrypted mobility** between WLCs requires **mobility encryption** to be enabled so **control** and **data** traffic on the inter-controller tunnel are protected (CAPWAP **DTLS** on mobility ports such as **UDP 16666/16667** in current releases). The feature must be enabled on **all mobility peers**, and controllers may **reboot** when it is turned on. **A** is wrong: **EoIP** carries **unencrypted** mobility data by default; when encryption is enabled, the controller uses **UDP 16667** instead of **EoIP**. **B** (**TCP 443**, **UDP 21**) does not describe WLC mobility encryption. **C** (**IPsec**) is not the encapsulation Cisco documents for encrypted mobility tunnels (**DTLS over CAPWAP** is).",
            "choices": [
                "The tunnel uses the EoIP protocol to transmit data traffic.",
                "TCP port 443 and UDP 21 are used.",
                "The tunnel uses the IPsec protocol for encapsulation.",
                "Control and data traffic encryption are enabled.",
            ],
        },
        {
            "slug": "api-keys-rate-limiting-identify-clients",
            "title": "CCNA — API keys and rate limiting",
            "stem": "Why are **API keys** used to enforce **rate limiting**?",
            "name": "apikey1",
            "correct": "A",
            "explain": "Correct. A \u2014 An **API key** identifies each **client/application** so the platform can **meter requests**, apply **per-client quotas**, and enforce **rate limits** based on observed **usage patterns**. **B** is wrong: **encryption** for data in transit is provided by mechanisms such as **HTTPS/TLS**, not the rate-limiting role of API keys. **C** describes **token expiration** or **scoped credentials**, not why keys enable throttling. **D** is wrong: **geolocation** may be logged separately but is not the primary reason API keys support rate limiting.",
            "choices": [
                "to uniquely identify clients to monitor their usage patterns",
                "to encrypt data to prevent excessive usage",
                "to contain embedded permissions that automatically expire",
                "to track the geographical location of each request",
            ],
        },
        {
            "slug": "wan-point-to-point-topology-behaviors-choose-two",
            "title": "CCNA — Point-to-point WAN (choose two)",
            "stem": "What are two behaviors of a **point-to-point** **WAN** topology? (Choose two)",
            "name": "p2pwan1",
            "choose_two": True,
            "correct": ["B", "C"],
            "explain": "Correct. B and C \u2014 A **point-to-point** WAN link is a **dedicated** circuit between **two** sites, typically carried over a **single line** (for example leased line, private fiber, or a point-to-point serial/MPLS pseudowire). **A** describes a **hub** model (one router forwarding between many sites), not the defining behavior of each P2P link. **D** (**redundancy**) requires **multiple paths**; a single P2P link is a **single point of failure**. **E** describes a **full mesh** (every router connected to every other), not the usual meaning of individual **point-to-point** WAN segments in a partial or hub-and-spoke design.",
            "choices": [
                "It uses a single router to route traffic between sites.",
                "It leverages a dedicated connection.",
                "It connects remote networks through a single line.",
                "It delivers redundancy between the central office and branch offices.",
                "It provides direct connections between each router in the topology.",
            ],
        },
        {
            "slug": "switch-excessive-collisions-syslog-16-retries",
            "title": "CCNA — Excessive collisions syslog",
            "stem": "What is occurring on this switch?",
            "name": "excoll1",
            "correct": "B",
            "prepend_html": """    <div class="exhibit-router-cli" role="region" aria-label="Excessive collisions syslog messages">
      <pre>AMDP2_FE-5-COLL: AMDP2/FE 0/0/ [DEC] , Excessive collisions, TDR=[DEC] , TRC=[DEC]
%DEC21140-5-COLL: [chars] excessive collisions
%ILACC-5-COLL: Unit [DEC], excessive collisions. TDR=[DEC]
%LANCE—5-COLL: Unit [DEC], excessive collisions. TDR=[DEC]
%PQUICC-5-COLL: Unit [DEC], excessive collisions. Retry limit [DEC] exceeded
%PQUICC_ETHER-5-COLL: Unit [DEC], excessive collisions. Retry limit [DEC] exceeded</pre>
    </div>""",
            "explain": "Correct. B \u2014 **Excessive collisions** means a port could not successfully transmit after the Ethernet **retry limit** (typically **16** attempts in half-duplex). The frame is **dropped** and the switch logs **%*-5-COLL** (often with **Retry limit exceeded**). Common causes include **duplex mismatch** or a faulty NIC/cable. **A** (**runts**, frames **&lt; 64** bytes) produces different counters/syslog. **C** (**transmit buffer** overload) is **output queue/buffer failure**, not collision retry exhaustion. **D** (**giants** **&gt; 1518** bytes) is a separate **oversize frame** error.",
            "choices": [
                "A high number of frames smaller than 64 bytes are received.",
                "Frames are dropped after 16 failed transmission attempts.",
                "The internal transmit buffer is overloaded.",
                "An excessive number of frames greater than 1518 bytes are received.",
            ],
        },
        {
            "slug": "virtualization-multiple-os-single-physical-server",
            "title": "CCNA — Virtualization on one server",
            "stem": "Which technology allows **multiple operating systems** to run on a **single physical server**?",
            "name": "virtmulti1",
            "correct": "B",
            "explain": "Correct. B \u2014 **Virtualization** (a **hypervisor**) runs multiple **virtual machines**, each with its own **guest operating system**, on one physical host. **A** (**cloud computing**) is a service/delivery model that may use virtualization but does not by itself define multiple OS instances on one server. **C** (**application hosting**) describes running apps on a platform, not multiple full OSs. **D** (**containers**) share the **host OS kernel** and isolate **processes**; they do not typically run separate **full guest operating systems** the way **VMs** do.",
            "choices": [
                "cloud computing",
                "virtualization",
                "application hosting",
                "containers",
            ],
        },
        {
            "slug": "mfa-otp-login-name-smartphone",
            "title": "CCNA — MFA with OTP and smartphone",
            "stem": "Which security element uses a combination of **one-time passwords**, a **login name**, and a **personal smartphone**?",
            "name": "mfaotp1",
            "correct": "B",
            "explain": "Correct. B \u2014 **Multifactor authentication (MFA)** combines **different factor types**. A **login name** with a password/PIN is typically **something you know**; **one-time passwords** delivered to or generated on a **personal smartphone** (authenticator app or SMS OTP) are **something you have**. **A** (**software-defined segmentation**) enforces **network/policy isolation**, not user login factors. **C** (**attribute-based access control**) grants access from **attributes/policies**, not this OTP-plus-phone pattern. **D** (**rule-based access control**) uses **static rules** (for example ACLs), not MFA.",
            "choices": [
                "software-defined segmentation",
                "multifactor authentication",
                "attribute-based access control",
                "rule-based access control",
            ],
        },
        {
            "slug": "predictive-ai-load-balancing-traffic-spikes",
            "title": "CCNA — Predictive AI and load balancing",
            "stem": "Which role do **predictive AI** models play in **network load balancing**?",
            "name": "predai1",
            "correct": "A",
            "explain": "Correct. A \u2014 **Predictive AI** uses historical and real-time telemetry to **forecast demand** and **anticipate traffic spikes**, so load balancers can **adjust distribution** before congestion affects users. **B** (**IP address assignment**) is **DHCP/IPAM**, not AI load balancing. **C** (**cabling types**) is physical design/planning, unrelated to predictive analytics. **D** is wrong: predictive models go beyond **only monitoring** past volumes\u2014they **project future load** to guide proactive balancing.",
            "choices": [
                "They anticipate future traffic spikes.",
                "They assign IP addresses to devices.",
                "They select correct cabling types for deployment.",
                "They solely monitor historical traffic volumes.",
            ],
        },
        {
            "slug": "ap-bridge-mode-connect-campus-building-segments",
            "title": "CCNA — AP bridge between buildings",
            "stem": "Which **AP mode** wirelessly connects two separate **network segments** each set up within a **different campus building**?",
            "name": "apbrbld1",
            "correct": "C",
            "explain": "Correct. C \u2014 **Bridge** mode turns APs into **wireless bridges** that link **wired LAN segments** (for example **root** and **non-root** bridge roles) across buildings where running cable is impractical. Clients do not associate for access in pure bridge deployments the way they do in **local** mode. **A** (**mesh**) interconnects APs for **coverage/backhaul** meshes, not the classic **two-segment** building extension use case. **B** (**local**) serves **WLAN clients** through a **WLC**, not bridging two building LANs. **D** (**point-to-point**) describes a **topology** within **bridge** mode, not the AP **mode** name tested here.",
            "choices": [
                "mesh",
                "local",
                "bridge",
                "point-to-point",
            ],
        },
        {
            "slug": "vrf-logical-layer3-separation-physical-equipment",
            "title": "CCNA — VRF Layer 3 separation",
            "stem": "Which technology allows for **logical Layer 3 separation** on **physical network equipment**?",
            "name": "vrfsep1",
            "correct": "B",
            "explain": "Correct. B \u2014 **Virtual Route Forwarding (VRF)** creates multiple **independent Layer 3 routing tables** (routing instances) on the **same physical router or switch**, so traffic and prefixes in one VRF stay separated from another (for example tenant, department, or management vs production). **A** (**Virtual Switch System**) pairs switches for **Layer 2** redundancy/control-plane simplification, not VRF-style L3 separation. **C** (**IPsec transport mode**) encrypts **IP payloads** between peers; it does not provide multiple **logical L3 domains** on one box. **D** (**TDM**) multiplexes channels in time on **physical circuits** (legacy WAN), not logical L3 separation on modern routers.",
            "choices": [
                "Virtual Switch System",
                "Virtual Route Forwarding",
                "IPsec Transport Mode",
                "Time Division Multiplexer",
            ],
        },
        {
            "slug": "syslog-trap-informational-exclude-debug-flood",
            "title": "CCNA — Exclude debug from syslog trap",
            "stem": "Which action prevents **debug** messages from being sent via **syslog** while allowing other messages when an abnormally high number of **syslog** messages are generated by a device with the **debug** process turned on?",
            "name": "slogdbg1",
            "correct": "D",
            "explain": "Correct. D \u2014 **`logging trap informational`** (severity **6**) sends messages at level **6 and lower** (more urgent) to the **syslog server**, but **not** **debug** (**7**). That stops **debug floods** from filling the remote syslog collector while **warnings, errors, and informational** events still go out. **A** (**ACL**) is not the standard IOS method to filter **syslog trap** severity. **B** (**no logging monitor**) affects the **monitor** (terminal) destination, not the **trap** level to syslog. **C** (**console logging**) affects the **console** only, not syslog-server **trap** filtering.",
            "choices": [
                "Use an access list to filter out the syslog messages.",
                "Turn off the logging monitor in global configuration mode.",
                "Disable logging to the console.",
                "Set the logging trap severity level to informational.",
            ],
        },
        {
            "slug": "wlc-virtual-interface-dhcp-relay-exclusive",
            "title": "CCNA — WLC virtual interface DHCP relay",
            "stem": "Which interface on the **WLC** is used exclusively as a **DHCP relay**?",
            "name": "wlcvirt1",
            "correct": "D",
            "explain": "Correct. D \u2014 The **virtual interface** (often a placeholder such as **1.1.1.1**) is the WLC function used for **DHCP proxy/relay** to wireless clients: it presents a **gateway-like** address to clients and forwards **DHCP** to configured servers on **dynamic interfaces**. **A** (**distribution**) is a **wired** client-facing interface/VLAN path, not the dedicated DHCP-relay role. **B** (**service**) supports **mobility/RADIUS** and related services on AireOS designs, not exclusive DHCP relay. **C** (**AP-manager**) is for **CAPWAP** to **lightweight APs**, not client DHCP relay.",
            "choices": [
                "distribution",
                "service",
                "AP-manager",
                "virtual",
            ],
        },
        {
            "slug": "ipsec-remote-access-vpn-encrypted-tunnel-purpose",
            "title": "CCNA — Why remote-access IPsec VPN",
            "stem": "Why does an administrator choose to implement a **remote access IPsec VPN**?",
            "name": "ipsecra1",
            "correct": "A",
            "explain": "Correct. A \u2014 A **remote-access IPsec VPN** builds an **encrypted tunnel** over the **Internet** so a **remote user** can reach **private enterprise** resources as if on the LAN. **B** describes **clientless SSL VPN** (browser/portal) access, not classic **IPsec** remote access. **C** mixes **HTTPS**, **authentication**, and server roles; it is not the purpose statement for **IPsec remote access**. **D** mentions **authentication** only and misstates the goal; **IPsec** also provides **confidentiality/integrity** for tunneled traffic, not just device\u2013user authentication at a gateway.",
            "choices": [
                "to establish an encrypted tunnel between a remote user and a private network over the internet",
                "to allow access to an enterprise network using any internet-enabled location via a web browser using SSL",
                "to provide a secure link between an HTTPS server, authentication subsystem, and an end-user",
                "to use cryptography for authentication between a device and user over a negotiated VPN gateway",
            ],
        },
        {
            "slug": "lightweight-ap-web-management-wlc-ip",
            "title": "CCNA — Lightweight AP web management IP",
            "stem": "Which IP address is used when an administrator must open a **web-based management session** with a **lightweight AP**?",
            "name": "lapweb1",
            "correct": "A",
            "explain": "Correct. A \u2014 A **lightweight AP** is **WLC-managed**; administrators do not use a standalone **autonomous AP** web GUI on the AP itself. **Web-based management** of lightweight APs and their WLANs is done through the **WLC** (typically its **management interface** IP) via HTTP/HTTPS. **B** (gateway) is a client default route, not the WLC management endpoint. **C** applies to **autonomous** APs with local management, not **split-MAC** lightweight APs. **D** (**ACS**/AAA server) handles **authentication/accounting**, not routine WLC/AP configuration GUI access.",
            "choices": [
                "WLC IP",
                "gateway IP",
                "autonomous AP IP",
                "ACS IP",
            ],
        },
        {
            "slug": "qos-phb-shaping-policing-principles-choose-two",
            "title": "CCNA — QoS PHB shaping and policing (choose two)",
            "stem": "Which two principles must be considered when using **per-hop behavior** in **QoS**? (Choose two.)",
            "name": "qosphb1",
            "choose_two": True,
            "correct": ["D", "E"],
            "explain": "Correct. D and E \u2014 **Shaping** smooths traffic by **buffering** bursts and **delaying** excess traffic so the average rate stays within policy. **Policing** can be applied in the **inbound** and **outbound** directions to enforce rates (drop, remark, or transmit conforming traffic). **A** is incorrect: **policing** is supported on **subinterfaces** on many Cisco platforms. **B** is incorrect: **shaping** defers excess traffic; **policing** (rate limiting) typically **drops** or **remarks** over-limit traffic\u2014they are not the same effect. **C** is incorrect: **shaping** adds **delay** by queuing excess traffic; immediate discard without deferral describes **policing**, not shaping.",
            "choices": [
                "Policing is not supported on subinterfaces.",
                "Shaping and rate limiting have the same effect.",
                "Shaping drops excessive traffic without adding traffic delay.",
                "Shaping levels out traffic bursts by delaying excess traffic.",
                "Policing is performed in the inbound and outbound directions.",
            ],
        },
        {
            "slug": "tcp-udp-connection-establishment-differentiator",
            "title": "CCNA — TCP vs UDP connection model",
            "stem": "What differentiates the **TCP** and **UDP** protocols?",
            "name": "tcpudpdiff1",
            "correct": "B",
            "explain": "Correct. B \u2014 **TCP** is **connection-oriented**: it runs a **three-way handshake** and establishes a session with the peer before transferring application data, then uses **sequencing** and **acknowledgments** for reliability. **UDP** is **connectionless**: it sends **datagrams** without setup (best-effort delivery). **A** reverses roles (**TCP** uses sequence numbers; **UDP** does not adjust flow like TCP congestion control). **C** misstates both: **TCP** does not send at a fixed constant rate, and **UDP** has **no** transport-layer sequencing or reliability. **D** reverses behavior: **TCP** waits for the handshake; **UDP** does not wait for receiver responses before sending more datagrams.",
            "choices": [
                "TCP tracks segments being transmitted or received by assigning segment numbers, and UDP adjusts data flow according to network conditions.",
                "TCP establishes a connection with the device on the other end before transferring, and UDP transfers without establishing a connection.",
                "TCP sends data at a constant rate with error checking on upper protocol layers, and UDP provides error-checking and sequencing.",
                "TCP immediately transmits data without waiting for a handshake, and UDP awaits a response from the receiver before sending additional data.",
            ],
        },
        {
            "slug": "hsrp-functionality-virtual-mac-lan-redundancy",
            "title": "CCNA — HSRP functionality",
            "stem": "What is a functionality of **HSRP**?",
            "name": "hsrpfn1",
            "correct": "D",
            "explain": "Correct. D \u2014 **HSRP** provides **first-hop (default gateway) redundancy** on a LAN using a shared **virtual IP** and **virtual MAC** that hosts use while **active** and **standby** routers coordinate failover. **A** overstates HSRP: it protects the **local default gateway**, not full **routing-domain reconvergence**. **B** describes a **failover mechanism** (gratuitous ARP can refresh client caches), but it is not the defining **functionality** statement here. **C** is wrong wording: HSRP uses **active/standby routers**, not separate **active and standby routes** in the routing table.",
            "choices": [
                "It provides router redundancy and route reconvergence when a router fails.",
                "It enlists gratuitous ARP to update a client\u2019s ARP cache when the active router switches over.",
                "It requires active and standby routes to provide failover in the case of a router failure.",
                "It uses virtual MAC addressing to provide gateway redundancy on a LAN.",
            ],
        },
        {
            "slug": "macos-ifconfig-en0-default-gateway-first-usable",
            "title": "CCNA — Default gateway from en0 ifconfig",
            "stem": "Refer to the exhibit.",
            "stem_after_exhibit": "If the **default gateway** is the **first usable IP address** in the subnet, what is the default gateway?",
            "name": "en0gw1",
            "correct": "A",
            "explain": "Correct. A \u2014 **10.8.138.14** with netmask **0xffffe000** (**255.255.255.224**, **/19**) belongs to subnet **10.8.128.0/19** (broadcast **10.8.159.255** in the exhibit). The **first usable** host address is **10.8.128.1**. **B** (**10.8.132.1**) is not the network\u2019s first host for this **/19**. **C** (**10.8.138.1**) matches the host\u2019s third octet but is not the subnet\u2019s first usable address. **D** (**10.8.144.1**) lies in a different **/19** block (the next subnet starts at **10.8.160.0**).",
            "post_stem_html": """    <div class="exhibit-stack">
      <div class="exhibit-terminal-white" role="region" aria-label="macOS ifconfig output for en0">
        <pre>MacOs$ ifconfig

en0: flags=8863&lt;UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST&gt; mtu 1500
	options=400&lt;CHANNEL_IO&gt;
	ether f0:18:98:64:60:32
	inet6 fe80::492:c09f:57cf:8c36%en0 prefixlen 64 secured scopeid 0x6
	inet 10.8.138.14 netmask 0xffffe000 broadcast 10.8.159.255
	nd6 options=201&lt;PERFORMNUD,DAD&gt;
	media: autoselect
	status: active</pre>
      </div>
    </div>""",
            "choices": [
                "10.8.128.1",
                "10.8.132.1",
                "10.8.138.1",
                "10.8.144.1",
            ],
        },
        {
            "slug": "r3-show-ip-route-10-10-10-14-out-interface",
            "title": "CCNA — R3 forward 10.10.10.14 (exhibit)",
            "stem": "Refer to the exhibit. Which interface does a packet take to reach the destination address of **10.10.10.14**?",
            "name": "r3rt14",
            "correct": "B",
            "explain": "Correct. B \u2014 **Longest-prefix match** selects **10.10.10.8/29** (connected on **FastEthernet 0/1**). That subnet covers hosts **10.10.10.9\u201310.10.10.14** (broadcast **10.10.10.15**). **10.10.10.16/28** on **Fa0/0** starts at **.16** and does not include **.14**. **10.10.10.4/30** (**Fa0/2**) covers **.4\u2013.7** only. **10.10.10.0/30** (**Serial 0/0**) covers **.0\u2013.3** only.",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="R3 show ip route CLI output">
        <pre>R3#show ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP, D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area,
      N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2,
      E1 - OSPF external type 1, E2 - OSPF external type 2, i - IS-IS,
      su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2, ia - IS-IS
      inter area, * - candidate default, I - per-user static route, o - ODR,
      P - periodic downloaded static route, H - NHRP, I - LISP,
      a - application route, + - replicated route, % - next hop override,
      p - overrides from PfR

Gateway of last resort is not set

     10.0.0.0/8 is variably subnetted, 8 subnets, 4 masks
C    10.10.10.16/28 is directly connected, FastEthernet 0/0
L    10.10.10.17/32 is directly connected, FastEthernet 0/0
C    10.10.10.8/29 is directly connected, FastEthernet 0/1
L    10.10.10.9/32 is directly connected, FastEthernet 0/1
C    10.10.10.4/30 is directly connected, FastEthernet 0/2
L    10.10.10.5/32 is directly connected, FastEthernet 0/2
C    10.10.10.0/30 is directly connected, Serial 0/0
L    10.10.10.1/32 is directly connected, Serial 0/0</pre>
      </div>
    </div>""",
            "choices": [
                "Serial 0/0",
                "FastEthernet 0/1",
                "FastEthernet 0/0",
                "FastEthernet 0/2",
            ],
        },
        {
            "slug": "layer2-switch-link-bundling-characteristic",
            "title": "CCNA — Layer 2 switch link bundling",
            "stem": "What is a characteristic of a **Layer 2 switch**?",
            "name": "l2sw2",
            "correct": "C",
            "explain": "Correct. C \u2014 **Layer 2 switches** can bundle multiple physical links into one logical path (**EtherChannel** / **LAG**) toward servers or uplinks for **higher bandwidth** and **redundancy**. **A** describes a **hub** (flood everything); switches **learn MACs** and forward **unicasts** to the correct port (unknown unicast/MACs may be **flooded** within the VLAN only). **B** is **stateful** tracking (for example firewalls at **Layer 4+**), not basic L2 switching. **D** is wrong: modern switch ports typically run **full duplex**, not **half duplex only**.",
            "choices": [
                "transfers all frames received to every connected device",
                "maintains stateful transaction information",
                "offers link bundling to servers",
                "transmits exclusively at half duplex",
            ],
        },
        {
            "slug": "json-line2-device-entry-is-object",
            "title": "CCNA — JSON line 2 is an object",
            "stem": "What is represented in **line 2** within this JSON schema?",
            "name": "jsonl2obj1",
            "correct": "D",
            "explain": "Correct. D \u2014 Line 2 is **`{\"switch\": \"SW_admin\", \"interface\":\"ge7/41\"}`**, a **JSON object**: curly braces **`{ }`** enclosing **key:value** pairs. The outer **`[ ]`** on lines 1 and 5 is the **array** that holds multiple objects. **\"switch\"** and **\"interface\"** are **keys**; **\"SW_admin\"** and **\"ge7/41\"** are **values**. The whole line 2 construct is not itself an array, key, or single value.",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="JSON device list with line numbers">
        <pre>1   [
2   {"switch": "SW_admin", "interface":"ge7/41"},
3   {"VPN concentrator": "VPN_finance", "interface":"fe9/5"},
4   {"IDS": "IPS_admin", "interface":"te2/10"},
5   ]</pre>
      </div>
    </div>""",
            "choices": [
                "array",
                "value",
                "key",
                "object",
            ],
        },
        {
            "slug": "rest-http-verbs-create-resource-choose-two",
            "title": "CCNA — REST HTTP verbs to create (choose two)",
            "stem": "Which two **HTTP verbs** does a **REST-based API** use to **create a resource**? (Choose two.)",
            "name": "restcreate2",
            "choose_two": True,
            "correct": ["C", "D"],
            "explain": "Correct. C and D \u2014 **POST** commonly **creates** a new resource (the server often assigns the URI and may return **201 Created**). **PUT** can **create or replace** a resource at a **known URI** (idempotent). **GET** (**A**) **reads** data only. **DELETE** (**B**) **removes** a resource. **PATCH** (**E**) applies a **partial update** to an existing resource, not the usual **create** operation on CCNA items.",
            "choices": [
                "GET",
                "DELETE",
                "POST",
                "PUT",
                "PATCH",
            ],
        },
        {
            "slug": "r4-show-ip-route-10-255-2-2-eigrp-protocol",
            "title": "CCNA — R4 route 10.255.2.2 protocol (exhibit)",
            "stem": "Refer to the exhibit. Considering **default routing protocol configurations** were used, which routing protocol is used to learn the **10.255.2.2/32** route?",
            "name": "r4rt222",
            "correct": "A",
            "explain": "Correct. A \u2014 The entry **10.255.2.2/32 [90/130816]** uses **administrative distance 90**, the default for **internal EIGRP** (code **D** in a full table). The second number is the **EIGRP composite metric**. **OSPF** defaults to **110**; **RIP** to **120**; **BGP** uses **20** (eBGP) or **200** (iBGP), not **90**. Other routes in the exhibit show **90** (EIGRP) or **100** (for example static/floating paths), but **10.255.2.2/32** is learned via **EIGRP**.",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="R4 show ip route CLI output">
        <pre>R4#show ip route
Gateway of last resort is not set

   10.0.0.0/8 is variably subnetted, 14 subnets, 2 masks
   10.0.12.0/24 [100/2] via 10.0.24.2, 00:02:27, GigabitEthernet0/1
   10.0.13.0/24 [90/3072] via 10.0.34.3, 00:00:19, GigabitEthernet0/0
   10.0.24.0/24 is directly connected, GigabitEthernet0/1
   10.0.24.4/32 is directly connected, GigabitEthernet0/1
   10.0.34.0/24 is directly connected, GigabitEthernet0/0
   10.0.34.4/32 is directly connected, GigabitEthernet0/0
   10.0.45.0/24 is directly connected, GigabitEthernet0/2
   10.0.45.4/32 is directly connected, GigabitEthernet0/2
   10.2.0.0/24 [90/1] via 10.0.45.5, 00:00:08, GigabitEthernet0/2
   10.255.1.1/32 [100/3] via 10.0.34.3, 00:02:27, GigabitEthernet0/0
                 [100/3] via 10.0.24.2, 00:02:27, GigabitEthernet0/1
   10.255.2.2/32 [90/130816] via 10.0.24.2, 00:14:46, GigabitEthernet0/1
   10.255.3.3/32 [100/2] via 10.0.34.3, 00:02:27, GigabitEthernet0/0
   10.255.4.4/32 is directly connected, Loopback0
   10.255.5.5/32 [90/1] via 10.0.45.5, 00:00:08, GigabitEthernet0/2</pre>
      </div>
    </div>""",
            "choices": [
                "EIGRP",
                "BGP",
                "RIP",
                "OSPF",
            ],
        },
        {
            "slug": "production-network-600-servers-subnet-slash22",
            "title": "CCNA — Subnet for 600 production servers",
            "stem": "An application in the network is being scaled up from **300** servers to **600**. Each server requires **3** network connections to support **production**, **backup**, and **management** traffic. Each connection resides on a **different subnet**. The router configuration for the **production** network must be configured first using a subnet in the **10.0.0.0/8** network. Which command must be configured on the interface of the router to accommodate the requirements and **limit wasted IP address space**?",
            "name": "prod600",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 **600** production hosts need a subnet with at least **600 usable** addresses (plus network/broadcast in classic subnetting \u2192 **2^10 = 1024** addresses, **/22**). **255.255.252.0** is **/22** (**1022** usable hosts), the **tightest** mask among the choices that fits **600**. **A** (**/28**, **14** hosts) is far too small. **C** (**/23**, **510** hosts) is still too small for **600**. **B** (**/20**, **4094** hosts) works but **wastes** far more space than **/22**.",
            "choices": [
                "ip address 10.10.10.1 255.255.255.240",
                "ip address 10.10.10.1 255.255.240.0",
                "ip address 10.10.10.1 255.255.254.0",
                "ip address 10.10.10.1 255.255.252.0",
            ],
        },
        {
            "slug": "switch-unknown-dest-mac-flood-frame-exhibit",
            "title": "CCNA — Switch unknown destination MAC (exhibit)",
            "stem": "Refer to the exhibit. How does the switch handle the frame?",
            "name": "swflood1",
            "correct": "A",
            "explain": "Correct. A \u2014 Destination **3C:5D:7E:9F:1A:2B** is **not** in the **MAC address table**, so the switch treats it as **unknown unicast** and **floods** the frame out **all ports in the VLAN** except the **ingress port** (**Gi1/0/1**, where source **D3:F4:47:57:67:46** was learned). **B** applies to **static** or **policy-based** forwarding, not an unknown destination. **C** is wrong: switches do not **hold** unknown-destination frames until aging adds the MAC; flooding happens immediately. **D** is wrong: unknown unicast is **flooded**, not **dropped**, to reach the host and allow learning from replies.",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="Ethernet frame and MAC address table exhibit">
        <pre>Switch# show ethernet-frame-and-mac-address-table

Ethernet Frame:
+----------------------------------------------------+
| Destination MAC Address: 3C:5D:7E:9F:1A:2B         |
| Source MAC Address: D3:F4:47:57:67:46              |
| EtherType/Length: 0x0800 (IPv4)                    |
| Payload: [Data]                                    |
| Frame Check Sequence: [CRC]                        |
+----------------------------------------------------+

MAC Address Table:
VLAN   MAC Address         Type      Ports
----   -----------------   --------  ----------
12     D3:F4:47:57:67:46   Dynamic   Gi1/0/1
16     20:31:42:53:64:DE   Static    Gi1/0/2
24     A0:B3:C4:D3:B4:48   Secure    Gi1/0/3
31     B5:16:32:12:6B:68   Dynamic   Gi1/0/4
44     8F:A0:B3:C4:34:50   Static    Gi1/0/5</pre>
      </div>
    </div>""",
            "choices": [
                "It floods the frame to all ports except the incoming port.",
                "It switches the frame to a predetermined port based on settings.",
                "It ages out the frame until the MAC address becomes known.",
                "It drops the frame to avoid unnecessary network congestion.",
            ],
        },
        {
            "slug": "virtual-machines-guest-os-service-statement",
            "title": "CCNA — Statement describing virtual machines",
            "stem": "Which statement describes **virtual machines**?",
            "name": "vmstmt1",
            "correct": "A",
            "explain": "Correct. A \u2014 A **virtual machine** runs a **guest operating system** and the **applications/services** on top of **virtual hardware** presented by a **hypervisor** on a physical host. **B** describes **management tools** for devices, not what a VM is. **C** confuses **Nexus supervisor** (switch control plane) or generic wording with **hypervisor-based** VM management. **D** is wrong: virtualization makes workloads **software-defined** and **less tied to specific hardware**, not **hardware-centric**.",
            "choices": [
                "They include a guest OS and the service.",
                "They facilitate local management of infrastructure devices.",
                "They use a supervisor to provide management for services.",
                "They enable the network to become agile and hardware-centric.",
            ],
        },
        {
            "slug": "mfa-complex-password-totp-minimum-security",
            "title": "CCNA — MFA minimum security combination",
            "stem": "Which combination of methods satisfies the **minimum security requirements** when a new **multifactor authentication** solution is deployed?",
            "name": "mfamin1",
            "correct": "C",
            "explain": "Correct. C \u2014 **MFA** requires **two different factor classes**. A **complex password** is **something you know**; a **time-based one-time password (TOTP)** from an app or token is **something you have**. **A** and the password+PIN pairs use only **knowledge** factors. **B** pairs two **possession** factors (**USB dongle** and **phone**) without a **know** or **are** factor in another class. **D** uses two **biometric** methods (**fingerprint** and **facial recognition**)\u2014both **something you are**.",
            "choices": [
                "password of 8 to 15 characters and personal 12-digit PIN",
                "authorized USB dongle and mobile phone",
                "complex password and time-based one-time password",
                "fingerprint scanning and facial recognition",
            ],
        },
        {
            "slug": "r4-dynamic-routes-least-preferred-metric-rip",
            "title": "CCNA — R4 least preferred dynamic metric (exhibit)",
            "stem": "Refer to the exhibit. Of the routes learned with **dynamic routing protocols**, which has the **least preferred** metric?",
            "name": "r4met1",
            "correct": "D",
            "explain": "Correct. D \u2014 Among common **IGPs**, **RIP** uses the **highest default administrative distance (120)**, so it is the **least preferred** when another protocol also offers a path. **EIGRP** (**B**, **D** routes, default **AD 90**) and **OSPF** (**C**, **O** routes, default **AD 110**) are preferred ahead of RIP. **A** (**Local**) is not learned by a **dynamic** routing protocol (**L**/**C** are connected/local). Within one protocol, a **higher** route **metric** is less preferred, but this item compares **protocols**; **RIP\u2019s AD 120** makes it least preferred overall.",
            "choices": [
                "Local",
                "EIGRP",
                "OSPF",
                "RIP",
            ],
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="R4 show ip route CLI output">
        <pre>R4#show ip route
Gateway of last resort is not set

   10.0.0.0/8 is variably subnetted, 14 subnets, 2 masks
O    10.0.12.0/24 [100/2] via 10.0.24.2, 00:02:27, GigabitEthernet0/1
D    10.0.13.0/24 [90/3072] via 10.0.34.3, 00:00:19, GigabitEthernet0/0
C    10.0.24.0/24 is directly connected, GigabitEthernet0/1
L    10.0.24.4/32 is directly connected, GigabitEthernet0/1
C    10.0.34.0/24 is directly connected, GigabitEthernet0/0
L    10.0.34.4/32 is directly connected, GigabitEthernet0/0
C    10.0.45.0/24 is directly connected, GigabitEthernet0/2
L    10.0.45.4/32 is directly connected, GigabitEthernet0/2
R    10.2.0.0/24 [120/1] via 10.0.45.5, 00:00:08, GigabitEthernet0/2
O    10.255.1.1/32 [100/3] via 10.0.34.3, 00:02:27, GigabitEthernet0/0
                   [100/3] via 10.0.24.2, 00:02:27, GigabitEthernet0/1
D    10.255.2.2/32 [90/130816] via 10.0.24.2, 00:01:46, GigabitEthernet0/1
O    10.255.3.3/32 [100/2] via 10.0.34.3, 00:02:27, GigabitEthernet0/0
C    10.255.4.4/32 is directly connected, Loopback0
R    10.255.5.5/32 [120/1] via 10.0.45.5, 00:00:08, GigabitEthernet0/2</pre>
      </div>
    </div>""",
        },
        {
            "slug": "r1-forward-192-168-18-16-longest-prefix-gi10",
            "title": "CCNA — R1 forward 192.168.18.16 (exhibit)",
            "stem": "Refer to the exhibit. Which interface does a packet take to reach the host address of **192.168.18.16**?",
            "name": "r1rt1816",
            "correct": "A",
            "explain": "Correct. A \u2014 **Longest-prefix match** selects **192.168.18.0/27** (**RIP** via **GigabitEthernet1/0**). **192.168.18.16** is in **.0\u2013.31** for **/27** but **outside** **192.168.18.0/28** (hosts **.0\u2013.15** only). The **/24 EIGRP** route on **Gi0/0** is less specific than **/27**. **Gi2/0** (**OSPF /28**) does not match **.16**. **Null0** is not in the routing table for this destination.",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="R1 show ip route CLI output">
        <pre>R1#show ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP,
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area,
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2,
       E1 - OSPF external type 1, E2 - OSPF external type 2, i - IS-IS,
       su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2,
       ia - IS-IS inter area, * - candidate default, I - per-user static route,
       o - ODR, P - periodic downloaded static route, H - NHRP, I - LISP, a -
       application route, + - replicated route, % - next hop override,
       p - overrides from PFR

Gateway of last resort is not set

        10.0.0.0/8 is variably subnetted, 6 subnets, 2 masks
C       10.10.10.0/24 is directly connected, GigabitEthernet0/0
L       10.10.10.1/32 is directly connected, GigabitEthernet0/0
C       10.10.20.0/24 is directly connected, GigabitEthernet1/0
L       10.10.20.1/32 is directly connected, GigabitEthernet1/0
C       10.10.30.0/24 is directly connected, GigabitEthernet2/0
L       10.10.30.1/32 is directly connected, GigabitEthernet2/0

        192.168.18.0/24 is variably subnetted, 3 subnets, 3 masks
D       192.168.18.0/24 [90/3072] via 10.10.10.10, 00:13:10, GigabitEthernet0/0
R       192.168.18.0/27 [120/1] via 10.10.20.10, 00:09:15, GigabitEthernet1/0
O       192.168.18.0/28 [110/2] via 10.10.30.10, 00:12:56, GigabitEthernet2/0</pre>
      </div>
    </div>""",
            "choices": [
                "GigabitEthernet1/0",
                "GigabitEthernet0/0",
                "GigabitEthernet2/0",
                "Null0",
            ],
        },
        {
            "slug": "lpm-152-168-32-85-next-hop-10-10-2-2",
            "title": "CCNA — LPM to 152.168.32.85",
            "stem": "Refer to the exhibit. Which **next hop** is used to route packets to the application server at **152.168.32.85**?",
            "name": "lpm3285",
            "correct": "B",
            "explain": "Correct. B \u2014 **Longest-prefix match** selects **152.168.32.0/24** (next hop **10.10.2.2**, interface **f1/0**). **152.168.32.85** is in **152.168.32.0\u2013152.168.32.255** but **not** in **152.168.32.0/26** (hosts **.1\u2013.62** only). **/24** is longer than **/23** and **/22**, so it wins over **10.10.4.2** and **10.10.1.2**. **10.10.3.2** (**/26**) does not match **.85**.",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="Routing table prefix list">
        <pre>Prefix               Interface   Next-hop
152.168.32.0/22      f0/0        10.10.1.2
152.168.32.0/24      f1/0        10.10.2.2
152.168.32.0/26      f2/0        10.10.3.2
152.168.32.0/23      f3/0        10.10.4.2</pre>
      </div>
    </div>""",
            "choices": [
                "10.10.1.2",
                "10.10.2.2",
                "10.10.3.2",
                "10.10.4.2",
            ],
        },
        {
            "slug": "floating-default-route-ad-25-preempts-dynamic-20",
            "title": "CCNA — Floating default until WAN (AD 20)",
            "stem": "A **default route** must be configured to use the IP address of **192.168.1.1** until a **WAN** circuit is installed. The WAN circuit will use a **dynamic routing protocol** with an **administrative distance of 20**. Which configuration must be applied to allow the **dynamic route** to take precedence when it is in place?",
            "name": "fltdef1",
            "correct": "B",
            "mono": True,
            "explain": "Correct. B \u2014 Configure a **floating static default** with **administrative distance 25** (**higher than 20**). While the WAN is down, the static default is used; when the dynamic default appears at **AD 20**, it **wins** and replaces the backup static. **A** uses the default static **AD 1**, which would **beat AD 20** and block the dynamic route. **C** (**track**) handles **next-hop reachability**, not preference versus a lower-AD dynamic route. **D** sets static **AD 20**, tying the dynamic protocol; the backup static must be **greater than 20**.",
            "choices": [
                "ip route 0.0.0.0 0.0.0.0 192.168.1.1",
                "ip route 0.0.0.0 0.0.0.0 192.168.1.1 25",
                "ip route 0.0.0.0 0.0.0.0 192.168.1.1 track 1",
                "ip route 0.0.0.0 0.0.0.0 192.168.1.1 20",
            ],
        },
        {
            "slug": "mfa-main-capability-identity-two-factors",
            "title": "CCNA — MFA main capability",
            "stem": "What is the main capability of **multifactor authentication**?",
            "name": "mfacap1",
            "correct": "C",
            "explain": "Correct. C \u2014 **MFA** verifies **who the user is** by requiring **two or more authentication factors** from **different classes** (for example **know** + **have**, or **know** + **are**). **A** confuses MFA with **authorization** (permissions) and wrongly centers on **three** factors. **B** mixes **authentication** and **authorization**; MFA\u2019s main role is **identity verification**, not granting permissions. **D** describes **authorization** (access permissions), not confirming identity with multiple factors.",
            "choices": [
                "Identifying permissions for end users using three authentication factors",
                "Authenticating and authorizing end users using two authentication factors",
                "Confirming end-user identity using two or more authentication factors",
                "Verifying end-user access permissions using two authentication factors",
            ],
        },
        {
            "slug": "flexconnect-flex-local-switching-trunk-pruned-vlans",
            "title": "CCNA — FlexConnect local switching switch port",
            "stem": "Which **switch port** configuration must be configured when connected to an AP running in **FlexConnect** mode, and the WLANs use **flex local switching**?",
            "name": "flexsw1",
            "correct": "B",
            "explain": "Correct. B \u2014 **FlexConnect local switching** bridges client traffic onto **multiple wired VLANs** at the AP. The switch port must be an **802.1Q trunk** carrying those VLANs (often **pruned** to only the VLANs in use). **A** (**access**, one VLAN) fits **centralized/CAPWAP** tunneling or a single-VLAN design, not multiple locally switched WLAN VLANs. **C** (**Layer 3** switch port) is not the standard AP uplink model. **D** (**tagged port with MAC filtering**) is not the required FlexConnect local-switching port configuration.",
            "choices": [
                "access port with one VLAN",
                "trunk port with pruned VLANs",
                "Layer 3 port with an IP address",
                "tagged port with MAC Filtering enabled",
            ],
        },
        {
            "slug": "wpa3-personal-ssid-mandatory-pmf",
            "title": "CCNA — WPA3-Personal mandatory PMF",
            "stem": "Which feature is **mandatory** when configuring a new **SSID** for a wireless network running **WPA3-Personal** mode?",
            "name": "wpa3pmf1",
            "correct": "B",
            "explain": "Correct. B \u2014 **WPA3** (including **WPA3-Personal** with **SAE**) requires **Protected Management Frames (802.11w / PMF)** to protect management traffic; controllers typically set **PMF** to **required/mandatory** on WPA3 WLANs. **A** (**OWE**) is **Enhanced Open**, not WPA3-Personal. **C** (**Enhanced Open**) is the service name for **OWE**, not a WPA3-Personal requirement. **D** (**Fast Transition**, **802.11r**) is **optional** for faster roaming and is often **disabled** on WPA3-Personal designs; it is not mandatory.",
            "choices": [
                "Opportunistic Wireless Encryption",
                "Protected Management Frame",
                "Enhanced Open",
                "Fast Transition",
            ],
        },
        {
            "slug": "digest-authentication-challenge-response-plaintext",
            "title": "CCNA — Digest Authentication challenge-response",
            "stem": "Which feature of **Digest Authentication** prevents credentials from being sent in **plaintext**?",
            "name": "digest1",
            "correct": "B",
            "explain": "Correct. B \u2014 **HTTP Digest Authentication** uses a **challenge-response** exchange: the server sends a **nonce** (challenge) and the client replies with a **hash** derived from the username, realm, password, nonce, and related parameters. The **password itself is not sent** in cleartext. **A** (**SSL/TLS**) encrypts the transport but is a separate layer, not the defining Digest Authentication mechanism. **C** (**token-based authorization**) describes access tokens after authentication, not Digest\u2019s credential protection. **D** (**PKI**) uses **certificates/keys** for trust and encryption/signing, not Digest\u2019s hash-based challenge model.",
            "choices": [
                "SSL/TLS encryption",
                "Challenge-response mechanism",
                "Token-based authorization",
                "Public key infrastructure",
            ],
        },
        {
            "slug": "trunk-port-carries-multiple-vlans",
            "title": "CCNA — Trunk carries multiple VLANs",
            "stem": "Which type of **port configuration** is used to carry traffic for **multiple VLANs**?",
            "name": "trunkmv1",
            "correct": "C",
            "explain": "Correct. C \u2014 A **trunk** port uses **802.1Q tagging** (and optional **native VLAN** handling) so **multiple VLANs** share one physical link while staying separated. **A** (**LAG**) and **B** (**EtherChannel**) **bundle** links for bandwidth/redundancy; VLAN behavior is still **access** or **trunk** on the logical interface. **D** (**access**) carries **one** VLAN (untagged), except special cases such as **voice VLAN** on the same access port.",
            "choices": [
                "LAG",
                "EtherChannel",
                "trunk",
                "access",
            ],
        },
        {
            "slug": "r1-192-168-64-22-null0-longest-prefix",
            "title": "CCNA — R1 forward 192.168.64.22 (exhibit)",
            "stem": "Refer to the exhibit. How will router **R1** handle packets destined to **192.168.64.22**?",
            "name": "r1rt6422",
            "correct": "D",
            "explain": "Correct. D \u2014 **Longest-prefix match** selects **192.168.64.0/19** via **Null0**, so traffic to **192.168.64.22** is **discarded**. The **/18** routes (**static** to **10.1.1.1** and **OSPF** via **10.1.1.2**/**10.1.1.3**) are **less specific** and are not used. **A** and **C** would apply only if **/19 Null0** were absent; among **/18** paths, **AD 1** static to **10.1.1.1** beats **OSPF AD 110**, not the lower-metric OSPF path alone. **B** is wrong: routing does not pick \u201chighest AD\u201d or \u201chighest destination IP.\u201d",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="R1 show ip route CLI output">
        <pre>R1#show ip route
   S  192.168.64.0/18 [1/0] via 10.1.1.1
   O  192.168.64.0/18 [110/236855] via 10.1.1.2
   O  192.168.64.0/18 [110/229840] via 10.1.1.3
   S  192.168.64.0/19 [1/0] via Null0</pre>
      </div>
    </div>""",
            "choices": [
                "It will use the static route to 10.1.1.1.",
                "It will use the route with the highest AD and highest destination IP.",
                "It will route the packets to 10.1.1.2.",
                "It will drop the packets.",
            ],
        },
        {
            "slug": "aa-show-ip-route-192-168-20-1-static-ad",
            "title": "CCNA — AA AD for 192.168.20.1 (exhibit)",
            "stem": "Refer to the exhibit. What is the **administrative distance** for the advertised prefix that includes the host IP address **192.168.20.1**?",
            "name": "aart201",
            "correct": "D",
            "explain": "Correct. D \u2014 **192.168.20.1** matches **S 192.168.20.0/24 [1/0] via 192.168.10.2**. In **`[AD/metric]`**, **1** is the **administrative distance** (default for a **static** route). **A** (**0**) is for **connected/local** routes (**C**/**L**), not this static. **B** (**192.168.10.2**) is the **next-hop** address, not AD. **C** (**24**) is the **prefix length** (/24), not administrative distance.",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="AA show ip route CLI output">
        <pre>AA#show ip route

   10.0.0.0/8 is variably subnetted, 6 subnets, 2 masks
C    10.0.0.0/30 is directly connected, GigabitEthernet0/0
L    10.0.0.1/32 is directly connected, GigabitEthernet0/0
C    10.10.0.0/30 is directly connected, GigabitEthernet0/1
L    10.10.0.1/32 is directly connected, GigabitEthernet0/1
O    10.20.0.0/30 [110/2] via 10.0.0.2, 00:00:40, GigabitEthernet0/0
O    10.30.0.0/30 [110/2] via 10.0.0.2, 00:00:40, GigabitEthernet0/0
   172.16.0.0/24 is subnetted, 1 subnets
S    172.16.10.0 [1/0] via 10.0.0.2
   192.168.10.0/24 is variably subnetted, 2 subnets, 2 masks
C    192.168.10.0/24 is directly connected, GigabitEthernet0/2
L    192.168.10.1/32 is directly connected, GigabitEthernet0/2
S    192.168.20.0/24 [1/0] via 192.168.10.2</pre>
      </div>
    </div>""",
            "choices": [
                "0",
                "192.168.10.2",
                "24",
                "1",
            ],
        },
        {
            "slug": "show-ip-route-default-ad-eigrp-ospf-choose-two",
            "title": "CCNA — Default AD by protocol (exhibit, choose two)",
            "stem": "Refer to the exhibit. Which routes are configured with their **default administrative distances**? (Choose two)",
            "name": "defad1",
            "choose_two": True,
            "correct": ["A", "B"],
            "explain": "Correct. A and B \u2014 In **`[AD/metric]`**, compare the first value to each protocol\u2019s default: **EIGRP (internal) 90**, **OSPF 110**, **RIP 120**. **O** routes (for example **10.0.12.0/24**, **10.255.2.2/32**) show **110**, so **OSPF** is at its default AD. Routes to **10.255.2.4/24** and **10.255.5.5/32** show **90** (code **D** in a full table), the default for **internal EIGRP**. **C (RIP)** is wrong: no entries use **120**, and **RIP\u2019s** default AD is **120**, not **90**. **D (Local)** is wrong: **L**/**C** routes are **directly connected** (AD **0**); they are not dynamic protocol routes displayed with an IGP default AD in this sense.",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="show ip route CLI output">
        <pre>#show ip route

   10.0.0.0/8 is variably subnetted, 15 subnets, 2 masks
O    10.0.12.0/24 [110/2] via 10.0.14.1, 00:17:46, GigabitEthernet0/2
C    10.0.14.0/24 is directly connected, GigabitEthernet0/2
L    10.0.14.4/32 is directly connected, GigabitEthernet0/2
O    10.0.23.0/24 [110/2] via 10.0.34.3, 00:17:46, GigabitEthernet0/0
C    10.0.34.0/24 is directly connected, GigabitEthernet0/0
L    10.0.34.4/32 is directly connected, GigabitEthernet0/0
C    10.0.45.0/24 is directly connected, GigabitEthernet0/1
L    10.0.45.4/32 is directly connected, GigabitEthernet0/1
O    10.0.254.1/32 [110/2] via 10.0.14.1, 00:17:46, GigabitEthernet0/2
D    10.255.2.4/24 [90/1] via 10.0.45.5, 00:00:13, GigabitEthernet0/1
O    10.255.1.1/32 [110/2] via 10.0.14.1, 00:17:46, GigabitEthernet0/0
O    10.255.2.2/32 [110/3] via 10.0.34.3, 00:17:46, GigabitEthernet0/0
                 [110/3] via 10.0.14.1, 00:17:46, GigabitEthernet0/2
O    10.255.3.3/32 [110/2] via 10.0.34.3, 00:17:46, GigabitEthernet0/0
C    10.255.3.4/32 is directly connected, Loopback0
D    10.255.5.5/32 [90/1] via 10.0.45.5, 00:00:13, GigabitEthernet0/1</pre>
      </div>
    </div>""",
            "choices": [
                "EIGRP",
                "OSPF",
                "RIP",
                "Local",
            ],
        },
        {
            "slug": "wpa3-implementation-security-protocol-gcmp",
            "title": "CCNA — WPA3 security protocol (GCMP)",
            "stem": "Which **security protocol** is appropriate for a **WPA3** implementation?",
            "name": "wpa3gcmp1",
            "correct": "B",
            "explain": "Correct. B \u2014 **WPA3** uses **GCMP** (**Galois/Counter Mode Protocol**) for over-the-air frame confidentiality and integrity (for example **GCMP-128**; stronger **GCMP-256** modes exist in enterprise Suite\u202fB deployments). **A** (**TKIP**) is a legacy **WPA** cipher, not WPA3. **C** (**MD5**) is a hash algorithm used in other contexts, not the WPA3 wireless data-protection protocol. **D** (**CCMP**) is the primary **WPA2** air-interface protocol (**AES-CCMP**); WPA3 may allow transitional **CCMP** interoperability, but **GCMP** is the protocol defined for WPA3 implementations.",
            "choices": [
                "TKIP",
                "GCMP",
                "MD5",
                "CCMP",
            ],
        },
        {
            "slug": "access-sw1-ntp-server-ipv6-replicate-config",
            "title": "CCNA — Replicate AccessSw1 NTP (exhibit)",
            "stem": "A network engineer must replicate the **AccessSw1** NTP configuration on a new switch. The engineer could not access privileged mode on **AccessSw1** to view its configuration. Which command must be applied to the new switch to replicate the configuration?",
            "name": "ntpacc1",
            "correct": "A",
            "mono": True,
            "explain": "Correct. A \u2014 **`show ntp associations`** shows **`*~2001:DB8:12::1`**: **`*`** is the current **sys.peer** and **`~`** means **configured** on this device. Replicate that client with **`ntp server 2001:db8:12::1`**. The **ref clock** column (**127.127.1.1**) is the upstream reference **on the remote NTP server**, not the address to configure on **AccessSw1** (**D**). **`ntp master`** (**B**, **C**) makes the local device an **NTP server** using its own clock, not an **NTP client** of **2001:DB8:12::1**.",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="AccessSw1 show ntp associations CLI output">
        <pre>AccessSw1&gt; show ntp associations
   address           ref clock     st  when  poll  reach  delay   offset   disp
   *~2001:DB8:12::1  127.127.1.1    3   39    64    377   23.903  -5.581   2.077
   * sys.peer, # selected, + candidate, - outlyer, x falseticker, ~ configured</pre>
      </div>
    </div>""",
            "choices": [
                "ntp server 2001:db8:12::1",
                "ntp master 3",
                "ntp master",
                "ntp server 127.127.1.1",
            ],
        },
        {
            "slug": "layer2-switch-data-link-layer-characteristic",
            "title": "CCNA — Layer 2 switch data link role",
            "stem": "What is a characteristic of a **Layer 2 switch**?",
            "name": "l2sw3",
            "correct": "C",
            "explain": "Correct. C \u2014 A **Layer 2 switch** operates at the **data link layer (Layer 2)**, forwarding **Ethernet frames** using **MAC addresses**. **A** (**stateful transactions**) is **Layer 4+** behavior (for example firewalls or load balancers), not basic switching. **B** (**deep packet inspection**) is an **advanced inspection/QoS/security** function, not the defining L2 switch characteristic here. **D** is wrong: VLANs create **multiple broadcast domains**; even on one VLAN, switches **segment collision domains per port** and do not behave like a single shared hub for all traffic.",
            "choices": [
                "maintains stateful transaction information",
                "prioritizes traffic using deep packet inspection",
                "uses the data link layer for communications",
                "provides a single broadcast domain for all connected devices",
            ],
        },
        {
            "slug": "tftp-no-auth-acknowledges-data-sent",
            "title": "CCNA — TFTP no login and ACKs",
            "stem": "Which **file transfer protocol** omits a **username or password** requirement and **acknowledges all data sent**?",
            "name": "tftpauth1",
            "correct": "B",
            "explain": "Correct. B \u2014 **TFTP** (UDP port **69**) has **no username/password** login step and transfers data in **fixed-size blocks**; each block is **acknowledged** before the next is sent (stop-and-wait reliability over UDP). **A** (**FTP**) uses **USER/PASS** authentication and **TCP** (separate control/data channels), not TFTP\u2019s block ACK model. **C** (**SCP**) and **D** (**SFTP**) run over **SSH** and require **authenticated** sessions; they are **secure** file-copy protocols, not credential-free TFTP-style transfers.",
            "choices": [
                "FTP",
                "TFTP",
                "SCP",
                "SFTP",
            ],
        },
        {
            "slug": "tcp-udp-difference-reliable-ordered-vs-latency",
            "title": "CCNA — TCP vs UDP difference",
            "stem": "What is the difference between the **TCP** and **UDP** protocols?",
            "name": "tcpudp2",
            "correct": "A",
            "explain": "Correct. A \u2014 **TCP** is **connection-oriented** and provides **ordered, reliable** delivery using **sequencing**, **acknowledgments**, and **retransmissions**. **UDP** is **connectionless** with lower overhead, favoring **low latency** and **high throughput** for applications that tolerate loss (for example VoIP/streaming). **B** is wrong: **multicast/broadcast** are not TCP\u2019s defining role; both can carry unicast traffic. **C** describes **Layer 2** functions (**neighbor discovery**, **loop prevention**), not transport protocols. **D** reverses identifiers: **MAC** addresses are **Layer 2**; **IP** addresses are **Layer 3**\u2014neither statement defines the TCP vs UDP difference.",
            "choices": [
                "TCP ensures ordered, reliable data delivery, and UDP offers low latency and high throughput.",
                "TCP manages multicast and broadcast data transfers, and UDP only handles unicast communications.",
                "TCP discovers neighboring devices on a local network segment, and UDP prevents Layer 2 switching loops.",
                "TCP identities devices by their MAC addresses, and UDP identities devices by their IP addresses.",
            ],
        },
        {
            "slug": "ansible-network-automation-features-choose-two",
            "title": "CCNA — Ansible features (choose two)",
            "stem": "Which two features are provided by **Ansible** in **network automation**? (Choose two)",
            "name": "ansfeat1",
            "choose_two": True,
            "correct": ["D", "E"],
            "explain": "Correct. D and E \u2014 **Ansible** playbooks are written in **YAML**, and Ansible is **agentless**: it connects to managed devices (commonly over **SSH**) without installing a persistent agent on each node. **A** is wrong: administrators supply credentials in **inventory** or **Ansible Vault**; Ansible does not \u201csupply\u201d credentials by itself. **B** describes a **push** model (modules/run tasks pushed from the **control node**), which is true in practice, but the paired CCNA answers here are **YAML** and **agentless** versus **Chef**/**Puppet** models. **C** (**job templates** with **version control**) is a feature of **Ansible Automation Platform** / **AWX**, not core open-source Ansible on the exam.",
            "choices": [
                "supplies network credentials",
                "pushes configurations to client",
                "launches job templates using version control",
                "uses YAML language",
                "offers agentless deployment",
            ],
        },
        {
            "slug": "remote-access-vpn-employee-public-wifi",
            "title": "CCNA — Remote-access VPN use case",
            "stem": "Which type of **VPN connection** is used when an **employee** accesses a **secure server** from **public Wi\u2011Fi**?",
            "name": "vpnrem1",
            "correct": "C",
            "explain": "Correct. C \u2014 A **remote-access** (client-to-site) **VPN** lets an individual host on an **untrusted network** (for example **public Wi\u2011Fi**) build an **encrypted tunnel** to a corporate **VPN gateway** and reach **private** servers. **A** (**site-to-site**) and **B** (**router-to-router**) connect **two fixed sites** or edge routers, not a single roaming user. **D** (**open**) is not a standard VPN category here; **open** Wi\u2011Fi is **unencrypted** local wireless\u2014the VPN protects traffic **after** the client connects.",
            "choices": [
                "site-to-site",
                "router-to-router",
                "remote",
                "open",
            ],
        },
        {
            "slug": "wlan-nonoverlapping-channels-reduce-interference",
            "title": "CCNA — Role of nonoverlapping channels",
            "stem": "What is the role of **nonoverlapping channels** in a **wireless environment**?",
            "name": "wlanov1",
            "correct": "A",
            "explain": "Correct. A \u2014 Assigning **nonoverlapping** channels (for example **1, 6, and 11** in **2.4 GHz**) keeps adjacent **AP** radios from stepping on each other\u2019s spectrum, **reducing co-channel and adjacent-channel interference** in dense WLANs. **B** (**channel bonding**) combines **adjacent** channels for wider bandwidth (for example **40 MHz**), which is a different technique than spacing APs on nonoverlapping centers. **C** (**faster roaming**) depends on mechanisms such as **802.11r/k/v**, not channel numbering alone. **D** is misleading: nonoverlapping planning improves **airtime quality**; raw **throughput** gains come mainly from **wider channels**, **MIMO**, and **higher PHY rates**, not merely picking 1/6/11.",
            "choices": [
                "to reduce interference",
                "to allow for channel bonding",
                "to enable faster roaming",
                "to increase bandwidth",
            ],
        },
        {
            "slug": "json-line3-load-balancer-entry-is-object",
            "title": "CCNA — JSON line 3 is an object",
            "stem": "What is represented in **line 3** within this JSON schema?",
            "name": "jsonl3obj1",
            "correct": "D",
            "explain": "Correct. D \u2014 Line 3 is **`{\"load balancer\": \"LB_munich\", \"port\":\"te8/26\"}`**, a **JSON object**: curly braces **`{ }`** with **key:value** pairs. Lines 1 and 5 **`[ ]`** form the **array** holding multiple objects. **\"load balancer\"** and **\"port\"** are **keys**; **\"LB_munich\"** and **\"te8/26\"** are **values**. Line 3 is not an array, a single key, or a lone value.",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="JSON device list with line numbers">
        <pre>1   [
2   {"switch": "SW_dallas", "port":"ge16"},
3   {"load balancer": "LB_munich", "port":"te8/26"},
4   {"VPN concentrator": "VPN_toronto", "port":"te8/15"},
5   ]</pre>
      </div>
    </div>""",
            "choices": [
                "array",
                "value",
                "key",
                "object",
            ],
        },
        {
            "slug": "security-user-awareness-email-sensitive-leak",
            "title": "CCNA — User awareness vs email leaks",
            "stem": "Which **security program element** helps protect against employees **unintentionally leaking sensitive information** via **email**?",
            "name": "secaware1",
            "correct": "B",
            "explain": "Correct. B \u2014 **User awareness campaigns** teach safe handling of **sensitive data** (classification, correct recipients, Bcc vs Reply All, phishing recognition) so **accidental email disclosure** is less likely. **A** (**screen recordings**) is invasive monitoring, not the standard **security program** element for preventing mistaken email leaks. **C** (**controlled internet access**) limits web browsing/downloads but does not directly stop users from emailing sensitive content to the wrong party. **D** (**physical access controls**) protect **facilities** and **badged entry**, not **email** misuse.",
            "choices": [
                "workstation screen recordings",
                "user awareness campaigns",
                "controlled internet access",
                "physical access controls",
            ],
        },
        {
            "slug": "syslog-logging-facility-purpose-process",
            "title": "CCNA — Purpose of logging facility",
            "stem": "What is the purpose of the **logging facility**?",
            "name": "sysfac2",
            "correct": "A",
            "explain": "Correct. A \u2014 The **facility** field in a **syslog** message identifies the **program or process** (subsystem) that generated the event (for example **KERNEL**, **LINE**, **LOCAL0\u2013LOCAL7** on Cisco IOS). **B** is the **message text** (description). **C** is **severity** (**level**: emergency through debug). **D** is the **timestamp** (when the event occurred).",
            "choices": [
                "It indicates the program or process that generated the syslog event.",
                "It contains the text message that describes the syslog event.",
                "It defines the severity of the syslog event.",
                "It represents the timestamp of the syslog event.",
            ],
        },
        {
            "slug": "ap-bridge-mode-wireless-two-network-segments",
            "title": "CCNA — AP bridge mode between segments",
            "stem": "Which **AP mode** provides a **wireless connection** between **two network segments**?",
            "name": "apbrseg1",
            "correct": "D",
            "explain": "Correct. D \u2014 **Bridge** mode uses APs as **wireless bridges** (for example **root** and **non-root** roles) to link **two wired LAN segments** where fiber/copper is impractical. **A** (**root**) is a **role** inside **bridge** mode, not the mode name itself. **B** (**local**) serves **WLAN clients** through a **WLC** with **CAPWAP**, not segment-to-segment bridging. **C** (**FlexConnect**) provides **branch local switching** under central WLC control, not wireless bridging between two building LANs.",
            "choices": [
                "root",
                "local",
                "FlexConnect",
                "bridge",
            ],
        },
        {
            "slug": "dns-cname-alias-canonical-domain",
            "title": "CCNA — DNS CNAME record purpose",
            "stem": "What is the purpose of a **CNAME** record?",
            "name": "dnscname1",
            "correct": "A",
            "explain": "Correct. A \u2014 A **CNAME** (**Canonical Name**) record creates an **alias** that points to another **canonical DNS name** (for example **www.example.com** \u2192 **server.example.com**). **B** is an **A** or **AAAA** record (name to **IP address**). **C** is an **NS** record (delegates **authoritative name servers** for a zone). **D** is an **MX** record (routes **email** to a **mail server**).",
            "choices": [
                "to associate an alias to a canonical domain name",
                "to map a domain name to an IP address",
                "to identify the authoritative name server for a domain",
                "to direct email to a mail server",
            ],
        },
        {
            "slug": "border-router-static-172-16-153-154-next-hop",
            "title": "CCNA — Static route LPM (exhibit)",
            "stem": "Refer to the exhibit. The static routes were implemented on the **border router**. What is the **next-hop IP address** for a **ping** sent to **172.16.153.154** from the border router?",
            "name": "brstat1",
            "correct": "D",
            "mono": True,
            "explain": "Correct. D \u2014 Use **longest-prefix match**. **172.16.153.154** matches **172.0.0.0/8**, **172.16.0.0/16**, and the default **0.0.0.0/0**; the most specific match is **172.16.0.0/16** \u2192 next hop **10.56.22.23**. **B** (**172.16.153.153/32**) matches only host **.153**, not **.154**. **A** (**122.16.153.0/24**) is the wrong **172** network. **C** (**172.0.0.0/8**) is less specific than **/16**.",
            "prepend_html": """    <div class="exhibit-stack">
      <div class="exhibit-router-cli" role="region" aria-label="Border router static routes">
        <pre>ip route 172.0.0.0 255.0.0.0 10.12.13.14
ip route 172.16.0.0 255.255.0.0 10.56.22.23
ip route 122.16.153.0 255.255.255.0 10.35.47.17
ip route 172.16.153.153 255.255.255.255 10.65.34.19
ip route 0.0.0.0 0.0.0.0 10.17.44.36</pre>
      </div>
    </div>""",
            "choices": [
                "10.35.47.17",
                "10.65.34.19",
                "10.12.13.14",
                "10.56.22.23",
            ],
        },
        {
            "slug": "router-switch-straight-through-cable",
            "title": "CCNA — Router to switch cable",
            "stem": "Which **cable type** must be used when connecting a **router** and **switch** together?",
            "name": "rtswcab1",
            "correct": "C",
            "explain": "Correct. C \u2014 A **straight-through** Ethernet cable connects **unlike** devices: a **router Ethernet port** behaves like an **end host (MDI)** and a **switch port** is **MDI-X**, so TX/RX pairs align (**1\u20131**, **2\u20132**, **3\u20133**, **6\u20136**). **Crossover** (**D**) is for **like** devices (switch\u2013switch, host\u2013host, router\u2013router) when **auto-MDI-X** is unavailable. **Console** (**A**) and **rollover** (**B**) cables are for **out-of-band management** (console port), not **Ethernet data** links between router and switch.",
            "choices": [
                "console",
                "rollover",
                "straight-through",
                "crossover",
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
    n_hub = sync_hub_all_slugs(chain)
    n_banks = math.ceil(n_hub / 100) if n_hub else 0
    print("Updated", HUB_JS.relative_to(ROOT), "—", n_hub, "hub slugs,", n_banks, "practice banks")
    manifest_script = ROOT / "scripts/build-ccna-practice-questions-manifest.py"
    if manifest_script.is_file():
        subprocess.run([sys.executable, str(manifest_script)], check=False, cwd=ROOT)


def _slugs_from_hub_js(text: str) -> list[str]:
    m = re.search(r"ALL_SLUGS\s*=\s*\[(.*?)\];", text, re.S)
    if not m:
        raise ValueError("ALL_SLUGS not found in ccna-practice-100-hub.js")
    return re.findall(r'"([^"]+)"', m.group(1))


def sync_hub_all_slugs(chain: list[dict]) -> int:
    """Keep ALL_SLUGS = hand-maintained prefix + chain slugs (portal banks slice by position)."""
    text = HUB_JS.read_text(encoding="utf-8")
    slugs = _slugs_from_hub_js(text)
    try:
        anchor = slugs.index(HUB_CHAIN_ANCHOR)
        prefix = slugs[: anchor + 1]
    except ValueError:
        prefix = slugs[:12]
    chain_slugs = [q["slug"] for q in chain]
    merged: list[str] = []
    seen: set[str] = set()
    for slug in prefix + chain_slugs:
        if slug in seen:
            continue
        seen.add(slug)
        merged.append(slug)
    inner = ",".join(json.dumps(s) for s in merged)
    new_text, n = re.subn(
        r"(window\.CCNA_PRACTICE_100\.ALL_SLUGS\s*=\s*\[)(.*?)(\];)",
        r"\1" + inner + r"\3",
        text,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise ValueError("Could not replace ALL_SLUGS in ccna-practice-100-hub.js")
    HUB_JS.write_text(new_text, encoding="utf-8")
    return len(merged)


if __name__ == "__main__":
    main()

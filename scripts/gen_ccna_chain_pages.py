#!/usr/bin/env python3
"""One-off generator for CCNA question HTML pages (inline template)."""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "public/CCNA-Study/CCNA_questions"

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
    .stem-note {
      margin: 0 0 18px;
      color: #b8c3d6;
      font-size: 0.95rem;
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
    .choice.mono {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.95rem;
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
  </style>"""


def page(
    *,
    title: str,
    slug: str,
    num: int,
    total: int,
    stem: str,
    select_note: str,
    choices_html: str,
    name: str,
    correct: str,
    explain: str,
    prev_slug: str | None,
    next_slug: str | None,
    mono_choices: bool = False,
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
  <main class="card">
    <h1>{stem}</h1>
    <p class="stem-note">Question {num} of {total} · {select_note}</p>

{choices_html}

    <div class="actions">
      <button id="resetBtn" type="button">Reset</button>
      <a class="home-link" href="/index.html">Home</a>
    </div>

    <div id="answerBox" class="answer" aria-live="polite"></div>

{nav}
  </main>

  <script>
    (function () {{
      var CORRECT = {json.dumps(correct)};
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
  </script>
</body>
</html>
"""


def choice_line(mono: bool, name: str, letter: str, text: str) -> str:
    cls = "choice mono" if mono else "choice"
    return f'    <label class="{cls}"><input type="radio" name="{name}" value="{letter}" />{letter}. {text}</label>'


def main() -> None:
    total = 25
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
            "stem": "Refer to the exhibit. What is the result if Gig1/11 receives an STP BPDU? Configuration: interface GigabitEthernet1/11 — switchport mode access — spanning-tree portfast — spanning-tree bpduguard enable.",
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
            "slug": "voice-data-vlan-access-ports-sw11",
            "title": "CCNA — Voice and data VLANs on access ports",
            "stem": "Refer to the exhibit. An administrator must configure interfaces Gi1/1 and Gi1/3 on switch SW11. PC-1 and PC-2 must be placed in the Data VLAN and Phone-1 must be placed in the Voice VLAN. Which configuration meets these requirements?",
            "name": "voicevlan",
            "correct": "C",
            "explain": "Correct. C — Option C: Gi1/1 access VLAN 8 for PC-1 (data). Gi1/3: switchport mode access, access VLAN 8 for the PC, voice VLAN 9 for the phone. Option A swaps voice and data on Gi1/3. B and D use switchport mode trunk on the phone port, which is not the usual access + voice VLAN pattern.",
            "choices": [
                "Option A (Gi1/1 access vlan 8; Gi1/3 access vlan 9, voice vlan 8)",
                "Option B (Gi1/1 access vlan 9; Gi1/3 mode trunk, voice 8, access 9)",
                "Option C (Gi1/1 access vlan 8; Gi1/3 access vlan 8, voice vlan 9)",
                "Option D (Gi1/1 access vlan 8; Gi1/3 mode trunk, voice 8, access 9)",
            ],
        },
        {
            "slug": "pat-vlan200-inside-source-overload",
            "title": "CCNA — PAT and NAT extended ACL",
            "stem": "Refer to the exhibit. Which configuration must be applied to the router so PAT translates addresses in VLAN 200 while devices on VLAN 100 use their own IP addresses? Choose the option letter that matches the correct full configuration block.",
            "name": "pat",
            "correct": "C",
            "explain": "Correct. C — The standard ACL for ip nat inside source list should permit only VLAN 200’s inside subnet (commonly 192.168.200.0/24 with wildcard 0.0.0.255 in lab items). VLAN 100 must not be permitted if it should bypass PAT. Options A/B reference 209.165.201.2 (not the inside range for the whole VLAN). B uses a subnet mask where a wildcard is required. D only matches a /27 unless the exhibit limits VLAN 200 to that block. Confirm the third octet against your exhibit (200 vs 100).",
            "choices": [
                "Option A (ACL permit 209.165.201.2 0.0.0.0; nat inside on Gi2/0/1.200; outside on Gi1/0/0)",
                "Option B (ACL permit 209.165.201.2 255.255.255.255; same NAT interfaces)",
                "Option C (ACL permit 192.168.100.0 0.0.0.255 — verify exhibit: often 192.168.200.0 for VLAN 200; same NAT interfaces)",
                "Option D (ACL permit 192.168.100.32 0.0.0.31; same NAT interfaces)",
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
    ]

    prev = "vty-access-list-ssh-secure"
    for idx, q in enumerate(chain):
        i = 13 + idx
        slug = q["slug"]
        ch_lines = "\n".join(
            choice_line(q.get("mono", False), q["name"], chr(ord("A") + j), t)
            for j, t in enumerate(q["choices"])
        )
        next_slug = chain[idx + 1]["slug"] if idx + 1 < len(chain) else None
        html = page(
            title=q["title"],
            slug=slug,
            num=i,
            total=total,
            stem=q["stem"],
            select_note="Select an answer — feedback appears immediately.",
            choices_html=ch_lines,
            name=q["name"],
            correct=q["correct"],
            explain=q["explain"],
            prev_slug=prev,
            next_slug=next_slug,
            mono_choices=q.get("mono", False),
        )
        (OUT / f"{slug}.html").write_text(html, encoding="utf-8")
        prev = slug

    print("Wrote", len(chain), "files under", OUT)


if __name__ == "__main__":
    main()

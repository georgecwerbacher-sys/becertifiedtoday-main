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
    stem: str,
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

{choices_html}

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
    cls = "choice mono" if mono else "choice"
    return f'    <label class="{cls}"><input type="radio" name="{name}" value="{letter}" />{letter}. {text}</label>'


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
    ]

    prev = "vty-access-list-ssh-secure"
    for idx, q in enumerate(chain):
        i = 13 + idx
        slug = q["slug"]
        next_slug = chain[idx + 1]["slug"] if idx + 1 < len(chain) else None
        if q.get("choose_two"):
            ch_lines = "\n".join(
                checkbox_choice_line(q["name"], chr(ord("A") + j), t)
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
            )
        (OUT / f"{slug}.html").write_text(html, encoding="utf-8")
        prev = slug

    print("Wrote", len(chain), "files under", OUT)


if __name__ == "__main__":
    main()

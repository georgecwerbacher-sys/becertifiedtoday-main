#!/usr/bin/env python3
"""Inject free-order engine wiring into CCNA *-test.html lab files."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LABS = ROOT / "public" / "CCNA-Study" / "CCNA_labs"

MARKER = "      // __CCNA_FREEORDER_TEST_WIRE__"

SNIPPETS: dict[str, str] = {
    "cli-lab-static-routing-test.html": """
      // __CCNA_FREEORDER_TEST_WIRE__
      var __fo = createStaticRoutingTestEngine({
        container: cliLabContainer,
        r1Baseline: SWITCH_SHOW_RUNNING_SNAPSHOT,
        r3Baseline: SWITCH3_SHOW_RUNNING_SNAPSHOT,
        checkBtn: document.getElementById("checkLabBtn"),
        labCheckEl: document.getElementById("labCheckResult"),
        passBanner: passBanner,
        passMsg: "[OK] Lab complete: static routes on R1 and R3.",
        pendingMsg: "Configure R1 and R3 in any order, then click Submit Lab.",
      });
      function __foCtx(line, append, setPrompt, matchShowRun) {
        return { line: line, normalize: normalize, append: append, setPrompt: setPrompt, matchShowRun: matchShowRun };
      }
      var __submitSwOrig = submitSw;
      submitSw = function () {
        var promptText = swPrompt.textContent;
        var line = swCmdline.value;
        var trimmed = String(line || "").trim();
        if (trimmed) appendSw("line-user", promptText + " " + expandInterfaceEcho(trimmed));
        pushLocalHistory(swCmdline, line);
        swCmdline.value = "";
        if (!trimmed) return;
        if (cliLabContainer.tryAppendIosHelp(line, appendSw, cliLabContainer.iosHelpOpts("router", promptText, ROUTER_CLI_HELP))) return;
        if (matchShowVersion(line)) { cliLabContainer.appendLabShowVersion(appendSw); return; }
        if (matchShowIpIntBrief(line)) { appendSw("line-showrun", SWITCH_SHOW_IP_INT_BRIEF); return; }
        __fo.submitR1(__foCtx(line, appendSw, function (t) { swPrompt.textContent = t; }, matchShowRun));
      };
      var __submitSw3Orig = submitSw3;
      submitSw3 = function () {
        var promptText = sw3Prompt.textContent;
        var line = sw3Cmdline.value;
        var trimmed = String(line || "").trim();
        if (trimmed) appendSw3("line-user", promptText + " " + expandInterfaceEcho(trimmed));
        pushLocalHistory(sw3Cmdline, line);
        sw3Cmdline.value = "";
        if (!trimmed) return;
        if (cliLabContainer.tryAppendIosHelp(line, appendSw3, cliLabContainer.iosHelpOpts("router", promptText, ROUTER_CLI_HELP))) return;
        if (matchShowVersion(line)) { cliLabContainer.appendLabShowVersion(appendSw3); return; }
        __fo.submitR3(__foCtx(line, appendSw3, function (t) { sw3Prompt.textContent = t; }, matchShowRun));
      };
      var __resetSwLabOrig = resetSwLab;
      resetSwLab = function () { __resetSwLabOrig(); __fo.reset(); };
""",
    "ipv4_ipv6_assign-test.html": """
      // __CCNA_FREEORDER_TEST_WIRE__
      var __fo = createIpv4Ipv6TestEngine({
        container: cliLabContainer,
        r1Baseline: SWITCH_SHOW_RUNNING_SNAPSHOT,
        r2Baseline: SWITCH2_SHOW_RUNNING_SNAPSHOT,
        checkBtn: document.getElementById("checkLabBtn"),
        labCheckEl: document.getElementById("labCheckResult"),
        passBanner: passBanner,
        passMsg: "[OK] Lab complete: IPv4/IPv6 addressing on R1 and R2.",
        pendingMsg: "Configure R1 and R2 in any order, then click Submit Lab.",
      });
      function __foCtx(line, append, setPrompt) {
        return { line: line, normalize: normalize, append: append, setPrompt: setPrompt, matchShowRun: matchShowRun };
      }
      var __submitSwOrig = submitSw;
      submitSw = function () {
        var promptText = swPrompt.textContent;
        var line = swCmdline.value;
        var trimmed = String(line || "").trim();
        if (trimmed) appendSw("line-user", promptText + " " + expandInterfaceEcho(trimmed));
        pushLocalHistory(swCmdline, line);
        swCmdline.value = "";
        if (!trimmed) return;
        if (cliLabContainer.tryAppendIosHelp(line, appendSw, cliLabContainer.iosHelpOpts("router", promptText, ROUTER_CLI_HELP))) return;
        if (matchShowVersion(line)) { cliLabContainer.appendLabShowVersion(appendSw); return; }
        __fo.submitR1(__foCtx(line, appendSw, function (t) { swPrompt.textContent = t; }));
      };
      var __submitSw2Orig = submitSw2;
      submitSw2 = function () {
        var promptText = sw2Prompt.textContent;
        var line = sw2Cmdline.value;
        var trimmed = String(line || "").trim();
        if (trimmed) appendSw2("line-user", promptText + " " + expandInterfaceEcho(trimmed));
        pushLocalHistory(sw2Cmdline, line);
        sw2Cmdline.value = "";
        if (!trimmed) return;
        if (cliLabContainer.tryAppendIosHelp(line, appendSw2, cliLabContainer.iosHelpOpts("router", promptText, ROUTER_CLI_HELP))) return;
        if (matchShowVersion(line)) { cliLabContainer.appendLabShowVersion(appendSw2); return; }
        __fo.submitR2(__foCtx(line, appendSw2, function (t) { sw2Prompt.textContent = t; }));
      };
      var __resetSwLabOrig = resetSwLab;
      resetSwLab = function () { __resetSwLabOrig(); __fo.reset(); };
""",
    "cli-lab-native_vlan_lacp-test.html": """
      // __CCNA_FREEORDER_TEST_WIRE__
      var __fo = createNativeVlanLacpTestEngine({
        container: cliLabContainer,
        hosts: [
          { id: "sw1", label: "SW1", baseline: SWITCH_SHOW_RUNNING_SNAPSHOT },
          { id: "sw2", label: "SW2", baseline: SWITCH2_SHOW_RUNNING_SNAPSHOT },
          { id: "sw3", label: "SW3", baseline: SWITCH3_SHOW_RUNNING_SNAPSHOT },
          { id: "sw4", label: "SW4", baseline: SWITCH4_SHOW_RUNNING_SNAPSHOT },
        ],
        required: [
          { deviceId: "sw1", label: "SW1", lines: [
            { ifName: "Ethernet0/0", line: "switchport trunk allowed vlan 5,6" },
            { ifName: "Ethernet0/1", line: "switchport trunk native vlan 77" },
          ]},
          { deviceId: "sw2", label: "SW2", lines: [
            { ifName: "Ethernet0/1", line: "switchport trunk native vlan 77" },
            { ifName: "Ethernet0/2", line: "switchport trunk allowed vlan 6" },
          ]},
          { deviceId: "sw3", label: "SW3", lines: [
            { ifName: "Ethernet0/0", line: "channel-group 34 mode active" },
            { ifName: "Ethernet0/1", line: "channel-group 34 mode active" },
          ]},
          { deviceId: "sw4", label: "SW4", lines: [
            { ifName: "Ethernet0/0", line: "channel-group 34 mode passive" },
            { ifName: "Ethernet0/1", line: "channel-group 34 mode passive" },
          ]},
        ],
        checkBtn: document.getElementById("checkLabBtn"),
        labCheckEl: document.getElementById("labCheckResult"),
        passBanner: passBanner,
        passMsg: "[OK] Lab complete: native VLAN and LACP tasks on all four switches.",
        pendingMsg: "Configure all switches in any order, then click Submit Lab.",
      });
      function __foSwCtx(line, append, setPrompt) {
        return { line: line, normalize: normalize, append: append, setPrompt: setPrompt, matchShowRun: matchShowRun };
      }
      var __submitSwOrig = submitSw;
      submitSw = function () {
        var dev = getLabDev();
        var id = dev === "SW3" ? "sw3" : "sw1";
        var promptText = swPrompt.textContent;
        var line = swCmdline.value;
        var trimmed = String(line || "").trim();
        if (trimmed) appendSw("line-user", promptText + " " + expandInterfaceEcho(trimmed));
        pushLocalHistory(swCmdline, line);
        swCmdline.value = "";
        if (!trimmed) return;
        if (cliLabContainer.tryAppendIosHelp(line, appendSw, cliLabContainer.iosHelpOpts("switch", promptText, SWITCH_CLI_HELP))) return;
        __fo["submit_" + id](__foSwCtx(line, appendSw, function (t) { swPrompt.textContent = t; }));
      };
      var __submitSw2Orig = submitSw2;
      submitSw2 = function () {
        var dev = getLabDev();
        var id = dev === "SW4" ? "sw4" : "sw2";
        var promptText = sw2Prompt.textContent;
        var line = sw2Cmdline.value;
        var trimmed = String(line || "").trim();
        if (trimmed) appendSw2("line-user", promptText + " " + expandInterfaceEcho(trimmed));
        pushLocalHistory(sw2Cmdline, line);
        sw2Cmdline.value = "";
        if (!trimmed) return;
        if (cliLabContainer.tryAppendIosHelp(line, appendSw2, cliLabContainer.iosHelpOpts("switch", promptText, SWITCH_CLI_HELP))) return;
        __fo["submit_" + id](__foSwCtx(line, appendSw2, function (t) { sw2Prompt.textContent = t; }));
      };
      var __resetSwLabOrig = resetSwLab;
      resetSwLab = function () { __resetSwLabOrig(); __fo.reset(); };
""",
    "cli-lab-named-acl-snoopimg-test.html": """
      // __CCNA_FREEORDER_TEST_WIRE__
      var __fo = createNamedAclTestEngine({
        container: cliLabContainer,
        sw1Baseline: SWITCH_SHOW_RUNNING_SNAPSHOT,
        r1Baseline: SWITCH2_SHOW_RUNNING_SNAPSHOT,
        sw3Baseline: SWITCH3_SHOW_RUNNING_SNAPSHOT,
        checkBtn: document.getElementById("checkLabBtn"),
        labCheckEl: document.getElementById("labCheckResult"),
        passBanner: passBanner,
        passMsg: "[OK] Lab complete: DHCP snooping, ACL, and Sw3 user tasks.",
        pendingMsg: "Configure Sw1, R1, and Sw3 in any order, then click Submit Lab.",
      });
      function __foCtx(line, append, setPrompt) {
        return { line: line, normalize: normalize, append: append, setPrompt: setPrompt, matchShowRun: matchShowRun };
      }
      var __submitSwOrig = submitSw;
      submitSw = function () {
        var line = swCmdline.value;
        var trimmed = String(line || "").trim();
        if (trimmed) appendSw("line-user", swPrompt.textContent + " " + expandInterfaceEcho(trimmed));
        pushLocalHistory(swCmdline, line);
        swCmdline.value = "";
        if (!trimmed) return;
        __fo.submitSw1(__foCtx(line, appendSw, function (t) { swPrompt.textContent = t; }));
      };
      var __submitSw2Orig = submitSw2;
      submitSw2 = function () {
        var line = sw2Cmdline.value;
        var trimmed = String(line || "").trim();
        if (trimmed) appendSw2("line-user", sw2Prompt.textContent + " " + expandInterfaceEcho(trimmed));
        pushLocalHistory(sw2Cmdline, line);
        sw2Cmdline.value = "";
        if (!trimmed) return;
        __fo.submitR1(__foCtx(line, appendSw2, function (t) { sw2Prompt.textContent = t; }));
      };
      var __submitSw3Orig = submitSw3;
      submitSw3 = function () {
        var line = sw3Cmdline.value;
        var trimmed = String(line || "").trim();
        if (trimmed) appendSw3("line-user", sw3Prompt.textContent + " " + expandInterfaceEcho(trimmed));
        pushLocalHistory(sw3Cmdline, line);
        sw3Cmdline.value = "";
        if (!trimmed) return;
        __fo.submitSw3(__foCtx(line, appendSw3, function (t) { sw3Prompt.textContent = t; }));
      };
      var __resetSwLabOrig = resetSwLab;
      resetSwLab = function () { __resetSwLabOrig(); __fo.reset(); };
""",
    "cli-lab-trunk_lacp-test.html": """
      // __CCNA_FREEORDER_TEST_WIRE__
      var __fo = createTrunkLacpTestEngine({
        container: cliLabContainer,
        sw1Baseline: SWITCH_SHOW_RUNNING_SNAPSHOT,
        sw2Baseline: SWITCH2_SHOW_RUNNING_SNAPSHOT,
        checkBtn: document.getElementById("checkLabBtn"),
        labCheckEl: document.getElementById("labCheckResult"),
        passBanner: passBanner,
        passMsg: "[OK] Lab complete: trunks, VLANs, and LACP on Sw1 and Sw2.",
        pendingMsg: "Configure both switches in any order, then click Submit Lab.",
      });
      function __foSwCtx(line, append, setPrompt) {
        return { line: line, normalize: normalize, append: append, setPrompt: setPrompt, matchShowRun: matchShowRun };
      }
      var __submitSwOrig = submitSw;
      submitSw = function () {
        var line = swCmdline.value;
        var trimmed = String(line || "").trim();
        if (trimmed) appendSw("line-user", swPrompt.textContent + " " + expandInterfaceEcho(trimmed));
        pushLocalHistory(swCmdline, line);
        swCmdline.value = "";
        if (!trimmed) return;
        if (cliLabContainer.tryAppendIosHelp(line, appendSw, cliLabContainer.iosHelpOpts("switch", swPrompt.textContent, SWITCH_CLI_HELP))) return;
        __fo.submitSw1(__foSwCtx(line, appendSw, function (t) { swPrompt.textContent = t; }));
      };
      var __submitSw2Orig = submitSw2;
      submitSw2 = function () {
        var line = sw2Cmdline.value;
        var trimmed = String(line || "").trim();
        if (trimmed) appendSw2("line-user", sw2Prompt.textContent + " " + expandInterfaceEcho(trimmed));
        pushLocalHistory(sw2Cmdline, line);
        sw2Cmdline.value = "";
        if (!trimmed) return;
        if (cliLabContainer.tryAppendIosHelp(line, appendSw2, cliLabContainer.iosHelpOpts("switch", sw2Prompt.textContent, SWITCH_CLI_HELP))) return;
        __fo.submitSw2(__foSwCtx(line, appendSw2, function (t) { sw2Prompt.textContent = t; }));
      };
      var __resetSwLabOrig = resetSwLab;
      resetSwLab = function () { __resetSwLabOrig(); __fo.reset(); };
""",
}


def inject(path: Path, snippet: str) -> None:
    text = path.read_text(encoding="utf-8")
    if MARKER.strip() in text:
        print(f"skip wired {path.name}")
        return
    # Insert before final reset call in IIFE
    patterns = [
        r"(\n      resetSwLab\(\);\n    }\)\(\);)",
        r"(\n      resetSwLab\(\);\n    }\)\(\);\n)",
    ]
    for pat in patterns:
        if re.search(pat, text):
            text = re.sub(pat, "\n" + snippet + r"\1", text, count=1)
            path.write_text(text, encoding="utf-8")
            print(f"wired {path.name}")
            return
    print(f"FAILED no anchor in {path.name}")


def main() -> None:
    for name, snippet in SNIPPETS.items():
        inject(LABS / name, snippet)


if __name__ == "__main__":
    main()

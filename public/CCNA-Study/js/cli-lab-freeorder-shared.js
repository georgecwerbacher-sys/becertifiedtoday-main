/**
 * Shared helpers for CCNA free-order CLI labs (running-config merge + Submit Lab).
 */
(function (global) {
  "use strict";

  function runningConfigHasLine(view, line) {
    return view.render().toLowerCase().indexOf(String(line || "").trim().toLowerCase()) !== -1;
  }

  function ifBlockHasLine(rendered, ifName, line) {
    var text = String(rendered || "");
    var label = String(ifName || "").trim();
    var escaped = label.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    var header = label.toLowerCase().indexOf("line ") === 0 ? escaped : "interface\\s+" + escaped;
    var ifRe = new RegExp(header + "[\\s\\S]*?(?=\\ninterface |\\nline |\\nend\\r?\\n|$)", "i");
    var m = ifRe.exec(text);
    if (!m) return false;
    return m[0].toLowerCase().indexOf(String(line || "").trim().toLowerCase()) !== -1;
  }

  function capitalizeEthernet(ifName) {
    var m = /^(ethernet)(\d+\/\d+)$/i.exec(String(ifName || "").trim());
    if (m) return "Ethernet" + m[2];
    return String(ifName || "").trim();
  }

  function parseSingleInterface(u) {
    var m = /^interface\s+(ethernet\d+\/\d+)$/i.exec(u);
    if (m) return capitalizeEthernet(m[1]);
    m = /^interface\s+(e\d+\/\d+)$/i.exec(u);
    if (m) return capitalizeEthernet("ethernet" + m[1].slice(1));
    m = /^interface\s+(gigabitethernet\d+\/\d+)$/i.exec(u);
    if (m) return "GigabitEthernet" + m[1].slice("gigabitethernet".length);
    m = /^interface\s+(gi\d+\/\d+)$/i.exec(u);
    if (m) return "GigabitEthernet" + m[1].slice(2);
    m = /^interface\s+(port-channel\d+)$/i.exec(u);
    if (m) return "Port-channel" + m[1].slice("port-channel".length);
    return null;
  }

  function routerPromptForMode(host, mode) {
    switch (mode) {
      case "exec":
        return host + "#";
      case "config":
        return host + "(config)#";
      case "config-if":
        return host + "(config-if)#";
      case "config-if-range":
        return host + "(config-if-range)#";
      case "config-router":
        return host + "(config-router)#";
      case "config-std-nacl":
        return host + "(config-std-nacl)#";
      case "config-ext-nacl":
        return host + "(config-ext-nacl)#";
      case "config-line":
        return host + "(config-line)#";
      case "config-vlan":
        return host + "(config-vlan)#";
      default:
        return host + "#";
    }
  }

  function switchPromptForMode(host, mode) {
    return routerPromptForMode(host, mode);
  }

  function handleRouterModeNavigation(state, u, setMode) {
    if (state.mode === "exec" && u === "configure terminal") {
      setMode("config");
      return true;
    }
    if (u === "end" && state.mode !== "exec") {
      state.activeIf = null;
      state.activeIfs = [];
      state.currentVlanId = null;
      setMode("exec");
      return true;
    }
    if (u !== "exit") {
      if (u.indexOf("interface range ") === 0) {
        state.activeIfs = parseInterfaceRange(u) || [];
        state.activeIf = null;
        setMode(state.activeIfs.length ? "config-if-range" : "config-if");
        return true;
      }
      if (
        (state.mode === "config" ||
          state.mode === "config-if" ||
          state.mode === "config-if-range" ||
          state.mode === "config-vlan") &&
        u.indexOf("interface ") === 0
      ) {
        var single = parseSingleInterface(u);
        if (single) {
          state.activeIf = single;
          state.activeIfs = [single];
          setMode("config-if");
          return true;
        }
      }
      if (state.mode === "config" && /^router ospf \d+$/.test(u)) {
        setMode("config-router");
        return true;
      }
      if (state.mode === "config" && /^ip access-list standard /.test(u)) {
        setMode("config-std-nacl");
        return true;
      }
      if (state.mode === "config" && /^ip access-list extended /.test(u)) {
        setMode("config-ext-nacl");
        return true;
      }
      if (state.mode === "config" && /^line vty /.test(u)) {
        setMode("config-line");
        return true;
      }
      var vlanM = /^vlan (\d+)$/.exec(u);
      if ((state.mode === "config" || state.mode === "config-vlan") && vlanM) {
        state.currentVlanId = vlanM[1];
        setMode("config-vlan");
        return true;
      }
      return false;
    }
    if (state.mode === "exec") return false;
    if (
      state.mode === "config-router" ||
      state.mode === "config-std-nacl" ||
      state.mode === "config-ext-nacl" ||
      state.mode === "config-line"
    ) {
      setMode("config");
      return true;
    }
    if (state.mode === "config-vlan") {
      state.currentVlanId = null;
      setMode("config");
      return true;
    }
    if (state.mode === "config-if" || state.mode === "config-if-range") {
      state.activeIf = null;
      state.activeIfs = [];
      setMode("config");
      return true;
    }
    if (state.mode === "config") {
      setMode("exec");
      return true;
    }
    return false;
  }

  function parseInterfaceRange(u) {
    var body = u.slice("interface range ".length);
    if (/gigabitethernet0\/1\s*-\s*2/i.test(body) || /gi0\/1\s*-\s*2/i.test(body)) {
      return ["GigabitEthernet0/1", "GigabitEthernet0/2"];
    }
    if (/ethernet0\/0\s*-\s*1/i.test(body) || /e0\/0\s*-\s*1/i.test(body)) {
      return ["Ethernet0/0", "Ethernet0/1"];
    }
    return null;
  }

  function showLabCheckResult(el, passBanner, result, passMsg) {
    if (!el) return;
    el.classList.add("visible");
    el.classList.remove("is-pass", "is-fail");
    if (result.ok) {
      el.classList.add("is-pass");
      el.innerHTML = "<strong>Lab passed.</strong> " + (result.passHtml || "Running-config meets all lab requirements.");
      if (passBanner) {
        passBanner.classList.add("visible");
        passBanner.textContent = passMsg;
      }
    } else {
      el.classList.add("is-fail");
      el.innerHTML =
        "<strong>Not complete yet.</strong> Missing from running-config:<ul>" +
        result.missing
          .map(function (item) {
            return "<li>" + item + "</li>";
          })
          .join("") +
        "</ul>";
    }
    return result.ok;
  }

  function resetLabCheckUi(el, passBanner, pendingMsg) {
    if (passBanner) {
      passBanner.classList.remove("visible");
      passBanner.textContent = pendingMsg;
    }
    if (el) {
      el.classList.remove("visible", "is-pass", "is-fail");
      el.innerHTML = "";
    }
  }

  /** Record IOS-shaped lab commands as typed; Submit Lab checks exact requirements. */
  function tryRecordRouterOspf(view, u) {
    if (!/^router ospf \d+$/.test(u)) return false;
    view.applyGlobal(u);
    return true;
  }

  function tryRecordRouterId(view, u) {
    var m = /^router-id (\S+)$/.exec(u);
    if (!m) return false;
    view.applyGlobal(" router-id " + m[1]);
    return true;
  }

  function tryRecordIpOspfArea(view, ifName, u) {
    if (!ifName || !/^ip ospf \d+ area \d+$/.test(u)) return false;
    view.applyInterface(ifName, u);
    return true;
  }

  function tryRecordIpOspfPriority(view, ifName, u) {
    if (!ifName || !/^ip ospf priority \d+$/.test(u)) return false;
    view.applyInterface(ifName, u);
    return true;
  }

  function tryRecordIpRoute(view, u) {
    if (!/^ip route /.test(u)) return false;
    view.applyGlobal(u);
    return true;
  }

  function tryRecordIpAddress(view, ifName, u) {
    if (!ifName || !/^ip address \S+ \S+$/.test(u)) return false;
    view.applyInterface(ifName, u);
    return true;
  }

  function tryRecordIpv6Address(view, ifName, u) {
    if (!ifName || !/^ipv6 address \S+$/.test(u)) return false;
    view.applyInterface(ifName, u);
    return true;
  }

  function tryRecordSwitchport(view, ifName, u) {
    if (!ifName || u.indexOf("switchport ") !== 0) return false;
    view.applyInterface(ifName, u);
    return true;
  }

  function tryRecordSwitchportOnIfs(view, ifNames, u) {
    if (!ifNames || !ifNames.length || u.indexOf("switchport ") !== 0) return false;
    ifNames.forEach(function (ifName) {
      view.applyInterface(ifName, u);
    });
    return true;
  }

  function tryRecordChannelGroup(view, ifNames, u) {
    if (!ifNames || !ifNames.length || !/^channel-group \d+ mode (active|passive|on)$/.test(u)) return false;
    ifNames.forEach(function (ifName) {
      view.applyInterface(ifName, u);
    });
    return true;
  }

  function tryRecordChannelProtocol(view, ifNames, u) {
    if (!ifNames || !ifNames.length || !/^channel-protocol (lacp|pagp)$/.test(u)) return false;
    ifNames.forEach(function (ifName) {
      view.applyInterface(ifName, u);
    });
    return true;
  }

  function tryRecordVlan(view, u) {
    if (!/^vlan \d+$/.test(u)) return false;
    view.applyGlobal(u);
    return true;
  }

  function tryRecordAclAce(view, u) {
    if (!/^(permit|deny) /.test(u)) return false;
    view.applyGlobal(u.charAt(0) === " " ? u : " " + u);
    return true;
  }

  function tryRecordIpAccessGroup(view, ifName, u) {
    var m = /^ip access-group (\S+) (in|out)$/.exec(u);
    if (!ifName || !m) return false;
    view.applyInterface(ifName, u);
    return true;
  }

  function tryRecordIpDhcpSnoopingGlobal(view, u) {
    if (u.indexOf("ip dhcp snooping") !== 0 && u.indexOf("no ip dhcp snooping") !== 0) return false;
    view.applyGlobal(u);
    return true;
  }

  function tryRecordIpNatIf(view, ifName, u) {
    if (!ifName || (u !== "ip nat inside" && u !== "ip nat outside")) return false;
    view.applyInterface(ifName, u);
    return true;
  }

  function tryRecordIpNatPool(view, u) {
    if (u.indexOf("ip nat pool ") !== 0) return false;
    view.applyGlobal(u);
    return true;
  }

  function tryRecordIpNatInsideSource(view, u) {
    if (u.indexOf("ip nat inside source ") !== 0) return false;
    view.applyGlobal(u);
    return true;
  }

  function tryRecordIpAccessListStandard(view, u) {
    if (!/^ip access-list standard \S+$/.test(u)) return false;
    view.applyGlobal(u);
    return true;
  }

  function tryRecordStdNaclPermit(view, u) {
    if (!/^permit /.test(u)) return false;
    view.applyGlobal(" " + u);
    return true;
  }

  function tryRecordUsername(view, u) {
    if (!/^username /.test(u)) return false;
    view.applyGlobal(u);
    return true;
  }

  function tryRecordLineVty(view, u) {
    if (!/^line vty /.test(u)) return false;
    view.applyGlobal(u);
    return true;
  }

  function tryRecordLineVtySubcmd(view, u) {
    if (u !== "login local" && u !== "transport input telnet" && u !== "transport input ssh" && u.indexOf("transport input ") !== 0) {
      return false;
    }
    view.applyInterface("line vty 0 4", u);
    return true;
  }

  function handleCopyRunStart(mode, u, append, container) {
    if (u !== "copy running-configuration startup-configuration") return false;
    if (mode !== "exec") {
      append("line-bad", container.INVALID_INPUT_MSG);
      return true;
    }
    append("line-sys", container.COPY_RUN_START_OK_MSG);
    return true;
  }

  global.CcnaFreeOrderShared = {
    runningConfigHasLine: runningConfigHasLine,
    ifBlockHasLine: ifBlockHasLine,
    capitalizeEthernet: capitalizeEthernet,
    parseSingleInterface: parseSingleInterface,
    parseInterfaceRange: parseInterfaceRange,
    routerPromptForMode: routerPromptForMode,
    switchPromptForMode: switchPromptForMode,
    handleRouterModeNavigation: handleRouterModeNavigation,
    showLabCheckResult: showLabCheckResult,
    resetLabCheckUi: resetLabCheckUi,
    handleCopyRunStart: handleCopyRunStart,
    tryRecordRouterOspf: tryRecordRouterOspf,
    tryRecordRouterId: tryRecordRouterId,
    tryRecordIpOspfArea: tryRecordIpOspfArea,
    tryRecordIpOspfPriority: tryRecordIpOspfPriority,
    tryRecordIpRoute: tryRecordIpRoute,
    tryRecordIpAddress: tryRecordIpAddress,
    tryRecordIpv6Address: tryRecordIpv6Address,
    tryRecordSwitchport: tryRecordSwitchport,
    tryRecordSwitchportOnIfs: tryRecordSwitchportOnIfs,
    tryRecordChannelGroup: tryRecordChannelGroup,
    tryRecordChannelProtocol: tryRecordChannelProtocol,
    tryRecordVlan: tryRecordVlan,
    tryRecordAclAce: tryRecordAclAce,
    tryRecordIpAccessGroup: tryRecordIpAccessGroup,
    tryRecordIpDhcpSnoopingGlobal: tryRecordIpDhcpSnoopingGlobal,
    tryRecordIpNatIf: tryRecordIpNatIf,
    tryRecordIpNatPool: tryRecordIpNatPool,
    tryRecordIpNatInsideSource: tryRecordIpNatInsideSource,
    tryRecordIpAccessListStandard: tryRecordIpAccessListStandard,
    tryRecordStdNaclPermit: tryRecordStdNaclPermit,
    tryRecordUsername: tryRecordUsername,
    tryRecordLineVty: tryRecordLineVty,
    tryRecordLineVtySubcmd: tryRecordLineVtySubcmd,
  };
})(typeof window !== "undefined" ? window : globalThis);

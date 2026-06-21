/**
 * Free-order VLAN lab engine — running-config merge + Submit Lab validation.
 * Used by cli-lab-vlan-sim.html (homepage sample lab).
 */
(function (global) {
  "use strict";

  var EXPECTED_VLAN_NAMES = {
    "77": "IT_User_VLAN",
    "88": "HR_User_VLAN",
    "177": "IT_Voice_VLAN",
    "188": "HR_Voice_VLAN",
  };

  var SW1_IF_REQUIRED = {
    "Ethernet0/1": { modeAccess: true, accessVlan: "77", voiceVlan: "177" },
    "Ethernet0/2": { modeAccess: true, accessVlan: "77" },
    "Ethernet0/3": { modeAccess: true, accessVlan: "88", voiceVlan: "188" },
  };

  var SW2_IF_REQUIRED = {
    "Ethernet0/3": { modeAccess: true, accessVlan: "77" },
    "Ethernet0/1": { modeAccess: true, accessVlan: "88", voiceVlan: "188" },
    "Ethernet0/2": { voiceVlan: "177" },
  };

  function emptyLabState() {
    return { vlanNames: {}, ifState: {}, currentVlanId: null, activeIfs: [] };
  }

  function capitalizeEthernet(ifName) {
    var m = /^(ethernet)(\d+\/\d+)$/i.exec(String(ifName || "").trim());
    if (m) return "Ethernet" + m[2];
    return String(ifName || "").trim();
  }

  function parseInterfaceTargets(u) {
    if (u.indexOf("interface range ") === 0) {
      var body = u.slice("interface range ".length);
      if (/gigabitethernet0\/1\s*-\s*2/.test(body) || /ethernet0\/1\s*-\s*2/.test(body)) {
        return ["Ethernet0/1", "Ethernet0/2"];
      }
      if (/e0\/1\s*-\s*2/.test(body)) {
        return ["Ethernet0/1", "Ethernet0/2"];
      }
      if (/e0\/1\s*-\s*2\s*,\s*e0\/3/.test(body) || /ethernet0\/1\s*-\s*2\s*,\s*ethernet0\/3/.test(body)) {
        return ["Ethernet0/1", "Ethernet0/2", "Ethernet0/3"];
      }
    }
    var m = /^interface\s+(ethernet\d+\/\d+)$/.exec(u);
    if (m) return [capitalizeEthernet(m[1])];
    m = /^interface\s+(e\d+\/\d+)$/.exec(u);
    if (m) return [capitalizeEthernet("ethernet" + m[1].slice(1))];
    return null;
  }

  function isVlanLabInterfaceNavMode(mode) {
    return mode === "config" || mode === "config-vlan" || mode === "config-if" || mode === "config-if-range";
  }

  function isPermissiveLldpGlobal(u) {
    return u === "lldp run" || u === "no lldp run";
  }

  function isPermissiveLldpIf(u) {
    return u === "lldp transmit" || u === "no lldp transmit" || u === "lldp receive" || u === "no lldp receive";
  }

  function isPermissiveCdpIf(u) {
    return u === "no cdp enable" || u === "cdp enable" || u === "no cdp run" || u === "cdp run";
  }

  function renderShowRun(view, vlanNames) {
    var base = view.render();
    var ids = Object.keys(vlanNames || {}).sort(function (a, b) {
      return parseInt(a, 10) - parseInt(b, 10);
    });
    if (!ids.length) return base;
    var blocks = [];
    for (var i = 0; i < ids.length; i++) {
      blocks.push("vlan " + ids[i]);
      blocks.push(" name " + vlanNames[ids[i]]);
      blocks.push("!");
    }
    var blockText = blocks.join("\r\n");
    if (/\r?\nend\r?\n?$/i.test(base)) {
      return base.replace(/\r?\nend\r?\n?$/i, "\r\n" + blockText + "\r\nend");
    }
    return base + "\r\n" + blockText + "\r\nend";
  }

  function touchIf(state, ifKey) {
    if (!state.ifState[ifKey]) state.ifState[ifKey] = {};
    return state.ifState[ifKey];
  }

  function recordSwitchport(state, ifKeys, u, view) {
    if (!ifKeys || !ifKeys.length) return false;
    var recorded = false;
    for (var i = 0; i < ifKeys.length; i++) {
      var key = ifKeys[i];
      var slot = touchIf(state, key);
      if (u === "switchport mode access") {
        slot.modeAccess = true;
        view.applyInterface(key, "switchport mode access");
        recorded = true;
      } else {
        var accessM = /^switchport access vlan (\d+)$/.exec(u);
        if (accessM) {
          slot.accessVlan = accessM[1];
          view.applyInterface(key, "switchport access vlan " + accessM[1]);
          recorded = true;
        } else {
          var voiceM = /^switchport voice vlan (\d+)$/.exec(u);
          if (voiceM) {
            slot.voiceVlan = voiceM[1];
            view.applyInterface(key, "switchport voice vlan " + voiceM[1]);
            recorded = true;
          }
        }
      }
    }
    return recorded;
  }

  function recordVlanName(state, vlanId, name) {
    if (!vlanId || !name) return;
    state.vlanNames[String(vlanId)] = name;
  }

  function ifStateMeets(required, actual) {
    if (!actual) return false;
    if (required.modeAccess && !actual.modeAccess) return false;
    if (required.accessVlan && String(actual.accessVlan) !== String(required.accessVlan)) return false;
    if (required.voiceVlan && String(actual.voiceVlan) !== String(required.voiceVlan)) return false;
    return true;
  }

  function checkVlanNames(host, names, missing) {
    Object.keys(EXPECTED_VLAN_NAMES).forEach(function (id) {
      if (names[id] !== EXPECTED_VLAN_NAMES[id]) {
        missing.push(host + ": vlan " + id + " name " + EXPECTED_VLAN_NAMES[id]);
      }
    });
  }

  function checkIfMap(host, required, actual, missing) {
    Object.keys(required).forEach(function (ifKey) {
      if (!ifStateMeets(required[ifKey], actual[ifKey])) {
        var req = required[ifKey];
        var parts = [host + ": " + ifKey];
        if (req.modeAccess) parts.push("switchport mode access");
        if (req.accessVlan) parts.push("switchport access vlan " + req.accessVlan);
        if (req.voiceVlan) parts.push("switchport voice vlan " + req.voiceVlan);
        missing.push(parts.join(" — "));
      }
    });
  }

  /**
   * @param {object} opts
   * @returns {object}
   */
  function createVlanSimEngine(opts) {
    var container = opts.container;
    var normalize = opts.normalize;
    var sw1View = container.createRunningConfigView(opts.sw1Baseline);
    var sw2View = container.createRunningConfigView(opts.sw2Baseline);
    var sw1Mode = "exec";
    var sw2Mode = "exec";
    var sw1 = emptyLabState();
    var sw2 = emptyLabState();
    var labCheckPassed = false;

    function promptForMode(host, mode) {
      switch (mode) {
        case "exec":
          return host + "#";
        case "config":
          return host + "(config)#";
        case "config-vlan":
          return host + "(config-vlan)#";
        case "config-if":
          return host + "(config-if)#";
        case "config-if-range":
          return host + "(config-if-range)#";
        default:
          return host + "#";
      }
    }

    function getLabCheckResult() {
      var missing = [];
      checkVlanNames(opts.sw1Host, sw1.vlanNames, missing);
      checkVlanNames(opts.sw2Host, sw2.vlanNames, missing);
      checkIfMap(opts.sw1Host, SW1_IF_REQUIRED, sw1.ifState, missing);
      checkIfMap(opts.sw2Host, SW2_IF_REQUIRED, sw2.ifState, missing);
      return { ok: missing.length === 0, missing: missing };
    }

    function showLabCheckResult(result) {
      var el = opts.labCheckEl;
      if (!el) return;
      el.classList.add("visible");
      el.classList.remove("is-pass", "is-fail");
      if (result.ok) {
        el.classList.add("is-pass");
        el.innerHTML =
          "<strong>Lab passed.</strong> Running-config on Sw1 and Sw2 includes all required VLAN and interface assignments.";
        labCheckPassed = true;
        opts.passBanner.classList.add("visible");
        opts.passBanner.textContent = opts.passMsg;
        if (typeof global.bccNotifyCliLabComplete === "function") {
          global.bccNotifyCliLabComplete({ lab: "vlan-sim" });
        }
      } else {
        el.classList.add("is-fail");
        el.innerHTML =
          "<strong>Not complete yet.</strong> Missing from running-config (use <code>show running-config</code> on each switch):<ul>" +
          result.missing
            .map(function (item) {
              return "<li>" + item + "</li>";
            })
            .join("") +
          "</ul>";
      }
    }

    function reset() {
      sw1Mode = "exec";
      sw2Mode = "exec";
      sw1 = emptyLabState();
      sw2 = emptyLabState();
      labCheckPassed = false;
      sw1View.reset();
      sw2View.reset();
      opts.passBanner.classList.remove("visible");
      opts.passBanner.textContent = opts.pendingMsg;
      if (opts.labCheckEl) {
        opts.labCheckEl.classList.remove("visible", "is-pass", "is-fail");
        opts.labCheckEl.innerHTML = "";
      }
    }

    function handleModeNavigation(mode, lab, setMode, u, line, labVlanIds) {
      if (mode === "exec" && u === "configure terminal") {
        setMode("config");
        return true;
      }
      if (u === "end" && mode !== "exec") {
        lab.activeIfs = [];
        lab.currentVlanId = null;
        setMode("exec");
        return true;
      }
      if (u !== "exit") {
        if (isVlanLabInterfaceNavMode(mode) && u.indexOf("interface range ") === 0) {
          lab.activeIfs = parseInterfaceTargets(u) || [];
          setMode("config-if-range");
          return true;
        }
        if (isVlanLabInterfaceNavMode(mode) && u.indexOf("interface ") === 0) {
          var targets = parseInterfaceTargets(u);
          if (targets && targets.length) {
            lab.activeIfs = targets;
            setMode(targets.length > 1 ? "config-if-range" : "config-if");
            return true;
          }
        }
        var vlanM = /^vlan (\d+)$/.exec(u);
        if ((mode === "config" || mode === "config-vlan") && vlanM) {
          lab.currentVlanId = vlanM[1];
          setMode("config-vlan");
          return true;
        }
        var nameM = /^name\s+(\S+)$/.exec(u);
        if (mode === "config-vlan" && nameM) {
          recordVlanName(lab, lab.currentVlanId, nameM[1]);
          return true;
        }
        return false;
      }
      if (mode === "exec") return false;
      if (mode === "config-vlan") {
        lab.currentVlanId = null;
        setMode("config");
        return true;
      }
      if (mode === "config-if" || mode === "config-if-range") {
        lab.activeIfs = [];
        setMode("config");
        return true;
      }
      if (mode === "config") {
        setMode("exec");
        return true;
      }
      return false;
    }

    function submitSwitch(ctx) {
      var line = ctx.cmdline.value;
      var trimmed = String(line || "").trim();
      var u = normalize(line);
      var hideInputLine =
        u === "configure terminal" || u === "end" || u === "exit" || u.indexOf("interface ") === 0;
      var echoLine = opts.expandInterfaceEcho(trimmed);
      if (!hideInputLine || u.indexOf("interface ") === 0 || /^ethernet \d+\/\d+$/.test(u)) {
        ctx.append("line-user", ctx.promptEl.textContent + " " + echoLine);
      }
      ctx.cmdline.value = "";
      if (!trimmed) return;

      if (container.tryAppendIosHelp(line, ctx.append, container.iosHelpOpts("switch", ctx.promptEl.textContent, null))) {
        return;
      }

      if (ctx.matchShowRun(line)) {
        ctx.append("line-showrun", renderShowRun(ctx.view, ctx.lab.vlanNames));
        return;
      }
      if (ctx.matchShowHistory(line)) {
        ctx.append("line-showrun", ctx.formatHistory(ctx.cmdline));
        return;
      }
      if (ctx.mode === "exec" && ctx.matchShowVersion(line)) {
        container.appendLabShowVersion(ctx.append);
        return;
      }
      if (ctx.matchCopyRunStart(line)) {
        if (ctx.mode !== "exec") {
          ctx.append("line-bad", container.INVALID_INPUT_MSG);
          return;
        }
        ctx.append("line-sys", container.COPY_RUN_START_OK_MSG);
        return;
      }
      if (ctx.mode === "exec" && (u.indexOf("show ") === 0 || u.indexOf("sh ") === 0)) {
        ctx.append("line-sys", opts.showDisabledMsg);
        return;
      }

      if (
        handleModeNavigation(ctx.mode, ctx.lab, ctx.setMode, u, line, opts.labVlanIds)
      ) {
        return;
      }

      var active = ctx.lab.activeIfs && ctx.lab.activeIfs.length ? ctx.lab.activeIfs.slice() : [];
      if (recordSwitchport(ctx.lab, active, u, ctx.view)) {
        return;
      }
      if (ctx.mode === "config" && isPermissiveLldpGlobal(u)) return;
      if ((ctx.mode === "config-if" || ctx.mode === "config-if-range") && (isPermissiveLldpIf(u) || isPermissiveCdpIf(u))) {
        return;
      }

      ctx.append("line-bad", container.INVALID_INPUT_MSG);
    }

    return {
      reset: reset,
      getLabCheckResult: getLabCheckResult,
      showLabCheckResult: showLabCheckResult,
      sw1PromptForMode: function () {
        return promptForMode(opts.sw1Host, sw1Mode);
      },
      sw2PromptForMode: function () {
        return promptForMode(opts.sw2Host, sw2Mode);
      },
      submitSw1: function (ctx) {
        submitSwitch({
          mode: sw1Mode,
          lab: sw1,
          view: sw1View,
          setMode: function (m) {
            sw1Mode = m;
            ctx.setPrompt();
          },
          append: ctx.appendSw,
          promptEl: ctx.swPrompt,
          cmdline: ctx.swCmdline,
          matchShowRun: ctx.matchShowRun,
          matchShowHistory: ctx.matchShowHistory,
          matchShowVersion: ctx.matchShowVersion,
          matchCopyRunStart: ctx.matchCopyRunStart,
          formatHistory: ctx.formatHistory,
        });
      },
      submitSw2: function (ctx) {
        submitSwitch({
          mode: sw2Mode,
          lab: sw2,
          view: sw2View,
          setMode: function (m) {
            sw2Mode = m;
            ctx.setPrompt();
          },
          append: ctx.appendSw2,
          promptEl: ctx.sw2Prompt,
          cmdline: ctx.sw2Cmdline,
          matchShowRun: ctx.matchShowRun,
          matchShowHistory: ctx.matchShowHistory,
          matchShowVersion: ctx.matchShowVersion,
          matchCopyRunStart: ctx.matchCopyRunStart,
          formatHistory: ctx.formatHistory,
        });
      },
      isLabCheckPassed: function () {
        return labCheckPassed;
      },
    };
  }

  global.createVlanSimEngine = createVlanSimEngine;
})(typeof window !== "undefined" ? window : globalThis);

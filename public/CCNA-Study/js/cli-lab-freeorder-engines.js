/**
 * Free-order + Submit Lab engines for CCNA CLI lab TEST copies (*-test.html).
 * Production labs unchanged until promoted.
 */
(function (global) {
  "use strict";

  var S = global.CcnaFreeOrderShared;

  function wireSubmitLab(opts) {
    var btn = opts.checkBtn;
    if (!btn) return;
    btn.addEventListener("click", function () {
      var result = opts.getLabCheckResult();
      S.showLabCheckResult(opts.labCheckEl, opts.passBanner, result, opts.passMsg);
    });
  }

  /** OSPF lab — R1 only */
  function createOspfTestEngine(opts) {
    var view = opts.container.createRunningConfigView(opts.baseline);
    var mode = "exec";
    var pid = opts.processId;
    var routerId = opts.routerId;
    var drPri = opts.drPriority;

    function prompt() {
      return S.routerPromptForMode(opts.host, mode);
    }

    var state = { mode: "exec", activeIf: null, activeIfs: [] };

    function reset() {
      mode = "exec";
      state.mode = "exec";
      state.activeIf = null;
      state.activeIfs = [];
      view.reset();
      S.resetLabCheckUi(opts.labCheckEl, opts.passBanner, opts.pendingMsg);
    }

    function getLabCheckResult() {
      var missing = [];
      var run = view.render();
      if (!S.runningConfigHasLine(view, "router ospf " + pid)) {
        missing.push(opts.host + ": router ospf " + pid);
      }
      if (!S.runningConfigHasLine(view, "router-id " + routerId)) {
        missing.push(opts.host + ": router-id " + routerId);
      }
      ["Ethernet0/0", "Ethernet0/1"].forEach(function (ifName) {
        if (!S.ifBlockHasLine(run, ifName, "ip ospf " + pid + " area 0")) {
          missing.push(opts.host + ": " + ifName + " — ip ospf " + pid + " area 0");
        }
        if (!S.ifBlockHasLine(run, ifName, "ip ospf priority " + drPri)) {
          missing.push(opts.host + ": " + ifName + " — ip ospf priority " + drPri);
        }
      });
      return {
        ok: missing.length === 0,
        missing: missing,
        passHtml: "R1 OSPF process, router-id, and interface assignments are correct.",
      };
    }

    function setMode(m) {
      mode = m;
      state.mode = m;
      opts.setPrompt(prompt());
    }

    function syncModeFromPrompt() {
      if (opts.container && typeof opts.container.parsePromptMode === "function" && opts.getPromptText) {
        var parsed = opts.container.parsePromptMode(opts.getPromptText());
        if (parsed) {
          mode = parsed;
          state.mode = parsed;
        }
      }
    }

    function record(u) {
      if (state.mode === "config-router" && S.tryRecordRouterId(view, u)) return true;
      if (state.activeIf) {
        if (S.tryRecordIpOspfArea(view, state.activeIf, u)) return true;
        if (S.tryRecordIpOspfPriority(view, state.activeIf, u)) return true;
      }
      return false;
    }

    function submit(ctx) {
      syncModeFromPrompt();
      var u = ctx.normalize(ctx.line);
      if (ctx.isOspfNetwork && ctx.isOspfNetwork(u)) {
        ctx.append("line-sys", ctx.forbiddenNetworkMsg);
        return;
      }
      if (ctx.matchShowRun(ctx.line)) {
        ctx.append("line-showrun", view.render());
        return;
      }
      if (S.handleRouterModeNavigation(state, u, setMode)) {
        if (state.activeIfs && state.activeIfs.length) state.activeIf = state.activeIfs[0];
        if (u.indexOf("interface ") === 0) {
          var parsedIf = S.parseSingleInterface(u);
          if (parsedIf) state.activeIf = parsedIf;
        }
        if (/^router ospf \d+$/.test(u)) {
          S.tryRecordRouterOspf(view, u);
        }
        return;
      }
      if (S.handleCopyRunStart(mode, u, ctx.append, opts.container)) return;
      if (record(u)) return;
      ctx.append("line-bad", opts.container.INVALID_INPUT_MSG);
    }

    wireSubmitLab({
      checkBtn: opts.checkBtn,
      labCheckEl: opts.labCheckEl,
      passBanner: opts.passBanner,
      passMsg: opts.passMsg,
      getLabCheckResult: getLabCheckResult,
    });

    return { reset: reset, submit: submit, prompt: prompt, getLabCheckResult: getLabCheckResult };
  }

  /** Static routing — R1 + R3 */
  function createStaticRoutingTestEngine(opts) {
    var r1View = opts.container.createRunningConfigView(opts.r1Baseline);
    var r3View = opts.container.createRunningConfigView(opts.r3Baseline);
    var r1Mode = "exec";
    var r3Mode = "exec";
    var r1State = { mode: r1Mode, activeIf: null, activeIfs: [] };
    var r3State = { mode: r3Mode, activeIf: null, activeIfs: [] };

    var R1_ROUTES = [
      "ip route 10.0.41.10 255.255.255.255 10.0.12.2",
      "ip route 10.0.41.10 255.255.255.255 10.0.13.3 254",
      "ip route 0.0.0.0 0.0.0.0 10.0.13.3",
    ];
    var R3_ROUTE = "ip route 0.0.0.0 0.0.0.0 209.165.201.1";

    function reset() {
      r1Mode = r3Mode = "exec";
      r1State.mode = r3State.mode = "exec";
      r1View.reset();
      r3View.reset();
      S.resetLabCheckUi(opts.labCheckEl, opts.passBanner, opts.pendingMsg);
    }

    function getLabCheckResult() {
      var missing = [];
      R1_ROUTES.forEach(function (line) {
        if (!S.runningConfigHasLine(r1View, line)) missing.push("R1: " + line);
      });
      if (!S.runningConfigHasLine(r3View, R3_ROUTE)) missing.push("R3: " + R3_ROUTE);
      return {
        ok: missing.length === 0,
        missing: missing,
        passHtml: "Static routes on R1 and R3 are configured.",
      };
    }

    function recordRoute(view, u) {
      return S.tryRecordIpRoute(view, u);
    }

    function submitR1(ctx) {
      var u = ctx.normalize(ctx.line);
      if (ctx.matchShowRun(ctx.line)) {
        ctx.append("line-showrun", r1View.render());
        return;
      }
      function setMode(m) {
        r1Mode = m;
        r1State.mode = m;
        ctx.setPrompt(S.routerPromptForMode("R1", m));
      }
      if (S.handleRouterModeNavigation(r1State, u, setMode)) return;
      if (S.handleCopyRunStart(r1Mode, u, ctx.append, opts.container)) return;
      if (r1Mode === "config" && recordRoute(r1View, u)) return;
      ctx.append("line-bad", opts.container.INVALID_INPUT_MSG);
    }

    function submitR3(ctx) {
      var u = ctx.normalize(ctx.line);
      if (ctx.matchShowRun(ctx.line)) {
        ctx.append("line-showrun", r3View.render());
        return;
      }
      function setMode(m) {
        r3Mode = m;
        r3State.mode = m;
        ctx.setPrompt(S.routerPromptForMode("R3", m));
      }
      if (S.handleRouterModeNavigation(r3State, u, setMode)) return;
      if (S.handleCopyRunStart(r3Mode, u, ctx.append, opts.container)) return;
      if (r3Mode === "config" && S.tryRecordIpRoute(r3View, u)) return;
      ctx.append("line-bad", opts.container.INVALID_INPUT_MSG);
    }

    wireSubmitLab({
      checkBtn: opts.checkBtn,
      labCheckEl: opts.labCheckEl,
      passBanner: opts.passBanner,
      passMsg: opts.passMsg,
      getLabCheckResult: getLabCheckResult,
    });

    return {
      reset: reset,
      submitR1: submitR1,
      submitR3: submitR3,
      getLabCheckResult: getLabCheckResult,
    };
  }

  /** IPv4/IPv6 assignment — R1 + R2 */
  function createIpv4Ipv6TestEngine(opts) {
    var r1View = opts.container.createRunningConfigView(opts.r1Baseline);
    var r2View = opts.container.createRunningConfigView(opts.r2Baseline);
    var r1Mode = "exec";
    var r2Mode = "exec";
    var r1State = { mode: r1Mode, activeIf: null, activeIfs: [] };
    var r2State = { mode: r2Mode, activeIf: null, activeIfs: [] };
    var r1Flags = { v4: false, v6: false };
    var r2Flags = { v4: false, v6: false };

    var R1_V4 = "ip address 10.0.12.5 255.255.255.252";
    var R2_V4 = "ip address 10.0.12.6 255.255.255.252";
    var R1_V6 = "ipv6 address 2001:db8:12::11/126";
    var R2_V6 = "ipv6 address 2001:db8:12::13/126";

    function reset() {
      r1Mode = r2Mode = "exec";
      r1View.reset();
      r2View.reset();
      r1Flags = { v4: false, v6: false };
      r2Flags = { v4: false, v6: false };
      S.resetLabCheckUi(opts.labCheckEl, opts.passBanner, opts.pendingMsg);
    }

    function getLabCheckResult() {
      var missing = [];
      var r1 = r1View.render();
      var r2 = r2View.render();
      if (!S.ifBlockHasLine(r1, "Ethernet0/0", R1_V4)) missing.push("R1: Ethernet0/0 — " + R1_V4);
      if (!S.ifBlockHasLine(r2, "Ethernet0/0", R2_V4)) missing.push("R2: Ethernet0/0 — " + R2_V4);
      if (!S.runningConfigHasLine(r1View, "ipv6 unicast-routing")) missing.push("R1: ipv6 unicast-routing");
      if (!S.runningConfigHasLine(r2View, "ipv6 unicast-routing")) missing.push("R2: ipv6 unicast-routing");
      if (!S.ifBlockHasLine(r1, "Ethernet0/0", R1_V6)) missing.push("R1: Ethernet0/0 — " + R1_V6);
      if (!S.ifBlockHasLine(r2, "Ethernet0/0", R2_V6)) missing.push("R2: Ethernet0/0 — " + R2_V6);
      return {
        ok: missing.length === 0,
        missing: missing,
        passHtml: "IPv4 and IPv6 addressing on R1 and R2 are correct.",
      };
    }

    function recordIf(view, flags, u, ifName) {
      if (S.tryRecordIpAddress(view, ifName, u)) {
        flags.v4 = true;
        return true;
      }
      if (S.tryRecordIpv6Address(view, ifName, u)) {
        flags.v6 = true;
        return true;
      }
      if (u === "no shutdown") {
        view.applyInterface(ifName, "no shutdown");
        return true;
      }
      if (u === "ipv6 unicast-routing") {
        view.applyGlobal("ipv6 unicast-routing");
        return true;
      }
      return false;
    }

    function makeSubmit(modeKey, stateKey, view, flags, host) {
      return function (ctx) {
        var mode = modeKey === "r1" ? r1Mode : r2Mode;
        var u = ctx.normalize(ctx.line);
        if (ctx.matchShowRun(ctx.line)) {
          ctx.append("line-showrun", view.render());
          return;
        }
        if (u === "ping 10.0.12.6" || u === "ping 2001:db8:12::13") {
          var ok =
            r1Flags.v4 && r2Flags.v4 && (u.indexOf("10.") === -1 || (r1Flags.v4 && r2Flags.v4));
          if (u.indexOf("2001:") === 0) ok = r1Flags.v6 && r2Flags.v6;
          ctx.append("line-sys", ok ? "!!!!!" : ".....");
          return;
        }
        function setMode(m) {
          if (modeKey === "r1") r1Mode = m;
          else r2Mode = m;
          stateKey.mode = m;
          ctx.setPrompt(S.routerPromptForMode(host, m));
        }
        var st = stateKey;
        if (S.handleRouterModeNavigation(st, u, setMode)) return;
        if (S.handleCopyRunStart(mode, u, ctx.append, opts.container)) return;
        if ((mode === "config-if" || mode === "config") && st.activeIf) {
          if (recordIf(view, flags, u, st.activeIf)) return;
        }
        if (mode === "config" && u === "ipv6 unicast-routing") {
          view.applyGlobal("ipv6 unicast-routing");
          return;
        }
        if (mode === "config-if" && u === "no shutdown" && st.activeIf) {
          view.applyInterface(st.activeIf, "no shutdown");
          return;
        }
        ctx.append("line-bad", opts.container.INVALID_INPUT_MSG);
      };
    }

    wireSubmitLab({
      checkBtn: opts.checkBtn,
      labCheckEl: opts.labCheckEl,
      passBanner: opts.passBanner,
      passMsg: opts.passMsg,
      getLabCheckResult: getLabCheckResult,
    });

    return {
      reset: reset,
      submitR1: makeSubmit("r1", r1State, r1View, r1Flags, "R1"),
      submitR2: makeSubmit("r2", r2State, r2View, r2Flags, "R2"),
      getLabCheckResult: getLabCheckResult,
    };
  }

  /** Native VLAN + LACP — SW1–SW4 */
  function createNativeVlanLacpTestEngine(opts) {
    var hosts = opts.hosts;
    var views = {};
    var modes = {};
    var states = {};
    hosts.forEach(function (h) {
      views[h.id] = opts.container.createRunningConfigView(h.baseline);
      modes[h.id] = "exec";
      states[h.id] = { mode: "exec", activeIf: null, activeIfs: [] };
    });

    var REQUIRED = opts.required;

    function reset() {
      hosts.forEach(function (h) {
        modes[h.id] = "exec";
        states[h.id] = { mode: "exec", activeIf: null, activeIfs: [] };
        views[h.id].reset();
      });
      S.resetLabCheckUi(opts.labCheckEl, opts.passBanner, opts.pendingMsg);
    }

    function getLabCheckResult() {
      var missing = [];
      REQUIRED.forEach(function (req) {
        var run = views[req.deviceId].render();
        req.lines.forEach(function (item) {
          if (item.global) {
            if (!S.runningConfigHasLine(views[req.deviceId], item.line)) {
              missing.push(req.label + ": " + item.line);
            }
          } else if (!S.ifBlockHasLine(run, item.ifName, item.line)) {
            missing.push(req.label + ": " + item.ifName + " — " + item.line);
          }
        });
      });
      return { ok: missing.length === 0, missing: missing, passHtml: "All trunk and LACP tasks are complete." };
    }

    function record(deviceId, u, st) {
      var view = views[deviceId];
      if (S.tryRecordVlan(view, u)) return true;
      if (st.activeIf && S.tryRecordSwitchport(view, st.activeIf, u)) return true;
      if (st.activeIfs && st.activeIfs.length) {
        if (S.tryRecordChannelGroup(view, st.activeIfs, u)) return true;
        if (S.tryRecordChannelProtocol(view, st.activeIfs, u)) return true;
        if (S.tryRecordSwitchportOnIfs(view, st.activeIfs, u)) return true;
      }
      return false;
    }

    function makeSubmit(deviceId, hostLabel) {
      return function (ctx) {
        var mode = modes[deviceId];
        var st = states[deviceId];
        var u = ctx.normalize(ctx.line);
        if (ctx.matchShowRun(ctx.line)) {
          ctx.append("line-showrun", views[deviceId].render());
          return;
        }
        function setMode(m) {
          modes[deviceId] = m;
          st.mode = m;
          ctx.setPrompt(S.switchPromptForMode(hostLabel, m));
        }
        if (S.handleRouterModeNavigation(st, u, setMode)) {
          if (st.activeIfs && st.activeIfs.length) st.activeIf = st.activeIfs[0];
          return;
        }
        if (S.handleCopyRunStart(mode, u, ctx.append, opts.container)) return;
        if ((mode === "config-if" || mode === "config-if-range") && record(deviceId, u, st)) return;
        ctx.append("line-bad", opts.container.INVALID_INPUT_MSG);
      };
    }

    wireSubmitLab({
      checkBtn: opts.checkBtn,
      labCheckEl: opts.labCheckEl,
      passBanner: opts.passBanner,
      passMsg: opts.passMsg,
      getLabCheckResult: getLabCheckResult,
    });

    var api = { reset: reset, getLabCheckResult: getLabCheckResult };
    hosts.forEach(function (h) {
      api["submit_" + h.id] = makeSubmit(h.id, h.label);
    });
    return api;
  }

  /** DHCP snooping + ACL — Sw1, R1, Sw3 */
  function createNamedAclTestEngine(opts) {
    var sw1View = opts.container.createRunningConfigView(opts.sw1Baseline);
    var r1View = opts.container.createRunningConfigView(opts.r1Baseline);
    var sw3View = opts.container.createRunningConfigView(opts.sw3Baseline);
    var modes = { sw1: "exec", r1: "exec", sw3: "exec" };
    var states = {
      sw1: { mode: "exec", activeIf: null, activeIfs: [] },
      r1: { mode: "exec", activeIf: null, activeIfs: [] },
      sw3: { mode: "exec", activeIf: null, activeIfs: [] },
    };
    var sw3Flags = { user: false, vty: false, telnet: false, login: false };

    var SW1_GLOBAL = [
      "ip dhcp snooping",
      "ip dhcp snooping vlan 101",
      "no ip dhcp snooping information option",
      "ip dhcp snooping verify mac-address",
    ];
    var R1_ACES = [
      "permit tcp 172.16.0.0 0.0.255.255 any eq 443",
      "permit tcp 172.16.101.0 0.0.0.255 any eq telnet",
      "deny ip any any log-input",
    ];

    function reset() {
      modes = { sw1: "exec", r1: "exec", sw3: "exec" };
      sw1View.reset();
      r1View.reset();
      sw3View.reset();
      sw3Flags = { user: false, vty: false, telnet: false, login: false };
      S.resetLabCheckUi(opts.labCheckEl, opts.passBanner, opts.pendingMsg);
    }

    function getLabCheckResult() {
      var missing = [];
      SW1_GLOBAL.forEach(function (line) {
        if (!S.runningConfigHasLine(sw1View, line)) missing.push("Sw1: " + line);
      });
      R1_ACES.forEach(function (line) {
        if (!S.runningConfigHasLine(r1View, line)) missing.push("R1: INTERNET_ACL — " + line);
      });
      ["Ethernet0/0", "Ethernet0/3"].forEach(function (ifName) {
        if (!S.ifBlockHasLine(r1View.render(), ifName, "ip access-group INTERNET_ACL in")) {
          missing.push("R1: " + ifName + " — ip access-group INTERNET_ACL in");
        }
      });
      if (!S.runningConfigHasLine(sw3View, "username devnet algorithm-type sha256 privilege 15 secret access8cli")) {
        missing.push("Sw3: username devnet … secret access8cli");
      }
      if (!S.ifBlockHasLine(sw3View.render(), "line vty 0 4", "transport input telnet")) {
        missing.push("Sw3: line vty 0 4 — transport input telnet");
      }
      if (!S.ifBlockHasLine(sw3View.render(), "line vty 0 4", "login local")) {
        missing.push("Sw3: line vty 0 4 — login local");
      }
      return { ok: missing.length === 0, missing: missing, passHtml: "ACL, DHCP snooping, and Sw3 user tasks are complete." };
    }

    function makeSubmit(key, view, host) {
      return function (ctx) {
        var mode = modes[key];
        var st = states[key];
        var u = ctx.normalize(ctx.line);
        if (ctx.matchShowRun(ctx.line)) {
          ctx.append("line-showrun", view.render());
          return;
        }
        function setMode(m) {
          modes[key] = m;
          st.mode = m;
          ctx.setPrompt(S.routerPromptForMode(host, m));
        }
        if (S.handleRouterModeNavigation(st, u, setMode)) return;
        if (S.handleCopyRunStart(mode, u, ctx.append, opts.container)) return;
        if (key === "sw1" && mode === "config" && S.tryRecordIpDhcpSnoopingGlobal(view, u)) return;
        if (key === "r1") {
          if (mode === "config-ext-nacl" && S.tryRecordAclAce(view, u)) return;
          if (mode === "config-if" && st.activeIf && S.tryRecordIpAccessGroup(view, st.activeIf, u)) return;
        }
        if (key === "sw3") {
          if (mode === "config" && S.tryRecordUsername(view, u)) {
            sw3Flags.user = true;
            return;
          }
          if (mode === "config" && S.tryRecordLineVty(view, u)) {
            sw3Flags.vty = true;
            return;
          }
          if (mode === "config" && S.tryRecordLineVtySubcmd(view, u)) {
            if (u.indexOf("transport input telnet") !== -1) sw3Flags.telnet = true;
            if (u === "login local") sw3Flags.login = true;
            return;
          }
        }
        ctx.append("line-bad", opts.container.INVALID_INPUT_MSG);
      };
    }

    wireSubmitLab({
      checkBtn: opts.checkBtn,
      labCheckEl: opts.labCheckEl,
      passBanner: opts.passBanner,
      passMsg: opts.passMsg,
      getLabCheckResult: getLabCheckResult,
    });

    return {
      reset: reset,
      submitSw1: makeSubmit("sw1", sw1View, "Sw1"),
      submitR1: makeSubmit("r1", r1View, "R1"),
      submitSw3: makeSubmit("sw3", sw3View, "Sw3"),
      getLabCheckResult: getLabCheckResult,
    };
  }

  /** IP services — R2 NAT + R1 NTP + R3 DHCP/SSH */
  function createIpServicesTestEngine(opts) {
    var r2View = opts.container.createRunningConfigView(opts.r2Baseline);
    var r1View = opts.container.createRunningConfigView(opts.r1Baseline);
    var r3View = opts.container.createRunningConfigView(opts.r3Baseline);
    var r2Mode = "exec";
    var r1Mode = "exec";
    var r3Mode = "exec";
    var r2State = { mode: "exec", activeIf: null, activeIfs: [] };
    var r1State = { mode: "exec", activeIf: null, activeIfs: [] };
    var r3State = { mode: "exec", activeIf: null, activeIfs: [] };
    var r3Crypto = false;
    var r2Nat = { acl: false, inside: false, outside: false, pool: false, source: false };
    var r2Permits = { a: false, b: false, c: false };

    function reset() {
      r2View.reset();
      r1View.reset();
      r3View.reset();
      r2Mode = r1Mode = r3Mode = "exec";
      r3Crypto = false;
      r2Nat = { acl: false, inside: false, outside: false, pool: false, source: false };
      r2Permits = { a: false, b: false, c: false };
      S.resetLabCheckUi(opts.labCheckEl, opts.passBanner, opts.pendingMsg);
    }

    function getLabCheckResult() {
      var missing = [];
      var r2 = r2View.render();
      if (!S.runningConfigHasLine(r2View, "ip access-list standard xlate")) missing.push("R2: ip access-list standard XLATE");
      ["permit 10.2.3.3", "permit 192.168.3.1", "permit 10.1.3.11"].forEach(function (p) {
        if (!S.runningConfigHasLine(r2View, p)) missing.push("R2: XLATE — " + p);
      });
      if (!S.ifBlockHasLine(r2, "GigabitEthernet0/1", "ip nat inside")) missing.push("R2: Gi0/1 — ip nat inside");
      if (!S.ifBlockHasLine(r2, "GigabitEthernet0/0", "ip nat outside")) missing.push("R2: Gi0/0 — ip nat outside");
      if (!S.runningConfigHasLine(r2View, "ip nat pool test_pool 10.10.10.1 10.10.10.254 netmask 255.255.255.0")) {
        missing.push("R2: ip nat pool test_pool …");
      }
      if (!S.runningConfigHasLine(r2View, "ip nat inside source list xlate pool test_pool")) {
        missing.push("R2: ip nat inside source list XLATE pool test_pool");
      }
      if (!S.runningConfigHasLine(r2View, "ntp server 10.1.2.1")) missing.push("R2: ntp server 10.1.2.1");
      if (!S.runningConfigHasLine(r1View, "ntp master 1") && !S.runningConfigHasLine(r1View, "ntp master")) {
        missing.push("R1: ntp master 1");
      }
      if (!S.ifBlockHasLine(r3View.render(), "GigabitEthernet0/2", "ip address dhcp")) {
        missing.push("R3: Gi0/2 — ip address dhcp");
      }
      if (!S.runningConfigHasLine(r3View, "username root privilege 15 secret s3cret")) {
        missing.push("R3: username root privilege 15 secret s3cret");
      }
      if (!r3Crypto) missing.push("R3: crypto key generate rsa modulus 1024");
      if (!S.ifBlockHasLine(r3View.render(), "line vty 0 4", "login local")) {
        missing.push("R3: line vty 0 4 — login local");
      }
      if (!S.ifBlockHasLine(r3View.render(), "line vty 0 4", "transport input ssh")) {
        missing.push("R3: line vty 0 4 — transport input ssh");
      }
      return { ok: missing.length === 0, missing: missing, passHtml: "All four IP services tasks are complete." };
    }

    function submitR2(ctx) {
      var u = ctx.normalize(ctx.line);
      if (ctx.matchShowRun(ctx.line)) {
        ctx.append("line-showrun", r2View.render());
        return;
      }
      function setMode(m) {
        r2Mode = m;
        r2State.mode = m;
        ctx.setPrompt(S.routerPromptForMode("R2", m));
      }
      if (S.handleRouterModeNavigation(r2State, u, setMode)) return;
      if (S.handleCopyRunStart(r2Mode, u, ctx.append, opts.container)) return;
      if (r2Mode === "config" && S.tryRecordIpAccessListStandard(r2View, u)) {
        r2Nat.acl = true;
        return;
      }
      if (r2Mode === "config-std-nacl" && S.tryRecordStdNaclPermit(r2View, u)) {
        r2Permits.a = r2Permits.b = r2Permits.c = true;
        return;
      }
      if (r2Mode === "config-if" && r2State.activeIf && S.tryRecordIpNatIf(r2View, r2State.activeIf, u)) {
        if (u === "ip nat inside") r2Nat.inside = true;
        if (u === "ip nat outside") r2Nat.outside = true;
        return;
      }
      if (r2Mode === "config" && S.tryRecordIpNatPool(r2View, u)) {
        r2Nat.pool = true;
        return;
      }
      if (r2Mode === "config" && S.tryRecordIpNatInsideSource(r2View, u)) {
        r2Nat.source = true;
        return;
      }
      if (r2Mode === "config" && /^ntp server \S+$/.test(u)) {
        r2View.applyGlobal(u);
        return;
      }
      ctx.append("line-bad", opts.container.INVALID_INPUT_MSG);
    }

    function submitR1(ctx) {
      var u = ctx.normalize(ctx.line);
      if (ctx.matchShowRun(ctx.line)) {
        ctx.append("line-showrun", r1View.render());
        return;
      }
      function setMode(m) {
        r1Mode = m;
        r1State.mode = m;
        ctx.setPrompt(S.routerPromptForMode("R1", m));
      }
      if (S.handleRouterModeNavigation(r1State, u, setMode)) return;
      if (S.handleCopyRunStart(r1Mode, u, ctx.append, opts.container)) return;
      if (r1Mode === "config" && /^ntp master( \d+)?$/.test(u)) {
        r1View.applyGlobal(u.indexOf(" ") === -1 ? "ntp master 1" : u);
        return;
      }
      ctx.append("line-bad", opts.container.INVALID_INPUT_MSG);
    }

    function submitR3(ctx) {
      var u = ctx.normalize(ctx.line);
      if (ctx.matchShowRun(ctx.line)) {
        ctx.append("line-showrun", r3View.render());
        return;
      }
      if (u === "ping 192.168.100.1") {
        var natOk = r2Nat.source && r2Nat.pool && r2Nat.inside && r2Nat.outside;
        ctx.append("line-sys", natOk ? "!!!!!" : ".....");
        return;
      }
      function setMode(m) {
        r3Mode = m;
        r3State.mode = m;
        ctx.setPrompt(S.routerPromptForMode("R3", m));
      }
      if (S.handleRouterModeNavigation(r3State, u, setMode)) return;
      if (S.handleCopyRunStart(r3Mode, u, ctx.append, opts.container)) return;
      if (opts.container.tryAppendCryptoKeyGenerateRsaOutput(ctx.line, ctx.append, {
        normalize: ctx.normalize,
        requireConfigMode: true,
        mode: r3Mode,
      })) {
        r3Crypto = true;
        return;
      }
      if (r3Mode === "config-if" && u === "ip address dhcp" && r3State.activeIf) {
        r3View.applyInterface(r3State.activeIf, "ip address dhcp");
        return;
      }
      if (r3Mode === "config" && S.tryRecordUsername(r3View, u)) return;
      if (r3Mode === "config" && S.tryRecordLineVty(r3View, u)) return;
      if (r3Mode === "config" && S.tryRecordLineVtySubcmd(r3View, u)) return;
      ctx.append("line-bad", opts.container.INVALID_INPUT_MSG);
    }

    wireSubmitLab({
      checkBtn: opts.checkBtn,
      labCheckEl: opts.labCheckEl,
      passBanner: opts.passBanner,
      passMsg: opts.passMsg,
      getLabCheckResult: getLabCheckResult,
    });

    return {
      reset: reset,
      submitR2: submitR2,
      submitR1: submitR1,
      submitR3: submitR3,
      getLabCheckResult: getLabCheckResult,
      r2NatFlags: function () {
        return r2Nat;
      },
    };
  }

  /** Trunk + LACP — Sw1 + Sw2 */
  function createTrunkLacpTestEngine(opts) {
    var sw1View = opts.container.createRunningConfigView(opts.sw1Baseline);
    var sw2View = opts.container.createRunningConfigView(opts.sw2Baseline);
    var sw1Mode = "exec";
    var sw2Mode = "exec";
    var sw1State = { mode: "exec", activeIf: null, activeIfs: [], currentVlanId: null };
    var sw2State = { mode: "exec", activeIf: null, activeIfs: [], currentVlanId: null };
    var vlans = { sw1: {}, sw2: {} };

    var TRUNK_LINES = [
      "switchport trunk encapsulation dot1q",
      "switchport mode trunk",
      "switchport trunk native vlan 45",
      "switchport trunk allowed vlan 15,45",
    ];

    function reset() {
      sw1View.reset();
      sw2View.reset();
      sw1Mode = sw2Mode = "exec";
      vlans = { sw1: {}, sw2: {} };
      S.resetLabCheckUi(opts.labCheckEl, opts.passBanner, opts.pendingMsg);
    }

    function checkSwitch(host, view, vlanMap, missing) {
      if (!vlanMap["15"] || !vlanMap["45"]) {
        missing.push(host + ": vlan 15 and vlan 45");
      }
      ["GigabitEthernet0/1", "GigabitEthernet0/2", "Port-channel15"].forEach(function (ifName) {
        var run = view.render();
        TRUNK_LINES.forEach(function (line) {
          if (!S.ifBlockHasLine(run, ifName, line)) {
            missing.push(host + ": " + ifName + " — " + line);
          }
        });
        if (ifName !== "Port-channel15") {
          if (!S.ifBlockHasLine(run, ifName, "channel-group 15 mode active")) {
            missing.push(host + ": " + ifName + " — channel-group 15 mode active");
          }
          if (!S.ifBlockHasLine(run, ifName, "channel-protocol lacp")) {
            missing.push(host + ": " + ifName + " — channel-protocol lacp");
          }
        }
      });
    }

    function getLabCheckResult() {
      var missing = [];
      checkSwitch("Sw1", sw1View, vlans.sw1, missing);
      checkSwitch("Sw2", sw2View, vlans.sw2, missing);
      return { ok: missing.length === 0, missing: missing, passHtml: "Trunks, VLANs, and LACP on both switches are complete." };
    }

    function recordVlan(map, u) {
      var m = /^vlan (\d+)$/.exec(u);
      if (!m) return false;
      map[m[1]] = true;
      return true;
    }

    function recordTrunk(view, st, u) {
      var targets = st.activeIfs && st.activeIfs.length ? st.activeIfs : st.activeIf ? [st.activeIf] : [];
      if (!targets.length) return false;
      if (S.tryRecordSwitchportOnIfs(view, targets, u)) return true;
      if (S.tryRecordChannelGroup(view, targets, u)) return true;
      if (S.tryRecordChannelProtocol(view, targets, u)) return true;
      return false;
    }

    function makeSubmit(modeKey, stateKey, view, vlanMap, host) {
      return function (ctx) {
        var mode = modeKey === "sw1" ? sw1Mode : sw2Mode;
        var st = stateKey;
        var u = ctx.normalize(ctx.line);
        if (ctx.matchShowRun(ctx.line)) {
          ctx.append("line-showrun", view.render());
          return;
        }
        function setMode(m) {
          if (modeKey === "sw1") sw1Mode = m;
          else sw2Mode = m;
          st.mode = m;
          ctx.setPrompt(S.switchPromptForMode(host, m));
        }
        if (S.handleRouterModeNavigation(st, u, setMode)) return;
        if (S.handleCopyRunStart(mode, u, ctx.append, opts.container)) return;
        if ((mode === "config" || mode === "config-vlan") && recordVlan(vlanMap, u)) {
          view.applyGlobal(u);
          return;
        }
        if (mode === "config-if" || mode === "config-if-range") {
          if (recordTrunk(view, st, u)) return;
        }
        ctx.append("line-bad", opts.container.INVALID_INPUT_MSG);
      };
    }

    wireSubmitLab({
      checkBtn: opts.checkBtn,
      labCheckEl: opts.labCheckEl,
      passBanner: opts.passBanner,
      passMsg: opts.passMsg,
      getLabCheckResult: getLabCheckResult,
    });

    return {
      reset: reset,
      submitSw1: makeSubmit("sw1", sw1State, sw1View, vlans.sw1, "Sw1"),
      submitSw2: makeSubmit("sw2", sw2State, sw2View, vlans.sw2, "Sw2"),
      getLabCheckResult: getLabCheckResult,
    };
  }

  global.createNamedAclTestEngine = createNamedAclTestEngine;
  global.createIpServicesTestEngine = createIpServicesTestEngine;
  global.createTrunkLacpTestEngine = createTrunkLacpTestEngine;
  global.createOspfTestEngine = createOspfTestEngine;
  global.createStaticRoutingTestEngine = createStaticRoutingTestEngine;
  global.createIpv4Ipv6TestEngine = createIpv4Ipv6TestEngine;
  global.createNativeVlanLacpTestEngine = createNativeVlanLacpTestEngine;
})(typeof window !== "undefined" ? window : globalThis);

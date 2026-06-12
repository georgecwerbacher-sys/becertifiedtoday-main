/**
 * Shared CLI container helpers (templates/containers/cli-container-template.html).
 * Labs keep device-specific ids (scrollR10, cmdR10, …); markup uses template classes
 * scrollback-area, prompt-el, cmdline-input alongside legacy names.
 */
(function () {
  function isModeNavigationCommand(normalizedCmd) {
    var u = String(normalizedCmd || "");
    return (
      u === "configure terminal" ||
      u === "end" ||
      u === "exit" ||
      u.indexOf("interface ") === 0
    );
  }

  function expandInterfaceEcho(raw) {
    var s = String(raw || "").trim();
    var m = /^(interface|int)\s+e(\d+)\/(\d+)$/i.exec(s);
    if (m) {
      return "interface Ethernet" + m[2] + "/" + m[3];
    }
    return s;
  }

  var CLI_UNSUPPORTED_MSG = "% command not supported in this lab simulation";
  var CLI_UNSUPPORTED_NUMERIC_HINT_MSG =
    "% command not supported in this lab simulation — check the lab Tasks and Verification sections for the exact values.";
  var CLI_VERIFY_INSTRUCTIONS_MSG =
    "% command not supported in this lab simulation. Verify the lab instructions (Tasks and Helper) for the required values.";

  /** @deprecated use CLI_UNSUPPORTED_MSG */
  var INVALID_INPUT_MSG = CLI_UNSUPPORTED_MSG;
  /** @deprecated use CLI_UNSUPPORTED_NUMERIC_HINT_MSG */
  var INVALID_INPUT_NUMERIC_HINT_MSG = CLI_UNSUPPORTED_NUMERIC_HINT_MSG;

  function invalidInputMsgForNormalizedCmd(u) {
    return /\d/.test(String(u || "")) ? CLI_UNSUPPORTED_NUMERIC_HINT_MSG : CLI_UNSUPPORTED_MSG;
  }

  function unsupportedCmdMsg(u) {
    return invalidInputMsgForNormalizedCmd(u);
  }

  var localHistoryByInput = new WeakMap();

  function getLocalHistoryState(input) {
    var state = localHistoryByInput.get(input);
    if (state) return state;
    state = { entries: [], idx: 0 };
    localHistoryByInput.set(input, state);
    return state;
  }

  function pushLocalHistory(input, raw) {
    var cmd = String(raw || "").trim();
    if (!cmd) return;
    var state = getLocalHistoryState(input);
    if (!state.entries.length || state.entries[state.entries.length - 1] !== cmd) {
      state.entries.push(cmd);
    }
    state.idx = state.entries.length;
  }

  function bindLocalHistory(input) {
    if (!input || input.dataset.localHistoryReady === "1") return;
    input.dataset.localHistoryReady = "1";
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        pushLocalHistory(input, input.value);
        return;
      }
      var usePrev = e.key === "ArrowUp" || (e.key === "Tab" && !e.shiftKey);
      var useNext = e.key === "ArrowDown" || (e.key === "Tab" && e.shiftKey);
      if (!usePrev && !useNext) return;
      var state = getLocalHistoryState(input);
      if (!state.entries.length) return;
      e.preventDefault();
      if (usePrev) {
        state.idx = Math.max(0, state.idx - 1);
      } else {
        state.idx = Math.min(state.entries.length, state.idx + 1);
      }
      input.value = state.idx >= state.entries.length ? "" : state.entries[state.idx];
    });
  }

  function pathLooksLikeCcnaLab(p) {
    p = String(p || "").toLowerCase();
    return (
      p.indexOf("/ccna-study/ccna_labs/") !== -1 ||
      p.indexOf("/ccna_sim_exam/embed/lab/") !== -1
    );
  }

  function isCcnaLabEmbedPath() {
    if (pathLooksLikeCcnaLab(location.pathname)) return true;
    try {
      return pathLooksLikeCcnaLab(sessionStorage.getItem("ccnaLastRealPath"));
    } catch (_) {}
    return !!document.querySelector(".cli-modal-overlay .scrollback-area");
  }

  function isExamSimEmbed() {
    try {
      return new URLSearchParams(location.search).get("examSim") === "1";
    } catch (_) {
      return false;
    }
  }

  /** Timed exam embed (?examSim=1) or CCNA home sample labs (?sample=1, /sample#ccnaHS=…). */
  function isBctCliBannerContext() {
    try {
      var params = new URLSearchParams(location.search);
      if (params.get("examSim") === "1") return true;
      if (!isCcnaLabEmbedPath()) return false;
      if (params.get("sample") === "1") return true;
      if (sessionStorage.getItem("ccnaHomeSample")) return true;
    } catch (_) {}
    return false;
  }

  var EXAM_SIM_CLI_BANNER_TEXT =
    "================================================================================\n" +
    "  Be Certified Today — BCT Lab Simulator v.1_2026\n" +
    "================================================================================\n" +
    "\n" +
    "Exam simulation environment. Help commands are disabled; only commands required\n" +
    "for this lab scenario are available. Use the Helper button to review the lab\n" +
    "outline and topology if needed.\n" +
    "================================================================================";

  /** Login-style banner when a CLI modal opens in exam sim or CCNA sample lab flows. */
  function showExamSimCliBanner(scrollbackEl) {
    if (!scrollbackEl || !isBctCliBannerContext()) return;
    var prev = scrollbackEl.querySelector('[data-bct-exam-sim-banner="1"]');
    if (prev) prev.remove();
    var div = document.createElement("div");
    div.className = "line-boot";
    div.setAttribute("data-bct-exam-sim-banner", "1");
    div.style.whiteSpace = "pre-wrap";
    div.textContent = EXAM_SIM_CLI_BANNER_TEXT;
    scrollbackEl.insertBefore(div, scrollbackEl.firstChild);
    scrollbackEl.scrollTop = 0;
  }

  /** Per-device IOS explore nav; delegates to cli-ios-mode.js when loaded. */
  function createExploreNav(host) {
    var iosMode =
      typeof window !== "undefined" && window.cliIosMode ? window.cliIosMode : null;
    if (iosMode && typeof iosMode.createDeviceExplore === "function") {
      return iosMode.createDeviceExplore(host);
    }
    return {
      getMode: function () {
        return null;
      },
      reset: function () {},
      promptWith: function (labPrompt) {
        return labPrompt || host + "#";
      },
      trySubmit: function () {
        return false;
      },
    };
  }

  var api = {
    isModeNavigationCommand: isModeNavigationCommand,
    expandInterfaceEcho: expandInterfaceEcho,
    CLI_UNSUPPORTED_MSG: CLI_UNSUPPORTED_MSG,
    CLI_UNSUPPORTED_NUMERIC_HINT_MSG: CLI_UNSUPPORTED_NUMERIC_HINT_MSG,
    CLI_VERIFY_INSTRUCTIONS_MSG: CLI_VERIFY_INSTRUCTIONS_MSG,
    INVALID_INPUT_MSG: INVALID_INPUT_MSG,
    INVALID_INPUT_NUMERIC_HINT_MSG: INVALID_INPUT_NUMERIC_HINT_MSG,
    invalidInputMsgForNormalizedCmd: invalidInputMsgForNormalizedCmd,
    unsupportedCmdMsg: unsupportedCmdMsg,
    bindLocalHistory: bindLocalHistory,
    createExploreNav: createExploreNav,
    isCcnaLabEmbedPath: isCcnaLabEmbedPath,
    isExamSimEmbed: isExamSimEmbed,
    isBctCliBannerContext: isBctCliBannerContext,
    EXAM_SIM_CLI_BANNER_TEXT: EXAM_SIM_CLI_BANNER_TEXT,
    showExamSimCliBanner: showExamSimCliBanner,
  };

  window.cliLabContainer = api;

  if (typeof window.expandInterfaceEcho !== "function") {
    window.expandInterfaceEcho = expandInterfaceEcho;
  }
  if (typeof window.isModeNavigationCommand !== "function") {
    window.isModeNavigationCommand = isModeNavigationCommand;
  }
  if (typeof window.invalidInputMsgForNormalizedCmd !== "function") {
    window.invalidInputMsgForNormalizedCmd = invalidInputMsgForNormalizedCmd;
  }
  if (typeof window.unsupportedCmdMsg !== "function") {
    window.unsupportedCmdMsg = unsupportedCmdMsg;
  }
  if (typeof window.bindLocalHistory !== "function") {
    window.bindLocalHistory = bindLocalHistory;
  }
})();

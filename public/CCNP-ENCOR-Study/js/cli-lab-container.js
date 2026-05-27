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

  var INVALID_INPUT_MSG = "% Invalid input";
  var INVALID_INPUT_NUMERIC_HINT_MSG =
    "% Invalid input — check the lab Tasks and Verification sections for the exact values.";

  function invalidInputMsgForNormalizedCmd(u) {
    return /\d/.test(String(u || "")) ? INVALID_INPUT_NUMERIC_HINT_MSG : INVALID_INPUT_MSG;
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

  var api = {
    isModeNavigationCommand: isModeNavigationCommand,
    expandInterfaceEcho: expandInterfaceEcho,
    INVALID_INPUT_MSG: INVALID_INPUT_MSG,
    INVALID_INPUT_NUMERIC_HINT_MSG: INVALID_INPUT_NUMERIC_HINT_MSG,
    invalidInputMsgForNormalizedCmd: invalidInputMsgForNormalizedCmd,
    bindLocalHistory: bindLocalHistory,
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
  if (typeof window.bindLocalHistory !== "function") {
    window.bindLocalHistory = bindLocalHistory;
  }
})();

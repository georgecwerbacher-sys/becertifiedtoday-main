/**
 * IOS-style config hierarchy for lab simulators: "exit" walks up one level
 * (e.g. config-ext-nacl → config → privileged) without advancing the lab step.
 * Use with a per-flow exitLevel counter; reset exitLevel to 0 on any non-exit
 * command or when the step index changes.
 */
(function (global) {
  const PARENT = {
    "config-ext-nacl": "config",
    "config-if": "config",
    "config-line": "config",
    "config-router": "config",
    "config-vrf": "config",
    "config-cmap": "config",
    "config-pmap": "config",
    "config-pmap-c": "config-pmap",
    "config-cp": "config",
    "config-ip-sla-echo": "config",
    "config-ip-sla-http": "config",
    "config-fe": "config",
    "config": "privileged",
    "privileged": null,
    "exec": null,
  };

  function effectiveMode(baseMode, exitLevel) {
    let m = baseMode == null ? "privileged" : baseMode;
    for (let i = 0; i < exitLevel; i++) {
      const next = PARENT[m];
      if (next == null) break;
      m = next;
    }
    return m;
  }

  function canExit(baseMode, exitLevel) {
    const eff = effectiveMode(baseMode, exitLevel);
    return PARENT[eff] != null;
  }

  function promptFromMode(host, mode) {
    const m = mode == null ? "privileged" : mode;
    if (m === "exec" || m === "privileged") return `${host}#`;
    if (m === "config") return `${host}(config)#`;
    if (m === "config-if") return `${host}(config-if)#`;
    if (m === "config-line") return `${host}(config-line)#`;
    if (m === "config-router") return `${host}(config-router)#`;
    if (m === "config-vrf") return `${host}(config-vrf)#`;
    if (m === "config-ext-nacl") return `${host}(config-ext-nacl)#`;
    if (m === "config-cmap") return `${host}(config-cmap)#`;
    if (m === "config-pmap") return `${host}(config-pmap)#`;
    if (m === "config-pmap-c") return `${host}(config-pmap-c)#`;
    if (m === "config-cp") return `${host}(config-cp)#`;
    if (m === "config-fe") return `${host}(config-flow-exporter)#`;
    if (m === "config-ip-sla-echo") return `${host}(config-ip-sla-echo)#`;
    if (m === "config-ip-sla-http") return `${host}(config-ip-sla-http)#`;
    return `${host}#`;
  }

  /** Prompt for steps[index].mode after applying exitLevel parent walks. */
  function promptForStep(host, steps, index, exitLevel) {
    if (!steps || index >= steps.length) return `${host}#`;
    const eff = effectiveMode(steps[index].mode, exitLevel || 0);
    return promptFromMode(host, eff);
  }

  global.cliIosMode = {
    PARENT,
    effectiveMode,
    canExit,
    promptFromMode,
    promptForStep,
  };
})(typeof window !== "undefined" ? window : globalThis);

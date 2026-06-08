/**
 * PBQ production labs — deep dive popup (vault deep-dive-solution.md via secplus-pbq-deep-dive-data.js).
 */
(function () {
  "use strict";

  function pageSlug() {
    var path = location.pathname || "";
    var match = /\/([^/]+\.html)$/.exec(path);
    if (match) return match[1];
    try {
      var remembered = sessionStorage.getItem("ccnaLastRealPath") || "";
      match = /\/([^/]+\.html)$/.exec(remembered);
      if (match) return match[1];
    } catch (e) {}
    return "";
  }

  function resolveKey(explicit) {
    if (explicit) return explicit;
    var btn = document.getElementById("pbqDeepDiveBtn");
    if (btn && btn.dataset.deepDiveKey) return btn.dataset.deepDiveKey;
    if (window.PBQ_DEEP_DIVE_KEY) return window.PBQ_DEEP_DIVE_KEY;
    return pageSlug();
  }

  function getEntry(key) {
    var content = window.SECPLUS_PBq_DEEP_DIVE;
    if (!content) return null;
    return content[resolveKey(key)] || null;
  }

  function openDeepDive(key, returnFocus) {
    var modalApi = window.SecplusDeepDiveModal;
    if (!modalApi) return false;
    var entry = getEntry(key);
    if (!entry) return false;
    return modalApi.open({
      title: entry.title,
      html: entry.html,
      returnFocus: returnFocus,
    });
  }

  window.SecplusPbqDeepDive = {
    open: openDeepDive,
    getEntry: getEntry,
    resolveKey: resolveKey,
  };

  function bindDeepDiveButton() {
    var btn = document.getElementById("pbqDeepDiveBtn");
    if (!btn || btn.dataset.deepDiveBound) return;

    btn.dataset.deepDiveBound = "1";
    btn.addEventListener("click", function (ev) {
      ev.preventDefault();
      var key = btn.dataset.deepDiveKey || null;
      if (!openDeepDive(key, btn)) {
        console.warn(
          "[SecplusPbqDeepDive] No deep dive content for key:",
          resolveKey(key)
        );
      }
    });
  }

  function init() {
    bindDeepDiveButton();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
  window.addEventListener("load", init);
})();

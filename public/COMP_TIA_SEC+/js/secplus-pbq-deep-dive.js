/**
 * PBQ production labs — deep dive popup (vault deep-dive-solution.md via secplus-pbq-deep-dive-data.js).
 */
(function () {
  "use strict";

  function pageSlug() {
    var path = location.pathname || "";
    var match = /\/([^/]+\.html)$/.exec(path);
    return match ? match[1] : "";
  }

  function getEntry(key) {
    var content = window.SECPLUS_PBq_DEEP_DIVE;
    if (!content) return null;
    return content[key || pageSlug()] || null;
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
  };

  function init() {
    var btn = document.getElementById("pbqDeepDiveBtn");
    if (!btn || btn.dataset.deepDiveBound) return;
    if (!getEntry()) return;

    btn.dataset.deepDiveBound = "1";
    btn.addEventListener("click", function () {
      openDeepDive(null, btn);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

/**
 * Redirect unpaid visitors away from paid ENCOR content (questions, drag-drop, labs).
 * Public homepage sample flow (encorHomeSample) and ENCOR_Samples stay open.
 */
(function () {
  "use strict";

  var HOME = "/ccnp-home.html#purchase";

  function pathLower() {
    return (location.pathname || "").toLowerCase();
  }

  function isLocalDevHost() {
    try {
      var h = (location.hostname || "").toLowerCase();
      return h === "localhost" || h === "127.0.0.1" || h === "[::1]";
    } catch (e) {
      return false;
    }
  }

  function isPaidContentPath() {
    var p = pathLower();
    if (p.indexOf("/ccnp-encor-study/") === -1) return false;
    if (p.indexOf("/ccnp-encor-study/encor_samples/") !== -1) return false;
    if (/encor_training_portal\.html$/i.test(p)) return false;
    if (/encor-portal-(magic|request-link|restore-access)\.html$/i.test(p)) return false;
    if (p === "/ccnp-encor-study/access-restricted.html") return false;
    return (
      p.indexOf("/ccnp-encor-study/encor_questions/") !== -1 ||
      p.indexOf("/ccnp-encor-study/ccnp-encor-drag-drop/") !== -1 ||
      p.indexOf("/ccnp-encor-study/ccnp-encor-labs/") !== -1
    );
  }

  function homeSampleActive() {
    try {
      return !!sessionStorage.getItem("encorHomeSample");
    } catch (e) {
      return false;
    }
  }

  function hasPortalAccess() {
    if (typeof window.bccEncorPortalAccessActiveSync === "function" && window.bccEncorPortalAccessActiveSync()) {
      return true;
    }
    if (typeof window.bccEncorPortalAccessActive === "function" && window.bccEncorPortalAccessActive()) {
      return true;
    }
    return false;
  }

  /** Set by test-simulation-runner while a timed attempt is in progress (iframe embed). */
  function examSimSessionActive() {
    try {
      if (sessionStorage.getItem("ccnpExamSim") === "1") return true;
      return new URLSearchParams(location.search).get("examSim") === "1";
    } catch (e) {
      return false;
    }
  }

  function redirectToPurchase() {
    location.replace(HOME);
  }

  function enforceGate() {
    if (!isPaidContentPath() || homeSampleActive()) return;
    if (isLocalDevHost()) return;
    if (hasPortalAccess()) return;
    if (examSimSessionActive()) return;
    redirectToPurchase();
  }

  function boot() {
    if (!isPaidContentPath() || homeSampleActive()) return;

    var chain = Promise.resolve();
    if (typeof window.bccApplyEncorPortalCheckoutFromUrl === "function") {
      chain = chain.then(function () {
        return window.bccApplyEncorPortalCheckoutFromUrl(null, true);
      });
    }
    if (typeof window.bccRestoreEncorPortalAccess === "function") {
      chain = chain.then(function () {
        return window.bccRestoreEncorPortalAccess();
      });
    }
    chain.finally(enforceGate);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();

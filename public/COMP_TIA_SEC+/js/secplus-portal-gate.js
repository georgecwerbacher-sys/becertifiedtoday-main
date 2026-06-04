/**
 * Redirect unpaid visitors away from paid Security+ content (questions, sims, D&D).
 * Public homepage sample flow (secplusHomeSample) and SEC+_Samples stay open.
 */
(function () {
  "use strict";

  var HOME = "/comptia-sec+-home.html#purchase";

  function pathLower() {
    return (location.pathname || "").toLowerCase();
  }

  /** Staging / noindex PBQ work under Sim_Hot_Spot — open for local authoring without portal or sample hijack. */
  function isSecplusSimStagingPath(p) {
    return (
      p.indexOf("/sec+_sim_hot_spot/pbq_production/") !== -1 ||
      p.indexOf("/sec+_sim_hot_spot/pending/") !== -1
    );
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
    if (p.indexOf("/comp_tia_sec+/") === -1) return false;
    if (p.indexOf("/sec+_samples/") !== -1) return false;
    if (isSecplusSimStagingPath(p)) return false;
    if (/sec\+_training_portal\.html$/i.test(p)) return false;
    if (/secplus-portal-(magic|request-link|restore-access)\.html$/i.test(p)) return false;
    return (
      p.indexOf("/sec+_questions/") !== -1 ||
      p.indexOf("/sec+_sim_hot_spot/") !== -1 ||
      p.indexOf("/sec+_d_d/") !== -1 ||
      p.indexOf("/sec+_labs/") !== -1
    );
  }

  function homeSampleActive() {
    try {
      return !!sessionStorage.getItem("secplusHomeSample");
    } catch (e) {
      return false;
    }
  }

  function hasPortalAccess() {
    if (typeof window.bccSecplusPortalAccessActive === "function" && window.bccSecplusPortalAccessActive()) {
      return true;
    }
    return false;
  }

  /** Set by test-simulation-runner while a timed attempt is in progress (iframe embed). */
  function examSimSessionActive() {
    try {
      return sessionStorage.getItem("secplusExamSim") === "1";
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
    if (typeof window.bccApplySecplusPortalCheckoutFromUrl === "function") {
      chain = chain.then(function () {
        return window.bccApplySecplusPortalCheckoutFromUrl(null, true);
      });
    }
    if (typeof window.bccRestoreSecplusPortalAccess === "function") {
      chain = chain.then(function () {
        return window.bccRestoreSecplusPortalAccess();
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

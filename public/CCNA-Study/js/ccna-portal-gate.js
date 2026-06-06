/**
 * Redirect unpaid visitors away from paid CCNA content (questions, D&D, labs).
 * Public homepage sample flow (ccnaHomeSample) and CCNA_Samples stay open.
 */
(function () {
  "use strict";

  var HOME = "/ccna-home.html#purchase";

  var FREE_LABS = {
    "/ccna-study/ccna_labs/cli-lab-trunk_lacp.html": true,
    "/ccna-study/ccna_labs/cli-lab-vlan-sim.html": true,
  };

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
    if (p.indexOf("/ccna-study/") === -1 && p.indexOf("/ccna_sim_exam/embed/") === -1) {
      return false;
    }
    if (p.indexOf("/ccna-study/ccna_samples/") !== -1) return false;
    if (/ccna_training_portal\.html$/i.test(p)) return false;
    if (/ccna-portal-(magic|request-link|restore-access)\.html$/i.test(p)) return false;
    if (FREE_LABS[p]) return false;
    return (
      p.indexOf("/ccna-study/ccna_questions/") !== -1 ||
      p.indexOf("/ccna-study/ccna_d_d/") !== -1 ||
      p.indexOf("/ccna-study/ccna_labs/") !== -1 ||
      p.indexOf("/ccna_sim_exam/embed/dnd/") !== -1 ||
      p.indexOf("/ccna_sim_exam/embed/lab/") !== -1
    );
  }

  function homeSampleActive() {
    try {
      return !!sessionStorage.getItem("ccnaHomeSample");
    } catch (e) {
      return false;
    }
  }

  function hasPortalAccess() {
    if (typeof window.bccPortalAccessActive === "function" && window.bccPortalAccessActive()) {
      return true;
    }
    return false;
  }

  /** Timed exam / free-assessment iframe embeds use ?examSim=1 on question URLs. */
  function examSimEmbedActive() {
    try {
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
    if (examSimEmbedActive()) return;
    redirectToPurchase();
  }

  function boot() {
    if (!isPaidContentPath() || homeSampleActive()) return;

    var chain = Promise.resolve();
    if (typeof window.bccApplyCcnaPortalCheckoutFromUrl === "function") {
      chain = chain.then(function () {
        return window.bccApplyCcnaPortalCheckoutFromUrl(null, true);
      });
    }
    if (typeof window.bccRestoreCcnaPortalAccess === "function") {
      chain = chain.then(function () {
        return window.bccRestoreCcnaPortalAccess();
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

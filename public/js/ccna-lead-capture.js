/**
 * CCNA free timed simulation — guest access (no email gate on the landing page).
 */
(function () {
  "use strict";

  var RUNNER_PATH = "/CCNA_Sim_EXAM/free-assessment.html?welcome=1";
  var HOME_PATH = "/ccna-home.html";
  var HOME_ASSESSMENT_HASH = "#ccna-lead-capture";

  function hasFreeSimAccess() {
    return typeof window.ccnaFreeSimAccessActive === "function" && window.ccnaFreeSimAccessActive();
  }

  function freeSimWasConsumed() {
    return typeof window.ccnaFreeSimWasConsumed === "function" && window.ccnaFreeSimWasConsumed();
  }

  function ensureGuestFreeSimAccess() {
    if (hasFreeSimAccess()) return true;
    if (freeSimWasConsumed()) return false;
    if (typeof window.grantCcnaGuestFreeSimAccess === "function") {
      return window.grantCcnaGuestFreeSimAccess();
    }
    return true;
  }

  function trackFreeSimStart(extra) {
    if (typeof window.bccShouldTrackAnalytics === "function" && !window.bccShouldTrackAnalytics()) {
      return;
    }
    if (typeof window.gtag !== "function") return;
    var attrs = typeof window.bccGetCampaignAttribution === "function" ? window.bccGetCampaignAttribution() || {} : {};
    window.gtag(
      "event",
      "ccna_free_sim_start",
      Object.assign(
        {
          product: "ccna",
          landing_path: location.pathname,
        },
        extra || {},
        attrs.utm_campaign ? { campaign_name: attrs.utm_campaign } : {},
        attrs.utm_content ? { campaign_content: attrs.utm_content } : {}
      )
    );
  }

  function startCcnaFreeSimulation(options) {
    options = options || {};
    if (freeSimWasConsumed()) {
      if (typeof options.onConsumed === "function") {
        options.onConsumed();
        return;
      }
      window.location.href = options.finishHome || HOME_PATH + "#purchase";
      return;
    }
    if (!ensureGuestFreeSimAccess()) {
      window.location.href = options.finishHome || HOME_PATH + HOME_ASSESSMENT_HASH;
      return;
    }
    trackFreeSimStart({ method: options.method || "ccna_free_sim_guest" });
    if (typeof options.onBeforeNavigate === "function") {
      options.onBeforeNavigate();
    }
    window.location.href = options.runnerUrl || RUNNER_PATH;
  }

  function updateLandingAssessmentCta(section) {
    if (!section) return;
    var startBtn = section.querySelector("[data-ccna-start-free-sim]");
    var continueLink = section.querySelector("[data-ccna-continue-free-sim]");
    var consumedNote = section.querySelector("[data-ccna-free-sim-consumed-note]");
    if (hasFreeSimAccess() && !freeSimWasConsumed()) {
      if (continueLink) continueLink.hidden = false;
      return;
    }
    if (freeSimWasConsumed()) {
      if (startBtn) {
        startBtn.textContent = "Free sample completed — see paid options";
        startBtn.setAttribute("href", "#purchase");
        startBtn.removeAttribute("data-ccna-start-free-sim");
        startBtn.classList.add("cta-main--muted");
      }
      if (consumedNote) consumedNote.hidden = false;
    }
  }

  function wireStartButtons() {
    document.querySelectorAll("[data-ccna-start-free-sim]").forEach(function (el) {
      if (el.getAttribute("data-ccna-start-wired") === "1") return;
      el.setAttribute("data-ccna-start-wired", "1");
      el.addEventListener("click", function (ev) {
        ev.preventDefault();
        startCcnaFreeSimulation({ method: el.getAttribute("data-ccna-start-method") || "ccna_free_sim_landing" });
      });
    });
  }

  function showCcnaFreeSimLeadModal(options) {
    startCcnaFreeSimulation(options || {});
  }

  function isCcnaLeadLanding() {
    if (location.hash === HOME_ASSESSMENT_HASH) return true;
    try {
      var qs = new URLSearchParams(location.search);
      if (/lead-free-sim|free-sim|free\.simulation/i.test(qs.get("utm_content") || "")) return true;
    } catch (e) {}
    return false;
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (isCcnaLeadLanding()) {
      document.documentElement.classList.add("ccna-landing-lead-first");
    }

    var section = document.getElementById("ccna-lead-capture");
    if (section) {
      updateLandingAssessmentCta(section);
      wireStartButtons();
    }

    if (
      section &&
      (location.hash === HOME_ASSESSMENT_HASH ||
        /lead-free-sim|free-sim|free\.simulation/i.test(
          (typeof window.bccGetCampaignAttribution === "function"
            ? window.bccGetCampaignAttribution() || {}
            : {}
          ).utm_content || ""
        ))
    ) {
      section.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });

  window.startCcnaFreeSimulation = startCcnaFreeSimulation;
  window.ccnaHasFreeSimAccess = hasFreeSimAccess;
  window.showCcnaFreeSimLeadModal = showCcnaFreeSimLeadModal;
  window.bccIsCcnaLeadLanding = isCcnaLeadLanding;
})();

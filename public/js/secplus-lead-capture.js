/**
 * Security+ free timed simulation — guest access (no email gate on the landing page).
 */
(function () {
  "use strict";

  var RUNNER_PATH = "/COMP_TIA_SEC+/test-simulation-runner.html?free=1";
  var HOME_PATH = "/comptia-sec+-home.html";
  var HOME_ASSESSMENT_HASH = "#secplus-lead-capture";

  function persistFreeSimSessionFlags() {
    try {
      sessionStorage.setItem("secplusTestSimFree", "1");
    } catch (_) {}
  }

  function hasFreeSimAccess() {
    return typeof window.secplusFreeSimAccessActive === "function" && window.secplusFreeSimAccessActive();
  }

  function freeSimWasConsumed() {
    return typeof window.secplusFreeSimWasConsumed === "function" && window.secplusFreeSimWasConsumed();
  }

  function ensureGuestFreeSimAccess() {
    if (hasFreeSimAccess()) return true;
    if (freeSimWasConsumed()) return false;
    if (typeof window.grantSecplusGuestFreeSimAccess === "function") {
      return window.grantSecplusGuestFreeSimAccess();
    }
    return false;
  }

  function trackFreeSimStart(extra) {
    if (typeof window.bccShouldTrackAnalytics === "function" && !window.bccShouldTrackAnalytics()) {
      return;
    }
    if (typeof window.gtag !== "function") return;
    var attrs = typeof window.bccGetCampaignAttribution === "function" ? window.bccGetCampaignAttribution() || {} : {};
    window.gtag(
      "event",
      "secplus_free_sim_start",
      Object.assign(
        {
          product: "secplus",
          landing_path: location.pathname,
        },
        extra || {},
        attrs.utm_campaign ? { campaign_name: attrs.utm_campaign } : {},
        attrs.utm_content ? { campaign_content: attrs.utm_content } : {}
      )
    );
  }

  function startSecplusFreeSimulation(options) {
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
    persistFreeSimSessionFlags();
    trackFreeSimStart({ method: options.method || "secplus_free_sim_guest" });
    if (typeof options.onBeforeNavigate === "function") {
      options.onBeforeNavigate();
    }
    window.location.href = options.runnerUrl || RUNNER_PATH;
  }

  function updateLandingAssessmentCta(section) {
    if (!section) return;
    var startBtn = section.querySelector("[data-secplus-start-free-sim]");
    var continueLink = section.querySelector("[data-secplus-continue-free-sim]");
    var consumedNote = section.querySelector("[data-secplus-free-sim-consumed-note]");
    if (hasFreeSimAccess() && !freeSimWasConsumed()) {
      if (continueLink) continueLink.hidden = false;
      return;
    }
    if (freeSimWasConsumed()) {
      if (startBtn) {
        startBtn.textContent = "Free sample completed — see paid options";
        startBtn.setAttribute("href", "#purchase");
        startBtn.removeAttribute("data-secplus-start-free-sim");
        startBtn.classList.add("cta-main--muted");
      }
      if (consumedNote) consumedNote.hidden = false;
    }
  }

  function wireStartButtons() {
    document.querySelectorAll("[data-secplus-start-free-sim]").forEach(function (el) {
      if (el.getAttribute("data-secplus-start-wired") === "1") return;
      el.setAttribute("data-secplus-start-wired", "1");
      el.addEventListener("click", function (ev) {
        ev.preventDefault();
        startSecplusFreeSimulation({ method: el.getAttribute("data-secplus-start-method") || "secplus_free_sim_landing" });
      });
    });
  }

  function showSecplusFreeSimLeadModal(options) {
    startSecplusFreeSimulation(options || {});
  }

  document.addEventListener("DOMContentLoaded", function () {
    var funnel = document.querySelector(".hero-content .funnel");
    var isLeadLanding =
      typeof window.bccIsSecplusLeadLanding === "function" && window.bccIsSecplusLeadLanding();
    if (isLeadLanding && funnel) {
      funnel.classList.add("funnel--lead-first");
    }

    var section = document.getElementById("secplus-lead-capture");
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

  window.startSecplusFreeSimulation = startSecplusFreeSimulation;
  window.secplusHasFreeSimAccess = hasFreeSimAccess;
  window.showSecplusFreeSimLeadModal = showSecplusFreeSimLeadModal;
})();

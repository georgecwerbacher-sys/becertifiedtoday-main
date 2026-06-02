/**
 * ENCOR free timed simulation — guest access (no email gate on the landing page).
 */
(function () {
  "use strict";

  var RUNNER_PATH = "/CCNP-ENCOR-Study/test-simulation-runner.html?free=1&welcome=1";
  var HOME_PATH = "/ccnp-home.html";
  var HOME_ASSESSMENT_HASH = "#encor-lead-capture";

  function hasFreeSimAccess() {
    return typeof window.encorFreeSimAccessActive === "function" && window.encorFreeSimAccessActive();
  }

  function freeSimWasConsumed() {
    return typeof window.encorFreeSimWasConsumed === "function" && window.encorFreeSimWasConsumed();
  }

  function ensureGuestFreeSimAccess() {
    if (hasFreeSimAccess()) return true;
    if (freeSimWasConsumed()) return false;
    if (typeof window.grantEncorGuestFreeSimAccess === "function") {
      return window.grantEncorGuestFreeSimAccess();
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
      "encor_free_sim_start",
      Object.assign(
        {
          product: "encor",
          landing_path: location.pathname,
        },
        extra || {},
        attrs.utm_campaign ? { campaign_name: attrs.utm_campaign } : {},
        attrs.utm_content ? { campaign_content: attrs.utm_content } : {}
      )
    );
  }

  function startEncorFreeSimulation(options) {
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
    try {
      sessionStorage.setItem("encorTestSimFree", "1");
    } catch (_) {}
    trackFreeSimStart({ method: options.method || "encor_free_sim_guest" });
    if (typeof options.onBeforeNavigate === "function") {
      options.onBeforeNavigate();
    }
    window.location.href = options.runnerUrl || RUNNER_PATH;
  }

  function updateLandingAssessmentCta(section) {
    if (!section) return;
    var startBtn = section.querySelector("[data-encor-start-free-sim]");
    var continueLink = section.querySelector("[data-encor-continue-free-sim]");
    var consumedNote = section.querySelector("[data-encor-free-sim-consumed-note]");
    if (hasFreeSimAccess() && !freeSimWasConsumed()) {
      if (continueLink) continueLink.hidden = false;
      return;
    }
    if (freeSimWasConsumed()) {
      if (startBtn) {
        startBtn.textContent = "Free sample completed — see paid options";
        startBtn.setAttribute("href", "#purchase");
        startBtn.removeAttribute("data-encor-start-free-sim");
        startBtn.classList.add("cta-main--muted");
      }
      if (consumedNote) consumedNote.hidden = false;
    }
  }

  function wireStartButtons() {
    document.querySelectorAll("[data-encor-start-free-sim]").forEach(function (el) {
      if (el.getAttribute("data-encor-start-wired") === "1") return;
      el.setAttribute("data-encor-start-wired", "1");
      el.addEventListener("click", function (ev) {
        ev.preventDefault();
        startEncorFreeSimulation({ method: el.getAttribute("data-encor-start-method") || "encor_free_sim_landing" });
      });
    });
  }

  function showEncorFreeSimLeadModal(options) {
    startEncorFreeSimulation(options || {});
  }

  function isEncorLeadLanding() {
    if (location.hash === HOME_ASSESSMENT_HASH) return true;
    try {
      var qs = new URLSearchParams(location.search);
      if (/lead-free-sim|free-sim|free\.simulation/i.test(qs.get("utm_content") || "")) return true;
    } catch (e) {}
    return false;
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (isEncorLeadLanding()) {
      document.documentElement.classList.add("encor-landing-lead-first");
    }

    var section = document.getElementById("encor-lead-capture");
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

  window.startEncorFreeSimulation = startEncorFreeSimulation;
  window.encorHasFreeSimAccess = hasFreeSimAccess;
  window.showEncorFreeSimLeadModal = showEncorFreeSimLeadModal;
  window.bccIsEncorLeadLanding = isEncorLeadLanding;
})();

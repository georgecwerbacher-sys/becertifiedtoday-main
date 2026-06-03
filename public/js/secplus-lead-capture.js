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

  function campaignAttributionPayload() {
    var attrs = typeof window.bccGetCampaignAttribution === "function" ? window.bccGetCampaignAttribution() || {} : {};
    var out = { product: "secplus", landing_path: location.pathname };
    if (attrs.utm_campaign) out.campaign_name = attrs.utm_campaign;
    if (attrs.utm_content) out.campaign_content = attrs.utm_content;
    if (attrs.utm_source) out.source = attrs.utm_source;
    if (attrs.utm_medium) out.medium = attrs.utm_medium;
    return out;
  }

  function trackFreeSimStart(extra) {
    if (typeof window.bccShouldTrackAnalytics === "function" && !window.bccShouldTrackAnalytics()) {
      return;
    }
    if (typeof window.gtag !== "function") return;
    var payload = Object.assign({}, campaignAttributionPayload(), extra || {}, {
      lead_type: "free_sim_start",
      value: 0,
      currency: "USD",
    });
    window.gtag("event", "secplus_free_sim_start", payload);
    window.gtag("event", "generate_lead", payload);
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
      window.location.href = options.finishHome || HOME_PATH;
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

    if (isLeadLanding && section) {
      var scrollTarget =
        typeof window.bccShouldScrollSecplusLeadCapture === "function" &&
        window.bccShouldScrollSecplusLeadCapture();
      if (scrollTarget) {
        requestAnimationFrame(function () {
          section.scrollIntoView({ behavior: "smooth", block: "start" });
          var startBtn = section.querySelector("[data-secplus-start-free-sim]");
          if (startBtn && typeof startBtn.focus === "function") {
            setTimeout(function () {
              try {
                startBtn.focus({ preventScroll: true });
              } catch (_) {
                startBtn.focus();
              }
            }, 450);
          }
          if (history.replaceState && location.hash === HOME_ASSESSMENT_HASH) {
            history.replaceState(null, "", location.pathname + location.search);
          }
        });
      }
      wireLeadStickyCta(section);
    }
  });

  function wireLeadStickyCta(section) {
    var sticky = document.getElementById("secplusLeadStickyCta");
    if (!sticky || !section) return;
    if (freeSimWasConsumed()) return;
    sticky.hidden = false;
    sticky.setAttribute("aria-hidden", "false");
    var panel = section.querySelector(".assessment-cta-panel");
    if (!panel || typeof IntersectionObserver === "undefined") {
      sticky.classList.add("secplus-lead-sticky-cta--visible");
      return;
    }
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          sticky.classList.toggle("secplus-lead-sticky-cta--visible", !entry.isIntersecting);
        });
      },
      { root: null, threshold: 0, rootMargin: "0px 0px -40% 0px" }
    );
    observer.observe(panel);
  }

  window.startSecplusFreeSimulation = startSecplusFreeSimulation;
  window.secplusHasFreeSimAccess = hasFreeSimAccess;
  window.showSecplusFreeSimLeadModal = showSecplusFreeSimLeadModal;
})();

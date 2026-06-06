/**
 * Bottom purple sticky free-simulation CTA on ccna-home.html and ccnp-home.html.
 * Mirrors SEC+ secplus-lead-sticky-cta behavior (shows after #purchase scrolls out of view).
 */
(function () {
  "use strict";

  var CONFIGS = {
    ccna: {
      homeMatch: "ccna-home",
      stickyId: "ccnaLeadStickyCta",
      linkId: "ccnaLeadStickyCtaLink",
      observeId: "purchase",
      htmlPadClass: "bcc-ccna-lead-sticky-visible",
      lastChanceVisibleClass: "bcc-ccna-last-chance-visible",
      freeLabel: "Start free 45-min simulation",
      consumedLabel: "Get 30-day access",
      runnerPath: "/CCNA_Sim_EXAM/free-assessment.html?welcome=1",
      purchaseHash: "#purchase",
      startMethod: "ccna_free_sim_sticky",
      startAttr: "data-ccna-start-free-sim",
      wasConsumed: function () {
        return (
          typeof window.ccnaFreeSimWasConsumed === "function" && window.ccnaFreeSimWasConsumed()
        );
      },
      startFree: function () {
        if (typeof window.startCcnaFreeSimulation === "function") {
          window.startCcnaFreeSimulation({ method: "ccna_free_sim_sticky" });
        } else {
          window.location.href = "/CCNA_Sim_EXAM/free-assessment.html?welcome=1";
        }
      },
    },
    encor: {
      homeMatch: "ccnp-home",
      stickyId: "encorLeadStickyCta",
      linkId: "encorLeadStickyCtaLink",
      observeId: "purchase",
      htmlPadClass: "bcc-encor-lead-sticky-visible",
      lastChanceVisibleClass: "bcc-encor-last-chance-visible",
      freeLabel: "Start free 45-min simulation",
      consumedLabel: "Get 30-day access",
      runnerPath: "/CCNP-ENCOR-Study/test-simulation-runner.html?free=1&welcome=1",
      purchaseHash: "#purchase",
      startMethod: "encor_free_sim_sticky",
      startAttr: "data-encor-start-free-sim",
      wasConsumed: function () {
        return (
          typeof window.encorFreeSimWasConsumed === "function" && window.encorFreeSimWasConsumed()
        );
      },
      startFree: function () {
        if (typeof window.startEncorFreeSimulation === "function") {
          window.startEncorFreeSimulation({ method: "encor_free_sim_sticky" });
        } else {
          window.location.href = "/CCNP-ENCOR-Study/test-simulation-runner.html?free=1&welcome=1";
        }
      },
    },
  };

  var cfg = null;
  var sticky = null;
  var link = null;
  var wired = false;

  function detectConfig() {
    var path = location.pathname || "";
    if (path.indexOf(CONFIGS.ccna.homeMatch) >= 0) return CONFIGS.ccna;
    if (path.indexOf(CONFIGS.encor.homeMatch) >= 0) return CONFIGS.encor;
    return null;
  }

  function offerModalOpen() {
    var ids = ["ccna10dOfferRoot", "encor10dOfferRoot"];
    for (var i = 0; i < ids.length; i++) {
      var root = document.getElementById(ids[i]);
      if (root && root.classList.contains("ccna-sim-promo-root--open")) return true;
    }
    return false;
  }

  function portalGateOpen() {
    var ids = ["ccna-portal-gate", "ccnp-portal-gate"];
    for (var i = 0; i < ids.length; i++) {
      var gate = document.getElementById(ids[i]);
      if (gate && gate.classList.contains("ccna-sim-promo-root--open")) return true;
    }
    return false;
  }

  function lastChanceVisible() {
    if (!cfg) return false;
    return document.documentElement.classList.contains(cfg.lastChanceVisibleClass);
  }

  function canShowSticky() {
    return !offerModalOpen() && !portalGateOpen() && !lastChanceVisible();
  }

  function setStickyVisible(show) {
    if (!sticky) return;
    var visible = !!show && canShowSticky();
    sticky.classList.toggle("bcc-lead-sticky-cta--visible", visible);
    document.documentElement.classList.toggle(cfg.htmlPadClass, visible);
  }

  function configureLink() {
    if (!link || !cfg) return;
    if (cfg.wasConsumed()) {
      link.textContent = cfg.consumedLabel;
      link.setAttribute("href", cfg.purchaseHash);
      link.removeAttribute(cfg.startAttr);
      link.removeAttribute("data-bcc-lead-sticky-start");
      return;
    }
    link.textContent = cfg.freeLabel;
    link.setAttribute("href", cfg.runnerPath);
    link.setAttribute(cfg.startAttr, "");
    link.setAttribute("data-bcc-lead-sticky-start", "");
  }

  function wireLink() {
    if (!link) return;
    link.addEventListener("click", function (ev) {
      if (!link.hasAttribute("data-bcc-lead-sticky-start")) return;
      ev.preventDefault();
      cfg.startFree();
    });
  }

  function wireObserver() {
    var target = document.getElementById(cfg.observeId);
    if (!sticky || !target) {
      setStickyVisible(true);
      return;
    }
    if (typeof IntersectionObserver === "undefined") {
      sticky.hidden = false;
      sticky.setAttribute("aria-hidden", "false");
      setStickyVisible(true);
      return;
    }
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          setStickyVisible(!entry.isIntersecting);
        });
      },
      { root: null, threshold: 0, rootMargin: "0px 0px -8% 0px" }
    );
    observer.observe(target);
  }

  function init() {
    cfg = detectConfig();
    if (!cfg || wired) return;
    sticky = document.getElementById(cfg.stickyId);
    link = document.getElementById(cfg.linkId);
    if (!sticky || !link) return;
    wired = true;
    sticky.hidden = false;
    sticky.setAttribute("aria-hidden", "false");
    configureLink();
    wireLink();
    wireObserver();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

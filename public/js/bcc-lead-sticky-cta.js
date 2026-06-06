/**
 * Bottom purple sticky $9.99 / 10-day offer on ccna-home.html, ccnp-home.html, and comptia-sec+-home.html.
 * Shows after #purchase scrolls out of view while the visitor has no active portal access.
 */
(function () {
  "use strict";

  var CONFIGS = {
    ccna: {
      homeMatch: "ccna-home",
      stickyId: "ccnaLeadStickyCta",
      btnId: "ccnaLeadStickyCtaBtn",
      observeId: "purchase",
      htmlPadClass: "bcc-ccna-lead-sticky-visible",
      lastChanceVisibleClass: "bcc-ccna-last-chance-visible",
      dismissedKey: "bcc_ccna_10d_one_time_offer_v1",
      checkoutAttr: "data-ccna-portal-10d-checkout",
      offerLabel: "Get 10-day access · $9.99",
      noteText: "One-time $9.99 · closes when you leave this page",
      hasAccess: function () {
        return (
          typeof window.bccPortalAccessActive === "function" && window.bccPortalAccessActive()
        );
      },
    },
    encor: {
      homeMatch: "ccnp-home",
      stickyId: "encorLeadStickyCta",
      btnId: "encorLeadStickyCtaBtn",
      observeId: "purchase",
      htmlPadClass: "bcc-encor-lead-sticky-visible",
      lastChanceVisibleClass: "bcc-encor-last-chance-visible",
      dismissedKey: "bcc_encor_10d_one_time_offer_v1",
      checkoutAttr: "data-encor-portal-10d-checkout",
      offerLabel: "Get 10-day access · $9.99",
      noteText: "One-time $9.99 · closes when you leave this page",
      hasAccess: function () {
        return (
          typeof window.bccEncorPortalAccessActive === "function" &&
          window.bccEncorPortalAccessActive()
        );
      },
    },
    secplus: {
      homeMatch: "comptia-sec+-home",
      stickyId: "secplusLeadStickyCta",
      btnId: "secplusLeadStickyCtaBtn",
      observeId: "purchase",
      htmlPadClass: "bcc-secplus-lead-sticky-visible",
      lastChanceVisibleClass: "bcc-secplus-last-chance-visible",
      dismissedKey: "bcc_secplus_10d_one_time_offer_v1",
      checkoutAttr: "data-secplus-portal-10d-checkout",
      offerLabel: "Get 10-day access · $9.99",
      noteText: "One-time $9.99 · closes when you leave this page",
      hasAccess: function () {
        return (
          typeof window.bccSecplusPortalAccessActive === "function" &&
          window.bccSecplusPortalAccessActive()
        );
      },
    },
  };

  var cfg = null;
  var sticky = null;
  var btn = null;
  var wired = false;

  function detectConfig() {
    var path = location.pathname || "";
    if (path.indexOf(CONFIGS.ccna.homeMatch) >= 0) return CONFIGS.ccna;
    if (path.indexOf(CONFIGS.encor.homeMatch) >= 0) return CONFIGS.encor;
    if (path.indexOf(CONFIGS.secplus.homeMatch) >= 0) return CONFIGS.secplus;
    return null;
  }

  function markDismissed() {
    if (typeof window.bccMark10dOneTimeOfferDismissed === "function") {
      window.bccMark10dOneTimeOfferDismissed();
    } else if (cfg) {
      try {
        localStorage.setItem(cfg.dismissedKey, "1");
      } catch (_) {}
    }
    setStickyVisible(false);
  }

  function canShowOffer() {
    return !!(cfg && !cfg.hasAccess());
  }

  function offerModalOpen() {
    var ids = ["ccna10dOfferRoot", "encor10dOfferRoot", "secplus10dOfferRoot"];
    for (var i = 0; i < ids.length; i++) {
      var root = document.getElementById(ids[i]);
      if (root && root.classList.contains("ccna-sim-promo-root--open")) return true;
    }
    return false;
  }

  function portalGateOpen() {
    var ids = ["ccna-portal-gate", "ccnp-portal-gate", "secplusPortalGateRoot"];
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
    return canShowOffer() && !offerModalOpen() && !portalGateOpen() && !lastChanceVisible();
  }

  function setStickyVisible(show) {
    if (!sticky || !cfg) return;
    var visible = !!show && canShowSticky();
    sticky.classList.toggle("bcc-lead-sticky-cta--visible", visible);
    document.documentElement.classList.toggle(cfg.htmlPadClass, visible);
    if (visible) {
      sticky.removeAttribute("hidden");
      sticky.hidden = false;
      sticky.setAttribute("aria-hidden", "false");
      return;
    }
    if (!canShowOffer()) {
      sticky.hidden = true;
      sticky.setAttribute("hidden", "");
      sticky.setAttribute("aria-hidden", "true");
      document.documentElement.classList.remove(cfg.htmlPadClass);
    }
  }

  function refreshStickyFromScroll() {
    if (!sticky || !cfg || !canShowOffer()) {
      setStickyVisible(false);
      return;
    }
    var target = document.getElementById(cfg.observeId);
    if (!target) {
      setStickyVisible(true);
      return;
    }
    var rect = target.getBoundingClientRect();
    var vh = window.innerHeight || document.documentElement.clientHeight || 0;
    var purchaseInView = rect.bottom > 0 && rect.top < vh * 0.92;
    setStickyVisible(!purchaseInView);
  }

  function wireCheckout() {
    if (!btn) return;
    btn.addEventListener("click", function () {
      markDismissed();
    });
  }

  function wireObserver() {
    if (!sticky) return;
    var target = document.getElementById(cfg.observeId);
    if (!target) {
      if (canShowOffer()) {
        sticky.hidden = false;
        sticky.setAttribute("aria-hidden", "false");
        setStickyVisible(true);
      }
      return;
    }
    if (typeof IntersectionObserver === "undefined") {
      window.addEventListener("scroll", refreshStickyFromScroll, { passive: true });
      window.addEventListener("resize", refreshStickyFromScroll, { passive: true });
      refreshStickyFromScroll();
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
    refreshStickyFromScroll();
  }

  function init() {
    cfg = detectConfig();
    if (!cfg || wired) return;
    sticky = document.getElementById(cfg.stickyId);
    btn = document.getElementById(cfg.btnId);
    if (!sticky || !btn) return;
    wired = true;
    document.addEventListener("bcc-10d-offer-state-change", function () {
      if (!canShowOffer()) setStickyVisible(false);
      else refreshStickyFromScroll();
    });
    document.addEventListener("bcc-10d-popup-closed", function () {
      if (!canShowOffer()) return;
      sticky.hidden = false;
      sticky.setAttribute("aria-hidden", "false");
      refreshStickyFromScroll();
    });
    if (!canShowOffer()) {
      sticky.hidden = true;
      sticky.setAttribute("aria-hidden", "true");
      return;
    }
    sticky.hidden = false;
    sticky.setAttribute("aria-hidden", "false");
    wireCheckout();
    wireObserver();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

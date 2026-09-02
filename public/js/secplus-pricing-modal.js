/**
 * Security+ home: show the 30-day access card as a popup after the visitor
 * scrolls past the samples (below the fold). #purchase links reopen it.
 */
(function () {
  "use strict";

  var MODAL_ID = "secplusPricingModal";
  var DISMISS_KEY = "bcc_secplus_pricing_modal_dismissed_v1";
  var AUTO_SHOWN_KEY = "bcc_secplus_pricing_modal_auto_v1";
  var open = false;
  var lastFocus = null;

  function modalEl() {
    return document.getElementById(MODAL_ID);
  }

  function isPortalMember() {
    return (
      typeof window.bccSecplusPortalAccessActive === "function" &&
      window.bccSecplusPortalAccessActive()
    );
  }

  function dismissed() {
    try {
      return sessionStorage.getItem(DISMISS_KEY) === "1";
    } catch (_) {
      return false;
    }
  }

  function markDismissed() {
    try {
      sessionStorage.setItem(DISMISS_KEY, "1");
    } catch (_) {}
  }

  function autoShown() {
    try {
      return sessionStorage.getItem(AUTO_SHOWN_KEY) === "1";
    } catch (_) {
      return false;
    }
  }

  function markAutoShown() {
    try {
      sessionStorage.setItem(AUTO_SHOWN_KEY, "1");
    } catch (_) {}
  }

  function portalGateOpen() {
    var gate = document.getElementById("secplusPortalGateRoot");
    return !!(gate && gate.classList.contains("ccna-sim-promo-root--open"));
  }

  function pastFold() {
    if ((window.scrollY || 0) < 64) return false;
    var trigger = document.getElementById("secplusPricingModalTrigger");
    if (trigger) {
      return trigger.getBoundingClientRect().top < window.innerHeight * 0.78;
    }
    var samples = document.getElementById("secplus-samples");
    if (samples) {
      return samples.getBoundingClientRect().bottom < window.innerHeight * 0.28;
    }
    return (window.scrollY || 0) > window.innerHeight * 0.55;
  }

  function openModal() {
    var root = modalEl();
    if (!root || open || isPortalMember() || portalGateOpen()) return;
    lastFocus = document.activeElement;
    open = true;
    root.hidden = false;
    root.classList.add("is-open");
    document.documentElement.classList.add("secplus-pricing-modal-open");
    var panel = root.querySelector(".secplus-pricing-modal-dialog");
    if (panel) panel.focus();
  }

  function closeModal(fromUser) {
    var root = modalEl();
    if (!root || !open) return;
    open = false;
    root.classList.remove("is-open");
    root.hidden = true;
    document.documentElement.classList.remove("secplus-pricing-modal-open");
    if (fromUser) markDismissed();
    if (location.hash === "#purchase") {
      try {
        history.replaceState(null, "", location.pathname + location.search);
      } catch (_) {}
    }
    if (lastFocus && typeof lastFocus.focus === "function") {
      try {
        lastFocus.focus();
      } catch (_) {}
    }
  }

  function isPurchaseHashLink(a) {
    if (!a) return false;
    var href = a.getAttribute("href") || "";
    if (href === "#purchase") return true;
    try {
      var u = new URL(a.href, location.href);
      var here = (location.pathname || "").replace(/\/$/, "") || "/";
      var there = (u.pathname || "").replace(/\/$/, "") || "/";
      return u.hash === "#purchase" && here === there;
    } catch (_) {
      return false;
    }
  }

  function onPurchaseLinkClick(event) {
    var a = event.target && event.target.closest ? event.target.closest("a[href]") : null;
    if (!isPurchaseHashLink(a)) return;
    event.preventDefault();
    event.stopPropagation();
    if (typeof event.stopImmediatePropagation === "function") event.stopImmediatePropagation();
    openModal();
  }

  function firstVisitBannerActive() {
    return typeof window.bccSave50PromoActive === "function" && window.bccSave50PromoActive();
  }

  function maybeAutoOpen() {
    if (open || isPortalMember() || dismissed() || autoShown()) return;
    if (firstVisitBannerActive()) return;
    if (!pastFold()) return;
    markAutoShown();
    openModal();
  }

  function boot() {
    var root = modalEl();
    if (!root) return;

    root.querySelectorAll("[data-secplus-pricing-dismiss]").forEach(function (el) {
      el.addEventListener("click", function () {
        closeModal(true);
      });
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && open) {
        event.preventDefault();
        closeModal(true);
      }
    });

    document.addEventListener("click", onPurchaseLinkClick, true);

    window.addEventListener(
      "scroll",
      function () {
        maybeAutoOpen();
      },
      { passive: true }
    );

    window.addEventListener("hashchange", function () {
      if (location.hash === "#purchase") openModal();
    });

    if (location.hash === "#purchase") {
      openModal();
    } else {
      maybeAutoOpen();
    }
  }

  window.bccOpenSecplusPricingModal = openModal;
  window.bccCloseSecplusPricingModal = closeModal;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();

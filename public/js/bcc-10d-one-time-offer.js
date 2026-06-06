/**
 * One-time $9.99 / 10-day access on ccna-home.html, ccnp-home.html, and comptia-sec+-home.html:
 * - Modal popup 5s after page load (top-of-page timing)
 * - Bottom “last chance” bar after #faq is in view (~5s)
 * Both use the same localStorage dismiss flag (once per browser).
 */
(function () {
  "use strict";

  var CONFIGS = {
    ccna: {
      dismissedKey: "bcc_ccna_10d_one_time_offer_v1",
      rootId: "ccna10dOfferRoot",
      lastChanceBarId: "ccna10dLastChanceBar",
      lastChanceVisibleClass: "bcc-ccna-last-chance-visible",
      homeMatch: "ccna-home",
      checkoutAttr: "data-ccna-portal-10d-checkout",
      samplesHref: "#home-ccna-samples-title",
      hasAccess: function () {
        return (
          typeof window.bccPortalAccessActive === "function" && window.bccPortalAccessActive()
        );
      },
    },
    encor: {
      dismissedKey: "bcc_encor_10d_one_time_offer_v1",
      rootId: "encor10dOfferRoot",
      lastChanceBarId: "encor10dLastChanceBar",
      lastChanceVisibleClass: "bcc-encor-last-chance-visible",
      homeMatch: "ccnp-home",
      checkoutAttr: "data-encor-portal-10d-checkout",
      samplesHref: "#home-encor-samples-title",
      hasAccess: function () {
        return (
          typeof window.bccEncorPortalAccessActive === "function" &&
          window.bccEncorPortalAccessActive()
        );
      },
    },
    secplus: {
      dismissedKey: "bcc_secplus_10d_one_time_offer_v1",
      rootId: "secplus10dOfferRoot",
      lastChanceBarId: "secplus10dLastChanceBar",
      lastChanceVisibleClass: "bcc-secplus-last-chance-visible",
      homeMatch: "comptia-sec+-home",
      checkoutAttr: "data-secplus-portal-10d-checkout",
      samplesHref: "#home-secplus-samples-title",
      hasAccess: function () {
        return (
          typeof window.bccSecplusPortalAccessActive === "function" &&
          window.bccSecplusPortalAccessActive()
        );
      },
    },
  };

  var PURCHASE_POPUP_DELAY_MS = 5000;
  var LAST_CHANCE_FAQ_DELAY_MS = 5000;
  var FAQ_ID = "faq";

  var cfg = null;
  var root = null;
  var panel = null;
  var lastChanceBar = null;
  var popupShown = false;
  var lastChanceShown = false;
  var faqObserver = null;
  var purchasePopupDelayId = null;
  var lastChanceDelayId = null;
  var wired = false;

  function detectConfig() {
    var path = location.pathname || "";
    if (path.indexOf(CONFIGS.ccna.homeMatch) >= 0) return CONFIGS.ccna;
    if (path.indexOf(CONFIGS.encor.homeMatch) >= 0) return CONFIGS.encor;
    if (path.indexOf(CONFIGS.secplus.homeMatch) >= 0) return CONFIGS.secplus;
    return null;
  }

  function wasDismissed() {
    if (!cfg) return true;
    try {
      return localStorage.getItem(cfg.dismissedKey) === "1";
    } catch (_) {
      return false;
    }
  }

  function getTenDayBox() {
    return document.querySelector("#purchase .purchase-track-box--ten-day");
  }

  function markDismissed() {
    if (!cfg) return;
    try {
      localStorage.setItem(cfg.dismissedKey, "1");
    } catch (_) {}
    syncOfferUi();
    hideLastChanceBar();
    try {
      document.dispatchEvent(new CustomEvent("bcc-10d-offer-state-change"));
    } catch (_) {}
  }

  function canOffer() {
    if (!cfg || wasDismissed()) return false;
    if (cfg.hasAccess()) return false;
    if (portalGateOpen()) return false;
    return true;
  }

  function ensureRoot() {
    if (!cfg) return false;
    if (!root) root = document.getElementById(cfg.rootId);
    if (!panel && root) panel = root.querySelector(".ccna-sim-promo-panel");
    return !!(root && panel);
  }

  function clearPurchasePopupDelay() {
    if (purchasePopupDelayId != null) {
      clearTimeout(purchasePopupDelayId);
      purchasePopupDelayId = null;
    }
  }

  function syncOfferUi() {
    if (!cfg) return;
    var box = getTenDayBox();
    if (!box) return;
    if (canOffer()) {
      box.classList.add("purchase-track-box--one-time-live");
    } else {
      box.classList.remove("purchase-track-box--one-time-live");
    }
  }

  function ensureLastChanceBar() {
    if (!cfg) return false;
    if (!lastChanceBar) lastChanceBar = document.getElementById(cfg.lastChanceBarId);
    return !!lastChanceBar;
  }

  function offerModalOpen() {
    return !!(root && root.classList.contains("ccna-sim-promo-root--open"));
  }

  function portalGateOpen() {
    var gateIds = ["ccna-portal-gate", "ccnp-portal-gate", "secplusPortalGateRoot"];
    for (var i = 0; i < gateIds.length; i++) {
      var gate = document.getElementById(gateIds[i]);
      if (gate && gate.classList.contains("ccna-sim-promo-root--open")) return true;
    }
    return false;
  }

  function hideLastChanceBar() {
    if (!ensureLastChanceBar()) return;
    lastChanceBar.classList.remove("bcc-last-chance-bar--visible");
    lastChanceBar.hidden = true;
    lastChanceBar.setAttribute("hidden", "");
    document.documentElement.classList.remove(cfg.lastChanceVisibleClass);
  }

  function showLastChanceBar() {
    if (!ensureLastChanceBar() || lastChanceShown || !canOffer() || offerModalOpen()) return false;
    lastChanceShown = true;
    clearLastChanceDelay();
    if (faqObserver) {
      faqObserver.disconnect();
      faqObserver = null;
    }
    lastChanceBar.removeAttribute("hidden");
    lastChanceBar.hidden = false;
    lastChanceBar.classList.add("bcc-last-chance-bar--visible");
    document.documentElement.classList.add(cfg.lastChanceVisibleClass);
    return true;
  }

  function clearLastChanceDelay() {
    if (lastChanceDelayId != null) {
      clearTimeout(lastChanceDelayId);
      lastChanceDelayId = null;
    }
  }

  function isFaqInView() {
    var faq = document.getElementById(FAQ_ID);
    if (!faq) return false;
    var rect = faq.getBoundingClientRect();
    var vh = window.innerHeight || document.documentElement.clientHeight || 0;
    if (vh <= 0 || rect.height <= 0) return false;
    var visiblePx = Math.min(rect.bottom, vh) - Math.max(rect.top, 0);
    return visiblePx >= 48;
  }

  function scheduleLastChanceDelay() {
    if (lastChanceShown || !canOffer() || lastChanceDelayId != null || offerModalOpen()) return;
    if (!isFaqInView()) return;
    lastChanceDelayId = window.setTimeout(function () {
      lastChanceDelayId = null;
      if (lastChanceShown || !canOffer() || !isFaqInView() || offerModalOpen()) return;
      showLastChanceBar();
    }, LAST_CHANCE_FAQ_DELAY_MS);
  }

  function checkFaqInView() {
    if (lastChanceShown || !canOffer()) {
      clearLastChanceDelay();
      return;
    }
    if (!isFaqInView()) {
      clearLastChanceDelay();
      return;
    }
    scheduleLastChanceDelay();
  }

  function dismissLastChanceBar() {
    markDismissed();
    hideLastChanceBar();
  }

  function closePopup(dismissOffer) {
    clearPurchasePopupDelay();
    if (!ensureRoot()) return;
    root.classList.remove("ccna-sim-promo-root--open");
    root.hidden = true;
    root.setAttribute("hidden", "");
    root.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
    if (dismissOffer) markDismissed();
    else {
      syncOfferUi();
      checkFaqInView();
    }
    try {
      document.dispatchEvent(
        new CustomEvent("bcc-10d-popup-closed", { detail: { dismissed: !!dismissOffer } })
      );
    } catch (_) {}
  }

  function openPopup() {
    if (!ensureRoot() || !canOffer()) return false;
    if (root.classList.contains("ccna-sim-promo-root--open")) return true;

    hideLastChanceBar();
    syncOfferUi();
    root.removeAttribute("hidden");
    root.hidden = false;
    root.setAttribute("aria-hidden", "false");
    root.classList.add("ccna-sim-promo-root--open");
    document.body.style.overflow = "hidden";
    try {
      panel.focus();
    } catch (_) {}
    return true;
  }

  function finishPurchasePopupTrigger() {
    popupShown = true;
    clearPurchasePopupDelay();
  }

  function wirePageLoadPopupTrigger() {
    if (popupShown || !canOffer() || purchasePopupDelayId != null) return;
    purchasePopupDelayId = window.setTimeout(function () {
      purchasePopupDelayId = null;
      if (popupShown || !canOffer()) return;
      if (openPopup()) finishPurchasePopupTrigger();
    }, PURCHASE_POPUP_DELAY_MS);
  }

  function dismissPopup(dismissOffer) {
    closePopup(!!dismissOffer);
  }

  function wirePopup() {
    if (!ensureRoot()) return;

    root.querySelectorAll("[data-bcc-10d-offer-dismiss]").forEach(function (el) {
      el.addEventListener("click", function (ev) {
        if (el.tagName === "A" && el.getAttribute("href") && el.getAttribute("href").charAt(0) === "#") {
          ev.preventDefault();
          dismissPopup(true);
          var target = document.querySelector(el.getAttribute("href"));
          if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
          return;
        }
        dismissPopup(true);
      });
    });

    var checkoutBtn = root.querySelector("[" + cfg.checkoutAttr + "]");
    if (checkoutBtn) {
      checkoutBtn.addEventListener("click", function () {
        markDismissed();
        closePopup(false);
      });
    }

    document.addEventListener("keydown", function (ev) {
      if (ev.key !== "Escape" || !root.classList.contains("ccna-sim-promo-root--open")) return;
      dismissPopup(true);
    });
  }

  function wireLastChanceBar() {
    if (!ensureLastChanceBar()) return;

    lastChanceBar.querySelectorAll("[data-bcc-10d-last-chance-dismiss]").forEach(function (el) {
      el.addEventListener("click", function (ev) {
        ev.preventDefault();
        dismissLastChanceBar();
      });
    });

    var checkoutBtn = lastChanceBar.querySelector("[data-bcc-10d-last-chance-checkout]");
    if (checkoutBtn) {
      checkoutBtn.addEventListener("click", function () {
        markDismissed();
        hideLastChanceBar();
      });
    }
  }

  function wireFaqScrollTrigger() {
    var faq = document.getElementById(FAQ_ID);
    if (!faq) return;

    if (typeof IntersectionObserver !== "undefined") {
      faqObserver = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) checkFaqInView();
            else clearLastChanceDelay();
          });
        },
        { root: null, rootMargin: "0px", threshold: [0, 0.1, 0.25] }
      );
      faqObserver.observe(faq);
    }

    window.addEventListener("scroll", checkFaqInView, { passive: true });
    window.addEventListener("resize", checkFaqInView, { passive: true });
    window.addEventListener("hashchange", checkFaqInView);

    window.requestAnimationFrame(checkFaqInView);
    window.setTimeout(checkFaqInView, 250);
    window.setTimeout(checkFaqInView, 800);
  }

  function init() {
    cfg = detectConfig();
    if (!cfg || wired) return;
    wired = true;
    syncOfferUi();
    wirePopup();
    wireLastChanceBar();
    wirePageLoadPopupTrigger();
    wireFaqScrollTrigger();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  window.bcc10dOneTimeOfferActive = function () {
    return !!(cfg && canOffer());
  };

  window.bccMark10dOneTimeOfferDismissed = function () {
    markDismissed();
  };

  window.bccClose10dOfferForPortalGate = function () {
    clearPurchasePopupDelay();
    clearLastChanceDelay();
    if (ensureRoot() && root.classList.contains("ccna-sim-promo-root--open")) {
      root.classList.remove("ccna-sim-promo-root--open");
      root.hidden = true;
      root.setAttribute("hidden", "");
      root.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
    }
    if (ensureLastChanceBar() && lastChanceBar.classList.contains("bcc-last-chance-bar--visible")) {
      lastChanceBar.classList.remove("bcc-last-chance-bar--visible");
      lastChanceBar.hidden = true;
      lastChanceBar.setAttribute("hidden", "");
      if (cfg) document.documentElement.classList.remove(cfg.lastChanceVisibleClass);
    }
  };
})();

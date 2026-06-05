/**
 * Launch-deal popup for Security+ ad traffic on comptia-sec+-home.html.
 * Opens when the user reaches #purchase (pricing). Launch pricing ($17.99 with ONETIMEDEAL
 * on $24.99 list) stays active only while the popup is open. Closing ends the offer for the session.
 */
(function () {
  "use strict";

  var DEAL = {
    launchPrice: 17.99,
    listPrice: 24.99,
    dismissedKey: "bcc_secplus_launch_deal_dismissed_v1",
  };

  var timerId = null;
  var openedAt = null;
  var root = null;
  var panel = null;
  var purchaseScrollTriggered = false;
  var purchaseObserver = null;
  var scrollListenerBound = false;

  function isSecplusHome() {
    return (location.pathname || "").indexOf("comptia-sec+-home") >= 0;
  }

  function hasTrackingParamsInUrl() {
    try {
      var qs = new URLSearchParams(window.location.search);
      return ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "gclid"].some(function (key) {
        return !!qs.get(key);
      });
    } catch (_) {
      return false;
    }
  }

  function isNewAdTraffic() {
    if (hasTrackingParamsInUrl()) return true;
    if (typeof window.bccShouldScrollSecplusLeadCapture === "function" && window.bccShouldScrollSecplusLeadCapture()) {
      return true;
    }
    var attrs = typeof window.bccGetCampaignAttribution === "function" ? window.bccGetCampaignAttribution() || {} : {};
    if (attrs.gclid) return true;
    if (/cpc|ppc|paid/i.test(attrs.utm_medium || "")) return true;
    if (/secplus/i.test(attrs.utm_campaign || "")) return true;
    if (/google/i.test(attrs.utm_source || "") && (attrs.utm_medium || attrs.utm_campaign)) return true;
    return false;
  }

  function wasDismissed() {
    try {
      return sessionStorage.getItem(DEAL.dismissedKey) === "1";
    } catch (_) {
      return false;
    }
  }

  function markDismissed() {
    try {
      sessionStorage.setItem(DEAL.dismissedKey, "1");
    } catch (_) {}
  }

  function pad(n) {
    return n < 10 ? "0" + n : String(n);
  }

  function formatElapsed(ms) {
    if (ms < 0) ms = 0;
    var totalSec = Math.floor(ms / 1000);
    var m = Math.floor(totalSec / 60);
    var s = totalSec % 60;
    return pad(m) + ":" + pad(s);
  }

  function formatSavings() {
    var save = Math.round((DEAL.listPrice - DEAL.launchPrice) * 100) / 100;
    return save % 1 === 0 ? String(save.toFixed(0)) : save.toFixed(2);
  }

  function setHidden(el, hidden) {
    if (!el) return;
    el.hidden = hidden;
  }

  function countdownEls() {
    return document.querySelectorAll("[data-secplus-launch-countdown]");
  }

  function activateDealUi() {
    document.documentElement.classList.add("secplus-launch-deal-active");

    setHidden(document.getElementById("secplusLaunchUrgencyBar"), false);
    setHidden(document.getElementById("secplusLaunchDealCallout"), false);
    setHidden(document.getElementById("secplusPurchasePriceDeal"), false);
    setHidden(document.getElementById("secplusPurchasePriceStandard"), true);
    setHidden(document.getElementById("secplusPurchaseLaunchPill"), false);
  }

  function deactivateDealUi() {
    document.documentElement.classList.remove("secplus-launch-deal-active");

    setHidden(document.getElementById("secplusLaunchUrgencyBar"), true);
    setHidden(document.getElementById("secplusLaunchDealCallout"), true);
    setHidden(document.getElementById("secplusPurchasePriceDeal"), true);
    setHidden(document.getElementById("secplusPurchasePriceStandard"), false);
    setHidden(document.getElementById("secplusPurchaseLaunchPill"), true);

    var stickyNote = document.getElementById("secplusLeadStickyDealNote");
    if (stickyNote) stickyNote.hidden = true;
  }

  function updateStickyDealNote(label) {
    var note = document.getElementById("secplusLeadStickyDealNote");
    if (!note || !document.documentElement.classList.contains("secplus-launch-deal-active")) return;
    var link = document.getElementById("secplusLeadStickyCtaLink");
    var isUpgrade =
      link &&
      (link.hasAttribute("data-secplus-portal-30d-checkout") || (link.getAttribute("href") || "").indexOf("#purchase") >= 0);
    if (isUpgrade) {
      note.textContent = "Launch rate active · " + label + " · save $" + formatSavings();
      note.hidden = false;
    } else {
      note.hidden = true;
    }
  }

  function tickCountdown() {
    if (!openedAt) return;
    var label = formatElapsed(Date.now() - openedAt);
    countdownEls().forEach(function (el) {
      el.textContent = label;
    });
    updateStickyDealNote(label);
  }

  function stopTimer() {
    if (timerId != null) {
      clearInterval(timerId);
      timerId = null;
    }
    openedAt = null;
  }

  function closePopup(dismissDeal) {
    if (!root) return;
    root.classList.remove("ccna-sim-promo-root--open");
    root.hidden = true;
    root.setAttribute("aria-hidden", "true");
    stopTimer();
    deactivateDealUi();
    if (dismissDeal) markDismissed();
  }

  function openPopup() {
    if (!root || !panel) return;
    openedAt = Date.now();
    activateDealUi();
    root.hidden = false;
    root.removeAttribute("hidden");
    root.setAttribute("aria-hidden", "false");
    root.classList.add("ccna-sim-promo-root--open");
    tickCountdown();
    timerId = setInterval(tickCountdown, 1000);
    try {
      panel.focus();
    } catch (_) {}
  }

  function wirePopup() {
    root = document.getElementById("secplusLaunchDealRoot");
    panel = root && root.querySelector(".ccna-sim-promo-panel");
    if (!root || !panel) return;

    root.querySelectorAll("[data-secplus-launch-deal-dismiss]").forEach(function (el) {
      el.addEventListener("click", function (ev) {
        if (el.hasAttribute("data-secplus-launch-deal-free-sim")) {
          ev.preventDefault();
          closePopup(true);
          var section = document.getElementById("secplus-lead-capture");
          if (section) section.scrollIntoView({ behavior: "smooth", block: "start" });
          return;
        }
        closePopup(true);
      });
    });

    var checkoutBtn = root.querySelector("[data-secplus-launch-deal-checkout]");
    if (checkoutBtn) {
      checkoutBtn.addEventListener("click", function (ev) {
        ev.preventDefault();
        if (typeof window.bccStartSecplusPortalCheckout === "function") {
          window.bccStartSecplusPortalCheckout("30d", checkoutBtn, { applyLaunchPromo: true });
        } else {
          var fallback = document.querySelector("[data-secplus-portal-30d-checkout]");
          if (fallback) fallback.click();
        }
        closePopup(false);
      });
    }

    document.addEventListener("keydown", function (ev) {
      if (ev.key !== "Escape" || root.hidden || !root.classList.contains("ccna-sim-promo-root--open")) return;
      closePopup(true);
    });
  }

  function wireStickyObserver() {
    var link = document.getElementById("secplusLeadStickyCtaLink");
    if (!link || typeof MutationObserver === "undefined") return;
    var observer = new MutationObserver(function () {
      if (document.documentElement.classList.contains("secplus-launch-deal-active") && openedAt) {
        updateStickyDealNote(formatElapsed(Date.now() - openedAt));
      }
    });
    observer.observe(link, { attributes: true, attributeFilter: ["href", "data-secplus-portal-30d-checkout"] });
  }

  function canOfferLaunchDeal() {
    return isNewAdTraffic() && !wasDismissed();
  }

  function tryOpenPopupAtPurchase() {
    if (purchaseScrollTriggered || !canOfferLaunchDeal()) return;
    if (root && !root.hidden && root.classList.contains("ccna-sim-promo-root--open")) return;
    purchaseScrollTriggered = true;
    if (purchaseObserver) {
      purchaseObserver.disconnect();
      purchaseObserver = null;
    }
    openPopup();
  }

  function isPurchaseSectionInView() {
    var purchase = document.getElementById("purchase");
    if (!purchase) return false;
    var rect = purchase.getBoundingClientRect();
    var vh = window.innerHeight || document.documentElement.clientHeight || 0;
    if (vh <= 0 || rect.height <= 0) return false;
    var visiblePx = Math.min(rect.bottom, vh) - Math.max(rect.top, 0);
    return visiblePx >= Math.min(80, rect.height * 0.12);
  }

  function checkPurchaseInView() {
    if (isPurchaseSectionInView()) tryOpenPopupAtPurchase();
  }

  function wirePurchaseScrollTrigger() {
    var purchase = document.getElementById("purchase");
    if (!purchase) return;

    if (typeof IntersectionObserver !== "undefined") {
      purchaseObserver = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) tryOpenPopupAtPurchase();
          });
        },
        { root: null, rootMargin: "0px 0px -5% 0px", threshold: [0, 0.08, 0.15] }
      );
      purchaseObserver.observe(purchase);
    }

    if (!scrollListenerBound) {
      scrollListenerBound = true;
      window.addEventListener("scroll", checkPurchaseInView, { passive: true });
      window.addEventListener("resize", checkPurchaseInView, { passive: true });
    }

    document.addEventListener(
      "click",
      function (ev) {
        var target = ev.target && ev.target.closest ? ev.target.closest("a[href*='#purchase'], [data-secplus-portal-30d-checkout]") : null;
        if (!target) return;
        window.setTimeout(checkPurchaseInView, 120);
        window.setTimeout(checkPurchaseInView, 480);
      },
      true
    );

    window.addEventListener("hashchange", function () {
      if (location.hash === "#purchase") checkPurchaseInView();
    });

    window.requestAnimationFrame(function () {
      checkPurchaseInView();
      window.setTimeout(checkPurchaseInView, 300);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (!isSecplusHome()) return;
    wirePopup();
    wireStickyObserver();
    wirePurchaseScrollTrigger();
  });

  window.bccSecplusLaunchDealActive = function () {
    return document.documentElement.classList.contains("secplus-launch-deal-active");
  };

  window.bccRefreshSecplusLaunchDealSticky = function () {
    if (!document.documentElement.classList.contains("secplus-launch-deal-active") || !openedAt) return;
    updateStickyDealNote(formatElapsed(Date.now() - openedAt));
  };
})();

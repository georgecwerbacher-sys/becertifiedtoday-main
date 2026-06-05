/**
 * Launch-deal popup on comptia-sec+-home.html.
 * Opens when the user reaches #purchase (pricing). ONETIMEDEAL ($17.99 on $24.99 list)
 * stays active only while the popup is open. Closing ends the offer for this session.
 */
(function () {
  "use strict";

  var DEAL = {
    launchPrice: 17.99,
    listPrice: 24.99,
    dismissedKey: "bcc_secplus_launch_deal_dismissed_v2",
  };

  var timerId = null;
  var openedAt = null;
  var root = null;
  var panel = null;
  var popupShown = false;
  var purchaseObserver = null;
  var wired = false;

  function isSecplusHome() {
    return (location.pathname || "").indexOf("comptia-sec+-home") >= 0;
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

  function canOfferLaunchDeal() {
    return !wasDismissed();
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

  function ensureRoot() {
    if (!root) root = document.getElementById("secplusLaunchDealRoot");
    if (!panel && root) panel = root.querySelector(".ccna-sim-promo-panel");
    return root && panel;
  }

  function closePopup(dismissDeal) {
    if (!ensureRoot()) return;
    root.classList.remove("ccna-sim-promo-root--open");
    root.hidden = true;
    root.setAttribute("hidden", "");
    root.setAttribute("aria-hidden", "true");
    root.style.display = "";
    document.body.style.overflow = "";
    stopTimer();
    deactivateDealUi();
    if (dismissDeal) markDismissed();
  }

  function openPopup() {
    if (!ensureRoot() || !canOfferLaunchDeal()) return false;
    if (root.classList.contains("ccna-sim-promo-root--open")) return true;

    openedAt = Date.now();
    activateDealUi();
    root.removeAttribute("hidden");
    root.hidden = false;
    root.setAttribute("aria-hidden", "false");
    root.classList.add("ccna-sim-promo-root--open");
    root.style.display = "grid";
    document.body.style.overflow = "hidden";
    tickCountdown();
    timerId = setInterval(tickCountdown, 1000);
    try {
      panel.focus();
    } catch (_) {}
    return true;
  }

  function tryOpenPopupAtPurchase() {
    if (popupShown || !canOfferLaunchDeal()) return;
    if (!isPurchaseSectionInView()) return;
    if (openPopup()) {
      popupShown = true;
      if (purchaseObserver) {
        purchaseObserver.disconnect();
        purchaseObserver = null;
      }
    }
  }

  function isPurchaseSectionInView() {
    var purchase = document.getElementById("purchase");
    if (!purchase) return false;
    var rect = purchase.getBoundingClientRect();
    var vh = window.innerHeight || document.documentElement.clientHeight || 0;
    if (vh <= 0 || rect.height <= 0) return false;
    var visiblePx = Math.min(rect.bottom, vh) - Math.max(rect.top, 0);
    return visiblePx >= 48;
  }

  function checkPurchaseInView() {
    tryOpenPopupAtPurchase();
  }

  function wirePopup() {
    if (!ensureRoot()) return;

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
      if (ev.key !== "Escape" || !root.classList.contains("ccna-sim-promo-root--open")) return;
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
        { root: null, rootMargin: "0px", threshold: [0, 0.1, 0.25] }
      );
      purchaseObserver.observe(purchase);
    }

    window.addEventListener("scroll", checkPurchaseInView, { passive: true });
    window.addEventListener("resize", checkPurchaseInView, { passive: true });

    document.addEventListener(
      "click",
      function (ev) {
        var target =
          ev.target && ev.target.closest
            ? ev.target.closest("a[href*='#purchase'], [data-secplus-portal-30d-checkout]")
            : null;
        if (!target) return;
        window.setTimeout(checkPurchaseInView, 100);
        window.setTimeout(checkPurchaseInView, 400);
        window.setTimeout(checkPurchaseInView, 900);
      },
      true
    );

    window.addEventListener("hashchange", checkPurchaseInView);

    window.requestAnimationFrame(checkPurchaseInView);
    window.setTimeout(checkPurchaseInView, 250);
    window.setTimeout(checkPurchaseInView, 800);
  }

  function init() {
    if (!isSecplusHome() || wired) return;
    wired = true;
    wirePopup();
    wireStickyObserver();
    wirePurchaseScrollTrigger();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  window.bccSecplusLaunchDealActive = function () {
    return document.documentElement.classList.contains("secplus-launch-deal-active");
  };

  window.bccRefreshSecplusLaunchDealSticky = function () {
    if (!document.documentElement.classList.contains("secplus-launch-deal-active") || !openedAt) return;
    updateStickyDealNote(formatElapsed(Date.now() - openedAt));
  };
})();

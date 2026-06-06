/**
 * Bottom “last chance” offer on comptia-sec+-home.html — opens 5s after #faq is in view.
 */
(function () {
  "use strict";

  var CONFIG = {
    dismissedKey: "bcc_secplus_last_chance_dismissed_v1",
    faqDelayMs: 5000,
    faqId: "faq",
  };

  var bar = null;
  var faqObserver = null;
  var faqDelayId = null;
  var lastChanceShown = false;
  var wired = false;

  function isSecplusHome() {
    return (location.pathname || "").indexOf("comptia-sec+-home") >= 0;
  }

  function wasDismissed() {
    try {
      return sessionStorage.getItem(CONFIG.dismissedKey) === "1";
    } catch (_) {
      return false;
    }
  }

  function markDismissed() {
    try {
      sessionStorage.setItem(CONFIG.dismissedKey, "1");
    } catch (_) {}
  }

  function isPortalMember() {
    return (
      typeof window.bccSecplusPortalAccessActive === "function" && window.bccSecplusPortalAccessActive()
    );
  }

  function needsPortalRestore() {
    return (
      typeof window.bccSecplusPortalNeedsRestoreLink === "function" &&
      window.bccSecplusPortalNeedsRestoreLink()
    );
  }

  function launchModalOpen() {
    var root = document.getElementById("secplusLaunchDealRoot");
    return !!(root && root.classList.contains("ccna-sim-promo-root--open"));
  }

  function portalGateOpen() {
    var gate = document.getElementById("secplusPortalGateRoot");
    return !!(gate && gate.classList.contains("ccna-sim-promo-root--open"));
  }

  function canOfferLastChance() {
    return !wasDismissed() && !isPortalMember() && !needsPortalRestore() && !portalGateOpen();
  }

  function ensureBar() {
    if (!bar) bar = document.getElementById("secplusLastChanceBar");
    return bar;
  }

  function clearFaqDelay() {
    if (faqDelayId != null) {
      clearTimeout(faqDelayId);
      faqDelayId = null;
    }
  }

  function hideBar() {
    if (!ensureBar()) return;
    bar.classList.remove("secplus-last-chance-bar--visible");
    bar.hidden = true;
    bar.setAttribute("hidden", "");
    document.documentElement.classList.remove("secplus-last-chance-visible");
  }

  function showBar() {
    if (!ensureBar() || lastChanceShown || !canOfferLastChance() || launchModalOpen() || portalGateOpen()) return false;
    lastChanceShown = true;
    clearFaqDelay();
    if (faqObserver) {
      faqObserver.disconnect();
      faqObserver = null;
    }
    bar.removeAttribute("hidden");
    bar.hidden = false;
    bar.classList.add("secplus-last-chance-bar--visible");
    document.documentElement.classList.add("secplus-last-chance-visible");
    return true;
  }

  function isFaqInView() {
    var faq = document.getElementById(CONFIG.faqId);
    if (!faq) return false;
    var rect = faq.getBoundingClientRect();
    var vh = window.innerHeight || document.documentElement.clientHeight || 0;
    if (vh <= 0 || rect.height <= 0) return false;
    var visiblePx = Math.min(rect.bottom, vh) - Math.max(rect.top, 0);
    return visiblePx >= 48;
  }

  function scheduleLastChanceDelay() {
    if (lastChanceShown || !canOfferLastChance() || faqDelayId != null || launchModalOpen() || portalGateOpen()) return;
    if (!isFaqInView()) return;
    faqDelayId = window.setTimeout(function () {
      faqDelayId = null;
      if (lastChanceShown || !canOfferLastChance() || !isFaqInView() || launchModalOpen()) return;
      showBar();
    }, CONFIG.faqDelayMs);
  }

  function checkFaqInView() {
    if (lastChanceShown || !canOfferLastChance()) {
      clearFaqDelay();
      return;
    }
    if (!isFaqInView()) {
      clearFaqDelay();
      return;
    }
    scheduleLastChanceDelay();
  }

  function dismissBar() {
    markDismissed();
    hideBar();
  }

  function wireBar() {
    if (!ensureBar()) return;

    bar.querySelectorAll("[data-secplus-last-chance-dismiss]").forEach(function (el) {
      el.addEventListener("click", function (ev) {
        ev.preventDefault();
        dismissBar();
      });
    });

    var checkoutBtn = bar.querySelector("[data-secplus-last-chance-checkout]");
    if (checkoutBtn) {
      checkoutBtn.addEventListener("click", function (ev) {
        ev.preventDefault();
        if (typeof window.bccStartSecplusPortalCheckout === "function") {
          window.bccStartSecplusPortalCheckout("30d", checkoutBtn, { applyLaunchPromo: true });
        } else {
          var fallback = document.querySelector("[data-secplus-portal-30d-checkout]");
          if (fallback) fallback.click();
        }
        hideBar();
      });
    }
  }

  function wireFaqTrigger() {
    var faq = document.getElementById(CONFIG.faqId);
    if (!faq) return;

    if (typeof IntersectionObserver !== "undefined") {
      faqObserver = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) checkFaqInView();
            else clearFaqDelay();
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
    if (!isSecplusHome() || wired) return;
    wired = true;
    wireBar();
    wireFaqTrigger();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

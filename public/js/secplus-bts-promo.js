/**
 * Security+ Back to School promo - retired.
 * isActive() stays false so leftover includes cannot remount
 * the banner. CCNA still uses /css/secplus-bts-promo.css for its own pass promo.
 */
(function () {
  "use strict";

  var PROMO_CODE = "AUGUSTPROMO2026";
  var LIST_PRICE = "19.99";
  var SALE_PRICE = "15.99";
  var PROMO_START_MS = new Date("2026-08-01T00:00:00-04:00").getTime();
  var PROMO_END_MS = new Date("2026-09-01T00:00:00-04:00").getTime();
  var VISIT_HOLD_MS = 15 * 60 * 1000;
  var VISIT_END_KEY = "bcc_secplus_bts_visit_end_v1";
  var DOCK_DISMISS_KEY = "bcc_secplus_bts_dock_dismissed_v1";
  var DOCK_SHOW_DELAY_MS = 10000;
  var BAR_ID = "secplusBtsPromoBar";
  var DOCK_ID = "secplusBtsClaimDock";
  var COUNTDOWN_ID = "secplusBtsCountdown";
  var DOCK_COUNTDOWN_ID = "secplusBtsDockCountdown";
  var timerId = null;
  var dockShowId = null;

  function landingPathKey() {
    var p = (location.pathname || "").toLowerCase().replace(/\/$/, "") || "/";
    if (p.endsWith(".html")) p = p.slice(0, -5);
    return p;
  }

  function isSecplusHome() {
    return landingPathKey() === "/comptia-sec+-home";
  }

  function promoEndMs() {
    return PROMO_END_MS;
  }

  function isActive() {
    return false;
  }

  function isPortalMember() {
    return (
      typeof window.bccSecplusPortalAccessActive === "function" &&
      window.bccSecplusPortalAccessActive()
    );
  }

  function visitEndMs() {
    try {
      var raw = sessionStorage.getItem(VISIT_END_KEY);
      var parsed = raw ? parseInt(raw, 10) : 0;
      if (parsed && parsed > Date.now()) return parsed;
      var end = Date.now() + VISIT_HOLD_MS;
      sessionStorage.setItem(VISIT_END_KEY, String(end));
      return end;
    } catch (_) {
      return Date.now() + VISIT_HOLD_MS;
    }
  }

  function visitLeftMs() {
    return Math.max(0, visitEndMs() - Date.now());
  }

  function visitHoldExpired() {
    return visitLeftMs() <= 0;
  }

  function formatCountdown(msLeft) {
    if (msLeft <= 0) return "0:00";
    var totalSec = Math.floor(msLeft / 1000);
    var mins = Math.floor(totalSec / 60);
    var secs = totalSec % 60;
    function pad(n) {
      return n < 10 ? "0" + n : String(n);
    }
    if (mins >= 60) {
      var hours = Math.floor(mins / 60);
      mins = mins % 60;
      return hours + ":" + pad(mins) + ":" + pad(secs);
    }
    return mins + ":" + pad(secs);
  }

  function syncBarHeight() {
    var bar = document.getElementById(BAR_ID);
    if (!bar) return;
    document.documentElement.style.setProperty("--secplus-bts-promo-h", bar.offsetHeight + "px");
  }

  function startCheckout(triggerEl) {
    if (typeof window.bccStartSecplusPortalCheckout === "function") {
      window.bccStartSecplusPortalCheckout("30d", triggerEl || null, { applyLaunchPromo: true });
      return;
    }
    var fallback = document.querySelector("[data-secplus-portal-30d-checkout]");
    if (fallback) fallback.click();
  }

  function updateCountdown() {
    if (!isActive()) {
      teardownAll();
      return;
    }
    var left = visitLeftMs();
    var label = visitHoldExpired() ? "Still open" : formatCountdown(left);
    var top = document.getElementById(COUNTDOWN_ID);
    var dock = document.getElementById(DOCK_COUNTDOWN_ID);
    if (top) top.textContent = label;
    if (dock) dock.textContent = label;

    var barSub = document.querySelector("[data-secplus-bts-visit-copy]");
    if (barSub) {
      if (visitHoldExpired()) {
        barSub.textContent =
          "Still $" + SALE_PRICE + " this August - claim it before you leave this page.";
      } else {
        barSub.innerHTML =
          "Claim <strong>$" +
          SALE_PRICE +
          "</strong> before you leave · code applied at checkout";
      }
    }

    var dockCopy = document.querySelector("[data-secplus-bts-dock-copy]");
    if (dockCopy) {
      dockCopy.innerHTML = visitHoldExpired()
        ? "Back to School <strong>$" + SALE_PRICE + "</strong> is still available - checkout now."
        : "Finish checkout on this visit · <strong>$" + SALE_PRICE + "</strong> locked in at Stripe";
    }
  }

  function teardownAll() {
    if (timerId != null) {
      clearInterval(timerId);
      timerId = null;
    }
    if (dockShowId != null) {
      clearTimeout(dockShowId);
      dockShowId = null;
    }
    var bar = document.getElementById(BAR_ID);
    if (bar) bar.remove();
    var dock = document.getElementById(DOCK_ID);
    if (dock) dock.remove();
    document.documentElement.classList.remove("secplus-bts-promo-active");
    document.documentElement.classList.remove("secplus-bts-dock-visible");
    document.documentElement.style.removeProperty("--secplus-bts-promo-h");
  }

  function updatePurchaseCard() {
    if (!isActive() || !isSecplusHome()) return;

    var priceEl = document.querySelector("#purchase .purchase-price");
    if (priceEl && !priceEl.querySelector(".purchase-price-now")) {
      priceEl.setAttribute("aria-label", "15 dollars and 99 cents for 30 days, back to school price");
      priceEl.innerHTML =
        '<span class="purchase-price-old">$' +
        LIST_PRICE +
        '</span> <span class="purchase-price-now">$' +
        SALE_PRICE +
        "</span> <span>/ 30 days</span>";
    }

    var btn = document.getElementById("secplusPortal30dPurchaseBtn");
    if (btn && !btn.getAttribute("data-bts-cta")) {
      btn.setAttribute("data-bts-cta", "1");
      btn.textContent = "Claim $" + SALE_PRICE + " now";
      btn.setAttribute(
        "aria-label",
        "Claim Back to School price of fifteen ninety-nine and start checkout"
      );
      btn.setAttribute("data-bcc-value", SALE_PRICE);
    }

    document.querySelectorAll("[data-secplus-portal-30d-checkout]").forEach(function (el) {
      el.setAttribute("data-bcc-value", SALE_PRICE);
    });

    var disclaimer = document.querySelector("#purchase .purchase-access-disclaimer");
    if (disclaimer && !disclaimer.getAttribute("data-bts-updated")) {
      disclaimer.setAttribute("data-bts-updated", "1");
      disclaimer.innerHTML =
        "<strong>Claim $" +
        SALE_PRICE +
        " while you're on this page.</strong> Back to School 20% off $" +
        LIST_PRICE +
        " through August - code <code>" +
        PROMO_CODE +
        "</code> is applied at Stripe. No subscription. Access is tied to this browser. " +
        'Eligible for a deeper verified discount? ' +
        '<a href="/verified-learner-discounts.html">Check verified learner pricing</a>.';
    }
  }

  function mountBanner() {
    if (!isSecplusHome() || !isActive() || document.getElementById(BAR_ID) || isPortalMember()) return;

    visitEndMs();
    document.documentElement.classList.add("secplus-bts-promo-active");

    var bar = document.createElement("div");
    bar.id = BAR_ID;
    bar.className = "secplus-bts-promo-bar";
    bar.setAttribute("role", "region");
    bar.setAttribute("aria-label", "Back to School offer - claim while on this page");
    bar.innerHTML =
      '<div class="secplus-bts-promo-bar__inner">' +
      '<div class="secplus-bts-promo-bar__main">' +
      '<p class="secplus-bts-promo-bar__eyebrow">While you\'re here · Back to School</p>' +
      '<p class="secplus-bts-promo-bar__headline">Lock in $' +
      SALE_PRICE +
      " before you leave</p>" +
      '<p class="secplus-bts-promo-bar__sub" data-secplus-bts-visit-copy>Claim <strong>$' +
      SALE_PRICE +
      "</strong> before you leave · code applied at checkout</p>" +
      "</div>" +
      '<div class="secplus-bts-promo-bar__actions">' +
      '<span class="secplus-bts-promo-bar__timer">This visit<br /><strong id="' +
      COUNTDOWN_ID +
      '">--</strong></span>' +
      '<button type="button" class="secplus-bts-promo-bar__cta" data-secplus-bts-checkout>Claim $' +
      SALE_PRICE +
      "</button>" +
      "</div></div>";

    document.body.insertBefore(bar, document.body.firstChild);

    var checkoutBtn = bar.querySelector("[data-secplus-bts-checkout]");
    if (checkoutBtn) {
      checkoutBtn.addEventListener("click", function () {
        startCheckout(checkoutBtn);
      });
    }

    updateCountdown();
    syncBarHeight();
    updatePurchaseCard();
    if (timerId == null) timerId = setInterval(updateCountdown, 1000);
    window.addEventListener("resize", syncBarHeight);
  }

  function dockDismissed() {
    try {
      return sessionStorage.getItem(DOCK_DISMISS_KEY) === "1";
    } catch (_) {
      return false;
    }
  }

  function markDockDismissed() {
    try {
      sessionStorage.setItem(DOCK_DISMISS_KEY, "1");
    } catch (_) {}
  }

  function hideDock() {
    var dock = document.getElementById(DOCK_ID);
    if (dock) dock.remove();
    document.documentElement.classList.remove("secplus-bts-dock-visible");
  }

  function showDock() {
    if (
      !isSecplusHome() ||
      !isActive() ||
      isPortalMember() ||
      dockDismissed() ||
      document.getElementById(DOCK_ID)
    ) {
      return;
    }

    var purchase = document.getElementById("purchase");
    if (purchase) {
      var rect = purchase.getBoundingClientRect();
      var vh = window.innerHeight || 0;
      if (rect.top < vh && rect.bottom > 0) return;
    }

    var dock = document.createElement("div");
    dock.id = DOCK_ID;
    dock.className = "secplus-bts-claim-dock";
    dock.setAttribute("role", "region");
    dock.setAttribute("aria-label", "Claim Back to School price now");
    dock.innerHTML =
      '<div class="secplus-bts-claim-dock__inner">' +
      '<button type="button" class="secplus-bts-claim-dock__close" data-secplus-bts-dock-dismiss aria-label="Dismiss">&times;</button>' +
      '<div class="secplus-bts-claim-dock__copy">' +
      '<p class="secplus-bts-claim-dock__eyebrow">Don\'t leave without it</p>' +
      '<p class="secplus-bts-claim-dock__text" data-secplus-bts-dock-copy>Finish checkout on this visit · <strong>$' +
      SALE_PRICE +
      "</strong> locked in at Stripe</p>" +
      "</div>" +
      '<div class="secplus-bts-claim-dock__actions">' +
      '<span class="secplus-bts-claim-dock__timer" id="' +
      DOCK_COUNTDOWN_ID +
      '">--</span>' +
      '<button type="button" class="secplus-bts-claim-dock__cta" data-secplus-bts-checkout>Claim $' +
      SALE_PRICE +
      " now</button>" +
      "</div></div>";

    document.body.appendChild(dock);
    document.documentElement.classList.add("secplus-bts-dock-visible");

    dock.querySelectorAll("[data-secplus-bts-dock-dismiss]").forEach(function (el) {
      el.addEventListener("click", function () {
        markDockDismissed();
        hideDock();
      });
    });

    var cta = dock.querySelector("[data-secplus-bts-checkout]");
    if (cta) {
      cta.addEventListener("click", function () {
        startCheckout(cta);
      });
    }

    updateCountdown();
  }

  function scheduleDock() {
    if (dockShowId != null || dockDismissed() || isPortalMember()) return;
    dockShowId = window.setTimeout(function () {
      dockShowId = null;
      showDock();
    }, DOCK_SHOW_DELAY_MS);

    var shownOnScroll = false;
    function onScroll() {
      if (shownOnScroll || dockDismissed()) return;
      var y = window.scrollY || document.documentElement.scrollTop || 0;
      if (y > 420) {
        shownOnScroll = true;
        if (dockShowId != null) {
          clearTimeout(dockShowId);
          dockShowId = null;
        }
        showDock();
      }
    }
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  function appendPromoToCheckoutUrl(url) {
    if (!url || !isActive()) return url;
    if (url.indexOf("prefilled_promo_code=") >= 0) return url;
    var sep = url.indexOf("?") >= 0 ? "&" : "?";
    return url + sep + "prefilled_promo_code=" + encodeURIComponent(PROMO_CODE);
  }

  function discountedValue(raw) {
    if (!isActive()) return raw;
    var n = parseFloat(raw);
    if (Number.isNaN(n)) return raw;
    if (Math.abs(n - parseFloat(LIST_PRICE)) < 0.01) return SALE_PRICE;
    return (Math.round(n * 80) / 100).toFixed(2);
  }

  window.bccSecplusBtsPromoActive = isActive;
  window.bccSecplusBtsPromoCode = function () {
    return PROMO_CODE;
  };
  window.bccSecplusBtsPromoEndMs = promoEndMs;
  window.bccSecplusBtsSalePrice = function () {
    return SALE_PRICE;
  };
  window.bccBuildCheckoutUrlWithBts = appendPromoToCheckoutUrl;
  window.bccSecplusBtsDiscountedValue = discountedValue;

  function boot() {
    if (!isActive() || !isSecplusHome()) return;
    mountBanner();
    updatePurchaseCard();
    scheduleDock();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
  window.addEventListener("load", boot);
})();

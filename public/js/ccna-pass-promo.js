/**
 * CCNA landing promo - 30% off (CCNAPASSTODAY → $13.99).
 * Same visit-urgency bar + claim dock as Security+ Back to School.
 * Calendar window through Aug 31, 2026.
 */
(function () {
  "use strict";

  var PROMO_CODE = "CCNAPASSTODAY";
  var LIST_PRICE = "19.99";
  var SALE_PRICE = "13.99";
  var PROMO_START_MS = new Date("2026-08-01T00:00:00-04:00").getTime();
  var PROMO_END_MS = new Date("2026-09-01T00:00:00-04:00").getTime();
  var VISIT_HOLD_MS = 15 * 60 * 1000;
  var VISIT_END_KEY = "bcc_ccna_pass_visit_end_v1";
  var DOCK_DISMISS_KEY = "bcc_ccna_pass_dock_dismissed_v1";
  var DOCK_SHOW_DELAY_MS = 10000;
  var BAR_ID = "ccnaPassPromoBar";
  var DOCK_ID = "ccnaPassClaimDock";
  var COUNTDOWN_ID = "ccnaPassCountdown";
  var DOCK_COUNTDOWN_ID = "ccnaPassDockCountdown";
  var timerId = null;
  var dockShowId = null;

  function landingPathKey() {
    var p = (location.pathname || "").toLowerCase().replace(/\/$/, "") || "/";
    if (p.endsWith(".html")) p = p.slice(0, -5);
    return p;
  }

  function isCcnaHome() {
    return landingPathKey() === "/ccna-home";
  }

  function promoEndMs() {
    return PROMO_END_MS;
  }

  function isActive() {
    if (typeof window.bccSave50PromoActive === "function" && window.bccSave50PromoActive()) {
      return false;
    }
    var now = Date.now();
    return now >= PROMO_START_MS && now < PROMO_END_MS;
  }

  function isPortalMember() {
    return typeof window.bccPortalAccessActive === "function" && window.bccPortalAccessActive();
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
    if (typeof window.bccStartCcnaPortalCheckout === "function") {
      window.bccStartCcnaPortalCheckout("30d", triggerEl || null, { applyLaunchPromo: true });
      return;
    }
    var fallback = document.querySelector("[data-ccna-portal-30d-checkout]");
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

    var barSub = document.querySelector("[data-ccna-pass-visit-copy]");
    if (barSub) {
      if (visitHoldExpired()) {
        barSub.textContent = "Still $" + SALE_PRICE + " with 30% off - claim it before you leave this page.";
      } else {
        barSub.innerHTML =
          "Claim <strong>$" +
          SALE_PRICE +
          "</strong> before you leave · code <code>" +
          PROMO_CODE +
          "</code>";
      }
    }

    var dockCopy = document.querySelector("[data-ccna-pass-dock-copy]");
    if (dockCopy) {
      dockCopy.innerHTML = visitHoldExpired()
        ? "30% off <strong>$" + SALE_PRICE + "</strong> is still available - checkout now."
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
    if (!isActive() || !isCcnaHome()) return;

    var priceEl = document.querySelector("#purchase .home-pricing-price");
    if (priceEl && !priceEl.querySelector(".home-pricing-price-now")) {
      priceEl.setAttribute("aria-label", "13 dollars and 99 cents for 30 days, 30 percent off");
      priceEl.innerHTML =
        '<span class="home-pricing-price-old">$' +
        LIST_PRICE +
        '</span><span class="home-pricing-price-now">$' +
        SALE_PRICE +
        "</span>";
    }

    var btn = document.getElementById("ccnaPortal30dPurchaseBtn");
    if (btn && !btn.getAttribute("data-pass-cta")) {
      btn.setAttribute("data-pass-cta", "1");
      btn.textContent = "Claim $" + SALE_PRICE + " now";
      btn.setAttribute(
        "aria-label",
        "Claim 30 percent off price of thirteen ninety-nine and start checkout"
      );
      btn.setAttribute("data-bcc-value", SALE_PRICE);
    }

    document.querySelectorAll("[data-ccna-portal-30d-checkout]").forEach(function (el) {
      el.setAttribute("data-bcc-value", SALE_PRICE);
    });

    var daily = document.querySelector("#purchase .home-pricing-daily");
    if (daily && !daily.getAttribute("data-pass-updated")) {
      daily.setAttribute("data-pass-updated", "1");
      daily.innerHTML = "Less than <strong>$0.50/day</strong>";
    }

    var badge = document.querySelector("#purchase .home-pricing-badge");
    if (badge && !badge.getAttribute("data-pass-updated")) {
      badge.setAttribute("data-pass-updated", "1");
      badge.textContent = "30% off";
    }

    var footnote = document.querySelector("#purchase .home-pricing-footnote");
    if (footnote && !footnote.getAttribute("data-pass-updated")) {
      footnote.setAttribute("data-pass-updated", "1");
      footnote.innerHTML =
        "<strong>Claim $" +
        SALE_PRICE +
        " while you're on this page.</strong> 30% off $" +
        LIST_PRICE +
        " - code <code>" +
        PROMO_CODE +
        "</code> is applied at Stripe. No subscription. Access is tied to this browser. " +
        'Eligible for a deeper verified discount? ' +
        '<a href="/verified-learner-discounts.html">Check verified learner pricing</a>.';
    }

    var heroUpgrade = document.querySelector(".hero-atf-upgrade a");
    if (heroUpgrade && !heroUpgrade.getAttribute("data-pass-updated")) {
      heroUpgrade.setAttribute("data-pass-updated", "1");
      heroUpgrade.textContent = "Get 30-day CCNA access · $" + SALE_PRICE;
    }
  }

  function mountBanner() {
    if (!isCcnaHome() || !isActive() || document.getElementById(BAR_ID) || isPortalMember()) return;

    visitEndMs();
    document.documentElement.classList.add("secplus-bts-promo-active");

    var bar = document.createElement("div");
    bar.id = BAR_ID;
    bar.className = "secplus-bts-promo-bar";
    bar.setAttribute("role", "region");
    bar.setAttribute("aria-label", "30 percent off CCNA access - claim while on this page");
    bar.innerHTML =
      '<div class="secplus-bts-promo-bar__inner">' +
      '<div class="secplus-bts-promo-bar__main">' +
      '<p class="secplus-bts-promo-bar__eyebrow">While you\'re here · 30% off</p>' +
      '<p class="secplus-bts-promo-bar__headline">Lock in $' +
      SALE_PRICE +
      " before you leave</p>" +
      '<p class="secplus-bts-promo-bar__sub" data-ccna-pass-visit-copy>Claim <strong>$' +
      SALE_PRICE +
      "</strong> before you leave · code <code>" +
      PROMO_CODE +
      "</code></p>" +
      "</div>" +
      '<div class="secplus-bts-promo-bar__actions">' +
      '<span class="secplus-bts-promo-bar__timer">This visit<br /><strong id="' +
      COUNTDOWN_ID +
      '">--</strong></span>' +
      '<button type="button" class="secplus-bts-promo-bar__cta" data-ccna-pass-checkout>Claim $' +
      SALE_PRICE +
      "</button>" +
      "</div></div>";

    document.body.insertBefore(bar, document.body.firstChild);

    var checkoutBtn = bar.querySelector("[data-ccna-pass-checkout]");
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
      !isCcnaHome() ||
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
    dock.setAttribute("aria-label", "Claim 30 percent off CCNA price now");
    dock.innerHTML =
      '<div class="secplus-bts-claim-dock__inner">' +
      '<button type="button" class="secplus-bts-claim-dock__close" data-ccna-pass-dock-dismiss aria-label="Dismiss">&times;</button>' +
      '<div class="secplus-bts-claim-dock__copy">' +
      '<p class="secplus-bts-claim-dock__eyebrow">Don\'t leave without it</p>' +
      '<p class="secplus-bts-claim-dock__text" data-ccna-pass-dock-copy>Finish checkout on this visit · <strong>$' +
      SALE_PRICE +
      "</strong> locked in at Stripe</p>" +
      "</div>" +
      '<div class="secplus-bts-claim-dock__actions">' +
      '<span class="secplus-bts-claim-dock__timer" id="' +
      DOCK_COUNTDOWN_ID +
      '">--</span>' +
      '<button type="button" class="secplus-bts-claim-dock__cta" data-ccna-pass-checkout>Claim $' +
      SALE_PRICE +
      " now</button>" +
      "</div></div>";

    document.body.appendChild(dock);
    document.documentElement.classList.add("secplus-bts-dock-visible");

    dock.querySelectorAll("[data-ccna-pass-dock-dismiss]").forEach(function (el) {
      el.addEventListener("click", function () {
        markDockDismissed();
        hideDock();
      });
    });

    var cta = dock.querySelector("[data-ccna-pass-checkout]");
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
    return (Math.round(n * 70) / 100).toFixed(2);
  }

  window.bccCcnaPassPromoActive = isActive;
  window.bccCcnaPassPromoCode = function () {
    return PROMO_CODE;
  };
  window.bccCcnaPassPromoEndMs = promoEndMs;
  window.bccCcnaPassSalePrice = function () {
    return SALE_PRICE;
  };
  window.bccBuildCheckoutUrlWithCcnaPass = appendPromoToCheckoutUrl;
  window.bccCcnaPassDiscountedValue = discountedValue;

  function boot() {
    if (!isActive() || !isCcnaHome()) return;
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

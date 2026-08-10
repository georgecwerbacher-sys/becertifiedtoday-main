/**
 * Stripe Payment Links for CompTIA Security+ portal access.
 *
 * 30-day list price: $19.99 on the Payment Link (same pattern as CCNA/ENCOR portal pricing).
 * Paste the live Payment Link URL into LINKS["30d"] below.
 *
 * Stripe product name: CompTIA Security+ SY0-701 - 30-day all-access pass
 * Stripe description (≤500 chars): 30 days of SY0-701 exam prep on Be Certified Today: 1000+ interactive practice questions (SY0-701 objectives), PBQ-style hot-spot simulations, adaptive domain review, progress tracking, and a full 90-minute timed practice exam - all in your browser on phone, tablet, or desktop. One-time purchase; no subscription. Access starts at checkout on this device and browser.
 *
 * Redirect after payment:
 *   /COMP_TIA_SEC+/secplus-portal-checkout-success.html?session_id={CHECKOUT_SESSION_ID}
 *
 * Optional metadata on the link: productId = secplus-portal-30d
 *
 * 3-day free trial Payment Link (promo / partner):
 *   https://buy.stripe.com/6oU3cu7gF5Ovglq1xac3m0b
 * Optional metadata: productId = secplus-portal-3d
 */
(function () {
  var LINKS = {
    "3d": "https://buy.stripe.com/6oU3cu7gF5Ovglq1xac3m0b",
    "10d": "https://buy.stripe.com/8x28wObwVfp54CIgs4c3m06",
    "30d": "https://buy.stripe.com/5kQ14mbwVgt93yEfo0c3m07",
  };

  /**
   * AUGUSTPROMO2026 - 20% off Sec+ 30-day ($15.99 on $19.99).
   * Public Back to School for all of August 2026 (see /js/secplus-bts-promo.js).
   * Also used when an older launch-deal session is still active.
   */
  var LAUNCH_PROMO_CODE = "AUGUSTPROMO2026";

  var PRODUCTS = {
    "3d": {
      id: "secplus_portal_3d",
      name: "CompTIA Security+ 3-day free access",
      value: "0.00",
      defaultLabel: "Get 3-day free access",
      labelKey: "secplusPortal3dCheckoutLabel",
    },
    "10d": {
      id: "secplus_portal_10d",
      name: "CompTIA Security+ 10-day access",
      value: "9.99",
      defaultLabel: "Get 10-day access",
      labelKey: "secplusPortal10dCheckoutLabel",
    },
    "30d": {
      id: "secplus_portal_30d",
      name: "CompTIA Security+ 30-day access",
      listValue: "19.99",
      launchValue: "15.99",
      value: "19.99",
      defaultLabel: "Get 30-day access",
      labelKey: "secplusPortal30dCheckoutLabel",
    },
  };

  function btsPromoActive() {
    return typeof window.bccSecplusBtsPromoActive === "function" && window.bccSecplusBtsPromoActive();
  }

  function shouldApplyLaunchPromo(tier, options) {
    if (typeof window.bccSave50PromoActive === "function" && window.bccSave50PromoActive()) {
      return false;
    }
    if (tier !== "30d" || !LAUNCH_PROMO_CODE) return false;
    if (options && options.applyLaunchPromo === true) return true;
    if (options && options.applyLaunchPromo === false) return false;
    if (btsPromoActive()) return true;
    return typeof window.bccSecplusLaunchDealActive === "function" && window.bccSecplusLaunchDealActive();
  }

  function checkoutValueFor(tier, applyLaunchPromo) {
    var product = PRODUCTS[tier];
    if (!product) return "0";
    var raw;
    if (tier === "30d" && applyLaunchPromo) raw = product.launchValue;
    else raw = product.value;
    if (typeof window.bccSave50DiscountedValue === "function") {
      return window.bccSave50DiscountedValue(raw);
    }
    if (typeof window.bccSecplusBtsDiscountedValue === "function") {
      return window.bccSecplusBtsDiscountedValue(raw);
    }
    return raw;
  }

  function buildCheckoutUrl(tier, applyLaunchPromo) {
    var url = LINKS[tier];
    if (!url) return url;
    if (typeof window.bccBuildCheckoutUrlWithSave50 === "function") {
      var withSave50 = window.bccBuildCheckoutUrlWithSave50(url);
      if (withSave50 !== url) return withSave50;
    }
    if (typeof window.bccBuildCheckoutUrlWithBts === "function") {
      var withBts = window.bccBuildCheckoutUrlWithBts(url);
      if (withBts !== url) return withBts;
    }
    if (!applyLaunchPromo || tier !== "30d" || !LAUNCH_PROMO_CODE) return url;
    var sep = url.indexOf("?") >= 0 ? "&" : "?";
    return url + sep + "prefilled_promo_code=" + encodeURIComponent(LAUNCH_PROMO_CODE);
  }

  function startSecplusPortalCheckout(tier, triggerEl, options) {
    options = options || {};
    var product = PRODUCTS[tier];
    var applyLaunchPromo = shouldApplyLaunchPromo(tier, options);
    var url = buildCheckoutUrl(tier, applyLaunchPromo);
    if (!product || !url) return false;

    var trackEl = triggerEl || document.createElement("button");
    if (typeof window.bccTrackBeginCheckout === "function") {
      trackEl.setAttribute("data-bcc-item-id", product.id);
      trackEl.setAttribute("data-bcc-item-name", product.name);
      trackEl.setAttribute("data-bcc-value", checkoutValueFor(tier, applyLaunchPromo));
      trackEl.setAttribute("data-bcc-currency", "USD");
      window.bccTrackBeginCheckout(trackEl);
    }
    if (typeof window.bccSetSecplusPendingPortalTier === "function") {
      window.bccSetSecplusPendingPortalTier(tier);
    }
    window.location.href = url;
    return true;
  }

  function wireCheckout(btn, tier) {
    var product = PRODUCTS[tier];
    if (!product) return;

    if (!btn.dataset[product.labelKey]) {
      btn.dataset[product.labelKey] = btn.textContent.trim() || product.defaultLabel;
    }

    btn.addEventListener("click", function (ev) {
      if (ev && typeof ev.preventDefault === "function") ev.preventDefault();
      if (btn.dataset.loading === "1") return;
      btn.dataset.loading = "1";
      var busyLabel = "Redirecting…";
      if (btn.tagName === "BUTTON") {
        btn.disabled = true;
        btn.textContent = busyLabel;
      } else {
        btn.setAttribute("aria-busy", "true");
        btn.textContent = busyLabel;
      }
      startSecplusPortalCheckout(tier, btn);
    });
  }

  function maybeAutoCheckoutFromUrl() {
    if (location.pathname.indexOf("comptia-sec+-home") < 0) return;
    var qs = new URLSearchParams(location.search);
    if (qs.get("checkout") !== "30d" && qs.get("start_checkout") !== "30d") return;
    startSecplusPortalCheckout("30d", null);
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-secplus-portal-3d-checkout]").forEach(function (btn) {
      wireCheckout(btn, "3d");
    });
    document.querySelectorAll("[data-secplus-portal-30d-checkout]").forEach(function (btn) {
      wireCheckout(btn, "30d");
    });
    maybeAutoCheckoutFromUrl();
  });

  window.bccStartSecplusPortalCheckout = startSecplusPortalCheckout;
  window.bccSecplusLaunchPromoCode = LAUNCH_PROMO_CODE;
})();

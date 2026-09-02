/**
 * Stripe Payment Link for CCNA 30-day full library access.
 *
 * Stripe Dashboard → each Payment Link → After payment → custom redirect URL:
 *   /CCNA-Study/CCNA_Training_Portal.html?session_id={CHECKOUT_SESSION_ID}
 *
 * Optional metadata on the link: productId = ccna-portal-30d
 *
 * CCNAPASSTODAY - 30% off CCNA 30-day ($13.99 on $29.99). Public offer through
 * August 2026 (see /js/ccna-pass-promo.js).
 */
(function () {
  var LINKS = {
    "30d": "https://buy.stripe.com/14A7sK58xccT4CI8ZCc3m03",
  };

  var LAUNCH_PROMO_CODE = "CCNAPASSTODAY";

  var PRODUCTS = {
    "30d": {
      id: "ccna_portal_30d",
      name: "CCNA 30-day access",
      value: "29.99",
      launchValue: "13.99",
      defaultLabel: "Get 30-day access",
      labelKey: "ccnaPortal30dCheckoutLabel",
    },
  };

  function passPromoActive() {
    return typeof window.bccCcnaPassPromoActive === "function" && window.bccCcnaPassPromoActive();
  }

  function shouldApplyLaunchPromo(tier, options) {
    if (typeof window.bccSave50PromoActive === "function" && window.bccSave50PromoActive()) {
      return false;
    }
    if (tier !== "30d" || !LAUNCH_PROMO_CODE) return false;
    if (options && options.applyLaunchPromo === true) return true;
    if (options && options.applyLaunchPromo === false) return false;
    return passPromoActive();
  }

  function checkoutValueFor(tier, applyLaunchPromo) {
    var product = PRODUCTS[tier];
    if (!product) return "0";
    var raw = tier === "30d" && applyLaunchPromo ? product.launchValue : product.value;
    if (typeof window.bccSave50DiscountedValue === "function") {
      var save50 = window.bccSave50DiscountedValue(raw);
      if (save50 !== raw) return save50;
    }
    if (typeof window.bccCcnaPassDiscountedValue === "function") {
      return window.bccCcnaPassDiscountedValue(raw);
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
    if (typeof window.bccBuildCheckoutUrlWithCcnaPass === "function") {
      var withPass = window.bccBuildCheckoutUrlWithCcnaPass(url);
      if (withPass !== url) return withPass;
    }
    if (!applyLaunchPromo || tier !== "30d" || !LAUNCH_PROMO_CODE) return url;
    var sep = url.indexOf("?") >= 0 ? "&" : "?";
    return url + sep + "prefilled_promo_code=" + encodeURIComponent(LAUNCH_PROMO_CODE);
  }

  function startCcnaPortalCheckout(tier, triggerEl, options) {
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
      startCcnaPortalCheckout(tier, btn);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-ccna-portal-30d-checkout]").forEach(function (btn) {
      wireCheckout(btn, "30d");
    });
  });

  window.bccStartCcnaPortalCheckout = startCcnaPortalCheckout;
  window.bccCcnaLaunchPromoCode = LAUNCH_PROMO_CODE;
})();

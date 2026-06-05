/**
 * Stripe Payment Links for CompTIA Security+ portal access.
 *
 * 30-day list price: $24.99 on the Payment Link. Launch offer uses promotion code SECPLUS7
 * ($7.00 off → $17.99 one-time deal at checkout). Create in Stripe Dashboard:
 *   1. Product price $24.99 on the 30-day Payment Link
 *   2. Coupon: $7.00 off (amount_off, USD), one-time, applies to that product
 *   3. Promotion code: SECPLUS7 (must match LAUNCH_PROMO_CODE below)
 *   4. Payment Link → Allow promotion codes: ON
 *   5. Paste the live Payment Link URL into LINKS["30d"] below
 *
 * Stripe product name: CompTIA Security+ SY0-701 — 30-day all-access pass
 * Stripe description (≤500 chars): 30 days of SY0-701 exam prep on Be Certified Today: 800+ interactive practice questions (objectives v5.0), PBQ-style hot-spot simulations, adaptive domain review, progress tracking, and a full 90-minute timed practice exam—all in your browser on phone, tablet, or desktop. One-time purchase; no subscription. Access starts at checkout on this device and browser.
 *
 * Redirect after payment:
 *   /COMP_TIA_SEC+/secplus-portal-checkout-success.html?session_id={CHECKOUT_SESSION_ID}
 *
 * Optional metadata on the link: productId = secplus-portal-30d
 */
(function () {
  var LINKS = {
    "10d": "https://buy.stripe.com/8x28wObwVfp54CIgs4c3m06",
    "30d": "https://buy.stripe.com/5kQ14mbwVgt93yEfo0c3m07",
  };

  /** Must match a live Stripe promotion code tied to a $7.00-off coupon on the 30-day price. */
  var LAUNCH_PROMO_CODE = "SECPLUS7";

  var PRODUCTS = {
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
      listValue: "24.99",
      launchValue: "17.99",
      value: "24.99",
      defaultLabel: "Get 30-day access",
      labelKey: "secplusPortal30dCheckoutLabel",
    },
  };

  function shouldApplyLaunchPromo(tier, options) {
    if (tier !== "30d" || !LAUNCH_PROMO_CODE) return false;
    if (options && options.applyLaunchPromo === true) return true;
    if (options && options.applyLaunchPromo === false) return false;
    return typeof window.bccSecplusLaunchDealActive === "function" && window.bccSecplusLaunchDealActive();
  }

  function checkoutValueFor(tier, applyLaunchPromo) {
    var product = PRODUCTS[tier];
    if (!product) return "0";
    if (tier === "30d" && applyLaunchPromo) return product.launchValue;
    return product.value;
  }

  function buildCheckoutUrl(tier, applyLaunchPromo) {
    var url = LINKS[tier];
    if (!url) return url;
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
    document.querySelectorAll("[data-secplus-portal-10d-checkout]").forEach(function (btn) {
      wireCheckout(btn, "10d");
    });
    document.querySelectorAll("[data-secplus-portal-30d-checkout]").forEach(function (btn) {
      wireCheckout(btn, "30d");
    });
    maybeAutoCheckoutFromUrl();
  });

  window.bccStartSecplusPortalCheckout = startSecplusPortalCheckout;
  window.bccSecplusLaunchPromoCode = LAUNCH_PROMO_CODE;
})();

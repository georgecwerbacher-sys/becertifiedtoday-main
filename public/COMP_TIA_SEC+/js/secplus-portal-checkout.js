/**
 * Stripe checkout for CompTIA Security+ portal access.
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

  var PORTAL_URL = "/COMP_TIA_SEC+/SEC+_Training_Portal.html";

  /**
   * Legacy launch-deal / fence-sitter code. Not a public promo.
   */
  var LAUNCH_PROMO_CODE = "AUGUSTPROMO2026";

  /** 20% off 30-day while an existing 24h entitlement is still active. */
  var TRIAL_PROMO_CODE = "SECPLUS24";

  var PRODUCTS = {
    "24h": {
      id: "secplus_portal_24h",
      name: "CompTIA Security+ 24-hour access",
      value: "0.00",
      defaultLabel: "Open portal",
      labelKey: "secplusPortal24hCheckoutLabel",
    },
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

  function storedPortalProductId() {
    if (typeof window.bccGetSecplusPortalProductId === "function") {
      return window.bccGetSecplusPortalProductId();
    }
    try {
      var stored = JSON.parse(localStorage.getItem("bcc_secplus_portal_v1") || "null");
      return stored && stored.productId ? stored.productId : null;
    } catch (e) {
      return null;
    }
  }

  function portalAccessActive() {
    return typeof window.bccSecplusPortalAccessActive === "function" && window.bccSecplusPortalAccessActive();
  }

  function is24hEntitlementActive() {
    return portalAccessActive() && storedPortalProductId() === "secplus-portal-24h";
  }

  function hasPaidPortalAccess() {
    if (!portalAccessActive()) return false;
    var id = storedPortalProductId();
    return id === "secplus-portal-30d" || id === "secplus-portal-10d";
  }

  function shouldApplyLaunchPromo(tier, options) {
    if (typeof window.bccSave50PromoActive === "function" && window.bccSave50PromoActive()) {
      return false;
    }
    if (tier !== "30d" || !LAUNCH_PROMO_CODE) return false;
    if (options && options.applyLaunchPromo === true) return true;
    if (options && options.applyLaunchPromo === false) return false;
    return typeof window.bccSecplusLaunchDealActive === "function" && window.bccSecplusLaunchDealActive();
  }

  function shouldApplyTrialPromo(tier, options) {
    if (tier !== "30d" || !TRIAL_PROMO_CODE) return false;
    if (typeof window.bccSave50PromoActive === "function" && window.bccSave50PromoActive()) {
      return false;
    }
    if (options && options.applyLaunchPromo === true) return false;
    if (options && options.applyTrialPromo === false) return false;
    if (options && options.applyTrialPromo === true) return true;
    return is24hEntitlementActive();
  }

  function checkoutValueFor(tier, applyLaunchPromo, applyTrialPromo) {
    var product = PRODUCTS[tier];
    if (!product) return "0";
    var raw;
    if (tier === "30d" && (applyLaunchPromo || applyTrialPromo)) raw = product.launchValue;
    else raw = product.value;
    if (typeof window.bccSave50DiscountedValue === "function") {
      return window.bccSave50DiscountedValue(raw);
    }
    return raw;
  }

  function buildCheckoutUrl(tier, applyLaunchPromo, applyTrialPromo) {
    var url = LINKS[tier];
    if (!url) return url;
    if (typeof window.bccBuildCheckoutUrlWithSave50 === "function") {
      var withSave50 = window.bccBuildCheckoutUrlWithSave50(url);
      if (withSave50 !== url) return withSave50;
    }
    var promo = null;
    if (applyLaunchPromo && tier === "30d" && LAUNCH_PROMO_CODE) promo = LAUNCH_PROMO_CODE;
    else if (applyTrialPromo && tier === "30d" && TRIAL_PROMO_CODE) promo = TRIAL_PROMO_CODE;
    if (!promo) return url;
    var sep = url.indexOf("?") >= 0 ? "&" : "?";
    return url + sep + "prefilled_promo_code=" + encodeURIComponent(promo);
  }

  function trackBeginCheckout(tier, triggerEl, applyLaunchPromo, applyTrialPromo) {
    var product = PRODUCTS[tier];
    if (!product || typeof window.bccTrackBeginCheckout !== "function") return;
    var trackEl = triggerEl || document.createElement("button");
    trackEl.setAttribute("data-bcc-item-id", product.id);
    trackEl.setAttribute("data-bcc-item-name", product.name);
    trackEl.setAttribute("data-bcc-value", checkoutValueFor(tier, applyLaunchPromo, applyTrialPromo));
    trackEl.setAttribute("data-bcc-currency", "USD");
    window.bccTrackBeginCheckout(trackEl);
  }

  function resetAllCheckoutButtons() {
    document.querySelectorAll("[data-secplus-portal-24h-checkout]").forEach(function (btn) {
      resetCheckoutButton(btn, PRODUCTS["24h"]);
    });
    document.querySelectorAll("[data-secplus-portal-30d-checkout]").forEach(function (btn) {
      resetCheckoutButton(btn, PRODUCTS["30d"]);
    });
  }

  function leavePricingPopup() {
    if (typeof window.bccCloseSecplusPricingModal === "function") {
      window.bccCloseSecplusPricingModal(true);
    }
  }

  function startSecplus24hCheckout(triggerEl) {
    if (hasPaidPortalAccess() || is24hEntitlementActive()) {
      window.location.href = PORTAL_URL;
      return Promise.resolve(true);
    }
    return Promise.resolve(false);
  }

  function startSecplusPortalCheckout(tier, triggerEl, options) {
    options = options || {};
    if (tier === "24h") {
      return startSecplus24hCheckout(triggerEl);
    }
    var product = PRODUCTS[tier];
    var applyLaunchPromo = shouldApplyLaunchPromo(tier, options);
    var applyTrialPromo = shouldApplyTrialPromo(tier, options);
    var url = buildCheckoutUrl(tier, applyLaunchPromo, applyTrialPromo);
    if (!product || !url) return false;

    trackBeginCheckout(tier, triggerEl, applyLaunchPromo, applyTrialPromo);
    if (typeof window.bccSetSecplusPendingPortalTier === "function") {
      window.bccSetSecplusPendingPortalTier(tier);
    }
    window.location.href = url;
    return true;
  }

  function resetCheckoutButton(btn, product) {
    if (!btn || !product) return;
    btn.dataset.loading = "0";
    var label = btn.dataset[product.labelKey] || product.defaultLabel;
    if (btn.tagName === "BUTTON") {
      btn.disabled = false;
      btn.textContent = label;
    } else {
      btn.removeAttribute("aria-busy");
      btn.textContent = label;
    }
  }

  function beginWiredCheckout(btn, tier) {
    var product = PRODUCTS[tier];
    if (!btn || !product) return;
    if (!btn.dataset[product.labelKey]) {
      btn.dataset[product.labelKey] = btn.textContent.trim() || product.defaultLabel;
    }
    if (btn.dataset.loading === "1") {
      resetCheckoutButton(btn, product);
      leavePricingPopup();
      return;
    }
    btn.dataset.loading = "1";
    var busyLabel = "Redirecting…";
    if (btn.tagName === "BUTTON") {
      btn.disabled = true;
      btn.textContent = busyLabel;
    } else {
      btn.setAttribute("aria-busy", "true");
      btn.textContent = busyLabel;
    }
    var started = startSecplusPortalCheckout(tier, btn);
    if (started && typeof started.then === "function") {
      started.catch(function (err) {
        resetCheckoutButton(btn, product);
        leavePricingPopup();
        window.alert(err && err.message ? err.message : "Could not start checkout.");
      });
    }
  }

  function wireCheckout(btn, tier) {
    var product = PRODUCTS[tier];
    if (!product) return;
    btn.addEventListener("click", function (ev) {
      if (ev && typeof ev.preventDefault === "function") ev.preventDefault();
      if (ev && typeof ev.stopPropagation === "function") ev.stopPropagation();
      beginWiredCheckout(btn, tier);
    });
  }

  function maybeAutoCheckoutFromUrl() {
    if (location.pathname.indexOf("comptia-sec+-home") < 0) return;
    var qs = new URLSearchParams(location.search);
    if (qs.get("checkout") === "24h" || qs.get("start_checkout") === "24h") {
      return;
    }
    if (qs.get("checkout") !== "30d" && qs.get("start_checkout") !== "30d") return;
    startSecplusPortalCheckout("30d", null);
  }

  function hide24hCtas() {
    document.querySelectorAll("[data-secplus-portal-24h-checkout]").forEach(function (el) {
      el.hidden = true;
    });
  }

  function mount24hUpgradeBanner() {
    var banner = document.getElementById("secplus24hUpgradeBanner");
    if (!banner) return;
    if (!is24hEntitlementActive()) return;
    banner.hidden = false;
  }

  document.addEventListener(
    "click",
    function (ev) {
      var btn =
        ev.target && ev.target.closest ? ev.target.closest("[data-secplus-portal-24h-checkout]") : null;
      if (!btn) return;
      if (ev.preventDefault) ev.preventDefault();
      if (ev.stopPropagation) ev.stopPropagation();
      if (ev.stopImmediatePropagation) ev.stopImmediatePropagation();
      if (hasPaidPortalAccess() || is24hEntitlementActive()) {
        window.location.href = PORTAL_URL;
      }
    },
    true
  );

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-secplus-portal-3d-checkout]").forEach(function (btn) {
      wireCheckout(btn, "3d");
    });
    document.querySelectorAll("[data-secplus-portal-30d-checkout]").forEach(function (btn) {
      if (btn.hasAttribute("data-secplus-portal-24h-checkout")) return;
      wireCheckout(btn, "30d");
    });
    hide24hCtas();
    maybeAutoCheckoutFromUrl();
    window.addEventListener("pageshow", resetAllCheckoutButtons);
  });

  window.bccStartSecplusPortalCheckout = startSecplusPortalCheckout;
  window.bccSecplusLaunchPromoCode = LAUNCH_PROMO_CODE;
  window.bccSecplusTrialPromoCode = TRIAL_PROMO_CODE;
  window.bccSecplus24hTrialActive = is24hEntitlementActive;
  window.bccMountSecplus24hUpgradeBanner = mount24hUpgradeBanner;
})();

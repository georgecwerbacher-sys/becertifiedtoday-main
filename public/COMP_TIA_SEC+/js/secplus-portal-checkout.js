/**
 * Stripe Payment Links for CompTIA Security+ portal access.
 *
 * Stripe Dashboard → Payment Link → After payment → custom redirect URL:
 *   https://becertifiedtoday.com/COMP_TIA_SEC+/secplus-portal-checkout-success.html?session_id={CHECKOUT_SESSION_ID}
 *
 * Optional metadata on the link: productId = secplus-portal-10d or secplus-portal-30d
 */
(function () {
  var LINKS = {
    "10d": "https://buy.stripe.com/8x28wObwVfp54CIgs4c3m06",
    "30d": "https://buy.stripe.com/5kQ14mbwVgt93yEfo0c3m07",
  };

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
      value: "19.99",
      defaultLabel: "Get 30-day access",
      labelKey: "secplusPortal30dCheckoutLabel",
    },
  };

  function startSecplusPortalCheckout(tier, triggerEl) {
    var product = PRODUCTS[tier];
    var url = LINKS[tier];
    if (!product || !url) return false;

    var trackEl = triggerEl || document.createElement("button");
    if (typeof window.bccTrackBeginCheckout === "function") {
      trackEl.setAttribute("data-bcc-item-id", product.id);
      trackEl.setAttribute("data-bcc-item-name", product.name);
      trackEl.setAttribute("data-bcc-value", product.value);
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
})();

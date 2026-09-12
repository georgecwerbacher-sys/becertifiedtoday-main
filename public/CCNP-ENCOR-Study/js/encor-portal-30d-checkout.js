/**
 * Stripe Payment Link for CCNP ENCOR 30-day full library access.
 *
 * Stripe Dashboard → each Payment Link → After payment → custom redirect URL:
 *   https://becertifiedtoday.com/CCNP-ENCOR-Study/ENCOR_Training_Portal.html?session_id={CHECKOUT_SESSION_ID}
 *
 * Optional metadata on the link: productId = encor-portal-30d
 */
(function () {
  var LINKS = {
    "30d": "https://buy.stripe.com/cNidR80Sh0ubc5aejWc3m00",
  };

  var PRODUCTS = {
    "30d": {
      id: "encor_portal_30d",
      name: "CCNP ENCOR 30-day access",
      value: "19.99",
      defaultLabel: "Get 30-day access",
      labelKey: "encorPortal30dCheckoutLabel",
    },
  };

  function buildCheckoutUrl(tier) {
    var url = LINKS[tier];
    if (!url) return url;
    if (typeof window.bccBuildCheckoutUrlWithSave50 === "function") {
      return window.bccBuildCheckoutUrlWithSave50(url);
    }
    return url;
  }

  function startEncorPortalCheckout(tier, triggerEl) {
    var product = PRODUCTS[tier];
    var url = buildCheckoutUrl(tier);
    if (!product || !url) return false;

    var trackEl = triggerEl || document.createElement("button");
    if (typeof window.bccTrackBeginCheckout === "function") {
      trackEl.setAttribute("data-bcc-item-id", product.id);
      trackEl.setAttribute("data-bcc-item-name", product.name);
      trackEl.setAttribute(
        "data-bcc-value",
        typeof window.bccSave50DiscountedValue === "function"
          ? window.bccSave50DiscountedValue(product.value)
          : product.value
      );
      trackEl.setAttribute("data-bcc-currency", "USD");
      window.bccTrackBeginCheckout(trackEl);
    }
    if (typeof window.bccSetEncorPendingPortalTier === "function") {
      window.bccSetEncorPendingPortalTier(tier);
    }
    window.location.href = url;
    return true;
  }

  function wireCheckout(btn, tier) {
    var product = PRODUCTS[tier];
    if (!product || !btn) return;

    if (!btn.dataset[product.labelKey]) {
      btn.dataset[product.labelKey] = btn.textContent.trim() || product.defaultLabel;
    }

    btn.addEventListener("click", function () {
      if (btn.dataset.loading === "1") return;
      btn.dataset.loading = "1";
      btn.textContent = "Redirecting…";
      btn.disabled = true;
      startEncorPortalCheckout(tier, btn);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-encor-portal-30d-checkout]").forEach(function (btn) {
      wireCheckout(btn, "30d");
    });
  });

  window.bccStartEncorPortalCheckout = startEncorPortalCheckout;
})();

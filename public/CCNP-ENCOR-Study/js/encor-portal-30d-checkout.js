/**
 * Stripe Payment Links for CCNP ENCOR 10-day and 30-day full library access.
 * Configure each payment link success URL to:
 *   /CCNP-ENCOR-Study/ENCOR_Training_Portal.html?session_id={CHECKOUT_SESSION_ID}
 */
(function () {
  var LINKS = {
    "10d": "https://buy.stripe.com/cNidR81Wlel13yEdfSc3m05",
    "30d": "https://buy.stripe.com/cNidR80Sh0ubc5aejWc3m00",
  };

  var PRODUCTS = {
    "10d": {
      id: "encor_portal_10d",
      name: "CCNP ENCOR 10-day access",
      value: "9.99",
      defaultLabel: "Get 10-day access",
      labelKey: "encorPortal10dCheckoutLabel",
    },
    "30d": {
      id: "encor_portal_30d",
      name: "CCNP ENCOR 30-day access",
      value: "19.99",
      defaultLabel: "Get 30-day access",
      labelKey: "encorPortal30dCheckoutLabel",
    },
  };

  function wireCheckout(btn, tier) {
    var product = PRODUCTS[tier];
    var url = LINKS[tier];
    if (!product || !url) return;

    if (!btn.dataset[product.labelKey]) {
      btn.dataset[product.labelKey] = btn.textContent.trim() || product.defaultLabel;
    }

    btn.addEventListener("click", function () {
      if (btn.dataset.loading === "1") return;
      if (typeof window.bccTrackBeginCheckout === "function") {
        btn.setAttribute("data-bcc-item-id", product.id);
        btn.setAttribute("data-bcc-item-name", product.name);
        btn.setAttribute("data-bcc-value", product.value);
        btn.setAttribute("data-bcc-currency", "USD");
        window.bccTrackBeginCheckout(btn);
      }
      btn.dataset.loading = "1";
      btn.textContent = "Redirecting…";
      btn.disabled = true;
      window.location.href = url;
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-encor-portal-10d-checkout]").forEach(function (btn) {
      wireCheckout(btn, "10d");
    });
    document.querySelectorAll("[data-encor-portal-30d-checkout]").forEach(function (btn) {
      wireCheckout(btn, "30d");
    });
  });
})();

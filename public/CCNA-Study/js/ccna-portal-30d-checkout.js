/**
 * Stripe Payment Link for CCNA 30-day full library access.
 *
 * Stripe Dashboard → each Payment Link → After payment → custom redirect URL:
 *   /CCNA-Study/CCNA_Training_Portal.html?session_id={CHECKOUT_SESSION_ID}
 *
 * Optional metadata on the link: productId = ccna-portal-30d
 */
(function () {
  var LINKS = {
    "30d": "https://buy.stripe.com/14A7sK58xccT4CI8ZCc3m03",
  };

  var PRODUCTS = {
    "30d": {
      id: "ccna_portal_30d",
      name: "CCNA 30-day access",
      value: "19.99",
      defaultLabel: "Get 30-day access",
      labelKey: "ccnaPortal30dCheckoutLabel",
    },
  };

  function wireCheckout(btn, tier) {
    var product = PRODUCTS[tier];
    var url = LINKS[tier];
    if (!product || !url) return;
    if (typeof window.bccBuildCheckoutUrlWithSave50 === "function") {
      url = window.bccBuildCheckoutUrlWithSave50(url);
    }

    if (!btn.dataset[product.labelKey]) {
      btn.dataset[product.labelKey] = btn.textContent.trim() || product.defaultLabel;
    }

    btn.addEventListener("click", function (ev) {
      if (ev && typeof ev.preventDefault === "function") ev.preventDefault();
      if (btn.dataset.loading === "1") return;
      if (typeof window.bccTrackBeginCheckout === "function") {
        btn.setAttribute("data-bcc-item-id", product.id);
        btn.setAttribute("data-bcc-item-name", product.name);
        btn.setAttribute(
          "data-bcc-value",
          typeof window.bccSave50DiscountedValue === "function"
            ? window.bccSave50DiscountedValue(product.value)
            : product.value
        );
        btn.setAttribute("data-bcc-currency", "USD");
        window.bccTrackBeginCheckout(btn);
      }
      btn.dataset.loading = "1";
      if (btn.tagName === "BUTTON") {
        btn.disabled = true;
        btn.textContent = "Redirecting…";
      } else {
        btn.setAttribute("aria-busy", "true");
        btn.textContent = "Redirecting…";
      }
      window.location.href = url;
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-ccna-portal-30d-checkout]").forEach(function (btn) {
      wireCheckout(btn, "30d");
    });
  });
})();

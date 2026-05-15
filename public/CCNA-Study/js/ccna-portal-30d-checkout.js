/**
 * Opens the Stripe Payment Link for CCNA 30-day training portal access.
 * Configure the Payment Link “After payment” redirect to:
 *   /CCNA-Study/CCNA_Training_Portal.html?session_id={CHECKOUT_SESSION_ID}
 * The portal page verifies the session, saves 30-day access in this browser, then strips session_id from the URL.
 */
(function () {
  var CCNA_PORTAL_30D_STRIPE_PAYMENT_LINK =
    "https://buy.stripe.com/14A7sK58xccT4CI8ZCc3m03";

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-ccna-portal-30d-checkout]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        if (btn.dataset.loading === "1") return;
        btn.dataset.loading = "1";
        btn.textContent = "Redirecting…";
        btn.disabled = true;
        window.location.href = CCNA_PORTAL_30D_STRIPE_PAYMENT_LINK;
      });
    });
  });
})();

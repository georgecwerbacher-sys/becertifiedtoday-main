/**
 * Opens the Stripe Payment Link for CCNA 30-day training portal access.
 * Configure the payment link’s “After payment” URL in Stripe to return customers to
 * /CCNA-Study/ccna-portal-30d-checkout-success.html?session_id={CHECKOUT_SESSION_ID} if you need session_id verification.
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

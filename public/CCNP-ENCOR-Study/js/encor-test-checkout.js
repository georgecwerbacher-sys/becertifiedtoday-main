/**
 * Stripe Payment Link for the ENCOR Timed Test Simulation (one-time purchase).
 * Set the payment link success URL to
 * /CCNP-ENCOR-Study/test-simulation.html?session_id={CHECKOUT_SESSION_ID}
 */
(function () {
  var ENCOR_TEST_SIM_STRIPE_PAYMENT_LINK =
    "https://buy.stripe.com/3cIaEWbwVb8P8SYejWc3m01";

  document.addEventListener("DOMContentLoaded", function () {
    var btn = document.getElementById("encorTestSimPurchaseBtn");
    if (!btn) return;
    btn.addEventListener("click", function () {
      if (btn.dataset.loading === "1") return;
      if (typeof window.bccTrackBeginCheckout === "function") {
        btn.setAttribute("data-bcc-item-id", "encor_timed_simulation");
        btn.setAttribute("data-bcc-item-name", "ENCOR Timed Test Simulation");
        btn.setAttribute("data-bcc-value", "4.99");
        btn.setAttribute("data-bcc-currency", "USD");
        window.bccTrackBeginCheckout(btn);
      }
      btn.dataset.loading = "1";
      btn.textContent = "Redirecting…";
      btn.disabled = true;
      window.location.href = ENCOR_TEST_SIM_STRIPE_PAYMENT_LINK;
    });
  });
})();

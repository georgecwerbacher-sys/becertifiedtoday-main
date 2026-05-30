/**
 * Stripe Payment Link for the Security+ timed exam simulation (one-time purchase).
 * Set the payment link success URL to:
 *   https://becertifiedtoday.com/COMP_TIA_SEC+/test-simulation-runner.html?session_id={CHECKOUT_SESSION_ID}
 * Optional metadata: productId = secplus-test-simulation
 */
(function () {
  var SECPLUS_TEST_SIM_STRIPE_PAYMENT_LINK =
    "https://buy.stripe.com/9B63cudF33Gnc5a1xac3m08";

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-secplus-test-sim-checkout]").forEach(function (btn) {
      if (!btn.dataset.secplusTestSimCheckoutLabel) {
        btn.dataset.secplusTestSimCheckoutLabel = btn.textContent.trim() || "Get simulated exam";
      }
      btn.addEventListener("click", function () {
        if (btn.dataset.loading === "1") return;
        if (typeof window.bccTrackBeginCheckout === "function") {
          btn.setAttribute("data-bcc-item-id", "secplus_timed_simulation");
          btn.setAttribute("data-bcc-item-name", "Security+ Timed Test Simulation");
          btn.setAttribute("data-bcc-value", "9.99");
          btn.setAttribute("data-bcc-currency", "USD");
          window.bccTrackBeginCheckout(btn);
        }
        btn.dataset.loading = "1";
        btn.textContent = "Redirecting…";
        btn.disabled = true;
        window.location.href = SECPLUS_TEST_SIM_STRIPE_PAYMENT_LINK;
      });
    });
  });
})();

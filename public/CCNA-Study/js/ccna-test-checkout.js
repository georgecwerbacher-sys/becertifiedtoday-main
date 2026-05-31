/**
 * Opens the Stripe Payment Link for the CCNA Timed Test Simulation (one-time purchase).
 * Configure the payment link’s “After payment” URL in Stripe to return customers to
 * /CCNA_Sim_EXAM/begin-test-simulation.html?session_id={CHECKOUT_SESSION_ID} if you need session_id verification.
 */
(function () {
  var CCNA_TEST_SIM_STRIPE_PAYMENT_LINK =
    "https://buy.stripe.com/7sY00iasR1yfedi1xac3m02";

  document.addEventListener("DOMContentLoaded", function () {
    var btn = document.getElementById("ccnaTestSimPurchaseBtn");
    if (!btn) return;
    btn.addEventListener("click", function () {
      if (btn.dataset.loading === "1") return;
      if (typeof window.bccTrackBeginCheckout === "function") {
        btn.setAttribute("data-bcc-item-id", "ccna_timed_simulation");
        btn.setAttribute("data-bcc-item-name", "CCNA Timed Test Simulation");
        btn.setAttribute("data-bcc-value", "9.99");
        btn.setAttribute("data-bcc-currency", "USD");
        window.bccTrackBeginCheckout(btn);
      }
      btn.dataset.loading = "1";
      btn.textContent = "Redirecting…";
      btn.disabled = true;
      window.location.href = CCNA_TEST_SIM_STRIPE_PAYMENT_LINK;
    });
  });
})();

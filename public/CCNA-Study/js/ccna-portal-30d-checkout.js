/**
 * Opens the Stripe Payment Link for CCNA 30-day training portal access.
 * URL comes from GET /api/ccna-portal-30d-payment-link (Vercel env STRIPE_PAYMENT_LINK_CCNA_PORTAL_30D).
 * Configure the Payment Link “After payment” redirect to:
 *   /CCNA-Study/CCNA_Training_Portal.html?session_id={CHECKOUT_SESSION_ID}
 * The portal page verifies the session, saves 30-day access in this browser (and the checkout session id for restore), then strips session_id from the URL.
 * If access disappears after clearing site data, use restore-access or email-link pages under /CCNA-Study/.
 * Magic-link email at checkout requires Stripe webhook + Resend + PORTAL_MAGIC_LINK_SECRET (same pattern as other training portals; see .env.example).
 */
(function () {
  function fetchPaymentLink() {
    return fetch("/api/ccna-portal-30d-payment-link")
      .then(function (r) {
        return r.json().then(function (body) {
          if (!r.ok) {
            throw new Error((body && body.error) || "Could not load checkout link");
          }
          if (!body || typeof body.url !== "string" || !body.url.length) {
            throw new Error("Invalid checkout link");
          }
          return body.url;
        });
      });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-ccna-portal-30d-checkout]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        if (btn.dataset.loading === "1") return;
        btn.dataset.loading = "1";
        btn.textContent = "Redirecting…";
        btn.disabled = true;
        fetchPaymentLink()
          .then(function (url) {
            window.location.href = url;
          })
          .catch(function () {
            btn.dataset.loading = "0";
            btn.disabled = false;
            btn.textContent = btn.dataset.ccnaPortal30dCheckoutLabel || "Buy";
            alert("Checkout is temporarily unavailable. Please try again in a moment.");
          });
      });
      if (!btn.dataset.ccnaPortal30dCheckoutLabel) {
        btn.dataset.ccnaPortal30dCheckoutLabel = btn.textContent.trim() || "Buy";
      }
    });
  });
})();

/**
 * Starts Stripe Checkout for the CCNA Timed Test Simulation (requires API + env on Vercel).
 */
(function () {
  async function startCheckout(button) {
    if (button.dataset.loading === "1") return;
    button.dataset.loading = "1";
    var label = button.textContent;
    button.textContent = "Redirecting…";
    button.disabled = true;

    try {
      var res = await fetch("/api/create-checkout-session", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ productId: "ccna-test-simulation" }),
      });
      var data = await res.json().catch(function () {
        return {};
      });

      if (!res.ok) {
        var msg =
          data.error ||
          data.hint ||
          ("HTTP " + res.status + ": configure Stripe env vars on Vercel.");
        if (data.hint && msg !== data.hint) {
          msg += "\n\n" + data.hint;
        }
        if (data.detail) {
          msg += "\n\n" + data.detail;
          if (data.code) msg += " (" + data.code + ")";
        }
        window.alert(msg);
        button.textContent = label;
        button.disabled = false;
        button.dataset.loading = "0";
        return;
      }

      if (data.url) {
        window.location.href = data.url;
        return;
      }

      window.alert("Checkout did not return a redirect URL.");
    } catch (e) {
      window.alert(
        "Could not start checkout. Deploy API routes (api/create-checkout-session.js) and set Stripe keys."
      );
    }

    button.textContent = label;
    button.disabled = false;
    button.dataset.loading = "0";
  }

  document.addEventListener("DOMContentLoaded", function () {
    var btn = document.getElementById("ccnaTestSimPurchaseBtn");
    if (!btn) return;
    btn.addEventListener("click", function () {
      startCheckout(btn);
    });
  });
})();

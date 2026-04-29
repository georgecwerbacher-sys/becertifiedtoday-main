(function () {
  async function createCheckout(payload) {
    var response = await fetch("/api/stripe/create-checkout-session", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload || { product: "encor" }),
    });
    if (!response.ok) {
      throw new Error("Could not start checkout");
    }
    return response.json();
  }

  async function onCheckoutClick(event) {
    event.preventDefault();
    var el = event.currentTarget;
    if (!el) return;
    var restoreText = el.textContent;
    el.disabled = true;
    el.textContent = "Redirecting...";
    try {
      var renew = el.getAttribute("data-renew") === "true";
      var result = await createCheckout({ product: "encor", renew: renew });
      if (!result || !result.url) throw new Error("No checkout URL returned");
      window.location.href = result.url;
    } catch (error) {
      console.error(error);
      el.textContent = "Try again";
      window.setTimeout(function () {
        el.textContent = restoreText;
        el.disabled = false;
      }, 1200);
      return;
    }
  }

  var buttons = document.querySelectorAll("[data-encor-checkout]");
  buttons.forEach(function (btn) {
    btn.addEventListener("click", onCheckoutClick);
  });
})();

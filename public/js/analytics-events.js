(function () {
  function send(event, path) {
    try {
      var payload = JSON.stringify({
        event: event,
        path: path || location.pathname || "/",
      });
      if (navigator.sendBeacon) {
        var blob = new Blob([payload], { type: "application/json" });
        navigator.sendBeacon("/api/analytics/track", blob);
        return;
      }
      fetch("/api/analytics/track", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: payload,
        keepalive: true,
      });
    } catch (_error) {}
  }

  send("page_view");

  document.addEventListener("click", function (event) {
    var target = event.target;
    if (!target) return;
    var button = target.closest("[data-encor-checkout]");
    if (button) {
      var renew = button.getAttribute("data-renew") === "true";
      send(renew ? "renew_clicked" : "purchase_clicked");
      return;
    }
  });
})();

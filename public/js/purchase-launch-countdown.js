(function () {
  /**
   * Checkout opens at **12:00 midnight US Eastern Time** — timezone **America/New_York**
   * (ET = EST or EDT depending on date). May 1, 2026 is **EDT** (UTC−4), so midnight ET =
   * 2026-05-01T04:00:00.000Z. Change both the ISO instant here and the copy on the page if you move the date.
   */
  var LAUNCH_MS = Date.parse("2026-05-01T04:00:00.000Z");

  var cd = document.getElementById("purchase-launch-countdown");
  var mount = document.getElementById("purchase-stripe-mount");
  var elDays = document.getElementById("plc-days");
  var elHours = document.getElementById("plc-hours");
  var elMinutes = document.getElementById("plc-minutes");
  var elSeconds = document.getElementById("plc-seconds");

  function pad(n) {
    return String(n).padStart(2, "0");
  }

  function applyLiveState() {
    var live = Date.now() >= LAUNCH_MS;
    var root = document.documentElement;
    if (live) {
      root.classList.add("purchase-checkout-live");
      if (mount) {
        mount.removeAttribute("inert");
        mount.classList.remove("purchase-stripe-mount--locked");
      }
      if (cd) cd.hidden = true;
      return true;
    }
    root.classList.remove("purchase-checkout-live");
    if (mount) {
      mount.setAttribute("inert", "");
      mount.classList.add("purchase-stripe-mount--locked");
    }
    if (cd) cd.hidden = false;
    return false;
  }

  function tick() {
    if (applyLiveState()) {
      return;
    }
    var left = LAUNCH_MS - Date.now();
    if (left <= 0) {
      applyLiveState();
      return;
    }
    var s = Math.floor(left / 1000);
    var days = Math.floor(s / 86400);
    var h = Math.floor((s % 86400) / 3600);
    var m = Math.floor((s % 3600) / 60);
    var sec = s % 60;
    if (elDays) elDays.textContent = String(days);
    if (elHours) elHours.textContent = pad(h);
    if (elMinutes) elMinutes.textContent = pad(m);
    if (elSeconds) elSeconds.textContent = pad(sec);
  }

  applyLiveState();
  tick();
  setInterval(tick, 1000);
})();

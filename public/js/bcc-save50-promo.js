/**
 * SAVE50 promo: 50% off everything with SAVE50PERCENT until midnight Jul 21, 2026 ET.
 */
(function () {
  "use strict";

  var PROMO_CODE = "SAVE50PERCENT";
  var PROMO_END_MS = new Date("2026-07-21T00:00:00-04:00").getTime();
  var BAR_ID = "bccSave50PromoBar";
  var COUNTDOWN_ID = "bccSave50Countdown";
  var timerId = null;

  function landingPathKey() {
    var p = (location.pathname || "").toLowerCase().replace(/\/$/, "") || "/";
    if (p.endsWith(".html")) p = p.slice(0, -5);
    return p;
  }

  function isLandingPage() {
    var p = landingPathKey();
    return (
      p === "/" ||
      p === "/index" ||
      p === "/ccna-home" ||
      p === "/ccnp-home" ||
      p === "/comptia-sec+-home" ||
      p === "/ccnaauto-home"
    );
  }

  function purchaseHref() {
    var p = landingPathKey();
    if (p === "/" || p === "/index") return "#main";
    if (document.getElementById("purchase")) return "#purchase";
    return "#purchase";
  }

  function purchaseCtaLabel() {
    var p = landingPathKey();
    if (p === "/" || p === "/index") return "Choose track · 50% off →";
    return "Get 50% off →";
  }

  function promoEndMs() {
    return PROMO_END_MS;
  }

  function isActive() {
    return Date.now() < promoEndMs();
  }

  function formatCountdown(msLeft) {
    if (msLeft <= 0) return "Ended";
    var totalSec = Math.floor(msLeft / 1000);
    var days = Math.floor(totalSec / 86400);
    var hours = Math.floor((totalSec % 86400) / 3600);
    var mins = Math.floor((totalSec % 3600) / 60);
    var secs = totalSec % 60;
    function pad(n) {
      return n < 10 ? "0" + n : String(n);
    }
    if (days > 0) {
      return days + "d " + pad(hours) + "h " + pad(mins) + "m " + pad(secs) + "s";
    }
    return pad(hours) + ":" + pad(mins) + ":" + pad(secs);
  }

  function updateCountdown() {
    var el = document.getElementById(COUNTDOWN_ID);
    if (!el) return;
    var left = promoEndMs() - Date.now();
    el.textContent = formatCountdown(left);
    if (left <= 0) teardownBanner();
  }

  function syncBarHeight() {
    var bar = document.getElementById(BAR_ID);
    if (!bar) return;
    document.documentElement.style.setProperty("--bcc-save50-promo-h", bar.offsetHeight + "px");
  }

  function copyCode(btn) {
    var done = function () {
      var prev = btn.textContent;
      btn.textContent = "Copied!";
      setTimeout(function () {
        btn.textContent = prev;
      }, 1600);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(PROMO_CODE).then(done).catch(function () {});
      return;
    }
    try {
      var ta = document.createElement("textarea");
      ta.value = PROMO_CODE;
      ta.setAttribute("readonly", "");
      ta.style.position = "absolute";
      ta.style.left = "-9999px";
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
      done();
    } catch (e) {}
  }

  function teardownBanner() {
    if (timerId != null) {
      clearInterval(timerId);
      timerId = null;
    }
    var bar = document.getElementById(BAR_ID);
    if (bar) bar.remove();
    document.documentElement.classList.remove("bcc-save50-promo-active");
    document.documentElement.style.removeProperty("--bcc-save50-promo-h");
  }

  function mountBanner() {
    if (!isLandingPage() || !isActive() || document.getElementById(BAR_ID)) return;

    document.documentElement.classList.add("bcc-save50-promo-active");

    var bar = document.createElement("div");
    bar.id = BAR_ID;
    bar.className = "bcc-save50-promo-bar";
    bar.setAttribute("role", "region");
    bar.setAttribute("aria-label", "50% off limited-time offer");
    bar.innerHTML =
      '<div class="bcc-save50-promo-bar__inner">' +
      '<div class="bcc-save50-promo-bar__main">' +
      '<p class="bcc-save50-promo-bar__headline">50% off everything</p>' +
      '<p class="bcc-save50-promo-bar__sub">Limited time · Use code <code>' +
      PROMO_CODE +
      '</code> at checkout <button type="button" class="bcc-save50-promo-bar__copy" data-bcc-save50-copy>Copy code</button></p>' +
      "</div>" +
      '<div class="bcc-save50-promo-bar__actions">' +
      '<span class="bcc-save50-promo-bar__timer">Offer ends in<br /><strong id="' +
      COUNTDOWN_ID +
      '">--:--:--</strong></span>' +
      '<div class="bcc-save50-promo-bar__cta-row">' +
      '<a class="bcc-save50-promo-bar__cta" href="' +
      purchaseHref() +
      '">' +
      purchaseCtaLabel() +
      "</a>" +
      "</div></div></div>";

    document.body.insertBefore(bar, document.body.firstChild);

    var copyBtn = bar.querySelector("[data-bcc-save50-copy]");
    if (copyBtn) {
      copyBtn.addEventListener("click", function () {
        copyCode(copyBtn);
      });
    }

    var purchaseLink = bar.querySelector(".bcc-save50-promo-bar__cta");
    if (purchaseLink && landingPathKey() !== "/" && landingPathKey() !== "/index" && !document.getElementById("purchase")) {
      purchaseLink.style.display = "none";
    }

    updateCountdown();
    syncBarHeight();
    if (timerId == null) timerId = setInterval(updateCountdown, 1000);
    window.addEventListener("resize", syncBarHeight);
  }

  function appendPromoToCheckoutUrl(url) {
    if (!url || !isActive()) return url;
    var sep = url.indexOf("?") >= 0 ? "&" : "?";
    return url + sep + "prefilled_promo_code=" + encodeURIComponent(PROMO_CODE);
  }

  function discountedValue(raw) {
    var n = parseFloat(raw);
    if (!isActive() || Number.isNaN(n)) return raw;
    return (Math.round(n * 50) / 100).toFixed(2);
  }

  window.bccSave50PromoActive = isActive;
  window.bccSave50PromoCode = function () {
    return PROMO_CODE;
  };
  window.bccSave50PromoEndMs = promoEndMs;
  window.bccBuildCheckoutUrlWithSave50 = appendPromoToCheckoutUrl;
  window.bccSave50DiscountedValue = discountedValue;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mountBanner);
  } else {
    mountBanner();
  }
  window.addEventListener("load", mountBanner);
})();

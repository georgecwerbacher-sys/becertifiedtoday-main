/**
 * September 50% off: SEP50PERCENTOFF through the end of Sept 2026 ET.
 *
 * Same one-time 30-day Payment Link for:
 *   - new first-time access (not a subscription)
 *   - members renewing current or expired access
 *
 * Prefills Stripe Payment Links via prefilled_promo_code. Create the same
 * promotion code in Stripe Dashboard (50% off) or checkout will reject it.
 */
(function () {
  "use strict";

  var PROMO_CODE = "SEP50PERCENTOFF";
  var PROMO_START_MS = new Date("2026-09-01T00:00:00-04:00").getTime();
  var PROMO_END_MS = new Date("2026-10-01T00:00:00-04:00").getTime();
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

  function currentTrack() {
    var p = (location.pathname || "").toLowerCase();
    if (
      p.indexOf("comptia-sec") >= 0 ||
      p.indexOf("/comp_tia_sec") >= 0 ||
      p.indexOf("/secplus") >= 0
    ) {
      return "secplus";
    }
    if (p.indexOf("/ccnp") >= 0 || p.indexOf("encor") >= 0) return "encor";
    if (p.indexOf("ccnaauto") >= 0) return "ccnaauto";
    if (p.indexOf("ccna") >= 0) return "ccna";
    var land = landingPathKey();
    if (land === "/comptia-sec+-home") return "secplus";
    if (land === "/ccnp-home") return "encor";
    if (land === "/ccnaauto-home") return "ccnaauto";
    if (land === "/ccna-home") return "ccna";
    return null;
  }

  function readJson(key) {
    try {
      var raw = localStorage.getItem(key);
      if (!raw) return null;
      return JSON.parse(raw);
    } catch (e) {
      return null;
    }
  }

  function hasCheckoutSession(key) {
    try {
      var s = localStorage.getItem(key);
      return typeof s === "string" && s.indexOf("cs_") === 0;
    } catch (e) {
      return false;
    }
  }

  function looksLikeMembership(obj) {
    return !!(obj && (typeof obj.expiresAt === "number" || obj.productId));
  }

  function trackHasMembership(track) {
    if (track === "secplus") {
      if (
        typeof window.bccSecplusPortalAccessActive === "function" &&
        window.bccSecplusPortalAccessActive()
      ) {
        return true;
      }
      if (
        typeof window.bccSecplusPortalNeedsRestoreLink === "function" &&
        window.bccSecplusPortalNeedsRestoreLink()
      ) {
        return true;
      }
      return (
        looksLikeMembership(readJson("bcc_secplus_portal_v1")) ||
        hasCheckoutSession("bcc_secplus_portal_cs_v1")
      );
    }
    if (track === "ccna") {
      if (typeof window.bccPortalAccessActive === "function" && window.bccPortalAccessActive()) {
        return true;
      }
      return (
        looksLikeMembership(readJson("bcc_ccna_portal_30d_v1")) ||
        hasCheckoutSession("bcc_ccna_portal_30d_cs_v1")
      );
    }
    if (track === "encor") {
      if (
        typeof window.bccEncorPortalAccessActive === "function" &&
        window.bccEncorPortalAccessActive()
      ) {
        return true;
      }
      return (
        looksLikeMembership(readJson("bcc_encor_portal_v1")) ||
        hasCheckoutSession("bcc_encor_portal_cs_v1")
      );
    }
    if (track === "ccnaauto") {
      return (
        looksLikeMembership(readJson("bcc_ccnaauto_portal_v1")) ||
        hasCheckoutSession("bcc_ccnaauto_portal_cs_v1")
      );
    }
    return false;
  }

  function isRenewingMember() {
    var track = currentTrack();
    if (track) return trackHasMembership(track);
    return (
      trackHasMembership("secplus") ||
      trackHasMembership("ccna") ||
      trackHasMembership("encor") ||
      trackHasMembership("ccnaauto")
    );
  }

  function purchaseHref() {
    var p = landingPathKey();
    if (p === "/" || p === "/index") return "#main";
    if (document.getElementById("purchase")) return "#purchase";
    return "#purchase";
  }

  function purchaseCtaLabel(renewing) {
    var p = landingPathKey();
    if (p === "/" || p === "/index") return "Choose track · 50% off →";
    return renewing ? "Renew 30 days · 50% off →" : "New 30-day access · 50% off →";
  }

  function promoEndMs() {
    return PROMO_END_MS;
  }

  function inCalendarWindow() {
    var now = Date.now();
    return now >= PROMO_START_MS && now < promoEndMs();
  }

  function isActive() {
    return inCalendarWindow();
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

    var renewing = isRenewingMember();
    document.documentElement.classList.add("bcc-save50-promo-active");

    var bar = document.createElement("div");
    bar.id = BAR_ID;
    bar.className = "bcc-save50-promo-bar";
    bar.setAttribute("role", "region");
    bar.setAttribute(
      "aria-label",
      renewing
        ? "Renew 30-day access at 50 percent off"
        : "New one-time 30-day access at 50 percent off"
    );
    bar.innerHTML =
      '<div class="bcc-save50-promo-bar__inner">' +
      '<div class="bcc-save50-promo-bar__main">' +
      '<p class="bcc-save50-promo-bar__headline">' +
      (renewing ? "Renew at 50% off" : "50% off 30-day access") +
      "</p>" +
      '<p class="bcc-save50-promo-bar__sub">' +
      (renewing
        ? "One-time renewal · Use code "
        : "New one-time access · Use code ") +
      "<code>" +
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
      purchaseCtaLabel(renewing) +
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
    if (
      purchaseLink &&
      landingPathKey() !== "/" &&
      landingPathKey() !== "/index" &&
      !document.getElementById("purchase")
    ) {
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
  window.bccSave50IsRenewingMember = isRenewingMember;
  window.bccBuildCheckoutUrlWithSave50 = appendPromoToCheckoutUrl;
  window.bccSave50DiscountedValue = discountedValue;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mountBanner);
  } else {
    mountBanner();
  }
  window.addEventListener("load", mountBanner);
})();

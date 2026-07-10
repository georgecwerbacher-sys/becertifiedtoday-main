/**
 * SAVE50 promo: free full portal access until midnight Jul 14, 2026 ET;
 * 50% off next 30-day purchase with SAVE50PERCENT while the timer runs.
 */
(function () {
  "use strict";

  var PROMO_CODE = "SAVE50PERCENT";
  var PROMO_END_MS = new Date("2026-07-14T00:00:00-04:00").getTime();
  var BAR_ID = "bccSave50PromoBar";
  var COUNTDOWN_ID = "bccSave50Countdown";
  var timerId = null;

  var TRACKS = {
    ccna: {
      storage: "/CCNA-Study/js/ccna-portal-30d-storage.js",
      portal: "/CCNA-Study/CCNA_Training_Portal.html",
      storageKey: "bcc_ccna_portal_30d_v1",
      isActive: function () {
        return typeof window.bccPortalAccessActive === "function" && window.bccPortalAccessActive();
      },
      grant: function (expMs) {
        return (
          typeof window.bccSetPortal30DayEntitlement === "function" &&
          window.bccSetPortal30DayEntitlement(expMs, null)
        );
      },
    },
    encor: {
      storage: "/CCNP-ENCOR-Study/js/encor-portal-storage.js",
      portal: "/CCNP-ENCOR-Study/ENCOR_Training_Portal.html",
      storageKey: "bcc_encor_portal_v1",
      isActive: function () {
        return typeof window.bccEncorPortalAccessActive === "function" && window.bccEncorPortalAccessActive();
      },
      grant: function (expMs) {
        return (
          typeof window.bccSetEncorPortalEntitlement === "function" &&
          window.bccSetEncorPortalEntitlement(expMs, null, "encor-portal-30d")
        );
      },
    },
    secplus: {
      storage: "/COMP_TIA_SEC+/js/secplus-portal-storage.js",
      portal: "/COMP_TIA_SEC+/SEC+_Training_Portal.html",
      storageKey: "bcc_secplus_portal_v1",
      isActive: function () {
        return typeof window.bccSecplusPortalAccessActive === "function" && window.bccSecplusPortalAccessActive();
      },
      grant: function (expMs) {
        return (
          typeof window.bccSetSecplusPortalEntitlement === "function" &&
          window.bccSetSecplusPortalEntitlement(expMs, null, "secplus-portal-30d")
        );
      },
    },
    ccnaauto: {
      storage: "/CCNAAUTO-Study/js/ccnaauto-portal-storage.js",
      portal: "/CCNAAUTO-Study/CCNAAUTO_Training_Portal.html",
      storageKey: "bcc_ccnaauto_portal_v1",
      isActive: function () {
        return typeof window.bccCcnaautoPortalAccessActive === "function" && window.bccCcnaautoPortalAccessActive();
      },
      grant: function (expMs) {
        return (
          typeof window.bccSetCcnaautoPortalEntitlement === "function" &&
          window.bccSetCcnaautoPortalEntitlement(expMs, null, "ccnaauto-portal-30d")
        );
      },
    },
  };

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

  function tracksForPage() {
    var p = landingPathKey();
    if (p === "/ccna-home") return ["ccna"];
    if (p === "/ccnp-home") return ["encor"];
    if (p === "/comptia-sec+-home") return ["secplus"];
    if (p === "/ccnaauto-home") return ["ccnaauto"];
    if (p === "/" || p === "/index") return ["ccna", "encor", "secplus"];
    return [];
  }

  function primaryPortalUrl() {
    var tracks = tracksForPage();
    if (tracks.length === 1 && TRACKS[tracks[0]]) return TRACKS[tracks[0]].portal;
    return "";
  }

  function promoEndMs() {
    return PROMO_END_MS;
  }

  function isActive() {
    return Date.now() < promoEndMs();
  }

  function readStoredExpiry(storageKey) {
    try {
      var raw = localStorage.getItem(storageKey);
      if (!raw) return 0;
      var o = JSON.parse(raw);
      return typeof o.expiresAt === "number" ? o.expiresAt : 0;
    } catch (e) {
      return 0;
    }
  }

  function loadScriptOnce(src) {
    return new Promise(function (resolve) {
      if (document.querySelector('script[src="' + src + '"]')) {
        resolve();
        return;
      }
      var s = document.createElement("script");
      s.src = src;
      s.defer = true;
      s.onload = function () {
        resolve();
      };
      s.onerror = function () {
        resolve();
      };
      (document.body || document.head).appendChild(s);
    });
  }

  function ensureTrackStorage(trackIds) {
    var loads = trackIds.map(function (id) {
      var cfg = TRACKS[id];
      return cfg ? loadScriptOnce(cfg.storage) : Promise.resolve();
    });
    return Promise.all(loads);
  }

  function grantPromoAccessForTrack(trackId, expMs) {
    var cfg = TRACKS[trackId];
    if (!cfg) return false;
    var current = readStoredExpiry(cfg.storageKey);
    if (current > Date.now() && current >= expMs) return true;
    return cfg.grant(expMs);
  }

  function grantPromoAccessForPage() {
    var expMs = promoEndMs();
    if (!isActive() || expMs <= Date.now()) return { ok: false, tracks: [] };
    var tracks = tracksForPage();
    var granted = [];
    tracks.forEach(function (id) {
      if (grantPromoAccessForTrack(id, expMs)) granted.push(id);
    });
    return { ok: granted.length > 0, tracks: granted };
  }

  function handleFreeAccessClick(btn) {
    if (!isActive()) return;
    if (btn && btn.dataset.loading === "1") return;
    if (btn) {
      btn.dataset.loading = "1";
      btn.disabled = true;
      btn.textContent = "Unlocking…";
    }

    ensureTrackStorage(tracksForPage())
      .then(function () {
        var result = grantPromoAccessForPage();
        if (!result.ok) {
          if (btn) {
            btn.dataset.loading = "0";
            btn.disabled = false;
            btn.textContent = primaryPortalUrl() ? "Open free portal →" : "Unlock free access →";
          }
          return;
        }

        var portal = primaryPortalUrl();
        if (portal) {
          window.location.href = portal;
          return;
        }

        if (btn) {
          btn.dataset.loading = "0";
          btn.disabled = false;
          btn.textContent = "Access unlocked ✓";
        }
        var status = document.getElementById("bccSave50PromoStatus");
        if (status) {
          status.textContent =
            "Free portal access is active on CCNA, ENCOR, and Security+ until the timer ends. Open your track below.";
        }
        var main = document.getElementById("main");
        if (main && main.scrollIntoView) main.scrollIntoView({ behavior: "smooth", block: "start" });
      })
      .catch(function () {
        if (btn) {
          btn.dataset.loading = "0";
          btn.disabled = false;
          btn.textContent = primaryPortalUrl() ? "Open free portal →" : "Unlock free access →";
        }
      });
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

  function primaryCtaLabel() {
    return primaryPortalUrl() ? "Open free portal →" : "Unlock free access →";
  }

  function mountBanner() {
    if (!isLandingPage() || !isActive() || document.getElementById(BAR_ID)) return;

    document.documentElement.classList.add("bcc-save50-promo-active");

    var bar = document.createElement("div");
    bar.id = BAR_ID;
    bar.className = "bcc-save50-promo-bar";
    bar.setAttribute("role", "region");
    bar.setAttribute("aria-label", "Free portal access and 50% off offer");
    bar.innerHTML =
      '<div class="bcc-save50-promo-bar__inner">' +
      '<div class="bcc-save50-promo-bar__main">' +
      '<p class="bcc-save50-promo-bar__headline">Free full portal access</p>' +
      '<p class="bcc-save50-promo-bar__sub">Unrestricted practice until the timer ends · Optional: add the next <strong>30 days at 50% off</strong> with <code>' +
      PROMO_CODE +
      '</code> <button type="button" class="bcc-save50-promo-bar__copy" data-bcc-save50-copy>Copy code</button></p>' +
      '<p class="bcc-save50-promo-bar__status" id="bccSave50PromoStatus" aria-live="polite"></p>' +
      "</div>" +
      '<div class="bcc-save50-promo-bar__actions">' +
      '<span class="bcc-save50-promo-bar__timer">Free access + 50% deal ends<br /><strong id="' +
      COUNTDOWN_ID +
      '">--:--:--</strong></span>' +
      '<div class="bcc-save50-promo-bar__cta-row">' +
      '<button type="button" class="bcc-save50-promo-bar__cta" data-bcc-save50-free-access>' +
      primaryCtaLabel() +
      "</button>" +
      '<a class="bcc-save50-promo-bar__cta bcc-save50-promo-bar__cta--secondary" href="#purchase">30 days · 50% off</a>' +
      "</div></div></div>";

    document.body.insertBefore(bar, document.body.firstChild);

    var copyBtn = bar.querySelector("[data-bcc-save50-copy]");
    if (copyBtn) {
      copyBtn.addEventListener("click", function () {
        copyCode(copyBtn);
      });
    }

    var freeBtn = bar.querySelector("[data-bcc-save50-free-access]");
    if (freeBtn) {
      freeBtn.addEventListener("click", function () {
        handleFreeAccessClick(freeBtn);
      });
    }

    var purchaseLink = bar.querySelector(".bcc-save50-promo-bar__cta--secondary");
    if (purchaseLink && (landingPathKey() === "/" || landingPathKey() === "/index")) {
      purchaseLink.setAttribute("href", "#main");
      purchaseLink.textContent = "Choose track · 50% off";
    } else if (purchaseLink && !document.getElementById("purchase")) {
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
  window.bccGrantSave50PromoPortalAccess = grantPromoAccessForPage;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mountBanner);
  } else {
    mountBanner();
  }
  window.addEventListener("load", mountBanner);
})();

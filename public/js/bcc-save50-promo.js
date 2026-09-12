/**
 * 50% off: SEP50PERCENTOFF for 30-day access. Applies on every visit
 * (not first-visit only). A 15-minute countdown resets each new session.
 *
 * Prefills Stripe via prefilled_promo_code / Checkout Session promoCode.
 * Create the same promotion code in Stripe Dashboard (50% off) or checkout
 * will reject it.
 */
(function () {
  "use strict";

  var PROMO_CODE = "SEP50PERCENTOFF";
  var PROMO_START_MS = new Date("2026-09-01T00:00:00-04:00").getTime();
  var PROMO_END_MS = new Date("2026-10-01T00:00:00-04:00").getTime();
  var OFFER_MS = 15 * 60 * 1000;
  var LEGACY_FIRST_VISIT_END_KEY = "bcc_save50_first_visit_15m_end_v1";
  var LEGACY_POPUP_SHOWN_KEY = "bcc_save50_coupon_popup_shown_v1";
  var OFFER_END_KEY = "bcc_save50_visit_15m_end_v1";
  var BAR_ID = "bccSave50PromoBar";
  var COUNTDOWN_ID = "bccSave50Countdown";
  var POPUP_ID = "bccSave50CouponPopup";
  var POPUP_COUNTDOWN_ID = "bccSave50PopupCountdown";
  var POPUP_PENDING_KEY = "bcc_save50_popup_pending_v1";
  var timerId = null;
  var popupWaitTimer = null;
  var memoryOfferEndMs = 0;
  var lastFocusedEl = null;
  var popupDismissedThisPage = false;

  var CHECKOUT_SCRIPTS = {
    secplus: "/COMP_TIA_SEC+/js/secplus-portal-checkout.js",
    ccna: "/CCNA-Study/js/ccna-portal-30d-checkout.js",
    encor: "/CCNP-ENCOR-Study/js/encor-portal-30d-checkout.js",
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

  function isCertHome() {
    var p = landingPathKey();
    return p === "/ccna-home" || p === "/ccnp-home" || p === "/comptia-sec+-home";
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

  function alreadyHasAccess() {
    return (
      trackHasMembership("secplus") ||
      trackHasMembership("ccna") ||
      trackHasMembership("encor") ||
      trackHasMembership("ccnaauto")
    );
  }

  function clearLegacyFirstVisitLocks() {
    try {
      localStorage.removeItem(LEGACY_FIRST_VISIT_END_KEY);
      localStorage.removeItem(LEGACY_POPUP_SHOWN_KEY);
    } catch (e) {}
  }

  function readStoredOfferEnd() {
    try {
      var n = parseInt(sessionStorage.getItem(OFFER_END_KEY) || "", 10);
      if (!isNaN(n) && n > Date.now()) return n;
    } catch (e) {}
    return memoryOfferEndMs && memoryOfferEndMs > Date.now() ? memoryOfferEndMs : 0;
  }

  function writeStoredOfferEnd(ms) {
    memoryOfferEndMs = ms;
    try {
      sessionStorage.setItem(OFFER_END_KEY, String(ms));
    } catch (e) {}
  }

  function visitOfferEndMs() {
    var stored = readStoredOfferEnd();
    if (stored) return stored;
    var end = Date.now() + OFFER_MS;
    writeStoredOfferEnd(end);
    return end;
  }

  function purchaseHref() {
    var p = landingPathKey();
    if (p === "/" || p === "/index") return "#main";
    if (document.getElementById("purchase")) return "#purchase";
    return trackHomeUrl(currentTrack());
  }

  function purchaseCtaLabel() {
    var p = landingPathKey();
    if (p === "/" || p === "/index") return "Choose track · 50% off →";
    return "Get 30-day access · 50% off →";
  }

  function promoEndMs() {
    return visitOfferEndMs();
  }

  function inCalendarWindow() {
    var now = Date.now();
    return now >= PROMO_START_MS && now < PROMO_END_MS;
  }

  function isActive() {
    if (!inCalendarWindow()) return false;
    if (alreadyHasAccess()) return false;
    return true;
  }

  function formatCountdown(msLeft) {
    if (msLeft <= 0) return "Ended";
    var totalSec = Math.floor(msLeft / 1000);
    var mins = Math.floor(totalSec / 60);
    var secs = totalSec % 60;
    function pad(n) {
      return n < 10 ? "0" + n : String(n);
    }
    return pad(mins) + ":" + pad(secs);
  }

  function updateCountdown() {
    var left = promoEndMs() - Date.now();
    if (left <= 0) {
      writeStoredOfferEnd(Date.now() + OFFER_MS);
      left = promoEndMs() - Date.now();
    }
    var text = formatCountdown(left);
    var barEl = document.getElementById(COUNTDOWN_ID);
    if (barEl) barEl.textContent = text;
    var popupEl = document.getElementById(POPUP_COUNTDOWN_ID);
    if (popupEl) popupEl.textContent = text;
  }

  function ensureTimer() {
    if (timerId == null) timerId = setInterval(updateCountdown, 1000);
    updateCountdown();
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
    if (timerId != null && !document.getElementById(POPUP_ID)) {
      clearInterval(timerId);
      timerId = null;
    }
    var bar = document.getElementById(BAR_ID);
    if (bar) bar.remove();
    document.documentElement.classList.remove("bcc-save50-promo-active");
    document.documentElement.style.removeProperty("--bcc-save50-promo-h");
  }

  function currentTrack() {
    var p = landingPathKey();
    if (
      p === "/comptia-sec+-home" ||
      p.indexOf("/comp_tia_sec+") === 0 ||
      p === "/secplus-sample"
    ) {
      return "secplus";
    }
    if (p === "/ccna-home" || p.indexOf("/ccna-study") === 0 || p.indexOf("/ccna_sim") === 0) {
      return "ccna";
    }
    if (p === "/ccnp-home" || p.indexOf("/ccnp-encor") === 0) {
      return "encor";
    }
    try {
      if (sessionStorage.getItem("secplusHomeSample")) return "secplus";
      if (sessionStorage.getItem("ccnaHomeSample")) return "ccna";
      if (sessionStorage.getItem("encorHomeSample")) return "encor";
    } catch (e) {}
    return "";
  }

  function trackHomeUrl(track) {
    if (track === "secplus") return "/comptia-sec+-home.html#purchase";
    if (track === "ccna") return "/ccna-home.html#purchase";
    if (track === "encor") return "/ccnp-home.html#purchase";
    return "/index.html";
  }

  function startFnFor(track) {
    if (track === "secplus") return window.bccStartSecplusPortalCheckout;
    if (track === "ccna") return window.bccStartCcnaPortalCheckout;
    if (track === "encor") return window.bccStartEncorPortalCheckout;
    return null;
  }

  function loadCheckoutScript(track, onReady) {
    var src = CHECKOUT_SCRIPTS[track];
    if (!src) {
      onReady(false);
      return;
    }
    if (typeof startFnFor(track) === "function") {
      onReady(true);
      return;
    }
    var existing = document.querySelector('script[src="' + src + '"]');
    function waitForFn(tries) {
      if (typeof startFnFor(track) === "function") {
        onReady(true);
        return;
      }
      if (tries <= 0) {
        onReady(false);
        return;
      }
      window.setTimeout(function () {
        waitForFn(tries - 1);
      }, 50);
    }
    if (existing) {
      waitForFn(40);
      return;
    }
    var s = document.createElement("script");
    s.src = src;
    s.onload = function () {
      waitForFn(40);
    };
    s.onerror = function () {
      onReady(false);
    };
    (document.body || document.head).appendChild(s);
  }

  function handleCheckoutStart(started, triggerEl) {
    if (!started) return false;
    if (typeof started.then === "function") {
      started.catch(function (err) {
        window.alert(err && err.message ? err.message : "Could not start checkout.");
        if (triggerEl) {
          triggerEl.disabled = false;
          triggerEl.removeAttribute("aria-busy");
        }
      });
    }
    return true;
  }

  function startTrackCheckout(triggerEl) {
    var track = currentTrack();
    if (!track || track === "ccnaauto") return false;
    var fn = startFnFor(track);
    if (typeof fn === "function") {
      return handleCheckoutStart(fn("30d", triggerEl), triggerEl);
    }
    loadCheckoutScript(track, function (ok) {
      var loaded = startFnFor(track);
      if (ok && typeof loaded === "function") {
        handleCheckoutStart(loaded("30d", triggerEl), triggerEl);
        return;
      }
      window.location.href = trackHomeUrl(track);
    });
    return true;
  }

  function wireCheckoutCta(linkEl) {
    if (!linkEl) return;
    linkEl.addEventListener("click", function (ev) {
      var started = startTrackCheckout(linkEl);
      if (!started) return;
      ev.preventDefault();
    });
  }

  function mountBanner() {
    if (!isLandingPage() || !isActive() || document.getElementById(BAR_ID)) return;

    document.documentElement.classList.add("bcc-save50-promo-active");

    var bar = document.createElement("div");
    bar.id = BAR_ID;
    bar.className = "bcc-save50-promo-bar";
    bar.setAttribute("role", "region");
    bar.setAttribute("aria-label", "50 percent off for 15 minutes");
    bar.innerHTML =
      '<div class="bcc-save50-promo-bar__inner">' +
      '<div class="bcc-save50-promo-bar__main">' +
      '<p class="bcc-save50-promo-bar__headline">50% off</p>' +
      '<p class="bcc-save50-promo-bar__sub">Use code ' +
      "<code>" +
      PROMO_CODE +
      '</code> at checkout <button type="button" class="bcc-save50-promo-bar__copy" data-bcc-save50-copy>Copy code</button></p>' +
      "</div>" +
      '<div class="bcc-save50-promo-bar__actions">' +
      '<span class="bcc-save50-promo-bar__timer">Offer ends in<br /><strong id="' +
      COUNTDOWN_ID +
      '">--:--</strong></span>' +
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
    wireCheckoutCta(purchaseLink);
    if (
      landingPathKey() !== "/" &&
      landingPathKey() !== "/index" &&
      !document.getElementById("purchase") &&
      !currentTrack()
    ) {
      purchaseLink.style.display = "none";
    }

    ensureTimer();
    syncBarHeight();
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
    var cents = Math.round(n * 100);
    return (Math.round(cents / 2) / 100).toFixed(2);
  }

  function ensureStyles() {
    if (document.querySelector('link[href*="bcc-save50-promo.css"]')) return;
    var link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "/css/bcc-save50-promo.css";
    (document.head || document.documentElement).appendChild(link);
  }

  function popupAlreadyShown() {
    return popupDismissedThisPage || !!document.getElementById(POPUP_ID);
  }

  function markPopupShown() {
    try {
      sessionStorage.removeItem(POPUP_PENDING_KEY);
    } catch (e) {}
  }

  function markPopupPending() {
    try {
      sessionStorage.setItem(POPUP_PENDING_KEY, "1");
    } catch (e) {}
  }

  function consumePendingPopup() {
    try {
      if (sessionStorage.getItem(POPUP_PENDING_KEY) !== "1") return false;
      sessionStorage.removeItem(POPUP_PENDING_KEY);
      return true;
    } catch (e) {
      return false;
    }
  }

  function jumpedToSamples() {
    var hash = (location.hash || "").toLowerCase();
    return (
      hash === "#ccna-samples" ||
      hash === "#encor-samples" ||
      hash === "#secplus-samples"
    );
  }

  function pastFold() {
    if (jumpedToSamples()) return true;
    var fold = Math.max(220, Math.floor(window.innerHeight * 0.4));
    return window.scrollY >= fold;
  }

  function competingModalOpen() {
    return !!(
      document.getElementById("ciscoSampleScorecard") ||
      document.getElementById("ciscoCcnaPortalOffer") ||
      document.getElementById("secplusSamplePbqScorecard") ||
      document.getElementById("secplusSamplePortalUpsell")
    );
  }

  function salePrice() {
    return discountedValue("19.99");
  }

  function popupSecondaryLabel() {
    if (isCertHome()) return "Keep browsing";
    var track = currentTrack();
    if (track === "secplus") return "Return to Security+ home";
    if (track === "ccna") return "Return to CCNA home";
    if (track === "encor") return "Return to CCNP home";
    return "Keep browsing";
  }

  function closePopup(expired) {
    var root = document.getElementById(POPUP_ID);
    if (!root) return;
    popupDismissedThisPage = true;
    root.remove();
    document.documentElement.classList.remove("bcc-save50-popup-open");
    document.body.classList.remove("bcc-save50-popup-open");
    document.removeEventListener("keydown", onPopupKey);
    if (lastFocusedEl && typeof lastFocusedEl.focus === "function") {
      try {
        lastFocusedEl.focus();
      } catch (e) {}
    }
    lastFocusedEl = null;
    if (expired && timerId != null && !document.getElementById(BAR_ID)) {
      clearInterval(timerId);
      timerId = null;
    }
  }

  function onPopupKey(ev) {
    if (ev.key === "Escape") {
      ev.preventDefault();
      closePopup(false);
    }
  }

  function mountPopup() {
    if (document.getElementById(POPUP_ID)) return true;
    if (!isActive() || popupAlreadyShown()) return false;

    ensureStyles();
    markPopupShown();
    lastFocusedEl = document.activeElement;

    var sale = salePrice();
    var root = document.createElement("div");
    root.id = POPUP_ID;
    root.className = "bcc-save50-popup-root";
    root.setAttribute("role", "presentation");
    root.innerHTML =
      '<div class="bcc-save50-popup-backdrop" data-bcc-save50-popup-dismiss tabindex="-1"></div>' +
      '<div class="bcc-save50-popup-panel" role="dialog" aria-modal="true" aria-labelledby="bccSave50PopupTitle" tabindex="-1">' +
      '<button type="button" class="bcc-save50-popup-close" data-bcc-save50-popup-dismiss aria-label="Close coupon offer">×</button>' +
      '<p class="bcc-save50-popup-eyebrow">50% off</p>' +
      '<h2 id="bccSave50PopupTitle">50% off 30-day access</h2>' +
      '<p class="bcc-save50-popup-lead">Copy this code. We apply it at checkout.</p>' +
      '<div class="bcc-save50-popup-code-row">' +
      '<code class="bcc-save50-popup-code">' +
      PROMO_CODE +
      "</code>" +
      '<button type="button" class="bcc-save50-popup-copy" data-bcc-save50-popup-copy>Copy code</button>' +
      "</div>" +
      '<p class="bcc-save50-popup-price"><s>$19.99</s> <strong>$' +
      sale +
      "</strong> <span>for 30 days</span></p>" +
      '<p class="bcc-save50-popup-note">One-time purchase. No subscription.</p>' +
      '<p class="bcc-save50-popup-timer">Offer ends in <strong id="' +
      POPUP_COUNTDOWN_ID +
      '">--:--</strong></p>' +
      '<div class="bcc-save50-popup-actions">' +
      '<a class="bcc-save50-popup-cta" href="' +
      purchaseHref() +
      '">Get 30-day access · $' +
      sale +
      "</a>" +
      '<button type="button" class="bcc-save50-popup-secondary" data-bcc-save50-popup-secondary>' +
      popupSecondaryLabel() +
      "</button>" +
      "</div></div>";

    document.body.appendChild(root);
    document.documentElement.classList.add("bcc-save50-popup-open");
    document.body.classList.add("bcc-save50-popup-open");

    var copyBtn = root.querySelector("[data-bcc-save50-popup-copy]");
    if (copyBtn) {
      copyBtn.addEventListener("click", function () {
        copyCode(copyBtn);
      });
    }

    root.querySelectorAll("[data-bcc-save50-popup-dismiss]").forEach(function (el) {
      el.addEventListener("click", function () {
        closePopup(false);
      });
    });

    var secondary = root.querySelector("[data-bcc-save50-popup-secondary]");
    if (secondary) {
      secondary.addEventListener("click", function () {
        if (isCertHome()) {
          closePopup(false);
          return;
        }
        window.location.href = trackHomeUrl(currentTrack()).split("#")[0];
      });
    }

    wireCheckoutCta(root.querySelector(".bcc-save50-popup-cta"));
    document.addEventListener("keydown", onPopupKey);
    ensureTimer();

    var panel = root.querySelector(".bcc-save50-popup-panel");
    if (panel) panel.focus();
    return true;
  }

  function waitForCompetingModalsThenOpen() {
    if (popupWaitTimer != null) return;
    var tries = 0;
    popupWaitTimer = window.setInterval(function () {
      tries += 1;
      if (!competingModalOpen()) {
        window.clearInterval(popupWaitTimer);
        popupWaitTimer = null;
        mountPopup();
        return;
      }
      if (tries > 120) {
        window.clearInterval(popupWaitTimer);
        popupWaitTimer = null;
      }
    }, 400);
  }

  function openPopup() {
    if (!isActive() || popupAlreadyShown()) return false;
    if (document.getElementById(POPUP_ID)) return true;
    if (competingModalOpen()) {
      waitForCompetingModalsThenOpen();
      return true;
    }
    return mountPopup();
  }

  var popupTriggersBound = false;

  function bindPopupTriggers() {
    if (popupTriggersBound) return;
    popupTriggersBound = true;

    window.addEventListener("bcc-save50-sample-complete", function () {
      popupDismissedThisPage = false;
      openPopup();
    });

    if (consumePendingPopup()) {
      openPopup();
    }

    if (!isCertHome()) return;

    var checking = false;
    function checkFold() {
      if (checking) return;
      checking = true;
      window.requestAnimationFrame(function () {
        checking = false;
        if (pastFold()) openPopup();
      });
    }

    window.addEventListener("scroll", checkFold, { passive: true });
    window.addEventListener("hashchange", checkFold);
    checkFold();
  }

  window.bccSave50PromoActive = isActive;
  window.bccSave50PromoCode = function () {
    return PROMO_CODE;
  };
  window.bccSave50PromoEndMs = promoEndMs;
  window.bccBuildCheckoutUrlWithSave50 = appendPromoToCheckoutUrl;
  window.bccSave50DiscountedValue = discountedValue;
  window.bccOpenSave50CouponPopup = openPopup;
  window.bccMarkSave50CouponPopupPending = markPopupPending;

  function boot() {
    clearLegacyFirstVisitLocks();
    ensureStyles();
    mountBanner();
    bindPopupTriggers();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
  window.addEventListener("load", function () {
    mountBanner();
    if (isCertHome() && pastFold()) openPopup();
  });
})();

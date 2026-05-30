/**
 * Security+ timed test simulation access (localStorage).
 * One-time Stripe checkout session id, or active Security+ portal pass on this browser.
 */
(function () {
  var LS_TEMP_TEST = "bcc_secplus_test_sim_temp_v1";
  var LS_FREE_SIM = "bcc_secplus_free_sim_v1";

  function readFreeSimRecord() {
    try {
      var raw = localStorage.getItem(LS_FREE_SIM);
      if (!raw) return null;
      var o = JSON.parse(raw);
      if (!o || typeof o.email !== "string" || !o.email) return null;
      return o;
    } catch (e) {
      return null;
    }
  }

  function grantSecplusFreeSimAccess(email) {
    var em = typeof email === "string" ? email.trim().toLowerCase() : "";
    if (!em || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em)) return;
    try {
      localStorage.setItem(
        LS_FREE_SIM,
        JSON.stringify({ email: em, grantedAt: Date.now(), consumed: false })
      );
    } catch (e) {}
  }

  function markSecplusFreeSimConsumed() {
    try {
      var o = readFreeSimRecord();
      if (!o) return;
      o.consumed = true;
      o.consumedAt = Date.now();
      localStorage.setItem(LS_FREE_SIM, JSON.stringify(o));
    } catch (e) {}
  }

  function clearSecplusFreeSimAccess() {
    try {
      localStorage.removeItem(LS_FREE_SIM);
    } catch (e) {}
  }

  function readSecplusFreeSimEmail() {
    var o = readFreeSimRecord();
    return o && !o.consumed ? o.email : "";
  }

  function secplusFreeSimAccessActive() {
    var o = readFreeSimRecord();
    return !!(o && o.consumed !== true);
  }

  function secplusPortalPassActive() {
    if (typeof window.bccSecplusPortalAccessActiveSync === "function") {
      return window.bccSecplusPortalAccessActiveSync();
    }
    if (typeof window.bccSecplusPortalAccessActive === "function") {
      return window.bccSecplusPortalAccessActive();
    }
    try {
      var raw = localStorage.getItem("bcc_secplus_portal_v1");
      if (!raw) return false;
      var o = JSON.parse(raw);
      return typeof o.expiresAt === "number" && o.expiresAt > Date.now();
    } catch (e) {
      return false;
    }
  }

  function grantSecplusTempTestAccess(stripeSessionId) {
    if (secplusPortalPassActive()) return;
    var cs = typeof stripeSessionId === "string" ? stripeSessionId.trim() : "";
    if (!cs || cs.indexOf("cs_") !== 0) return;
    try {
      localStorage.setItem(
        LS_TEMP_TEST,
        JSON.stringify({ stripeSessionId: cs, grantedAt: Date.now(), consumed: false })
      );
    } catch (e) {}
  }

  function markSecplusTempTestConsumed() {
    if (secplusPortalPassActive()) return;
    try {
      var raw = localStorage.getItem(LS_TEMP_TEST);
      if (!raw) return;
      var o = JSON.parse(raw);
      o.consumed = true;
      localStorage.setItem(LS_TEMP_TEST, JSON.stringify(o));
    } catch (e) {}
  }

  function clearSecplusTempTestAccess() {
    try {
      localStorage.removeItem(LS_TEMP_TEST);
    } catch (e) {}
  }

  function readSecplusStoredStripeSessionId() {
    try {
      var raw = localStorage.getItem(LS_TEMP_TEST);
      if (!raw) return null;
      var o = JSON.parse(raw);
      if (o && o.consumed === true) return null;
      if (o && typeof o.stripeSessionId === "string" && o.stripeSessionId.indexOf("cs_") === 0) {
        return o.stripeSessionId;
      }
    } catch (e) {}
    return null;
  }

  function secplusTimedSimAccessActive() {
    return secplusPortalPassActive() || !!readSecplusStoredStripeSessionId();
  }

  if (typeof window !== "undefined") {
    window.secplusPortalPassActive = secplusPortalPassActive;
    window.secplusTimedSimAccessActive = secplusTimedSimAccessActive;
    window.secplusFreeSimAccessActive = secplusFreeSimAccessActive;
    window.grantSecplusFreeSimAccess = grantSecplusFreeSimAccess;
    window.clearSecplusFreeSimAccess = clearSecplusFreeSimAccess;
    window.readSecplusFreeSimEmail = readSecplusFreeSimEmail;
    window.markSecplusFreeSimConsumed = markSecplusFreeSimConsumed;
    window.grantSecplusTempTestAccess = grantSecplusTempTestAccess;
    window.clearSecplusTempTestAccess = clearSecplusTempTestAccess;
    window.readSecplusStoredStripeSessionId = readSecplusStoredStripeSessionId;
    window.markSecplusTempTestConsumed = markSecplusTempTestConsumed;
  }
})();

/**
 * ENCOR timed test simulation access (localStorage).
 * One-time Stripe checkout session id, or active ENCOR portal pass on this browser.
 */
(function () {
  var LS_TEMP_TEST = "bcc_encor_test_sim_temp_v1";
  var LS_FREE_SIM = "bcc_encor_free_sim_v1";

  function readEncorFreeSimRecordRaw() {
    try {
      var raw = localStorage.getItem(LS_FREE_SIM);
      if (!raw) return null;
      var o = JSON.parse(raw);
      return o && typeof o === "object" ? o : null;
    } catch (e) {
      return null;
    }
  }

  function readEncorFreeSimRecord() {
    var o = readEncorFreeSimRecordRaw();
    if (!o || typeof o.email !== "string" || !o.email) return null;
    return o;
  }

  function encorFreeSimWasConsumed() {
    var o = readEncorFreeSimRecordRaw();
    return !!(o && o.consumed === true);
  }

  function encorFreeSimAccessActive() {
    var o = readEncorFreeSimRecordRaw();
    if (!o || o.consumed === true) return false;
    if (o.viaGuest === true) return true;
    return !!(o.email && o.viaLeadApi === true);
  }

  function grantEncorGuestFreeSimAccess() {
    if (encorFreeSimWasConsumed()) return false;
    try {
      localStorage.setItem(
        LS_FREE_SIM,
        JSON.stringify({
          email: "",
          grantedAt: Date.now(),
          consumed: false,
          viaGuest: true,
        })
      );
      return true;
    } catch (e) {
      return false;
    }
  }

  function markEncorFreeSimConsumed() {
    try {
      var o = readEncorFreeSimRecordRaw();
      if (!o) {
        o = { email: "", grantedAt: Date.now(), viaGuest: true };
      }
      o.consumed = true;
      o.consumedAt = Date.now();
      localStorage.setItem(LS_FREE_SIM, JSON.stringify(o));
    } catch (e) {}
  }

  function encorPortalPassActive() {
    if (typeof window.bccEncorPortalAccessActiveSync === "function") {
      return window.bccEncorPortalAccessActiveSync();
    }
    if (typeof window.bccEncorPortalAccessActive === "function") {
      return window.bccEncorPortalAccessActive();
    }
    try {
      var raw = localStorage.getItem("bcc_encor_portal_v1");
      if (!raw) return false;
      var o = JSON.parse(raw);
      return typeof o.expiresAt === "number" && o.expiresAt > Date.now();
    } catch (e) {
      return false;
    }
  }

  function grantEncorTempTestAccess(stripeSessionId) {
    if (encorPortalPassActive()) return;
    var cs = typeof stripeSessionId === "string" ? stripeSessionId.trim() : "";
    if (!cs || cs.indexOf("cs_") !== 0) return;
    try {
      localStorage.setItem(
        LS_TEMP_TEST,
        JSON.stringify({ stripeSessionId: cs, grantedAt: Date.now(), consumed: false })
      );
    } catch (e) {}
  }

  function markEncorTempTestConsumed() {
    if (encorPortalPassActive()) return;
    try {
      var raw = localStorage.getItem(LS_TEMP_TEST);
      if (!raw) return;
      var o = JSON.parse(raw);
      o.consumed = true;
      localStorage.setItem(LS_TEMP_TEST, JSON.stringify(o));
    } catch (e) {}
  }

  function clearEncorTempTestAccess() {
    try {
      localStorage.removeItem(LS_TEMP_TEST);
    } catch (e) {}
  }

  function readEncorStoredStripeSessionId() {
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

  function trackEncorSimPurchase(stripeSessionId, productId) {
    if (
      typeof window.bccShouldTrackAnalytics === "function" &&
      !window.bccShouldTrackAnalytics()
    ) {
      return;
    }
    if (productId !== "encor-test-simulation" || typeof window.gtag !== "function") return;
    var trackKey = "bcc_encor_test_sim_purchase_tracked_" + stripeSessionId;
    try {
      if (localStorage.getItem(trackKey) === "1") return;
      localStorage.setItem(trackKey, "1");
    } catch (e) {}

    var attrs =
      typeof window.bccGetCampaignAttribution === "function" ? window.bccGetCampaignAttribution() : {};
    var params = {
      transaction_id: stripeSessionId,
      currency: "USD",
      value: 9.99,
      campaign_source: attrs.utm_source || undefined,
      campaign_medium: attrs.utm_medium || undefined,
      campaign_name: attrs.utm_campaign || undefined,
      campaign_content: attrs.utm_content || undefined,
      campaign_term: attrs.utm_term || undefined,
      gclid: attrs.gclid || undefined,
      items: [
        {
          item_id: "encor_timed_simulation",
          item_name: "ENCOR Timed Test Simulation",
          price: 9.99,
          quantity: 1,
        },
      ],
    };
    window.gtag("event", "purchase", params);

    if (typeof window.bccTrackGoogleAdsPurchaseConversion === "function") {
      window.bccTrackGoogleAdsPurchaseConversion(stripeSessionId, {
        currency: "USD",
        value: 9.99,
      });
    }
  }

  if (typeof window !== "undefined") {
    window.encorPortalPassActive = encorPortalPassActive;
    window.encorFreeSimAccessActive = encorFreeSimAccessActive;
    window.encorFreeSimWasConsumed = encorFreeSimWasConsumed;
    window.grantEncorGuestFreeSimAccess = grantEncorGuestFreeSimAccess;
    window.grantEncorTempTestAccess = grantEncorTempTestAccess;
    window.clearEncorTempTestAccess = clearEncorTempTestAccess;
    window.readEncorStoredStripeSessionId = readEncorStoredStripeSessionId;
    window.trackEncorSimPurchase = trackEncorSimPurchase;
    window.markEncorTempTestConsumed = markEncorTempTestConsumed;
    window.markEncorFreeSimConsumed = markEncorFreeSimConsumed;
  }
})();

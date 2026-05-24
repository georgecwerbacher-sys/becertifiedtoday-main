/**
 * ENCOR timed test simulation access (localStorage).
 * One-time Stripe checkout session id, or active ENCOR portal pass on this browser.
 */
(function () {
  var LS_TEMP_TEST = "bcc_encor_test_sim_temp_v1";

  function encorPortalPassActive() {
    if (typeof window.bccEncorPortalAccessActive === "function") {
      return window.bccEncorPortalAccessActive();
    }
    return false;
  }

  function grantEncorTempTestAccess(stripeSessionId) {
    if (encorPortalPassActive()) return;
    var cs = typeof stripeSessionId === "string" ? stripeSessionId.trim() : "";
    if (!cs || cs.indexOf("cs_") !== 0) return;
    try {
      localStorage.setItem(
        LS_TEMP_TEST,
        JSON.stringify({ stripeSessionId: cs, grantedAt: Date.now() })
      );
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
      if (o && typeof o.stripeSessionId === "string" && o.stripeSessionId.indexOf("cs_") === 0) {
        return o.stripeSessionId;
      }
    } catch (e) {}
    return null;
  }

  function trackEncorSimPurchase(stripeSessionId, productId) {
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
      value: 4.99,
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
          price: 4.99,
          quantity: 1,
        },
      ],
    };
    window.gtag("event", "purchase", params);

    if (typeof window.bccTrackGoogleAdsPurchaseConversion === "function") {
      window.bccTrackGoogleAdsPurchaseConversion(stripeSessionId, {
        currency: "USD",
        value: 4.99,
      });
    }
  }

  if (typeof window !== "undefined") {
    window.encorPortalPassActive = encorPortalPassActive;
    window.grantEncorTempTestAccess = grantEncorTempTestAccess;
    window.clearEncorTempTestAccess = clearEncorTempTestAccess;
    window.readEncorStoredStripeSessionId = readEncorStoredStripeSessionId;
    window.trackEncorSimPurchase = trackEncorSimPurchase;
  }
})();

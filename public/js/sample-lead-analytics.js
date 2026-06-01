/**
 * Log homepage sample → email capture funnel events (CCNA, ENCOR, Security+).
 */
(function () {
  "use strict";

  function shouldSend() {
    if (typeof window.bccShouldTrackAnalytics === "function" && !window.bccShouldTrackAnalytics()) {
      return false;
    }
    return true;
  }

  function utmPayload() {
    if (typeof window.bccGetCampaignAttribution !== "function") return {};
    return window.bccGetCampaignAttribution() || {};
  }

  /**
   * @param {{ event: string, product: string, email?: string, sampleKind?: string, source?: string, success?: boolean }} opts
   */
  function logSampleLeadEvent(opts) {
    if (!shouldSend() || !opts || !opts.event || !opts.product) return;
    var body = {
      event: opts.event,
      product: opts.product,
      email: opts.email || "",
      sample_kind: opts.sampleKind || "",
      source: opts.source || "",
      success: opts.success === true,
      utm: utmPayload(),
      company_website: "",
    };
    try {
      fetch("/api/sample-lead-event", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
        keepalive: true,
      }).catch(function () {});
    } catch (_) {}
  }

  function isSampleSource(source) {
    return String(source || "").toLowerCase().indexOf("sample") !== -1;
  }

  function logSampleFormAttempt(product, email, source, sampleKind) {
    if (!isSampleSource(source)) return;
    logSampleLeadEvent({
      event: "email_submit_attempt",
      product: product,
      email: email,
      source: source,
      sampleKind: sampleKind || "",
    });
  }

  function logSampleFormFail(product, email, source, sampleKind) {
    if (!isSampleSource(source)) return;
    logSampleLeadEvent({
      event: "email_capture_fail",
      product: product,
      email: email,
      source: source,
      sampleKind: sampleKind || "",
      success: false,
    });
  }

  window.bccLogSampleLeadEvent = logSampleLeadEvent;
  window.bccLogSampleLeadFormAttempt = logSampleFormAttempt;
  window.bccLogSampleLeadFormFail = logSampleFormFail;
})();

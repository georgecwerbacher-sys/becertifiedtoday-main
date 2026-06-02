/**
 * CCNA free timed assessment access (localStorage).
 * Guest access (no email) or legacy lead-capture unlock on this browser.
 */
(function () {
  "use strict";

  var LS_FREE_ASSESSMENT = "bcc_ccna_free_assessment_v1";
  var LS_FREE_SIM = "bcc_ccna_free_sim_v1";

  function readFreeSimRecordRaw() {
    try {
      var raw = localStorage.getItem(LS_FREE_SIM);
      if (!raw) return null;
      var o = JSON.parse(raw);
      return o && typeof o === "object" ? o : null;
    } catch (e) {
      return null;
    }
  }

  function ccnaFreeAssessmentWasCompleted() {
    try {
      var raw = localStorage.getItem(LS_FREE_ASSESSMENT);
      if (!raw) return false;
      var o = JSON.parse(raw);
      return !!(o && o.completedAt);
    } catch (e) {
      return false;
    }
  }

  function ccnaFreeSimWasConsumed() {
    if (ccnaFreeAssessmentWasCompleted()) return true;
    var o = readFreeSimRecordRaw();
    return !!(o && o.consumed === true);
  }

  function ccnaFreeSimAccessActive() {
    if (ccnaFreeAssessmentWasCompleted()) return false;
    var o = readFreeSimRecordRaw();
    if (!o || o.consumed === true) return false;
    if (o.viaGuest === true) return true;
    return !!(o.email && o.viaLeadApi === true);
  }

  function grantCcnaGuestFreeSimAccess() {
    if (ccnaFreeSimWasConsumed()) return false;
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

  function markCcnaFreeSimConsumed() {
    try {
      var o = readFreeSimRecordRaw();
      if (!o) {
        o = { email: "", grantedAt: Date.now(), viaGuest: true };
      }
      o.consumed = true;
      localStorage.setItem(LS_FREE_SIM, JSON.stringify(o));
    } catch (e) {}
  }

  window.ccnaFreeSimAccessActive = ccnaFreeSimAccessActive;
  window.ccnaFreeSimWasConsumed = ccnaFreeSimWasConsumed;
  window.grantCcnaGuestFreeSimAccess = grantCcnaGuestFreeSimAccess;
  window.markCcnaFreeSimConsumed = markCcnaFreeSimConsumed;
})();

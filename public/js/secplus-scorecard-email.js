/**
 * Email Security+ simulation scorecard from results panel.
 */
(function () {
  "use strict";

  function showMessage(form, text, isError) {
    var el = form.querySelector("[data-scorecard-email-message]");
    if (!el) return;
    el.textContent = text;
    el.hidden = !text;
    el.classList.toggle("scorecard-email-message--error", !!isError);
  }

  function setBusy(form, busy) {
    var btn = form.querySelector("[type=submit]");
    if (btn) {
      btn.disabled = busy;
      btn.setAttribute("aria-busy", busy ? "true" : "false");
    }
  }

  function trackEvent(name) {
    if (typeof window.gtag !== "function") return;
    window.gtag("event", name, { product: "secplus", lead_magnet: "secplus-free-simulation" });
  }

  window.SECPLUS_SCORECARD_EMAIL = {
    init: function (resultPack, defaultEmail) {
      var section = document.getElementById("scorecardEmailSection");
      var form = document.getElementById("scorecardEmailForm");
      if (!section || !form || !resultPack || !resultPack.emailPayload) return;

      section.hidden = false;
      var emailInput = form.querySelector('input[type="email"]');
      if (emailInput && defaultEmail) emailInput.value = defaultEmail;

      if (form.getAttribute("data-scorecard-wired") === "1") return;
      form.setAttribute("data-scorecard-wired", "1");

      form.addEventListener("submit", function (ev) {
        ev.preventDefault();
        showMessage(form, "", false);

        var email = emailInput ? String(emailInput.value || "").trim() : "";
        var consent = form.querySelector('input[name="scorecard_consent"]');
        if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
          showMessage(form, "Enter a valid email address.", true);
          return;
        }
        if (!consent || !consent.checked) {
          showMessage(form, "Check the box to email your scorecard.", true);
          return;
        }

        setBusy(form, true);
        trackEvent("secplus_scorecard_email_request");

        fetch("/api/secplus-scorecard-email", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: email,
            consent: true,
            scorecard: resultPack.emailPayload,
          }),
        })
          .then(function (res) {
            return res.json().then(function (data) {
              return { ok: res.ok, data: data };
            });
          })
          .then(function (result) {
            if (!result.ok || !result.data || !result.data.ok) throw new Error("fail");
            trackEvent("secplus_scorecard_email_sent");
            showMessage(form, "Scorecard sent — check your inbox (and spam).", false);
            setBusy(form, true);
          })
          .catch(function () {
            showMessage(form, "Could not send email. Try again in a moment.", true);
            setBusy(form, false);
          });
      });
    },
  };
})();

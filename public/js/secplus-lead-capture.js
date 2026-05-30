/**
 * Security+ lead magnet — unlock free timed simulation.
 */
(function () {
  "use strict";

  var MAGNET_ID = "secplus-free-simulation";
  var RUNNER_PATH = "/COMP_TIA_SEC+/test-simulation-runner.html?free=1";

  function campaignParams() {
    if (typeof window.bccGetCampaignAttribution !== "function") return {};
    return window.bccGetCampaignAttribution() || {};
  }

  function trackLeadEvent(name, extra) {
    if (typeof window.gtag !== "function") return;
    var attrs = campaignParams();
    window.gtag(
      "event",
      name,
      Object.assign(
        {
          lead_magnet: MAGNET_ID,
          product: "secplus",
          landing_path: location.pathname,
        },
        extra || {},
        attrs.utm_campaign ? { campaign_name: attrs.utm_campaign } : {},
        attrs.utm_content ? { campaign_content: attrs.utm_content } : {}
      )
    );
  }

  function setBusy(form, busy) {
    var btn = form.querySelector("[type=submit]");
    if (btn) {
      btn.disabled = busy;
      btn.setAttribute("aria-busy", busy ? "true" : "false");
    }
  }

  function showMessage(form, text, isError) {
    var el = form.querySelector("[data-lead-message]");
    if (!el) return;
    el.textContent = text;
    el.hidden = !text;
    el.classList.toggle("lead-capture-message--error", !!isError);
  }

  function hasFreeSimAccess() {
    return typeof window.secplusFreeSimAccessActive === "function" && window.secplusFreeSimAccessActive();
  }

  function wireForm(form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      showMessage(form, "", false);

      var emailInput = form.querySelector('input[type="email"]');
      var consent = form.querySelector('input[name="lead_consent"]');
      var email = emailInput ? String(emailInput.value || "").trim() : "";

      if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        showMessage(form, "Enter a valid email address.", true);
        emailInput && emailInput.focus();
        return;
      }
      if (!consent || !consent.checked) {
        showMessage(form, "Check the box to start your free simulation.", true);
        return;
      }

      setBusy(form, true);
      trackLeadEvent("generate_lead", { method: "secplus_free_sim_form" });

      fetch("/api/lead-capture", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: email,
          magnet: MAGNET_ID,
          product: "secplus",
          consent: true,
          company_website: (form.querySelector('input[name="company_website"]') || {}).value || "",
        }),
      })
        .then(function (res) {
          return res.json().then(function (data) {
            return { ok: res.ok, data: data };
          });
        })
        .then(function (result) {
          if (!result.ok || !result.data || !result.data.redirectUrl) {
            throw new Error((result.data && result.data.error) || "request_failed");
          }
          if (typeof window.grantSecplusFreeSimAccess === "function") {
            window.grantSecplusFreeSimAccess(email);
          }
          try {
            sessionStorage.setItem("secplusTestSimFree", "1");
          } catch (_) {}
          trackLeadEvent("secplus_free_sim_unlock", { email_domain: email.split("@")[1] || "" });
          window.location.href = result.data.redirectUrl;
        })
        .catch(function () {
          showMessage(form, "Something went wrong. Try again or use the free samples below.", true);
          setBusy(form, false);
        });
    });
  }

  function enhanceUnlockedState(section) {
    if (!hasFreeSimAccess()) return;
    var link = section.querySelector("[data-lead-open-sim]");
    if (link) link.hidden = false;
    var formWrap = section.querySelector("[data-lead-form-wrap]");
    if (formWrap) formWrap.hidden = true;
  }

  document.addEventListener("DOMContentLoaded", function () {
    var section = document.getElementById("secplus-lead-capture");
    if (!section) return;

    var form = section.querySelector("form[data-secplus-lead-form]");
    if (form) wireForm(form);
    enhanceUnlockedState(section);

    var utmContent = campaignParams().utm_content || "";
    if (
      location.hash === "#secplus-lead-capture" ||
      /lead-free-sim|free-sim|free.simulation/i.test(utmContent)
    ) {
      section.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });
})();

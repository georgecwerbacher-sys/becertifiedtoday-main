/**
 * Security+ lead magnet — unlock free timed simulation.
 */
(function () {
  "use strict";

  var MAGNET_ID = "secplus-free-simulation";
  var RUNNER_PATH = "/COMP_TIA_SEC+/test-simulation-runner.html?free=1";
  var LS_FREE_SIM = "bcc_secplus_free_sim_v1";

  /** Must match secplus-test-sim-storage.js — landing page loads before runner scripts. */
  function grantFreeSimAccessLocal(email, opts) {
    opts = opts || {};
    var em = typeof email === "string" ? email.trim().toLowerCase() : "";
    if (!em || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em)) return false;
    try {
      localStorage.setItem(
        LS_FREE_SIM,
        JSON.stringify({
          email: em,
          grantedAt: Date.now(),
          consumed: false,
          viaLeadApi: opts.viaLeadApi === true,
        })
      );
      return true;
    } catch (e) {
      return false;
    }
  }

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

  function readFreeSimRecordLocal() {
    try {
      var raw = localStorage.getItem(LS_FREE_SIM);
      if (!raw) return null;
      return JSON.parse(raw);
    } catch (e) {
      return null;
    }
  }

  function hasFreeSimAccess() {
    if (typeof window.secplusFreeSimAccessActive === "function" && window.secplusFreeSimAccessActive()) {
      return true;
    }
    var o = readFreeSimRecordLocal();
    return !!(o && o.consumed !== true && o.email && o.viaLeadApi === true);
  }

  function persistFreeSimSessionFlags(email) {
    try {
      sessionStorage.setItem("secplusTestSimFree", "1");
      sessionStorage.setItem("secplusTestSimFreeEmail", email);
    } catch (_) {}
  }

  function grantFreeSimAccess(email) {
    if (typeof window.grantSecplusFreeSimAccess === "function") {
      window.grantSecplusFreeSimAccess(email, { viaLeadApi: true });
    } else {
      grantFreeSimAccessLocal(email, { viaLeadApi: true });
    }
    persistFreeSimSessionFlags(email);
  }

  function wireSecplusLeadForm(form, options) {
    if (!form || form.getAttribute("data-secplus-lead-wired") === "1") return;
    form.setAttribute("data-secplus-lead-wired", "1");
    options = options || {};

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
      trackLeadEvent("generate_lead", { method: options.method || "secplus_free_sim_form" });

      var attrs = campaignParams();
      fetch("/api/lead-capture", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: email,
          magnet: MAGNET_ID,
          product: "secplus",
          consent: true,
          source: options.method || "secplus_free_sim_form",
          utm: attrs,
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
          grantFreeSimAccess(email);
          trackLeadEvent("secplus_free_sim_unlock", { email_domain: email.split("@")[1] || "" });
          if (typeof options.onSuccess === "function") {
            options.onSuccess(email, result.data);
            setBusy(form, false);
            return;
          }
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
  }

  document.addEventListener("DOMContentLoaded", function () {
    var section = document.getElementById("secplus-lead-capture");
    if (section) {
      var form = section.querySelector("form[data-secplus-lead-form]");
      if (form) wireSecplusLeadForm(form, { method: "secplus_free_sim_landing" });
      enhanceUnlockedState(section);
    }

    var utmContent = campaignParams().utm_content || "";
    if (
      section &&
      (location.hash === "#secplus-lead-capture" ||
        /lead-free-sim|free-sim|free.simulation/i.test(utmContent))
    ) {
      section.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });

  window.wireSecplusLeadForm = wireSecplusLeadForm;
  window.secplusHasFreeSimAccess = hasFreeSimAccess;
})();

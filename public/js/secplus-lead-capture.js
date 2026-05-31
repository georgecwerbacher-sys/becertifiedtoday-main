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

  function injectLeadModalStyles() {
    if (document.head.querySelector("style[data-secplus-lead-modal]")) return;
    var s = document.createElement("style");
    s.setAttribute("data-secplus-lead-modal", "1");
    s.textContent =
      ".secplus-lead-modal-root{position:fixed;inset:0;z-index:20003;display:flex;align-items:center;justify-content:center;padding:16px}" +
      ".secplus-lead-modal-backdrop{position:absolute;inset:0;background:rgba(8,12,24,.72);backdrop-filter:blur(4px)}" +
      ".secplus-lead-modal-panel{position:relative;z-index:1;width:min(560px,100%);max-height:min(92vh,760px);overflow:auto;margin:0;padding:0;border-radius:16px;box-shadow:0 24px 64px rgba(0,0,0,.45)}" +
      ".secplus-lead-modal-close{position:absolute;top:10px;right:12px;z-index:2;border:0;background:rgba(255,255,255,.9);color:#475569;font-size:1.5rem;line-height:1;cursor:pointer;padding:4px 10px;border-radius:8px}" +
      ".secplus-lead-modal-section{margin:0;padding:clamp(18px,3vw,24px);border-radius:16px;border:1px solid rgba(47,102,191,.38);background:linear-gradient(165deg,#eff6ff 0%,#f8fafc 55%,#fff 100%);color:#0b1020}" +
      ".secplus-lead-modal-section .lead-capture-badge{display:inline-block;margin:0 0 10px;padding:4px 10px;border-radius:999px;font-size:.72rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#1e3a5f;background:rgba(47,102,191,.14);border:1px solid rgba(47,102,191,.28)}" +
      ".secplus-lead-modal-section h2{margin:0 0 8px;font-size:clamp(1.12rem,2.5vw,1.32rem);font-weight:800;letter-spacing:-.02em;line-height:1.3;color:#0b1020}" +
      ".secplus-lead-modal-section .lead-capture-lead{margin:0 0 14px;color:#475569;font-size:clamp(.92rem,2vw,1rem);line-height:1.55}" +
      ".secplus-lead-modal-section .lead-capture-list{margin:0 0 14px;padding-left:1.15rem;color:#475569;font-size:.92rem;line-height:1.55}" +
      ".secplus-lead-modal-section .lead-capture-list li+li{margin-top:6px}" +
      ".secplus-lead-modal-section .lead-capture-list a{font-weight:700;color:#2f66bf;text-decoration:underline;text-underline-offset:2px}" +
      ".secplus-lead-modal-section .lead-capture-form{display:grid;gap:12px;max-width:420px}" +
      ".secplus-lead-modal-section .lead-capture-form label{display:grid;gap:6px;font-size:.88rem;font-weight:600;color:#0b1020}" +
      ".secplus-lead-modal-section .lead-capture-form input[type=email]{width:100%;min-height:48px;padding:12px 14px;border-radius:10px;border:1px solid #cbd5e1;font:inherit;color:#0b1020;background:#fff;box-sizing:border-box}" +
      ".secplus-lead-modal-section .lead-capture-form input[type=email]:focus-visible{outline:2px solid #4f84d8;outline-offset:2px}" +
      ".secplus-lead-modal-section .lead-capture-consent{display:flex;gap:10px;align-items:flex-start;font-size:.84rem;font-weight:400;color:#475569;line-height:1.45}" +
      ".secplus-lead-modal-section .lead-capture-consent input{margin-top:.2em;flex-shrink:0}" +
      ".secplus-lead-modal-section .lead-capture-honeypot{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}" +
      ".secplus-lead-modal-section .lead-capture-message{margin:0;font-size:.88rem;color:#166534}" +
      ".secplus-lead-modal-section .lead-capture-message--error{color:#b91c1c}" +
      ".secplus-lead-modal-section .lead-capture-fine{margin:10px 0 0;font-size:.78rem;color:#64748b;line-height:1.45}" +
      ".secplus-lead-modal-section .lead-capture-fine a{font-weight:700;color:#2f66bf}" +
      ".secplus-lead-modal-section .lead-capture-open-link{margin:0 0 14px;font-size:.92rem}" +
      ".secplus-lead-modal-section .lead-capture-open-link a{font-weight:800;color:#2f66bf}" +
      ".secplus-lead-modal-section .cta-main{display:inline-flex;justify-content:center;align-items:center;width:100%;min-height:48px;padding:12px 18px;border:0;border-radius:10px;background:linear-gradient(135deg,#4f84d8,#2f66bf);color:#fff;font:inherit;font-weight:800;cursor:pointer;box-sizing:border-box}" +
      ".secplus-lead-modal-section .cta-main:disabled{opacity:.65;cursor:not-allowed}" +
      "body.secplus-lead-modal-open{overflow:hidden}";
    document.head.appendChild(s);
  }

  function buildLeadModalInner(finishHome) {
    var home = finishHome || "/comptia-sec+-home.html";
    var purchaseHref = home + "#purchase";
    return (
      '<section class="lead-capture-section secplus-lead-modal-section" aria-labelledby="secplusLeadModalTitle">' +
      '<p class="lead-capture-badge">Free · 35 minutes · no checkout</p>' +
      '<h2 id="secplusLeadModalTitle">Start your free SY0-701 timed simulation</h2>' +
      '<p class="lead-capture-lead">Enter your email to unlock a <strong>35-minute sample exam</strong> in your browser: ' +
      "<strong>20 multiple-choice questions</strong> (four from each SY0-701 domain) plus the " +
      "<strong>dark web account protection</strong> performance-based simulation—the same mix of item types you will see on test day.</p>" +
      "<ul class=\"lead-capture-list\">" +
      "<li><strong>Back</strong>, <strong>Mark for review</strong>, and <strong>Next</strong>—same navigation as the full 90-minute sim</li>" +
      "<li>Scaled score and domain breakdown on the results screen; email your scorecard when you finish</li>" +
      "<li>One free attempt per browser</li>" +
      '<li>Ready for a full dry run? <a href="' +
      purchaseHref +
      '" data-secplus-lead-purchase>90-minute simulation — $9.99</a> or portal access below</li>' +
      "</ul>" +
      '<p class="lead-capture-open-link" data-lead-open-sim hidden>Already unlocked on this browser? ' +
      '<a href="' +
      RUNNER_PATH +
      '" data-secplus-lead-continue>Continue your free simulation →</a></p>' +
      '<form class="lead-capture-form" data-secplus-lead-form action="/api/lead-capture" method="post" novalidate>' +
      "<label>Email<input type=\"email\" name=\"email\" autocomplete=\"email\" inputmode=\"email\" placeholder=\"you@example.com\" required /></label>" +
      '<label class="lead-capture-honeypot" aria-hidden="true">Company website<input type="text" name="company_website" tabindex="-1" autocomplete="off" /></label>' +
      '<label class="lead-capture-consent"><input type="checkbox" name="lead_consent" value="1" required />' +
      "<span>Start my free simulation and send my scorecard to this email when I request it. Occasional Security+ exam prep tips — unsubscribe anytime.</span></label>" +
      '<button type="submit" class="cta-main">Start free simulation</button>' +
      '<p class="lead-capture-message" data-lead-message hidden></p>' +
      "</form>" +
      '<p class="lead-capture-fine">Exam prep only — not affiliated with CompTIA. Prefer no email? <a href="/secplus-sample?track=questions">Try free sample questions</a>.</p>' +
      "</section>"
    );
  }

  function showSecplusFreeSimLeadModal(options) {
    options = options || {};
    if (document.getElementById("secplusSampleLeadModal")) return;

    var finishHome = options.finishHome || "/comptia-sec+-home.html";

    if (hasFreeSimAccess()) {
      if (typeof options.onBeforeNavigate === "function") options.onBeforeNavigate();
      window.location.href = RUNNER_PATH;
      return;
    }

    injectLeadModalStyles();

    var root = document.createElement("div");
    root.id = "secplusSampleLeadModal";
    root.className = "secplus-lead-modal-root";
    root.setAttribute("role", "presentation");
    root.innerHTML =
      '<div class="secplus-lead-modal-backdrop" data-secplus-lead-modal-dismiss tabindex="-1"></div>' +
      '<div class="secplus-lead-modal-panel" role="dialog" aria-modal="true" aria-labelledby="secplusLeadModalTitle" tabindex="-1">' +
      '<button type="button" class="secplus-lead-modal-close" data-secplus-lead-modal-dismiss aria-label="Close dialog">×</button>' +
      buildLeadModalInner(finishHome) +
      "</div>";

    document.body.appendChild(root);
    document.body.classList.add("secplus-lead-modal-open");

    var panel = root.querySelector(".secplus-lead-modal-panel");
    var prevOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    function closeLeadModal() {
      root.remove();
      document.body.classList.remove("secplus-lead-modal-open");
      document.body.style.overflow = prevOverflow;
      document.removeEventListener("keydown", onKey);
    }

    function onKey(ev) {
      if (ev.key === "Escape") {
        ev.preventDefault();
        closeLeadModal();
      }
    }

    document.addEventListener("keydown", onKey);

    root.querySelectorAll("[data-secplus-lead-modal-dismiss]").forEach(function (el) {
      el.addEventListener("click", closeLeadModal);
    });

    var purchaseLink = root.querySelector("[data-secplus-lead-purchase]");
    if (purchaseLink) {
      purchaseLink.addEventListener("click", function (ev) {
        ev.preventDefault();
        if (typeof options.onBeforeNavigate === "function") options.onBeforeNavigate();
        window.location.href = finishHome + "#purchase";
      });
    }

    var continueLink = root.querySelector("[data-secplus-lead-continue]");
    if (continueLink) {
      continueLink.addEventListener("click", function (ev) {
        ev.preventDefault();
        if (typeof options.onBeforeNavigate === "function") options.onBeforeNavigate();
        window.location.href = RUNNER_PATH;
      });
    }

    if (hasFreeSimAccess()) {
      var openLink = root.querySelector("[data-lead-open-sim]");
      if (openLink) openLink.hidden = false;
    }

    var form = root.querySelector("form[data-secplus-lead-form]");
    wireSecplusLeadForm(form, {
      method: options.method || "secplus_free_sim_sample_popup",
      onSuccess: function (_email, data) {
        if (typeof options.onBeforeNavigate === "function") options.onBeforeNavigate();
        window.location.href = data.redirectUrl || RUNNER_PATH;
      },
    });

    var emailInput = form && form.querySelector('input[type="email"]');
    if (emailInput) emailInput.focus();
    else if (panel) panel.focus();
  }

  document.addEventListener("DOMContentLoaded", function () {
    var funnel = document.querySelector(".hero-content .funnel");
    var isLeadLanding =
      typeof window.bccIsSecplusLeadLanding === "function" && window.bccIsSecplusLeadLanding();
    if (isLeadLanding && funnel) {
      funnel.classList.add("funnel--lead-first");
    }

    var section = document.getElementById("secplus-lead-capture");
    if (section) {
      var form = section.querySelector("form[data-secplus-lead-form]");
      if (form) wireSecplusLeadForm(form, { method: "secplus_free_sim_landing" });
      enhanceUnlockedState(section);
    }

    if (section && isLeadLanding && location.hash === "#secplus-lead-capture") {
      section.scrollIntoView({ behavior: "smooth", block: "start" });
    } else if (
      section &&
      !isLeadLanding &&
      (location.hash === "#secplus-lead-capture" ||
        /lead-free-sim|free-sim|free\.simulation/i.test(campaignParams().utm_content || ""))
    ) {
      section.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });

  window.wireSecplusLeadForm = wireSecplusLeadForm;
  window.secplusHasFreeSimAccess = hasFreeSimAccess;
  window.showSecplusFreeSimLeadModal = showSecplusFreeSimLeadModal;
})();

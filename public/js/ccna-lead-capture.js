/**
 * CCNA lead magnet — unlock free timed simulation (20 MCQ + 2 D&D + 1 lab).
 */
(function () {
  "use strict";

  var MAGNET_ID = "ccna-free-simulation";
  var RUNNER_PATH = "/CCNA_Sim_EXAM/free-assessment.html?welcome=1";
  var LS_FREE_SIM = "bcc_ccna_free_sim_v1";
  var HOME = "/ccna-home.html";
  var LEAD_HASH = "#ccna-lead-capture";
  var SAMPLE_QUESTIONS_HREF = "/sample?track=ccna-questions";

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
    if (typeof window.bccShouldTrackAnalytics === "function" && !window.bccShouldTrackAnalytics()) {
      return;
    }
    if (typeof window.gtag !== "function") return;
    var attrs = campaignParams();
    window.gtag(
      "event",
      name,
      Object.assign(
        {
          lead_magnet: MAGNET_ID,
          product: "ccna",
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
    if (typeof window.ccnaFreeSimAccessActive === "function" && window.ccnaFreeSimAccessActive()) {
      return true;
    }
    var o = readFreeSimRecordLocal();
    return !!(o && o.consumed !== true && o.email && o.viaLeadApi === true);
  }

  function grantFreeSimAccess(email) {
    grantFreeSimAccessLocal(email, { viaLeadApi: true });
  }

  function wireCcnaLeadForm(form, options) {
    if (!form || form.getAttribute("data-ccna-lead-wired") === "1") return;
    form.setAttribute("data-ccna-lead-wired", "1");
    options = options || {};

    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      showMessage(form, "", false);

      var emailInput = form.querySelector('input[type="email"]');
      var consent = form.querySelector('input[name="lead_consent"]');
      var email = emailInput ? String(emailInput.value || "").trim() : "";

      if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        showMessage(form, "Enter a valid email address.", true);
        if (emailInput) emailInput.focus();
        return;
      }
      if (!consent || !consent.checked) {
        showMessage(form, "Check the box to start your free simulation.", true);
        return;
      }

      setBusy(form, true);
      var leadSource = options.method || "ccna_free_sim_form";
      if (typeof window.bccLogSampleLeadFormAttempt === "function") {
        window.bccLogSampleLeadFormAttempt("ccna", email, leadSource, options.sampleKind || "");
      }
      if (window.bccIsInternalAnalyticsEmail && window.bccIsInternalAnalyticsEmail(email)) {
        if (typeof window.bccSetAnalyticsExclude === "function") window.bccSetAnalyticsExclude(true);
      } else {
        trackLeadEvent("generate_lead", { method: leadSource });
      }

      var attrs = campaignParams();
      fetch("/api/lead-capture", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: email,
          magnet: MAGNET_ID,
          product: "ccna",
          consent: true,
          source: leadSource,
          sample_kind: options.sampleKind || "",
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
          trackLeadEvent("ccna_free_sim_unlock", { email_domain: email.split("@")[1] || "" });
          if (typeof options.onSuccess === "function") {
            options.onSuccess(email, result.data);
            setBusy(form, false);
            return;
          }
          window.location.href = result.data.redirectUrl;
        })
        .catch(function () {
          if (typeof window.bccLogSampleLeadFormFail === "function") {
            window.bccLogSampleLeadFormFail("ccna", email, leadSource, options.sampleKind || "");
          }
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
    if (document.head.querySelector("style[data-ccna-lead-modal]")) return;
    var s = document.createElement("style");
    s.setAttribute("data-ccna-lead-modal", "1");
    s.textContent =
      ".ccna-lead-modal-root{position:fixed;inset:0;z-index:20003;display:flex;align-items:center;justify-content:center;padding:16px}" +
      ".ccna-lead-modal-backdrop{position:absolute;inset:0;background:rgba(8,12,24,.72);backdrop-filter:blur(4px)}" +
      ".ccna-lead-modal-panel{position:relative;z-index:1;width:min(560px,100%);max-height:min(92vh,760px);overflow:auto;margin:0;padding:0;border-radius:16px;box-shadow:0 24px 64px rgba(0,0,0,.45)}" +
      ".ccna-lead-modal-close{position:absolute;top:10px;right:12px;z-index:2;border:0;background:rgba(255,255,255,.9);color:#475569;font-size:1.5rem;line-height:1;cursor:pointer;padding:4px 10px;border-radius:8px}" +
      ".ccna-lead-modal-section{margin:0;padding:clamp(18px,3vw,24px);border-radius:16px;border:1px solid rgba(47,102,191,.38);background:linear-gradient(165deg,#eff6ff 0%,#f8fafc 55%,#fff 100%);color:#0b1020}" +
      ".ccna-lead-modal-section .lead-capture-badge{display:inline-block;margin:0 0 10px;padding:4px 10px;border-radius:999px;font-size:.72rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#1e3a5f;background:rgba(47,102,191,.14);border:1px solid rgba(47,102,191,.28)}" +
      ".ccna-lead-modal-section h2{margin:0 0 8px;font-size:clamp(1.12rem,2.5vw,1.32rem);font-weight:800;letter-spacing:-.02em;line-height:1.3;color:#0b1020}" +
      ".ccna-lead-modal-section .lead-capture-lead{margin:0 0 14px;color:#475569;font-size:clamp(.92rem,2vw,1rem);line-height:1.55}" +
      ".ccna-lead-modal-section .lead-capture-list{margin:0 0 14px;padding-left:1.15rem;color:#475569;font-size:.92rem;line-height:1.55}" +
      ".ccna-lead-modal-section .lead-capture-list li+li{margin-top:6px}" +
      ".ccna-lead-modal-section .lead-capture-form{display:grid;gap:12px;max-width:420px}" +
      ".ccna-lead-modal-section .lead-capture-form label{display:grid;gap:6px;font-size:.88rem;font-weight:600;color:#0b1020}" +
      ".ccna-lead-modal-section .lead-capture-form input[type=email]{width:100%;min-height:48px;padding:12px 14px;border-radius:10px;border:1px solid #cbd5e1;font:inherit;color:#0b1020;background:#fff;box-sizing:border-box}" +
      ".ccna-lead-modal-section .lead-capture-consent{display:flex;gap:10px;align-items:flex-start;font-size:.84rem;font-weight:400;color:#475569;line-height:1.45}" +
      ".ccna-lead-modal-section .lead-capture-consent input{margin-top:.2em;flex-shrink:0}" +
      ".ccna-lead-modal-section .lead-capture-honeypot{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}" +
      ".ccna-lead-modal-section .lead-capture-message{margin:0;font-size:.88rem;color:#166534}" +
      ".ccna-lead-modal-section .lead-capture-message--error{color:#b91c1c}" +
      ".ccna-lead-modal-section .lead-capture-fine{margin:10px 0 0;font-size:.78rem;color:#64748b;line-height:1.45}" +
      ".ccna-lead-modal-section .lead-capture-fine a{font-weight:700;color:#2f66bf}" +
      ".ccna-lead-modal-section .cta-main{display:inline-flex;justify-content:center;align-items:center;width:100%;min-height:48px;padding:12px 18px;border:0;border-radius:10px;background:linear-gradient(135deg,#4f84d8,#2f66bf);color:#fff;font:inherit;font-weight:800;cursor:pointer;box-sizing:border-box}" +
      "body.ccna-lead-modal-open{overflow:hidden}";
    document.head.appendChild(s);
  }

  function buildLeadModalInner(finishHome) {
    var home = finishHome || HOME;
    return (
      '<section class="lead-capture-section ccna-lead-modal-section" aria-labelledby="ccnaLeadModalTitle">' +
      '<p class="lead-capture-badge">Free · 45 minutes · no checkout</p>' +
      '<h2 id="ccnaLeadModalTitle">Start your free CCNA 200-301 timed simulation</h2>' +
      '<p class="lead-capture-lead">Enter your email to unlock a <strong>45-minute sample exam</strong> in your browser: ' +
      "<strong>20 multiple-choice questions</strong>, <strong>2 drag-and-drop</strong> items, and the <strong>VLAN CLI lab</strong>—the same mix of item types you will see on test day.</p>" +
      "<ul class=\"lead-capture-list\">" +
      "<li><strong>Back</strong>, <strong>Home</strong>, and <strong>Next</strong>—same navigation as the full timed sim</li>" +
      "<li>Scaled score and domain breakdown on the results screen when you finish</li>" +
      "<li>One free attempt per browser after email unlock</li>" +
      '<li>Ready for a full dry run? <a href="' +
      home +
      '#purchase">120-minute simulation — $9.99</a> or portal access above</li>' +
      "</ul>" +
      '<p class="lead-capture-open-link" data-lead-open-sim hidden>Already unlocked on this browser? ' +
      '<a href="' +
      RUNNER_PATH +
      '">Continue your free simulation →</a></p>' +
      '<form class="lead-capture-form" data-ccna-lead-form action="/api/lead-capture" method="post" novalidate>' +
      "<label>Email<input type=\"email\" name=\"email\" autocomplete=\"email\" inputmode=\"email\" placeholder=\"you@example.com\" required /></label>" +
      '<label class="lead-capture-honeypot" aria-hidden="true">Company website<input type="text" name="company_website" tabindex="-1" autocomplete="off" /></label>' +
      '<label class="lead-capture-consent"><input type="checkbox" name="lead_consent" value="1" required />' +
      "<span>Start my free simulation and send occasional CCNA exam prep tips — unsubscribe anytime.</span></label>" +
      '<button type="submit" class="cta-main">Start free simulation</button>' +
      '<p class="lead-capture-message" data-lead-message hidden></p>' +
      "</form>" +
      '<p class="lead-capture-fine">Exam prep only — not affiliated with Cisco. Prefer no email? <a href="' +
      SAMPLE_QUESTIONS_HREF +
      '">Try free sample questions</a>.</p>' +
      "</section>"
    );
  }

  function showCcnaFreeSimLeadModal(options) {
    options = options || {};
    if (document.getElementById("ccnaSampleLeadModal")) return;

    var finishHome = options.finishHome || HOME;

    if (hasFreeSimAccess()) {
      if (typeof options.onBeforeNavigate === "function") options.onBeforeNavigate();
      window.location.href = RUNNER_PATH;
      return;
    }

    injectLeadModalStyles();

    var root = document.createElement("div");
    root.id = "ccnaSampleLeadModal";
    root.className = "ccna-lead-modal-root";
    root.setAttribute("role", "presentation");
    root.innerHTML =
      '<div class="ccna-lead-modal-backdrop" data-ccna-lead-modal-dismiss tabindex="-1"></div>' +
      '<div class="ccna-lead-modal-panel" role="dialog" aria-modal="true" aria-labelledby="ccnaLeadModalTitle" tabindex="-1">' +
      '<button type="button" class="ccna-lead-modal-close" data-ccna-lead-modal-dismiss aria-label="Close dialog">×</button>' +
      buildLeadModalInner(finishHome) +
      "</div>";

    document.body.appendChild(root);
    document.body.classList.add("ccna-lead-modal-open");

    var panel = root.querySelector(".ccna-lead-modal-panel");
    var prevOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    function closeLeadModal() {
      root.remove();
      document.body.classList.remove("ccna-lead-modal-open");
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

    root.querySelectorAll("[data-ccna-lead-modal-dismiss]").forEach(function (el) {
      el.addEventListener("click", closeLeadModal);
    });

    if (hasFreeSimAccess()) {
      var openLink = root.querySelector("[data-lead-open-sim]");
      if (openLink) openLink.hidden = false;
    }

    var form = root.querySelector("form[data-ccna-lead-form]");
    wireCcnaLeadForm(form, {
      method: options.method || "ccna_free_sim_sample_popup",
      onSuccess: function (_email, data) {
        if (typeof options.onBeforeNavigate === "function") options.onBeforeNavigate();
        window.location.href = data.redirectUrl || RUNNER_PATH;
      },
    });

    var emailInput = form && form.querySelector('input[type="email"]');
    if (emailInput) emailInput.focus();
    else if (panel) panel.focus();
  }

  function isCcnaLeadLanding() {
    if (location.hash === LEAD_HASH) return true;
    try {
      var qs = new URLSearchParams(location.search);
      if (/lead-free-sim|free-sim|free\.simulation/i.test(qs.get("utm_content") || "")) return true;
    } catch (e) {}
    return false;
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (isCcnaLeadLanding()) {
      document.documentElement.classList.add("ccna-landing-lead-first");
    }

    var section = document.getElementById("ccna-lead-capture");
    if (section) {
      var form = section.querySelector("form[data-ccna-lead-form]");
      if (form) wireCcnaLeadForm(form, { method: "ccna_free_sim_landing" });
      enhanceUnlockedState(section);
    }

    if (section && location.hash === LEAD_HASH) {
      section.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });

  window.wireCcnaLeadForm = wireCcnaLeadForm;
  window.ccnaFreeSimAccessActive = hasFreeSimAccess;
  window.ccnaHasFreeSimAccess = hasFreeSimAccess;
  window.showCcnaFreeSimLeadModal = showCcnaFreeSimLeadModal;
  window.bccIsCcnaLeadLanding = isCcnaLeadLanding;
})();

/**
 * Bottom-of-page feedback on practice questions, labs, scenarios, and drag-and-drop.
 */
(function () {
  "use strict";

  var STYLE_ID = "bcc-page-feedback-style";
  var ROOT_ID = "bccPageFeedback";
  var STORAGE_PREFIX = "bccPageFeedbackDone:";

  function detectProduct() {
    var p = (location.pathname || "").toLowerCase();
    if (p.indexOf("comptia-sec") !== -1 || p.indexOf("/comp_tia_sec+/") !== -1) return "secplus";
    if (p.indexOf("ccnp-encor") !== -1 || p.indexOf("/ccnp-encor-study/") !== -1) return "encor";
    if (p.indexOf("ccnaauto") !== -1 || p.indexOf("/ccnaauto-study/") !== -1) return "ccnaauto";
    if (p.indexOf("ccna") !== -1 || p.indexOf("/ccna-study/") !== -1) return "ccna";
    return "general";
  }

  function detectContentType() {
    var p = (location.pathname || "").toLowerCase();
    if (
      p.indexOf("/ccna_d_d/") !== -1 ||
      p.indexOf("/ccnp-encor-drag-drop/") !== -1 ||
      p.indexOf("/ccnaauto_d_d/") !== -1 ||
      p.indexOf("/ccnaauto_coding/") !== -1 ||
      p.indexOf("dragdrop") !== -1
    ) {
      return "drag_drop";
    }
    if (p.indexOf("/ccna_labs/") !== -1 || p.indexOf("/ccnp-encor-labs/") !== -1 || p.indexOf("cli-lab") !== -1) {
      return "lab";
    }
    if (p.indexOf("/pbq_production/") !== -1 || p.indexOf("/sec+_sim_hot_spot/") !== -1) return "pbq";
    if (p.indexOf("/encor_samples/") !== -1 || p.indexOf("/sec+_samples/") !== -1) return "scenario";
    return "question";
  }

  function injectStyles() {
    if (document.getElementById(STYLE_ID)) return;
    var style = document.createElement("style");
    style.id = STYLE_ID;
    style.textContent =
      ".bcc-page-feedback{margin:32px auto 24px;padding:18px 16px 20px;max-width:min(720px,calc(100vw - 32px));" +
      "background:#0d1b3d;border:1px solid #2a4a7a;border-radius:12px;box-shadow:0 8px 24px rgba(0,0,0,.25);" +
      "color:#9fb0cc;font-size:.88rem;line-height:1.5}" +
      ".bcc-page-feedback h3{margin:0 0 10px;font-size:.95rem;font-weight:800;color:#d8e4f8}" +
      ".bcc-pf-toggle{display:flex;gap:10px;align-items:flex-start;cursor:pointer;font-weight:700;color:#c5d4f0}" +
      ".bcc-pf-toggle input{width:auto;margin:3px 0 0;flex-shrink:0}" +
      ".bcc-pf-form{margin-top:14px}" +
      ".bcc-pf-form label{display:block;margin:0 0 6px;font-size:.8rem;font-weight:700;color:#9fb0cc}" +
      ".bcc-pf-form textarea,.bcc-pf-form input[type=email]{width:100%;box-sizing:border-box;margin:0 0 12px;padding:10px 12px;" +
      "border-radius:8px;border:1px solid #2d3b5a;background:#0f1729;color:#e6edf3;font:inherit}" +
      ".bcc-pf-form textarea{min-height:96px;resize:vertical}" +
      ".bcc-pf-btn{padding:9px 16px;border-radius:10px;border:1px solid #4f84d8;background:#2f66bf;color:#f4f7ff;font:inherit;font-weight:800;cursor:pointer}" +
      ".bcc-pf-btn:hover{filter:brightness(1.08)}" +
      ".bcc-pf-btn:disabled{opacity:.55;cursor:not-allowed}" +
      ".bcc-pf-status{margin:10px 0 0;font-size:.85rem}" +
      ".bcc-pf-status.err{color:#f07178}.bcc-pf-status.ok{color:#3dd68c}" +
      ".bcc-pf-hp{position:absolute;left:-9999px;width:1px;height:1px;opacity:0;pointer-events:none}" +
      ".bcc-pf-thanks{margin:0;color:#3dd68c;font-weight:700}";
    document.head.appendChild(style);
  }

  function alreadySubmitted() {
    try {
      return sessionStorage.getItem(STORAGE_PREFIX + location.pathname) === "1";
    } catch (e) {
      return false;
    }
  }

  function markSubmitted() {
    try {
      sessionStorage.setItem(STORAGE_PREFIX + location.pathname, "1");
    } catch (e) {}
  }

  function normalizeEmail(raw) {
    var s = String(raw || "").trim().toLowerCase();
    if (!s) return "";
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s)) return "";
    return s.slice(0, 254);
  }

  function createWidget() {
    injectStyles();
    if (document.getElementById(ROOT_ID)) return document.getElementById(ROOT_ID);

    var root = document.createElement("section");
    root.id = ROOT_ID;
    root.className = "bcc-page-feedback";
    root.setAttribute("aria-label", "Page feedback");

    if (alreadySubmitted()) {
      root.innerHTML =
        "<h3>Page feedback</h3><p class=\"bcc-pf-thanks\">Thanks — your feedback was received.</p>";
      document.body.appendChild(root);
      return root;
    }

    root.innerHTML =
      "<h3>Page feedback</h3>" +
      '<label class="bcc-pf-toggle"><input type="checkbox" id="bccPfEnable" />' +
      "<span>I have feedback about this page</span></label>" +
      '<div class="bcc-pf-form" id="bccPfForm" hidden>' +
      '<label for="bccPfComment">Comment</label>' +
      '<textarea id="bccPfComment" maxlength="2000" placeholder="What is wrong, unclear, or needs fixing on this page?"></textarea>' +
      '<label for="bccPfEmail">Email <span style="font-weight:400">(optional — only if you want a reply)</span></label>' +
      '<input id="bccPfEmail" type="email" autocomplete="email" maxlength="254" />' +
      '<input class="bcc-pf-hp" type="text" name="company_website" tabindex="-1" autocomplete="off" aria-hidden="true" />' +
      '<button type="button" class="bcc-pf-btn" id="bccPfSubmit">Send feedback</button>' +
      '<p id="bccPfStatus" class="bcc-pf-status" aria-live="polite"></p>' +
      "</div>";

    document.body.appendChild(root);

    var enable = root.querySelector("#bccPfEnable");
    var form = root.querySelector("#bccPfForm");
    var submitBtn = root.querySelector("#bccPfSubmit");
    var status = root.querySelector("#bccPfStatus");

    enable.addEventListener("change", function () {
      form.hidden = !enable.checked;
      if (status) {
        status.textContent = "";
        status.className = "bcc-pf-status";
      }
    });

    submitBtn.addEventListener("click", function () {
      if (!enable.checked) {
        if (status) {
          status.textContent = "Check the box above to send feedback.";
          status.className = "bcc-pf-status err";
        }
        return;
      }

      var commentEl = root.querySelector("#bccPfComment");
      var emailEl = root.querySelector("#bccPfEmail");
      var hp = root.querySelector(".bcc-pf-hp");
      var comment = commentEl ? String(commentEl.value || "").trim() : "";
      var email = emailEl ? normalizeEmail(emailEl.value) : "";
      if (emailEl && emailEl.value.trim() && !email) {
        if (status) {
          status.textContent = "Enter a valid email or leave it blank.";
          status.className = "bcc-pf-status err";
        }
        return;
      }

      submitBtn.disabled = true;
      if (status) {
        status.textContent = "Sending…";
        status.className = "bcc-pf-status";
      }

      fetch("/api/sample-lead", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          action: "submit_page_feedback",
          product: detectProduct(),
          content_type: detectContentType(),
          page_path: location.pathname || "",
          page_title: (document.title || "").trim(),
          comment: comment,
          email: email,
          company_website: hp ? hp.value : "",
        }),
      })
        .then(function (r) {
          return r.json().then(function (j) {
            return { ok: r.ok, body: j };
          });
        })
        .then(function (res) {
          if (!res.ok || !res.body || res.body.ok === false) {
            var msg =
              (res.body && (res.body.error || res.body.reason)) || "Could not send feedback. Try again.";
            if (status) {
              status.textContent = msg;
              status.className = "bcc-pf-status err";
            }
            submitBtn.disabled = false;
            return;
          }
          markSubmitted();
          root.innerHTML =
            "<h3>Page feedback</h3><p class=\"bcc-pf-thanks\">Thanks — your feedback was received.</p>";
        })
        .catch(function () {
          if (status) {
            status.textContent = "Network error. Try again.";
            status.className = "bcc-pf-status err";
          }
          submitBtn.disabled = false;
        });
    });

    return root;
  }

  function ensureWidget() {
    if (window.bccPageFeedbackMounted) return;
    window.bccPageFeedbackMounted = true;
    createWidget();
  }

  window.bccEnsurePageFeedback = ensureWidget;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", ensureWidget);
  } else {
    ensureWidget();
  }
})();

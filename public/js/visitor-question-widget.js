/**
 * Footer "Ask a question" modal — posts to /api/sample-lead (action submit_question).
 */
(function () {
  "use strict";

  var STYLE_ID = "bcc-visitor-question-style";

  function detectProduct() {
    var p = (location.pathname || "").toLowerCase();
    if (p.indexOf("comptia-sec") !== -1 || p.indexOf("/comp_tia_sec+/") !== -1) return "secplus";
    if (p.indexOf("ccnp-encor") !== -1 || p.indexOf("/ccnp-encor-study/") !== -1) return "encor";
    if (p.indexOf("ccna") !== -1 || p.indexOf("/ccna-study/") !== -1) return "ccna";
    return "general";
  }

  function injectStyles() {
    if (document.getElementById(STYLE_ID)) return;
    var style = document.createElement("style");
    style.id = STYLE_ID;
    style.textContent =
      ".bcc-vq-backdrop{position:fixed;inset:0;z-index:10050;background:rgba(8,14,28,.72);backdrop-filter:blur(4px)}" +
      ".bcc-vq-panel{position:fixed;z-index:10051;left:50%;top:50%;transform:translate(-50%,-50%);width:min(92vw,440px);max-height:min(88vh,560px);overflow:auto;" +
      "background:#121a2b;border:1px solid #2d3b5a;border-radius:14px;padding:22px 20px;color:#e6edf3;box-shadow:0 18px 48px rgba(0,0,0,.45)}" +
      ".bcc-vq-panel h2{margin:0 0 6px;font-size:1.15rem;font-weight:800}" +
      ".bcc-vq-lead{margin:0 0 16px;font-size:.88rem;line-height:1.5;color:#9fb0cc}" +
      ".bcc-vq-panel label{display:block;margin:0 0 6px;font-size:.82rem;font-weight:700;color:#9fb0cc}" +
      ".bcc-vq-panel input,.bcc-vq-panel textarea{width:100%;box-sizing:border-box;margin:0 0 14px;padding:10px 12px;border-radius:8px;border:1px solid #2d3b5a;background:#0f1729;color:#e6edf3;font:inherit}" +
      ".bcc-vq-panel textarea{min-height:120px;resize:vertical}" +
      ".bcc-vq-actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:4px}" +
      ".bcc-vq-btn{padding:10px 16px;border-radius:10px;border:1px solid #4f84d8;background:#2f66bf;color:#f4f7ff;font:inherit;font-weight:800;cursor:pointer}" +
      ".bcc-vq-btn:hover{filter:brightness(1.08)}" +
      ".bcc-vq-btn.secondary{background:transparent;border-color:#2d3b5a;color:#c5d4f0}" +
      ".bcc-vq-status{margin:12px 0 0;font-size:.88rem;line-height:1.45}" +
      ".bcc-vq-status.err{color:#f07178}.bcc-vq-status.ok{color:#3dd68c}" +
      ".bcc-vq-hp{position:absolute;left:-9999px;width:1px;height:1px;opacity:0;pointer-events:none}";
    document.head.appendChild(style);
  }

  function createModal() {
    injectStyles();
    var root = document.createElement("div");
    root.id = "bccVisitorQuestionRoot";
    root.hidden = true;
    root.innerHTML =
      '<div class="bcc-vq-backdrop" data-bcc-vq-dismiss tabindex="-1"></div>' +
      '<div class="bcc-vq-panel" role="dialog" aria-modal="true" aria-labelledby="bccVqTitle" tabindex="-1">' +
      '<h2 id="bccVqTitle">Ask a question</h2>' +
      '<p class="bcc-vq-lead">Send a message about exam prep, access, or the practice site. We review questions in the admin dashboard — no email client needed.</p>' +
      '<form id="bccVqForm">' +
      '<label for="bccVqEmail">Your email</label>' +
      '<input id="bccVqEmail" name="email" type="email" autocomplete="email" required maxlength="254" />' +
      '<label for="bccVqMessage">Your question</label>' +
      '<textarea id="bccVqMessage" name="message" required minlength="10" maxlength="2000" placeholder="What can we help with?"></textarea>' +
      '<input class="bcc-vq-hp" type="text" name="company_website" tabindex="-1" autocomplete="off" aria-hidden="true" />' +
      '<div class="bcc-vq-actions">' +
      '<button type="submit" class="bcc-vq-btn">Send question</button>' +
      '<button type="button" class="bcc-vq-btn secondary" data-bcc-vq-dismiss>Cancel</button>' +
      "</div>" +
      '<p id="bccVqStatus" class="bcc-vq-status" aria-live="polite"></p>' +
      "</form></div>";
    document.body.appendChild(root);
    return root;
  }

  function openModal(root) {
    root.hidden = false;
    document.body.style.overflow = "hidden";
    var panel = root.querySelector(".bcc-vq-panel");
    var status = root.querySelector("#bccVqStatus");
    if (status) {
      status.textContent = "";
      status.className = "bcc-vq-status";
    }
    var form = root.querySelector("#bccVqForm");
    if (form) form.reset();
    if (panel) panel.focus();
  }

  function closeModal(root) {
    root.hidden = true;
    document.body.style.overflow = "";
  }

  function bindModal(root) {
    root.querySelectorAll("[data-bcc-vq-dismiss]").forEach(function (el) {
      el.addEventListener("click", function () {
        closeModal(root);
      });
    });

    var form = root.querySelector("#bccVqForm");
    if (!form) return;

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var status = root.querySelector("#bccVqStatus");
      var emailEl = root.querySelector("#bccVqEmail");
      var msgEl = root.querySelector("#bccVqMessage");
      var hp = form.querySelector('[name="company_website"]');
      var email = emailEl ? emailEl.value.trim() : "";
      var message = msgEl ? msgEl.value.trim() : "";

      if (status) {
        status.textContent = "Sending…";
        status.className = "bcc-vq-status";
      }

      fetch("/api/sample-lead", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          action: "submit_question",
          email: email,
          message: message,
          product: detectProduct(),
          page_path: location.pathname + (location.search || ""),
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
            var err =
              (res.body && (res.body.error || res.body.reason)) || "Could not send your question.";
            if (res.body && res.body.hint) err += " " + res.body.hint;
            throw new Error(err);
          }
          if (status) {
            status.textContent =
              "Thanks — your question was submitted. We will follow up at the email you provided.";
            status.className = "bcc-vq-status ok";
          }
          setTimeout(function () {
            closeModal(root);
          }, 2200);
        })
        .catch(function (err) {
          if (status) {
            status.textContent = err.message || "Something went wrong. Try again in a moment.";
            status.className = "bcc-vq-status err";
          }
        });
    });
  }

  function wireFooterLinks(root) {
    document.querySelectorAll("a.footer-mailto").forEach(function (link) {
      link.setAttribute("href", "#ask");
      link.setAttribute("role", "button");
      link.addEventListener("click", function (e) {
        e.preventDefault();
        openModal(root);
      });
    });
  }

  function init() {
    var root = document.getElementById("bccVisitorQuestionRoot") || createModal();
    bindModal(root);
    wireFooterLinks(root);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

/**
 * Shared deep-dive popup modal for Security+ PBQ labs and published simulations.
 */
(function () {
  "use strict";

  var modal = null;
  var titleEl = null;
  var bodyEl = null;
  var closeBtn = null;
  var returnFocusEl = null;

  function ensureModal() {
    if (modal) return modal;
    modal = document.getElementById("secplusDeepDiveModal");
    if (modal) {
      titleEl = document.getElementById("secplusDeepDiveTitle");
      bodyEl = document.getElementById("secplusDeepDiveBody");
      closeBtn = document.getElementById("secplusDeepDiveClose");
      return modal;
    }

    modal = document.createElement("div");
    modal.id = "secplusDeepDiveModal";
    modal.className = "secplus-deep-dive-modal";
    modal.setAttribute("role", "dialog");
    modal.setAttribute("aria-modal", "true");
    modal.setAttribute("aria-labelledby", "secplusDeepDiveTitle");
    modal.setAttribute("hidden", "");
    modal.innerHTML =
      '<div class="secplus-deep-dive-modal__panel">' +
      '<div class="secplus-deep-dive-modal__head">' +
      '<h2 class="secplus-deep-dive-modal__title" id="secplusDeepDiveTitle">Deep dive</h2>' +
      '<button type="button" class="secplus-deep-dive-modal__close" id="secplusDeepDiveClose">Close</button>' +
      "</div>" +
      '<div class="secplus-deep-dive-modal__body" id="secplusDeepDiveBody"></div>' +
      "</div>";

    document.body.appendChild(modal);
    titleEl = document.getElementById("secplusDeepDiveTitle");
    bodyEl = document.getElementById("secplusDeepDiveBody");
    closeBtn = document.getElementById("secplusDeepDiveClose");

    closeBtn.addEventListener("click", close);
    modal.addEventListener("click", function (ev) {
      if (ev.target === modal) close();
    });
    modal.querySelector(".secplus-deep-dive-modal__panel").addEventListener("click", function (ev) {
      ev.stopPropagation();
    });

    if (!document.documentElement.dataset.secplusDeepDiveEsc) {
      document.documentElement.dataset.secplusDeepDiveEsc = "1";
      document.addEventListener("keydown", function (ev) {
        if (ev.key === "Escape" && modal.classList.contains("open")) close();
      });
    }

    return modal;
  }

  function open(opts) {
    if (!opts || !opts.html) return false;
    ensureModal();
    returnFocusEl = opts.returnFocus || null;
    titleEl.textContent = opts.title || "Deep dive";
    bodyEl.innerHTML = opts.html;
    modal.removeAttribute("hidden");
    modal.classList.add("open");
    document.body.classList.add("secplus-deep-dive-open");
    closeBtn.focus();
    return true;
  }

  function close() {
    if (!modal) return;
    modal.classList.remove("open");
    modal.setAttribute("hidden", "");
    if (bodyEl) bodyEl.innerHTML = "";
    document.body.classList.remove("secplus-deep-dive-open");
    if (returnFocusEl && typeof returnFocusEl.focus === "function") {
      returnFocusEl.focus();
    }
    returnFocusEl = null;
  }

  window.SecplusDeepDiveModal = {
    open: open,
    close: close,
  };
})();

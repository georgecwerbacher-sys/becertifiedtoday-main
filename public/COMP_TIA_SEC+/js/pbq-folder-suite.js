/**
 * PBQ Production suite — folder sidebar, section panels, exhibit modals.
 */
(function () {
  var modal = null;
  var modalTitle = null;
  var modalBody = null;

  function ensureModal() {
    if (modal) return modal;
    modal = document.getElementById("pbqExhibitModal");
    if (modal) {
      modalTitle = document.getElementById("pbqExhibitModalTitle");
      modalBody = document.getElementById("pbqExhibitModalBody");
      return modal;
    }
    modal = document.createElement("div");
    modal.id = "pbqExhibitModal";
    modal.className = "pbq-exhibit-modal";
    modal.setAttribute("role", "dialog");
    modal.setAttribute("aria-modal", "true");
    modal.setAttribute("aria-labelledby", "pbqExhibitModalTitle");
    modal.hidden = true;
    modal.innerHTML =
      '<div class="pbq-exhibit-modal__backdrop" data-pbq-modal-close></div>' +
      '<div class="pbq-exhibit-modal__panel">' +
      '<div class="pbq-exhibit-modal__head">' +
      '<h2 class="pbq-exhibit-modal__title" id="pbqExhibitModalTitle">Exhibit</h2>' +
      '<button type="button" class="pbq-exhibit-modal__close" data-pbq-modal-close aria-label="Close">×</button>' +
      "</div>" +
      '<div class="pbq-exhibit-modal__body" id="pbqExhibitModalBody"></div>' +
      "</div>";
    document.body.appendChild(modal);
    modalTitle = document.getElementById("pbqExhibitModalTitle");
    modalBody = document.getElementById("pbqExhibitModalBody");
    modal.querySelectorAll("[data-pbq-modal-close]").forEach(function (el) {
      el.addEventListener("click", closeModal);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && modal && !modal.hidden) closeModal();
    });
    return modal;
  }

  function resolveExhibitTarget(sel) {
    if (!sel || sel.charAt(0) !== "#") return null;
    var id = sel.slice(1);
    return (
      document.querySelector(sel) ||
      document.querySelector('[id="' + id + '"]') ||
      document.querySelector('[id$="-' + id + '"]')
    );
  }

  function openModal(target) {
    if (!target) return;
    ensureModal();
    var title =
      target.querySelector(".pbq-ai-exhibit__banner, .pbq-exhibit__banner, h2, legend") ||
      target;
    modalTitle.textContent =
      (title.textContent || "Exhibit").trim().slice(0, 120) || "Exhibit";
    modalBody.innerHTML = "";
    var clone = target.cloneNode(true);
    clone.removeAttribute("id");
    clone.hidden = false;
    clone.style.display = "";
    modalBody.appendChild(clone);
    modal.hidden = false;
    modal.classList.add("is-open");
    document.body.classList.add("pbq-modal-open");
    modal.querySelector(".pbq-exhibit-modal__close").focus();
  }

  function closeModal() {
    if (!modal) return;
    modal.hidden = true;
    modal.classList.remove("is-open");
    document.body.classList.remove("pbq-modal-open");
    if (modalBody) modalBody.innerHTML = "";
  }

  function bindModalTriggers(root) {
    root.querySelectorAll("[data-pbq-modal]").forEach(function (btn) {
      if (btn.dataset.pbqModalBound) return;
      btn.dataset.pbqModalBound = "1";
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        var sel = btn.getAttribute("data-pbq-modal");
        var target = sel ? resolveExhibitTarget(sel) : null;
        if (target) openModal(target);
      });
    });
    root.querySelectorAll('a[href^="#exhibit-"], a[href^="#zt-"]').forEach(function (a) {
      if (a.dataset.pbqModalBound) return;
      var href = a.getAttribute("href");
      if (!href || href.length < 2) return;
      var target = resolveExhibitTarget(href);
      if (!target || !target.matches("figure, .pbq-exhibit, .pbq-ai-exhibit")) return;
      a.dataset.pbqModalBound = "1";
      a.addEventListener("click", function (e) {
        e.preventDefault();
        openModal(target);
      });
    });
  }

  function setActiveSection(sectionId) {
    document.querySelectorAll(".pbq-suite-section").forEach(function (panel) {
      var on = panel.id === sectionId;
      panel.classList.toggle("is-active", on);
      panel.hidden = !on;
    });
    document.querySelectorAll(".pbq-suite-folder__item").forEach(function (btn) {
      var on = btn.getAttribute("data-section") === sectionId;
      btn.classList.toggle("is-active", on);
      btn.setAttribute("aria-current", on ? "true" : "false");
    });
    if (sectionId && history.replaceState) {
      history.replaceState(null, "", "#" + sectionId);
    }
    var panel = document.getElementById(sectionId);
    if (panel) bindModalTriggers(panel);
  }

  function markSectionProgress(sectionId) {
    var btn = document.querySelector('.pbq-suite-folder__item[data-section="' + sectionId + '"]');
    if (btn) btn.classList.add("is-complete");
  }

  function initSectionProgress() {
    document.querySelectorAll(".pbq-suite-section").forEach(function (panel) {
      var status = panel.querySelector('[role="status"]');
      if (!status) return;
      var observer = new MutationObserver(function () {
        if (status.classList.contains("is-pass")) markSectionProgress(panel.id);
      });
      observer.observe(status, { attributes: true, attributeFilter: ["class"] });
      if (status.classList.contains("is-pass")) markSectionProgress(panel.id);
    });
  }

  function initDrStickyMetrics() {
    if (!document.body.classList.contains("pbq-dr-ransomware")) return;
    var source = document.querySelector("#dr-overview .pbq-dr-metrics");
    var layout = document.querySelector(".pbq-suite-layout");
    if (!source || !layout || document.getElementById("pbqDrStickyMetrics")) return;
    var bar = source.cloneNode(true);
    bar.id = "pbqDrStickyMetrics";
    bar.classList.add("pbq-dr-metrics--sticky");
    bar.setAttribute("aria-label", "Scenario constraints (sticky)");
    layout.insertBefore(bar, layout.firstChild);
  }

  function initFolders() {
    document.querySelectorAll(".pbq-suite-folder__item").forEach(function (btn) {
      btn.addEventListener("click", function () {
        setActiveSection(btn.getAttribute("data-section"));
      });
    });
    var hash = (location.hash || "").replace(/^#/, "");
    var defaultId = window.PBQ_SUITE_DEFAULT_SECTION || "";
    var first =
      document.querySelector('.pbq-suite-folder__item[data-section="' + hash + '"]') ||
      document.querySelector('.pbq-suite-folder__item[data-section="' + defaultId + '"]') ||
      document.querySelector(".pbq-suite-folder__item");
    if (first) {
      setActiveSection(first.getAttribute("data-section"));
    } else if (defaultId && document.getElementById(defaultId)) {
      setActiveSection(defaultId);
    }
    window.addEventListener("hashchange", function () {
      var id = (location.hash || "").replace(/^#/, "");
      if (id && document.getElementById(id)) setActiveSection(id);
    });
    bindModalTriggers(document);
    initSectionProgress();
    initDrStickyMetrics();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initFolders);
  } else {
    initFolders();
  }
})();

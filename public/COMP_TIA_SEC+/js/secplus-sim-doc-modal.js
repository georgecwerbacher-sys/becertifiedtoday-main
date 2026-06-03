/**
 * Floating document viewer for Security+ dark-web IR simulation.
 * Used by guest samples, training portal, and timed exam iframe embeds.
 */
(function () {
  "use strict";

  var MIN_W = 300;
  var MIN_H = 220;

  function simDocumentBaseHref() {
    try {
      var path = (location.pathname || "").toLowerCase();
      if (path === "/secplus-sample" || path === "/secplus-sample/") {
        var remembered = sessionStorage.getItem("ccnaLastRealPath");
        if (remembered) {
          return new URL(remembered, window.location.origin).href;
        }
      }
    } catch (e) {}
    return window.location.href;
  }

  function resolveSimDocUrl(relativePath) {
    if (!relativePath) return relativePath;
    if (relativePath.charAt(0) === "/") {
      try {
        return new URL(relativePath, window.location.origin).href;
      } catch (e) {
        return relativePath;
      }
    }
    try {
      return new URL(relativePath, simDocumentBaseHref()).href;
    } catch (e) {
      return relativePath;
    }
  }

  function bootPortalSimChrome() {
    try {
      if (sessionStorage.getItem("secplusHomeSample")) {
        document.body.classList.add("secplus-home-sample-sim");
        return;
      }
      document.body.classList.add("secplus-portal-sim");
    } catch (e) {}

    try {
      if (new URLSearchParams(location.search).get("examSim") === "1") {
        document.body.classList.add("secplus-exam-sim-embed");
      }
    } catch (e) {}
  }

  function initSecplusSimDocModal(config) {
    config = config || {};
    var docContent = config.docContent || {};
    var artifactSelector = config.artifactSelector || ".artifact[data-doc]";

    var docModal = document.getElementById("docModal");
    var docModalTitle = document.getElementById("docModalTitle");
    var docModalBody = document.getElementById("docModalBody");
    var docModalClose = document.getElementById("docModalClose");
    var docModalPanel = document.getElementById("docModalPanel");
    var docModalHead = document.getElementById("docModalHead");
    var docModalResize = document.getElementById("docModalResize");

    if (!docModal || !docModalPanel || !docModalBody) return null;
    if (docModal.dataset.docModalReady === "1") {
      return { openDoc: docModal._secplusOpenDoc, closeDoc: docModal._secplusCloseDoc };
    }
    docModal.dataset.docModalReady = "1";

    var docModalTrigger = null;
    var docModalDragged = false;
    var docModalResized = false;

    function docModalMaxSize() {
      return {
        w: Math.max(MIN_W, window.innerWidth - 16),
        h: Math.max(MIN_H, window.innerHeight - 16),
      };
    }

    function clampDocModalSize(width, height) {
      var max = docModalMaxSize();
      return {
        w: Math.min(Math.max(width, MIN_W), max.w),
        h: Math.min(Math.max(height, MIN_H), max.h),
      };
    }

    function clampDocModalPos(left, top) {
      var rect = docModalPanel.getBoundingClientRect();
      var maxLeft = Math.max(8, window.innerWidth - rect.width - 8);
      var maxTop = Math.max(8, window.innerHeight - rect.height - 8);
      return {
        left: Math.min(Math.max(left, 8), maxLeft),
        top: Math.min(Math.max(top, 8), maxTop),
      };
    }

    function resetDocModalPosition() {
      docModalDragged = false;
      docModalResized = false;
      docModalPanel.style.left = "";
      docModalPanel.style.top = "";
      docModalPanel.style.width = "";
      docModalPanel.style.height = "";
      docModalPanel.style.margin = "";
      docModalPanel.style.transform = "";
      docModalPanel.classList.remove("is-dragging", "is-resizing", "doc-modal__panel--report");
      docModalPanel.dataset.dragged = "";
      docModalPanel.dataset.resized = "";
    }

    function syncDocModalBodyLayout(isReport) {
      docModalPanel.classList.toggle("doc-modal__panel--report", !!isReport);
    }

    function centerDocModalPanel() {
      if (docModalDragged) return;
      requestAnimationFrame(function () {
        if (docModalDragged || !docModal.classList.contains("open")) return;
        var w = docModalPanel.offsetWidth;
        var h = docModalPanel.offsetHeight;
        var pos = clampDocModalPos((window.innerWidth - w) / 2, (window.innerHeight - h) / 2);
        docModalPanel.style.margin = "0";
        docModalPanel.style.transform = "none";
        docModalPanel.style.left = pos.left + "px";
        docModalPanel.style.top = pos.top + "px";
      });
    }

    function showDocModal(doc, trigger) {
      docModal.removeAttribute("hidden");
      docModal.classList.add("open");
      centerDocModalPanel();
      if (docModalClose) docModalClose.focus();
      if (trigger) trigger.classList.add("reviewed");
    }

    function closeDoc() {
      docModal.setAttribute("hidden", "");
      docModal.classList.remove("open");
      resetDocModalPosition();
      docModalBody.innerHTML = "";
      docModalBody.classList.remove("doc-modal__body--report");
      if (docModalTrigger) {
        docModalTrigger.focus();
        docModalTrigger = null;
      }
    }

    function loadReportIntoModal(reportUrl, docTitle, trigger, reportRoot, reportLinkLabel) {
      var linkLabel = reportLinkLabel || "document";
      docModalBody.innerHTML = '<p class="doc-load-fallback">Loading document…</p>';
      docModalBody.classList.add("doc-modal__body--report");
      syncDocModalBodyLayout(true);
      showDocModal({ title: docTitle }, trigger);
      fetch(reportUrl)
        .then(function (res) {
          if (!res.ok) throw new Error("HTTP " + res.status);
          return res.text();
        })
        .then(function (html) {
          var parsed = new DOMParser().parseFromString(html, "text/html");
          var sheet =
            (reportRoot && parsed.getElementById(reportRoot)) || parsed.querySelector(".report-sheet");
          docModalBody.innerHTML = "";
          if (sheet) {
            docModalBody.appendChild(sheet.cloneNode(true));
            centerDocModalPanel();
          } else {
            throw new Error("Report content not found");
          }
        })
        .catch(function () {
          docModalBody.innerHTML =
            '<p class="doc-load-fallback">Could not load the document in this view. ' +
            '<a href="' +
            reportUrl +
            '" target="_blank" rel="noopener noreferrer">Open ' +
            linkLabel +
            "</a> in a new tab.</p>";
        });
    }

    function openDoc(key, trigger) {
      var doc = docContent[key];
      if (!doc) return;
      docModalTrigger = trigger || null;
      docModalTitle.textContent = doc.title;
      docModalBody.innerHTML = "";
      docModalBody.classList.remove("doc-modal__body--report");
      syncDocModalBodyLayout(!!doc.report);
      if (doc.report) {
        var reportUrl = resolveSimDocUrl(doc.report);
        if (window.location.protocol === "file:") {
          window.open(reportUrl, "_blank", "noopener,noreferrer");
          if (trigger) trigger.classList.add("reviewed");
          return;
        }
        loadReportIntoModal(reportUrl, doc.title, trigger, doc.reportRoot, doc.reportLinkLabel);
        return;
      }
      if (doc.html) {
        docModalBody.innerHTML = doc.html;
      }
      showDocModal(doc, trigger);
    }

    docModal._secplusOpenDoc = openDoc;
    docModal._secplusCloseDoc = closeDoc;

    function initDocModalDrag() {
      if (!docModalHead || docModalHead.dataset.dragReady === "1") return;
      docModalHead.dataset.dragReady = "1";

      var dragging = false;
      var pointerId = null;
      var startX = 0;
      var startY = 0;
      var originLeft = 0;
      var originTop = 0;
      var moved = false;

      function onDocumentMove(e) {
        if (!dragging || e.pointerId !== pointerId) return;
        if (Math.abs(e.clientX - startX) > 3 || Math.abs(e.clientY - startY) > 3) moved = true;
        var pos = clampDocModalPos(originLeft + (e.clientX - startX), originTop + (e.clientY - startY));
        docModalPanel.style.left = pos.left + "px";
        docModalPanel.style.top = pos.top + "px";
      }

      function endDrag(e) {
        if (!dragging || e.pointerId !== pointerId) return;
        dragging = false;
        docModalPanel.classList.remove("is-dragging");
        document.removeEventListener("pointermove", onDocumentMove);
        document.removeEventListener("pointerup", endDrag);
        document.removeEventListener("pointercancel", endDrag);
        try {
          docModalHead.releasePointerCapture(pointerId);
        } catch (err) {}
        if (moved) {
          docModalDragged = true;
          docModalPanel.dataset.dragged = "1";
        }
        pointerId = null;
      }

      docModalHead.addEventListener("pointerdown", function (e) {
        if (e.button !== 0 && e.pointerType !== "touch") return;
        if (e.target && e.target.closest(".doc-modal__close")) return;

        var rect = docModalPanel.getBoundingClientRect();
        dragging = true;
        moved = false;
        pointerId = e.pointerId;
        startX = e.clientX;
        startY = e.clientY;
        originLeft = rect.left;
        originTop = rect.top;

        docModalPanel.style.margin = "0";
        docModalPanel.style.transform = "none";
        docModalPanel.style.left = originLeft + "px";
        docModalPanel.style.top = originTop + "px";
        docModalPanel.classList.add("is-dragging");

        document.addEventListener("pointermove", onDocumentMove);
        document.addEventListener("pointerup", endDrag);
        document.addEventListener("pointercancel", endDrag);

        try {
          docModalHead.setPointerCapture(e.pointerId);
        } catch (err) {}
        e.preventDefault();
      });
    }

    function initDocModalResize() {
      if (!docModalResize || docModalResize.dataset.resizeReady === "1") return;
      docModalResize.dataset.resizeReady = "1";

      var resizing = false;
      var pointerId = null;
      var startX = 0;
      var startY = 0;
      var originW = 0;
      var originH = 0;
      var originLeft = 0;
      var originTop = 0;
      var moved = false;

      function onResizeMove(e) {
        if (!resizing || e.pointerId !== pointerId) return;
        if (Math.abs(e.clientX - startX) > 3 || Math.abs(e.clientY - startY) > 3) moved = true;
        var size = clampDocModalSize(originW + (e.clientX - startX), originH + (e.clientY - startY));
        docModalPanel.style.width = size.w + "px";
        docModalPanel.style.height = size.h + "px";
        var pos = clampDocModalPos(originLeft, originTop);
        docModalPanel.style.left = pos.left + "px";
        docModalPanel.style.top = pos.top + "px";
      }

      function endResize(e) {
        if (!resizing || e.pointerId !== pointerId) return;
        resizing = false;
        docModalPanel.classList.remove("is-resizing");
        document.removeEventListener("pointermove", onResizeMove);
        document.removeEventListener("pointerup", endResize);
        document.removeEventListener("pointercancel", endResize);
        try {
          docModalResize.releasePointerCapture(pointerId);
        } catch (err) {}
        if (moved) {
          docModalResized = true;
          docModalPanel.dataset.resized = "1";
        }
        pointerId = null;
      }

      docModalResize.addEventListener("pointerdown", function (e) {
        if (e.button !== 0 && e.pointerType !== "touch") return;

        var rect = docModalPanel.getBoundingClientRect();
        resizing = true;
        moved = false;
        pointerId = e.pointerId;
        startX = e.clientX;
        startY = e.clientY;
        originW = rect.width;
        originH = rect.height;
        originLeft = rect.left;
        originTop = rect.top;

        docModalPanel.style.width = originW + "px";
        docModalPanel.style.height = originH + "px";
        docModalPanel.style.left = originLeft + "px";
        docModalPanel.style.top = originTop + "px";
        docModalPanel.classList.add("is-resizing");

        document.addEventListener("pointermove", onResizeMove);
        document.addEventListener("pointerup", endResize);
        document.addEventListener("pointercancel", endResize);

        try {
          docModalResize.setPointerCapture(e.pointerId);
        } catch (err) {}
        e.preventDefault();
        e.stopPropagation();
      });
    }

    document.querySelectorAll(artifactSelector).forEach(function (btn) {
      btn.addEventListener("click", function () {
        openDoc(btn.getAttribute("data-doc"), btn);
      });
    });

    initDocModalDrag();
    initDocModalResize();

    if (docModalClose) docModalClose.addEventListener("click", closeDoc);

    window.addEventListener("resize", function () {
      if (!docModal.classList.contains("open")) return;
      if (docModalResized) {
        var w = parseFloat(docModalPanel.style.width);
        var h = parseFloat(docModalPanel.style.height);
        if (Number.isFinite(w) && Number.isFinite(h)) {
          var size = clampDocModalSize(w, h);
          docModalPanel.style.width = size.w + "px";
          docModalPanel.style.height = size.h + "px";
        }
      }
      var left = parseFloat(docModalPanel.style.left);
      var top = parseFloat(docModalPanel.style.top);
      if (!Number.isFinite(left) || !Number.isFinite(top)) {
        centerDocModalPanel();
        return;
      }
      var pos = clampDocModalPos(left, top);
      docModalPanel.style.left = pos.left + "px";
      docModalPanel.style.top = pos.top + "px";
    });

    document.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape" && docModal.classList.contains("open")) closeDoc();
    });

    bootPortalSimChrome();

    return { openDoc: openDoc, closeDoc: closeDoc };
  }

  window.initSecplusSimDocModal = initSecplusSimDocModal;
  window.bootSecplusPortalSimChrome = bootPortalSimChrome;
})();

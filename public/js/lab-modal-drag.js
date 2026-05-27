(function () {
  var modalStackZ = 25000;

  function clamp(value, min, max) {
    return Math.min(Math.max(value, min), max);
  }

  function positionWithinViewport(dialog, left, top) {
    var rect = dialog.getBoundingClientRect();
    var maxLeft = Math.max(8, window.innerWidth - rect.width - 8);
    var maxTop = Math.max(8, window.innerHeight - rect.height - 8);
    return {
      left: clamp(left, 8, maxLeft),
      top: clamp(top, 8, maxTop),
    };
  }

  function bumpOverlayZ(overlay) {
    if (!overlay) return;
    modalStackZ += 1;
    overlay.style.zIndex = String(modalStackZ);
  }

  function isInteractiveControl(target) {
    return !!(target && target.closest && target.closest(
      "button, input, textarea, select, label, a[href], .cli-modal-close"
    ));
  }

  function makeDialogDraggable(dialog) {
    if (!dialog || dialog.dataset.dragReady === "1") return;
    var header = dialog.querySelector(".cli-modal-header");
    if (!header) return;
    var overlay = dialog.closest(".cli-modal-overlay");

    dialog.dataset.dragReady = "1";
    header.style.cursor = "move";
    header.style.touchAction = "none";

    var dragging = false;
    var pointerId = null;
    var startX = 0;
    var startY = 0;
    var originLeft = 0;
    var originTop = 0;

    dialog.addEventListener("pointerdown", function (e) {
      if (isInteractiveControl(e.target)) return;
      bumpOverlayZ(overlay);
    });

    function onDocumentMove(e) {
      if (!dragging || e.pointerId !== pointerId) return;
      var pos = positionWithinViewport(
        dialog,
        originLeft + (e.clientX - startX),
        originTop + (e.clientY - startY)
      );
      dialog.style.left = pos.left + "px";
      dialog.style.top = pos.top + "px";
    }

    function endDrag(e) {
      if (!dragging || e.pointerId !== pointerId) return;
      dragging = false;
      dialog.classList.remove("is-dragging");
      document.removeEventListener("pointermove", onDocumentMove);
      document.removeEventListener("pointerup", endDrag);
      document.removeEventListener("pointercancel", endDrag);
      try {
        header.releasePointerCapture(pointerId);
      } catch (err) {}
      pointerId = null;
    }

    header.addEventListener("pointerdown", function (e) {
      if (e.button !== 0 && e.pointerType !== "touch") return;
      if (e.target && e.target.closest(".cli-modal-close")) return;

      var rect = dialog.getBoundingClientRect();
      dragging = true;
      pointerId = e.pointerId;
      startX = e.clientX;
      startY = e.clientY;
      originLeft = rect.left;
      originTop = rect.top;

      dialog.style.transform = "none";
      dialog.style.margin = "0";
      dialog.style.left = originLeft + "px";
      dialog.style.top = originTop + "px";
      dialog.classList.add("is-dragging");
      dialog.dataset.dragged = "1";
      bumpOverlayZ(overlay);

      document.addEventListener("pointermove", onDocumentMove);
      document.addEventListener("pointerup", endDrag);
      document.addEventListener("pointercancel", endDrag);

      try {
        header.setPointerCapture(e.pointerId);
      } catch (err) {}
      e.preventDefault();
    });
  }

  var historyByInput = new WeakMap();

  function getHistoryState(input) {
    var state = historyByInput.get(input);
    if (state) return state;
    state = { entries: [], idx: 0 };
    historyByInput.set(input, state);
    return state;
  }

  function pushHistory(input, value) {
    var cmd = String(value || "").trim();
    if (!cmd) return;
    var state = getHistoryState(input);
    if (!state.entries.length || state.entries[state.entries.length - 1] !== cmd) {
      state.entries.push(cmd);
    }
    state.idx = state.entries.length;
  }

  function bindInputHistory(input) {
    if (!input || input.dataset.historyReady === "1") return;
    input.dataset.historyReady = "1";

    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        var raw = input.value || "";
        var cmd = raw.trim().toLowerCase().replace(/\s+/g, " ");
        var isSilentExit = cmd === "exit";
        var rowNow = input.closest(".input-row");
        var promptElNow =
          rowNow &&
          rowNow.querySelector(".prompt-el, .prompt, #prompt, [id^='prompt']");
        var promptSnapshot = promptElNow ? (promptElNow.textContent || "").trim() : "";
        pushHistory(input, raw);
        setTimeout(function () {
          var row = input.closest(".input-row");
          var promptEl =
            row && row.querySelector(".prompt-el, .prompt, #prompt, [id^='prompt']");
          if (promptEl) {
            var txt = promptSnapshot || (promptEl.textContent || "").trim();
            var execMatch = txt.match(/^([A-Za-z0-9._-]+)#$/);
            var cfgMatch = txt.match(/^([A-Za-z0-9._-]+)\(([^)]+)\)#$/);

            if ((cmd === "conf t" || cmd === "configure terminal") && execMatch) {
              promptEl.textContent = execMatch[1] + "(config)#";
            } else if (cmd === "end" && cfgMatch) {
              promptEl.textContent = cfgMatch[1] + "#";
            } else if (cmd === "exit" && cfgMatch) {
              var host = cfgMatch[1];
              var mode = cfgMatch[2];
              if (mode === "config") {
                promptEl.textContent = host + "#";
              } else {
                promptEl.textContent = host + "(config)#";
              }
            }
          }
          if (isSilentExit) {
            var terminal = input.closest(".terminal");
            var scroll =
              terminal &&
              terminal.querySelector(
                ".scrollback-area, #scrollback, .console-scroll, [id^='scroll']"
              );
            if (scroll && scroll.lastElementChild) {
              var last = scroll.lastElementChild;
              var txt = (last.textContent || "").trim().toLowerCase();
              if (last.classList.contains("line-user") && /\bexit$/.test(txt)) {
                last.remove();
              }
            }
          }
          if (!document.contains(input)) return;
          if (input.disabled) return;
          input.focus();
        }, 0);
        return;
      }
      var usePrev = e.key === "ArrowUp" || (e.key === "Tab" && !e.shiftKey);
      var useNext = e.key === "ArrowDown" || (e.key === "Tab" && e.shiftKey);
      if (!usePrev && !useNext) return;
      var state = getHistoryState(input);
      if (!state.entries.length) return;
      e.preventDefault();
      if (usePrev) {
        state.idx = Math.max(0, state.idx - 1);
      } else {
        state.idx = Math.min(state.entries.length, state.idx + 1);
      }
      input.value = state.idx >= state.entries.length ? "" : state.entries[state.idx];
    }, true);
  }

  function bindAllInputs() {
    document
      .querySelectorAll(
        'input.cmdline-input, .terminal input[type="text"], input.cmdline, #cmdline, #cmdlineR2, #cmdlineR3, [id^="cmd"], [id$="Cmdline"]'
      )
      .forEach(bindInputHistory);
  }

  function init() {
    document.querySelectorAll(".cli-modal-dialog").forEach(makeDialogDraggable);
    bindAllInputs();
  }

  window.bccInitLabModalDrag = init;
  window.bccWireFloatingModal = function (dialogEl, overlayEl) {
    if (dialogEl) makeDialogDraggable(dialogEl);
    if (overlayEl) bumpOverlayZ(overlayEl);
  };

  if (!window.__bccLabModalDragObserver) {
    window.__bccLabModalDragObserver = true;
    var observer = new MutationObserver(function (mutations) {
      mutations.forEach(function (mutation) {
        mutation.addedNodes.forEach(function (node) {
          if (!node || node.nodeType !== 1) return;
          if (node.classList && node.classList.contains("cli-modal-dialog")) {
            makeDialogDraggable(node);
          }
          if (node.querySelectorAll) {
            node.querySelectorAll(".cli-modal-dialog").forEach(makeDialogDraggable);
            node.querySelectorAll(
              'input.cmdline-input, .terminal input[type="text"], input.cmdline, #cmdline, [id^="cmd"], [id$="Cmdline"]'
            ).forEach(bindInputHistory);
          }
        });
      });
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

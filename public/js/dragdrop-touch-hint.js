(function () {
  "use strict";

  var HINT_TEXT = "Phone or tablet: tap an option, then tap a placement area.";

  function findDropRoot(scope) {
    var layout = scope.querySelector(".layout");
    if (layout) return layout;

    var slot = scope.querySelector(".drop-slot");
    if (!slot) return null;

    return (
      slot.closest(".category-stack") ||
      slot.closest(".match-list") ||
      slot.closest("pre") ||
      slot.closest(".panel") ||
      slot.parentElement
    );
  }

  function injectDragdropTouchHint() {
    var main = document.querySelector("main.card") || document.querySelector("main");
    if (!main) return;
    if (main.querySelector(".dragdrop-touch-hint")) return;
    if (!main.querySelector(".drop-slot")) return;
    if (!main.querySelector('.token[draggable="true"]')) return;

    var root = findDropRoot(main);
    if (!root || !root.parentNode) return;

    var hint = document.createElement("p");
    hint.className = "dragdrop-touch-hint";
    hint.textContent = HINT_TEXT;
    root.parentNode.insertBefore(hint, root);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", injectDragdropTouchHint);
  } else {
    injectDragdropTouchHint();
  }
})();

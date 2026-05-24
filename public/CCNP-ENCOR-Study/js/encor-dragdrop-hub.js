(function () {
  "use strict";

  var STUDY_CFG_URL = "/CCNP-ENCOR-Study/js/study-config.json";
  var BEGIN_RANDOM = "/CCNP-ENCOR-Study/begin-questions-random.html";
  var BEGIN_REVIEW = "/CCNP-ENCOR-Study/begin-questions-review.html";

  function launch(sessionKind) {
    var base = sessionKind === "review" ? BEGIN_REVIEW : BEGIN_RANDOM;
    location.href = base + "?mode=dragdrop";
  }

  function updateBankMeta(cfg) {
    var ids = cfg.dragDropIds || [];
    var meta = document.querySelector("[data-encor-dnd-meta]");
    if (meta) {
      if (!ids.length) {
        meta.textContent = "No exercises in this bank yet.";
      } else {
        meta.textContent =
          ids.length +
          " standard drag-and-drop exercise" +
          (ids.length === 1 ? "" : "s") +
          " from " +
          (cfg.dragDropDirectory || "CCNP-ENCOR-Drag-Drop") +
          ". Random shuffles once at start; Review sends misses to the back of the queue.";
      }
    }
    document.querySelectorAll("[data-encor-dnd-mode]").forEach(function (btn) {
      if (!ids.length) {
        btn.disabled = true;
        btn.classList.add("is-placeholder");
      } else {
        btn.disabled = false;
        btn.classList.remove("is-placeholder");
      }
    });
  }

  document.addEventListener(
    "click",
    function (e) {
      var t = e.target;
      if (!t || typeof t.closest !== "function") return;
      var btn = t.closest("[data-encor-dnd-mode]");
      if (!btn || btn.disabled) return;
      var mode = btn.getAttribute("data-encor-dnd-mode");
      if (mode !== "random" && mode !== "review") return;
      e.preventDefault();
      launch(mode);
    },
    false
  );

  function bootstrap() {
    fetch(STUDY_CFG_URL, { cache: "no-store" })
      .then(function (r) {
        if (!r.ok) throw new Error("study config");
        return r.json();
      })
      .then(updateBankMeta)
      .catch(function () {
        var meta = document.querySelector("[data-encor-dnd-meta]");
        if (meta) {
          meta.textContent =
            "Could not load drag-and-drop bank. Refresh the page or try again later.";
        }
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bootstrap, { once: true });
  } else {
    bootstrap();
  }
})();

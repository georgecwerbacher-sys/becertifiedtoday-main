(function () {
  "use strict";

  var STUDY_CFG_URL = "/CCNP-ENCOR-Study/js/study-config.json";
  var SUBJECTS_URL = "/CCNP-ENCOR-Study/js/question-subjects.json";
  var OBJECTIVES_URL = "/CCNP-ENCOR-Study/data/encor-exam-objectives-350-401-v1.2.json";
  var QUESTION_HUB_DIR = "/CCNP-ENCOR-Study/ENCOR_Questions";
  var BEGIN_RANDOM = "/CCNP-ENCOR-Study/begin-questions-random.html";
  var BEGIN_REVIEW = "/CCNP-ENCOR-Study/begin-questions-review.html";
  var BANK_SIZE = 100;
  var BANK_COUNT = 4;

  window.ENCOR_PRACTICE = window.ENCOR_PRACTICE || {};

  function filterIdsByDomain(ids, domain, subjects) {
    if (!domain || !subjects || !subjects.questions) return ids.slice();
    var want = String(domain);
    return ids.filter(function (id) {
      var entry = subjects.questions[String(id)];
      if (!entry) return false;
      var section = typeof entry === "string" ? entry : entry.section || "";
      return String(section).split(".")[0] === want;
    });
  }

  function getSelectedDomain() {
    var sel = document.getElementById("encor-practice-domain-select");
    if (!sel) return "";
    var v = String(sel.value || "").trim();
    return /^[1-6]$/.test(v) ? v : "";
  }

  function getAdaptiveEnabled() {
    try {
      var r = document.querySelector('input[name="encor-practice-adaptive"]:checked');
      if (!r) return false;
      return String(r.value || "").trim() === "1";
    } catch (e) {
      return false;
    }
  }

  function enablePortalControls() {
    var sel = document.getElementById("encor-practice-domain-select");
    if (sel) sel.disabled = false;
    document.querySelectorAll('input[name="encor-practice-adaptive"]').forEach(function (el) {
      el.disabled = false;
    });
  }

  function populateDomainSelect(objectives) {
    var sel = document.getElementById("encor-practice-domain-select");
    if (!sel || !objectives || !Array.isArray(objectives.domains)) return;
    var current = sel.value;
    while (sel.options.length > 1) sel.remove(1);
    objectives.domains.forEach(function (domain) {
      var opt = document.createElement("option");
      var major = String(domain.id || "").split(".")[0];
      opt.value = major;
      opt.textContent = domain.id + " — " + (domain.name || "");
      sel.appendChild(opt);
    });
    if (current) sel.value = current;
  }

  function bankIds(allIds, bankIndex) {
    var n = parseInt(String(bankIndex), 10);
    if (!n || n < 1) n = 1;
    var start = (n - 1) * BANK_SIZE;
    return (allIds || []).slice(start, start + BANK_SIZE);
  }

  function formatRange(first, last) {
    if (first >= last) return String(first);
    return String(first) + "–" + String(last);
  }

  function launchBank(mode, bankIndex) {
    var domain = getSelectedDomain();
    var cfg = window.ENCOR_PRACTICE._studyConfig;
    var subjects = window.ENCOR_PRACTICE._subjects;
    if (cfg && domain) {
      var ids = filterIdsByDomain(bankIds(cfg.allIds || [], bankIndex), domain, subjects);
      if (!ids.length) {
        window.alert(
          "No questions in this bank match the selected domain. Pick another subject or choose “All subjects”."
        );
        return;
      }
    }
    try {
      sessionStorage.setItem("encorPracticeAdaptive", getAdaptiveEnabled() ? "1" : "");
    } catch (e) {}
    var base = mode === "review" ? BEGIN_REVIEW : BEGIN_RANDOM;
    var url = base + "?bank=" + encodeURIComponent(String(bankIndex));
    if (domain) url += "&domain=" + encodeURIComponent(domain);
    location.href = url;
  }

  function updatePracticeBanks(cfg, subjects) {
    var grid = document.getElementById("encor-practice-banks-grid");
    if (!grid) return;

    var allIds = Array.isArray(cfg.allIds) ? cfg.allIds : [];
    var domain = getSelectedDomain();
    var totalFiltered = 0;

    for (var b = 1; b <= BANK_COUNT; b++) {
      var article = grid.querySelector('[data-encor-bank-index="' + b + '"]');
      if (!article) continue;

      var startIdx = (b - 1) * BANK_SIZE;
      var endIdx = Math.min(b * BANK_SIZE, allIds.length);
      var firstNum = startIdx + 1;
      var slotEnd = b * BANK_SIZE;
      var idsInBank = bankIds(allIds, b);
      var ids = filterIdsByDomain(idsInBank, domain, subjects);
      totalFiltered += ids.length;
      var countInBank = idsInBank.length;

      var isPartial = countInBank > 0 && countInBank < BANK_SIZE;
      var nextBankCount = b < BANK_COUNT ? bankIds(allIds, b + 1).length : 0;
      article.classList.toggle(
        "encor-practice-bank--remainder",
        isPartial && (b === BANK_COUNT || nextBankCount === 0)
      );

      var h4 = article.querySelector(".sim-box-title");
      if (h4) {
        var titleInner =
          countInBank === 0 ? formatRange(firstNum, slotEnd) : formatRange(firstNum, endIdx);
        h4.textContent = "Bank " + String(b) + " · questions " + titleInner;
      }

      var meta = article.querySelector("[data-encor-bank-meta]");
      if (meta) {
        if (countInBank === 0) {
          meta.textContent =
            "Reserved for questions " + formatRange(firstNum, slotEnd) + " when the hub list grows.";
        } else if (domain) {
          meta.textContent =
            ids.length +
            " question" +
            (ids.length === 1 ? "" : "s") +
            " in this bank match the selected domain (" +
            countInBank +
            " total in bank).";
        } else {
          meta.textContent =
            countInBank +
            " question" +
            (countInBank === 1 ? "" : "s") +
            " · use Random or Review for this bank only.";
        }
      }

      article.querySelectorAll("[data-encor-mode]").forEach(function (btn) {
        if (!ids.length) {
          btn.disabled = true;
          btn.classList.add("is-placeholder");
        } else {
          btn.disabled = false;
          btn.classList.remove("is-placeholder");
        }
      });
    }

    var summary = document.getElementById("encor-practice-banks-summary");
    if (summary) {
      var lastBankCount = allIds.length - (BANK_COUNT - 1) * BANK_SIZE;
      var summaryText =
        allIds.length +
        " multiple-choice questions from " +
        QUESTION_HUB_DIR +
        " in " +
        BANK_COUNT +
        " banks (positions 1–100, 101–200, and so on in hub order). ";
      if (lastBankCount > 0 && lastBankCount < BANK_SIZE) {
        summaryText +=
          "Bank " +
          BANK_COUNT +
          " (positions " +
          formatRange((BANK_COUNT - 1) * BANK_SIZE + 1, BANK_COUNT * BANK_SIZE) +
          ") has " +
          lastBankCount +
          " questions until the list reaches " +
          BANK_SIZE +
          "; then the next bank fills automatically. ";
      }
      summaryText += domain
        ? "Showing " + totalFiltered + " questions in the selected domain across all banks."
        : "Each bank has its own Random and Review session. Domain filter above applies to the bank you start.";
      summary.textContent = summaryText;
      summary.hidden = false;
    }

    grid.setAttribute(
      "aria-label",
      "Practice question banks: " +
        BANK_COUNT +
        " banks of up to " +
        BANK_SIZE +
        " questions each (" +
        allIds.length +
        " total)"
    );
  }

  function showLoadError(msg) {
    var err = document.getElementById("encor-study-load-error");
    if (err) {
      err.textContent = msg;
      err.hidden = false;
    }
  }

  function refreshBanks() {
    var cfg = window.ENCOR_PRACTICE._studyConfig;
    var subjects = window.ENCOR_PRACTICE._subjects;
    if (cfg) updatePracticeBanks(cfg, subjects);
  }

  function bootstrap() {
    enablePortalControls();

    Promise.all([
      fetch(STUDY_CFG_URL, { cache: "no-store" }).then(function (r) {
        if (!r.ok) throw new Error("study config");
        return r.json();
      }),
      fetch(SUBJECTS_URL, { cache: "no-store" })
        .then(function (r) {
          if (!r.ok) throw new Error("subjects");
          return r.json();
        })
        .catch(function () {
          return null;
        }),
      fetch(OBJECTIVES_URL, { cache: "no-store" })
        .then(function (r) {
          if (!r.ok) return null;
          return r.json();
        })
        .catch(function () {
          return null;
        }),
    ])
      .then(function (res) {
        window.ENCOR_PRACTICE._studyConfig = res[0];
        window.ENCOR_PRACTICE._subjects = res[1];
        if (res[2]) populateDomainSelect(res[2]);
        updatePracticeBanks(res[0], res[1]);
      })
      .catch(function () {
        showLoadError("Could not load ENCOR practice config. Refresh the page or try again later.");
      });
  }

  document.addEventListener(
    "click",
    function (e) {
      var t = e.target;
      if (!t || typeof t.closest !== "function") return;
      var el = t.closest("[data-encor-mode]");
      if (!el || el.disabled) return;
      var mode = el.getAttribute("data-encor-mode");
      var bank = parseInt(el.getAttribute("data-encor-bank") || "1", 10);
      if (mode !== "random" && mode !== "review") return;
      if (bank < 1 || bank !== bank) bank = 1;
      e.preventDefault();
      launchBank(mode, bank);
    },
    false
  );

  document.addEventListener("change", function (e) {
    if (!e.target) return;
    if (
      e.target.id === "encor-practice-domain-select" ||
      (e.target.name === "encor-practice-adaptive" && e.target.type === "radio")
    ) {
      refreshBanks();
    }
  });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bootstrap, { once: true });
  } else {
    bootstrap();
  }
  window.addEventListener("pageshow", refreshBanks);
})();

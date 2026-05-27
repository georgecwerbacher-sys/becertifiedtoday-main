(function () {
  "use strict";

  var KEY = "secplusPractice";
  var BANK_SIZE = 100;
  var TOPIC_MAP_URL = "/COMP_TIA_SEC+/data/secplus-question-topic-map.json";
  var QUESTIONS_BASE = "/COMP_TIA_SEC+/SEC+_Questions/";

  function shuffle(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i];
      a[i] = a[j];
      a[j] = t;
    }
    return a;
  }

  window.SECPLUS_PRACTICE = window.SECPLUS_PRACTICE || {};
  window.SECPLUS_PRACTICE.SLUGS = [
    "pentest-hypervisor-vm-escape"
  ];
  window.SECPLUS_PRACTICE._topicAssignments = null;
  window.SECPLUS_PRACTICE._topicAssignmentsPromise = fetch(TOPIC_MAP_URL, { credentials: "same-origin" })
    .then(function (res) {
      if (!res.ok) throw new Error("topic map http " + res.status);
      return res.json();
    })
    .then(function (data) {
      var a = data && data.assignments;
      window.SECPLUS_PRACTICE._topicAssignments = a && typeof a === "object" ? a : {};
      return window.SECPLUS_PRACTICE._topicAssignments;
    })
    .catch(function () {
      window.SECPLUS_PRACTICE._topicAssignments = false;
      return false;
    });

  function objectivesForSlug(assignments, slug) {
    if (!assignments || !slug) return null;
    return assignments[slug + ".html"] || null;
  }

  function slugMatchesMajor(assignments, slug, major) {
    var objs = objectivesForSlug(assignments, slug);
    if (!objs || !objs.length) return false;
    var want = String(major);
    for (var i = 0; i < objs.length; i++) {
      var maj = String(objs[i]).split(".")[0];
      if (maj === want) return true;
    }
    return false;
  }

  function filterSlugsByMajor(slugs, assignments, major) {
    if (!major) return slugs.slice();
    if (!assignments || typeof assignments !== "object") return [];
    var out = [];
    for (var i = 0; i < slugs.length; i++) {
      if (slugMatchesMajor(assignments, slugs[i], major)) out.push(slugs[i]);
    }
    return out;
  }

  function getSelectedPracticeDomain() {
    var sel = document.getElementById("secplus-practice-domain-select");
    if (!sel) return "";
    var v = String(sel.value || "").trim();
    return /^[1-5]$/.test(v) ? v : "";
  }

  function getAdaptiveLearningEnabled() {
    try {
      var r = document.querySelector('input[name="secplus-practice-adaptive"]:checked');
      if (!r) return false;
      return String(r.value || "").trim() === "1";
    } catch (e) {
      return false;
    }
  }

  function bankSlugs(bankId) {
    var all = window.SECPLUS_PRACTICE.SLUGS;
    var n = parseInt(String(bankId), 10);
    if (!n || n < 1) n = 1;
    var start = (n - 1) * BANK_SIZE;
    return all.slice(start, start + BANK_SIZE);
  }

  function practiceBankCount() {
    var all = window.SECPLUS_PRACTICE.SLUGS;
    if (!all || !all.length) return 1;
    return Math.ceil(all.length / BANK_SIZE);
  }

  function start(mode, bankId, domainMajor) {
    bankId = bankId || "1";
    var fixed = bankSlugs(bankId);
    var map = window.SECPLUS_PRACTICE._topicAssignments;
    if (domainMajor) {
      if (!map || typeof map !== "object") {
        window.alert("Topic assignments are still loading. Try again in a moment.");
        return;
      }
      fixed = filterSlugsByMajor(fixed, map, domainMajor);
    }
    if (!fixed.length) {
      window.alert(
        "No questions in this bank match the selected domain. Pick another subject or choose “All subjects”."
      );
      return;
    }
    var order;
    if (mode === "linear") {
      order = fixed;
    } else {
      order = shuffle(fixed);
    }
    var session = { v: 1, mode: mode, bank: bankId, order: order };
    if (domainMajor) session.domain = domainMajor;
    if (getAdaptiveLearningEnabled()) {
      session.adaptive = true;
      session.adaptiveExtrasInjected = 0;
    }
    try {
      sessionStorage.setItem(KEY, JSON.stringify(session));
    } catch (e) {}
    window.location.href = QUESTIONS_BASE + order[0] + ".html#secplusP=0";
  }

  function startWithOptionalDomain(mode, bankId) {
    var domainMajor = getSelectedPracticeDomain() || null;
    if (!domainMajor) {
      start(mode, bankId, null);
      return;
    }
    var inst = window.SECPLUS_PRACTICE;
    var assign = inst._topicAssignments;
    if (assign === false) {
      window.alert(
        'Could not load the topic map for this site. Use "All subjects" or try again later.'
      );
      return;
    }
    if (assign && typeof assign === "object") {
      start(mode, bankId, domainMajor);
      return;
    }
    inst._topicAssignmentsPromise.then(function () {
      if (inst._topicAssignments === false) {
        window.alert(
          'Could not load the topic map for this site. Use "All subjects" or try again later.'
        );
        return;
      }
      start(mode, bankId, domainMajor);
    });
  }

  window.SECPLUS_PRACTICE.BANK_SIZE = BANK_SIZE;
  window.SECPLUS_PRACTICE.start = start;
  window.SECPLUS_PRACTICE.startWithOptionalDomain = startWithOptionalDomain;
  window.SECPLUS_PRACTICE.bankSlugs = bankSlugs;
  window.SECPLUS_PRACTICE.practiceBankCount = practiceBankCount;
  window.SECPLUS_PRACTICE.filterSlugsByMajor = filterSlugsByMajor;
  window.SECPLUS_PRACTICE.getSelectedPracticeDomain = getSelectedPracticeDomain;

  document.addEventListener(
    "click",
    function (e) {
      var t = e.target;
      if (!t || typeof t.closest !== "function") return;
      var el = t.closest("[data-secplus-practice]");
      if (!el || el.disabled) return;
      var m = el.getAttribute("data-secplus-practice");
      var bank = el.getAttribute("data-secplus-practice-bank") || "1";
      if (m === "random" || m === "review" || m === "linear") {
        e.preventDefault();
        startWithOptionalDomain(m, bank);
      }
    },
    false
  );

  function injectPortalPracticeBanks() {
    var grid = document.getElementById("secplus-practice-banks-grid");
    if (!grid) return;

    var all = window.SECPLUS_PRACTICE.SLUGS;
    if (!Array.isArray(all)) return;

    var prior = grid.querySelectorAll("[data-secplus-practice-bank-index]");
    for (var pi = 0; pi < prior.length; pi++) prior[pi].remove();

    var nBanks = practiceBankCount();
    var total = all.length;

    function formatRange(first, last) {
      if (first >= last) return String(first);
      return String(first) + "–" + String(last);
    }

    var summary = document.getElementById("secplus-practice-banks-summary");
    if (summary) {
      var lastBankCount = total - (nBanks - 1) * BANK_SIZE;
      var bankWord = nBanks === 1 ? "bank" : "banks";
      var summaryText =
        total +
        " practice question" +
        (total === 1 ? "" : "s") +
        " in " +
        nBanks +
        " " +
        bankWord +
        " (hub order). ";
      if (lastBankCount > 0 && lastBankCount < BANK_SIZE) {
        summaryText +=
          "The current bank has " +
          lastBankCount +
          " question" +
          (lastBankCount === 1 ? "" : "s") +
          " until the list reaches " +
          BANK_SIZE +
          ". ";
      }
      summaryText +=
        'Use <strong>Practice by subject</strong> to limit Random or Review to a SY0-701 domain before you start.';
      summary.innerHTML = summaryText;
      summary.hidden = false;
    }

    for (var b = 1; b <= nBanks; b++) {
      var startIdx = (b - 1) * BANK_SIZE;
      var endIdx = Math.min(b * BANK_SIZE, all.length);
      var firstNum = startIdx + 1;
      var slotEnd = b * BANK_SIZE;
      var countInBank = endIdx > startIdx ? endIdx - startIdx : 0;

      var article = document.createElement("article");
      article.className = "sim-box";
      article.setAttribute("data-secplus-practice-bank-index", String(b));
      article.setAttribute("aria-labelledby", "secplus-bank-title-" + b);

      var h4 = document.createElement("h4");
      h4.className = "sim-box-title";
      h4.id = "secplus-bank-title-" + b;
      if (countInBank === 0) {
        h4.textContent = "Question bank " + formatRange(firstNum, slotEnd);
      } else {
        h4.textContent = "Question bank " + formatRange(firstNum, endIdx);
      }
      article.appendChild(h4);

      var meta = document.createElement("p");
      meta.className = "study-meta";
      meta.textContent =
        countInBank +
        " item" +
        (countInBank === 1 ? "" : "s") +
        " · Random shuffles once; Review sends misses to the back of the queue.";
      article.appendChild(meta);

      var actions = document.createElement("div");
      actions.className = "study-actions";
      actions.setAttribute("role", "group");
      actions.setAttribute("aria-label", "Practice modes for bank " + String(b));

      var br = document.createElement("button");
      br.type = "button";
      br.className = "start-btn";
      br.setAttribute("data-secplus-practice", "random");
      br.setAttribute("data-secplus-practice-bank", String(b));
      br.textContent = "Random";

      var rev = document.createElement("button");
      rev.type = "button";
      rev.className = "start-btn";
      rev.setAttribute("data-secplus-practice", "review");
      rev.setAttribute("data-secplus-practice-bank", String(b));
      rev.textContent = "Review";

      if (countInBank === 0) {
        br.disabled = true;
        rev.disabled = true;
        br.classList.add("is-placeholder");
        rev.classList.add("is-placeholder");
      }

      actions.appendChild(br);
      actions.appendChild(rev);
      article.appendChild(actions);
      grid.appendChild(article);
    }
  }

  window.SECPLUS_PRACTICE.injectPortalPracticeBanks = injectPortalPracticeBanks;

  function schedulePortalPracticeBanks() {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", injectPortalPracticeBanks, { once: true });
    } else {
      injectPortalPracticeBanks();
    }
  }

  schedulePortalPracticeBanks();
  window.addEventListener("pageshow", injectPortalPracticeBanks);
})();

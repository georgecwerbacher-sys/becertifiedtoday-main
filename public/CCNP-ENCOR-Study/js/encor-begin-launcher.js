/**
 * Shared launcher for begin-questions-{random,review,linear}.html under CCNP-ENCOR-Study.
 */
(function () {
  "use strict";

  var STUDY_CFG_URL = "/CCNP-ENCOR-Study/js/study-config.json";
  var SUBJECTS_URL = "/CCNP-ENCOR-Study/js/question-subjects.json";
  var PORTAL_URL = "/CCNP-ENCOR-Study/ENCOR_Training_Portal.html";
  /** MCQ pages under public/CCNP-ENCOR-Study/ENCOR_Questions/ */
  var QUESTION_BASE = "/CCNP-ENCOR-Study/ENCOR_Questions/question-";
  /** Drag-and-drop pages under public/CCNP-ENCOR-Study/CCNP-ENCOR-Drag-Drop/ */
  var DRAG_DROP_BASE = "/CCNP-ENCOR-Study/CCNP-ENCOR-Drag-Drop/question-";
  var BANK_SIZE = 100;

  function isDragDropId(id, cfg) {
    var n = Number(id);
    if ((cfg.dragDropIds || []).indexOf(n) >= 0) return true;
    if ((cfg.dragDropJsonIds || []).indexOf(n) >= 0) return true;
    return false;
  }

  function questionUrl(id, cfg) {
    var base = cfg && isDragDropId(id, cfg) ? DRAG_DROP_BASE : QUESTION_BASE;
    if (cfg && isDragDropId(id, cfg) && cfg.dragDropDirectory) {
      base = "/" + cfg.dragDropDirectory + "/question-";
    } else if (cfg && !isDragDropId(id, cfg) && cfg.sourceDirectory) {
      base = "/" + cfg.sourceDirectory + "/question-";
    }
    return base + id + ".html";
  }

  function filterByDomain(ids, domain, subjects) {
    if (!domain || !subjects || !subjects.questions) return ids;
    var want = String(domain);
    return ids.filter(function (id) {
      var entry = subjects.questions[String(id)];
      if (!entry) return false;
      var section = typeof entry === "string" ? entry : entry.section || "";
      return String(section).split(".")[0] === want;
    });
  }

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

  function fetchJson(url) {
    return fetch(url, { cache: "no-store" }).then(function (r) {
      if (!r.ok) throw new Error("http " + url);
      return r.json();
    });
  }

  function bankIds(allIds, bankIndex) {
    var n = parseInt(String(bankIndex), 10);
    if (!n || n < 1) n = 1;
    var start = (n - 1) * BANK_SIZE;
    return (allIds || []).slice(start, start + BANK_SIZE);
  }

  function collectIds(cfg, params) {
    var dragDropAll = {};
    (cfg.dragDropIds || []).concat(cfg.dragDropJsonIds || []).forEach(function (id) {
      dragDropAll[id] = true;
    });
    var ids = [];
    if (params.modeParam === "dragdrop") {
      ids = (cfg.dragDropIds || []).slice();
    } else if (params.modeParam === "dragdrop-json") {
      ids = (cfg.dragDropJsonIds || []).slice();
    } else if (params.bankParam) {
      ids = bankIds(cfg.allIds || [], params.bankIndex);
    } else if (params.sectionParam) {
      ids = bankIds(cfg.allIds || [], params.sectionIndex);
    } else {
      var study = (cfg.studies || [])[params.studyIndex - 1];
      ids =
        study && study.ids
          ? study.ids.filter(function (id) {
              return !dragDropAll[id];
            })
          : [];
    }
    return ids;
  }

  function parseParams() {
    var qs = new URLSearchParams(location.search);
    var studyIndex = parseInt(qs.get("study") || "1", 10);
    var sectionIndex = parseInt(qs.get("section") || "1", 10);
    var bankIndex = parseInt(qs.get("bank") || "0", 10);
    if (studyIndex < 1 || studyIndex !== studyIndex) studyIndex = 1;
    if (sectionIndex < 1 || sectionIndex !== sectionIndex) sectionIndex = 1;
    if (bankIndex < 1 || bankIndex !== bankIndex) bankIndex = 0;
    return {
      studyParam: qs.get("study"),
      sectionParam: qs.get("section"),
      bankParam: qs.get("bank"),
      modeParam: qs.get("mode"),
      domainParam: qs.get("domain"),
      studyIndex: studyIndex,
      sectionIndex: sectionIndex,
      bankIndex: bankIndex,
    };
  }

  function fail() {
    location.replace(PORTAL_URL);
  }

  function run(sessionKind) {
    var params = parseParams();
    Promise.all([fetchJson(STUDY_CFG_URL), fetchJson(SUBJECTS_URL).catch(function () { return null; })])
      .then(function (res) {
        var cfg = res[0];
        var subjects = res[1];
        var ids = collectIds(cfg, params);
        ids = filterByDomain(ids, params.domainParam, subjects);
        if (!ids.length) {
          fail();
          return;
        }
        if (sessionKind === "random" || sessionKind === "review") {
          ids = shuffle(ids);
        }
        try {
          sessionStorage.removeItem("ccnpQuestionQueue");
          sessionStorage.removeItem("ccnpQuestionQueueIndex");
          sessionStorage.removeItem("ccnpLinearScope");
          sessionStorage.removeItem("ccnpReviewMode");
          sessionStorage.removeItem("ccnpReviewQueue");
          sessionStorage.removeItem("ccnpQueueExitHref");
          sessionStorage.removeItem("ccnpUrlMaskPath");
          sessionStorage.removeItem("ccnpMaskedPageQid");
          if (sessionKind === "linear") {
            sessionStorage.setItem("ccnpLinearScope", JSON.stringify({ ids: ids.slice() }));
          } else if (sessionKind === "review") {
            sessionStorage.setItem("ccnpReviewMode", "1");
            sessionStorage.setItem("ccnpReviewQueue", JSON.stringify(ids));
          } else {
            sessionStorage.setItem("ccnpQuestionQueue", JSON.stringify(ids));
            sessionStorage.setItem("ccnpQuestionQueueIndex", "0");
          }
        } catch (e) {}
        location.replace(questionUrl(ids[0], cfg));
      })
      .catch(fail);
  }

  window.ENCOR_BEGIN_LAUNCH = run;
})();

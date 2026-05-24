/**
 * CCNA-style timed test scorecard for ENCOR (scaled score, domain rollup, objectives table).
 */
(function () {
  "use strict";

  var OBJECTIVES_URL = "/CCNP-ENCOR-Study/data/encor-exam-objectives-350-401-v1.2.json";
  var SUBJECTS_URL = "/CCNP-ENCOR-Study/js/question-subjects.json";
  var BLUEPRINT_URL = "/CCNP-ENCOR-Study/data/encor-test-simulation-blueprint.json";

  var cachedSubjects = null;
  var cachedObjectiveLabels = null;
  var cachedDomainTitles = null;
  var cachedScoreConfig = null;
  var cachedLabSections = null;

  function escapeHtml(s) {
    return String(s || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function compareObjIds(a, b) {
    var pa = String(a).split(".").map(Number);
    var pb = String(b).split(".").map(Number);
    var len = Math.max(pa.length, pb.length);
    for (var i = 0; i < len; i++) {
      var da = pa[i] || 0;
      var db = pb[i] || 0;
      if (da !== db) return da - db;
    }
    return 0;
  }

  function buildObjectiveLabels(examJson) {
    var map = {};
    (examJson.domains || []).forEach(function (d) {
      (d.objectives || []).forEach(function (o) {
        if (o.id) map[o.id] = o.text || o.id;
      });
    });
    return map;
  }

  function buildDomainMajorTitles(examJson) {
    var map = {};
    (examJson.domains || []).forEach(function (d) {
      var id = String(d.id || "").trim();
      var m = id.match(/^(\d+)\.0$/);
      if (m) map[m[1]] = d.name || "Domain " + m[1];
    });
    return map;
  }

  function scoreConfigFromBlueprint(bp) {
    var w = bp.weights || {};
    var scaleMax = bp.scaledScoreMax != null ? bp.scaledScoreMax : 1000;
    return {
      maxTotal: scaleMax,
      passing: bp.passingScaledScore != null ? bp.passingScaledScore : 800,
      maxMcq: scaleMax * (typeof w.multipleChoiceFraction === "number" ? w.multipleChoiceFraction : 0.7),
      maxDnd: scaleMax * (typeof w.dragDropFraction === "number" ? w.dragDropFraction : 0.1),
      maxLab: scaleMax * (typeof w.labFraction === "number" ? w.labFraction : 0.2),
    };
  }

  function queueItemType(item) {
    var kind = String(item.kind || "");
    if (kind === "sim") return "lab";
    if (kind === "dragdrop" || kind === "dragdrop-json") return "dnd";
    return "mcq";
  }

  function questionIdFromUrl(url) {
    var m = String(url || "").match(/question-(\d+)\.html/i);
    return m ? m[1] : null;
  }

  function labKeyFromUrl(url) {
    var s = String(url || "");
    var idx = s.indexOf("/CCNP-ENCOR-Labs/");
    if (idx >= 0) return s.slice(idx + "/CCNP-ENCOR-Labs/".length).split("?")[0];
    return s.split("/").pop() || "";
  }

  function objectiveIdsForQueueItem(item, subjects, labSections) {
    labSections = labSections || {};
    var kind = String(item.kind || "");
    if (kind === "sim") {
      var key = labKeyFromUrl(item.url);
      var sec = labSections[key] || labSections[key.split("/").pop()] || "3.0";
      return [sec];
    }
    var qid = questionIdFromUrl(item.url);
    if (!qid || !subjects || !subjects.questions) return [];
    var entry = subjects.questions[String(qid)];
    if (!entry) return [];
    var section = typeof entry === "string" ? entry : entry.section || "";
    if (!section) return [];
    return [section];
  }

  function buildAttemptResults(queue, answeredByIndex, subjects, labSections) {
    var results = [];
    for (var i = 0; i < queue.length; i++) {
      var item = queue[i] || {};
      results.push({
        itemIndex: i,
        type: queueItemType(item),
        objectiveIds: objectiveIdsForQueueItem(item, subjects, labSections),
        correct: answeredByIndex[i] === true,
      });
    }
    return results;
  }

  function primaryDomainMajorFromObjectiveIds(ids) {
    if (!ids || !ids.length) return "__none__";
    var sorted = ids.slice().sort(compareObjIds);
    for (var i = 0; i < sorted.length; i++) {
      var maj = String(sorted[i]).split(".")[0];
      if (/^[1-6]$/.test(maj)) return maj;
    }
    return "__none__";
  }

  function emptyDomainAgg() {
    return {
      correct: 0,
      total: 0,
      types: { mcq: { c: 0, t: 0 }, dnd: { c: 0, t: 0 }, lab: { c: 0, t: 0 } },
    };
  }

  function formatScorecardByType(types) {
    var parts = [];
    [
      { k: "mcq", lab: "MCQ" },
      { k: "dnd", lab: "D&D" },
      { k: "lab", lab: "Lab" },
    ].forEach(function (o) {
      var x = types[o.k];
      if (!x || !x.t) return;
      parts.push(o.lab + " " + x.c + "/" + x.t);
    });
    return parts.length ? parts.join(" · ") : "—";
  }

  function domainReviewTier(pct, total) {
    if (total < 2) {
      return {
        label: "Limited sample",
        cls: "scorecard-tier-muted",
        hint: "Not enough items mapped here—treat this row as directional only.",
      };
    }
    if (pct < 60) {
      return {
        label: "Priority review",
        cls: "scorecard-tier-priority",
        hint: "Strong candidate for focused study and labs next.",
      };
    }
    if (pct < 75) {
      return {
        label: "Needs work",
        cls: "scorecard-tier-review",
        hint: "Revisit objectives below and drill similar questions.",
      };
    }
    if (pct < 85) {
      return {
        label: "Almost there",
        cls: "scorecard-tier-solid",
        hint: "Light review recommended before exam day.",
      };
    }
    return {
      label: "Strong",
      cls: "scorecard-tier-strong",
      hint: "Keep sharp with occasional mixed practice.",
    };
  }

  function computeScaledScore(attemptResults, queue, cfg) {
    var den = { mcq: 0, dnd: 0, lab: 0 };
    queue.forEach(function (it) {
      var ty = queueItemType(it);
      if (ty === "mcq") den.mcq++;
      else if (ty === "dnd") den.dnd++;
      else if (ty === "lab") den.lab++;
    });
    var mcqCorrect = 0;
    var dndCorrect = 0;
    var labCorrect = 0;
    attemptResults.forEach(function (r) {
      if (!r.correct) return;
      if (r.type === "mcq") mcqCorrect++;
      else if (r.type === "dnd") dndCorrect++;
      else if (r.type === "lab") labCorrect++;
    });
    var mcqPts = den.mcq ? (cfg.maxMcq * mcqCorrect) / den.mcq : 0;
    var dndPts = den.dnd ? (cfg.maxDnd * dndCorrect) / den.dnd : 0;
    var labPts = den.lab ? (cfg.maxLab * labCorrect) / den.lab : 0;
    var total = Math.round(mcqPts + dndPts + labPts);
    return {
      total: total,
      pass: total >= cfg.passing,
      mcqCorrect: mcqCorrect,
      dndCorrect: dndCorrect,
      labCorrect: labCorrect,
      den: den,
      mcqPts: mcqPts,
      dndPts: dndPts,
      labPts: labPts,
      cfg: cfg,
    };
  }

  function objectiveTopicLabel(oid, objectiveLabels, subjects) {
    if (oid === "__none__") return "Not mapped in topic tracker";
    if (objectiveLabels[oid]) return objectiveLabels[oid];
    if (subjects && subjects.questions) {
      var keys = Object.keys(subjects.questions);
      for (var i = 0; i < keys.length; i++) {
        var entry = subjects.questions[keys[i]];
        var section = typeof entry === "string" ? entry : entry.section || "";
        if (section === oid) {
          return typeof entry === "string" ? entry : entry.label || entry.name || oid;
        }
      }
    }
    return "(see ENCOR objectives)";
  }

  function populateResults(reason, attemptResults, queue, ctx) {
    ctx = ctx || {};
    var objectiveLabels = ctx.objectiveLabels || {};
    var domainMajorTitles = ctx.domainMajorTitles || {};
    var scoreScaledConfig = ctx.scoreScaledConfig || scoreConfigFromBlueprint({});

    var headline = "Attempt summary";
    var reasonText = "";
    if (reason === "complete") {
      headline = "Test complete";
      reasonText = "You reached the end of this timed session.";
    } else if (reason === "timeout") {
      headline = "Time expired";
      reasonText = "The timer hit zero. Results include every item scored before the clock stopped.";
    } else if (reason === "quit") {
      headline = "Attempt ended";
      reasonText = "You quit before finishing. Scored items include everything you completed.";
    }

    document.getElementById("resultsHeadline").textContent = headline;
    document.getElementById("resultsReason").textContent = reasonText;

    var scaled = computeScaledScore(attemptResults, queue, scoreScaledConfig);
    document.getElementById("resultsScore").textContent =
      "Scaled score: " +
      scaled.total +
      " / " +
      scaled.cfg.maxTotal +
      " — " +
      (scaled.pass ? "Pass" : "Did not pass") +
      " (passing score " +
      scaled.cfg.passing +
      ").";

    var breakdown =
      "Weighted scoring: multiple-choice " +
      scaled.mcqCorrect +
      "/" +
      scaled.den.mcq +
      " → up to " +
      Math.round(scaled.cfg.maxMcq) +
      " pts (" +
      Math.round(scaled.mcqPts) +
      " earned); drag-and-drop " +
      scaled.dndCorrect +
      "/" +
      scaled.den.dnd +
      " → up to " +
      Math.round(scaled.cfg.maxDnd) +
      " pts (" +
      Math.round(scaled.dndPts) +
      " earned); labs " +
      scaled.labCorrect +
      "/" +
      scaled.den.lab +
      " → up to " +
      Math.round(scaled.cfg.maxLab) +
      " pts (" +
      Math.round(scaled.labPts) +
      " earned).";

    document.getElementById("resultsNote").textContent =
      breakdown +
      " Use the study scorecard for blueprint gaps; the objective table lists every tagged objective from your attempt.";

    var rollup = {};
    attemptResults.forEach(function (r) {
      var ids = r.objectiveIds && r.objectiveIds.length ? r.objectiveIds : ["__none__"];
      ids.forEach(function (oid) {
        if (!rollup[oid]) rollup[oid] = { correct: 0, total: 0 };
        rollup[oid].total += 1;
        if (r.correct) rollup[oid].correct += 1;
      });
    });

    var domainAgg = {};
    attemptResults.forEach(function (r) {
      var maj = primaryDomainMajorFromObjectiveIds(r.objectiveIds);
      if (!domainAgg[maj]) domainAgg[maj] = emptyDomainAgg();
      var b = domainAgg[maj];
      b.total += 1;
      if (r.correct) b.correct += 1;
      var ty = r.type;
      if (ty === "mcq" || ty === "dnd" || ty === "lab") {
        b.types[ty].t += 1;
        if (r.correct) b.types[ty].c += 1;
      }
    });

    var scorecardLead = document.getElementById("resultsScorecardLead");
    scorecardLead.textContent =
      "Each scored item is counted once under its primary blueprint domain (first mapped objective ID by exam order). Rows are sorted with the weakest domains first.";

    var scorecardBody = document.getElementById("resultsDomainScorecardBody");
    scorecardBody.innerHTML = "";
    var domainKeys = Object.keys(domainAgg).filter(function (k) {
      return domainAgg[k].total > 0;
    });
    domainKeys.sort(function (a, b) {
      function pctFor(k) {
        var z = domainAgg[k];
        return z.total ? z.correct / z.total : 1;
      }
      if (a === "__none__") return 1;
      if (b === "__none__") return -1;
      var pa = pctFor(a);
      var pb = pctFor(b);
      if (pa !== pb) return pa - pb;
      return compareObjIds(a + ".0", b + ".0");
    });

    if (!domainKeys.length) {
      scorecardLead.textContent =
        "No domain rollup available—your attempt may lack objective mappings in question-subjects.json.";
    }

    domainKeys.forEach(function (maj) {
      var d = domainAgg[maj];
      var pct = d.total ? Math.round((d.correct / d.total) * 1000) / 10 : 0;
      var tier = domainReviewTier(pct, d.total);
      var domainTitle =
        maj === "__none__"
          ? "Not mapped / miscellaneous"
          : "Domain " + maj + " — " + (domainMajorTitles[maj] || "ENCOR blueprint");
      var tr = document.createElement("tr");
      tr.innerHTML =
        "<td>" +
        escapeHtml(domainTitle) +
        "</td><td>" +
        d.correct +
        " / " +
        d.total +
        ' (<span class="obj-pct">' +
        pct +
        "%</span>)</td><td><span class=\"scorecard-by-type\">" +
        escapeHtml(formatScorecardByType(d.types)) +
        "</span></td><td><span class=\"" +
        tier.cls +
        "\">" +
        escapeHtml(tier.label) +
        '</span><span class="scorecard-hint">' +
        escapeHtml(tier.hint) +
        "</span></td>";
      scorecardBody.appendChild(tr);
    });

    var weakLead = document.getElementById("resultsWeakObjectiveLead");
    var weakList = document.getElementById("resultsWeakObjectiveList");
    weakList.innerHTML = "";
    var weaknessCandidates = [];
    Object.keys(rollup).forEach(function (oid) {
      if (oid === "__none__") return;
      var rw = rollup[oid];
      var pctW = rw.total ? Math.round((rw.correct / rw.total) * 1000) / 10 : 0;
      if (rw.total >= 2 && pctW < 70) weaknessCandidates.push({ oid: oid, row: rw, pct: pctW });
    });
    weaknessCandidates.sort(function (a, b) {
      if (a.pct !== b.pct) return a.pct - b.pct;
      return compareObjIds(a.oid, b.oid);
    });

    if (!weaknessCandidates.length) {
      weakLead.textContent =
        "No individual objectives scored below 70% with at least two tagged attempts—or every miss was spread thin. Keep drilling weak domains above.";
    } else {
      weakLead.textContent =
        "Lowest performers among mapped objectives (under 70%, two or more attempts). Use these IDs with the blueprint and ENCOR Training Portal banks.";
      var limit = Math.min(weaknessCandidates.length, 18);
      for (var wi = 0; wi < limit; wi++) {
        var wc = weaknessCandidates[wi];
        var topicW = objectiveTopicLabel(wc.oid, objectiveLabels, ctx.subjects);
        var li = document.createElement("li");
        li.innerHTML =
          "<strong>" +
          escapeHtml(wc.oid) +
          '</strong> — <span class="scorecard-weak-pct">' +
          wc.pct +
          "%</span> (" +
          wc.row.correct +
          "/" +
          wc.row.total +
          ") · " +
          escapeHtml(topicW);
        weakList.appendChild(li);
      }
    }

    var tbody = document.getElementById("resultsObjectiveBody");
    tbody.innerHTML = "";
    Object.keys(rollup)
      .sort(compareObjIds)
      .forEach(function (oid) {
        var row = rollup[oid];
        var pctO = row.total ? Math.round((row.correct / row.total) * 1000) / 10 : 0;
        var tr = document.createElement("tr");
        var label = oid === "__none__" ? "—" : oid;
        var topic = objectiveTopicLabel(oid, objectiveLabels, ctx.subjects);
        tr.innerHTML =
          "<td>" +
          escapeHtml(label) +
          "</td><td>" +
          escapeHtml(topic) +
          "</td><td>" +
          row.correct +
          "</td><td>" +
          row.total +
          '</td><td class="obj-pct">' +
          pctO +
          "%</td>";
        tbody.appendChild(tr);
      });
  }

  function loadContext() {
    if (cachedSubjects && cachedObjectiveLabels && cachedDomainTitles && cachedScoreConfig) {
      return Promise.resolve({
        subjects: cachedSubjects,
        objectiveLabels: cachedObjectiveLabels,
        domainMajorTitles: cachedDomainTitles,
        scoreScaledConfig: cachedScoreConfig,
        labSections: cachedLabSections || {},
      });
    }
    return Promise.all([
      fetch(SUBJECTS_URL, { cache: "no-store" }).then(function (r) {
        return r.ok ? r.json() : { questions: {} };
      }),
      fetch(OBJECTIVES_URL, { cache: "no-store" }).then(function (r) {
        return r.ok ? r.json() : { domains: [] };
      }),
      fetch(BLUEPRINT_URL, { cache: "no-store" }).then(function (r) {
        return r.ok ? r.json() : {};
      }),
    ]).then(function (res) {
      cachedSubjects = res[0];
      cachedObjectiveLabels = buildObjectiveLabels(res[1]);
      cachedDomainTitles = buildDomainMajorTitles(res[1]);
      var bp = res[2];
      cachedScoreConfig = scoreConfigFromBlueprint(bp);
      cachedLabSections = bp.labSections || {};
      return {
        subjects: cachedSubjects,
        objectiveLabels: cachedObjectiveLabels,
        domainMajorTitles: cachedDomainTitles,
        scoreScaledConfig: cachedScoreConfig,
        labSections: cachedLabSections,
      };
    });
  }

  function showResults(reason, queue, answeredByIndex) {
    return loadContext().then(function (ctx) {
      var attemptResults = buildAttemptResults(queue, answeredByIndex, ctx.subjects, ctx.labSections);
      populateResults(reason, attemptResults, queue, ctx);
      return attemptResults;
    });
  }

  window.ENCOR_TEST_SIM_SCORECARD = {
    showResults: showResults,
    buildAttemptResults: buildAttemptResults,
    populateResults: populateResults,
  };
})();

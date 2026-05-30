/**
 * Timed Security+ test scorecard (scaled score, SY0-701 domain rollup, objectives table).
 */
(function () {
  "use strict";

  var OBJECTIVES_URL = "/COMP_TIA_SEC+/data/secplus-exam-objectives-sy0-701.json";
  var TOPIC_MAP_URL = "/COMP_TIA_SEC+/data/secplus-question-topic-map.json";
  var BLUEPRINT_URL = "/COMP_TIA_SEC+/data/secplus-test-simulation-blueprint.json";

  var cachedTopicMap = null;
  var cachedObjectiveLabels = null;
  var cachedDomainTitles = null;
  var cachedScoreConfig = null;
  var cachedSimSections = null;

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
    var scaleMax = bp.scaledScoreMax != null ? bp.scaledScoreMax : 900;
    return {
      maxTotal: scaleMax,
      passing: bp.passingScaledScore != null ? bp.passingScaledScore : 750,
      maxMcq: scaleMax * (typeof w.multipleChoiceFraction === "number" ? w.multipleChoiceFraction : 0.85),
      maxSim: scaleMax * (typeof w.simFraction === "number" ? w.simFraction : 0.15),
    };
  }

  function queueItemType(item) {
    return String(item.kind || "") === "sim" ? "sim" : "mcq";
  }

  function slugFileFromUrl(url) {
    var m = String(url || "").match(/SEC\+_Questions\/([^/?#]+)\.html/i);
    return m ? m[1] + ".html" : null;
  }

  function simKeyFromUrl(url) {
    var s = String(url || "");
    var idx = s.indexOf("/SEC+_Sim_Hot_Spot/");
    if (idx >= 0) return s.slice(idx + "/SEC+_Sim_Hot_Spot/".length).split("?")[0];
    return s.split("/").pop() || "";
  }

  function objectiveIdsForQueueItem(item, topicMap, simSections) {
    simSections = simSections || {};
    var kind = String(item.kind || "");
    if (kind === "sim") {
      var key = simKeyFromUrl(item.url);
      var sec = simSections[key] || simSections[key.split("/").pop()] || "4.0";
      return [sec];
    }
    var fileName = slugFileFromUrl(item.url);
    if (!fileName || !topicMap || !topicMap.assignments) return [];
    var ids = topicMap.assignments[fileName];
    return Array.isArray(ids) && ids.length ? ids.slice() : [];
  }

  function buildAttemptResults(queue, answeredByIndex, topicMap, simSections) {
    var results = [];
    for (var i = 0; i < queue.length; i++) {
      var item = queue[i] || {};
      results.push({
        itemIndex: i,
        type: queueItemType(item),
        objectiveIds: objectiveIdsForQueueItem(item, topicMap, simSections),
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
      if (/^[1-5]$/.test(maj)) return maj;
    }
    return "__none__";
  }

  function emptyDomainAgg() {
    return {
      correct: 0,
      total: 0,
      types: { mcq: { c: 0, t: 0 }, sim: { c: 0, t: 0 } },
    };
  }

  function formatScorecardByType(types) {
    var parts = [];
    [
      { k: "mcq", lab: "MCQ" },
      { k: "sim", lab: "Sim / hot spot" },
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
        hint: "Strong candidate for focused study next.",
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
    var den = { mcq: 0, sim: 0 };
    queue.forEach(function (it) {
      var ty = queueItemType(it);
      if (ty === "mcq") den.mcq++;
      else if (ty === "sim") den.sim++;
    });
    var mcqCorrect = 0;
    var simCorrect = 0;
    attemptResults.forEach(function (r) {
      if (!r.correct) return;
      if (r.type === "mcq") mcqCorrect++;
      else if (r.type === "sim") simCorrect++;
    });
    var mcqPts = den.mcq ? (cfg.maxMcq * mcqCorrect) / den.mcq : 0;
    var simPts = den.sim ? (cfg.maxSim * simCorrect) / den.sim : 0;
    var total = Math.round(mcqPts + simPts);
    return {
      total: total,
      pass: total >= cfg.passing,
      mcqCorrect: mcqCorrect,
      simCorrect: simCorrect,
      den: den,
      mcqPts: mcqPts,
      simPts: simPts,
      cfg: cfg,
    };
  }

  function objectiveTopicLabel(oid, objectiveLabels) {
    if (oid === "__none__") return "Not mapped in topic tracker";
    if (objectiveLabels[oid]) return objectiveLabels[oid];
    return "(see SY0-701 objectives)";
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
      reasonText = "The timer hit zero. Results include every item you scored before the clock stopped.";
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
      " earned); simulations & hot spots " +
      scaled.simCorrect +
      "/" +
      scaled.den.sim +
      " → up to " +
      Math.round(scaled.cfg.maxSim) +
      " pts (" +
      Math.round(scaled.simPts) +
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
      if (ty === "mcq" || ty === "sim") {
        b.types[ty].t += 1;
        if (r.correct) b.types[ty].c += 1;
      }
    });

    var scorecardLead = document.getElementById("resultsScorecardLead");
    scorecardLead.textContent =
      "Each scored item is counted once under its primary SY0-701 domain (first mapped objective ID by exam order). Rows are sorted with the weakest domains first.";

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

    domainKeys.forEach(function (maj) {
      var d = domainAgg[maj];
      var pct = d.total ? Math.round((d.correct / d.total) * 1000) / 10 : 0;
      var tier = domainReviewTier(pct, d.total);
      var domainTitle =
        maj === "__none__"
          ? "Not mapped / miscellaneous"
          : "Domain " + maj + " — " + (domainMajorTitles[maj] || "SY0-701 blueprint");
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
        "Lowest performers among mapped objectives (under 70%, two or more attempts). Use these IDs with the blueprint and Security+ Training Portal banks.";
      var limit = Math.min(weaknessCandidates.length, 18);
      for (var wi = 0; wi < limit; wi++) {
        var wc = weaknessCandidates[wi];
        var topicW = objectiveTopicLabel(wc.oid, objectiveLabels);
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
        var topic = objectiveTopicLabel(oid, objectiveLabels);
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

  function buildScorecardEmailPayload(reason, attemptResults, queue, ctx) {
    ctx = ctx || {};
    var domainMajorTitles = ctx.domainMajorTitles || {};
    var objectiveLabels = ctx.objectiveLabels || {};
    var scoreScaledConfig = ctx.scoreScaledConfig || scoreConfigFromBlueprint({});
    var scaled = computeScaledScore(attemptResults, queue, scoreScaledConfig);

    var domainAgg = {};
    attemptResults.forEach(function (r) {
      var maj = primaryDomainMajorFromObjectiveIds(r.objectiveIds);
      if (!domainAgg[maj]) domainAgg[maj] = emptyDomainAgg();
      var b = domainAgg[maj];
      b.total += 1;
      if (r.correct) b.correct += 1;
    });

    var domains = Object.keys(domainAgg)
      .filter(function (k) {
        return domainAgg[k].total > 0;
      })
      .map(function (maj) {
        var d = domainAgg[maj];
        var pct = d.total ? Math.round((d.correct / d.total) * 1000) / 10 : 0;
        var tier = domainReviewTier(pct, d.total);
        return {
          id: maj,
          title:
            maj === "__none__"
              ? "Not mapped / miscellaneous"
              : "Domain " + maj + " — " + (domainMajorTitles[maj] || "SY0-701 blueprint"),
          correct: d.correct,
          total: d.total,
          pct: pct,
          priority: tier.label,
        };
      })
      .sort(function (a, b) {
        return a.pct - b.pct;
      });

    var rollup = {};
    attemptResults.forEach(function (r) {
      var ids = r.objectiveIds && r.objectiveIds.length ? r.objectiveIds : ["__none__"];
      ids.forEach(function (oid) {
        if (!rollup[oid]) rollup[oid] = { correct: 0, total: 0 };
        rollup[oid].total += 1;
        if (r.correct) rollup[oid].correct += 1;
      });
    });

    var weakObjectives = [];
    Object.keys(rollup).forEach(function (oid) {
      if (oid === "__none__") return;
      var rw = rollup[oid];
      var pctW = rw.total ? Math.round((rw.correct / rw.total) * 1000) / 10 : 0;
      if (rw.total >= 1 && pctW < 70) {
        weakObjectives.push({
          id: oid,
          topic: objectiveTopicLabel(oid, objectiveLabels),
          correct: rw.correct,
          total: rw.total,
          pct: pctW,
        });
      }
    });
    weakObjectives.sort(function (a, b) {
      return a.pct - b.pct;
    });

    return {
      reason: reason,
      scaledScore: scaled.total,
      scaledMax: scaled.cfg.maxTotal,
      passingScore: scaled.cfg.passing,
      passed: scaled.pass,
      mcqCorrect: scaled.mcqCorrect,
      mcqTotal: scaled.den.mcq,
      simCorrect: scaled.simCorrect,
      simTotal: scaled.den.sim,
      domains: domains.slice(0, 8),
      weakObjectives: weakObjectives.slice(0, 12),
      isFreeSample: queue.length <= 20,
    };
  }

  function loadContext() {
    if (cachedTopicMap && cachedObjectiveLabels && cachedDomainTitles && cachedScoreConfig) {
      return Promise.resolve({
        topicMap: cachedTopicMap,
        objectiveLabels: cachedObjectiveLabels,
        domainMajorTitles: cachedDomainTitles,
        scoreScaledConfig: cachedScoreConfig,
        simSections: cachedSimSections || {},
      });
    }
    return Promise.all([
      fetch(TOPIC_MAP_URL, { cache: "no-store" }).then(function (r) {
        return r.ok ? r.json() : { assignments: {} };
      }),
      fetch(OBJECTIVES_URL, { cache: "no-store" }).then(function (r) {
        return r.ok ? r.json() : { domains: [] };
      }),
      fetch(BLUEPRINT_URL, { cache: "no-store" }).then(function (r) {
        return r.ok ? r.json() : {};
      }),
    ]).then(function (res) {
      cachedTopicMap = res[0];
      cachedObjectiveLabels = buildObjectiveLabels(res[1]);
      cachedDomainTitles = buildDomainMajorTitles(res[1]);
      var bp = res[2];
      cachedScoreConfig = scoreConfigFromBlueprint(bp);
      cachedSimSections = bp.simSections || {};
      return {
        topicMap: cachedTopicMap,
        objectiveLabels: cachedObjectiveLabels,
        domainMajorTitles: cachedDomainTitles,
        scoreScaledConfig: cachedScoreConfig,
        simSections: cachedSimSections,
      };
    });
  }

  function showResults(reason, queue, answeredByIndex) {
    return loadContext().then(function (ctx) {
      var attemptResults = buildAttemptResults(
        queue,
        answeredByIndex,
        ctx.topicMap,
        ctx.simSections
      );
      populateResults(reason, attemptResults, queue, ctx);
      return {
        attemptResults: attemptResults,
        emailPayload: buildScorecardEmailPayload(reason, attemptResults, queue, ctx),
      };
    });
  }

  window.SECPLUS_TEST_SIM_SCORECARD = {
    showResults: showResults,
    buildAttemptResults: buildAttemptResults,
    populateResults: populateResults,
    buildScorecardEmailPayload: buildScorecardEmailPayload,
  };
})();

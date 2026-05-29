/**
 * Build mixed Security+ timed-test queue from topic map + secplus-test-simulation-blueprint.json.
 */
(function () {
  "use strict";

  var TOPIC_MAP_URL = "/COMP_TIA_SEC+/data/secplus-question-topic-map.json";
  var BLUEPRINT_URL = "/COMP_TIA_SEC+/data/secplus-test-simulation-blueprint.json";
  var SIM_BASE = "/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/";
  var MCQ_BASE = "/COMP_TIA_SEC+/SEC+_Questions/";

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

  function pickRandom(list, n) {
    return shuffle(list).slice(0, Math.min(n, list.length));
  }

  function slugFromAssignmentKey(key) {
    return String(key || "").replace(/\.html$/i, "");
  }

  function mcqUrl(slug) {
    return MCQ_BASE + slug + ".html";
  }

  function buildQueue(topicMap, bp) {
    bp = bp || {};
    var assignments = (topicMap && topicMap.assignments) || {};
    var slugPool = Object.keys(assignments)
      .map(slugFromAssignmentKey)
      .filter(Boolean);

    var mcqN = bp.multipleChoiceCount != null ? bp.multipleChoiceCount : 90;
    var simFiles = Array.isArray(bp.simFiles) && bp.simFiles.length ? bp.simFiles : [];

    var questionSlugs = pickRandom(slugPool, mcqN);
    var simUrls = simFiles.map(function (f) {
      return SIM_BASE + String(f).replace(/^\//, "");
    });

    var queue = []
      .concat(
        questionSlugs.map(function (slug) {
          return { kind: "question", url: mcqUrl(slug) };
        })
      )
      .concat(
        simUrls.map(function (url) {
          return { kind: "sim", url: url };
        })
      );

    return shuffle(queue);
  }

  function loadConfigAndBlueprint() {
    return Promise.all([
      fetch(TOPIC_MAP_URL, { cache: "no-store" }).then(function (r) {
        if (!r.ok) throw new Error("topic map");
        return r.json();
      }),
      fetch(BLUEPRINT_URL, { cache: "no-store" }).then(function (r) {
        if (!r.ok) throw new Error("blueprint");
        return r.json();
      }),
    ]).then(function (res) {
      var topicMap = res[0];
      var bp = res[1];
      return {
        topicMap: topicMap,
        bp: bp,
        queue: buildQueue(topicMap, bp),
        durationMinutes: bp.durationMinutes != null ? bp.durationMinutes : 90,
      };
    });
  }

  window.SECPLUS_TEST_SIM_BUILD = {
    buildQueue: buildQueue,
    loadConfigAndBlueprint: loadConfigAndBlueprint,
  };
})();

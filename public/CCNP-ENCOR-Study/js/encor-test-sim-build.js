/**
 * Build mixed ENCOR timed-test queue from study-config + encor-test-simulation-blueprint.json.
 */
(function () {
  "use strict";

  var STUDY_CFG_URL = "/CCNP-ENCOR-Study/js/study-config.json";
  var BLUEPRINT_URL = "/CCNP-ENCOR-Study/data/encor-test-simulation-blueprint.json";
  var FREE_BLUEPRINT_URL = "/CCNP-ENCOR-Study/data/encor-free-simulation-blueprint.json";
  var LAB_BASE = "/CCNP-ENCOR-Study/CCNP-ENCOR-Labs/";

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

  function mcqUrl(cfg, id) {
    var dir = cfg.sourceDirectory || "CCNP-ENCOR-Study/ENCOR_Questions";
    return "/" + dir + "/question-" + id + ".html";
  }

  function dragUrl(cfg, id) {
    var dir = cfg.dragDropDirectory || "CCNP-ENCOR-Study/CCNP-ENCOR-Drag-Drop";
    return "/" + dir + "/question-" + id + ".html";
  }

  function buildQueue(cfg, bp) {
    bp = bp || {};
    var dragDropLookup = {};
    (cfg.dragDropIds || []).concat(cfg.dragDropJsonIds || []).forEach(function (id) {
      dragDropLookup[id] = true;
    });

    var nonDragIds = (cfg.allIds || []).filter(function (id) {
      return !dragDropLookup[id];
    });

    var mcqN = bp.multipleChoiceCount != null ? bp.multipleChoiceCount : 50;
    var dndN = bp.dragDropCount != null ? bp.dragDropCount : 5;
    var labFiles = Array.isArray(bp.labFiles) && bp.labFiles.length ? bp.labFiles : [];

    var questionIds = pickRandom(nonDragIds, mcqN);
    var dragPool = (cfg.dragDropIds || []).slice();
    if (dragPool.length < dndN) {
      dragPool = dragPool.concat(cfg.dragDropJsonIds || []);
    }
    var dragPicked = pickRandom(dragPool, dndN);

    var simUrls = labFiles.map(function (f) {
      return LAB_BASE + String(f).replace(/^\//, "");
    });

    var queue = []
      .concat(
        questionIds.map(function (id) {
          return { kind: "question", url: mcqUrl(cfg, id) };
        })
      )
      .concat(
        dragPicked.map(function (id) {
          return { kind: "dragdrop", url: dragUrl(cfg, id) };
        })
      )
      .concat(
        simUrls.map(function (url) {
          return { kind: "sim", url: url };
        })
      );

    return shuffle(queue);
  }

  function dndPathForBlueprint(bp, id) {
    var map = bp.dragDropPaths || {};
    if (map[String(id)]) return map[String(id)];
    if (id === 365) return "/CCNP-ENCOR-Study/ENCOR_Samples/question-365.html";
    return "/CCNP-ENCOR-Study/CCNP-ENCOR-Drag-Drop/question-" + id + ".html";
  }

  function buildFreeQueue(bp) {
    bp = bp || {};
    var queue = [];
    (bp.multipleChoiceIds || []).forEach(function (id) {
      queue.push({
        kind: "question",
        url: "/CCNP-ENCOR-Study/ENCOR_Questions/question-" + id + ".html",
      });
    });
    (bp.dragDropIds || []).forEach(function (id) {
      queue.push({
        kind: "dragdrop",
        url: dndPathForBlueprint(bp, id),
      });
    });
    (bp.labFiles || []).forEach(function (fn) {
      queue.push({
        kind: "sim",
        url: LAB_BASE + String(fn).replace(/^\//, ""),
      });
    });
    return shuffle(queue);
  }

  function loadFreeSimulationQueue() {
    return fetch(FREE_BLUEPRINT_URL, { cache: "no-store" })
      .then(function (r) {
        if (!r.ok) throw new Error("blueprint");
        return r.json();
      })
      .then(function (bp) {
        var queue = buildFreeQueue(bp);
        if (!queue.length) throw new Error("empty");
        return {
          bp: bp,
          queue: queue,
          durationMinutes: bp.durationMinutes != null ? bp.durationMinutes : 45,
        };
      });
  }

  function loadConfigAndBlueprint(options) {
    options = options || {};
    var blueprintUrl = options.blueprintUrl || BLUEPRINT_URL;
    return Promise.all([
      fetch(STUDY_CFG_URL, { cache: "no-store" }).then(function (r) {
        if (!r.ok) throw new Error("study config");
        return r.json();
      }),
      fetch(blueprintUrl, { cache: "no-store" }).then(function (r) {
        if (!r.ok) throw new Error("blueprint");
        return r.json();
      }),
    ]).then(function (res) {
      var cfg = res[0];
      var bp = res[1];
      return {
        cfg: cfg,
        bp: bp,
        queue: buildQueue(cfg, bp),
        durationMinutes: bp.durationMinutes != null ? bp.durationMinutes : 120,
      };
    });
  }

  window.ENCOR_TEST_SIM_BUILD = {
    buildQueue: buildQueue,
    buildFreeQueue: buildFreeQueue,
    loadConfigAndBlueprint: loadConfigAndBlueprint,
    loadFreeSimulationQueue: loadFreeSimulationQueue,
    FREE_BLUEPRINT_URL: FREE_BLUEPRINT_URL,
  };
})();

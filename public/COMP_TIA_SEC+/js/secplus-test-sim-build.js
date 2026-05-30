/**
 * Build mixed Security+ timed-test queue from topic map + secplus-test-simulation-blueprint.json.
 */
(function () {
  "use strict";

  var TOPIC_MAP_URL = "/COMP_TIA_SEC+/data/secplus-question-topic-map.json";
  var BLUEPRINT_URL = "/COMP_TIA_SEC+/data/secplus-test-simulation-blueprint.json";
  var FREE_BLUEPRINT_URL = "/COMP_TIA_SEC+/data/secplus-free-simulation-blueprint.json";
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

  function domainMajorFromSlug(assignments, slug) {
    var ids = assignments[slug] || assignments[slug + ".html"] || [];
    if (!Array.isArray(ids) || !ids.length) return "__none__";
    for (var i = 0; i < ids.length; i++) {
      var maj = String(ids[i]).split(".")[0];
      if (/^[1-5]$/.test(maj)) return maj;
    }
    return "__none__";
  }

  function buildQueueBalancedByDomain(topicMap, bp) {
    bp = bp || {};
    var assignments = (topicMap && topicMap.assignments) || {};
    var mcqN = bp.multipleChoiceCount != null ? bp.multipleChoiceCount : 20;
    var perDomain = Math.max(1, Math.floor(mcqN / 5));
    var buckets = { 1: [], 2: [], 3: [], 4: [], 5: [], __none__: [] };

    Object.keys(assignments).forEach(function (key) {
      var slug = slugFromAssignmentKey(key);
      if (!slug) return;
      var maj = domainMajorFromSlug(assignments, key);
      if (!buckets[maj]) maj = "__none__";
      buckets[maj].push(slug);
    });

    var picked = [];
    ["1", "2", "3", "4", "5"].forEach(function (maj) {
      picked = picked.concat(pickRandom(buckets[maj], perDomain));
    });
    if (picked.length < mcqN) {
      var rest = [];
      Object.keys(buckets).forEach(function (k) {
        buckets[k].forEach(function (slug) {
          if (picked.indexOf(slug) === -1) rest.push(slug);
        });
      });
      picked = picked.concat(pickRandom(rest, mcqN - picked.length));
    }
    picked = picked.slice(0, mcqN);

    var simFiles = Array.isArray(bp.simFiles) && bp.simFiles.length ? bp.simFiles : [];
    var simUrls = simFiles.map(function (f) {
      return SIM_BASE + String(f).replace(/^\//, "");
    });

    var queue = picked
      .map(function (slug) {
        return { kind: "question", url: mcqUrl(slug) };
      })
      .concat(
        simUrls.map(function (url) {
          return { kind: "sim", url: url };
        })
      );

    return shuffle(queue);
  }

  function buildQueue(topicMap, bp) {
    if (bp && bp.balancedDomains) {
      return buildQueueBalancedByDomain(topicMap, bp);
    }
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

  function loadConfigAndBlueprint(options) {
    options = options || {};
    var blueprintUrl = options.blueprintUrl || BLUEPRINT_URL;
    return Promise.all([
      fetch(TOPIC_MAP_URL, { cache: "no-store" }).then(function (r) {
        if (!r.ok) throw new Error("topic map");
        return r.json();
      }),
      fetch(blueprintUrl, { cache: "no-store" }).then(function (r) {
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
    buildQueueBalancedByDomain: buildQueueBalancedByDomain,
    loadConfigAndBlueprint: loadConfigAndBlueprint,
    FREE_BLUEPRINT_URL: FREE_BLUEPRINT_URL,
  };
})();

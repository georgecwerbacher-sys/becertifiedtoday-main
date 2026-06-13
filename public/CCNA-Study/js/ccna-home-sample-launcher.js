(function () {
  "use strict";

  var KEY = "ccnaHomeSample";
  var BLUEPRINT_URL = "/CCNA-Study/data/ccna-home-sample-blueprint.json";
  var TOPIC_MAP_URL = "/CCNA-Study/data/ccna-question-topic-map.json";
  var DND_TOPIC_MAP_URL = "/CCNA-Study/data/ccna-dnd-topic-map.json";
  var MANIFEST_URL = "/CCNA-Study/data/ccna-practice-questions-manifest.json";
  var MCQ_BASE = "/CCNA-Study/CCNA_questions/";
  var DND_BASE = "/CCNA-Study/CCNA_D_D/";
  var SAMPLE_DND_FTP = "/CCNA-Study/CCNA_Samples/dragdrop-ftp-vs-tftp.html";
  var HASH_PREFIX = "ccnaHS=";
  var CCNA_DOMAINS = ["1.0", "2.0", "3.0", "4.0", "5.0", "6.0"];
  var CCNA_DOMAIN_NAMES = {
    "1.0": "Network Fundamentals",
    "2.0": "Network Access",
    "3.0": "IP Connectivity",
    "4.0": "IP Services",
    "5.0": "Security Fundamentals",
    "6.0": "Automation and Programmability",
  };

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

  function majorDomain(objectiveId) {
    var n = parseFloat(objectiveId);
    if (Number.isNaN(n)) return null;
    return Math.floor(n) + ".0";
  }

  function itemHref(item, index) {
    var hash = "#" + HASH_PREFIX + index;
    if (item.type === "lab" || item.type === "dnd") return item.path + "?sample=1" + hash;
    return MCQ_BASE + item.slug + ".html?sample=1" + hash;
  }

  function slugPoolFromManifest(manifest, blueprint) {
    var seen = Object.create(null);
    var pool = [];
    (manifest && manifest.items ? manifest.items : []).forEach(function (row) {
      if (!row || !row.slug || seen[row.slug]) return;
      seen[row.slug] = true;
      pool.push(row.slug);
    });
    if (!pool.length) {
      (blueprint.mcqSlugs || []).forEach(function (slug) {
        if (slug && !seen[slug]) {
          seen[slug] = true;
          pool.push(slug);
        }
      });
    }
    return pool;
  }

  function buildMcqOrderPerDomain(blueprint, topicMap, manifest) {
    var perDomain = blueprint.homeSampleQuestionCountPerDomain;
    if (perDomain == null || perDomain < 1) return null;

    var assignments = (topicMap && topicMap.assignments) || {};
    var byDomain = Object.create(null);
    CCNA_DOMAINS.forEach(function (domainId) {
      byDomain[domainId] = [];
    });

    slugPoolFromManifest(manifest, blueprint).forEach(function (slug) {
      var objs = assignments[slug + ".html"] || [];
      if (!objs.length) return;
      var domainId = majorDomain(objs[0]);
      if (!domainId || !byDomain[domainId]) return;
      byDomain[domainId].push(slug);
    });

    var order = [];
    CCNA_DOMAINS.forEach(function (domainId) {
      shuffle(byDomain[domainId] || [])
        .slice(0, perDomain)
        .forEach(function (slug) {
          order.push({
            type: "mcq",
            slug: slug,
            domain: domainId,
            domainName: CCNA_DOMAIN_NAMES[domainId] || domainId,
          });
        });
    });
    return shuffle(order);
  }

  function buildMcqOrder(blueprint, topicMap, manifest) {
    var perDomainOrder = buildMcqOrderPerDomain(blueprint, topicMap, manifest);
    if (perDomainOrder && perDomainOrder.length) return perDomainOrder;

    var total = blueprint.homeSampleQuestionCountTotal;
    var pool = slugPoolFromManifest(manifest, blueprint);
    var pick =
      typeof total === "number" && total > 0 ? shuffle(pool).slice(0, total) : shuffle(pool);
    return pick.map(function (slug) {
      return { type: "mcq", slug: slug };
    });
  }

  function buildDndPoolFromTopicMap(topicMap, blueprint) {
    var pool = [];
    var seen = Object.create(null);
    Object.keys((topicMap && topicMap.assignments) || {}).forEach(function (fn) {
      if (!/^dragdrop-/i.test(fn)) return;
      var slug = fn.replace(/\.html$/i, "");
      if (seen[slug]) return;
      seen[slug] = true;
      pool.push({
        type: "dnd",
        path: DND_BASE + slug + ".html",
        title: "Drag-and-drop",
      });
    });
    if (!seen["dragdrop-ftp-vs-tftp"]) {
      pool.push({
        type: "dnd",
        path: SAMPLE_DND_FTP,
        title: "FTP vs TFTP drag-and-drop",
      });
    }
    (blueprint.dragDrop || []).forEach(function (d) {
      if (!d || !d.path) return;
      var found = false;
      for (var i = 0; i < pool.length; i++) {
        if (pool[i].path === d.path) {
          found = true;
          break;
        }
      }
      if (!found) pool.push(d);
    });
    return pool;
  }

  function buildDndOrder(blueprint, dndTopicMap) {
    var count = blueprint.homeSampleDragDropCount || 4;
    var pool = blueprint.useFullDragDropBank
      ? buildDndPoolFromTopicMap(dndTopicMap, blueprint)
      : blueprint.dragDrop || [];
    return shuffle(pool)
      .slice(0, count)
      .map(function (d) {
        return { type: "dnd", path: d.path, title: d.title || "Drag-and-drop" };
      });
  }

  function buildLabOrder(blueprint) {
    if (!blueprint.lab || !blueprint.lab.path) return [];
    return [
      {
        type: "lab",
        path: blueprint.lab.path,
        title: blueprint.lab.title || "CLI lab",
      },
    ];
  }

  function domainsFromOrder(order) {
    var seen = Object.create(null);
    var list = [];
    (order || []).forEach(function (item) {
      if (!item || item.type !== "mcq" || !item.domain) return;
      if (seen[item.domain]) return;
      seen[item.domain] = true;
      list.push(item.domain);
    });
    list.sort(function (a, b) {
      return parseFloat(a) - parseFloat(b);
    });
    return list;
  }

  function persistSession(order, finishHome, blueprint, kind) {
    if (!order.length) throw new Error("empty");
    var mcqCount = order.filter(function (item) {
      return item.type === "mcq";
    }).length;
    var session = {
      order: order,
      mcqCount: mcqCount,
      totalCount: order.length,
      sampleDomains: domainsFromOrder(order),
      sampleResults: {},
      finishHome: finishHome || blueprint.finishHome || "/ccna-home.html",
      leadCaptureHash: blueprint.leadCaptureHash || "#ccna-lead-capture",
      title: blueprint.title || "CCNA sample",
      product: "ccna",
    };
    try {
      sessionStorage.setItem(KEY, JSON.stringify(session));
      sessionStorage.setItem("ccnpUrlMaskPath", "/sample");
      sessionStorage.setItem("ccnpSampleKind", kind || "ccna-home");
      sessionStorage.removeItem("encorHomeSample");
      sessionStorage.removeItem("ccnaPractice100");
      sessionStorage.removeItem("ccnaDnd25");
      sessionStorage.removeItem("ccnpQuestionQueue");
    } catch (e) {}
    var singleTrack =
      order.every(function (item) {
        return item && item.type === "mcq";
      }) ||
      order.every(function (item) {
        return item && (item.type === "dnd" || item.type === "lab");
      });
    if (singleTrack) {
      location.replace("/sample#ccnaHS=0");
      return;
    }
    location.replace(itemHref(order[0], 0));
  }

  function loadBlueprint() {
    return fetch(BLUEPRINT_URL, { cache: "no-store" }).then(function (r) {
      if (!r.ok) throw new Error("blueprint");
      return r.json();
    });
  }

  function startQuestionsSample(finishHome) {
    return Promise.all([
      loadBlueprint(),
      fetch(TOPIC_MAP_URL, { cache: "no-store" }).then(function (r) {
        if (!r.ok) throw new Error("topics");
        return r.json();
      }),
      fetch(MANIFEST_URL, { cache: "no-store" }).then(function (r) {
        if (!r.ok) throw new Error("manifest");
        return r.json();
      }),
    ]).then(function (results) {
      persistSession(buildMcqOrder(results[0], results[1], results[2]), finishHome, results[0], "ccna-questions");
    });
  }

  function startDndSample(finishHome) {
    return loadBlueprint()
      .then(function (blueprint) {
        if (!blueprint.useFullDragDropBank) return [blueprint, null];
        return fetch(DND_TOPIC_MAP_URL, { cache: "no-store" })
          .then(function (r) {
            if (!r.ok) throw new Error("dnd-topics");
            return r.json();
          })
          .then(function (dndTopicMap) {
            return [blueprint, dndTopicMap];
          });
      })
      .then(function (results) {
        var order = buildDndOrder(results[0], results[1]);
        if (!order.length) throw new Error("dnd");
        persistSession(order, finishHome, results[0], "ccna-dnd");
      });
  }

  function startLabSample(finishHome) {
    return loadBlueprint().then(function (blueprint) {
      var order = buildLabOrder(blueprint);
      if (!order.length) throw new Error("lab");
      persistSession(order, finishHome, blueprint, "ccna-lab");
    });
  }

  function resumeFromHash() {
    var params = new URLSearchParams(location.search || "");
    if (params.get("track")) return false;
    var m = /^#ccnaHS=(\d+)$/.exec(location.hash || "");
    if (!m) return false;
    var idx = parseInt(m[1], 10);
    var raw;
    try {
      raw = sessionStorage.getItem(KEY);
    } catch (e) {
      return false;
    }
    if (!raw) return false;
    var session;
    try {
      session = JSON.parse(raw);
    } catch (e2) {
      return false;
    }
    if (!session || !Array.isArray(session.order) || !session.order[idx]) return false;
    location.replace(itemHref(session.order[idx], idx));
    return true;
  }

  window.CCNA_HOME_SAMPLE = {
    startQuestions: startQuestionsSample,
    startDnd: startDndSample,
    startLab: startLabSample,
    resumeFromHash: resumeFromHash,
    KEY: KEY,
  };
})();

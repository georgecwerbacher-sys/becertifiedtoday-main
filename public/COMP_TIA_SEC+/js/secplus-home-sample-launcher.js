(function () {
  "use strict";

  var KEY = "secplusHomeSample";
  var BLUEPRINT_URL = "/COMP_TIA_SEC+/data/secplus-home-sample-blueprint.json";
  var MCQ_BASE = "/COMP_TIA_SEC+/SEC+_Questions/";
  var HASH_PREFIX = "secplusHS=";

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

  function itemHref(item, index) {
    var hash = "#" + HASH_PREFIX + index;
    if (item.type === "sim") return item.path + hash;
    return MCQ_BASE + item.slug + ".html" + hash;
  }

  function buildMcqOrder(blueprint, perDomain) {
    var order = [];
    var seen = Object.create(null);
    var byDomain = blueprint.multipleChoiceByDomain || {};
    ["1.0", "2.0", "3.0", "4.0", "5.0"].forEach(function (domainId) {
      var slugs = (byDomain[domainId] || []).slice(0, perDomain);
      slugs.forEach(function (slug) {
        if (!slug || seen[slug]) return;
        seen[slug] = true;
        order.push({ type: "mcq", slug: slug, domain: domainId });
      });
    });
    return order;
  }

  function buildFullOrder(blueprint) {
    var order = buildMcqOrder(blueprint, 5);
    if (blueprint.simulation && blueprint.simulation.path) {
      order.push({
        type: "sim",
        path: blueprint.simulation.path,
        title: blueprint.simulation.title || "Performance-based simulation",
      });
    }
    return shuffle(order);
  }

  function buildQuestionsOrder(blueprint) {
    var total = blueprint.homeSampleQuestionCountTotal;
    if (typeof total === "number" && total > 0) {
      var pool = [];
      var seen = Object.create(null);
      var byDomain = blueprint.multipleChoiceByDomain || {};
      ["1.0", "2.0", "3.0", "4.0", "5.0"].forEach(function (domainId) {
        (byDomain[domainId] || []).forEach(function (slug) {
          if (!slug || seen[slug]) return;
          seen[slug] = true;
          pool.push({ type: "mcq", slug: slug, domain: domainId });
        });
      });
      return shuffle(pool).slice(0, total);
    }
    var perDomain =
      blueprint.homeSampleQuestionCountPerDomain != null
        ? blueprint.homeSampleQuestionCountPerDomain
        : 4;
    return shuffle(buildMcqOrder(blueprint, perDomain));
  }

  function buildSimOrder(blueprint, simKey) {
    var sims = blueprint.simulationsByKey || {};
    var sim = sims[simKey];
    if (!sim || !sim.path) return [];
    return [
      {
        type: "sim",
        path: sim.path,
        title: sim.title || "Performance-based simulation",
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

  function persistSession(order, finishHome, blueprint) {
    if (!order.length) throw new Error("empty");
    var mcqCount = order.filter(function (item) {
      return item.type === "mcq";
    }).length;
    var session = {
      order: order,
      mcqCount: mcqCount,
      totalCount: order.length,
      sampleDomains: domainsFromOrder(order),
      finishHome: finishHome || blueprint.finishHome || "/comptia-sec+-home.html",
      title: blueprint.title || "Security+ sample",
    };
    try {
      sessionStorage.setItem(KEY, JSON.stringify(session));
      sessionStorage.setItem("secplusUrlMaskPath", "/secplus-sample");
      sessionStorage.removeItem("secplusPractice");
      sessionStorage.removeItem("ccnpHomeSecplusSimSample");
    } catch (e) {}
    var singleTrackSample =
      order.every(function (item) {
        return item && item.type === "mcq";
      }) ||
      order.every(function (item) {
        return item && item.type === "sim";
      });
    if (singleTrackSample) {
      location.replace("/secplus-sample#secplusHS=0");
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

  function startSample(finishHome) {
    return loadBlueprint().then(function (blueprint) {
      persistSession(shuffle(buildFullOrder(blueprint)), finishHome, blueprint);
    });
  }

  function startQuestionsSample(finishHome) {
    return loadBlueprint().then(function (blueprint) {
      persistSession(buildQuestionsOrder(blueprint), finishHome, blueprint);
    });
  }

  function startSimSample(simKey, finishHome) {
    return loadBlueprint().then(function (blueprint) {
      var order = buildSimOrder(blueprint, simKey);
      if (!order.length) throw new Error("sim");
      persistSession(order, finishHome, blueprint);
    });
  }

  function resumeFromHash() {
    var params = new URLSearchParams(location.search || "");
    if (params.get("track")) return false;
    var m = /^#secplusHS=(\d+)$/.exec(location.hash || "");
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

  window.SECPLUS_HOME_SAMPLE = {
    start: startSample,
    startQuestions: startQuestionsSample,
    startSim: startSimSample,
    resumeFromHash: resumeFromHash,
    KEY: KEY,
  };
})();

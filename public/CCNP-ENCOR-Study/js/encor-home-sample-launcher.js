(function () {
  "use strict";

  var KEY = "encorHomeSample";
  var BLUEPRINT_URL = "/CCNP-ENCOR-Study/data/encor-home-sample-blueprint.json";
  var MCQ_DIR = "/CCNP-ENCOR-Study/ENCOR_Questions";
  var SUBJECTS_URL = "/CCNP-ENCOR-Study/js/question-subjects.json";
  var HASH_PREFIX = "encorHS=";

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

  function dndPath(blueprint, id) {
    var map = blueprint.dragDropPaths || {};
    if (map[String(id)]) return map[String(id)];
    if (id === 365) return "/CCNP-ENCOR-Study/ENCOR_Samples/question-365.html";
    return "/CCNP-ENCOR-Study/CCNP-ENCOR-Drag-Drop/question-" + id + ".html";
  }

  function itemHref(item, index) {
    var hash = "#" + HASH_PREFIX + index;
    if (item.type === "lab" || item.type === "dnd") return item.path + "?sample=1" + hash;
    return MCQ_DIR + "/question-" + item.id + ".html?sample=1" + hash;
  }

  function buildMcqOrder(blueprint) {
    var total = blueprint.homeSampleQuestionCountTotal;
    var pool = (blueprint.mcqIds || []).slice();
    var pick = typeof total === "number" && total > 0 ? shuffle(pool).slice(0, total) : shuffle(pool);
    return pick.map(function (id) {
      return { type: "mcq", id: id };
    });
  }

  function buildDndOrder(blueprint) {
    return shuffle((blueprint.dragDropIds || []).slice()).map(function (id) {
      return { type: "dnd", id: id, path: dndPath(blueprint, id) };
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

  function enrichMcqOrder(order, subjects) {
    var map = (subjects && subjects.questions) || {};
    return order.map(function (item) {
      if (!item || item.type !== "mcq" || item.id == null) return item;
      var meta = map[String(item.id)];
      if (!meta) return item;
      return {
        type: "mcq",
        id: item.id,
        domain: meta.section,
        domainName: meta.name,
      };
    });
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
      finishHome: finishHome || blueprint.finishHome || "/ccnp-home.html",
      leadCaptureHash: blueprint.leadCaptureHash || "#encor-lead-capture",
      title: blueprint.title || "ENCOR sample",
      product: "encor",
    };
    try {
      sessionStorage.setItem(KEY, JSON.stringify(session));
      sessionStorage.setItem("ccnpUrlMaskPath", "/sample");
      sessionStorage.setItem("ccnpSampleKind", kind || "encor-home");
      sessionStorage.removeItem("ccnpQuestionQueue");
      sessionStorage.removeItem("ccnaHomeSample");
    } catch (e) {}
    var singleTrack =
      order.every(function (item) {
        return item && item.type === "mcq";
      }) ||
      order.every(function (item) {
        return item && (item.type === "dnd" || item.type === "lab");
      });
    if (singleTrack) {
      location.replace("/sample#encorHS=0");
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
      fetch(SUBJECTS_URL, { cache: "no-store" }).then(function (r) {
        if (!r.ok) throw new Error("subjects");
        return r.json();
      }),
    ]).then(function (results) {
      var blueprint = results[0];
      var subjects = results[1];
      var order = enrichMcqOrder(buildMcqOrder(blueprint), subjects);
      persistSession(order, finishHome, blueprint, "encor-questions");
    });
  }

  function startDndSample(finishHome) {
    return loadBlueprint().then(function (blueprint) {
      var order = buildDndOrder(blueprint);
      if (!order.length) throw new Error("dnd");
      persistSession(order, finishHome, blueprint, "encor-dnd");
    });
  }

  function startLabSample(finishHome) {
    return loadBlueprint().then(function (blueprint) {
      var order = buildLabOrder(blueprint);
      if (!order.length) throw new Error("lab");
      persistSession(order, finishHome, blueprint, "encor-lab");
    });
  }

  function resumeFromHash() {
    var params = new URLSearchParams(location.search || "");
    if (params.get("track")) return false;
    var m = /^#encorHS=(\d+)$/.exec(location.hash || "");
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

  function buildFullFreeSimOrder(blueprint) {
    var order = [];
    (blueprint.multipleChoiceIds || []).forEach(function (id) {
      order.push({ type: "mcq", id: id });
    });
    (blueprint.dragDropIds || []).forEach(function (id) {
      order.push({ type: "dnd", id: id, path: dndPath(blueprint, id) });
    });
    (blueprint.labFiles || []).forEach(function (fn) {
      order.push({
        type: "lab",
        path: "/CCNP-ENCOR-Study/CCNP-ENCOR-Labs/" + fn,
        title: "CLI lab",
      });
    });
    return shuffle(order);
  }

  function startFreeSimSample(finishHome) {
    return fetch("/CCNP-ENCOR-Study/data/encor-free-simulation-blueprint.json", { cache: "no-store" })
      .then(function (r) {
        if (!r.ok) throw new Error("blueprint");
        return r.json();
      })
      .then(function (blueprint) {
        var order = buildFullFreeSimOrder(blueprint);
        persistSession(order, finishHome, blueprint, "encor-free-sim");
      });
  }

  window.ENCOR_HOME_SAMPLE = {
    startQuestions: startQuestionsSample,
    startDnd: startDndSample,
    startLab: startLabSample,
    startFreeSim: startFreeSimSample,
    resumeFromHash: resumeFromHash,
    KEY: KEY,
  };
})();

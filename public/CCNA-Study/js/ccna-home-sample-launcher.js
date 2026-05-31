(function () {
  "use strict";

  var KEY = "ccnaHomeSample";
  var BLUEPRINT_URL = "/CCNA-Study/data/ccna-home-sample-blueprint.json";
  var MCQ_BASE = "/CCNA-Study/CCNA_questions/";
  var HASH_PREFIX = "ccnaHS=";

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
    if (item.type === "lab" || item.type === "dnd") return item.path + "?sample=1" + hash;
    return MCQ_BASE + item.slug + ".html?sample=1" + hash;
  }

  function buildMcqOrder(blueprint) {
    var total = blueprint.homeSampleQuestionCountTotal;
    var pool = (blueprint.mcqSlugs || []).slice();
    if (typeof total === "number" && total > 0) {
      return shuffle(pool)
        .slice(0, total)
        .map(function (slug) {
          return { type: "mcq", slug: slug };
        });
    }
    return shuffle(pool).map(function (slug) {
      return { type: "mcq", slug: slug };
    });
  }

  function buildDndOrder(blueprint) {
    return (blueprint.dragDrop || []).map(function (d) {
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

  function persistSession(order, finishHome, blueprint, kind) {
    if (!order.length) throw new Error("empty");
    var mcqCount = order.filter(function (item) {
      return item.type === "mcq";
    }).length;
    var session = {
      order: order,
      mcqCount: mcqCount,
      totalCount: order.length,
      finishHome: finishHome || blueprint.finishHome || "/ccna-home.html",
      leadCaptureHash: blueprint.leadCaptureHash || "#ccna-lead-capture",
      title: blueprint.title || "CCNA sample",
      product: "ccna",
    };
    try {
      sessionStorage.setItem(KEY, JSON.stringify(session));
      sessionStorage.setItem("ccnpUrlMaskPath", "/sample");
      sessionStorage.setItem("ccnpSampleKind", kind || "ccna-home");
      sessionStorage.removeItem("ccnaPractice100");
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
    return loadBlueprint().then(function (blueprint) {
      persistSession(buildMcqOrder(blueprint), finishHome, blueprint, "ccna-questions");
    });
  }

  function startDndSample(finishHome) {
    return loadBlueprint().then(function (blueprint) {
      var order = buildDndOrder(blueprint);
      if (!order.length) throw new Error("dnd");
      persistSession(order, finishHome, blueprint, "ccna-dnd");
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

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

  function buildOrder(blueprint) {
    var order = [];
    var byDomain = blueprint.multipleChoiceByDomain || {};
    ["1.0", "2.0", "3.0", "4.0", "5.0"].forEach(function (domainId) {
      var slugs = byDomain[domainId] || [];
      slugs.forEach(function (slug) {
        order.push({ type: "mcq", slug: slug, domain: domainId });
      });
    });
    if (blueprint.simulation && blueprint.simulation.path) {
      order.push({
        type: "sim",
        path: blueprint.simulation.path,
        title: blueprint.simulation.title || "Performance-based simulation",
      });
    }
    return shuffle(order);
  }

  function startSample(finishHome) {
    return fetch(BLUEPRINT_URL)
      .then(function (r) {
        if (!r.ok) throw new Error("blueprint");
        return r.json();
      })
      .then(function (blueprint) {
        var order = buildOrder(blueprint);
        if (!order.length) throw new Error("empty");
        var session = {
          order: order,
          finishHome: finishHome || blueprint.finishHome || "/comptia-sec+-home.html",
          title: blueprint.title || "Security+ sample",
        };
        try {
          sessionStorage.setItem(KEY, JSON.stringify(session));
          sessionStorage.setItem("secplusUrlMaskPath", "/secplus-sample");
          sessionStorage.removeItem("secplusPractice");
        } catch (e) {}
        location.replace(itemHref(order[0], 0));
      });
  }

  window.SECPLUS_HOME_SAMPLE = {
    start: startSample,
    KEY: KEY,
  };
})();

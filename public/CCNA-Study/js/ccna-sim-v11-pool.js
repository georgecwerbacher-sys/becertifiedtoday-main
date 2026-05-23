/**
 * CCNA timed simulations: MCQ pool limited to Version 1.1 2026 (hub positions 1–300).
 * Hub order matches ccna-practice-questions-manifest.json / ccna-practice-100-hub.js ALL_SLUGS.
 */
(function () {
  "use strict";

  var VERSION_11_2026_MAX = 300;
  var MANIFEST_URL = "/CCNA-Study/data/ccna-practice-questions-manifest.json";
  /** @type {Record<string, number>|null} slug → 1-based hub index */
  var hubIndexBySlug = null;
  var loadPromise = null;

  function buildIndexMap(manifest) {
    var map = Object.create(null);
    var items = manifest && manifest.items;
    if (!Array.isArray(items)) return map;
    for (var i = 0; i < items.length; i++) {
      var slug = items[i] && items[i].slug;
      if (slug) map[slug] = i + 1;
    }
    return map;
  }

  function loadHubIndexMap() {
    if (loadPromise) return loadPromise;
    loadPromise = fetch(MANIFEST_URL, { credentials: "same-origin" })
      .then(function (r) {
        if (!r.ok) throw new Error("manifest http " + r.status);
        return r.json();
      })
      .then(function (manifest) {
        hubIndexBySlug = buildIndexMap(manifest);
        return hubIndexBySlug;
      })
      .catch(function () {
        hubIndexBySlug = Object.create(null);
        return hubIndexBySlug;
      });
    return loadPromise;
  }

  function slugFromFileName(fileName) {
    return String(fileName || "").replace(/\.html$/i, "");
  }

  function hubIndexForFileName(fileName) {
    if (!hubIndexBySlug) return null;
    return hubIndexBySlug[slugFromFileName(fileName)] || null;
  }

  function isV11McqFileName(fileName) {
    var idx = hubIndexForFileName(fileName);
    return idx != null && idx <= VERSION_11_2026_MAX;
  }

  function filterMcqAssignmentKeys(assignments) {
    var keys = Object.keys(assignments || {});
    var out = [];
    for (var i = 0; i < keys.length; i++) {
      if (isV11McqFileName(keys[i])) out.push(keys[i]);
    }
    return out;
  }

  function filterMcqAssignments(assignments) {
    var qa = assignments || {};
    var out = {};
    Object.keys(qa).forEach(function (fn) {
      if (isV11McqFileName(fn)) out[fn] = qa[fn];
    });
    return out;
  }

  window.CCNA_SIM_V11_POOL = {
    VERSION_11_2026_MAX: VERSION_11_2026_MAX,
    load: loadHubIndexMap,
    hubIndexForFileName: hubIndexForFileName,
    isV11McqFileName: isV11McqFileName,
    filterMcqAssignmentKeys: filterMcqAssignmentKeys,
    filterMcqAssignments: filterMcqAssignments,
  };
})();

/**
 * CCNA timed simulations: MCQ pool limited to Version 1.1 2026 (excludes tagged v2.0 slugs).
 * Hub order matches ccna-practice-questions-manifest.json / ccna-practice-100-hub.js ALL_SLUGS.
 */
(function () {
  "use strict";

  var VERSION_20_SLUGS_URL = "/CCNA-Study/data/ccna-version-2-0-slugs.json";
  /** @type {Record<string, true>|null} */
  var version20SlugSet = null;
  var loadPromise = null;

  function buildVersion20Set(data) {
    var set = Object.create(null);
    var slugs = data && data.slugs;
    if (!Array.isArray(slugs)) return set;
    for (var i = 0; i < slugs.length; i++) {
      if (slugs[i]) set[String(slugs[i])] = true;
    }
    return set;
  }

  function loadVersion20SlugSet() {
    if (loadPromise) return loadPromise;
    loadPromise = fetch(VERSION_20_SLUGS_URL, { credentials: "same-origin" })
      .then(function (r) {
        if (!r.ok) throw new Error("version 2.0 slugs http " + r.status);
        return r.json();
      })
      .then(function (data) {
        version20SlugSet = buildVersion20Set(data);
        return version20SlugSet;
      })
      .catch(function () {
        version20SlugSet = Object.create(null);
        return version20SlugSet;
      });
    return loadPromise;
  }

  function slugFromFileName(fileName) {
    return String(fileName || "").replace(/\.html$/i, "");
  }

  function isVersion20FileName(fileName) {
    if (!version20SlugSet) return false;
    return !!version20SlugSet[slugFromFileName(fileName)];
  }

  function isV11McqFileName(fileName) {
    return !isVersion20FileName(fileName);
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
    load: loadVersion20SlugSet,
    isVersion20FileName: isVersion20FileName,
    isV11McqFileName: isV11McqFileName,
    filterMcqAssignmentKeys: filterMcqAssignmentKeys,
    filterMcqAssignments: filterMcqAssignments,
  };
})();

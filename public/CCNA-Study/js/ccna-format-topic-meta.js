(function () {
  "use strict";

  var UPDATED_LABEL = "Updated for 2026";
  var DND_MAP_URL = "/CCNA-Study/data/ccna-dnd-topic-map.json";
  var LAB_MAP_URL = "/CCNA-Study/data/ccna-lab-topic-map.json";
  var DOMAIN_NAMES = {
    "1.0": "Network Fundamentals",
    "2.0": "Network Access",
    "3.0": "IP Connectivity",
    "4.0": "IP Services",
    "5.0": "Security Fundamentals",
    "6.0": "Automation and Programmability",
  };

  var mapCache = null;

  function isDragDropPage() {
    return document.body && document.body.classList.contains("dragdrop-exercise");
  }

  function isLabPage() {
    return /\/CCNA_labs\//i.test(location.pathname);
  }

  function fileNameFromPath() {
    var m = location.pathname.match(/\/([^/]+\.html)$/i);
    return m ? m[1] : "";
  }

  function mapUrl() {
    return isLabPage() ? LAB_MAP_URL : DND_MAP_URL;
  }

  function loadMap() {
    if (mapCache) return Promise.resolve(mapCache);
    return fetch(mapUrl(), { credentials: "same-origin" })
      .then(function (r) {
        if (!r.ok) throw new Error("topic map");
        return r.json();
      })
      .then(function (data) {
        mapCache = (data && data.assignments) || {};
        return mapCache;
      })
      .catch(function () {
        mapCache = {};
        return mapCache;
      });
  }

  function subjectLabel(assignments, fileName) {
    if (!assignments || !fileName) return "";
    var objs = assignments[fileName];
    if (!objs || !objs.length) return "";
    var majNum = String(objs[0]).split(".")[0];
    if (!/^[1-6]$/.test(majNum)) return "";
    var majKey = majNum + ".0";
    var name = DOMAIN_NAMES[majKey] || "Domain " + majKey;
    return majNum + " \u2014 " + name;
  }

  function syncMeta() {
    if (!isDragDropPage() && !isLabPage()) return;

    var versionEl = document.querySelector(".question-topic-meta__version");
    var subjectEl = document.querySelector(".question-topic-meta__subject");
    if (!versionEl && !subjectEl) return;

    if (versionEl) versionEl.textContent = UPDATED_LABEL;

    if (!subjectEl) return;
    var fileName = fileNameFromPath();
    loadMap().then(function (assignments) {
      subjectEl.textContent = subjectLabel(assignments, fileName);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", syncMeta);
  } else {
    syncMeta();
  }
})();

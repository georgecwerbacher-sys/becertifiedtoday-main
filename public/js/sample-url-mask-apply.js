(function () {
  try {
    var originalPath = location.pathname || "";
    var pathLower = originalPath.toLowerCase();
    var isSamplePath =
      pathLower === "/sample" ||
      pathLower === "/sample/" ||
      pathLower === "/secplus-sample" ||
      pathLower === "/secplus-sample/";
    if (!isSamplePath) {
      sessionStorage.setItem("ccnaLastRealPath", originalPath);
    }
    var mask =
      sessionStorage.getItem("ccnpUrlMaskPath") ||
      sessionStorage.getItem("secplusUrlMaskPath");
    if (!mask && /(?:\?|&)sample=1(?:&|$)/.test(location.search || "")) {
      mask = "/sample";
      sessionStorage.setItem("ccnpUrlMaskPath", mask);
    }
    if (!mask) return;
    history.replaceState(null, "", mask);
  } catch (e) {}
})();

(function () {
  "use strict";

  function inTargetPage() {
    var path = (location.pathname || "").toLowerCase();
    return (
      path.indexOf("/ccna-study/ccna_questions/") !== -1 ||
      path.indexOf("/ccna-study/ccna_d_d/") !== -1 ||
      path.indexOf("/ccna-study/ccna_labs/") !== -1 ||
      path.indexOf("/ccna_sim_exam/embed/dnd/") !== -1 ||
      path.indexOf("/ccna_sim_exam/embed/lab/") !== -1
    );
  }

  function moveHomeLinkToBottom() {
    if (!inTargetPage()) return;

    var main = document.querySelector("main.card") || document.querySelector("main");
    if (!main) return;

    var homeLink = main.querySelector("a.home-link");
    if (!homeLink) return;

    var originalActions = homeLink.closest(".actions");
    var nextWrap = main.querySelector(".next-wrap");
    var targetWrap = main.querySelector(".home-bottom-wrap");
    if (!targetWrap) {
      targetWrap = document.createElement("div");
      targetWrap.className = "home-bottom-wrap";
      targetWrap.style.marginTop = "18px";
      targetWrap.style.display = "flex";
      targetWrap.style.justifyContent = "flex-end";
      if (nextWrap && nextWrap.parentNode === main) {
        nextWrap.insertAdjacentElement("afterend", targetWrap);
      } else {
        main.appendChild(targetWrap);
      }
    }

    targetWrap.appendChild(homeLink);

    if (originalActions && originalActions.children.length === 0) {
      originalActions.remove();
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", moveHomeLinkToBottom);
  } else {
    moveHomeLinkToBottom();
  }
})();

(function () {
  "use strict";

  var OBJECTIVES_URL = "/CCNA-Study/data/ccna-exam-objectives-200-301-v1.1.json";
  var MANIFEST_URL = "/CCNA-Study/data/ccna-practice-questions-manifest.json";
  var MAP_BY_PATH = [
    { pathPart: "/ccna-study/ccna_questions/", mapUrl: "/CCNA-Study/data/ccna-question-topic-map.json" },
    { pathPart: "/ccna-study/ccna_d_d/", mapUrl: "/CCNA-Study/data/ccna-dnd-topic-map.json" },
    { pathPart: "/ccna-study/ccna_labs/", mapUrl: "/CCNA-Study/data/ccna-lab-topic-map.json" },
    { pathPart: "/ccna_sim_exam/embed/dnd/", mapUrl: "/CCNA-Study/data/ccna-dnd-topic-map.json" },
    { pathPart: "/ccna_sim_exam/embed/lab/", mapUrl: "/CCNA-Study/data/ccna-lab-topic-map.json" }
  ];

  function getSlugAndMap() {
    var pathRaw = location.pathname || "";
    if (
      pathRaw.toLowerCase() === "/sample" ||
      pathRaw.toLowerCase() === "/sample/" ||
      pathRaw.toLowerCase().indexOf("/sample?") === 0
    ) {
      try {
        var remembered = sessionStorage.getItem("ccnaLastRealPath");
        if (remembered) pathRaw = remembered;
      } catch (e) {}
    }
    var path = pathRaw.toLowerCase();
    var fileName = "";
    var dndRel = /\/ccna_d_d\/(.+\.html)$/.exec(path);
    var embedDndRel = /\/embed\/dnd\/(.+\.html)$/.exec(path);
    if (dndRel) {
      fileName = decodeURIComponent(dndRel[1]);
    } else if (embedDndRel) {
      fileName = decodeURIComponent(embedDndRel[1]);
    } else {
      var match = /\/([^/]+)\.html$/.exec(path);
      if (!match) return null;
      fileName = decodeURIComponent(match[1]) + ".html";
    }
    for (var i = 0; i < MAP_BY_PATH.length; i++) {
      if (path.indexOf(MAP_BY_PATH[i].pathPart) !== -1) {
        return { fileName: fileName, mapUrl: MAP_BY_PATH[i].mapUrl };
      }
    }
    return null;
  }

  function isCcnaQuestionPage(path) {
    return (path || "").indexOf("/ccna-study/ccna_questions/") !== -1;
  }

  function hubIndexForSlug(slug, manifest) {
    if (!slug || !manifest || !manifest.items) return null;
    for (var i = 0; i < manifest.items.length; i++) {
      if (manifest.items[i].slug === slug) return i + 1;
    }
    return null;
  }

  function versionLabelForHubIndex(index) {
    if (!index || index < 1) return null;
    if (index <= 300) return "Version: 1.1 2026";
    return "pre v1.0";
  }

  function renderObjectiveTag() {
    var target = getSlugAndMap();
    if (!target) return;
    var host = document.querySelector("main.card") || document.querySelector("main");
    if (!host || host.querySelector(".ccna-objective-tag")) return;

    var pathLower = (location.pathname || "").toLowerCase();
    try {
      if (
        pathLower === "/sample" ||
        pathLower === "/sample/" ||
        pathLower.indexOf("/sample?") === 0
      ) {
        var remembered = sessionStorage.getItem("ccnaLastRealPath");
        if (remembered) pathLower = remembered.toLowerCase();
      }
    } catch (e) {}
    var questionPage = isCcnaQuestionPage(pathLower);
    var slug = target.fileName.replace(/\.html$/i, "");

    var fetches = [
      fetch(OBJECTIVES_URL).then(function (r) { return r.json(); }),
      fetch(target.mapUrl).then(function (r) { return r.json(); })
    ];
    if (questionPage) {
      fetches.push(
        fetch(MANIFEST_URL)
          .then(function (r) { return r.json(); })
          .catch(function () { return null; })
      );
    }

    Promise.all(fetches).then(function (res) {
      var objectives = res[0];
      var map = res[1];
      var manifest = questionPage ? res[2] : null;
      if (!map || !map.assignments) return;

      var linkedIds = map.assignments[target.fileName] || [];
      var domainLookup = {};
      var objectiveLookup = {};
      (objectives.domains || []).forEach(function (domain) {
        domainLookup[domain.id] = domain.name;
        (domain.objectives || []).forEach(function (obj) {
          objectiveLookup[obj.id] = { domainName: domain.name, text: obj.text };
        });
      });

      var labels = linkedIds.map(function (id) {
        if (domainLookup[id]) return id + " (" + domainLookup[id] + ")";
        if (objectiveLookup[id]) return id + " (" + objectiveLookup[id].domainName + "): " + objectiveLookup[id].text;
        return null;
      }).filter(Boolean);

      if (!labels.length) labels = ["Unassigned objective (needs mapping)"];

      var box = document.createElement("div");
      box.className = "ccna-objective-tag";
      box.style.marginTop = "12px";
      box.style.padding = "10px 12px";
      box.style.borderRadius = "10px";
      box.style.border = "1px solid #2d3b5a";
      box.style.background = "#0f1729";
      box.style.color = "#b8c3d6";
      box.style.fontSize = "0.86rem";
      box.style.lineHeight = "1.45";

      var title = document.createElement("div");
      title.style.fontWeight = "700";
      title.style.color = "#e6edf3";
      title.style.marginBottom = "4px";
      title.textContent = "CCNA objective section";
      box.appendChild(title);

      if (questionPage) {
        var versionText = versionLabelForHubIndex(hubIndexForSlug(slug, manifest));
        if (versionText) {
          var versionRow = document.createElement("div");
          versionRow.style.marginBottom = "6px";
          versionRow.style.color = "#9fb0cc";
          versionRow.style.fontSize = "0.82rem";
          versionRow.textContent = versionText;
          box.appendChild(versionRow);
        }
      }

      labels.forEach(function (line) {
        var row = document.createElement("div");
        row.textContent = "• " + line;
        box.appendChild(row);
      });

      host.appendChild(box);
    }).catch(function () {
      // Silent fail keeps pages working if map files are absent.
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderObjectiveTag);
  } else {
    renderObjectiveTag();
  }
})();

/** CCNA timed exam embed (?examSim=1): hide chrome so iframe matches runner footer UX */
(function () {
  "use strict";

  function examSimActive() {
    try {
      return new URLSearchParams(location.search).get("examSim") === "1";
    } catch (e) {
      return false;
    }
  }

  function isCcnaLabPath() {
    var p = (location.pathname || "").toLowerCase();
    return (
      p.indexOf("/ccna-study/ccna_labs/") !== -1 ||
      p.indexOf("/ccna_sim_exam/embed/lab/") !== -1
    );
  }

  function applyExamSimEmbedStyles() {
    if (!examSimActive()) return;
    if (document.head.querySelector("style[data-bcc-exam-sim-embed]")) return;
    var s = document.createElement("style");
    s.setAttribute("data-bcc-exam-sim-embed", "1");
    var css =
      "nav.sim-nav{display:none!important}" + ".ccna-objective-tag{display:none!important}";
    if (isCcnaLabPath()) {
      css +=
        "body{padding-bottom:max(16px,env(safe-area-inset-bottom,0px))!important}";
    }
    s.textContent = css;
    document.head.appendChild(s);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", applyExamSimEmbedStyles);
  } else {
    applyExamSimEmbedStyles();
  }
})();

/** Google tag (gtag.js) on CCNA pages without static head snippet */
(function () {
  "use strict";
  var head = document.head || document.documentElement;
  var ga = document.createElement("script");
  ga.src = "/js/install-google-tag.js";
  head.appendChild(ga);
  var va = document.createElement("script");
  va.src = "/js/install-vercel-analytics.js";
  head.appendChild(va);
})();

/** Drag-and-drop touch hint above .layout on phones and tablets */
(function () {
  "use strict";
  var head = document.head || document.documentElement;
  if (head.querySelector('script[src*="dragdrop-touch-hint.js"]')) return;
  var hint = document.createElement("script");
  hint.src = "/js/dragdrop-touch-hint.js";
  hint.defer = true;
  head.appendChild(hint);
})();

/** Shared order-independent category validation for CCNA D&D pages */
(function () {
  "use strict";
  var p = (location.pathname || "").toLowerCase();
  if (p.indexOf("/ccna-study/ccna_d_d/") === -1) return;
  var head = document.head || document.documentElement;
  if (head.querySelector('script[src*="ccna-dnd-category-check.js"]')) return;
  var s = document.createElement("script");
  s.src = "/CCNA-Study/js/ccna-dnd-category-check.js";
  head.appendChild(s);
})();


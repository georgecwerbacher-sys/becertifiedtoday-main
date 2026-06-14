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
    var hash = location.hash || "";
    history.replaceState(null, "", mask + hash);
  } catch (e) {}
})();

/** Sync-load category D&D validation before inline page scripts (incl. masked /sample URLs). */
(function () {
  try {
    var pathLower = (location.pathname || "").toLowerCase();
    var remembered = "";
    try {
      remembered = (sessionStorage.getItem("ccnaLastRealPath") || "").toLowerCase();
    } catch (e) {}
    var onCcnaDnd =
      pathLower.indexOf("/ccna-study/ccna_d_d/") !== -1 ||
      pathLower.indexOf("/ccna_sim_exam/embed/dnd/") !== -1 ||
      remembered.indexOf("/ccna-study/ccna_d_d/") !== -1 ||
      remembered.indexOf("/ccna_sim_exam/embed/dnd/") !== -1;
    if (!onCcnaDnd) return;
    var src = "/CCNA-Study/js/ccna-dnd-category-check.js";
    if (document.querySelector('script[src="' + src + '"]')) return;
    document.write('<script src="' + src + '"><\/script>');
  } catch (e) {}
})();

(function () {
  "use strict";
  try {
    var hasHomeSample = false;
    try {
      hasHomeSample =
        !!sessionStorage.getItem("ccnaHomeSample") || !!sessionStorage.getItem("encorHomeSample");
    } catch (e) {}
    if (!hasHomeSample) return;
    var path = (location.pathname || "").toLowerCase();
    var remembered = "";
    try {
      remembered = (sessionStorage.getItem("ccnaLastRealPath") || "").toLowerCase();
    } catch (e) {}
    var onSamplePage =
      path.indexOf("/ccna-study/") !== -1 ||
      path.indexOf("/ccnp-encor-study/") !== -1 ||
      remembered.indexOf("/ccna-study/") !== -1 ||
      remembered.indexOf("/ccnp-encor-study/") !== -1;
    if (!onSamplePage) return;

    var kind = "";
    try {
      kind = sessionStorage.getItem("ccnpSampleKind") || "";
    } catch (e) {}

    var samplePath = path;
    if (
      (samplePath === "/sample" || samplePath === "/sample/") &&
      remembered.indexOf("/ccna-study/") === -1 &&
      remembered.indexOf("/ccnp-encor-study/") === -1
    ) {
      samplePath = remembered || samplePath;
    } else if (remembered.indexOf("/ccna-study/") !== -1 || remembered.indexOf("/ccnp-encor-study/") !== -1) {
      samplePath = remembered;
    }

    var onCcnaSample =
      samplePath.indexOf("/ccna-study/") !== -1 || samplePath.indexOf("/ccna_sim_exam/") !== -1;
    var onEncorSample = samplePath.indexOf("/ccnp-encor-study/") !== -1;
    var encorKind = kind.indexOf("encor") === 0 || kind === "labs" || kind === "drag";
    var onDragDropSample =
      samplePath.indexOf("/ccna-study/ccna_d_d/") !== -1 ||
      samplePath.indexOf("/ccna-study/ccna_samples/dragdrop-") !== -1 ||
      samplePath.indexOf("/ccnp-encor-study/ccnp-encor-drag-drop/") !== -1 ||
      samplePath.indexOf("/ccnp-encor-study/encor_samples/question-365") !== -1;

    var leadScript = null;
    if (onCcnaSample && (sessionStorage.getItem("ccnaHomeSample") || kind.indexOf("ccna") === 0)) {
      leadScript = "/js/ccna-lead-capture.js";
    } else if (onEncorSample && (sessionStorage.getItem("encorHomeSample") || encorKind)) {
      leadScript = "/js/encor-lead-capture.js";
    } else if (sessionStorage.getItem("ccnaHomeSample") || kind.indexOf("ccna") === 0) {
      leadScript = "/js/ccna-lead-capture.js";
    } else if (sessionStorage.getItem("encorHomeSample") || encorKind) {
      leadScript = "/js/encor-lead-capture.js";
    }
    if (
      leadScript &&
      !onDragDropSample &&
      !document.head.querySelector('script[src="' + leadScript + '"]')
    ) {
      var lead = document.createElement("script");
      lead.src = leadScript;
      lead.defer = true;
      (document.head || document.body).appendChild(lead);
    }

    if (!document.head.querySelector('script[src*="sample-lead-analytics.js"]')) {
      var analytics = document.createElement("script");
      analytics.src = "/js/sample-lead-analytics.js";
      analytics.defer = true;
      (document.head || document.body).appendChild(analytics);
    }

    if (document.head.querySelector('script[src*="cisco-home-sample-nav.js"]')) return;
    var s = document.createElement("script");
    s.src = "/js/cisco-home-sample-nav.js";
    s.defer = true;
    (document.body || document.head).appendChild(s);
  } catch (e) {}
})();

(function () {
  "use strict";
  function isSecplusSimStagingPath(p) {
    return (
      p.indexOf("/sec+_sim_hot_spot/pbq_production/") !== -1 ||
      p.indexOf("/sec+_sim_hot_spot/pending/") !== -1
    );
  }

  try {
    if (!sessionStorage.getItem("secplusHomeSample")) return;
    var path = (location.pathname || "").toLowerCase();
    var remembered = "";
    try {
      remembered = (sessionStorage.getItem("ccnaLastRealPath") || "").toLowerCase();
    } catch (e) {}
    if (isSecplusSimStagingPath(path) || isSecplusSimStagingPath(remembered)) return;
    var onSecplusPage =
      path.indexOf("/comp_tia_sec+/sec+_questions/") !== -1 ||
      path.indexOf("/comp_tia_sec+/sec+_sim_hot_spot/") !== -1 ||
      remembered.indexOf("/comp_tia_sec+/sec+_questions/") !== -1 ||
      remembered.indexOf("/comp_tia_sec+/sec+_sim_hot_spot/") !== -1;
    if (!onSecplusPage) return;
    if (!document.head.querySelector('script[src*="sample-lead-analytics.js"]')) {
      var analytics = document.createElement("script");
      analytics.src = "/js/sample-lead-analytics.js";
      analytics.defer = true;
      (document.head || document.body).appendChild(analytics);
    }

    if (document.head.querySelector('script[src*="secplus-sample-nav.js"]')) return;
    var s = document.createElement("script");
    s.src = "/COMP_TIA_SEC+/js/secplus-sample-nav.js";
    s.defer = true;
    (document.body || document.head).appendChild(s);
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

  var CCNA_OBJECTIVES_URL = "/CCNA-Study/data/ccna-exam-objectives-200-301-v1.1.json";
  var SECPLUS_OBJECTIVES_URL = "/COMP_TIA_SEC+/data/secplus-exam-objectives-sy0-701.json";
  var MANIFEST_URL = "/CCNA-Study/data/ccna-practice-questions-manifest.json";
  var MAP_BY_PATH = [
    { pathPart: "/ccna-study/ccna_questions/", mapUrl: "/CCNA-Study/data/ccna-question-topic-map.json", track: "ccna" },
    { pathPart: "/ccna-study/ccna_d_d/", mapUrl: "/CCNA-Study/data/ccna-dnd-topic-map.json", track: "ccna" },
    { pathPart: "/ccna-study/ccna_labs/", mapUrl: "/CCNA-Study/data/ccna-lab-topic-map.json", track: "ccna" },
    { pathPart: "/ccna_sim_exam/embed/dnd/", mapUrl: "/CCNA-Study/data/ccna-dnd-topic-map.json", track: "ccna" },
    { pathPart: "/ccna_sim_exam/embed/lab/", mapUrl: "/CCNA-Study/data/ccna-lab-topic-map.json", track: "ccna" },
    {
      pathPart: "/comp_tia_sec+/sec+_questions/",
      mapUrl: "/COMP_TIA_SEC+/data/secplus-question-topic-map.json",
      track: "secplus"
    }
  ];

  function getSlugAndMap() {
    var pathRaw = location.pathname || "";
    var pathLowerRaw = pathRaw.toLowerCase();
    if (
      pathLowerRaw === "/sample" ||
      pathLowerRaw === "/sample/" ||
      pathLowerRaw.indexOf("/sample?") === 0 ||
      pathLowerRaw === "/secplus-sample" ||
      pathLowerRaw === "/secplus-sample/"
    ) {
      try {
        var remembered = sessionStorage.getItem("ccnaLastRealPath");
        if (remembered) pathRaw = remembered;
      } catch (e) {}
    }
    var path = pathRaw.toLowerCase();
    try {
      path = decodeURIComponent(path);
    } catch (e) {}
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
        return {
          fileName: fileName,
          mapUrl: MAP_BY_PATH[i].mapUrl,
          track: MAP_BY_PATH[i].track || "ccna"
        };
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
    if (!host || host.querySelector(".ccna-objective-tag, .secplus-objective-tag, .question-topic-meta")) return;

    var pathLower = (location.pathname || "").toLowerCase();
    try {
      if (
        pathLower === "/sample" ||
        pathLower === "/sample/" ||
        pathLower.indexOf("/sample?") === 0 ||
        pathLower === "/secplus-sample" ||
        pathLower === "/secplus-sample/"
      ) {
        var remembered = sessionStorage.getItem("ccnaLastRealPath");
        if (remembered) pathLower = remembered.toLowerCase();
      }
    } catch (e) {}
    var questionPage = isCcnaQuestionPage(pathLower);
    var slug = target.fileName.replace(/\.html$/i, "");

    var objectivesUrl =
      target.track === "secplus" ? SECPLUS_OBJECTIVES_URL : CCNA_OBJECTIVES_URL;
    var sectionTitle =
      target.track === "secplus" ? "Security+ objective section" : "CCNA objective section";

    var fetches = [
      fetch(objectivesUrl).then(function (r) { return r.json(); }),
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
      box.className =
        target.track === "secplus" ? "secplus-objective-tag ccna-objective-tag" : "ccna-objective-tag";
      box.style.marginTop = "12px";
      box.style.padding = "10px 12px";
      box.style.borderRadius = "10px";
      box.style.border = "1px solid #2d3b5a";
      box.style.background = "#0f1729";
      box.style.color = "#b8c3d6";
      box.style.fontSize = "0.65rem";
      box.style.lineHeight = "1.45";

      if (target.track === "secplus") {
        var secplusVersion = document.createElement("div");
        secplusVersion.className = "secplus-objective-tag__version";
        secplusVersion.style.marginBottom = "6px";
        secplusVersion.style.color = "#9fb0cc";
        secplusVersion.style.fontSize = "0.62rem";
        secplusVersion.textContent = "Version: 1.1 2026";
        box.appendChild(secplusVersion);
      }

      var title = document.createElement("div");
      if (target.track === "secplus") title.className = "secplus-objective-tag__title";
      title.style.fontWeight = "700";
      title.style.color = "#e6edf3";
      title.style.marginBottom = "4px";
      title.textContent = sectionTitle;
      box.appendChild(title);

      if (questionPage) {
        var versionText = versionLabelForHubIndex(hubIndexForSlug(slug, manifest));
        if (versionText) {
          var versionRow = document.createElement("div");
          versionRow.style.marginBottom = "6px";
          versionRow.style.color = "#9fb0cc";
          versionRow.style.fontSize = "0.62rem";
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

  function pathLooksLikeCcnaLab(p) {
    p = String(p || "").toLowerCase();
    return (
      p.indexOf("/ccna-study/ccna_labs/") !== -1 ||
      p.indexOf("/ccna_sim_exam/embed/lab/") !== -1
    );
  }

  function isCcnaLabPath() {
    if (pathLooksLikeCcnaLab(location.pathname)) return true;
    try {
      if (pathLooksLikeCcnaLab(sessionStorage.getItem("ccnaLastRealPath"))) return true;
    } catch (e) {}
    return !!document.querySelector(".cli-modal-overlay .scrollback-area");
  }

  function bctCliBannerContextActive() {
    var container = window.cliLabContainer;
    if (container && typeof container.isBctCliBannerContext === "function") {
      return container.isBctCliBannerContext();
    }
    return isCcnaLabPath();
  }

  var BCT_CLI_BANNER_LAB_CSS =
    ".terminal .line-boot{white-space:pre-wrap;word-break:break-word;color:#94a3b8;font-size:.82rem;line-height:1.45;margin-bottom:10px;padding:10px 12px;border-radius:6px;background:#0a0e14;border:1px solid #1e293b}";

  function injectBctCliBannerLabStyles() {
    if (!bctCliBannerContextActive() || !isCcnaLabPath()) return;
    if (document.head.querySelector("style[data-bcc-cli-banner-lab]")) return;
    var s = document.createElement("style");
    s.setAttribute("data-bcc-cli-banner-lab", "1");
    s.textContent = BCT_CLI_BANNER_LAB_CSS;
    document.head.appendChild(s);
  }

  function applyExamSimEmbedStyles() {
    if (!examSimActive()) return;
    if (document.head.querySelector("style[data-bcc-exam-sim-embed]")) return;
    var s = document.createElement("style");
    s.setAttribute("data-bcc-exam-sim-embed", "1");
    var css =
      "nav.sim-nav{display:none!important}" +
      ".ccna-objective-tag{display:none!important}" +
      "#showBtn,.nav-show-answer,.answer-side-actions .nav-show-answer{display:none!important}";
    if (isCcnaLabPath()) {
      css +=
        "body{padding-bottom:max(16px,env(safe-area-inset-bottom,0px))!important}" +
        BCT_CLI_BANNER_LAB_CSS;
    }
    s.textContent = css;
    document.head.appendChild(s);
  }

  function wireExamSimCliOpenBanner() {
    if (!bctCliBannerContextActive() || !isCcnaLabPath()) return;
    var container = window.cliLabContainer;
    if (!container || typeof container.showExamSimCliBanner !== "function") return;

    function onOverlayOpened(overlay) {
      if (!overlay || !overlay.classList.contains("is-open")) return;
      requestAnimationFrame(function () {
        var scroll = overlay.querySelector(".scrollback-area");
        if (scroll) container.showExamSimCliBanner(scroll);
      });
    }

    document.querySelectorAll(".cli-modal-overlay").forEach(function (overlay) {
      if (overlay.dataset.bctExamSimCliBanner === "1") return;
      overlay.dataset.bctExamSimCliBanner = "1";
      new MutationObserver(function (mutations) {
        mutations.forEach(function (m) {
          if (m.attributeName === "class") onOverlayOpened(overlay);
        });
      }).observe(overlay, { attributes: true, attributeFilter: ["class"] });
      if (overlay.classList.contains("is-open")) onOverlayOpened(overlay);
    });
  }

  function bootExamSimEmbed() {
    applyExamSimEmbedStyles();
    if (window.cliLabContainer && typeof window.cliLabContainer.initBctCliBanner === "function") {
      window.cliLabContainer.initBctCliBanner();
      return;
    }
    injectBctCliBannerLabStyles();
    wireExamSimCliOpenBanner();
  }

  function scheduleBootExamSimEmbed() {
    function run() {
      bootExamSimEmbed();
    }
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", run, { once: true });
      return;
    }
    if (document.querySelector(".cli-modal-overlay")) {
      run();
      return;
    }
    document.addEventListener("DOMContentLoaded", run, { once: true });
  }

  scheduleBootExamSimEmbed();
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

/** Security+ paid content: load portal storage + gate on question/sim pages. */
(function () {
  "use strict";
  function isSecplusSimStagingPath(pathLower) {
    return (
      pathLower.indexOf("/sec+_sim_hot_spot/pbq_production/") !== -1 ||
      pathLower.indexOf("/sec+_sim_hot_spot/pending/") !== -1
    );
  }

  var p = (location.pathname || "").toLowerCase();
  if (p.indexOf("/comp_tia_sec+/") === -1) return;
  if (p.indexOf("/sec+_samples/") !== -1) return;
  if (isSecplusSimStagingPath(p)) return;
  if (/sec\+_training_portal\.html$/i.test(p)) return;
  if (/secplus-portal-(magic|request-link|restore-access)\.html$/i.test(p)) return;
  if (
    p.indexOf("/sec+_questions/") === -1 &&
    p.indexOf("/sec+_sim_hot_spot/") === -1 &&
    p.indexOf("/sec+_d_d/") === -1 &&
    p.indexOf("/sec+_labs/") === -1
  ) {
    return;
  }

  function appendScript(src, next) {
    if (document.querySelector('script[src="' + src + '"]')) {
      if (next) next();
      return;
    }
    var s = document.createElement("script");
    s.src = src;
    s.onload = function () {
      if (next) next();
    };
    s.onerror = function () {
      if (next) next();
    };
    (document.head || document.documentElement).appendChild(s);
  }

  appendScript("/COMP_TIA_SEC+/js/secplus-portal-storage.js", function () {
    appendScript("/COMP_TIA_SEC+/js/secplus-portal-gate.js");
  });
})();

/** CCNA paid content: load portal storage + gate on question/D&D/lab pages. */
(function () {
  "use strict";

  var p = (location.pathname || "").toLowerCase();
  if (
    p.indexOf("/ccna-study/ccna_questions/") === -1 &&
    p.indexOf("/ccna-study/ccna_d_d/") === -1 &&
    p.indexOf("/ccna-study/ccna_labs/") === -1 &&
    p.indexOf("/ccna_sim_exam/embed/dnd/") === -1 &&
    p.indexOf("/ccna_sim_exam/embed/lab/") === -1
  ) {
    return;
  }

  function appendScript(src, next) {
    if (document.querySelector('script[src="' + src + '"]')) {
      if (next) next();
      return;
    }
    var s = document.createElement("script");
    s.src = src;
    s.onload = function () {
      if (next) next();
    };
    s.onerror = function () {
      if (next) next();
    };
    (document.head || document.documentElement).appendChild(s);
  }

  appendScript("/CCNA-Study/js/ccna-portal-30d-storage.js", function () {
    appendScript("/CCNA-Study/js/ccna-portal-gate.js");
  });
})();

/** ENCOR paid content: load portal storage + gate on question/drag-drop/lab pages. */
(function () {
  "use strict";

  var p = (location.pathname || "").toLowerCase();
  if (
    p.indexOf("/ccnp-encor-study/encor_questions/") === -1 &&
    p.indexOf("/ccnp-encor-study/ccnp-encor-drag-drop/") === -1 &&
    p.indexOf("/ccnp-encor-study/ccnp-encor-labs/") === -1
  ) {
    return;
  }

  function appendScript(src, next) {
    if (document.querySelector('script[src="' + src + '"]')) {
      if (next) next();
      return;
    }
    var s = document.createElement("script");
    s.src = src;
    s.onload = function () {
      if (next) next();
    };
    s.onerror = function () {
      if (next) next();
    };
    (document.head || document.documentElement).appendChild(s);
  }

  appendScript("/CCNP-ENCOR-Study/js/encor-portal-storage.js", function () {
    appendScript("/CCNP-ENCOR-Study/js/encor-portal-gate.js");
  });
})();

/** Security+ timed exam embed (?examSim=1): hide question chrome in iframe runner */
(function () {
  "use strict";

  function examSimActive() {
    try {
      return new URLSearchParams(location.search).get("examSim") === "1";
    } catch (e) {
      return false;
    }
  }

  function isSecplusPaidPath() {
    var p = (location.pathname || "").toLowerCase();
    return (
      p.indexOf("/comp_tia_sec+/sec+_questions/") !== -1 ||
      p.indexOf("/comp_tia_sec+/sec+_sim_hot_spot/") !== -1
    );
  }

  function applySecplusExamSimEmbedStyles() {
    if (!examSimActive() || !isSecplusPaidPath()) return;
    if (document.head.querySelector("style[data-bcc-secplus-exam-sim-embed]")) return;
    var s = document.createElement("style");
    s.setAttribute("data-bcc-secplus-exam-sim-embed", "1");
    s.textContent =
      ".site-logo-corner{display:none!important}" +
      ".question-nav{display:none!important}" +
      ".secplus-objective-tag{display:none!important}" +
      "a.nav-home{display:none!important}" +
      "#showBtn,.nav-show-answer,.answer-side-actions .nav-show-answer{display:none!important}" +
      ".review-mark-box{display:none!important}";
    document.head.appendChild(s);
  }

  function bootSecplusExamSimEmbedStyles() {
    if (!examSimActive() || !isSecplusPaidPath()) return;
    applySecplusExamSimEmbedStyles();
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", applySecplusExamSimEmbedStyles);
    }
  }

  bootSecplusExamSimEmbedStyles();
})();

/** Guest sample pages: exam prep home links (not gated Training Portal). */
(function () {
  "use strict";

  function isGuestSamplePath() {
    var path = (location.pathname || "").toLowerCase();
    return (
      path.indexOf("/ccna-study/ccna_samples/") !== -1 ||
      path.indexOf("/ccnp-encor-study/encor_samples/") !== -1 ||
      path.indexOf("/comp_tia_sec+/sec+_samples/") !== -1 ||
      path === "/ccna-study/ccna_labs/cli-lab-trunk_lacp.html" ||
      path === "/ccna-study/ccna_labs/cli-lab-vlan-sim.html"
    );
  }

  function rewriteGuestHomeLinks() {
    if (!isGuestSamplePath()) return;

    var map = [
      { re: /\/ccna-study\/ccna_training_portal\.html/i, href: "/ccna-home.html", label: "CCNA exam prep" },
      { re: /\/ccnp-encor-study\/encor_training_portal\.html/i, href: "/ccnp-home.html", label: "ENCOR exam prep" },
      { re: /\/comp_tia_sec+\/sec\+_training_portal\.html/i, href: "/comptia-sec+-home.html", label: "Security+ exam prep" },
    ];

    document.querySelectorAll("a[href]").forEach(function (a) {
      var href = a.getAttribute("href") || "";
      for (var i = 0; i < map.length; i++) {
        if (map[i].re.test(href)) {
          a.setAttribute("href", map[i].href);
          if (a.classList.contains("sim-nav-home") || a.classList.contains("nav-home")) {
            a.textContent = map[i].label;
          }
          break;
        }
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", rewriteGuestHomeLinks);
  } else {
    rewriteGuestHomeLinks();
  }
})();

/** ENCOR guest samples: apply Home tab after URL mask (labs / ENCOR_Samples pages). */
(function () {
  "use strict";

  function boot() {
    if (typeof window.applyEncorSampleGuestChrome === "function") {
      window.applyEncorSampleGuestChrome();
    }
  }

  var head = document.head || document.documentElement;
  if (head.querySelector('script[src*="encor-sample-guest.js"]')) {
    boot();
    return;
  }

  var s = document.createElement("script");
  s.src = "/js/encor-sample-guest.js";
  s.onload = boot;
  head.appendChild(s);
})();

/** Guest samples (CCNA, ENCOR, SEC+): top-left logo only (no link); remove top-right corner logos. */
(function () {
  "use strict";

  function samplePathMatch(path) {
    return (
      path.indexOf("/ccna-study/ccna_samples/") !== -1 ||
      path.indexOf("/ccnp-encor-study/encor_samples/") !== -1 ||
      path.indexOf("/comp_tia_sec+/sec+_samples/") !== -1 ||
      path === "/ccna-study/ccna_labs/cli-lab-trunk_lacp.html" ||
      path === "/ccna-study/ccna_labs/cli-lab-vlan-sim.html"
    );
  }

  function isSampleExperience() {
    var path = (location.pathname || "").toLowerCase();
    var remembered = "";
    try {
      remembered = (sessionStorage.getItem("ccnaLastRealPath") || "").toLowerCase();
    } catch (e) {}
    if (samplePathMatch(path) || samplePathMatch(remembered)) return true;
    try {
      if (sessionStorage.getItem("ccnaHomeSample")) return true;
      if (sessionStorage.getItem("encorHomeSample")) return true;
      if (sessionStorage.getItem("secplusHomeSample")) return true;
      if (sessionStorage.getItem("ccnpUrlMaskPath") === "/sample") return true;
      if (sessionStorage.getItem("secplusUrlMaskPath") === "/secplus-sample") return true;
    } catch (e) {}
    try {
      if (new URLSearchParams(location.search).get("sample") === "1") return true;
    } catch (e) {}
    return false;
  }

  function readSampleSessionHome(key, fallback) {
    try {
      var raw = sessionStorage.getItem(key);
      if (!raw) return fallback;
      var session = JSON.parse(raw);
      if (session && session.finishHome) return session.finishHome;
    } catch (e) {}
    return fallback;
  }

  function sampleLogoHomeHref() {
    if (/\/CCNA-Study\/CCNA_labs\//i.test(String(location.pathname || ""))) {
      return "/CCNA-Study/CCNA_Training_Portal.html";
    }
    try {
      if (sessionStorage.getItem("ccnaHomeSample")) {
        return readSampleSessionHome("ccnaHomeSample", "/ccna-home.html");
      }
      if (sessionStorage.getItem("encorHomeSample")) {
        return readSampleSessionHome("encorHomeSample", "/ccnp-home.html");
      }
      var kind = sessionStorage.getItem("ccnpSampleKind") || "";
      if (kind.indexOf("ccna") === 0) return "/ccna-home.html";
      if (kind.indexOf("encor") === 0) return "/ccnp-home.html";
    } catch (e) {}
    return null;
  }

  function sampleLogoAriaLabel(href) {
    if (href === "/CCNA-Study/CCNA_Training_Portal.html") return "CCNA training portal";
    if (href === "/ccna-home.html") return "Back to CCNA home";
    if (href === "/ccnp-home.html") return "Back to ENCOR home";
    return "Back to home";
  }

  function stripSampleLogoLinks() {
    document.querySelectorAll("a.site-logo-corner").forEach(function (a) {
      var span = document.createElement("span");
      span.className = a.className;
      span.setAttribute("aria-hidden", "true");
      span.innerHTML = a.innerHTML;
      a.parentNode.replaceChild(span, a);
    });
  }

  function wireSampleLogoLinks() {
    var href = sampleLogoHomeHref();
    if (!href) {
      stripSampleLogoLinks();
      return;
    }
    document.querySelectorAll("a.site-logo-corner").forEach(function (a) {
      a.href = href;
      a.setAttribute("aria-label", sampleLogoAriaLabel(href));
      a.removeAttribute("aria-hidden");
    });
  }

  function injectSampleLogoStyles() {
    if (document.head.querySelector("style[data-bcc-sample-logo]")) return;
    var s = document.createElement("style");
    s.setAttribute("data-bcc-sample-logo", "1");
    s.textContent =
      "body.bcc-sample-experience .site-logo-corner," +
      "body.ccna-static-sample .site-logo-corner," +
      "body.ccna-sample-guest-ui .site-logo-corner," +
      "body.encor-static-sample .site-logo-corner," +
      "body.encor-sample-guest-ui .site-logo-corner," +
      "body.secplus-static-sample .site-logo-corner," +
      "body.secplus-sample-guest-ui .site-logo-corner{" +
      "display:inline-flex!important;" +
      "position:fixed!important;" +
      "top:max(12px,env(safe-area-inset-top,0px))!important;" +
      "left:max(12px,env(safe-area-inset-left,0px))!important;" +
      "right:auto!important;" +
      "bottom:auto!important;" +
      "align-self:auto!important;" +
      "margin:0!important;" +
      "background:transparent!important;" +
      "border:none!important;" +
      "padding:0!important;" +
      "backdrop-filter:none!important;" +
      "}" +
      "body.bcc-sample-experience span.site-logo-corner," +
      "body.ccna-static-sample span.site-logo-corner," +
      "body.ccna-sample-guest-ui span.site-logo-corner," +
      "body.encor-static-sample span.site-logo-corner," +
      "body.encor-sample-guest-ui span.site-logo-corner," +
      "body.secplus-static-sample span.site-logo-corner," +
      "body.secplus-sample-guest-ui span.site-logo-corner{" +
      "pointer-events:none!important;" +
      "cursor:default!important;" +
      "}" +
      "body.bcc-sample-experience a.site-logo-corner," +
      "body.ccna-static-sample a.site-logo-corner," +
      "body.ccna-sample-guest-ui a.site-logo-corner," +
      "body.encor-static-sample a.site-logo-corner," +
      "body.encor-sample-guest-ui a.site-logo-corner{" +
      "pointer-events:auto!important;" +
      "cursor:pointer!important;" +
      "text-decoration:none!important;" +
      "color:inherit!important;" +
      "}" +
      "body.bcc-sample-experience a.site-logo-corner:focus-visible," +
      "body.ccna-static-sample a.site-logo-corner:focus-visible," +
      "body.ccna-sample-guest-ui a.site-logo-corner:focus-visible," +
      "body.encor-static-sample a.site-logo-corner:focus-visible," +
      "body.encor-sample-guest-ui a.site-logo-corner:focus-visible{" +
      "outline:2px solid #4f84d8!important;" +
      "outline-offset:3px!important;" +
      "}";
    document.head.appendChild(s);
  }

  function applySampleLogoChrome() {
    if (window.cliLabContainer && typeof window.cliLabContainer.initCcnaLabTopChrome === "function") {
      window.cliLabContainer.initCcnaLabTopChrome();
    }
    if (!isSampleExperience()) return;
    document.body.classList.add("bcc-sample-experience");
    injectSampleLogoStyles();
    wireSampleLogoLinks();
    if (window.cliLabContainer && typeof window.cliLabContainer.initCcnaLabTopChrome === "function") {
      window.cliLabContainer.initCcnaLabTopChrome();
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", applySampleLogoChrome);
  } else {
    applySampleLogoChrome();
  }
})();


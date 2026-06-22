/**
 * Build mixed Security+ timed-test queue from topic map + secplus-test-simulation-blueprint.json.
 */
(function () {
  "use strict";

  var TOPIC_MAP_URL = "/COMP_TIA_SEC+/data/secplus-question-topic-map.json";
  var BLUEPRINT_URL = "/COMP_TIA_SEC+/data/secplus-test-simulation-blueprint.json";
  var FREE_BLUEPRINT_URL = "/COMP_TIA_SEC+/data/secplus-free-simulation-blueprint.json";
  var FREE_QUEUE_URL = "/COMP_TIA_SEC+/data/free-simulation/queue.json";
  var FREE_SIM_DURATION_MINUTES = 35;
  /** Mirror of data/free-simulation/queue.json — sync start, no fetch at exam launch. */
  var FREE_SIM_QUEUE_ITEMS = [
    { kind: "question", url: "/COMP_TIA_SEC+/SEC+_Questions/aaa-accounting-login-time-tracking.html" },
    { kind: "question", url: "/COMP_TIA_SEC+/SEC+_Questions/accounting-fake-vendor-invoice-scam.html" },
    { kind: "question", url: "/COMP_TIA_SEC+/SEC+_Questions/ai-ticketing-tool-intellectual-property.html" },
    { kind: "question", url: "/COMP_TIA_SEC+/SEC+_Questions/admin-credential-guessing-user-activity-logs.html" },
    { kind: "question", url: "/COMP_TIA_SEC+/SEC+_Questions/annual-risk-assessment-recurring.html" },
    { kind: "question", url: "/COMP_TIA_SEC+/SEC+_Questions/accountant-ftp-bank-encryption-confidentiality.html" },
    { kind: "question", url: "/COMP_TIA_SEC+/SEC+_Questions/accounting-login-watering-hole-download.html" },
    { kind: "question", url: "/COMP_TIA_SEC+/SEC+_Questions/air-gapped-firmware-manual-updates.html" },
    { kind: "question", url: "/COMP_TIA_SEC+/SEC+_Questions/aggregate-logs-alerts-siem.html" },
    { kind: "question", url: "/COMP_TIA_SEC+/SEC+_Questions/application-out-of-scope-management-attestation.html" },
    { kind: "question", url: "/COMP_TIA_SEC+/SEC+_Questions/after-login-granting-access-authorization.html" },
    { kind: "question", url: "/COMP_TIA_SEC+/SEC+_Questions/admin-access-bastion-host.html" },
    { kind: "question", url: "/COMP_TIA_SEC+/SEC+_Questions/air-gapped-network-data-loss-removable-devices.html" },
    { kind: "question", url: "/COMP_TIA_SEC+/SEC+_Questions/alert-fatigue-false-positive-ignored.html" },
    { kind: "question", url: "/COMP_TIA_SEC+/SEC+_Questions/auditor-risk-management-policies-first.html" },
    { kind: "question", url: "/COMP_TIA_SEC+/SEC+_Questions/aup-managerial-control-type.html" },
    { kind: "question", url: "/COMP_TIA_SEC+/SEC+_Questions/admin-phishing-email-server-password.html" },
    { kind: "question", url: "/COMP_TIA_SEC+/SEC+_Questions/application-availability-load-balancing-replace-server.html" },
    { kind: "question", url: "/COMP_TIA_SEC+/SEC+_Questions/always-on-vpn-fail-host-content-filtering.html" },
    { kind: "question", url: "/COMP_TIA_SEC+/SEC+_Questions/aup-integrity-ethical-behavior-expectations.html" },
    {
      kind: "sim",
      url: "/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/dark-web-account-protection/dark-web-account-protection.html",
    },
  ];
  var SIM_BASE = "/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/";

  function simUrl(file) {
    var path = String(file || "").replace(/^\//, "");
    if (path.indexOf("PBQ_Production/") === 0) {
      return SIM_BASE + path;
    }
    return SIM_BASE + path;
  }
  var MCQ_BASE = "/COMP_TIA_SEC+/SEC+_Questions/";

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

  function pickRandom(list, n) {
    return shuffle(list).slice(0, Math.min(n, list.length));
  }

  function slugFromAssignmentKey(key) {
    return String(key || "").replace(/\.html$/i, "");
  }

  function mcqUrl(slug) {
    return MCQ_BASE + slug + ".html";
  }

  function domainMajorFromSlug(assignments, slug) {
    var ids = assignments[slug] || assignments[slug + ".html"] || [];
    if (!Array.isArray(ids) || !ids.length) return "__none__";
    for (var i = 0; i < ids.length; i++) {
      var maj = String(ids[i]).split(".")[0];
      if (/^[1-5]$/.test(maj)) return maj;
    }
    return "__none__";
  }

  function buildQueueBalancedByDomain(topicMap, bp) {
    bp = bp || {};
    var assignments = (topicMap && topicMap.assignments) || {};
    var mcqN = bp.multipleChoiceCount != null ? bp.multipleChoiceCount : 20;
    var perDomain = Math.max(1, Math.floor(mcqN / 5));
    var buckets = { 1: [], 2: [], 3: [], 4: [], 5: [], __none__: [] };

    Object.keys(assignments).forEach(function (key) {
      var slug = slugFromAssignmentKey(key);
      if (!slug) return;
      var maj = domainMajorFromSlug(assignments, key);
      if (!buckets[maj]) maj = "__none__";
      buckets[maj].push(slug);
    });

    var picked = [];
    ["1", "2", "3", "4", "5"].forEach(function (maj) {
      picked = picked.concat(pickRandom(buckets[maj], perDomain));
    });
    if (picked.length < mcqN) {
      var rest = [];
      Object.keys(buckets).forEach(function (k) {
        buckets[k].forEach(function (slug) {
          if (picked.indexOf(slug) === -1) rest.push(slug);
        });
      });
      picked = picked.concat(pickRandom(rest, mcqN - picked.length));
    }
    picked = picked.slice(0, mcqN);

    var simFiles = Array.isArray(bp.simFiles) && bp.simFiles.length ? bp.simFiles : [];
    var simUrls = simFiles.map(simUrl);

    var queue = picked
      .map(function (slug) {
        return { kind: "question", url: mcqUrl(slug) };
      })
      .concat(
        simUrls.map(function (url) {
          return { kind: "sim", url: url };
        })
      );

    return shuffle(queue);
  }

  function buildQueue(topicMap, bp) {
    if (bp && bp.balancedDomains) {
      return buildQueueBalancedByDomain(topicMap, bp);
    }
    bp = bp || {};
    var assignments = (topicMap && topicMap.assignments) || {};
    var slugPool = Object.keys(assignments)
      .map(slugFromAssignmentKey)
      .filter(Boolean);

    var mcqN = bp.multipleChoiceCount != null ? bp.multipleChoiceCount : 90;
    var simFiles = Array.isArray(bp.simFiles) && bp.simFiles.length ? bp.simFiles : [];

    var questionSlugs = pickRandom(slugPool, mcqN);
    var simUrls = simFiles.map(simUrl);

    var queue = []
      .concat(
        questionSlugs.map(function (slug) {
          return { kind: "question", url: mcqUrl(slug) };
        })
      )
      .concat(
        simUrls.map(function (url) {
          return { kind: "sim", url: url };
        })
      );

    return shuffle(queue);
  }

  function normalizeFreeQueueItems(raw) {
    if (!Array.isArray(raw)) return [];
    return raw
      .map(function (item) {
        if (!item || !item.url) return null;
        return {
          kind: item.kind === "sim" ? "sim" : "question",
          url: String(item.url),
        };
      })
      .filter(Boolean);
  }

  function getFreeSimulationPackSync() {
    return {
      topicMap: null,
      bp: null,
      queue: FREE_SIM_QUEUE_ITEMS.map(function (item) {
        return { kind: item.kind, url: item.url };
      }),
      durationMinutes: FREE_SIM_DURATION_MINUTES,
    };
  }

  function loadFreeSimulationQueue() {
    var embedded = getFreeSimulationPackSync();
    if (embedded.queue.length) {
      return Promise.resolve(embedded);
    }
    return Promise.all([
      fetch(FREE_QUEUE_URL, { cache: "no-store" }).then(function (r) {
        if (!r.ok) throw new Error("free queue");
        return r.json();
      }),
      fetch(FREE_BLUEPRINT_URL, { cache: "no-store" }).then(function (r) {
        if (!r.ok) throw new Error("blueprint");
        return r.json();
      }),
    ]).then(function (res) {
      var pack = res[0];
      var bp = res[1];
      var queue = normalizeFreeQueueItems(pack.queue);
      if (!queue.length) throw new Error("empty");
      return {
        topicMap: null,
        bp: bp,
        queue: queue,
        durationMinutes:
          pack.durationMinutes != null
            ? pack.durationMinutes
            : bp.durationMinutes != null
              ? bp.durationMinutes
              : FREE_SIM_DURATION_MINUTES,
      };
    });
  }

  function loadConfigAndBlueprint(options) {
    options = options || {};
    var blueprintUrl = options.blueprintUrl || BLUEPRINT_URL;
    return Promise.all([
      fetch(TOPIC_MAP_URL, { cache: "no-store" }).then(function (r) {
        if (!r.ok) throw new Error("topic map");
        return r.json();
      }),
      fetch(blueprintUrl, { cache: "no-store" }).then(function (r) {
        if (!r.ok) throw new Error("blueprint");
        return r.json();
      }),
    ]).then(function (res) {
      var topicMap = res[0];
      var bp = res[1];
      return {
        topicMap: topicMap,
        bp: bp,
        queue: buildQueue(topicMap, bp),
        durationMinutes: bp.durationMinutes != null ? bp.durationMinutes : 90,
      };
    });
  }

  window.SECPLUS_TEST_SIM_BUILD = {
    buildQueue: buildQueue,
    buildQueueBalancedByDomain: buildQueueBalancedByDomain,
    loadConfigAndBlueprint: loadConfigAndBlueprint,
    loadFreeSimulationQueue: loadFreeSimulationQueue,
    getFreeSimulationPackSync: getFreeSimulationPackSync,
    FREE_BLUEPRINT_URL: FREE_BLUEPRINT_URL,
    FREE_QUEUE_URL: FREE_QUEUE_URL,
  };
})();

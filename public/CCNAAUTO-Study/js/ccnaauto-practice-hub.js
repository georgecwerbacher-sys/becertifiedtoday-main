(function () {
  "use strict";

  var UTIL = window.BCC_QUESTION_BANK;
  var KEY = "ccnaautoPractice";
  var BANK_SIZE = UTIL.DEFAULT_BANK_SIZE;
  var FILTER_BANK_ID = "filter";
  var BLUEPRINT_URL = "/CCNAAUTO-Study/data/ccnaauto-practice-bank-blueprint.json";
  var TOPIC_MAP_URL = "/CCNAAUTO-Study/data/ccnaauto-question-topic-map.json";
  var TRACKER_URL = "/CCNAAUTO-Study/data/ccnaauto-question-topic-tracker.json";
  var QUESTIONS_BASE = "/CCNAAUTO-Study/CCNAAUTO_Questions/";

  window.CCNAAUTO_PRACTICE = window.CCNAAUTO_PRACTICE || {};
  window.CCNAAUTO_PRACTICE.SLUGS = [
    "rest-constraint-no-client-context-server",
    "cisco-dna-center-controller-level-management",
    "bare-metal-application-deployment-characteristics",
    "ios-xe-restconf-basic-authentication",
    "tdd-refactoring-existing-test-coverage",
    "bash-redirect-output-to-file",
    "git-merge-unified-history",
    "jenkins-cicd-automation-tool",
    "rest-api-large-results-pagination",
    "edge-computing-reduces-latency",
    "unified-diff-hunk-header-line",
    "cucm-api-voicemail-port-data",
    "docker-app-security-benefits",
    "package-updates-local-server-proxy",
    "yang-interface-encoding-formats",
    "safely-store-api-keys",
    "virtual-platform-hypervisor",
    "rest-api-valid-response-status-code",
    "routing-protocol-traffic-control-plane",
    "json-xml-true-statements",
    "restconf-401-check-authentication-credentials",
    "repeated-code-use-functions",
    "hostile-data-to-interpreter-injection",
    "cicd-pipeline-minimal-manual-interaction",
    "ansible-ios-running-config-backup",
    "artifact-repository-cicd-pipeline-role",
    "cisco-virl-network-simulation-purpose",
    "routing-table-destination-next-hop-interface",
    "python-filter-fruit-nested-json-output",
    "rest-api-incorrect-payload-status-code-400",
    "mac-address-unique-network-interface-lan",
    "rest-api-json-parse-error-formatting-issue",
    "version-control-advantages-choose-two",
    "webhook-interacting-application-descriptions-choose-two",
    "default-gateway-description-true",
    "git-delete-local-branch-force-experiment",
    "netconf-default-port-830",
    "tdd-concepts-choose-two",
    "intermittent-server-connection-device-at-fault",
    "cisco-devnet-resources-choose-two",
    "platform-run-directly-using-hypervisor",
    "network-programmability-scalable-replicable-provisioning",
    "bash-script-create-next-missing-directory",
    "unified-diff-chunk-start-example",
    "yang-interface-supported-encoding-formats-choose-two",
    "python-requests-success-status-code-expression",
    "git-clone-creates-local-repository-copy",
    "python-function-returns-dnac-auth-token",
    "nat-types-static-dynamic-choose-two",
    "python-json-loads-returns-dict",
    "firewall-controls-traffic-security-rules",
    "ucs-sdk-ucshandle-instance-code-snippet",
    "xml-books-equivalent-json",
    "devnet-sandbox-development-lab-resource",
    "webex-rooms-sortby-lastactivity",
    "asynchronous-api-call-traits-choose-two",
    "python-unittest-asserttrue-function",
    "ios-xe-restconf-default-data-encoding",
    "network-interface-hardware-address-example",
    "webex-messages-401-authorization-header",
    "devops-foundational-principles-choose-two",
    "meraki-api-use-cases-choose-two",
    "api-network-configuration-benefits-choose-two",
    "version-control-branching-collaboration-choose-two",
    "dns-cname-alias-record",
    "basic-auth-base64-credential-string",
    "restconf-patch-logging-severity-204",
    "netconf-operations-restconf-get-choose-two",
    "unified-diff-single-request-timeout-choose-two",
    "dna-center-log-bundle-voice-quality",
    "yang-ethernet-interface-management",
    "docker-container-host-port-connection",
    "cisco-amp-vulnerable-software-api",
    "webhook-notifications-http-post",
    "code-review-before-merge",
    "dna-center-network-device-get-json-fill",
    "topology-subnet-serial-statements-choose-two",
    "restconf-hostname-get-remove-accept-header",
    "nxos-python-sdk-loopback-json-effects-choose-two",
    "ansible-ios-vlan-trunk-effects-choose-two",
    "mvc-design-pattern-advantages-choose-two",
    "ios-xe-model-driven-programmability-gnmi",
    "tdd-first-task-failing-test",
    "yang-infrastructure-automation-advantages-choose-two",
    "version-control-merge-conflict-resolution",
    "git-checkout-new-bugfix-branch",
    "dns-directory-lookup-ip-hostnames",
    "client-server-subnet-separation-reasons-choose-two",
    "router-transports-between-broadcast-domains",
    "yang-union-ippeer-single-address-value",
    "ansible-ios-startup-config-backup-show-conf",
    "rest-api-401-requires-authentication",
    "icmp-time-exceeded-routing-loop",
  ];
  window.CCNAAUTO_PRACTICE._topicAssignments = null;
  window.CCNAAUTO_PRACTICE._blueprint = null;
  window.CCNAAUTO_PRACTICE._tracker = null;

  window.CCNAAUTO_PRACTICE._loadPromise = Promise.all([
    fetch(TOPIC_MAP_URL, { credentials: "same-origin" }).then(function (r) {
      if (!r.ok) throw new Error("topic map");
      return r.json();
    }),
    fetch(BLUEPRINT_URL, { credentials: "same-origin" }).then(function (r) {
      if (!r.ok) throw new Error("blueprint");
      return r.json();
    }),
    fetch(TRACKER_URL, { credentials: "same-origin" })
      .then(function (r) {
        if (!r.ok) return null;
        return r.json();
      })
      .catch(function () {
        return null;
      }),
  ])
    .then(function (res) {
      var map = res[0];
      window.CCNAAUTO_PRACTICE._topicAssignments =
        map && map.assignments && typeof map.assignments === "object" ? map.assignments : {};
      window.CCNAAUTO_PRACTICE._blueprint = res[1];
      window.CCNAAUTO_PRACTICE._tracker = res[2];
      return res;
    })
    .catch(function () {
      window.CCNAAUTO_PRACTICE._topicAssignments = false;
      return false;
    });

  function allSlugs() {
    return (window.CCNAAUTO_PRACTICE.SLUGS || []).slice();
  }

  function getSelectedDomain() {
    var sel = document.getElementById("ccnaauto-practice-domain-select");
    if (!sel) return "";
    var v = String(sel.value || "").trim();
    return /^[1-6]$/.test(v) ? v : "";
  }

  function bankSlugsForIndex(bankId) {
    return UTIL.bankSlugs(allSlugs(), bankId, BANK_SIZE);
  }

  function start(mode, bankId, domainMajor) {
    bankId = bankId || "1";
    var fixed =
      bankId === FILTER_BANK_ID
        ? allSlugs()
        : bankSlugsForIndex(parseInt(String(bankId), 10) || 1);
    var map = window.CCNAAUTO_PRACTICE._topicAssignments;
    if (domainMajor) {
      if (!map || typeof map !== "object") {
        window.alert("Topic assignments are still loading. Try again in a moment.");
        return;
      }
      fixed = UTIL.filterSlugsByMajor(fixed, map, domainMajor);
    }
    if (!fixed.length) {
      window.alert(
        "No CCNAAUTO questions in this bank yet—or none match the selected domain. " +
          "The dedicated bank is building; try overlap samples below."
      );
      return;
    }
    var order = mode === "linear" ? fixed : UTIL.shuffle(fixed);
    try {
      sessionStorage.setItem(
        KEY,
        JSON.stringify({ v: 1, mode: mode, bank: bankId, order: order, domain: domainMajor || null })
      );
    } catch (e) {}
    window.location.href = QUESTIONS_BASE + order[0] + ".html#ccnaautoP=0";
  }

  function startWithOptionalDomain(mode, bankId) {
    start(mode, bankId, getSelectedDomain() || null);
  }

  function populateDomainSelect(blueprint) {
    var sel = document.getElementById("ccnaauto-practice-domain-select");
    if (!sel || !blueprint || !Array.isArray(blueprint.domains)) return;
    var current = sel.value;
    while (sel.options.length > 1) sel.remove(1);
    blueprint.domains.forEach(function (d) {
      var opt = document.createElement("option");
      var major = String(d.id || "").split(".")[0];
      opt.value = major;
      opt.textContent =
        d.id + " \u2014 " + (d.name || "") + " (" + (d.weightPercent || 0) + "%)";
      sel.appendChild(opt);
    });
    if (current) sel.value = current;
  }

  function renderBanksGrid() {
    var grid = document.getElementById("ccnaauto-practice-banks-grid");
    var summary = document.getElementById("ccnaauto-practice-banks-summary");
    if (!grid) return;

    var all = allSlugs();
    var domain = getSelectedDomain();
    var map = window.CCNAAUTO_PRACTICE._topicAssignments;
    var filtered = domain && map ? UTIL.filterSlugsByMajor(all, map, domain) : all;
    var nBanks = UTIL.practiceBankCount(all.length, BANK_SIZE);
    var blueprint = window.CCNAAUTO_PRACTICE._blueprint;
    var pdf = blueprint && blueprint.sourcePdf ? blueprint.sourcePdf : "exam topics PDF";
    var version = blueprint && blueprint.blueprintVersion ? blueprint.blueprintVersion : "v1.1";

    if (summary) {
      if (!all.length) {
        summary.hidden = false;
        summary.textContent =
          "Bank 1 is open (0/" +
          BANK_SIZE +
          " questions). Target mix follows " +
          version +
          " domain weights from " +
          pdf +
          ".";
      } else if (domain) {
        summary.hidden = false;
        summary.textContent =
          filtered.length +
          " question(s) match domain " +
          domain +
          ". Filtered Random/Review uses the full filtered set—not a 100-question bank slice.";
      } else {
        summary.hidden = false;
        summary.textContent =
          all.length +
          " question(s) across " +
          nBanks +
          " bank(s) of up to " +
          BANK_SIZE +
          " each (" +
          version +
          " objective tags).";
      }
    }

    if (domain) {
      grid.innerHTML =
        '<article class="sim-box" aria-labelledby="ccnaauto-filter-bank-title">' +
        '<h4 class="sim-box-title" id="ccnaauto-filter-bank-title">Filtered set · domain ' +
        domain +
        "</h4>" +
        '<p class="study-meta">' +
        filtered.length +
        " matching question(s). Random shuffles once; Review sends misses to the back.</p>" +
        '<div class="study-actions" role="group" aria-label="Practice modes for filtered domain">' +
        '<button type="button" class="start-btn" data-ccnaauto-mode="random" data-ccnaauto-bank="filter">Random</button>' +
        '<button type="button" class="start-btn" data-ccnaauto-mode="review" data-ccnaauto-bank="filter">Review</button>' +
        "</div></article>";
      return;
    }

    if (!all.length) {
      grid.innerHTML =
        '<article class="sim-box" aria-labelledby="ccnaauto-bank-title-1">' +
        '<h4 class="sim-box-title" id="ccnaauto-bank-title-1">Bank 1 · questions 1\u2013100</h4>' +
        '<p class="study-meta">0 / ' +
        BANK_SIZE +
        " published \u2014 building toward " +
        version +
        " domain mix (15/20/15/15/20/15 per bank).</p>" +
        '<div class="study-actions" role="group" aria-label="Practice modes for bank 1">' +
        '<button type="button" class="start-btn start-btn--muted" disabled>Random</button>' +
        '<button type="button" class="start-btn start-btn--muted" disabled>Review</button>' +
        "</div></article>";
      return;
    }

    var html = "";
    for (var b = 1; b <= nBanks; b++) {
      var inBank = bankSlugsForIndex(b);
      var startIdx = (b - 1) * BANK_SIZE;
      var endIdx = Math.min(b * BANK_SIZE, all.length);
      var slotEnd = b * BANK_SIZE;
      var rangeLabel = UTIL.formatRange(startIdx + 1, slotEnd);
      var isPartial = inBank.length > 0 && inBank.length < BANK_SIZE;
      html +=
        '<article class="sim-box" data-ccnaauto-bank-index="' +
        b +
        '" aria-labelledby="ccnaauto-bank-title-' +
        b +
        '">' +
        '<h4 class="sim-box-title" id="ccnaauto-bank-title-' +
        b +
        '">Bank ' +
        b +
        " \u00b7 questions " +
        rangeLabel +
        "</h4>" +
        '<p class="study-meta">' +
        inBank.length +
        " question(s)" +
        (isPartial ? " (partial bank)" : "") +
        " \u00b7 Random or Review for this bank only.</p>" +
        '<div class="study-actions" role="group" aria-label="Practice modes for bank ' +
        b +
        '">' +
        '<button type="button" class="start-btn" data-ccnaauto-mode="random" data-ccnaauto-bank="' +
        b +
        '">Random</button>' +
        '<button type="button" class="start-btn" data-ccnaauto-mode="review" data-ccnaauto-bank="' +
        b +
        '">Review</button>' +
        "</div></article>";
    }
    grid.innerHTML = html;
  }

  function refreshUI() {
    var weightRoot = document.getElementById("ccnaauto-bank-weight-table");
    UTIL.renderDomainWeightTable(
      weightRoot,
      window.CCNAAUTO_PRACTICE._tracker,
      window.CCNAAUTO_PRACTICE._blueprint
    );
    populateDomainSelect(window.CCNAAUTO_PRACTICE._blueprint);
    renderBanksGrid();
  }

  function bootstrap() {
    window.CCNAAUTO_PRACTICE._loadPromise.then(function (ok) {
      if (!ok) {
        var grid = document.getElementById("ccnaauto-practice-banks-grid");
        if (grid) {
          grid.innerHTML =
            '<p class="study-meta">Could not load CCNAAUTO practice config. Refresh the page.</p>';
        }
        return;
      }
      refreshUI();
    });
  }

  document.addEventListener(
    "click",
    function (e) {
      var t = e.target;
      if (!t || typeof t.closest !== "function") return;
      var el = t.closest("[data-ccnaauto-mode]");
      if (!el || el.disabled) return;
      var mode = el.getAttribute("data-ccnaauto-mode");
      var bank = el.getAttribute("data-ccnaauto-bank") || "1";
      if (mode !== "random" && mode !== "review") return;
      e.preventDefault();
      startWithOptionalDomain(mode, bank);
    },
    false
  );

  document.addEventListener("change", function (e) {
    if (e.target && e.target.id === "ccnaauto-practice-domain-select") refreshUI();
  });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bootstrap);
  } else {
    bootstrap();
  }
})();

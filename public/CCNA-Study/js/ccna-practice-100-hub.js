(function () {
  "use strict";

  var KEY = "ccnaPractice100";
  var TOPIC_MAP_URL = "/CCNA-Study/data/ccna-question-topic-map.json";

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

  window.CCNA_PRACTICE_100 = window.CCNA_PRACTICE_100 || {};
  /** @type {Record<string, string[]>|null|false} null = loading, false = failed, object = assignments keyed by "slug.html" */
  window.CCNA_PRACTICE_100._topicAssignments = null;
  window.CCNA_PRACTICE_100._topicAssignmentsPromise = fetch(TOPIC_MAP_URL, { credentials: "same-origin" })
    .then(function (res) {
      if (!res.ok) throw new Error("topic map http " + res.status);
      return res.json();
    })
    .then(function (data) {
      var a = data && data.assignments;
      window.CCNA_PRACTICE_100._topicAssignments = a && typeof a === "object" ? a : {};
      return window.CCNA_PRACTICE_100._topicAssignments;
    })
    .catch(function () {
      window.CCNA_PRACTICE_100._topicAssignments = false;
      return false;
    });

  function objectivesForSlug(assignments, slug) {
    if (!assignments || !slug) return null;
    return assignments[slug + ".html"] || null;
  }

  function slugMatchesMajor(assignments, slug, major) {
    var objs = objectivesForSlug(assignments, slug);
    if (!objs || !objs.length) return false;
    var want = String(major);
    for (var i = 0; i < objs.length; i++) {
      var maj = String(objs[i]).split(".")[0];
      if (maj === want) return true;
    }
    return false;
  }

  function filterSlugsByMajor(slugs, assignments, major) {
    if (!major) return slugs.slice();
    if (!assignments || typeof assignments !== "object") return [];
    var out = [];
    for (var i = 0; i < slugs.length; i++) {
      if (slugMatchesMajor(assignments, slugs[i], major)) out.push(slugs[i]);
    }
    return out;
  }

  function getSelectedPracticeDomain() {
    var sel = document.getElementById("ccna-practice-domain-select");
    if (!sel) return "";
    var v = String(sel.value || "").trim();
    if (!v || !/^[1-6]$/.test(v)) return "";
    return v;
  }

  function startWithOptionalDomain(mode, bankId, domainMajor) {
    if (!domainMajor) {
      start(mode, bankId, null);
      return;
    }
    var inst = window.CCNA_PRACTICE_100;
    var assign = inst._topicAssignments;
    if (assign === false) {
      window.alert(
        "Could not load the topic map for this site. Use \"All subjects\" or try again later."
      );
      return;
    }
    if (assign && typeof assign === "object") {
      start(mode, bankId, domainMajor);
      return;
    }
    inst._topicAssignmentsPromise.then(function () {
      if (inst._topicAssignments === false) {
        window.alert(
          "Could not load the topic map for this site. Use \"All subjects\" or try again later."
        );
        return;
      }
      start(mode, bankId, domainMajor);
    });
  }

  window.CCNA_PRACTICE_100.ALL_SLUGS = ["qos-minimum-bandwidth-choose-two","security-physical-access-tailgating","private-ipv4-subnet-appropriate","etherchannel-lacp-active-active","rstp-port-states-choose-two","wireless-controller-enterprise-role","virtual-server-hypervisor-vswitch","http-get-crud-operation","rest-api-accept-header","firewall-stateful-connection-forwarding","lightweight-ap-wlc-authentication-forward","vty-access-list-ssh-secure","dhcp-relay-dhcpdiscover","arp-first-ping-switch-flood","stp-bpduguard-portfast-errdisable","stp-root-bridge-vlan110","trunk-native-vlan-untagged","wan-t1-bandwidth","wireless-rrm-channel-overlap","wlan-design-nonoverlapping-2-4-channels-1-6-11","wlan-nonoverlapping-channels-discontinuous-frequency","switch-mac-table-ingress-learning","control-plane-routing-decisions","ios-dns-lookup-default-behavior","dns-lookup-operation-definition","voice-data-vlan-access-ports-sw11","pat-vlan200-inside-source-overload","switch-unknown-unicast-flood","vrrp-gateway-redundancy-benefit","dhcp-ipv4-assigned-by-protocol","dhcp-pool-default-router-command","dhcp-relay-r4-fa01-acl100-exhibit","ospf-r14-r86-broadcast-dr-adjacency","native-vlan-security-separated","stp-portfast-default-immediate-forwarding","wireless-wpa2-aes-strongest","vm-shared-disk-resource","soho-broadband-shared-connection","snmp-trap-mib-requirement","standard-acl-permit-deny-two-subnets","netconf-xml-filter-get-config","sdn-controller-functions-choose-two","switch-egress-queue-during-transmit","wan-topology-point-to-point-simplicity","ntp-master-internal-clock-server","trunk-allowed-vlan-add-no-disruption","sdn-southbound-api-purpose","err-disabled-port-security-violation","northbound-rest-sdn-applications","physical-access-badge-readers-datacenter","private-ipv4-characteristic-registration","private-ipv4-appropriate-use-internal-only","data-plane-forwarding-lookup","sdn-automation-improvements-choose-two","ssh-crypto-rsa-key-generation","pki-components-crl-ca-choose-two","sdn-southbound-openflow-forwarding","wireless-band-select-5ghz-preference","wlc-wpa2-psk-gui-format","data-plane-forward-remote-client-traffic","ipv6-compress-db8-interface-command","ipv6-compress-hq-serial-s0-700-400f","ipv6-compress-2001-eb8-c1-2200-0331","wlc-pmf-comeback-spoofed-association","fhrp-benefit-default-gateway-redundancy","wlan-roam-reassociation-request-frame","wlan-probe-response-frame-type","fiber-om3-om4-fifty-micron-core","ap-switch-poe-cdp-discovery","syslog-severity-informational-level","dtp-dynamic-auto-passive-trunk","dtp-sw1-sw2-printer-vlan5-trunk","wlc-ds-port-switch-ap-traffic","syslog-trap-severity-informational-included","route-ad-ebgp-eigrp-ospf-r4-server","cloud-topology-public-private-hybrid","ios-clock-set-exec-date-time","rest-http-200-successful-request","router-inter-subnet-forwarding-role","sdn-controller-role-central-point","switch-known-mac-unicast-forward","rfc1918-purpose-conserve-public-ipv4","wlc-aaa-override-ise-dynamic-vlan","ftp-authentication-backup-config-copy","sdn-control-to-infrastructure-boundary","router-forward-hop-mac-rewrite","ipsec-tunnel-esp-encrypt-whole-packet","ipv6-static-summary-and-host-via-next-hops","firewall-role-untrusted-to-trusted","firewall-permit-deny-traffic-rules","portfast-benefit-user-data-sooner","vlan-hopping-mitigation-dtp-trunk","routing-longest-match-default-172-16-1-1","floating-static-default-route-router-a-command","r1-management-network-static-route-new-server","r1-backup-default-route-via-r2-ad10","ansible-playbook-task-vlan-config","spine-leaf-full-mesh-uplinks","sdn-data-plane-forwarding-router","wlc-hardening-disable-telnet-http","dna-center-overall-health-dashboard","hypervisor-vm-hardware-communication","distribution-layer-two-characteristics","layer3-switch-flood-broadcast-within-vlan","qos-pq-voice-over-data-traffic","dhcp-default-gateway-windows-workstation","subnet-included-hosts-192-168-1-0-26","network-automation-drivers-choose-two","tcp-vs-udp-connection-reliability","network-endpoints-security-definition","physical-access-control-scope","wireless-80211a-five-ghz-consideration","lldp-run-global-isp-handoff","r5-disable-discovery-gi0-1-cdp-lldp-verify","qos-voice-reduce-packet-loss","dna-center-add-device-two-events","portfast-benefits-choose-two","stp-portfast-bypass-states-choose-two","unused-switchports-black-hole-vlan","dhcp-snooping-rate-limit-function","dhcp-snooping-trust-server-same-switch-vlan1","sdn-controller-centralizes-control-plane","utp-cat5e-cat6a-two-similarities","ospf-dr-election-priority-options","ospf-dr-election-router-a-area-zero","ospf-ia-route-metric-display","access-layer-8021x-identity-security","dhcp-relay-different-subnet-forwarding","route-no-match-101016-discard","ssh-loopback-source-next-hop-10-0-1-15-exhibit","site-ab-tenge-sfp-sr-vs-lr-smf-intermittent-exhibit","switch-host-a-to-d-unknown-dest-flood-exhibit","switch-sw1-pc2-mac-missing-fa02-trunk-exhibit","gigabit-lx-t-l2-frame-similarity","wpa3-sae-improves-security","wireless-wpa3-perfect-forward-secrecy","subnet-en0-configured-ip-ifconfig-exhibit","subnet-split-10-70-128-19-two-vlans-choose-two","capwap-lightweight-ap-mode","etherchannel-lacp-active-switch2","etherchannel-lacp-trunk-dynamic-industry-standard","wireless-auth-layer2","three-tier-workstation-to-workstation-path","fhrp-two-benefits-choose-two","ssid-purpose-identifies-wlan","ssid-two-characteristics-choose-two","qos-llq-interactive-voice-video","sdn-southbound-api-controller-to-infrastructure","sdn-controller-dynamic-changes-southbound-api","ipv6-link-local-scope-neighbor-discovery","nat-inside-global-address-from-example","switch-collision-domain-per-port","icmp-echo-request-reply-ping","acl-numbered-fifteen-standard-range","vty-access-class-permit-any-after-deny-pc1","switchport-priority-extend-trust-ip-phone-access","spanning-tree-portfast-supported-access-ports","syslog-facility-definition","public-cloud-two-characteristics-choose-two","ipsec-pure-traffic-unicast-ip","dhcp-workstation-blocked-8021x","ftp-control-data-connections-capability","static-default-route-r1-r2-two-sites-exhibit","collapsed-core-small-organization-cost","ipv6-route-r17-ping-r18-wan-interface","ipv6-anycast-unicast-multiple-interfaces","radius-access-request-password-encrypted","ngips-user-activity-network-events","ipv6-unicast-vs-anycast-assignment","data-plane-fib-lookup-action","rapid-pvst-plus-per-vlan-instance","wlc-telnet-mitm-management","aaa-authentication-identity-verification","syn-flood-half-open-tcp-resources","lightweight-ap-centralized-access-mode","data-plane-actions-8021q-mac-lookup","wlc-centralized-auth-roaming","owe-opportunistic-wireless-encryption","physical-access-ip-cameras-monitoring","qos-marking-tos-ipv4-field","qos-trust-boundary-access-phone-pc-exhibit","wlc-lag-link-redundancy-load-balance","wlc-lag-configure-remove-reboot-requirement","poe-static-mode-guaranteed-power","switch-access-vlan20-voice-vlan30","https-uses-ssl-tls","ssid-wireless-lan-identifier","ssh-ip-domain-name-before-rsa-key","r1-ssh-secure-remote-access-choose-two","qos-traffic-shaping-buffer-excess","vlan-tagging-trunk-separation","utp-vs-stp-shielding-emi","flexconnect-local-switching-trunk-ap","wlan-passive-client-static-ip","ipv6-static-route-global-config-nexthop","qos-policing-exceed-drop-mark","sdn-disaggregation-control-data-plane","dna-center-intent-api-rest-put","amp-ngips-file-malware-analysis","password-complexity-enable-prerequisite","r1-username-engineer2-scrypt-local-database","commodity-switches-data-plane-forwarding","security-posture-practices-choose-two","wan-topology-full-mesh-reliability","wpa-tkip-mic-encryption-feature","tftp-operation-block-numbers-udp","ntp-master-fallback-upstream-failure","authentication-vs-authorization-definition","ospf-gigabitethernet-default-broadcast-network","public-cloud-benefit-internet-access","sdn-controller-centralizes-routing-decision","sdn-controller-function-making-routing-decisions","sdn-plane-forwards-user-traffic","collapsed-core-small-network-minimal-growth","wpa2-wpa3-ccmp-encryption-choose-two","mac-learning-switch-source-address","gigabit-lx-lh-vs-zx-fiber-reach","ospf-router-id-without-loopback-or-router-id","router-subnet-10pct-host-growth-r789","show-ip-route-eigrp-learned-prefix","lacp-etherchannel-sw1-sw2-mode-fix","switch2-lldp-timer-holdtime","ssh-vty-access-class-10-139-58-28","ssh-secure-remote-cli-protocol","private-ipv4-characteristic-no-registry","enterprise-network-wlc-auth-roaming","nat-pat-standard-acl1-gi01-exhibit","ipv6-vlan2000-unique-local-ula","ospf-r1-r2-point-to-point-no-dr-bdr","switchport-trunk-fa01-vlans-10-15-complete","route-best-path-10-10-10-24-exhibit","ip-address-dhcp-interface-client","endpoint-network-function-client-server","ipv6-internal-device-unique-local-address","etherchannel-port-channel10-lacp-modes-choose-two","ospf-dr-r1-priority-r3-zero-choose-two","r1-ntp-server-requirements-config","r1-floating-static-ospf-backup-server","ospf-r1-r2-p2p-link-network-command","ten-gigabitethernet0-0-0-slow-transfer-show-interface"];
  window.CCNA_PRACTICE_100.SLUGS = window.CCNA_PRACTICE_100.ALL_SLUGS;

  function bankSlugs(bankId) {
    var all = window.CCNA_PRACTICE_100.ALL_SLUGS;
    var n = parseInt(String(bankId), 10);
    if (!n || n < 1) n = 1;
    var start = (n - 1) * 100;
    return all.slice(start, start + 100);
  }

  function practiceBankCount() {
    var all = window.CCNA_PRACTICE_100.ALL_SLUGS;
    if (!all || !all.length) return 1;
    return Math.ceil(all.length / 100);
  }

  function start(mode, bankId, domainMajor) {
    bankId = bankId || "1";
    var fixed = bankSlugs(bankId);
    var map = window.CCNA_PRACTICE_100._topicAssignments;
    if (domainMajor) {
      if (!map || typeof map !== "object") {
        window.alert("Topic assignments are still loading. Try again in a moment.");
        return;
      }
      fixed = filterSlugsByMajor(fixed, map, domainMajor);
    }
    if (!fixed.length) {
      window.alert(
        "No questions in this bank match the selected subject. Pick another subject, choose “All subjects”, or try a different bank."
      );
      return;
    }
    var order;
    if (mode === "linear") {
      order = fixed;
    } else {
      order = shuffle(fixed);
    }
    var session = { v: 1, mode: mode, bank: bankId, order: order };
    if (domainMajor) session.domain = domainMajor;
    try {
      sessionStorage.setItem(KEY, JSON.stringify(session));
    } catch (e) {}
    var slugFile = order[0] + ".html";
    var path = window.location.pathname || "";
    var studyIdx = path.indexOf("/CCNA-Study/");
    if (studyIdx >= 0) {
      window.location.href =
        window.location.origin +
        path.slice(0, studyIdx + "/CCNA-Study/".length) +
        "CCNA_questions/" +
        slugFile +
        "#ccnaP=0";
    } else {
      window.location.href = "/CCNA-Study/CCNA_questions/" + slugFile + "#ccnaP=0";
    }
  }

  window.CCNA_PRACTICE_100.start = start;
  window.CCNA_PRACTICE_100.startWithOptionalDomain = startWithOptionalDomain;
  window.CCNA_PRACTICE_100.bankSlugs = bankSlugs;
  window.CCNA_PRACTICE_100.practiceBankCount = practiceBankCount;
  window.CCNA_PRACTICE_100.filterSlugsByMajor = filterSlugsByMajor;

  document.addEventListener(
    "click",
    function (e) {
      var t = e.target;
      if (!t || typeof t.closest !== "function") return;
      var el = t.closest("[data-ccna100]");
      if (!el || el.disabled) return;
      var m = el.getAttribute("data-ccna100");
      var bank = el.getAttribute("data-ccna100-bank") || "1";
      if (m === "random" || m === "review" || m === "linear") {
        e.preventDefault();
        var domain = getSelectedPracticeDomain();
        if (m === "random" || m === "review") {
          startWithOptionalDomain(m, bank, domain || null);
        } else {
          start(m, bank, null);
        }
      }
    },
    false
  );

  /** CCNA_Training_Portal.html: three sim-boxes (100 + 100 + remainder); no per-question list. */
  function injectPortalPracticeBanks() {
    var grid = document.getElementById("ccna-practice-banks-grid");
    if (!grid) return;

    var all = window.CCNA_PRACTICE_100.ALL_SLUGS;
    if (!Array.isArray(all)) return;
    if (grid.querySelector("[data-ccna-practice-bank-index]")) return;

    var maxPortalBanks = 3;
    var nBanks = maxPortalBanks;

    function formatRange(first, last) {
      if (first >= last) return String(first);
      return String(first) + "–" + String(last);
    }

    for (var b = 1; b <= nBanks; b++) {
      var startIdx = (b - 1) * 100;
      var endIdx = Math.min(b * 100, all.length);
      var firstNum = startIdx + 1;
      var slotEnd = b * 100;
      var countInBank = endIdx > startIdx ? endIdx - startIdx : 0;

      var article = document.createElement("article");
      article.className = "sim-box";
      article.setAttribute("data-ccna-practice-bank-index", String(b));
      article.setAttribute("aria-labelledby", "ccna-bank-title-" + b);

      var h4 = document.createElement("h4");
      h4.className = "sim-box-title";
      h4.id = "ccna-bank-title-" + b;
      var isLastBank = b === nBanks;
      var isPartial = countInBank > 0 && countInBank < 100;
      var titleInner;
      if (countInBank === 0) {
        titleInner = formatRange(firstNum, slotEnd);
      } else if (isLastBank && isPartial && firstNum >= 201) {
        titleInner = String(firstNum) + " through end";
        article.classList.add("ccna-practice-bank--remainder");
      } else {
        titleInner = formatRange(firstNum, endIdx);
      }
      h4.textContent = "Practice questions (" + titleInner + ")";

      var p = document.createElement("p");
      p.className = "study-meta";
      if (countInBank > 0) {
        p.innerHTML =
          "Up to <strong>100</strong> items in this slice of the hub list (this bank has <strong>" +
          String(countInBank) +
          "</strong>). Use <strong>Practice by subject</strong> above to limit <strong>Random</strong> and <strong>Review</strong> to one CCNA domain. <strong>Random</strong> shuffles once. <strong>Review</strong> re-queues misses until the session completes.";
      } else {
        p.innerHTML =
          "Reserved for questions <strong>" +
          formatRange(firstNum, slotEnd) +
          "</strong> when the hub list grows. <strong>Random</strong> and <strong>Review</strong> stay disabled until this range has items.";
      }

      var actions = document.createElement("div");
      actions.className = "study-actions";
      actions.setAttribute("role", "group");
      actions.setAttribute("aria-label", "Practice question modes bank " + String(b));

      var br = document.createElement("button");
      br.type = "button";
      br.className = "start-btn";
      br.setAttribute("data-ccna100", "random");
      br.setAttribute("data-ccna100-bank", String(b));
      br.textContent = "Random";

      var rev = document.createElement("button");
      rev.type = "button";
      rev.className = "start-btn";
      rev.setAttribute("data-ccna100", "review");
      rev.setAttribute("data-ccna100-bank", String(b));
      rev.textContent = "Review";

      if (countInBank === 0) {
        br.disabled = true;
        rev.disabled = true;
        br.classList.add("is-placeholder");
        rev.classList.add("is-placeholder");
      }

      actions.appendChild(br);
      actions.appendChild(rev);
      article.appendChild(h4);
      article.appendChild(p);
      article.appendChild(actions);

      grid.appendChild(article);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", injectPortalPracticeBanks);
  } else {
    injectPortalPracticeBanks();
  }
})();

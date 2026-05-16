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

  /** Practice-by-subject: optional adaptive queue (misses appended until session completes). */
  function getAdaptiveLearningEnabled() {
    try {
      var r = document.querySelector('input[name="ccna-practice-adaptive"]:checked');
      if (!r) return false;
      return String(r.value || "").trim() === "1";
    } catch (e) {
      return false;
    }
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

  window.CCNA_PRACTICE_100.ALL_SLUGS = ["qos-minimum-bandwidth-choose-two","security-physical-access-tailgating","private-ipv4-subnet-appropriate","etherchannel-lacp-active-active","rstp-port-states-choose-two","wireless-controller-enterprise-role","virtual-server-hypervisor-vswitch","http-get-crud-operation","rest-api-accept-header","firewall-stateful-connection-forwarding","lightweight-ap-wlc-authentication-forward","vty-access-list-ssh-secure","dhcp-relay-dhcpdiscover","arp-first-ping-switch-flood","stp-bpduguard-portfast-errdisable","stp-root-bridge-vlan110","trunk-native-vlan-untagged","wan-t1-bandwidth","wireless-rrm-channel-overlap","wlan-design-nonoverlapping-2-4-channels-1-6-11","wlan-nonoverlapping-channels-discontinuous-frequency","switch-mac-table-ingress-learning","control-plane-routing-decisions","ios-dns-lookup-default-behavior","dns-lookup-operation-definition","voice-data-vlan-access-ports-sw11","pat-vlan200-inside-source-overload","switch-unknown-unicast-flood","vrrp-gateway-redundancy-benefit","dhcp-ipv4-assigned-by-protocol","dhcp-pool-default-router-command","dhcp-relay-r4-fa01-acl100-exhibit","ospf-r14-r86-broadcast-dr-adjacency","native-vlan-security-separated","stp-portfast-default-immediate-forwarding","wireless-wpa2-aes-strongest","vm-shared-disk-resource","soho-broadband-shared-connection","snmp-trap-mib-requirement","standard-acl-permit-deny-two-subnets","netconf-xml-filter-get-config","sdn-controller-functions-choose-two","switch-egress-queue-during-transmit","wan-topology-point-to-point-simplicity","ntp-master-internal-clock-server","trunk-allowed-vlan-add-no-disruption","sdn-southbound-api-purpose","err-disabled-port-security-violation","northbound-rest-sdn-applications","physical-access-badge-readers-datacenter","private-ipv4-characteristic-registration","private-ipv4-appropriate-use-internal-only","data-plane-forwarding-lookup","sdn-automation-improvements-choose-two","ssh-crypto-rsa-key-generation","pki-components-crl-ca-choose-two","sdn-southbound-openflow-forwarding","wireless-band-select-5ghz-preference","wlc-wpa2-psk-gui-format","data-plane-forward-remote-client-traffic","ipv6-compress-db8-interface-command","ipv6-compress-hq-serial-s0-700-400f","ipv6-compress-2001-eb8-c1-2200-0331","wlc-pmf-comeback-spoofed-association","fhrp-benefit-default-gateway-redundancy","wlan-roam-reassociation-request-frame","wlan-probe-response-frame-type","fiber-om3-om4-fifty-micron-core","ap-switch-poe-cdp-discovery","syslog-severity-informational-level","dtp-dynamic-auto-passive-trunk","dtp-sw1-sw2-printer-vlan5-trunk","wlc-ds-port-switch-ap-traffic","syslog-trap-severity-informational-included","route-ad-ebgp-eigrp-ospf-r4-server","cloud-topology-public-private-hybrid","ios-clock-set-exec-date-time","rest-http-200-successful-request","router-inter-subnet-forwarding-role","sdn-controller-role-central-point","switch-known-mac-unicast-forward","rfc1918-purpose-conserve-public-ipv4","wlc-aaa-override-ise-dynamic-vlan","ftp-authentication-backup-config-copy","sdn-control-to-infrastructure-boundary","router-forward-hop-mac-rewrite","ipsec-tunnel-esp-encrypt-whole-packet","ipv6-static-summary-and-host-via-next-hops","firewall-role-untrusted-to-trusted","firewall-permit-deny-traffic-rules","portfast-benefit-user-data-sooner","vlan-hopping-mitigation-dtp-trunk","routing-longest-match-default-172-16-1-1","floating-static-default-route-router-a-command","r1-management-network-static-route-new-server","r1-backup-default-route-via-r2-ad10","ansible-playbook-task-vlan-config","spine-leaf-full-mesh-uplinks","sdn-data-plane-forwarding-router","wlc-hardening-disable-telnet-http","dna-center-overall-health-dashboard","hypervisor-vm-hardware-communication","distribution-layer-two-characteristics","layer3-switch-flood-broadcast-within-vlan","qos-pq-voice-over-data-traffic","dhcp-default-gateway-windows-workstation","subnet-included-hosts-192-168-1-0-26","network-automation-drivers-choose-two","tcp-vs-udp-connection-reliability","network-endpoints-security-definition","physical-access-control-scope","wireless-80211a-five-ghz-consideration","lldp-run-global-isp-handoff","r5-disable-discovery-gi0-1-cdp-lldp-verify","qos-voice-reduce-packet-loss","dna-center-add-device-two-events","portfast-benefits-choose-two","stp-portfast-bypass-states-choose-two","unused-switchports-black-hole-vlan","dhcp-snooping-rate-limit-function","dhcp-snooping-trust-server-same-switch-vlan1","sdn-controller-centralizes-control-plane","utp-cat5e-cat6a-two-similarities","ospf-dr-election-priority-options","ospf-dr-election-router-a-area-zero","ospf-ia-route-metric-display","access-layer-8021x-identity-security","dhcp-relay-different-subnet-forwarding","route-no-match-101016-discard","ssh-loopback-source-next-hop-10-0-1-15-exhibit","site-ab-tenge-sfp-sr-vs-lr-smf-intermittent-exhibit","switch-host-a-to-d-unknown-dest-flood-exhibit","switch-sw1-pc2-mac-missing-fa02-trunk-exhibit","gigabit-lx-t-l2-frame-similarity","wpa3-sae-improves-security","wireless-wpa3-perfect-forward-secrecy","subnet-en0-configured-ip-ifconfig-exhibit","subnet-split-10-70-128-19-two-vlans-choose-two","capwap-lightweight-ap-mode","etherchannel-lacp-active-switch2","etherchannel-lacp-trunk-dynamic-industry-standard","wireless-auth-layer2","three-tier-workstation-to-workstation-path","fhrp-two-benefits-choose-two","ssid-purpose-identifies-wlan","ssid-two-characteristics-choose-two","qos-llq-interactive-voice-video","sdn-southbound-api-controller-to-infrastructure","sdn-controller-dynamic-changes-southbound-api","ipv6-link-local-scope-neighbor-discovery","nat-inside-global-address-from-example","switch-collision-domain-per-port","icmp-echo-request-reply-ping","acl-numbered-fifteen-standard-range","vty-access-class-permit-any-after-deny-pc1","switchport-priority-extend-trust-ip-phone-access","spanning-tree-portfast-supported-access-ports","syslog-facility-definition","public-cloud-two-characteristics-choose-two","ipsec-pure-traffic-unicast-ip","dhcp-workstation-blocked-8021x","ftp-control-data-connections-capability","static-default-route-r1-r2-two-sites-exhibit","collapsed-core-small-organization-cost","ipv6-route-r17-ping-r18-wan-interface","ipv6-anycast-unicast-multiple-interfaces","radius-access-request-password-encrypted","ngips-user-activity-network-events","ipv6-unicast-vs-anycast-assignment","data-plane-fib-lookup-action","rapid-pvst-plus-per-vlan-instance","wlc-telnet-mitm-management","aaa-authentication-identity-verification","syn-flood-half-open-tcp-resources","lightweight-ap-centralized-access-mode","data-plane-actions-8021q-mac-lookup","wlc-centralized-auth-roaming","owe-opportunistic-wireless-encryption","physical-access-ip-cameras-monitoring","qos-marking-tos-ipv4-field","qos-trust-boundary-access-phone-pc-exhibit","wlc-lag-link-redundancy-load-balance","wlc-lag-configure-remove-reboot-requirement","poe-static-mode-guaranteed-power","switch-access-vlan20-voice-vlan30","https-uses-ssl-tls","ssid-wireless-lan-identifier","ssh-ip-domain-name-before-rsa-key","r1-ssh-secure-remote-access-choose-two","qos-traffic-shaping-buffer-excess","vlan-tagging-trunk-separation","utp-vs-stp-shielding-emi","flexconnect-local-switching-trunk-ap","wlan-passive-client-static-ip","ipv6-static-route-global-config-nexthop","qos-policing-exceed-drop-mark","sdn-disaggregation-control-data-plane","dna-center-intent-api-rest-put","amp-ngips-file-malware-analysis","password-complexity-enable-prerequisite","floating-static-router1-primary-default-route","switchport-trunk-allowed-vlan-add-104","wan-gigabitethernet0-0-0-crc-errors-poor-performance","ospf-r3-dr-priority-gi01-104","router1-longest-match-10-10-13-158-show-ip-route","r1-wan-lan-route-10-0-10-ad-precedence","r15-ssh-version2-minimum-config-show-run","wlc-80211r-fast-transition-ft-psk","etherchannel-lacp-sw1-active-sw2-passive-initiation","stp-vlan20-four-switch-root-bridge","nat-router1-vlan200-acl-inside-source-overload","switch-a-gi01-ip-phone-vlan50-voice51","r1-floating-static-19216820-via-r3-ospf-area20","r1-r2-floating-static-backup-gi01-workstation-lans","cat9300-cdp-timer-rapid-neighbor-discovery","sw2-fa01-dynamic-auto-trunk-allowed-vlan5-10","wlc-enterprise-wlan-80211r-fast-transition","etherchannel-lacp-sw1-sw2-g1-1-3-trunk-active","wlc-radius-authentication-server-network-user","ip-arp-inspection-vlan5-10-fa01-untrusted-effect","router-gi00-lldp-third-party-isp-exhibit","r1-show-ip-route-10-56-192-1-default-next-hop","r1-username-engineer2-scrypt-local-database","commodity-switches-data-plane-forwarding","security-posture-practices-choose-two","wan-topology-full-mesh-reliability","wpa-tkip-mic-encryption-feature","tftp-operation-block-numbers-udp","ntp-master-fallback-upstream-failure","authentication-vs-authorization-definition","ospf-gigabitethernet-default-broadcast-network","public-cloud-benefit-internet-access","sdn-controller-centralizes-routing-decision","sdn-controller-function-making-routing-decisions","sdn-plane-forwards-user-traffic","collapsed-core-small-network-minimal-growth","wpa2-wpa3-ccmp-encryption-choose-two","mac-learning-switch-source-address","gigabit-lx-lh-vs-zx-fiber-reach","ospf-router-id-without-loopback-or-router-id","router-subnet-10pct-host-growth-r789","show-ip-route-eigrp-learned-prefix","lacp-etherchannel-sw1-sw2-mode-fix","switch2-lldp-timer-holdtime","ssh-vty-access-class-10-139-58-28","ssh-secure-remote-cli-protocol","private-ipv4-characteristic-no-registry","enterprise-network-wlc-auth-roaming","nat-pat-standard-acl1-gi01-exhibit","ipv6-vlan2000-unique-local-ula","ospf-r1-r2-point-to-point-no-dr-bdr","switchport-trunk-fa01-vlans-10-15-complete","route-best-path-10-10-10-24-exhibit","ip-address-dhcp-interface-client","endpoint-network-function-client-server","ipv6-internal-device-unique-local-address","etherchannel-port-channel10-lacp-modes-choose-two","ospf-dr-r1-priority-r3-zero-choose-two","r1-ntp-server-requirements-config","r1-floating-static-ospf-backup-server","ospf-r1-r2-p2p-link-network-command","ten-gigabitethernet0-0-0-slow-transfer-show-interface","ospf-serial-neighbor-stuck-exchange-mtu","routing-cpe-longest-match-192-168-1-250","switch-pc1-access-duplex-mismatch-performance","ipv6-ho-fa01-eui64-from-mac-topology","dhcp-relay-gi00-helper-server-subnet-exhibit","static-route-r14-172-21-34-25-via-r86","wlc-wlan-security-wpa-wpa2-8021x-enterprise","cat9k-lldp-suppress-management-address","ospf-r1-drother-elect-dr-priority-clear","dc1-hq1-interface-usable-host-addresses","json-routers-switches-array-elements-are-values","vlan14-trunk-ring-sw4-sw11-sw9-pc2-pc7","ospf-r1-passive-priority-router-id-neighbor-r2-only","r1-static-route-10-0-3-via-transit-r3","r1-r2-floating-static-default-wan-failover","pc-a-pc-b-vlan200-switch-unicast-mac","collapsed-core-distribution-core-merged","vrrp-virtual-mac-iana-format","wlan-24ghz-us-nonoverlapping-channels-set","rapid-pvst-plus-forward-time-listen-learn","lacp-layer3-port-channel-neighbor-passive-after-static","dna-center-controller-purpose-manage-deploy","tftp-feature-anonymous-style-no-login","lightweight-ap-mode-centralized-wlc-ssid-roaming","nat-inside-source-static-private-to-public-pc","longest-match-10-1-1-19-rip-28-ospf-eigrp","rest-http-status-classes-errors-4xx-5xx","ssh-next-step-crypto-key-generate-after-domain-user","wpa3-encryption-method-sae","ssh-interface-acl-inbound-10-139-58-28","spine-leaf-predictable-latency-uniform-path","dna-center-traditional-campus-centralized-management","zero-day-exploit-vulnerability-no-patch","aaa-console-local-username-line-con-zero","snmp-v3-implied-by-snmp-server-user","switch-unknown-destination-mac-flood-except-ingress","port-security-trunk-default-violation-errdisable","multifactor-authentication-examples-choose-two","show-ip-route-10-10-13-160-slash-29-subnet-mask","endpoint-function-user-access-network-services","dhcp-relay-agent-features-choose-two","cloud-rapid-elasticity-capacity-demand","flexconnect-local-switch-different-vlans-trunk-port","wlc-config-serial-timeout-no-auto-logout","mac-address-learning-enabled-default-vlans","flexconnect-branch-local-switching-wan-survivability","poe-auto-mode-detects-powered-device","cpe-floating-static-default-when-ebgp-invalid","telnet-unsecured-remote-cli-access","wlc-functions-vs-autonomous-ap-choose-two","ospf-gi0-0-point-to-point-desired-full-dash","sw1-fa01-notconnect-wrong-cable-type","ssh-transport-rsa-modulus-2048-choose-two","longest-match-192-168-2-2-static-routes","json-mycar-wheels-warning-in-array","wlan-office-ssid-same-security-policies-branches","dna-center-single-pane-faster-deployment","tcp-udp-query-response-connection-model","serial0-ip-access-list-in-syntax-fails-apply","show-ip-route-10-10-8-14-slash-28-mask","private-ipv4-reasons-implement-choose-two","puppet-manifests-modules-paradigm","ipsec-tunnel-mode-encrypts-header-and-payload","wpa3-safeguards-brute-force-sae","show-ip-route-ospf-metric-172-16-0-128-25","traffic-policing-drop-remark-choose-two","static-route-best-path-10-10-10-3-slash-28","wlc-rogue-ap-class-type-friendly-autonomous","anti-replay-prevent-mitm-attack","ospf-r2-must-be-dr-gi0-0-priority","r1-show-ip-route-10-1-2-126-next-hop","r1-static-route-10-0-0-24-r3-pc1-via-r2","ospf-r2-wan-dr-gi0-0-address-priority","r1-route-host-b-10-10-13-25-lowest-ad","windows-ipconfig-dns-query-www-cisco-com","r1-static-route-r3-lan-10-0-15-via-20-3","wlc-wlan-80211r-enable-ft-8021x","json-aaa-user-nested-roles-object-count","r2-no-cdp-enable-g02-hide-neighbor-from-r3","port-security-dynamic-mac-restrict-violation-choose-two","r1-host-route-server-10-10-10-10-via-r2"];
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
    if (getAdaptiveLearningEnabled()) {
      session.adaptive = true;
      session.adaptiveExtrasInjected = 0;
    }
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

  /** CCNA_Training_Portal.html: one sim-box per 100 hub positions (ceil); last box may be partial. */
  function injectPortalPracticeBanks() {
    var grid = document.getElementById("ccna-practice-banks-grid");
    if (!grid) return;

    var all = window.CCNA_PRACTICE_100.ALL_SLUGS;
    if (!Array.isArray(all)) return;
    if (grid.querySelector("[data-ccna-practice-bank-index]")) return;

    var nBanks = practiceBankCount();
    var total = all.length;

    function formatRange(first, last) {
      if (first >= last) return String(first);
      return String(first) + "–" + String(last);
    }

    var summary = document.getElementById("ccna-practice-banks-summary");
    if (summary) {
      var lastBankCount = total - (nBanks - 1) * 100;
      var bankWord = nBanks === 1 ? "bank" : "banks";
      var summaryText =
        total +
        " practice questions in " +
        nBanks +
        " " +
        bankWord +
        " (positions 1–100, 101–200, and so on in hub order). ";
      if (lastBankCount > 0 && lastBankCount < 100) {
        summaryText +=
          "The newest bank (positions " +
          formatRange((nBanks - 1) * 100 + 1, nBanks * 100) +
          ") has " +
          lastBankCount +
          " questions until the list reaches 100; then the next bank appears automatically. ";
      }
      summaryText +=
        "Each bank has its own Random and Review session. Domain filter and adaptive learning apply to the bank you start.";
      summary.textContent = summaryText;
      summary.hidden = false;
    }

    grid.setAttribute(
      "aria-label",
      "Practice question banks: " +
        nBanks +
        " banks of up to 100 questions each (" +
        total +
        " total)"
    );

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
      if (isLastBank && isPartial) {
        article.classList.add("ccna-practice-bank--remainder");
      }
      var titleInner;
      if (countInBank === 0) {
        titleInner = formatRange(firstNum, slotEnd);
      } else {
        titleInner = formatRange(firstNum, endIdx);
      }
      h4.textContent = "Bank " + String(b) + " · questions " + titleInner;

      var actions = document.createElement("div");
      actions.className = "study-actions";
      actions.setAttribute("role", "group");
      actions.setAttribute("aria-label", "Practice question modes for bank " + String(b));

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
      if (countInBank === 0) {
        var p = document.createElement("p");
        p.className = "study-meta";
        p.innerHTML =
          "Reserved for questions <strong>" +
          formatRange(firstNum, slotEnd) +
          "</strong> when the hub list grows. <strong>Random</strong> and <strong>Review</strong> stay disabled until this range has items.";
        article.appendChild(p);
      }
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

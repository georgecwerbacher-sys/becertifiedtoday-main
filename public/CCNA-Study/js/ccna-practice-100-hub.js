(function () {
  "use strict";

  var KEY = "ccnaPractice100";
  var BANK_SIZE = 100;
  var FILTER_BANK_ID = "filter";
  var VERSION_11_2026_MAX = 300;
  var VERSION_20_MIN = 301;
  var TOPIC_MAP_URL = "/CCNA-Study/data/ccna-question-topic-map.json";
  var DOMAIN_NAMES = {
    "1": "Network fundamentals",
    "2": "LAN switching (network access)",
    "3": "Routing (IP connectivity)",
    "4": "IP services",
    "5": "Security fundamentals",
    "6": "Automation & programmability"
  };

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

  function hubIndexForSlug(slug) {
    var all = window.CCNA_PRACTICE_100.ALL_SLUGS;
    if (!slug || !Array.isArray(all)) return null;
    for (var i = 0; i < all.length; i++) {
      if (all[i] === slug) return i + 1;
    }
    return null;
  }

  function filterSlugsByHubMax(slugs, maxHubIndex) {
    if (!maxHubIndex || maxHubIndex < 1) return slugs.slice();
    var out = [];
    for (var i = 0; i < slugs.length; i++) {
      var idx = hubIndexForSlug(slugs[i]);
      if (idx && idx <= maxHubIndex) out.push(slugs[i]);
    }
    return out;
  }

  function filterSlugsByHubMin(slugs, minHubIndex) {
    if (!minHubIndex || minHubIndex < 1) return slugs.slice();
    var out = [];
    for (var i = 0; i < slugs.length; i++) {
      var idx = hubIndexForSlug(slugs[i]);
      if (idx && idx >= minHubIndex) out.push(slugs[i]);
    }
    return out;
  }

  function getSelectedPracticeFilter() {
    var sel = document.getElementById("ccna-practice-domain-select");
    if (!sel) return { domain: null, versionMax: null, versionMin: null };
    var v = String(sel.value || "").trim();
    if (v === "v11-2026") return { domain: null, versionMax: VERSION_11_2026_MAX, versionMin: null };
    if (v === "v20") return { domain: null, versionMin: VERSION_20_MIN, versionMax: null };
    if (/^[1-6]$/.test(v)) return { domain: v, versionMax: null, versionMin: null };
    return { domain: null, versionMax: null, versionMin: null };
  }

  function hasActivePracticeFilter(filter) {
    filter = filter || getSelectedPracticeFilter();
    return !!(filter.domain || filter.versionMax || filter.versionMin);
  }

  function filterSessionLabel(filter) {
    if (filter.versionMax) return "Version 1.1 2026";
    if (filter.versionMin) return "Version 2.0 2026";
    if (filter.domain) {
      var name = DOMAIN_NAMES[filter.domain] || "Domain " + filter.domain;
      return filter.domain + " — " + name;
    }
    return "Filtered set";
  }

  function applySlugsFilters(slugs, filter, assignments) {
    var out = slugs.slice();
    if (filter.domain) {
      if (!assignments || typeof assignments !== "object") return [];
      out = filterSlugsByMajor(out, assignments, filter.domain);
    }
    if (filter.versionMax) out = filterSlugsByHubMax(out, filter.versionMax);
    if (filter.versionMin) out = filterSlugsByHubMin(out, filter.versionMin);
    return out;
  }

  /** Full hub slice for an active portal filter; null when domain filter needs topic map still loading. */
  function collectFilteredSlugs(filter) {
    var all = window.CCNA_PRACTICE_100.ALL_SLUGS;
    if (!Array.isArray(all)) return [];
    if (filter.domain) {
      var map = window.CCNA_PRACTICE_100._topicAssignments;
      if (map === null) return null;
      if (map === false) return [];
    }
    return applySlugsFilters(all, filter, window.CCNA_PRACTICE_100._topicAssignments);
  }

  /** @deprecated use getSelectedPracticeFilter */
  function getSelectedPracticeDomain() {
    return getSelectedPracticeFilter().domain || "";
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

  function startWithOptionalDomain(mode, bankId, filter) {
    filter = filter || { domain: null, versionMax: null, versionMin: null };
    var domainMajor = filter.domain || null;
    var versionMax = filter.versionMax || null;
    var versionMin = filter.versionMin || null;
    if (!domainMajor) {
      start(mode, bankId, null, versionMax, versionMin);
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
      start(mode, bankId, domainMajor, versionMax, versionMin);
      return;
    }
    inst._topicAssignmentsPromise.then(function () {
      if (inst._topicAssignments === false) {
        window.alert(
          "Could not load the topic map for this site. Use \"All subjects\" or try again later."
        );
        return;
      }
      start(mode, bankId, domainMajor, versionMax, versionMin);
    });
  }

  window.CCNA_PRACTICE_100.ALL_SLUGS = ["qos-minimum-bandwidth-choose-two","security-physical-access-tailgating","private-ipv4-subnet-appropriate","etherchannel-lacp-active-active","rstp-port-states-choose-two","wireless-controller-enterprise-role","virtual-server-hypervisor-vswitch","http-get-crud-operation","rest-api-accept-header","firewall-stateful-connection-forwarding","lightweight-ap-wlc-authentication-forward","vty-access-list-ssh-secure","dhcp-relay-dhcpdiscover","arp-first-ping-switch-flood","stp-bpduguard-portfast-errdisable","stp-root-bridge-vlan110","trunk-native-vlan-untagged","wan-t1-bandwidth","wireless-rrm-channel-overlap","wlan-design-nonoverlapping-2-4-channels-1-6-11","wlan-nonoverlapping-channels-discontinuous-frequency","switch-mac-table-ingress-learning","control-plane-routing-decisions","ios-dns-lookup-default-behavior","dns-lookup-operation-definition","voice-data-vlan-access-ports-sw11","pat-vlan200-inside-source-overload","switch-unknown-unicast-flood","vrrp-gateway-redundancy-benefit","dhcp-ipv4-assigned-by-protocol","dhcp-pool-default-router-command","dhcp-relay-r4-fa01-acl100-exhibit","ospf-r14-r86-broadcast-dr-adjacency","native-vlan-security-separated","stp-portfast-default-immediate-forwarding","wireless-wpa2-aes-strongest","vm-shared-disk-resource","soho-broadband-shared-connection","snmp-trap-mib-requirement","standard-acl-permit-deny-two-subnets","netconf-xml-filter-get-config","sdn-controller-functions-choose-two","switch-egress-queue-during-transmit","wan-topology-point-to-point-simplicity","ntp-master-internal-clock-server","trunk-allowed-vlan-add-no-disruption","sdn-southbound-api-purpose","err-disabled-port-security-violation","northbound-rest-sdn-applications","physical-access-badge-readers-datacenter","private-ipv4-characteristic-registration","private-ipv4-appropriate-use-internal-only","data-plane-forwarding-lookup","sdn-automation-improvements-choose-two","ssh-crypto-rsa-key-generation","pki-components-crl-ca-choose-two","sdn-southbound-openflow-forwarding","wireless-band-select-5ghz-preference","wlc-wpa2-psk-gui-format","data-plane-forward-remote-client-traffic","ipv6-compress-db8-interface-command","ipv6-compress-hq-serial-s0-700-400f","ipv6-compress-2001-eb8-c1-2200-0331","wlc-pmf-comeback-spoofed-association","fhrp-benefit-default-gateway-redundancy","wlan-roam-reassociation-request-frame","wlan-probe-response-frame-type","fiber-om3-om4-fifty-micron-core","ap-switch-poe-cdp-discovery","syslog-severity-informational-level","dtp-dynamic-auto-passive-trunk","dtp-sw1-sw2-printer-vlan5-trunk","wlc-ds-port-switch-ap-traffic","syslog-trap-severity-informational-included","route-ad-ebgp-eigrp-ospf-r4-server","cloud-topology-public-private-hybrid","ios-clock-set-exec-date-time","rest-http-200-successful-request","router-inter-subnet-forwarding-role","sdn-controller-role-central-point","switch-known-mac-unicast-forward","rfc1918-purpose-conserve-public-ipv4","wlc-aaa-override-ise-dynamic-vlan","ftp-authentication-backup-config-copy","sdn-control-to-infrastructure-boundary","router-forward-hop-mac-rewrite","ipsec-tunnel-esp-encrypt-whole-packet","ipv6-static-summary-and-host-via-next-hops","firewall-role-untrusted-to-trusted","firewall-permit-deny-traffic-rules","portfast-benefit-user-data-sooner","vlan-hopping-mitigation-dtp-trunk","routing-longest-match-default-172-16-1-1","floating-static-default-route-router-a-command","r1-backup-default-route-via-r2-ad10","r1-management-network-static-route-new-server","ansible-playbook-task-vlan-config","spine-leaf-full-mesh-uplinks","sdn-data-plane-forwarding-router","wlc-hardening-disable-telnet-http","dna-center-overall-health-dashboard","hypervisor-vm-hardware-communication","distribution-layer-two-characteristics","layer3-switch-flood-broadcast-within-vlan","qos-pq-voice-over-data-traffic","dhcp-default-gateway-windows-workstation","subnet-included-hosts-192-168-1-0-26","network-automation-drivers-choose-two","tcp-vs-udp-connection-reliability","network-endpoints-security-definition","physical-access-control-scope","wireless-80211a-five-ghz-consideration","lldp-run-global-isp-handoff","r5-disable-discovery-gi0-1-cdp-lldp-verify","qos-voice-reduce-packet-loss","dna-center-add-device-two-events","portfast-benefits-choose-two","stp-portfast-bypass-states-choose-two","unused-switchports-black-hole-vlan","dhcp-snooping-rate-limit-function","dhcp-snooping-trust-server-same-switch-vlan1","sdn-controller-centralizes-control-plane","utp-cat5e-cat6a-two-similarities","ospf-dr-election-priority-options","ospf-dr-election-router-a-area-zero","ospf-ia-route-metric-display","access-layer-8021x-identity-security","dhcp-relay-different-subnet-forwarding","route-no-match-101016-discard","ssh-loopback-source-next-hop-10-0-1-15-exhibit","site-ab-tenge-sfp-sr-vs-lr-smf-intermittent-exhibit","switch-host-a-to-d-unknown-dest-flood-exhibit","switch-sw1-pc2-mac-missing-fa02-trunk-exhibit","gigabit-lx-t-l2-frame-similarity","wpa3-sae-improves-security","wireless-wpa3-perfect-forward-secrecy","subnet-en0-configured-ip-ifconfig-exhibit","subnet-split-10-70-128-19-two-vlans-choose-two","capwap-lightweight-ap-mode","etherchannel-lacp-active-switch2","etherchannel-lacp-trunk-dynamic-industry-standard","wireless-auth-layer2","three-tier-workstation-to-workstation-path","fhrp-two-benefits-choose-two","ssid-purpose-identifies-wlan","ssid-two-characteristics-choose-two","qos-llq-interactive-voice-video","sdn-southbound-api-controller-to-infrastructure","sdn-controller-dynamic-changes-southbound-api","ipv6-link-local-scope-neighbor-discovery","nat-inside-global-address-from-example","switch-collision-domain-per-port","icmp-echo-request-reply-ping","acl-numbered-fifteen-standard-range","vty-access-class-permit-any-after-deny-pc1","switchport-priority-extend-trust-ip-phone-access","spanning-tree-portfast-supported-access-ports","syslog-facility-definition","public-cloud-two-characteristics-choose-two","ipsec-pure-traffic-unicast-ip","dhcp-workstation-blocked-8021x","ftp-control-data-connections-capability","static-default-route-r1-r2-two-sites-exhibit","collapsed-core-small-organization-cost","ipv6-route-r17-ping-r18-wan-interface","ipv6-anycast-unicast-multiple-interfaces","radius-access-request-password-encrypted","ngips-user-activity-network-events","ipv6-unicast-vs-anycast-assignment","data-plane-fib-lookup-action","rapid-pvst-plus-per-vlan-instance","wlc-telnet-mitm-management","aaa-authentication-identity-verification","syn-flood-half-open-tcp-resources","lightweight-ap-centralized-access-mode","data-plane-actions-8021q-mac-lookup","wlc-centralized-auth-roaming","owe-opportunistic-wireless-encryption","physical-access-ip-cameras-monitoring","qos-marking-tos-ipv4-field","qos-trust-boundary-access-phone-pc-exhibit","wlc-lag-link-redundancy-load-balance","wlc-lag-configure-remove-reboot-requirement","poe-static-mode-guaranteed-power","switch-access-vlan20-voice-vlan30","https-uses-ssl-tls","ssid-wireless-lan-identifier","ssh-ip-domain-name-before-rsa-key","r1-ssh-secure-remote-access-choose-two","qos-traffic-shaping-buffer-excess","vlan-tagging-trunk-separation","utp-vs-stp-shielding-emi","flexconnect-local-switching-trunk-ap","wlan-passive-client-static-ip","ipv6-static-route-global-config-nexthop","qos-policing-exceed-drop-mark","sdn-disaggregation-control-data-plane","dna-center-intent-api-rest-put","amp-ngips-file-malware-analysis","password-complexity-enable-prerequisite","r1-username-engineer2-scrypt-local-database","commodity-switches-data-plane-forwarding","security-posture-practices-choose-two","wan-topology-full-mesh-reliability","wpa-tkip-mic-encryption-feature","tftp-operation-block-numbers-udp","ntp-master-fallback-upstream-failure","authentication-vs-authorization-definition","ospf-gigabitethernet-default-broadcast-network","public-cloud-benefit-internet-access","sdn-controller-centralizes-routing-decision","sdn-controller-function-making-routing-decisions","sdn-plane-forwards-user-traffic","collapsed-core-small-network-minimal-growth","wpa2-wpa3-ccmp-encryption-choose-two","mac-learning-switch-source-address","gigabit-lx-lh-vs-zx-fiber-reach","ospf-router-id-without-loopback-or-router-id","router-subnet-10pct-host-growth-r789","show-ip-route-eigrp-learned-prefix","lacp-etherchannel-sw1-sw2-mode-fix","switch2-lldp-timer-holdtime","ssh-vty-access-class-10-139-58-28","ssh-secure-remote-cli-protocol","private-ipv4-characteristic-no-registry","enterprise-network-wlc-auth-roaming","nat-pat-standard-acl1-gi01-exhibit","ipv6-vlan2000-unique-local-ula","ospf-r1-r2-point-to-point-no-dr-bdr","switchport-trunk-fa01-vlans-10-15-complete","route-best-path-10-10-10-24-exhibit","ip-address-dhcp-interface-client","endpoint-network-function-client-server","ipv6-internal-device-unique-local-address","etherchannel-port-channel10-lacp-modes-choose-two","ospf-dr-r1-priority-r3-zero-choose-two","r1-ntp-server-requirements-config","r1-floating-static-ospf-backup-server","ospf-r1-r2-p2p-link-network-command","ten-gigabitethernet0-0-0-slow-transfer-show-interface","ospf-serial-neighbor-stuck-exchange-mtu","routing-cpe-longest-match-192-168-1-250","switch-pc1-access-duplex-mismatch-performance","ipv6-ho-fa01-eui64-from-mac-topology","dhcp-relay-gi00-helper-server-subnet-exhibit","static-route-r14-172-21-34-25-via-r86","floating-static-router1-primary-default-route","switchport-trunk-allowed-vlan-add-104","wan-gigabitethernet0-0-0-crc-errors-poor-performance","ospf-r3-dr-priority-gi01-104","router1-longest-match-10-10-13-158-show-ip-route","r1-wan-lan-route-10-0-10-ad-precedence","r15-ssh-version2-minimum-config-show-run","wlc-80211r-fast-transition-ft-psk","etherchannel-lacp-sw1-active-sw2-passive-initiation","stp-vlan20-four-switch-root-bridge","nat-router1-vlan200-acl-inside-source-overload","switch-a-gi01-ip-phone-vlan50-voice51","r1-floating-static-19216820-via-r3-ospf-area20","r1-r2-floating-static-backup-gi01-workstation-lans","cat9300-cdp-timer-rapid-neighbor-discovery","sw2-fa01-dynamic-auto-trunk-allowed-vlan5-10","wlc-enterprise-wlan-80211r-fast-transition","etherchannel-lacp-sw1-sw2-g1-1-3-trunk-active","wlc-radius-authentication-server-network-user","ip-arp-inspection-vlan5-10-fa01-untrusted-effect","router-gi00-lldp-third-party-isp-exhibit","r1-show-ip-route-10-56-192-1-default-next-hop","wlc-wlan-security-wpa-wpa2-8021x-enterprise","cat9k-lldp-suppress-management-address","ospf-r1-drother-elect-dr-priority-clear","dc1-hq1-interface-usable-host-addresses","json-routers-switches-array-elements-are-values","vlan14-trunk-ring-sw4-sw11-sw9-pc2-pc7","ospf-r1-passive-priority-router-id-neighbor-r2-only","r1-static-route-10-0-3-via-transit-r3","r1-r2-floating-static-default-wan-failover","pc-a-pc-b-vlan200-switch-unicast-mac","collapsed-core-distribution-core-merged","vrrp-virtual-mac-iana-format","wlan-24ghz-us-nonoverlapping-channels-set","rapid-pvst-plus-forward-time-listen-learn","lacp-layer3-port-channel-neighbor-passive-after-static","dna-center-controller-purpose-manage-deploy","tftp-feature-anonymous-style-no-login","lightweight-ap-mode-centralized-wlc-ssid-roaming","nat-inside-source-static-private-to-public-pc","longest-match-10-1-1-19-rip-28-ospf-eigrp","rest-http-status-classes-errors-4xx-5xx","ssh-next-step-crypto-key-generate-after-domain-user","wpa3-encryption-method-sae","ssh-interface-acl-inbound-10-139-58-28","spine-leaf-predictable-latency-uniform-path","dna-center-traditional-campus-centralized-management","zero-day-exploit-vulnerability-no-patch","aaa-console-local-username-line-con-zero","snmp-v3-implied-by-snmp-server-user","switch-unknown-destination-mac-flood-except-ingress","port-security-trunk-default-violation-errdisable","multifactor-authentication-examples-choose-two","show-ip-route-10-10-13-160-slash-29-subnet-mask","endpoint-function-user-access-network-services","dhcp-relay-agent-features-choose-two","cloud-rapid-elasticity-capacity-demand","flexconnect-local-switch-different-vlans-trunk-port","wlc-config-serial-timeout-no-auto-logout","mac-address-learning-enabled-default-vlans","flexconnect-branch-local-switching-wan-survivability","poe-auto-mode-detects-powered-device","cpe-floating-static-default-when-ebgp-invalid","telnet-unsecured-remote-cli-access","wlc-functions-vs-autonomous-ap-choose-two","ospf-gi0-0-point-to-point-desired-full-dash","sw1-fa01-notconnect-wrong-cable-type","ssh-transport-rsa-modulus-2048-choose-two","longest-match-192-168-2-2-static-routes","json-mycar-wheels-warning-in-array","wlan-office-ssid-same-security-policies-branches","dna-center-single-pane-faster-deployment","tcp-udp-query-response-connection-model","serial0-ip-access-list-in-syntax-fails-apply","show-ip-route-10-10-8-14-slash-28-mask","private-ipv4-reasons-implement-choose-two","puppet-manifests-modules-paradigm","ipsec-tunnel-mode-encrypts-header-and-payload","wpa3-safeguards-brute-force-sae","show-ip-route-ospf-metric-172-16-0-128-25","traffic-policing-drop-remark-choose-two","static-route-best-path-10-10-10-3-slash-28","wlc-rogue-ap-class-type-friendly-autonomous","anti-replay-prevent-mitm-attack","ospf-r2-must-be-dr-gi0-0-priority","r1-show-ip-route-10-1-2-126-next-hop","r1-static-route-10-0-0-24-r3-pc1-via-r2","ospf-r2-wan-dr-gi0-0-address-priority","r1-route-host-b-10-10-13-25-lowest-ad","windows-ipconfig-dns-query-www-cisco-com","r1-static-route-r3-lan-10-0-15-via-20-3","wlc-wlan-80211r-enable-ft-8021x","json-aaa-user-nested-roles-object-count","r2-no-cdp-enable-g02-hide-neighbor-from-r3","port-security-dynamic-mac-restrict-violation-choose-two","r1-host-route-server-10-10-10-10-via-r2","northbound-api-function-sdn-controller-applications","qos-traffic-shaping-purpose","autonomous-ap-wlan-vlan-wired-trunk-port","switch-destination-mac-missing-cam-flood-vlan","collapsed-core-distribution-single-layer-characteristic","southbound-interface-controller-device-programs","private-address-space-primary-purpose-conserve","wlc-distribution-port-trunk-multiple-vlans","wpa2-wireless-encryption-cipher-aes","longest-prefix-match-192-168-10-5-entry-table","snmpv2-getbulk-inform-large-data-choose-two","forward-172-18-32-38-longest-match-g0-0","wpa3-enhancement-brute-force-protection","hsrp-virtual-ip-default-gateway","switch-frame-flooding-reasons-choose-two","tcp-over-udp-https-error-checking-ack","security-badge-datacenter-physical-access","vlan10-subnet-192-168-32-last-usable-no-switchport","ipv6-anycast-global-unicast-dhcp-dns","r19-fa0-0-output-drops-oversubscription","port-security-voip-mac-address-vlan-voice","wireless-encryption-protects-confidentiality-algorithm","firewall-segregates-zones-security-policies","ssid-specification-case-sensitive","private-ipv4-reason-security-breach-risk","ftp-fact-two-connections-control-data","ap-admin-auth-tacacs-radius-choose-two","nat-partial-config-outside-interface-cpe1","ipv4-private-address-conserve-global-unique","route-192-168-12-16-longest-prefix-ospf","ipv6-floating-default-route-cpe-nd","private-ipv4-benefit-shield-internal-devices","qos-policing-drops-exceed-committed-rate","trunk-dot1q-allowed-vlans-1-10","network-automation-consistent-configuration-state","vrrp-multivendor-default-gateway-redundancy","ssh-username-ccuser-secret-encrypted","route-172-16-4-0-subnet-mask-slash-21","wlc-management-interface-inband-ap-admin","wlc-fast-ssid-change-multiple-wlans","vpn-dmvpn-getvpn-branch-scale-choose-two","json-test-questions-three-arrays-count","router1-eth1-collisions-duplex-mismatch","sw1-pagp-group2-lacp-active-multivendor","forward-172-31-0-1-longest-prefix-25","password-protection-special-chars-max-length","ap-join-wlc-discovery-request-ap-manager","network-automation-reduce-config-inconsistencies","device-separates-security-domains-firewall","vm-characteristics-independent-same-hardware","r7-show-ip-route-default-eigrp-ex-null0","show-ip-route-172-16-3-254-slash-23-mask","rapid-pvst-backup-port-blocking-designated","wlc-sip-cac-media-snooping-platinum-qos","wpa3-personal-psk-ccmp128-cipher","dna-center-sdn-automation-controller-function","qos-marking-changes-dscp-ipv4-header","router-y-route-10-227-225-255-via-router-d","ipsec-suite-protocols-ah-esp-choose-two","private-ipv4-benefits-reuse-conserve-choose-two","sw1-vty-ssh-crypto-rsa-key-choose-two","json-switch-property-name-is-key","1000base-sx-gbic-sfp-lc-sc-patch-cable","wlc-distribution-lag-channel-group-active","subnet-mask-binary-11111000-slash-29","dns-resolver-authoritative-name-resolution-choose-two","switch-mac-address-aging-removes-stale","sdn-northbound-apis-soap-rest-choose-two","rest-http-messages-transfer-applications","switch-unknown-unicast-flooding-except-ingress","rsa-asymmetric-encryption-characteristic","dna-center-assurance-correlates-protocol-insights","signal-frequency-1hz-sixty-per-minute","lap-local-mode-wired-access-port","cat9300-gi1-0-1-trunk-match-native-321","sdn-controller-packet-handling-policies","server-fcs-err-physical-cable-fault","hypervisor-distributes-physical-resources-vm","wlc-config-network-webmode-http-access","loopback-ipv4-mapped-ipv6-prefix-128","wlc-console-port-oob-async-management","fhrp-protects-default-gateway-failure","forward-192-168-0-55-static-24-gi0-1","ospf-crossover-p2p-faster-full-adjacency","json-test-schema-objects-keys-lists","p2p-leased-line-simple-configuration-benefit","wpa2-wpa3-differences-sae-128-192-choose-two","syslog-transport-tcp-udp-choose-two","internet-default-route-ad-1-from-10-10-10-32","http-put-method-update-resource","northbound-rest-api-application-facing-http","forward-172-16-1-190-ospf-slash-29-via-35","ospf-r2-dead-interval-40-match-r1-neighbor","ospf-neighbor-must-match-area-hello-choose-two","ssh-remove-unnecessary-name-server-password-encryption","wlc-lag-increase-throughput-reason","wlc-oob-management-service-console-choose-two","fiber-vs-copper-distance-throughput-choose-two","vrrp-multivendor-subnet-interoperate-vendors","autonomous-vs-cloud-ap-deployment-comparison","crud-update-http-put-patch-choose-two","controller-based-architecture-advantages-choose-two","fa0-13-high-crc-input-errors-physical","ospf-overlapping-10-routes-all-three-in-table","rapid-pvst-portfast-bypass-learning-state","switch-learn-unknown-source-mac-ingress-port","sdn-southbound-api-flow-control-switching-fabric","r25-fa0-0-runts-duplex-mismatch","r25-fa0-0-txload-255-high-throughput","dhcp-relay-helper-192-168-10-1-cross-subnet","ospf-r2-gi01-area-1-match-r1-neighbor","route-10-0-1-3-slash-32-host-route-meaning","r1-ssh-version2-minimum-config-options","r19-fa0-0-collisions-portland-subnet","static-routes-same-destination-different-next-hop","r17-fa0-0-txload-255-high-throughput-chicago","10gbase-sr-lr-shared-fiber-media-property","datacenter-backup-more-specific-route-secondary-circuit","ospf-r2-hello-interval-10-match-r1-neighbor","soho-environment-characteristics-choose-two","syslog-severity-emergency-system-unusable","dna-center-apis-vs-traditional-manual-gathering","r25-fa0-0-queueing-tokyo-subnet","snmp-community-string-mib-access-password","wlc-lag-one-port-passes-client-traffic","r1-telnet-login-local-privilege-15-username","backdoor-malware-unauthorized-access-definition","wlc-console-connection-out-of-band-management","wlc-flexconnect-local-switching-wlan-advanced-gui","sw1-pc1-port-security-access-mac-exhibit","r2-wan-ipv6-global-unicast-internet-access","sw1-sw2-trunk-native-vlan5-layer3-all-pcs","r1-r2-p2p-subnet-minimum-two-growth-hosts","r1-gi0-0-ipv6-eui64-dynamic-assignment-block","ntp-clients-r1-r2-r3-show-run-exhibit","r1-floating-default-route-pc1-pc3-routing","router1-pat-1921681-pool-209165202129","sw1-voip-lldp-gi101-multivendor-discovery","wlc-guest-wlan-layer2-prep-web-auth-choose-two","r1-static-host-10-10-2-1-via-r3-ospf-override","pc-internet-tcp80-www-cisco-subnet-mask-exhibit","etherchannel-sw2-port-channel1-min-links-exhibit","newsw-trunk-native-vlan2-sw1-fa0-exhibit","wlc-userwl-vlan20-max-allowed-clients-exhibit","cpe-dual-isp-static-route-load-balance-exhibit","r2-lan-ipv6-eui64-address-exhibit","switch-a-etherchannel-lacp-passive-exhibit","r4-local-telnet-enable-secret-vty-exhibit","dscp-phb-assured-forwarding-drop-probability","switch-frame-switching-known-destination-forward","endpoint-protection-antivirus-software","rest-http-methods-get-post-choose-two","wlc-lag-redundancy-bandwidth-layer2-switch","hsrp-cisco-proprietary-edge-failover-recovery","wpa3-enhancement-pmf-deauth-disassociation","ipv6-link-local-all-nodes-multicast-ff02-1","gi1-ipv6-modified-eui64-from-mac-exhibit","wan-full-mesh-topology-disadvantages-choose-two","qos-classification-traffic-treatment-purpose","private-ipv4-benefit-reuse-same-addresses","sdn-separate-control-data-plane-advantage","r1-eigrp-ecmp-172-16-1-4-30-show-ip-route-exhibit","syslog-server-filter-by-severity-level","frame-switching-store-forward-buffer-error-check","json-router-r20-property-is-value","wlc-new-wlan-gui-profile-name-ssid-choose-two","vm-deploy-resource-limits-cpu-memory","stp-root-port-role-nonroot-best-path","wpa1-data-protection-tkip-encryption","r1-forward-192-168-20-75-longest-match-exhibit","switch-destination-mac-aged-out-flood-vlan","dhcp-snooping-identify-rogue-server-dhcoffer","rapid-pvst-plus-port-state-after-boot-discarding","lightweight-ap-split-mac-wlc-zero-touch","vm-components-configuration-files-hypervisor-resources","wlc-capwap-tunnel-source-ap-manager-interface","switch-cam-lookup-destination-mac-forwarding","hypervisor-type1-bare-metal-no-host-os","windows-ipv4-preferred-dhcp-renew-same-address","vrrp-lan-capabilities-redundancy-load-sharing-choose-two","forward-10-18-75-113-ospf-metric-g0-6-exhibit","ap-sniffer-mode-packet-analyzer-capture","layer2-switch-forwarding-decision-mac-address","r30-fa0-0-collisions-duplex-mismatch-madrid-exhibit","forward-10-47-114-119-eigrp-metric-f0-2-exhibit","tcp-preferred-over-udp-reliability-critical","pc-subnet-mask-192-168-25-128-and-100-same-lan","vrrp-protocol-default-gateway-fhrp-type","rfc1918-private-ipv4-nat-preserve-public","ap-firmware-updates-lightweight-require-wlc","dhcp-pool-control-helper-address-relay-server","r1-forward-10-56-0-62-longest-match-vlan58-exhibit","r1-gi001-line-protocol-down-duplex-mismatch-exhibit","json-interfaces-ethernet-object-type-shown","switch-mac-aging-default-300-seconds-workstation","wlc-radius-wireless-aaa-override-ip-address","hub-vs-switch-known-destination-mac-forwarding","essid-multiple-aps-common-wireless-network","port-security-restrict-unknown-mac-snmp-trap","vm-shared-hardware-resources-same-hypervisor","crossover-cable-like-devices-no-auto-mdix","pc2-unknown-mac-vlan-frame-flooding-concept","security-physical-access-tasks-choose-two","r9-fa0-0-queueing-atlanta-subnet-exhibit","security-phishing-user-awareness-training","ipsec-security-associations-peers-organization","multifactor-authentication-pin-rsa-certificate","network-automation-manual-errors-inconsistencies-consideration","tftp-loads-config-diskless-systems-capability","cat9k-gi101-broadcast-storm-printing-exhibit","ap-console-no-ip-management-connection","autonomous-ap-single-ssid-access-port","sw2-lacp-gi01-02-channel-group-active-exhibit","windows-service-desk-ipconfig-all-verify-ip-dns","dhcp-server-functions-centralized-dynamic-choose-two","snmp-inform-reliable-manager-acknowledgment","wlc-multiple-ap-manager-fewest-aps-join","wlc-service-manages-interference-dense-network","windows-dhcp-renew-contact-server-wifi-exhibit","json-cisco-devices-missing-closing-brace","private-ipv4-benefits-shortage-security-choose-two","access-switch-arp-spoof-dai-dhcp-snooping-po1-choose-two","wlc-maximum-concurrent-telnet-sessions-five","firewall-enterprise-vpn-url-functions-choose-two","chef-agent-pulls-cookbook-configuration-from-server","ansible-inventory-defines-target-devices","private-ipv4-host-addresses-rfc1918-choose-two","wlc-switch-etherchannel-load-balance-src-dst-ip","aaa-authentication-vs-accounting-choose-two","rest-api-supported-methods-get-put-post-delete","json-rfc4627-default-encoding-utf8","json-array-red-one-string-elements","branch-router-ntp-server-sync-head-office","router-wan1-gi00-isp-crc-collisions-duplex-exhibit","forward-100-100-100-100-longest-match-exhibit","rapid-pvst-plus-blocking-no-mac-learning","ftp-tcp-20-21-large-files-intranet","enterprise-device-certificate-auth-corporate-network","secure-password-policy-complex-length-guideline","sw1-vty-ssh-only-service-password-encryption-exhibit","ml-ids-identifies-intrusion-patterns","ipsec-vpn-deployment-transport-mode-consideration","split-mac-realtime-functions-processed-ap","authentication-biometric-physical-attribute","ansible-ssh-push-modules-to-nodes","dns-iterative-query-contact-servers","controller-based-vs-traditional-control-plane","ipsec-vpn-implementation-tunnel-mode-factor","wlc-inband-wireless-management-default-interface","dna-center-lifecycle-management-patches-updates","ipsec-tunnel-mode-site-to-site-capabilities-choose-two","ai-network-traffic-analysis-anomaly-detection","control-plane-exchanges-topology-information","rest-uri-identifies-target-resource","flexconnect-prefer-centralized-management-remote-offices","acl-services-add-tcp-dns-sequence-35-exhibit","windows-ipconfig-remote-subnet-verify-gateway-exhibit","mitigate-sniffed-admin-password-mfa","wlc-basic-config-create-wlan-bind-interface","ml-network-security-real-time-threat-detection","ap-hotspot-captive-portal-guest-access","split-mac-definition-data-link-layer","wlan-architectures-autonomous-cloud-splitmac-choose-two","ap-bridge-mode-point-to-multipoint-hub","network-automation-reduce-downtime-templates-testing","snmp-traps-vs-polling-push-pull","syslog-level-7-debug-monitoring","autonomous-ap-small-office-no-central-management","dns-aaaa-ipv6-address-record","wlc-aireos-gui-simultaneous-management-users-five","ssh-management-access-secured-inbound-purpose","automation-data-models-vendor-agnostic-complexity","generative-ai-network-operations-synthetic-configs","security-program-user-training-distribute-policies","wlc-lag-8023ad-bundle-distribution-ports","wlan-ssid-maximum-length-32-characters","container-virtualization-os-level-description","hsrp-implement-redundancy-router-failure","etherchannel-add-member-po1-lacp-layer3-exhibit","ospf-route-10-30-0-1-administrative-distance-exhibit","etherchannel-connect-switches-increase-bandwidth","sdn-security-unified-control-policies","radius-tacacs-separate-auth-authorization","r1-forward-10-0-4-10-show-ip-route-exhibit","aaa-operations-identification-services-access-control","r1-same-prefix-lowest-ad-route-installed","dai-trust-fa01-router-connected-device","wlc-wpa2-psk-minimum-passphrase-characters","office-ports-security-shutdown-8021x-choose-two","network-monitoring-highest-security-snmpv3","ipv6-multicast-address-block-ff00-12","r1-192-168-12-24-isis-ospf-rip-eigrp-installed","r1-show-ip-route-internal-eigrp-prefix-exhibit","nat-pool-10-10-0-0-source-three-global-addresses","hsrp-first-hop-redundancy-virtual-ip-mac","tftp-function-ios-image-firmware-upgrade","default-gateway-ad-static-route-exhibit","wlc-encrypted-mobility-tunnel-default-condition","api-keys-rate-limiting-identify-clients","wan-point-to-point-topology-behaviors-choose-two","switch-excessive-collisions-syslog-16-retries","virtualization-multiple-os-single-physical-server","mfa-otp-login-name-smartphone","predictive-ai-load-balancing-traffic-spikes","ap-bridge-mode-connect-campus-building-segments","vrf-logical-layer3-separation-physical-equipment","syslog-trap-informational-exclude-debug-flood","wlc-virtual-interface-dhcp-relay-exclusive","ipsec-remote-access-vpn-encrypted-tunnel-purpose","lightweight-ap-web-management-wlc-ip","qos-phb-shaping-policing-principles-choose-two","tcp-udp-connection-establishment-differentiator","hsrp-functionality-virtual-mac-lan-redundancy","macos-ifconfig-en0-default-gateway-first-usable","r3-show-ip-route-10-10-10-14-out-interface","layer2-switch-link-bundling-characteristic","json-line2-device-entry-is-object","rest-http-verbs-create-resource-choose-two","r4-show-ip-route-10-255-2-2-eigrp-protocol","production-network-600-servers-subnet-slash22","switch-unknown-dest-mac-flood-frame-exhibit","virtual-machines-guest-os-service-statement","mfa-complex-password-totp-minimum-security","r4-dynamic-routes-least-preferred-metric-rip","r1-forward-192-168-18-16-longest-prefix-gi10","lpm-152-168-32-85-next-hop-10-10-2-2","floating-default-route-ad-25-preempts-dynamic-20","mfa-main-capability-identity-two-factors","flexconnect-flex-local-switching-trunk-pruned-vlans","wpa3-personal-ssid-mandatory-pmf","digest-authentication-challenge-response-plaintext","trunk-port-carries-multiple-vlans","r1-192-168-64-22-null0-longest-prefix","aa-show-ip-route-192-168-20-1-static-ad","show-ip-route-default-ad-eigrp-ospf-choose-two","wpa3-implementation-security-protocol-gcmp","access-sw1-ntp-server-ipv6-replicate-config","layer2-switch-data-link-layer-characteristic","tftp-no-auth-acknowledges-data-sent","tcp-udp-difference-reliable-ordered-vs-latency","ansible-network-automation-features-choose-two","remote-access-vpn-employee-public-wifi","wlan-nonoverlapping-channels-reduce-interference","json-line3-load-balancer-entry-is-object","security-user-awareness-email-sensitive-leak","syslog-logging-facility-purpose-process","ap-bridge-mode-wireless-two-network-segments","dns-cname-alias-canonical-domain","border-router-static-172-16-153-154-next-hop","router-switch-straight-through-cable","r14-floating-static-r86-lan-external-eigrp","r1-lan-interface-ipv6-address-dhcp","r14-host-route-pc10-via-r86","r86-static-route-172-16-34-0-29-via-r14","r1-r3-loopback-valid-routes-ad-metric-choose-two","site-b-router2-no-default-route-192-168-0-10","r1-static-nat-pc1-to-r2-loopback","r1-static-routes-pc1-to-all-10-10-10-pcs-choose-two","r2-eigrp-next-hop-pc2-to-application-server","mdf-dc-default-stp-root-lowest-mac","sw1-sw12-multivendor-dot1q-trunk","r7-r8-r9-last-usable-interface-addresses","r1-static-route-new-office-172-25-25-via-r2","sw1-conference-room-port-security-maximum-two","sw1-vlan10-dhcp-helper-to-server-vlan20","r1-floating-static-rip-backup-192-168-23","switch-a-b-cat5-speed-mismatch-down","r1-best-path-1-0-0-8-lpm-metric-choose-two","new-york-ipv6-primary-and-floating-static-atlanta","sw1-host-d-to-host-a-unknown-unicast-vlan2","r1-least-desirable-route-metric-next-hop","network-automation-benefits-choose-two","router-dhcp-client-command","wlan-80211b-deploy-nonoverlapping-channels-best-practice","ipv6-interface-multicast-groups-joined-choose-two","json-structured-data-includes-arrays","ipv6-unique-local-inter-subnet-not-internet","service-password-encryption-prevents-plaintext","southbound-apis-openflow-netconf-choose-two","security-phishing-simulation-user-awareness-program","wpa2-psk-encryption-aes-128","ssh-operate-k9-image-domain-name-choose-two","nat-public-ip-inside-global-address","spine-leaf-scale-add-leaf-to-every-spine","wred-actions-choose-two","snmp-backup-router-configs-ios-mib","switch-fcs-failure-crc-input-errors-choose-two","ssh-rsa-key-dns-domain-name-prerequisite","ip-phone-untagged-pc-traffic-passthrough","router-p2p-slash-30-usable-address","wlc-benefit-centralized-ap-management","hsrp-predictable-behaviors-choose-two","wlan-80211-association-response-frame-type","ntp-trusted-server-client-mode-choose-two","hsrp-active-failure-standby-forwards","controller-based-network-characteristics-choose-two","ospf-eigrp-competing-route-administrative-distance","route-best-path-different-protocols-administrative-distance","stp-portfast-primary-effect-convergence-time","flexconnect-ap-mode-wlc-connectivity-lost","layer2-switch-unknown-destination-mac-flood-behavior","rest-api-encoding-methods-json-xml-choose-two","ipv6-multicast-group-address-block-ff00-8","ethernet-late-collisions-increment-choose-two","ospf-dr-election-most-significant-priority","dna-center-centralized-wired-wireless-management","client-server-architecture-server-primary-role","ieee-8021q-vlan-tag-size-bytes","rest-api-http-post-create-resource","router-ipv4-default-static-route-next-hop","catalyst-default-vlan1-ports-cannot-delete","router-vty-transport-input-ssh-encrypted-only","ios-banner-motd-pre-authentication-warning","nat-inside-source-static-192-168-1-10-mapping","cloud-services-scalability-without-physical-infrastructure","route-same-protocol-preferred-path-metric","ml-algorithms-model-network-behavior-unusual-activity","portfast-access-port-single-end-device","lldp-neighbors-detail-vendor-neutral-discovery","nat-pool-define-isp-209-165-200-range","ai-ml-proactive-unusual-traffic-patterns","layer3-switch-svi-inter-subnet-routing","stp-operation-layer2-root-priority-choose-two","layer3-interfaces-switch-router-choose-two","secure-remote-admin-ssh-acl-choose-two","vlan-core-advantages-segmentation-choose-two","nat-pat-overload-share-single-public-choose-two","ipv6-addressing-features-choose-two","ospf-link-state-cost-metric-choose-two","ios-static-ip-interface-commands-choose-two","switch-unknown-dest-mac-flood-except-ingress","show-ip-interface-brief-verify-status","tcp-udp-connection-establishment-three-way-handshake","hypervisor-virtualizes-cpu-memory-storage-vm","ipv6-address-eui-64-prefix-mac-command","switch-cam-flood-attack-host-c-to-a-port-security","rogue-dhcp-mitigate-snooping-dai-pair","acl-110-gi01-https-permitted-traffic","branch-office-site-to-site-ipsec-vpn-hq","rogue-switch-bpduguard-access-ports","corporate-wpa3-enterprise-192-bit-security","extended-acl-source-dest-port-filtering","dhcp-vlan20-helper-address-vlan10-server","syslog-severity-level-2-critical-meaning","nat-static-192-168-1-100-one-to-one-mapping","qos-wfq-llq-reorder-high-priority-voice","ntp-synchronize-clocks-inconsistent-log-timestamps","dhcp-pool-office-excluded-address-assignable-range","small-office-pat-single-public-ip-fifteen-hosts","ospf-abr-area0-area1-network-statements","ospf-default-administrative-distance-110","hsrp-preemption-router-a-recovers-priority-110","ospf-nbma-dr-bdr-manual-neighbor-config","longest-match-10-1-1-50-static-ospf-next-hop","ospf-ecmp-10-5-5-0-equal-cost-routes","voice-vlan-phone-pc-qos-separation-purpose","stp-loop-guard-blocking-forwarding-flap","switch-24-ports-vlan10-vlan20-trunk-domains","lap-centralized-local-mode-capwap-data-tunnel","lacp-active-passive-etherchannel-will-form","stp-triangle-root-bridge-lowest-priority","dot1q-trunk-native-vlan-untagged-statement","subnet-10-10-0-0-16-at-least-500-hosts","full-mesh-topology-highest-redundancy","inter-subnet-hosts-gateway-routing-troubleshoot","vm-network-service-hardware-utilization","ipv6-anycast-one-to-nearest-closest-interface","auto-mdix-switch-switch-either-cable","tcp-udp-reliable-ordered-vs-best-effort","subnet-172-16-0-0-22-usable-host-addresses","dna-center-intent-based-ai-ml-assurance","terraform-plan-apply-create-modify-resources","rest-api-http-401-authentication-required","ids-ml-anomaly-detection-unknown-attacks","dna-center-api-json-health-issues-exhibit","ansible-vs-terraform-agentless-provisioning","rest-api-put-update-vlan-description-200","generative-vs-predictive-ai-network-operations","predictive-ai-forecast-bandwidth-congestion","terraform-provider-plugins-ccna-v1-1","sdn-southbound-openflow-netconf-role","rest-api-json-interfaces-operational-loopback-ip","dna-center-northbound-rest-api","rest-api-get-interfaces-json-xml","sdn-control-plane-forwarding-decisions-centralized","port-security-errdisable-recovery-restore-port","port-security-mitigate-mac-flooding-dhcp-starvation","port-security-maximum-two-restrict-third-mac","dai-dhcp-snooping-binding-table-arp-spoofing","dhcp-snooping-prevent-rogue-dhcp-servers","wireless-client-isolation-peer-blocking-same-ssid","wpa3-enterprise-192-bit-gcmp-256-suite","unauthorized-rogue-access-point-corporate-network","wpa2-enterprise-8021x-eap-radius","wpa3-personal-sae-vs-wpa2-psk-handshake","wpa2-aes-ccmp-enterprise-minimum-standard","ipsec-vs-ssl-tls-vpn-comparison","ike-role-ipsec-negotiate-security-associations","hq-branch-site-to-site-ipsec-static-ips","ipsec-esp-data-confidentiality-vpn","remote-access-vpn-employee-laptop-internet","vty-access-class-10-0-0-24-implicit-deny","named-extended-acl-sequence-insert-entry","extended-acl-ping-icmp-denied-line-30","extended-acl-ssh-management-192-168-5-inbound"];
  window.CCNA_PRACTICE_100.SLUGS = window.CCNA_PRACTICE_100.ALL_SLUGS;

  function bankSlugs(bankId) {
    var all = window.CCNA_PRACTICE_100.ALL_SLUGS;
    var n = parseInt(String(bankId), 10);
    if (!n || n < 1) n = 1;
    var start = (n - 1) * BANK_SIZE;
    return all.slice(start, start + BANK_SIZE);
  }

  function practiceBankCount() {
    var all = window.CCNA_PRACTICE_100.ALL_SLUGS;
    if (!all || !all.length) return 1;
    return Math.ceil(all.length / BANK_SIZE);
  }

  function start(mode, bankId, domainMajor, versionMax, versionMin) {
    var filter = {
      domain: domainMajor || null,
      versionMax: versionMax || null,
      versionMin: versionMin || null
    };
    var useFilterPool = hasActivePracticeFilter(filter);
    var fixed;
    if (useFilterPool) {
      fixed = collectFilteredSlugs(filter);
      if (fixed === null) {
        window.alert("Topic assignments are still loading. Try again in a moment.");
        return;
      }
    } else {
      bankId = bankId || "1";
      fixed = bankSlugs(bankId);
    }
    if (!fixed.length) {
      window.alert(
        useFilterPool
          ? "No questions match the selected filter. Pick another subject or version, or choose “All subjects”."
          : "No questions in this bank. Try another bank."
      );
      return;
    }
    var order;
    if (mode === "linear") {
      order = fixed;
    } else {
      order = shuffle(fixed);
    }
    var session = {
      v: 1,
      mode: mode,
      bank: useFilterPool ? FILTER_BANK_ID : bankId,
      order: order
    };
    if (useFilterPool) {
      session.filtered = true;
      session.filterLabel = filterSessionLabel(filter);
    }
    if (domainMajor) session.domain = domainMajor;
    if (versionMax) session.versionMax = versionMax;
    if (versionMin) session.versionMin = versionMin;
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

  window.CCNA_PRACTICE_100.BANK_SIZE = BANK_SIZE;
  window.CCNA_PRACTICE_100.start = start;
  window.CCNA_PRACTICE_100.startWithOptionalDomain = startWithOptionalDomain;
  window.CCNA_PRACTICE_100.bankSlugs = bankSlugs;
  window.CCNA_PRACTICE_100.practiceBankCount = practiceBankCount;
  window.CCNA_PRACTICE_100.filterSlugsByMajor = filterSlugsByMajor;
  window.CCNA_PRACTICE_100.VERSION_11_2026_MAX = VERSION_11_2026_MAX;
  window.CCNA_PRACTICE_100.VERSION_20_MIN = VERSION_20_MIN;
  window.CCNA_PRACTICE_100.filterSlugsByHubMax = filterSlugsByHubMax;
  window.CCNA_PRACTICE_100.filterSlugsByHubMin = filterSlugsByHubMin;
  window.CCNA_PRACTICE_100.hubIndexForSlug = hubIndexForSlug;
  window.CCNA_PRACTICE_100.getSelectedPracticeFilter = getSelectedPracticeFilter;
  window.CCNA_PRACTICE_100.hasActivePracticeFilter = hasActivePracticeFilter;
  window.CCNA_PRACTICE_100.collectFilteredSlugs = collectFilteredSlugs;
  window.CCNA_PRACTICE_100.filterSessionLabel = filterSessionLabel;
  window.CCNA_PRACTICE_100.FILTER_BANK_ID = FILTER_BANK_ID;

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
        var filter = getSelectedPracticeFilter();
        if (m === "random" || m === "review") {
          startWithOptionalDomain(m, bank, filter);
        } else {
          start(m, bank, filter.domain, filter.versionMax, filter.versionMin);
        }
      }
    },
    false
  );

  function formatHubRange(first, last) {
    if (first >= last) return String(first);
    return String(first) + "–" + String(last);
  }

  function bindPortalFilterSelect() {
    var sel = document.getElementById("ccna-practice-domain-select");
    if (!sel || sel._ccnaFilterBound) return;
    sel._ccnaFilterBound = true;
    sel.addEventListener("change", injectPortalPracticeBanks);
  }

  function appendFilteredBankArticle(grid, filter, count, pending) {
    var label = filterSessionLabel(filter);
    var article = document.createElement("article");
    article.className = "sim-box ccna-practice-bank--filtered";
    article.setAttribute("data-ccna-practice-bank-index", FILTER_BANK_ID);
    article.setAttribute("aria-labelledby", "ccna-bank-title-filter");

    var h4 = document.createElement("h4");
    h4.className = "sim-box-title";
    h4.id = "ccna-bank-title-filter";
    h4.textContent = "Filtered set · " + label;
    article.appendChild(h4);

    var meta = document.createElement("p");
    meta.className = "ccna-bank-version-tag";
    if (pending) {
      meta.textContent = "Loading question count…";
    } else if (count === 1) {
      meta.textContent = "1 question across the full hub (not a numbered bank)";
    } else {
      meta.textContent =
        String(count) + " questions across the full hub (not a numbered bank)";
    }
    article.appendChild(meta);

    var actions = document.createElement("div");
    actions.className = "study-actions";
    actions.setAttribute("role", "group");
    actions.setAttribute("aria-label", "Practice modes for filtered set: " + label);

    var br = document.createElement("button");
    br.type = "button";
    br.className = "start-btn";
    br.setAttribute("data-ccna100", "random");
    br.setAttribute("data-ccna100-bank", FILTER_BANK_ID);
    br.textContent = "Random";

    var rev = document.createElement("button");
    rev.type = "button";
    rev.className = "start-btn";
    rev.setAttribute("data-ccna100", "review");
    rev.setAttribute("data-ccna100-bank", FILTER_BANK_ID);
    rev.textContent = "Review";

    if (pending || !count) {
      br.disabled = true;
      rev.disabled = true;
      if (!pending && !count) {
        br.classList.add("is-placeholder");
        rev.classList.add("is-placeholder");
      }
    }

    actions.appendChild(br);
    actions.appendChild(rev);
    article.appendChild(actions);
    grid.appendChild(article);
  }

  function updatePortalBanksSummary(all, filter, filteredCount, pending) {
    var summary = document.getElementById("ccna-practice-banks-summary");
    if (!summary) return;

    var total = all.length;
    var nBanks = practiceBankCount();
    var summaryText;

    if (hasActivePracticeFilter(filter)) {
      var label = filterSessionLabel(filter);
      if (pending) {
        summaryText =
          "Loading questions for “" +
          label +
          "”. Random and Review will use every matching question in the hub—not a fixed 100-question bank.";
      } else {
        summaryText =
          (filteredCount === 1 ? "1 question" : filteredCount + " questions") +
          " match “" +
          label +
          "” across the full hub (" +
          total +
          " total). Random and Review use only this filtered set across the hub—not a numbered bank slice.";
      }
    } else {
      var lastBankCount = total - (nBanks - 1) * BANK_SIZE;
      var bankWord = nBanks === 1 ? "bank" : "banks";
      summaryText =
        total +
        " practice questions in " +
        nBanks +
        " " +
        bankWord +
        " (positions 1–100, 101–200, and so on in hub order). ";
      if (lastBankCount > 0 && lastBankCount < BANK_SIZE) {
        summaryText +=
          "The newest bank (positions " +
          formatHubRange((nBanks - 1) * BANK_SIZE + 1, nBanks * BANK_SIZE) +
          ") has " +
          lastBankCount +
          " questions until the list reaches " +
          BANK_SIZE +
          "; then the next bank appears automatically. ";
      }
      summaryText +=
        "Each bank has its own Random and Review session. Pick a subject or version above to bypass banks and practice the full filtered hub instead.";
    }

    summary.textContent = summaryText;
    summary.hidden = false;
  }

  /** CCNA_Training_Portal.html: numbered banks, or one temporary bank when a filter is active. */
  function injectPortalPracticeBanks() {
    var grid = document.getElementById("ccna-practice-banks-grid");
    if (!grid) return;

    bindPortalFilterSelect();

    var all = window.CCNA_PRACTICE_100.ALL_SLUGS;
    if (!Array.isArray(all)) return;

    var prior = grid.querySelectorAll("[data-ccna-practice-bank-index]");
    for (var pi = 0; pi < prior.length; pi++) prior[pi].remove();
    var loadingEl = document.getElementById("ccna-practice-banks-loading");
    if (loadingEl) loadingEl.remove();

    var filter = getSelectedPracticeFilter();
    var filterActive = hasActivePracticeFilter(filter);
    var nBanks = practiceBankCount();
    var total = all.length;

    if (filterActive && filter.domain && window.CCNA_PRACTICE_100._topicAssignments === null) {
      updatePortalBanksSummary(all, filter, 0, true);
      grid.setAttribute(
        "aria-label",
        "Filtered practice set: " + filterSessionLabel(filter) + " (loading)"
      );
      appendFilteredBankArticle(grid, filter, 0, true);
      window.CCNA_PRACTICE_100._topicAssignmentsPromise.then(function () {
        injectPortalPracticeBanks();
      });
      return;
    }

    if (filterActive) {
      var filtered = collectFilteredSlugs(filter);
      var filteredCount = filtered ? filtered.length : 0;
      updatePortalBanksSummary(all, filter, filteredCount, false);
      grid.setAttribute(
        "aria-label",
        "Filtered practice set: " +
          filterSessionLabel(filter) +
          " (" +
          filteredCount +
          " questions)"
      );
      appendFilteredBankArticle(grid, filter, filteredCount, false);
      return;
    }

    updatePortalBanksSummary(all, filter, 0, false);

    grid.setAttribute(
      "aria-label",
      "Practice question banks: " +
        nBanks +
        " banks of up to " +
        BANK_SIZE +
        " questions each (" +
        total +
        " total)"
    );

    for (var b = 1; b <= nBanks; b++) {
      var startIdx = (b - 1) * BANK_SIZE;
      var endIdx = Math.min(b * BANK_SIZE, all.length);
      var firstNum = startIdx + 1;
      var slotEnd = b * BANK_SIZE;
      var countInBank = endIdx > startIdx ? endIdx - startIdx : 0;

      var article = document.createElement("article");
      article.className = "sim-box";
      article.setAttribute("data-ccna-practice-bank-index", String(b));
      article.setAttribute("aria-labelledby", "ccna-bank-title-" + b);

      var h4 = document.createElement("h4");
      h4.className = "sim-box-title";
      h4.id = "ccna-bank-title-" + b;
      var isLastBank = b === nBanks;
      var isPartial = countInBank > 0 && countInBank < BANK_SIZE;
      if (isLastBank && isPartial) {
        article.classList.add("ccna-practice-bank--remainder");
      }
      var titleInner;
      if (countInBank === 0) {
        titleInner = formatHubRange(firstNum, slotEnd);
      } else {
        titleInner = formatHubRange(firstNum, endIdx);
      }
      h4.textContent = "Bank " + String(b) + " · questions " + titleInner;

      article.appendChild(h4);
      var verTag = document.createElement("p");
      verTag.className = "ccna-bank-version-tag";
      if (firstNum >= VERSION_20_MIN) {
        verTag.textContent = "Version 2.0 2026";
      } else if (endIdx <= VERSION_11_2026_MAX) {
        verTag.textContent = "Version 1.1 2026";
      } else {
        verTag.textContent = "Version 1.1 2026 & Version 2.0 2026";
      }
      article.appendChild(verTag);

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
      article.appendChild(actions);

      grid.appendChild(article);
    }
  }

  window.CCNA_PRACTICE_100.injectPortalPracticeBanks = injectPortalPracticeBanks;

  function schedulePortalPracticeBanks() {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", injectPortalPracticeBanks, { once: true });
    } else {
      injectPortalPracticeBanks();
    }
  }

  schedulePortalPracticeBanks();
  window.addEventListener("pageshow", injectPortalPracticeBanks);
})();

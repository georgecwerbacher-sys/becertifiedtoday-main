(function () {
  "use strict";

  var KEY = "ccnaPractice100";

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
  window.CCNA_PRACTICE_100.SLUGS = ["qos-minimum-bandwidth-choose-two", "security-physical-access-tailgating", "private-ipv4-subnet-appropriate", "etherchannel-lacp-active-active", "rstp-port-states-choose-two", "wireless-controller-enterprise-role", "virtual-server-hypervisor-vswitch", "http-get-crud-operation", "rest-api-accept-header", "firewall-stateful-connection-forwarding", "lightweight-ap-wlc-authentication-forward", "vty-access-list-ssh-secure", "dhcp-relay-dhcpdiscover", "arp-first-ping-switch-flood", "stp-bpduguard-portfast-errdisable", "stp-root-bridge-vlan110", "trunk-native-vlan-untagged", "wan-t1-bandwidth", "wireless-rrm-channel-overlap", "switch-mac-table-ingress-learning", "control-plane-routing-decisions", "ios-dns-lookup-default-behavior", "voice-data-vlan-access-ports-sw11", "pat-vlan200-inside-source-overload", "switch-unknown-unicast-flood", "vrrp-gateway-redundancy-benefit", "dhcp-ipv4-assigned-by-protocol", "dhcp-pool-default-router-command", "native-vlan-security-separated", "stp-portfast-default-immediate-forwarding", "wireless-wpa2-aes-strongest", "vm-shared-disk-resource", "soho-broadband-shared-connection", "snmp-trap-mib-requirement", "standard-acl-permit-deny-two-subnets", "netconf-xml-filter-get-config", "sdn-controller-functions-choose-two", "switch-egress-queue-during-transmit", "wan-topology-point-to-point-simplicity", "ntp-master-internal-clock-server", "trunk-allowed-vlan-add-no-disruption", "sdn-southbound-api-purpose", "err-disabled-port-security-violation", "northbound-rest-sdn-applications", "physical-access-badge-readers-datacenter", "private-ipv4-characteristic-registration", "data-plane-forwarding-lookup", "sdn-automation-improvements-choose-two", "ssh-crypto-rsa-key-generation", "sdn-southbound-openflow-forwarding", "wireless-band-select-5ghz-preference", "wlc-wpa2-psk-gui-format", "data-plane-forward-remote-client-traffic", "ipv6-compress-db8-interface-command", "wlc-pmf-comeback-spoofed-association", "fhrp-benefit-default-gateway-redundancy", "wlan-roam-reassociation-request-frame", "fiber-om3-om4-fifty-micron-core", "ap-switch-poe-cdp-discovery", "syslog-severity-informational-level", "dtp-dynamic-auto-passive-trunk", "wlc-ds-port-switch-ap-traffic", "syslog-trap-severity-informational-included", "route-ad-ebgp-eigrp-ospf-r4-server", "cloud-topology-public-private-hybrid", "ios-clock-set-exec-date-time", "rest-http-200-successful-request", "router-inter-subnet-forwarding-role", "sdn-controller-role-central-point", "switch-known-mac-unicast-forward", "rfc1918-purpose-conserve-public-ipv4", "wlc-aaa-override-ise-dynamic-vlan", "ftp-authentication-backup-config-copy", "sdn-control-to-infrastructure-boundary", "router-forward-hop-mac-rewrite", "ipsec-tunnel-esp-encrypt-whole-packet", "ipv6-static-summary-and-host-via-next-hops", "firewall-role-untrusted-to-trusted", "portfast-benefit-user-data-sooner", "vlan-hopping-mitigation-dtp-trunk", "routing-longest-match-default-172-16-1-1", "ansible-playbook-task-vlan-config", "spine-leaf-full-mesh-uplinks", "sdn-data-plane-forwarding-router", "wlc-hardening-disable-telnet-http", "dna-center-overall-health-dashboard", "hypervisor-vm-hardware-communication", "distribution-layer-two-characteristics", "qos-pq-voice-over-data-traffic", "dhcp-default-gateway-windows-workstation", "subnet-included-hosts-192-168-1-0-26", "network-automation-drivers-choose-two", "tcp-vs-udp-connection-reliability", "network-endpoints-security-definition", "physical-access-control-scope", "wireless-80211a-five-ghz-consideration", "lldp-run-global-isp-handoff", "qos-voice-reduce-packet-loss", "dna-center-add-device-two-events", "portfast-benefits-choose-two", "unused-switchports-black-hole-vlan"];

  function start(mode) {
    var fixed = window.CCNA_PRACTICE_100.SLUGS.slice();
    var order;
    if (mode === "linear") {
      order = fixed;
    } else {
      order = shuffle(fixed);
    }
    var session = { v: 1, mode: mode, order: order };
    try {
      sessionStorage.setItem(KEY, JSON.stringify(session));
    } catch (e) {}
    window.location.href =
      "/CCNA-Study/CCNA_questions/" + order[0] + ".html#ccnaP=0";
  }

  window.CCNA_PRACTICE_100.start = start;

  function bindHub() {
    document.querySelectorAll("[data-ccna100]").forEach(function (el) {
      el.addEventListener("click", function () {
        var m = el.getAttribute("data-ccna100");
        if (m === "linear" || m === "random" || m === "review") start(m);
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bindHub);
  } else {
    bindHub();
  }
})();

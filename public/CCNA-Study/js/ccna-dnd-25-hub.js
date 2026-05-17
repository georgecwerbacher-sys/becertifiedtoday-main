(function () {
  "use strict";

  var BASE = "/CCNA-Study/CCNA_D_D/";
  var SLUGS = [
    "dragdrop-80211-standards-matching",
    "dragdrop-80211-standards-nonoverlapping-channels",
    "dragdrop-aaa-accounting-auth-resources-unused-one",
    "dragdrop-aaa-accounting-auth-statements-unused-two",
    "dragdrop-aaa-auth-authz-statements-unused-two",
    "dragdrop-aaa-features-accounting-authorization-unused-two",
    "dragdrop-aaa-features-auth-authz-unused-two",
    "dragdrop-aaa-services-by-description",
    "dragdrop-aaa-services-statements-by-category",
    "dragdrop-aaa-terms-descriptions",
    "dragdrop-ap-monitor-sensor-sniffer-statements",
    "dragdrop-ansible-features-unused-two",
    "dragdrop-ansible-terms-to-definitions",
    "dragdrop-autonomous-lightweight-ap-facts",
    "dragdrop-configuration-management-terms-unused-pull",
    "dragdrop-cloud-essential-characteristics-to-descriptions",
    "dragdrop-cloud-lightweight-ap-architecture-facts-unused",
    "dragdrop-device-management-campus-traditional-statements",
    "dragdrop-device-management-dna-traditional-netflow-cli",
    "dragdrop-device-management-dna-traditional-use-cases",
    "dragdrop-device-management-types-by-description",
    "dragdrop-dna-center-vs-traditional-characteristics",
    "dragdrop-dhcp-functions-unused",
    "dragdrop-dns-lookup-commands-to-functions",
    "dragdrop-dns-lookup-components",
    "dragdrop-dns-lookup-operation-steps-order",
    "dragdrop-enable-secret-command-sequence",
    "dragdrop-fiber-multimode-singlemode-characteristics",
    "dragdrop-hsrp-state-behaviors",
    "dragdrop-ios-dns-commands-to-effects",
    "dragdrop-ipv6-addresses-to-types",
    "dragdrop-ipv6-addresses-to-types-set-two",
    "dragdrop-ipv6-address-examples-to-descriptions",
    "dragdrop-ipv6-global-unicast-linklocal-characteristics",
    "dragdrop-ipv6-global-unicast-linklocal-single-link",
    "dragdrop-ipv6-global-unicast-multicast-characteristics",
    "dragdrop-ipv6-global-unicast-unique-local-characteristics",
    "dragdrop-ipv6-global-unicast-ula-characteristics",
    "dragdrop-ipv6-ula-linklocal-descriptions-unused-one",
    "dragdrop-ipv6-address-type-characteristics",
    "dragdrop-ipv6-anycast-multicast-characteristics",
    "dragdrop-ipv6-anycast-multicast-type-statements",
    "dragdrop-ipv6-anycast-multicast-unicast-details",
    "dragdrop-lightweight-ap-operation-modes",
    "dragdrop-northbound-api-characteristics-unused-three",
    "dragdrop-networking-statements-by-type-v2",
    "dragdrop-networking-types-statements-unused",
    "dragdrop-ospf-learned-prefixes-subnet-masks",
    "dragdrop-qos-terms-descriptions",
    "dragdrop-qos-traffic-types-delivery-mechanisms",
    "dragdrop-radius-tacacs-aaa-functions",
    "dragdrop-rapid-pvst-forwarding-state-actions",
    "dragdrop-rest-http-methods-actions-unused-patch",
    "dragdrop-rest-http-methods-descriptions",
    "dragdrop-rf-terms-to-statements",
    "dragdrop-route-ad-winner-multiprotocol-conditions",
    "dragdrop-router1-masks-to-prefixes-unused-one",
    "dragdrop-security-program-elements-descriptions",
    "dragdrop-snmp-fault-management-functions",
    "dragdrop-snmp-components-to-descriptions",
    "dragdrop-snmp-verify-commands",
    "dragdrop-split-mac-autonomous-benefits",
    "dragdrop-subnet-masks-to-prefixes-unused-one",
    "dragdrop-subnet-masks-to-101013-prefixes-unused-two",
    "dragdrop-tcp-udp-best-effort-reliable",
    "dragdrop-tcp-udp-connection-reliable-best-effort",
    "dragdrop-tcp-udp-details-by-category",
    "dragdrop-tcpip-protocols-primary-transport",
    "dragdrop-traditional-controller-networking-statements",
    "dragdrop-vlan-port-modes-to-descriptions",
    "dragdrop-virtualization-concepts-to-statements",
    "dragdrop-wifi-terms-to-descriptions",
    "dragdrop-wireless-ap-architecture-facts-unused",
  ];

  function shuffle(arr) {
    var out = arr.slice();
    for (var i = out.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = out[i];
      out[i] = out[j];
      out[j] = t;
    }
    return out;
  }

  function start(mode) {
    var order = shuffle(SLUGS);
    var first = order[0];
    var qs = mode === "review" ? "?mode=review" : "?mode=random";
    var session = { v: 1, mode: mode, order: order };
    try {
      sessionStorage.setItem("ccnaDnd25", JSON.stringify(session));
    } catch (e) {}
    window.location.href = BASE + first + ".html" + qs + "#ccnaDd=0";
  }

  function bind() {
    document.querySelectorAll("[data-ccnadd25]").forEach(function (el) {
      el.addEventListener("click", function () {
        var mode = el.getAttribute("data-ccnadd25");
        if (mode === "random" || mode === "review") start(mode);
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bind);
  } else {
    bind();
  }
})();

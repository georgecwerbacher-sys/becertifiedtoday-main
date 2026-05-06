(function () {
  "use strict";

  var BASE = "/CCNA-Study/CCNA_D_D/";
  var SLUGS = [
    "dragdrop-snmp-verify-commands",
    "dragdrop-80211-standards-matching",
    "dragdrop-dhcp-functions-unused",
    "dragdrop-ipv6-address-type-characteristics",
    "dragdrop-enable-secret-command-sequence",
    "dragdrop-networking-types-statements-unused",
    "dragdrop-dns-lookup-components",
    "dragdrop-aaa-terms-descriptions",
    "dragdrop-lightweight-ap-operation-modes",
    "dragdrop-device-management-types-by-description",
    "dragdrop-tcpip-protocols-primary-transport",
    "dragdrop-rapid-pvst-forwarding-state-actions",
    "dragdrop-aaa-services-by-description",
    "dragdrop-tcp-udp-details-by-category",
    "dragdrop-networking-statements-by-type-v2"
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
    window.location.href = BASE + first + ".html" + qs;
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

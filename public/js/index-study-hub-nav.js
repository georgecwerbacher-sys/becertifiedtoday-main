/**
 * index.html — "Open study hub" cards: portal if access active on this browser, else gate dialog.
 */
(function () {
  function hasCcnaPortalAccess() {
    return typeof window.bccPortalAccessActive === "function" && window.bccPortalAccessActive();
  }

  function hasEncorPortalAccess() {
    return typeof window.bccEncorPortalAccessActive === "function" && window.bccEncorPortalAccessActive();
  }

  function createGateController(gateRoot) {
    var gatePanel = gateRoot && gateRoot.querySelector(".ccna-sim-promo-panel");
    var prevOverflow = "";
    var gateOpen = false;

    function closeGate() {
      if (!gateRoot || !gateOpen) return;
      gateOpen = false;
      gateRoot.classList.remove("ccna-sim-promo-root--open");
      gateRoot.setAttribute("hidden", "");
      gateRoot.setAttribute("aria-hidden", "true");
      document.body.style.overflow = prevOverflow;
      document.removeEventListener("keydown", onKeyGate);
    }

    function openGate() {
      if (!gateRoot || !gatePanel || gateOpen) return;
      gateOpen = true;
      prevOverflow = document.body.style.overflow;
      document.body.style.overflow = "hidden";
      gateRoot.removeAttribute("hidden");
      gateRoot.classList.add("ccna-sim-promo-root--open");
      gateRoot.setAttribute("aria-hidden", "false");
      gatePanel.focus();
      document.addEventListener("keydown", onKeyGate);
    }

    function onKeyGate(ev) {
      if (ev.key === "Escape") {
        ev.preventDefault();
        closeGate();
      }
    }

    gateRoot.querySelectorAll("[data-index-gate-dismiss]").forEach(function (el) {
      el.addEventListener("click", function () {
        closeGate();
      });
    });

    return { openGate: openGate, closeGate: closeGate };
  }

  function wireHubLink(linkEl, hasAccess, gate) {
    if (!linkEl || !gate) return;
    linkEl.addEventListener("click", function (ev) {
      if (hasAccess()) return;
      ev.preventDefault();
      gate.openGate();
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var ccnaGateRoot = document.getElementById("indexCcnaPortalGateRoot");
    var encorGateRoot = document.getElementById("indexEncorPortalGateRoot");
    var ccnaLink = document.getElementById("path-ccna");
    var encorLink = document.getElementById("path-encor");

    var ccnaGate = ccnaGateRoot ? createGateController(ccnaGateRoot) : null;
    var encorGate = encorGateRoot ? createGateController(encorGateRoot) : null;

    wireHubLink(ccnaLink, hasCcnaPortalAccess, ccnaGate);
    wireHubLink(encorLink, hasEncorPortalAccess, encorGate);
  });
})();

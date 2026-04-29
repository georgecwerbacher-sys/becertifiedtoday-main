(function () {
  function onReady(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
      return;
    }
    fn();
  }

  onReady(function () {
    if (!document.body || document.querySelector("[data-global-site-menu]")) return;

    var nav = document.createElement("nav");
    nav.setAttribute("data-global-site-menu", "true");
    nav.setAttribute("aria-label", "Site menu");
    nav.style.position = "sticky";
    nav.style.top = "0";
    nav.style.zIndex = "1000";
    nav.style.display = "flex";
    nav.style.flexWrap = "wrap";
    nav.style.alignItems = "center";
    nav.style.gap = "10px";
    nav.style.padding = "10px 14px";
    nav.style.borderBottom = "1px solid #2d3b5a";
    nav.style.background = "rgba(11,16,32,0.95)";
    nav.style.backdropFilter = "blur(6px)";

    function addLink(label, href, options) {
      var a = document.createElement("a");
      a.textContent = label;
      a.href = href;
      a.style.display = "inline-flex";
      a.style.alignItems = "center";
      a.style.minHeight = "34px";
      a.style.padding = "6px 12px";
      a.style.borderRadius = "8px";
      a.style.border = "1px solid #4f84d8";
      a.style.color = "#e6edf3";
      a.style.textDecoration = "none";
      a.style.fontSize = "0.9rem";
      a.style.fontWeight = "700";
      a.style.background = "rgba(79,132,216,0.08)";
      if (options && options.id) {
        a.id = options.id;
      }
      if (options && options.youtube) {
        a.style.borderColor = "#c43b3b";
        a.style.background = "#c43b3b";
        a.style.color = "#ffffff";
      }
      if (options && options.alignRight) {
        a.style.marginLeft = "auto";
      }
      if (options && options.newTab) {
        a.target = "_blank";
        a.rel = "noopener noreferrer";
      }
      nav.appendChild(a);
    }

    function addTrainingAccessMenu() {
      var wrap = document.createElement("div");
      wrap.style.position = "relative";
      wrap.style.display = "inline-flex";

      var trigger = document.createElement("button");
      trigger.type = "button";
      trigger.textContent = "Training Access";
      trigger.style.display = "inline-flex";
      trigger.style.alignItems = "center";
      trigger.style.minHeight = "34px";
      trigger.style.padding = "6px 12px";
      trigger.style.borderRadius = "8px";
      trigger.style.border = "1px solid #4f84d8";
      trigger.style.color = "#e6edf3";
      trigger.style.fontSize = "0.9rem";
      trigger.style.fontWeight = "700";
      trigger.style.background = "rgba(79,132,216,0.08)";
      trigger.style.cursor = "pointer";

      var menu = document.createElement("div");
      menu.style.position = "absolute";
      menu.style.top = "42px";
      menu.style.left = "0";
      menu.style.minWidth = "170px";
      menu.style.padding = "8px";
      menu.style.border = "1px solid #2d3b5a";
      menu.style.borderRadius = "10px";
      menu.style.background = "#0f1730";
      menu.style.display = "none";
      menu.style.boxShadow = "0 8px 18px rgba(0,0,0,0.35)";

      var ciscoLabel = document.createElement("div");
      ciscoLabel.textContent = "Cisco";
      ciscoLabel.style.padding = "6px 8px";
      ciscoLabel.style.color = "#9fb8e5";
      ciscoLabel.style.fontWeight = "700";
      ciscoLabel.style.fontSize = "0.82rem";

      var encorLink = document.createElement("a");
      encorLink.textContent = "ENCOR";
      encorLink.href = "https://becertifiedtoday-encor.vercel.app";
      encorLink.style.display = "block";
      encorLink.style.padding = "6px 8px";
      encorLink.style.marginTop = "2px";
      encorLink.style.borderRadius = "6px";
      encorLink.style.color = "#e6edf3";
      encorLink.style.textDecoration = "none";
      encorLink.style.background = "rgba(79,132,216,0.08)";

      menu.appendChild(ciscoLabel);
      menu.appendChild(encorLink);
      wrap.appendChild(trigger);
      wrap.appendChild(menu);
      nav.appendChild(wrap);

      function show() {
        menu.style.display = "block";
      }
      function hide() {
        menu.style.display = "none";
      }

      wrap.addEventListener("mouseenter", show);
      wrap.addEventListener("mouseleave", hide);
      trigger.addEventListener("focus", show);
      wrap.addEventListener("focusout", function (event) {
        if (!wrap.contains(event.relatedTarget)) hide();
      });
    }

    addLink("Home", "/");
    addTrainingAccessMenu();
    addLink("Access Help", "/cert-access-help.html");
    addLink("Follow on YouTube", "https://www.youtube.com/@BeCertifiedToday", {
      alignRight: true,
      youtube: true,
      newTab: true,
    });

    document.body.insertBefore(nav, document.body.firstChild);
  });
})();

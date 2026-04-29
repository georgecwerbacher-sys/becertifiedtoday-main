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

    addLink("Home", "/");
    addLink("Access Help", "/cert-access-help.html");
    addLink("Follow on YouTube", "https://www.youtube.com/@BeCertifiedToday", {
      alignRight: true,
      youtube: true,
      newTab: true,
    });

    document.body.insertBefore(nav, document.body.firstChild);
  });
})();

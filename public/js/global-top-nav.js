(function () {
  function ready(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
      return;
    }
    fn();
  }

  ready(function () {
    if (!document.body || document.querySelector("[data-global-top-nav]")) return;

    var nav = document.createElement("nav");
    nav.setAttribute("data-global-top-nav", "true");
    nav.setAttribute("aria-label", "Global page navigation");
    nav.style.position = "sticky";
    nav.style.top = "0";
    nav.style.zIndex = "999";
    nav.style.display = "flex";
    nav.style.flexWrap = "wrap";
    nav.style.gap = "10px";
    nav.style.padding = "10px 14px";
    nav.style.borderBottom = "1px solid #2d3b5a";
    nav.style.background = "rgba(11,16,32,0.95)";
    nav.style.backdropFilter = "blur(6px)";

    var links = [
      { href: "/", label: "Home" },
      { href: "/CCNP_Encor.html", label: "Certifications" },
      { href: "/cert-access-help.html", label: "Access Help" },
    ];

    links.forEach(function (item) {
      var a = document.createElement("a");
      a.href = item.href;
      a.textContent = item.label;
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
      nav.appendChild(a);
    });

    document.body.insertBefore(nav, document.body.firstChild);
  });
})();

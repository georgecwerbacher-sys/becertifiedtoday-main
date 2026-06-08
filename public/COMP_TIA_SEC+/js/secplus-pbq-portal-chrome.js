(function () {
  var path = location.pathname || "";
  if (path.indexOf("/PBQ_Production/") === -1) return;
  if (/\/sections\//.test(path)) return;
  if (/\/review-index\.html$/.test(path)) return;

  var portal = "/COMP_TIA_SEC+/SEC+_Training_Portal.html";
  var logo = "/images/logo/becertifiedtoday_logo_trans.png";

  function initPbqPortalChrome() {
    document.body.classList.add("pbq-portal-chrome");

    var logos = document.querySelectorAll(".site-logo-corner");
    if (logos.length > 1) {
      var keep =
        document.querySelector(".question-shell .site-logo-corner") || logos[0];
      logos.forEach(function (el) {
        if (el !== keep) el.remove();
      });
    }

    if (!document.querySelector(".site-logo-corner")) {
      var logoLink = document.createElement("a");
      logoLink.className = "site-logo-corner site-logo-corner--pbq";
      logoLink.href = portal;
      logoLink.setAttribute("aria-label", "Security+ practice portal");
      logoLink.innerHTML =
        '<img src="' + logo + '" width="52" height="52" alt="Be Certified Today" />';
      var contentRoot =
        document.querySelector(".question-shell") ||
        document.querySelector("main.wrap") ||
        document.querySelector("main") ||
        document.querySelector(".wrap");
      if (contentRoot) {
        contentRoot.insertBefore(logoLink, contentRoot.firstChild);
      } else {
        document.body.insertBefore(logoLink, document.body.firstChild);
      }
    } else {
      var existingLogo = document.querySelector(".site-logo-corner");
      if (existingLogo.getAttribute("href") !== portal) {
        existingLogo.setAttribute("href", portal);
      }
    }

    document.querySelectorAll(".home-link, .nav-home").forEach(function (link) {
      link.setAttribute("href", portal);
    });

    var hasFooterNav =
      document.querySelector(".pbq-suite-footer .question-nav--footer") ||
      document.querySelector(".question-nav .nav-home") ||
      document.querySelector(".home-link") ||
      document.getElementById("pbqPortalFooter");

    if (!hasFooterNav) {
      var footer = document.createElement("nav");
      footer.id = "pbqPortalFooter";
      footer.className = "pbq-portal-footer";
      footer.setAttribute("aria-label", "Portal navigation");
      footer.innerHTML =
        '<a class="pbq-portal-footer__home" href="' + portal + '">SEC+ Home</a>';
      document.body.appendChild(footer);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initPbqPortalChrome);
  } else {
    initPbqPortalChrome();
  }
})();

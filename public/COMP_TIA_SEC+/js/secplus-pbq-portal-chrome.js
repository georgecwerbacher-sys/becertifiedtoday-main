(function () {
  var path = location.pathname || "";
  if (path.indexOf("/PBQ_Production/") === -1) return;
  if (/\/sections\//.test(path)) return;
  if (/\/review-index\.html$/.test(path)) return;

  function homeSampleActive() {
    try {
      return !!sessionStorage.getItem("secplusHomeSample");
    } catch (e) {
      return false;
    }
  }

  if (homeSampleActive()) return;

  var publicHome = "/comptia-sec+-home.html";
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
      logoLink.href = publicHome;
      logoLink.setAttribute("aria-label", "Return to Security+ home");
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
      if (existingLogo.getAttribute("href") !== publicHome) {
        existingLogo.setAttribute("href", publicHome);
        existingLogo.setAttribute("aria-label", "Return to Security+ home");
      }
    }

    document.querySelectorAll(".home-link, .nav-home").forEach(function (link) {
      link.setAttribute("href", publicHome);
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
        '<a class="pbq-portal-footer__home" href="' + publicHome + '">Security+ home</a>';
      document.body.appendChild(footer);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initPbqPortalChrome);
  } else {
    initPbqPortalChrome();
  }
})();

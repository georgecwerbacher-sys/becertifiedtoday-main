(function () {
  try {
    var mask = sessionStorage.getItem("ccnpUrlMaskPath");
    if (!mask && /(?:\?|&)sample=1(?:&|$)/.test(location.search || "")) {
      mask = "/sample";
      sessionStorage.setItem("ccnpUrlMaskPath", mask);
    }
    if (!mask) return;
    history.replaceState(null, "", mask);
  } catch (e) {}
})();

(function () {
  "use strict";

  function inTargetPage() {
    var path = (location.pathname || "").toLowerCase();
    return path.indexOf("/ccna-study/ccna_questions/") !== -1 || path.indexOf("/ccna-study/ccna_d_d/") !== -1;
  }

  function moveHomeLinkToBottom() {
    if (!inTargetPage()) return;

    var main = document.querySelector("main.card") || document.querySelector("main");
    if (!main) return;

    var homeLink = main.querySelector("a.home-link");
    if (!homeLink) return;

    var originalActions = homeLink.closest(".actions");
    var nextWrap = main.querySelector(".next-wrap");
    var targetWrap = main.querySelector(".home-bottom-wrap");
    if (!targetWrap) {
      targetWrap = document.createElement("div");
      targetWrap.className = "home-bottom-wrap";
      targetWrap.style.marginTop = "18px";
      targetWrap.style.display = "flex";
      targetWrap.style.justifyContent = "flex-end";
      if (nextWrap && nextWrap.parentNode === main) {
        nextWrap.insertAdjacentElement("afterend", targetWrap);
      } else {
        main.appendChild(targetWrap);
      }
    }

    targetWrap.appendChild(homeLink);

    if (originalActions && originalActions.children.length === 0) {
      originalActions.remove();
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", moveHomeLinkToBottom);
  } else {
    moveHomeLinkToBottom();
  }
})();


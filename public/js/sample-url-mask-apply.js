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

  var MAIL = "becertifiedtoday@gmail.com";

  function injectCcnaAnyQuestionsLink() {
    var path = (location.pathname || "").toLowerCase();
    if (path.indexOf("/ccna-study/") === -1) return;
    if (/\/ccna-study\/ccna-index\.html$/.test(path)) return;
    if (/\/ccna-study\/ccna_training_portal\.html$/.test(path)) return;
    if (document.getElementById("ccna-any-questions")) return;

    var wrap =
      document.querySelector("main.card") ||
      document.querySelector("main") ||
      document.querySelector(".card");
    if (!wrap) return;

    if (!document.getElementById("ccna-any-questions-style")) {
      var st = document.createElement("style");
      st.id = "ccna-any-questions-style";
      st.textContent =
        ".ccna-any-questions{margin-top:22px;padding-top:16px;border-top:1px solid #2d3b5a;text-align:center;font-size:0.88rem;color:#94a3b8;line-height:1.45}" +
        ".ccna-any-questions a{color:#8ab4ff;text-decoration:underline}" +
        ".ccna-any-questions a:hover{filter:brightness(1.1)}";
      document.head.appendChild(st);
    }

    var p = document.createElement("p");
    p.className = "ccna-any-questions";
    p.id = "ccna-any-questions";
    var a = document.createElement("a");
    var subj = encodeURIComponent("CCNA practice — question");
    var body = encodeURIComponent("Page: " + location.href + "\n\n");
    a.href = "mailto:" + MAIL + "?subject=" + subj + "&body=" + body;
    a.textContent = "Any questions?";
    a.setAttribute(
      "aria-label",
      "Any questions? Email Be Certified Today at becertifiedtoday at gmail dot com"
    );
    p.appendChild(a);

    var nextWrap = wrap.querySelector(".next-wrap");
    if (nextWrap && nextWrap.parentNode === wrap) {
      nextWrap.insertAdjacentElement("afterend", p);
    } else {
      wrap.appendChild(p);
    }
  }

  function onReady() {
    injectCcnaAnyQuestionsLink();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onReady);
  } else {
    onReady();
  }
})();

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

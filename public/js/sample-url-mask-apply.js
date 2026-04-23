(function () {
  try {
    var mask = sessionStorage.getItem("ccnpUrlMaskPath");
    if (!mask) return;
    history.replaceState(null, "", mask);
  } catch (e) {}
})();

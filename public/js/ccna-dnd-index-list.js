(function () {
  "use strict";

  var list = document.getElementById("ccna-dnd-index-list");
  if (!list) return;

  var BASE = "/CCNA-Study/CCNA_D_D/";

  function titleFromSlug(slug) {
    return slug
      .replace(/^dragdrop-/, "")
      .split("-")
      .map(function (w) {
        return w.charAt(0).toUpperCase() + w.slice(1);
      })
      .join(" ");
  }

  function render(slugs) {
    slugs.forEach(function (slug) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = BASE + slug + ".html";
      a.textContent = titleFromSlug(slug);
      li.appendChild(a);
      list.appendChild(li);
    });
    var countEl = document.getElementById("ccna-dnd-count");
    if (countEl) countEl.textContent = String(slugs.length);
  }

  function renderFromHub() {
    if (window.CCNA_DND_SLUGS && window.CCNA_DND_SLUGS.length) {
      render(window.CCNA_DND_SLUGS.slice());
      return true;
    }
    return false;
  }

  function renderFromMap() {
    fetch("/CCNA-Study/data/ccna-dnd-topic-map.json")
      .then(function (r) {
        return r.json();
      })
      .then(function (map) {
        var slugs = Object.keys(map)
          .map(function (file) {
            return file.replace(/\.html$/, "");
          })
          .sort();
        render(slugs);
      })
      .catch(function () {});
  }

  function init() {
    if (renderFromHub()) return;
    renderFromMap();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  window.addEventListener("load", function () {
    if (!list.children.length) init();
  });
})();

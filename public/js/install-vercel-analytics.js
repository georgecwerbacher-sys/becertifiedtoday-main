/**
 * Vercel Web Analytics — injects /_vercel/insights/script.js when not already present.
 * Enable Web Analytics in the Vercel project dashboard, then deploy.
 */
(function () {
  "use strict";

  var path = (location.pathname || "").toLowerCase();
  if (path.indexOf("/admin/") === 0) return;
  try {
    if (new URLSearchParams(location.search).get("examSim") === "1") return;
  } catch (_) {}

  var head = document.head || document.getElementsByTagName("head")[0];
  if (!head || head.querySelector('script[data-bcc-vercel-analytics="1"]')) return;

  var queue = document.createElement("script");
  queue.setAttribute("data-bcc-vercel-analytics", "1");
  queue.textContent =
    "window.va=window.va||function(){(window.vaq=window.vaq||[]).push(arguments);};";
  head.appendChild(queue);

  var loader = document.createElement("script");
  loader.defer = true;
  loader.src = "/_vercel/insights/script.js";
  loader.setAttribute("data-bcc-vercel-analytics", "1");
  head.appendChild(loader);
})();

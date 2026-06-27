(function () {
  "use strict";

  function esc(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function countObjectives(objectives) {
    var n = 0;
    objectives.forEach(function (obj) {
      n += 1;
      if (obj.children && obj.children.length) n += obj.children.length;
    });
    return n;
  }

  function renderObjective(obj) {
    var hasChildren = obj.children && obj.children.length;
    if (!hasChildren) {
      return (
        '<li class="ccnaauto-bp-obj">' +
        '<span class="ccnaauto-bp-id">' +
        esc(obj.id) +
        "</span> " +
        esc(obj.text) +
        "</li>"
      );
    }

    var html =
      '<li class="ccnaauto-bp-obj ccnaauto-bp-obj--parent">' +
      '<details class="ccnaauto-bp-sub-details">' +
      '<summary class="ccnaauto-bp-sub-summary">' +
      '<span class="ccnaauto-bp-chevron" aria-hidden="true"></span>' +
      '<span class="ccnaauto-bp-id">' +
      esc(obj.id) +
      "</span> " +
      '<span class="ccnaauto-bp-summary-text">' +
      esc(obj.text) +
      "</span>" +
      '<span class="ccnaauto-bp-sub-count">' +
      obj.children.length +
      " sub</span>" +
      "</summary>" +
      '<ul class="ccnaauto-bp-sub">';

    obj.children.forEach(function (child) {
      html += renderObjective(child);
    });
    html += "</ul></details></li>";
    return html;
  }

  function setAllDetails(root, open) {
    if (!root) return;
    root.querySelectorAll("details.ccnaauto-bp-domain, details.ccnaauto-bp-sub-details").forEach(function (el) {
      el.open = open;
    });
  }

  function bindToolbar(root) {
    if (!root) return;
    var expandBtn = root.querySelector("[data-bp-expand-all]");
    var collapseBtn = root.querySelector("[data-bp-collapse-all]");
    if (expandBtn) {
      expandBtn.addEventListener("click", function () {
        setAllDetails(root, true);
      });
    }
    if (collapseBtn) {
      collapseBtn.addEventListener("click", function () {
        setAllDetails(root, false);
      });
    }
  }

  function renderBlueprint(data, root) {
    if (!data || !data.domains || !root) return;

    var parts = [
      '<div class="ccnaauto-blueprint">',
      '<div class="ccnaauto-bp-toolbar" role="group" aria-label="Blueprint sections">',
      '<button type="button" class="ccnaauto-bp-tool-btn" data-bp-expand-all>Expand all</button>',
      '<button type="button" class="ccnaauto-bp-tool-btn" data-bp-collapse-all>Collapse all</button>',
      "</div>",
    ];

    data.domains.forEach(function (domain) {
      var slug = esc(domain.id.replace(".", "-"));
      var total = countObjectives(domain.objectives);
      parts.push(
        '<details class="ccnaauto-bp-domain" id="ccnaauto-domain-' + slug + '">',
        '<summary class="ccnaauto-bp-domain-summary">',
        '<span class="ccnaauto-bp-chevron ccnaauto-bp-chevron--domain" aria-hidden="true"></span>',
        '<span class="ccnaauto-bp-domain-title">' +
          esc(domain.id + " " + domain.title) +
          ' <span class="ccnaauto-bp-weight">(' +
          esc(domain.weight) +
          ")</span></span>",
        '<span class="ccnaauto-bp-domain-count">' + total + " objectives</span>",
        "</summary>",
        '<div class="ccnaauto-bp-domain-body">',
        '<ol class="ccnaauto-bp-list">'
      );
      domain.objectives.forEach(function (obj) {
        parts.push(renderObjective(obj));
      });
      parts.push("</ol></div></details>");
    });

    parts.push("</div>");
    root.innerHTML = parts.join("");
    bindToolbar(root);
  }

  function typeLabel(type) {
    if (type === "removed") return "Removed";
    if (type === "rename") return "Renamed";
    if (type === "content") return "Content";
    return "Wording";
  }

  function renderChanges(data, root) {
    if (!data || !root || !data.changes) return;

    var parts = [
      '<div class="ccnaauto-bp-changes">',
      '<details class="ccnaauto-bp-changes-panel">',
      '<summary class="ccnaauto-bp-changes-summary">',
      '<span class="ccnaauto-bp-chevron ccnaauto-bp-chevron--domain" aria-hidden="true"></span>',
      "<span><strong>v1.0 → v1.1 changes only</strong> ",
      esc(data.from_label) + " → " + esc(data.to_label),
      "</span>",
      '<span class="ccnaauto-bp-domain-count">' + data.changes.length + " diffs</span>",
      "</summary>",
      '<div class="ccnaauto-bp-changes-body">',
      "<p class=\"ccnaauto-bp-changes-intro\">" + esc(data.intro) + "</p>",
    ];

    if (data.outdated_terms && data.outdated_terms.length) {
      parts.push('<div class="ccnaauto-bp-term-block"><p class="ccnaauto-bp-term-label">Likely outdated in v1.1</p><ul class="ccnaauto-bp-term-list">');
      data.outdated_terms.forEach(function (term) {
        parts.push('<li class="ccnaauto-bp-term ccnaauto-bp-term--out">' + esc(term) + "</li>");
      });
      parts.push("</ul></div>");
    }

    if (data.added_terms && data.added_terms.length) {
      parts.push('<div class="ccnaauto-bp-term-block"><p class="ccnaauto-bp-term-label">Added / emphasized in v1.1</p><ul class="ccnaauto-bp-term-list">');
      data.added_terms.forEach(function (term) {
        parts.push('<li class="ccnaauto-bp-term ccnaauto-bp-term--new">' + esc(term) + "</li>");
      });
      parts.push("</ul></div>");
    }

    parts.push('<div class="ccnaauto-bp-changes-table-wrap"><table class="ccnaauto-bp-changes-table">');
    parts.push(
      "<thead><tr>",
      "<th scope=\"col\">ID</th>",
      "<th scope=\"col\">Type</th>",
      "<th scope=\"col\">v1.0 (DEVASC)</th>",
      "<th scope=\"col\">v1.1 (CCNAAUTO)</th>",
      "<th scope=\"col\">Hunt triage</th>",
      "</tr></thead><tbody>"
    );

    data.changes.forEach(function (row) {
      parts.push(
        "<tr>",
        '<th scope="row">' + esc(row.id) + "</th>",
        '<td><span class="ccnaauto-bp-change-type ccnaauto-bp-change-type--' + esc(row.type) + '">' + esc(typeLabel(row.type)) + "</span></td>",
        "<td>" + esc(row.v1_0) + "</td>",
        "<td>" + esc(row.v1_1) + "</td>",
        "<td>" + esc(row.hunt) + "</td>",
        "</tr>"
      );
    });

    parts.push("</tbody></table></div></div></details></div>");
    root.innerHTML = parts.join("");
  }

  window.CCNAAUTO_BLUEPRINT = {
    render: renderBlueprint,
    renderChanges: renderChanges,
    load: function (rootId, jsonUrl, changesRootId, changesUrl) {
      var root = document.getElementById(rootId);
      if (!root) return Promise.resolve();

      var changesRoot = changesRootId ? document.getElementById(changesRootId) : null;
      var blueprintPromise = fetch(jsonUrl).then(function (r) {
        if (!r.ok) throw new Error("blueprint fetch failed");
        return r.json();
      });

      var changesPromise = changesRoot && changesUrl
        ? fetch(changesUrl).then(function (r) {
            if (!r.ok) throw new Error("changes fetch failed");
            return r.json();
          })
        : Promise.resolve(null);

      return Promise.all([blueprintPromise, changesPromise])
        .then(function (pair) {
          renderBlueprint(pair[0], root);
          if (changesRoot && pair[1]) renderChanges(pair[1], changesRoot);
        })
        .catch(function () {
          root.innerHTML = '<p class="ccnaauto-bp-error">Could not load blueprint objectives.</p>';
          if (changesRoot) {
            changesRoot.innerHTML = '<p class="ccnaauto-bp-error">Could not load v1.0 → v1.1 changes.</p>';
          }
        });
    },
  };
})();

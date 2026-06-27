(function () {
  "use strict";

  var CHANGES_URL = "/COMP_TIA_SEC+/data/secplus-blueprint-sy0-601-to-701-changes.json";
  var ARCHIVE_URL = "/COMP_TIA_SEC+/data/secplus-obsolete-question-archive.json";

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function uniqueLegacyObjectives(review) {
    var set = {};
    (review || []).forEach(function (row) {
      (row.objectives || []).forEach(function (id) {
        set[String(id)] = true;
      });
    });
    return Object.keys(set).sort();
  }

  function renderRemovedDomains(data) {
    var rows = (data.domain_renames || []).filter(function (r) {
      return r.sy0_601 && r.sy0_601 !== "(none)";
    });
    if (!rows.length) return "";
    var html =
      '<table class="secplus-601-701-table">' +
      "<thead><tr><th scope=\"col\">Removed SY0-601 domain</th><th scope=\"col\">SY0-701 successor</th></tr></thead><tbody>";
    rows.forEach(function (row) {
      html +=
        "<tr><td>" +
        esc(row.sy0_601) +
        "</td><td>" +
        esc(row.sy0_701) +
        " <span class=\"secplus-601-701-tag\">" +
        esc(row.type || "") +
        "</span></td></tr>";
    });
    html += "</tbody></table>";
    return html;
  }

  function renderConsolidatedObjectives(changes) {
    var consolidated = (changes || []).filter(function (c) {
      return c.type === "consolidated" && c.sy0_601;
    });
    if (!consolidated.length) return "";
    var html =
      '<details class="secplus-601-701-details">' +
      "<summary>" +
      consolidated.length +
      " SY0-601 objectives folded into broader SY0-701 objectives (not separate exam lines anymore)</summary>" +
      '<div class="secplus-601-701-details-body">' +
      '<table class="secplus-601-701-table secplus-601-701-table--compact">' +
      "<thead><tr><th scope=\"col\">601 ID</th><th scope=\"col\">601 objective</th><th scope=\"col\">701 successor</th></tr></thead><tbody>";
    consolidated.forEach(function (row) {
      html +=
        "<tr>" +
        '<th scope="row">' +
        esc(row.id) +
        "</th>" +
        "<td>" +
        esc(row.sy0_601) +
        "</td>" +
        "<td>" +
        esc(row.sy0_701) +
        "</td>" +
        "</tr>";
    });
    html += "</tbody></table></div></details>";
    return html;
  }

  function renderTrackingBlock(archive) {
    var review = archive && Array.isArray(archive.candidateReview) ? archive.candidateReview : [];
    if (!review.length) {
      return (
        '<p class="secplus-601-701-tracking">' +
        "No legacy objective-ID mismatches pending in the tracker.</p>"
      );
    }
    var legacyIds = uniqueLegacyObjectives(review);
    var html =
      '<p class="secplus-601-701-tracking">' +
      "<strong>" +
      review.length +
      " practice item(s)</strong> still carry legacy objective IDs that are " +
      "<strong>not on the official SY0-701 PDF</strong> (for example " +
      esc(legacyIds.slice(0, 4).join(", ")) +
      (legacyIds.length > 4 ? ", …" : "") +
      "). They stay visible while we remap or retire them—do not treat these IDs as SY0-701 exam lines.</p>" +
      '<details class="secplus-601-701-details">' +
      "<summary>Legacy objective IDs under review (" +
      legacyIds.length +
      ")</summary>" +
      '<ul class="secplus-601-701-id-list">';
    legacyIds.forEach(function (id) {
      html += "<li><code>" + esc(id) + "</code></li>";
    });
    html += "</ul></details>";
    return html;
  }

  function renderPanel(data, archive, root) {
    if (!data || !root) return;
    var cmp = data.comptia_official_comparison || {};
    var blogUrl = cmp.url || "";
    var blogTitle = cmp.title || "CompTIA Security+ 601 vs. 701";

    var html =
      '<div class="secplus-601-701-panel-inner">' +
      '<p class="secplus-601-701-eyebrow">Study path alignment</p>' +
      "<h2 class=\"secplus-601-701-title\">SY0-601 → SY0-701: what left the active study path</h2>" +
      '<p class="secplus-601-701-lead">' +
      esc(data.intro || "") +
      "</p>";

    if (blogUrl) {
      html +=
        '<p class="secplus-601-701-source">' +
        "Summary cross-checked with CompTIA’s official comparison: " +
        '<a href="' +
        esc(blogUrl) +
        '" rel="noopener noreferrer">' +
        esc(blogTitle) +
        "</a>.</p>";
    }

    if (cmp.highlights && cmp.highlights.length) {
      html += '<ul class="secplus-601-701-highlights">';
      cmp.highlights.forEach(function (h) {
        html += "<li>" + esc(h) + "</li>";
      });
      html += "</ul>";
    }

    if (cmp.domain_table && cmp.domain_table.length) {
      html +=
        '<h3 class="secplus-601-701-h3">How CompTIA remapped the five domains</h3>' +
        '<table class="secplus-601-701-table">' +
        "<thead><tr><th scope=\"col\">SY0-601 (retired)</th><th scope=\"col\">SY0-701 (current)</th></tr></thead><tbody>";
      cmp.domain_table.forEach(function (row) {
        html +=
          "<tr><td>" +
          esc(row.sy0_601) +
          "</td><td>" +
          esc(row.sy0_701) +
          "</td></tr>";
      });
      html += "</tbody></table>";
    }

    html +=
      '<h3 class="secplus-601-701-h3">Not on your SY0-701 study path</h3>' +
      '<ul class="secplus-601-701-removed-list">' +
      "<li><strong>SY0-601 exam objectives</strong> — retired 2024-07-31; superseded by SY0-701.</li>" +
      "<li><strong>Standalone “Implementation” domain (25%)</strong> — absorbed into Security Operations on 701.</li>" +
      "<li><strong>35 granular 601 objectives</strong> — consolidated to 28 broader 701 objectives; old numbered lines below are not separate targets.</li>" +
      "</ul>" +
      renderRemovedDomains(data) +
      renderConsolidatedObjectives(data.changes) +
      '<h3 class="secplus-601-701-h3">What we are tracking in this bank</h3>' +
      renderTrackingBlock(archive) +
      '<p class="secplus-601-701-foot">' +
      "Practice below follows <strong>SY0-701</strong> domain weights only. The " +
      (archive && Array.isArray(archive.candidateReview) ? archive.candidateReview.length : 0) +
      " outdated item(s) are in the green <strong>SY0-601 Outdated</strong> audit bank on this portal—not promoted in Random/Review mix.</p>" +
      "</div>";

    root.innerHTML = html;
  }

  function load(rootId) {
    var root = document.getElementById(rootId);
    if (!root) return Promise.resolve();

    return Promise.all([
      fetch(CHANGES_URL, { credentials: "same-origin" }).then(function (r) {
        if (!r.ok) throw new Error("changes");
        return r.json();
      }),
      fetch(ARCHIVE_URL, { credentials: "same-origin" })
        .then(function (r) {
          if (!r.ok) return null;
          return r.json();
        })
        .catch(function () {
          return null;
        }),
    ])
      .then(function (pair) {
        renderPanel(pair[0], pair[1], root);
      })
      .catch(function () {
        root.innerHTML =
          '<p class="study-meta">Could not load SY0-601 → SY0-701 study path comparison. Refresh the page.</p>';
      });
  }

  window.SECPLUS_BLUEPRINT_CHANGES = {
    load: load,
    render: renderPanel,
  };
})();

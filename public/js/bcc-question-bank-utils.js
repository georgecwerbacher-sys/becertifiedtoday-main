(function (global) {
  "use strict";

  var DEFAULT_BANK_SIZE = 100;

  function shuffle(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i];
      a[i] = a[j];
      a[j] = t;
    }
    return a;
  }

  function formatRange(first, last) {
    if (first >= last) return String(first);
    return String(first) + "\u2013" + String(last);
  }

  /** @param {unknown} entry */
  function normalizeAssignment(entry) {
    if (Array.isArray(entry)) {
      return { objectives: entry.map(String), subObjectives: [] };
    }
    if (entry && typeof entry === "object") {
      var o = entry;
      return {
        objectives: Array.isArray(o.objectives) ? o.objectives.map(String) : [],
        subObjectives: Array.isArray(o.subObjectives) ? o.subObjectives.map(String) : [],
      };
    }
    return { objectives: [], subObjectives: [] };
  }

  function objectivesForFile(assignments, fileName) {
    if (!assignments || !fileName) return null;
    var entry = assignments[fileName];
    if (!entry) return null;
    var norm = normalizeAssignment(entry);
    var all = norm.objectives.concat(norm.subObjectives);
    return all.length ? all : null;
  }

  function slugMatchesMajor(assignments, slug, major, ext) {
    ext = ext || ".html";
    var objs = objectivesForFile(assignments, slug + ext);
    if (!objs || !objs.length) return false;
    var want = String(major);
    for (var i = 0; i < objs.length; i++) {
      var maj = String(objs[i]).split(".")[0];
      if (maj === want) return true;
    }
    return false;
  }

  function filterSlugsByMajor(slugs, assignments, major, ext) {
    if (!major) return slugs.slice();
    if (!assignments || typeof assignments !== "object") return [];
    var out = [];
    for (var i = 0; i < slugs.length; i++) {
      if (slugMatchesMajor(assignments, slugs[i], major, ext)) out.push(slugs[i]);
    }
    return out;
  }

  function bankSlugs(allSlugs, bankIndex, bankSize) {
    bankSize = bankSize || DEFAULT_BANK_SIZE;
    var n = parseInt(String(bankIndex), 10);
    if (!n || n < 1) n = 1;
    var start = (n - 1) * bankSize;
    return (allSlugs || []).slice(start, start + bankSize);
  }

  function practiceBankCount(slugCount, bankSize) {
    bankSize = bankSize || DEFAULT_BANK_SIZE;
    if (!slugCount) return 1;
    return Math.ceil(slugCount / bankSize);
  }

  function escHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  /**
   * @param {HTMLElement} root
   * @param {{ domains?: Array<{id:string,name:string,weightPercent:number,questionsPerBankTarget?:number,questionsPerBank?:number,assignedQuestionCount?:number,gapToTarget?:number}> }} tracker
   * @param {{ domains?: Array<{id:string,name:string,weightPercent:number,questionsPerBank:number}> }} blueprint
   */
  function renderDomainWeightTable(root, tracker, blueprint) {
    renderSecplusDomainWeightTable(root, tracker, blueprint, null);
  }

  function countForObjective(id, counts) {
    if (!counts || id == null) return 0;
    return counts[id] != null ? counts[id] : 0;
  }

  function renderSubObjectiveList(children, counts) {
    if (!children || !children.length) return "";
    var html = '<ul class="bcc-bank-subobjective-list">';
    children.forEach(function (child) {
      html += '<li class="bcc-bank-subobjective-item">';
      if (child.id) {
        html +=
          '<span class="bcc-bank-subobjective-id">' +
          escHtml(child.id) +
          "</span> ";
      }
      html += escHtml(child.text || "");
      if (child.id) {
        html +=
          ' <span class="bcc-bank-subobjective-count">' +
          escHtml(countForObjective(child.id, counts)) +
          " published</span>";
      }
      html += renderSubObjectiveList(child.children, counts);
      html += "</li>";
    });
    html += "</ul>";
    return html;
  }

  function renderObjectiveTreeItem(obj, counts) {
    var published = countForObjective(obj.id, counts);
    var subs = renderSubObjectiveList(obj.children, counts);
    if (!subs) {
      return (
        '<div class="bcc-bank-objective-row">' +
        '<span class="bcc-bank-objective-id">' +
        escHtml(obj.id) +
        "</span> " +
        escHtml(obj.text || "") +
        ' <span class="bcc-bank-objective-count">' +
        escHtml(published) +
        " published</span>" +
        "</div>"
      );
    }
    return (
      '<details class="bcc-bank-objective-details">' +
      "<summary>" +
      '<span class="bcc-bank-objective-id">' +
      escHtml(obj.id) +
      "</span> " +
      escHtml(obj.text || "") +
      ' <span class="bcc-bank-objective-count">' +
      escHtml(published) +
      " published</span>" +
      "</summary>" +
      subs +
      "</details>"
    );
  }

  /**
   * Security+ portal table with expandable PDF sub-subjects per domain.
   * @param {{ domains?: Array<{id:string,objectives?:Array<{id:string,text:string,children?:Array}>}> }} objectivesOutline
   */
  function renderSecplusDomainWeightTable(root, tracker, blueprint, objectivesOutline) {
    if (!root) return;
    var rows = [];
    var fromTracker = tracker && Array.isArray(tracker.domains) ? tracker.domains : null;
    var fromBlueprint = blueprint && Array.isArray(blueprint.domains) ? blueprint.domains : null;
    var domains = fromTracker || (fromBlueprint || []).map(function (d) {
      return {
        id: d.id,
        name: d.name,
        weightPercent: d.weightPercent,
        questionsPerBankTarget: d.questionsPerBank,
        assignedQuestionCount: 0,
        gapToTarget: d.questionsPerBank,
      };
    });
    if (!domains.length) {
      root.innerHTML = '<p class="study-meta">Domain weights unavailable.</p>';
      return;
    }

    var objectiveCounts =
      tracker && tracker.objectiveCounts && typeof tracker.objectiveCounts === "object"
        ? tracker.objectiveCounts
        : {};
    var outlineById = {};
    if (objectivesOutline && Array.isArray(objectivesOutline.domains)) {
      objectivesOutline.domains.forEach(function (d) {
        outlineById[d.id] = d;
      });
    }

    var html =
      '<table class="bcc-bank-weight-table' +
      (objectivesOutline ? " bcc-bank-weight-table--expandable" : "") +
      '">' +
      "<thead><tr>" +
      "<th scope=\"col\">Domain</th>" +
      "<th scope=\"col\">Exam weight</th>" +
      "<th scope=\"col\">Target / bank</th>" +
      "<th scope=\"col\">Published</th>" +
      "<th scope=\"col\">Gap</th>" +
      "</tr></thead><tbody>";

    domains.forEach(function (d) {
      var target = d.questionsPerBankTarget != null ? d.questionsPerBankTarget : d.questionsPerBank;
      var count = d.assignedQuestionCount != null ? d.assignedQuestionCount : 0;
      var gap = d.gapToTarget != null ? d.gapToTarget : target - count;
      var gapLabel = gap > 0 ? "+" + gap + " needed" : gap === 0 ? "On target" : String(gap);
      var outline = outlineById[d.id];
      var objectiveTree = "";
      if (outline && Array.isArray(outline.objectives) && outline.objectives.length) {
        objectiveTree =
          '<div class="bcc-bank-objective-tree">' +
          outline.objectives
            .map(function (obj) {
              return renderObjectiveTreeItem(obj, objectiveCounts);
            })
            .join("") +
          "</div>";
      }

      var domainCell;
      if (objectiveTree) {
        domainCell =
          '<details class="bcc-bank-domain-details">' +
          "<summary>" +
          '<span class="bcc-bank-domain-id">' +
          escHtml(d.id) +
          "</span> " +
          escHtml(d.name) +
          "</summary>" +
          objectiveTree +
          "</details>";
      } else {
        domainCell =
          '<span class="bcc-bank-domain-id">' + escHtml(d.id) + "</span> " + escHtml(d.name);
      }

      html +=
        "<tr>" +
        "<td>" +
        domainCell +
        "</td>" +
        "<td>" +
        escHtml(d.weightPercent) +
        "%</td>" +
        "<td>" +
        escHtml(target) +
        "</td>" +
        "<td>" +
        escHtml(count) +
        "</td>" +
        "<td>" +
        escHtml(gapLabel) +
        "</td>" +
        "</tr>";
    });
    html += "</tbody></table>";
    root.innerHTML = html;
  }

  global.BCC_QUESTION_BANK = global.BCC_QUESTION_BANK || {};
  global.BCC_QUESTION_BANK.DEFAULT_BANK_SIZE = DEFAULT_BANK_SIZE;
  global.BCC_QUESTION_BANK.shuffle = shuffle;
  global.BCC_QUESTION_BANK.formatRange = formatRange;
  global.BCC_QUESTION_BANK.normalizeAssignment = normalizeAssignment;
  global.BCC_QUESTION_BANK.objectivesForFile = objectivesForFile;
  global.BCC_QUESTION_BANK.slugMatchesMajor = slugMatchesMajor;
  global.BCC_QUESTION_BANK.filterSlugsByMajor = filterSlugsByMajor;
  global.BCC_QUESTION_BANK.bankSlugs = bankSlugs;
  global.BCC_QUESTION_BANK.practiceBankCount = practiceBankCount;
  global.BCC_QUESTION_BANK.renderDomainWeightTable = renderDomainWeightTable;
  global.BCC_QUESTION_BANK.renderSecplusDomainWeightTable = renderSecplusDomainWeightTable;
})(typeof window !== "undefined" ? window : globalThis);

(function (global) {
  "use strict";

  /**
   * Order-independent validation for category-grouped CCNA drag-and-drop pages.
   * Tokens may sit in any slot under their category; only membership counts.
   */
  function check(opts) {
    if (!opts || !opts.correctGroup) return false;
    var bank = opts.bank;
    var allSlots = opts.allSlots;
    var correctGroup = opts.correctGroup;
    var resultEl = opts.result;
    var messages = opts.messages || {};
    var mustBank = opts.mustBank || [];
    var rejectInSlots = opts.rejectInSlots || mustBank.slice();
    var tokenInBank = opts.tokenInBank;
    var requireEmptyBank = opts.requireEmptyBank;
    if (requireEmptyBank === undefined) {
      requireEmptyBank = !mustBank.length && !rejectInSlots.length;
    }
    var allOk = true;

    allSlots().forEach(function (slot) {
      slot.classList.remove("correct", "incorrect", "over");
      var t = slot.querySelector(".token");
      if (!t) {
        slot.classList.add("incorrect");
        allOk = false;
        return;
      }
      var v = t.getAttribute("data-value");
      if (rejectInSlots.indexOf(v) >= 0) {
        slot.classList.add("incorrect");
        allOk = false;
        return;
      }
      var ok = correctGroup[v] === slot.getAttribute("data-target");
      slot.classList.add(ok ? "correct" : "incorrect");
      if (!ok) allOk = false;
    });

    if (requireEmptyBank && bank && bank.querySelectorAll(".token").length) {
      allOk = false;
    }

    mustBank.forEach(function (id) {
      if (typeof tokenInBank === "function" && !tokenInBank(id)) {
        allOk = false;
      }
    });

    if (resultEl) {
      resultEl.textContent = allOk
        ? messages.ok || "Correct."
        : messages.fail || "Incorrect.";
    }

    return allOk;
  }

  /** Fill answer slots by category; order within each category is arbitrary. */
  function show(opts) {
    if (!opts || !opts.correctGroup || typeof opts.takeFromBank !== "function") return;
    var bank = opts.bank;
    var allSlots = opts.allSlots;
    var correctGroup = opts.correctGroup;
    var resultEl = opts.result;
    var byCategory = {};
    var cat;

    allSlots().forEach(function (slot) {
      slot.classList.remove("correct", "incorrect", "over");
      var t = slot.querySelector(".token");
      if (t && bank) bank.appendChild(t);
    });

    Object.keys(correctGroup).forEach(function (tokenId) {
      cat = correctGroup[tokenId];
      if (!byCategory[cat]) byCategory[cat] = [];
      byCategory[cat].push(tokenId);
    });

    Object.keys(byCategory).forEach(function (categoryId) {
      var slots = [].slice
        .call(allSlots())
        .filter(function (slot) {
          return slot.getAttribute("data-target") === categoryId;
        });
      byCategory[categoryId].forEach(function (tokenId, i) {
        var tok = opts.takeFromBank(tokenId);
        if (tok && slots[i]) {
          slots[i].appendChild(tok);
          slots[i].classList.add("correct");
        }
      });
    });

    if (resultEl) {
      resultEl.textContent = opts.showMessage || "Answer shown.";
    }
  }

  /** Parse CORRECT_GROUP from inline page scripts (exam-sim fallback). */
  function parseCorrectGroup(doc) {
    if (!doc) return null;
    var scripts = doc.querySelectorAll("script");
    var i;
    for (i = 0; i < scripts.length; i++) {
      var text = scripts[i].textContent || "";
      var m = /var\s+CORRECT_GROUP\s*=\s*(\{[\s\S]*?\});/m.exec(text);
      if (!m) continue;
      try {
        return new Function("return " + m[1])();
      } catch (e) {}
    }
    return null;
  }

  /** Score category-grouped layout without clicking Check (order-independent). */
  function scoreDocument(doc) {
    if (!doc) return false;
    var correctGroup = parseCorrectGroup(doc);
    if (!correctGroup) return null;
    var slots = doc.querySelectorAll(".drop-slot[data-target]");
    if (!slots.length) return false;
    var j;
    for (j = 0; j < slots.length; j++) {
      var slot = slots[j];
      var tok = slot.querySelector(".token");
      if (!tok) return false;
      var v = (tok.getAttribute("data-value") || "").trim();
      if (correctGroup[v] !== slot.getAttribute("data-target")) return false;
    }
    var bank = doc.getElementById("bank");
    var expectedCount = Object.keys(correctGroup).length;
    if (bank && expectedCount === slots.length && bank.querySelectorAll(".token").length) {
      return false;
    }
    return true;
  }

  global.CcnaDndCategoryCheck = {
    check: check,
    show: show,
    parseCorrectGroup: parseCorrectGroup,
    scoreDocument: scoreDocument,
  };
})(typeof window !== "undefined" ? window : this);

/**
 * Practice UI: toolbar (Home, Show answer, Next), navigation from:
 * - Random queue (ccnpQuestionQueue), or
 * - Linear study scope (ccnpLinearScope), or
 * - Global question order (study-config.json allIds), or
 * - Review quiz (ccnpReviewQueue): missed questions move to end until cleared or Home.
 */
(function () {
  var QUEUE_KEY = "ccnpQuestionQueue";
  var LINEAR_SCOPE_KEY = "ccnpLinearScope";
  var REVIEW_MODE_KEY = "ccnpReviewMode";
  var REVIEW_QUEUE_KEY = "ccnpReviewQueue";

  function isReviewMode() {
    try {
      return sessionStorage.getItem(REVIEW_MODE_KEY) === "1";
    } catch (e) {
      return false;
    }
  }

  function parseReviewQueue() {
    var raw;
    try {
      raw = sessionStorage.getItem(REVIEW_QUEUE_KEY);
    } catch (e) {
      return null;
    }
    if (!raw) return null;
    try {
      var q = JSON.parse(raw);
      return Array.isArray(q) && q.length ? q : null;
    } catch (e2) {
      return null;
    }
  }

  function clearReviewState() {
    try {
      sessionStorage.removeItem(REVIEW_MODE_KEY);
      sessionStorage.removeItem(REVIEW_QUEUE_KEY);
    } catch (e) {}
  }

  function elementVisible(el) {
    if (!el) return false;
    var s = window.getComputedStyle(el);
    return s.display !== "none" && s.visibility !== "hidden" && s.opacity !== "0";
  }

  /**
   * @returns {"correct"|"wrong"|"unknown"}
   */
  function detectAnswerOutcome() {
    var box = document.getElementById("answerBox");
    if (box && elementVisible(box)) {
      var cn = box.className || "";
      if (/\bcorrect\b/.test(cn)) return "correct";
      if (/\bincorrect\b/.test(cn)) return "wrong";
    }
    var card = document.querySelector("main.card");
    if (card) {
      var ans = card.querySelector(".answer.correct, .answer.incorrect");
      if (ans && elementVisible(ans)) {
        if (ans.classList.contains("correct")) return "correct";
        if (ans.classList.contains("incorrect")) return "wrong";
      }
    }
    var result = document.getElementById("result") || document.getElementById("status");
    if (result) {
      var t = (result.textContent || "").trim();
      var m = t.match(/Score:\s*(\d+)\s*\/\s*(\d+)/i);
      if (m) {
        var x = parseInt(m[1], 10);
        var y = parseInt(m[2], 10);
        if (y > 0 && x === y) return "correct";
        if (y > 0 && x < y) return "wrong";
      }
    }
    return "unknown";
  }

  function questionIdFromPath() {
    var p = location.pathname || "";
    var m = p.match(/question-(\d+)\.html/i);
    return m ? parseInt(m[1], 10) : null;
  }

  function injectStyles() {
    if (document.getElementById("ccnp-practice-questions-style")) return;
    var el = document.createElement("style");
    el.id = "ccnp-practice-questions-style";
    el.textContent =
      "body.ccnp-practice-ui a.home-key{display:none!important;}" +
      "body.ccnp-practice-ui .sim-nav .sim-nav-home{display:none!important;}" +
      "body.ccnp-practice-ui main.card .ccnp-q-toolbar{position:sticky;top:0;z-index:200;display:flex!important;flex-wrap:wrap;gap:10px;align-items:center;margin:0 0 16px;padding:10px 0 14px;border-bottom:1px solid #2d3b5a;background:rgba(18,26,43,.96);backdrop-filter:blur(8px);}" +
      ".ccnp-q-toolbar a,.ccnp-q-toolbar button{text-decoration:none;background:#254b8a;border:1px solid #3d6dbb;color:#e6edf3;border-radius:10px;padding:8px 14px;font-weight:700;font-size:.95rem;cursor:pointer;font-family:inherit;display:inline-block!important;box-sizing:border-box;visibility:visible!important;opacity:1!important;}" +
      ".ccnp-q-toolbar a:hover,.ccnp-q-toolbar button:hover{filter:brightness(1.08);}" +
      ".ccnp-q-toolbar button[aria-pressed=true]{background:#1a3d6e;}" +
      "#ccnpSolutionReveal{display:none;margin-top:12px;margin-bottom:8px;padding:14px;border-radius:10px;font-weight:700;background:#113e2d;border:1px solid #1f7a58;color:#e6edf3;line-height:1.45;}" +
      "#ccnpSolutionReveal.is-visible{display:block;}" +
      "body.ccnp-practice-ui main.card label.choice{cursor:pointer;-webkit-tap-highlight-color:rgba(77,137,255,.22);touch-action:manipulation;user-select:none;-webkit-user-select:none;}" +
      "body.ccnp-practice-ui main.card label.choice input[type=checkbox],body.ccnp-practice-ui main.card label.choice input[type=radio]{width:1.2em;height:1.2em;min-width:1.2em;min-height:1.2em;margin-right:12px;vertical-align:middle;}";
    document.head.appendChild(el);
  }

  /**
   * Pointer-only / locked-down UIs: activate choice from any click on the row
   * (not only the tiny control). Checkboxes toggle independently for multi-answer.
   */
  function bindPointerFriendlyChoices(card) {
    if (!card || card.dataset.ccnpChoicePointer === "1") return;
    card.dataset.ccnpChoicePointer = "1";

    card.addEventListener(
      "click",
      function (e) {
        var choice = e.target.closest(".choice");
        if (!choice || !card.contains(choice)) return;
        var input = choice.querySelector(
          'input[type="checkbox"], input[type="radio"]'
        );
        if (!input) return;
        if (e.target === input) return;

        if (e.cancelable) e.preventDefault();

        if (input.type === "checkbox") {
          input.checked = !input.checked;
        } else {
          var nm = input.name;
          card.querySelectorAll('input[type="radio"]').forEach(function (r) {
            if (r.name === nm) r.checked = false;
          });
          input.checked = true;
        }

        try {
          input.dispatchEvent(
            new InputEvent("input", { bubbles: true, cancelable: true })
          );
        } catch (err1) {
          input.dispatchEvent(new Event("input", { bubbles: true }));
        }
        input.dispatchEvent(new Event("change", { bubbles: true }));
      },
      true
    );
  }

  function parseQueue() {
    var raw = sessionStorage.getItem(QUEUE_KEY);
    if (!raw) return null;
    try {
      var q = JSON.parse(raw);
      return Array.isArray(q) && q.length ? q : null;
    } catch (e) {
      return null;
    }
  }

  function parseLinearScope() {
    var raw = sessionStorage.getItem(LINEAR_SCOPE_KEY);
    if (!raw) return null;
    try {
      var o = JSON.parse(raw);
      if (o && Array.isArray(o.ids) && o.ids.length) return o.ids;
    } catch (e) {}
    return null;
  }

  function loadStudyConfig(cb) {
    if (window.__ccnpStudyConfig) {
      cb(null, window.__ccnpStudyConfig);
      return;
    }
    fetch("/js/study-config.json", { cache: "no-store" })
      .then(function (res) {
        if (!res.ok) throw new Error("bad");
        return res.json();
      })
      .then(function (data) {
        window.__ccnpStudyConfig = data;
        cb(null, data);
      })
      .catch(function () {
        cb(new Error("fetch"), null);
      });
  }

  function stripBottomNextFromCard(card) {
    if (!card || card.dataset.ccnpBottomNextStripped === "1") return;
    card.dataset.ccnpBottomNextStripped = "1";

    var first = card.querySelector("a.next-link");
    if (first) {
      var href = first.getAttribute("href");
      if (href) card.dataset.ccnpIntrinsicNextHref = href;
      var lab = (first.textContent || "").trim();
      if (lab) card.dataset.ccnpIntrinsicNextLabel = lab;
    }

    card.querySelectorAll("#nextWrap, .next-wrap").forEach(function (el) {
      el.remove();
    });
    card.querySelectorAll("a.next-link").forEach(function (a) {
      a.remove();
    });
  }

  function stripDuplicateSimNavNext() {
    document.querySelectorAll("nav.sim-nav a.sim-nav-btn").forEach(function (a) {
      if (a.classList.contains("sim-nav-home")) return;
      var href = (a.getAttribute("href") || "").trim();
      if (href === "/practice-launcher.html") a.remove();
    });
  }

  function readIntrinsicNextFromPage() {
    var card = document.querySelector("main.card");
    if (card && card.dataset.ccnpIntrinsicNextHref) {
      return {
        href: card.dataset.ccnpIntrinsicNextHref,
        label: (card.dataset.ccnpIntrinsicNextLabel || "Next").replace(
          /\s+/g,
          " "
        ),
      };
    }
    var a = document.querySelector(
      "#nextWrap a.next-link, .next-wrap a.next-link"
    );
    if (!a) return null;
    var href = a.getAttribute("href");
    if (!href) return null;
    return {
      href: href,
      label: ((a.textContent || "").trim() || "Next").replace(/\s+/g, " "),
    };
  }

  function resolveNext(qid, cfg) {
    if (isReviewMode()) {
      var rq = parseReviewQueue();
      if (rq && rq.length) {
        if (rq[0] !== qid) {
          return { href: "/question-" + rq[0] + ".html", label: "Next" };
        }
        if (rq.length >= 2) {
          return { href: "/question-" + rq[1] + ".html", label: "Next" };
        }
        return {
          href: "/question-" + qid + ".html",
          label: "Next",
        };
      }
    }

    var queue = parseQueue();
    if (queue) {
      var idx = queue.indexOf(qid);
      if (idx >= 0) {
        var nid = queue[idx + 1];
        if (nid != null) {
          return { href: "/question-" + nid + ".html", label: "Next" };
        }
        return {
          href: "/practice-launcher.html",
          label: "Back to launcher",
        };
      }
    }

    var linearIds = parseLinearScope();
    if (linearIds) {
      var li = linearIds.indexOf(qid);
      if (li >= 0) {
        var lid = linearIds[li + 1];
        if (lid != null) {
          return { href: "/question-" + lid + ".html", label: "Next" };
        }
        return {
          href: "/practice-launcher.html",
          label: "Back to launcher",
        };
      }
    }

    var all = cfg && Array.isArray(cfg.allIds) && cfg.allIds.length ? cfg.allIds : [];
    var gi = all.indexOf(qid);
    if (gi >= 0 && gi < all.length - 1) {
      return {
        href: "/question-" + all[gi + 1] + ".html",
        label: "Next",
      };
    }
    return {
      href: "/practice-launcher.html",
      label: "Back to launcher",
    };
  }

  function syncToolbarNext(href, label) {
    var tb = document.getElementById("ccnpToolbarNext");
    if (tb) {
      tb.setAttribute("href", href);
      tb.textContent = label;
    }
  }

  function loadAnswers(cb) {
    if (window.__ccnpAnswers) {
      cb(null, window.__ccnpAnswers);
      return;
    }
    fetch("/js/question-answers.json", { cache: "no-store" })
      .then(function (res) {
        if (!res.ok) throw new Error("bad status");
        return res.json();
      })
      .then(function (data) {
        window.__ccnpAnswers = data;
        cb(null, data);
      })
      .catch(function () {
        cb(new Error("fetch"));
      });
  }

  function init() {
    var qid = questionIdFromPath();
    if (qid == null) return;

    if (isReviewMode()) {
      var rq0 = parseReviewQueue();
      if (!rq0 || !rq0.length) {
        clearReviewState();
      } else if (rq0[0] !== qid) {
        location.replace("/question-" + rq0[0] + ".html");
        return;
      }
    }

    injectStyles();
    document.body.classList.add("ccnp-practice-ui");

    var card = document.querySelector("main.card");
    if (!card || document.getElementById("ccnpQToolbar")) return;

    bindPointerFriendlyChoices(card);
    stripBottomNextFromCard(card);
    stripDuplicateSimNavNext();

    var toolbar = document.createElement("div");
    toolbar.id = "ccnpQToolbar";
    toolbar.className = "ccnp-q-toolbar";
    toolbar.setAttribute("role", "toolbar");

    var home = document.createElement("a");
    home.href = "/practice-launcher.html";
    home.textContent = "Home";

    var btn = document.createElement("button");
    btn.type = "button";
    btn.id = "ccnpShowAnswerBtn";
    btn.textContent = "Show answer";
    btn.setAttribute("aria-pressed", "false");

    var nextA = document.createElement("a");
    nextA.id = "ccnpToolbarNext";
    nextA.href = "/practice-launcher.html";
    nextA.textContent = "Next";

    var reveal = document.createElement("div");
    reveal.id = "ccnpSolutionReveal";
    reveal.setAttribute("role", "region");
    reveal.setAttribute("aria-label", "Revealed answer");

    toolbar.appendChild(home);
    toolbar.appendChild(btn);
    toolbar.appendChild(nextA);
    card.insertBefore(toolbar, card.firstChild);
    card.insertBefore(reveal, toolbar.nextSibling);

    btn.addEventListener("click", function () {
      var visible = reveal.classList.toggle("is-visible");
      btn.setAttribute("aria-pressed", visible ? "true" : "false");
      btn.textContent = visible ? "Hide answer" : "Show answer";
      if (!visible || reveal.dataset.filled) return;
      loadAnswers(function (err, answers) {
        if (err) {
          reveal.textContent = "Could not load answer data.";
        } else {
          reveal.textContent = answers[String(qid)] || "Answer not available.";
        }
        reveal.dataset.filled = "1";
      });
    });

    home.addEventListener("click", function () {
      if (isReviewMode()) clearReviewState();
    });

    nextA.addEventListener("click", function (e) {
      if (!isReviewMode()) return;
      var rq = parseReviewQueue();
      if (!rq || !rq.length) return;
      e.preventDefault();
      var cur = rq[0];
      if (cur !== qid) {
        location.href = "/question-" + rq[0] + ".html";
        return;
      }
      var out = detectAnswerOutcome();
      if (out === "wrong") {
        rq.shift();
        rq.push(cur);
      } else {
        rq.shift();
      }
      try {
        sessionStorage.setItem(REVIEW_QUEUE_KEY, JSON.stringify(rq));
      } catch (errNav) {}
      if (!rq.length) {
        clearReviewState();
        location.href = "/practice-launcher.html?review=complete";
        return;
      }
      location.href = "/question-" + rq[0] + ".html";
    });

    loadStudyConfig(function (err, cfg) {
      var c =
        !err && cfg && Array.isArray(cfg.allIds) && cfg.allIds.length
          ? cfg
          : { allIds: [] };
      var r = resolveNext(qid, c);
      if (
        !isReviewMode() &&
        !parseQueue() &&
        !parseLinearScope() &&
        (!c.allIds.length || c.allIds.indexOf(qid) < 0)
      ) {
        var intr = readIntrinsicNextFromPage();
        if (intr) {
          r = { href: intr.href, label: intr.label };
        }
      }
      nextA.setAttribute("href", r.href);
      nextA.textContent = r.label;
      syncToolbarNext(r.href, r.label);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

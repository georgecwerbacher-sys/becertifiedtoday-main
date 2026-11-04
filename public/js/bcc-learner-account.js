/**
 * Shared learner account client: auth helpers, attempt reporting, profile widgets.
 */
(function (global) {
  "use strict";

  var TRACK_LABELS = {
    ccna: "CCNA",
    encor: "ENCOR",
    secplus: "Security+",
    ccnaauto: "CCNAAUTO",
  };

  var PAID_KEYS = {
    ccna: ["bcc_ccna_portal_30d_v1", "bcc_ccna_portal_30d_cs_v1"],
    encor: ["bcc_encor_portal_v1", "bcc_encor_portal_cs_v1"],
    secplus: ["bcc_secplus_portal_v1", "bcc_secplus_portal_cs_v1"],
    ccnaauto: ["bcc_ccnaauto_portal_v1", "bcc_ccnaauto_portal_cs_v1"],
  };

  function readJson(key) {
    try {
      var raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : null;
    } catch (e) {
      return null;
    }
  }

  function looksPaid(track) {
    var keys = PAID_KEYS[track] || [];
    for (var i = 0; i < keys.length; i++) {
      var k = keys[i];
      if (k.indexOf("_cs_") >= 0) {
        try {
          if (localStorage.getItem(k)) return true;
        } catch (e) {}
        continue;
      }
      var o = readJson(k);
      if (o && typeof o.expiresAt === "number" && o.expiresAt > Date.now()) return true;
    }
    return false;
  }

  function paidTracksQuery() {
    var paid = [];
    Object.keys(PAID_KEYS).forEach(function (t) {
      if (looksPaid(t)) paid.push(t);
    });
    return paid.join(",");
  }

  function api(path, opts) {
    opts = opts || {};
    return fetch(path, {
      method: opts.method || "GET",
      credentials: "same-origin",
      headers: Object.assign(
        { Accept: "application/json" },
        opts.body ? { "Content-Type": "application/json" } : {}
      ),
      body: opts.body ? JSON.stringify(opts.body) : undefined,
      cache: "no-store",
    }).then(function (r) {
      return r.text().then(function (t) {
        var d = {};
        try {
          d = t ? JSON.parse(t) : {};
        } catch (e) {}
        return { ok: r.ok, status: r.status, data: d };
      });
    });
  }

  function fetchMe() {
    var q = paidTracksQuery();
    var url = "/api/account-me" + (q ? "?paid=" + encodeURIComponent(q) : "");
    return api(url).then(function (res) {
      if (res.ok && res.data && res.data.ok) {
        global.__bccLearnerMe = res.data;
        return res.data;
      }
      global.__bccLearnerMe = null;
      return null;
    });
  }

  function requestLogin(email) {
    return api("/api/account-request-login", {
      method: "POST",
      body: { email: email },
    });
  }

  function redeemLogin(token) {
    return api("/api/account-redeem-login", {
      method: "POST",
      body: { token: token },
    });
  }

  function logout() {
    return api("/api/account-logout", { method: "POST" }).then(function () {
      global.__bccLearnerMe = null;
    });
  }

  /**
   * Fire-and-forget attempt recording when signed in.
   * @param {Array|object} attempts
   */
  function recordAttempts(attempts) {
    var list = Array.isArray(attempts) ? attempts : [attempts];
    list = list.filter(Boolean);
    if (!list.length) return Promise.resolve({ skipped: true });
    return api("/api/account-record-attempt", {
      method: "POST",
      body: { attempts: list },
    }).catch(function () {
      return { ok: false };
    });
  }

  function recordCurrentAnswer(opts) {
    opts = opts || {};
    var box = document.getElementById("answerBox");
    if (!box) return;
    if (!box.classList.contains("correct") && !box.classList.contains("incorrect")) return;
    if (box.dataset.bccLearnerRecorded === "1") return;
    box.dataset.bccLearnerRecorded = "1";
    recordAttempts({
      track: opts.track || detectTrack(),
      mode: opts.mode || "bank",
      item_id: opts.itemId || detectItemId(),
      domain: opts.domain || detectDomain(),
      correct: box.classList.contains("correct"),
    });
  }

  function detectTrack() {
    var p = (location.pathname || "").toLowerCase();
    if (p.indexOf("/ccnp-encor-study/") >= 0) return "encor";
    if (p.indexOf("/comp_tia_sec+/") >= 0) return "secplus";
    if (p.indexOf("/ccnaauto-study/") >= 0) return "ccnaauto";
    if (p.indexOf("/ccna-study/") >= 0) return "ccna";
    return "ccna";
  }

  function detectItemId() {
    var p = location.pathname || "";
    var m = p.match(/question-(\d+)(?:\.html)?\/?$/i);
    if (m) return m[1];
    m = p.match(/\/([^/]+?)(?:\.html)?\/?$/i);
    return m ? decodeURIComponent(m[1]) : p;
  }

  function detectDomain() {
    var el = document.querySelector(".question-topic-meta__subject");
    if (el) {
      var t = (el.textContent || "").trim();
      var m = t.match(/(\d+(?:\.\d+)?)/);
      if (m) return m[1];
    }
    var obj = document.getElementById("ccnpObjectiveSection");
    if (obj) {
      var m2 = (obj.textContent || "").match(/(\d+\.\d+)/);
      if (m2) return m2[1];
    }
    return null;
  }

  function observeAnswerRecording(opts) {
    var box = document.getElementById("answerBox");
    if (!box || box.dataset.bccLearnerObs === "1") return;
    box.dataset.bccLearnerObs = "1";
    var mo = new MutationObserver(function () {
      recordCurrentAnswer(opts);
    });
    mo.observe(box, { attributes: true, attributeFilter: ["class"] });
    recordCurrentAnswer(opts);
  }

  function startGeneratedSession(exam) {
    if (!exam || !exam.items || !exam.items.length) return;
    var track = exam.track;
    var ids = exam.items.map(function (it) {
      return it.id;
    });
    try {
      if (track === "encor") {
        var numeric = ids
          .map(function (x) {
            return parseInt(x, 10);
          })
          .filter(function (n) {
            return Number.isFinite(n);
          });
        if (numeric.length) {
          sessionStorage.removeItem("ccnpReviewMode");
          sessionStorage.removeItem("ccnpReviewQueue");
          sessionStorage.setItem("ccnpQuestionQueue", JSON.stringify(numeric));
          sessionStorage.setItem("ccnpQuestionQueueIndex", "0");
          location.href = exam.items[0].url;
          return;
        }
      }
      if (track === "ccna") {
        sessionStorage.setItem(
          "ccnaPractice100",
          JSON.stringify({ v: 1, mode: "generated", order: ids, missed: [], leaveRetry: false })
        );
        location.href = exam.items[0].url + "#ccnaP=0";
        return;
      }
      if (track === "secplus") {
        sessionStorage.setItem(
          "secplusPractice",
          JSON.stringify({ v: 1, mode: "generated", order: ids, missed: [] })
        );
        location.href = exam.items[0].url + "#secplusP=0";
        return;
      }
      if (track === "ccnaauto") {
        sessionStorage.setItem(
          "ccnaautoPractice",
          JSON.stringify({ v: 1, mode: "generated", order: ids, missed: [] })
        );
        location.href = exam.items[0].url + "#ccnaautoP=0";
        return;
      }
    } catch (e) {}
    location.href = exam.items[0].url;
  }

  function generateExam(track, limit) {
    return api("/api/account-generate-exam", {
      method: "POST",
      body: {
        track: track,
        paid: looksPaid(track),
        limit: limit || 10,
      },
    });
  }

  function saveSchedule(track, examDate, notes) {
    return api("/api/account-schedule", {
      method: "POST",
      body: { track: track, exam_date: examDate, notes: notes || "" },
    });
  }

  function daysUntil(dateStr) {
    if (!dateStr) return null;
    var t = Date.parse(dateStr + "T00:00:00");
    if (!Number.isFinite(t)) return null;
    var now = new Date();
    var today = Date.parse(
      now.getFullYear() +
        "-" +
        String(now.getMonth() + 1).padStart(2, "0") +
        "-" +
        String(now.getDate()).padStart(2, "0") +
        "T00:00:00"
    );
    return Math.round((t - today) / 86400000);
  }

  function wireHeaderAccountLink() {
    document.querySelectorAll("[data-bcc-account-link]").forEach(function (el) {
      el.setAttribute("href", "/account/");
    });
    fetchMe().then(function (me) {
      document.querySelectorAll("[data-bcc-account-label]").forEach(function (el) {
        el.textContent = me && me.learner ? "Account" : "Sign in";
      });
    });
  }

  function bootQuestionPages() {
    var p = (location.pathname || "").toLowerCase();
    var isQ =
      p.indexOf("/ccna_questions/") >= 0 ||
      p.indexOf("/encor_questions/") >= 0 ||
      p.indexOf("/sec+_questions/") >= 0 ||
      p.indexOf("/ccnaauto_questions/") >= 0 ||
      p.indexOf("/ccna_samples/") >= 0 ||
      p.indexOf("/encor_samples/") >= 0 ||
      p.indexOf("/sec+_samples/") >= 0;
    if (!isQ) return;
    fetchMe().then(function (me) {
      if (!me) return;
      observeAnswerRecording({
        track: detectTrack(),
        mode: p.indexOf("_samples/") >= 0 ? "sample" : "bank",
      });
    });
  }

  global.BCC_LEARNER = {
    TRACK_LABELS: TRACK_LABELS,
    looksPaid: looksPaid,
    paidTracksQuery: paidTracksQuery,
    api: api,
    fetchMe: fetchMe,
    requestLogin: requestLogin,
    redeemLogin: redeemLogin,
    logout: logout,
    recordAttempts: recordAttempts,
    observeAnswerRecording: observeAnswerRecording,
    generateExam: generateExam,
    startGeneratedSession: startGeneratedSession,
    saveSchedule: saveSchedule,
    daysUntil: daysUntil,
    wireHeaderAccountLink: wireHeaderAccountLink,
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      wireHeaderAccountLink();
      bootQuestionPages();
    });
  } else {
    wireHeaderAccountLink();
    bootQuestionPages();
  }
})(typeof window !== "undefined" ? window : globalThis);

;(function () {
  "use strict";

  var EXAM_MINUTES = 25;

  var QUESTIONS = [
    // Domain 1.0 - General Security Concepts
    {
      id: "Q1",
      domainId: "1.0",
      domainLabel: "1.0 · General Security Concepts",
      type: "single",
      stem:
        "A security engineer wants to reduce the impact of a single web server failure. Which control best supports availability for a public-facing site?",
      choices: [
        { id: "A", text: "Enforce complex passwords on the web server", correct: false },
        { id: "B", text: "Place the server behind a stateful packet-filtering firewall", correct: false },
        { id: "C", text: "Deploy a load balancer with multiple web server instances", correct: true },
        { id: "D", text: "Enable full-disk encryption on the web server", correct: false },
      ],
    },
    {
      id: "Q2",
      domainId: "1.0",
      domainLabel: "1.0 · General Security Concepts",
      type: "single",
      stem:
        "Which term best describes the security goal of ensuring that log entries cannot be altered without detection?",
      choices: [
        { id: "A", text: "Confidentiality", correct: false },
        { id: "B", text: "Integrity", correct: true },
        { id: "C", text: "Availability", correct: false },
        { id: "D", text: "Non-repudiation", correct: false },
      ],
    },
    {
      id: "Q3",
      domainId: "1.0",
      domainLabel: "1.0 · General Security Concepts",
      type: "single",
      stem:
        "A company uses a cloud-based password manager that unlocks with a single master password. From a Security+ perspective, which risk is most important to explain to users?",
      choices: [
        {
          id: "A",
          text: "Losing internet connectivity will cause the password manager to run slowly",
          correct: false,
        },
        {
          id: "B",
          text: "Compromise of the master password exposes all stored account credentials",
          correct: true,
        },
        {
          id: "C",
          text: "The password manager prevents users from changing any existing account passwords",
          correct: false,
        },
        {
          id: "D",
          text: "Using a password manager requires users to disable multi-factor authentication",
          correct: false,
        },
      ],
    },
    {
      id: "Q4",
      domainId: "1.0",
      domainLabel: "1.0 · General Security Concepts",
      type: "multi",
      stem:
        "An architect is designing defense in depth for a new internal HR application. Which TWO controls together best illustrate this concept?",
      choices: [
        { id: "A", text: "Network segmentation plus host-based firewalls", correct: true },
        { id: "B", text: "Weekly vulnerability scanning only", correct: false },
        { id: "C", text: "A single perimeter firewall rule for all traffic", correct: false },
        { id: "D", text: "Strong authentication plus role-based access control", correct: true },
      ],
    },

    // Domain 2.0 - Threats, Vulnerabilities, and Mitigations
    {
      id: "Q5",
      domainId: "2.0",
      domainLabel: "2.0 · Threats, Vulnerabilities, and Mitigations",
      type: "single",
      stem:
        "Users report receiving emails that appear to come from the internal help desk asking them to reset their password on an external site. Which attack type does this BEST describe?",
      choices: [
        { id: "A", text: "Whaling", correct: false },
        { id: "B", text: "Spear phishing", correct: true },
        { id: "C", text: "Tailgating", correct: false },
        { id: "D", text: "War driving", correct: false },
      ],
    },
    {
      id: "Q6",
      domainId: "2.0",
      domainLabel: "2.0 · Threats, Vulnerabilities, and Mitigations",
      type: "single",
      stem:
        "A security analyst sees repeated authentication attempts from a single IP address against many different usernames. Which control would MOST directly reduce the impact of this activity?",
      choices: [
        { id: "A", text: "DNS sinkholing", correct: false },
        { id: "B", text: "Account lockout thresholds", correct: true },
        { id: "C", text: "Full disk encryption", correct: false },
        { id: "D", text: "Time-based one-time passwords (TOTP)", correct: false },
      ],
    },
    {
      id: "Q7",
      domainId: "2.0",
      domainLabel: "2.0 · Threats, Vulnerabilities, and Mitigations",
      type: "multi",
      stem:
        "A developer downloads an open-source library that later turns out to contain a backdoor. Which TWO practices best reduce this type of supply-chain risk?",
      choices: [
        { id: "A", text: "Pinning library versions and reviewing release notes", correct: true },
        { id: "B", text: "Relying only on vendor marketing materials", correct: false },
        { id: "C", text: "Using code-signing and integrity checks in the build pipeline", correct: true },
        { id: "D", text: "Disabling multi-factor authentication for developers", correct: false },
      ],
    },
    {
      id: "Q8",
      domainId: "2.0",
      domainLabel: "2.0 · Threats, Vulnerabilities, and Mitigations",
      type: "single",
      stem:
        "Which of the following BEST describes a zero-day vulnerability from a defender's perspective?",
      choices: [
        {
          id: "A",
          text: "A vulnerability that already has a vendor patch but has not been deployed",
          correct: false,
        },
        {
          id: "B",
          text: "A vulnerability that is publicly known but considered low risk",
          correct: false,
        },
        {
          id: "C",
          text: "A vulnerability that is being actively exploited before a patch or mitigation is available",
          correct: true,
        },
        {
          id: "D",
          text: "A vulnerability that only affects legacy operating systems",
          correct: false,
        },
      ],
    },

    // Domain 3.0 - Security Architecture
    {
      id: "Q9",
      domainId: "3.0",
      domainLabel: "3.0 · Security Architecture",
      type: "single",
      stem:
        "An organization wants to ensure that internal users can access SaaS applications without directly exposing those apps to the internet. Which design choice BEST supports this requirement?",
      choices: [
        { id: "A", text: "Site-to-site IPsec VPN between each user and the SaaS provider", correct: false },
        { id: "B", text: "Client-based VPN from users to the corporate network, then SSO to SaaS", correct: true },
        { id: "C", text: "Publishing SaaS login pages on an internal-only DNS zone", correct: false },
        { id: "D", text: "Using port forwarding on the user workstation router", correct: false },
      ],
    },
    {
      id: "Q10",
      domainId: "3.0",
      domainLabel: "3.0 · Security Architecture",
      type: "single",
      stem:
        "A network engineer is segmenting a production network into a user VLAN, server VLAN, and management VLAN. This design decision primarily improves which security goal?",
      choices: [
        { id: "A", text: "Non-repudiation", correct: false },
        { id: "B", text: "Least privilege and blast-radius reduction", correct: true },
        { id: "C", text: "Obfuscation of IP addressing", correct: false },
        { id: "D", text: "Physical security", correct: false },
      ],
    },
    {
      id: "Q11",
      domainId: "3.0",
      domainLabel: "3.0 · Security Architecture",
      type: "multi",
      stem:
        "A security team is designing a zero trust architecture. Which TWO principles are MOST aligned with this approach?",
      choices: [
        { id: "A", text: "Always require re-authentication when context changes significantly", correct: true },
        { id: "B", text: "Grant broad network access after initial VPN login", correct: false },
        { id: "C", text: "Use microsegmentation and per-application access policies", correct: true },
        { id: "D", text: "Rely only on perimeter firewalls for access control", correct: false },
      ],
    },
    {
      id: "Q12",
      domainId: "3.0",
      domainLabel: "3.0 · Security Architecture",
      type: "single",
      stem:
        "Which statement BEST explains the benefit of using a reverse proxy in front of a group of web applications?",
      choices: [
        { id: "A", text: "It eliminates the need for TLS on backend servers", correct: false },
        { id: "B", text: "It centralizes access control, TLS termination, and request inspection", correct: true },
        { id: "C", text: "It replaces the need for web application firewalls entirely", correct: false },
        { id: "D", text: "It stores user credentials for all backend applications", correct: false },
      ],
    },

    // Domain 4.0 - Security Operations
    {
      id: "Q13",
      domainId: "4.0",
      domainLabel: "4.0 · Security Operations",
      type: "single",
      stem:
        "An incident responder is in the containment phase of an active ransomware attack. Which action is MOST appropriate at this stage?",
      choices: [
        { id: "A", text: "Rebuild all affected systems from known-good images", correct: false },
        { id: "B", text: "Disconnect infected hosts from the network to limit spread", correct: true },
        { id: "C", text: "Publish a post-incident report to leadership", correct: false },
        { id: "D", text: "Notify users that normal operations have fully resumed", correct: false },
      ],
    },
    {
      id: "Q14",
      domainId: "4.0",
      domainLabel: "4.0 · Security Operations",
      type: "single",
      stem:
        "A SOC analyst wants to detect unusual outbound connections from endpoints. Which tool or capability is MOST appropriate?",
      choices: [
        { id: "A", text: "Configuration management database (CMDB)", correct: false },
        { id: "B", text: "NetFlow or similar flow-based monitoring", correct: true },
        { id: "C", text: "Password vault", correct: false },
        { id: "D", text: "Static application security testing (SAST)", correct: false },
      ],
    },
    {
      id: "Q15",
      domainId: "4.0",
      domainLabel: "4.0 · Security Operations",
      type: "multi",
      stem:
        "A security team is tuning SIEM alerts to reduce noise from false positives. Which TWO steps are MOST effective?",
      choices: [
        { id: "A", text: "Create baselines for normal behavior before adjusting thresholds", correct: true },
        { id: "B", text: "Disable all correlation rules that ever produced a false positive", correct: false },
        { id: "C", text: "Group related events into correlation rules instead of single-event alerts", correct: true },
        { id: "D", text: "Forward all raw logs to email for manual review", correct: false },
      ],
    },
    {
      id: "Q16",
      domainId: "4.0",
      domainLabel: "4.0 · Security Operations",
      type: "single",
      stem:
        "Which documentation would MOST likely contain step-by-step guidance for isolating a compromised workstation?",
      choices: [
        { id: "A", text: "Acceptable use policy", correct: false },
        { id: "B", text: "Incident response playbook", correct: true },
        { id: "C", text: "Memorandum of understanding (MOU)", correct: false },
        { id: "D", text: "End user license agreement (EULA)", correct: false },
      ],
    },

    // Domain 5.0 - Governance, Risk, and Compliance
    {
      id: "Q17",
      domainId: "5.0",
      domainLabel: "5.0 · Governance, Risk, and Compliance",
      type: "single",
      stem:
        "A security manager wants to estimate the expected yearly financial impact if a specific database is breached once every five years. Which metric BEST represents this value?",
      choices: [
        { id: "A", text: "Annualized loss expectancy (ALE)", correct: true },
        { id: "B", text: "Single loss expectancy (SLE)", correct: false },
        { id: "C", text: "Mean time to repair (MTTR)", correct: false },
        { id: "D", text: "Recovery point objective (RPO)", correct: false },
      ],
    },
    {
      id: "Q18",
      domainId: "5.0",
      domainLabel: "5.0 · Governance, Risk, and Compliance",
      type: "single",
      stem:
        "A company is required by law to implement specific controls to protect cardholder data. This requirement BEST describes which type of control driver?",
      choices: [
        { id: "A", text: "Regulatory", correct: true },
        { id: "B", text: "Advisory", correct: false },
        { id: "C", text: "Discretionary", correct: false },
        { id: "D", text: "Technical", correct: false },
      ],
    },
    {
      id: "Q19",
      domainId: "5.0",
      domainLabel: "5.0 · Governance, Risk, and Compliance",
      type: "multi",
      stem:
        "An internal audit finds that several systems processing personal data do not have data retention limits. Which TWO actions BEST address this finding?",
      choices: [
        { id: "A", text: "Define maximum retention periods based on legal and business requirements", correct: true },
        { id: "B", text: "Ignore the finding because storage is inexpensive", correct: false },
        { id: "C", text: "Implement automated deletion or archiving after the retention period", correct: true },
        { id: "D", text: "Disable all logging on systems that handle personal data", correct: false },
      ],
    },
    {
      id: "Q20",
      domainId: "5.0",
      domainLabel: "5.0 · Governance, Risk, and Compliance",
      type: "single",
      stem:
        "Which document typically defines roles, responsibilities, and high-level expectations for how information security is managed in an organization?",
      choices: [
        { id: "A", text: "Security awareness training slide deck", correct: false },
        { id: "B", text: "Information security policy", correct: true },
        { id: "C", text: "Standard operating procedure (SOP)", correct: false },
        { id: "D", text: "System hardening checklist", correct: false },
      ],
    },

    {
      id: "PBQ_FIREWALL",
      domainId: "3.0",
      domainLabel: "3.0 · Security Architecture (PBQ-style)",
      type: "multi",
      isPbq: true,
      previewOnly: true,
      stem:
        "Performance-based scenario: You are reviewing a three-tier web application protected by a perimeter, application, and database firewall. " +
        "Use the <strong>Three-Tier Firewall - ACL Rule Builder</strong> simulation below (Open firewall PBQ) to experiment with rules, then answer: " +
        "Which TWO rule design choices BEST follow least-privilege principles for the application tier?",
      choices: [],
    },
  ];

  var state = {
    startedAt: null,
    finishedAt: null,
    timerId: null,
    currentIndex: 0,
    answers: Object.create(null), // id -> array of choiceIds
    marked: Object.create(null), // id -> bool
    submitted: false,
    popupTimerId: null,
  };

  function $(id) {
    return document.getElementById(id);
  }

  function formatTime(ms) {
    var totalSec = Math.max(0, Math.floor(ms / 1000));
    var min = Math.floor(totalSec / 60);
    var sec = totalSec % 60;
    var mm = String(min).padStart(2, "0");
    var ss = String(sec).padStart(2, "0");
    return mm + ":" + ss;
  }

  function clampIndex(index) {
    if (index < 0) return 0;
    if (index >= QUESTIONS.length) return QUESTIONS.length - 1;
    return index;
  }

  function currentQuestion() {
    return QUESTIONS[state.currentIndex] || QUESTIONS[0];
  }

  function readAnswer(questionId) {
    var a = state.answers[questionId];
    if (!Array.isArray(a)) return [];
    return a.slice();
  }

  function writeAnswer(questionId, values) {
    if (!questionId) return;
    var arr = Array.isArray(values) ? values.filter(Boolean) : [];
    state.answers[questionId] = arr;
  }

  function isAnswered(question) {
    var a = readAnswer(question.id);
    return a.length > 0;
  }

  function toggleMarked(questionId) {
    if (!questionId) return;
    state.marked[questionId] = !state.marked[questionId];
  }

  function isMarked(questionId) {
    return !!state.marked[questionId];
  }

  function questionScore(question) {
    if (!question || !question.choices) return { correct: false, counted: false };
    var selected = readAnswer(question.id);
    if (!selected.length) return { correct: false, counted: false };
    var correctIds = question.choices.filter(function (c) {
      return c.correct;
    }).map(function (c) {
      return c.id;
    });
    if (!correctIds.length) return { correct: false, counted: false };
    if (selected.length !== correctIds.length) return { correct: false, counted: true };
    var allMatch = correctIds.every(function (id) {
      return selected.indexOf(id) !== -1;
    });
    return { correct: allMatch, counted: true };
  }

  function computeScores() {
    var totalCounted = 0;
    var totalCorrect = 0;
    var answeredCount = 0;
    var markedCount = 0;
    var byDomain = Object.create(null);

    QUESTIONS.forEach(function (q) {
      var s = questionScore(q);
      var answered = isAnswered(q);
      var marked = isMarked(q.id);
      if (answered) answeredCount++;
      if (marked) markedCount++;
      if (s.counted) {
        totalCounted++;
        if (s.correct) totalCorrect++;
      }
      var key = q.domainId + "|" + q.domainLabel;
      if (!byDomain[key]) {
        byDomain[key] = { correct: 0, total: 0 };
      }
      if (s.counted) {
        byDomain[key].total++;
        if (s.correct) byDomain[key].correct++;
      }
    });

    var domainRows = Object.keys(byDomain).map(function (key) {
      var parts = key.split("|");
      var label = parts[1] || parts[0];
      var row = byDomain[key];
      var pct = row.total ? Math.round((row.correct / row.total) * 100) : 0;
      return {
        domainLabel: label,
        correct: row.correct,
        total: row.total,
        pct: pct,
      };
    });

    domainRows.sort(function (a, b) {
      return a.domainLabel.localeCompare(b.domainLabel);
    });

    var overallPct = totalCounted ? Math.round((totalCorrect / totalCounted) * 100) : 0;

    var elapsedMs = 0;
    if (state.startedAt && state.finishedAt) {
      elapsedMs = Math.max(0, state.finishedAt - state.startedAt);
    }

    return {
      totalCounted: totalCounted,
      totalCorrect: totalCorrect,
      overallPct: overallPct,
      answeredCount: answeredCount,
      markedCount: markedCount,
      domainRows: domainRows,
      elapsedMs: elapsedMs,
    };
  }

  function updateTimer() {
    var timerEl = $("secplus-landing-exam-timer");
    if (!timerEl || !state.startedAt) return;
    var totalMs = EXAM_MINUTES * 60 * 1000;
    var elapsed = Date.now() - state.startedAt;
    var remaining = Math.max(0, totalMs - elapsed);
    timerEl.textContent = formatTime(remaining);
    if (remaining <= 0 && !state.submitted) {
      clearInterval(state.timerId);
      state.timerId = null;
      goToReview(true);
    }
  }

  function startTimer() {
    if (state.timerId) {
      clearInterval(state.timerId);
      state.timerId = null;
    }
    updateTimer();
    state.timerId = setInterval(updateTimer, 1000);
  }

  function renderNav() {
    var list = $("secplus-landing-exam-nav-list");
    var progress = $("secplus-landing-exam-progress");
    var q = currentQuestion();
    if (!list || !progress || !q) return;

    progress.textContent =
      "Question " + (state.currentIndex + 1) + " of " + QUESTIONS.length;

    list.innerHTML = "";
    QUESTIONS.forEach(function (item, index) {
      var li = document.createElement("li");
      var btn = document.createElement("button");
      btn.type = "button";
      btn.textContent = String(index + 1);
      btn.className = "landing-sample-exam-nav-item";
      if (index === state.currentIndex) btn.classList.add("is-current");
      if (isAnswered(item)) btn.classList.add("is-answered");
      if (isMarked(item.id)) btn.classList.add("is-marked");
      btn.addEventListener("click", function () {
        if (state.submitted) return;
        state.currentIndex = index;
        renderQuestion();
      });
      li.appendChild(btn);
      list.appendChild(li);
    });
  }

  function renderQuestion() {
    var host = $("secplus-landing-exam-question");
    var markBtn = $("secplus-landing-exam-mark");
    var prevBtn = $("secplus-landing-exam-prev");
    var nextBtn = $("secplus-landing-exam-next");
    var clearBtn = $("secplus-landing-exam-clear");
    var reviewBtn = $("secplus-landing-exam-review");
    var shell = $("secplus-landing-sample-exam-shell");
    var pbqSection = document.querySelector(".landing-sample-exam-pbq-embed");

    if (!host || !shell) return;

    shell.hidden = false;
    shell.setAttribute("aria-hidden", "false");

    var q = currentQuestion();
    if (!q) return;

    var selected = readAnswer(q.id);

    var html = '<p class="landing-sample-exam-question-stem">' + q.stem + "</p>";

    if (!q.previewOnly && q.choices && q.choices.length) {
      html += '<form class="landing-sample-exam-question-form" id="secplus-landing-exam-form">';

      q.choices.forEach(function (choice) {
        var inputType = q.type === "multi" ? "checkbox" : "radio";
        var checked = selected.indexOf(choice.id) !== -1;
        var name = "choice";
        var id = "secplus-choice-" + q.id + "-" + choice.id;
        html +=
          '<label class="landing-sample-exam-choice">' +
          '<input type="' +
          inputType +
          '" name="' +
          name +
          '" value="' +
          choice.id +
          '" id="' +
          id +
          '"' +
          (checked ? ' checked="checked"' : "") +
          (state.submitted ? ' disabled="disabled"' : "") +
          " />" +
          "<span>" +
          choice.text +
          "</span>" +
          "</label>";
      });

      html += "</form>";
    }

    host.innerHTML = html;

    var form = $("secplus-landing-exam-form");
    if (form && !state.submitted && !q.previewOnly) {
      form.addEventListener("change", function () {
        var chosen = [];
        var inputs = form.querySelectorAll("input[name='choice']");
        inputs.forEach(function (input) {
          if (input.checked) chosen.push(input.value);
        });
        writeAnswer(q.id, chosen);
        renderNav();
      });
    }

    if (markBtn) {
      var marked = isMarked(q.id);
      markBtn.textContent = marked ? "Unmark review" : "Mark for review";
      markBtn.disabled = !!state.submitted;
    }

    if (prevBtn) {
      prevBtn.disabled = state.currentIndex === 0 || state.submitted;
    }
    if (nextBtn) {
      nextBtn.disabled = state.currentIndex === QUESTIONS.length - 1 || state.submitted;
    }
    if (clearBtn) {
      clearBtn.disabled = state.submitted || q.previewOnly || !isAnswered(q);
    }
    if (reviewBtn) {
      reviewBtn.disabled = !!state.submitted;
    }

    if (pbqSection) {
      if (q && q.isPbq) {
        pbqSection.hidden = false;
        pbqSection.setAttribute("aria-hidden", "false");
      } else {
        pbqSection.hidden = true;
        pbqSection.setAttribute("aria-hidden", "true");
      }
    }

    renderNav();
  }

  function goToReview(autoFromTimer) {
    var shell = $("secplus-landing-sample-exam-shell");
    var confirm = $("secplus-landing-exam-confirm");
    var summary = $("secplus-landing-exam-summary");
    if (!confirm || !summary) return;

    if (shell) {
      shell.hidden = true;
      shell.setAttribute("aria-hidden", "true");
    }

    var answered = 0;
    var marked = 0;
    QUESTIONS.forEach(function (q) {
      if (isAnswered(q)) answered++;
      if (isMarked(q.id)) marked++;
    });

    var remaining = QUESTIONS.length - answered;

    summary.innerHTML = "";
    var items = [
      "Total questions: " + QUESTIONS.length,
      "Answered: " + answered,
      "Marked for review: " + marked,
      "Not answered yet: " + remaining,
    ];
    items.forEach(function (text) {
      var li = document.createElement("li");
      li.textContent = text;
      summary.appendChild(li);
    });

    if (autoFromTimer) {
      var li = document.createElement("li");
      li.textContent = "Time expired: the exam moved into review automatically.";
      summary.appendChild(li);
    }

    var check = $("secplus-landing-exam-confirm-check");
    var submit = $("secplus-landing-exam-submit");
    if (check && submit) {
      check.checked = false;
      submit.disabled = true;
      check.addEventListener("change", function () {
        submit.disabled = !check.checked;
      });
    }

    confirm.hidden = false;
  }

  function renderScorecard() {
    var scoreRoot = $("secplus-landing-exam-scorecard");
    var lead = $("secplus-landing-exam-scorecard-lead");
    var overallEl = $("secplus-landing-exam-score-overall");
    var answeredEl = $("secplus-landing-exam-score-answered");
    var markedEl = $("secplus-landing-exam-score-marked");
    var timeEl = $("secplus-landing-exam-score-time");
    var domainsBody = $("secplus-landing-exam-score-domains");
    var itemsRoot = $("secplus-landing-exam-score-items");
    if (
      !scoreRoot ||
      !lead ||
      !overallEl ||
      !answeredEl ||
      !markedEl ||
      !timeEl ||
      !domainsBody ||
      !itemsRoot
    ) {
      return;
    }

    var scores = computeScores();
    var timeUsed = scores.elapsedMs || (state.startedAt && state.finishedAt ? state.finishedAt - state.startedAt : 0);
    var percentUsed =
      state.startedAt && state.finishedAt
        ? Math.min(100, Math.round((timeUsed / (EXAM_MINUTES * 60 * 1000)) * 100))
        : null;

    var leadText =
      "You completed this timed Security+ sample with " +
      scores.answeredCount +
      " of " +
      QUESTIONS.length +
      " questions answered.";
    if (percentUsed != null) {
      leadText += " Time used: about " + formatTime(timeUsed) + " (" + percentUsed + "% of the preview limit).";
    }
    lead.textContent = leadText;

    overallEl.textContent = scores.totalCounted
      ? scores.overallPct + "% (" + scores.totalCorrect + " of " + scores.totalCounted + " scored items)"
      : "Preview only";
    answeredEl.textContent = scores.answeredCount + " of " + QUESTIONS.length;
    markedEl.textContent = String(scores.markedCount);
    timeEl.textContent = formatTime(timeUsed);

    domainsBody.innerHTML = "";
    scores.domainRows.forEach(function (row) {
      var tr = document.createElement("tr");
      var tdDomain = document.createElement("td");
      tdDomain.textContent = row.domainLabel;
      var tdCorrect = document.createElement("td");
      tdCorrect.textContent = String(row.correct);
      var tdTotal = document.createElement("td");
      tdTotal.textContent = String(row.total);
      var tdPct = document.createElement("td");
      tdPct.textContent = row.total ? row.pct + "%" : " - ";
      tr.appendChild(tdDomain);
      tr.appendChild(tdCorrect);
      tr.appendChild(tdTotal);
      tr.appendChild(tdPct);
      domainsBody.appendChild(tr);
    });

    itemsRoot.innerHTML = "";
    QUESTIONS.forEach(function (q, index) {
      var s = questionScore(q);
      var answered = isAnswered(q);
      var marked = isMarked(q.id);
      var li = document.createElement("li");
      li.className = "landing-sample-exam-scorecard-item";

      var status;
      var statusClass = "status--unanswered";
      if (!answered) {
        status = "Not answered";
      } else if (!s.counted) {
        status = "Not scored";
      } else if (s.correct) {
        status = "Correct";
        statusClass = "status--correct";
      } else {
        status = "Review";
        statusClass = "status--review";
      }

      var markLabel = marked ? " · Marked for review" : "";

      li.innerHTML =
        '<div class="landing-sample-exam-scorecard-item-main">' +
        "<span class=\"landing-sample-exam-scorecard-item-title\">Q" +
        (index + 1) +
        (q.isPbq ? " (PBQ-style)" : "") +
        "</span>" +
        "<span class=\"landing-sample-exam-scorecard-item-domain\">" +
        q.domainLabel +
        "</span>" +
        "</div>" +
        '<div class="landing-sample-exam-scorecard-item-meta">' +
        "<span class=\"landing-sample-exam-scorecard-status " +
        statusClass +
        "\">" +
        status +
        "</span>" +
        (markLabel
          ? '<span class="landing-sample-exam-scorecard-flag">' + markLabel.replace(/^\s*·\s*/, "") + "</span>"
          : "") +
        "</div>";

      itemsRoot.appendChild(li);
    });

    scoreRoot.hidden = false;
  }

  function schedulePopup() {
    if (state.popupTimerId) {
      clearTimeout(state.popupTimerId);
      state.popupTimerId = null;
    }
    state.popupTimerId = setTimeout(function () {
      showPopup();
    }, 2 * 60 * 1000);
  }

  function showPopup() {
    var existing = document.getElementById("secplus-landing-exam-popup");
    if (existing) return;

    var root = document.createElement("div");
    root.id = "secplus-landing-exam-popup";
    root.className = "landing-sample-exam-popup-root";
    root.setAttribute("role", "dialog");
    root.setAttribute("aria-modal", "true");
    root.innerHTML =
      '<div class="landing-sample-exam-popup-backdrop"></div>' +
      '<div class="landing-sample-exam-popup-panel" aria-labelledby="secplus-landing-exam-popup-title" tabindex="-1">' +
      '<button type="button" class="landing-sample-exam-popup-close" aria-label="Close dialog">×</button>' +
      '<p class="landing-sample-exam-popup-eyebrow">30-day full access · $19.99</p>' +
      '<h2 id="secplus-landing-exam-popup-title">Ready to practice like test day?</h2>' +
      '<p class="landing-sample-exam-popup-lead">' +
      "You just finished a timed preview. The full Security+ library adds 1000+ questions, 34 PBQ scenarios, adaptive review, and the complete 90-minute exam simulation in your browser." +
      "</p>" +
      '<div class="landing-sample-exam-popup-actions">' +
      '<a href="#purchase" class="landing-sample-exam-btn landing-sample-exam-btn--primary" data-secplus-portal-30d-checkout>' +
      "Unlock full Security+ access · $19.99" +
      "</a>" +
      '<a href="/comptia-sec+-home.html" class="landing-sample-exam-btn landing-sample-exam-btn--secondary">' +
      "Return to Security+ home" +
      "</a>" +
      "</div>" +
      "</div>";

    document.body.appendChild(root);

    var panel = root.querySelector(".landing-sample-exam-popup-panel");
    var closeBtn = root.querySelector(".landing-sample-exam-popup-close");
    var backdrop = root.querySelector(".landing-sample-exam-popup-backdrop");

    function close() {
      root.remove();
      document.removeEventListener("keydown", onKey);
    }

    function onKey(ev) {
      if (ev.key === "Escape") {
        ev.preventDefault();
        close();
      }
    }

    if (closeBtn) closeBtn.addEventListener("click", close);
    if (backdrop) backdrop.addEventListener("click", close);
    document.addEventListener("keydown", onKey);
    if (panel) panel.focus();
  }

  function injectStyles() {
    if (document.head.querySelector("style[data-secplus-landing-exam]")) return;
    var s = document.createElement("style");
    s.setAttribute("data-secplus-landing-exam", "1");
    s.textContent =
      ".landing-sample-exam{margin-top:24px;padding:18px 16px;border-radius:16px;border:1px solid rgba(148,163,184,.4);background:linear-gradient(135deg,rgba(15,23,42,.96),rgba(30,64,175,.85));color:#e5e7eb}" +
      ".landing-sample-exam__intro h3{margin:0 0 8px;font-size:1.15rem;line-height:1.3;color:#f9fafb}" +
      ".landing-sample-exam-lead{margin:0 0 6px;font-size:.9rem;line-height:1.55;color:#e5e7eb}" +
      ".landing-sample-exam-meta{margin:0 0 10px;font-size:.85rem;line-height:1.5;color:#cbd5e1}" +
      ".landing-sample-exam-note{margin:6px 0 0;font-size:.8rem;color:#9ca3af}" +
      ".landing-sample-exam-start{margin-top:8px}" +
      ".landing-sample-exam-shell{margin-top:16px;padding:14px 0;border-radius:0;background:transparent;border:0}" +
      ".landing-sample-exam-header{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:6px 10px;margin-bottom:10px}" +
      ".landing-sample-exam-timer-wrap{display:flex;flex-direction:column;gap:2px}" +
      ".landing-sample-exam-timer-label{font-size:.75rem;color:#9ca3af;text-transform:uppercase;letter-spacing:.06em;font-weight:700}" +
      ".landing-sample-exam-timer{font-variant-numeric:tabular-nums;font-size:1.1rem;font-weight:800;color:#f97316}" +
      ".landing-sample-exam-progress{font-size:.82rem;font-weight:600;color:#e5e7eb}" +
      ".landing-sample-exam-layout{display:grid;grid-template-columns: minmax(0,3fr) minmax(0,1.4fr);gap:14px}" +
      "@media (max-width:960px){.landing-sample-exam-layout{grid-template-columns:minmax(0,1fr);}}" +
      ".landing-sample-exam-question-header{margin-bottom:4px}" +
      ".landing-sample-exam-question-type{margin:0;font-size:.8rem;color:#cbd5e1}" +
      ".landing-sample-exam-question-stem{margin:8px 0 10px;font-size:.92rem;line-height:1.55;color:#f9fafb}" +
      ".landing-sample-exam-choice{display:flex;align-items:flex-start;gap:8px;margin-bottom:6px;padding:8px 9px;border-radius:10px;background:rgba(15,23,42,.9);border:1px solid rgba(148,163,184,.4);cursor:pointer;font-size:.9rem;line-height:1.45;color:#e5e7eb}" +
      ".landing-sample-exam-choice input{margin-top:3px}" +
      ".landing-sample-exam-choice:hover{border-color:#a5b4fc;background:rgba(30,64,175,.4)}" +
      ".landing-sample-exam-nav{padding:6px 0 4px}" +
      ".landing-sample-exam-nav-title{margin:0 0 6px;font-size:.85rem;font-weight:700;color:#e5e7eb}" +
      ".landing-sample-exam-nav-list{display:flex;flex-wrap:wrap;gap:6px;list-style:none;margin:0 0 6px;padding:0}" +
      ".landing-sample-exam-nav-item{min-width:32px;min-height:32px;border-radius:999px;border:1px solid rgba(148,163,184,.7);background:rgba(15,23,42,.95);color:#e5e7eb;font-size:.8rem;font-weight:700;cursor:pointer}" +
      ".landing-sample-exam-nav-item.is-current{border-color:#f97316;background:rgba(249,115,22,.16)}" +
      ".landing-sample-exam-nav-item.is-answered{border-color:#22c55e}" +
      ".landing-sample-exam-nav-item.is-marked{box-shadow:0 0 0 2px rgba(251,191,36,.8)}" +
      ".landing-sample-exam-legend{margin:0;font-size:.75rem;color:#9ca3af;display:flex;align-items:center;gap:10px;flex-wrap:wrap}" +
      ".legend-dot{width:10px;height:10px;border-radius:999px;display:inline-block}" +
      ".legend-dot--answered{background:#22c55e}" +
      ".legend-dot--marked{background:#fbbf24}" +
      ".landing-sample-exam-actions{margin-top:12px;display:flex;flex-wrap:wrap;gap:8px;justify-content:flex-end}" +
      ".landing-sample-exam-btn{border-radius:999px;padding:8px 14px;font-size:.85rem;font-weight:700;border:1px solid transparent;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;justify-content:center;gap:6px;white-space:nowrap}" +
      ".landing-sample-exam-btn--primary{background:#4f46e5;border-color:#6366f1;color:#f9fafb}" +
      ".landing-sample-exam-btn--primary:hover{filter:brightness(1.05)}" +
      ".landing-sample-exam-btn--secondary{background:transparent;border-color:rgba(148,163,184,.8);color:#e5e7eb}" +
      ".landing-sample-exam-btn--secondary:hover{background:rgba(148,163,184,.12)}" +
      ".landing-sample-exam-btn--ghost{background:transparent;border-color:transparent;color:#cbd5e1}" +
      ".landing-sample-exam-btn--ghost:hover{background:rgba(148,163,184,.12)}" +
      ".landing-sample-exam-btn--finish{background:#f97316;border-color:#fdba74;color:#111827}" +
      ".landing-sample-exam-btn--quit{margin-right:auto}" +
      ".landing-sample-exam-btn[disabled]{opacity:.55;cursor:not-allowed}" +
      ".landing-sample-exam-confirm{margin-top:16px;padding:14px 12px;border-radius:14px;background:rgba(15,23,42,.98);border:1px solid rgba(148,163,184,.6);color:#e5e7eb}" +
      ".landing-sample-exam-confirm h3{margin:0 0 8px;font-size:1rem;color:#f9fafb}" +
      ".landing-sample-exam-summary{margin:4px 0 10px;padding-left:1.1rem;font-size:.88rem;color:#e5e7eb}" +
      ".landing-sample-exam-confirm-check{display:flex;align-items:flex-start;gap:8px;margin:0 0 12px;font-size:.86rem;color:#e5e7eb}" +
      ".landing-sample-exam-confirm-check input{margin-top:3px}" +
      ".landing-sample-exam-compare{margin:0 0 12px;padding-top:8px;border-top:1px solid rgba(148,163,184,.5);font-size:.86rem;color:#e5e7eb}" +
      ".landing-sample-exam-compare h4{margin:0 0 6px;font-size:.9rem;color:#f9fafb}" +
      ".landing-sample-exam-compare ul{margin:0;padding-left:1.1rem}" +
      ".landing-sample-exam-confirm-actions{display:flex;flex-wrap:wrap;gap:8px;justify-content:flex-end}" +
      ".landing-sample-exam-scorecard{margin-top:16px;padding:14px 12px 12px;border-radius:14px;background:rgba(15,23,42,.98);border:1px solid rgba(148,163,184,.6);color:#e5e7eb}" +
      ".landing-sample-exam-scorecard-lead{margin:0 0 10px;font-size:.9rem;color:#e5e7eb}" +
      ".landing-sample-exam-scorecard-grid{display:grid;grid-template-columns: minmax(0,1.3fr) minmax(0,2fr);gap:12px;margin-bottom:10px}" +
      "@media (max-width:960px){.landing-sample-exam-scorecard-grid{grid-template-columns:minmax(0,1fr);}}" +
      ".landing-sample-exam-scorecard-metrics{margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px 10px;font-size:.86rem}" +
      ".landing-sample-exam-scorecard-metrics div{display:flex;flex-direction:column;gap:2px;padding:6px 8px;border-radius:10px;background:rgba(15,23,42,.9);border:1px solid rgba(148,163,184,.5)}" +
      ".landing-sample-exam-scorecard-metrics dt{font-size:.78rem;color:#9ca3af}" +
      ".landing-sample-exam-scorecard-metrics dd{margin:0;font-size:.9rem;font-weight:700;color:#f9fafb}" +
      ".landing-sample-exam-scorecard-table{width:100%;border-collapse:collapse;font-size:.82rem}" +
      ".landing-sample-exam-scorecard-table th,.landing-sample-exam-scorecard-table td{border:1px solid rgba(148,163,184,.55);padding:4px 6px;text-align:left}" +
      ".landing-sample-exam-scorecard-table th{background:rgba(15,23,42,.95);font-weight:700;color:#e5e7eb}" +
      ".landing-sample-exam-scorecard-detail h4{margin:0 0 6px;font-size:.9rem;color:#f9fafb}" +
      ".landing-sample-exam-scorecard-list{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:6px;font-size:.86rem}" +
      ".landing-sample-exam-scorecard-item{padding:7px 8px;border-radius:10px;border:1px solid rgba(148,163,184,.5);background:rgba(15,23,42,.9);display:flex;flex-direction:column;gap:2px}" +
      ".landing-sample-exam-scorecard-item-main{display:flex;flex-wrap:wrap;justify-content:space-between;gap:4px 10px}" +
      ".landing-sample-exam-scorecard-item-title{font-weight:700;color:#f9fafb}" +
      ".landing-sample-exam-scorecard-item-domain{font-size:.8rem;color:#9ca3af}" +
      ".landing-sample-exam-scorecard-item-meta{display:flex;flex-wrap:wrap;gap:6px 10px;font-size:.8rem}" +
      ".landing-sample-exam-scorecard-status{font-weight:700;text-transform:uppercase;letter-spacing:.04em}" +
      ".landing-sample-exam-scorecard-status.status--correct{color:#4ade80}" +
      ".landing-sample-exam-scorecard-status.status--review{color:#facc15}" +
      ".landing-sample-exam-scorecard-status.status--unanswered{color:#9ca3af}" +
      ".landing-sample-exam-scorecard-flag{color:#facc15}" +
      ".landing-sample-exam-cta-row{margin-top:10px;display:flex;flex-wrap:wrap;gap:8px;justify-content:flex-end}" +
      ".landing-sample-exam-scorecard-note{margin:6px 0 0;font-size:.8rem;color:#9ca3af}" +
      ".landing-sample-exam-pbq-embed{margin-top:16px;padding-top:10px;border-top:1px solid rgba(148,163,184,.45);font-size:.86rem;color:#cbd5e1}" +
      ".landing-sample-exam-pbq-embed h4{margin:0 0 6px;font-size:.9rem;color:#f9fafb}" +
      ".landing-sample-exam-pbq-embed p{margin:0 0 8px}" +
      ".landing-sample-exam-pbq-frame-wrap{border-radius:12px;overflow:hidden;border:1px solid rgba(148,163,184,.6);background:#020617}" +
      ".landing-sample-exam-pbq-frame-wrap iframe{display:block;width:100%;min-height:460px;border:0;background:#020617}" +
      ".landing-sample-exam-popup-root{position:fixed;inset:0;z-index:22000;display:flex;align-items:center;justify-content:center;padding:16px}" +
      ".landing-sample-exam-popup-backdrop{position:absolute;inset:0;background:rgba(15,23,42,.8);backdrop-filter:blur(4px)}" +
      ".landing-sample-exam-popup-panel{position:relative;z-index:1;width:min(520px,100%);max-height:min(90vh,640px);overflow:auto;margin:0;padding:20px 18px 18px;border-radius:16px;border:1px solid #6366f1;background:linear-gradient(155deg,rgba(15,23,42,.98),rgba(30,64,175,.96));color:#e5e7eb;box-shadow:0 24px 64px rgba(15,23,42,.8)}" +
      ".landing-sample-exam-popup-close{position:absolute;top:8px;right:10px;border:0;background:transparent;color:#cbd5e1;font-size:1.6rem;line-height:1;cursor:pointer;padding:4px 6px}" +
      ".landing-sample-exam-popup-eyebrow{margin:0 0 6px;font-size:.78rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#c4b5fd}" +
      ".landing-sample-exam-popup-panel h2{margin:0 0 10px;font-size:1.15rem;color:#f9fafb}" +
      ".landing-sample-exam-popup-lead{margin:0 0 14px;font-size:.9rem;line-height:1.55;color:#e5e7eb}" +
      ".landing-sample-exam-popup-actions{display:flex;flex-direction:column;gap:8px}" +
      ".landing-sample-exam-popup-actions .landing-sample-exam-btn{width:100%}";
    document.head.appendChild(s);
  }

  function wireEvents() {
    var startBtn = $("secplus-landing-sample-exam-start");
    var sampleRoot = $("secplus-landing-sample-exam");
    var shell = $("secplus-landing-sample-exam-shell");
    var quitBtn = $("secplus-landing-exam-quit");
    var pbqSection = document.querySelector(".landing-sample-exam-pbq-embed");
    var confirm = $("secplus-landing-exam-confirm");
    var scorecard = $("secplus-landing-exam-scorecard");
    var prevBtn = $("secplus-landing-exam-prev");
    var nextBtn = $("secplus-landing-exam-next");
    var markBtn = $("secplus-landing-exam-mark");
    var clearBtn = $("secplus-landing-exam-clear");
    var reviewBtn = $("secplus-landing-exam-review");
    var confirmBackBtn = $("secplus-landing-exam-confirm-back");
    var submitBtn = $("secplus-landing-exam-submit");

    if (startBtn) {
      startBtn.addEventListener("click", function () {
        if (!state.startedAt) {
          state.startedAt = Date.now();
          startTimer();
        }
        if (sampleRoot) {
          var intro = sampleRoot.querySelector(".landing-sample-exam__intro");
          if (intro) {
            intro.hidden = true;
            intro.setAttribute("aria-hidden", "true");
          }
        }
        if (shell) {
          shell.hidden = false;
          shell.setAttribute("aria-hidden", "false");
        }
        if (confirm) confirm.hidden = true;
        if (scorecard) scorecard.hidden = true;
        state.submitted = false;
        renderQuestion();
      });
    }

    if (quitBtn) {
      quitBtn.addEventListener("click", function () {
        // Reset timer
        if (state.timerId) {
          clearInterval(state.timerId);
          state.timerId = null;
        }
        if (state.popupTimerId) {
          clearTimeout(state.popupTimerId);
          state.popupTimerId = null;
        }
        state.startedAt = null;
        state.finishedAt = null;
        state.currentIndex = 0;
        state.answers = Object.create(null);
        state.marked = Object.create(null);
        state.submitted = false;

        // Hide exam shell, show intro text again
        if (shell) {
          shell.hidden = true;
          shell.setAttribute("aria-hidden", "true");
        }
        if (sampleRoot) {
          var intro = sampleRoot.querySelector(".landing-sample-exam__intro");
          if (intro) {
            intro.hidden = false;
            intro.setAttribute("aria-hidden", "false");
          }
        }

        if (confirm) confirm.hidden = true;
        if (scorecard) scorecard.hidden = true;
      });
    }

    if (prevBtn) {
      prevBtn.addEventListener("click", function () {
        if (state.submitted) return;
        state.currentIndex = clampIndex(state.currentIndex - 1);
        renderQuestion();
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener("click", function () {
        if (state.submitted) return;
        state.currentIndex = clampIndex(state.currentIndex + 1);
        renderQuestion();
      });
    }

    if (markBtn) {
      markBtn.addEventListener("click", function () {
        if (state.submitted) return;
        var q = currentQuestion();
        if (!q) return;
        toggleMarked(q.id);
        renderQuestion();
      });
    }

    if (clearBtn) {
      clearBtn.addEventListener("click", function () {
        if (state.submitted) return;
        var q = currentQuestion();
        if (!q) return;
        writeAnswer(q.id, []);
        renderQuestion();
      });
    }

    if (reviewBtn) {
      reviewBtn.addEventListener("click", function () {
        if (state.submitted) return;
        goToReview(false);
      });
    }

    if (confirmBackBtn) {
      confirmBackBtn.addEventListener("click", function () {
        if (confirm) confirm.hidden = true;
        if (shell) {
          shell.hidden = false;
          shell.setAttribute("aria-hidden", "false");
        }
        renderQuestion();
      });
    }

    if (submitBtn) {
      submitBtn.addEventListener("click", function () {
        if (submitBtn.disabled || state.submitted) return;
        state.submitted = true;
        state.finishedAt = Date.now();
        if (state.timerId) {
          clearInterval(state.timerId);
          state.timerId = null;
        }
        if (confirm) confirm.hidden = true;
        renderScorecard();
        schedulePopup();
      });
    }
  }

  function init() {
    var root = $("secplus-landing-sample-exam");
    if (!root) return;
    injectStyles();
    state.currentIndex = 0;
    wireEvents();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();


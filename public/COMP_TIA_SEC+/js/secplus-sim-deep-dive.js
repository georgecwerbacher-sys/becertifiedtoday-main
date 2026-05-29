(function () {
  "use strict";

  var CONTENT = {
    "simulation-dark-web-account-protection.html": {
      title: "Deep dive — dark web account protection",
      html:
        '<p>Use this walkthrough after you have opened all three leaked documents. Each step builds on the evidence.</p>' +
        '<ol class="deep-dive-steps">' +
        "<li><h3>Understand the scenario</h3>" +
        "<p>Directory contents, a compensation report, and user data appeared on the dark web. The CIO wants the <strong>most secure account protection</strong> now, plus a <strong>containment</strong> control that does <strong>not</strong> wipe kiosk forensic images.</p></li>" +
        "<li><h3>Review the leaked evidence</h3><ul>" +
        "<li><strong>Directory</strong> — 8-character minimum, weak complexity, 90-day expiration is enforced.</li>" +
        "<li><strong>Compensation report</strong> — reuse, short passwords, long password age; compares PIN, SMS, OTP, and FIDO.</li>" +
        "<li><strong>User data</strong> — audit table shows age, length, complexity, and reuse across apps.</li>" +
        "</ul></li>" +
        "<li><h3>Step 2 — weak password practices</h3><ul>" +
        "<li><strong>Age</strong> — passwords unchanged 12–15 months.</li>" +
        "<li><strong>Reuse</strong> — same password on VPN, email, timeclock.</li>" +
        "<li><strong>Length</strong> — most at 8-character minimum.</li>" +
        "<li><strong>Complexity</strong> — dictionary words, no symbols.</li>" +
        "<li><strong>Expiration</strong> — do <em>not</em> select; rotation is active.</li>" +
        '</ul><p class="deep-dive-answer">Answer: Age, Reuse, Length, Complexity.</p></li>' +
        "<li><h3>Step 3 — containment</h3><ul>" +
        "<li><strong>FIDO security key</strong> — hardware-bound, phishing-resistant, no secrets typed on a compromised host.</li>" +
        "<li>PIN, SMS, and OTP are weaker and may leave traces on the workstation.</li>" +
        '</ul><p class="deep-dive-answer">Answer: FIDO security key.</p></li>' +
        "<li><h3>Submit</h3><p>Select the four weak practices and FIDO, then <strong>Check Answers</strong>.</p></li>" +
        "</ol>",
    },
    "hotspot-attack-identification-remediation.html": {
      title: "Deep dive — attack identification and remediation",
      html:
        "<p>Match each scenario to the attack type, then pick the best preventive or remediation action for that threat.</p>" +
        '<ol class="deep-dive-steps">' +
        "<li><h3>Row 1 — distributed SYN flood</h3>" +
        "<p>Multiple SYN packets from many sources targeting a web server describes a <strong>DDoS</strong> pattern, often executed by a <strong>botnet</strong>.</p>" +
        '<p class="deep-dive-answer">Botnet → Enable DDoS protection.</p></li>' +
        "<li><h3>Row 2 — remote command execution</h3>" +
        "<p>A connection that lets an attacker run commands remotely is a <strong>RAT</strong> (remote access trojan). Disable the service that allows unsolicited remote control.</p>" +
        '<p class="deep-dive-answer">RAT → Disable remote access services.</p></li>' +
        "<li><h3>Row 3 — self-propagating SQL compromise</h3>" +
        "<p>Self-propagation plus default credentials on a database server is classic <strong>worm</strong> behavior. Change weak default passwords.</p>" +
        '<p class="deep-dive-answer">Worm → Change the default system password.</p></li>' +
        "<li><h3>Row 4 — credential harvesting via input monitoring</h3>" +
        "<p>Hardware or software that captures keystrokes is a <strong>keylogger</strong>. Push-based <strong>2FA</strong> reduces reliance on typed passwords alone.</p>" +
        '<p class="deep-dive-answer">Keylogger → Implement 2FA using push notification.</p></li>' +
        "<li><h3>Row 5 — hidden access in custom code</h3>" +
        "<p>Hidden access that bypasses login in an internal application is a <strong>backdoor</strong>. Find and remove it with a <strong>code review</strong>.</p>" +
        '<p class="deep-dive-answer">Backdoor → Conduct a code review.</p></li>' +
        "<li><h3>Verify</h3><p>All five rows must be correct. Use <strong>Show Answer</strong> to compare, then <strong>Reset</strong> to retry.</p></li>" +
        "</ol>",
    },
    "simulation-malware-outbreak-classification.html": {
      title: "Deep dive — malware outbreak classification",
      html:
        "<p>Classify each host as <strong>Origin</strong>, <strong>Infected</strong>, or <strong>Clean</strong> using endpoint logs and AV events.</p>" +
        '<ol class="deep-dive-steps">' +
        "<li><h3>Review every host log</h3>" +
        "<p>Click each device in the topology and read the full log before classifying. Look for typosquatted processes (<code>svch0st</code>, <code>scvh0st</code>), disabled AV, failed quarantine, and early outbound traffic.</p></li>" +
        "<li><h3>Find the origin</h3>" +
        "<p><strong>192.168.10.22</strong> shows AV disabled around 02:31, suspicious process names, and outbound traffic before other hosts were affected. That is the outbreak source.</p>" +
        '<p class="deep-dive-answer">Origin: 192.168.10.22</p></li>' +
        "<li><h3>Mark still-infected hosts</h3>" +
        "<p><strong>192.168.10.41</strong> and <strong>10.10.9.18</strong> could not quarantine <code>svch0st.exe</code> (or similar) — malware is still present.</p>" +
        '<p class="deep-dive-answer">Infected: 192.168.10.41 and 10.10.9.18</p></li>' +
        "<li><h3>Mark cleaned hosts</h3>" +
        "<p><strong>192.168.10.37</strong> and <strong>10.10.9.12</strong> successfully quarantined the threat after definitions updated.</p>" +
        '<p class="deep-dive-answer">Clean: 192.168.10.37 and 10.10.9.12</p></li>' +
        "<li><h3>Submit</h3><p>Every host needs a classification. <strong>Check Answers</strong> when all five are set.</p></li>" +
        "</ol>",
    },
    "simulation-vpc-payment-architecture.html": {
      title: "Deep dive — VPC payment architecture",
      html:
        "<p>Place each component in the payment VPC and label the middle tier subnet correctly.</p>" +
        '<ol class="deep-dive-steps">' +
        "<li><h3>Internet edge</h3>" +
        "<p>Traffic from the Internet Gateway hits <strong>WAF</strong> first (node 2) to filter application-layer attacks before it reaches internal tiers.</p>" +
        '<p class="deep-dive-answer">Node 2: WAF</p></li>' +
        "<li><h3>Public subnet — load balancing</h3>" +
        "<p>Nodes <strong>1</strong> and <strong>3</strong> sit in the public subnet as redundant <strong>Load Balancers</strong> distributing traffic to the app tier.</p>" +
        '<p class="deep-dive-answer">Nodes 1 &amp; 3: Load Balancer</p></li>' +
        "<li><h3>Middle tier — application</h3>" +
        "<p>The middle zone is a <strong>Private subnet</strong>. Node <strong>4</strong> is an <strong>Autoscaling Instance</strong> for elastic app capacity; nodes <strong>5</strong> and <strong>6</strong> are standard <strong>Instance</strong> nodes.</p>" +
        '<p class="deep-dive-answer">Middle subnet: Private subnet · Node 4: Autoscaling Instance · Nodes 5 &amp; 6: Instance</p></li>' +
        "<li><h3>Data tier</h3>" +
        "<p>Node <strong>7</strong> in the private subnet is the <strong>Database</strong> — no direct internet path; payment data stays isolated.</p>" +
        '<p class="deep-dive-answer">Node 7: Database</p></li>' +
        "<li><h3>Verify</h3><p>Fill every dropdown, then <strong>Check Answers</strong>. WAF at the edge, LB in public, apps in private, DB deepest.</p></li>" +
        "</ol>",
    },
    "simulation-secure-web-architecture-openssl.html": {
      title: "Deep dive — secure web architecture and OpenSSL CSR",
      html:
        "<p>Complete <strong>Part 1</strong> (architecture) and <strong>Part 2</strong> (OpenSSL command snippets).</p>" +
        '<ol class="deep-dive-steps">' +
        "<li><h3>Part 1 — perimeter to application</h3><ul>" +
        "<li><strong>Position 1 (Internet)</strong> — <strong>Firewall</strong> filters inbound traffic first.</li>" +
        "<li><strong>Position 2</strong> — <strong>Router</strong> moves traffic between network segments.</li>" +
        "<li><strong>Position 3</strong> — <strong>WAF</strong> blocks XSS, CSRF, and directory traversal against the web app.</li>" +
        "<li><strong>Position 4</strong> — <strong>Web server</strong> hosts the application.</li>" +
        "<li><strong>Position 5 (PKI)</strong> — <strong>PKI certificate</strong> enables TLS for secure protocols.</li>" +
        '</ul><p class="deep-dive-answer">arch-1 Firewall · arch-2 Router · arch-3 WAF · arch-4 Web server · arch-5 PKI certificate</p></li>' +
        "<li><h3>Part 2 — OpenSSL CSR syntax</h3>" +
        "<p>Command: <code>openssl req -new -newkey … -key … -out …</code></p><ul>" +
        "<li><strong>-new -newkey</strong> → <code>rsa:2048</code> (2048-bit RSA key pair).</li>" +
        "<li><strong>-key</strong> → <code>/certificate/csr.key</code> (private key output path).</li>" +
        "<li><strong>-out</strong> → <code>/certificate/example.com.csr</code> (CSR output file).</li>" +
        '</ul><p class="deep-dive-answer">cmd-1 rsa:2048 · cmd-2 /certificate/csr.key · cmd-3 /certificate/example.com.csr</p></li>' +
        "<li><h3>Verify</h3><p>Switch tabs to complete both parts, then <strong>Check Answers</strong>.</p></li>" +
        "</ol>",
    },
  };

  function pageSlug() {
    var path = location.pathname || "";
    try {
      var lower = path.toLowerCase();
      if (lower === "/secplus-sample" || lower === "/secplus-sample/") {
        var remembered = sessionStorage.getItem("ccnaLastRealPath");
        if (remembered) path = remembered;
      }
    } catch (e) {}
    var match = /\/([^/]+\.html)$/.exec(path);
    return match ? match[1] : "";
  }

  function ensureActionsLayout() {
    var actions = document.querySelector(".actions");
    if (!actions) return null;
    if (!actions.querySelector(".actions__primary")) {
      var primary = document.createElement("div");
      primary.className = "actions__primary";
      while (actions.firstChild) {
        primary.appendChild(actions.firstChild);
      }
      actions.appendChild(primary);
    }
    if (!actions.querySelector(".deep-dive-btn")) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "deep-dive-btn";
      btn.id = "deepDiveBtn";
      btn.textContent = "Deep dive explanation";
      actions.appendChild(btn);
    }
    return actions;
  }

  function ensureModal() {
    var modal = document.getElementById("secplusDeepDiveModal");
    if (modal) return modal;
    modal = document.createElement("div");
    modal.id = "secplusDeepDiveModal";
    modal.className = "secplus-deep-dive-modal";
    modal.setAttribute("role", "dialog");
    modal.setAttribute("aria-modal", "true");
    modal.setAttribute("aria-labelledby", "secplusDeepDiveTitle");
    modal.hidden = true;
    modal.innerHTML =
      '<div class="secplus-deep-dive-modal__panel">' +
      '<div class="secplus-deep-dive-modal__head">' +
      '<h2 class="secplus-deep-dive-modal__title" id="secplusDeepDiveTitle">Deep dive</h2>' +
      '<button type="button" class="secplus-deep-dive-modal__close" id="secplusDeepDiveClose">Close</button>' +
      "</div>" +
      '<div class="secplus-deep-dive-modal__body" id="secplusDeepDiveBody"></div>' +
      "</div>";
    document.body.appendChild(modal);
    return modal;
  }

  function init() {
    var slug = pageSlug();
    var entry = CONTENT[slug];
    if (!entry) return;

    ensureActionsLayout();
    var modal = ensureModal();
    var titleEl = document.getElementById("secplusDeepDiveTitle");
    var bodyEl = document.getElementById("secplusDeepDiveBody");
    var closeBtn = document.getElementById("secplusDeepDiveClose");
    var openBtn = document.getElementById("deepDiveBtn");

    function openDeepDive() {
      titleEl.textContent = entry.title;
      bodyEl.innerHTML = entry.html;
      modal.hidden = false;
      modal.classList.add("open");
      closeBtn.focus();
    }

    function closeDeepDive() {
      modal.hidden = true;
      modal.classList.remove("open");
      bodyEl.innerHTML = "";
      if (openBtn) openBtn.focus();
    }

    if (openBtn && !openBtn.dataset.deepDiveBound) {
      openBtn.dataset.deepDiveBound = "1";
      openBtn.addEventListener("click", openDeepDive);
    }
    if (closeBtn && !closeBtn.dataset.deepDiveBound) {
      closeBtn.dataset.deepDiveBound = "1";
      closeBtn.addEventListener("click", closeDeepDive);
    }
    if (!modal.dataset.deepDiveBound) {
      modal.dataset.deepDiveBound = "1";
      modal.addEventListener("click", function (ev) {
        if (ev.target === modal) closeDeepDive();
      });
    }
    if (!document.documentElement.dataset.secplusDeepDiveEsc) {
      document.documentElement.dataset.secplusDeepDiveEsc = "1";
      document.addEventListener("keydown", function (ev) {
        if (ev.key === "Escape" && modal.classList.contains("open")) closeDeepDive();
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

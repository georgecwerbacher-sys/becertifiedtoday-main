(function () {
  "use strict";

  var CONTENT = {
    "simulation-dark-web-account-protection.html": {
      title: "Deep dive — BeCertifiedToday.com dark web IR",
      html:
        '<p>Use this walkthrough after you have opened all three leaked documents. Each step builds on the evidence.</p>' +
        '<ol class="deep-dive-steps">' +
        "<li><h3>Understand the scenario</h3>" +
        "<p><strong>BeCertifiedToday.com</strong> case <strong>IR-2024-0847</strong> (ASAP): directory contents, a compensation report, and user data appeared on the dark web. " +
        "Contain account risk with the <strong>most secure protection</strong> available and choose a <strong>containment</strong> control that does <strong>not</strong> wipe kiosk forensic images.</p></li>" +
        "<li><h3>Directory contents — leaked file index</h3>" +
        "<p>IR recovered this index from the dark-web bundle. It shows how the three exposed data sets relate and what to read in each artifact.</p>" +
        '<ul class="doc-tree" style="list-style:none;margin:0 0 12px;padding:12px;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:0.84rem;background:#f8fafc;border:1px solid #e5e7eb;border-radius:8px">' +
        '<li style="margin:4px 0;color:#2563eb;font-weight:700">/leak/becertifiedtoday-com/</li>' +
        '<li style="margin:4px 0;color:#334155;padding-left:1rem">├── directory/</li>' +
        '<li style="margin:4px 0;color:#334155;padding-left:1rem">│   ├── ad_password_policy.txt</li>' +
        '<li style="margin:4px 0;color:#334155;padding-left:1rem">│   └── shared_drive_index.csv</li>' +
        '<li style="margin:4px 0;color:#334155;padding-left:1rem">├── compensation/</li>' +
        '<li style="margin:4px 0;color:#334155;padding-left:1rem">│   └── compensation_report_Q3.pdf</li>' +
        '<li style="margin:4px 0;color:#334155;padding-left:1rem">└── user_data/</li>' +
        '<li style="margin:4px 0;color:#334155;padding-left:1rem">    └── employee_credential_audit.csv</li>' +
        "</ul>" +
        "<p><strong>ad_password_policy.txt</strong></p>" +
        '<pre style="margin:0 0 12px;padding:12px;background:#0f172a;color:#e2e8f0;border-radius:8px;font-size:0.8rem;line-height:1.45;white-space:pre-wrap">Minimum password length .......... 8 characters\nComplexity requirement ............. Letters OR numbers (symbols not required)\nPassword history ................... Last 3 passwords remembered\nMaximum password age ............... 90 days (expiration enforced)\n\nIR note: Password expiration is functioning for standard accounts.\nInvestigate age, reuse, length, and complexity gaps instead.</pre>' +
        "<p><strong>shared_drive_index.csv (excerpt)</strong></p>" +
        '<pre style="margin:0 0 12px;padding:12px;background:#0f172a;color:#e2e8f0;border-radius:8px;font-size:0.8rem;line-height:1.45;white-space:pre-wrap">HR/Policies/password-guidelines.docx\nFinance/compensation_report_Q3.pdf\nIT/Forensics/kiosk_disk_image_hold-list.txt  ← do not reimage until containment chosen</pre>' +
        "<p>Takeaway: 8-character minimum, weak complexity, and active 90-day expiration — focus Step 2 on <strong>age, reuse, length, and complexity</strong>, not missing expiration.</p></li>" +
        "<li><h3>Compensation report — Q3 (HR document)</h3>" +
        "<p>Open the <strong>Compensation report</strong> tile for payroll and bonus sample tables only (department accruals and individual base/bonus excerpt). " +
        "That file is the original HR submission — not where security findings appear in this simulation.</p></li>" +
        "<li><h3>User data — payroll export from file share</h3>" +
        "<p>Open <strong>User data</strong> for <code>employee_credential_audit.csv</code> pulled from <code>\\\\corp-fs01\\Finance\\Restricted\\user_data\\</code>. " +
        "The sim shows the export table only (logo, sensitive tag, file-share path). Use the table plus the interpretation below for Step 2.</p>" +
        "<h4 style=\"margin:14px 0 8px;font-size:0.9rem;color:#0f172a\">What the audit shows</h4>" +
        "<ul>" +
        "<li><strong>Age:</strong> Passwords used for a long time without change — easier to compromise over time.</li>" +
        "<li><strong>Reuse:</strong> One leaked password unlocks multiple accounts.</li>" +
        "<li><strong>Length:</strong> Nearly all affected accounts use the 8-character minimum.</li>" +
        "<li><strong>Complexity:</strong> No symbols required; many passwords are simple words or patterns.</li>" +
        "<li><strong>Expiration:</strong> Policy rotation is enabled — expiration itself is not the primary weakness in this breach.</li>" +
        "</ul></li>" +
        "<li><h3>CISO IR addendum — credential exposure summary</h3>" +
        "<p>IR appended this write-up to the leaked bundle (not part of the HR compensation PDF). It states the same themes formally:</p>" +
        "<p><strong style=\"color:#991b1b\">Confirmed — Finding 1 — Credential reuse across services.</strong> " +
        "Employee credentials recovered from the breach were reused on multiple corporate and third-party services. " +
        "A single compromised password therefore placed VPN, email, and timekeeping accounts at concurrent risk.</p>" +
        "<p><strong style=\"color:#991b1b\">Confirmed — Finding 2 — Insufficient length and complexity.</strong> " +
        "Recovered passwords were short and lacked required complexity. Many matched dictionary words or simple patterns and did not include symbols, " +
        "consistent with the eight-character minimum described in directory policy artifacts.</p>" +
        "<p><strong style=\"color:#991b1b\">Confirmed — Finding 3 — Excessive password age.</strong> " +
        "Many affected accounts had not changed passwords in over twelve months despite policy intent. Exemptions and poor hygiene amplified exposure " +
        "relative to accounts rotated on schedule.</p>" +
        "<p><strong style=\"color:#166534\">Not the primary focus — Finding 4 — Password expiration.</strong> " +
        "Ninety-day rotation remains enforced for standard accounts through Active Directory. Missing expiration is not the primary driver of this incident; " +
        "investigators should prioritize age, reuse, length, and complexity.</p></li>" +
        "<li><h3>Containment options under review (IR note)</h3>" +
        "<p>Use this IR note for Step 3 (it is not shown in the in-sim payroll export):</p>" +
        '<pre style="margin:0 0 12px;padding:12px;background:#0f172a;color:#e2e8f0;border-radius:8px;font-size:0.8rem;line-height:1.45;white-space:pre-wrap">CIO requirement: Protect employee accounts going forward WITHOUT wiping kiosk\nimages that may hold forensic evidence.\n\nPIN code .............. Weak factor; may be cached or typed on a compromised host.\nSMS authentication .... Interceptable; SMS logs may remain on the device.\nOTP token ............. Codes still entered on the host; some apps log OTP material.\nFIDO security key ..... Hardware-bound, phishing-resistant; proves possession\n                        without sending secrets through the compromised workstation.</pre></li>' +
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

(function () {
  "use strict";

  var KEY = "secplusPractice";
  var BANK_SIZE = 100;
  var TOPIC_MAP_URL = "/COMP_TIA_SEC+/data/secplus-question-topic-map.json";
  var QUESTIONS_BASE = "/COMP_TIA_SEC+/SEC+_Questions/";

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

  window.SECPLUS_PRACTICE = window.SECPLUS_PRACTICE || {};
  window.SECPLUS_PRACTICE.SLUGS = [
    "pentest-hypervisor-vm-escape",
    "public-download-code-signing-integrity",
    "mdm-mitigate-jailbreaking-mobile",
    "authorized-before-authenticated-tailgating",
    "kiosk-dns-poisoning-hourly-credentials",
    "cloud-international-data-protection-regulations",
    "reset-local-passwords-pass-the-hash",
    "credential-harvesting-social-engineering",
    "network-segmentation-security-zones-advantage",
    "dlp-classify-data-before-policies",
    "iot-exploit-firewall-logs-first",
    "ai-ticketing-tool-intellectual-property",
    "aaa-accounting-login-time-tracking",
    "low-cost-standby-warm-site-hardware",
    "right-to-be-forgotten-remove-data",
    "unpatched-app-segmentation-mitigation",
    "wifi-iot-sensors-vlan-segmentation",
    "compensating-controls-alternative-measure",
    "download-integrity-verify-hashes",
    "data-lifecycle-retention-regulations",
    "decommission-device-encryption-updates",
    "uat-production-data-masking",
    "equipment-aro-ten-incidents-five-years",
    "multicloud-iaas-vm-resilience",
    "soc-failed-logins-password-spraying",
    "os-image-baseline-configuration-first",
    "zero-trust-policy-engine-access",
    "design-change-management-review",
    "developer-code-signing-application-integrity",
    "lost-mobile-device-fde",
    "joint-development-ip-moa-breach",
    "password-hashing-mathematical-algorithms",
    "legacy-gas-pipeline-scada",
    "critical-system-patch-least-privilege",
    "client-sla-service-time-resources",
    "admin-access-bastion-host",
    "dba-jump-server-database-segment",
    "security-awareness-policies-handbooks-first",
    "bulk-account-creation-orchestration",
    "data-retention-custodian-role",
    "incident-identified-containment-next",
    "remote-access-ipsec-radius-aaa",
    "vpn-mfa-password-token-thumbprint",
    "insider-threat-behavioral-analytics",
    "sideloading-rootkit-threat",
    "linux-shadow-permissions-chmod",
    "certificate-expired-status-crl",
    "pentest-local-credential-reuse-centralized-auth",
    "dr-plan-hot-site-immediate-operations",
    "web-form-regex-input-validation",
    "shared-backup-account-pam-sso-failure",
    "unauthorized-app-install-sideloading",
    "remote-auth-time-based-tokens",
    "staging-subset-customer-data-upgrades",
    "maximum-accepted-risk-threshold",
    "reported-phish-not-tuning-filters",
    "os-vulnerability-system-wide-access",
    "bia-rto-downtime-tolerance",
    "accounting-login-watering-hole-download",
    "risk-analysis-likelihood-exploitation",
    "incident-response-lessons-learned-reports",
    "dr-strategy-warm-quick-low-cost",
    "certificate-presented-ocsp-validation",
    "hr-fileshare-least-privilege-confidentiality",
    "email-malicious-attachments-inline-scan",
    "vuln-remediation-rescan-network",
    "unauthorized-devices-nac-8021x-posture",
    "new-email-servers-update-spf",
    "pci-dss-failure-fines",
    "zero-day-bastion-compensating-control",
    "pentest-rules-of-engagement",
    "automate-account-permissions-user-provisioning",
    "legacy-device-end-of-support-decommission",
    "technical-security-control-firewall",
    "rogue-device-mac-cloning-audit",
    "decommission-data-retention-secure-destruction",
    "payroll-text-smishing-impersonation",
    "batch-job-memory-injection-outbound-traffic",
    "stakeholders-tabletop-exercise-roles",
    "replace-expired-ssl-certificate-csr",
    "unexpected-characters-sql-injection",
    "inbound-smb-rdp-honeynet-vlan",
    "annual-risk-assessment-recurring",
    "server-cluster-load-balancer-traffic",
    "extended-power-failure-generator",
    "automate-infrastructure-deployment-iac",
    "unauthorized-disclosure-confidentiality",
    "mobile-policy-company-owned-cobo",
    "shared-files-malware-rat-infection",
    "iot-smart-lighting-segmentation-credentials",
    "vulnerability-risk-asset-inventory",
    "security-awareness-curriculum-threat-cadence",
    "mac-table-flood-port-security",
    "hips-preventive-detective-controls",
    "injection-attacks-input-validation",
    "tablets-missing-features-mdm",
    "security-governance-roles-responsibilities",
    "vulnerability-assessment-risk-false-positives",
    "visitor-vestibule-physical-security-control",
    "inbound-firewall-deny-malicious-ip",
    "spreadsheet-credentials-honeytoken",
    "air-gapped-firmware-manual-updates",
    "image-backup-full-system-recovery",
    "change-management-unauthorized-modifications",
    "insider-threat-decoy-salaries-file",
    "ir-stop-spread-containment-first",
    "classified-defense-espionage-motivation",
    "phishing-sim-report-suspicious-email",
    "hardware-vulnerability-firmware-version",
    "employee-pii-privacy-data-classification",
    "mssp-firewall-benchmark-config-template",
    "memory-injection-running-process-example",
    "daily-vuln-scans-patch-status",
    "typosquatting-url-impersonation",
    "wifi-wpa3-heat-map-site-survey",
    "physically-isolate-secure-systems-air-gapped",
    "web-logs-directory-traversal-etc-passwd",
    "lost-decryption-key-escrow-recovery",
    "dr-plan-cold-site-minimum-cost",
    "post-incident-review-root-cause",
    "external-attacks-nips-protection",
    "mdm-lost-phone-screen-lock-remote-wipe",
    "international-expansion-on-premises-security",
    "containers-reduce-os-patching",
    "saas-soc2-report-due-diligence",
    "zero-trust-continuous-validation",
    "web-server-go-live-harden-virtual-host",
    "ip-camera-live-stream-srtp",
    "revise-change-management-cloud-updates",
    "automate-data-sharing-api",
    "radius-server-aaa-authentication",
    "service-provider-baseline-enforcement-scale",
    "firewall-fail-closed-confidentiality-priority",
    "fde-workstations-data-at-rest",
    "next-gen-siem-automated-response",
    "internet-facing-app-bug-bounty-program",
    "wwww-domain-typosquatting-attack",
    "tabletop-exercise-update-irp",
    "rainbow-table-salting-defense",
    "siem-logs-correlation-multiple-hosts",
    "ryk-extension-ransomware-infection",
    "failed-change-backout-plan",
    "vulnerability-management-reporting-prioritization",
    "unknown-patch-fim-rootkit",
    "risk-avoidance-different-market-segment",
    "file-label-data-classification",
    "security-awareness-phishing-campaign",
    "decommission-drive-sanitization-recycling",
    "osint-public-breach-information",
    "physical-security-tailgating-situational-awareness",
    "donate-network-hardware-sanitization",
    "national-id-dlp-accidental-disclosure",
    "data-sanitization-used-hard-drives",
    "multiple-log-types-siem-management",
    "input-field-sql-injection-data-manipulation",
    "bulk-unsolicited-messages-phishing",
    "repeatable-sanitization-reuse-hard-drives",
    "ceo-gift-card-smishing-attack",
    "private-cloud-sensitive-data-ipsec",
    "iac-configuration-managed-replicated",
    "bc-staff-capacity-planning",
    "reissue-laptop-retention-sanitization",
    "team-folder-access-role-based-group",
    "harden-end-user-devices-fde-epp",
    "phishing-link-malware-awareness-training",
    "payroll-insider-manipulation-detective-control",
    "block-unknown-programs-application-allow-list",
    "on-premises-access-swipe-biometric",
    "tcp-445-high-traffic-worm-root-cause",
    "cmd-exe-fim-hash-change-rootkit",
    "incident-cost-sle-risk-quantification",
    "container-image-hardening-production",
    "windows-4625-bruteforce-admin-log",
    "supply-chain-servers-acquisition-process",
    "inadvertent-malware-application-allow-list",
    "sdlc-policy-peer-review-requirements",
    "data-sovereignty-global-regulations",
    "research-laws-regulations-due-diligence",
    "incident-frequency-aro-definition",
    "insider-records-permission-restrictions",
    "power-failure-resiliency-production-failover",
    "fingerprinted-files-email-dlp",
    "resigned-batch-jobs-job-rotation",
    "tabletop-exercise-ir-familiarization",
    "counterfeit-hardware-supply-chain-analysis",
    "zero-trust-validate-traffic-between-systems",
    "school-arp-poisoning-unskilled-attacker",
    "phishing-lateral-ransomware-ips-spread",
    "aggregate-logs-alerts-siem",
    "insurance-policy-risk-transfer",
    "wpa2-enterprise-radius-8021x-directory",
    "data-sovereignty-at-rest-cross-border",
    "sdlc-penetration-testing-methodology",
    "industry-blog-watering-hole-malware",
    "honeypot-analyze-attacker-techniques",
    "pentest-partially-known-environment-device",
    "endpoint-management-unauthorized-changes",
    "mfa-patch-preventative-technical-controls",
    "consultant-remote-access-ipsec",
    "banned-vendor-hardware-refresh-sanctions",
    "cloud-iot-management-encrypted-connection",
    "vpn-login-impossible-travel-indicator",
    "ips-active-mode-signature-blocking",
    "c2-exfiltration-packet-capture-forensics",
    "web-server-tls-public-key-certificate",
    "payment-site-email-phishing-credentials",
    "vm-escape-hypervisor-compromise-other-vms",
    "pentest-database-input-validation-sqli",
    "cold-site-insufficient-capacity-planning",
    "software-release-hashing-integrity",
    "secure-baseline-establish-deploy-maintain",
    "hardware-repair-mean-time-to-repair",
    "pentest-unknown-environment-external-attack",
    "ssl-certificate-not-trusted-root-ca",
    "host-isolation-network-resource-inaccessible",
    "lobby-jack-port-security-visitor",
    "university-two-cloud-platform-diversity",
    "code-deployment-serverless-architecture",
    "web-app-auth-weakness-dynamic-analysis",
    "hard-drive-wipe-tool-repurpose",
    "admin-phishing-email-server-password",
    "sql-log-or-1-equals-1-injection",
    "layoffs-disgruntled-employee-supervisor-training",
    "suspicious-email-file-sandbox-analysis",
    "risk-assessment-osint-no-proprietary-info",
    "mfa-token-bypass-pretexting-attack",
    "lost-mobile-device-mdm-prevent-data-loss",
    "data-classification-most-impacted-when-lost",
    "web-app-vulnerability-no-patch-zero-day",
    "iaas-enclave-csp-responsibility-matrix",
    "unsupported-critical-system-risk-accept",
    "encrypt-data-algorithms-key-length",
    "production-patch-change-control-first",
    "bank-vendor-stolen-laptop-encryption-at-rest",
    "iam-shift-access-time-of-day-restrictions",
    "change-management-board-approved-update",
    "database-encrypted-insider-threat-domain-user",
    "high-risk-region-ip-geolocation-mitigation",
    "login-script-baseline-enforcement",
    "supply-chain-provider-privileged-access-target",
    "database-misconfiguration-sql-injection",
    "domain-admin-audit-remove-rotate-passwords",
    "alert-fatigue-false-positive-ignored",
    "ha-network-recovery-responsiveness",
    "internal-audit-control-gaps-remediation",
    "network-device-hardening-telnet-to-ssh",
    "asset-tracking-unauthorized-devices",
    "byod-mdm-approved-applications-only",
    "risk-ale-15000-twice-in-three-years",
    "file-server-slow-resource-consumption-alert",
    "mou-vs-sow-legally-binding",
    "server-hardening-disable-accounts-services",
    "sql-update-temp-field-race-condition",
    "phishing-incentive-gamification-awareness",
    "iaas-database-security-client-responsibility",
    "powershell-ioc-edr-logs-investigation",
    "bia-backup-schedule-rpo",
    "removable-media-malware-awareness-training",
    "new-regulation-gap-analysis-next",
    "dlp-dns-filtering-email-web-protection",
    "soc-soar-reduce-manual-analyst-work",
    "data-in-transit-tls-13-protection",
    "remote-to-office-recurring-training-awareness",
    "waf-policies-iac-automatic-deployment",
    "sqli-forensics-application-log-threat-command",
    "nac-platform-wired-attack-surface",
    "vendor-diversity-zero-day-resiliency-benefit",
    "executive-boardroom-tabletop-incident-response",
    "controls-assurance-independent-audit-report",
    "ids-database-login-credential-replay-attack",
    "aup-managerial-control-type",
    "saas-separate-logins-idp-federation-remediation",
    "drp-critical-systems-restore-order-outage",
    "legacy-critical-app-mitigate-missing-preventive-controls",
    "customer-data-role-subject-marketing-custodian",
    "application-availability-load-balancing-replace-server",
    "web-log-useragent-command-injection-input-sanitization",
    "financial-industry-tokenization-mask-sensitive-data",
    "soar-reduce-steps-identify-contain-threats",
    "digital-forensics-preservation-evidence-integrity",
    "compensating-control-high-risk-website-firewall-threat-prevention",
    "cvss-prioritize-vulnerability-remediation",
    "ddos-protection-availability-security-concept",
    "financial-cloud-homomorphic-encrypted-processing",
    "reduce-enterprise-attack-surface-disable-unused-services",
    "accounting-fake-vendor-invoice-scam",
    "global-privacy-compliance-dpa-third-party-vendors",
    "full-disk-encryption-confidentiality-concept",
    "hr-onboarding-phish-social-engineering-attack-vector",
    "visitor-badge-endpoint-concurrent-session-alert",
    "ransomware-usb-recovery-sandboxing-environment",
    "ir-containment-phase-minimize-disruption",
    "merger-align-security-programs-nist-csf",
    "ceo-smishing-gift-card-training-warning",
    "malicious-file-signature-static-analysis",
    "malware-desktops-first-step-contain-hosts",
    "data-exfiltration-firewall-network-logs-investigation",
    "certificate-internal-source-self-signed",
    "ics-proprietary-controls-harsh-environment",
    "tabletop-generator-failure-bia-risk-management",
    "foreign-callers-company-numbers-weak-sip-security",
    "attorney-copier-ldap-secure-print-prevention",
    "raas-threat-actor-organized-crime-ciso-report",
    "marketing-email-spf-next-dkim",
    "quarantine-infected-system-air-gapped",
    "standardize-server-builds-infrastructure-as-code",
    "ciso-compliance-tracking-internal-auditing",
    "unusual-dns-queries-non-business-hours-exfiltration",
    "siem-automation-orchestration-workforce-multiplier",
    "tokenization-strategy-surrogate-values",
    "unencrypted-plc-management-traffic-scada",
    "dr-site-geographic-dispersion-natural-disaster-backups",
    "sideloading-unapproved-software-repository",
    "remote-work-no-vpn-secure-web-gateway",
    "bank-pii-server-file-integrity-monitoring",
    "data-modified-in-transit-hashing-integrity",
    "traveling-employees-endpoint-hips-protection",
    "new-tactic-no-siem-alerts-threat-hunting",
    "foreign-government-hires-organized-crime-critical-systems",
    "vulnerability-prioritization-focus-cvss",
    "guest-quarantine-mdm-compliance-attestation",
    "network-auth-8021x-certificate-nac-quarantine",
    "file-integrity-confirmation-hashing-strategy",
    "operational-changes-scheduled-downtime-window",
    "bia-process-estimate-system-recovery-time",
    "saas-purchase-review-third-party-audit",
    "osint-social-engineering-testing-activity",
    "firewall-fail-open-availability-priority-website",
    "aup-preventive-security-control-type",
    "xss-insert-scripts-control-client-browser",
    "low-cost-cloud-app-hosting-serverless",
    "saas-firewall-ports-supply-chain-vendor-risk",
    "daily-server-security-settings-automation-check",
    "track-vm-build-code-version-control",
    "compromising-photos-blackmail-threat-intent",
    "router-mgmt-ip-restrict-preventive-control",
    "legacy-iot-vulnerability-segmentation-mitigate",
    "login-rejected-spring2023-password-spraying",
    "employees-frequent-site-watering-hole-attack",
    "avoid-bloatware-application-allow-list",
    "log-script-tag-xss-vulnerability",
    "internal-endpoint-connections-host-based-firewall",
    "critical-patch-asset-inventory-systems",
    "incident-response-first-stage-detection",
    "decommissioned-laptops-data-wiping",
    "detect-fraud-job-rotation-different-roles",
    "encrypted-outbound-endpoint-logs-investigation",
    "billing-system-fraudulent-checks-application-logs",
    "saas-domain-credentials-single-sign-on",
    "decoy-vulnerable-infrastructure-honeypot-reconnaissance",
    "third-party-contract-end-data-retention-liability",
    "vendor-email-compromise-awareness-familiar-addresses",
    "phishing-false-positives-awareness-training",
    "web-filter-block-http-unencrypted-urls",
    "critical-systems-air-gapped-remote-access-isolation",
    "cfo-vendor-friend-conflict-of-interest",
    "osint-public-platforms-security-exposures",
    "team-file-permissions-access-control-list",
    "outbound-dns-acl-single-resolver-10-50-10-25",
    "firewall-open-ports-attack-surface-principle",
    "contractor-access-expansion-risk-appetite",
    "hacktivist-vs-insider-threat-distinction",
    "vendor-bank-change-business-email-compromise",
    "marketing-unsanctioned-software-shadow-it",
    "printing-center-hygiene-dumpster-diving",
    "banking-audit-regulatory-requirement",
    "authorized-devices-access-lists-admission",
    "site-recovery-resource-group-rbac",
    "cspm-misconfigurations-soar-workflows",
    "web-server-vulnerability-patching",
    "dr-site-validate-simulated-failover",
    "admin-credential-guessing-user-activity-logs",
    "file-server-confidential-data-acl-restrict",
    "mssp-alerts-automated-ticket-creation-itsm",
    "help-desk-admin-console-least-privilege",
    "datacenter-attack-surface-upgrade-eol-os",
    "after-hours-remote-data-copy-insider-threat",
    "off-premises-migration-cloud-provider-security-first",
    "preventive-physical-security-bollards",
    "pentest-badge-unauthorized-area-physical",
    "remote-access-vpn-agent-ipsec-tunnel",
    "need-to-know-roles-confidentiality",
    "open-service-ports-attack-surface-exposure",
    "secure-zone-policy-zero-trust",
    "email-digital-signature-non-repudiation",
    "saas-multiple-logins-select-idp-first",
    "unrelated-sensitive-projects-uba-detection",
    "pci-dss-noncompliance-customer-reputational-damage",
    "incident-response-final-step-lessons-learned",
    "ceo-phish-ransomware-awareness-training-prevention",
    "eol-hardware-vendor-patches-vulnerability",
    "browser-exploit-signatures-ips-block",
    "av-false-positives-heuristic-edr-replacement",
    "encryption-key-multiple-entities-key-escrow",
    "cloud-breach-sensitivity-data-classification",
    "manufacturing-legacy-embedded-systems-pentest",
    "ceo-email-financial-info-bec-attack-vector",
    "certificate-management-misconfiguration-vulnerability",
    "laptop-web-filtering-agent-based-remote",
    "legacy-server-critical-app-segmentation",
    "firewall-rules-change-management-procedure",
    "insider-malicious-code-peer-review-approval",
    "smartphone-unauthorized-software-jailbreaking",
    "caller-id-spoof-credit-card-vishing",
    "ir-documentation-next-tabletop-exercise",
    "ransomware-recovery-offline-backup-rpo-rto",
    "vdi-file-copy-time-based-access-control",
    "encryption-vs-hashing-ciphertext-checksum",
    "remote-connection-confidentiality-vpn",
    "government-noncompliance-sanctions-concern",
    "soc-just-in-time-playbook-reference",
    "compliance-segmentation-firewall-block-external",
    "intellectual-property-awareness-insider-threat",
    "unauthorized-website-aup-violation",
    "regulatory-audit-gap-analysis-self-assessment",
    "sso-access-tokens-oauth-authorization",
    "recovery-site-warm-no-immediate-failover",
    "vendor-installer-hash-integrity-verification",
    "microsegmentation-software-defined-networking",
    "mfa-push-notifications-byod-seamless",
    "network-traffic-transit-tls-encrypted-protocols",
    "patch-update-secure-baseline-sop",
    "application-out-of-scope-management-attestation",
    "remote-malicious-urls-sase-inline-filtering",
    "government-project-data-confidential-restricted",
    "risk-transfer-cost-vs-impact-ale",
    "suspicious-ip-logins-mfa-prevention",
    "soc-benign-activity-alert-tuning",
    "database-trap-user-honeytoken",
    "privacy-compliance-data-protection-policies-first",
    "two-companies-secure-connectivity-vpn",
    "retail-site-miscategorized-gambling-content-filter",
    "shredded-devices-legal-backup-data-retention",
    "classified-sensitive-data-exfiltration-dlp",
    "cope-mdm-policy-remote-wipe-encryption",
    "cloud-responsibility-matrix-customer-data",
    "database-access-hardening-jump-server-hbf",
    "cloud-hosting-virtualization-isolation-resources",
    "sms-otp-riskier-than-totp-interception",
    "login-database-breach-impact-password-hashing",
    "dpo-data-inventory-breach-impact",
    "environmental-variables-vulnerability-scope-impact",
    "server-replacement-cost-quantitative-risk-analysis",
    "cloud-adoption-saas-vendor-patching",
    "xss-vulnerability-input-validation-remediation",
    "automation-script-knowledge-single-point-failure",
    "social-engineering-training-phishing-campaign-test",
    "one-way-transform-salting-complexity",
    "sqli-breach-input-sanitization-developers",
    "byod-primary-concern-jailbreaking",
    "insider-pii-misuse-privacy-legislation-training",
    "c2-investigation-endpoint-logs-deleted-firewall",
    "sql-credit-card-pending-purchases-tokenization",
    "network-share-deletions-permissions-fim",
    "open-source-libraries-zero-day-remediation",
    "legacy-system-firewall-compensating-controls",
    "cloud-logging-monitoring-siem",
    "exploit-undetected-os-memory-injection",
    "malicious-video-file-metadata-forensics",
    "after-login-granting-access-authorization",
    "outdated-algorithms-keys-cryptographic-vulnerability",
    "telnet-scan-false-positive-encryption-verified",
    "credit-card-last-four-masking",
    "ir-preparation-roles-responsibilities",
    "jsmith-domain-mfa-brute-force-log",
    "directive-managerial-control-aup",
    "dev-team-corporate-policy-internal-noncompliance",
    "sqli-web-logs-check-users-table-first",
    "epp-false-positive-download-misconfiguration",
    "zero-day-mission-critical-compensating-controls",
    "web-filter-malicious-links-categorization-review",
    "departing-employees-customer-data-uba",
    "rush-deploy-insufficient-due-diligence-risk-acceptance",
    "air-gapped-network-data-loss-removable-devices",
    "manual-account-errors-user-provisioning-script",
    "sla-response-time-escalation-performance-metrics",
    "same-password-different-hashes-salting",
    "ir-understand-incident-source-analysis",
    "xss-web-server-compromise-waf-prevention",
    "hq-branch-vpn-data-in-transit",
    "malicious-insider-risk-uba",
    "multi-provider-email-spf-authorized-senders",
    "always-on-vpn-fail-host-content-filtering",
    "secure-data-track-changes-fim",
    "wifi-filter-bypass-rogue-access-point",
    "fake-credentials-document-honeyfile",
    "forensic-evidence-handling-chain-of-custody",
    "ciso-ignores-vulnerabilities-risk-accept",
    "offensive-assessment-pen-test-red-team",
    "public-rdp-vpn-jump-server-firewall",
    "decrease-hardware-attack-surface-virtualization",
    "contract-employees-gpo-logon-hours",
    "datacenter-safety-controls-fail-open",
    "secure-data-in-transit-encryption",
    "eol-business-critical-system-isolation",
    "inbound-malicious-traffic-ips-automated-block",
    "bec-gift-card-executive-display-name",
    "nation-state-financial-resources-critical-systems-abroad",
    "two-person-integrity-process-security-control",
    "dns-server-reflected-dos-inbound-flood",
    "wlan-lobby-channel-overlap-high-power",
    "customer-data-network-segmentation-corporate",
    "secure-coding-training-customer-attestation",
    "external-network-testing-third-party-attestation",
    "stolen-website-private-key-update-crl",
    "tokenization-credit-card-customer-storage",
    "effective-change-management-backout-plan",
    "saas-legal-docs-geolocation-policy-high-risk",
    "regulatory-audit-failure-fines-non-compliance",
    "newly-deployed-server-first-step-update-software",
    "controlled-software-version-release-change-management",
    "high-school-unvetted-simulation-shadow-it",
    "board-quarterly-incident-report-dashboard",
    "jump-server-layer-internal-resource-access",
    "vulnerability-list-first-automated-scanning",
    "verify-data-not-modified-hash-algorithm",
    "cloud-easy-deployment-infrastructure-as-code",
    "weather-server-room-geographic-dispersion",
    "failed-drive-downtime-estimate-mttr",
    "limited-resources-communications-ecc",
    "incident-response-evidence-chain-of-custody",
    "vm-escape-access-adjacent-hosts",
    "vendor-compliance-objectives-attestation-letter",
    "phishing-click-impact-edr-block-execution",
    "right-to-be-forgotten-noncompliance-fines",
    "sensitive-data-at-rest-encryption-unreadable",
    "cfo-credit-card-phone-executive-whaling",
    "provider-97-percent-uptime-sla",
    "wireless-ap-count-site-survey",
    "employee-laptops-encrypt-all-data-fde",
    "rd-department-bypass-vpn-shadow-it",
    "pentest-passive-recon-osint",
    "verify-software-from-vendor-code-signature",
    "datacenter-insider-intrusion-access-badge",
    "malware-download-alert-sandbox-analysis",
    "remote-workforce-vpn-firewall-sase",
    "found-usb-parking-lot-security-team",
    "vuln-remediation-prioritize-risk-tolerance",
    "technical-security-task-procedure-document",
    "privacy-delete-user-data-right-to-be-forgotten",
    "malware-data-movement-monitor-outbound-traffic",
    "stolen-laptop-mdm-force-security-config",
    "music-group-website-defacement-unskilled-attacker",
    "data-privacy-program-controller-processor-role",
    "database-active-processing-data-in-use",
    "pentest-download-website-passive-recon",
    "cyber-insurance-ransomware-coverage-aro",
    "soc-improve-incident-response-playbooks",
    "ir-team-compromised-systems-edr-tool",
    "fido2-passkeys-biometrics-single-auth",
    "offsite-employees-remote-access-vpn",
    "legacy-critical-system-single-point-of-failure",
    "scap-benefit-security-tool-interoperability",
    "forensic-preserve-data-order-of-volatility",
    "evil-twin-insecure-network-attack",
    "risk-management-scope-risk-identification",
    "password-audit-policy-length-complexity",
    "ceo-gift-card-phone-impersonation",
    "onboarding-intranet-federation-password-complexity",
    "email-link-csrf-password-changed",
    "anomaly-detection-first-step-baseline",
    "auditor-risk-management-policies-first",
    "vulnerability-criticality-cvss-score",
    "soar-playbooks-reduce-false-positive-review",
    "identify-legacy-systems-vulnerability-scan",
    "phone-port-laptop-scan-prevent-segmentation",
    "updated-systems-prevent-known-exploits",
    "unapproved-software-vulnerabilities-shadow-it",
    "prevent-reverse-engineering-obfuscation-toolkit",
    "c2-destination-identify-firewall-logs",
    "register-overwrite-malicious-address-buffer-overflow",
    "legacy-plaintext-third-party-compensating-controls",
    "data-at-rest-most-secure-aes-256",
    "classified-storage-disposal-vendor-certification",
    "duplicate-email-site-phishing",
    "pentest-port-scans-active-reconnaissance",
    "secure-zone-access-policy-reduce-threat-scope-zero-trust",
    "improve-incident-response-tabletop-exercise",
    "corrective-controls-interconnected-financial-systems-errors",
    "legacy-ftp-financial-data-compensating-control-ssh-tunnel",
    "fde-laptop-planning-key-escrow-tpm",
    "logic-bomb-internal-app-trusted-insider",
    "cloud-migration-limited-it-resources-sase",
    "hypervisor-unauthorized-access-vm-escape",
    "rnd-data-type-intellectual-property",
    "ciso-noncompliance-board-budget-fines",
    "global-incident-plan-business-continuity",
    "cloud-instance-vulnerability-priority-vm-escape",
    "message-attribution-non-repudiation",
    "log-correlation-definition-patterns",
    "cloud-native-redundancy-critical-business-processes",
    "corrective-controls-financial-system-regulatory-requirement",
    "virtualization-reduce-physical-servers",
    "shadow-it-cloud-first-inline-casb",
    "kiosk-eol-os-patch-availability",
    "msa-general-terms-yearly-engagements",
    "load-balancer-virtual-servers-performance-availability",
    "pentest-sow-hours-estimate",
    "pentest-osint-passive-reconnaissance",
    "spoofed-website-blocked-page-awareness-training",
    "spoofed-certificate-identity-private-key-self-signed",
    "mdm-prevent-jailbreaking-os-changes",
    "vpn-secure-remote-access-minimize-exposure",
    "firewall-fail-open-traffic-bypass-inspection",
    "automation-disable-access-employee-departure",
    "cameras-recording-signs-deterrent-detective",
    "c2-incident-network-firewall-logs-impacted-host",
    "pentest-xss-form-field-input-validation",
    "bios-update-security-bulletin-firmware",
    "vpn-scaling-remote-work-sase-solution",
    "wire-transfer-process-update-vishing-prevention",
    "eol-os-critical-system-isolated-vlan",
    "risk-register-risks-owners-thresholds",
    "data-sovereignty-stored-outside-origin-laws",
    "root-cause-analysis-prevent-future-incidents",
    "regular-patching-mitigate-known-vulnerabilities",
    "availability-incidents-mtbf-technology-investment",
    "hospital-patient-data-sensitive-classification",
    "system-level-data-changes-fim-prevention",
    "repeated-attacks-firewall-only-add-ips",
    "full-disk-encryption-data-at-rest-crypto",
    "deployed-application-runtime-dynamic-analysis",
    "malicious-web-requests-waf-prevention",
    "false-negative-vulnerability-scan-report",
    "tokenization-reference-values-protect-sensitive-data",
    "cybersecurity-readiness-tabletop-exercise",
    "ticketing-automation-incident-escalation",
    "purple-team-offensive-defensive-testing",
    "buffer-overflow-website-waf-protection",
    "ransomware-log-review-detective-control",
    "health-emergency-reporting-app-availability",
    "malicious-software-update-supply-chain",
    "prevent-internet-access-air-gapped",
    "malicious-download-link-edr-prevention",
    "single-public-ip-ipsec-vpn-remote-access",
    "server-hardening-secure-configuration-guide",
    "mfp-unattended-documents-authentication-print-release",
    "hardcoded-credentials-static-analysis-sdlc",
    "secure-network-no-external-communication-air-gap",
    "constantly-changing-environments-containers",
    "vpn-appliance-default-password-prevention",
    "offshore-finance-team-vdi-company-data",
    "siem-investigation-executable-endpoint-logs",
    "router-firmware-upgrade-maintenance-window",
    "vendor-secure-file-transfer-ssh-sftp",
    "unsupported-app-server-air-gap-network-threats",
    "device-communications-host-based-firewall",
    "phishing-credentials-exposed-lock-account",
    "employee-departure-restrictions-nda",
    "customer-transactions-archive-retention-policy",
    "file-transfer-integrity-verify-hashing",
    "new-network-devices-change-default-passwords",
    "ha-website-bug-bounty-find-issues",
    "bank-cold-storage-destruction-certification",
    "production-vm-os-update-snapshot-first",
    "pentest-procedures-rules-of-engagement",
    "edr-technical-security-category",
    "mfa-setup-authentication-tokens-biometrics",
    "javascript-injection-waf-remove-payment-data",
    "unused-social-media-terminate-account",
    "hacktivist-motivation-philosophical-beliefs",
    "legacy-linux-host-firewall-compensating-control",
    "contractor-test-environment-jump-server",
    "forensic-images-acquisition-stage",
    "pii-protection-dlp-classification-labels",
    "microservices-scalability-compartmentalization",
    "customers-security-controls-third-party-attestation",
    "firewall-deny-any-test-non-production",
    "hardware-memory-encryption-data-in-use",
    "legal-requests-investigation-e-discovery",
    "aup-integrity-ethical-behavior-expectations",
    "reduce-investigation-storage-packet-capture-retention",
    "employee-workstation-preapproved-list-cyod",
    "database-data-at-rest-tokenization",
    "insider-exfiltration-removable-devices",
    "pass-the-hash-domain-admin-pam-prevention",
    "system-failure-restore-process-drp",
    "security-project-cost-timeline-sow",
    "phishing-link-click-network-logs-connection",
    "enterprise-password-policy-gpo-push",
    "rtos-compromise-memory-injection",
    "siem-receives-logs-presents-alerts",
    "ciso-policies-external-regulators-examination",
    "conceal-code-text-graphical-image-steganography",
    "tune-file-permissions-access-control-list",
    "pentest-vendor-red-team-partially-known",
    "ongoing-vendor-monitoring-security-assessments",
    "ransomware-recovery-backup-immutability",
    "manual-url-different-site-typosquatting",
    "ransomware-license-cost-decision-ale",
    "pentest-guidance-attack-surface-reduction",
    "legacy-production-vendor-support-security-concern",
    "customer-web-portal-waf-protection",
    "siem-alert-detective-control-type",
    "saas-no-onprem-accessible-anywhere",
    "firewall-assessment-custom-packets-hping",
    "webshop-logic-bomb-waf-command-injection-logs",
    "bug-bounty-benefits-zero-day-quicker-discovery",
    "cloud-credential-leakage-code-repositories",
    "breach-lawsuit-legal-hold-communications",
    "edr-malware-lateral-movement-protection",
    "zero-trust-data-plane-secured-zones",
    "dlp-prerequisite-data-classification",
    "security-program-system-operation-aup",
    "no-alerts-lurking-actors-threat-hunting",
    "awareness-program-report-phishing-communication",
    "secure-facility-badge-access-vestibule",
    "password-random-string-salting",
    "sqli-monitoring-ssl-decrypt-full-packet-capture",
    "cloud-vendor-tool-saml-corporate-directory",
    "hr-contract-revisions-version-control",
    "router-hardening-disable-web-administration",
    "smbv1-remediation-gpo-disable",
    "vendor-left-architecture-file-proprietary-data",
    "phishing-memory-scrape-pass-the-hash-lateral",
    "accountant-ftp-bank-encryption-confidentiality",
    "laptop-asset-stickers-employee-id-benefits",
    "dark-web-proprietary-data-notify-applicable-parties",
    "hr-remote-laptop-layoffs-opsec-policy",
    "log-live-storage-90-days-compression",
    "security-director-prioritize-patching-cvss",
    "gpo-deployment-workstation-misconfiguration-vulnerabilities",
    "web-logs-databaseinfo-directory-traversal",
    "scap-automate-vulnerability-management",
    "container-security-limited-by-monolithic-code",
    "backup-datacenter-rto-rpo-two-days-cold-site"
  ];

  window.SECPLUS_PRACTICE._topicAssignments = null;
  window.SECPLUS_PRACTICE._topicAssignmentsPromise = fetch(TOPIC_MAP_URL, { credentials: "same-origin" })
    .then(function (res) {
      if (!res.ok) throw new Error("topic map http " + res.status);
      return res.json();
    })
    .then(function (data) {
      var a = data && data.assignments;
      window.SECPLUS_PRACTICE._topicAssignments = a && typeof a === "object" ? a : {};
      return window.SECPLUS_PRACTICE._topicAssignments;
    })
    .catch(function () {
      window.SECPLUS_PRACTICE._topicAssignments = false;
      return false;
    });

  function objectivesForSlug(assignments, slug) {
    if (!assignments || !slug) return null;
    return assignments[slug + ".html"] || null;
  }

  function slugMatchesMajor(assignments, slug, major) {
    var objs = objectivesForSlug(assignments, slug);
    if (!objs || !objs.length) return false;
    var want = String(major);
    for (var i = 0; i < objs.length; i++) {
      var maj = String(objs[i]).split(".")[0];
      if (maj === want) return true;
    }
    return false;
  }

  function filterSlugsByMajor(slugs, assignments, major) {
    if (!major) return slugs.slice();
    if (!assignments || typeof assignments !== "object") return [];
    var out = [];
    for (var i = 0; i < slugs.length; i++) {
      if (slugMatchesMajor(assignments, slugs[i], major)) out.push(slugs[i]);
    }
    return out;
  }

  function getSelectedPracticeDomain() {
    var sel = document.getElementById("secplus-practice-domain-select");
    if (!sel) return "";
    var v = String(sel.value || "").trim();
    return /^[1-5]$/.test(v) ? v : "";
  }

  function getAdaptiveLearningEnabled() {
    try {
      var r = document.querySelector('input[name="secplus-practice-adaptive"]:checked');
      if (!r) return false;
      return String(r.value || "").trim() === "1";
    } catch (e) {
      return false;
    }
  }

  function bankSlugs(bankId) {
    var all = window.SECPLUS_PRACTICE.SLUGS;
    var n = parseInt(String(bankId), 10);
    if (!n || n < 1) n = 1;
    var start = (n - 1) * BANK_SIZE;
    return all.slice(start, start + BANK_SIZE);
  }

  function practiceBankCount() {
    var all = window.SECPLUS_PRACTICE.SLUGS;
    if (!all || !all.length) return 1;
    return Math.ceil(all.length / BANK_SIZE);
  }

  function portalAccessActive() {
    return (
      typeof window.bccSecplusPortalAccessActive === "function" && window.bccSecplusPortalAccessActive()
    );
  }

  function requirePortalAccess() {
    if (portalAccessActive()) return true;
    window.location.href = "/comptia-sec+-home.html#purchase";
    return false;
  }

  function start(mode, bankId, domainMajor) {
    if (!requirePortalAccess()) return;
    bankId = bankId || "1";
    var fixed = bankSlugs(bankId);
    var map = window.SECPLUS_PRACTICE._topicAssignments;
    if (domainMajor) {
      if (!map || typeof map !== "object") {
        window.alert("Topic assignments are still loading. Try again in a moment.");
        return;
      }
      fixed = filterSlugsByMajor(fixed, map, domainMajor);
    }
    if (!fixed.length) {
      window.alert(
        "No questions in this bank match the selected domain. Pick another subject or choose “All subjects”."
      );
      return;
    }
    var order;
    if (mode === "linear") {
      order = fixed;
    } else {
      order = shuffle(fixed);
    }
    var session = { v: 1, mode: mode, bank: bankId, order: order };
    if (domainMajor) session.domain = domainMajor;
    if (getAdaptiveLearningEnabled()) {
      session.adaptive = true;
      session.adaptiveExtrasInjected = 0;
    }
    try {
      sessionStorage.setItem(KEY, JSON.stringify(session));
    } catch (e) {}
    window.location.href = QUESTIONS_BASE + order[0] + ".html#secplusP=0";
  }

  function startWithOptionalDomain(mode, bankId) {
    var domainMajor = getSelectedPracticeDomain() || null;
    if (!domainMajor) {
      start(mode, bankId, null);
      return;
    }
    var inst = window.SECPLUS_PRACTICE;
    var assign = inst._topicAssignments;
    if (assign === false) {
      window.alert(
        'Could not load the topic map for this site. Use "All subjects" or try again later.'
      );
      return;
    }
    if (assign && typeof assign === "object") {
      start(mode, bankId, domainMajor);
      return;
    }
    inst._topicAssignmentsPromise.then(function () {
      if (inst._topicAssignments === false) {
        window.alert(
          'Could not load the topic map for this site. Use "All subjects" or try again later.'
        );
        return;
      }
      start(mode, bankId, domainMajor);
    });
  }

  window.SECPLUS_PRACTICE.BANK_SIZE = BANK_SIZE;
  window.SECPLUS_PRACTICE.start = start;
  window.SECPLUS_PRACTICE.startWithOptionalDomain = startWithOptionalDomain;
  window.SECPLUS_PRACTICE.bankSlugs = bankSlugs;
  window.SECPLUS_PRACTICE.practiceBankCount = practiceBankCount;
  window.SECPLUS_PRACTICE.filterSlugsByMajor = filterSlugsByMajor;
  window.SECPLUS_PRACTICE.getSelectedPracticeDomain = getSelectedPracticeDomain;

  document.addEventListener(
    "click",
    function (e) {
      var t = e.target;
      if (!t || typeof t.closest !== "function") return;
      var el = t.closest("[data-secplus-practice]");
      if (!el || el.disabled) return;
      var m = el.getAttribute("data-secplus-practice");
      var bank = el.getAttribute("data-secplus-practice-bank") || "1";
      if (m === "random" || m === "review" || m === "linear") {
        e.preventDefault();
        startWithOptionalDomain(m, bank);
      }
    },
    false
  );

  function refreshPortalPracticeBanksSummary(nBanks) {
    var all = window.SECPLUS_PRACTICE.SLUGS;
    var total = Array.isArray(all) ? all.length : 0;
    if (!nBanks || nBanks < 1) nBanks = practiceBankCount();

    function formatRange(first, last) {
      if (first >= last) return String(first);
      return String(first) + "–" + String(last);
    }

    var summary = document.getElementById("secplus-practice-banks-summary");
    if (summary) {
      var lastBankCount = total - (nBanks - 1) * BANK_SIZE;
      var bankWord = nBanks === 1 ? "bank" : "banks";
      var summaryText =
        total +
        " practice question" +
        (total === 1 ? "" : "s") +
        " in " +
        nBanks +
        " " +
        bankWord +
        " (positions 1–100, 101–200, and so on in hub order). ";
      if (lastBankCount > 0 && lastBankCount < BANK_SIZE) {
        summaryText +=
          "The newest bank (positions " +
          formatRange((nBanks - 1) * BANK_SIZE + 1, nBanks * BANK_SIZE) +
          ") has " +
          lastBankCount +
          " question" +
          (lastBankCount === 1 ? "" : "s") +
          " until the list reaches " +
          BANK_SIZE +
          "; then the next bank appears automatically. ";
      }
      summaryText +=
        "Each bank has its own Random and Review session. Use Practice by subject to limit a session to one SY0-701 domain before you start.";
      summary.textContent = summaryText;
      summary.hidden = false;
    }

    var grid = document.getElementById("secplus-practice-banks-grid");
    if (grid) {
      grid.setAttribute(
        "aria-label",
        "Practice question banks: " +
          nBanks +
          " banks of up to " +
          BANK_SIZE +
          " questions each (" +
          total +
          " total)"
      );
    }
  }

  function injectPortalPracticeBanks() {
    var grid = document.getElementById("secplus-practice-banks-grid");
    if (!grid) return;

    var all = window.SECPLUS_PRACTICE.SLUGS;
    var existing = grid.querySelectorAll("[data-secplus-practice-bank-index]");
    if (existing.length) {
      refreshPortalPracticeBanksSummary(existing.length);
      return;
    }

    var loadingEl = document.getElementById("secplus-practice-banks-loading");
    if (loadingEl) loadingEl.remove();

    if (!Array.isArray(all) || !all.length) {
      if (!grid.querySelector("[data-secplus-practice-banks-error]")) {
        var err = document.createElement("p");
        err.className = "study-meta";
        err.setAttribute("data-secplus-practice-banks-error", "1");
        err.setAttribute("role", "status");
        err.textContent =
          "Practice banks could not load. Refresh the page; if the problem continues, check that secplus-practice-hub.js loaded correctly.";
        grid.appendChild(err);
      }
      return;
    }

    var prior = grid.querySelectorAll("[data-secplus-practice-banks-error]");
    for (var pe = 0; pe < prior.length; pe++) prior[pe].remove();

    var nBanks = practiceBankCount();
    var total = all.length;

    function formatRange(first, last) {
      if (first >= last) return String(first);
      return String(first) + "–" + String(last);
    }

    refreshPortalPracticeBanksSummary(nBanks);

    for (var b = 1; b <= nBanks; b++) {
      var startIdx = (b - 1) * BANK_SIZE;
      var endIdx = Math.min(b * BANK_SIZE, all.length);
      var firstNum = startIdx + 1;
      var slotEnd = b * BANK_SIZE;
      var countInBank = endIdx > startIdx ? endIdx - startIdx : 0;

      var article = document.createElement("article");
      article.className = "sim-box";
      article.setAttribute("data-secplus-practice-bank-index", String(b));
      article.setAttribute("aria-labelledby", "secplus-bank-title-" + b);

      var isLastBank = b === nBanks;
      var isPartial = countInBank > 0 && countInBank < BANK_SIZE;
      if (isLastBank && isPartial) {
        article.classList.add("secplus-practice-bank--remainder");
      }

      var h4 = document.createElement("h4");
      h4.className = "sim-box-title";
      h4.id = "secplus-bank-title-" + b;
      var titleInner;
      if (countInBank === 0) {
        titleInner = formatRange(firstNum, slotEnd);
      } else {
        titleInner = formatRange(firstNum, endIdx);
      }
      h4.textContent = "Bank " + String(b) + " · questions " + titleInner;
      article.appendChild(h4);

      var meta = document.createElement("p");
      meta.className = "study-meta";
      meta.textContent =
        countInBank +
        " item" +
        (countInBank === 1 ? "" : "s") +
        " · Random shuffles once; Review sends misses to the back of the queue.";
      article.appendChild(meta);

      var actions = document.createElement("div");
      actions.className = "study-actions";
      actions.setAttribute("role", "group");
      actions.setAttribute("aria-label", "Practice modes for bank " + String(b));

      var br = document.createElement("button");
      br.type = "button";
      br.className = "start-btn";
      br.setAttribute("data-secplus-practice", "random");
      br.setAttribute("data-secplus-practice-bank", String(b));
      br.textContent = "Random";

      var rev = document.createElement("button");
      rev.type = "button";
      rev.className = "start-btn";
      rev.setAttribute("data-secplus-practice", "review");
      rev.setAttribute("data-secplus-practice-bank", String(b));
      rev.textContent = "Review";

      if (countInBank === 0) {
        br.disabled = true;
        rev.disabled = true;
        br.classList.add("is-placeholder");
        rev.classList.add("is-placeholder");
      }

      actions.appendChild(br);
      actions.appendChild(rev);
      article.appendChild(actions);
      grid.appendChild(article);
    }
  }

  window.SECPLUS_PRACTICE.injectPortalPracticeBanks = injectPortalPracticeBanks;

  function schedulePortalPracticeBanks() {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", injectPortalPracticeBanks, { once: true });
    } else {
      injectPortalPracticeBanks();
    }
  }

  schedulePortalPracticeBanks();
  window.addEventListener("pageshow", injectPortalPracticeBanks);
})();

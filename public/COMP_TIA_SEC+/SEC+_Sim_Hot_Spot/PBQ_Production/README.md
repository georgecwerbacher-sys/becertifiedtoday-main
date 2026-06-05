# PBQ_Production

**Active workspace** for new SY0-701 PBQ scenarios before they ship to the public bank.

Answer keys were verified against CompTIA-aligned objectives and primary sources (NIST, RFC, OWASP, OpenSSH). See **[VERIFICATION.md](VERIFICATION.md)** (2026-06-04).

**Adding a new scenario:** follow **[ADD-PBQ.md](ADD-PBQ.md)**.

## Published simulations (`index, follow`)

Legacy `SEC+_Sim_Hot_Spot/simulation-*.html` URLs redirect here. Same folder convention as PBQ labs: `{slug}/{slug}.html`.

| Slug | Page |
|------|------|
| `dark-web-account-protection` | [Dark Web IR](dark-web-account-protection/dark-web-account-protection.html) |
| `malware-outbreak-classification` | [Malware outbreak](malware-outbreak-classification/malware-outbreak-classification.html) |
| `secure-web-architecture-openssl` | [Secure web & OpenSSL](secure-web-architecture-openssl/secure-web-architecture-openssl.html) |
| `vpc-payment-architecture` | [VPC payment network](vpc-payment-architecture/vpc-payment-architecture.html) |

## Entry points

Labs are linked from [`SEC+_Training_Portal.html`](../../SEC+_Training_Portal.html). Each scenario is one page:

| Page | Role |
|------|------|
| `{scenario-slug}/{scenario-slug}.html` | **One scenario, one page** — folder sidebar for all sections on that page |

Example: [`acme-rag-hr-ai/acme-rag-hr-ai.html`](acme-rag-hr-ai/acme-rag-hr-ai.html) with sections `#acme-exhibits`, `#acme-config`, …

Legacy `*-partN.html` URLs redirect to `{slug}/{slug}.html#section-id`.

## Scenario chain (Back / Next)

1. [BeCertifiedToday RAG HR AI](acme-rag-hr-ai/acme-rag-hr-ai.html)
2. [Zero Trust migration](zero-trust-zta-migration/zero-trust-zta-migration.html)
3. [Hybrid PKI audit](hybrid-pki-audit/hybrid-pki-audit.html)
4. [Ubuntu SSH breach hardening](ubuntu-ssh-breach-hardening/ubuntu-ssh-breach-hardening.html)
5. [Firewall ACL — Security Operations](firewall-acl-secops/firewall-acl-secops.html)
6. [Ransomware DR — BeCertifiedToday](ransomware-dr-acme/ransomware-dr-acme.html)
7. [SIEM ransomware — Sigma & MITRE](siem-ransomware-mitre/siem-ransomware-mitre.html)
8. [Advanced Firewall Rule Configurator](advanced-firewall-rule-configurator/advanced-firewall-rule-configurator.html)
9. [Network Diagram — Security Control Placement](security-control-placement/security-control-placement.html)
10. [Subnetting & IP Addressing Configuration](subnetting-ip-addressing/subnetting-ip-addressing.html)
11. [Ubuntu 22.04 baseline hardening](ubuntu-cis-hardening/ubuntu-cis-hardening.html)
12. [Wireless Access Point — Secure Configuration](wap-secure-configuration/wap-secure-configuration.html)
13. [Log Timeline Forensics](log-timeline-forensics/log-timeline-forensics.html)
14. [PKI Certificate Chain — Browser Error](pki-certificate-chain-browser-error/pki-certificate-chain-browser-error.html)
15. [Phishing Email Analysis](phishing-email-analysis/phishing-email-analysis.html)
16. [Vulnerability Management](vulnerability-management/vulnerability-management.html)
17. [Incident Response — Ransomware IR](incident-response/incident-response.html)
18. [Quantitative Risk — ALE](quantitative-risk-ale/quantitative-risk-ale.html)
19. [Malware IOC Analysis](malware-ioc-analysis/malware-ioc-analysis.html)
20. [Data Protection](data-protection/data-protection.html)
21. [Governance](governance/governance.html)

## Section source files

Edit `{scenario-slug}/sections/{section-id}.html`, then:

```bash
npm run build:pbq-suite
```

## Scenarios

| Folder | Sections |
|--------|----------|
| [`acme-rag-hr-ai/`](acme-rag-hr-ai/) | exhibits, config, guardrails, attacks, p2 |
| [`zero-trust-zta-migration/`](zero-trust-zta-migration/) | exhibit, concept, zone map, trade-offs |
| [`hybrid-pki-audit/`](hybrid-pki-audit/) | chain, algorithms, revocation |
| [`ubuntu-ssh-breach-hardening/`](ubuntu-ssh-breach-hardening/) | intro, sshd, fail2ban, ufw, consequences |
| [`firewall-acl-secops/`](firewall-acl-secops/) | ACL rule table (web + DB tier) |
| [`ransomware-dr-acme/`](ransomware-dr-acme/) | DR step order, RTO/RPO/site, trade-offs |
| [`siem-ransomware-mitre/`](siem-ransomware-mitre/) | Sigma rule, MITRE classify, containment |
| [`advanced-firewall-rule-configurator/`](advanced-firewall-rule-configurator/) | Perimeter ACL — policy, topology, dynamic rule table |
| [`security-control-placement/`](security-control-placement/) | Three-zone diagram — drag controls to labeled slots |
| [`subnetting-ip-addressing/`](subnetting-ip-addressing/) | /24 subnet calculator + department assignment |
| [`ubuntu-cis-hardening/`](ubuntu-cis-hardening/) | Checklist, sshd_config, pwquality.conf (CIS) |
| [`wap-secure-configuration/`](wap-secure-configuration/) | WPA3-Enterprise WAP — toggles + live preview |
| [`log-timeline-forensics/`](log-timeline-forensics/) | SSH log snippet reorder — brute force to privesc |
| [`pki-certificate-chain-browser-error/`](pki-certificate-chain-browser-error/) | PKI chain exhibit + ERR_CERT_AUTHORITY_INVALID MCQ |
| [`phishing-email-analysis/`](phishing-email-analysis/) | Phishing exhibit + social-engineering fill-in |
| [`vulnerability-management/`](vulnerability-management/) | Scanner exhibit + Log4Shell compensating control MCQ |
| [`incident-response/`](incident-response/) | NIST SP 800-61 IR term fill-in (ransomware) |
| [`quantitative-risk-ale/`](quantitative-risk-ale/) | SLE/ARO/ALE worksheet + training ROI MCQ |
| [`malware-ioc-analysis/`](malware-ioc-analysis/) | Endpoint IOC console + malware classification MCQ |
| [`data-protection/`](data-protection/) | Classification exhibit + PCI tokenization MCQ |
| [`governance/`](governance/) | Frameworks, policies, breach notification MCQ |

## Preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/acme-rag-hr-ai/acme-rag-hr-ai.html
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/acme-rag-hr-ai/acme-rag-hr-ai.html#acme-config
```

`PBQ_Production/` skips the paid portal gate on localhost.

## Styles

`/COMP_TIA_SEC+/js/secplus-pbq-page.css` · `pbq-folder-suite.js` · `/css/bcc-question-link-nav.css`

# PBQ_Production

**Active workspace** for new SY0-701 PBQ scenarios before they ship to the public bank.

Answer keys were verified against CompTIA-aligned objectives and primary sources (NIST, RFC, OWASP, OpenSSH). See **[VERIFICATION.md](VERIFICATION.md)** (2026-06-04).

**Adding a new scenario:** follow **[ADD-PBQ.md](ADD-PBQ.md)**.

The **26-lab chain** is registered in `scripts/build-pbq-production-suite.py`. **BCT standalone sims** on the portal also live here as single-page HTML. Scenarios **not** on [`SEC+_Training_Portal.html`](../../SEC+_Training_Portal.html) stay in [`../pending/`](../pending/) for review.

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
22. [Sec+ Cloud Web Application Firewall Setup](cloud-waf-setup/cloud-waf-setup.html)
23. [SEC+ Incident Response and Phase Matching](incident-response-matching/incident-response-matching.html)
24. [SEC+ Cryptographic Algorithms Matching](cryptographic-algorithms-matching/cryptographic-algorithms-matching.html)
25. [SEC+ Malware Infection Log Analysis](malware-infection-log-analysis/malware-infection-log-analysis.html)
26. [Sec+ Director and Administrator WLAN Setup](home-wlan-director-config/home-wlan-director-config.html)
27. [SEC+ Public WLAN Guest Configuration](public-wlan-guest-config/public-wlan-guest-config.html)
28. [SEC+ MDM Enrollment Configuration](mdm-enrollment-config/mdm-enrollment-config.html)
29. [SEC+ Network Protocols Matching](network-protocols-matching/network-protocols-matching.html)
30. [SEC+ Site-to-Site VPN Configuration](site-to-site-vpn-config/site-to-site-vpn-config.html)
31. [SEC+ Web App Subnet Zoning](web-app-subnet-zoning/web-app-subnet-zoning.html)
32. [SEC+ Dark Web Incident Response](dark-web-account-protection/dark-web-account-protection.html)
33. [SEC+ Malware Outbreak Classification](malware-outbreak-classification/malware-outbreak-classification.html)
34. [SEC+ VPC Payment Architecture](vpc-payment-architecture/vpc-payment-architecture.html)

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
| [`cloud-waf-setup/`](cloud-waf-setup/) | Sample ticket + four-tab cloud WAF console |
| [`incident-response-matching/`](incident-response-matching/) | NIST IR phase buckets — twelve action tokens |
| [`cryptographic-algorithms-matching/`](cryptographic-algorithms-matching/) | Ten crypto algorithms matched to use-case descriptions |
| [`malware-infection-log-analysis/`](malware-infection-log-analysis/) | Six-host AV + firewall log triage — source / infected / clean |
| [`home-wlan-director-config/`](home-wlan-director-config/) | Director WLAN — WPA2, MAC filter, admin password |
| [`public-wlan-guest-config/`](public-wlan-guest-config/) | BCT lobby guest WLAN — open SSID, channel 11, admin username |
| [`mdm-enrollment-config/`](mdm-enrollment-config/) | BeCertifiedToday MDM — iOS compliance, app restrictions, ADE |
| [`network-protocols-matching/`](network-protocols-matching/) | Eleven protocols matched to security functions |
| [`site-to-site-vpn-config/`](site-to-site-vpn-config/) | Dual-gateway IKE Phase 1 + IPsec Phase 2 for BCT_HQ1/BCT_HQ2 |
| [`web-app-subnet-zoning/`](web-app-subnet-zoning/) | Three-tier cloud drag-and-drop — WAF, tiers, LB, database |
| [`dark-web-account-protection/`](dark-web-account-protection/) | Dark web credential exposure IR — exhibits + FIDO containment |
| [`malware-outbreak-classification/`](malware-outbreak-classification/) | AV log triage — origin / infected / clean on five hosts |
| [`vpc-payment-architecture/`](vpc-payment-architecture/) | PCI VPC diagram — WAF, LB, app tier, database placement |

## BCT standalone sims (portal, not in build chain)

| Folder | Description |
|--------|-------------|
| [`secure-web-architecture-openssl/`](secure-web-architecture-openssl/) | TLS, ciphers, OpenSSL practices |

_WLAN / config PBQs not yet on the portal live in [`../pending/`](../pending/) for review._


## Preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/acme-rag-hr-ai/acme-rag-hr-ai.html
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/acme-rag-hr-ai/acme-rag-hr-ai.html#acme-config
```

`PBQ_Production/` skips the paid portal gate on localhost.

## Styles

`/COMP_TIA_SEC+/js/secplus-pbq-page.css` · `pbq-folder-suite.js` · `/css/bcc-question-link-nav.css`

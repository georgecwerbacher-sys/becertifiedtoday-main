---
type: pbq-index
exam: SY0-701
last_updated: 2026-06-05
---

# Security+ PBQ — production labs (Obsidian)

Study and authoring notes for each scenario under `public/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/`.

**Discovery:** `SEC+_Training_Portal.html` (per-lab links; no PBQ hub index)  
**Answer audit (repo):** `public/.../PBQ_Production/VERIFICATION.md`  
**Rebuild after HTML edits:** `npm run build:pbq-suite`

## Scenario chain

| # | Folder | Live page | Vault folder |
|---|--------|-----------|--------------|
| 1 | `acme-rag-hr-ai` | [RAG HR AI](https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/acme-rag-hr-ai/acme-rag-hr-ai.html) | [[acme-rag-hr-ai/notes|BeCertifiedToday RAG]] |
| 2 | `zero-trust-zta-migration` | [Zero Trust](https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/zero-trust-zta-migration/zero-trust-zta-migration.html) | [[zero-trust-zta-migration/notes|ZTA]] |
| 3 | `hybrid-pki-audit` | [Hybrid PKI](https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/hybrid-pki-audit/hybrid-pki-audit.html) | [[hybrid-pki-audit/notes|PKI]] |
| 4 | `ubuntu-ssh-breach-hardening` | [Ubuntu SSH breach](https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/ubuntu-ssh-breach-hardening/ubuntu-ssh-breach-hardening.html) | [[ubuntu-ssh-breach-hardening/notes|Ubuntu SSH breach]] |
| 5 | `firewall-acl-secops` | [Firewall ACL](https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/firewall-acl-secops/firewall-acl-secops.html) | [[firewall-acl-secops/notes|Firewall ACL]] |
| 6 | `ransomware-dr-acme` | [Ransomware DR](https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/ransomware-dr-acme/ransomware-dr-acme.html) | [[ransomware-dr-acme/notes|Ransomware DR]] |
| 7 | `siem-ransomware-mitre` | [SIEM / MITRE](https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/siem-ransomware-mitre/siem-ransomware-mitre.html) | [[siem-ransomware-mitre/notes|SIEM MITRE]] |
| 8 | `advanced-firewall-rule-configurator` | [Advanced firewall](https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/advanced-firewall-rule-configurator/advanced-firewall-rule-configurator.html) | [[advanced-firewall-rule-configurator/notes|Advanced firewall]] |
| 9 | `security-control-placement` | [Control placement](https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/security-control-placement/security-control-placement.html) | [[security-control-placement/notes|Control placement]] |
| 10 | `subnetting-ip-addressing` | [Subnetting](https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/subnetting-ip-addressing/subnetting-ip-addressing.html) | [[subnetting-ip-addressing/notes|Subnetting]] |
| 11 | `ubuntu-cis-hardening` | [Ubuntu CIS](https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/ubuntu-cis-hardening/ubuntu-cis-hardening.html) | [[ubuntu-cis-hardening/notes|Ubuntu CIS]] |
| 12 | `wap-secure-configuration` | [WAP config](https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/wap-secure-configuration/wap-secure-configuration.html) | [[wap-secure-configuration/notes|WAP config]] |
| 13 | `log-timeline-forensics` | [Log timeline](https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/log-timeline-forensics/log-timeline-forensics.html) | [[log-timeline-forensics/notes|Log timeline]] |
| 14 | `pki-certificate-chain-browser-error` | [PKI browser error](https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/pki-certificate-chain-browser-error/pki-certificate-chain-browser-error.html) | [[pki-certificate-chain-browser-error/notes|PKI browser]] |
| 15 | `phishing-email-analysis` | [Phishing analysis](https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/phishing-email-analysis/phishing-email-analysis.html) | [[phishing-email-analysis/notes|Phishing]] |
| 16 | `vulnerability-management` | [Vuln management](https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/vulnerability-management/vulnerability-management.html) | [[vulnerability-management/notes|Vuln mgmt]] |
| 17 | `incident-response` | [Incident response](https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/incident-response/incident-response.html) | [[incident-response/notes|IR fill-in]] |
| 18 | `quantitative-risk-ale` | [Risk / ALE](https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/quantitative-risk-ale/quantitative-risk-ale.html) | [[quantitative-risk-ale/notes|Risk ALE]] |
| 19 | `malware-ioc-analysis` | [Malware IOCs](https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/malware-ioc-analysis/malware-ioc-analysis.html) | [[malware-ioc-analysis/notes|Malware IOC]] |
| 20 | `data-protection` | [Data protection](https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/data-protection/data-protection.html) | [[data-protection/notes|Data protection]] |
| 21 | `governance` | [Governance](https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/governance/governance.html) | [[governance/notes|Governance]] |

Each scenario folder contains:

- **[[…/notes|notes]]** — scenario summary, SY0-701 mapping, section map
- **[[…/recommendations|recommendations]]** — product, teaching, and exam-prep improvements
- **[[…/deep-dive-solution|deep-dive-solution]]** — full keyed walkthrough with distractor analysis

## Related vault links

- [[../11-question-sourcing/pbq/README|SY0-701 PBQ sourcing]]
- [[../11-question-sourcing/pbq/secplus-pbq-not-in-bct|Net-new PBQ log]]
- [[../05-playbooks/secplus-monthly-pbq-sourcing|Monthly PBQ sourcing playbook]]

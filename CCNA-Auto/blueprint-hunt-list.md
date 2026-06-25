---
type: hunt-blueprint
exam: CCNAAUTO-200-901
blueprint_version: v1.1
source: Cisco Learning Network CCNAAUTO exam topics
source_pdf: https://learningcontent.cisco.com/documents/marketing/exam-topics/200-901-CCNAAUTO_v.1.1.pdf
---

# CCNAAUTO 200-901 — blueprint hunt list

Use this checklist when reviewing competitor captures. Mark **MCQ**, **Lab**, or **Sim/PBQ** as you find or draft coverage. Verify every answer on **Cisco Tier A** (official docs, Learning Network, DevNet) before bank draft.

**Legend:** `[ ]` not started · `[~]` partial competitor signal · `[x]` in BCT bank · `[!]` needs manual exhibit/script capture

Back: [[README|CCNA-Auto]]

---

## 1.0 Software Development and Design (15%)

| ID | Objective | MCQ | Lab | Notes |
|----|-----------|:---:|:---:|-------|
| 1.1 | Compare data formats (XML, JSON, YAML, plain text) | [ ] | [ ] | CCNA overlap: JSON slugs in `CCNA_questions/json-*` |
| 1.2 | Parse, construct, and validate JSON/XML/YAML/Python data structures | [ ] | [ ] | Hunt JSON drag-and-drop + script output items |
| 1.3 | Describe concepts of test-driven development | [ ] | [ ] | |
| 1.4 | Compare software development methods (agile, lean, waterfall) | [ ] | [ ] | |
| 1.5 | Describe the advantages of version control | [ ] | [ ] | |
| 1.6 | Describe the characteristics of API styles (REST, RPC, synchronous, async) | [ ] | [ ] | CCNA overlap: REST API MCQs |
| 1.7 | Describe the challenges of network programmability | [ ] | [ ] | CCNA overlap: automation benefits/drivers |
| 1.8 | Utilize common Git operations (clone, add/remove, commit, push/pull, branch, merge, diff) | [ ] | [ ] | Hunt CLI-style Git transcript labs |

---

## 2.0 Understanding and Using APIs (20%)

| ID | Objective | MCQ | Lab | Notes |
|----|-----------|:---:|:---:|-------|
| 2.1 | Construct a REST API request from API documentation | [ ] | [ ] | Hunt curl/Postman-style exhibits |
| 2.2 | Describe webhook usage patterns | [ ] | [ ] | |
| 2.3 | Describe constraints when consuming APIs | [ ] | [ ] | |
| 2.4 | Explain common HTTP response codes for REST APIs | [ ] | [ ] | CCNA overlap: `rest-api-http-*` slugs |
| 2.5 | Troubleshoot using HTTP response code + request + docs | [ ] | [ ] | |
| 2.6 | Interpret HTTP response parts (code, headers, body) | [ ] | [ ] | |
| 2.7 | Utilize API auth: basic, custom token, API keys | [ ] | [ ] | |
| 2.8 | Compare API styles (REST, RPC, sync, async) | [ ] | [ ] | |
| 2.9 | Construct Python `requests` script calling a REST API | [ ] | [ ] | **Lab priority** — script PBQ |

---

## 3.0 Cisco Platforms and Development (15%)

| ID | Objective | MCQ | Lab | Notes |
|----|-----------|:---:|:---:|-------|
| 3.1 | Describe Cisco SDKs and their use | [ ] | [ ] | DevNet platform docs |
| 3.2 | Describe capabilities of Cisco network management platforms (Meraki, Catalyst Center, SD-WAN, NSO) | [ ] | [ ] | CCNA overlap: DNA Center / Meraki MCQs |
| 3.3 | Describe compute management APIs (UCS Manager, Intersight) | [ ] | [ ] | v1.1: UCS Director removed |
| 3.4 | Describe collaboration APIs (Webex, CUCM AXL/UDS) | [ ] | [ ] | v1.1: Webex Teams → Webex |
| 3.5 | Describe security platform APIs (XDR, Firepower, Umbrella, Secure Endpoint, ISE, Secure Malware Analytics) | [ ] | [ ] | v1.1 naming updates |
| 3.6 | Describe device management APIs (IOS XE, NX-OS, IOS XR) | [ ] | [ ] | |
| 3.7 | Describe model-driven telemetry (gRPC, MDT, YANG) | [ ] | [ ] | |
| 3.8 | Describe RESTCONF/NETCONF capabilities | [ ] | [ ] | v1.1 emphasis |
| 3.9.a | Code: list devices (Meraki, Catalyst Center, ACI, SD-WAN, NSO) | [ ] | [ ] | **Lab priority** |
| 3.9.b | Code: manage Webex spaces/participants/messages | [ ] | [ ] | |
| 3.9.c | Code: list clients/hosts (Meraki, Catalyst Center) | [ ] | [ ] | |

---

## 4.0 Application Deployment and Security (15%)

| ID | Objective | MCQ | Lab | Notes |
|----|-----------|:---:|:---:|-------|
| 4.1 | Describe characteristics of API styles in application deployment | [ ] | [ ] | |
| 4.2 | Describe the concepts of edge computing | [ ] | [ ] | |
| 4.3.a | Describe VM deployment attributes | [ ] | [ ] | |
| 4.3.b | Describe bare-metal deployment attributes | [ ] | [ ] | |
| 4.3.c | Describe container deployment attributes | [ ] | [ ] | Hunt Docker/K8s MCQs |
| 4.4 | Describe CI/CD pipeline concepts | [ ] | [ ] | |
| 4.5 | Describe application security (OWASP, secrets, TLS) | [ ] | [ ] | |
| 4.6 | Describe OWASP threats and mitigations | [ ] | [ ] | |
| 4.7 | Describe secure coding practices | [ ] | [ ] | |

---

## 5.0 Infrastructure and Automation (20%)

| ID | Objective | MCQ | Lab | Notes |
|----|-----------|:---:|:---:|-------|
| 5.1 | Describe model-driven programmability value | [ ] | [ ] | CCNA overlap: YANG/JSON models |
| 5.2 | Compare controller-level vs device-level management | [ ] | [ ] | CCNA overlap: SDN controller |
| 5.3 | Describe network simulation tools (CML, pyATS) | [ ] | [ ] | v1.1: VIRL → CML |
| 5.4 | Describe CI/CD pipeline in infrastructure automation | [ ] | [ ] | |
| 5.5 | Describe infrastructure-as-code principles | [ ] | [ ] | |
| 5.6 | Describe Ansible, Terraform, Cisco NSO capabilities | [ ] | [ ] | CCNA overlap: Ansible/Terraform MCQs; v1.1 adds Terraform |
| 5.7 | Identify workflow in Python script using Cisco APIs (ACI, Meraki, Catalyst Center, RESTCONF) | [ ] | [ ] | **Lab priority** |
| 5.8 | Interpret Ansible playbook workflow | [ ] | [ ] | **Lab priority** — playbook PBQ |
| 5.9 | Interpret bash script workflow | [ ] | [ ] | **Lab priority** |
| 5.10 | Interpret RESTCONF/NETCONF query results | [ ] | [ ] | **Lab priority** |
| 5.11 | Interpret basic YANG models | [ ] | [ ] | Hunt YANG tree drag-and-drop |
| 5.12 | Interpret unified diff | [ ] | [ ] | v1.1 new |
| 5.13 | Describe code review principles and benefits | [ ] | [ ] | v1.1 new |
| 5.14 | Interpret API sequence diagram | [ ] | [ ] | v1.1 new |

---

## 6.0 Network Fundamentals (15%)

| ID | Objective | MCQ | Lab | Notes |
|----|-----------|:---:|:---:|-------|
| 6.1 | MAC addresses and VLANs | [ ] | [ ] | CCNA core overlap |
| 6.2 | IP addresses, routes, prefix, gateways | [ ] | [ ] | CCNA core overlap |
| 6.3 | Common components (switch, router, firewall, load balancer) | [ ] | [ ] | |
| 6.4 | Interpret topology diagram | [ ] | [ ] | Hunt topology exhibits |
| 6.5 | Management, data, and control planes | [ ] | [ ] | CCNA overlap |
| 6.6 | IP services (DHCP, DNS, NAT, SNMP, NTP) | [ ] | [ ] | CCNA overlap |
| 6.7 | Common protocol ports (SSH, Telnet, HTTP, HTTPS, NETCONF) | [ ] | [ ] | CCNA overlap |
| 6.8 | Diagnose app connectivity (NAT, port block, proxy, VPN) | [ ] | [ ] | Troubleshooting PBQ |
| 6.9 | Impacts of network constraints on applications | [ ] | [ ] | |

---

## CCNA 200-301 domain 6.0 cross-reference

These CCNA objectives overlap CCNAAUTO hunt scope. Existing BCT slugs tagged `6.x` in `ccna-question-topic-map.json` count as partial coverage — extend or rewrite for CCNAAUTO depth.

| CCNA ID | CCNA objective | BCT status |
|---------|----------------|------------|
| 6.1 | Explain how automation impacts network management | partial MCQ |
| 6.2 | Compare traditional vs controller-based networking | partial MCQ |
| 6.3 | SDN architecture (overlay, underlay, fabric) | partial MCQ |
| 6.4 | AI/ML in network operations | gap |
| 6.5 | REST API characteristics (auth, CRUD, verbs, encoding) | partial MCQ |
| 6.6 | Ansible and Terraform capabilities | partial MCQ |
| 6.7 | JSON-encoded data components | partial MCQ + D&D |

---

## Hunt priorities (first pass)

1. **Python REST script PBQs** (2.9, 5.7) — highest CCNAAUTO differentiator vs CCNA MCQs alone
2. **Ansible playbook interpretation** (5.8) — playbook exhibit labs
3. **JSON/YANG drag-and-drop** (1.2, 5.11) — extend CCNA JSON D&D pattern
4. **RESTCONF/NETCONF output** (5.10) — CLI/XML exhibit transcripts
5. **Terraform IaC** (5.6) — v1.1 net-new vs CCNA V_2025 bank

After each monthly run, link net-new items here from [[Hunt/ccnaauto/README|ccnaauto hunt runs]] (`Hunt/ccnaauto/YYYY-MM-DD/`).

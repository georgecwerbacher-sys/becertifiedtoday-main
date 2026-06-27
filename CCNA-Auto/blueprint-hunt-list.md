---
type: hunt-blueprint
exam: CCNAAUTO-200-901
blueprint_version: v1.1
source: Cisco Learning Network CCNAAUTO exam topics
source_pdf: blueprints/200-901-CCNAAUTO_v.1.1.pdf
source_legacy_pdf: blueprints/200-901-DEVASC_v1.0.pdf
objectives_note: [[exam-objectives|Official exam objectives (v1.0 + v1.1)]]
web_blueprint_json: ../../public/CCNAAUTO-Study/data/ccnaauto-blueprint-v1.1.json
---

# CCNAAUTO 200-901 — blueprint hunt list

Use this checklist when reviewing competitor captures. Mark **MCQ**, **Lab**, or **Sim/PBQ** as you find or draft coverage. Verify every answer on **Cisco Tier A** (official docs, Learning Network, DevNet) before bank draft.

**Source:** verbatim from `blueprints/200-901-CCNAAUTO_v.1.1.pdf` · [[exam-objectives|exam-objectives]] · legacy `200-901-DEVASC_v1.0.pdf`

**v1.0 → v1.1 diff (outdated vs in-scope):** [[blueprint-v1-changes|Changes only]]

**Legend:** `[ ]` not started · `[~]` partial competitor signal · `[x]` in BCT bank · `[!]` needs manual exhibit/script capture

Back: [[README|CCNA-Auto]]

---

## 1.0 Software Development and Design (15%)

| ID | Objective | MCQ | Lab | Notes |
|----|-----------|:---:|:---:|-------|
| 1.1 | Compare data formats (XML, JSON, and YAML) | [ ] | [ ] | CCNA overlap: `json-*` slugs |
| 1.2 | Describe parsing of common data format (XML, JSON, and YAML) to Python data structures | [ ] | [ ] | JSON drag-and-drop |
| 1.3 | Describe the concepts of test-driven development | [ ] | [ ] | |
| 1.4 | Compare software development methods (agile, lean, and waterfall) | [ ] | [ ] | |
| 1.5 | Explain the benefits of organizing code into methods / functions, classes, and modules | [ ] | [ ] | |
| 1.6 | Explain the advantages of common design patterns (MVC and Observer) | [ ] | [ ] | |
| 1.7 | Explain the advantages of version control | [ ] | [ ] | |
| 1.8 | Utilize common version control operations with Git | [ ] | [ ] | |
| 1.8.a | Clone | [ ] | [ ] | |
| 1.8.b | Add/remove | [ ] | [ ] | |
| 1.8.c | Commit | [ ] | [ ] | |
| 1.8.d | Push / pull | [ ] | [ ] | |
| 1.8.e | Branch | [ ] | [ ] | |
| 1.8.f | Merge and handling conflicts | [ ] | [ ] | |
| 1.8.g | diff | [ ] | [ ] | Hunt Git transcript labs |

---

## 2.0 Understanding and Using APIs (20%)

| ID | Objective | MCQ | Lab | Notes |
|----|-----------|:---:|:---:|-------|
| 2.1 | Construct a REST API request to accomplish a task given API documentation | [ ] | [ ] | curl/Postman exhibits |
| 2.2 | Describe common usage patterns related to webhooks | [ ] | [ ] | |
| 2.3 | Describe the constraints when consuming APIs | [ ] | [ ] | |
| 2.4 | Explain common HTTP response codes associated with REST APIs | [ ] | [ ] | CCNA overlap: `rest-api-http-*` |
| 2.5 | Troubleshoot a problem given the HTTP response code, request and API documentation | [ ] | [ ] | |
| 2.6 | Interpret the parts of an HTTP response (response code, headers, body) | [ ] | [ ] | |
| 2.7 | Utilize common API authentication mechanisms: basic, custom token, and API keys | [ ] | [ ] | |
| 2.8 | Compare common API styles (REST, RPC, synchronous, and asynchronous) | [ ] | [ ] | |
| 2.9 | Construct a Python script that calls a REST API using the requests library | [ ] | [ ] | **Lab priority** — script PBQ |

---

## 3.0 Cisco Platforms and Development (15%)

| ID | Objective | MCQ | Lab | Notes |
|----|-----------|:---:|:---:|-------|
| 3.1 | Construct a Python script that uses a Cisco SDK given SDK documentation | [ ] | [ ] | **Lab priority** |
| 3.2 | Describe the capabilities of Cisco network management platforms and APIs (Meraki, Cisco Catalyst Center, ACI, Cisco Catalyst SD-WAN, and NSO) | [ ] | [ ] | v1.1 naming |
| 3.3 | Describe the capabilities of Cisco compute management platforms and APIs (UCS Manager and Intersight) | [ ] | [ ] | v1.1: UCS Director removed |
| 3.4 | Describe the capabilities of Cisco collaboration platforms and APIs (Webex, Webex devices, Cisco Unified Communications Manager including AXL and UDS interfaces) | [ ] | [ ] | v1.1: Webex Teams → Webex |
| 3.5 | Describe the capabilities of Cisco security platforms and APIs (XDR, Firepower, Secure Connect, Secure Endpoint, ISE, and Secure Malware Analytics) | [ ] | [ ] | v1.1 product names |
| 3.6 | Describe the device level APIs and dynamic interfaces for IOS XE and NX-OS | [ ] | [ ] | |
| 3.7 | Describe the appropriate DevNet resource for a given scenario (Sandbox, Code Exchange, support, forums, Learning Labs, and API documentation) | [ ] | [ ] | |
| 3.8 | Apply concepts of model driven programmability (YANG, RESTCONF, and NETCONF) in a Cisco environment | [ ] | [ ] | |
| 3.9 | Construct code to perform a specific operation based on a set of requirements and given API reference documentation such as these: | [ ] | [ ] | parent |
| 3.9.a | Obtain a list of network devices by using Meraki, Cisco Catalyst Center, ACI, Cisco Catalyst SD-WAN, or NSO | [ ] | [ ] | **Lab priority** |
| 3.9.b | Manage spaces, participants, and messages in Webex | [ ] | [ ] | |
| 3.9.c | Obtain a list of clients / hosts seen on a network using Meraki or Cisco Catalyst Center | [ ] | [ ] | |

---

## 4.0 Application Deployment and Security (15%)

| ID | Objective | MCQ | Lab | Notes |
|----|-----------|:---:|:---:|-------|
| 4.1 | Describe the benefits of edge computing | [ ] | [ ] | |
| 4.2 | Describe the attributes of different application deployment models (private cloud, public cloud, hybrid cloud, and edge) | [ ] | [ ] | |
| 4.3 | Describe the attributes of these application deployment types | [ ] | [ ] | parent |
| 4.3.a | Virtual machines | [ ] | [ ] | |
| 4.3.b | Bare metal | [ ] | [ ] | |
| 4.3.c | Containers | [ ] | [ ] | Docker MCQs |
| 4.4 | Describe components for a CI/CD pipeline in application deployments | [ ] | [ ] | |
| 4.5 | Construct a Python unit test | [ ] | [ ] | **Lab priority** |
| 4.6 | Interpret contents of a Dockerfile | [ ] | [ ] | |
| 4.7 | Utilize Docker images in local developer environment | [ ] | [ ] | |
| 4.8 | Describe application security issues related to secret protection, encryption (storage and transport), and data handling | [ ] | [ ] | |
| 4.9 | Explain how firewall, DNS, load balancers, and reverse proxy in application deployment | [ ] | [ ] | |
| 4.10 | Describe top OWASP threats (such as XSS, SQL injections, and CSRF) | [ ] | [ ] | |
| 4.11 | Utilize Bash commands (file management, directory navigation, and environmental variables) | [ ] | [ ] | **Lab priority** |
| 4.12 | Describe the principles of DevOps practices | [ ] | [ ] | |

---

## 5.0 Infrastructure and Automation (20%)

| ID | Objective | MCQ | Lab | Notes |
|----|-----------|:---:|:---:|-------|
| 5.1 | Describe the value of model driven programmability for infrastructure automation | [ ] | [ ] | YANG/JSON models |
| 5.2 | Compare controller-level to device-level management | [ ] | [ ] | SDN controller overlap |
| 5.3 | Describe the use and roles of network simulation and test tools (such as Cisco Modeling Labs and pyATS) | [ ] | [ ] | v1.1: VIRL → CML |
| 5.4 | Describe the components and benefits of CI/CD pipeline in infrastructure automation | [ ] | [ ] | |
| 5.5 | Describe the principles of infrastructure as code | [ ] | [ ] | |
| 5.6 | Describe the capabilities of automation tools such as Ansible, Terraform, and Cisco NSO | [ ] | [ ] | v1.1: +Terraform, −Puppet/Chef |
| 5.7 | Identify the workflow being automated by a Python script that uses Cisco APIs including ACI, Meraki, Cisco Catalyst Center, and RESTCONF | [ ] | [ ] | **Lab priority** |
| 5.8 | Interpret the workflow being automated by an Ansible playbook (management packages, user management related to services, basic service configuration, and start/stop) | [ ] | [ ] | **Lab priority** |
| 5.9 | Interpret the workflow being automated by a bash script (such as file management, app install, user management, directory navigation) | [ ] | [ ] | **Lab priority** |
| 5.10 | Interpret the results of a RESTCONF or NETCONF query | [ ] | [ ] | **Lab priority** |
| 5.11 | Interpret basic YANG models | [ ] | [ ] | YANG tree D&D |
| 5.12 | Interpret a unified diff | [ ] | [ ] | v1.1 |
| 5.13 | Describe the principles and benefits of a code review process | [ ] | [ ] | v1.1 |
| 5.14 | Interpret a sequence diagram that includes API calls | [ ] | [ ] | v1.1 |

---

## 6.0 Network Fundamentals (15%)

| ID | Objective | MCQ | Lab | Notes |
|----|-----------|:---:|:---:|-------|
| 6.1 | Describe the purpose and usage of MAC addresses and VLANs | [ ] | [ ] | CCNA core overlap |
| 6.2 | Describe the purpose and usage of IP addresses, routes, subnet mask / prefix, and gateways | [ ] | [ ] | CCNA core overlap |
| 6.3 | Describe the function of common networking components (such as switches, routers, firewalls, and load balancers) | [ ] | [ ] | |
| 6.4 | Interpret a basic network topology diagram with elements such as switches, routers, firewalls, load balancers, and port values | [ ] | [ ] | topology exhibits |
| 6.5 | Describe the function of management, data, and control planes in a network device | [ ] | [ ] | CCNA overlap |
| 6.6 | Describe the functionality of these IP Services: DHCP, DNS, NAT, SNMP, NTP | [ ] | [ ] | |
| 6.7 | Recognize common protocol port values (such as, SSH, Telnet, HTTP, HTTPS, and NETCONF) | [ ] | [ ] | |
| 6.8 | Diagnose application connectivity issues (NAT problem, Transport Port blocked, proxy, and VPN) | [ ] | [ ] | troubleshooting PBQ |
| 6.9 | Explain the impacts of network constraints on applications | [ ] | [ ] | |

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

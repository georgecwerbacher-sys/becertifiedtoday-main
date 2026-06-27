---
type: exam-blueprint
exam: CCNAAUTO-200-901
aliases:
  - DEVASC
  - DevNet Associate
  - CCNA Automation
updated: 2026-06-27
---

# CCNAAUTO 200-901 — official exam objectives

Canonical Cisco exam-topic PDFs for hunt blueprint work. Same exam code (**200-901**); branding moved from **DevNet Associate (DEVASC) v1.0** to **CCNA Automation (CCNAAUTO) v1.1** (Feb 2026).

| Version | Exam title | Certification | Local PDF |
|---------|------------|---------------|-----------|
| **v1.1** (current) | Automating Networks Using Cisco Platforms | CCNA Automation | [[blueprints/200-901-CCNAAUTO_v.1.1.pdf\|200-901-CCNAAUTO_v.1.1.pdf]] |
| **v1.0** (legacy) | DevNet Associate Exam | DevNet Associate – Developer | [[blueprints/200-901-DEVASC_v1.0.pdf\|200-901-DEVASC_v1.0.pdf]] |

Official URLs (Cisco Learning Network):

- v1.1: https://learningcontent.cisco.com/documents/marketing/exam-topics/200-901-CCNAAUTO_v.1.1.pdf
- v1.0: archived as `200-901-DEVASC.pdf` (DevNet Associate)

Hunt checklist derived from v1.1: [[blueprint-hunt-list|Blueprint hunt list]]

Web mirror (same objectives): `public/CCNAAUTO-Study/data/ccnaauto-blueprint-v1.1.json`

**Changes only (v1.0 → v1.1):** [[blueprint-v1-changes|blueprint-v1-changes]] · `public/CCNAAUTO-Study/data/ccnaauto-blueprint-v1-changes.json`

---

## v1.0 → v1.1 changes (summary)

Domain weights unchanged: **1.0** 15% · **2.0** 20% · **3.0** 15% · **4.0** 15% · **5.0** 20% · **6.0** 15%.

| Area | v1.0 (DEVASC) | v1.1 (CCNAAUTO) |
|------|---------------|-----------------|
| Branding | DevNet Associate | CCNA Automation |
| 3.2 platforms | DNA Center, SD-WAN | **Catalyst Center**, **Catalyst SD-WAN** |
| 3.3 compute | UCS Manager, **UCS Director**, Intersight | UCS Manager, Intersight (**UCS Director removed**) |
| 3.4 collaboration | **Webex Teams**, Finesse | **Webex** (Teams name retired) |
| 3.5 security APIs | Firepower, Umbrella, AMP, ISE, ThreatGrid | **XDR**, Firepower, **Secure Connect**, **Secure Endpoint**, ISE, **Secure Malware Analytics** |
| 3.9 refs | DNA Center, Webex Teams | Catalyst Center, Webex |
| 5.3 simulation | **VIRL**, pyATS | **Cisco Modeling Labs**, pyATS |
| 5.6 automation tools | Ansible, **Puppet**, **Chef**, NSO | Ansible, **Terraform**, NSO |
| 5.7 script APIs | DNA Center | Catalyst Center |
| 5.8–5.9 | **Identify** workflow | **Interpret** workflow |
| 6.8 connectivity | **Identify cause** | **Diagnose** issues |

Many objectives keep the same ID but shift verbs (`Identify` → `Describe` / `Explain` / `Utilize`). Treat competitor content tagged **DEVASC** or pre-2026 as v1.0 unless stems match v1.1 naming.

---

## v1.1 — Automating Networks Using Cisco Platforms (200-901)

**Exam description:** 120-minute exam for **CCNA Automation**. Tests software development and design: APIs, application deployment and security, infrastructure and automation on Cisco platforms. Prep course: *Developing Applications and Automating Workflows using Cisco Core Platforms*.

### 1.0 Software Development and Design (15%)

- 1.1 Compare data formats (XML, JSON, and YAML)
- 1.2 Describe parsing of common data format (XML, JSON, and YAML) to Python data structures
- 1.3 Describe the concepts of test-driven development
- 1.4 Compare software development methods (agile, lean, and waterfall)
- 1.5 Explain the benefits of organizing code into methods / functions, classes, and modules
- 1.6 Explain the advantages of common design patterns (MVC and Observer)
- 1.7 Explain the advantages of version control
- 1.8 Utilize common version control operations with Git
  - 1.8.a Clone
  - 1.8.b Add/remove
  - 1.8.c Commit
  - 1.8.d Push / pull
  - 1.8.e Branch
  - 1.8.f Merge and handling conflicts
  - 1.8.g diff

### 2.0 Understanding and Using APIs (20%)

- 2.1 Construct a REST API request to accomplish a task given API documentation
- 2.2 Describe common usage patterns related to webhooks
- 2.3 Describe the constraints when consuming APIs
- 2.4 Explain common HTTP response codes associated with REST APIs
- 2.5 Troubleshoot a problem given the HTTP response code, request and API documentation
- 2.6 Interpret the parts of an HTTP response (response code, headers, body)
- 2.7 Utilize common API authentication mechanisms: basic, custom token, and API keys
- 2.8 Compare common API styles (REST, RPC, synchronous, and asynchronous)
- 2.9 Construct a Python script that calls a REST API using the requests library

### 3.0 Cisco Platforms and Development (15%)

- 3.1 Construct a Python script that uses a Cisco SDK given SDK documentation
- 3.2 Describe the capabilities of Cisco network management platforms and APIs (Meraki, Cisco Catalyst Center, ACI, Cisco Catalyst SD-WAN, and NSO)
- 3.3 Describe the capabilities of Cisco compute management platforms and APIs (UCS Manager and Intersight)
- 3.4 Describe the capabilities of Cisco collaboration platforms and APIs (Webex, Webex devices, Cisco Unified Communications Manager including AXL and UDS interfaces)
- 3.5 Describe the capabilities of Cisco security platforms and APIs (XDR, Firepower, Secure Connect, Secure Endpoint, ISE, and Secure Malware Analytics)
- 3.6 Describe the device level APIs and dynamic interfaces for IOS XE and NX-OS
- 3.7 Describe the appropriate DevNet resource for a given scenario (Sandbox, Code Exchange, support, forums, Learning Labs, and API documentation)
- 3.8 Apply concepts of model driven programmability (YANG, RESTCONF, and NETCONF) in a Cisco environment
- 3.9 Construct code to perform a specific operation based on a set of requirements and given API reference documentation such as these:
  - 3.9.a Obtain a list of network devices by using Meraki, Cisco Catalyst Center, ACI, Cisco Catalyst SD-WAN, or NSO
  - 3.9.b Manage spaces, participants, and messages in Webex
  - 3.9.c Obtain a list of clients / hosts seen on a network using Meraki or Cisco Catalyst Center

### 4.0 Application Deployment and Security (15%)

- 4.1 Describe the benefits of edge computing
- 4.2 Describe the attributes of different application deployment models (private cloud, public cloud, hybrid cloud, and edge)
- 4.3 Describe the attributes of these application deployment types
  - 4.3.a Virtual machines
  - 4.3.b Bare metal
  - 4.3.c Containers
- 4.4 Describe components for a CI/CD pipeline in application deployments
- 4.5 Construct a Python unit test
- 4.6 Interpret contents of a Dockerfile
- 4.7 Utilize Docker images in local developer environment
- 4.8 Describe application security issues related to secret protection, encryption (storage and transport), and data handling
- 4.9 Explain how firewall, DNS, load balancers, and reverse proxy in application deployment
- 4.10 Describe top OWASP threats (such as XSS, SQL injections, and CSRF)
- 4.11 Utilize Bash commands (file management, directory navigation, and environmental variables)
- 4.12 Describe the principles of DevOps practices

### 5.0 Infrastructure and Automation (20%)

- 5.1 Describe the value of model driven programmability for infrastructure automation
- 5.2 Compare controller-level to device-level management
- 5.3 Describe the use and roles of network simulation and test tools (such as Cisco Modeling Labs and pyATS)
- 5.4 Describe the components and benefits of CI/CD pipeline in infrastructure automation
- 5.5 Describe the principles of infrastructure as code
- 5.6 Describe the capabilities of automation tools such as Ansible, Terraform, and Cisco NSO
- 5.7 Identify the workflow being automated by a Python script that uses Cisco APIs including ACI, Meraki, Cisco Catalyst Center, and RESTCONF
- 5.8 Interpret the workflow being automated by an Ansible playbook (management packages, user management related to services, basic service configuration, and start/stop)
- 5.9 Interpret the workflow being automated by a bash script (such as file management, app install, user management, directory navigation)
- 5.10 Interpret the results of a RESTCONF or NETCONF query
- 5.11 Interpret basic YANG models
- 5.12 Interpret a unified diff
- 5.13 Describe the principles and benefits of a code review process
- 5.14 Interpret a sequence diagram that includes API calls

### 6.0 Network Fundamentals (15%)

- 6.1 Describe the purpose and usage of MAC addresses and VLANs
- 6.2 Describe the purpose and usage of IP addresses, routes, subnet mask / prefix, and gateways
- 6.3 Describe the function of common networking components (such as switches, routers, firewalls, and load balancers)
- 6.4 Interpret a basic network topology diagram with elements such as switches, routers, firewalls, load balancers, and port values
- 6.5 Describe the function of management, data, and control planes in a network device
- 6.6 Describe the functionality of these IP Services: DHCP, DNS, NAT, SNMP, NTP
- 6.7 Recognize common protocol port values (such as, SSH, Telnet, HTTP, HTTPS, and NETCONF)
- 6.8 Diagnose application connectivity issues (NAT problem, Transport Port blocked, proxy, and VPN)
- 6.9 Explain the impacts of network constraints on applications

---

## v1.0 — DevNet Associate Exam (200-901 DEVASC)

**Exam description:** 120-minute exam for **DevNet Associate – Developer**. Same six domains and weights as v1.1. Full text preserved for competitor dedupe (many hunt sources still use DevNet / DEVASC naming).

<details>
<summary>Expand v1.0 objective list</summary>

### 1.0 Software Development and Design (15%)

- 1.1 Compare data formats (XML, JSON, and YAML)
- 1.2 Describe parsing of common data format (XML, JSON, and YAML) to Python data structures
- 1.3 Describe the concepts of test-driven development
- 1.4 Compare software development methods (agile, lean, and waterfall)
- 1.5 Explain the benefits of organizing code into methods / functions, classes, and modules
- 1.6 **Identify** the advantages of common design patterns (MVC and Observer)
- 1.7 Explain the advantages of version control
- 1.8 Utilize common version control operations with Git (1.8.a–g same as v1.1)

### 2.0 Understanding and Using APIs (20%)

- 2.1 Construct a REST API request to accomplish a task given API documentation
- 2.2 Describe common usage patterns related to webhooks
- 2.3 **Identify** the constraints when consuming APIs
- 2.4 Explain common HTTP response codes associated with REST APIs
- 2.5 Troubleshoot a problem given the HTTP response code, request and API documentation
- 2.6 **Identify** the parts of an HTTP response (response code, headers, body)
- 2.7 Utilize common API authentication mechanisms: basic, custom token, and API keys
- 2.8 Compare common API styles (REST, RPC, synchronous, and asynchronous)
- 2.9 Construct a Python script that calls a REST API using the requests library

### 3.0 Cisco Platforms and Development (15%)

- 3.1 Construct a Python script that uses a Cisco SDK given SDK documentation
- 3.2 Meraki, **Cisco DNA Center**, ACI, **Cisco SD-WAN**, and NSO
- 3.3 UCS Manager, **UCS Director**, and Intersight
- 3.4 **Webex Teams**, Webex devices, CUCM (AXL/UDS), **Finesse**
- 3.5 Firepower, **Umbrella**, **AMP**, ISE, **ThreatGrid**
- 3.6 Device level APIs for IOS XE and NX-OS
- 3.7 **Identify** the appropriate DevNet resource
- 3.8 YANG, RESTCONF, NETCONF
- 3.9.a Meraki, **DNA Center**, ACI, SD-WAN, or NSO
- 3.9.b **Webex Teams**
- 3.9.c Meraki or **DNA Center**

### 4.0 Application Deployment and Security (15%)

- 4.1 Describe benefits of edge computing
- 4.2 **Identify** attributes of deployment models
- 4.3 **Identify** attributes of VM / bare metal / containers
- 4.4–4.7 Same topics as v1.1 (CI/CD, unit test, Dockerfile, Docker images)
- 4.8 **Identify** application security issues
- 4.9–4.10 Same as v1.1
- 4.11 Utilize Bash commands
- 4.12 **Identify** DevOps principles

### 5.0 Infrastructure and Automation (20%)

- 5.1–5.5 Same topics as v1.1
- 5.3 **VIRL** and pyATS
- 5.6 Ansible, **Puppet**, **Chef**, and Cisco NSO
- 5.7 **DNA Center** (not Catalyst Center)
- 5.8–5.9 **Identify** workflow (Ansible / bash)
- 5.10–5.14 Same IDs as v1.1 (RESTCONF/NETCONF, YANG, diff, code review, sequence diagram)

### 6.0 Network Fundamentals (15%)

- 6.1–6.7 Same as v1.1
- 6.8 **Identify cause** of application connectivity issues
- 6.9 Explain impacts of network constraints

</details>

---

Back: [[README|CCNA-Auto]] · [[blueprint-hunt-list|Blueprint hunt list]]

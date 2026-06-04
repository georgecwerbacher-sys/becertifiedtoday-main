# PBQ_Production — answer verification (SY0-701)

**Audited:** 2026-06-04  
**Scope:** All graded keys in `PBQ_Production/` (four production scenarios).  
**Method:** Cross-check answer keys against CompTIA Security+ SY0-701 learning objectives (1.x general security, 2.x threats, 3.x architecture, 4.x operations) and primary references: NIST, IETF RFCs, OWASP, vendor-neutral hardening guidance (OpenSSH, fail2ban, Ubuntu UFW). Third-party exam dumps were not used.

**Summary:** All four simulations are **aligned** with credible sources. No answer key changes are required. Two items carry **pedagogical caveats** (real-world nuance); see notes below.

---

## 1. BeCertifiedToday RAG HR AI (`acme-rag-hr-ai/`)

| Section | Key | Verdict | Primary sources |
|---------|-----|---------|-----------------|
| **Config** | `secure`, `filter`, `approved`, `no-train`, `redact`, `untrusted` | **Pass** | OWASP [LLM Top 10 2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/) (LLM01 prompt injection, LLM08 vector/embedding weaknesses); [LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) (segregate untrusted content, RBAC on retrieval) |
| **Guardrails** | Enable: injection, PII output, retrieval filter, rate limit, ingest scan. Disable: anonymous, debug prompts, external tools | **Pass** | OWASP LLM01/LLM06 (excessive agency); least privilege and logging without exposing system prompts |
| **Attacks** | `input-guard`, `ingest-sanitize`, `ingest-controls`, `minimize-dlp`, `rbac-retrieval` | **Pass** | OWASP LLM01 indirect injection via retrieved docs; LLM04 data poisoning (ingest integrity); LLM02 disclosure (RBAC + minimization + rate limits) |
| **Part 2 MCQ** | All **B** (PI, data poisoning, model inversion) | **Pass** (see caveat on MI) | OWASP: input separation + classifiers; ingestion approval + integrity; rate limiting + output redaction |

**CompTIA SY0-701 fit:** Emerging AI risk, data governance, access control, and secure architecture (verify explicitly, least privilege) — consistent with objective themes in 1.2 and 3.x even though CompTIA does not publish a separate “RAG PBQ” spec.

**Model inversion (Part 2, answer B):** Pass message and choice B text emphasize **rate limiting** and **output PII redaction** first; differential privacy is noted as secondary when training is not used (matches `no-train` config).

---

## 2. Zero Trust migration (`zero-trust-zta-migration/`)

| Section | Key | Verdict | Primary sources |
|---------|-----|---------|-----------------|
| **Concept** | **B** — no implicit internal trust; PEP; adaptive identity; never trust / always verify | **Pass** | [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final); CompTIA SY0-701 1.2 zero trust control/data plane |
| **Zone map** | Internet → `ztna-gateway`; DMZ → `identity-provider`, `continuous-auth`; Internal → `micro-segmentation`, `pam-vault`, `jit-access`; Cloud → `casb`, `dlp-proxy` | **Pass** | NIST SP 800-207 (resource-focused access, PEP at boundary); ZTNA vs broad VPN (least privilege); CASB/DLP for SaaS/cloud egress |
| **Trade-offs Q1–Q3** | All **B** | **Pass** | Q1: ZTNA per-app + continuous verification vs VPN network-wide trust. Q2: PAM with privileged internal assets (blast radius). Q3: East-west verification / micro-segmentation — [CISA ZT microsegmentation guidance](https://www.cisa.gov/sites/default/files/2025-07/ZT-Microsegmentation-Guidance-Part-One_508c.pdf) |

**CompTIA SY0-701 fit:** **1.2** security principles and zero trust (control plane: policy engine/administrator, adaptive identity; data plane: PEP, micro-segmentation).

**Note:** PAM can be deployed in cloud in some enterprises; the item is written as a **trade-off** scenario where the senior engineer’s internal-placement argument is the security-best answer among choices (not a claim that cloud PAM is always forbidden).

---

## 3. Hybrid PKI audit (`hybrid-pki-audit/`)

| Section | Key | Verdict | Primary sources |
|---------|-----|---------|-----------------|
| **Chain (TLS)** | Root → `azure-inter-ca` → `leaf-api` | **Pass** | X.509 path validation; exclude SHA-1 on-prem intermediate and unrelated code-sign leaf |
| **Algorithms** | TLS kex: **ECDHE or DHE**; passwords: **bcrypt**; CA signing: **SHA-256**; blob: **AES-256-GCM** | **Pass** | [RFC 8446](https://datatracker.ietf.org/doc/html/rfc8446) (TLS 1.3 ephemeral KEX / forward secrecy); [NIST SP 800-63B](https://pages.nist.gov/800-63-4/sp800-63b/passwords/) (salted, costly password hashing); NIST/CA/Browser Forum deprecation of SHA-1 for signatures; NIST SP 800-38D (GCM) |
| **Revocation** | Check: `code-sign`, `onprem-inter` | **Pass** (see caveat) | Weak/expired code-sign (RSA-1024, expired); SHA-1 issuing CA must be retired from trust |

**CompTIA SY0-701 fit:** **1.4** cryptography (hashing, symmetric/asymmetric use cases, PKI, certificate lifecycle, CRL freshness called out in stem).

**Revoke on-prem SHA-1 intermediate:** Pass message notes **re-issue a SHA-256 intermediate and migrate** in production, while still selecting the weak issuer for immediate revocation in this audit scenario.

**Note:** Expired code-signing cert: revocation is still reasonable to **remove from trust stores** and satisfy audit hygiene even though expiry already blocks new signatures.

---

## 4. Ubuntu SSH breach hardening (`ubuntu-ssh-breach-hardening/`)

| Section | Key | Verdict | Primary sources |
|---------|-----|---------|-----------------|
| **sshd_config** | Port `4422`, Protocol `2`, `PermitRootLogin no`, `PasswordAuthentication no`, `MaxAuthTries 3`, `LoginGraceTime 30`, `X11Forwarding no` | **Pass** | [OpenSSH sshd_config](https://man.openbsd.org/sshd_config); CIS/benchmark-style SSH hardening |
| **fail2ban** | `enabled=true`, `port=4422`, `maxretry=3`, `bantime=24h` | **Pass** | [fail2ban jail.local](https://github.com/fail2ban/fail2ban/wiki/Configure-action) — port must match `sshd` Port |
| **UFW** | (1) allow 4422/tcp from `10.0.1.0/24`; (2) `ufw allow 'Nginx Full'`; (3) default deny incoming, allow outgoing | **Pass** | [Ubuntu UFW](https://documentation.ubuntu.com/server/how-to/security/firewalls/) — least exposure for SSH; application profile for web |
| **Consequences** | Q1 **b**, Q2 **b**, Q3 **c**, Q4 **b** | **Pass** | Q1: key-only auth lockout without keys. Q2: jail watches wrong port. Q3: disable password auth stops brute force (port change is obscurity). Q4: cron/backdoor hunt — [NIST SP 800-61](https://csrc.nist.gov/pubs/sp/800/61/r2/final) incident eradication |

**CompTIA SY0-701 fit:** **4.1** secure baselines, **4.4** host/application hardening, **2.4** indicator analysis / persistence removal.

**Note:** Non-default SSH port is **defense in depth**, not the most effective single control (Q3 correctly picks key-based auth).

---

## 5. Firewall ACL — Security Operations (`firewall-acl-secops/`)

| Section | Key | Verdict | Primary sources |
|---------|-----|---------|-----------------|
| **ACL table** | R1–R3 permits + R4 deny as documented in scenario README | **Pass** | Least privilege; tiered segmentation; explicit default deny (CompTIA network/security operations) |

**CompTIA SY0-701 fit:** **3.3** network implementation, **4.1** secure configuration, ACL evaluation order.

---

## 6. Ransomware DR — Acme Corp (`ransomware-dr-acme/`)

| Part | Key | Verdict | Primary sources |
|------|-----|---------|-----------------|
| **Step order** | Mobilize → isolate → assess → declare → verify backup → failover warm → restore → validate | **Pass** | NIST SP 800-61 (contain before recovery); DR runbook sequencing |
| **Targets** | RTO 4h · RPO 6h · backup ≤4h · warm site · why not hot = both | **Pass** | RTO/RPO definitions; hot/warm/cold cost vs. recovery time |
| **Trade-offs** | Q1–Q3 all **B** | **Pass** | No ransom (FBI/CISA guidance); CDP for near-zero RPO; eradicate before restore |

**CompTIA SY0-701 fit:** **3.4** resilience / BC-DR; **2.5** incident response; **4.6** recovery.

---

## 7. SIEM ransomware — Sigma & MITRE (`siem-ransomware-mitre/`)

| Part | Key | Verdict |
|------|-----|---------|
| Sigma | **B** (winword → powershell -enc) | **Pass** | Sigma parent-child correlation |
| MITRE table | See scenario README | **Pass** | MITRE ATT&CK mapping |
| Containment | A001+A002 · isolate A002 · SOAR isolate workflow | **Pass** | NIST IR contain before impact; CISA ransomware guidance (no ransom) |

**CompTIA SY0-701 fit:** **2.4** analysis; **2.5** incident response; **3.2** SIEM/SOAR; **4.5** detection engineering.

---

## References (quick list)

| Topic | Reference |
|-------|-----------|
| Zero Trust | NIST SP 800-207 |
| TLS / PKI | RFC 8446; NIST SP 800-57, SP 800-63B |
| LLM / RAG | OWASP Top 10 for LLM Applications 2025 |
| Linux hardening | OpenSSH, fail2ban, Ubuntu Server firewall docs |
| Incident response | NIST SP 800-61 |

---

## Maintenance

Re-run this audit when:

- Answer keys in `sections/*.html` change
- CompTIA releases a new exam version
- OWASP LLM Top 10 or NIST 800-63 revisions alter password/AI guidance

After key edits: `npm run build:pbq-suite`

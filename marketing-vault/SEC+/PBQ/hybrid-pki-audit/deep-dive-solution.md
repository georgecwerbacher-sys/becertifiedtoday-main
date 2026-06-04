---
type: pbq-scenario-solution
exam: SY0-701
scenario: hybrid-pki-audit
last_updated: 2026-06-04
---

# Hybrid PKI audit — deep dive solution

> Sources: RFC 8446 (TLS 1.3), NIST SP 800-63B (passwords), NIST SP 800-57 / CA/Browser Forum (SHA-1 deprecation), NIST SP 800-38D (GCM).

---

## Part 1 — TLS chain for api.becertifiedtoday.com

**Order (top → bottom):**

1. **BeCertifiedToday Root CA** (trust anchor)
2. **Azure Issuing CA** (intermediate that signed the API leaf)
3. **Leaf: api.becertifiedtoday.com**

**Leave in bank (not in this chain):**

- **On-Prem Issuing CA** — SHA-1 intermediate; wrong path for API TLS validation.
- **Code Signing leaf** — different EKU/purpose; expired; issued under on-prem SHA-1 chain.

**Why order matters:** TLS clients walk **issuer → subject** from anchor to EE cert; API hostname must match leaf SAN/CN.

---

## Part 2 — Algorithms

| Use case | Correct | Explanation |
|----------|---------|-------------|
| TLS 1.3 key exchange (forward secrecy) | **ECDHE** or **DHE** | Ephemeral DH provides **perfect forward secrecy**; TLS 1.3 deprecates static RSA key transport. |
| Password hashing (identity DB) | **bcrypt** | Adaptive, salted, slow — resists offline brute force (NIST 800-63B spirit). |
| Intermediate CA certificate signing | **SHA-256** | SHA-1 signatures deprecated for certificates; SHA-256 is standard minimum. |
| Encrypting files at rest (Azure Blob) | **AES-256-GCM** | Authenticated encryption (confidentiality + integrity); upgrade from AES-128-CBC acceptable. |

**Distractor logic**

| Wrong option | Why |
|--------------|-----|
| RSA-2048 (same) for TLS KEX | Not ephemeral FS model for TLS 1.3 handshake. |
| AES-256-GCM as “key exchange” | Symmetric cipher, wrong layer. |
| SHA-256 for passwords | Fast hash — unsuitable for password storage. |
| MD5 / SHA-1 for CA signing | Broken or deprecated. |
| RSA-4096 for bulk blob encrypt | Asymmetric encryption wrong for bulk data at rest. |
| 3DES | Legacy; NIST deprecated. |

---

## Part 3 — Immediate revocation (check both)

| Certificate | Revoke? | Reason |
|-------------|---------|--------|
| **Code Signing Cert** | **YES** | Expired 2024-11-30, RSA-1024 weak; remove from trust stores / audit hygiene. |
| **On-Prem Issuing CA** | **YES** | SHA-1 signing algorithm; issued weak code-signing leaf. |
| Root CA | NO | Valid SHA-256, offline, long-lived anchor. |
| api.becertifiedtoday.com leaf | NO | Valid SHA-256 leaf for production API. |
| Azure Issuing CA | NO | Valid SHA-256 intermediate for API chain. |

**Production nuance (in-app pass message):** Stand up a **SHA-256 replacement intermediate**, re-issue affected certs, **then** retire the weak CA. The PBQ still selects on-prem intermediate for **immediate revocation** to satisfy audit findings and stop trusting SHA-1 issuers.

**After revocation:** Publish updated **CRL** within **7-day** policy (stem: CRL was 11 days stale).

---

## Quick reference

```
Chain:   root-ca → azure-inter-ca → leaf-api
Algos:   ecdhe|dhe | bcrypt | sha256 | gcm
Revoke:  code-sign + onprem-inter
```

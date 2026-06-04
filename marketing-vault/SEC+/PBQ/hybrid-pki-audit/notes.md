---
type: pbq-scenario-notes
exam: SY0-701
scenario: hybrid-pki-audit
title: Hybrid PKI audit
status: production
last_updated: 2026-06-04
---

# Hybrid PKI audit — notes

## What this lab tests

Post-audit remediation for **BeCertifiedToday hybrid PKI**:

1. Build correct **TLS chain** for `api.becertifiedtoday.com` (drag three certs).
2. Pick correct **algorithms** for four use cases (TLS KEX, password hash, CA signing, blob encryption).
3. Select certificates requiring **immediate revocation** (multi-select).

Stem facts: offline root, on-prem + Azure intermediates, **SHA-1** on-prem intermediate, **expired** weak code-signing leaf, **CRL 11 days old** (max 7).

## SY0-701 alignment

| Theme | Lab element |
|-------|-------------|
| **1.4** Cryptography | Symmetric vs asymmetric use; hashing vs encryption |
| PKI | Chain of trust, intermediate CA, leaf EE cert |
| Certificate management | Expiry, weak key sizes, CRL freshness |
| TLS | Forward secrecy (TLS 1.3 / ECDHE) |

## Page structure

| Section | Task |
|---------|------|
| `pki-p1` | Chain ladder: root → intermediate → leaf |
| `pki-p2` | Four algorithm dropdowns |
| `pki-p3` | Revocation checkboxes |

**Previous:** [[../zero-trust-zta-migration/notes|ZTA]] · **Next:** [[../ubuntu-ssh-breach-hardening/notes|Ubuntu SSH]]

## Certificates in the bank

| Token | Role in story |
|-------|----------------|
| Root CA | Trust anchor (SHA-256, offline) |
| Azure Issuing CA | Valid intermediate for API leaf |
| On-Prem Issuing CA | SHA-1 — audit finding |
| api.becertifiedtoday.com leaf | Valid TLS leaf |
| Code Signing leaf | Expired, RSA-1024, on-prem issued |

## Preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/hybrid-pki-audit/hybrid-pki-audit.html#pki-p1
```

→ [[recommendations]] · [[deep-dive-solution]]

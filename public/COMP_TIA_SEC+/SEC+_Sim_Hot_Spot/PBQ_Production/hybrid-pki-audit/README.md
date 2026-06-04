# BeCertifiedToday hybrid PKI audit (PBQ)

SY0-701 performance-based practice: certificate chain ordering, algorithm remediation, and immediate revocation after a PKI audit.

## Chain

| File | Part |
|------|------|
| `hybrid-pki-audit-part1.html` | Drag certs into api.becertifiedtoday.com TLS chain (root → Azure inter → leaf) |
| `hybrid-pki-audit-part2.html` | Select correct algorithm per use case (4 rows) |
| `hybrid-pki-audit-part3.html` | Select all certs requiring immediate revocation |

**Previous scenario:** [zero-trust-zta-migration](../zero-trust-zta-migration/) Part 3 → Part 1 here.

## Answer key

**Part 1:** Root CA → Azure Issuing CA → api.becertifiedtoday.com leaf

**Part 2:** ECDHE · bcrypt · SHA-256 · AES-256-GCM

**Part 3:** Revoke Code Signing Cert + On-Prem Issuing CA (not root, API leaf, or Azure inter)

## Preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/hybrid-pki-audit/hybrid-pki-audit-part1.html
```

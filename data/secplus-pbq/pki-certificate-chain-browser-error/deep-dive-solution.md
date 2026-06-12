---
type: pbq-scenario-solution
exam: SY0-701
scenario: pki-certificate-chain-browser-error
last_updated: 2026-06-05
---

# PKI Certificate Chain — Browser Error — deep dive solution

> `NET::ERR_CERT_AUTHORITY_INVALID` on intranet TLS — find cause and fix.

---

## Step 1 — Match the error code to the problem class

| Browser error | Typical cause |
|---------------|---------------|
| **ERR_CERT_AUTHORITY_INVALID** | Browser cannot build trust to a known root CA |
| ERR_CERT_COMMON_NAME_INVALID | Hostname/CN/SAN mismatch |
| Expired cert | Date validity failure (different warning text) |

Stem specifies **AUTHORITY_INVALID**, not name mismatch or expiry.

---

## Step 2 — Walk the chain in the exhibit

Valid TLS path:

1. **Root CA** (in OS/browser trust store)
2. **Intermediate CA** (signed by root; **must be sent by server**)
3. **End-entity cert** (`intranet.example.com`)

If the server presents only the leaf cert, the browser cannot link the issuer to a trusted root.

---

## Step 3 — Select cause and fix

**Correct: B** — Server is **not sending the intermediate CA certificate**.

**Fix options:**

1. Configure the web server to serve the **full chain** (leaf + intermediate).
2. Distribute the enterprise **root CA** to managed endpoints via **Group Policy** (common on intranet PKI).

---

## Step 4 — Eliminate distractors

| Choice | Why wrong |
|--------|-----------|
| A — CN mismatch / wildcard | Produces COMMON_NAME_INVALID, not authority invalid |
| C — Expired cert | Different browser warning; exhibit lists separate error |
| D — Disable OCSP stapling | Does not repair incomplete or untrusted chain |

---

## Exam takeaway

Authority errors = **trust path** problems. Fix the **chain presentation** or **client trust store**, not hostname or revocation stapling alone.

**Related lab:** [[../hybrid-pki-audit/notes|Hybrid PKI audit]] (chain order, algorithms, revocation)

**Objectives:** 1.4 PKI · TLS trust paths

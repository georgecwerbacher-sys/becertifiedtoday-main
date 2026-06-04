---
type: pbq-scenario-recommendations
exam: SY0-701
scenario: hybrid-pki-audit
last_updated: 2026-06-04
---

# Hybrid PKI audit — recommendations

## For learners

1. **Chain task = path validation for one purpose** (TLS to API host), not “use every cert in the bank.”
2. **Algorithm row:** read the *use case* column first — AES-256-GCM is not a TLS *key exchange*.
3. TLS 1.3 → think **ECDHE or DHE** (forward secrecy); static RSA key transport is legacy.
4. Password storage → **slow salted hash** (bcrypt), not SHA-256 alone.
5. Revocation: distinguish **audit “revoke now”** vs production **migrate then retire** (explained in pass message).

## For instructors

| Priority | Recommendation |
|----------|----------------|
| High | Draw one chain on whiteboard: Root → Azure Inter → Leaf; cross out On-Prem SHA-1 path. |
| Medium | Part 2: explain why SHA-512 for CA is acceptable but SHA-256 is the keyed “minimum.” |
| Low | Link to browser `ERR_CERT_AUTHORITY_INVALID` standalone PBQ in `SEC+_PBQ/` for reinforcement. |

## For product

- Show **CRL age** countdown in exhibit (11 vs 7 days) — already in stem; could animate on Submit.
- After Part 3 pass, optional link: “Practice browser PKI error PBQ” (`pki-certificate-chain-browser-error.html` in public bank).

## Vault / ops

- Algorithm keys live in `sections/pki-p2.html` — document ECDHE **or** DHE acceptance in [[deep-dive-solution|deep dive]] only (already there).
- Rebuild: `npm run build:pbq-suite` after section edits.

## Exam prep positioning

- Strong fit for **federal/defense** audience studying PKI + TLS ([[../../01-strategy/security-plus-federal-defense-foundation|Security+ federal foundation]]).

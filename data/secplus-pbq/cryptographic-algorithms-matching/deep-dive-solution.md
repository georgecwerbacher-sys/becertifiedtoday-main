---
type: pbq-deep-dive
exam: SY0-701
scenario: cryptographic-algorithms-matching
last_updated: 2026-06-22
---

# Cryptographic algorithms matching — solution walkthrough

## Symmetric encryption

- **AES** — modern block cipher for bulk data at rest and in transit (WPA2, TLS ciphersuites).
- **3DES** — legacy triple-DES; stronger than single DES but deprecated in favor of AES.

## Asymmetric cryptography

- **RSA** — widely used for key exchange and encryption with large public keys.
- **ECC** — elliptic-curve asymmetric crypto; smaller keys with comparable strength to RSA.
- **Diffie-Hellman** — establishes shared secrets over an insecure channel without sending the key itself.

## Hashing and integrity

- **SHA-256** — current standard hash for file integrity and certificate fingerprints.
- **MD5** — fast but collision-prone; unsuitable for security-sensitive integrity checks.
- **HMAC** — hash-based message authentication code; proves authenticity with a shared secret key.

## Passwords and signatures

- **PBKDF2** — password-based key derivation; applies salts and iteration counts to slow offline cracking.
- **DSA** — digital signature algorithm for creating and verifying non-repudiation signatures.

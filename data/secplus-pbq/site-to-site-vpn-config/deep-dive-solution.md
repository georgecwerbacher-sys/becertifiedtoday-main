---
type: pbq-deep-dive
exam: SY0-701
scenario: site-to-site-vpn-config
last_updated: 2026-06-22
---

# Site-to-site VPN — solution walkthrough

## Phase 1 (IKE) — secure the management channel

Both gateways need matching IKE proposals:

- **Pre-Shared Key** — standard for site-to-site when PKI is not required.
- **AES** — current symmetric choice; avoid 3DES/DES.
- **SHA-256** — strong integrity for IKE; avoid MD5/SHA-1.
- **DH Group 14** — 2048-bit MODP; stronger than Group 2/5.
- **Peer IP** — opposite site's **public** address (`5.5.5.20` from HQ1, `5.5.5.10` from HQ2).

## Phase 2 (IPsec) — protect the traffic

Define what crosses the tunnel:

- **Local / Remote subnets** — mirror between sites (`192.168.10.0/24` ↔ `192.168.20.0/24`).
- **ESP** — encrypts payload and provides integrity; preferred over AH (no encryption) or plain GRE.
- **AES + SHA-256** — same modern crypto as Phase 1 for the data plane.

If Phase 1 and Phase 2 settings disagree, the tunnel will not establish even when subnets and peer IPs are correct.

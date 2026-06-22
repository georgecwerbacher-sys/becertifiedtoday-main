# Site-to-Site VPN Tunnel Configuration

**SY0-701 PBQ · dual-gateway IPsec configuration**

Configure Phase 1 (IKE) and Phase 2 (IPsec) on both VPN gateways for HQ1 (`192.168.10.0/24`, public `5.5.5.10`) and HQ2 (`192.168.20.0/24`, public `5.5.5.20`).

## Answer key (both gateways)

| Setting | HQ 1 | HQ 2 |
|---------|------|------|
| **Phase 1 — Auth** | Pre-Shared Key | Pre-Shared Key |
| **Phase 1 — Encryption** | AES | AES |
| **Phase 1 — Hash** | SHA-256 | SHA-256 |
| **Phase 1 — DH Group** | Group 14 | Group 14 |
| **Phase 1 — Peer IP** | `5.5.5.20` | `5.5.5.10` |
| **Phase 2 — Local subnet** | `192.168.10.0/24` | `192.168.20.0/24` |
| **Phase 2 — Remote subnet** | `192.168.20.0/24` | `192.168.10.0/24` |
| **Phase 2 — Protocol** | ESP | ESP |
| **Phase 2 — Encryption** | AES | AES |
| **Phase 2 — Hash** | SHA-256 | SHA-256 |

**Status:** Pending — not in `PBQ_Production` build chain.

## Pending chain

- **Previous:** [`../../PBQ_Production/cryptographic-algorithms-matching/`](../../PBQ_Production/cryptographic-algorithms-matching/cryptographic-algorithms-matching.html) *(production)*
- **Next:** [`../web-app-subnet-zoning/`](../web-app-subnet-zoning/)

## Preview

http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/pending/site-to-site-vpn-config/site-to-site-vpn-config.html

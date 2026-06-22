# SEC+ Site-to-Site VPN Configuration

**SY0-701 PBQ · dual-gateway IPsec configuration**

Configure Phase 1 (IKE) and Phase 2 (IPsec) on both VPN gateways for **BeCertifiedToday.com** BCT_HQ1 (`172.16.50.0/24`, public `198.51.100.41`) and BCT_HQ2 (`172.16.60.0/24`, public `198.51.100.52`).

## Answer key (both gateways)

| Setting | BCT_HQ1 | BCT_HQ2 |
|---------|---------|---------|
| **Phase 1 — Auth** | Pre-Shared Key | Pre-Shared Key |
| **Phase 1 — Encryption** | AES | AES |
| **Phase 1 — Hash** | SHA-256 | SHA-256 |
| **Phase 1 — DH Group** | Group 14 | Group 14 |
| **Phase 1 — Peer IP** | `198.51.100.52` | `198.51.100.41` |
| **Phase 2 — Local subnet** | `172.16.50.0/24` | `172.16.60.0/24` |
| **Phase 2 — Remote subnet** | `172.16.60.0/24` | `172.16.50.0/24` |
| **Phase 2 — Protocol** | ESP | ESP |
| **Phase 2 — Encryption** | AES | AES |
| **Phase 2 — Hash** | SHA-256 | SHA-256 |

## Chain position

- **Previous:** [`../network-protocols-matching/`](../network-protocols-matching/network-protocols-matching.html)
- **Next:** [`../web-app-subnet-zoning/`](../web-app-subnet-zoning/web-app-subnet-zoning.html)

## Preview

http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/site-to-site-vpn-config/site-to-site-vpn-config.html

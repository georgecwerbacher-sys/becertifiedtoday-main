---
type: pbq-scenario-notes
exam: SY0-701
scenario: vpc-payment-architecture
last_updated: 2026-06-22
---

# VPC payment architecture

Cloud VPC diagram with custom slot menus — place WAF, load balancers, app instances, and database; label middle tier subnet.

## SY0-701 mapping

- **3.1** — secure network architecture and segmentation
- **3.2** — cloud and virtualization security

## Answer key

| Node | Component |
|------|-----------|
| 1 | Load Balancer |
| 2 | WAF |
| 3 | Load Balancer |
| 4 | Autoscaling Instance |
| 5 | Instance |
| 6 | Instance |
| 7 | Database |
| Middle tier subnet | Private subnet |

Node 8 is decorative (no answer required).

**Status:** Production — chain #34, linked on `SEC+_Training_Portal.html` (Network & Zero Trust).

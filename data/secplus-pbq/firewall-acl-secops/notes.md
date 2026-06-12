---
type: pbq-scenario-notes
exam: SY0-701
scenario: firewall-acl-secops
title: Firewall ACL Configuration — Security Operations
status: production
last_updated: 2026-06-04
---

# Firewall ACL — Security Operations — notes

## What this lab tests

Configure **four top-down inbound ACL rules** for a two-tier internal network:

- **Web** `10.0.0.10` — HTTP/HTTPS from any source
- **DB** `10.0.0.20` — MySQL (3306) only from web server
- **Implicit deny** — all other inbound traffic denied

## SY0-701 alignment

| Theme | Coverage |
|-------|----------|
| **3.3** Network security | ACLs, least privilege, tiered segmentation |
| **4.1** Secure baselines | Default deny, explicit permits |
| Security operations | Rule order, first-match semantics |

## Page structure

| Section ID | Content |
|------------|---------|
| `firewall-acl-config` | Policy box + 4-row ACL table (row 4 fixed ANY + DENY action) |

**Previous:** [[../ubuntu-ssh-breach-hardening/notes|Ubuntu SSH]] · End of chain.

## Local preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/firewall-acl-secops/firewall-acl-secops.html
```

→ [[recommendations]] · [[deep-dive-solution]]

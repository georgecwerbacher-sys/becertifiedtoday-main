---
type: pbq-scenario-notes
exam: SY0-701
scenario: zero-trust-zta-migration
title: Zero Trust Architecture migration
status: production
last_updated: 2026-06-04
---

# Zero Trust migration — notes

## What this lab tests

Three-part **Zero Trust Architecture (ZTA)** migration for BeCertifiedToday:

1. Fundamental shift vs traditional perimeter (MCQ + exhibit).
2. **Zone map** — pick the best control per slot (two options per row, eight slots across four zones).
3. **Trade-off MCQs** — ZTNA vs VPN, PAM placement, east-west traffic.

Primary reference framed in the UI: **NIST SP 800-207**.

## SY0-701 alignment

| Objective area | Coverage |
|----------------|----------|
| **1.2** Security principles & Zero Trust | Never trust / always verify; PEP; policy engine/administrator; adaptive identity |
| **3.x** Enterprise architecture | Segmentation types in exhibit (VLAN, DMZ, SDN, air-gap) |
| Access control | ZTNA least privilege vs VPN; JIT + PAM for privileged access |
| Cloud security | CASB + DLP for SaaS/shadow IT |

## Page structure

| Section ID | Content |
|------------|---------|
| `zta-exhibit` | Traditional perimeter vs ZTA + segmentation glossary (modal/popup) |
| `zta-concept` or `zta-p1` | Fundamental change MCQ |
| `zta-p2` | Zone control map (8 slots, best-of-two per row) |
| `zta-p3` | Three trade-off MCQs |

**Previous:** [[../acme-rag-hr-ai/notes|BeCertifiedToday RAG]] · **Next:** [[../hybrid-pki-audit/notes|Hybrid PKI]]

## Zone map (correct placement)

| Zone | Controls |
|------|----------|
| Internet (untrusted) | ZTNA Gateway |
| DMZ / edge | Identity Provider, Continuous Auth |
| Internal | Micro-segmentation, PAM Vault, JIT Access |
| Cloud (Azure / SaaS) | CASB, DLP Proxy |

## Grading

- Part 1: **B**
- Part 2: every slot `data-correct` must match the selected radio value
- Part 3: Q1–Q3 all **B**

## Verification

NIST SP 800-207 + CISA ZT microsegmentation guidance — see `PBQ_Production/VERIFICATION.md`.

## Preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/zero-trust-zta-migration/zero-trust-zta-migration.html#zta-p2
```

→ [[recommendations]] · [[deep-dive-solution]]

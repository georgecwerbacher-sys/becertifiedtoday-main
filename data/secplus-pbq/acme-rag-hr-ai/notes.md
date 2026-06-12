---
type: pbq-scenario-notes
exam: SY0-701
scenario: acme-rag-hr-ai
title: BeCertifiedToday RAG HR AI
status: production
last_updated: 2026-06-04
---

# BeCertifiedToday RAG HR AI — notes

## What this lab tests

Candidates secure a **retrieval-augmented generation (RAG)** HR policy assistant: architecture controls, guardrails, attack-to-mitigation mapping, then three **AI-specific** MCQs (prompt injection, data poisoning, model inversion).

Fictional employer: **BeCertifiedToday** (consistent with other PBQ_Production scenarios).

## SY0-701 alignment (themes)

| Domain theme | How the lab exercises it |
|--------------|---------------------------|
| Secure architecture / least privilege | Private vector API, RBAC retrieval, approved corpus only |
| Data protection | No training on chats, redacted audit logs, PII output filtering |
| Threats (emerging) | LLM01-style injection, indirect injection via documents, poisoning, inference abuse |
| Governance | Ingestion approval, classification metadata, rate limits |

CompTIA does not publish a canonical “RAG PBQ”; this lab maps to **general security concepts** and **architecture** objectives plus current industry guidance (OWASP LLM Top 10 2025).

## Page structure (one HTML, folder sections)

| Section ID | Task |
|------------|------|
| `acme-exhibits` | Architecture + linked exhibits (corpus, chat, chunk, poisoned PDF) |
| `acme-config` | Six configuration dropdowns |
| `acme-guardrails` | Eight enable/disable toggles |
| `acme-attacks` | Five attack → mitigation selects (grades config + guardrails too) |
| `acme-p2` | Three MCQs with exhibits |

**Source:** `public/.../PBQ_Production/acme-rag-hr-ai/sections/`  
**Chain next:** [[../zero-trust-zta-migration/notes|Zero Trust migration]]

## Exhibits (Part 1)

- **A — Corpus index:** compensation/leave docs in index → sets up unauthorized disclosure (atk-5).
- **B — Chat log:** direct prompt injection attempt.
- **C — Retrieved chunk:** cross-department data in answer.
- **D — Quarantined PDF:** hidden instructions in indexed layer (indirect injection / poisoning).

## Grading model

- Part 1 sections: per-control match against keyed values; attacks section also requires prior config + guardrails correct.
- Part 2: all three MCQs must be **B**.

## Verification status

Keys audited 2026-06-04 against OWASP LLM guidance — see repo `PBQ_Production/VERIFICATION.md` and [[deep-dive-solution|deep dive]].

## Local preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/acme-rag-hr-ai/acme-rag-hr-ai.html
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/acme-rag-hr-ai/acme-rag-hr-ai.html#acme-config
```

→ [[recommendations]] · [[deep-dive-solution]]

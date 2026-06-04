---
type: pbq-scenario-recommendations
exam: SY0-701
scenario: acme-rag-hr-ai
last_updated: 2026-06-04
---

# BeCertifiedToday RAG HR AI — recommendations

## For learners (exam prep)

1. **Treat retrieved text as untrusted data**, not as system instructions — this single idea unlocks config, guardrails, atk-2, and prompt-injection MCQ.
2. **Separate controls by attack phase:** input (injection classifier), ingest (approval + sanitize), runtime (RBAC retrieval, rate limits), output (PII redaction).
3. On model inversion, prioritize **rate limiting + output redaction** for RAG; differential privacy applies mainly if you **train** on sensitive data (this lab sets `no-train`).
4. Review exhibits before Task 3 — attack rows reference Exhibit B/D explicitly.

## For instructors / content

| Priority | Recommendation |
|----------|----------------|
| High | Add a one-line “trust boundary” callout on the architecture exhibit (system prompt ≠ user ≠ retrieved). |
| Medium | In Show Answer for `acme-attacks`, briefly say why MD5-hashing PDFs or WAF-on-UI are insufficient distractors. |
| Low | Optional fourth MCQ on **LLM06 Excessive Agency** (unrestricted tools toggle already in guardrails). |

## For product / site

- Surface **section progress** on the folder sidebar (checkmarks when config/guardrails/attacks pass).
- Link from [[../README|PBQ index]] to this vault folder for “solutions study guide” (gated or post-submit).
- When publishing to `SEC+_PBQ/`, keep slug `acme-rag-hr-ai` for URL stability in ads/YouTube.

## For sourcing / competitive positioning

- Maps to OWASP **LLM01, LLM04, LLM08** — cite in landing copy as “RAG + vector store hardening,” not generic “AI security.”
- Differentiator vs dump sites: **interactive** guardrail toggles + exhibit-linked attacks; document in [[../../11-question-sourcing/pbq/secplus-pbq-not-in-bct|net-new log]].

## Maintenance triggers

- OWASP LLM Top 10 revision → re-read [[deep-dive-solution|deep dive]] and `VERIFICATION.md`.
- Any change to `sections/acme-*.html` → `npm run build:pbq-suite`.

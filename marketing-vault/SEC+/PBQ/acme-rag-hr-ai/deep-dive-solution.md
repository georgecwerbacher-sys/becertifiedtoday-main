---
type: pbq-scenario-solution
exam: SY0-701
scenario: acme-rag-hr-ai
last_updated: 2026-06-04
---

# BeCertifiedToday RAG HR AI — deep dive solution

> Full keyed walkthrough. Sources: OWASP Top 10 for LLM Applications 2025, OWASP LLM Prompt Injection Prevention Cheat Sheet. Not third-party exam dumps.

---

## Task 1 — System configuration

| Control | Correct value | Why |
|---------|---------------|-----|
| Vector database API exposure | **Private network only; authentication + RBAC on every query** | Public/anonymous APIs expose embeddings and chunks; API keys in browser are extractable. |
| Retrieval authorization | **Filter by user role and document classification** | Top-k over the whole index causes cross-department disclosure (Exhibit C / atk-5). |
| Document corpus scope | **Approved HR policy repository only** | Ad-hoc or full file-share indexing expands poisoning and leakage surface. |
| Prompt / conversation retention for training | **Do not train or fine-tune on prompts or retrieved text** | Minimizes memorization and regulatory risk; supports inversion defense story in Part 2. |
| Audit logging | **Log queries and sources with PII redaction** | Plain-text full logging increases breach impact; no logging blocks forensics. |
| Retrieved context handling | **Treat retrieved text as untrusted data; isolate from system instructions** | Core OWASP LLM01 mitigation for **indirect** injection via RAG. |

**Wrong-pattern traps:** “Trust index labels without re-checking identity,” “anonymous read for speed,” “treat policy text as trusted system instructions.”

---

## Task 2 — Guardrails

| Guardrail | State | Why |
|-----------|-------|-----|
| Prompt injection / jailbreak detection (input) | **ON** | Blocks direct override attempts (Exhibit B). |
| Output filter for PII / sensitive HR fields | **ON** | Limits disclosure even if retrieval over-fetches. |
| Enforce classification filter at retrieval | **ON** | Enforces ABAC/RBAC at retrieval time. |
| Per-user rate limiting (chat + retrieval APIs) | **ON** | Primary defense against inversion-style probing (Part 2). |
| Scan and quarantine documents at ingestion | **ON** | Supports poisoned-document detection. |
| Allow anonymous access | **OFF** | HR data requires authenticated subjects. |
| Debug mode: return full system prompt | **OFF** | Prevents LLM07-style leakage. |
| Unrestricted outbound tools (email, HTTP fetch) | **OFF** | LLM06 excessive agency — exfiltration path. |

---

## Task 3 — Attack mitigations

| Scenario | Correct mitigation | Why others fail |
|----------|-------------------|-----------------|
| Direct prompt injection (“ignore previous instructions…”) | **Input sanitization + prompt-injection guardrail** | Output-only DLP runs after damage; firewall/TLS rotation do not parse prompts. |
| Hidden instructions in uploaded “policy” PDF (indexed) | **Sanitize at ingestion; treat retrieved text as untrusted** | AV on laptops does not scan server index; MD5 alone does not remove instruction text; disabling RAG is not a business fix. |
| Compromised ingest account injects malicious embeddings | **Validate sources; least-privilege ingest; integrity checks on embeddings** | WAF in front of chat UI does not protect ingest pipeline; spam filter irrelevant. |
| Model inversion–style probing of embedding store | **Minimize sensitive data in corpus; output DLP; query rate limits** | AES-only on index does not stop inference via queries; “theoretical only” is false. |
| Manager sees another department’s leave balances | **RBAC + classification filtering at retrieval** | VPN does not filter chunks; short answers do not fix authorization. |

**Grading note:** This section also checks that Task 1 config and Task 2 guardrails are already correct.

---

## Part 2 — MCQs (all **B**)

### Prompt injection

**Correct (B):** Separate system prompt from user input; input sanitization; dedicated injection classifier for override patterns.

| Choice | Verdict |
|--------|---------|
| A — Block one phrase | Bypassed by paraphrase; not scalable. |
| C — Longer system prompt | Does not remove trust-boundary flaw. |
| D — HTTPS only | Protects transport, not instruction override in app layer. |

### Data poisoning

**Correct (B):** Hash verification + authorized-reviewer workflow for ingestion + anomaly detection on output drift.

| Choice | Verdict |
|--------|---------|
| A — Encrypt vector DB at rest | Confidentiality, not integrity of content. |
| C — MFA for queriers | Authenticates users, not document trust. |
| D — AV scan only | Misses malicious **policy text** that is not malware. |

### Model inversion

**Correct (B):** Per-user rate limiting, output PII redaction; differential privacy **if** training on sensitive data (secondary here because config is **no-train**).

| Choice | Verdict |
|--------|---------|
| A — CAPTCHA only | Slows casual abuse; scripted probing continues. |
| C — Block PII keywords | Incomplete; attackers rephrase probes. |
| D — Smaller model | Not a primary control; wrong problem framing. |

**Exam sentence to remember:** *RAG makes retrieved content part of the prompt — classify it as data, not instructions.*

---

## Quick reference card

```
Config:  secure | filter | approved | no-train | redact | untrusted
Guards:  ON injection, PII-out, retrieval-filter, rate-limit, ingest-scan
         OFF anonymous, debug-prompts, external-tools
Attacks: input-guard | ingest-sanitize | ingest-controls | minimize-dlp | rbac-retrieval
MCQ:     B | B | B
```

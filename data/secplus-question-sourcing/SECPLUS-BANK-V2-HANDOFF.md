# Security+ (SY0-701) — PDF check & question verification handoff

**Goal:** Repeat the CCNAAUTO v2 question-bank workflow for Sec+: official PDF anchor, blueprint diff, schema v2 topic map with Tier A verification, 100-question banks by domain weight, obsolete handling.

**Do not** center competitor scraping on the public verification story. Tier A sources only (CompTIA official, NIST, IETF, OWASP as appropriate).

---

## Reference implementation (CCNAAUTO — done)

| Piece | Path |
|-------|------|
| Question bank template | `templates/question-bank/README.md` |
| Blueprint weights | `public/CCNAAUTO-Study/data/ccnaauto-practice-bank-blueprint.json` |
| PDF diff log | `public/CCNAAUTO-Study/data/ccnaauto-blueprint-v1-changes.json` |
| Topic map v2 | `public/CCNAAUTO-Study/data/ccnaauto-question-topic-map.json` |
| Tracker (generated) | `public/CCNAAUTO-Study/data/ccnaauto-question-topic-tracker.json` |
| Tracker build | `npm run build:ccnaauto-tracker` |
| Practice hub | `public/CCNAAUTO-Study/js/ccnaauto-practice-hub.js` |
| Verification marketing page | `public/how-we-verify-questions.html` |
| Cursor rule | `.cursor/rules/question-bank-template.mdc` |

---

## Sec+ current state

| Piece | Status | Path |
|-------|--------|------|
| Question HTML | **~1005 files** | `public/COMP_TIA_SEC+/SEC+_Questions/` |
| Topic map | **Schema v1** (objective arrays only, no verification) | `public/COMP_TIA_SEC+/data/secplus-question-topic-map.json` |
| Objectives JSON | **SY0-701 v5.0** domains + objective text | `public/COMP_TIA_SEC+/data/secplus-exam-objectives-sy0-701.json` |
| Practice hub | Banks of 100, 11 bank cards, **no domain weight table** | `public/COMP_TIA_SEC+/js/secplus-practice-hub.js` |
| Portal | Static bank grid | `public/COMP_TIA_SEC+/SEC+_Training_Portal.html` |
| Blueprint JSON | **Missing** | (create `secplus-practice-bank-blueprint.json`) |
| PDF diff JSON | **Missing** | (create e.g. `secplus-blueprint-sy0-601-to-701-changes.json`) |
| Tracker script | **Not wired** | extend `scripts/build-question-bank-tracker.py` |
| PBQ verification model | NIST / CompTIA themes | `public/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/VERIFICATION.md` |

### SY0-701 v5.0 domain weights (per 100 Q)

| Domain | Weight | Target / bank |
|--------|-------:|--------------:|
| 1.0 General Security Concepts | 12% | 12 |
| 2.0 Threats, Vulnerabilities, and Mitigations | 22% | 22 |
| 3.0 Security Architecture | 18% | 18 |
| 4.0 Security Operations | 28% | 28 |
| 5.0 Security Program Management and Oversight | 20% | 20 |

Source PDF name in objectives JSON: `CompTIA-Security-Plus-SY0-701-Exam-Objectives.pdf`

---

## Suggested work order (new chat)

### Phase 1 — Infrastructure (same pattern as CCNAAUTO)

1. Create `public/COMP_TIA_SEC+/data/secplus-practice-bank-blueprint.json` from objectives JSON + CompTIA Tier A `verificationPolicy` hosts (`comptia.org`, `learn.comptia.org`, plus NIST `nist.gov`, etc. as configured).
2. Add `--track secplus` to `scripts/build-question-bank-tracker.py`; run first tracker against **existing v1 map** (counts only).
3. Wire portal **domain weight table** + tracker-driven summary (reuse `public/js/bcc-question-bank-utils.js` + CCNAAUTO hub patterns).
4. Update `.cursor/rules/question-bank-template.mdc` / answer-verification rule for **CompTIA Tier A** (not Cisco-only).

### Phase 2 — PDF comparison

1. Obtain / locate official PDFs: **SY0-601** (retired) vs **SY0-701 v5.0** (current).
2. Build structured diff JSON (renames, removals, new objectives) like `ccnaauto-blueprint-v1-changes.json`.
3. Flag questions mapped only to dropped/changed objectives → **obsolete archive** (do not serve in default SY0-701 pools).

### Phase 3 — Question verification (phased; 1000+ items)

1. Define schema v2 migration for `secplus-question-topic-map.json`: `objectives`, `subObjectives`, `blueprintVersion`, `verification.sources`.
2. Pilot batch: verify keys on Tier A sources for **Bank 1** (first 100 slugs) or one domain (e.g. 4.0 Operations at 28%).
3. Run `npm run lint:question-urls` after any HTML edits.
4. Expand verification in batches; tracker reports `missing_verification` until complete.

### Phase 4 — Docs & site copy

1. Extend `how-we-verify-questions.html` with Sec+ example (domain table already uses CCNAAUTO; add SY0-701 row or swap).
2. Guest copy rules: first-person persuasive, **no em/en dashes** (`marketing-research/Website_Main/Question Verification.md`).

---

## CompTIA Tier A (verification)

Use for keys and explanations:

- CompTIA exam objectives / official learning content (`comptia.org`, `learn.comptia.org`)
- NIST publications (e.g. SP 800-207 zero trust) where topic is standards-based
- IETF RFCs, OWASP guidance for app/web topics

**Not used:** ExamTopics, braindumps, Reddit recall, competitor practice sites.

---

## Commands (after wiring)

```bash
python3 scripts/build-question-bank-tracker.py --track secplus
npm run lint:question-urls
npm run serve   # portal: COMP_TIA_SEC+/SEC+_Training_Portal.html
```

---

## Scale note

~1005 questions already mapped in v1. Full v2 + verification in one session is unrealistic. Ship **infra + PDF diff + pilot bank** first; migrate verification metadata in domain batches.

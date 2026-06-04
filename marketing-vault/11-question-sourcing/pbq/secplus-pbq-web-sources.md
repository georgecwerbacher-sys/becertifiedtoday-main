---
type: question-source-catalog
exam: SY0-701
content_type: pbq
exam_version: V7
objectives_version: "5.0"
last_updated: 2026-06-03
verify_answers_against: CompTIA official only
---

# SY0-701 PBQ — web source catalog

**Exam:** CompTIA Security+ **SY0-701** (cert **V7**) · **Objectives v5.0**  
**Local bank:** `public/COMP_TIA_SEC+/SEC+_PBQ/` + `public/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/`  
**Workflow:** [[README|PBQ sourcing README]] · `npm run secplus:pbq-monthly`

Same tier policy as [[../secplus-sy0-701-web-sources|MCQ catalog]] — Tier C is discovery only; verify on Tier A before publishing.

---

## Tier A — verification authority (PBQ)

| Source | URL | PBQ count (stated) | Source version | date_added | Notes |
|--------|-----|-------------------|----------------|------------|-------|
| Exam objectives PDF | https://assets.ctfassets.net/82ripq7fjls2/6TYWUym0Nudqa8nGEnegjG/0f9b974d3b1837fe85ab8e6553f4d623/CompTIA-Security-Plus-SY0-701-Exam-Objectives.pdf | — (blueprint) | Objectives v5.0 | 2026-06-03 | Defines performance-based domains |
| CertMaster Practice | https://www.comptia.org/training/certmaster-practice/security-plus | Paid (MCQ + PBQ) | SY0-701 | 2026-06-03 | Official PBQ-style interactions |
| Official Study Guide | https://www.comptia.org/training/books/security-study-guide | Chapter labs / PBQ prep | SY0-701 | 2026-06-03 | Authorized reference |
| CompTIA practice questions (web) | https://www.comptia.org/en-us/certifications/security/practice-questions/ | 10 MCQ samples only | V7 | 2026-06-03 | MCQ verification; not PBQ auto-fetch |

---

## Tier B — legitimate PBQ / sim practice

| Source | URL | PBQ / sim (stated) | Source version | date_added | Notes |
|--------|-----|---------------------|----------------|------------|-------|
| Crucial Exams | https://crucialexams.com/exams/comptia/security/sy0-701/practice-tests-practice-questions | **9 PBQ** + 1400 MCQ | SY0-701 (V7) | 2026-06-03 | [[../../10-competitors/sites/crucial-exams\|crucial-exams]] · `pbq_poll` when sample URL confirmed |
| Professor Messer — Practice Exams | https://www.professormesser.com/amember/signup/sy0701pe | **3 × 90** exams (PBQ + MCQ) | SY0-701 | 2026-06-03 | Paid PDF; widely used PBQ style |
| BCT OpenSSL PBQ landing | `/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/simulation-secure-web-architecture-openssl.html` | 2-part sim | SY0-701 | 2026-06-03 | In-repo reference implementation |
| BCT SEC+_PBQ | `/COMP_TIA_SEC+/SEC+_PBQ/` | Growing set | SY0-701 | 2026-06-03 | security-control-map · log-timeline-forensics |

---

## Tier C — uncredited PBQ recall (discovery only)

| Source | URL | date_added | Notes |
|--------|-----|------------|-------|
| r/CompTIA | https://www.reddit.com/r/CompTIA/ | 2026-06-03 | “What PBQ did you get?” threads — paraphrase only |
| r/SecurityPlus | https://www.reddit.com/r/SecurityPlus/ | 2026-06-03 | Exam experience / sim recall |
| ExamTopics | https://www.examtopics.com/exams/comptia/sy0-701/ | 2026-06-03 | Research index only — Ads negative |

**Import convention:** paste into [[templates/discovered-pbq-import|discovered-pbq-import.csv]] with `topic_notes`: `Tier C research — community recall; verify on CompTIA Tier A only`.

---

## PBQ types to track

| pbq_type | Examples |
|----------|----------|
| `drag-drop` | Security control map, architecture placement |
| `ordered-sequence` | Log timeline forensics, IR kill chain |
| `hotspot` | Click region on diagram |
| `fill-in` | OpenSSL CSR syntax, command fragments |
| `simulation` | Multi-pane dark web, malware outbreak |

When adding a source row, note stated **PBQ count** and **interaction style** so compare net-new stays meaningful.

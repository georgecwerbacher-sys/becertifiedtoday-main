---
type: question-source-catalog
exam: CCNA-200-301
exam_version: v1.1
objectives_version: "1.1"
last_updated: 2026-06-06
verify_answers_against: Cisco official only
catalog_rule: "List practice sources with stated refresh 2026+; drop dated product rows before 2026."
tracker: ../../10-competitors/competitors-ccna-practice-samples-tracker.csv
---

# CCNA 200-301 practice questions — web source catalog

**Exam:** Cisco **CCNA 200-301** (v1.1 blueprint, Aug 2024)  
**Local objectives:** `public/CCNA-Study/data/ccna-exam-objectives-200-301-v1.1.json`  
**In-repo bank:** **~714** MCQ pages under `public/CCNA-Study/CCNA_questions/` (generator: `scripts/gen_ccna_chain_pages.py`)  
**Labs / sim catalog:** [[ccna-labs-sim-web-sources|ccna-labs-sim-web-sources.md]] · `npm run ccna:labs-monthly`

**Policy:** Tier C = discovery only — compare vs BCT, verify on **Cisco Tier A**, draft **original** stems. Never copy verbatim recall or dump text.

| Tier | Use |
|------|-----|
| **A** | **Verify answers** — Cisco docs, Learning Network, exam topics outline |
| **B** | **Discovery + gap analysis** — credited practice sites; `npm run ccna:monthly` when `question_poll.enabled` |
| **C** | **Discovery only** — community recall / dump syndicates; paraphrase; verify on Tier A |

**Poll registry:** `marketing-vault/10-competitors/sites/*-ccna.md` · list: `npm run ccna:poll-sources`  
**Tracker sheet:** [[../../10-competitors/competitors-ccna-practice-samples-tracker.csv|competitors-ccna-practice-samples-tracker.csv]]  
**Runs:** `runs/YYYY-MM-DD-net-new.md`

`date_added` = when this row entered the vault. **Source version / date** = publisher-stated refresh (**2026+** preferred).

---

## Tier A — verification authority

| Source | URL | Q count (stated) | Source version / date | Answers public? | date_added | Notes |
|--------|-----|------------------|------------------------|-----------------|------------|-------|
| Exam topics outline | https://learningnetwork.cisco.com/s/ccna-exam-topics | — (blueprint) | **200-301 v1.1** | N/A | 2026-06-06 | Domain weights; Terraform / AI ops additions |
| CCNA cert hub | https://www.cisco.com/c/en/us/training-events/training-certifications/certifications/associate/ccna.html | — | **200-301** | N/A | 2026-06-06 | Exam metadata, 120 min |
| Cisco Learning Network | https://learningnetwork.cisco.com/s/ccna | Community + resources | Rolling | Partial | 2026-06-06 | Blueprint discussions; not a dump source |
| Official Cert Guide (OCG) | https://www.cisco.com/c/en/us/training-events/training-certifications/exam-voucher/book-exam.html | Chapter review Qs | **200-301** edition | In book | 2026-06-06 | Cisco Press — verify against docs |
| Packet Tracer labs | https://www.netacad.com/courses/packet-tracer | Labs (not MCQ bank) | Rolling | Free | 2026-06-06 | Hands-on; complements BCT CLI labs |
| Certification policies | https://www.cisco.com/c/en/us/training-events/training-certifications/exams/certification-exam-policies.html | — | Policy (ongoing) | N/A | 2026-06-06 | Unauthorized braindump guidance |

---

## Tier B — legitimate practice (verify keys against Tier A)

Poll **on** = included in `npm run ccna:monthly` today. Poll **off** = manual import or enable in site note when parser is ready.

| id | Source | URL | Q count (stated) | Source version / date | Answers public? | Poll | date_added | Site note |
|----|--------|-----|------------------|------------------------|-----------------|------|------------|-----------|
| 1 | OpenExamPrep | https://open-exam-prep.com/practice/ccna | **200+** free MCQs + AI tutor | v1.1 / **2026-06-06** | Yes (on page) | **on** | 2026-06-06 | [[../../10-competitors/sites/open-exam-prep-ccna\|open-exam-prep-ccna]] |
| 3 | Mastery Exam Prep | https://masteryexamprep.com/exams/cisco/ccna/ | **24** public samples; full bank paid | v2.0 / **2026** | Samples yes | **on** | 2026-06-06 | [[../../10-competitors/sites/mastery-exam-prep-ccna\|mastery-exam-prep-ccna]] |
| 4 | Crucial Exams | https://crucialexams.com/exams/cisco/ccna/200-301/practice-tests-practice-questions | **530** MCQ + **7** PBQ; **20** Q free demo | **2026** | In product | off | 2026-06-06 | [[../../10-competitors/sites/crucial-exams-ccna\|crucial-exams-ccna]] |
| 5 | HowToNetwork | https://www.howtonetwork.com/free/cisco-ccna-exam-walkthrough/ | **103** Q walkthrough (H5P) | **2026** | After submit | off | 2026-06-06 | [[../../10-competitors/sites/howtonetwork-ccna\|howtonetwork-ccna]] · D&D / sim patterns |
| 6 | CertiMaan | https://www.certimaan.com/post/ccna-sample-questions | **90+** blog MCQs | **2026** | No key on page | off | 2026-06-06 | [[../../10-competitors/sites/certimaan-ccna\|certimaan-ccna]] · alt [40+ post](https://www.certimaan.com/post/ccna-certification-sample-questions) |
| 7 | 9tut | https://www.9tut.com/topics/ccna-quizzes | Free topic quizzes; **600+** premium engine | **2026** | Partial | off | 2026-06-06 | [[../../10-competitors/sites/9tut\|9tut]] · labs [[ccna-tutorials](https://www.9tut.com/ccna-tutorials-practice-labs-lab-challenges)] |
| — | Odom / Pearson CCNA | https://www.pearsonitcertification.com/store/ccna-200-301-official-cert-guide-library-9780135792735 | Chapter exams | **200-301** | In book | — | 2026-06-06 | Widely used; not web-scraped |
| — | Boson ExSim | https://www.boson.com/ccna-200-301 | Paid sim exams | **200-301** | Paid | — | 2026-06-06 | High-quality sim; course competitor |
| — | Jeremy's IT Lab | https://www.jeremysitlab.com/ccna | Video + labs | **200-301** track | Free videos | — | 2026-06-06 | Course intent — stem intel only |

**Not CCNA (CompTIA-only in vault):** ExamCompass · PrepTIA · CertBlaster · Tech Exam Lexicon — no 200-301 sample pages found (2026-06-06).

**First collect (2026-06-06):** OpenExamPrep **200** + Mastery **24** + ExamTopics p1 **8** = **232** rows → [[runs/2026-06-06-net-new|net-new review]].

---

## Tier C — uncredited / community (discovery → review → maybe add to BCT)

| id | Source | URL | Q count (stated) | Source version / date | Poll | date_added | Notes |
|----|--------|-----|------------------|------------------------|------|------------|-------|
| 2 | ExamTopics | https://www.examtopics.com/exams/cisco/200-301/ | **1395+** visible | Updated **2026-06-06** | **on** (p1) | 2026-06-06 | [[../../10-competitors/sites/examtopics-ccna\|examtopics-ccna]] · Ads negative `examtopics` |
| 8 | ExamCollection | https://www.examcollection.com/200-301-dumps.html | **719+** syndicated | **2026-05-19** | off | 2026-06-06 | [[../../10-competitors/sites/examcollection-ccna\|examcollection-ccna]] |
| 9 | Exam-Labs | https://www.exam-labs.com/dumps/200-301 | **719** premium; **20** free sample | **2026-05-19** | off | 2026-06-06 | [[../../10-competitors/sites/exam-labs-ccna\|exam-labs-ccna]] |
| 10 | PrepAway | https://www.prepaway.com/ccna-certification-exams.html | **719+** syndicated | **2026-05-19** | off | 2026-06-06 | [[../../10-competitors/sites/prepaway-ccna\|prepaway-ccna]] |
| — | CertiMaan dumps hub | https://www.certimaan.com/certifications/cisco-dumps | SEO dump pages | **2026** | off | 2026-06-06 | Tier C sizing only |
| — | r/ccna | https://www.reddit.com/r/ccna/ | Ongoing threads | Rolling | off | 2026-06-06 | “Passed 200-301” recall — paraphrase only |
| — | r/Cisco | https://www.reddit.com/r/Cisco/ | Ongoing | Rolling | off | 2026-06-06 | Exam experience threads |

**Import convention:** `source_id` from site note YAML; `topic_notes`: `Tier C research — community recall; verify answer on Cisco Tier A only`.

---

## Tier C — blocked for Ads / publishing

Same research rules as above. **Google Ads negatives:** `examtopics`, `braindump`, `exam dumps`, `pass4sure`, `actual test questions`.

| Source | Notes |
|--------|-------|
| VCE / ETE / PDF dump bundles | Tracker intel only; Cisco policy — no verbatim BCT copy |
| SPOTO / DumpsMate / CertEmpire (CCNA SKUs) | See dump market if CCNA rows added to pdf tracker later |

---

## Internal — Be Certified Today

| Source | Path | Q count | Version / date | date_added | Notes |
|--------|------|---------|----------------|------------|-------|
| CCNA MCQ chain | `public/CCNA-Study/CCNA_questions/*.html` | **~714** pages | v1.1 objectives JSON | 2026-06-06 | Original stems; verify new items vs Cisco Tier A |
| Drag-and-drop | `public/CCNA-Study/CCNA_D_D/` | D&D set | v1.1 | 2026-06-06 | PBQ-style |
| CLI labs | `public/CCNA-Study/CCNA_labs/` | Lab pages | v1.1 | 2026-06-06 | VLAN / trunk samples on landing |
| Free samples | `/sample?track=ccna-questions` etc. | **2** MCQ + D&D + lab | **2026** | 2026-06-06 | `ccna-home.html` lead funnel |
| Free assessment | `CCNA_Sim_EXAM/free-assessment.html` | **45** min sim | **2026** | 2026-06-06 | Domain scorecard |
| Timed sim | `CCNA_Sim_EXAM/test-simulation.html` | **120** min | **2026** | 2026-06-06 | Paid one-shot |

---

## Suggested workflow for new items

1. Run `npm run ccna:monthly` or paste import CSV into `imports/` (create when needed).
2. Review net-new in `runs/YYYY-MM-DD-net-new.md`.
3. Verify concept on **Cisco Tier A** (docs / exam topics).
4. Draft original stem in `scripts/gen_ccna_chain_pages.py`; tag objective in `ccna-question-topic-map.json`.
5. Regenerate: `python3 scripts/gen_ccna_chain_pages.py` · `python3 scripts/build-ccna-objective-tracker.py`.

---

## Gaps to research next (2026+ sources only)

- [ ] Enable poll: **Crucial Exams**, **CertiMaan** (`certimaan` parser), **HowToNetwork** (H5P embed)
- [ ] ExamTopics: raise `max_pages` after spot-check page quality
- [ ] **Cisco practice exam** SKU — capture if Cisco publishes free web samples for 200-301
- [ ] **Wendell Odom** / **31 Days Before Your CCNA** — 2026 edition dates
- [ ] New SERP entrants for `ccna 200-301 practice questions` in **2026**

---

## Change log

| date_added | Change |
|------------|--------|
| 2026-06-06 | Initial CCNA catalog; 10 competitor tracker rows; 3 polls enabled; first run 232 discovered |
| 2026-06-06 | Linked to `ccna_monthly_question_hunt.py` + `10-competitors/sites/*-ccna.md` |

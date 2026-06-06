---
type: question-source-catalog
exam: CCNA-200-301
content_type: labs-sim
exam_version: v1.1
objectives_version: "1.1"
last_updated: 2026-06-06
verify_answers_against: Cisco official only
tracker: competitors-ccna-labs-sim-tracker.csv
---

# CCNA 200-301 — labs, drag-and-drop & simulation source catalog

**Exam:** Cisco **CCNA 200-301** (v1.1) — live exam mixes **MCQ**, **drag-and-drop**, **simlet**, and **CLI-style** items  
**Local bank:**

| Path | Content |
|------|---------|
| `public/CCNA-Study/CCNA_D_D/` | **~90+** drag-and-drop pages |
| `public/CCNA-Study/CCNA_labs/` | **9** browser CLI lab sims (VLAN, OSPF, NAT, ACL, …) |
| `public/CCNA_Sim_EXAM/` | Free **45-min** assessment + **120-min** timed sim |

**Workflow:** `npm run ccna:labs-monthly` · runs → `labs-sim/runs/`  
**MCQ catalog:** [[ccna-200-301-web-sources|ccna-200-301-web-sources.md]]

Same tier policy as MCQ — Tier C is discovery only; verify on **Cisco Tier A** before shipping HTML.

---

## Interaction types to track

| `pbq_type` | CCNA exam examples |
|------------|-------------------|
| `drag-drop` | Match protocol ↔ port, subnet ↔ mask, HSRP state ↔ behavior |
| `simulation` | Multi-step topology fix, ACL placement, OSPF adjacency |
| `cli-lab` | Configure VLAN, trunk, static route, NAT overload |
| `hotspot` | Click region on topology / `show` output |
| `ordered-sequence` | Troubleshooting steps, DNS lookup order |
| `fill-in` | IOS command fragment, IPv6 compress |

---

## Tier A — verification authority (labs / sim)

| Source | URL | Labs / sim (stated) | Source version | date_added | Notes |
|--------|-----|---------------------|----------------|------------|-------|
| Exam topics outline | https://learningnetwork.cisco.com/s/ccna-exam-topics | Simlet + D&D in exam format | **v1.1** | 2026-06-06 | Blueprint defines PBQ-style load |
| Packet Tracer | https://www.netacad.com/courses/packet-tracer | Topology labs | Rolling | 2026-06-06 | Official hands-on; download app |
| OCG lab manual | https://www.cisco.com/c/en/us/training-events/training-certifications/certifications/associate/ccna.html | Book labs | **200-301** | 2026-06-06 | Cisco Press companion |
| IOS command reference | https://www.cisco.com/c/en/us/support/docs/ios-nx-os-software/ios-software-releases-121-t/12778-ospf-12.html | — | Rolling | 2026-06-06 | Verify CLI tasks against docs |

---

## Tier B — legitimate labs / sim practice

Poll **on** = `pbq_poll.enabled` in `sites/*-ccna.md` · `npm run ccna:labs-poll-sources`

| id | Source | URL | Labs / sim (stated) | Free tier | Poll | date_added | Site note |
|----|--------|-----|---------------------|-----------|------|------------|-----------|
| 1 | Crucial Exams | https://crucialexams.com/exams/cisco/ccna/200-301/practice-tests-practice-questions | **7 PBQ** mini-games (preview on page) | Read-only preview | **on** | 2026-06-06 | [[../../10-competitors/sites/crucial-exams-ccna\|crucial-exams-ccna]] |
| 2 | HowToNetwork | https://www.howtonetwork.com/free/cisco-ccna-exam-walkthrough/ | **103** Q H5P (D&D + matching) | Full walkthrough | **on** | 2026-06-06 | [[../../10-competitors/sites/howtonetwork-ccna\|howtonetwork-ccna]] |
| 3 | 9tut engine | https://www.9tut.com/ccna-testing-engine | **D&D + lab sims** (premium) | Paid | **on** | 2026-06-06 | [[../../10-competitors/sites/9tut\|9tut]] |
| 4 | 9tut labs | https://www.9tut.com/ccna-tutorials-practice-labs-lab-challenges | **32+** PT / GNS3 labs | Free pages | off | 2026-06-06 | Manual lab intel; not HTML poll |
| 5 | OpenExamPrep | https://open-exam-prep.com/practice/ccna | Landing cites D&D + sim | Full MCQ free | **on** | 2026-06-06 | [[../../10-competitors/sites/open-exam-prep-ccna\|open-exam-prep-ccna]] |
| 6 | Mastery Exam Prep | https://masteryexamprep.com/exams/cisco/ccna/ | Scan landing | Samples | **on** | 2026-06-06 | [[../../10-competitors/sites/mastery-exam-prep-ccna\|mastery-exam-prep-ccna]] |
| — | Boson ExSim | https://www.boson.com/ccna-200-301 | Full timed sim | Paid | off | 2026-06-06 | Desktop sim — manual reference |
| — | Pearson OCG | https://www.pearsonitcertification.com/store/ccna-200-301-official-cert-guide-library-9780135792735 | Book + PT labs | In book | off | 2026-06-06 | Not web-scraped |

---

## Tier C — uncredited / VCE (discovery only)

| id | Source | URL | date_added | Poll | Notes |
|----|--------|-----|------------|------|-------|
| 7 | ExamTopics | https://www.examtopics.com/exams/cisco/200-301/ | 2026-06-06 | **on** | D&D recall in index — [[../../10-competitors/sites/examtopics-ccna\|examtopics-ccna]] |
| 8 | ExamCollection | https://www.examcollection.com/200-301-dumps.html | 2026-06-06 | **on** | VCE sim claims |
| 9 | Exam-Labs | https://www.exam-labs.com/dumps/200-301 | 2026-06-06 | **on** | VCE Virtual CertExam |
| 10 | PrepAway | https://www.prepaway.com/ccna-certification-exams.html | 2026-06-06 | **on** | ETE sim ecosystem |
| — | r/ccna | https://www.reddit.com/r/ccna/ | 2026-06-06 | off | “What sims on exam?” recall threads |

**Import:** paste into `labs-sim/imports/` with `topic_notes`: `Tier C — verify on Cisco Tier A`.

---

## Internal — Be Certified Today

| Source | Path | Count | date_added | Notes |
|--------|------|------:|------------|-------|
| Drag-and-drop bank | `public/CCNA-Study/CCNA_D_D/**/*.html` | **~90+** | 2026-06-06 | `ccna-dnd-page.css` shell |
| CLI labs | `public/CCNA-Study/CCNA_labs/*.html` | **9** | 2026-06-06 | VLAN · trunk/LACP · OSPF · NAT/DHCP · ACL/snooping · static route · IPv4/IPv6 |
| Free D&D sample | `/sample?track=ccna-dnd` | 4 shuffled | 2026-06-06 | Landing lead magnet |
| Free VLAN lab | `/sample?track=ccna-vlan` | 1 CLI | 2026-06-06 | Landing lead magnet |
| Free assessment | `CCNA_Sim_EXAM/free-assessment.html` | 45 min (20 MCQ + 2 D&D + 1 lab) | 2026-06-06 | Domain scorecard |
| Timed sim | `CCNA_Sim_EXAM/test-simulation.html` | 120 min | 2026-06-06 | Paid one-shot |

---

## Suggested workflow

1. `npm run ccna:labs-monthly` — competitor `generic_pbq` scan + compare vs BCT D&D/labs/sim.
2. Review `labs-sim/runs/YYYY-MM-DD-net-new.md`.
3. Verify IOS behavior on Cisco docs (Tier A).
4. New D&D → `public/CCNA-Study/CCNA_D_D/` · new CLI lab → `CCNA_labs/` · update topic maps + regenerate manifests.

---

## Gaps to research next

- [ ] H5P embed parser for **HowToNetwork** walkthrough (full D&D stems)
- [ ] **Crucial Exams** PBQ preview URLs (read-only UI capture)
- [ ] **Boson** / **Pearson** sim topic checklist vs BCT objective map
- [ ] Reddit `r/ccna` sim recall — optional `reddit_pbq` with CCNA queries

---

## Change log

| date_added | Change |
|------------|--------|
| 2026-06-06 | Initial labs/sim catalog + tracker + `ccna_monthly_labs_sim_hunt.py` |
| 2026-06-06 | First collect: 7 catalog signals vs BCT index 112 pages → [[labs-sim/runs/2026-06-06-net-new|net-new review]] |

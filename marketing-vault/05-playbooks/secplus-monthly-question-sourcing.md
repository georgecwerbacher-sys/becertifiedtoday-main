---
type: playbook
exam: SY0-701
frequency: monthly
status: active
created: 2026-06-03
---

# Monthly SY0-701 — collect · compare · save

Three steps. One command if you prefer.

Script: `scripts/secplus_monthly_question_hunt.py`

---

## One command (monthly)

```bash
npm run secplus:monthly
```

With Tier B or Tier C paste file:

```bash
python3 scripts/secplus_monthly_question_hunt.py run \
  --import marketing-vault/11-question-sourcing/imports/YYYY-MM-manual.csv
```

Same `--import` path for **Tier B** (practice sites) and **Tier C** (Reddit, forums, recall threads). Use one combined CSV if you like.

**Outputs** (same date folder):

| Step | File |
|------|------|
| 1 Collect | `runs/YYYY-MM-DD-discovered.csv` |
| 2 Compare | `runs/YYYY-MM-DD-net-new.csv` + `runs/YYYY-MM-DD-compare.md` |
| 3 Save | `runs/YYYY-MM-DD-net-new.md` (Obsidian note) |

Step 1 does **not** read BCT. Step 2 compares. Step 3 writes **net-new only** as markdown in the vault.

---

## Three steps (manual)

### 1 — Collect (no BCT)

```bash
npm run secplus:collect
```

- Auto **Tier A:** CompTIA V7 practice page (`secplus-web-sources.json`)
- Auto **Tier B/C samples:** every `marketing-vault/10-competitors/sites/*.md` with `question_poll.enabled: true` — see [[../10-competitors/sites/README|competitor poll registry]]
- Optional manual rows: `--import path/to/manual.csv`

### 2 — Compare (reads BCT)

```bash
npm run secplus:compare
```

Writes net-new CSV for the save step.

### 3 — Save (Obsidian .md)

```bash
npm run secplus:save
```

Opens cleanly in Obsidian under `marketing-vault/11-question-sourcing/runs/`.

---

## After the net-new note

For each net-new row you accept:

1. Verify answer on **CompTIA Tier A** only.
2. Write **original** stem in `scripts/gen_secplus_chain_pages.py`.
3. Run `python3 scripts/gen_secplus_chain_pages.py`.
4. Log in [[../11-question-sourcing/secplus-external-not-in-bct|external log]].

**Uncredited sources (Tier C)** never go straight into BCT — they only surface **candidates to review**. Accepted items are rewrites verified on Tier A.

Do **not** copy verbatim from any external source.

---

## Tier B sources (credited practice — discovery paste)

Add or enable in [[../10-competitors/sites/README|10-competitors/sites]] — e.g. [[../10-competitors/sites/techexamlexicon|Tech Exam Lexicon]], [[../10-competitors/sites/certblaster|CertBlaster]], [[../10-competitors/sites/mastery-exam-prep|Mastery]]. Set `question_poll.enabled: true` to poll on collect.

Sites without a working parser: keep `enabled: false` and paste into [[../11-question-sourcing/templates/discovered-questions-import|import CSV]].

---

## Tier C sources (uncredited — discovery paste only)

Same registry: [[../10-competitors/sites/examtopics|ExamTopics]] (`tier: c`, page 1 polled). Reddit/forums: add new `.md` files with `enabled: false` + manual import, or a custom `sample_url` when a parser exists.

**Workflow:**

1. Skim threads for **SY0-701** shared scenarios / “what was on the exam” posts.
2. **Paraphrase** the concept into your import CSV (not verbatim dump text).
3. Set `topic_notes` to `Tier C research — community recall; verify answer on CompTIA Tier A only`.
4. Put community-claimed answers in `stated_answer` only as a **note** — never use them as the key.
5. Run the same `collect` / `run --import` pipeline; compare still finds net-new vs BCT.
6. Before publishing: verify concept on **Tier A**, write an **original** stem in `gen_secplus_chain_pages.py`.

**Ads negatives (unchanged):** dump sellers, ExamTopics as ad traffic — see `ads_negative_dump_domains` in config. Research paste in the vault is separate from Ads targeting.

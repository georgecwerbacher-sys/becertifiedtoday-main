# Competitor sites — question poll registry

Add one `.md` file per site. The monthly hunt script reads **YAML frontmatter** and polls every file with `question_poll.enabled: true`.

Script: `scripts/secplus_competitor_poll.py` · wired from `scripts/secplus_monthly_question_hunt.py collect`

## Add a new site

1. Copy an existing note or use this frontmatter block:

```yaml
---
type: competitor
brand: Example Prep
domain: example.com
url: https://example.com/sy0-701/
product: SY0-701
category: practice_samples
research_date: 2026-06-03
question_poll:
  enabled: true
  tier: b
  id: example-sy0-701
  sample_url: https://example.com/sy0-701/samples/
  parser: generic_mcq
  version_note: SY0-701
  topic_notes: Tier B — verify answer on CompTIA Tier A
---
```

2. Set **`tier`**: `b` (credited practice samples) or `c` (uncredited / community recall — discovery only).
3. Set **`parser`** (see below). Use `enabled: false` until a parser works or for manual-only sites.
4. Run `npm run secplus:monthly` — collect polls all enabled sites automatically.

## Parsers

| parser | Sites |
|--------|--------|
| `techexamlexicon` | Tech Exam Lexicon sample pages |
| `certblaster` | CertBlaster free practice pages |
| `mastery` | Mastery Exam Prep public samples |
| `openexamprep` | OpenExamPrep Security+ practice page (embedded question JSON) |
| `preptia` | PrepTIA SY0-701 practice test (page 1 samples) |
| `certimaan` | CertiMaan blog sample questions (40 MCQs) |
| `examtopics` | ExamTopics `/view/N/` pages (`max_pages: 1` recommended) |
| `generic_mcq` | Fallback — try last |

CompTIA official (Tier A) stays in `11-question-sourcing/config/secplus-web-sources.json` → `tier_a_fetch`.

## Tiers (reminder)

- **Tier A** — verify answers (CompTIA only)
- **Tier B / C poll results** — discovery → compare vs BCT → review → optional **original** add to bank
- Never trust community keys; never copy verbatim into BCT

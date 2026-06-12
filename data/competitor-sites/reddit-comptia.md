---
type: competitor
brand: r/CompTIA
domain: reddit.com
url: https://www.reddit.com/r/CompTIA/
product: SY0-701
category: community_forum
research_date: 2026-06-03
question_poll:
  enabled: false
  tier: c
  id: reddit-comptia
  sample_url: https://www.reddit.com/r/CompTIA/
  parser: generic_mcq
  version_note: rolling threads
  topic_notes: Tier C research — community recall; verify answer on CompTIA Tier A only
pbq_poll:
  enabled: true
  tier: c
  id: reddit-comptia-pbq
  sample_url: https://www.reddit.com/r/CompTIA/
  subreddit: CompTIA
  parser: reddit_pbq
  max_questions: 25
  version_note: rolling threads
  topic_notes: Tier C PBQ recall — Reddit search; paraphrase into pbq/imports/; verify Tier A
---

# r/CompTIA — SY0-701 recall threads

**PBQ poll:** `reddit_pbq` searches recent posts for SY0-701 / Security+ PBQ, simulation, and drag-and-drop recall. Paraphrase into `pbq/imports/` — verify on CompTIA Tier A only.

**Note:** Reddit often returns **403** to automated scripts. If poll is empty, skim threads manually and paste into `pbq/imports/` or use `register --kind pbq-preview` with screenshots.

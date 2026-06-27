# Question bank template (site-wide)

Every certification track on Be Certified Today uses the same **100-question bank** model aligned to the **official exam topics PDF** for that blueprint version.

## Bank model

| Rule | Detail |
|------|--------|
| **Bank size** | **100** questions per bank (MCQ unless the track defines mixed formats). |
| **Next bank** | When bank *N* reaches 100 published items, bank *N+1* opens for the next hundred (questions 101–200, 201–300, …). |
| **Domain mix** | Each bank targets the **exam domain weights** from the blueprint PDF (e.g. CCNAAUTO v1.1: 15% / 20% / 15% / 15% / 20% / 15%). |
| **Blueprint version** | Every question maps to the **PDF version** in effect when it was authored (`v1.1`, `v1.2`, `V_2025`, …). |
| **Objectives** | Assign at least one **objective ID** (`2.4`, `5.8`, …). Use **sub-objective** IDs when the PDF lists children (`1.8.c`, `3.9.a`, …). |
| **Verification** | Keys and explanations must be confirmed on **Tier A sources** only (vendor official docs / learning network). Never Reddit, forums, or competitor dumps. |

### Per-bank domain targets (100 questions)

Multiply each domain weight by 100 and round so the six domains sum to 100:

| CCNAAUTO v1.1 domain | Weight | Target Qs / bank |
|----------------------|-------:|-----------------:|
| 1.0 Software Development and Design | 15% | 15 |
| 2.0 Understanding and Using APIs | 20% | 20 |
| 3.0 Cisco Platforms and Development | 15% | 15 |
| 4.0 Application Deployment and Security | 15% | 15 |
| 5.0 Infrastructure and Automation | 20% | 20 |
| 6.0 Network Fundamentals | 15% | 15 |

Other tracks: copy `practice-bank-blueprint.example.json` and set weights from that exam’s PDF.

## Files per track

```
public/{Track}-Study/data/
  {track}-practice-bank-blueprint.json   # weights, bankSize, sourcePdf, verification policy
  {track}-question-topic-map.json        # slug → objectives + verification (schema v2)
  {track}-question-topic-tracker.json    # generated: actual vs target counts

public/{Track}-Study/{Track}_Questions/  # one HTML file per slug
public/{Track}-Study/js/{track}-practice-hub.js
```

## Topic map (schema v2)

Legacy maps (CCNA, Sec+, ENCOR) use `"assignments": { "file.html": ["1.5"] }`. **New banks** use schema v2:

```json
{
  "schemaVersion": 2,
  "blueprintVersion": "v1.1",
  "sourcePdf": "200-901-CCNAAUTO_v.1.1.pdf",
  "assignments": {
    "rest-http-401-unauthorized-fix.html": {
      "objectives": ["2.4", "2.5"],
      "subObjectives": [],
      "verification": {
        "verifiedAt": "2026-06-27",
        "sources": [
          {
            "type": "cisco-doc",
            "title": "REST API authentication overview",
            "url": "https://developer.cisco.com/docs/..."
          }
        ]
      }
    },
    "git-merge-conflict-resolution.html": {
      "objectives": ["1.8"],
      "subObjectives": ["1.8.f"],
      "verification": {
        "verifiedAt": "2026-06-27",
        "sources": [
          {
            "type": "cisco-learning",
            "title": "DevNet Git module",
            "url": "https://learningnetwork.cisco.com/..."
          }
        ]
      }
    }
  }
}
```

**Verification rules**

- `sources[].url` must be `cisco.com`, `*.cisco.com`, `developer.cisco.com`, or `learningnetwork.cisco.com`.
- Do **not** cite ExamTopics, Reddit, Discord, or competitor practice sites in verification metadata or published HTML.
- Paraphrase stems; do not copy dump wording.
- Run `npm run lint:question-urls` after HTML edits.

## Practice portal UI

Training portals expose **Choose your practice mode**:

1. **Domain weight table** — target vs current count per domain (from tracker JSON).
2. **Practice by subject** — filter Random/Review to one domain (optional).
3. **Numbered banks** — Bank 1 (1–100), Bank 2 (101–200), each with Random + Review.

Wire-up:

- Shared helpers: `public/js/bcc-question-bank-utils.js`
- Track hub: `public/{Track}-Study/js/{track}-practice-hub.js`
- Portal markup: see `templates/pages/Training_Portal_Template.html` § Practice questions

## Generators & lint

| Command | Purpose |
|---------|---------|
| `python3 scripts/build-question-bank-tracker.py --track ccnaauto` | Regenerate `{track}-question-topic-tracker.json` |
| `npm run lint:question-urls` | Block non-Cisco URLs in published question HTML |

## Adding a new track checklist

1. Copy `practice-bank-blueprint.example.json` → `{track}-practice-bank-blueprint.json` (set weights from official PDF).
2. Add `{track}-question-topic-map.json` (schema v2, empty `assignments`).
3. Create `{track}-practice-hub.js` using CCNAAUTO hub as reference.
4. Add portal section with domain filter + bank grid.
5. Author questions from `templates/questions/question-mc-baseline.html`; register each slug in the topic map before publish.
6. Run tracker build after every batch of new questions.

## Reference implementations

| Track | Hub JS | Blueprint |
|-------|--------|-----------|
| CCNA | `ccna-practice-100-hub.js` | 200-301 domain weights (legacy v1 map) |
| ENCOR | `encor-practice-hub.js` | 350-401 v1.2 |
| Sec+ | `secplus-practice-hub.js` | SY0-701 |
| **CCNAAUTO** | `ccnaauto-practice-hub.js` | 200-901 v1.1 (first full v2 template) |

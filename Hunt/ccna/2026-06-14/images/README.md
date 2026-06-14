# Hunt images — 2026-06-14

Optional folder for **diagram / topology** exhibits that the monthly poll cannot extract.

## Automatic fetch (export script)

When you run:

```bash
python3 scripts/export_ccna_hunt_obsidian.py --date 2026-06-14
```

the exporter downloads exhibits when possible:

| Source | Exhibit type | Saved as |
|--------|----------------|----------|
| `mastery-ccna-public` | IOS CLI in `<pre><code>` | inlined in note (no PNG) |
| `howtonetwork-ccna-walkthrough` | lazy-loaded PNG screenshots | `howtonetwork-ccna-walkthrough-q{watupro-id}.png` |
| `examtopics-ccna-research` | `/assets/media/exam-media/…` diagrams | `examtopics-ccna-research-q{N}.png` |

## Manual diagram override

If auto-fetch fails, save a screenshot with a predictable name:

| Pattern | Example |
|---------|---------|
| `mastery-q{N}.png` | `mastery-q10.png` |
| `howtonetwork-ccna-walkthrough-q8603.png` | WatuPro question id |
| `examtopics-ccna-research-q1.png` | Question number on view page |
| `q{NNN}-slug.png` | `q096-nat-topology.png` |

Re-run the export script after adding files.

[[../2026-06-14|Back to run index]]

Security+ Google Ads — AdWords checklist (Apple Numbers)
============================================================

File: marketing-research/Sec+ Campaign/secplus-campaign-checklist.csv

One campaign · one ad group · $20/day:
  • Setup checklist (pre-launch through negatives)
  • 6 campaign sitelinks (Extensions phase — paste URLs + descriptions)
  • 67 positive keywords (rank order — paste into Google Ads)
  • RSA headlines + descriptions (Security+ PBQ Practice)
  • 46 campaign negatives + 8 ad group negatives

Columns
-------
  Done      — set to TRUE when complete (or convert to checkbox in Numbers)
  Section   — Setup | Headline | Description | Ops
  Phase     — Pre-launch, Campaign, Extensions, Ad group, Negatives, Launch, Week 1, etc.
  Step      — step number within that phase
  Task      — what to do (Add exact keyword, Campaign negative phrase, …)
  Value     — paste value, URL, keyword, headline, or description text
  Ad group  — Security+ PBQ Practice or Campaign
  Notes     — rank, pins, char counts

Open in Numbers
---------------
1. Numbers → File → Open → secplus-campaign-checklist.csv
2. Select Done column → Format → Checkbox (optional)
3. Filter Section = Setup and Phase = Ad group to paste keywords only
4. Filter Section = Setup and Phase = Extensions for sitelinks
5. Filter Section = Setup and Phase = Negatives for negatives
6. File → Save to create a .numbers file

Regenerate after keyword CSV edits
----------------------------------
  npm run sync:secplus-checklist

Source keywords: marketing-research/Sec+ Campaign/secplus-keywords.csv

Campaign summary
----------------
Campaign:   Security+ SY0-701 · Exam prep · becertifiedtoday
Budget:     $20.00/day · max CPC $2.75
Ad group:   Security+ PBQ Practice (only)
Landing:    https://becertifiedtoday.com/comptia-sec+-home.html
UTM:        utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=pbq-wedge

Full reference: marketing-research/Sec+ Campaign/Sec+ Notes.md

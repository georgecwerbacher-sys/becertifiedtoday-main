Security+ Google Ads — AdWords checklist (Apple Numbers)
============================================================

File: marketing-research/Sec+ Campaign/secplus-campaign-checklist.csv

Three US-only campaigns · one intent-matched ad group each · $20/day each:
  • Setup checklist (pre-launch through negatives)
  • 6 campaign sitelinks (Extensions phase — paste URLs + descriptions)
  • 64 positive keywords (rank order — paste into Google Ads)
  • RSA headlines + descriptions (Security+ PBQ Practice)
  • 59 campaign negatives + 8 ad group negatives

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
Campaigns:  Core Exam Prep · US / Military Gov 8140 · US / Student Workforce · US
Budget:     $20.00/day each · $60/day total · max CPC $2.75
Bid rule:   Hold keyword bids 7 days; adjust after week 1 from keyword results
Ad groups:  One intent-matched ad group per campaign
Landing:    https://becertifiedtoday.com/comptia-sec+-home.html
UTM:        secplus_core_us / secplus_gov_us / secplus_workforce_us

Full reference: marketing-research/Sec+ Campaign/Sec+ Notes.md

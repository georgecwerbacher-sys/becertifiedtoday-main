Security+ Google Ads — combined checklist for Apple Numbers
============================================================

File: scripts/secplus-google-ads-campaign-checklist.csv

One file contains everything:
  • Setup checklist (pre-launch through initial test)
  • RSA headlines (15 per ad group)
  • RSA descriptions (4 per ad group)

Columns
-------
  Done      — set to TRUE when complete (or convert to checkbox in Numbers)
  Section   — Setup | Headline | Description | Ops
  Phase     — Pre-launch, Campaign, Ad group 1, secplus_portal_10d, etc.
  Step      — step number within that phase
  Task      — what to do
  Value     — paste value, URL, keyword, headline text, or description text
  Ad group  — secplus_portal_10d, secplus_pbq_wedge, Campaign, Both
  Notes     — pins, char counts, reminders

Open in Numbers
---------------
1. Numbers → File → Open → secplus-google-ads-campaign-checklist.csv
2. Select Done column → Format → Checkbox (optional)
3. Filter by Section column to show only Setup, Headline, or Description
4. File → Save to create a .numbers file

Campaign summary
----------------
Budget:     $10.00/day
Ad groups:  secplus_portal_10d (~$7/day) portal baseline only
Landing:    https://becertifiedtoday.com/comptia-sec+-home.html#purchase
Wedge:      Dedicated SEC+_Wedge_PBQ — see secplus-wedge-pbq-google-ads-checklist.csv
UTM:        utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=portal-10d

Full reference: scripts/secplus-portal-10d-google-ads.md
Campaign doc:   marketing-research/campaigns/Security+ Campaign.md
Funnel tracker: marketing-research/Wedge Marketing plan/SEC+ funnel build tracker.md

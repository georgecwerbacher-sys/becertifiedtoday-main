CCNA Google Ads — single combined checklist for Apple Numbers
=============================================================

File: scripts/ccna-google-ads-campaign-checklist.csv

One file contains everything:
  • Setup checklist (pre-launch through scale)
  • RSA headlines (30 rows — 15 per ad group)
  • RSA descriptions (8 rows — 4 per ad group)

Columns
-------
  Done      — set to TRUE when complete (or convert to checkbox in Numbers)
  Section   — Setup | Headline | Description | Ops
  Phase     — Pre-launch, Campaign, Ad group 1, ccna_practice_test, etc.
  Step      — step number within that phase
  Task      — what to do
  Value     — paste value, URL, keyword, headline text, or description text
  Ad group  — ccna_practice_test, ccna_browser_labs, Campaign, Both
  Notes     — pins, char counts, reminders

Open in Numbers
---------------
1. Numbers → File → Open → ccna-google-ads-campaign-checklist.csv
2. Select Done column → Format → Checkbox (optional)
3. Filter by Section column to show only Setup, Headline, or Description
4. File → Save to create a .numbers file

Campaign summary
----------------
Budget:     $25.00/day
Ad groups:  ccna_practice_test (~$17/day) + ccna_browser_labs (~$8/day)
Landing:    https://becertifiedtoday.com/ccna-home.html#purchase
UTM:        utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=portal-10d

Full reference: scripts/ccna-portal-10d-google-ads.md

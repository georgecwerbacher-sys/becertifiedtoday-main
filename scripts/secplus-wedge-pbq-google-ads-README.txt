SEC+_Wedge_PBQ — Google Ads checklist for Apple Numbers
=========================================================

File: scripts/secplus-wedge-pbq-google-ads-checklist.csv

Dedicated wedge campaign for Security+ PBQ / performance-based keywords.
One ad group: SEC+_Wedge_PBQ → pbq-practice-browser landing page.

Columns
-------
  Done      — set to TRUE when complete (or checkbox in Numbers)
  Section   — Setup | Headline | Description | Ops
  Phase     — Pre-launch, Keyword Planner, Campaign, Ad group, etc.
  Step      — step number within phase
  Task      — what to do in Google Ads UI
  Value     — paste value, URL, keyword, headline, or description
  Ad group  — SEC+_Wedge_PBQ, Campaign
  Notes     — pins, char counts, Planner verify reminders

Open in Numbers
---------------
1. Numbers → File → Open → secplus-wedge-pbq-google-ads-checklist.csv
2. Select Done column → Format → Checkbox (optional)
3. Filter Section = Setup for build steps; Headline/Description for RSA paste
4. Complete Keyword Planner phase before adding keywords to Google Ads
5. Save as .numbers to track progress

Campaign summary
----------------
Campaign:   SEC+_Wedge_PBQ
Ad group:   SEC+_Wedge_PBQ
Budget:     $8.00/day (launch)
Bidding:    Maximize clicks, max CPC $3.50
Landing:    https://becertifiedtoday.com/secplus/pbq-practice-browser.html
UTM:        utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=pbq-wedge
Conversion: GA4 begin_checkout (secplus_portal_10d, secplus_portal_30d)

Before launch: pause secplus_pbq_wedge in the combined Security+ campaign.

Full reference: scripts/secplus-wedge-pbq-google-ads.md
Obsidian folder: marketing-research/Wedge Marketing plan/secplus-wedge-campaign/
Build steps:  01-build-steps.md
Keywords:     03-keywords-ad-group.md · 04-keywords-campaign-negatives.md

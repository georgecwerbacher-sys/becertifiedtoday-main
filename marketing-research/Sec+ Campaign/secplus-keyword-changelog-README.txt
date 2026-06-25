Sec+ keyword change log — quick tracker notes
=============================================

File: marketing-research/Sec+ Campaign/secplus-keyword-changelog.csv

Use for:
  • Admin /admin/#section-campaign-plan → Ops notes (copy Tracker note column)
  • Remember what changed in Google Ads vs repo only
  • Day 3 / 7 / 14 / 21 search-term reviews

Columns
-------
  Date          — YYYY-MM-DD
  Action        — remove positive | add neg campaign | add neg adgroup | keep positive | repo sync
  Keyword       — as in Google Ads
  Match         — Exact | Phrase | Broad
  Why           — one line (CPC, intent, search term)
  Google Ads    — pending | pending paste | live | done
  Admin day     — D1–D21 or date
  Tracker note  — paste into admin Ops notes if useful

After each edit to secplus-keywords.csv:
  1. Append row(s) here
  2. npm run sync:secplus-checklist
  3. Admin: check Keyword CSV synced (+ Negatives added if negatives changed)
  4. Paste pending rows in Google Ads → set Google Ads column to live

Copy-paste block for admin (2026-06-25 D3)
------------------------------------------
KW D3: cut 3 practice-questions positives; +13 campaign negs pending paste. Keep PBQ/timed. 64 pos live in repo. Overview → google-ads-overview-2026-06-25/

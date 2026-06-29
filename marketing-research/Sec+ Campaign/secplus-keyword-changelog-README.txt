Sec+ keyword change log — quick tracker notes
=============================================

File: marketing-research/Sec+ Campaign/secplus-keyword-changelog.csv

Use for:
  • Remember what changed in Google Ads vs repo only
  • Search-term reviews and negative keyword changes

Columns
-------
  Date          — YYYY-MM-DD
  Action        — remove positive | add neg campaign | add neg adgroup | keep positive | repo sync
  Keyword       — as in Google Ads
  Match         — Exact | Phrase | Broad
  Why           — one line (CPC, intent, search term)
  Google Ads    — pending | pending paste | live | done
  Admin day     — legacy D1–D21 label or date
  Tracker note  — short note for repo history

After each edit to secplus-keywords.csv:
  1. Append row(s) here
  2. npm run sync:secplus-checklist
  3. Paste pending rows in Google Ads → set Google Ads column to live

Copy-paste block for admin (2026-06-25 D3)
------------------------------------------
KW D3: cut 3 practice-questions positives; +13 campaign negs pending paste. Keep PBQ/timed. 64 pos live in repo. Overview → google-ads-overview-2026-06-25/

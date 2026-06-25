---
type: competitor
brand: Dion Training
domain: diontraining.com
url: https://www.diontraining.com/
product: CCNAAUTO-200-901
category: practice_samples
research_date: 2026-06-25
question_poll:
  enabled: false
  tier: b
  id: diontraining-ccnaauto-practice
  sample_url: https://www.diontraining.com/search?q=ccna+automation&type=product
  parser: generic_mcq
  version_note: 200-901 v1.1
  topic_notes: Tier B — Shopify practice exam packs when CCNAAUTO SKU exists; verify on Cisco Tier A
pbq_poll:
  enabled: false
  tier: b
  id: diontraining-ccnaauto-pbq
  sample_url: https://www.diontraining.com/search?q=ccna+automation&type=product
  parser: generic_pbq
  version_note: 200-901 v1.1
  topic_notes: Tier B — PBQ / lab packs (Sec+ model); verify on Cisco Tier A
---

# Dion Training — CCNAAUTO hunt target

## Model

- Shopify storefront: **practice exams**, **PBQ practice packs**, **labs**, courses, and discounted exam vouchers  
- CompTIA Platinum Partner (SY0-701 PBQ packs, practice exams, labs live today)  
- Blog covers CCNA vs Network+, network automation career paths, DevOps/IaC (Ansible, Terraform) — SEO funnel, not yet a CCNAAUTO product line  
- **Catalog check (2026-06-25):** site search `cisco automation` → **0 products**; add poll URLs when a CCNAAUTO / DevNet Associate SKU ships

## Hunt angle

- Watch for **CCNA Automation (200-901)** practice exam + PBQ + lab bundles mirroring Sec+ SY0-701 packs  
- Jason Dion **Udemy** Cisco/DevNet courses may feed question ideas — manual research only; no poll until on-site samples exist  
- Paid traffic lands on homepage (`diontraining.com`) — compare BCT free bank + timed sim vs Dion bundled practice

## Weakness vs BCT (when they launch)

- Paid packs vs BCT growing free objective-mapped bank  
- Keys are vendor-authored — verify every stem on **Cisco Tier A** / DevNet docs before BCT draft

## BCT angle

Free CCNA + CCNAAUTO overlap samples, CLI labs, JSON drag-and-drop, and objective checklist ([[../../../CCNA-Auto/blueprint-hunt-list|CCNA-Auto blueprint]]) without checkout.

**Poll:** `npm run ccnaauto:poll-sources` · `npm run ccnaauto:labs-poll-sources` after `enabled: true` and parser smoke test.

Sec+ research context: negated `"dion training"` / `"jason dion"` in Google Ads — separate from CCNAAUTO content hunt.

[Dion Training](https://www.diontraining.com/)

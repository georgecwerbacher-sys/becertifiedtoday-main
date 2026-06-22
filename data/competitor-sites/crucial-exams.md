---
type: competitor
brand: Crucial Exams
domain: crucialexams.com
url: https://crucialexams.com/exams/comptia/security/sy0-701/practice-tests-practice-questions
product: SY0-701
category: practice_samples
research_date: 2026-06-03
question_poll:
  enabled: false
  tier: b
  id: crucialexams-samples
  sample_url: https://crucialexams.com/exams/comptia/security/sy0-701/practice-tests-practice-questions
  parser: generic_mcq
  version_note: SY0-701
  topic_notes: Tier B — verify answer on CompTIA Tier A
pbq_poll:
  enabled: true
  tier: b
  id: crucialexams-pbq
  sample_url: https://crucialexams.com/exams/comptia/security/sy0-701/practice-tests-practice-questions
  parser: generic_pbq
  version_note: SY0-701
  topic_notes: Tier B PBQ — 9 PBQ stated; verify on CompTIA Tier A
---

# Crucial Exams — SY0-701

Nine **read-only preview** PBQs (headless capture hits login wall — open in browser). Capture targets: `data/secplus-pbq-sourcing/config/secplus-pbq-capture-targets.json` (`crucialexams-pbq-*`).

| # | PBQ | Preview URL |
|---|-----|-------------|
| 1 | Home WLAN Network Configuration | `/study/sy0-701/simulations/configuration/home-wlan-network-configuration` |
| 2 | Public Wi-Fi Network Configuration | `/study/sy0-701/simulations/configuration/public-wlan-network-configuration` |
| 3 | Cloud Web Application Firewall Setup | `/study/sy0-701/simulations/configuration/cloud-web-application-firewall-setup` |
| 4 | Mobile Device Management Enrollment | `/study/sy0-701/simulations/configuration/mobile-device-management-enrollment` |
| 5 | SIEM Alarm Configuration | `/study/sy0-701/simulations/configuration/siem-alert-configuration` |
| 6 | Network Security Protocols and Technologies | `/study/sy0-701/simulations/matching/network-security-protocols-and-technologies` |
| 7 | Incident Response Procedures | `/study/sy0-701/simulations/matching/incident-response-procedures` |
| 8 | Cryptographic Concepts | `/study/sy0-701/simulations/matching/cryptographic-concepts` |
| 9 | Network Components and Common Protocols | `/study/sy0-701/simulations/matching-diagram/network-components-and-common-protocols` |

Base: `https://crucialexams.com` · Catalog: [SY0-701 study materials](https://crucialexams.com/exams/comptia/security/sy0-701/practice-tests-practice-questions)

**Capture:** `python3 scripts/secplus_pbq_capture.py run --source-prefix crucialexams-pbq-` (merge into today's run folder). Manual PNG: `register --png … --source-id crucialexams-pbq-home-wlan --url …`

**Tracker row:** id **8** in [[../competitors-practice-samples-tracker.csv]]

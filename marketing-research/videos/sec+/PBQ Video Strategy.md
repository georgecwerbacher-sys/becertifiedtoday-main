---
type: video-strategy
track: secplus
priority: primary
tags:
  - videos
  - secplus
  - pbq
  - security+
---

# Security+ PBQ videos — primary focus

**Channel priority:** Most new videos are **SY0-701 PBQ prep** — how to practice performance-based items in the browser, not domain lectures.

**Welcome video** ships first ([[../website/welcome-video|website/welcome-video]]), then **PBQ prep** becomes the default pipeline.

**Voice:** [[../../Sec+ Campaign/Sec+ Positioning|Sec+ Positioning]] · [[../../YouTube Channels|YouTube Channels]] · [[PBQ Video Format|PBQ Video Format]]

---

## What each PBQ video teaches

| ✅ Show | ❌ Skip |
|---------|---------|
| How to **read** the prompt and multi-part chain | Teaching SY0-701 domain from zero |
| **Exam-style UI** — drag, drop, tabs, exhibits | Full spoiler walkthrough of every answer |
| **Prep technique** — flag, move on, revisit; zone maps; ordering logs | “Here’s what ZTA means for 10 minutes” |
| **Same scenario on the site** (free sample when public) | Paid bank or checkout on screen |
| **One mistake pattern** learners hit on this PBQ type | Guaranteed pass · real exam claims |

**Standard hook:** *“You’ve finished your Security+ course — here’s how I practice this PBQ before test day.”*

---

## YouTube playlist

**Primary:** `Security+ PBQ Prep` (all PBQ videos)

**Secondary:** `Test Prep Techniques` — only for cross-cert meta (timed sim, scorecard, last 3 weeks). CCNA/ENCOR lab videos **on hold** until PBQ backlog is moving.

---

## UTM pattern (every PBQ video)

```
https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=youtube&utm_medium=organic&utm_campaign=youtube_secplus_pbq&utm_content=[slug]
```

**Free sample PBQs** — pin comment can deep-link sample path when public:

| Slug | Sample path |
|------|-------------|
| `dark-web-account-protection` | `/COMP_TIA_SEC+/SEC+_Samples/pbq/dark-web-account-protection/…` |
| `home-wlan-director-config` | `/COMP_TIA_SEC+/SEC+_Samples/pbq/home-wlan-director-config/…` |
| `firewall-acl-secops` | `/COMP_TIA_SEC+/SEC+_Samples/pbq/firewall-acl-secops/…` |

Landing anchor for 3-PBQ preview: `#home-secplus-darkweb-title` on `comptia-sec+-home.html`

---

## Production workflow

1. Pick slug from backlog below
2. Read `data/secplus-pbq/[slug]/recommendations.md` if present
3. Duplicate [[../_video-template|_video-template]] → `sec+/[slug]-pbq-prep.md`
4. Apply [[PBQ Video Format|PBQ Video Format]] section timings
5. Record portal in OBS — **sample URL only** unless scenario is in free bundle
6. Publish · add row to backlog table · update status

**Filled example:** [[zero-trust-zta-migration-pbq-prep|Zero Trust PBQ prep]] (first PBQ after welcome)

---

## Ship order (backlog)

### Tier 0 — channel setup

| # | Status | Slug | Working title | Format | Sample? | Notes |
|---|--------|------|---------------|--------|---------|-------|
| 0 | published | — | Welcome to Be Certified Today | 2:30 | — | `public/videos/bct-intro.mp4` · [[../website/welcome-video\|brief]] |

### Tier 1 — align with landing + Google Ads (free samples)

| # | Status | Slug | Working title | Format | Sample? | Notes |
|---|--------|------|---------------|--------|---------|-------|
| 1 | idea | `dark-web-account-protection` | How I practice Security+ IR PBQs (dark web scenario) | 4–6 min | ✅ | Landing 3-PBQ preview #1 |
| 2 | idea | `home-wlan-director-config` | PBQ prep: WLAN configuration (exam-style steps) | 4–6 min | ✅ | Landing preview #2 |
| 3 | idea | `firewall-acl-secops` | Three-tier firewall ACL — PBQ practice method | 4–6 min | ✅ | Landing preview #3 |
| 4 | idea | *(meta)* | How to work Security+ chain PBQs (multi-part prompts) | 5–7 min | ✅ | Technique · use 3 samples as B-roll |

### Tier 2 — high clip value + chain start

| # | Status | Slug | Working title | Format | Sample? | Notes |
|---|--------|------|---------------|--------|---------|-------|
| 5 | script | `zero-trust-zta-migration` | PBQ tip: Zero Trust zone map (8 controls, 4 zones) | 90 s Short + 5 min | ❌ | [[zero-trust-zta-migration-pbq-prep\|Brief]] · chain #2 |
| 6 | idea | `wap-secure-configuration` | Secure WAP PBQ — preview panel technique | 3–5 min | ❌ | Short-friendly per recommendations |
| 7 | idea | `subnetting-ip-addressing` | Subnet PBQ — calculator & magic table prep | 4–6 min | ❌ | Standalone demo clip |
| 8 | idea | `security-control-placement` | Drag-and-drop controls into zones | 4–6 min | ❌ | Classic DnD PBQ type |

### Tier 3 — chain labs (portal order)

Ship in chain order after Tier 2; one video per scenario unless Short + long pair.

| # | Slug | Title (short) | Type |
|---|------|---------------|------|
| 9 | `acme-rag-hr-ai` | RAG / HR AI exhibits | Chain · multi-section |
| 10 | `hybrid-pki-audit` | PKI audit & revocation | Chain |
| 11 | `ubuntu-ssh-breach-hardening` | SSH breach hardening | Chain |
| 12 | `ransomware-dr-acme` | Ransomware DR order | Chain |
| 13 | `siem-ransomware-mitre` | SIEM + MITRE mapping | Chain |
| 14 | `advanced-firewall-rule-configurator` | Edge firewall rules | Builder |
| 15 | `ubuntu-cis-hardening` | CIS hardening checklist | Chain |
| 16 | `log-timeline-forensics` | Log timeline ordering | Ordering |
| 17 | `pki-certificate-chain-browser-error` | TLS chain browser error | Hot spot / diagnose |
| 18 | `phishing-email-analysis` | Phishing email analysis | Exhibit |
| 19 | `vulnerability-management` | Vulnerability management | Chain |
| 20 | `incident-response` | IR ransomware phases | Chain |
| 21 | `quantitative-risk-ale` | ALE / quantitative risk | Calculation |
| 22 | `malware-ioc-analysis` | Malware IOC analysis | Exhibit |
| 23 | `data-protection` | Data protection controls | Chain |
| 24 | `governance` | Governance mapping | DnD |
| 25+ | *remaining 34* | See PBQ_Production README chain 22–34 | Mixed |

Full chain list: `public/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/README.md`

---

## Formats

| Format | Length | When |
|--------|--------|------|
| **PBQ prep (main)** | 4–8 min | Default — technique + partial portal demo |
| **PBQ tip (Short)** | 60–90 s | One technique · cut from main or standalone |
| **PBQ type explainer** | 5–7 min | Chain vs hot spot vs ordering — meta only |

---

## Thumbnail patterns (Photoshop)

- **Text:** `PBQ Prep` + scenario hook (3–4 words) e.g. `Zone Map` · `Dark Web IR`
- **Visual:** Blurred portal screenshot + SY0-701 badge optional
- **Avoid:** CompTIA logo · “pass guaranteed” · “real exam”

---

## Deferred (not primary)

| Track | When |
|-------|------|
| CCNA exam practice labs | After Tier 1–2 PBQ videos publishing steadily |
| ENCOR exam practice labs | Same |
| Long SY0-701 domain series | **Never** — conflicts with positioning |

---

## Related

[[README|sec+ folder]] · [[PBQ Video Format]] · [[../Production Template|Production Template]] · [[../../Sec+ Campaign/Sec+ RSA Copy|RSA policy]]

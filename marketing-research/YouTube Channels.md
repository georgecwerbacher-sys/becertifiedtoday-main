---
type: content-plan
channels: youtube
tags:
  - marketing
  - youtube
  - content
  - becertifiedtoday
---

# YouTube channels — content plan

**Purpose:** Organic discovery and trust for Be Certified Today — every video supports **testing techniques and exam preparation**, not first-time learning.

**North star:** You are not teaching the cert from zero. You are helping someone who **already studied** practice smarter, use the portal, and answer *Am I ready?*

**Voice:** [[Site Mission]] — *practice and readiness*, not instructor-led courses or dump sites.

**Relationship to ads:** RSA copy positions the product as *not another video bootcamp*. YouTube matches that: **prep technique + portal demos**, with CTAs to **free samples** and the timed sim — never a substitute for Messer, CBT, or INE when someone needs to learn the material the first time.

**Primary content (2026):** **Security+ PBQ prep videos** — see [[videos/sec+/PBQ Video Strategy|PBQ Video Strategy]]. CCNA/ENCOR lab videos are secondary until the PBQ pipeline is publishing steadily.

---

## What every video is (and is not)

| ✅ Make | ❌ Do not make |
|---------|----------------|
| How to **practice** PBQs, labs, and timed sims | Full **course** modules or chapter walkthroughs |
| **Exam-style** task flow — read prompt, work interface, review mistakes | Teaching fundamentals from scratch (*“What is OSPF?”* for beginners) |
| **Last-mile** tips — sprint schedule, scorecard use, flag-and-move | Long lecture series that compete with video bootcamps |
| **Browser portal** demos — same UI as test day | Slides-only theory with no practice tie-in |
| **Technique** — adaptive review, readiness signals, exam logistics | Promising pass, dumps, or *real exam* content |

**Audience line (use in intros):** *“You’ve already done your course or book — this is how I prep for test day.”*

**Playlist names** — lead with prep, not curriculum: `Security+ PBQ Prep`, `CCNA Exam Practice Labs`, `ENCOR Exam Practice Labs`, `Test Prep Techniques`.

---

## Channel structure

| Option | When to use |
|--------|-------------|
| **One channel** — playlists above by cert + techniques | Start here; easier to grow and cross-link |
| **Separate channels per cert** | Only if analytics show distinct audiences and you can post consistently on each |

**Suggested channel name:** Be Certified Today (or match site branding exactly).

**Production notes:** [[videos/README|Videos]] — duplicate [[videos/_video-template|_video-template]] per video · [[videos/Production Template|Production Template]] · [[videos/Premiere and OBS Setup|Premiere/OBS]] · [[videos/Envato Asset Guide|Envato]]. First ship: [[videos/website/welcome-video|Welcome video]] (filled example).

**Default CTA in description:**

```
Try the same scenario in your browser (free samples):
https://becertifiedtoday.com/[exam-home]?utm_source=youtube&utm_medium=organic&utm_campaign=youtube_[playlist]&utm_content=[video-slug]
```

Replace `[exam-home]` with `comptia-sec+-home.html`, `ccna-home.html`, or `ccnp-home.html`.

---

## Content pillars

All four pillars are **prep and technique**. PBQ and lab videos are not separate “product demos” — they teach *how to work exam-style items* and point to the same practice on the site.

### 1. Security+ PBQ prep (technique + portal)

**Goal:** Prep technique for performance-based items — how to read multi-part prompts, use the interface, and review after — not a SY0-701 curriculum.

| Format | Length | Example titles |
|--------|--------|----------------|
| **PBQ prep walkthrough** | 3–8 min | *How I practice Security+ PBQs: Zero Trust zone map* |
| **Short / Short** | 60–90 s | *PBQ tip: map controls to zones in 90 seconds* |
| **Portal practice demo** | 2–4 min | *Try this PBQ in your browser — exam-style UI* |

**Frame every clip:** *practice method* first, scenario second. Open with *“After your course, use PBQs like this…”*

**Source ideas:** `data/secplus-pbq/*/recommendations.md`. Ship order: PBQs on landing and in ads first (chain labs, hot spots, IR).

**Do not:** Teach Security+ domains from zero; claim *real exam*, *actual exam questions*, or *walk in ready* — mirror [[Sec+ RSA Copy#Do not use in RSA|RSA policy-safe language]].

---

### 2. CCNA exam practice labs *(deferred)*

**Status:** On hold — concentrate on [[videos/sec+/PBQ Video Strategy|Sec+ PBQ videos]] first.

**Goal:** **Exam-style lab prep** in the browser — timed task, CLI habits, common sim mistakes — not a CCNA course replacement.

| Format | Length | Example titles |
|--------|--------|----------------|
| **Practice run** | 5–12 min | *CCNA prep: OSPF lab under exam-style instructions* |
| **Task + try it** | 2–3 min | Read the lab brief → *practice the same task on the site* |
| **Prep mistake** | 3–5 min | *Why I fail NAT labs on practice runs (and how I fix it)* |

**Lab inventory:** `public/CCNA-Study/CCNA_labs/` · topic map: `public/CCNA-Study/data/ccna-lab-topic-map.json`

**Priority for first videos:** static routing, VLAN/trunk, OSPF, NAT/DHCP — high exam weight; always tie back to **practice**, not teaching the protocol.

---

### 3. ENCOR exam practice labs *(deferred)*

**Status:** On hold — same as CCNA; PBQ pipeline first.

**Goal:** Same prep frame as CCNA — **exam-style CLI practice** for people who already know ENCOR topics.

| Format | Length | Example titles |
|--------|--------|----------------|
| **Practice run** | 8–15 min | *ENCOR prep: eBGP lab — exam-style steps on R1* |
| **Prep hook** | 4–6 min | *Before your timed sim: practice CoPP in the browser lab* |

**Lab inventory:** `public/CCNP-ENCOR-Study/CCNP-ENCOR-Labs/`

**Note:** Smaller audience; 1–2 strong **prep** videos, then expand if watch time holds.

---

### 4. Test preparation techniques (core playlist)

**Goal:** Cert-agnostic and cert-specific **prep methodology** — the spine of the channel. Pillars 1–3 feed this playlist when the angle is clearly technique-first.

| Topic | Angle | Site tie-in |
|-------|-------|-------------|
| **Timed simulation strategy** | How to run a full sim, review scorecard, retake weak domains | Timed sim on each exam home |
| **Last 2–3 weeks sprint** | Schedule: samples → full bank → sim → gap review | 10/30-day access framing |
| **PBQ exam mechanics** | How to read multi-part prompts, when to flag and move on | Sec+ PBQ samples |
| **Adaptive review** | Why missed questions recycle; focused vs random sessions | Portal review modes |
| **Readiness vs false confidence** | Dumps vs interactive practice; what “ready” looks like | [[Site Mission#What I promise you (most important first)|Mission pillars]] |
| **Exam day logistics** | Pearson VUE check-in, ID, breaks — factual, no braindump hype | About / FAQ |
| **Mobile study** | Short sessions between shifts on phone/tablet | Mobile-friendly MCQ/PBQ |

**Formats:** 5–10 min main videos; 60 s Shorts for one tip each (*One thing I do the week before Security+*).

---

## Production checklist (per video)

- [ ] **Prep filter** — Would this help someone *after* a course/book, before test day? If it teaches the cert from zero, cut or reframe.
- [ ] **Title + thumbnail** — *prep*, *practice*, or *technique* in the angle; no policy-risk phrases
- [ ] **Hook (first 15 s)** — *“You’ve studied — test in X weeks. Here’s how I practice…”*
- [ ] **Show portal or lab UI** — exam-style practice, not slide deck lectures
- [ ] **Description** — prep technique summary; sample link with UTM; *not a course* + disclaimer (*independent prep, not affiliated with CompTIA/Cisco*)
- [ ] **End screen** — subscribe + `Test Prep Techniques` or cert prep playlist + sample URL
- [ ] **Pin comment** — link to free sample for that cert
- [ ] **Log in backlog** below when published

---

## Backlog (planning)

| Status | Pillar | Working title | Portal link / slug | Notes |
|--------|--------|---------------|-------------------|-------|
| script | website | Welcome to Be Certified Today | `index.html` | [[videos/website/welcome-video\|Brief + script]] |
| idea | Sec+ PBQ | Dark web IR — PBQ practice method | `dark-web-account-protection` | Tier 1 · free sample · [[videos/sec+/PBQ Video Strategy\|strategy]] |
| idea | Sec+ PBQ | WLAN configuration PBQ prep | `home-wlan-director-config` | Tier 1 · free sample |
| idea | Sec+ PBQ | Firewall ACL PBQ prep | `firewall-acl-secops` | Tier 1 · free sample |
| script | Sec+ PBQ | Zero Trust zone map | `zero-trust-zta-migration` | [[videos/sec+/zero-trust-zta-migration-pbq-prep\|Brief]] · 90 s Short + 5 min |
| idea | Test prep techniques | How Security+ chain PBQs work (meta) | `#home-secplus-samples-title` | Tier 1 · uses 3 samples as B-roll |
| idea | Test prep techniques | Timed sim — scorecard technique | `comptia-sec+-home.html` | After Tier 1 PBQs |
| deferred | CCNA exam practice | | | After PBQ pipeline steady |
| deferred | ENCOR exam practice | | | After PBQ pipeline steady |

**Status values:** `idea` → `script` → `record` → `edit` → `published`

---

## Metrics (monthly)

Track in a separate sheet or append here:

| Month | Videos published | Views | Subs net | Clicks to site (UTM) | Sample → checkout (if measurable) |
|-------|------------------|-------|----------|----------------------|-----------------------------------|
| | | | | | |

YouTube Studio → **Traffic sources → External** and GA4 → `utm_source=youtube` for landing sessions.

---

## Related

- [[Site Mission]] · [[Marketing Research]] · [[Sec+ Campaign/Sec+ Positioning|Sec+ Positioning]]
- PBQ clip notes: `data/secplus-pbq/*/recommendations.md`
- Keep YouTube organic and lightweight while Google Ads setup remains the paid acquisition focus; batch videos without letting production delay ad ops.

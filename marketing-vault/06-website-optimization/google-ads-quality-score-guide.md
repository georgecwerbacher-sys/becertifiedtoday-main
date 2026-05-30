---
type: reference
topic: google-ads-quality
---

# Google Ads quality & landing page experience

Google assigns a **Quality Score** (1–10) per keyword. Higher scores typically mean **lower cost per click** and **better ad positions**. Three components matter for optimization work in this vault:

| Component | What Google evaluates | What you control on the site |
|-----------|----------------------|------------------------------|
| **Expected CTR** | Likely click rate for the ad | Mostly ad copy & extensions — note alignment in campaign file |
| **Ad relevance** | Ad vs keyword intent | Message match: keyword → ad headline → landing H1 |
| **Landing page experience** | Usefulness after the click | Page content, speed, mobile, clarity, trust |

Below focuses on **landing page experience** — the part you improve in `public/` and track in `06-website-optimization/`.

---

## Landing page experience — what helps

### Relevance & message match

- [ ] **Headline (H1)** reflects exam **prep / practice test** intent — not “training course” ([[../01-strategy/positioning-and-messaging|positioning]])
- [ ] **Above the fold** states: browser-based, no PDF, exam-realistic practice (see [[../01-strategy/google-ai-search-strategy|AI search FAQ]])
- [ ] **No bait-and-switch** — page delivers what the ad claims; pricing visible before checkout
- [ ] **Single clear path** for ad traffic: sample → purchase, or direct to `#purchase`

### Usability

- [ ] **Mobile-friendly** — readable text, tappable buttons (min ~44px touch targets)
- [ ] **Fast load** — compress images, avoid blocking scripts where possible
- [ ] **No intrusive interstitials** on landing (popups that block content hurt experience)
- [ ] **Working links** — no broken CTAs; checkout buttons functional

### Transparency & trust

- [ ] **Pricing shown** before Stripe redirect ($9.99 / $19.99 / $4.99 for Security+)
- [ ] **What’s included** spelled out (question banks, sim, access duration)
- [ ] **Business identity** — site name/logo, contact or support path if available
- [ ] **Privacy / terms** linked where appropriate (especially if collecting email at checkout)

### Technical checks (quick)

Run periodically on each ad landing URL:

- [ ] [Google PageSpeed Insights](https://pagespeed.web.dev/) — mobile + desktop
- [ ] [Google Mobile-Friendly Test](https://search.google.com/test/mobile-friendly) *(legacy but still useful)*
- [ ] GA4 — engagement rate, bounce on landing page vs site average
- [ ] Google Ads → Keywords → **Landing page experience** column (Below average / Average / Above average)

---

## Ad relevance — message match table

Keep this aligned between [[../02-campaigns/security-plus-google-ads|Security+ campaign]] ad groups and [[pages/comptia-sec-plus-home|landing page]]:

| Ad group theme | Example keywords | Ad headline idea | Landing must say |
|----------------|------------------|------------------|------------------|
| Practice test | security+ practice test, sy0-701 practice | SY0-701 Practice Tests | “practice tests”, exam-style questions |
| Exam prep | security+ exam prep, sy0-701 study | Security+ Exam Prep | structured prep, domains, simulation |
| Simulation | security+ simulation exam | Timed SY0-701 Simulation | timed exam, performance-based items |

When you change H1 or hero copy on the site, update this table and verify ad headlines still match.

---

## Quality Score is not instant

- Changes in `public/` need a **deploy** (Vercel) before Google sees them
- Ads Quality Score / LP experience often lag **days to 2 weeks** after meaningful traffic
- Log every change in [[content-change-log|content change log]] with date so you can correlate with Ads reports

---

## Policy reminders (avoid disapproval)

- Do not imply CompTIA endorsement unless licensed
- Use “exam prep”, “practice”, “aligned to objectives” — not “guaranteed pass”
- Match product names accurately: **CompTIA Security+ SY0-701**

---

## When to open a page-specific note

Create or update a file in `pages/` for each **final URL** in Google Ads. Track audit scores, open issues, and planned Cursor edits there.

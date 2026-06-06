# CCNA Google Ads — ad group `ccna_portal_10d`

Paste-ready setup for Google Ads UI. Landing: `public/ccna-home.html` with `utm_content=portal-10d` shows **$9.99 / 10-day** as the only primary purchase CTA.

---

## Campaign shell

| Setting | Value |
|---------|--------|
| Campaign name | `CCNA 200-301 · Exam prep · becertifiedtoday` |
| Type | Search (Search partners off until baseline) |
| Daily budget | $10.00/day |
| Bidding | Maximize clicks, max CPC **$2.75** |
| utm_campaign | `ccna_portal` |
| Locations | **52 countries** + key cities — see `scripts/ccna-portal-10d-google-ads.md` |
| Language | English |

---

## Location targeting

**Presence only.** Tier A countries first: India · United States · United Kingdom · Canada · Australia · Philippines · UAE · Singapore · Nigeria · Pakistan · South Africa · Saudi Arabia · Malaysia · Ireland · Germany · Netherlands · New Zealand. Full international list in `scripts/ccna-portal-10d-google-ads.md`.

---

## Ad group

| Setting | Value |
|---------|--------|
| Ad group name | `ccna_portal_10d` |
| Display path | `CCNA` / `10-Day-Access` |
| Primary conversion | GA4 `begin_checkout` (`ccna_portal_10d`) |

**Final URL:**

```
https://becertifiedtoday.com/ccna-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=portal-10d
```

---

## Products or services to advertise

**Names only** — keep titles short. Put online, no downloads, labs, drag-and-drop, and timed sim in the **description** under each product.

**Category:** Education & training → Test preparation (or Educational software / Online education)

| # | Product / service name | Description (paste under name in Google Ads) |
|---|------------------------|-----------------------------------------------|
| 1 | CCNA 200-301 10-Day Exam Prep Access | 10 days of CCNA 200-301 v1.1 exam prep in your browser: 700+ practice questions with new items added continuously, CLI labs, drag-and-drop, portal modes, and 120-min timed sim. Current-objective alignment—not stale PDF dumps. $9.99 one-time. |
| 2 | CCNA 200-301 30-Day Exam Prep Access | 30 days of the same v1.1 library: latest CCNA practice questions, verified explanations, CLI labs, drag-and-drop sets, progress tracking, and timed simulation. New questions added continuously. $19.99 one-time. |
| 3 | Free CCNA 200-301 Practice Questions | Preview current CCNA 200-301 v1.1 practice questions—shuffled each run, instant feedback, same style as the full bank. Free on ccna-home.html; no checkout. |
| 4 | Free CCNA 200-301 Drag-and-Drop Practice | Current exam-style drag-and-drop items for CCNA 200-301 v1.1—four shuffled PBQ-style prompts per run. Free preview; no checkout. |
| 5 | Free CCNA 200-301 CLI Lab Practice | Browser VLAN CLI lab aligned to current CCNA objectives. Hands-on practice without GNS3. Free preview; no checkout. |

**Do not add as separate products:** “All online,” “no downloads,” “labs,” or “drag-and-drop” as standalone line items — those are features inside the products above.

**Do not add:** Free timed simulation sample or standalone 120-min timed sim — not on `ccna-home.html`.

---

## RSA headlines (≤30 chars)

Use all 15 — see `scripts/ccna-portal-10d-google-ads.md` for full list. Pin: H1 `CCNA 200-301 Practice Test` · H2 `$9.99 for 10-Day Access` · H3 `CCNA 200-301 Exam Prep`

---

## RSA descriptions (≤90 chars)

```
CCNA 200-301 practice test bank: 700+ questions, v1.1 aligned. Labs & D&D included.
$9.99 for 10-day access. Cisco CCNA exam prep—not a course. No PDFs or GNS3.
CCNA practice questions with verified explanations. Timed simulation + portal modes.
Try free CCNA samples first. Unlock 10-day question bank access at checkout.
```

---

## Sitelink extensions (ad group — minimum 6)

Sitelink text ≤25 chars · each description line ≤35 chars.

| # | Link text | Description 1 | Description 2 | Full URL |
|---|-----------|---------------|---------------|----------|
| 1 | 10-Day Access · $9.99 | Full v1.1 question bank | $9.99 one-time, no sub | `https://becertifiedtoday.com/ccna-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=portal-10d` |
| 2 | Free Practice Questions | Current v1.1 MCQ preview | Instant feedback, free | `https://becertifiedtoday.com/sample?track=ccna-questions&utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=sitelink-sample` |
| 3 | Sample Drag-and-Drop | Four PBQ-style items | Shuffled each run, free | `https://becertifiedtoday.com/sample?track=ccna-dnd&utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=sitelink-dnd` |
| 4 | Free VLAN CLI Lab | Hands-on lab in browser | No GNS3 required | `https://becertifiedtoday.com/sample?track=ccna-vlan&utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=sitelink-lab` |
| 5 | Latest v1.1 Questions | 700+ items, updated often | Not stale PDF dumps | `https://becertifiedtoday.com/ccna-home.html#home-ccna-samples-title?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=sitelink-samples` |
| 6 | Timed Sim Included | 120-min exam-style run | With 10-day portal access | `https://becertifiedtoday.com/ccna-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=portal-10d` |

---

## Keywords

**Exact**

```
[ccna 200-301 question bank]
[ccna question bank]
```

**Phrase**

```
"ccna exam prep online"
"ccna practice test online"
"ccna 200-301 prep"
"ccna question bank"
"ccna 200-301 question bank"
"cisco ccna practice portal"
"ccna study prep online"
```

**Ad group negatives (Phrase)**

```
"free"
"bootcamp"
"course"
"dump"
"pdf"
"jobs"
"netacad"
```

---

## Campaign-level negatives (Phrase)

```
"free course"
"training course"
"bootcamp"
"instructor led"
"brain dump"
"exam dump"
"guaranteed pass"
"pdf download"
"udemy"
"coursera"
"cbt nuggets"
"ine ccna"
"cisco netacad"
"jobs"
"salary"
"ccnp encor"
"ccie"
"comptia security+"
"packet tracer course"
"gns3 tutorial"
```

---

## Setup checklist

- [ ] Ad group enabled: `ccna_portal_10d`
- [ ] Final URL includes `#purchase` and `utm_content=portal-10d`
- [ ] Products list pasted (5 items above)
- [ ] RSA + keywords pasted
- [ ] Pause other CCNA ad groups if testing this group solo
- [ ] GA4 `begin_checkout` imported as Primary in Google Ads
- [ ] Stripe `ccna-portal-10d` payment link = $9.99
- [ ] Test: open Final URL → only **Get 10-day access · $9.99** above the fold → click → `begin_checkout` in GA4 Realtime

---

## Site behavior (`utm_content=portal-10d`)

- Purchase fold: 10-day $9.99 only (30-day hidden)
- Auto-scroll to `#purchase`
- 10-day popup suppressed (script: `public/js/ccna-portal-10d-landing.js`)
- Mobile sticky: `Get 10-day access · $9.99`

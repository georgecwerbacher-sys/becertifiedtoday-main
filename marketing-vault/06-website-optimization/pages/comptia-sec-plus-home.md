---
type: landing-page
url: /comptia-sec+-home.html
canonical: https://becertifiedtoday.com/comptia-sec+-home.html
campaign: secplus_portal
status: active
repo_file: public/comptia-sec+-home.html
last_audit: 2026-05-30
quality_score_notes: Free sim + $9.99 pricing + runner nav live prod 2026-05-30 — re-check Ads LP exp. ~2026-06-06
---

# comptia-sec+-home.html — ad landing page

Primary **Google Ads final URL** for [[../../02-campaigns/security-plus/security-plus-google-ads|Security+ campaign]].

## Live URLs

- Full page: `https://becertifiedtoday.com/comptia-sec+-home.html`
- Purchase block: `…/comptia-sec+-home.html#purchase`
- Lead magnet form: `…/comptia-sec+-home.html#secplus-lead-capture`
- Free sim (post opt-in): `/COMP_TIA_SEC+/test-simulation-runner.html?free=1`
- With UTMs: `…?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal`

### Ad group → URL map

| Ad group | Recommended final URL |
|----------|----------------------|
| `secplus_lead_free_sim` | `…#secplus-lead-capture?utm_content=lead-free-sim` |
| `secplus_sim_purchase` | `…#purchase?utm_content=sim-purchase` |
| `secplus_portal_access` | `…#purchase&utm_content=portal-30d` (or `portal-10d`) |
| Generic / brand | `…/comptia-sec+-home.html` |

## Repo & tracking

| Item | Location |
|------|----------|
| HTML | `public/comptia-sec+-home.html` |
| Checkout JS | `public/COMP_TIA_SEC+/js/secplus-portal-checkout.js` |
| Test sim checkout | `public/COMP_TIA_SEC+/js/secplus-test-checkout.js` |
| Lead capture | `public/js/secplus-lead-capture.js` · `POST /api/lead-capture` |
| Free sim runner | `public/COMP_TIA_SEC+/test-simulation-runner.html` |
| Free sim blueprint | `public/COMP_TIA_SEC+/data/secplus-free-simulation-blueprint.json` |
| GA4 + UTM | `public/js/campaign-attribution.js` ✓ |

## Current hero / message (prod 2026-06-04)

- **Page order:** `#purchase` (pricing) → intro → free sim → samples → compare → study plan — matches CCNA funnel (`order: 0` on `#purchase`)
- **H1:** SY0-701 Security+ Exam Prep: 1000+ Questions, Simulations & Adaptive Testing
- **Lead:** You-focused exam prep (not a course); 1000+ bank, **28 PBQ practice scenarios** (21 chain labs, 4 standalone, 1 hot spot, 2 IR report exhibits), adaptive modes; browser-only; federal/DoD context with “confirm with your manager”; free samples + 35-min timed exam
- **Writing rules:** [[../../12-Writing/_Writing-Rules|Guest page writing rules]] applied 2026-06-04
- **Federal section:** Removed as dedicated block (2026-05-30); DoD/8140 still in hero, meta, keywords, FAQ
- **Lead magnet:** `#secplus-lead-capture` — badge “Free · 35 minutes”; H2 “Start your free SY0-701 timed simulation”; **20 MCQ + 1 PBQ**; scorecard + optional email
- **Sim runner nav (free + paid):** **Back**, **Mark for review**, **Next** / **Finish**; embedded question Back/Home hidden in exam mode
- **Primary CTAs:** free sim (no checkout), free samples; **paid:** 30-day ($19.99) only on `#purchase` (2026-06-03)
- **Launch deal:** popup when any visitor scrolls to `#purchase` — **$17.99** with **ONETIMEDEAL** ($7 off $24.99) while popup open; dismiss ends offer for session

## Audit history

| Date | Avg checklist score | Top issue fixed | [[../landing-page-audit-checklist\|Checklist]] |
|------|--------------------:|-----------------|--------|
| 2026-05-30 | — | Positioning + FAQ for Ads/AI search | partial (copy deploy) |
| 2026-05-30 | — | Free sim live; $9.99 sim; relative image paths; vault sync | post-deploy |

## Open optimization items

- [x] **Messaging:** H1/hero say “exam prep” / “practice test” — done 2026-05-30
- [x] **AI search:** FAQ block — done 2026-05-30
- [x] **Free sim lead magnet** — live prod 2026-05-30
- [x] **Lead block copy:** Back + mark for review — done 2026-05-30
- [ ] PageSpeed mobile score baseline recorded
- [ ] Re-check Ads LP experience ~7 days after deploy (target ~2026-06-06)
- [x] **Lead-first layout** for `#secplus-lead-capture` / `utm_content=lead-free-sim` — done 2026-05-30

## Planned content changes (Cursor)

| Priority | Change | File / section | Status |
|----------|--------|----------------|--------|
| P1 | Fix lead capture bullet (Back + mark for review) | `#secplus-lead-capture` list | done 2026-05-30 |
| P2 | Results “Back to Security+ home” link on free sim | `test-simulation-runner.html` | backlog |

## Google Ads feedback

Record from Ads UI (Keywords → columns → Quality Score, Landing page exp.):

| Date | Keyword (example) | Quality Score | LP experience | Expected CTR | Ad relevance |
|------|-------------------|:-------------:|:-------------:|:------------:|:------------:|
| | | | | | |

---

After each deploy, log in [[../content-change-log|content change log]] and update hero copy section above.

# CCNA Google Ads — ad group `ccna_portal_10d`

Paste-ready setup for Google Ads UI. Landing: `public/ccna-home.html` with `utm_content=portal-10d` shows **$9.99 / 10-day** as the only primary purchase CTA.

**Browser preview (local):** http://localhost:3000/ccna-portal-10d-google-ads.html

---

## Campaign shell

| Setting | Value |
|---------|--------|
| Campaign name | `CCNA 200-301 · Exam prep · becertifiedtoday` |
| Type | Search (Search partners off until baseline) |
| Daily budget | $10.00/day |
| Bidding | Maximize clicks, max CPC **$2.75** |
| utm_campaign | `ccna_portal` |
| Locations | **Countries + cities below** (presence-only) |
| Language | English (site is English; most CCNA searches are English globally) |

---

## Location targeting

**Goal:** Reach searchers where CCNA certification, network engineering hiring, MSP/NOC work, and telecom/enterprise IT are prominent — **US and international**.

**Setup:**

1. **Location options:** **Presence: People in or regularly in your targeted locations** (not interest)
2. Add **countries** first (paste list below), then optional **city boosts** where listed
3. On **$10/day:** start with **Tier A countries** (15–20); expand after search-term review
4. Landing is English-only — Tier A/B are strongest fits; Tier C/D test after baseline CPA

### Tier A — Countries (highest CCNA / network engineer volume)

Add whole country in Google Ads → Locations:

```
India
United States
United Kingdom
Canada
Australia
Philippines
United Arab Emirates
Singapore
Nigeria
Pakistan
South Africa
Saudi Arabia
Malaysia
Ireland
Germany
Netherlands
New Zealand
```

### Tier B — Countries (strong IT outsourcing, telecom & enterprise networking)

```
Bangladesh
Sri Lanka
Egypt
Kenya
Ghana
Indonesia
Vietnam
Thailand
Brazil
Mexico
Colombia
Argentina
Chile
Poland
Romania
Czech Republic
Israel
Qatar
Kuwait
Jordan
Oman
Bahrain
Hong Kong
Taiwan
Japan
South Korea
Portugal
Spain
Italy
France
Belgium
Switzerland
Sweden
Norway
Denmark
Finland
Morocco
Trinidad and Tobago
Jamaica
Costa Rica
Panama
Peru
Uganda
Tanzania
Nepal
```

### Tier A cities — add for bid boost or narrow testing

| Country | Cities (search in Google Ads) |
|---------|--------------------------------|
| India | Bengaluru · Hyderabad · Mumbai · Chennai · Pune · New Delhi · Noida · Gurugram · Kolkata · Ahmedabad |
| United States | (see US metros below) |
| United Kingdom | London · Manchester · Birmingham · Edinburgh · Leeds · Bristol |
| Canada | Toronto · Vancouver · Ottawa · Montreal · Calgary · Edmonton |
| Australia | Sydney · Melbourne · Brisbane · Perth · Canberra |
| Philippines | Manila · Quezon City · Cebu City · Davao City |
| UAE | Dubai · Abu Dhabi · Sharjah |
| Singapore | Singapore |
| Nigeria | Lagos · Abuja · Port Harcourt |
| Pakistan | Karachi · Lahore · Islamabad · Rawalpindi |
| South Africa | Johannesburg · Cape Town · Pretoria · Durban |
| Saudi Arabia | Riyadh · Jeddah · Dammam |
| Ireland | Dublin · Cork |
| Germany | Berlin · Munich · Frankfurt · Hamburg |
| Netherlands | Amsterdam · Rotterdam · The Hague |

### United States — Federal, defense & contractor metros

| Metro / area | Add in Google Ads (search these) |
|--------------|----------------------------------|
| National Capital (DC / NoVA / MD beltway) | Washington DC · Arlington VA · Alexandria VA · Fairfax VA · Bethesda MD · Silver Spring MD · Reston VA · McLean VA |
| Colorado Springs | Colorado Springs CO |
| San Antonio | San Antonio TX |
| Hampton Roads | Norfolk VA · Virginia Beach VA · Chesapeake VA · Newport News VA |
| Huntsville (Army / aerospace) | Huntsville AL |
| Omaha (STRATCOM / telecom) | Omaha NE · Council Bluffs IA |
| Tampa (CENTCOM / MacDill) | Tampa FL · St. Petersburg FL |
| Dayton (Wright-Patterson AFB) | Dayton OH |
| Jacksonville (Navy / contractors) | Jacksonville FL |
| Oklahoma City (Tinker AFB) | Oklahoma City OK |
| Augusta (Fort Eisenhower / cyber) | Augusta GA |

### United States — Commercial network engineering & data-center hubs

| Metro / area | Add in Google Ads (search these) |
|--------------|----------------------------------|
| Dallas–Fort Worth | Dallas TX · Fort Worth TX · Plano TX · Irving TX |
| Atlanta | Atlanta GA · Sandy Springs GA |
| Research Triangle | Raleigh NC · Durham NC · Cary NC |
| Austin | Austin TX · Round Rock TX |
| Phoenix | Phoenix AZ · Mesa AZ · Scottsdale AZ |
| Seattle | Seattle WA · Bellevue WA · Tacoma WA |
| Bay Area | San Jose CA · Santa Clara CA · San Francisco CA · Oakland CA |
| Chicago | Chicago IL · Naperville IL |
| Houston | Houston TX · The Woodlands TX |
| New York / NJ | New York NY · Jersey City NJ · Newark NJ |
| Boston | Boston MA · Cambridge MA |
| Charlotte | Charlotte NC |
| Columbus | Columbus OH |
| Philadelphia | Philadelphia PA |
| Los Angeles | Los Angeles CA · Long Beach CA |
| Nashville | Nashville TN |
| Minneapolis | Minneapolis MN · St. Paul MN |
| Kansas City | Kansas City MO · Kansas City KS |
| Portland | Portland OR |
| Las Vegas | Las Vegas NV |
| Miami / South Florida | Miami FL · Fort Lauderdale FL |
| Pittsburgh | Pittsburgh PA |
| Baltimore | Baltimore MD |
| Richmond | Richmond VA |
| St. Louis | St. Louis MO |
| Denver | Denver CO · Aurora CO |
| Salt Lake City | Salt Lake City UT |

### United States — Tier 3 metros (if budget rises)

Charleston SC · Honolulu HI · San Diego CA · Sacramento CA · Indianapolis IN · Milwaukee WI · Memphis TN · Louisville KY · Boise ID

### Quick paste — all Tier A countries (16)

```
India
United States
United Kingdom
Canada
Australia
Philippines
United Arab Emirates
Singapore
Nigeria
Pakistan
South Africa
Saudi Arabia
Malaysia
Ireland
Germany
Netherlands
New Zealand
```

### Quick paste — full country list (Tier A + B, 52)

```
India, United States, United Kingdom, Canada, Australia, Philippines, United Arab Emirates, Singapore, Nigeria, Pakistan, South Africa, Saudi Arabia, Malaysia, Ireland, Germany, Netherlands, New Zealand, Bangladesh, Sri Lanka, Egypt, Kenya, Ghana, Indonesia, Vietnam, Thailand, Brazil, Mexico, Colombia, Argentina, Chile, Poland, Romania, Czech Republic, Israel, Qatar, Kuwait, Jordan, Oman, Bahrain, Hong Kong, Taiwan, Japan, South Korea, Portugal, Spain, Italy, France, Belgium, Switzerland, Sweden, Norway, Denmark, Finland
```

### Quick paste — US metros (35)

```
Washington DC, Arlington VA, Alexandria VA, Fairfax VA, Bethesda MD, Colorado Springs CO, San Antonio TX, Norfolk VA, Virginia Beach VA, Huntsville AL, Omaha NE, Tampa FL, Dallas TX, Fort Worth TX, Atlanta GA, Raleigh NC, Austin TX, Phoenix AZ, Seattle WA, San Jose CA, Chicago IL, Houston TX, New York NY, Boston MA, Charlotte NC, Columbus OH, Philadelphia PA, Los Angeles CA, Nashville TN, Minneapolis MN, Kansas City MO, Denver CO, Baltimore MD, Jacksonville FL, Dayton OH
```

**Exclude (optional):** None at launch. Drop countries with junk search terms or no checkout completions after 30 days.

**Notes:** Stripe checkout must work for targeted countries — verify before scaling non-US spend. Site copy is USD; no geo pricing yet.

**Federal US landing (optional):** `ccna-home.html#exam-audience` · `utm_content=federal-{market}`

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

**Names only** — keep titles short (what you sell). Put “online,” “no downloads,” labs, drag-and-drop, and timed sim in the **description** under each product, not in the name line.

**Category:** Education & training → Test preparation (or Educational software / Online education)

| # | Product / service name | Description (paste under name in Google Ads) |
|---|------------------------|-----------------------------------------------|
| 1 | CCNA 200-301 10-Day Exam Prep Access | 10 days of CCNA 200-301 v1.1 exam prep in your browser: 700+ practice questions with new items added continuously, CLI labs, drag-and-drop, portal modes, and 120-min timed sim. Current-objective alignment—not stale PDF dumps. $9.99 one-time. |
| 2 | CCNA 200-301 30-Day Exam Prep Access | 30 days of the same v1.1 library: latest CCNA practice questions, verified explanations, CLI labs, drag-and-drop sets, progress tracking, and timed simulation. New questions added continuously. $19.99 one-time. |
| 3 | Free CCNA 200-301 Practice Questions | Preview current CCNA 200-301 v1.1 practice questions—shuffled each run, instant feedback, same style as the full bank. Free on ccna-home.html; no checkout. |
| 4 | Free CCNA 200-301 Drag-and-Drop Practice | Current exam-style drag-and-drop items for CCNA 200-301 v1.1—four shuffled PBQ-style prompts per run. Free preview; no checkout. |
| 5 | Free CCNA 200-301 CLI Lab Practice | Browser VLAN CLI lab aligned to current CCNA objectives. Hands-on practice without GNS3. Free preview; no checkout. |

**Do not add as separate products:** “All online,” “no downloads,” “labs,” or “drag-and-drop” as standalone line items — those are **features inside** the portal and samples above, not separate services.

**Do not add:** Free timed simulation sample or standalone 120-min timed sim — not offered on `ccna-home.html`.

---

## RSA headlines (≤30 chars)

**Use all 15** — each headline must be **structurally different** (Google rejects duplicate patterns like multiple “X Included” or repeated “Exam Prep”). Every line below maps to **page copy** on `ccna-home.html` (H1, meta keywords, purchase fold).

```
CCNA 200-301 Practice Test
CCNA 200-301 Exam Prep
$9.99 for 10-Day Access
CCNA Practice Questions
Cisco CCNA Practice Test
CCNA Question Bank Online
Practice Tests & Simulation
700+ Questions · v1.1 2026
Drag-Drop + CLI Lab Prep
Browser CCNA Exam Prep
Timed CCNA Simulation
Latest 200-301 Questions
No PDFs — Interactive Prep
10-Day Full Library Access
Be Certified Today
```

**Pin:** H1 `CCNA 200-301 Practice Test` · H2 `$9.99 for 10-Day Access` · H3 `CCNA 200-301 Exam Prep`

**Page keyword coverage:** practice test · 200-301 · exam prep · practice questions · cisco ccna · question bank · practice tests · simulation · mock exam (via practice test) · cli lab · drag-and-drop · v1.1 · 700+ questions · browser · no PDFs · 10-day · $9.99

**Avoid swapping in:** extra “Included” headlines, duplicate “Exam Prep” without a new modifier, or headlines that don’t appear on the landing page.

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

Attach at **ad group** or **campaign** level. Sitelink text ≤25 chars · each description line ≤35 chars.

| # | Link text | Description 1 | Description 2 | Full URL |
|---|-----------|---------------|---------------|----------|
| 1 | 10-Day Access · $9.99 | Full v1.1 question bank | $9.99 one-time, no sub | `https://becertifiedtoday.com/ccna-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=portal-10d` |
| 2 | Free Practice Questions | Current v1.1 MCQ preview | Instant feedback, free | `https://becertifiedtoday.com/sample?track=ccna-questions&utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=sitelink-sample` |
| 3 | Sample Drag-and-Drop | Four PBQ-style items | Shuffled each run, free | `https://becertifiedtoday.com/sample?track=ccna-dnd&utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=sitelink-dnd` |
| 4 | Free VLAN CLI Lab | Hands-on lab in browser | No GNS3 required | `https://becertifiedtoday.com/sample?track=ccna-vlan&utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=sitelink-lab` |
| 5 | Latest v1.1 Questions | 700+ items, updated often | Not stale PDF dumps | `https://becertifiedtoday.com/ccna-home.html#home-ccna-samples-title?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=sitelink-samples` |
| 6 | Timed Sim Included | 120-min exam-style run | With 10-day portal access | `https://becertifiedtoday.com/ccna-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=portal-10d` |

**Do not use:** Free timed simulation (`#ccna-lead-capture`) or standalone 120-min sim purchase — not on `ccna-home.html`.

**Paste block (copy row by row into Google Ads):**

```
10-Day Access · $9.99 | Full v1.1 question bank | $9.99 one-time, no sub | https://becertifiedtoday.com/ccna-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=portal-10d

Free Practice Questions | Current v1.1 MCQ preview | Instant feedback, free | https://becertifiedtoday.com/sample?track=ccna-questions&utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=sitelink-sample

Sample Drag-and-Drop | Four PBQ-style items | Shuffled each run, free | https://becertifiedtoday.com/sample?track=ccna-dnd&utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=sitelink-dnd

Free VLAN CLI Lab | Hands-on lab in browser | No GNS3 required | https://becertifiedtoday.com/sample?track=ccna-vlan&utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=sitelink-lab

Latest v1.1 Questions | 700+ items, updated often | Not stale PDF dumps | https://becertifiedtoday.com/ccna-home.html#home-ccna-samples-title?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=sitelink-samples

Timed Sim Included | 120-min exam-style run | With 10-day portal access | https://becertifiedtoday.com/ccna-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=portal-10d
```

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
- [ ] 6 sitelinks pasted (table above)
- [ ] Locations: United States + Tier 1 & 2 metros (or national with presence-only)
- [ ] Pause other CCNA ad groups if testing this group solo
- [ ] GA4 `begin_checkout` imported as Primary in Google Ads
- [ ] Stripe `ccna-portal-10d` payment link = $9.99
- [ ] Test: open Final URL → only **Get 10-day access · $9.99** above the fold → click → `begin_checkout` in GA4 Realtime

---

## Site behavior (`utm_content=portal-10d`)

- Purchase fold: 10-day $9.99 only (30-day hidden)
- Auto-scroll to `#purchase`
- One-time $9.99 / 10-day popup after 5s (same as organic traffic; `bcc-10d-one-time-offer.js`)
- Mobile sticky: `Get 10-day access · $9.99`

---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v2.0
source_id: mastery-ccna-public
source_question_id: 24
bct_match_score: 0.18
blueprint: V2.0
exhibit: cli
status: review
---

# Question 110

**Topic:** Tier B — 24 on-page samples; verify answer on Cisco Tier A

**Exhibit (CLI transcript)**

```text
Traceroute from
```

A user in VLAN 10 reports that a server in another building is unreachable. The PC has a valid DHCP address, can ping its default gateway, and the access switch trunk shows VLAN 10 allowed. OSPF between R1 and R2 is FULL. the PC to 10.30.30.20 Tracing route to 10.30.30.20 1 10.10.10.1 2 ms 1 ms 1 ms 2 192.0.2.2 4 ms 4 ms 5 ms 3 * * * 4 * * * Which routed segment is the most likely place to investigate first?

- A. R1-to-R2 routed segment
- B. R2-to-next-hop routed segment
- C. PC-to-access-switch segment
- D. Access switch-to-R1 VLAN 10 path

**Stated answer (external):** B

**External explanation (unverified):**

Traceroute identifies each Layer 3 hop that returns a TTL-expired message. Because hop 1, the default gateway, replies, the local VLAN and gateway path are working. Because hop 2 replies, traffic is reaching R2 across the R1-to-R2 routed path. The first missing hop is hop 3, so the investigation should begin after R2: the R2 outbound interface, the next-hop router, or the routed segment between them. A timeout after a hop does not prove the last responding router is faulty, but it narrows the likely failure point to the path beyond that router. CCNA troubleshooting map flowchart LR A["User or network symptom"] --> B["Confirm Layer 1 and addressing"] B --> C["Check VLAN and switching path"] C --> D["Validate routing and default gateway"] D --> E["Review services and security filters"] E --> F["Verify and document the fix"] Use this map when a CCNA question describes broken connectivity. Strong answers usually move from physical/link and addressing evidence through switching, routing, services, and security filters rather than guessing from one symptom. Mini Glossary Default gateway: Router address a host uses to reach destinations outside its local subnet. Trunk port: Switch port that carries traffic for multiple VLANs. STP: Spanning Tree Protocol, used to prevent Layer 2 loops. ACL: Access control list that permits or denies traffic based on defined conditions. Administrative distance: Router preference value used when multiple route sources exist. Web preview and premium practice Web/public preview: public sample questions, the diagnostic page, and the web app entry so you can inspect the question style and explanation depth. Premium: interactive CCNA 200-301 v2.0 practice with focused drills, mixed sets, timed mock exams, detailed explanations, and progress tracking across web and mobile. Good related pages CompTIA Network+ if you need a live vendor-neutral networking practice page first Official sources Cisco CCNA 200-301 exam page In this section Free Cisco CCNA 200-301 v2.0 Practice Questions: Network Infrastructure and Connectivity Practice 10 free Cisco CCNA (Cisco CCNA 200-301 v2.0) questions on Network Infrastructure and Connectivity, with answers, explanations, and the IT Mastery next step. Free Cisco CCNA 200-301 v2.0 Practice Questions: Switching and Network Access Practice 10 free Cisco CCNA (Cisco CCNA 200-301 v2.0) questions on Switching and Network Access, with answers, explanations, and the IT Mastery next step. Free Cisco CCNA 200-301 v2.0 Practice Questions: IP Routing Practice 10 free Cisco CCNA (Cisco CCNA 200-301 v2.0) questions on IP Routing, with answers, explanations, and the IT Mastery next step. Free Cisco CCNA 200-301 v2.0 Practice Questions: Network Services and Security Practice 10 free Cisco CCNA (Cisco CCNA 200-301 v2.0) questions on Network Services and Security, with answers, explanations, and the IT Mastery next step. Free Cisco CCNA 200-301 v2.0 Practice Questions: AI, Network Operations and Management Practice 10 free Cisco CCNA (Cisco CCNA 200-301 v2.0) questions on AI, Network Operations and Management, with answers, explanations, and the IT Mastery next step. Free Cisco CCNA 200-301 v2.0 Practice Exam: Cisco CCNA Try 100 free Cisco CCNA (Cisco CCNA 200-301 v2.0) questions across the exam domains, with explanations, then continue with IT Mastery practice. Share this guide: {const e=this.textContent;this.textContent="Copied",setTimeout(()=>{this.textContent=e},1200)}):window.prompt("Copy link:",this.dataset.copyUrl),!1'>Copy link · LinkedIn · Email · Reddit 300-640 DCAI Cisco AITECH Browse Certification Practice Tests by Exam Family 300-640 DCAI AI Fundamentals and Applications AI Infrastructure Components and Architecture AI Infrastructure Deployment and Data Management AI Infrastructure Operations and Troubleshooting Free Practice Exam CCNA Network Infrastructure and Connectivity Switching and Network Access IP Routing Network Services and Security AI, Network Operations and Management Free Practice Exam Cisco AITECH Generative AI Models Prompt Engineering Ethics and Security Data Research and Analysis Development and Workflow Automation Agentic AI Free Practice Exam Mastery Exam Prep Mastery by Tokenizer provides text-first, practice-driven exam study tools with realistic exam-style questions and clear explanations for focused, self-paced learning. Navigate Support FAQ Methodology Author Page About Us For Organizations Institutional Access Training Providers Referral Partners Legal Privacy Policy Terms of Service Refund Policy (Books) Trademarks & Disclaimer Get the Apps Finance Prep — Finance, accounting, licensing & insurance App Store (Canada) · App Store (U.S.) · Google Play (Canada) · Google Play (U.S.) · Web App · Login · CISI exam pages IT Mastery — Cloud & IT certifications App Store · Google Play · Web App · Login PM Mastery — Project management & agile App Store · Google Play · Web App · Login Use these links for web access, subscriber login, and mobile installs. Each app family stays in sync across web and mobile with the same exam coverage, and Finance Prep also includes six live CISI exams. © 2026 Tokenizer Inc. (Canada) · Built by Tokenizer (function(){var r=20,h=.5,l=60,c=.8,o=!1,i=!1,s=!1,e=document.visibilityState==="visible"?Date.now():null,a=0;function n(){if(window.gtag)try{gtag.apply(null,arguments)}catch{}}function d(){return(a+(e?Date.now()-e:0))/1e3}function u(){var e=document.documentElement,t=document.body,n=e.scrollTop||t.scrollTop,s=Math.max(e.scrollHeight-e.clientHeight,1);return n/s}function t(){var e=d(),t=u();!o&&(s||e>=r&&t>=h)&&(o=!0,n("event","qualified_view",{page_location:location.href,visible_seconds:Math.round(e),depth:Math.round(t*100),site:"Mastery"})),!i&&e>=l&&t>=c&&(i=!0,n("event","deep_read",{page_location:location.href,visible_seconds:Math.round(e),depth:Math.round(t*100),site:"Mastery"}))}document.addEventListener("visibilitychange",function(){document.visibilityState==="visible"?e=Date.now():e&&(a+=Date.now()-e,e=null),t()}),window.addEventListener("scroll",t,{passive:!0}),document.addEventListener("click",function(e){var o=e.target.closest("a[data-cta]");if(!o)return;s=!0,n("event","cta_click",{id:o.getAttribute("data-cta")||"unknown",page_location:location.href,site:"Mastery"}),t()},{capture:!0}),setInterval(t,1e3),document.visibilityState==="visible"&&(e=Date.now()),t()})() import mermaid from "https:\/\/cdn.jsdelivr.net\/npm\/mermaid@latest\/dist\/mermaid.esm.min.mjs"; window.mermaid = mermaid

V2.0

**Source:** `mastery-ccna-public` · Q `24` · [link](https://masteryexamprep.com/exams/cisco/ccna/)

**BCT match score:** 0.18

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]
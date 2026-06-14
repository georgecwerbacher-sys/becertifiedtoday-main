---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v2.0
source_id: mastery-ccna-public
source_question_id: 21
bct_match_score: 0.14
blueprint: V2.0
status: review
---

# Question 107

**Topic:** Tier B — 24 on-page samples; verify answer on Cisco Tier A

A network monitoring server polls SW1 every 5 minutes. The NMS graphs interface counters and CPU normally, but it did not alert when uplink Gi1/0/48 went down for 2 minutes. Exhibit: SW1 clues show running-config | include snmp-server snmp-server community MON ro show logging | include Gi1/0/48 %LINK-3-UPDOWN: Interface Gi1/0/48, changed state to down %LINK-3-UPDOWN: Interface Gi1/0/48, changed state to up Which action best addresses the supported root cause?

- A. Increase the NMS polling interval to 30 minutes.
- B. Add a static route from SW1 to the NMS subnet.
- C. Configure SW1 to send SNMP notifications to the NMS.
- D. Change the SNMP community used for polling. Best answer: C Explanation: SNMP monitoring uses two complementary behaviors. An SNMP manager polls an agent on a device to read MIB values such as interface counters and CPU usage. SNMP notifications, such as traps or informs, are agent-initiated messages sent to a configured manager when an event occurs. In this case, polling succeeds, so basic SNMP read access and reachability are already working. The syslog proves the link-down and link-up events occurred, but the configuration shown only has a read-only community and no notification destination. To receive immediate event alerts between polling cycles, the switch must be configured to send SNMP notifications to the NMS.

V2.0

**Source:** `mastery-ccna-public` · Q `21` · [link](https://masteryexamprep.com/exams/cisco/ccna/)

**BCT match score:** 0.14

- [ ] Verified vs Cisco Tier A
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]
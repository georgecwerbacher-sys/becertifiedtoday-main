---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v2.0
source_id: mastery-ccna-public
source_question_id: 12
bct_match_score: 0.20
blueprint: V2.0
exhibit: cli
status: review
---

# Question 98

**Topic:** Tier B — 24 on-page samples; verify answer on Cisco Tier A

**Exhibit (CLI transcript)**

```text
Switch Gi1/0/12: up/up, access VLAN 30 Linux host eth0: 10.30.10.10/24, gateway 10.30.10.1 Container eth0: 172.17.0.2/16, gateway 172.17.0.1 Host route: 172.17.0.0/16 connected via docker0
```

A portable web service was moved from a VM to a container on a Linux server. Users on VLAN 30 cannot reach the service at 10.30.10.50 , but the physical server can ping the VLAN 30 gateway. Which root cause is best supported by the facts?

- A. The hypervisor virtual switch is missing a VLAN trunk.
- B. The container is attached to an isolated bridge network.
- C. The switch access port is in the wrong VLAN.
- D. The VM network adapter is disconnected.

**Stated answer (external):** B

**External explanation (unverified):**

Containers are portable and process-isolated, but their network attachment depends on the container network mode. The physical server is connected correctly to VLAN 30 because its interface is up and it can reach the VLAN gateway. The failed service has an address on the container bridge network, 172.17.0.0/16 , so hosts on VLAN 30 cannot reach it directly at 10.30.10.50 unless the service is published/NATed or attached to an appropriate VLAN-aware network. The evidence points to the container networking layer, not the physical switch, hypervisor, or VM layer.

V2.0

**Source:** `mastery-ccna-public` · Q `12` · [link](https://masteryexamprep.com/exams/cisco/ccna/)

**BCT match score:** 0.20

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]
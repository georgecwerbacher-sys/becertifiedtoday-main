---
type: pbq-scenario-solution
exam: SY0-701
scenario: subnetting-ip-addressing
last_updated: 2026-06-05
---

# Subnetting & IP Addressing — deep dive solution

> Subnet 192.168.10.0/24 for ≥6 subnets; maximize hosts; assign first three to departments.

---

## Subnet sizing

| Field | Value |
|-------|-------|
| Subnets needed | 6 |
| Borrowed bits | 3 (2³ = 8 subnets ≥ 6) |
| New prefix | **/27** |
| Subnet mask | 255.255.255.224 |
| Block size (magic #) | 32 |
| Usable hosts / subnet | 30 (2⁵ − 2) |

**/27** is the largest block that still provides at least 6 subnets **and** fits Sales (25 hosts). /28 only provides 14 hosts.

---

## Department assignments

| Dept | Hosts required | Subnet |
|------|----------------|--------|
| Sales | 25 | 192.168.10.0/27 |
| HR | 20 | 192.168.10.32/27 |
| IT | 10 | 192.168.10.64/27 |

Subsequent /27 blocks (if needed): .96, .128, .160, .192, .224.

---

## Prefix comparison (from /24)

| Prefix | Subnets | Usable hosts | Meets 6 subnets? | Meets Sales 25? |
|--------|---------|--------------|------------------|-----------------|
| /25 | 2 | 126 | No | Yes |
| /26 | 4 | 62 | No | Yes |
| **/27** | **8** | **30** | **Yes** | **Yes** |
| /28 | 16 | 14 | Yes | **No** |

---

## Common mistakes

| Mistake | Result |
|---------|--------|
| Choosing /28 | Not enough hosts for Sales |
| Choosing /26 | Only 4 subnets (< 6 required) |
| Assigning .1/27 or host addresses | Need **network** address for subnet ID |
| Skipping department order | First three subnets must map Sales → HR → IT in order |

---

## Exam takeaway

When the stem says **maximize hosts per subnet**, pick the **longest prefix (smallest subnet)** that still satisfies **subnet count** and **largest department host requirement**.

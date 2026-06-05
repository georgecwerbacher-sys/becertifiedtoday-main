# Ransomware DR — BeCertifiedToday (PBQ)

SY0-701 performance-based practice: invoke DR after ransomware with budget, SLA, and backup-age constraints.

## Constraints

| Metric | Value |
|--------|-------|
| SLA (RTO) | 4 hours max downtime |
| Last backup | 6 hours ago (RPO window) |
| IT budget | $2M / year |
| Attack | Ransomware — primary DC encrypted |

## Parts

| Section | Task |
|---------|------|
| `dr-overview` | Scenario + constraint cards |
| `dr-part1-order` | Order 8 DR activation steps |
| `dr-part2-targets` | RTO, RPO, backup frequency, warm site, why not hot |
| `dr-part3-tradeoffs` | 3 MCQs (ransom, CDP, eradication before restore) |

## Answer key

**Part 1 order:** Activate team → Isolate → Assess scope → Declare disaster → Verify backup → Failover warm → Restore → Validate/lessons

**Part 2:** RTO 4h · RPO 6h · Backup every 4h or less · Warm site · Why not hot = Both A and B

**Part 3:** B · B · B

## Chain

**Previous:** [Firewall ACL](../firewall-acl-secops/firewall-acl-secops.html)

## Preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/ransomware-dr-acme/ransomware-dr-acme.html
```

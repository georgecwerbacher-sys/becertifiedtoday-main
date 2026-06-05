# Subnetting & IP Addressing Configuration

SY0-701 PBQ: subnet 192.168.10.0/24 for ≥6 subnets (maximize hosts), then assign first three /27 networks to Sales, HR, IT.

## Section

| ID | Content |
|----|---------|
| `subnet-ip-config` | Calculator, binary visualizer, magic table, department assignment |

## Answer key

| Field | Value |
|-------|-------|
| Subnets needed | 6 |
| New prefix | /27 |
| Borrowed bits | 3 |
| Subnet mask | 255.255.255.224 |
| Block size | 32 |
| Usable hosts / subnet | 30 |
| Sales | 192.168.10.0/27 |
| HR | 192.168.10.32/27 |
| IT | 192.168.10.64/27 |

**/27** is the largest subnet size that yields at least 6 subnets and still supports Sales (25 hosts).

## SY0-701 themes

- IPv4 addressing and subnetting (1.4 / network fundamentals)
- Network segmentation for departments (3.3)

## Chain

**Previous:** [Network Diagram — Security Control Placement](../security-control-placement/security-control-placement.html)

## Preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/subnetting-ip-addressing/subnetting-ip-addressing.html
```

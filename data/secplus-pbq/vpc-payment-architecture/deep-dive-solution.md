---
type: pbq-deep-dive
exam: SY0-701
scenario: vpc-payment-architecture
last_updated: 2026-06-22
---

# VPC payment architecture — solution walkthrough

Place each component in the payment VPC and label the middle tier subnet correctly.

## Internet edge

Traffic from the Internet Gateway hits **WAF** first (node 2) to filter application-layer attacks before it reaches internal tiers.

**Answer:** Node 2: WAF

## Public subnet — load balancing

Nodes **1** and **3** sit in the public subnet as redundant **Load Balancers** distributing traffic to the app tier.

**Answer:** Nodes 1 & 3: Load Balancer

## Middle tier — application

The middle zone is a **Private subnet**. Node **4** is an **Autoscaling Instance** for elastic app capacity; nodes **5** and **6** are standard **Instance** nodes.

**Answer:** Middle subnet: Private subnet · Node 4: Autoscaling Instance · Nodes 5 & 6: Instance

## Data tier

Node **7** in the private subnet is the **Database** — no direct internet path; payment data stays isolated.

**Answer:** Node 7: Database

## Verify

Fill every dropdown, then **Check Answers**. WAF at the edge, LB in public, apps in private, DB deepest.

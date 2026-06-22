---
type: pbq-deep-dive
exam: SY0-701
scenario: web-app-subnet-zoning
last_updated: 2026-06-22
---

# Subnet zoning — solution walkthrough

## Traffic flow

User → **WAF** (filter attacks) → **Static instances** (front-end) → **Load balancers** (distribute sessions) → **Dynamic instances** (app logic) → **Database** (data at rest).

## Public subnet

- **WAF** sits at the edge before web servers inspect HTTP(S).
- **Static instances** serve public content and presentation tier.
- **Load balancers** live in the public tier to fan out traffic into the application layer without exposing app servers directly to the internet.

## Middle subnet → Private

Application logic (**dynamic instances**) should not be internet-routable. Set the middle tier to **Private** so only the load balancer path reaches app servers.

## Bottom private subnet

The **database** has no business on a public route — deepest private zone only.

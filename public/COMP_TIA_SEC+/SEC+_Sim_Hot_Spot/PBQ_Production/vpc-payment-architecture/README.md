# SEC+ VPC Payment Architecture

**SY0-701 PBQ · cloud VPC component placement**

Place WAF, load balancers, autoscaling and instance nodes, and database on a payment-application VPC diagram; label the middle tier subnet.

## Answer key

| Node | Component |
|------|-----------|
| 1 | **Load Balancer** |
| 2 | **WAF** |
| 3 | **Load Balancer** |
| 4 | **Autoscaling Instance** |
| 5 | **Instance** |
| 6 | **Instance** |
| 7 | **Database** |
| Middle tier | **Private subnet** |

## Chain position

- **Previous:** [`../malware-outbreak-classification/`](../malware-outbreak-classification/malware-outbreak-classification.html)
- **Next:** *(end of chain)*

## Preview

http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/vpc-payment-architecture/vpc-payment-architecture.html

Rebuild after section edits: `npm run build:pbq-suite`

Legacy redirect: `../simulation-vpc-payment-architecture.html`

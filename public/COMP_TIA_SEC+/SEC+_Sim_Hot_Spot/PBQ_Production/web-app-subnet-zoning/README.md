# SEC+ Web App Subnet Zoning

**SY0-701 PBQ · drag-and-drop cloud tier placement**

Place five components across three subnet zones and set the middle tier type for a secure three-tier web application deployment.

## Answer key

| Zone | Setting | Component |
|------|---------|-----------|
| **Public** | WAF slot | WAF (before web tier) |
| **Public** | Static slot | Static instances |
| **Public** | LB slot | Load balancers (between edge and app tier) |
| **Middle** | Subnet type | **Private** |
| **Middle** | App slot | Dynamic instances |
| **Private** | Data slot | Database |

## Chain position

- **Previous:** [`../site-to-site-vpn-config/`](../site-to-site-vpn-config/site-to-site-vpn-config.html)
- **Next:** [`../dark-web-account-protection/`](../dark-web-account-protection/dark-web-account-protection.html)

## Preview

http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/web-app-subnet-zoning/web-app-subnet-zoning.html

Rebuild after section edits: `npm run build:pbq-suite`

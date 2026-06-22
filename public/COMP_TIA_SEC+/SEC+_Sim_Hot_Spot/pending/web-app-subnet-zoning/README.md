# Subnet Zoning — Web Application Deployment

**SY0-701 PBQ · drag-and-drop cloud tier placement**

Place five components across three subnet zones and set the middle tier type.

## Answer key

| Zone | Setting | Component |
|------|---------|-----------|
| **Public** | WAF slot | WAF (before web tier) |
| **Public** | Static slot | Static instances |
| **Public** | LB slot | Load balancers (between edge and app tier) |
| **Middle** | Subnet type | **Private** |
| **Middle** | App slot | Dynamic instances |
| **Private** | Data slot | Database |

**Status:** Pending — not in `PBQ_Production` build chain.

## Pending chain

- **Previous:** `../site-to-site-vpn-config/`
- **Next:** *(none)*

## Preview

http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/pending/web-app-subnet-zoning/web-app-subnet-zoning.html

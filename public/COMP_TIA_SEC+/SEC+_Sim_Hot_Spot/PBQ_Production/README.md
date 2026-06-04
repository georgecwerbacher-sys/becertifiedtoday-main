# PBQ_Production

**Active workspace** for new SY0-701 PBQ scenarios before they ship to the public bank.

## Entry points

| Page | Role |
|------|------|
| [`index.html`](index.html) | Hub — links to each scenario |
| `{scenario-slug}/{scenario-slug}.html` | **One scenario, one page** — folder sidebar for all sections on that page |

Example: [`acme-rag-hr-ai/acme-rag-hr-ai.html`](acme-rag-hr-ai/acme-rag-hr-ai.html) with sections `#acme-exhibits`, `#acme-config`, …

Legacy `*-partN.html` URLs redirect to `{slug}/{slug}.html#section-id`.

## Scenario chain (Back / Next)

1. [BeCertifiedToday RAG HR AI](acme-rag-hr-ai/acme-rag-hr-ai.html)
2. [Zero Trust migration](zero-trust-zta-migration/zero-trust-zta-migration.html)
3. [Hybrid PKI audit](hybrid-pki-audit/hybrid-pki-audit.html)
4. [Ubuntu SSH breach hardening](ubuntu-ssh-breach-hardening/ubuntu-ssh-breach-hardening.html)

## Section source files

Edit `{scenario-slug}/sections/{section-id}.html`, then:

```bash
npm run build:pbq-suite
```

## Scenarios

| Folder | Sections |
|--------|----------|
| [`acme-rag-hr-ai/`](acme-rag-hr-ai/) | exhibits, config, guardrails, attacks, p2 |
| [`zero-trust-zta-migration/`](zero-trust-zta-migration/) | exhibit, concept, zone map, trade-offs |
| [`hybrid-pki-audit/`](hybrid-pki-audit/) | chain, algorithms, revocation |
| [`ubuntu-ssh-breach-hardening/`](ubuntu-ssh-breach-hardening/) | intro, sshd, fail2ban, ufw, consequences |

## Preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/index.html
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/acme-rag-hr-ai/acme-rag-hr-ai.html
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/acme-rag-hr-ai/acme-rag-hr-ai.html#acme-config
```

`PBQ_Production/` skips the paid portal gate on localhost.

## Styles

`/COMP_TIA_SEC+/js/secplus-pbq-page.css` · `pbq-folder-suite.js` · `/css/bcc-question-link-nav.css`

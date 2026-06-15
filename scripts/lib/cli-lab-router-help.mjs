/**
 * Single source of truth for router IOS `?` help docs, smoke-test profiles, and lab scaffolding.
 *
 * CLI:
 *   node scripts/lib/cli-lab-router-help.mjs comment <lab-basename-or-path>
 *   node scripts/lib/cli-lab-router-help.mjs profiles
 *   node scripts/lib/cli-lab-router-help.mjs patch-list
 */

/** @typedef {[deviceType: string, prompt: string, cmd: string, mustInclude: string[]]} HelpCase */
/** @typedef {{ label: string, pathname: string, cases: HelpCase[], switchCases?: HelpCase[] }} HelpProfile */

export const ROUTER_HELP_WIRING = [
  "IOS `?` help — ROUTER_CLI_HELP = null → DEFAULT_ROUTER_CLI_HELP (/js/cli-lab-container.js):",
  'tryAppendIosHelp(..., iosHelpOpts("router", promptText, ROUTER_CLI_HELP)) in every router submit handler.',
  "Help is read-only — using ? does not change config, advance steps, or affect completion.",
];

export const ROUTER_HELP_BASE_CHAINS = [
  "Interface/address: interface ?, interface ethernet ?, (config-if)# ip address ?,",
  "  (config-if)# ipv6 ?, ipv6 address ?",
  "OSPF chain: router ?, router ospf ?, (config-router)# ?, router-id ?,",
  "  (config-if)# ip ospf ?, ip ospf <pid> ?, ip ospf <pid> area ?, ip ospf priority ?",
  "IPv6 routing: (config)# ipv6 ? (unicast-routing)",
  "Static route chain: ip route ?, ip route <dest> ?, ip route <dest> <mask> ?,",
  "  ip route <dest> <mask> <next-hop> ?",
  "ACL: ip access-list ?, ip access-list standard ? (<1-99> / WORD); (config-std-nacl)# ? → permit/deny/remark;",
  "  permit ? → any / host / <ip-address> / <line-number>",
  "NAT: (config)# ip nat ?; ip nat inside ? (source); ip nat inside source ?;",
  "  ip nat inside source list <acl> ? (pool / interface); … pool ? (<name>); … pool <name> ? (overload);",
  "  ip nat pool ? / … netmask ? (A.B.C.D); (config-if)# ip nat ? (inside / outside)",
  "NTP: (config)# ntp ?; ntp master ?; ntp server ?; ntp source-interface ?",
  "SSH: crypto ? → key ? → generate ? → rsa ? → modulus ?;",
  "  username ?; username … privilege … secret ? (<password>); line vty / login / transport input ?",
  "Reference labs: cli-lab-static-routing.html, cli-lab-ospf_config_sim_v3.html, ipv4_ipv6_assign.html",
  "Router template: templates/labs/cli-lab-router-baseline.html",
  "Test: node scripts/test-cli-lab-help.mjs <lab>  |  node scripts/test-cli-lab-help.mjs --all",
];

/** Per-lab intro lines (before IOS help block) and optional chain overrides appended after base. */
export const ROUTER_LAB_META = {
  "cli-lab-static-routing.html": {
    label: "Static Routing",
    pathname: "/CCNA-Study/CCNA_labs/cli-lab-static-routing.html",
    intro: [
      "Reference router sample lab — IOS `?` help and CLI login banner patterns for all routers.",
      "",
      "Shared defaults (/js/cli-lab-container.js):",
      "- DEFAULT_ROUTER_CLI_HELP — baseline for every router session; override with ROUTER_CLI_HELP",
      "- Login banner (BCT_CLI_HELP_NOTICE) — injected when each router CLI modal opens",
      '- tryAppendIosHelp(line, appendFn, cliLabContainer.iosHelpOpts("router", promptText, ROUTER_CLI_HELP))',
      "- Router `?` chains (ROUTER_CLI_HELP = null): interface/ethernet, ip address, ipv6/ipv6 address,",
      "  OSPF (router → ip ospf → area → priority), (config)# ipv6 ?, static route (4-step ip route chain)",
      "- This lab: ip route ? → <dest> ? → <dest> <mask> ? → <dest> <mask> <next-hop> ?",
      "- Also see: cli-lab-ospf_config_sim_v3.html, ipv4_ipv6_assign.html",
    ],
    extraChains: [],
  },
  "cli-lab-ip-services-sim-v2.html": {
    label: "IP Services Simulation V.3",
    pathname: "/CCNA-Study/CCNA_labs/cli-lab-ip-services-sim-v2.html",
    intro: [
      "CLI lab — IP Services (NAT, ACL, NTP, SSH). Multi-router R1/R2/R3.",
    ],
    extraChains: [],
  },
  "cli-lab-nat-dhcp-sim.html": {
    label: "CCNA: DHCP, NAT, and SSH Simulation V.3",
    pathname: "/CCNA-Study/CCNA_labs/cli-lab-nat-dhcp-sim.html",
    intro: ["CLI lab — NAT overload, DHCP helper, NTP, SSH (R1 router + Sw1 switch)."],
    extraChains: [],
  },
  "cli-lab-ospf_config_sim_v3.html": {
    label: "OSPF Configuration V.3",
    pathname: "/CCNA-Study/CCNA_labs/cli-lab-ospf_config_sim_v3.html",
    intro: [
      "CCNA CLI lab — OSPF Configuration Simulation V3: graded OSPF on R1.",
      "Baseline: templates/labs/cli-lab-router-baseline.html",
    ],
    extraChains: [],
  },
  "ipv4_ipv6_assign.html": {
    label: "IPv4/IPv6 Addressing",
    pathname: "/CCNA-Study/CCNA_labs/ipv4_ipv6_assign.html",
    intro: ["CLI lab — dual-stack IPv4/IPv6 addressing on R1/R2."],
    extraChains: [],
  },
  "cli-lab-named-acl-snoopimg.html": {
    label: "Named ACL DHCP Snooping",
    pathname: "/CCNA-Study/CCNA_labs/cli-lab-named-acl-snoopimg.html",
    intro: [
      "CCNA CLI lab — Named ACL and DHCP Snooping (R1 router + switches).",
      "Kin labs: cli-lab-nat-dhcp-sim.html, cli-lab-ospf_config_sim_v3.html",
    ],
    extraChains: [],
  },
  "CCNA_Samples/cli-lab-ip-services-sim-v2.html": {
    label: "IP Services Simulation V.3 (CCNA sample URL)",
    pathname: "/CCNA-Study/CCNA_Samples/cli-lab-ip-services-sim-v2.html",
    intro: ["Sample URL shell for IP Services lab — same router help baseline."],
    extraChains: [],
  },
};

/** Shared router smoke tests included in every router profile. */
export const CORE_ROUTER_CASES = /** @type {HelpCase[]} */ ([
  ["router", "R1(config)#", "ip route ?", ["A.B.C.D"]],
  ["router", "R1(config)#", "router ?", ["ospf"]],
  ["router", "R1(config)#", "router ospf ?", ["<1-65535>"]],
  ["router", "R1(config-if)#", "ip ospf ?", ["<1-65535>"]],
  ["router", "R1(config)#", "ip access-list standard ?", ["<1-99>", "WORD"]],
  ["router", "R1(config-std-nacl)#", "permit ?", ["any", "host"]],
]);

export const IP_SERVICES_ROUTER_CASES = /** @type {HelpCase[]} */ ([
  ["router", "R2(config)#", "ip nat ?", ["inside", "outside", "pool"]],
  ["router", "R2(config)#", "ip nat pool ?", ["<name>", "netmask"]],
  ["router", "R2(config)#", "ip nat pool test_pool ?", ["netmask", "prefix-length"]],
  ["router", "R2(config)#", "ip nat pool test_pool 10.10.10.1 ?", ["netmask", "prefix-length"]],
  [
    "router",
    "R2(config)#",
    "ip nat pool test_pool 10.10.10.1 10.10.10.254 ?",
    ["netmask", "prefix-length"],
  ],
  [
    "router",
    "R2(config)#",
    "ip nat pool test_pool 10.10.10.1 10.10.10.254 netmask ?",
    ["A.B.C.D"],
  ],
  ["router", "R2(config)#", "ip nat inside ?", ["source"]],
  ["router", "R2(config)#", "ip nat inside source ?", ["list", "static"]],
  ["router", "R2(config)#", "ip nat inside source list XLATE ?", ["pool", "interface"]],
  ["router", "R2(config)#", "ip nat inside source list XLATE pool ?", ["<name>"]],
  ["router", "R2(config)#", "ip nat inside source list XLATE pool test_pool ?", ["overload"]],
  ["router", "R2(config-if)#", "ip ?", ["address", "nat"]],
  ["router", "R2(config-if)#", "ip nat ?", ["inside", "outside"]],
  ["router", "R2(config-if)#", "ip address ?", ["dhcp"]],
  ["router", "R1(config)#", "ntp ?", ["master", "server"]],
  ["router", "R1(config)#", "ntp master ?", ["<1-15>"]],
  ["router", "R2(config)#", "ntp server ?", ["A.B.C.D"]],
  ["router", "R3(config)#", "crypto ?", ["key"]],
  ["router", "R3(config)#", "crypto key ?", ["generate"]],
  ["router", "R3(config)#", "crypto key generate ?", ["rsa"]],
  ["router", "R3(config)#", "crypto key generate rsa ?", ["modulus"]],
  ["router", "R3(config)#", "crypto key generate rsa modulus ?", ["<360-4096>"]],
  ["router", "R3(config)#", "username ?", ["<WORD>"]],
  ["router", "R3(config)#", "username root privilege 15 secret ?", ["<password>"]],
  ["router", "R3(config)#", "line vty ?", ["<0-15>"]],
  ["router", "R3(config-line)#", "login ?", ["local"]],
  ["router", "R3(config-line)#", "transport input ?", ["ssh"]],
]);

export const NAT_DHCP_ROUTER_CASES = /** @type {HelpCase[]} */ ([
  ["router", "R1(config)#", "ip nat ?", ["inside", "outside", "inside source"]],
  ["router", "R1(config)#", "ip nat inside ?", ["source"]],
  ["router", "R1(config)#", "ip nat inside source ?", ["list", "static"]],
  ["router", "R1(config-if)#", "ip nat ?", ["inside", "outside"]],
  ["router", "R1(config)#", "ntp ?", ["master", "server"]],
  ["router", "R1(config)#", "ntp master ?", ["<1-15>"]],
  ["router", "R1(config)#", "ntp source-interface ?", ["Loopback0"]],
]);

export const NAT_DHCP_SWITCH_CASES = /** @type {HelpCase[]} */ ([
  ["switch", "Sw1(config)#", "ntp server ?", ["A.B.C.D"]],
  ["switch", "Sw1(config)#", "interface ethernet ?", ["<0-9>"]],
  ["switch", "Sw1(config-if)#", "ip ?", ["helper-address"]],
  ["switch", "Sw1(config-if)#", "ip helper-address ?", ["A.B.C.D"]],
  ["switch", "Sw1(config)#", "crypto ?", ["key"]],
  ["switch", "Sw1(config)#", "crypto key ?", ["generate"]],
  ["switch", "Sw1(config)#", "crypto key generate ?", ["rsa"]],
  ["switch", "Sw1(config)#", "crypto key generate rsa ?", ["modulus"]],
  ["switch", "Sw1(config)#", "crypto key generate rsa modulus ?", ["<360-4096>"]],
  ["switch", "Sw1(config)#", "ip ssh ?", ["version"]],
  ["switch", "Sw1(config)#", "ip ssh version ?", ["2"]],
]);

/** @type {Record<string, HelpProfile>} */
export const ROUTER_HELP_PROFILES = {
  "cli-lab-static-routing.html": {
    label: ROUTER_LAB_META["cli-lab-static-routing.html"].label,
    pathname: ROUTER_LAB_META["cli-lab-static-routing.html"].pathname,
    cases: [
      ...CORE_ROUTER_CASES,
      ["router", "R1(config)#", "ip route 10.0.0.0 255.0.0.0 ?", ["A.B.C.D", "GigabitEthernet"]],
    ],
  },
  "cli-lab-ip-services-sim-v2.html": {
    label: ROUTER_LAB_META["cli-lab-ip-services-sim-v2.html"].label,
    pathname: ROUTER_LAB_META["cli-lab-ip-services-sim-v2.html"].pathname,
    cases: [...CORE_ROUTER_CASES, ...IP_SERVICES_ROUTER_CASES],
  },
  "CCNA_Samples/cli-lab-ip-services-sim-v2.html": {
    label: ROUTER_LAB_META["CCNA_Samples/cli-lab-ip-services-sim-v2.html"].label,
    pathname: ROUTER_LAB_META["CCNA_Samples/cli-lab-ip-services-sim-v2.html"].pathname,
    cases: [...CORE_ROUTER_CASES, ...IP_SERVICES_ROUTER_CASES],
  },
  "cli-lab-nat-dhcp-sim.html": {
    label: ROUTER_LAB_META["cli-lab-nat-dhcp-sim.html"].label,
    pathname: ROUTER_LAB_META["cli-lab-nat-dhcp-sim.html"].pathname,
    cases: [...CORE_ROUTER_CASES, ...NAT_DHCP_ROUTER_CASES],
  },
  "cli-lab-ospf_config_sim_v3.html": {
    label: ROUTER_LAB_META["cli-lab-ospf_config_sim_v3.html"].label,
    pathname: ROUTER_LAB_META["cli-lab-ospf_config_sim_v3.html"].pathname,
    cases: CORE_ROUTER_CASES,
  },
  "ipv4_ipv6_assign.html": {
    label: ROUTER_LAB_META["ipv4_ipv6_assign.html"].label,
    pathname: ROUTER_LAB_META["ipv4_ipv6_assign.html"].pathname,
    cases: CORE_ROUTER_CASES,
  },
  "cli-lab-named-acl-snoopimg.html": {
    label: ROUTER_LAB_META["cli-lab-named-acl-snoopimg.html"].label,
    pathname: ROUTER_LAB_META["cli-lab-named-acl-snoopimg.html"].pathname,
    cases: CORE_ROUTER_CASES,
  },
};

export const ALL_PROFILE_KEYS = [
  "cli-lab-static-routing.html",
  "cli-lab-nat-dhcp-sim.html",
  "cli-lab-ip-services-sim-v2.html",
  "CCNA_Samples/cli-lab-ip-services-sim-v2.html",
  "cli-lab-ospf_config_sim_v3.html",
  "ipv4_ipv6_assign.html",
  "cli-lab-named-acl-snoopimg.html",
];

/**
 * @param {string} labRef basename or path
 */
export function normalizeLabBasename(labRef) {
  const normalized = String(labRef || "")
    .replace(/^public\//, "")
    .replace(/^CCNA-Study\/CCNA_labs\//, "")
    .replace(/^CCNA-Study\//, "");
  if (ROUTER_HELP_PROFILES[normalized]) return normalized;
  const basename = normalized.replace(/^.*\//, "");
  if (ROUTER_HELP_PROFILES[basename]) return basename;
  return normalized;
}

/** Chains + wiring only (patch existing lab HTML without replacing intro). */
export function buildRouterHelpChainsOnly() {
  return [...ROUTER_HELP_WIRING, "", ...ROUTER_HELP_BASE_CHAINS].join("\n");
}

/**
 * Build the IOS `?` help section for an HTML comment (no comment delimiters).
 * @param {string} labRef
 * @param {string[]} [customIntro]
 */
export function buildRouterHelpComment(labRef, customIntro = []) {
  const basename = normalizeLabBasename(labRef);
  const meta = ROUTER_LAB_META[basename];
  const intro = customIntro.length ? customIntro : meta?.intro || [];
  const extra = meta?.extraChains || [];
  const lines = [...intro];
  if (intro.length) lines.push("");
  lines.push(...ROUTER_HELP_WIRING, "", ...ROUTER_HELP_BASE_CHAINS);
  if (extra.length) {
    lines.push(...extra);
  }
  return lines.join("\n");
}

/**
 * @param {string} labRef
 */
export function getHelpProfile(labRef) {
  const basename = normalizeLabBasename(labRef);
  const profile = ROUTER_HELP_PROFILES[basename];
  if (!profile) return null;
  return { ...profile, cases: [...profile.cases] };
}

function main() {
  const [cmd, arg] = process.argv.slice(2);
  if (cmd === "comment" && arg) {
    process.stdout.write(buildRouterHelpComment(arg));
    return;
  }
  if (cmd === "comment-chains") {
    process.stdout.write(buildRouterHelpChainsOnly());
    return;
  }
  if (cmd === "profiles") {
    console.log(JSON.stringify(Object.keys(ROUTER_HELP_PROFILES), null, 2));
    return;
  }
  if (cmd === "patch-list") {
    console.log(ALL_PROFILE_KEYS.join("\n"));
    return;
  }
  console.error("Usage: node scripts/lib/cli-lab-router-help.mjs <comment|comment-chains|profiles|patch-list> [lab]");
  process.exit(1);
}

if (import.meta.url === new URL(process.argv[1], "file:").href) {
  main();
}

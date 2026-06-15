/**
 * Single source of truth for switch IOS `?` help docs, smoke-test profiles, and lab scaffolding.
 *
 * CLI:
 *   node scripts/lib/cli-lab-switch-help.mjs comment <lab-basename-or-path>
 *   node scripts/lib/cli-lab-switch-help.mjs comment-chains
 *   node scripts/lib/cli-lab-switch-help.mjs profiles
 *   node scripts/lib/cli-lab-switch-help.mjs patch-list
 */

/** @typedef {[deviceType: string, prompt: string, cmd: string, mustInclude: string[]]} HelpCase */
/** @typedef {{ label: string, pathname: string, cases: HelpCase[] }} SwitchHelpProfile */

export const SWITCH_HELP_WIRING = [
  "IOS `?` help — SWITCH_CLI_HELP = null → DEFAULT_SWITCH_CLI_HELP (/js/cli-lab-container.js):",
  'tryAppendIosHelp(..., iosHelpOpts("switch", promptText, SWITCH_CLI_HELP)) in every switch submit handler.',
  "Help is read-only — using ? does not change config, advance steps, or affect completion.",
];

export const SWITCH_HELP_BASE_CHAINS = [
  "VLAN: (config)# vlan ?  |  (config-vlan)# ? (name / exit / end)",
  "Show: show vlan ?  →  show vlan id ?  |  show vlan name ?",
  "Interface: (config)# interface ?  →  interface gigabitethernet ?  |  interface range ?",
  "Access: (config-if)# switchport mode ?  |  switchport access ?  |  switchport voice ?  →  switchport voice vlan ?",
  "Trunk/LACP: (config-if)# switchport trunk ?  →  encapsulation ?  →  native ?  →  allowed vlan ?",
  "  channel-group ?  →  channel-group <n> mode ?  |  channel-protocol ?  |  lldp ?",
  "Identity: username / line vty / login / transport input ? (shared with router baseline)",
  "L3 services (switch): (config-if)# ip ? → helper-address ? (A.B.C.D); (config)# ntp server ?;",
  "  crypto ? → key ? → generate ? → rsa ? → modulus ?; ip ssh ? → version ?",
  "Reference labs: cli-lab-vlan-sim.html, cli-lab-trunk_lacp.html, cli-lab-native_vlan_lacp.html, cli-lab-nat-dhcp-sim.html",
  "Switch template: templates/labs/cli-lab-switch-baseline.html",
  "Test: node scripts/test-cli-lab-help.mjs <lab>  |  npm run test:cli-lab-help",
];

export const SWITCH_LAB_META = {
  "cli-lab-vlan-sim.html": {
    label: "CCNA: VLAN Setup Simulation V.3",
    pathname: "/CCNA-Study/CCNA_labs/cli-lab-vlan-sim.html",
    intro: [
      "Reference switch sample lab — IOS `?` help and CLI login banner patterns for all switches.",
      "CCNA VLAN lab: dual switches Sw1/Sw2, VLANs 77/88 (data) and 177/188 (voice), access-mode assignments.",
    ],
    extraChains: [],
  },
  "cli-lab-trunk_lacp.html": {
    label: "CCNA: LACP and Trunking Simulation V.3",
    pathname: "/CCNA-Study/CCNA_labs/cli-lab-trunk_lacp.html",
    intro: [
      "Reference switch lab — trunk, allowed VLANs, and LACP EtherChannel on Sw1/Sw2.",
    ],
    extraChains: [],
  },
  "cli-lab-native_vlan_lacp.html": {
    label: "CCNA: Native VLAN and LACP Simulation V.3",
    pathname: "/CCNA-Study/CCNA_labs/cli-lab-native_vlan_lacp.html",
    intro: ["CLI lab — native VLAN and LACP across multiple switches."],
    extraChains: [],
  },
  "cli-lab-nat-dhcp-sim.html": {
    label: "CCNA: DHCP, NAT, and SSH Simulation V.3",
    pathname: "/CCNA-Study/CCNA_labs/cli-lab-nat-dhcp-sim.html",
    intro: [
      "Mixed router/switch lab — R1 NAT/DHCP/NTP; Sw1 DHCP relay (helper-address), NTP, crypto RSA, SSH v2.",
    ],
    extraChains: [],
  },
};

/** Shared switch smoke tests for access/VLAN labs. */
export const CORE_SWITCH_CASES = /** @type {HelpCase[]} */ ([
  ["switch", "Sw1(config)#", "vlan ?", ["<1-4094>"]],
  ["switch", "Sw1(config)#", "interface ?", ["vlan"]],
  ["switch", "Sw1(config)#", "interface gigabitethernet ?", ["<0-9>", "range"]],
  ["switch", "Sw1(config-if)#", "switchport mode ?", ["access", "trunk"]],
  ["switch", "Sw1(config-if)#", "switchport access ?", ["vlan"]],
  ["switch", "Sw1#", "show vlan ?", ["brief", "id"]],
]);

/** Trunk + LACP chains used in cli-lab-trunk_lacp.html. */
export const TRUNK_LACP_SWITCH_CASES = /** @type {HelpCase[]} */ ([
  ["switch", "Sw1(config-if)#", "switchport trunk ?", ["encapsulation", "allowed"]],
  ["switch", "Sw1(config-if)#", "switchport trunk encapsulation ?", ["dot1q"]],
  ["switch", "Sw1(config-if)#", "switchport trunk native ?", ["vlan"]],
  ["switch", "Sw1(config-if)#", "switchport trunk allowed vlan ?", ["add", "all", "none"]],
  ["switch", "Sw1(config-if)#", "channel-group ?", ["<1-255>"]],
  ["switch", "Sw1(config-if)#", "channel-group 1 mode ?", ["active", "on"]],
  ["switch", "Sw1(config-if)#", "lldp ?", ["run", "transmit"]],
]);

/** NAT/DHCP lab Sw1 — L3 services on switch. */
export const NAT_DHCP_SWITCH_CASES = /** @type {HelpCase[]} */ ([
  ["switch", "Sw1(config)#", "ntp server ?", ["A.B.C.D"]],
  ["switch", "Sw1(config)#", "interface ethernet ?", ["<0-9>"]],
  ["switch", "Sw1(config-if)#", "ip ?", ["helper-address"]],
  ["switch", "Sw1(config-if)#", "ip helper-address ?", ["A.B.C.D"]],
  ["switch", "Sw1(config-if)#", "crypto ?", ["key"]],
  ["switch", "Sw1(config)#", "crypto ?", ["key"]],
  ["switch", "Sw1(config)#", "crypto key ?", ["generate"]],
  ["switch", "Sw1(config)#", "crypto key generate ?", ["rsa"]],
  ["switch", "Sw1(config)#", "crypto key generate rsa ?", ["modulus"]],
  ["switch", "Sw1(config)#", "crypto key generate rsa modulus ?", ["<360-4096>"]],
  ["switch", "Sw1(config)#", "ip ssh ?", ["version"]],
  ["switch", "Sw1(config)#", "ip ssh version ?", ["2"]],
]);

/** @type {Record<string, SwitchHelpProfile>} */
export const SWITCH_HELP_PROFILES = {
  "cli-lab-vlan-sim.html": {
    label: SWITCH_LAB_META["cli-lab-vlan-sim.html"].label,
    pathname: SWITCH_LAB_META["cli-lab-vlan-sim.html"].pathname,
    cases: [
      ...CORE_SWITCH_CASES,
      ["switch", "Sw1(config-if)#", "switchport voice ?", ["vlan"]],
    ],
  },
  "cli-lab-trunk_lacp.html": {
    label: SWITCH_LAB_META["cli-lab-trunk_lacp.html"].label,
    pathname: SWITCH_LAB_META["cli-lab-trunk_lacp.html"].pathname,
    cases: [...CORE_SWITCH_CASES, ...TRUNK_LACP_SWITCH_CASES],
  },
  "cli-lab-native_vlan_lacp.html": {
    label: SWITCH_LAB_META["cli-lab-native_vlan_lacp.html"].label,
    pathname: SWITCH_LAB_META["cli-lab-native_vlan_lacp.html"].pathname,
    cases: [...CORE_SWITCH_CASES, ...TRUNK_LACP_SWITCH_CASES],
  },
  "cli-lab-nat-dhcp-sim.html": {
    label: SWITCH_LAB_META["cli-lab-nat-dhcp-sim.html"].label,
    pathname: SWITCH_LAB_META["cli-lab-nat-dhcp-sim.html"].pathname,
    cases: NAT_DHCP_SWITCH_CASES,
  },
};

export const ALL_SWITCH_PROFILE_KEYS = [
  "cli-lab-vlan-sim.html",
  "cli-lab-trunk_lacp.html",
  "cli-lab-native_vlan_lacp.html",
  "cli-lab-nat-dhcp-sim.html",
];

/**
 * @param {string} labRef
 */
export function normalizeSwitchLabBasename(labRef) {
  const normalized = String(labRef || "")
    .replace(/^public\//, "")
    .replace(/^CCNA-Study\/CCNA_labs\//, "")
    .replace(/^CCNA-Study\//, "");
  if (SWITCH_HELP_PROFILES[normalized]) return normalized;
  const basename = normalized.replace(/^.*\//, "");
  if (SWITCH_HELP_PROFILES[basename]) return basename;
  return normalized;
}

export function buildSwitchHelpChainsOnly() {
  return [...SWITCH_HELP_WIRING, "", ...SWITCH_HELP_BASE_CHAINS].join("\n");
}

/**
 * @param {string} labRef
 * @param {string[]} [customIntro]
 */
export function buildSwitchHelpComment(labRef, customIntro = []) {
  const basename = normalizeSwitchLabBasename(labRef);
  const meta = SWITCH_LAB_META[basename];
  const intro = customIntro.length ? customIntro : meta?.intro || [];
  const extra = meta?.extraChains || [];
  const lines = [...intro];
  if (intro.length) lines.push("");
  lines.push(...SWITCH_HELP_WIRING, "", ...SWITCH_HELP_BASE_CHAINS);
  if (extra.length) lines.push(...extra);
  return lines.join("\n");
}

/**
 * @param {string} labRef
 */
export function getSwitchHelpProfile(labRef) {
  const basename = normalizeSwitchLabBasename(labRef);
  return SWITCH_HELP_PROFILES[basename] || null;
}

function main() {
  const [cmd, arg] = process.argv.slice(2);
  if (cmd === "comment" && arg) {
    process.stdout.write(buildSwitchHelpComment(arg));
    return;
  }
  if (cmd === "comment-chains") {
    process.stdout.write(buildSwitchHelpChainsOnly());
    return;
  }
  if (cmd === "profiles") {
    console.log(JSON.stringify(Object.keys(SWITCH_HELP_PROFILES), null, 2));
    return;
  }
  if (cmd === "patch-list") {
    console.log(ALL_SWITCH_PROFILE_KEYS.join("\n"));
    return;
  }
  console.error("Usage: node scripts/lib/cli-lab-switch-help.mjs <comment|comment-chains|profiles|patch-list> [lab]");
  process.exit(1);
}

if (import.meta.url === new URL(process.argv[1], "file:").href) {
  main();
}

#!/usr/bin/env node
/**
 * Smoke-test IOS ? help chains for CCNA CLI labs (router + switch).
 *
 * Usage:
 *   node scripts/test-cli-lab-help.mjs cli-lab-nat-dhcp-sim.html
 *   node scripts/test-cli-lab-help.mjs cli-lab-ip-services-sim-v2.html
 *   node scripts/test-cli-lab-help.mjs CCNA_Samples/cli-lab-ip-services-sim-v2.html
 *   node scripts/test-cli-lab-help.mjs --all
 */
import { readFileSync } from "fs";
import vm from "vm";

function makeEl() {
  const el = {
    classList: { add() {}, remove() {} },
    children: [],
    style: {},
    firstChild: null,
    setAttribute() {},
    appendChild(child) {
      this.children.push(child);
      if (!this.firstChild) this.firstChild = child;
    },
    insertBefore(child) {
      this.appendChild(child);
    },
    querySelector() {
      return null;
    },
    querySelectorAll() {
      return [];
    },
  };
  return el;
}

function loadCliLabContainer(pathname) {
  const head = Object.assign(makeEl(), { querySelector: () => null });
  const document = {
    head,
    body: makeEl(),
    querySelector: () => null,
    addEventListener: () => {},
    createElement: () => makeEl(),
  };
  const sandbox = {
    window: { location: { pathname } },
    document,
    CustomEvent: class {},
    console,
    location: { pathname },
  };
  sandbox.window.document = document;
  vm.createContext(sandbox);
  vm.runInContext(readFileSync("public/js/cli-lab-container.js", "utf8"), sandbox);
  return sandbox.window.cliLabContainer;
}

const IP_SERVICES_CASES = [
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
  ["router", "R2(config)#", "ip access-list standard ?", ["<1-99>", "WORD"]],
  ["router", "R2(config-std-nacl)#", "permit ?", ["any", "host"]],
  ["router", "R1(config)#", "ntp ?", ["master", "server"]],
  ["router", "R1(config)#", "ntp master ?", ["<1-15>"]],
  ["router", "R2(config)#", "ntp server ?", ["A.B.C.D"]],
  ["router", "R3(config)#", "crypto ?", ["key"]],
  ["router", "R3(config)#", "crypto key ?", ["generate"]],
  ["router", "R3(config)#", "crypto key generate ?", ["rsa"]],
  ["router", "R3(config)#", "crypto key generate rsa ?", ["modulus"]],
  ["router", "R3(config)#", "crypto key generate rsa modulus ?", ["<360-4096>"]],
  ["router", "R3(config)#", "username ?", ["<WORD>"]],
  ["router", "R3(config)#", "line vty ?", ["<0-15>"]],
  ["router", "R3(config-line)#", "login ?", ["local"]],
  ["router", "R3(config-line)#", "transport input ?", ["ssh"]],
];

const NAT_DHCP_CASES = [
  ["router", "R1(config)#", "ip nat ?", ["inside", "outside", "inside source"]],
  ["router", "R1(config)#", "ip nat inside ?", ["source"]],
  ["router", "R1(config)#", "ip nat inside source ?", ["list", "static"]],
  ["router", "R1(config-if)#", "ip nat ?", ["inside", "outside"]],
  ["router", "R1(config)#", "ntp ?", ["master", "server"]],
  ["router", "R1(config)#", "ntp master ?", ["<1-15>"]],
  ["router", "R1(config)#", "ntp source-interface ?", ["Loopback0"]],
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
];

/** @type {Record<string, { label: string, pathname: string, cases: typeof IP_SERVICES_CASES }>} */
const PROFILES = {
  "cli-lab-ip-services-sim-v2.html": {
    label: "IP Services Simulation V.3",
    pathname: "/CCNA-Study/CCNA_labs/cli-lab-ip-services-sim-v2.html",
    cases: IP_SERVICES_CASES,
  },
  "CCNA_Samples/cli-lab-ip-services-sim-v2.html": {
    label: "IP Services Simulation V.3 (CCNA sample URL)",
    pathname: "/CCNA-Study/CCNA_Samples/cli-lab-ip-services-sim-v2.html",
    cases: IP_SERVICES_CASES,
  },
  "cli-lab-nat-dhcp-sim.html": {
    label: "NAT DHCP SSH",
    pathname: "/CCNA-Study/CCNA_labs/cli-lab-nat-dhcp-sim.html",
    cases: NAT_DHCP_CASES,
  },
};

const ALL_KEYS = [
  "cli-lab-nat-dhcp-sim.html",
  "cli-lab-ip-services-sim-v2.html",
  "CCNA_Samples/cli-lab-ip-services-sim-v2.html",
];

function resolveProfileKey(arg) {
  if (!arg) return "cli-lab-ip-services-sim-v2.html";
  if (arg === "--all") return "--all";
  const normalized = arg
    .replace(/^public\//, "")
    .replace(/^CCNA-Study\//, "");
  if (PROFILES[normalized]) return normalized;
  const basename = normalized.replace(/^.*\//, "");
  if (PROFILES[basename]) return basename;
  return null;
}

function runProfile(key) {
  const profile = PROFILES[key];
  const c = loadCliLabContainer(profile.pathname);
  let failed = 0;

  console.log(`Lab: ${profile.label}`);
  console.log(`Path: ${profile.pathname}\n`);

  for (const [deviceType, prompt, cmd, mustInclude] of profile.cases) {
    let out = null;
    const ok = c.tryAppendIosHelp(
      cmd,
      (_cls, text) => {
        out = text;
      },
      c.iosHelpOpts(deviceType, prompt, null)
    );

    const missing = mustInclude.filter((needle) => !out || !out.includes(needle));
    if (!ok || missing.length) {
      failed += 1;
      console.error("FAIL", `[${deviceType}]`, prompt, cmd);
      if (!ok) console.error("  help handler returned false");
      if (missing.length) console.error("  missing:", missing.join(", "));
      if (out) console.error("  got:", out.replace(/\n/g, " | "));
      continue;
    }
    console.log("ok", `[${deviceType}]`, prompt, cmd);
  }

  if (failed) {
    console.error(`\n${failed} help check(s) failed for ${profile.label}.\n`);
    return failed;
  }

  console.log(`\nAll ${profile.cases.length} help checks passed for ${profile.label}.\n`);
  return 0;
}

const arg = process.argv[2];
const resolved = resolveProfileKey(arg);

if (!resolved) {
  console.error(`Unknown lab: ${arg}`);
  console.error("Known labs:", Object.keys(PROFILES).join(", "));
  console.error("Or pass --all to run every profile.");
  process.exit(1);
}

if (resolved === "--all") {
  let totalFailed = 0;
  for (const key of ALL_KEYS) {
    totalFailed += runProfile(key);
  }
  if (totalFailed) {
    console.error(`${totalFailed} profile(s) had failures.`);
    process.exit(1);
  }
  console.log(`All ${ALL_KEYS.length} lab profiles passed.`);
  process.exit(0);
}

process.exit(runProfile(resolved) ? 1 : 0);

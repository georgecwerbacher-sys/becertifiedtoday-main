#!/usr/bin/env node
/**
 * Smoke-test IOS ? help chains for CCNA CLI labs (router + switch).
 *
 * Profiles and router help docs: scripts/lib/cli-lab-router-help.mjs
 *
 * Usage:
 *   node scripts/test-cli-lab-help.mjs cli-lab-nat-dhcp-sim.html
 *   node scripts/test-cli-lab-help.mjs cli-lab-ip-services-sim-v2.html
 *   node scripts/test-cli-lab-help.mjs CCNA_Samples/cli-lab-ip-services-sim-v2.html
 *   node scripts/test-cli-lab-help.mjs --all
 */
import { readFileSync } from "fs";
import vm from "vm";
import {
  ALL_PROFILE_KEYS,
  ROUTER_HELP_PROFILES,
  getHelpProfile,
  normalizeLabBasename,
} from "./lib/cli-lab-router-help.mjs";

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

function resolveProfileKey(arg) {
  if (!arg) return "cli-lab-ip-services-sim-v2.html";
  if (arg === "--all") return "--all";
  const normalized = normalizeLabBasename(arg);
  if (ROUTER_HELP_PROFILES[normalized]) return normalized;
  return null;
}

function runProfile(key) {
  const profile = getHelpProfile(key);
  if (!profile) {
    console.error(`No profile for ${key}`);
    return 1;
  }
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
  console.error("Known labs:", Object.keys(ROUTER_HELP_PROFILES).join(", "));
  console.error("Or pass --all to run every profile.");
  process.exit(1);
}

if (resolved === "--all") {
  let totalFailed = 0;
  for (const key of ALL_PROFILE_KEYS) {
    totalFailed += runProfile(key);
  }
  if (totalFailed) {
    console.error(`${totalFailed} profile(s) had failures.`);
    process.exit(1);
  }
  console.log(`All ${ALL_PROFILE_KEYS.length} lab profiles passed.`);
  process.exit(0);
}

process.exit(runProfile(resolved) ? 1 : 0);

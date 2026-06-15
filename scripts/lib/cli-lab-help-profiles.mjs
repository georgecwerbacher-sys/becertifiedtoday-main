/**
 * Unified router + switch CLI `?` help smoke-test profiles.
 */
import {
  ROUTER_HELP_PROFILES,
  ALL_PROFILE_KEYS as ROUTER_PROFILE_KEYS,
  normalizeLabBasename,
  getHelpProfile as getRouterHelpProfile,
  NAT_DHCP_SWITCH_CASES,
} from "./cli-lab-router-help.mjs";
import {
  SWITCH_HELP_PROFILES,
  ALL_SWITCH_PROFILE_KEYS,
  normalizeSwitchLabBasename,
  getSwitchHelpProfile,
} from "./cli-lab-switch-help.mjs";

/** @typedef {import("./cli-lab-router-help.mjs").HelpCase} HelpCase */

/** Labs with both router and switch devices. */
const MIXED_LAB_SWITCH_CASES = {
  "cli-lab-nat-dhcp-sim.html": NAT_DHCP_SWITCH_CASES,
};

/** @type {Record<string, { label: string, pathname: string, cases: HelpCase[] }>} */
export const LAB_HELP_PROFILES = { ...ROUTER_HELP_PROFILES, ...SWITCH_HELP_PROFILES };

/** Profile keys in default --all run order (router labs, then switch-only labs). */
export const ALL_PROFILE_KEYS = [
  ...ROUTER_PROFILE_KEYS,
  ...ALL_SWITCH_PROFILE_KEYS.filter((k) => !ROUTER_PROFILE_KEYS.includes(k)),
];

/**
 * @param {string} labRef
 */
export function resolveProfileKey(labRef) {
  const normalized = normalizeLabBasename(labRef);
  if (LAB_HELP_PROFILES[normalized]) return normalized;
  const switchKey = normalizeSwitchLabBasename(labRef);
  if (LAB_HELP_PROFILES[switchKey]) return switchKey;
  return null;
}

/**
 * @param {string} key
 */
export function getLabHelpProfile(key) {
  const switchOnly = getSwitchHelpProfile(key);
  if (switchOnly && !ROUTER_HELP_PROFILES[key]) {
    return switchOnly;
  }

  const routerProfile = getRouterHelpProfile(key);
  if (!routerProfile) {
    return switchOnly;
  }

  const extraSwitch = MIXED_LAB_SWITCH_CASES[key] || routerProfile.switchCases || [];
  if (!extraSwitch.length) {
    return routerProfile;
  }

  return {
    label: routerProfile.label,
    pathname: routerProfile.pathname,
    cases: [...routerProfile.cases, ...extraSwitch],
  };
}

export { normalizeLabBasename, normalizeSwitchLabBasename };

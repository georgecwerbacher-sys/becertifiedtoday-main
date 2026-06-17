#!/usr/bin/env node
/**
 * Unit tests for cliLabContainer.createRunningConfigView (public/js/cli-lab-container.js).
 */
import { readFileSync } from "node:fs";
import vm from "node:vm";

function makeEl() {
  return {
    classList: { add() {}, remove() {} },
    children: [],
    style: {},
    appendChild() {},
    querySelector: () => null,
    querySelectorAll: () => [],
  };
}

const document = {
  head: makeEl(),
  body: makeEl(),
  querySelector: () => null,
  querySelectorAll: () => [],
  addEventListener: () => {},
  createElement: () => makeEl(),
  dispatchEvent: () => {},
};

const sandbox = {
  window: { location: { pathname: "/test" } },
  document,
  CustomEvent: class {},
  console,
  location: { pathname: "/test" },
};
sandbox.window.document = document;
vm.createContext(sandbox);
vm.runInContext(readFileSync("public/js/cli-lab-container.js", "utf8"), sandbox);

const { createRunningConfigView } = sandbox.window.cliLabContainer;
let failed = 0;

function assert(cond, msg) {
  if (!cond) {
    console.error("FAIL:", msg);
    failed++;
  }
}

const baseline = [
  "hostname R1",
  "ip domain-name lab.local",
  "ip name-server 209.165.202.129",
  "!",
  "interface Ethernet0/1",
  " ip address 172.16.0.9 255.255.255.252",
  " duplex auto",
  "!",
  "access-list 192 permit ip 192.168.0.0 0.0.3.255 any",
  "!",
  "line con 0",
  "!",
  "end",
].join("\r\n");

const view = createRunningConfigView(baseline);
assert(view.render() === baseline, "baseline unchanged before apply");

view.applyGlobal("ntp master");
const withNtp = view.render();
assert(withNtp.includes("ntp master"), "ntp master present");
assert(
  withNtp.indexOf("ntp master") > withNtp.indexOf("ip name-server 209.165.202.129"),
  "ntp master after ip name-server"
);
assert(withNtp.indexOf("ntp master") < withNtp.indexOf("access-list 192"), "ntp master before access-list");

view.applyGlobal("ip nat inside source list 192 interface Ethernet0/0 overload");
const withNat = view.render();
assert(
  withNat.indexOf("ip nat inside source list 192") > withNat.indexOf("access-list 192 permit"),
  "NAT overload immediately after matching access-list"
);
assert(withNat.indexOf("ip nat inside source list 192") < withNat.indexOf("line con 0"), "NAT before line templates");

view.applyInterface("e0/1", "ip helper-address 172.16.0.9");
const withHelper = view.render();
assert(withHelper.includes(" ip helper-address 172.16.0.9"), "helper-address under interface");
assert(
  withHelper.indexOf(" ip helper-address 172.16.0.9") > withHelper.indexOf(" ip address 172.16.0.9"),
  "helper after ip address"
);
assert(
  withHelper.indexOf(" ip helper-address 172.16.0.9") < withHelper.indexOf(" duplex auto"),
  "helper before duplex"
);

view.reset();
assert(view.render() === baseline, "reset restores baseline only");

assert(
  sandbox.window.cliLabContainer.cryptoKeyGenerateRsaSysMsg(2048) ===
    "% Generating 2048 bit RSA keys, keys will be non-exportable...",
  "RSA 2048 sys message"
);
assert(
  sandbox.window.cliLabContainer.cryptoKeyGenerateRsaSysMsg(4096) ===
    "% Generating 4096 bit RSA keys, keys will be non-exportable...",
  "RSA 4096 sys message"
);
assert(
  sandbox.window.cliLabContainer.parseCryptoKeyGenerateRsaModulus(
    "crypto key generate rsa general-keys modulus 2048"
  ) === 2048,
  "parse general-keys modulus 2048"
);

if (failed) {
  console.error(failed + " test(s) failed");
  process.exit(1);
}
console.log("OK — createRunningConfigView");

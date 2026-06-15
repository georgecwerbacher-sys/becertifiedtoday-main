#!/usr/bin/env node
/** @deprecated Use scripts/test-cli-lab-help.mjs cli-lab-ip-services-sim-v2.html */
import { spawnSync } from "child_process";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const dir = dirname(fileURLToPath(import.meta.url));
const result = spawnSync(
  process.execPath,
  [join(dir, "test-cli-lab-help.mjs"), "cli-lab-ip-services-sim-v2.html"],
  { stdio: "inherit" }
);
process.exit(result.status ?? 1);

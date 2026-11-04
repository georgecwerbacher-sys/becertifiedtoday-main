/**
 * Item pools for learner-generated weak-area practice exams.
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const PUBLIC = path.join(ROOT, "public");

const FREE_POOLS = {
  ccna: [
    {
      id: "sample-question-1",
      url: "/CCNA-Study/CCNA_Samples/sample-question-1.html",
      domain: "1.0",
    },
    {
      id: "sample-question-2",
      url: "/CCNA-Study/CCNA_Samples/sample-question-2.html",
      domain: "2.0",
    },
    {
      id: "sample-question-3",
      url: "/CCNA-Study/CCNA_Samples/sample-question-3.html",
      domain: "3.0",
    },
    {
      id: "sample-question-4",
      url: "/CCNA-Study/CCNA_Samples/sample-question-4.html",
      domain: "4.0",
    },
    {
      id: "sample-question-5",
      url: "/CCNA-Study/CCNA_Samples/sample-question-5.html",
      domain: "5.0",
    },
  ],
  encor: [
    {
      id: "sample-question-1",
      url: "/CCNP-ENCOR-Study/ENCOR_Samples/sample-question-1.html",
      domain: "1.0",
    },
    {
      id: "sample-question-2",
      url: "/CCNP-ENCOR-Study/ENCOR_Samples/sample-question-2.html",
      domain: "3.0",
    },
    {
      id: "sample-question-3",
      url: "/CCNP-ENCOR-Study/ENCOR_Samples/sample-question-3.html",
      domain: "5.0",
    },
    {
      id: "sample-question-4",
      url: "/CCNP-ENCOR-Study/ENCOR_Samples/sample-question-4.html",
      domain: "6.0",
    },
    {
      id: "sample-question-5",
      url: "/CCNP-ENCOR-Study/ENCOR_Samples/sample-question-5.html",
      domain: "4.0",
    },
  ],
  secplus: [
    {
      id: "sample-question-1",
      url: "/COMP_TIA_SEC+/SEC+_Samples/sample-question-1.html",
      domain: "1.0",
    },
    {
      id: "sample-question-2",
      url: "/COMP_TIA_SEC+/SEC+_Samples/sample-question-2.html",
      domain: "2.0",
    },
    {
      id: "sample-question-3",
      url: "/COMP_TIA_SEC+/SEC+_Samples/sample-question-3.html",
      domain: "3.0",
    },
  ],
  ccnaauto: [
    {
      id: "rest-api-success-status-code-200",
      url: "/CCNAAUTO-Study/CCNAAUTO_Questions/rest-api-success-status-code-200.html",
      domain: "3.0",
    },
    {
      id: "docker-app-security-benefits",
      url: "/CCNAAUTO-Study/CCNAAUTO_Questions/docker-app-security-benefits.html",
      domain: "4.0",
    },
    {
      id: "virtual-platform-hypervisor",
      url: "/CCNAAUTO-Study/CCNAAUTO_Questions/virtual-platform-hypervisor.html",
      domain: "1.0",
    },
  ],
};

function readJsonSafe(rel) {
  try {
    const full = path.join(PUBLIC, rel);
    if (!fs.existsSync(full)) return null;
    return JSON.parse(fs.readFileSync(full, "utf8"));
  } catch {
    return null;
  }
}

function shuffle(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const t = a[i];
    a[i] = a[j];
    a[j] = t;
  }
  return a;
}

function majorDomain(domain) {
  return String(domain || "")
    .trim()
    .split(".")[0];
}

/** Paid ENCOR pool from study-config + subjects. */
function encorPaidPool() {
  const cfg = readJsonSafe("CCNP-ENCOR-Study/js/study-config.json");
  const subjects = readJsonSafe("CCNP-ENCOR-Study/js/question-subjects.json");
  const ids = (cfg && cfg.allIds) || [];
  const qmap = (subjects && subjects.questions) || {};
  return ids.map((id) => {
    const entry = qmap[String(id)];
    const section =
      typeof entry === "string" ? entry : entry && entry.section ? entry.section : "";
    return {
      id: String(id),
      url: `/CCNP-ENCOR-Study/ENCOR_Questions/question-${id}.html`,
      domain: section || "3.0",
      sessionKey: "encor",
    };
  });
}

function freePool(track) {
  return (FREE_POOLS[track] || []).map((x) => ({ ...x, sessionKey: track }));
}

/**
 * @param {{track:string, paid:boolean, weakItemIds?:string[], weakDomains?:string[], limit:number}} opts
 */
export function buildGeneratedExam(opts) {
  const track = String(opts.track || "").toLowerCase();
  const limit = Math.min(Math.max(Number(opts.limit) || 10, 1), 20);
  const weakItemIds = new Set((opts.weakItemIds || []).map(String));
  const weakMajors = new Set(
    (opts.weakDomains || []).map((d) => majorDomain(d)).filter(Boolean)
  );

  let pool = opts.paid && track === "encor" ? encorPaidPool() : freePool(track);
  if (!pool.length) pool = freePool(track);

  const preferred = [];
  const rest = [];
  for (const item of pool) {
    const maj = majorDomain(item.domain);
    if (weakItemIds.has(String(item.id)) || (maj && weakMajors.has(maj))) {
      preferred.push(item);
    } else {
      rest.push(item);
    }
  }

  const picked = shuffle(preferred).concat(shuffle(rest)).slice(0, limit);
  return {
    track,
    paidPool: Boolean(opts.paid && track === "encor"),
    items: picked.map((p, i) => ({
      index: i,
      id: p.id,
      url: p.url,
      domain: p.domain || null,
    })),
  };
}

export function freePoolSize(track) {
  return (FREE_POOLS[track] || []).length;
}

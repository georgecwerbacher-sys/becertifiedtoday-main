/**
 * Append marketing leads to marketing-vault/leads/*.csv (synced via git).
 *
 * Production (Vercel): set GITHUB_LEADS_TOKEN — commits each row via GitHub Contents API.
 * Local / vercel dev: appends to the CSV file on disk when no token is set.
 */
import fs from "fs";
import path from "path";

const CSV_HEADER =
  "captured_at_utc,event,email,magnet,product,source,utm_source,utm_medium,utm_campaign,utm_content";

const DEFAULT_CSV_REL = "marketing-vault/leads/secplus-free-simulation-leads.csv";

function csvCell(value) {
  const s = value == null ? "" : String(value);
  if (/[",\n\r]/.test(s)) {
    return `"${s.replace(/"/g, '""')}"`;
  }
  return s;
}

function formatLeadRow(row) {
  return [
    row.captured_at_utc,
    row.event,
    row.email,
    row.magnet,
    row.product,
    row.source,
    row.utm_source,
    row.utm_medium,
    row.utm_campaign,
    row.utm_content,
  ]
    .map(csvCell)
    .join(",");
}

function resolveCsvRelPath() {
  return (process.env.LEADS_CSV_PATH || DEFAULT_CSV_REL).replace(/^\/+/, "");
}

function resolveGithubRepo() {
  const combined = (process.env.GITHUB_LEADS_REPO || "").trim();
  if (combined && combined.includes("/")) {
    const [owner, name] = combined.split("/", 2);
    if (owner && name) return { owner, repo: name };
  }
  const owner = (process.env.GITHUB_LEADS_REPO_OWNER || process.env.VERCEL_GIT_REPO_OWNER || "").trim();
  const repo = (process.env.GITHUB_LEADS_REPO_NAME || process.env.VERCEL_GIT_REPO_SLUG || "").trim();
  if (!owner || !repo) return null;
  return { owner, repo };
}

function decodeGithubContent(data) {
  if (!data || !data.content) return "";
  const raw = data.content.replace(/\n/g, "");
  return Buffer.from(raw, "base64").toString("utf8");
}

function encodeGithubContent(text) {
  return Buffer.from(text, "utf8").toString("base64");
}

async function fetchGithubFile({ token, owner, repo, filePath }) {
  const url = `https://api.github.com/repos/${encodeURIComponent(owner)}/${encodeURIComponent(repo)}/contents/${filePath.split("/").map(encodeURIComponent).join("/")}`;
  const res = await fetch(url, {
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "becertifiedtoday-lead-csv",
    },
  });
  if (res.status === 404) {
    return { content: CSV_HEADER + "\n", sha: null };
  }
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`github_get_${res.status}:${text.slice(0, 200)}`);
  }
  const data = await res.json();
  return { content: decodeGithubContent(data), sha: data.sha || null };
}

async function putGithubFile({ token, owner, repo, filePath, content, sha, message }) {
  const url = `https://api.github.com/repos/${encodeURIComponent(owner)}/${encodeURIComponent(repo)}/contents/${filePath.split("/").map(encodeURIComponent).join("/")}`;
  const body = {
    message,
    content: encodeGithubContent(content),
    committer: {
      name: "Be Certified Today Lead Capture",
      email: "leads@becertifiedtoday.com",
    },
  };
  if (sha) body.sha = sha;
  const res = await fetch(url, {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/vnd.github+json",
      "Content-Type": "application/json",
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "becertifiedtoday-lead-csv",
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`github_put_${res.status}:${text.slice(0, 200)}`);
  }
  return true;
}

async function appendLeadToGithubCsv(row, attempt) {
  attempt = attempt || 0;
  const token = (process.env.GITHUB_LEADS_TOKEN || "").trim();
  const repoInfo = resolveGithubRepo();
  if (!token || !repoInfo) {
    return { ok: false, reason: "github_not_configured" };
  }

  const filePath = resolveCsvRelPath();
  const line = formatLeadRow(row);
  const file = await fetchGithubFile({ token, ...repoInfo, filePath });
  let content = file.content || "";
  if (!content.trim()) {
    content = CSV_HEADER + "\n";
  } else if (!content.includes("captured_at_utc")) {
    content = CSV_HEADER + "\n" + content.replace(/^\n+/, "");
  }
  if (!content.endsWith("\n")) content += "\n";
  content += line + "\n";

  try {
    await putGithubFile({
      token,
      ...repoInfo,
      filePath,
      content,
      sha: file.sha,
      message: `Lead: ${row.event} ${row.email}`,
    });
    return { ok: true, backend: "github" };
  } catch (err) {
    const msg = String(err?.message || err);
    if (attempt < 2 && msg.includes("github_put_409")) {
      return appendLeadToGithubCsv(row, attempt + 1);
    }
    throw err;
  }
}

function appendLeadToLocalCsv(row) {
  const rel = resolveCsvRelPath();
  const filePath = path.join(process.cwd(), rel);
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  if (!fs.existsSync(filePath) || fs.statSync(filePath).size === 0) {
    fs.writeFileSync(filePath, CSV_HEADER + "\n", "utf8");
  }
  fs.appendFileSync(filePath, formatLeadRow(row) + "\n", "utf8");
  return { ok: true, backend: "local" };
}

function canWriteLocalCsv() {
  if ((process.env.LEADS_CSV_DISABLE_LOCAL || "").trim() === "1") return false;
  if ((process.env.GITHUB_LEADS_TOKEN || "").trim()) return false;
  if (process.env.VERCEL === "1") return false;
  return true;
}

export function buildLeadCsvRow(body, defaults) {
  defaults = defaults || {};
  const utm = body && typeof body.utm === "object" && body.utm ? body.utm : {};
  return {
    captured_at_utc: new Date().toISOString(),
    event: defaults.event || "lead_signup",
    email: defaults.email || "",
    magnet: defaults.magnet || "",
    product: defaults.product || "",
    source: defaults.source || body?.source || "",
    utm_source: utm.utm_source || body?.utm_source || "",
    utm_medium: utm.utm_medium || body?.utm_medium || "",
    utm_campaign: utm.utm_campaign || body?.utm_campaign || "",
    utm_content: utm.utm_content || body?.utm_content || "",
  };
}

export async function appendMarketingLeadCsv(row) {
  if (!row || !row.email) {
    return { ok: false, reason: "missing_email" };
  }

  try {
    const token = (process.env.GITHUB_LEADS_TOKEN || "").trim();
    if (token) {
      return await appendLeadToGithubCsv(row);
    }
    if (canWriteLocalCsv()) {
      return appendLeadToLocalCsv(row);
    }
    console.warn("[lead-csv] No GITHUB_LEADS_TOKEN and local CSV disabled — row not persisted:", row.email);
    return { ok: false, reason: "not_configured" };
  } catch (err) {
    console.error("[lead-csv] append failed:", err?.message || err);
    return { ok: false, reason: "error" };
  }
}

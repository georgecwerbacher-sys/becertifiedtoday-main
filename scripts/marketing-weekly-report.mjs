#!/usr/bin/env node
/**
 * Pull GA4 summary + top pages and write marketing-vault/03-reports/weekly/YYYY-MM-DD.md
 *
 * Usage:
 *   node scripts/marketing-weekly-report.mjs
 *   node scripts/marketing-weekly-report.mjs --range 28d
 *   node scripts/marketing-weekly-report.mjs --force
 *
 * Env: same as /admin/analytics — GA_PROPERTY_ID + service account in .env.local
 */
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import {
  analyticsApiReady,
  fetchAnalyticsSummary,
  fetchDailyTrend,
  fetchTopPages,
  getAnalyticsDataClient,
  getGoogleAnalyticsEnv,
  rangeFromPreset,
} from "../server-lib/google-analytics.js";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..");
const VAULT = join(ROOT, "marketing-vault");
const REPORTS_DIR = join(VAULT, "03-reports", "weekly");

const AUTO_START = "<!-- auto:body -->";
const AUTO_END = "<!-- /auto:body -->";

function loadEnvLocal() {
  const path = join(ROOT, ".env.local");
  if (!existsSync(path)) return;
  const text = readFileSync(path, "utf8");
  for (const line of text.split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const eq = trimmed.indexOf("=");
    if (eq <= 0) continue;
    const key = trimmed.slice(0, eq).trim();
    let val = trimmed.slice(eq + 1).trim();
    if (
      (val.startsWith('"') && val.endsWith('"')) ||
      (val.startsWith("'") && val.endsWith("'"))
    ) {
      val = val.slice(1, -1);
    }
    if (!process.env[key]) process.env[key] = val;
  }
}

function parseArgs(argv) {
  let range = "7d";
  let force = false;
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === "--range" && argv[i + 1]) {
      range = argv[++i];
    } else if (argv[i] === "--force") {
      force = true;
    }
  }
  return { range, force };
}

function todayIso() {
  return new Date().toISOString().slice(0, 10);
}

function yamlScalar(v) {
  if (v == null || v === "") return "null";
  if (typeof v === "number") return String(v);
  const s = String(v);
  if (/^[a-z0-9._-]+$/i.test(s)) return s;
  return JSON.stringify(s);
}

function fmt(n) {
  return Number(n || 0).toLocaleString("en-US");
}

function fmtDuration(sec) {
  const s = Math.round(Number(sec) || 0);
  if (s < 60) return `${s}s`;
  return `${Math.floor(s / 60)}m ${s % 60}s`;
}

function formatGaDate(yyyymmdd) {
  if (!yyyymmdd || yyyymmdd.length !== 8) return yyyymmdd;
  return `${yyyymmdd.slice(0, 4)}-${yyyymmdd.slice(4, 6)}-${yyyymmdd.slice(6, 8)}`;
}

async function fetchCampaignSessions(client, propertyId, range) {
  try {
    const [response] = await client.runReport({
      property: `properties/${propertyId}`,
      dateRanges: [range],
      dimensions: [{ name: "sessionCampaignName" }],
      metrics: [{ name: "sessions" }, { name: "activeUsers" }],
      orderBys: [{ metric: { metricName: "sessions" }, desc: true }],
      limit: 15,
    });
    return (response.rows || []).map((row) => ({
      campaign: row.dimensionValues?.[0]?.value || "(not set)",
      sessions: Number(row.metricValues?.[0]?.value || 0),
      users: Number(row.metricValues?.[1]?.value || 0),
    }));
  } catch {
    return [];
  }
}

function buildAutoBody(data) {
  const { summary, topPages, dailyTrend, campaigns, rangePreset, fetchedAt, gaReady } = data;
  const lines = [];

  if (!gaReady) {
    lines.push(
      "> GA4 Data API not configured locally. Copy metrics from [/admin/analytics.html](/admin/analytics.html) or set `GA_PROPERTY_ID` + service account in `.env.local`, then re-run this script.",
      ""
    );
  } else {
    lines.push(`Fetched: ${fetchedAt}`, "");
  }

  lines.push("## Summary", "");
  if (summary) {
    lines.push(
      "| Metric | Value |",
      "|--------|------:|",
      `| Active users | ${fmt(summary.activeUsers)} |`,
      `| New users | ${fmt(summary.newUsers)} |`,
      `| Sessions | ${fmt(summary.sessions)} |`,
      `| Page views | ${fmt(summary.screenPageViews)} |`,
      `| Avg session | ${fmtDuration(summary.averageSessionDurationSeconds)} |`,
      `| Engagement rate | ${(Number(summary.engagementRate || 0) * 100).toFixed(1)}% |`,
      ""
    );
  }

  if (campaigns && campaigns.length) {
    lines.push("## Sessions by campaign (GA4)", "");
    lines.push("| Campaign | Sessions | Users |", "|----------|----------:|------:|");
    for (const c of campaigns) {
      lines.push(`| ${c.campaign} | ${fmt(c.sessions)} | ${fmt(c.users)} |`);
    }
    lines.push("");
  }

  if (topPages && topPages.length) {
    lines.push("## Top pages", "");
    lines.push("| Path | Views | Users |", "|------|------:|------:|");
    for (const p of topPages) {
      lines.push(`| \`${p.pagePath}\` | ${fmt(p.screenPageViews)} | ${fmt(p.activeUsers)} |`);
    }
    lines.push("");
  }

  if (dailyTrend && dailyTrend.length) {
    lines.push("## Daily trend", "");
    lines.push("| Date | Users | Sessions | Page views |", "|------|------:|---------:|-----------:|");
    for (const d of dailyTrend) {
      lines.push(
        `| ${formatGaDate(d.date)} | ${fmt(d.activeUsers)} | ${fmt(d.sessions)} | ${fmt(d.screenPageViews)} |`
      );
    }
    lines.push("");
  }

  lines.push(
    "## Funnel (manual until Stripe pull)",
    "",
    "Fill from GA4 events + Stripe admin panel:",
    "",
    "- `begin_checkout` events:",
    "- Portal / test purchases:",
    "- Revenue (USD):",
    ""
  );

  return lines.join("\n");
}

function buildFrontmatter({ date, rangePreset, summary, gaReady }) {
  const s = summary || {};
  return [
    "---",
    "type: weekly-report",
    `date: ${date}`,
    `range: ${rangePreset}`,
    "site: becertifiedtoday.com",
    `sessions: ${s.sessions ?? 0}`,
    `users: ${s.activeUsers ?? 0}`,
    `page_views: ${s.screenPageViews ?? 0}`,
    "begin_checkout: null",
    "purchases: null",
    "revenue_usd: null",
    `ga_configured: ${gaReady}`,
    "source: scripts/marketing-weekly-report.mjs",
    "---",
  ].join("\n");
}

function mergeReport(existing, frontmatter, autoBody, date) {
  const humanTail = [
    "",
    "## Decisions",
    "",
    "- ",
    "",
    "## Follow-up",
    "",
    "- ",
    "",
    "## Notes",
    "",
  ].join("\n");

  const autoBlock = `${AUTO_START}\n${autoBody}\n${AUTO_END}`;

  if (!existing) {
    return [
      frontmatter,
      "",
      `# Weekly marketing report — ${date}`,
      "",
      autoBlock,
      humanTail,
    ].join("\n");
  }

  const startIdx = existing.indexOf(AUTO_START);
  const endIdx = existing.indexOf(AUTO_END);
  if (startIdx >= 0 && endIdx > startIdx) {
    const before = existing.slice(0, startIdx);
    const after = existing.slice(endIdx + AUTO_END.length);
    const fmEnd = existing.indexOf("---", 4);
    const restAfterFm = fmEnd >= 0 ? existing.slice(fmEnd + 3).replace(/^\s*\n/, "") : "";
    const titleMatch = restAfterFm.match(/^#\s+Weekly marketing report[^\n]*\n*/);
    const title = titleMatch ? titleMatch[0].trimEnd() : `# Weekly marketing report — ${date}`;
    return [frontmatter, "", title, "", autoBlock, after.replace(/^\s*/, "\n")].join("\n");
  }

  return [frontmatter, "", `# Weekly marketing report — ${date}`, "", autoBlock, humanTail].join("\n");
}

async function main() {
  loadEnvLocal();
  const { range: rangePreset, force } = parseArgs(process.argv.slice(2));
  const date = todayIso();
  const outPath = join(REPORTS_DIR, `${date}.md`);

  if (existsSync(outPath) && !force) {
    console.error(`Report already exists: ${outPath}`);
    console.error("Use --force to regenerate metrics (preserves Decisions/Notes outside auto block).");
    process.exit(1);
  }

  mkdirSync(REPORTS_DIR, { recursive: true });

  const env = getGoogleAnalyticsEnv();
  const gaReady = analyticsApiReady(env);
  let summary = null;
  let topPages = [];
  let dailyTrend = [];
  let campaigns = [];
  const fetchedAt = new Date().toISOString();

  if (gaReady) {
    const range = rangeFromPreset(rangePreset);
    const client = getAnalyticsDataClient(env);
    [summary, topPages, dailyTrend, campaigns] = await Promise.all([
      fetchAnalyticsSummary(client, env.propertyId, range),
      fetchTopPages(client, env.propertyId, range, 15),
      fetchDailyTrend(client, env.propertyId, range),
      fetchCampaignSessions(client, env.propertyId, range),
    ]);
  }

  const frontmatter = buildFrontmatter({ date, rangePreset, summary, gaReady });
  const autoBody = buildAutoBody({
    summary,
    topPages,
    dailyTrend,
    campaigns,
    rangePreset,
    fetchedAt,
    gaReady,
  });

  const existing = existsSync(outPath) ? readFileSync(outPath, "utf8") : null;
  const content = mergeReport(existing, frontmatter, autoBody, date);
  writeFileSync(outPath, content, "utf8");

  console.log(`Wrote ${outPath.replace(ROOT + "/", "")}`);
  if (!gaReady) {
    console.log("Note: GA4 not configured — stub report written. Set credentials in .env.local and re-run with --force.");
  }
}

main().catch((err) => {
  console.error(err.message || err);
  process.exit(1);
});

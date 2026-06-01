/**
 * Internal / admin traffic excluded from GA4 Data API reports and portal subscriber lists.
 * Set GA_INTERNAL_EMAILS (comma-separated) on Vercel; defaults include site owner test email.
 */

const DEFAULT_INTERNAL_EMAILS = [
  "georgecwerbacher@gmail.com",
  "georeg.werbacher@gmail.com",
];

export function parseInternalEmailsFromEnv(env = process.env) {
  const raw = (env.GA_INTERNAL_EMAILS || "").trim();
  const source = raw || DEFAULT_INTERNAL_EMAILS.join(",");
  return source
    .split(/[,;\s]+/)
    .map((e) => e.trim().toLowerCase())
    .filter((e) => e.includes("@"));
}

export function isInternalAnalyticsEmail(email, env = process.env) {
  const em = String(email || "")
    .trim()
    .toLowerCase();
  if (!em) return false;
  return parseInternalEmailsFromEnv(env).includes(em);
}

/**
 * GA4 Data API dimensionFilter for runReport (core), not runRealtimeReport.
 * Realtime API does not support hostName and requires any filtered dimension in the request.
 */
export function gaCustomerTrafficDimensionFilter() {
  return {
    andGroup: {
      expressions: [
        {
          notExpression: {
            filter: {
              fieldName: "hostName",
              stringFilter: { matchType: "EXACT", value: "localhost" },
            },
          },
        },
        {
          notExpression: {
            filter: {
              fieldName: "hostName",
              stringFilter: { matchType: "EXACT", value: "127.0.0.1" },
            },
          },
        },
        {
          notExpression: {
            filter: {
              fieldName: "pagePath",
              stringFilter: { matchType: "BEGINS_WITH", value: "/admin" },
            },
          },
        },
      ],
    },
  };
}

export function filterPortalSubscriberRows(rows, env = process.env) {
  if (!Array.isArray(rows)) return [];
  return rows.filter((row) => !isInternalAnalyticsEmail(row && row.email, env));
}

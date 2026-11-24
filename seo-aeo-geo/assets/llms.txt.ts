import type { APIRoute } from "astro";

interface PageItem {
  title: string;
  slug: string;
  summary: string;
  category: string;
  is_optional?: boolean;
}

function resolveBaseUrl(request: Request, site?: URL): { hostname: string; baseUrl: string } {
  const forwarded = request.headers.get("x-forwarded-host")?.split(",")[0]?.trim();
  const host = (forwarded || request.headers.get("host") || site?.host || "localhost").split(":")[0].toLowerCase();
  const proto = request.headers.get("x-forwarded-proto") || (host === "localhost" || host === "127.0.0.1" ? "http" : "https");
  return { hostname: host, baseUrl: `${proto}://${host}` };
}

/**
 * Optional Directus adapter — runs only when DIRECTUS_URL is explicitly set.
 * Projects without Directus pass their static/DB page catalog directly.
 */
async function fetchOptionalDirectusPages(): Promise<PageItem[]> {
  const directusUrl = import.meta.env.DIRECTUS_URL || process.env.DIRECTUS_URL;
  if (!directusUrl) return [];
  const token = import.meta.env.DIRECTUS_STATIC_TOKEN || process.env.DIRECTUS_STATIC_TOKEN;
  try {
    const res = await fetch(
      `${directusUrl.replace(/\/$/, "")}/items/pages?filter[status][_eq]=published&fields=title,slug,summary,category,is_optional&sort=category,title`,
      { headers: token ? { Authorization: `Bearer ${token}` } : {} }
    );
    if (!res.ok) return [];
    const json = (await res.json()) as { data?: PageItem[] };
    return json.data || [];
  } catch {
    return [];
  }
}

export const GET: APIRoute = async ({ request, site }) => {
  const { hostname, baseUrl } = resolveBaseUrl(request, site);
  const envPrefix = hostname.toUpperCase().replace(/[^A-Z0-9]+/g, "_");
  const brandName =
    process.env[`${envPrefix}_BRAND_NAME`] ||
    process.env.SITE_BRAND_NAME ||
    hostname;
  const brandSummary =
    process.env[`${envPrefix}_BRAND_SUMMARY`] ||
    process.env.SITE_BRAND_SUMMARY ||
    `Structured machine-readable knowledge index for ${hostname}.`;

  const pages = await fetchOptionalDirectusPages();
  const corePages = pages.filter((p) => !p.is_optional);
  const optionalPages = pages.filter((p) => p.is_optional);
  const categories = Array.from(new Set(corePages.map((p) => p.category || "General")));

  let markdown = `# ${brandName}\n\n> ${brandSummary}\n\nCanonical URL: ${baseUrl}\n`;

  for (const category of categories) {
    markdown += `\n## ${category}\n\n`;
    for (const page of corePages.filter((p) => (p.category || "General") === category)) {
      markdown += `- [${page.title}](${baseUrl}/${page.slug}): ${page.summary || page.title}\n`;
    }
  }

  if (optionalPages.length > 0) {
    markdown += `\n## Optional\n\n`;
    for (const page of optionalPages) {
      markdown += `- [${page.title}](${baseUrl}/${page.slug}): ${page.summary || page.title}\n`;
    }
  }

  if (pages.length === 0) {
    markdown += `\n## Primary Endpoints\n\n- [Home](${baseUrl}/): Primary landing and canonical entity graph\n- [Full Context](${baseUrl}/llms-full.txt): Extended semantic documentation\n`;
  }

  const isPreview = hostname.endsWith(".zerops.app") || hostname === "localhost" || hostname === "127.0.0.1";

  return new Response(markdown, {
    status: 200,
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": isPreview ? "no-store" : "public, max-age=3600, s-maxage=86400, stale-while-revalidate=604800",
      ...(isPreview ? { "X-Robots-Tag": "noindex, nofollow" } : {}),
    },
  });
};

import type { APIRoute } from "astro";

function resolveRequestHost(request: Request, site?: URL): string {
  const forwarded = request.headers.get("x-forwarded-host")?.split(",")[0]?.trim();
  const direct = request.headers.get("host")?.trim();
  const raw = forwarded || direct || site?.host || "localhost";
  return raw.split(":")[0].toLowerCase();
}

function isPreviewHost(hostname: string): boolean {
  return (
    hostname.endsWith(".zerops.app") ||
    hostname === "localhost" ||
    hostname === "127.0.0.1"
  );
}

export const GET: APIRoute = async ({ request, site }) => {
  const hostname = resolveRequestHost(request, site);

  if (isPreviewHost(hostname)) {
    return new Response("User-agent: *\nDisallow: /\n", {
      headers: {
        "Content-Type": "text/plain; charset=utf-8",
        "Cache-Control": "no-store",
        "X-Robots-Tag": "noindex, nofollow",
      },
    });
  }

  const proto = request.headers.get("x-forwarded-proto") || "https";
  const baseUrl = `${proto}://${hostname}`;

  const robots = `# ==============================================================================
# ROBOTS.TXT (AI-Optimized 2026 Standard — Host: ${hostname})
# ==============================================================================

# Search & Retrieval AI Engines (Allowed for real-time AI citation)
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: PerplexityBot
User-agent: Perplexity-User
User-agent: Bingbot
User-agent: Googlebot
Allow: /

# Training-Only AI Bots
User-agent: GPTBot
User-agent: ClaudeBot
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: CCBot
User-agent: Bytespider
User-agent: Meta-ExternalAgent
Disallow: /admin/
Disallow: /adminn/
Disallow: /api/private/
Allow: /

# General Crawlers
User-agent: *
Disallow: /admin/
Disallow: /adminn/
Disallow: /api/private/
Allow: /

# Sitemaps & AI Knowledge Manifest
Sitemap: ${baseUrl}/sitemap-index.xml
Sitemap: ${baseUrl}/sitemap.xml
`;

  return new Response(robots, {
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "public, max-age=3600",
    },
  });
};

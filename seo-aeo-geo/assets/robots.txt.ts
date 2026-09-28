import type { APIRoute } from 'astro';

export const GET: APIRoute = async ({ site }) => {
  const baseUrl = site ? site.toString().replace(/\/$/, '') : 'https://example.com';

  const robots = `# ==============================================================================
# ROBOTS.TXT (AI-Optimized 2026 Standard)
# ==============================================================================

# Search & Retrieval AI Engines (Permitidos para citación en respuestas de IA)
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
Disallow: /api/private/
Allow: /

# Rastreadores Generales
User-agent: *
Disallow: /admin/
Disallow: /api/private/
Allow: /

# Directivas de Sitemaps
Sitemap: ${baseUrl}/sitemap-index.xml
Sitemap: ${baseUrl}/sitemap.xml
`;

  return new Response(robots, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=86400',
    },
  });
};

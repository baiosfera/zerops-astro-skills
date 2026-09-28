import type { APIRoute } from 'astro';

const DIRECTUS_URL = import.meta.env.DIRECTUS_URL || process.env.DIRECTUS_URL || 'http://directus:8055';
const DIRECTUS_STATIC_TOKEN = import.meta.env.DIRECTUS_STATIC_TOKEN || process.env.DIRECTUS_STATIC_TOKEN;

interface PageItem {
  id: string;
  title: string;
  slug: string;
  summary: string;
  category: string;
  is_optional?: boolean;
}

export const GET: APIRoute = async ({ site }) => {
  const baseUrl = site ? site.toString().replace(/\/$/, '') : 'https://example.com';
  let pages: PageItem[] = [];

  try {
    const res = await fetch(`${DIRECTUS_URL}/items/pages?filter[status][_eq]=published&fields=id,title,slug,summary,category,is_optional&sort=category,title`, {
      headers: DIRECTUS_STATIC_TOKEN ? { Authorization: `Bearer ${DIRECTUS_STATIC_TOKEN}` } : {},
    });
    if (res.ok) {
      const data = await res.json();
      pages = data.data || [];
    }
  } catch (error) {
    console.error('Error al generar llms.txt desde Directus:', error);
  }

  const corePages = pages.filter((p) => !p.is_optional);
  const optionalPages = pages.filter((p) => p.is_optional);
  const categories = Array.from(new Set(corePages.map((p) => p.category || 'General')));

  let markdown = `# Gentle AI Knowledge Base\n\n`;
  markdown += `> Plataforma empresarial de agentes autónomos y software de alta fidelidad desplegado sobre Zerops.\n\n`;
  markdown += `Este manifiesto provee documentación limpia y referencias estructuradas para motores de búsqueda de IA y agentes de código.\n\n`;

  for (const category of categories) {
    markdown += `## ${category}\n\n`;
    const catPages = corePages.filter((p) => (p.category || 'General') === category);
    for (const page of catPages) {
      markdown += `- [${page.title}](${baseUrl}/${page.slug}.md): ${page.summary || page.title}\n`;
    }
    markdown += `\n`;
  }

  if (optionalPages.length > 0) {
    markdown += `## Opcional\n\n`;
    for (const page of optionalPages) {
      markdown += `- [${page.title}](${baseUrl}/${page.slug}.md): ${page.summary || page.title}\n`;
    }
    markdown += `\n`;
  }

  return new Response(markdown, {
    status: 200,
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=3600, s-maxage=86400, stale-while-revalidate=604800',
    },
  });
};

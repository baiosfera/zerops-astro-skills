# Modern SEO, AEO & GEO Developer Reference Manual: Schemas, llms.txt & Knowledge Graphs (v1.0)

> **Documento Normativo SSoT:** Referencia técnica del Pipeline Multi-Superficie 2026: optimización para motores de búsqueda tradicionales (SEO), motores de respuesta directa (AEO - Perplexity, SearchGPT, Gemini), optimización generativa (GEO - `llms.txt` v2) y grafos semánticos RDF interconectados (`@graph`) con `schema-dts`.

---

## 1. Arquitectura de Optimización Multi-Superficie (2026)

### A. AEO (Answer Engine Optimization)
- **Lead Direct-Answer Block**: Bloque conciso de 40 a 60 palabras inmediatamente después del encabezado H1/H2 que responde directamente a la intención de búsqueda.
- **Microformatos Estructurados**: Listas semánticas (`<ol>` para instrucciones paso a paso, `<ul>` con negritas iniciales para atributos) y tablas comparativas HTML nativas sin JavaScript.
- **E-E-A-T Semántico**: Vinculación explícita de autores mediante `@id` de tipo `Person` con enlaces `sameAs` a Wikidata, GitHub o perfiles académicos.

### B. GEO (Generative Engine Optimization & `llms.txt` v2)
- **Manifiesto `/llms.txt`**: Archivo Markdown curado en la raíz del sitio conforme a la especificación `llmstxt.org v2` que resume el conocimiento y estructura del sitio para crawlers de IA y pipelines RAG.
- **Cabeceras y Enlaces de Descubrimiento**:
  ```html
  <link rel="describedby" href="/llms.txt" />
  <link rel="alternate" type="text/markdown" href="/articulo.md" />
  ```

---

## 2. Modelado de Grafos Semánticos con `schema-dts` (`@graph`)

Unificación de todas las entidades de una página en un único grafo RDF interconectado por `@id`:

```typescript
import type { Graph } from 'schema-dts';

export function buildPageJsonLd({
  siteUrl,
  pageUrl,
  title,
  description,
  publishedTime,
  modifiedTime,
  authorName
}: {
  siteUrl: string;
  pageUrl: string;
  title: string;
  description: string;
  publishedTime?: string;
  modifiedTime?: string;
  authorName?: string;
}): Graph {
  return {
    '@context': 'https://schema.org',
    '@graph': [
      // 1. Organización Raíz
      {
        '@type': 'Organization',
        '@id': `${siteUrl}/#organization`,
        name: 'Gentle AI',
        url: siteUrl,
        logo: `${siteUrl}/logo.png`,
        sameAs: [
          'https://twitter.com/gentle_ai',
          'https://github.com/gentleman-programming'
        ]
      },
      // 2. Sitio Web Global
      {
        '@type': 'WebSite',
        '@id': `${siteUrl}/#website`,
        url: siteUrl,
        name: 'Gentle AI Ecosystem',
        publisher: { '@id': `${siteUrl}/#organization` }
      },
      // 3. Página Web Específica
      {
        '@type': 'WebPage',
        '@id': `${pageUrl}#webpage`,
        url: pageUrl,
        name: title,
        description: description,
        isPartOf: { '@id': `${siteUrl}/#website` },
        breadcrumb: { '@id': `${pageUrl}#breadcrumb` }
      },
      // 4. Artículo / Contenido Principal (si aplica)
      ...(publishedTime ? [{
        '@type': 'Article' as const,
        '@id': `${pageUrl}#article`,
        isPartOf: { '@id': `${pageUrl}#webpage` },
        headline: title,
        description: description,
        datePublished: publishedTime,
        dateModified: modifiedTime || publishedTime,
        mainEntityOfPage: `${pageUrl}#webpage`,
        publisher: { '@id': `${siteUrl}/#organization` },
        author: {
          '@type': 'Person' as const,
          name: authorName || 'Gentle AI Core Team'
        }
      }] : [])
    ]
  };
}
```

---

## 3. Taxonomía Granular de Bots y Crawlers (2026)

- **Search & Retrieval Bots (Permitidos para citación en IA)**:
  * `OAI-SearchBot`, `ChatGPT-User`, `PerplexityBot`, `Perplexity-User`, `Claude-SearchBot`, `Claude-User`, `Googlebot`, `Bingbot`.
- **Training-Only Bots (Opcional restringir sin perder presencia en respuestas)**:
  * `GPTBot`, `ClaudeBot`, `Google-Extended`, `Applebot-Extended`, `CCBot`, `Bytespider`.

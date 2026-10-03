# Modern SEO, AEO & GEO Developer Reference Manual: Schemas, llms.txt & Knowledge Graphs (v2.0)

> **Documento Normativo SSoT:** Referencia técnica del Pipeline Multi-Superficie 2026: optimización para motores de búsqueda tradicionales (SEO), motores de respuesta directa (AEO - Perplexity, SearchGPT, Gemini), optimización generativa (GEO - `llms.txt` v2), grafos semánticos RDF interconectados (`@graph`) con `schema-dts`, suites visuales completas de Favicon y OpenGraph multi-red (<300KB WhatsApp budget) y metadatos IPTC para imágenes.

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

Unificación de todas las entidades de una página en un único grafo RDF interconectado por `@id`, incluyendo `ImageObject`:

```typescript
import type { Graph } from 'schema-dts';

export function buildPageJsonLd({
  siteUrl,
  pageUrl,
  title,
  description,
  imageUrl,
  imageAlt,
  publishedTime,
  modifiedTime,
  authorName
}: {
  siteUrl: string;
  pageUrl: string;
  title: string;
  description: string;
  imageUrl?: string;
  imageAlt?: string;
  publishedTime?: string;
  modifiedTime?: string;
  authorName?: string;
}): Graph {
  const primaryImageUrl = imageUrl || `${siteUrl}/og-default.jpg`;

  return {
    '@context': 'https://schema.org',
    '@graph': [
      // 1. Organización Raíz
      {
        '@type': 'Organization',
        '@id': `${siteUrl}/#organization`,
        name: title,
        url: siteUrl,
        logo: {
          '@type': 'ImageObject',
          '@id': `${siteUrl}/#logo`,
          contentUrl: `${siteUrl}/logo.png`,
          caption: `${title} Logo`
        }
      },
      // 2. Sitio Web Global
      {
        '@type': 'WebSite',
        '@id': `${siteUrl}/#website`,
        url: siteUrl,
        name: title,
        publisher: { '@id': `${siteUrl}/#organization` }
      },
      // 3. Imagen Primaria / Hero (ImageObject)
      {
        '@type': 'ImageObject',
        '@id': `${pageUrl}#primaryimage`,
        url: primaryImageUrl,
        contentUrl: primaryImageUrl,
        caption: imageAlt || title,
        representativeOfPage: true
      },
      // 4. Página Web Específica
      {
        '@type': 'WebPage',
        '@id': `${pageUrl}#webpage`,
        url: pageUrl,
        name: title,
        description: description,
        isPartOf: { '@id': `${siteUrl}/#website` },
        primaryImageOfPage: { '@id': `${pageUrl}#primaryimage` },
        breadcrumb: { '@id': `${pageUrl}#breadcrumb` }
      },
      // 5. Artículo / Contenido Principal (si aplica)
      ...(publishedTime ? [{
        '@type': 'Article' as const,
        '@id': `${pageUrl}#article`,
        isPartOf: { '@id': `${pageUrl}#webpage` },
        headline: title,
        description: description,
        image: { '@id': `${pageUrl}#primaryimage` },
        datePublished: publishedTime,
        dateModified: modifiedTime || publishedTime,
        mainEntityOfPage: `${pageUrl}#webpage`,
        publisher: { '@id': `${siteUrl}/#organization` },
        author: {
          '@type': 'Person' as const,
          name: authorName || 'Editorial Team'
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

---

## 4. Matriz de Dimensiones Sociales & Umbral WhatsApp (<300KB)

| Superficie / Red | Resolución Óptima | Aspect Ratio | Safe Zone (Centro) | Límite de Peso |
|---|---|---|---|---|
| **Universal OG** (Facebook, LinkedIn, Slack, Discord, Threads) | 1200 × 630 px | 1.91:1 | 1080 × 600 px | **< 300 KB** (WhatsApp safe) |
| **X (Twitter) Large Card** | 1200 × 675 px | 16:9 | 1080 × 580 px | < 5 MB |
| **Feed Cuadrado / WhatsApp Catalog** | 1080 × 1080 px | 1:1 | 960 × 960 px | < 1 MB |
| **Stories / Reels / TikTok** | 1080 × 1920 px | 9:16 | 1080 × 1420 px | < 2 MB |
| **Pinterest Pin** | 1000 × 1500 px | 2:3 | 900 × 1400 px | < 5 MB |

> [!CRITICAL]
> **El Filtro Silencioso de WhatsApp:** WhatsApp Link Preview falla silenciosamente y descarta la imagen si el archivo referenciado en `og:image` supera los **300 KB**. Para el OpenGraph universal (1200×630), se debe aplicar compresión WebP/JPEG optimizada con calidad 82-85% (buffer 180KB–260KB).

---

## 5. Arquitectura de Favicons & PWA App Icons

Toda aplicación web de élite debe inyectar la suite de 5 capas en `<head>`:

```html
<!-- Vectorial escalable con soporte dinámico para tema oscuro/claro -->
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />

<!-- Fallback clásico PNG multi-resolución para navegadores legacy -->
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
<link rel="shortcut icon" href="/favicon.ico" />

<!-- Dispositivos iOS / Apple Touch Icon (Fondo sólido opaco, 180x180 px) -->
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />

<!-- Web App Manifest (PWA) -->
<link rel="manifest" href="/site.webmanifest" />
<meta name="theme-color" content="#050505" />
```

---

## 6. Image SEO: IPTC Photo Metadata vs Mito de Keywords en EXIF

- **Mito de Ranking EXIF:** John Mueller (Google) confirmó oficialmente que Googlebot **no utiliza metadatos EXIF como factor de posicionamiento**. Incrustar listas de palabras clave en EXIF es checklist theater.
- **Lo que SÍ indexa y premia Google Search:**
  1. **IPTC Photo Metadata:**
     - `Creator`: Fotógrafo u Organización creadora.
     - `Credit Line`: Crédito institucional.
     - `Copyright Notice`: Titular de derechos de autor.
     - `Licensor URL` y `Web Statement of Rights`: Habilitan el badge oficial **"Licenciable" (Licensable Badge)** en Google Imágenes.
     - `Digital Source Type`: `trainedAlgorithmicMedia` (requerido para imágenes generadas por IA bajo C2PA v2.1+).
  2. **Computer Vision & OCR Multimodal:** Motores como Google Lens, Perplexity y GPT-4o leen el texto renderizado en la imagen. Exige alto contraste tipográfico (APCA Lc 60+ o WCAG AAA).

---

## 7. Componentes Astro Reusables

La skill incluye dos componentes de referencia listos para importar:
- [`assets/SEO.astro`](file:///var/www/.agents/skills/seo-aeo-geo/assets/SEO.astro): Inyecta metadatos canónicos, OpenGraph con ancho/alto/alt explícitos y Twitter Card.
- [`assets/FaviconSuite.astro`](file:///var/www/.agents/skills/seo-aeo-geo/assets/FaviconSuite.astro): Inyecta de forma limpia y condensada toda la suite de favicons y PWA manifest.

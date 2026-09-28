# Research Reference Manual: Pipeline, Heuristics & Free Quota Preservation (v6.0)

Este manual establece los invariantes epistémicos, heurísticas de decisión y el protocolo de preservación estricta de cuotas gratuitas.

---

## 1. El Pipeline Sinérgico de 7 Fases Epistémicas

```
[FASE 0: Recall Local LTM]
   ➔ Invocación: engram (mem_search) [Costo 0]
   ➔ Objetivo: Recuperar contexto previo, arquitecturas aprobadas y decisiones previas.
         ↓
[FASE 1: Documentación Canónica de Librerías]
   ➔ Invocación: context7 (resolve-library-id + query-docs) [Costo 0]
   ➔ Objetivo: Extraer firmas de funciones y esquemas de tipos directamente de fuentes oficiales.
         ↓
[FASE 2: Triangulación de Búsqueda Web & Fallbacks]
   ➔ Primario Código/Arquitectura: exa (web_search_exa - type="neural")
   ➔ Primario Factual/Changelogs: tavily (tavily_search - search_depth="basic")
   ➔ Primario Web Global/Diseño: brave (brave_web_search - freshness="py")
   ➔ Búsqueda Markdown Directa: jina search (s.jina.ai/<query>)
   ➔ Fallback Ilimitado: duckduckgo (duckduckgo_web_search) [Costo 0]
   ➔ Objetivo: Obtener de 3 a 5 URLs canónicas oficiales sin descargar el texto completo.
         ↓
[FASE 3: Extracción Verbatim Universal con Headers]
   ➔ Invocación: Jina Reader -> read_url_content("https://r.jina.ai/<url>")
   ➔ Headers: X-Target-Selector, X-Remove-Selector, X-With-Generated-Alt, X-Respond-With: readerlm-v2
   ➔ Fallback Estático: Native HTTP -> read_url_content(Url) [Costo 0]
   ➔ Objetivo: Lectura íntegra del documento en Markdown limpio ("Snippet is Not Evidence").
         ↓
[FASE 4: Infiltración Local, SPAs & Scrapers Estructurados]
   ➔ Invocación Local: crawl4ai (AsyncWebCrawler + fit_markdown + JsonCss) [Costo 0]
   ➔ Invocación Headless: playwright / puppeteer (Route Abort de imágenes/medios) [Costo 0]
   ➔ Invocación Cloud: firecrawl (firecrawl_scrape / map - Último recurso si hay anti-bot)
   ➔ Objetivo: Parsear aplicaciones interactivas, generar PDFs vectoriales o capturas Retina 2x.
         ↓
[FASE 5: Síntesis Epistémica & Citación Canónica]
   ➔ Invariantes: "Snippet is Not Evidence" + Anclaje Temporal (date -u) + Estabilidad LTS/GA.
   ➔ Objetivo: Estructurar hechos técnicos demostrables con citas canónicas exactas.
         ↓
[FASE 6: Persistencia LTM & Cierre RDD]
   ➔ Invocación: engram (mem_save con category, tags y rationale)
   ➔ Objetivo: Sellar el aprendizaje en la memoria permanente para sesiones futuras.
```

---

## 2. Invariantes Epistémicas Fundacionales

### 🔹 A. "SNIPPET IS NOT EVIDENCE" (Profundidad Obligatoria)
- **Regla Inviolable:** Un snippet devuelto por un buscador es únicamente un puntero de descubrimiento, nunca un hecho técnico.
- **Acción Obligatoria:** Toda URL canónica identificada DEBE ser leída completamente mediante **Jina Reader** (`https://r.jina.ai/<url>`), **Native HTTP** o **Crawl4AI** antes de incluir conclusiones en planes o código.

### 🔹 B. Dynamic Temporal Anchoring (Anclaje Temporal Dinámico)
- El conocimiento pre-entrenado sufre de sesgos temporales.
- Toda búsqueda debe anclarse al estado o versión activa (`date -u`):
  * ✅ *Correcto:* `"Next.js 15 App Router server actions stable current LTS"`
  * ❌ *Incorrecto:* `"Next.js server actions"`

### 🔹 C. Clasificación de Estabilidad: Latest Stable vs Pre-Release
- **Por Defecto:** Seleccionar versiones GA (General Availability) o LTS (Long Term Support).
- **Pre-Releases:** Si se investigan versiones `-rc`, `-beta` o `-canary`, se deben documentar explícitamente sus breaking changes y requerir confirmación humana antes de adoptarlas.

---

## 3. Heurísticas de Preservación de Cuotas Gratuitas (Costo Cero)

Para garantizar un funcionamiento continuo sin incurrir en costes de API:

1. **Memoria Local Primero (Tier 0):** Consultar siempre `engram` (`mem_search`). Si la decisión ya existe en memoria, el costo es 0 ms y 0 peticiones de red.
2. **Docs de Librerías con Context7 (Tier 1):** Usar `context7` para paquetes NPM/PyPI. Costo = 0 créditos de búsqueda web.
3. **Descubrimiento Ligero (Tier 2):**
   - En **Exa**, usar `numResults=5` y `type="neural"`. Priorizar la lectura de URLs con Jina Reader o Crawl4AI para preservar créditos de fetch.
   - En **Tavily**, enfocar siempre `search_depth="basic"` para descubrimiento inicial de fuentes canónicas.
   - En **Brave**, respetar el rate-limit de 1 req/segundo.
   - Si se detecta agotamiento de cuota o error 429, conmutar inmediatamente a **DuckDuckGo** (`duckduckgo_web_search`).
4. **Extracción Verbatim con Jina Reader (Tier 3):** Aprovechar la cuota de 1M tokens/minuto de Jina Reader usando `X-Target-Selector` para extraer únicamente el cuerpo principal (`article`, `main`), reduciendo el tamaño del payload.
5. **Scraping Pesado Local con Crawl4AI / Playwright (Tier 4):**
   - Ejecutar `crawl4ai` localmente con `CacheMode.ENABLED` y `fit_markdown`.
   - Ejecutar `playwright` abortando peticiones a `image`, `stylesheet`, `font`, `media` para scraping en menos de 150 ms con cero consumo de ancho de banda.
   - Usar `firecrawl` exclusivamente como último recurso si el sitio objetivo bloquea activamente navegadores locales.

---

## 4. Decision Matrix por Naturaleza del Objetivo

| Naturaleza de la Consulta | Fase 0/1: Base | Fase 2: Búsqueda | Fase 3: Lectura | Fase 4: Scraper Avanzado |
|---|---|---|---|---|
| **Librería NPM / PyPI** | `engram` ➔ `context7` | — | `context7` / **Jina Reader** | — |
| **Repositorio / OpenAPI** | `engram` | `exa` (`category: "github"`) | **Jina Reader** (`r.jina.ai`) | **Crawl4AI** (`fit_markdown`) |
| **Changelogs & Versiones** | `engram` | `tavily` (`search_depth: "basic"`) | **Jina Reader** (`r.jina.ai`) | **Crawl4AI** |
| **Branding & Tipografía** | `engram` | `brave` / `exa` | **Jina Reader** | **Playwright** / **Puppeteer** |
| **Fallback de Búsqueda** | `engram` | **DuckDuckGo** / **Jina Search** | **Jina Reader** / Native HTTP | **Crawl4AI** |
| **SPA Compleja / Anti-bot** | `engram` | `brave` / `tavily_map` | **Crawl4AI** / **Playwright** | **Firecrawl** (`/v1/scrape`) |

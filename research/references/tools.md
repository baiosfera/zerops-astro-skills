# Research Reference Manual: Multi-Tier Epistemic & Crawler Tools Specification (v6.0)

Este manual define la especificación técnica exhaustiva de los **12 motores y herramientas** del ecosistema epistémico de Gentle AI.

---

## 1. Tier 0: Memoria Semántica a Largo Plazo (LTM)

### 🔹 Engram (`ServerName: "engram"` / CLI `/var/www/.bin/engram`)
- **Naturaleza:** Base de datos local SQLite con extensiones FTS5 y embeddings vectoriales.
- **Cuota:** **Ilimitada (100% Local / Costo 0).**
- **Funciones Principales:**
  - `mem_search(query: str)`: Búsqueda híbrida (FTS5 + Vectorial) para recuperar decisiones arquitectónicas, dependencias y lecciones previas.
  - `mem_get_observation(id: int)`: Recuperación del texto íntegro de una memoria específica.
  - `mem_save(category: str, tags: str, content: str)`: Persistencia inmutable de hitos tras verificar una ejecución.
- **Regla Operativa:** Ejecutar siempre en **Fase 0** antes de cualquier llamada de red.

---

## 2. Tier 1: Documentación Oficial de Librerías y Paquetes

### 🔹 Context7 Docs (`ServerName: "context7"`)
- **Naturaleza:** Motor REST especializado en documentación canónica versionada de ecosistemas (NPM, PyPI, Crates, Go).
- **Cuota:** **Ilimitada (Costo 0).**
- **Herramientas:**
  - `resolve-library-id(query: str)`: Resuelve nombres populares a IDs canónicos (ej. `"tailwind"` ➔ `"/tailwindlabs/tailwindcss"`).
  - `query-docs(libraryId: str, query: str)`: Consulta la documentación oficial para obtener firmas de funciones, esquemas de tipos y métodos vigentes.
- **Regla Operativa:** Primera parada obligatoria en **Fase 1** para código, librerías y frameworks.

---

## 3. Tier 2: Motores de Búsqueda Web & Descubrimiento

### 🔹 A. Exa Search (`ServerName: "exa"`)
- **Naturaleza:** Motor neural semántico optimizado para código, repositorios GitHub y arquitecturas técnicas.
- **Cuota:** 1.000 peticiones / mes.
- **Herramientas & Parámetros:**
  - `web_search_exa(query: str, numResults?: number)`: Búsqueda basada en descripciones ricas de la página ideal. Admite prefijos inline como `category:company` o `category:people`. Por defecto retorna 10 resultados con highlights limpios.
  - `web_fetch_exa(urls: list[str], maxCharacters?: number)`: Extracción de páginas indexadas en Markdown. **Parámetro CoHaLo:** fijar `maxCharacters: 2000-3000` para acotar el consumo de tokens en contexto.
- **Regla de Ahorro:** Usar `web_search_exa` para obtener URLs y highlights. Usar `web_fetch_exa` con `maxCharacters` acotado o delegar a Jina Reader (`r.jina.ai`) para lectura gratuita.

### 🔹 B. Tavily Search (`ServerName: "tavily"`)
- **Naturaleza:** Motor de precisión factual optimizado para fechas de lanzamiento, changelogs, breaking changes y CVEs.
- **Cuota:** 1.000 peticiones / mes.
- **Herramientas & Parámetros:**
  - `tavily_search(query: str, search_depth?: str, max_results?: number, include_raw_content?: bool, ...)`:
    * `search_depth`: `"basic"`, `"advanced"`, `"fast"`, `"ultra-fast"`. **Usar siempre "basic" o "fast" para descubrimiento.**
    * `max_results`: Entre 5 y 20 (mínimo contractual: 5).
    * `include_raw_content`: **Obligatoriamente `false`** para erradicar vertidos de HTML crudo que saturan tokens.
    * `include_images`: `false` por defecto en workflows de código.
  - `tavily_extract(urls: list[str], extract_depth?: "basic"|"advanced", format?: "markdown"|"text", query?: str)`: Extrae contenido estructurado con reordenamiento semántico por `query`.
  - `tavily_map(url: str, limit?: int, max_depth?: int)`: Mapeo de sitemap sin descargar cuerpos de página.
- **Regla de Ahorro:** Usar `search_depth="basic"` con `max_results=5` y `include_raw_content=false`.

### 🔹 C. Brave Search (`ServerName: "brave"`)
- **Naturaleza:** Índice web global independiente con más de 30 mil millones de páginas.
- **Cuota:** 2.000 consultas / mes. **Rate limit: 1 petición / segundo.**
- **Herramientas & Parámetros:**
  - `brave_web_search(query: str, count?: number, offset?: number)`: Retorna `count` (1-20, default 10) resultados con títulos, descripciones y URLs.
  - `brave_local_search(query: str)`: Búsqueda geolocalizada.
- **Regla de Control:** Aplicar pausas de al menos 1.1s entre llamadas consecutivas para prevenir errores HTTP 429.

### 🔹 D. Jina Search (`s.jina.ai`)
- **Naturaleza:** Motor de búsqueda web que devuelve directamente Markdown limpio optimizado para LLMs sin snippets.
- **Cuota:** Capa gratuita de 1.000.000 tokens / minuto.
- **Invocación:** `read_url_content("https://s.jina.ai/<query_url_encoded>")`.

### 🔹 E. DuckDuckGo Search (`ServerName: "duckduckgo"`)
- **Naturaleza:** Motor de búsqueda sin autenticación.
- **Cuota:** **Ilimitada (Costo 0).**
- **Herramienta:** `duckduckgo_web_search(query: str, count?: number, safeSearch?: str)`.
- **Gotcha Empírico & Circuit Breaker (Crítico):** Los nodos en centros de datos o IPs de nube pueden disparar anomalías en DDG (`Error: DDG detected an anomaly in the request, you are likely making requests too quickly`). **Regla de Arnés:** El llamador debe atrapar esta excepción y alternar inmediatamente a Jina Reader o Native HTTP sin reintentos ciegos en bucle.

---

## 4. Tier 3: Extracción Verbatim Universal

### 🔹 Jina Reader Protocol (`r.jina.ai`)
- **Naturaleza:** Conversor universal de HTML / JS a Markdown limpio con soporte para VLM y modelos de lectura.
- **Cuota:** 1.000.000 tokens gratuitos.
- **Invocación:** `read_url_content("https://r.jina.ai/<url>")`
- **Headers HTTP de Control de Precisión:**
  * `X-Target-Selector`: Selector CSS para extraer únicamente el contenido objetivo (`article, .main-content, #docs`).
  * `X-Remove-Selector`: Selector CSS para eliminar ruido (`nav, footer, .sidebar, #ads, header`).
  * `X-Wait-For-Selector`: Selector CSS para esperar a que elementos dinámicos aparezcan antes de extraer.
  * `X-Retain-Images`: `"none"` (ahorro de tokens) o `"all"`.
  * `X-With-Generated-Alt`: `true` (genera captions descriptivos de imágenes mediante modelos de visión).
  * `X-With-Links-Summary`: `true` (resumen de enlaces al final del documento).
  * `X-Respond-With`: `"readerlm-v2"`, `"frontmatter"`, `"markdown"`.
  * `X-Token-Budget`: Límite máximo de tokens por petición.

### 🔹 Native HTTP Reader
- **Naturaleza:** Petición HTTP nativa mediante `read_url_content(Url)`.
- **Cuota:** **Ilimitada (Costo 0).**
- **Uso:** Lectura directa de archivos crudos en GitHub (`raw.githubusercontent.com`), sitemaps, JSONs y páginas estáticas simples.

---

## 5. Tier 4: Scrapers Locales de Alta Velocidad, SPAs & Automatización

### 🔹 A. Crawl4AI (`.agents/skills/crawl4ai/`)
- **Naturaleza:** Motor asíncrono en Python de alto rendimiento para crawling, poda inteligente y extracción estructurada.
- **Cuota:** **100% Local / Costo 0.**
- **Módulos y Configuración Clave:**
  ```python
  from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
  from crawl4ai.content_filter_strategy import PruningContentFilter
  from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
  from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

  browser_cfg = BrowserConfig(browser_type="chromium", headless=True, text_mode=True)
  
  # Poda inteligente y extracción fit_markdown
  md_generator = DefaultMarkdownGenerator(content_filter=PruningContentFilter(threshold=0.48))
  run_cfg = CrawlerRunConfig(
      cache_mode=CacheMode.ENABLED,
      markdown_generator=md_generator,
      word_count_threshold=15,
      excluded_tags=["nav", "footer", "header", "aside"],
      exclude_external_links=True
  )
  ```
- **Salida:** `result.markdown.fit_markdown` (contenido denso sin elementos superfluos).

### 🔹 B. Playwright (`.agents/skills/playwright/`)
- **Naturaleza:** Automatización multi-navegador (Chromium, Firefox, WebKit) para testing E2E y scraping interactivo.
- **Cuota:** **100% Local / Costo 0.**
- **Patrón de Route Interception para Scraping en < 150 ms:**
  ```python
  async def intercept_route(route):
      if route.request.resource_type in ["image", "stylesheet", "font", "media"]:
          await route.abort()
      else:
          await route.continue_()
  
  page.route("**/*", intercept_route)
  await page.goto("https://target-spa.com")
  ```

### 🔹 C. Puppeteer (`.agents/skills/puppeteer/`)
- **Naturaleza:** Automatización de Chrome DevTools Protocol en Node.js.
- **Cuota:** **100% Local / Costo 0.**
- **Casos de Uso Óptimos:** Generación de PDFs vectoriales (`page.pdf()`), capturas Full-Page Retina $2\times$ y evaluación directa de JavaScript en el DOM.

### 🔹 D. Firecrawl (`ServerName: "firecrawl"`)
- **Naturaleza:** Plataforma cloud integral de extracción, crawling y búsqueda para agentes autónomos.
- **Capacidades Operativas SOTA (26 Operaciones MCP):**
  - `firecrawl_developer_search(query: str, k?: int, skills?: "only")`: Búsqueda de alta especialización en repositorios públicos, GitHub issues, pull requests fusionados, READMEs y documentación. El parámetro `skills="only"` restringe la búsqueda exclusivamente a archivos de habilidades de agentes y guías de prompts.
  - `firecrawl_search(query: str, categories?: ["developer"|"research"|"pdf"], limit?: int, highlights?: bool)`: Búsqueda web filtrada por fuentes de desarrollo o académicas con excerpts limpios.
  - `firecrawl_scrape(url: str, formats?: ["markdown"|"json"])`: Extracción individual de páginas con renderizado dinámico de JavaScript y conversión directa a Markdown o JSON estructurado.
  - `firecrawl_map(url: str)`: Mapeo y enumeración instantánea de rutas y jerarquía de un sitio sin descargar el cuerpo completo.
  - `firecrawl_crawl(url: str)`: Crawling recursivo estructurado de múltiples páginas bajo un dominio.
  - `firecrawl_interact(url: str, actions: list)`: Navegación dinámica en vivo (clics, inputs, scrolls y ejecución de scripts en SPAs complejas).
  - `firecrawl_research_*(query: str)`: Consulta y lectura de papers científicos y literatura técnica (arXiv, PubMed).
- **Orquestación Compuesta:** Se articula sinérgicamente en el pipeline multi-motor junto a Exa, Brave y Jina Reader para mapear y extraer sin recorte de snippets.



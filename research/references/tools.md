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
  - `web_search_exa(query: str, numResults: int, ...)`: Búsqueda basada en descripciones ricas de la página ideal.
    * `type`: `"neural"` (conceptos) o `"keyword"` (términos exactos).
    * `category`: `"github"`, `"research paper"`, `"company"`, `"news"`.
    * `includeDomains` / `excludeDomains`: Lista de dominios para acotar la búsqueda.
    * `startPublishedDate`: Filtro ISO para anclaje temporal (`YYYY-MM-DD`).
  - `web_fetch_exa(urls: list[str])`: Extracción directa de páginas indexadas.
- **Regla de Ahorro:** Usar `web_search_exa` solo para obtener URLs canónicas. No llamar a `web_fetch_exa` si Jina Reader o Crawl4AI pueden leer la URL gratuitamente.

### 🔹 B. Tavily Search (`ServerName: "tavily"`)
- **Naturaleza:** Motor de precisión factual optimizado para fechas de lanzamiento, changelogs, breaking changes y CVEs.
- **Cuota:** 1.000 peticiones / mes.
- **Herramientas & Parámetros:**
  - `tavily_search(query: str, search_depth: str, max_results: int, ...)`:
    * `search_depth`: `"basic"` (1 crédito) o `"advanced"` (2 créditos). **Usar siempre "basic" para descubrimiento.**
    * `include_domains`: Dominios a incluir.
    * `time_range`: `"day"`, `"week"`, `"month"`, `"year"`.
  - `tavily_map(url: str)`: Mapeo ligero de rutas de un dominio sin descargar el contenido.
  - `tavily_extract(urls: list[str])`: Extracción de contenido estructurado.
- **Regla de Ahorro:** Usar `search_depth="basic"` con `max_results=5` para no saturar créditos.

### 🔹 C. Brave Search (`ServerName: "brave"`)
- **Naturaleza:** Índice web global independiente con más de 30 mil millones de páginas.
- **Cuota:** 2.000 consultas / mes. **Rate limit: 1 petición / segundo.**
- **Herramientas & Parámetros:**
  - `brave_web_search(query: str)`: Búsqueda web general para benchmarking de marcas, estudios de diseño y documentación.
  - `brave_local_search(query: str)`: Búsqueda geolocalizada.
- **Regla de Control:** Aplicar pausas de al menos 1.1s entre llamadas consecutivas para evitar HTTP 429.

### 🔹 D. Jina Search (`s.jina.ai`)
- **Naturaleza:** Motor de búsqueda web que devuelve directamente Markdown limpio optimizado para LLMs sin snippets.
- **Cuota:** Capa gratuita de 1.000.000 tokens / minuto.
- **Invocación:** `read_url_content("https://s.jina.ai/<query_url_encoded>")`.

### 🔹 E. DuckDuckGo Search (`ServerName: "duckduckgo"`)
- **Naturaleza:** Motor de búsqueda sin autenticación ni límites estrictos de cuota mensual.
- **Cuota:** **Ilimitada (Costo 0).**
- **Herramienta:** `duckduckgo_web_search(query: str)`.
- **Regla Operativa:** Fallback automático e inmediato si Exa, Tavily o Brave alcanzan rate limits o agotan cuota.

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
- **Naturaleza:** API de scraping y crawling cloud con renderizado de SPAs y bypass de protecciones avanzadas.
- **Cuota:** 500 créditos / mes.
- **Herramientas:**
  - `firecrawl_map(url)`: Mapeo de sitemap (1 crédito).
  - `firecrawl_scrape(url)`: Scraping individual con JS rendering.
  - `firecrawl_crawl(url)`: Crawling recursivo.
  - `firecrawl_extract(urls, schema)`: Extracción estructurada JSON.
- **Regla de Ahorro:** Usar exclusivamente como **último recurso** si Crawl4AI, Playwright o Jina Reader son bloqueados por protecciones Cloudflare/anti-bot severas.


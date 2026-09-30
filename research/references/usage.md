# Research Reference Manual: Comprehensive 12-Engine Usage & Workflows (v7.2)

This manual provides the exhaustive operational guide for the **12 epistemic engines** of the Gentle AI ecosystem. It covers both **Inline Compound Grounding** and **Deep Research Dossiers**, local headless scraping, and cloud crawling.

---

## 1. Grounding Architectures & Modalities

### Modality A: Inline Compound Grounding (Turn-Level Inflow)
Used directly within conversation turns during planning, auditing, coding, or technology comparison:
1. **Recall LTM First (Tier 0):** Run `mem_search(query)` in Engram to retrieve internal decisions, prior benchmarks, and project gotchas.
2. **Package/API Verification (Tier 1):** For package schemas, type signatures, or breaking changes in NPM/PyPI/Crates, query Context7 (`resolve-library-id` followed by `query-docs`).
3. **Compound Search (Tier 2):**
   - For code, GitHub repos, or architectural benchmarks: `web_search_exa(query: "...", numResults: 3)`.
   - For agent patterns, prompt engineering, or skill design: `firecrawl_developer_search(query: "...", k: 3, skills="only")`.
   - For factual release dates, changelogs, CVEs: `tavily_search(query: "...", search_depth="basic", max_results=5, include_raw_content=false)`.
   - For broad independent index and news: `brave_web_search(query: "...", count=3)`.
   - For unmetered fallback: `duckduckgo_web_search(query: "...")` with circuit breaker for anomaly blocks.
4. **Verbatim Primary Source Grounding (Tier 3):** Read the actual raw documentation via Jina Reader (`read_url_content("https://r.jina.ai/<url>")`) or `web_fetch_exa(urls=["<url>"], maxCharacters=3000)`.
5. **Synthesis:** Deliver findings citing canonical URLs directly without gating behind cumbersome XML boilerplate.

### Modality B: Deep Research Dossier (Subagent Delegation)
Mandatory when analyzing large external codebases, synthesizing 10+ sources, or producing formal architecture dossiers:
1. Launch subagent via `invoke_subagent` (`TypeName: "research"`, `Role: "Codebase Researcher"`).
2. Inject [`assets/subagent_prompt_contract.md`](file:///var/www/.agents/skills/research/assets/subagent_prompt_contract.md).
3. The subagent executes the 7-phase cascade and writes the dossier to `/var/www/artifacts/<target>_research_report.md`.
4. The parent agent ingests the executive summary and links the report.

---

## 2. Exhaustive 12-Engine Catalog & Tool Recipes

### 🔹 Tier 0: Semantic Long-Term Memory (LTM)
#### 1. Engram (`ServerName: "engram"`)
- **Nature:** Local SQLite vector + FTS5 memory database. Cost: $0.
- **Tools:**
  - `mem_search(query: str, project?: str)`: Hybrid search. Use clean alphanumeric terms.
  - `mem_get_observation(id: int)`: Retrieve full observation text.
  - `mem_save(title: str, content: str, topic_key?: str, type?: str)`: Persist milestone.
- **Workflow:** Always query Engram before any external network requests.

---

### 🔹 Tier 1: Canonical Ecosystem Documentation
#### 2. Context7 (`ServerName: "context7"`)
- **Nature:** Versioned documentation resolver for NPM, PyPI, Crates, Go. Cost: $0.
- **Tools:**
  - `resolve-library-id(query: str)`: Resolves package names to canonical IDs (e.g. `"fastapi"` $\to$ `"/tiangolo/fastapi"`).
  - `query-docs(libraryId: str, query: str)`: Fetches precise type signatures and official guide sections.
- **Recipe:**
  ```json
  {"ServerName": "context7", "ToolName": "query-docs", "Arguments": {"libraryId": "/tailwindlabs/tailwindcss", "query": "v4 theme configuration"}}
  ```

---

### 🔹 Tier 2: Live Web Search & Discovery
#### 3. Exa Search (`ServerName: "exa"`)
- **Nature:** Neural embeddings search engine optimized for code, GitHub repos, and research papers.
- **Tools:**
  - `web_search_exa(query: str, numResults?: int)`: Discover canonical URLs and clean semantic highlights.
  - `web_fetch_exa(urls: list[str], maxCharacters?: int)`: Direct page fetch with token control (`maxCharacters: 2000-3000`).
- **Recipe:**
  ```json
  {"ServerName": "exa", "ToolName": "web_search_exa", "Arguments": {"query": "Astro 5 server islands directus SDK integration", "numResults": 3}}
  ```

#### 4. Tavily Search (`ServerName: "tavily"`)
- **Nature:** Factual real-time web search engine optimized for release notes, CVEs, and breaking changes.
- **Tools:**
  - `tavily_search(query: str, search_depth: "basic" | "advanced", max_results: int, time_range?: "day" | "week" | "month" | "year")`.
  - `tavily_map(url: str)`: Lightweight site tree mapping without content download.
  - `tavily_extract(urls: list[str])`: Extract structured data.
- **Recipe:**
  ```json
  {"ServerName": "tavily", "ToolName": "tavily_search", "Arguments": {"query": "Bun 1.3 changelog breaking changes", "search_depth": "basic", "max_results": 3}}
  ```

#### 5. Brave Search (`ServerName: "brave"`)
- **Nature:** Independent global index with 30B+ pages.
- **Tools:**
  - `brave_web_search(query: str)`: Broad web search.
  - `brave_local_search(query: str)`: Localized POI queries.
- **Rate Limit Policy:** Enforce >= 1.1s pauses between calls to honor the 1 req/s rate limit.

#### 6. Jina Search (`s.jina.ai`)
- **Nature:** Returns clean markdown search results directly from web queries.
- **Tool:** `read_url_content(Url: "https://s.jina.ai/<query_url_encoded>")`.

#### 7. DuckDuckGo Search (`ServerName: "duckduckgo"`)
- **Nature:** Zero-cost fallback search engine without rate limit quotas.
- **Tool:** `duckduckgo_web_search(query: str)`. Use whenever Exa, Tavily, or Brave hit quota limits.

---

### 🔹 Tier 3: Verbatim Content Extraction
#### 8. Jina Reader (`r.jina.ai`)
- **Nature:** Universal HTML/JS-to-Markdown streaming proxy.
- **Tool:** `read_url_content(Url: "https://r.jina.ai/<canonical_url>")`.
- **Target Filtering:** Prefix selector to extract dense text: `https://r.jina.ai/https://example.com/docs`.

#### 9. Native HTTP Reader
- **Tool:** `read_url_content(Url: "<url>")`.
- **Usage:** Ideal for raw GitHub URLs (`raw.githubusercontent.com`), JSON configs, and sitemaps.

---

### 🔹 Tier 4: Scrapers, Headless Browsers & Cloud Crawling
#### 10. Crawl4AI (Local Python Async Crawler)
- **Nature:** High-throughput async crawler with heuristic markdown pruning (`fit_markdown`). Cost: $0.
- **Code Template:**
  ```python
  import asyncio
  from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
  from crawl4ai.content_filter_strategy import PruningContentFilter
  from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

  async def crawl_site(url: str):
      browser_cfg = BrowserConfig(browser_type="chromium", headless=True, text_mode=True)
      md_gen = DefaultMarkdownGenerator(content_filter=PruningContentFilter(threshold=0.48))
      run_cfg = CrawlerRunConfig(
          cache_mode=CacheMode.ENABLED,
          markdown_generator=md_gen,
          word_count_threshold=15,
          excluded_tags=["nav", "footer", "header", "aside"]
      )
      async with AsyncWebCrawler(config=browser_cfg) as crawler:
          result = await crawler.arun(url=url, config=run_cfg)
          return result.markdown.fit_markdown
  ```

#### 11. Playwright / Puppeteer (Local Browser Interception)
- **Nature:** Headless Chromium automation with route interception for ultra-fast scraping (<150ms). Cost: $0.
- **Route Interception Pattern:**
  ```python
  async def intercept_route(route):
      if route.request.resource_type in ["image", "stylesheet", "font", "media"]:
          await route.abort()
      else:
          await route.continue_()

  page.route("**/*", intercept_route)
  await page.goto("https://target-spa.com")
  content = await page.content()
  ```

#### 12. Firecrawl (`ServerName: "firecrawl"`)
- **Nature:** Cloud crawling API with anti-bot bypass and structured extraction across 27 MCP tools.
- **Core Tools:**
  - `firecrawl_developer_search(query: str, k?: int, skills?: "only")`: Specialized index over public repos, GitHub PRs, issues, READMEs, and agent skills.
  - `firecrawl_scrape(url: str, formats: ["markdown", "html"])`: Single-page scrape with JS rendering.
  - `firecrawl_crawl(url: str, limit: int, scrapeOptions?: dict)`: Recursive domain crawl.
  - `firecrawl_map(url: str)`: Fast sitemap mapping (1 credit).
  - `firecrawl_extract(urls: list[str], prompt: str, schema: dict)`: Structured extraction via LLM.
- **Policy:** Cloud fallback when local Crawl4AI or Playwright are blocked by severe Cloudflare/WAF challenges.

#### 13. Zerops Browser (`ServerName: "zerops"`)
- **Nature:** Platform-managed headless browser container (`zerops_browser`).
- **Tool:** `zerops_browser(url: str, action: "screenshot" | "html" | "text")`.
- **Usage:** Ideal for inspecting live internal Zerops subdomains and service previews.

---

## 3. Decision Matrix: Routing by Task Nature

| Task Nature | Primary Discovery | Verbatim Inflow | Scraper / Advanced |
|---|---|---|---|
| **Ecosystem & Types** | `context7` (`resolve-library-id` + `query-docs`) | `context7` · Jina Reader | Native HTTP |
| **Agent Skills & Prompt Guides** | `firecrawl_developer_search` (`skills="only"`) | Jina Reader (`r.jina.ai`) | Exa AI (`web_fetch_exa`) |
| **GitHub & Architecture** | `web_search_exa` (code/concepts) | Jina Reader (`r.jina.ai`) | Crawl4AI (`fit_markdown`) |
| **Changelogs & Breaking Changes** | `tavily_search` (basic) | Jina Reader | Native HTTP |
| **Brand & Design Research** | `brave_web_search` · Exa | Jina Reader | Playwright / Puppeteer |
| **Deep Domain Crawling** | `tavily_map` · Firecrawl Map | Jina Reader | Firecrawl Crawl / Crawl4AI |
| **Anti-Bot Protected SPAs** | Firecrawl Scrape | Firecrawl Extract | Zerops Browser |
| **Zero-Quota Fallback** | `duckduckgo_web_search` (with anomaly catch) | Native HTTP | Crawl4AI |

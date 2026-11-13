# Research Reference Manual: Tools & Parameters Specification (v9.0)

Technical specification of tools exposed across the 7-phase epistemic stack in Antigravity CLI (`agy`).

---

## Tier 0 — Local Memory (`engram`)
- `mem_search(query: str, project?: str)`: Hybrid FTS5 + semantic recall. Execute before network calls.
- `mem_context(project?: str)`: Recent session history.
- `mem_get_observation(id: int)`: Retrieve full untruncated observation.
- `mem_save(title: str, type: str, content: str, topic_key?: str)`: Persist verified discoveries and URLs.

## Tier 1 — Canonical Package Docs (`context7`)
- `resolve-library-id(query: str, libraryName: str)`: Resolve package slug to canonical Context7 ID (e.g. `"/withastro/astro"`).
- `query-docs(libraryId: str, query: str)`: Fetch exact signatures, configuration fields, and breaking-change guides.

## Tier 2 — Web Discovery Primaries & Fallbacks

### Primary A: Exa (`exa`, remote `https://mcp.exa.ai/mcp`)
- `web_search_exa(query: str, numResults?: int)`: Neural embeddings index strong on GitHub repos, technical docs, and code examples (`numResults: 5`).
- `web_fetch_exa(urls: list[str], maxCharacters?: int)`: Clean markdown extraction (`maxCharacters: 3000`).
- `agent_run`: Multi-step Exa research helper when deep synthesis is explicitly required.

### Primary B: Tavily (`tavily`, remote `https://mcp.tavily.com/mcp/`)
- `tavily_search(query: str, search_depth?: "basic"|"advanced"|"fast"|"ultra-fast", max_results?: int, include_raw_content?: bool, time_range?: "day"|"week"|"month"|"year")`: Fresh releases, changelogs, CVEs. Keep `search_depth="basic"` and `include_raw_content=false`.
- `tavily_extract(urls: list[str], extract_depth?: "basic"|"advanced", format?: "markdown"|"text", query?: str)`: Structured page extraction.
- `tavily_map(url: str)` / `tavily_crawl` / `tavily_research`: Site mapping and deep topic reports.

### Primary C & Tier 3 Core: Jina AI (`jina`, remote `https://mcp.jina.ai/v1`)
- `read_url(url: str, question?: str)`: Core Jina Reader MCP converting web pages or PDFs to clean markdown (`question` extracts targeted passages).
- `search_web(query: str)`: Clean search results via Jina Reader API.
- `search_arxiv(query: str)`: Academic preprints and technical papers on arXiv.
- `extract_pdf(url: str)`: Extract figures, tables, and equations from PDFs.
- `guess_datetime_url(url: str)`: Publication / last-updated timestamp detection for Temporal Anchoring.
- `capture_screenshot_url(url: str)`: Visual screenshot verification via Reader API.
- **Direct Jina HTTP Headers (`curl` via `run_command`):**
  * `https://r.jina.ai/<url>` with `X-Target-Selector`, `X-Remove-Selector`, `X-Wait-For-Selector`, `X-Retain-Images: none`, `X-Respond-With: readerlm-v2`, `X-Token-Budget`.
  * `https://s.jina.ai/<url_encoded_query>` as unmetered markdown search backup.

### Primary D & Tier 4 Cloud: Firecrawl (`firecrawl`, remote `https://mcp.firecrawl.dev/v2/mcp`)
- `firecrawl_developer_search(query: str, k?: int, skills?: "only")`: Search repos, PRs, issues, READMEs, and agent skills.
- `firecrawl_search(query: str, categories?: list, limit?: int)`: Web/research/PDF discovery.
- `firecrawl_scrape(url: str, formats?: list)`: JS-rendered SPA and anti-bot extraction.
- `firecrawl_map(url: str)` / `firecrawl_crawl(url: str)`: Domain URL hierarchy and multi-page crawls.
- `firecrawl_interact(...)`: Live browser clicks, inputs, and dynamic state execution.
- `firecrawl_research_*`: Scientific literature search and reading.

### Fallback 1: Brave Search (`brave`, `npx -y @brave/brave-search-mcp-server`)
- `brave_web_search(query: str, count?: int, freshness?: "pd"|"pw"|"pm"|"py")`: Independent 30B+ page fallback index when primary APIs error, rate-limit, or deplete quota. Honor `1 req/s`.
- `brave_local_search(query: str)`: Localized place/business search (Pro plan).

### Fallback 2: DuckDuckGo (`duckduckgo`, `npx -y duckduckgo-mcp-server`)
- `duckduckgo_web_search(query: str)`: Zero-key unlimited search fallback. Catch anomaly errors cleanly and pivot to `jina:search_web` or `s.jina.ai`.

## Tier 4 — Local & Platform Headless Scrapers
- **Native `curl` (`run_command`):** Direct HTTP fetch for `raw.githubusercontent.com`, JSON configs, and sitemaps (`timeout 10s`).
- **Crawl4AI (`python3 -B`):** Local async Chromium crawler (`PruningContentFilter` + `fit_markdown`) when cloud credits must stay zero.
- **Playwright / Puppeteer:** Local headless browser with route interception (`image`/`font`/`media` aborted) for <150ms DOM scraping.
- **Zerops Browser (`zerops_browser`):** Platform-managed browser for live Zerops service previews.

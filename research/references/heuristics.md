# Research Reference Manual: Epistemic Phases & Anti-AMN Heuristics (v9.0)

Decision heuristics enforcing `"Snippet is Not Evidence"`, Temporal Anchoring, and zero wasted API credits.

---

## 1. The 7-Phase Epistemic Pipeline (F0–F6)

```text
[F0: Local Memory Recall]       engram (mem_search / mem_context)                       [$0]
   │
   ▼ (Need live verification or missing in LTM)
[F1: Canonical Library Docs]    context7 (resolve-library-id -> query-docs)             [$0]
   │
   ▼ (Need benchmarks, changelogs, external specs, or repos)
[F2: Discovery + Fallbacks]     Primaries: exa | tavily | jina:search_web | firecrawl_developer_search
                                Fallback 1 (error/429/empty): brave (1.1s pause)
                                Fallback 2 (last-resort):     duckduckgo -> s.jina.ai
   │
   ▼ (3–5 canonical primary URLs found)
[F3: Verbatim Reading]          JINA IMPRESCINDIBLE: jina:read_url | jina:extract_pdf | curl r.jina.ai
                                Complementary: web_fetch_exa (maxCharacters: 3000) | tavily_extract | raw curl
   │
   ▼ (JS-heavy SPA, dynamic DOM, or Cloudflare/WAF gate)
[F4: Deep Crawling & SPAs]      firecrawl (scrape/map/crawl/interact) | zerops_browser | crawl4ai | playwright
   │
   ▼ (Facts extracted verbatim)
[F5: Temporal Synthesis]        Anchor to date -u + jina:guess_datetime_url; cross-check >= 2 primary sources;
                                tag GA/LTS vs beta/deprecated; strip internal jargon from queries.
   │
   ▼ (Verified technical truth ready)
[F6: LTM Persistence]           engram (mem_save) with exact versions, gotchas, and canonical URLs.
```

---

## 2. Core Epistemic Invariants

1. **Snippet Is Not Evidence (Jina F3 Mandate):** Search results from Exa, Tavily, Brave, or DuckDuckGo provide discovery URLs only. Read the canonical target page via `jina:read_url`, `curl r.jina.ai/<url>`, `context7:query-docs`, or `web_fetch_exa` before citing schemas, flags, or breaking changes.
2. **Dynamic Temporal Anchoring (`date -u`):** Pair discovery queries with the current year/release baseline and verify publication or modification timestamps via `jina:guess_datetime_url` or changelog headers.
3. **Stability Classification (GA/LTS First):** Recommend GA/LTS releases by default; explicitly label release-candidate, beta, or archived packages (`@modelcontextprotocol/server-brave-search` $\to$ `@brave/brave-search-mcp-server`).
4. **Ordered Quota Fallback (Zero Blind Retries):**
   - Route primary queries to `exa` (code/repos), `tavily` (releases/dates), `jina` (clean reading/arXiv/PDFs), and `firecrawl_developer_search` (skills/repos).
   - Switch to `brave` (1.1s throttle) only on primary failure, HTTP 429, or depleted quota.
   - Switch to `duckduckgo` $\to$ `s.jina.ai` only as an unmetered last resort, immediately tripping circuit breakers on DDG anomaly responses.

---

## 3. Inquiry Routing Table

| Inquiry Nature | F0–F1 | F2 Primary Discovery | F2 Fallback | F3 Verbatim (Required) | F4 Advanced |
|---|---|---|---|---|---|
| **NPM / PyPI / Crates / Go** | `engram` $\to$ `context7` | `exa` (`web_search_exa`) | `brave` $\to$ `duckduckgo` | `context7` / `jina:read_url` | Raw `curl` |
| **GitHub Repos & Benchmarks** | `engram` | `exa` / `firecrawl_developer_search` | `brave` $\to$ `duckduckgo` | `jina:read_url` / `web_fetch_exa` | `crawl4ai` |
| **Versions, CVEs & Breaking** | `engram` $\to$ `context7` | `tavily` (`tavily_search`) | `brave` $\to$ `duckduckgo` | `jina:read_url` + `guess_datetime_url` | `firecrawl_scrape` |
| **Branding, Design & Docs** | `engram` | `exa` / `jina:search_web` | `brave` $\to$ `duckduckgo` | `jina:read_url` (`r.jina.ai`) | `playwright` |
| **Papers & PDFs** | `engram` | `jina:search_arxiv` / `firecrawl_research_*` | `exa` $\to$ `brave` | `jina:extract_pdf` / `read_url` | `firecrawl_research_read_paper` |
| **Blocked SPA / WAF Site** | `engram` | `tavily` / `exa` | `brave` $\to$ `duckduckgo` | `jina:read_url` | `firecrawl` / `crawl4ai` / `zerops_browser` |

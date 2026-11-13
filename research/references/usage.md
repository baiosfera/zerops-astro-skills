# Research Reference Manual: 7-Phase Epistemic Workflows (v9.0)

Exhaustive operational guide for the multi-tier epistemic grounding pipeline in Antigravity CLI (`agy`).

---

## 1. Operating Modalities

### Modality A: Inline Compound Grounding (Turn-Level Inflow)
Execute sequentially inside the active turn for single-library checks, API verification, or configuration lookups:
1. **F0 — Local Recall (`engram`):** Call `mem_search(query)` to recover prior verified benchmarks and gotchas.
2. **F1 — Canonical Library Docs (`context7`):** Call `resolve-library-id` followed by `query-docs` for package signatures, SDK schemas, and breaking changes.
3. **F2 — Multi-Engine Discovery (Primaries $\to$ Fallbacks):**
   - **Code, GitHub repos & benchmarks:** `call_mcp_tool(ServerName="exa", ToolName="web_search_exa", Arguments={"query": "...", "numResults": 5})`.
   - **Releases, changelogs, CVEs & dates:** `call_mcp_tool(ServerName="tavily", ToolName="tavily_search", Arguments={"query": "...", "search_depth": "basic", "max_results": 5, "include_raw_content": false})`.
   - **LLM-native web & paper search:** `call_mcp_tool(ServerName="jina", ToolName="search_web", Arguments={"query": "..."})` (or `search_arxiv` for papers).
   - **Repos, agent skills & docs:** `call_mcp_tool(ServerName="firecrawl", ToolName="firecrawl_developer_search", Arguments={"query": "...", "k": 3, "skills": "only"})`.
   - **Fallback 1 (API errors / 429 / depleted primary quota):** `call_mcp_tool(ServerName="brave", ToolName="brave_web_search", Arguments={"query": "...", "count": 5})` (pause `>= 1.1s` between consecutive calls).
   - **Fallback 2 (Unmetered last-resort):** `call_mcp_tool(ServerName="duckduckgo", ToolName="duckduckgo_web_search", Arguments={"query": "..."})` (on anomaly block, switch immediately to `s.jina.ai` via `curl`).
4. **F3 — Verbatim Primary Reading (Jina Imprescindible):**
   - **Primary Reader MCP:** `call_mcp_tool(ServerName="jina", ToolName="read_url", Arguments={"url": "<canonical_url>"})` (supports `question` for targeted extraction; use `extract_pdf` for PDFs and `guess_datetime_url` to verify freshness).
   - **Selector-Filtered Jina HTTP:** `run_command("timeout 10s curl -sL -H \"Authorization: Bearer $JINA_API_KEY\" -H \"X-Target-Selector: article, main\" -H \"X-Retain-Images: none\" \"https://r.jina.ai/<canonical_url>\"")`.
   - **Secondary Extractors:** `exa:web_fetch_exa(urls=[...], maxCharacters=3000)`, `tavily:tavily_extract`, or raw `curl` for `raw.githubusercontent.com` / JSON endpoints.
5. **F4 — Dynamic SPAs & Anti-Bot Fallback:**
   - **Cloud SPA/WAF:** `firecrawl:firecrawl_scrape`, `firecrawl_map`, `firecrawl_crawl`, or `firecrawl_interact`.
   - **Zerops Previews:** `zerops:zerops_browser`.
   - **Local Zero-Cost Headless:** `crawl4ai` or `playwright` via `run_command`.
6. **F5–F6 — Synthesize & Persist:** Verify current time (`date -u`), cross-check `>= 2` primary sources, cite canonical URLs, and save durable insights with `engram:mem_save`.

### Modality B: Deep Research Dossier (Subagent Delegation)
Activate when synthesizing `>= 5` sources, comparing multiple tools/frameworks, or inspecting external repositories:
1. Launch `invoke_subagent` with `TypeName: "research"` and `Role: "<Scope> Researcher"`, injecting [`assets/subagent_prompt_contract.md`](file:///var/www/.agents/skills/research/assets/subagent_prompt_contract.md).
2. The subagent runs F0–F6, writes the report to `/var/www/artifacts/research/<target>_research_report.md`, and returns a concise summary with `<epistemic_attestation>`.
3. Await all subagent completion messages before drafting final architecture plans or mutating skills.

---

## 2. Neutral Query Engineering (Zero Internal Jargon)

Translate local project terms into universal engineering terminology before querying any external engine:
- Prompt caching & context governance $\to$ `"context engineering" "prompt caching" prefix stability`
- Deterministic hooks & syntax validation $\to$ `"agent harness" PreToolUse hook deterministic AST validation`
- Progressive disclosure in skills $\to$ `"progressive disclosure" LLM agent skills markdown router`
- Remote MCP transport $\to$ `"Streamable HTTP" MCP server endpoint authentication headers`

---

## 3. Exact `call_mcp_tool` Recipes (Antigravity CLI Native)

### Context7 (`ServerName: "context7"`)
```json
{"ServerName": "context7", "ToolName": "resolve-library-id", "Arguments": {"query": "astro", "libraryName": "astro"}}
```
```json
{"ServerName": "context7", "ToolName": "query-docs", "Arguments": {"libraryId": "/withastro/astro", "query": "server islands SSR"}}
```

### Jina Remote MCP (`ServerName: "jina"`)
```json
{"ServerName": "jina", "ToolName": "read_url", "Arguments": {"url": "https://docs.example.com/guide"}}
```
```json
{"ServerName": "jina", "ToolName": "search_web", "Arguments": {"query": "Streamable HTTP MCP specification 2026"}}
```
```json
{"ServerName": "jina", "ToolName": "guess_datetime_url", "Arguments": {"url": "https://docs.example.com/changelog"}}
```

### Exa (`ServerName: "exa"`)
```json
{"ServerName": "exa", "ToolName": "web_search_exa", "Arguments": {"query": "FastAPI Granian ASGI production benchmarks 2026", "numResults": 5}}
```
```json
{"ServerName": "exa", "ToolName": "web_fetch_exa", "Arguments": {"urls": ["https://github.com/org/repo/blob/main/README.md"], "maxCharacters": 3000}}
```

### Tavily (`ServerName: "tavily"`)
```json
{"ServerName": "tavily", "ToolName": "tavily_search", "Arguments": {"query": "Bun 1.3 changelog breaking changes", "search_depth": "basic", "max_results": 5, "include_raw_content": false}}
```

### Fallbacks (`brave` then `duckduckgo`)
```json
{"ServerName": "brave", "ToolName": "brave_web_search", "Arguments": {"query": "PostgreSQL 18 uuidv7 release notes", "count": 5}}
```
```json
{"ServerName": "duckduckgo", "ToolName": "duckduckgo_web_search", "Arguments": {"query": "PostgreSQL 18 uuidv7 syntax"}}
```

---

## 4. Routing Matrix by Inquiry Type

| Inquiry Type | F1 Official | F2 Discovery | F2 Fallback | F3 Verbatim | F4 Advanced |
|---|---|---|---|---|---|
| **SDK / Types / APIs** | `context7` | `exa` (`web_search_exa`) | `brave` $\to$ `duckduckgo` | `jina` (`read_url`) / `context7` | Native `curl` |
| **Releases / CVEs** | `context7` | `tavily` (`tavily_search`) | `brave` $\to$ `duckduckgo` | `jina` (`read_url` + `guess_datetime_url`) | `firecrawl_scrape` |
| **Repos / Agent Skills** | — | `firecrawl_developer_search` / `exa` | `jina` (`search_web`) $\to$ `brave` | `jina` (`read_url`) / `web_fetch_exa` | `crawl4ai` |
| **Academic / PDFs** | — | `jina` (`search_arxiv`) / `firecrawl_research_search_papers` | `exa` $\to$ `brave` | `jina` (`extract_pdf` / `read_url`) | `firecrawl_research_read_paper` |
| **WAF / JS-Heavy SPA** | — | `tavily_search` / `brave` | `duckduckgo` | `jina` (`r.jina.ai`) | `firecrawl` (`scrape`/`interact`) / `zerops_browser` |

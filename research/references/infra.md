# Research Infrastructure Manual: Quotas, Rate Limits & Failover Architecture (v7.2)

This manual defines the technical operating parameters, environment credentials, rate limits, credit preservation policies, and error recovery cascades for the 12 research engines.

---

## 1. Engine Quotas & Operating Parameters

| Tier | Engine | Transport / Protocol | Monthly Quota | Rate Limit | Token / Cost Impact |
|---|---|---|---|---|---|
| **Tier 0** | **Engram LTM** | Local SQLite + FTS5 | **Unlimited** | None (O(1)) | **$0 / 0 Tokens** |
| **Tier 1** | **Context7 Docs** | REST API | **Unlimited** | None | **$0** |
| **Tier 2** | **Exa Search** | MCP (`exa`) | 1,000 req/mo | Standard | ~1 credit per query |
| **Tier 2** | **Tavily Search** | MCP (`tavily`) | 1,000 req/mo | Standard | 1 credit (basic), 2 (advanced) |
| **Tier 2** | **Brave Search** | MCP (`brave`) | 2,000 queries/mo | **1 req/second** | **Enforce >= 1.1s delay** |
| **Tier 2** | **Jina Search** | HTTP (`s.jina.ai`) | 1M tokens/min | Free tier | Free |
| **Tier 2** | **DuckDuckGo** | MCP (`duckduckgo`) | **Unlimited** | Standard | **$0 / Zero Quota** |
| **Tier 3** | **Jina Reader** | HTTP (`r.jina.ai`) | 1M tokens/min | Free tier | Free Markdown proxy |
| **Tier 3** | **Native HTTP** | Antigravity `read_url_content` | **Unlimited** | Network-bound | **$0** |
| **Tier 4** | **Crawl4AI** | Local Python 3.12+ | **Unlimited** | CPU/RAM-bound | **$0 / 100% Local** |
| **Tier 4** | **Playwright** | Local Headless Chromium | **Unlimited** | Local runtime | **$0 / 100% Local** |
| **Tier 4** | **Firecrawl** | MCP (`firecrawl`) | 500 credits/mo | Standard | 1 credit per scrape/map |
| **Tier 4** | **Zerops Browser** | MCP (`zerops`) | Platform-managed | Incus container | Zero external credits |

---

## 2. Environment Variables & Secret Ingestion

All external API keys are ingested natively via Zerops project environment variables (`zerops_env` / `/etc/environment`) and referenced exclusively by variable name in shell scripts, never logged or hardcoded in chat:
- `EXA_API_KEY`: Authenticates Exa MCP server.
- `TAVILY_API_KEY`: Authenticates Tavily MCP server.
- `BRAVE_API_KEY`: Authenticates Brave Search MCP server.
- `FIRECRAWL_API_KEY`: Authenticates Firecrawl MCP server.
- `JINA_API_KEY`: Optional; elevates rate limits on `r.jina.ai` and `s.jina.ai`.

---

## 3. Credit Preservation & Zero-Waste Cascade

To avoid depleting monthly quotas on paid APIs, research strictly follows this progressive cascade:

```text
┌──────────────────────────────────────────────────────────┐
│              ZERO-WASTE EXECUTION CASCADE                │
└────────────────────────────┬─────────────────────────────┘
                             │
            ┌────────────────▼────────────────┐
            │   Tier 0: Engram LTM Recall     │ ──► [Cached Memory Found?] ──► Return
            └────────────────┬────────────────┘
                             │ (Cache Miss)
            ┌────────────────▼────────────────┐
            │ Tier 1: Context7 Canonical Docs │ ──► [Package/Types Query?] ──► Done
            └────────────────┬────────────────┘
                             │ (General Research)
            ┌────────────────▼────────────────┐
            │   Tier 2: Exa / Tavily / DDG    │ ──► Discovery of URLs
            └────────────────┬────────────────┘
                             │ (Extract Content)
            ┌────────────────▼────────────────┐
            │ Tier 3: Jina Reader / Native    │ ──► Markdown Extraction
            └────────────────┬────────────────┘
                             │ (Cloudflare / WAF Blocked)
            ┌────────────────▼────────────────┐
            │ Tier 4: Crawl4AI / Firecrawl    │ ──► Deep Scraping / Anti-bot Bypass
            └─────────────────────────────────┘
```

### Golden Rules for Quota & Token Conservation (CoHaLo SOTA):
1. **Never use `web_fetch_exa`** without specifying `maxCharacters: 2000-3000` to prevent token bloat, or prefer Jina Reader (`r.jina.ai`) / `read_url_content` for free zero-credit extraction.
2. **Always default Tavily to `search_depth="basic"`** with `max_results=5` and `include_raw_content=false` to avoid burning double credits and flooding context with raw HTML.
3. **Always pause >= 1.1s** before invoking `brave_web_search` consecutively to prevent HTTP 429 rate limit errors.
4. **Use `firecrawl_developer_search`** with `skills="only"` when investigating agent architectures, prompt engineering, or SDK patterns.
5. **Reserve Firecrawl Scrape** exclusively for Cloudflare-protected SPAs or deep recursive crawling where local Crawl4AI fails.

---

## 4. Bounded Execution, Token Engineering & Hygiene Invariants

- **Timeout Clamps:** All HTTP and CLI operations must run with `timeout 10s` to prevent hanging processes.
- **Async Execution Guard:** Terminal tools must set `WaitMsBeforeAsync: 10000` to prevent unintended background detachments.
- **Clean Hygiene:** Python scripts executed for Crawl4AI must use `-B` (`python3 -B`) and enforce `sys.dont_write_bytecode = True` to eliminate residual `__pycache__` artifacts.
- **CoHaLo Token Reduction Mechanisms (SOTA 49% Savings):**
  1. *Action Fusion:* Merge adjacent read and verification steps into unified passes to eliminate redundant model roundtrips.
  2. *ObservationPack:* Restrict payload lengths (`maxCharacters: 3000`, `max_results: 5`, `k: 3`) and avoid raw HTML dumps.
  3. *Evidence-Preserving Reducer:* Distill raw tool outputs into compact `<epistemic_attestation>` blocks with canonical URLs.
  4. *Context Compact:* Archive intermediate research logs to `/var/www/artifacts/` instead of carrying full raw dumps in active context.
- **Circuit Breakers & Empirical Anomaly Handling:** Maximum 2 retry attempts per failed request. On DuckDuckGo anomaly detection (`Error: DDG detected an anomaly`), abort DDG immediately and fallback to Jina Reader or Native HTTP without looping.

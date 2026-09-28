---
name: research
description: "Trigger: research, investigar, buscar en vivo, estado del arte, benchmark, comparar tecnologias, versiones actuales, exa, tavily, brave, duckduckgo, jina, context7, firecrawl, crawl4ai, playwright, puppeteer, engram. Multi-tier compound epistemic research pipeline with 12 engines and zero-quota-waste state machine."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "7.2"
---

# `research` — Compound Epistemic Grounding Engine (v7.2)

High-performance multi-tier research engine orchestrating 12 epistemic tools across memory, official package docs, neural search, and headless scraping. Benchmarks local code against external SOTA in the Continuous Present (`date -u`).

## Architecture & Dual-RAG SSoT

- **Exhaustive Workflows & Tool Recipes:** [references/usage.md](file:///var/www/.agents/skills/research/references/usage.md) — 12-engine operational catalog, inline compound grounding recipes, Crawl4AI local scraping, Playwright route aborts (<150ms), and Firecrawl structured extraction.
- **Infrastructure, Quotas & Fallbacks:** [references/infra.md](file:///var/www/.agents/skills/research/references/infra.md) — API keys, quotas, rate limits (Brave 1 req/s), bounded timeouts (`timeout 10s`), and zero-cost failover cascade.
- **Engines Reference & Heuristics:** [references/tools.md](file:///var/www/.agents/skills/research/references/tools.md) · [references/heuristics.md](file:///var/www/.agents/skills/research/references/heuristics.md) — In-depth engine specifications and research heuristics.

## Operating Modalities

1. **Inline Compound Grounding (Turn-Level Inflow):**
   Active during development, auditing, planning, or technical verification. The agent invokes Exa (`web_search_exa`), Tavily (`tavily_search`), Context7 (`query-docs`), or Jina Reader (`r.jina.ai`) directly in the turn to contrast local code with live primary sources. Action-First Execution Lockdown guarantees live verification before technical assertions (documented via epistemic_attestation in formal subagent reports).
2. **Deep Research Dossier (Subagent Delegation):**
   Mandatory when analyzing external GitHub repositories, synthesizing 10+ sources, or producing formal architecture proposals. Delegates to subagent (`typeName: "research"`) injecting [assets/subagent_prompt_contract.md](file:///var/www/.agents/skills/research/assets/subagent_prompt_contract.md) and offloading to `/var/www/artifacts/<target>_research_report.md`.

## Decision Routing Matrix

| Task Nature | Primary Discovery | Verbatim Inflow | Scraper / Advanced |
|---|---|---|---|
| **Ecosystem & Types** | `context7` (`query-docs`) | `context7` · Jina Reader | Native HTTP |
| **GitHub & Architecture** | `web_search_exa` (code) | Jina Reader (`r.jina.ai`) | Crawl4AI (`fit_markdown`) |
| **Changelogs & CVEs** | `tavily_search` (basic) | Jina Reader | Native HTTP |
| **Brand & Design** | `brave_web_search` · Exa | Jina Reader | Playwright / Puppeteer |
| **Deep Domain Crawling** | `tavily_map` · Firecrawl Map | Jina Reader | Firecrawl Crawl / Crawl4AI |
| **Anti-Bot SPAs** | Firecrawl Scrape | Firecrawl Extract | Zerops Browser |
| **Zero-Quota Fallback** | `duckduckgo_web_search` | Native HTTP | Crawl4AI |

## Hard Invariants

1. **Zero-Local Isolation & Mandatory Web Grounding:** Architecture, security, and technology evaluations must benchmark local files against live primary sources. Local introspection alone is strictly incomplete without web grounding.
2. **Primary Sources (Matt Pocock Standard):** Search snippets serve strictly as discovery pointers. Read canonical raw files via Jina Reader (`r.jina.ai`) or Context7 before establishing claims.
3. **Credit Conservation:** Query Engram LTM first. Use `search_depth="basic"` on Tavily. Enforce >= 1.1s pauses between Brave calls. Reserve Firecrawl for anti-bot protected sites.

## Resources & Sensors

- **Query Matrix:** [assets/research_query_matrix.json](file:///var/www/.agents/skills/research/assets/research_query_matrix.json)
- **Subagent Contract:** [assets/subagent_prompt_contract.md](file:///var/www/.agents/skills/research/assets/subagent_prompt_contract.md)
- **Physical Sensor:** [scripts/research-validate.sh](file:///var/www/.agents/skills/research/scripts/research-validate.sh)

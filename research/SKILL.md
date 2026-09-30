---
name: research
description: "Trigger: research, investigar, buscar en vivo, estado del arte, benchmark, comparar tecnologias, versiones actuales, exa, tavily, brave, duckduckgo, jina, context7, firecrawl, crawl4ai, playwright, puppeteer, engram. Multi-tier compound epistemic research pipeline with 12 engines under Supreme Directive v8.2."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "8.4"
---

# `research` — Compound Epistemic Grounding Engine (v8.4)

Multi-tier engine orchestrating 12 epistemic tools across memory, package docs, search, and headless scraping. Benchmarks code against SOTA in the Continuous Present (`date -u`), enforcing Epistemic Honesty and Anti-AMN Mandates under [`00-SUPREME-DIRECTIVE.md`](file:///var/www/.agents/rules/00-SUPREME-DIRECTIVE.md). Prohibits local isolation ("black box") by mandating real-time web verification.

## Architecture & Dual-RAG SSoT

- **Exhaustive Workflows & Tool Recipes:** [references/usage.md](file:///var/www/.agents/skills/research/references/usage.md) — 12-engine catalog, grounding recipes, Crawl4AI, and Firecrawl extraction.
- **Infrastructure, Quotas & Fallbacks:** [references/infra.md](file:///var/www/.agents/skills/research/references/infra.md) — API keys, quotas, rate limits, timeouts (`timeout 10s`), and failover.
- **Engines Reference & Heuristics:** [references/tools.md](file:///var/www/.agents/skills/research/references/tools.md) · [references/heuristics.md](file:///var/www/.agents/skills/research/references/heuristics.md) — Engine specifications.

## Operating Modalities

1. **Inline Compound Grounding (Turn-Level Inflow):**
   Invokes Exa, Brave, Tavily, Context7, or Jina Reader directly to contrast code with primary sources. Action-First Execution Lockdown guarantees verification before technical assertions (documented via epistemic_attestation in subagent reports). Model weights are unverified hypotheses.
2. **Deep Research Dossier (Subagent Delegation):**
   Mandatory when synthesizing 10+ sources or analyzing GitHub repos. Delegates to subagent injecting [assets/subagent_prompt_contract.md](file:///var/www/.agents/skills/research/assets/subagent_prompt_contract.md) and offloading to `/var/www/artifacts/<target>_research_report.md`.

## Decision Routing Matrix (Compound Discovery Pipeline)

| Research Stage | Orchestrated Tools | Epistemic Objective |
|---|---|---|
| **Multi-Index Discovery** | `web_search_exa` · `brave_web_search` · `tavily_search` · `firecrawl_developer_search` | Neural semantic search, 30B+ neutral index, agent skills |
| **Site & API Mapping** | `firecrawl_map` · `tavily_map` | Complete URL hierarchy and documentation sitemaps |
| **Verbatim Deep Inflow** | Jina Reader (`r.jina.ai`) · `web_fetch_exa` · `firecrawl_scrape` | Full Markdown extraction, JSON schemas, zero snippet clipping |
| **Live AST & Contracts** | `context7` (`resolve-library-id` · `query-docs`) | Live package documentation, types, and official API specs |
| **Dynamic SPAs & State** | `firecrawl_interact` · Zerops Browser · Playwright | DOM actions, JS rendering, dynamic state execution |
| **Zero-Quota Fallback** | `duckduckgo_web_search` · Native HTTP · Crawl4AI | Resilient unmetered multi-hop fallback |

## Hard Invariants

1. **Zero-Local Isolation & Mandatory Web Grounding:** Technical evaluations must benchmark local files against live external sources in the Continuous Present (`date -u`). Prohibido autoaislarse en el contenedor ZCP.
2. **Epistemic Honesty & Absolute Anti-AMN Mandate:** Pretrained memory (AMN) is unverified hypothesis. Grounding requires live primary sources verbatim (Context7, docs, AST, source code).
3. **Primary Sources (Matt Pocock Standard):** Search snippets serve strictly as discovery pointers. Read canonical raw files via Jina Reader (`r.jina.ai`) or Context7 before establishing claims.
4. **Credit Conservation & Token Hygiene:** Query Engram first. Set `maxCharacters: 3000` on Exa. Enforce >= 1.1s pauses on Brave. Catch DDG anomalies. Reserve Firecrawl for anti-bot sites.

## Resources & Sensors

- **Query Matrix:** [assets/research_query_matrix.json](file:///var/www/.agents/skills/research/assets/research_query_matrix.json)
- **Subagent Contract:** [assets/subagent_prompt_contract.md](file:///var/www/.agents/skills/research/assets/subagent_prompt_contract.md)
- **Physical Sensor:** [scripts/research-validate.sh](file:///var/www/.agents/skills/research/scripts/research-validate.sh)

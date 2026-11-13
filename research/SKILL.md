---
name: research
description: "Trigger: research, investigar, buscar en vivo, estado del arte, benchmark, comparar tecnologias, versiones actuales, exa, tavily, brave, duckduckgo, jina, context7, firecrawl, crawl4ai, playwright, puppeteer, engram. Multi-tier 7-phase epistemic grounding pipeline (Engram, Context7, Exa, Tavily, Jina, Firecrawl, Brave/DuckDuckGo fallbacks) under Supreme Directive v9.0."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "9.0"
---

# `research` — Compound Epistemic Grounding Engine (v9.0)

Anti-AMN analytical backbone enforcing live primary-source verification in the Continuous Present (`date -u`) under [`00-SUPREME-DIRECTIVE.md`](file:///var/www/.agents/rules/00-SUPREME-DIRECTIVE.md). Parametric weights serve exclusively as unverified hypotheses until grounded across the 7 epistemic phases.

## Dual-RAG SSoT Pointers

- **7-Phase Workflows & Tool Calls:** [references/usage.md](file:///var/www/.agents/skills/research/references/usage.md)
- **Remote MCPs, Quotas & Fallback Cascade:** [references/infra.md](file:///var/www/.agents/skills/research/references/infra.md)
- **Engine Catalog & Parameters:** [references/tools.md](file:///var/www/.agents/skills/research/references/tools.md) · [references/heuristics.md](file:///var/www/.agents/skills/research/references/heuristics.md)

## 7 Epistemic Phases (Mandatory Order)

| Phase | Role | Active Engines (`ServerName` / CLI) | Exit Criterion |
|---|---|---|---|
| **F0** | **Local LTM Recall** | `engram` (`mem_search`, `mem_context`) | Check prior verified project decisions ($0) |
| **F1** | **Canonical SDK Docs** | `context7` (`resolve-library-id`, `query-docs`) | Exact library signatures & active version ($0) |
| **F2** | **Discovery + Fallbacks** | **Primary:** `exa` (`web_search_exa`), `tavily` (`tavily_search`), `jina` (`search_web`), `firecrawl` (`firecrawl_developer_search`)<br>**Fallbacks:** `brave` (`brave_web_search`) $\to$ `duckduckgo` (`duckduckgo_web_search`) | 3–5 canonical primary URLs; trigger Brave/DDG on error, 429, or empty quota |
| **F3** | **Verbatim Reading** | **Jina Imprescindible:** `jina` (`read_url`, `extract_pdf`, `guess_datetime_url`) or `curl` `r.jina.ai/<url>`; secondary `web_fetch_exa`, `tavily_extract` | Full primary markdown read; snippets serve as discovery pointers only |
| **F4** | **SPAs & Anti-Bot** | `firecrawl` (`firecrawl_scrape`, `firecrawl_map`, `firecrawl_interact`), `zerops_browser`, `crawl4ai`, `playwright` | Dynamic JS/WAF pages extracted cleanly |
| **F5** | **Temporal Synthesis** | `date -u` + `jina` (`guess_datetime_url`) | Triangulate $\ge 2$ primary sources; mark GA/LTS vs beta/deprecated |
| **F6** | **LTM Persistence** | `engram` (`mem_save`) | Store verified facts and canonical URLs |

## Operating Modalities

1. **Inline Compound Grounding:** Run F0 $\to$ F1/F2 $\to$ **F3 Jina Verbatim** directly for single-library lookups, API diffs, or focused bug diagnosis.
2. **Deep Research Dossier:** Delegate via `invoke_subagent` (`TypeName: "research"`) using [assets/subagent_prompt_contract.md](file:///var/www/.agents/skills/research/assets/subagent_prompt_contract.md) when benchmarking stacks, inspecting repos, or synthesizing $\ge 5$ sources; write dossier to `/var/www/artifacts/research/<target>_research_report.md`.

## Positive Behavioral Contract

- **Zero-AMN Execution:** Verify every version, limit, schema, and flag through live F1–F4 tool calls before stating facts or editing skills/plans.
- **Neutral Query Formulation:** Translate internal governance terms into universal industry keywords before querying external search engines.
- **Jina-First Verbatim Extraction:** Read full candidate docs with `jina` (`read_url`) or `r.jina.ai` prior to citing conclusions; trigger `brave` then `duckduckgo` only as F2 fallbacks.

## Resources & Sensors

- **Routing Matrix:** [assets/research_query_matrix.json](file:///var/www/.agents/skills/research/assets/research_query_matrix.json) · **Subagent Contract:** [assets/subagent_prompt_contract.md](file:///var/www/.agents/skills/research/assets/subagent_prompt_contract.md)
- **Sensors:** `tool-guard.py --test` · `skills-suite-validate` · `ssot-parity-check`

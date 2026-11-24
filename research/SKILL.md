---
name: research
description: "Trigger: research, investigar, buscar en vivo, estado del arte, benchmark, comparar tecnologias, versiones actuales, exa, tavily, brave, duckduckgo, jina, context7, firecrawl, engram. Multi-tier live epistemic grounding pipeline under Supreme Directive v10.0."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "10.0"
---

# `research` — Compound Epistemic Grounding Engine (v10.0)

Anti-AMN grounding workflow verifying live primary sources in the Continuous Present (`date -u`) under [`00-SUPREME-DIRECTIVE.md`](file:///var/www/.agents/rules/00-SUPREME-DIRECTIVE.md).

## Dual-RAG Pointers
- **Workflows & Tool Calls**: [references/usage.md](file:///var/www/.agents/skills/research/references/usage.md)
- **Remote MCPs & Fallbacks**: [references/infra.md](file:///var/www/.agents/skills/research/references/infra.md) · [references/tools.md](file:///var/www/.agents/skills/research/references/tools.md) · [references/heuristics.md](file:///var/www/.agents/skills/research/references/heuristics.md)

## 7 Epistemic Phases

| Phase | Role | Active Engines (`ServerName` / Tool) | Exit Criterion |
|---|---|---|---|
| **F0** | **Local LTM Recall** | `engram` (`mem_search`, `mem_context`) | Prior verified decisions checked |
| **F1** | **Canonical SDK Docs** | `context7` (`resolve-library-id`, `query-docs`) | Exact library signatures & version |
| **F2** | **Web Discovery** | Primary: `exa`, `tavily`, `jina:search_web`, `firecrawl`<br>Fallbacks: `brave` $\to$ `duckduckgo` $\to$ `search_web` | 2–5 canonical primary URLs |
| **F3** | **Verbatim Reading** | `jina:read_url` (pass `question` to save tokens), `extract_pdf`, `web_fetch_exa`, `tavily_extract` | Primary markdown read (not snippets) |
| **F4** | **SPAs & Anti-Bot** | `firecrawl_scrape`, `firecrawl_map`, `zerops_browser` | Dynamic JS/WAF pages extracted |
| **F5** | **Temporal Synthesis** | `date -u` + `>= 2` primary sources | Verified GA/LTS vs deprecated |
| **F6** | **LTM Persistence** | `engram` (`mem_save`) | Verified facts saved before reply |

## Operating Modalities
1. **Inline External Grounding (Default)**: Run F0 $\to$ F1/F2 $\to$ F3 verbatim directly in the parent thread via MCP tools.
2. **Broad Local Codebase Audit**: Delegate local read-only surveys via `invoke_subagent(TypeName="research", Model="flash")` using [assets/subagent_prompt_contract.md](file:///var/www/.agents/skills/research/assets/subagent_prompt_contract.md) (`research` subagents have no external network access).

## Resources
- **Routing Matrix**: [assets/research_query_matrix.json](file:///var/www/.agents/skills/research/assets/research_query_matrix.json) · **Subagent Contract**: [assets/subagent_prompt_contract.md](file:///var/www/.agents/skills/research/assets/subagent_prompt_contract.md)

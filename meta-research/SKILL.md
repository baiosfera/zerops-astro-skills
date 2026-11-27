---
name: meta-research
description: "Trigger: meta-research, research, investigar, buscar en vivo, estado del arte, benchmark, comparar tecnologias, versiones actuales, exa, tavily, brave, duckduckgo, jina, context7, firecrawl, engram. Compound live research and Anti-AMN grounding orchestrator."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "3.1"
---

# `meta-research` — Epistemic Grounding & Anti-AMN Orchestrator (v3.1)

## Activation Contract
Activate when evaluating SOTA approaches, comparing architectural trade-offs, verifying breaking changes, or grounding unfamiliar APIs under [`00-SUPREME-DIRECTIVE.md`](file:///var/www/.agents/rules/00-SUPREME-DIRECTIVE.md).

## Positive Operational Contract
- **Primary-Source Anchoring**: Anchor versions, flags, limits, and APIs in live primary sources (`date -u`) or live topology (`zerops_discover`).
- **Inline External Grounding (MCP First)**: The `research` subagent runs in a read-only sandbox **with no external network access**. Run all external web/SDK lookups inline in the parent thread using MCP:
  `engram` (F0) $\to$ `context7` (F1) $\to$ `exa` / `tavily` / `jina` / `firecrawl`, fallbacks `brave` $\to$ `duckduckgo` $\to$ `search_web` (F2) $\to$ **`jina:read_url`** / `web_fetch_exa` verbatim reading (F3) $\to$ `firecrawl_scrape` / `zerops_browser` (F4) $\to$ `mem_save` (F6).
- **Meta Ad Library (`ad-library` First)**: For Meta Ad Library competitive intelligence, never dump ~65 KB raw `firecrawl_scrape` markdown into chat context. Run `ad-library fetch` (or pipe `firecrawl_scrape` into `ad-library parse`) to strip boilerplate in pure Python (`0` LLM tokens) into a `< 3 KB` brief, then inspect winning destination URLs with `jina:read_url(question=...)`.
- **Snippet Is Not Evidence**: Treat search snippets strictly as pointers; read canonical pages with `jina:read_url` (`question` parameter saves tokens), `context7:query-docs`, or `web_fetch_exa`.
- **Frugal Local Subagent Delegation**: Run focused local checks inline. Delegate via `invoke_subagent(TypeName="research", Model="flash")` strictly for broad multi-directory local codebase audits.

## Active Sub-Skills & References
- **7-Phase Engine**: [`research`](file:///var/www/.agents/skills/research/SKILL.md)
- **Protocols & Infra**: [`references/usage.md`](file:///var/www/.agents/skills/meta-research/references/usage.md) · [`references/infra.md`](file:///var/www/.agents/skills/meta-research/references/infra.md)

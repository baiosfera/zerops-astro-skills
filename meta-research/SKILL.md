---
name: meta-research
description: "Trigger: meta-research, research, investigar, buscar en vivo, estado del arte, benchmark, comparar tecnologias, versiones actuales, exa, tavily, brave, duckduckgo, jina, context7, firecrawl, crawl4ai, playwright, puppeteer, engram. Multi-tier compound epistemic research pipeline orchestrator."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.0"
---

# `meta-research` — Master Epistemic Grounding & Multi-Engine Research Orchestrator (v1.0)

## Activation Contract
Activate when evaluating SOTA approaches, comparing architectural trade-offs, investigating unfamiliar third-party libraries, verifying breaking API changes, or benchmarking frameworks. Exclusively governs EPISTEMIC RESEARCH, MULTI-TIER SEARCH, DOCUMENTATION GROUNDING, AND ANTI-AMN SAFEGUARDS.

## Hard Rules & Positive Guidance
- **Absolute Anti-AMN Invariant**: Never state technical claims, library limits, breaking changes, or API schemas from parametric stochastic memory. Anchor every technical assertion in primary sources or live platform inspection (`zerops_discover`).
- **Verbatim Evidence Anchoring**: Back all technical comparisons and architectural proposals with exact verbatim citations and verified primary source URLs.
- **Epistemic Multi-Engine Triangulation**: Cross-verify technical findings across multiple independent tiers: code intelligence (`context7`), semantic/web search (`exa`, `tavily`, `brave`), and full-text scrapers (`jina`, `firecrawl`).
- **Thin Orchestrator Delegation**: Launch exploratory or multi-query research via dedicated read-only subagents (`invoke_subagent` with `research`) to keep the primary orchestrator context window clean.
- **Physical Attestation Before Assertion**: Claim task completion strictly after `skills-suite-validate` and `ssot-parity-check` pass with exit code 0.

## Active Sub-Skills Dispatch Table

| Focus | Sub-Skill | Canonical SSoT Pointer | Responsibility |
|---|---|---|---|
| **Multi-Tier Pipeline** | `research` | [`research`](file:///var/www/.agents/skills/research/SKILL.md) | 12-engine compound epistemic research pipeline |
| **Doc Interrogation** | `grill-with-docs` | [`grill-with-docs`](file:///var/www/.agents/skills/grill-with-docs/SKILL.md) | Relentless verification against verbatim official documentation |

## Epistemic Multi-Tier Engine Matrix

| Tier | Engine Category | Active Tools / MCPs | Best Used For |
|---|---|---|---|
| **Tier 1** | Code & Library Documentation | `context7` (`resolve-library-id`, `query-docs`) | Official SDK reference, exact method signatures, breaking changes |
| **Tier 2** | Semantic & Neural Web Search | `exa` (`web_search_exa`), `tavily` (`tavily_search`), `brave` | Modern technical blogs, ecosystem updates, GitHub discussions |
| **Tier 3** | Markdown Extraction & Scrapers | `jina` (r.jina.ai), `firecrawl` (`firecrawl_scrape`) | Clean full-text scraping without DOM noise, paywall-free technical reading |

## Decision Gates

| Challenge | Action / Protocol | Reference |
|---|---|---|
| API or Library Version Unknown | Query Context7 before proposing architecture | [`references/usage.md#1-context7-protocol`](file:///var/www/.agents/skills/meta-research/references/usage.md) |
| Multi-Engine Technical Comparison | Triangulate across Exa, Context7, and official repos | [`references/usage.md#2-triangulation-protocol`](file:///var/www/.agents/skills/meta-research/references/usage.md) |
| Deep Scraping & Content Ingestion | Scrape clean markdown via Jina Reader or Firecrawl | [`references/usage.md#3-scraping-protocol`](file:///var/www/.agents/skills/meta-research/references/usage.md) |
| Research Delegation Strategy | Spawn scoped research subagent to protect context | [`references/infra.md#1-subagent-delegation`](file:///var/www/.agents/skills/meta-research/references/infra.md) |

## Commands
```bash
# Verify SSoT parity across Drive, Git, and active services
ssot-parity-check

# Execute universal skill validation
skills-suite-validate
```

## References
- [`references/usage.md`](file:///var/www/.agents/skills/meta-research/references/usage.md) · [`references/infra.md`](file:///var/www/.agents/skills/meta-research/references/infra.md)

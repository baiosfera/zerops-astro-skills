---
name: meta-research
description: "Trigger: meta-research, research, investigar, buscar en vivo, estado del arte, benchmark, comparar tecnologias, versiones actuales, exa, tavily, brave, duckduckgo, jina, context7, firecrawl, crawl4ai, playwright, puppeteer, engram. Master 7-phase Anti-AMN epistemic research orchestrator."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# `meta-research` — Master Epistemic Grounding & Anti-AMN Orchestrator (v2.0)

## Activation Contract
Activate when evaluating SOTA approaches, comparing architectural trade-offs, investigating unfamiliar libraries, verifying breaking changes, or benchmarking stacks under [`00-SUPREME-DIRECTIVE.md`](file:///var/www/.agents/rules/00-SUPREME-DIRECTIVE.md). Governs the 7-phase epistemic pipeline (F0–F6), Jina verbatim primary reading, ordered quota fallbacks (`brave` $\to$ `duckduckgo`), and `tool-guard.py` Anti-AMN enforcement.

## Positive Operational Contract
- **Primary-Source Anchoring:** Anchor every version, limit, signature, and architectural claim in live primary sources verified in the Continuous Present (`date -u`) or live inspection (`zerops_discover`).
- **7-Phase Pipeline Fidelity:** Execute `F0` (`engram`) $\to$ `F1` (`context7`) $\to$ `F2` (`exa` / `tavily` / `jina` / `firecrawl`, fallback `brave` $\to$ `duckduckgo`) $\to$ **`F3` (`jina:read_url` / `r.jina.ai` mandatory verbatim reading)** $\to$ `F4` (`firecrawl_scrape` / `crawl4ai` / `zerops_browser`) $\to$ `F5` (`date -u` triangulation) $\to$ `F6` (`engram` `mem_save`).
- **Snippet Is Not Evidence:** Treat search snippets strictly as discovery pointers; read full canonical pages via `jina` (`read_url` / `r.jina.ai`), `context7`, or `web_fetch_exa` before drawing conclusions.
- **Thin Orchestrator Delegation:** Launch `invoke_subagent` (`TypeName: "research"`) for investigations requiring $\ge 3$ queries or $\ge 5$ primary sources, waiting for all reports before drafting plans.
- **Physical Attestation:** Verify updates with `tool-guard.py --test`, `skills-suite-validate`, and `ssot-parity-check` (`exit code 0`).

## Active Sub-Skills Dispatch Table

| Focus | Sub-Skill | Canonical SSoT Pointer | Responsibility |
|---|---|---|---|
| **7-Phase Engine** | `research` | [`research`](file:///var/www/.agents/skills/research/SKILL.md) | 7-phase pipeline, remote MCPs, Jina verbatim core & fallbacks |
| **Doc Interrogation** | `grill-with-docs` | [`grill-with-docs`](file:///var/www/.agents/skills/grill-with-docs/SKILL.md) | Verbatim claim auditing against official documentation |

## Epistemic Multi-Tier Matrix

| Tier | Engines (`ServerName`) | Operational Role |
|---|---|---|
| **F0 Memory** | `engram` | Prior verified decisions & gotchas ($0) |
| **F1 Official SDK** | `context7` (remote HTTP) | Canonical package docs & signatures ($0) |
| **F2 Discovery** | Primary: `exa`, `tavily`, `jina`, `firecrawl` (remote HTTP)<br>Fallbacks: `brave` $\to$ `duckduckgo` | Multi-index URL discovery + quota failover |
| **F3 Verbatim Core** | `jina` (`read_url`, `extract_pdf`, `r.jina.ai`), `web_fetch_exa` | Full primary markdown & PDF extraction |
| **F4 Dynamic SPAs** | `firecrawl`, `zerops_browser`, `crawl4ai`, `playwright` | JS rendering, maps & WAF bypass |

## Decision Gates & Sensors

| Challenge | Action / Protocol | Reference |
|---|---|---|
| Library / SDK Specs | Run `context7` (`resolve-library-id` + `query-docs`) | [`references/usage.md#1-context7-code-intelligence-protocol`](file:///var/www/.agents/skills/meta-research/references/usage.md) |
| Multi-Engine SOTA Comparison | Triangulate `exa`/`tavily` + **`jina:read_url`** ($\ge 2$ sources) | [`references/usage.md#2-multi-engine-triangulation-protocol`](file:///var/www/.agents/skills/meta-research/references/usage.md) |
| Subagent & Anti-AMN Guard | Delegate via `research` subagent; satisfy `tool-guard.py` | [`references/infra.md`](file:///var/www/.agents/skills/meta-research/references/infra.md) |

## References
- [`references/usage.md`](file:///var/www/.agents/skills/meta-research/references/usage.md) · [`references/infra.md`](file:///var/www/.agents/skills/meta-research/references/infra.md)

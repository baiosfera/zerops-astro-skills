# `meta-research` — Infrastructure & Anti-AMN Harness Contracts (v2.0)

Subagent delegation rules, remote MCP architecture, and `tool-guard.py` physical enforcement governing `meta-research`.

---

## 1. Subagent Delegation Architecture

Delegate exploratory or multi-source inquiries to keep the parent orchestrator context compact:
1. **When to Delegate:** Inquiries requiring `>= 3` queries, multi-library benchmarks, or external repo audits.
2. **How to Delegate:** Call `invoke_subagent(TypeName="research", Role="Epistemic Researcher")` with explicit questions, target URLs/repos, and expected comparison format.
3. **Mandatory Wait Gate:** Await subagent completion messages before drafting final F4 plans or creating Linear tickets (`tool-guard.py` enforces this wait in `PreToolUse` and `Stop`).

---

## 2. Context Window & Transport Hygiene

| Strategy | Token Footprint | Execution Path |
|---|---|---|
| **Single SDK signature lookup** | Low (< 2K tokens) | Inline `context7:query-docs` |
| **2–3 option verification** | Medium (5–10K tokens) | Inline `exa`/`tavily` + **`jina:read_url`** |
| **Deep multi-repo / RFC audit** | High (> 20K tokens) | Delegate to `invoke_subagent(TypeName="research")` |

Five primary research servers (`context7`, `exa`, `tavily`, `jina`, `firecrawl`) run via remote Streamable HTTP MCPs (`serverUrl`), consuming **0 local processes and 0 MB idle RAM** on `zcp`. Only F2 quota-fallback servers (`brave` 2.x, `duckduckgo`) run ephemeral `npx` processes on demand.

---

## 3. Physical Anti-AMN Guards (`tool-guard.py`) & Parity Sensors

1. **`search_web` Routing Gate:** Built-in `search_web` is blocked and redirected to `context7`, `exa`, `tavily`, `jina`, `firecrawl`, fallbacks `brave`/`duckduckgo`, or `research` subagents.
2. **Skill & F4 Plan Grounding Gate:** Mutating skills or writing final F4 plans requires recent live research telemetry in `/tmp/.research_grounding_state.json`.
3. **Anti-AMN Stop Gate:** Prompts requesting external research, SOTA benchmarks, or Anti-AMN checks must invoke at least one live research engine AND a verbatim primary read (F3 Jina/Context7/Fetch) during the turn.
4. **Sensors:** Verify every change with `tool-guard.py --test`, `skills-suite-validate`, and `ssot-parity-check` (`exit code 0`).

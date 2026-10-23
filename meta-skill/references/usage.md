# `meta-skill` Usage Guide: The Sovereign Skill Lifecycle

This manual documents the deterministic 7-step lifecycle for authoring, auditing, and modernizing skills in the ecosystem. It enforces epistemic grounding as a non-negotiable prerequisite before any text or code mutation.

---

## 1. Step 1: Epistemic Inflow via `research` (Queen Engine)

Before authoring a new skill or auditing an existing one:
1. **Delegation to Subagents**:
   Launch a specialized research subagent via `invoke_subagent`:
   ```python
   invoke_subagent(
       TypeName="research",
       Role="Epistemic SOTA Grounding Worker",
       Prompt="Investigate canonical 2026 specifications, breaking changes, AST contracts, and real APIs for <technology> using Exa, Context7, and Tavily. Output a verbatim research report."
   )
   ```
2. **Triangulation Across 12 Live Engines**:
   - `context7`: Official live package documentation, TypeScript definitions, and AST interfaces (`resolve-library-id`, `query-docs`).
   - `web_search_exa` & `web_fetch_exa`: Neural search across 30B+ clean pages, technical changelogs, and GitHub release notes.
   - `tavily_search` & `brave_web_search`: Multi-index web search, documentation sitemaps, and official architectural guides.
   - Jina Reader (`r.jina.ai`): Verbatim extraction of full markdown documentation, avoiding snippet clipping.
   - `firecrawl`: Deep scraping, crawling, and API mapping of modern dynamic SPAs.
3. **Artifact Compilation**:
   Save raw findings to `/var/www/artifacts/<target>_research_dossier.md` with verbatim URLs, tested code examples, and explicit version tags.

---

## 2. Step 2: Canonical Documentation via `docu` (Truth Documentalist)

Ingest raw research dossiers to establish the verified baseline:
1. **Contrast Code Against Reality**: Compare local implementation or instructions against the 2026 live APIs discovered in Step 1.
2. **Author Canonical Reference Specs**:
   - `references/usage.md`: Step-by-step verified execution workflows, curl commands, payload schemas, and practical examples.
   - `references/infra.md`: Environment variables, topology invariants, quotas, timeouts, and platform constraints.
3. **Lossless Technical Fidelity**: Capture 100% of discovered configurations, error scenarios, and recovery paths. `docu` documents the truth without structural truncation.

---

## 3. Step 3: Prompt Engineering via `cohalo` (Positive Guidance)

Translate verified technical reality into agent-executable prompt instructions:
1. **Positive Guidance Contract**: Formulate all instructions affirmatively ("Execute via...", "Emit strictly...", "Instead, do X").
2. **Closed Domains**: Define explicit, bounded options rather than open-ended choices.
3. **Elimination of Ambiguity**: Replace generic buzzwords with deterministic identifiers.

---

## 4. Step 4: Lossless Dual-RAG via `skill-improver` (AST Invariant)

Apply upstream `skill-improver` standards:
1. **Router Budget Enforcement**:
   - Measure router words: `wc -w <skill>/SKILL.md`.
   - Ensure the router is strictly $\le 480$ words / ~550 tokens.
2. **Spatial Offloading**:
   - Move deep implementation details, large code blocks, and API tables to `references/usage.md` and `references/infra.md`.
   - Keep the router as a high-density decision matrix and dispatch table.
3. **AST Preservation**: Preserve 100% of function signatures, method bodies, and error branches without deletion.

---

## 5. Step 5: Cognitive Polishing via `writing-for-agents` & `writing-skills`

Refine the ergonomic interface for LLM agents:
1. **Seam Optimization (`writing-for-agents`)**: Clarify module boundaries so agents navigate files with minimal tool calls.
2. **Evaluation Scenarios (`writing-skills`)**: Define concrete input-output test scenarios to verify skill behavior under load.

---

## 6. Step 6: Scaffolding New Skills via `skill-creator`

When creating a brand-new skill:
1. Apply clean-room directory structure:
   ```
   zerops-astro-skills/<skill-name>/
   ├── SKILL.md                  # Compact router (<= 480 words)
   └── references/
       ├── usage.md              # Workflows, step-by-step guides, payload examples
       └── infra.md              # Architectural contracts, topology, env vars
   ```
2. Verify valid YAML frontmatter (`name`, `description` with bounded triggers, `license`, `metadata`).

---

## 7. Step 7: Physical Attestation & SSoT Parity

Verify the completed work with physical sensors:
1. **Capability Sensor**: Run `skills-suite-validate` to confirm all 127+ skills pass word count, frontmatter, and AST checks.
2. **SSoT Parity**: Run `ssot-parity-check` to confirm zero drift across runtime, Drive SSoT, and GitHub repos.
3. **Persist State**: Record learnings in Linear (`linear-cli comment`) and Engram (`mem_save`).

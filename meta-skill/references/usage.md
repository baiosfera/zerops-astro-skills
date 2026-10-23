# `meta-skill` Usage Guide & Lifecycle Protocols

This guide specifies the operational procedures for authoring, auditing, and optimizing skills in the ecosystem without context pollution or information loss.

---

## 1. Scaffolding Protocol (New Skill Creation)

When bootstrapping a new sovereign skill:
1. **Identify Functional Archetype**:
   - *Framework*: Technology integration (e.g. `bun`, `astro-web`, `fastapi`).
   - *Infra*: Cloud/storage primitives (e.g. `postgresql`, `valkey`, `nats`, `zcp`).
   - *Domain*: Business engines (e.g. `checkout-funnels`, `oraculo`, `brandbook`).
   - *Cognitive*: High-leverage meta-reasoning (e.g. `docu`, `cohalo`, `planner`).
2. **Scaffold Directory Layout**:
   ```
   zerops-astro-skills/<skill-name>/
   ├── SKILL.md                  # Compact router (<= 480 words)
   └── references/
       ├── usage.md              # Workflows, step-by-step guides, payload examples
       └── infra.md              # Architectural contracts, topology, env vars
   ```
3. **Draft Minimal Router**:
   - YAML frontmatter with explicit `name`, concise `description` with bounded `Trigger:`, `license`, and `metadata`.
   - Core invariants formulated in Positive Guidance.
   - Decision gates table mapping tasks to `references/`.
   - Unified command section invoking `skills-suite-validate`.

---

## 2. Audit & Unbundling Protocol (Existing Skills)

When auditing an existing skill for trigger bloat or token excess:
1. **Trigger Audit**:
   - Purge generic buzzwords (e.g., `data`, `api`, `code`, `test`).
   - Keep only deterministic identifiers (e.g., `postgresql@18`, `pgvector`, `wompi sha256`).
2. **Router Word Budget Gate**:
   - Measure router body: `wc -w <skill>/SKILL.md`.
   - If words > 480, unbundle explanations into `references/usage.md` or `references/infra.md`.
   - The router MUST remain a pure navigation table and decision gate.
3. **Lossless Spatial Offloading**:
   - Move code snippets, API tables, and JSON schemas to `references/`.
   - Do NOT delete or truncate technical details; relocate them deterministically.
4. **Physical Verification**:
   - Run `skills-suite-validate` to confirm schema and word budgets pass exit code 0.

---

## 3. Sub-Skills Orchestration Matrix

| Intent | Primary Sub-Skill | Secondary Supporting Skills |
|---|---|---|
| New skill creation from scratch | `skill-creator` | `docu`, `writing-skills` |
| Deep unbundling to Dual-RAG | `docu` | `cohalo`, `writing-for-agents` |
| AST & code preservation audit | `skill-improver` | `cohalo` |
| Cognitive clarity & prompt audit | `writing-for-agents` | `cohalo` |
| Antigravity CLI rule priority | `agy-customizations` | `docu` |

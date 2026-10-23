# `meta-research` — Infrastructure & Harness Contracts

This document specifies the subagent delegation architecture, context window budgeting, and verification gates governing `meta-research`.

---

## 1. Subagent Delegation Architecture

Deep research inquiries involving multiple searches, extensive page reading, or exploratory comparisons consume significant context tokens:

1. **When to Delegate**:
   - Tasks requiring $\ge 3$ consecutive search queries.
   - Broad competitive surveys across multiple libraries or frameworks.
   - Parsing large technical documentation pages.
2. **How to Delegate**:
   - Use `invoke_subagent` with `TypeName: "research"`, `Role: "Epistemic Researcher"`.
   - Pass a tightly scoped prompt naming the exact technical questions, target libraries, and expected comparison table.
3. **Synthesis Delivery**:
   - The primary orchestrator reads the child agent's synthesized output, verifies the conclusions against project constraints, and communicates the result concisely to the user.

---

## 2. Context Window & Token Economy

To prevent context exhaustion during intensive research sessions:

| Research Strategy | Token Footprint | Recommended Action |
|---|---|---|
| Single API signature lookup | Low (< 2K tokens) | Execute inline with `context7 query-docs` |
| Library comparison (2-3 options) | Medium (5-10K tokens) | Execute inline with `exa` + `context7` |
| Architectural benchmark or RFC study | High (> 20K tokens) | Delegate to `invoke_subagent` with `research` |

---

## 3. Physical Verification & Anti-Drift Gates

All additions or updates to `meta-research` must satisfy the universal sensors:

1. **Universal Skill Sensor (`skills-suite-validate`)**:
   - Validates frontmatter, word count limits ($\le$ 480 words), and reference link integrity.
2. **SSoT Parity Sensor (`ssot-parity-check`)**:
   - Asserts bit-for-bit parity across `/var/www/zerops-astro-skills/`, `/var/www/.agents/skills/`, and Google Drive SSoT.

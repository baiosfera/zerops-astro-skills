# `meta-skill` Technical Architecture & Quality Standards

This document establishes the invariant technical requirements and quality gates governing skills in the ecosystem.

---

## 1. AST Preservation & Zero Mutilation Invariant

When refactoring scripts, tools, or references associated with skills:
1. **Preservation of AST Nodes**:
   - Every function, method, class, and exported type must retain its full signature and implementation.
   - Prohibited to insert placeholder comments (`// TODO`, `# pass`, `implement later`) to reduce line counts.
2. **Deterministic Syntax Verification**:
   - Python code: `python3 -m py_compile <file>`
   - Bash scripts: `bash -n <file>`
   - TypeScript/JSON: Validated via compiler or runtime lint before committing.

---

## 2. Dual-RAG Sizing & Cognitive Load Floors

| Component | Strict Threshold | Rationale |
|---|---|---|
| Router (`SKILL.md`) | $\le$ 480 words (~550 tokens) | Prevents prompt pollution; loaded into agent working context |
| Trigger Frontmatter | 3 to 10 specific keywords | Eliminates false positive activations |
| Reference Modules | Modular, focused files ($\le$ 30KB) | JIT retrieval via file reading only when activated |
| Total References Depth | Bounded to 2 hierarchy levels | Prevents multi-hop reference confusion |

---

## 3. Physical Validation Harness (Zero Checklist Theater)

Verification of skills is governed by physical assertions:
1. **Sensor Universal**: `skills-suite-validate` iterates through custom skills and asserts:
   - Presence of non-empty `SKILL.md`.
   - Valid YAML frontmatter (`name`, `description`).
   - Absence of deprecated synthetic validator scripts.
   - Word count bounds.
2. **Zero 404s Policy**:
   - Any link in a `SKILL.md` (e.g., `file:///...`) must point to an existing file in the workspace.
   - Broken links constitute a physical defect and must be resolved before git commit.

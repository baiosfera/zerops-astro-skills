# `meta-system` — Infrastructure & Harness Contracts (v2.0)

Sizing bounds, physical verification gates, and harness contracts governing system directives and context architectures under Supreme Directive v10.0.

---

## 1. Rule Sizing Thresholds & Context Budgets

Always-loaded rules consume context window on every turn. Sizing must adhere to the following ceilings:

| Component | Strict Threshold | Rationale |
|---|---|---|
| `00-SUPREME-DIRECTIVE.md` | $\le$ 50 lines / $\le$ 250 words | Lean constitutional bounds loaded on every turn |
| `AGENTS.md` (`CUSTOM` block) | $\le$ 25 lines / $\le$ 200 words | ZCP topology and CLI pointers without duplicating rules |
| Global Rules (`~/.gemini/config/rules/`) | Lean & non-overlapping | Prevents prompt dilution and instruction-budget rot |
| Disclosed Reference Documents | Modular, single-topic (`references/`) | Retrieved JIT only when an active task branches to them |

---

## 2. Physical Verification Harness (Zero Checklist Theater)

Run only the validators matching the modified scope:
1. **Skill Sensor (`skills-suite-validate`)**: Checks non-empty `SKILL.md`, valid YAML frontmatter, word budget (`<= 480` words), Python AST, Bash syntax, and zero broken `file:///` links (`--with-tests` runs per-skill test suites).
2. **SSoT Parity Sensor (`ssot-parity-check`)**: Verifies parity between workspace governance/CLIs and `zerops-astrobranding` / `zerops-astro-skills`, clean git working tree, bytecode hygiene, and zero `0zcp-123` or secret leaks.
3. **Safety Hook (`tool-guard.py`)**: Lean PreToolUse/PostToolUse physical guard (<15ms, zero prompt injections) covering secrets, upstream isolation, handover immunity, syntax pre-flight, ZCP single-node, kill/rm/find safety, pilot guard, and Engram auto-sync.

---

## 3. Strict Link Integrity Policy (Zero 404s)

Every `file:///` reference link inside a system directive or skill MUST resolve to an existing file in the workspace.

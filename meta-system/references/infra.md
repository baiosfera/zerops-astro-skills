# `meta-system` — Infrastructure & Harness Contracts

This document specifies the sizing bounds, physical verification gates, and harness constraints governing system directives and context architectures.

---

## 1. Rule Sizing Thresholds & Context Budgets

Always-loaded rules consume context window on every turn. Sizing must adhere to the following ceilings:

| Component | Strict Threshold | Rationale |
|---|---|---|
| `00-SUPREME-DIRECTIVE.md` | $\le$ 50 lines / $\le$ 600 words | High-priority constitutional bounds; loaded on every turn |
| `AGENTS.md` (Operational Contract) | $\le$ 70 lines / $\le$ 800 words | ZCP control plane, SSHFS mounting, runtime execution contracts |
| System Prompts (Agent Customizations) | Focused, task-specific | Eliminates prompt dilution and competing personas |
| Disclosed Reference Documents | Modular, single-topic ($\le$ 30KB) | Retrieved JIT only when an active task branches to them |

---

## 2. Physical Verification Harness (Zero Checklist Theater)

System rules must be backed by automated physical checks:

1. **Universal Sensor (`skills-suite-validate`)**:
   - Asserts non-empty `SKILL.md` for all meta-skills.
   - Verifies valid YAML frontmatter and word count budgets.
   - Ensures zero broken internal links (`file:///...`).
2. **SSoT Parity Sensor (`ssot-parity-check`)**:
   - Asserts bit-for-bit parity between local rules (`/var/www/.agents/rules/`), Git upstream, and Google Drive SSoT.
   - Verifies bytecode hygiene (`sys.dont_write_bytecode=True`, zero `__pycache__`).
   - Asserts that no sensitive tokens or plaintext secrets are committed to rules.
3. **Execution Sensor (`tool-guard.py`)**:
   - Enforces pre-tool hooks that block unvalidated edits to rules or scripts.
   - Enforces exit-0 testing before transitioning tasks to Done.

---

## 3. Strict Link Integrity Policy (Zero 404s)

Every reference link within a system directive or rule MUST resolve to a physical file in the workspace:
- Correct canonical pattern: `[`link-text`](file:///absolute/path/to/file.md)`
- Relative links or unresolved anchors (`404 Not Found`) are classified as physical defects and block task completion.

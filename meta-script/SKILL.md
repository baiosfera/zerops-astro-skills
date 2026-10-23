---
name: meta-script
description: "Trigger: meta-script, tool-guard, python script, bash script, platform scripts, harness engineering, pre-tool hook, exit 0 validation. Master Platform Scripts, Security Hooks & Physical Harness Orchestrator."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.0"
---

# `meta-script` — Master Platform Scripts, Hooks & Physical Harness Orchestrator (v1.0)

## Activation Contract
Activate when authoring, modifying, auditing, or refactoring operational bash/python scripts in `/scripts/`, `.bin/`, security hooks (`tool-guard.py`), or physical harness sensors. Exclusively governs EXECUTABLE PLATFORM SCRIPTS, HOOKS, AND SYSTEM SENSORS.

## Hard Rules & Positive Guidance
- **Domain Boundary (Platform Scripts Only)**: Operate strictly on executable scripts (`.sh`, `.py`), CLI tools in `.bin/`, and security hooks (`tool-guard.py`). Direct markdown skills to `meta-skill`, application features to `codecraft`, and directives to `meta-system`.
- **CoHaLo Engineering Invariant**: Write robust code without arbitrary token limits. Encapsulate state, eliminate mutable globals, and propagate errors deterministically without silent catch blocks (`except: pass` or `2>/dev/null`).
- **Physical AST Syntax Gates**: Execute physical syntax verification before presenting or committing code:
  * Python: `python3 -m py_compile <path>` (exit code 0 required).
  * Bash: `bash -n <path>` (exit code 0 required).
- **Pre-Mutation Snapshot**: Create an automated preventive backup (`cp <file> <file>.bak`) before editing critical operational scripts or security hooks.
- **Two Sovereign Sensors Invariant**: Centralize all capability and drift validation strictly in `skills-suite-validate` and `ssot-parity-check`. Prohibit synthetic redundant sensors.
- **Physical Attestation Before Assertion**: Claim task completion strictly after test suites pass with exit code 0 (`tool-guard.py --test` and sensor runs).

## Active Sub-Skills Dispatch Table

| Focus | Sub-Skill | Canonical SSoT Pointer | Responsibility |
|---|---|---|---|
| **Harness & Loops** | `cohalo` | [`cohalo`](file:///var/www/.agents/skills/cohalo/SKILL.md) | CoHaLo Engineering, AST verification, deterministic loops |
| **Craftsmanship** | `codecraft` | [`codecraft`](file:///var/www/.agents/skills/codecraft/SKILL.md) | ODD lifecycle, deep modules, surgical TDD, atomic commits |
| **Surgical Discipline** | `karpathy-guidelines` | [`karpathy-guidelines`](file:///var/www/.agents/skills/karpathy-guidelines/SKILL.md) | Minimal surgical diffs, zero overcomplication |
| **Physical Proof** | `verification-before-completion` | [`verification-before-completion`](file:///var/www/.agents/skills/verification-before-completion/SKILL.md) | Evidence before assertions, exit code 0 validation |

## Decision Gates

| Challenge | Action / Protocol | Reference |
|---|---|---|
| Script Scaffolding | Author modular deep scripts with error handling | [`references/usage.md#1-script-authoring`](file:///var/www/.agents/skills/meta-script/references/usage.md) |
| Security Hook Hardening | Intercept in PreToolUse, validate AST and backups | [`references/usage.md#2-hook-architecture`](file:///var/www/.agents/skills/meta-script/references/usage.md) |
| Pre-Mutation Safety | Enforce backup snapshots and safe rollback | [`references/usage.md#3-safe-mutation`](file:///var/www/.agents/skills/meta-script/references/usage.md) |
| Test Suite Execution | Execute physical tests and self-test harness | [`references/infra.md#1-testing-harness`](file:///var/www/.agents/skills/meta-script/references/infra.md) |
| Physical Certification | Execute universal validation and SSoT anti-drift sensors | `skills-suite-validate` · `ssot-parity-check` |

## Commands
```bash
# Verify Python script AST syntax
python3 -m py_compile <script.py>

# Verify Bash script syntax
bash -n <script.sh>

# Execute tool-guard test suite
python3 /var/www/zerops-astrobranding/scripts/hooks/tool-guard.py --test

# Execute universal physical validation sensor
skills-suite-validate

# Verify SSoT parity across Drive, Git, and active scripts
ssot-parity-check
```

## References
- [`references/usage.md`](file:///var/www/.agents/skills/meta-script/references/usage.md) · [`references/infra.md`](file:///var/www/.agents/skills/meta-script/references/infra.md)

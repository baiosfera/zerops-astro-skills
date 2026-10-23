# `meta-script` — Usage & Implementation Guide

This guide establishes the concrete procedures for authoring, auditing, and hardening operational scripts and security hooks under Supreme Directive v8.5 and CoHaLo Engineering standards.

---

## 1. Script Authoring & Hardening Protocol

When creating or modifying operational scripts in `/scripts/` or `.bin/`:

1. **Deterministic Shebang & Strict Flags**:
   - Bash: `#!/usr/bin/env bash` with `set -euo pipefail`.
   - Python: `#!/usr/bin/env python3` with `sys.dont_write_bytecode = True`.
2. **Bounded State & Zero Mutable Globals**:
   - Encapsulate execution inside functions (e.g. `main()`).
   - Pass configuration via explicit arguments or environment variables.
   - Prohibit global mutable dictionaries or arrays that create state leakages.
3. **Deterministic Error Handling**:
   - Catch specific exceptions in Python; log error causes before exiting.
   - Never suppress errors with bare `except: pass` or `2>/dev/null` unless explicitly testing expected error branches.
   - Use standardized exit codes (0 for success, non-zero for failure).

---

## 2. Security Hook Architecture (`tool-guard.py`)

Security hooks protect container integrity and prevent catastrophic regressions:

1. **PreToolUse Interception**:
   - Intercept destructive commands (e.g., recursive deletes, unauthorized kills).
   - Enforce router word budgets ($\le$ 480 words) on `SKILL.md` before writes.
   - Enforce physical syntax gates (`python3 -m py_compile`, `bash -n`) before saving code.
2. **Pre-Mutation Automatic Snapshot**:
   - Before mutating any script or hook, create a timestamped backup in `/var/www/bak/` or a local `.bak`.
   - Enable instant atomic rollback if syntax validation fails post-edit.
3. **PostToolUse & SSoT Triad Mirror**:
   - Maintain real-time mirror synchronization between `/var/www/zerops-astro-skills/`, `/var/www/.agents/skills/`, and Google Drive SSoT.

---

## 3. Safe Mutation & Self-Test Harness

Every script modification must follow the 4-phase safety loop:

1. **Snapshot**: Capture pre-edit state (`cp script.py script.py.bak`).
2. **Surgical Edit**: Apply changes adhering to `karpathy-guidelines` (minimal necessary diff).
3. **Syntax Assertion**:
   - Python: `python3 -m py_compile script.py` (assert exit code 0).
   - Bash: `bash -n script.sh` (assert exit code 0).
4. **Self-Test Execution**:
   - Run the script's automated test suite: `python3 <script> --test`.
   - Confirm exit code 0 before deleting or rotating the backup snapshot.

# `meta-script` — Infrastructure & Harness Contracts

This document specifies the execution environments, performance bounds, and physical verification gates governing platform scripts and security hooks.

---

## 1. Testing Harness & Execution Ceilings

Operational scripts must run reliably within bounded resource and time budgets:

| Metric / Parameter | Strict Threshold | Purpose |
|---|---|---|
| Command Execution Timeout | $\le$ 10 seconds (`timeout 10s`) | Prevents hanging commands from exhausting thread pools |
| WaitMsBeforeAsync | 10000 ms (synchronous commands) | Ensures clean synchronous returns for short-lived utilities |
| Self-Test Runner | `python3 <script> --test` | Deterministic verification of internal assertion contracts |
| Memory Footprint | Bounded in-process execution | Prevents container memory exhaustion on single-node ZCP |

---

## 2. Two Sovereign Sensors Verification Gate

Validation of operational scripts and hooks is centralized exclusively in the two sovereign sensors:

1. **`skills-suite-validate`**:
   - Asserts non-empty `SKILL.md` and valid YAML frontmatter for `meta-script`.
   - Verifies router word budget ($\le$ 480 words).
   - Validates zero broken links (`file:///...`).
2. **`ssot-parity-check`**:
   - Asserts bit-for-bit parity between local scripts in `/var/www/zerops-astrobranding/scripts/` and Google Drive SSoT.
   - Verifies Python AST syntax and bytecode hygiene (zero `__pycache__` residue).
   - Verifies CLI symlink availability in `/usr/local/bin` and `/var/www/.bin`.

---

## 3. Tool-Guard Self-Test Invariant

Any modification to `tool-guard.py` must pass its built-in self-test suite:
```bash
python3 /var/www/zerops-astrobranding/scripts/hooks/tool-guard.py --test
```
A non-zero exit code indicates an invariant breach and mandates immediate rollback.

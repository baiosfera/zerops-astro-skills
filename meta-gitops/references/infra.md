# `meta-gitops` — Infrastructure & Harness Contracts

This document specifies the verification gates, safety hooks, and repository topologies governing `meta-gitops`.

---

## 1. SSoT Parity Gate (`ssot-parity-check`)

Before any push to `origin/main` or deployment branch, the workspace must satisfy the universal anti-drift invariant:

```bash
# Must return exit code 0 with zero detected discrepancies
ssot-parity-check
```

### Verification Checks

1. **Governance Rules**: Bit-for-bit parity between `/var/www/.agents/rules/` and Google Drive SSoT (`/var/www/baiosfera/0ZEROPS-AGY/0zcp-123/.agents/rules/`).
2. **Core Scripts**: Executable integrity in `/var/www/zerops-astrobranding/scripts/` and `/usr/local/bin/`.
3. **Custom Skills**: Parity across all 74 sovereign custom skills in `/var/www/zerops-astro-skills/` and Drive SSoT.
4. **Git Status**: Working tree clean and up to date with `origin/main`.

---

## 2. Git Guardrails & Pre-Tool Interception

The platform security harness (`tool-guard.py` and `git-guardrails-claude-code`) intercepts destructive Git operations in real time:

| Blocked Action | Risk Prevented | Safe Alternative |
|---|---|---|
| `git reset --hard` | Unrecoverable loss of local changes | Create branch snapshot before testing |
| `git push --force` | Overwriting remote commit history | Rebase or chained PR |
| `git clean -fd` | Deletion of untracked assets or uncommitted work | Review `git status` explicitly |
| Direct main edit | Split-brain between dev and production | Feature branches and pull requests |

---

## 3. Judgment Day Dual-Review Gate (`judgment-day`)

For high-risk architectural or production releases:

1. **Blind Review Lenses**: Evaluate the PR against two independent axes:
   - *Standards Lens*: Does the code satisfy architectural invariants, typing, and safety standards?
   - *Spec Lens*: Does the code completely satisfy the acceptance criteria of the Linear issue?
2. **Exit Criteria**: Both lenses must return approval without blocking defects before merging.

---
name: meta-gitops
description: "Trigger: meta-gitops, gitops, work-unit-commits, conventional commits, atomic delivery, ssot-parity, branch-pr, chained-pr, zero live edits, ghcicd. Master GitOps, Atomic Delivery & SSoT Synchronization Orchestrator."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.0"
---

# `meta-gitops` — Master GitOps, Atomic Delivery & SSoT Parity Orchestrator (v1.0)

## Activation Contract
Activate when planning commits, opening pull requests, configuring CI/CD pipelines, enforcing commit standards, or synchronizing repositories with Google Drive SSoT. Exclusively governs GITOPS DELIVERY, WORK-UNIT COMMITS, REPOSITORY PARITY, AND BRANCH STRATEGY.

## Hard Rules & Positive Guidance
- **Zero AI Attribution in Commits**: Formulate all commits strictly as Conventional Commits (`feat:`, `fix:`, `refactor:`, `chore:`). Prohibit `Co-Authored-By` or AI attribution trailers.
- **Atomic Work Units**: Scope commits and PRs into small, self-contained units ($\le$ 400 lines). Break large initiatives into stacked, reviewable branches (`chained-pr`).
- **Physical SSoT Parity Before Push**: Execute `ssot-parity-check` and assert exit code 0 before pushing changes to `origin/main` or deployment branches.
- **Zero Live Edits Invariant**: Direct all production and preview code changes through Git repositories (`ghcicd`). Runtime containers mount repositories; never perform untracked live modifications.
- **Destructive Command Guardrails**: Guard against destructive operations (`git reset --hard`, `git push --force`, `rm -rf /`). Respect platform hooks and verification gates.

## Active Sub-Skills Dispatch Table

| Focus | Sub-Skill | Canonical SSoT Pointer | Responsibility |
|---|---|---|---|
| **GitOps Delivery** | `ghcicd` | [`ghcicd`](file:///var/www/.agents/skills/ghcicd/SKILL.md) | GitHub Actions pipelines, Zerops deploys, zero live edits |
| **Atomic Commits** | `work-unit-commits` | [`work-unit-commits`](file:///var/www/.agents/skills/work-unit-commits/SKILL.md) | Conventional commits, work unit splitting, clean commit messages |
| **Branch Management** | `branch-pr` | [`branch-pr`](file:///var/www/.agents/skills/branch-pr/SKILL.md) | Issue-first branches, clean PR bodies, review readiness |
| **Stacked PR Slicing** | `chained-pr` | [`chained-pr`](file:///var/www/.agents/skills/chained-pr/SKILL.md) | Slicing large changes ($\ge$ 400 lines) into chained review units |
| **Adversarial Review** | `judgment-day` | [`judgment-day`](file:///var/www/.agents/skills/judgment-day/SKILL.md) | Blind dual-lens review before production merges |
| **Safety Guardrails** | `git-guardrails-claude-code` | [`git-guardrails-claude-code`](file:///var/www/.agents/skills/git-guardrails-claude-code/SKILL.md) | Blocking destructive git commands in execution environments |

## Decision Gates

| Challenge | Action / Protocol | Reference |
|---|---|---|
| Large Change ($\ge$ 400 lines) | Slice into stacked branches with independent test passes | [`references/usage.md#1-chained-prs`](file:///var/www/.agents/skills/meta-gitops/references/usage.md) |
| Commit Authoring | Format with Conventional Commits, zero AI trailers | [`references/usage.md#2-conventional-commits`](file:///var/www/.agents/skills/meta-gitops/references/usage.md) |
| Pre-Push Certification | Verify bit-for-bit parity and test suites (exit code 0) | [`references/infra.md#1-ssot-parity-gate`](file:///var/www/.agents/skills/meta-gitops/references/infra.md) |
| Dual-Review Approval | Run blind dual review before final delivery gate | [`references/infra.md#2-judgment-day-gate`](file:///var/www/.agents/skills/meta-gitops/references/infra.md) |

## Commands
```bash
# Verify SSoT parity across Drive, Git, and active services
ssot-parity-check

# Execute universal skill validation
skills-suite-validate

# Push with conventional commit
git commit -m "feat(scope): concise description" && git push origin main
```

## References
- [`references/usage.md`](file:///var/www/.agents/skills/meta-gitops/references/usage.md) · [`references/infra.md`](file:///var/www/.agents/skills/meta-gitops/references/infra.md)

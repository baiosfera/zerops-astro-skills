---
name: ghcicd
description: "Trigger: ghcicd, git push, zerops deploy, github actions zerops, zeropsio/actions, zcli push, gh auth login, stage branch, production deploy, ci cd pipeline. Sovereign GitOps CI/CD Delivery Engine & Zero Live Edits Protocol in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "3.2"
---

# `ghcicd` — Sovereign GitOps CI/CD & Dev/Prod Delivery Engine (v3.2)

## Activation Contract
Activate for CI/CD pipelines, GitHub Actions (`zeropsio/actions@v1.0.2`), `gh` CLI, Cloudflare API, ephemeral workspaces, or multi-environment delivery in Zerops.

## Hard Rules & Positive Guidance
- **Commit Discipline & Anti-Commit-Spam**: Local commits track atomic steps under Conventional Commits. Batched pushes or feature branches merged via **Squash & Merge** (`gh pr merge --squash --delete-branch`). Avoid micro-pushes to `main`.
- **Zero Live Edits on Production**: Production runs immutable releases exclusively via GitHub Actions or release tags (`v*`). Never edit live production code directly on `<app_domain>`.
- **Sovereign Dev/Prod Delivery (Option B Priority)**: The canonical default workflow couples iterative development in Zerops (`/var/www/{hostname}` with subdomains, hot-reload, zero commit spam) with automated, immutable production deploys via GitHub Actions (`zeropsio/actions@v1.0.2`) on push to `main` connected to Cloudflare SSL Full Strict.
- **Ephemeral & Disposable Workspaces ($0 Cost)**: The development workspace (`webdev`) is 100% disposable. With SSoT in GitHub (`main`) and production deployed, `webdev` can be stopped or deleted when not in active use for zero cost, and re-provisioned in seconds from `main` when needed.
- **Optional Staging Layer**: Staging (`<service>-stage`) remains supported as an optional layer for formal QA, without acting as a mandatory gate for Dev/Prod delivery. Base chasis templates never execute direct deploy workflows.
- **Agnostic Delivery Shield**: Disconnect Zerops GUI webhooks when using GitHub Actions to avoid duplicate builds.
- **Kebab-Case CI/CD Contract**: `zeropsio/actions@v1.0.2` strictly requires `access-token` and `service-id` in kebab-case.
- **Autonomous Provisioning**: Manage secrets via `gh secret set ZEROPS_TOKEN` and `gh secret set ZEROPS_PROD_SERVICE_ID`. Configure DNS and SSL Full Strict (`value: strict`) via Cloudflare API v4.
- **Fractal CoHaLo**: Enforce bounded execution (`timeout 10s`), wait limits (`WaitMsBeforeAsync: 10000`), and sensors (`gh auth status` / `zerops_verify`).
- **Zero Deletion Invariant**: Lossless specifications in [`references/usage.md`](file:///var/www/.agents/skills/ghcicd/references/usage.md) and [`references/infra.md`](file:///var/www/.agents/skills/ghcicd/references/infra.md).

## Decision Gates

| Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| Anti-Spam & 4D | 4D Git, Squash & Merge, gh vs Actions | [`references/usage.md#0-modelo-mental-4d-de-git-y-disciplina-anti-commit-spam`](file:///var/www/.agents/skills/ghcicd/references/usage.md) |
| Dev/Prod & Ephemeral | Option B Default & Ephemeral Workspaces | [`references/usage.md#c-arquitectura-canónica-de-ambientes-en-zerops-opción-b-devprod-y-staging-opcional`](file:///var/www/.agents/skills/ghcicd/references/usage.md) |
| Secrets & DNS | gh secret set and Cloudflare API v4 | [`references/usage.md#d-aprovisionamiento-autónomo-de-secretos-en-github-gh-secret-set`](file:///var/www/.agents/skills/ghcicd/references/usage.md) |
| 4D CI/CD Matrix | Actions vs Webhook vs zcli vs dev_server | [`references/usage.md#1-4d-comparative-architectural-matrix-deployment-methods-in-zerops`](file:///var/www/.agents/skills/ghcicd/references/usage.md) |
| Workflows | Production, staging & release workflows | [`references/usage.md#3-github-actions-workflows-with-zeropsioactionsv102`](file:///var/www/.agents/skills/ghcicd/references/usage.md) |
| Secrets & Ports | ZEROPS_TOKEN, Service IDs & Ports | [`references/infra.md`](file:///var/www/.agents/skills/ghcicd/references/infra.md) |
| Physical Validation | Deterministic validation sensor | [`scripts/ghcicd-validate.sh`](file:///var/www/.agents/skills/ghcicd/scripts/ghcicd-validate.sh) |

## References
- [`references/usage.md`](file:///var/www/.agents/skills/ghcicd/references/usage.md) · [`references/infra.md`](file:///var/www/.agents/skills/ghcicd/references/infra.md)
- [`assets/ghcicd_production_recipes.json`](file:///var/www/.agents/skills/ghcicd/assets/ghcicd_production_recipes.json) · [`scripts/ghcicd-validate.sh`](file:///var/www/.agents/skills/ghcicd/scripts/ghcicd-validate.sh)

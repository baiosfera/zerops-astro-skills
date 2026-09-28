---
name: ghcicd
description: "Trigger: ghcicd, git push, zerops deploy, github actions zerops, zeropsio/actions, zcli push, gh auth login, stage branch, production deploy, ci cd pipeline. Sovereign GitOps CI/CD Delivery Engine, 3-Environment Promotion & Zero Live Edits Protocol in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "3.0"
---

# `ghcicd` — Sovereign GitOps CI/CD & 3-Environment Delivery Engine (v3.0)

## Activation Contract
Activate for CI/CD pipelines, GitHub Actions (`zeropsio/actions@v1.0.2`), Git CLI operations (`gh auth login`, `gh pr`, `gh secret set`), Cloudflare API automation, or multi-environment workflows in Zerops.

## Hard Rules & Positive Guidance
- **Commit Discipline & Anti-Commit-Spam (MANDATORY)**: Local commits track atomic steps under Conventional Commits in `.git/`. Batched pushes or feature branches merged via **Squash & Merge** (`gh pr merge --squash --delete-branch`). No direct micro-pushes to `main`.
- **Zero Live Edits on Production (MANDATORY)**: NEVER edit production files on `<app_domain>`. Production runs immutable releases via GitHub Actions or tags (`v*`).
- **3-Environment Lifecycle**: Supports Multi-Service isolation (`<service>-stage` vs `<service>-prod`) and **Single-Runtime Host Router** (single container mapping `<zerops_subdomain>`, `<staging_domain>`, `<app_domain>` to port 3000, saving >70% RAM).
- **Agnostic Delivery Shield**: Disconnect Zerops GUI webhooks when using GitHub Actions.
- **Kebab-Case CI/CD Contract**: `zeropsio/actions@v1.0.2` strictly requires `access-token` and `service-id` in kebab-case.
- **Autonomous Provisioning**: Manage secrets via `gh secret set ZEROPS_TOKEN` and `gh secret set ZEROPS_SERVICE_ID`. Configure DNS and SSL Full Strict (`value: strict`) via Cloudflare API v4.
- **Fractal CoHaLo**: Enforce bounded execution (`timeout 10s`), wait limits (`WaitMsBeforeAsync: 10000`), and sensors (`gh auth status` / `zerops_verify`).
- **Zero Deletion Invariant**: Full lossless specifications in [`references/usage.md`](file:///var/www/.agents/skills/ghcicd/references/usage.md) and [`references/infra.md`](file:///var/www/.agents/skills/ghcicd/references/infra.md).

## Decision Gates

| Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| Anti-Spam & 4D | 4D Git, Squash & Merge, gh vs Actions | [`references/usage.md#0-modelo-mental-4d-de-git-y-disciplina-anti-commit-spam`](file:///var/www/.agents/skills/ghcicd/references/usage.md) |
| Host Routing | Single-Runtime Router vs Multi-Service | [`references/usage.md#c-enrutamiento-de-dominios-en-zerops-multi-contenedor-vs-runtime-único-por-host`](file:///var/www/.agents/skills/ghcicd/references/usage.md) |
| Secrets & DNS | gh secret set and Cloudflare API v4 | [`references/usage.md#d-aprovisionamiento-autónomo-de-secretos-en-github-gh-secret-set`](file:///var/www/.agents/skills/ghcicd/references/usage.md) |
| 4D CI/CD Matrix | Actions vs Webhook vs zcli vs dev_server | [`references/usage.md#1-4d-comparative-architectural-matrix-deployment-methods-in-zerops`](file:///var/www/.agents/skills/ghcicd/references/usage.md) |
| Git & gh Auth | Authenticate PAT & git identity | [`references/usage.md#2-git--gh-cli-authentication-in-zcp-container`](file:///var/www/.agents/skills/ghcicd/references/usage.md) |
| Workflows | Production, staging & release workflows | [`references/usage.md#3-github-actions-workflows-with-zeropsioactionsv102`](file:///var/www/.agents/skills/ghcicd/references/usage.md) |
| Port & URLs | Service ports & preview URLs | [`references/infra.md#1-complete-service-port--url-catalog`](file:///var/www/.agents/skills/ghcicd/references/infra.md) |
| Secrets Config | ZEROPS_TOKEN & Service IDs | [`references/infra.md#2-secret-management-zerops_token--service-ids`](file:///var/www/.agents/skills/ghcicd/references/infra.md) |
| Production Recipes | Workflow recipes catalog | [`assets/ghcicd_production_recipes.json`](file:///var/www/.agents/skills/ghcicd/assets/ghcicd_production_recipes.json) |
| Validation Sensor | Deterministic validation sensor | [`scripts/ghcicd-validate.sh`](file:///var/www/.agents/skills/ghcicd/scripts/ghcicd-validate.sh) |

## References
- [`references/usage.md`](file:///var/www/.agents/skills/ghcicd/references/usage.md) — 4D matrix, anti-spam runbook, gh secrets, Cloudflare API, and workflows.
- [`references/infra.md`](file:///var/www/.agents/skills/ghcicd/references/infra.md) — Port & URL catalog, ZEROPS_TOKEN secret management, and CoHaLo harness.
- [`assets/ghcicd_production_recipes.json`](file:///var/www/.agents/skills/ghcicd/assets/ghcicd_production_recipes.json) — Production GitHub Actions workflow recipes.
- [`scripts/ghcicd-validate.sh`](file:///var/www/.agents/skills/ghcicd/scripts/ghcicd-validate.sh) — Deterministic quality & token validation sensor.

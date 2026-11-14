---
name: ghcicd
description: "Trigger: ghcicd, git push, zerops deploy, github actions zerops, zeropsio/actions, zcli push, gh auth login, webdev subdomain, production deploy, ci cd pipeline. Sovereign GitOps CI/CD Delivery Engine & Zero Live Edits Protocol in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "3.3"
---

# `ghcicd` — Sovereign GitOps CI/CD & Dev/Prod Delivery Engine (v3.3)

## Activation Contract
Activate for CI/CD pipelines, GitHub Actions (`zeropsio/actions@v1.0.2`), `gh` CLI, Cloudflare API, ephemeral workspaces, or multi-environment delivery in Zerops.

## Hard Rules & Positive Guidance
- **Commit Discipline & Anti-Commit-Spam**: Use Conventional Commits locally and batch pushes or **Squash & Merge** (`gh pr merge --squash --delete-branch`). Avoid micro-pushes to `main`.
- **Zero Live Edits on Production**: Production runs immutable releases exclusively via GitHub Actions or release tags (`v*`). Never edit live production code directly.
- **Namespace Sovereignty (Upstream vs Client)**: `baiosfera/*` is reserved for upstream platform repos (`zerops-astrobranding`, `zerops-astro-skills`, `template-astro-web`, `runtime-*`). Client apps live in `https://github.com/<marca>/<app>` using tokens from `/var/www/baiosfera/0ZEROPS-AGY/users-apis/<Marca>/<marca>-keys.md` (`main` -> `webprod`, `dev` -> `webdev`).
- **Sovereign Dev/Prod Delivery (Option B)**: Develop iteratively in Zerops (`/var/www/{hostname}`) and deploy immutable builds to production via GitHub Actions (`zeropsio/actions@v1.0.2`) behind Cloudflare SSL Full Strict.
- **Ephemeral Dev Workspaces**: With SSoT in GitHub (`main`), `webdev` is disposable ($0 when stopped/deleted) and re-provisions from `main`.
- **Agnostic Delivery & Kebab-Case**: Disconnect Zerops GUI webhooks when using GitHub Actions. `zeropsio/actions@v1.0.2` requires `access-token` and `service-id` in kebab-case.
- **Autonomous Provisioning & CoHaLo**: Set `ZEROPS_TOKEN` / `ZEROPS_PROD_SERVICE_ID` via `gh secret set`, configure DNS/SSL Strict via Cloudflare API v4, and enforce `timeout 10s` + `zerops_verify`.
- **References**: Full specifications in [`references/usage.md`](file:///var/www/.agents/skills/ghcicd/references/usage.md) and [`references/infra.md`](file:///var/www/.agents/skills/ghcicd/references/infra.md).

## Decision Gates

| Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| Anti-Spam & 4D | 4D Git, Squash & Merge, gh vs Actions | [`references/usage.md#0-modelo-mental-4d-de-git-y-disciplina-anti-commit-spam`](file:///var/www/.agents/skills/ghcicd/references/usage.md) |
| Dev/Prod & Ephemeral | Option B Default & Ephemeral Workspaces | [`references/usage.md#c-arquitectura-canónica-de-ambientes-en-zerops-opción-b-devprod-y-staging-opcional`](file:///var/www/.agents/skills/ghcicd/references/usage.md) |
| Secrets & DNS | gh secret set and Cloudflare API v4 | [`references/usage.md#d-aprovisionamiento-autónomo-de-secretos-en-github-gh-secret-set`](file:///var/www/.agents/skills/ghcicd/references/usage.md) |
| 4D CI/CD Matrix | Actions vs Webhook vs zcli vs dev_server | [`references/usage.md#1-4d-comparative-architectural-matrix-deployment-methods-in-zerops`](file:///var/www/.agents/skills/ghcicd/references/usage.md) |
| Workflows | Production, staging & release workflows | [`references/usage.md#3-github-actions-workflows-with-zeropsioactionsv102`](file:///var/www/.agents/skills/ghcicd/references/usage.md) |
| Secrets & Ports | ZEROPS_TOKEN, Service IDs & Ports | [`references/infra.md`](file:///var/www/.agents/skills/ghcicd/references/infra.md) |
| Physical Validation | Deterministic validation sensor | [`scripts/ghcicd-validate.sh``skills-suite-validate` |

## References
- [`references/usage.md`](file:///var/www/.agents/skills/ghcicd/references/usage.md) · [`references/infra.md`](file:///var/www/.agents/skills/ghcicd/references/infra.md)
- [`assets/ghcicd_production_recipes.json`](file:///var/www/.agents/skills/ghcicd/assets/ghcicd_production_recipes.json) · [`scripts/ghcicd-validate.sh``skills-suite-validate`

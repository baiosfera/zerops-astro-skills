---
name: zcp
description: "Trigger: zcp, scaffold zerops, native runtime, deploy import.yaml, configure zerops.yaml, provision managed db, zerops_*, lxc, local-storage, run.volume, postgresql, valkey. Master Zerops Platform & Workload Orchestrator with 22 MCP tools, Incus LXC, PostgreSQL 18 & Valkey 7.2."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "6.2"
---

# `zcp` — Zerops Platform & Infrastructure Master Suite (v6.2)

## Activation Contract
Activate when provisioning or managing native runtimes (Astro, Directus, FastAPI), data engines (PostgreSQL 18, Valkey 7.2, NATS 2.12), local storage volumes (`local-storage:single@1`), Cloudflare ingress, or operating the 22 Zerops MCP tools.

## Hard Rules
- **Clarification Gate (HARD STOP)**: Confirm before provisioning:
  1. **Hostname**: Lowercase alphanumeric (`[a-z0-9]`), max 25 chars, **no hyphens**.
  2. **Base OS**: `os: ubuntu` (glibc) vs `os: alpine` (musl minimal).
  3. **Managed DB Variant & Profile**: `:single` vs `:ha` (immutable) and profile (`oltp-hobby`, `oltp-staging`, `oltp-production`, `hobby`, `staging`, `production`).
- **Zero-Boilerplate Autoscaling Law**: Zerops Incus LXC runtimes scale dynamically by default without requiring `verticalAutoscaling` or manual `min`/`max` boundaries in `import.yaml`. Keep manifests clean (`hostname`, `type`). `verticalAutoscaling` is reserved strictly for advanced overrides (`cpuMode: DEDICATED`, `minRam` spike buffers).
- **Custom Domain**: Enforce Cloudflare **Full (Strict)** SSL/TLS mode.
- **MCP vs SSH Demarcation**: Platform lifecycle, envs, logs, and dev-servers use `zerops_*` MCP tools. SSH is for build/test commands.
- **Local Storage**: Declare `type: local-storage:single@1` in `import.yaml`. Mount in `zerops.yaml` via `run.volume: {hostname: <storageHostname>, mountPath: /path, readOnly: false}`. Never declare legacy `mount:` in `import.yaml`.
- **Anti Self-Shadow Trap**: Never self-reference variables (`API_URL: ${API_URL}`); use distinct source names (`DB_HOST: ${db_hostname}`).
- **Fractal CoHaLo**: Enforce hygiene (`timeout 10s`), wait (`WaitMsBeforeAsync: 10000`), zero orphans (`manage_task action="kill"`), sensor (`zerops_discover`).
- **Zero Deletion**: See [`references/usage.md`](file:///var/www/.agents/skills/zcp/references/usage.md) and [`references/infra.md`](file:///var/www/.agents/skills/zcp/references/infra.md).

## Decision Gates

| Task / Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| 22 MCP Tools & Schemas | Full MCP catalogue & workflow contracts | [`references/usage.md#2-comprehensive-catalogue-of-the-22-zerops-mcp-tools-zerops_`](file:///var/www/.agents/skills/zcp/references/usage.md) |
| Operational Demarcation | MCP vs SSH/Bash rules and boundaries | [`references/usage.md#3-operational-demarcation-mcp-tools-vs-ssh--bash`](file:///var/www/.agents/skills/zcp/references/usage.md) |
| Canonical import.yaml | Clean multi-service manifest with Bun, Node, Python & DBs | [`references/usage.md#4-canonical-importyaml-manifest-specification`](file:///var/www/.agents/skills/zcp/references/usage.md) |
| Canonical zerops.yaml | Dev keepalive and production rolling release | [`references/usage.md#5-canonical-zeropsyaml-lifecycle-recipes`](file:///var/www/.agents/skills/zcp/references/usage.md) |
| Autoscaling Architecture | Autonomous scale & clean manifest rules | [`references/infra.md#1-autonomous-elastic-autoscaling--clean-manifest-architecture`](file:///var/www/.agents/skills/zcp/references/infra.md) |
| Managed DB Profiles | Sizing profiles for PostgreSQL 18, Valkey 7.2 & NATS | [`references/infra.md#2-managed-database--message-broker-profiles`](file:///var/www/.agents/skills/zcp/references/infra.md) |
| POSIX Local Storage | Kernel POSIX volume mount (run.volume) & SQLite WAL | [`references/infra.md#3-local-storage-architecture--single-kernel-posix-engine`](file:///var/www/.agents/skills/zcp/references/infra.md) |
| Import Template Asset | Declarative multi-service import YAML manifest | [`assets/import_template.yaml`](file:///var/www/.agents/skills/zcp/assets/import_template.yaml) |
| Lifecycle Template Asset | Production zerops.yaml template for runtimes | [`assets/zerops_template.yaml`](file:///var/www/.agents/skills/zcp/assets/zerops_template.yaml) |
| Production Recipes JSON | Manifests and scaling recipe indexes | [`assets/zcp_production_recipes.json`](file:///var/www/.agents/skills/zcp/assets/zcp_production_recipes.json) |
| Physical Validation Sensor | Attest skill structure, frontmatter, tokens & links | [`scripts/zcp-validate.sh`](file:///var/www/.agents/skills/zcp/scripts/zcp-validate.sh) |

## Execution Steps
1. Execute `zerops_discover` to discover live topology.
2. Formulate and validate `import.yaml` or `zerops.yaml` manifests.
3. Provision or import services via `zerops_workflow` / `zerops_import`.
4. Supervise development servers with `zerops_dev_server`.
5. Attest container health with `zerops_verify` and `zerops_logs`.

## Output Contract
- Scalable, resilient multi-service topology deployed in Zerops Incus LXC.
- Validated elastic autoscaling, kernel-attached persistent volumes, and passing physical sensors.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/zcp/references/usage.md) — 4D matrix, 22 MCP tools catalogue, import/zerops schemas, and 5 production patterns.
- [`references/infra.md`](file:///var/www/.agents/skills/zcp/references/infra.md) — Autoscaling mathematics, DB profiles, Local Storage, and CoHaLo harness.
- [`assets/zcp_production_recipes.json`](file:///var/www/.agents/skills/zcp/assets/zcp_production_recipes.json) — Production import manifests and scaling recipes.
- [`assets/import_template.yaml`](file:///var/www/.agents/skills/zcp/assets/import_template.yaml) — Production import manifest template.
- [`assets/zerops_template.yaml`](file:///var/www/.agents/skills/zcp/assets/zerops_template.yaml) — Production lifecycle YAML template.
- [`scripts/zcp-validate.sh`](file:///var/www/.agents/skills/zcp/scripts/zcp-validate.sh) — Deterministic quality & token validation sensor.

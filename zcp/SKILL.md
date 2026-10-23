---
name: zcp
description: "Trigger: zcp, scaffold zerops, native runtime, deploy import.yaml, configure zerops.yaml, provision managed db, zerops_*, lxc, local-storage, run.volume, postgresql, valkey. Master Zerops Platform & Workload Orchestrator with 22 MCP tools, Incus LXC, PostgreSQL 18 & Valkey 7.2."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "6.5"
---

# `zcp` — Zerops Platform & Infrastructure Master Suite (v6.5)

## Activation Contract
Provisioning or managing runtimes (Astro, Directus, FastAPI), data engines (PostgreSQL 18, Valkey 7.2, NATS 2.12), local storage (`local-storage:single@1`), Cloudflare ingress, or operating the 22 Zerops MCP tools.

## Core Directives & Invariants
- **Clarification Gate**: Verify hostname (`[a-z0-9]`, $\le$ 25 chars), base OS (`os: ubuntu` vs `os: alpine`), and database variant (`:single` vs `:ha`) before provisioning.
- **Frugal & Elastic Autoscaling**: Use `cpuMode: SHARED`, `minContainers: 1`, `maxContainers: 2`. Omit `minCpu`, `maxCpu`, `minRam`, `maxRam` to let Zerops manage native elasticity (0.125–48 GB RAM). Configure dual buffers: `minFreeRamGB: 0.25` and `minFreeRamPercent: 10`. Mutate in real-time with `zerops_scale`.
- **MCP vs SSH Demarcation**: Platform lifecycle, environment variables, logs, and dev servers run via `zerops_*` MCP tools. SSH is reserved for build and testing inside `/var/www`.
- **POSIX Local Storage**: Declare `type: local-storage:single@1` in `import.yaml`. Mount in `zerops.yaml` via `run.volume: { hostname: <storageHostname>, mountPath: /path, readOnly: false }`.
- **Secret Hygiene**: Avoid self-shadowing variables (`API_URL: ${API_URL}`); use distinct names (`DB_HOST: ${db_hostname}`).

## Decision Gates & References

| Objective | Protocol | Reference |
|---|---|---|
| 22 MCP Tools | Platform operations and demarcation rules | [`usage.md`](file:///var/www/zerops-astro-skills/zcp/references/usage.md) |
| Manifest Blueprints | Production `import.yaml` and `zerops.yaml` recipes | [`usage.md`](file:///var/www/zerops-astro-skills/zcp/references/usage.md) |
| Autoscaling & Storage | Dual-RAM buffers, DB profiles, POSIX volumes | [`infra.md`](file:///var/www/zerops-astro-skills/zcp/references/infra.md) |
| Templates & Recipes | Multi-service templates and JSON index | [`import_template.yaml`](file:///var/www/zerops-astro-skills/zcp/assets/import_template.yaml) / [`zerops_template.yaml`](file:///var/www/zerops-astro-skills/zcp/assets/zerops_template.yaml) |
| Validation Sensor | Attest skill structure, tokens and links | [`zcp-validate.sh``skills-suite-validate` |

## Output Contract
Multi-service Incus LXC topology with frugal autoscaling, kernel-level POSIX storage, and green physical sensors.

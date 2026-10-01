---
name: zcp
description: "Trigger: zcp, scaffold zerops, native runtime, deploy import.yaml, configure zerops.yaml, provision managed db, zerops_*, lxc, local-storage, run.volume, postgresql, valkey. Master Zerops Platform & Workload Orchestrator with 22 MCP tools, Incus LXC, PostgreSQL 18 & Valkey 7.2."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "6.4"
---

# `zcp` — Zerops Platform & Infrastructure Master Suite (v6.4)

## Activation Contract
Activate when provisioning or managing runtimes (Astro, Directus, FastAPI), data engines (PostgreSQL 18, Valkey 7.2, NATS 2.12), local storage (`local-storage:single@1`), Cloudflare ingress, or operating the 22 Zerops MCP tools.

## Hard Rules
- **Clarification Gate (HARD STOP)**: Confirm before provisioning:
  1. **Hostname**: Lowercase alphanumeric (`[a-z0-9]`), max 25 chars, no hyphens.
  2. **Base OS**: `os: ubuntu` (glibc) vs `os: alpine` (musl minimal).
  3. **Managed DB Variant & Profile**: `:single` vs `:ha` (immutable) and profile (`oltp-hobby`, `oltp-staging`, `oltp-production`, `hobby`, `staging`, `production`).
- **Ley de Autoescalado Frugal & Elástico**:
  - *Arranque Frugal*: `cpuMode: SHARED` obligatorio (cero `DEDICATED` en arranque), `startCpuCoreCount: 1` o no declarado, `minContainers: 1`, `maxContainers: 2` como seguro de saturación.
  - *Límites Omitidos*: Omitir `minCpu`, `maxCpu`, `minRam`, `maxRam` en manifiestos y GUI. Zerops gestiona la elasticidad nativa (0.125-48 GB RAM, 1-8 vCPUs) sin límites artificiales ni OOMKilled por techos bajos.
  - *Colchón Dual Dinámico*: `minFreeRamGB: 0.25` y `minFreeRamPercent: 10` para prevenir OOM sin inflar reposo.
  - *Herencia Modular Obligatoria*: Toda composición modular o importación ad-hoc DEBE incluir `verticalAutoscaling` completo.
  - *Mutación en Caliente*: Ajustar en runtime con `zerops_scale` sin reiniciar contenedores.
  - *Circuit Breaker Financiero*: `maxRam` (ej. 4 u 8 GB) opcional contra memory leaks desatendidos.
- **Custom Domain**: Enforce Cloudflare Full (Strict) SSL/TLS.
- **MCP vs SSH Demarcation**: Platform lifecycle, envs, logs y dev-servers vía `zerops_*`. SSH solo para build/test en `/var/www`.
- **Local Storage**: `type: local-storage:single@1` en `import.yaml`. Montar en `zerops.yaml` vía `run.volume: {hostname: <storageHostname>, mountPath: /path, readOnly: false}`. Prohibido `mount:` en `import.yaml`.
- **Anti Self-Shadow**: Jamás autorreferenciar variables (`API_URL: ${API_URL}`); usar nombres distintos (`DB_HOST: ${db_hostname}`).
- **Fractal CoHaLo**: `timeout 10s`, `WaitMsBeforeAsync: 10000`, matar procesos huérfanos (`manage_task action="kill"`), sensor `zerops_discover`.
- **Zero Deletion**: Ver [`references/usage.md`](file:///var/www/.agents/skills/zcp/references/usage.md) e [`references/infra.md`](file:///var/www/.agents/skills/zcp/references/infra.md).

## Decision Gates

| Task / Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| 22 MCP Tools & Demarcation | Operations catalogue and boundaries | [`references/usage.md`](file:///var/www/.agents/skills/zcp/references/usage.md) |
| Canonical Manifests | `import.yaml` and `zerops.yaml` recipes | [`references/usage.md`](file:///var/www/.agents/skills/zcp/references/usage.md) |
| Frugal Autoscaling & DBs | Dual-RAM thresholds, DB sizing, POSIX storage | [`references/infra.md`](file:///var/www/.agents/skills/zcp/references/infra.md) |
| Import & Lifecycle Templates | Multi-service templates and JSON index | [`assets/import_template.yaml`](file:///var/www/.agents/skills/zcp/assets/import_template.yaml) / [`assets/zerops_template.yaml`](file:///var/www/.agents/skills/zcp/assets/zerops_template.yaml) / [`assets/zcp_production_recipes.json`](file:///var/www/.agents/skills/zcp/assets/zcp_production_recipes.json) |
| Physical Validation Sensor | Attest skill structure, tokens and links | [`scripts/zcp-validate.sh`](file:///var/www/.agents/skills/zcp/scripts/zcp-validate.sh) |

## Execution Steps
1. Descubrir topología con `zerops_discover`.
2. Formular manifiestos `import.yaml` y `zerops.yaml`.
3. Provisionar con `zerops_workflow` o `zerops_import`.
4. Supervisar dev servers con `zerops_dev_server`.
5. Atestar salud con `zerops_verify` y `zerops_logs`.

## Output Contract
- Topología multi-servicio en Incus LXC con autoscaling frugal y resiliente.
- Volúmenes POSIX a nivel de kernel y sensores físicos en verde.

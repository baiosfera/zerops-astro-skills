---
name: dckr
description: "Trigger: deploy docker container, docker-compose stack, webtop desktop, custom dockerfile, docker vm zerops. Deploy and manage Docker containers directly on Zerops VM."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.2"
---

# DCKR — Dedicated Docker VM & Container Orchestration (v1.2)

## Activation Contract
Activate when deploying, configuring, or running Docker containers, Docker Compose stacks, or containerized GUI applications (WebTop, databases, custom Dockerfiles) on Zerops dedicated VMs (`type: docker@...`).

## Hard Rules
- **Fixed Compute Invariant**: Docker runs in a dedicated QEMU/Incus VM. Always configure fixed resources (`minCpu == maxCpu` and `minRam == maxRam`); validate via `zcp-validate scaling docker`.
- **Host Networking (`network_mode: host`)**: Obligatory for all Docker Compose services to bind ports to the VM interface for Zerops L7 routing.
- **Direct Binary Start**: `run.start` must execute directly (`start: docker compose -f /var/www/docker-compose.yml up`); prohibit shell `cd` chains.
- **Local Storage Volume Mount**: Attach persistent volumes in `zerops.yaml` under `run.volume: {hostname: <storageHostname>, mountPath: /mnt/<storageHostname>}` and map into containers via Compose `volumes:` (`/mnt/<storageHostname>/<service>/data:/data`).

## Decision Gates

| Task / Workload | Strategy / Standard | Reference / Asset |
|---|---|---|
| Compose & Custom Dockerfiles | Developer Guide & Anti-Patterns | [`references/usage.md`](file:///var/www/.agents/skills/dckr/references/usage.md) |
| VM Hardware & Persistent Volumes | VM Specs, Ports & Volume Configuration | [`references/infra.md`](file:///var/www/.agents/skills/dckr/references/infra.md) |
| Standard Compose Template | Production `docker-compose.yml` | [`assets/docker_compose_template.yml`](file:///var/www/.agents/skills/dckr/assets/docker_compose_template.yml) |
| WebTop Desktop Template | Ubuntu-XFCE + Chrome + Rclone | [`assets/Dockerfile.webtop`](file:///var/www/.agents/skills/dckr/assets/Dockerfile.webtop) |

## Execution Steps
1. Determine required vCPU, RAM, and storage volumes (`run.volume: {hostname: storage, mountPath: /mnt/storage}`).
2. Validate scaling parameters using `zcp-validate scaling docker <cpu> <cpu> <ram> <ram>`.
3. Generate `Dockerfile` and `docker-compose.yml` with `network_mode: host`.
4. Configure `zerops.yaml` with `prepareCommands` (installing `docker-cli-compose`) and persistent volume mount.
5. Deploy service and verify container logs.

## Output Contract
- Verified `docker-compose.yml`, `Dockerfile`, and `zerops.yaml` manifests.
- Active Docker VM service status, ports, and storage volume mappings.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/dckr/references/usage.md) — Docker Compose architecture, WebTop configuration, and anti-patterns.
- [`references/infra.md`](file:///var/www/.agents/skills/dckr/references/infra.md) — QEMU/Incus VM specifications, fixed scaling rules, and persistent volume integration.
- [`assets/docker_compose_template.yml`](file:///var/www/.agents/skills/dckr/assets/docker_compose_template.yml) — Production Docker Compose template.
- [`assets/Dockerfile.webtop`](file:///var/www/.agents/skills/dckr/assets/Dockerfile.webtop) — Custom WebTop desktop Dockerfile.

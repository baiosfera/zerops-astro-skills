---
name: local-storage
description: "Trigger: local-storage, storage, local disk, run.volume, persistent volume, sqlite zerops, posix storage, mount /mnt/, local-storage:single@1. Architect, mount, optimize, and operate Zerops Local Storage persistent volumes with native POSIX single-kernel semantics."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.6"
---

# Local Storage — Persistent Disk Volume & POSIX Engine (v1.6)

## Activation Contract
Activate whenever provisioning, configuring, or mounting Zerops Local Storage (`type: local-storage:single@1`), shared disk mounts, persistent SQLite databases, upload directories, or application caches requiring true POSIX filesystem semantics.

## Hard Rules & Positive Guidance
- **Native POSIX Single-Kernel Semantics**: Local Storage operates with single-kernel POSIX filesystem locks (`fcntl`, `flock`), making it safe for SQLite, embedded databases, and file caches within the container.
- **Mount Syntax in zerops.yaml**: Mount volumes inside the application service using:
  ```yaml
  run:
    volume:
      hostname: <storageHostname>
      mountPath: /mnt/<storageHostname>
  ```
- **Shared Storage Single-Node Rule**: To share a volume across multiple services, all mounting services must be pinned to `minContainers: 1, maxContainers: 1` to prevent split-brain filesystem corruption.
- **Disk Expansion Law**: Allocated storage expands automatically with data growth and never shrinks.
- **Ephemeral Container Boundary**: Data written outside the mounted volume path (`/mnt/...`) is ephemeral and wiped upon new deployments. All durable state must reside inside the mount path.

## Decision Matrix

| Storage Objective | Recommended Pattern | Reference |
|---|---|---|
| SQLite & Key-Value DBs | Local Storage mount with fcntl locks | [`references/usage.md#sqlite-storage`](file:///var/www/.agents/skills/local-storage/references/usage.md) |
| App Uploads & Caches | Volume mount at /mnt/storage | [`references/usage.md#uploads-cache`](file:///var/www/.agents/skills/local-storage/references/usage.md) |
| Shared Volume Topology | Single-node shared volume architecture | [`references/infra.md#shared-volume`](file:///var/www/.agents/skills/local-storage/references/infra.md) |
| Backup & Snapshot Strategy | Automated volume backup workflows | [`references/infra.md#backups`](file:///var/www/.agents/skills/local-storage/references/infra.md) |

## Critical Workflows
1. Provision `local-storage:single@1` in `import.yaml`.
2. Declare `run.volume` mount path in the consumer service's `zerops.yaml`.
3. Verify mount availability inside container (`df -h /mnt/<storageHostname>`).

## References
- [`references/usage.md`](file:///var/www/.agents/skills/local-storage/references/usage.md) — POSIX filesystem patterns, SQLite on Zerops, mount configurations, and performance tuning.
- [`references/infra.md`](file:///var/www/.agents/skills/local-storage/references/infra.md) — Sizing profiles, multi-service shared storage topology, backup automation, and safety invariants.

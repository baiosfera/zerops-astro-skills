---
name: local-storage
description: "Trigger: local-storage, storage, local disk, run.volume, persistent volume, sqlite zerops, posix storage, mount /mnt/, local-storage:single@1. Architect, mount, optimize, and operate Zerops Local Storage persistent volumes with native POSIX single-kernel semantics."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.4"
  cohalo-standard: "6.7"
---

# Local Storage — Persistent Disk Volume & Single-Kernel POSIX Engine (v1.4)

## Activation Contract
Activate when architecting, configuring, mounting, optimizing, or operating Zerops Local Storage (`local-storage:single@1`) persistent disk volumes across runtime services, embedded database workloads (SQLite, Prometheus TSDB), control-plane staging mounts, or migrating from legacy Shared Storage.

## Hard Rules & Critical Invariants
1. **Exclusive `run.volume` Gate**: Local storage volumes MUST be mounted exclusively in `zerops.yaml` under `run.volume` (`{hostname, mountPath, readOnly}`). Declaring `mount:` in `import.yaml` or `run.mount` is invalid.
2. **Single-Kernel POSIX Semantics**: Advisory locks (`flock`, `fcntl`), memory mapping (`mmap`), `inotify`, and atomic renames operate natively across containers via shared host kernel.
3. **Embedded Database & SQLite Safe**: SQLite WAL mode is fully supported. Coordinate writes via a single writer container; mount `readOnly: true` on readers.
4. **Co-Location Law**: All containers mounting the same volume are scheduled onto the same physical machine. Horizontal scale is bounded by host capacity.
5. **Native Ownership**: Mount point is owned natively by `zerops:zerops` (UID/GID 1000). No `chmod` workarounds needed.
6. **Atomic Database Backups**: Live `.tar.gz` captures require quiet I/O. For SQLite, run `sqlite3 <db> ".backup <dest>"` via `run.crontab` (`allContainers: false`).
7. **Volume Deletion Blocker**: Local Storage cannot be deleted while connected runtimes declare `run.volume`. Remove `run.volume` and redeploy first.
8. **ZCP Control-Plane Mount Law**: When mounting to `/var/www/{hostname}` in ZCP, bind `/data` to `/var/www` on storage (`mount --bind /data /var/www` in `/etc/fstab`). Automate via `scripts/localstorage-mount-zcp.sh`.
9. **Subdirectory Permission Bootstrap**: While the mount root is owned natively by the platform, new application subdirectories on the persistent volume (e.g. `/mnt/localstorage/<service>`) must be provisioned in `prepareCommands` via `sudo mkdir -p <dir> && sudo chown -R zerops:zerops <dir>` to prevent unprivileged runtime crashes during initial database creation.

## Decision Matrix

| Task / Domain | Technical Pattern | Reference / Asset |
|---|---|---|
| Runtime Volume Mounting & MountPath | `run.volume: {hostname, mountPath, readOnly}` | [`references/usage.md`](references/usage.md) |
| Architecture & Single-Kernel Semantics | POSIX locks, mmap coherence, co-location, vs S3 | [`references/infra.md`](references/infra.md) |
| SQLite WAL & Consistent Backup Pattern | Single-writer + `readOnly` + `sqlite3 .backup` cron | [`references/usage.md#3-sqlite-wal-mode--consistent-database-backups`](references/usage.md) |
| Control-Plane Mount in ZCP (`/var/www/{host}`) | Bind mount (`/data` $\leftrightarrow$ `/var/www`) + SSHFS | [`scripts/localstorage-mount-zcp.sh`](scripts/localstorage-mount-zcp.sh) |
| Migration from Deprecated Shared Storage | Zero-downtime migration to `local-storage:single@1` | [`references/infra.md#4-migration-from-deprecated-shared-storage`](references/infra.md) |
| Multi-Service Import Manifest Template | `local-storage:single@1` + Consumer Runtimes | [`assets/import_template.yaml`](assets/import_template.yaml) |
| Runtime Lifecycle & Volume Configuration | `run.volume` declaration in `zerops.yaml` | [`assets/zerops_template.yaml`](assets/zerops_template.yaml) |

## References
- [`references/usage.md`](references/usage.md) — Local storage mount flows, `run.volume` options, ZCP protocol, SQLite backup patterns, directory hierarchies, and diagnostic CLI tools.
- [`references/infra.md`](references/infra.md) — Architecture, POSIX locking, mmap coherence, co-location, and comparisons.
- [`scripts/localstorage-mount-zcp.sh`](scripts/localstorage-mount-zcp.sh) — Deterministic CLI utility to automate storage bind mounting and ZCP control-plane SSHFS mounts.
- [`assets/import_template.yaml`](assets/import_template.yaml) — Production-ready `import.yaml` storage manifest.
- [`assets/zerops_template.yaml`](assets/zerops_template.yaml) — Production runtime `zerops.yaml` with `run.volume` configuration.

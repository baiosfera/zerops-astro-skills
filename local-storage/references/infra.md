# Local Storage Infrastructure & Single-Kernel Architecture Manual (v1.3)

> **SSoT Technical Specification:** Deep infrastructure architecture for Zerops Local Storage (`local-storage:single@1`), single-kernel POSIX semantics (`flock`, `fcntl`, `mmap`), co-location scheduling, embedded database safety (SQLite WAL), failure modes, and comparison against Object Storage (MinIO S3) and deprecated Shared Storage (SeaweedFS).

---

## 1. Local Storage Architecture

A Zerops Local Storage service consists of:
1. **Persistent Block Volume**: A persistent disk volume managed natively by the host hypervisor. It exists independently of any container and survives container restarts and upgrades.
2. **Maintenance Container**: A lightweight Alpine Linux container with the persistent volume mounted natively at `/data`. It provides:
   - Service hostname resolution within the project network.
   - Direct SSH and Web Shell access for maintenance and file inspection.
   - Execution environment for automated daily `.tar.gz` backups.
   - *Note:* It never runs user application code.
3. **Consumer Runtimes**: Runtime services connect to the volume by declaring `run.volume` in `zerops.yaml`. The volume is attached natively into the consumer container at container initialization.
4. **ZCP Control-Plane Bridge**: Because the maintenance container mounts the persistent block volume at `/data` while ZCP remote mounts target `/var/www`, a persistent kernel bind mount (`mount --bind /data /var/www` in `/etc/fstab`) exposes the volume directly to ZCP control-plane mounts (`/var/www/{hostname}`) via SSHFS without intermediate copying.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     PHYSICAL HOST MACHINE (CO-LOCATED)                  │
│                                                                         │
│  ┌──────────────────────┐   ┌──────────────────┐   ┌─────────────────┐  │
│  │ Local Storage Service│   │ Runtime: backend │   │ Runtime: worker │  │
│  │ (/data maintenance)  │   │ (/mnt/storage)   │   │ (/mnt/storage)  │  │
│  └──────────┬───────────┘   └────────┬─────────┘   └────────┬────────┘  │
│             │                        │                      │           │
│             └────────────────────────┴──────────────────────┘           │
│                                      │                                  │
│                 Shared Host Kernel (Direct POSIX I/O)                   │
│                                      │                                  │
│                 ┌────────────────────┴───────────────────┐              │
│                 │   Persistent Disk Volume (/data)      │              │
│                 └────────────────────────────────────────┘              │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Filesystem Semantics & Single-Kernel POSIX Engine

Because all connected containers run on the same physical host and share one kernel:
1. **Advisory Locking Across Containers**: `flock` and `fcntl` locks are enforced globally by the shared kernel. A lock held in one container is immediately visible and respected in all other containers mounting the volume.
2. **Memory-Mapped Coherence (`mmap`)**: Memory-mapped files remain coherent across all containers. This makes SQLite WAL (Write-Ahead Logging) mode 100% safe, as WAL coordinates through shared-memory (`-shm`) mmap files.
3. **Unified Page Cache**: Writes in one container are immediately visible to reads in another container without close-to-open consistency lag or network latency round trips.
4. **Atomic Operations**: Atomic renames (`renameat2`) and `O_APPEND` operations behave identically to a local disk.
5. **Inotify Propagation**: File system event watchers in one container receive real-time notifications for modifications made by other containers.

---

## 3. Storage Decision Matrix

| Criterion | Local Storage (`local-storage:single@1`) | Object Storage (`object-storage`) | Shared Storage (*Deprecated*) |
|---|---|---|---|
| **Access Interface** | POSIX Filesystem (`/mnt/<hostname>/`) | S3 REST API (`PUT/GET/DELETE`) | POSIX FUSE (`/mnt/<hostname>/`) |
| **Protocol** | Direct Kernel Mount / Local Disk I/O | HTTP/HTTPS TCP (`${storage_apiUrl}`) | FUSE over Network (SeaweedFS) |
| **Locking (`flock`/`fcntl`)** | Full Cross-Container Enforced | No Locking (API Level) | Container-Local Only (Unsafe) |
| **mmap & SQLite WAL** | **Safe & Coherent** | Unsupported | **Unsafe (Data Corruption)** |
| **Throughput / Latency** | Ultra-low local NVMe/SSD Latency | High Throughput HTTP Streaming | Network FUSE Roundtrips |
| **High Availability** | Single-Machine (Non-HA) | HA Clustered | HA Clustered (SeaweedFS) |
| **Public CDN Ingress** | Not Directly Exposed to CDN | Native Zerops CDN (`${storageCdnUrl}`) | Not Exposed |
| **Ideal Workloads** | SQLite, Prometheus, shared app state, caches | User uploads, media, backups, public assets | *Migrate to Local Storage or S3* |

---

## 4. Co-Location & Failure Behavior

1. **Co-Location Law**: Every container of every runtime service that mounts a Local Storage volume is scheduled onto the exact physical server holding the volume.
2. **Horizontal Scaling Ceiling**: Horizontal scaling of connected runtimes is limited by the free CPU/RAM capacity of that single physical machine.
3. **Hardware Failure & Maintenance**: If the physical host fails or undergoes maintenance, Zerops migrates the volume to a healthy host; all connected runtime services go through a stop $\to$ move $\to$ start cycle.
4. **Automated Backups**: Zerops generates daily compressed `.tar.gz` archives of the `/data` volume. Point-in-time snapshot backups are planned.

---

## 5. Migration from Deprecated Shared Storage

To migrate data from a deprecated Shared Storage service (hostname: `volume`) to a new Local Storage service (hostname: `storage`):
1. **Stop Writers**: Stop application services writing to the legacy storage.
2. **Provision Migrator Service**: Provision `local-storage:single@1` and a temporary Ubuntu container with both storages mounted:
   - Local storage via `run.volume.hostname: storage` in `zerops.yaml`.
   - Legacy shared storage via `startCommands: [sudo zsc shared-storage mount volume]`.
3. **Copy Data**: Execute `cp -a /mnt/volume/. /mnt/storage/` (or `rsync -avP`).
4. **Update Consumers**: Update consuming services' `zerops.yaml` to point to `storage` via `run.volume`.
5. **Decommission**: Delete the temporary migrator and legacy shared storage.

---

## 6. Execution Harness & Governance (Fractal CoHaLo)

- **Timeouts**: All CLI inspections executed with `timeout 10s`.
- **Synchronous Wait**: `WaitMsBeforeAsync: 10000`.
- **Zero Orphaned Tasks**: Terminate lingering background processes via `manage_task action="kill"`.
- **Physical Sensors**: File write probes `test -w /mnt/<storage>` and `zerops_discover`.

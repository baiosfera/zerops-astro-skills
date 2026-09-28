# Zerops Infrastructure, Autoscaling Architecture & Storage Engine (v6.2)

This manual provides detailed engineering specifications for autonomous vertical autoscaling, real platform limits, managed database sizing profiles, POSIX shared storage architecture, and the Fractal CoHaLo operational harness in Zerops.

---

## 1. Autonomous Elastic Autoscaling & Clean Manifest Architecture

Zerops Incus LXC runtimes scale dynamically by default without container restarts. The platform continuously monitors cgroup metrics and adjusts resources automatically.

### A. Zero-Boilerplate Standard (No Min/Max Required)
In modern Zerops (2026), service manifests in `import.yaml` **do not require defining `verticalAutoscaling` or manual `min`/`max` boundaries**:
* **Autonomous Platform Defaults**: When `verticalAutoscaling` is omitted, Zerops automatically enables elastic scaling across native resource boundaries:
  * **CPU**: Scales dynamically up to 8 cores per container (default `SHARED` mode, burst step up to 4 cores / 20s).
  * **RAM**: Scales dynamically up to 48 GB per container (granularity 0.125 GB, burst step up to 32 GB / 10s).
  * **Disk**: Scales dynamically up to 250 GB per container (persistent, grow-only, step up to 128 GB).
  * **Horizontal Scaling**: 1 to 10 containers (up to 80 cores and 480 GB RAM aggregate compute).
* **Pay-per-Use Billing Reality**: Zerops meters CPU, RAM, and disk by actual sub-second utilization, NOT allocated headroom. Setting arbitrary low ceilings (`maxRam: 4.0`, `maxCpu: 4`) does not reduce costs; it only creates artificial bottlenecks and risks `OOMKilled` crashes on legitimate traffic surges.

### B. When to Use `verticalAutoscaling` (Advanced Overrides Only)
The `verticalAutoscaling` block is optional and reserved strictly for intentional, advanced overrides:
1. **Dedicated CPU Allocation**: Enforce `cpuMode: DEDICATED` for CPU-intensive, zero-jitter production workloads.
2. **Startup Spike Buffering**: Setting `minRam` (e.g. `minRam: 1.0` or `minRam: 2.0`) when heavy frameworks (`npm install`, Rust/Go builds, JVM warming) spike faster than the 10-20s autoscaler reaction window.
3. **Fixed Compute Pinning**: Setting `min == max` (e.g. `minRam: 4, maxRam: 4`) to intentionally pin resources and disable autoscaling for deterministic benchmarking.
4. **Dual Threshold Tuning (Optional)**:
   * Scaling evaluates free RAM: $\text{Scale Up} = (\text{Free RAM} < \text{minFreeRamGB}) \lor (\text{Free RAM \%} < \text{minFreeRamPercent})$.
   * Defaults: `minFreeRamGB: 0.0625` (64 MB), `minFreeRamPercent: 0%` (disabled). Whichever grants more buffer wins.

---

## 2. Managed Database & Message Broker Profiles

Zerops managed databases require explicit sizing profiles during import or scaling:

| Managed Service | Single Node (`:single`) | High Availability (`:ha`) | Available Profiles |
|---|---|---|---|
| **PostgreSQL 18** | `postgresql:single@18` | `postgresql:ha@18` | `oltp-hobby`, `oltp-staging`, `oltp-production` |
| **Valkey 7.2** | `valkey:single@7.2` | `valkey:ha@7.2` | `hobby`, `staging`, `production` |
| **NATS 2.12** | `nats:single@2.12` | `nats:ha@2.12` | `hobby`, `staging`, `production` |
| **Local Storage** | `local-storage:single@1` | — (Co-located disk) | Persistent disk volume (`minDisk` to `maxDisk`) |

> **Immutability Invariant:** A database service created as `:single` cannot be converted to `:ha` in-place; upgrading to High Availability requires the `launch-production` workflow or data migration to a new `:ha` service.

---

## 3. Local Storage Architecture & Single-Kernel POSIX Engine

Zerops Local Storage (`local-storage:single@1`) provides persistent disk volumes attached directly at kernel level:

1. **Service Provisioning**: Declare `type: local-storage:single@1` in `import.yaml`.
2. **Runtime Volume Mounting**: Attach the volume in consumer services via `zerops.yaml`:
   ```yaml
   run:
     volume:
       hostname: storage
       mountPath: /mnt/storage
       readOnly: false
   ```
3. **Single-Kernel POSIX Semantics**: Enforces advisory locks (`flock`, `fcntl`), unified page cache, and coherent `mmap` across co-located containers, making embedded databases (SQLite WAL mode, Prometheus TSDB) 100% safe.
4. **Ownership**: Native `zerops:zerops` (UID 1000) ownership on the mount path. No FUSE workarounds required.
5. **Strict Prohibition**: Legacy `mount:` in `import.yaml` or `run.mount` in `zerops.yaml` are obsolete and must not be used.

---

## 4. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

All operations with `zcp` must strictly comply with the Fractal CoHaLo standard:

* **Bounded Timeouts**: All CLI probes and platform checks must use explicit timeouts (`timeout 10s ...`).
* **Synchronous Wait Enforcement**: For CLI commands and status verifications, specify `WaitMsBeforeAsync: 10000`.
* **Zero Orphan Tasks**: Terminate all lingering dev servers or monitoring tasks using `manage_task action="kill"`.
* **Physical Sensor Attestation**:
  * Discover sensor: `zerops_discover` returns `ACTIVE` status for critical services.
  * Verify sensor: `zerops_verify` returns `pass` or `info` on all container endpoints.
* **Circuit Breaker Policy**: If a build fails twice in `zerops_events`, halt execution, examine build logs via `zerops_logs`, and adjust `prepareCommands` or dependencies before retrying.

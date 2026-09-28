# Zerops Infrastructure, Autoscaling Architecture & Storage Engine (v6.3)

This manual provides detailed engineering specifications for autonomous vertical autoscaling, real platform limits, managed database sizing profiles, POSIX shared storage architecture, and the Fractal CoHaLo operational harness in Zerops.

---

## 1. Autonomous Elastic Autoscaling & Clean Manifest Architecture

Zerops Incus LXC runtimes scale dynamically by default without container restarts. The platform continuously monitors cgroup metrics and adjusts allocated compute and memory automatically.

### A. Canonical Frugal & Resilient Autoscaling Recipe (`frugal-elastic`)
The recommended architecture for production runtimes balances absolute minimal baseline spend with resilient spike handling:

```yaml
minContainers: 1
maxContainers: 2
verticalAutoscaling:
  cpuMode: SHARED
  minFreeRamGB: 0.25
  minFreeRamPercent: 10
```

- **`cpuMode: SHARED` (Mandatory Frugal Core)**: Runtimes start on shared multi-tenant cores (up to 10 tenants per physical core). Performance scales smoothly from 1/10 to 10/10 of a core based on demand without paying for dedicated compute during idle or low-traffic periods. Dedicated CPU (`cpuMode: DEDICATED`) is never required at startup.
- **`startCpuCoreCount: 1` (or omitted)**: Allocates a baseline of 1 vCPU at startup, avoiding over-provisioning.
- **`minContainers: 1`, `maxContainers: 2` (Saturation Insurance)**: Baseline is kept at a single container to minimize cost. Capping `maxContainers: 2` provides an automated redundancy and load-distribution shield if the primary container approaches vertical saturation under sudden surges.

### B. The Clean Manifest Pattern (Omission of minCpu, maxCpu, minRam, maxRam)
In modern Zerops, clean service manifests in `import.yaml` intentionally omit explicit resource boundary keys (`minCpu`, `maxCpu`, `minRam`, `maxRam`):

* **Native Elasticity Across Full Platform Envelope**: When these keys are omitted, the corresponding input boxes in the Zerops GUI dashboard remain completely unconstrained (empty defaults). Zerops automatically orchestrates vertical scaling across its entire native hardware range:
  * **RAM**: Elastic scaling from **0.125 GB (128 MB)** up to **48 GB** per container (granularity 0.125 GB, burst step up to 32 GB / 10s).
  * **CPU**: Elastic scaling from **1 core** up to **8 vCPUs** per container (burst step up to 4 cores / 20s).
  * **Disk**: Elastic scaling up to **250 GB** per container (persistent, grow-only, step up to 128 GB).
* **Pay-per-Use Billing Reality**: Zerops bills strictly by actual sub-second utilization, NOT allocated ceiling headroom. Setting artificial ceilings (`maxRam: 2.0`, `maxCpu: 2`) does **not** save money during normal operations; it only creates artificial choke points and triggers catastrophic `OOMKilled` crashes on legitimate traffic surges.

### C. Dual-RAM Threshold Mathematics & Dynamic Buffer Policy
Zerops evaluates memory pressure every **10 seconds**. Two independent thresholds control when vertical RAM scale-up triggers, governed by the invariant that **whichever threshold provides the larger free memory buffer wins**:

$$\text{Required Free Buffer} = \max\left(\text{minFreeRamGB}, \; \frac{\text{minFreeRamPercent}}{100} \times \text{Granted RAM}\right)$$

Scale-up triggers immediately upon a single 10s measurement where:
$$\text{Free RAM} < \text{Required Free Buffer}$$

1. **Absolute Threshold (`minFreeRamGB: 0.25`)**: Guarantees a minimum fixed cushion of 256 MB of unallocated RAM at all times. At low memory consumption (e.g. 512 MB to 1 GB granted), 10% is only 51-100 MB; the absolute 256 MB threshold takes precedence, preventing abrupt out-of-memory errors caused by small application allocations.
2. **Dynamic Percentage Threshold (`minFreeRamPercent: 10`)**: Adapts proportionally to overall memory grant. As granted memory scales up to 4 GB, 8 GB, or 16 GB, the buffer automatically expands to 400 MB, 800 MB, and 1.6 GB respectively. This accommodates large transient request bursts and preserves Linux kernel page cache without latency degradation.
3. **Comparison with Platform Defaults**:
   * *Platform Defaults*: `minFreeRamGB: 0.0625` (64 MB), `minFreeRamPercent: 0%` (disabled).
   * *Frugal Resilient Standard*: `minFreeRamGB: 0.25` (256 MB), `minFreeRamPercent: 10%`. Quadruples the base safety buffer and adds dynamic expansion, completely eliminating micro-OOMs while remaining ultra-frugal at rest.

### D. Financial Circuit Breaker Pattern (`maxRam`)
While resource boundaries should normally remain unconstrained, `maxRam` can be deployed as an intentional **Financial Circuit Breaker**:
- **Risk Profile**: Long-running background workers, unvetted third-party libraries, or experimental services susceptible to uncontrolled heap memory leaks.
- **Circuit Breaker Action**: Declaring `maxRam: 4` or `maxRam: 8` sets an immutable ceiling. If a runaway leak occurs while unmonitored, the container will restart upon hitting the limit rather than silently expanding memory to 48 GB and causing unexpected billing spikes.

### E. Hot Runtime Scaling via `zerops_scale`
All scaling thresholds and boundaries can be mutated on live, running containers without downtime or container restarts using the `zerops_scale` MCP tool:

```bash
# Apply Frugal Resilient dual-RAM threshold to live container
zerops_scale serviceHostname="zcp" minFreeRamGB=0.25 minFreeRamPercent=10

# Adjust horizontal safety boundaries and apply financial circuit breaker
zerops_scale serviceHostname="appdev" minContainers=1 maxContainers=2 maxRam=8
```

Scale changes are registered immediately by the Zerops control plane and take effect within the next 10-second metric evaluation cycle.

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

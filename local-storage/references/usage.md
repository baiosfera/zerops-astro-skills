# Local Storage Operations & Developer Reference Manual (v1.3)

> **SSoT Developer Reference:** Step-by-step integration guide for Zerops Local Storage, `run.volume` syntax in `zerops.yaml`, mountPath options, readOnly protection, multi-service directory hierarchies, SQLite WAL single-writer architecture, and consistent database backup routines.

---

## 1. Provisioning in `import.yaml`

Local storage services are provisioned declaratively in `import.yaml`:

```yaml
#zeropsPreprocessor=on
services:
  # ==========================================
  # 1. LOCAL STORAGE PERSISTENT DISK SERVICE
  # ==========================================
  - hostname: storage
    type: local-storage:single@1
    priority: 10 # Starts before consumer runtime services
    verticalAutoscaling:
      cpuMode: SHARED
      minCpu: 1
      maxCpu: 2
      minRam: 0.5
      maxRam: 1.0
      minDisk: 10.0
      maxDisk: 100.0

  # ==========================================
  # 2. CONSUMER RUNTIME SERVICE
  # ==========================================
  - hostname: backend
    type: nodejs@24
    priority: 5
    buildFromGit: https://github.com/myorg/backend
```

*Note:* Do **NOT** put `mount:` in `import.yaml`. The mount relationship is declared inside the consumer's `zerops.yaml`.

---

## 2. Mounting Volume in `zerops.yaml`

Runtime services attach the volume via the `run.volume` directive in `zerops.yaml`:

```yaml
zerops:
  - setup: prod
    build:
      base: nodejs@24
      buildCommands:
        - npm ci
        - npm run build
      deployFiles:
        - dist/
        - node_modules/
        - package.json

    run:
      base: nodejs@24
      # ==========================================
      # ATTACH LOCAL STORAGE VOLUME
      # ==========================================
      volume:
        hostname: storage           # Hostname of local-storage service (Required)
        mountPath: /mnt/storage     # Target path (Optional, default: /mnt/{hostname})
        readOnly: false             # Read-only flag (Optional, default: false)
      
      ports:
        - port: 3000
          httpSupport: true
      start: node dist/index.js
```

### `run.volume` Field Specifications

| Field | Required | Default | Description |
|---|---|---|---|
| `hostname` | **Yes** | — | Hostname of the `local-storage:single@1` service in the same project. |
| `mountPath` | No | `/mnt/{hostname}` | Absolute destination directory inside runtime containers. System roots (`/etc`, `/var`, `/tmp`) rejected. |
| `readOnly` | No | `false` | When `true`, mounts the volume read-only. Enforces single-writer architecture for reader replicas. |

---

## 3. SQLite WAL Mode & Consistent Database Backups

### Single-Writer Pattern
While single-kernel POSIX locking makes concurrent reads and writes safe, SQLite allows only one writer at a time. To prevent `SQLITE_BUSY` contention:
- Designate a single primary container for write operations.
- Mount the volume as `readOnly: true` on background workers or read replicas.

### Consistent Database Backup via `run.crontab`
Because platform `.tar.gz` backups archive the live volume, SQLite database files might be captured during a write. To guarantee atomic, restorable backups:

```yaml
run:
  volume:
    hostname: storage
    mountPath: /mnt/storage
  
  # Perform atomic online SQLite backup every night at 02:00 UTC
  crontab:
    - command: sqlite3 /mnt/storage/app/data.db ".backup /mnt/storage/app/backups/data_$(date +\%Y\%m\%d).db"
      timing: "0 2 * * *"
      allContainers: false # Execute on one container only
```

---

## 4. Multi-Service Directory Hierarchy

To keep multi-service data cleanly structured on a shared volume:

```
/mnt/storage/
├── backend/
│   ├── uploads/            # App media uploads
│   └── data.db             # Primary SQLite database file
├── worker/
│   └── processing_cache/   # Worker temporary cache
└── shared/
    └── static-assets/      # Shared assets across services
```

*Ownership Note:* The mount point is automatically owned by `zerops:zerops` (UID 1000). No `chmod 777` workarounds are necessary.

---

## 5. Inspection, SSH Access & Troubleshooting

### A. Inspecting the Volume from Runtime Service
```bash
# Verify volume mount and available disk capacity
df -h | grep /mnt/storage

# Check permissions and files
ls -la /mnt/storage/
```

### B. Direct Inspection in Local Storage Maintenance Container
```bash
# Connect over SSH to the storage maintenance container
ssh storage "ls -la /data"

# Check storage capacity directly on the host volume
ssh storage "df -h /data"
```

### C. Disconnecting / Deleting a Volume
To delete a Local Storage service, first remove the `run.volume` block from all connecting `zerops.yaml` files and deploy them. Once no active services reference the volume, it can be safely removed via `zerops_delete`.

---

## 6. ZCP Control-Plane Mounting Protocol (`/var/www/{hostname}`)

To inspect, stage, and transfer assets directly from the ZCP terminal or IDE workspace without passing large payloads through web interfaces:

### A. Root Path Discrepancy & Remote Bind Mount
Inside managed `local-storage:single@1` containers, the physical volume mounts internally at `/data`. However, ZCP conventions and tools (`zerops_mount`, SSHFS) default to `/var/www`. 
To bridge this seamlessly, establish a persistent kernel bind mount inside the storage container:

```bash
# Executed on the storage container (via SSH)
sudo mkdir -p /var/www
sudo mount --bind /data /var/www
echo '/data /var/www none bind 0 0' | sudo tee -a /etc/fstab
```

### B. Automated Control-Plane Mounting
Use the bundled determinism script:
```bash
# Mount storage locally at /var/www/localstorage
bash .agents/skills/local-storage/scripts/localstorage-mount-zcp.sh mount localstorage

# Check status and capacity
bash .agents/skills/local-storage/scripts/localstorage-mount-zcp.sh status localstorage

# Unmount cleanly
bash .agents/skills/local-storage/scripts/localstorage-mount-zcp.sh unmount localstorage
```

### C. Manual Mounting via SSHFS
```bash
mkdir -p /var/www/{hostname}
sshfs -o allow_other,default_permissions,reconnect {hostname}:/var/www /var/www/{hostname}
```

### D. Clean Unmounting (Preventing FUSE Locks)
Never terminate SSHFS abruptly. Unmount cleanly using:
```bash
fusermount3 -u /var/www/{hostname} || fusermount3 -uz /var/www/{hostname}
```

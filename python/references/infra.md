# Python — Infrastructure & Platform Lifecycle Manual on Zerops

This manual specifies the infrastructure topology, build/run lifecycle mechanics, base OS options, multi-dimensional container comparisons, and bounded execution harnesses for deploying the **Zerops Managed Python Runtime** (`type: python@...` / `python@3.12`).

---

## 1. Platform Topology & Service Provisioning (`import.yaml`)

Zerops Managed Python runs in unprivileged **Incus Linux Containers (LXC)** attached to an isolated VXLAN project network.

```yaml
# import.yaml - Production Topology for Python
services:
  - hostname: api
    type: python@3.12 # or python@latest
    enableSubdomainAccess: true
```

> **Automatic Vertical Autoscaling Invariant**:
> Do not author manual `verticalAutoscaling` min/max blocks. Zerops natively monitors CPU and memory usage and auto-scales vertically on demand with sub-second responsiveness.

---

## 2. Multi-Dimensional Comparison: Managed vs Generic Containers

| Criterio | Zerops Managed Python Runtime (`type: python@3.12`) | Generic Ubuntu LXC con Python (`type: ubuntu@24`) | Generic Alpine LXC con Python (`type: alpine@3.20`) |
|---|---|---|---|
| **Aprovisionamiento** | **1 línea en `import.yaml` (`type: python@3.12`)** | Requiere instalar `python3`, `pip`, `venv` en `prepareCommands` | Requiere instalar `python3`, `py3-pip` en `prepareCommands` |
| **Toolchain Python** | **Preinstalado y optimizado por Zerops** | Instalado manualmente vía `apt-get` | Instalado manualmente vía `apk` |
| **Manejo de Dependencias** | **`pip --target=./vendor` con `cache: [vendor]`** | Requiere crear y gestionar `venv` manual | Requiere crear y gestionar `venv` manual |
| **Ruedas C (Data Science)** | Switch nativo `os: ubuntu` (ruedas manylinux instantáneas) | Soporta ruedas manylinux (`glibc 2.39`) | Falla o tarda 10–30m compilando en `musl` |
| **Tiempo de Build** | **Ultra-Rápido** (toolchain listo + cache nativo) | Medio (instala paquetes apt en base) | Medio (instala paquetes apk en base) |
| **Overhead de RAM Base** | **Mínimo (~20–35 MB)** | Medio (~35–50 MB) | Mínimo (~15–25 MB) |
| **Mantenimiento Operativo** | **Cero**: Zerops parchea el runtime | Alto: Mantenimiento manual de toolchain | Alto: Mantenimiento manual de toolchain |
| **Autoescalado Vertical** | **Elástico Automático Nativo (`min < max`)** | **Elástico Automático Nativo (`min < max`)** | **Elástico Automático Nativo (`min < max`)** |

---

## 3. Build & Deploy Lifecycle Mechanics (`zerops.yaml`)

```
+--------------------------------------------------------------------------+
| Zerops Build Container (Envelope: 1-5 CPU, 8GB RAM fixed, 60m timeout)   |
| - Base: python@3.12 (os: alpine or os: ubuntu)                           |
| - Installs: pip install --target=./vendor -r requirements.txt            |
| - Cache: vendor                                                          |
+------------------------------------+-------------------------------------+
                                     |
                                     | deployFiles: [./src, ./vendor]
                                     v
+--------------------------------------------------------------------------+
| Zerops Runtime Container (Incus LXC - Native Dynamic Autoscaling)        |
| - Base: python@3.12 (os: alpine or os: ubuntu)                           |
| - envVariables: PYTHONPATH: /var/www/vendor                              |
| - run.initCommands: zsc execOnce ${appVersionId} -- alembic upgrade head |
| - run.start: granian --interface asgi src.main:app                       |
| - deploy.readinessCheck: HTTP 200 at /healthz                            |
+--------------------------------------------------------------------------+
```

### Complete Production `zerops.yaml` Specification
```yaml
zerops:
  - setup: prod
    build:
      base: python@3.12
      os: alpine
      buildCommands:
        - pip install --target=./vendor -r requirements.txt
      deployFiles:
        - ./src
        - ./vendor
        - ./alembic
        - ./alembic.ini
      cache:
        - vendor

    deploy:
      readinessCheck:
        httpGet:
          port: 8000
          path: /healthz

    run:
      base: python@3.12
      os: alpine
      initCommands:
        - zsc execOnce ${appVersionId} --retryUntilSuccessful -- /var/www/vendor/bin/alembic upgrade head
      ports:
        - port: 8000
          httpSupport: true
      envVariables:
        PORT: "8000"
        PYTHONPATH: /var/www/vendor
        DB_HOST: ${db_hostname}
        DB_PORT: ${db_port}
        DB_USER: ${db_user}
        DB_PASS: ${db_password}
        DB_NAME: db
      start: /var/www/vendor/bin/granian --interface asgi --host 0.0.0.0 --port 8000 --workers 2 src.main:app
```

---

## 4. Environment Variables Reference (.env)

| Variable | Type | Required | Default | Purpose |
|---|---|---|---|---|
| `PORT` | Number | Yes | `8000` | Internal listening port routed by L7 load balancer |
| `PYTHONPATH` | String | Yes | `/var/www/vendor` | Points Python import system to deployed vendored packages |
| `DB_HOST` | String | No | `${db_hostname}` | Internal DNS address of Zerops PostgreSQL service |
| `DB_PORT` | Number | No | `${db_port}` | Port of Zerops PostgreSQL service |
| `DB_USER` | String | No | `${db_user}` | Database user generated by Zerops |
| `DB_PASS` | String | No | `${db_password}` | Database password generated by Zerops |
| `DB_NAME` | String | No | `db` | Database name matching database hostname |

---

## 5. Storage Mounts & FUSE Permission Safeguards

When mounting shared storage (`shared-storage`) to Python runtime containers:

```bash
# Storage mount destination convention
/mnt/<storageHostname>/<service>/

# FUSE Permission Shield (executed in run.initCommands or prepareCommands)
chmod -R 777 /mnt/<storageHostname>/<service>/
```

---

## 6. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

* **Strict Synchronous Timeouts**: All terminal healthchecks and diagnostics MUST execute with explicit timeouts:
  ```bash
  timeout 10s curl -s -f http://localhost:8000/healthz
  ```
* **Circuit Breaker (2-Attempt Limit)**: On consecutive HTTP 500 or timeout failures, immediately halt execution and trigger human escalation.
* **Zero Orphaned Tasks Invariant**: Always clean lingering background inspection tasks:
  ```typescript
  await manage_task({ Action: 'kill', TaskId: taskId });
  ```

# Docker on Zerops (dckr) — Infrastructure & Deployment Manual

## 1. Especificaciones de la Máquina Virtual Docker

- **Tipo de Servicio en Zerops:** Docker VM (`type: docker@1`).
- **Arquitectura de Cómputo:** Máquina Virtual QEMU/Incus dedicada con recursos fijos (`min == max`).
- **Configuración de Recursos:**
  - `cpuMode: SHARED`
  - `minCpu: 2, maxCpu: 2` (vCPU fijas)
  - `minRam: 6, maxRam: 6` (GB RAM fijas)
  - `minDisk: 10, maxDisk: 10` (GB Disco base VM)
- **Validación con Arnés:** `zcp-validate scaling docker 2 2 6 6`

---

## 2. Red y Puertos de Acceso

- **Modo de Red:** `network_mode: host` (mandatorio para exponer puertos directamente a la red Zerops).
- **Puertos en `zerops.yaml`:**
  - Puerto WebTop HTTP: `3000` (con `httpSupport: true` para subdominios `*.zerops.app` y HTTPS automático).
  - Puerto WebTop HTTPS: `3001` (opcional / acceso directo).

---

## 3. Persistencia y Almacenamiento Local (Local Storage)

- **Declaración de Servicio:** `type: local-storage:single@1` en `import.yaml`.
- **Montaje en VM Docker:** `run.volume: {hostname: <storageHostname>, mountPath: /mnt/<storageHostname>}` en `zerops.yaml`.
- **Rutas de Montaje en Compose:**
  - Configuración y Home: `/mnt/<storageHostname>/<service>/config` -> `/config`
  - Datos de Trabajo: `/mnt/<storageHostname>/<service>/data` -> `/data`
- **Propiedad de Archivos:**
  - El volumen persistente es propiedad nativa de `zerops:zerops` (`PUID=1000`, `PGID=1000`), coincidiendo de forma exacta con la configuración estándar de contenedores LinuxServer (`PUID=1000`).

---

## 4. Ciclo de Vida en `zerops.yaml`

```yaml
zerops:
  - setup: webtop
    build:
      prepareCommands:
        - sudo apk update && sudo apk add git docker-cli-compose nano curl
    run:
      volume:
        hostname: storage
        mountPath: /mnt/storage
      prepareCommands:
        - mkdir -p /mnt/storage/webtop/config /mnt/storage/webtop/data
      start: docker compose -f /var/www/docker-compose.yml up --build -d && docker compose -f /var/www/docker-compose.yml logs -f
      ports:
        - port: 3000
          httpSupport: true
```

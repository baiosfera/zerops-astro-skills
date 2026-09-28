# Docker on Zerops (dckr) — Developer & Agent Usage Manual

## 1. Inicialización y Estructura del Stack en Zerops

En Zerops, los servicios Docker operan dentro de una máquina virtual dedicada (QEMU/Incus). El código del servicio reside en `/var/www/{hostname}` y se gestiona mediante `docker compose` o un `Dockerfile` a medida.

### Estructura Canónica de Archivos:
```text
/var/www/{hostname}/
├── Dockerfile              # Construcción personalizada (Chrome, Rclone, Node, etc.)
├── docker-compose.yml      # Definición del stack con network_mode: host y volúmenes
└── zerops.yaml             # Contrato de despliegue y ciclo de vida de Zerops
```

---

## 2. Definición del Dockerfile y Compose para WebTop

### Dockerfile Personalizado (Ubuntu-XFCE + Chrome + Rclone):
```dockerfile
FROM lscr.io/linuxserver/webtop:ubuntu-xfce-version-ac42946c

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    gnupg \
    ca-certificates \
    rclone \
    fonts-liberation \
    xdg-utils \
    libnss3 \
    libgbm1 \
    libasound2 \
    dbus-x11 \
    && curl -fsSL "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" -o /tmp/google-chrome.deb \
    && dpkg -i /tmp/google-chrome.deb || apt-get install -fy \
    && rm -f /tmp/google-chrome.deb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN if [ -f /kclient/public/index.html ]; then sed -i 's/resize=remote/resize=scale/g' /kclient/public/index.html; fi
```

### `docker-compose.yml` Canónico:
```yaml
services:
  webtop:
    build:
      context: /var/www
      dockerfile: Dockerfile
    container_name: webtop
    network_mode: host
    restart: unless-stopped
    shm_size: "2gb"
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=UTC
      - TITLE=WebTop Ubuntu Desktop
      - CUSTOM_USER=admin
      - PASSWORD=${WEBTOP_PASSWORD:-admin123}
    volumes:
      - /mnt/storage/webtop/config:/config
      - /mnt/storage/webtop/data:/data
```

---

## 3. Patrones de Producción y Casos de Uso

### A. Google Chrome en WebTop
Google Chrome requiere memoria compartida (`shm_size: 2gb` o superior) para evitar caídas en renderizado WebRTC/WebGL. En entornos no-root dentro del contenedor WebTop, Chrome opera de forma nativa sin banderas `--no-sandbox` si se ejecuta como usuario estándar (`PUID=1000`).

### B. Persistencia con Rclone
Rclone almacena sus configuraciones en `/config/.config/rclone/rclone.conf`. Dado que `/config` está mapeado al almacenamiento persistente (`/mnt/storage/webtop/config`), cualquier remoto configurado (`rclone config` o montajes automáticos) persistirá a través de reinicios y redespliegues.

---

## 4. Trampas Comunes y Gotchas (Anti-Patterns)

1. **Tag `:latest` Prohibido**: Zerops cachea imágenes Docker sin re-descargar si se usa `:latest`. Usar siempre tags inmutables o compilación local con Dockerfile.
2. **`network_mode: host` Obligatorio**: Sin `network_mode: host`, los puertos del contenedor no se vinculan a la interfaz de la VM de Zerops y el enrutador L7 no podrá entregar tráfico.
3. **Mapeo de Rutas de Almacenamiento**: Los volúmenes deben apuntar a rutas absolutas montadas en el host (`/mnt/<storageHostname>/<service>/...`), asegurando permisos 777 antes de iniciar el contenedor.
4. **Comando `start` en `zerops.yaml`**: Debe invocar directamente el binario con ruta completa (`docker compose -f /var/www/docker-compose.yml up`). Nunca usar encadenamientos con `cd`.

# Alpine Linux — Developer & Agent Usage Manual on Zerops

This manual provides production-tested specifications, APK package management standards, musl libc architecture, and code recipes for developing on **Alpine Linux** (`base: alpine@3.20` / `os: alpine`) in Zerops.

---

## 1. System Ecosystem & Package Management

### System Architecture Highlights (Alpine Linux)
* **C Standard Library**: **musl libc** — lightweight, POSIX-compliant C standard library optimized for static linking and minimal memory overhead.
* **Base Footprint**: **~5 MB base image**, requiring only ~8–15 MB RAM in idle runtime.
* **Core Utilities**: BusyBox multi-call binary.
* **Package Manager**: Alpine Package Keeper (`apk`).

### Production `apk` Execution Standard
In Zerops, runtime and build containers execute under the unprivileged `zerops` user. All package installations require `sudo` and MUST use the `--no-cache` flag:

```bash
# Standard Non-Interactive apk Pipeline
sudo apk add --no-cache \
  ca-certificates \
  curl \
  tzdata \
  git

# Ephemeral Build Dependencies Pattern (Clean Layering)
sudo apk add --no-cache --virtual .build-deps \
  build-base \
  make \
  gcc && \
# ... run build commands ...
sudo apk del .build-deps
```

---

## 2. musl libc Architecture & Static Linking

### Strengths of musl libc
1. **True Static Binaries**: Compiling with `CGO_ENABLED=0` in Go or `--target x86_64-unknown-linux-musl` in Rust produces fully self-contained binaries that run on Alpine without external shared libraries.
2. **Minimal Memory Overhead**: Eliminates GNU libc glibc overhead, enabling container cold-boots in under 1 second.
3. **Security Footprint**: Ultra-minimal attack surface with near-zero extraneous binaries.

### Limitations & When to Switch to Ubuntu
* **C-Extension Python Wheels**: Packages like `torch`, `numpy`, `pandas`, `opencv-python` do not distribute musl wheels. In Alpine, they must compile from source, often failing or taking 30+ minutes. Use `os: ubuntu` instead.
* **CGO Dynamic Linking**: Go programs using dynamic C bindings (`libvips`, `librdkafka`) will suffer memory allocation contention in musl or fail with dynamic loader errors. Use `os: ubuntu` instead.
* **Deno Runtime**: Zerops does not offer an Alpine build for Deno. Deno requires `os: ubuntu`.

---

## 3. Production Patterns & Verified Code Recipes

### Pattern 1: Ultra-Lean Static Web Server with Nginx (~8 MB RAM)
```nginx
# nginx.conf
events { worker_connections 1024; }
http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    sendfile on;
    keepalive_timeout 65;

    server {
        listen 80;
        server_name localhost;
        root /var/www;
        index index.html;

        location / {
            try_files $uri $uri/ /index.html;
        }

        location /healthz {
            access_log off;
            return 200 "healthy\n";
        }
    }
}
```

In `zerops.yaml`:
```yaml
zerops:
  - setup: staticweb
    run:
      base: alpine@3.20
      prepareCommands:
        - sudo apk add --no-cache nginx
      start: nginx -g "daemon off;"
      ports:
        - port: 80
          httpSupport: true
```

### Pattern 2: Pure Go Static Microservice (`CGO_ENABLED=0`)
```go
package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
)

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	http.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprintf(w, "OK - Alpine pure Go service running")
	})

	log.Printf("Starting static server on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
```

### Pattern 3: Rust Web API with Musl Target
```bash
# In zerops.yaml buildCommands
cargo build --release --target x86_64-unknown-linux-musl
```

### Pattern 4: Node.js / Bun Production Server (Pure JS/TS)
```yaml
zerops:
  - setup: api
    build:
      base: nodejs@22
      os: alpine
      buildCommands:
        - npm ci --omit=dev
        - npm run build
      deployFiles:
        - dist/
        - node_modules/
        - package.json
    run:
      base: nodejs@22
      os: alpine
      start: node dist/index.js
      ports:
        - port: 3000
          httpSupport: true
```

### Pattern 5: Network Diagnostics & Troubleshooting in Alpine
```bash
# Install network inspection utilities
sudo apk add --no-cache bind-tools curl busybox-extras iputils

# Test DNS resolution
dig +short api.zerops.io

# Inspect open TCP connections
netstat -tulpn
```

---

## 4. Anti-Patterns & Gotchas in Zerops

| Anti-Pattern | Why it Fails | Correct Solution |
|---|---|---|
| Running `apt-get` on Alpine | `apt-get: command not found` | Always use `sudo apk add --no-cache <pkg>`. |
| Omitting `--no-cache` on `apk add` | Leaves apk index cache on disk, bloating image layers | Always append `--no-cache` to `apk add`. |
| Compiling PyTorch/SciPy on Alpine | Requires compiling huge C/C++ source on musl; slow or broken | Switch service to `os: ubuntu` to use pre-built manylinux wheels. |
| Forgetting `sudo` with `apk` | `apk: Permission denied` (Zerops runs as unprivileged user) | Prefix package commands with `sudo`. |
| Hardcoding `verticalAutoscaling` | Overrides Zerops' native dynamic elastic scaling | Omit `verticalAutoscaling` and allow Zerops to auto-scale. |

# Ubuntu 24.04 LTS — Developer & Agent Usage Manual

This manual provides production-tested specifications, compilation pipelines, native C/C++ build patterns, and gotcha resolutions for running on **Ubuntu 24.04 LTS (Noble Numbat)** in Zerops.

---

## 1. System Ecosystem & Package Management

### System Architecture Highlights (Ubuntu 24.04 LTS)
* **C Standard Library**: GNU C Library (**glibc 2.39**-0ubuntu8.x) with multi-threaded, lock-free `ptmalloc3` memory allocator.
* **Compiler Toolchain**: GCC 13.2 / GCC 14.x, Clang 18, Make 4.3, Binutils 2.42.
* **Cryptography & SSL**: OpenSSL 3.3.x (FIPS ready, TLS 1.3 default).
* **Package Manager**: Advanced Packaging Tool (`apt-get`).

### Production `apt-get` Execution Standard
In Zerops, runtime and build containers execute under the unprivileged `zerops` user. All package installations require `sudo` and must clean the local apt cache to prevent image bloat:

```bash
# Standard Non-Interactive apt-get Pipeline
sudo DEBIAN_FRONTEND=noninteractive apt-get update -y && \
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  build-essential \
  pkg-config \
  curl \
  ca-certificates \
  libssl-dev \
  git && \
sudo rm -rf /var/lib/apt/lists/*
```

---

## 2. Native Compilation Pipelines

### A. Go with CGO (C-Linked Binaries)
When building Go binaries that bind C libraries (e.g. SQLite, libvips, duckdb), Alpine's musl libc causes dynamic linking mismatches that lead to immediate `502 Bad Gateway` errors upon startup. Ubuntu 24 provides native glibc dynamic linking:

```bash
# Compilation flags for CGO on Ubuntu 24
export CGO_ENABLED=1
export CC=gcc
export CXX=g++
go build -ldflags="-s -w -extldflags '-static-libgcc'" -o /var/www/app main.go
```

### B. Python Data Science & glibc Wheels
Python packages with heavy C/C++ backends (numpy, pandas, scipy, torch, opencv) provide pre-compiled `manylinux_2_39` glibc wheels. In Alpine, these wheels must compile from raw source (often taking 20–40 minutes or failing due to musl header differences). On Ubuntu 24, wheels install in seconds:

```bash
# Production Python virtualenv setup in Ubuntu prepareCommands
sudo apt-get update && sudo apt-get install -y python3-dev python3-venv libvips-dev
python3 -m venv /var/www/venv
/var/www/venv/bin/pip install --upgrade pip setuptools wheel
/var/www/venv/bin/pip install numpy pandas scipy torch torchvision --extra-index-url https://download.pytorch.org/whl/cpu
```

### C. Node.js Native Addons (`node-gyp`)
Node packages containing native C++ bindings (`sharp`, `better-sqlite3`, `canvas`, `bcrypt`) compile smoothly with Ubuntu's standard Python 3 and GCC toolchain:

```bash
# prepareCommands for node-gyp on Ubuntu 24
sudo apt-get update && sudo apt-get install -y python3 make g++ libvips-dev
npm install --build-from-source
```

### D. Deno Runtime
Zerops explicitly requires `os: ubuntu` for Deno (no Alpine build exists on the platform):

```yaml
zerops:
  - setup: denoapp
    build:
      base: nodejs@22
      os: ubuntu
      prepareCommands:
        - sudo apt-get update && sudo apt-get install -y unzip curl
        - curl -fsSL https://deno.land/install.sh | sh
      buildCommands:
        - /home/zerops/.deno/bin/deno compile --allow-net --allow-read --output dist/server main.ts
      deployFiles:
        - dist/server
    run:
      base: ubuntu@24
      start: ./dist/server
```

---

## 3. Production Patterns & Verified Code Recipes

### Pattern 1: High-Throughput Go CGO Image Service (`libvips`)
```go
package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
)

// In Ubuntu 24, libvips is linked dynamically via pkg-config
// #cgo pkg-config: vips
// #include <vips/vips.h>
import "C"

func main() {
	if C.vips_init(C.CString("img-service")) != 0 {
		log.Fatal("Unable to initialize libvips")
	}
	defer C.vips_shutdown()

	port := os.Getenv("PORT")
	if port == "" {
		port = "3000"
	}

	http.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprintf(w, "OK - Ubuntu 24 glibc 2.39 engine running")
	})

	log.Printf("Starting CGO server on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
```

### Pattern 2: Python FastAPI Data Processing with glibc Wheels
```python
import os
import numpy as np
from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(title="Ubuntu 24 Data API")

@app.get("/healthz")
def health():
    # Verify glibc matrix computation in memory
    arr = np.random.rand(100, 100)
    res = float(np.linalg.det(arr))
    return {"status": "healthy", "det_sample": res, "glibc": "2.39"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

### Pattern 3: Node.js Native Addon Worker with `sharp`
```typescript
import express, { Request, Response } from 'express';
import sharp from 'sharp';

const app = express();
const PORT = process.env.PORT || 3000;

app.get('/healthz', async (_req: Request, res: Response) => {
  // Test native C++ libvips pipeline via sharp
  const buffer = await sharp({
    create: {
      width: 100,
      height: 100,
      channels: 4,
      background: { r: 0, g: 128, b: 255, alpha: 1 }
    }
  }).png().toBuffer();

  res.setHeader('Content-Type', 'image/png');
  res.send(buffer);
});

app.listen(PORT, () => {
  console.log(`Node.js Sharp Worker running on port ${PORT}`);
});
```

### Pattern 4: System Profiling & Diagnosis (`strace` & `perf`)
When diagnosing system bottlenecks, lock contention, or slow syscalls inside Ubuntu runtime containers:

```bash
# 1. Install diagnostics in prepareCommands (ephemeral) or runtime
sudo apt-get update && sudo apt-get install -y strace lsof procps gdb

# 2. Trace system calls of running process
strace -c -p $(pgrep -f "node|python|main")

# 3. Inspect open file descriptors & network sockets
lsof -i -P -n
```

### Pattern 5: Multi-Stage Lean Production Packaging
```yaml
zerops:
  - setup: api
    build:
      base: nodejs@22
      os: ubuntu
      prepareCommands:
        - sudo apt-get update && sudo apt-get install -y build-essential python3
      buildCommands:
        - npm ci
        - npm run build
        - npm prune --production
      deployFiles:
        - dist/
        - node_modules/
        - package.json
    run:
      base: ubuntu@24
      start: node dist/index.js
      ports:
        - port: 3000
          httpSupport: true
```

---

## 4. Error Handling & Edge Cases

| Symptom / Error | Root Cause | Remediation Strategy |
|---|---|---|
| `apk: command not found` | Attempting to run Alpine `apk` inside Ubuntu | Switch command to `sudo apt-get install -y <pkg>`. |
| `E: Could not open lock file /var/lib/dpkg/lock-frontend` | Concurrent apt process or unprivileged execution | Prefix with `sudo` and ensure prior apt process is completed. |
| `GLIBC_2.39 not found` | Binary compiled on newer glibc executed on older OS | Ensure target runtime matches build OS (`base: ubuntu@24`). |
| `502 Bad Gateway` on Go startup | CGO binary linked against missing shared library | Install required runtime shared libraries in `run.prepareCommands`. |

---

## 5. Anti-Patterns & Deprecations
* ❌ **Anti-Pattern 1: Targeting `ubuntu@22` or older**: Ubuntu 22.04 LTS is deprecated for new services. All new architectures MUST target `ubuntu@24`.
* ❌ **Anti-Pattern 2: Forgetting `sudo` on `apt-get`**: Zerops containers run as the non-root `zerops` user. Omitting `sudo` results in permission denied errors.
* ❌ **Anti-Pattern 3: Omitting `rm -rf /var/lib/apt/lists/*`**: Leaving apt package indices consumes 40–80 MB of unnecessary disk space in container layers.

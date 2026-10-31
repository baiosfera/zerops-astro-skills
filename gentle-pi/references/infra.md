# `gentle-pi` — Infrastructure, Runtime Topology & Zerops MCP Manual

This manual specifies the deployment architecture, container configuration, MCP observational mesh, and storage mounts for the **Pi Coding Agent** (`pidev`) on Zerops.

---

## 1. Zerops Service Specification (`ubuntu/nodejs@26`)

The `pidev` service runs as a simple developer container based on Ubuntu 26.04 LTS and Node.js 26.

```yaml
# recipes/services/12-pidev.yaml
services:
  - hostname: pidev
    type: nodejs@26
    mode: dev
    ports:
      - port: 3000
        protocol: TCP
        httpSupport: true
    mount:
      - /mnt/localstorage
```

### Why `ubuntu/nodejs@26`?
- **Pi Coding Agent**: Native support for Node.js 26 V8 engine (v14.6+) with type stripping.
- **glibc Compatibility**: Needed for native terminal bindings (`node-pty`, `quickjs-emscripten`, `tree-sitter`).
- **Memory Footprint**: ~60MB idle RAM, scaling up to 1GB during heavy TS compilation.

---

## 2. Zerops MCP Integration (`.pi/mcp.json`)

To prevent cluster myopia, Pi connects to the Zerops platform via an observational Model Context Protocol (MCP) server.

### MCP Configuration File (`/var/www/.pi/mcp.json`)
```json
{
  "mcpServers": {
    "zerops": {
      "command": "node",
      "args": ["/opt/zerops-mcp/dist/index.js"],
      "env": {
        "ZEROPS_READ_ONLY": "true",
        "ZEROPS_OBSERVATIONAL_ONLY": "true"
      }
    }
  }
}
```

### Observational Capabilities
- `zerops_discover`: Inspects active services, hostnames, and IP addresses in the private VXLAN.
- `zerops_logs`: Reads runtime logs from `webdev` to diagnose 500 errors or SSR crashes in real time.
- `zerops_env`: Reads environment variable names and wire definitions without leaking secret values.
- `zerops_verify`: Performs HTTP health checks and synthetic probes against application subdomains.

> **Zero Destruction Boundary**:
> Pi's MCP tools are strictly read-only and observational. Pi cannot mutate platform infrastructure, scale containers, or restart database clusters.

---

## 3. Storage Mounts & Brand SSoT Sharing

Pi has direct POSIX file access to:
1. **Application Code**: Mounted at `/var/www` (the shared Astro 5 project).
2. **Local Storage Volume**: Mounted at `/mnt/localstorage/pidev` containing:
   - `brandbook_state.json`: DTCG design tokens (colors, typography, spacing).
   - `assets/`: Vector icons, fonts, and optimized WebP images.
   - `receipts/`: Historical RDD audit receipts.

---

## 4. Bounded Execution & Process Daemon (`systemd` / supervisor)

Pi runs as an automated background daemon listening on NATS RPC `rpc.coding.execute`:

```bash
# pidev-daemon.sh
#!/usr/bin/env bash
set -euo pipefail

echo "Starting Pi Coding Agent NATS Worker on rpc.coding.execute..."
exec node /var/www/scripts/pi-nats-worker.mjs
```

### Resource Bounds
- Maximum task timeout: `120s`.
- RAM ceiling: 2048 MB.
- Maximum concurrent tasks: 1 (single-threaded determinism to prevent race conditions).

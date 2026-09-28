# Hermes-Agent to AGY (Antigravity) Execution Bridge Architecture

This guide specifies the bidirectional execution bridge allowing **Hermes-Agent on Telegram** to trigger, orchestrate, and supervise **Antigravity (AGY)** and the **Zerops Control Plane (ZCP)**.

---

## 1. Architectural Bridge Overview

When an authorized user communicates with Hermes via Telegram, Hermes parses administrative or operational intent and routes tasks into ZCP. Because Zerops deployments and code refactoring can take from seconds to minutes, a synchronous HTTP call risks dropping the Telegram connection or timing out.

The architecture provides **4 Bridge Modes**, with **Mode B (NATS JetStream)** designated as the SOTA production standard.

```
┌────────────────────────────────────────────────────────────────────────┐
│                          TELEGRAM CLIENT                               │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ HTTPS Message
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     HERMES-AGENT RUNTIME (Ubuntu)                      │
│                                                                        │
│  1. Parse User Intent (ChatML)                                         │
│  2. High-Risk Action Check (Require Inline Approval Button)            │
│  3. Formulate Task Payload                                             │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
           ┌───────────────────────┼───────────────────────┐
           │                       │                       │
     Mode A (MCP)            Mode B (NATS)           Mode C (SSH)
           │                       │                       │
           ▼                       ▼                       ▼
    ZCP HTTP MCP           NATS JetStream         SSH Host Command
    (:8080/mcp)            zerops.ops.requests    ssh zcp "cd /var/www..."
           │                       │                       │
           └───────────────────────┼───────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        ZCP / AGY RUNTIME HOST                          │
│                                                                        │
│  • Consumes Task Payload & Validates Authorization                     │
│  • Executes Antigravity Workflow / Zerops API                          │
│  • Publishes Progress Updates to JetStream / Outflow Channel           │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                 TELEGRAM FEEDBACK & STATUS STREAMING                   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. The 4 Operational Bridge Modes

### Mode A: Streamable MCP Client Mode
- **Mechanism**: Hermes acts as an MCP client connecting to the ZCP MCP server (`http://zcp:8080/mcp`).
- **Use Case**: Real-time read operations and lightweight mutations (`zerops_discover`, `zerops_logs`, `zerops_env`, `zerops_status`).
- **Strengths**: Native protocol alignment, direct JSON-RPC validation, zero middle tier.
- **Boundaries**: Not recommended for long-running workflows (>30s) due to client connection timeout windows.

### Mode B: NATS JetStream Event Bus (Recommended Production Standard)
- **Mechanism**: Hermes publishes asynchronous task requests to `zerops.ops.requests` with message deduplication (`Nats-Msg-Id`). A dedicated worker on the ZCP host receives the event, triggers AGY, and publishes progress logs to `zerops.ops.updates.{task_id}`.
- **Use Case**: Deployments, multi-service migrations, framework builds, and full SDD workflows.
- **Strengths**: Complete temporal decoupling, at-least-once delivery, zero Telegram timeouts, resumable state, and audit logs.

### Mode C: Bounded SSH / Headless CLI Mode
- **Mechanism**: Hermes invokes commands directly over SSH to the `zcp` container:
  ```bash
  ssh zcp "cd /var/www && timeout 10s zcli service deploy <service>"
  ```
- **Use Case**: Standalone single-command tasks, emergency restarts, direct container diagnostics.
- **Strengths**: Bypasses any application middleware; direct container access.
- **Boundaries**: Requires SSH key injection; must be guarded by strict command timeouts (`timeout 10s`).

### Mode D: Native Custom Hermes Plugin Mode
- **Mechanism**: Hermes loads a custom plugin in `~/.hermes/plugins/zerops_bridge/` exposing Python tools that wrap the Zerops REST API directly using `$ZEROPS_TOKEN`.
- **Use Case**: Self-contained edge deployments without external brokers.

---

## 3. Production Implementation: Mode B (NATS JetStream)

### Step 1: NATS Stream Topology & Setup

```bash
# Ensure the stream exists on the Zerops NATS cluster
nats stream add ZEROPS_OPS   --subjects "zerops.ops.requests,zerops.ops.updates.>"   --storage file   --retention limits   --max-age 24h
```

### Step 2: Hermes Task Publisher (Python)

```python
import json
import uuid
import time
from nats.aio.client import Client as NATS
from nats.js.api import PublishAck

class HermesAgyBridge:
    def __init__(self, nats_url: str = "nats://nats:4222"):
        self.nats_url = nats_url
        self.nc = NATS()

    async def connect(self):
        if not self.nc.is_connected:
            await self.nc.connect(self.nats_url)
            self.js = self.nc.jetstream()

    async def dispatch_task(self, action: str, service: str, caller_id: int, params: dict = None) -> str:
        await self.connect()
        task_id = str(uuid.uuid4())
        payload = {
            "task_id": task_id,
            "action": action,
            "target_service": service,
            "caller_id": caller_id,
            "params": params or {},
            "timestamp": time.time()
        }
        
        # Deduplication using task_id as Nats-Msg-Id
        headers = {"Nats-Msg-Id": task_id}
        await self.js.publish(
            "zerops.ops.requests",
            json.dumps(payload).encode("utf-8"),
            headers=headers
        )
        return task_id

    async def listen_for_progress(self, task_id: str, callback):
        await self.connect()
        subject = f"zerops.ops.updates.{task_id}"
        sub = await self.nc.subscribe(subject)
        async for msg in sub.messages:
            data = json.loads(msg.data.decode("utf-8"))
            await callback(data)
            if data.get("status") in ["completed", "failed"]:
                break
        await sub.unsubscribe()
```

### Step 3: ZCP Background Worker & AGY Execution Trigger

```python
import json
import subprocess
import asyncio
from nats.aio.client import Client as NATS

async def start_zcp_worker():
    nc = NATS()
    await nc.connect("nats://nats:4222")
    js = nc.jetstream()

    sub = await js.subscribe("zerops.ops.requests", durable="zcp-agy-executor")
    print("🚀 ZCP AGY Worker listening on zerops.ops.requests...")

    async for msg in sub.messages:
        try:
            task = json.loads(msg.data.decode("utf-8"))
            task_id = task["task_id"]
            action = task["action"]
            service = task["target_service"]

            # Emit in-progress status back to Telegram stream
            await nc.publish(
                f"zerops.ops.updates.{task_id}",
                json.dumps({"status": "running", "message": f"Executing {action} on {service}..."}).encode("utf-8")
            )

            # Execution logic: Call Zerops CLI / AGY workflow
            if action == "deploy":
                cmd = ["timeout", "120s", "zcli", "service", "deploy", service]
                proc = subprocess.run(cmd, capture_output=True, text=True)
                exit_code = proc.returncode
                output = proc.stdout if exit_code == 0 else proc.stderr
            elif action == "restart":
                cmd = ["timeout", "30s", "zcli", "service", "restart", service]
                proc = subprocess.run(cmd, capture_output=True, text=True)
                exit_code = proc.returncode
                output = proc.stdout if exit_code == 0 else proc.stderr
            else:
                exit_code = 1
                output = f"Unknown action: {action}"

            # Emit final status
            final_status = "completed" if exit_code == 0 else "failed"
            await nc.publish(
                f"zerops.ops.updates.{task_id}",
                json.dumps({"status": final_status, "output": output, "exit_code": exit_code}).encode("utf-8")
            )
            await msg.ack()
        except Exception as e:
            await msg.nak()
```

---

## 4. Security, Confirmation, & Audit Trail

1. **Strict RBAC**: Only Telegram users whose numeric ID is listed in `TELEGRAM_ALLOWED_USERS` can trigger the bridge.
2. **Inline Interactive Confirmation**: Operations categorized as high-impact (`deploy`, `restart`, `delete`, `migrate`, `env_set`) require explicit tap confirmation via Telegram inline keyboards before publishing to NATS.
3. **Audit Log Persistence**: Every published task record and outcome is written to `/var/log/hermes/bridge_audit.jsonl` and mirrored to the ZCP audit trail.

# Hermes-Agent Zerops Infrastructure & Runtime Specification

This specification establishes the deployment standard for running **Hermes-Agent** inside Zerops, enforcing the **Ubuntu Invariant**, vendor caching, and process supervision.

---

## 1. The Ubuntu Invariant (Non-Negotiable)

Hermes-Agent and modern agentic libraries rely on binary wheels for high-performance operations:
- `cryptography>=43.0.0`
- `pydantic-core>=2.20.0`
- `brotlicffi>=1.1.0`
- `tokenizers>=0.19.0`
- `orjson>=3.10.0`

### Alpine / musl Failure Mode
When deploying Python runtimes with native Rust/C extensions on **Alpine Linux** (`musl` libc), `pip` fails to locate matching `manylinux` wheels and attempts to compile from source. This results in:
1. Protracted build times (>15 minutes) or complete build timeouts.
2. Missing Rust toolchain errors (`cargo: command not found`).
3. Runtime segfaults during cryptographic handshakes.

### Mandate
All Zerops runtime services running Hermes-Agent **MUST** explicitly specify:
```yaml
zerops:
  - setup: hermes
    build:
      base: python@3.12
      os: ubuntu
    run:
      base: python@3.12
      os: ubuntu
```

---

## 2. Dependency Management & Vendor Caching

To guarantee instant boot times and deterministic deployments, dependencies must be installed into a localized `vendor/` directory during the build phase:

```yaml
build:
  base: python@3.12
  os: ubuntu
  buildCommands:
    - pip install --upgrade pip
    - pip install --target=./vendor -r requirements.txt
  deployFiles:
    - vendor/
    - hermes/
    - config/
    - main.py
    - zerops.yaml
```

At runtime, configure `PYTHONPATH` in the service environment:
```yaml
run:
  envVariables:
    PYTHONPATH: "./vendor"
```

---

## 3. Environment Variable Dictionary

| Variable Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `HERMES_MODEL_ENDPOINT` | URL | Yes | — | Base URL of the OpenAI-compatible inference endpoint (e.g. `http://bifrost:8080/v1` or vLLM). |
| `HERMES_MODEL_NAME` | String | Yes | `hermes-3-llama-3.1-8b` | Exact model identifier used for inference. |
| `HERMES_API_KEY` | Secret | No | `dummy` | Authorization token for the upstream LLM endpoint. |
| `TELEGRAM_BOT_TOKEN` | Secret | Yes | — | Authentication token issued by `@BotFather`. |
| `TELEGRAM_ALLOWED_USERS` | String | Yes | — | Comma-separated list of authorized Telegram numeric user IDs (`e.g. "123456789,987654321"`). |
| `TELEGRAM_WEBHOOK_URL` | URL | No | — | Public HTTPS URL for Telegram webhooks. If unset, polling mode is activated. |
| `ZCP_NATS_URL` | URL | No | `nats://nats:4222` | Internal connection URL for the Zerops NATS JetStream cluster. |
| `ZCP_MCP_URL` | URL | No | `http://zcp:8080/mcp` | Internal URL of the Zerops Control Plane MCP server. |
| `VALKEY_URL` | URL | No | `redis://valkey:6379/0` | Connection string for session caching and rate-limiting state. |
| `PORT` | Integer | No | `8000` | HTTP listen port for webhooks and health probes. |

---

## 4. Complete `zerops.yaml` Production Recipe

```yaml
zerops:
  - setup: hermes
    build:
      base: python@3.12
      os: ubuntu
      buildCommands:
        - pip install --upgrade pip setuptools wheel
        - pip install --target=./vendor -r requirements.txt
      deployFiles:
        - vendor/
        - hermes/
        - config/
        - main.py
        - zerops.yaml
      cacheFiles:
        - /root/.cache/pip
    run:
      base: python@3.12
      os: ubuntu
      ports:
        - port: 8000
          httpSupport: true
      envVariables:
        PORT: "8000"
        PYTHONPATH: "./vendor"
        HERMES_MODEL_ENDPOINT: "http://bifrost:8080/v1"
        HERMES_MODEL_NAME: "hermes-3-llama-3.1-8b"
        ZCP_NATS_URL: "nats://nats:4222"
      start: python main.py
      healthCheck:
        httpGet:
          port: 8000
          path: /healthz
```

---

## 5. CoHaLo Operational Timeouts & Resource Boundaries

| Metric | Boundary | Enforcement Mechanism |
|---|---|---|
| **Max Webhook Execution Time** | 10 seconds | Telegram drops webhooks taking >15s. Heavy operations must offload to background tasks. |
| **Max CLI / Task Timeout** | 10 seconds | `timeout 10s <cmd>` on all container and subshell executions. |
| **Tool Execution Sensor** | Exit code `0` or valid JSON | Strict attestation before returning result to LLM scratchpad. |
| **Container Memory Target** | 512 MB – 2 GB | Configurable in Zerops GUI / manifest based on traffic volume. |
| **Container vCPU Target** | 0.5 – 2 vCPU | Elastic scaling handled automatically by Zerops LXC manager. |

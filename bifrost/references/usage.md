# Maxim AI Bifrost & Bifrost CLI — Developer & Operational Usage Manual (v2.0)

> **Governance Framework:** Supreme Directive v6.8 · Docu v5.5 · Zero Deletion Invariant · Bifrost v2.0.0 GA & v1.6.11 LTS · SSoT Indivisible

---

## 1. Architectural Surface & Front Gateway Integration

Bifrost (`maximhq/bifrost`) is an ultra-low-overhead enterprise AI gateway written natively in Go. It operates as the **Single Front Door (Unified Entry Point)** for all LLM inference traffic across sovereign infrastructure, adding only **~11 µs** of request overhead at 5,000 RPS (50x faster than Python proxies).

Behind Bifrost, requests are dynamically routed across two primary upstream targets:
1. **FreeLLMAPI Upstream (`http://freellmapi:3001/v1`):** High-throughput sustrato managing 34+ free provider pools, rotating keys, and mitigating 429 errors.
2. **Pro Provider Slot (`env.PRO_BASE_URL`):** Parametrizable commercial slot (OpenAI, Anthropic, Gemini Pro, etc.) ready for premium inference or contingency failover.

### Connection Architecture
- **Unified Base URL**: `http://<bifrost-host>:8080/v1`
- **Native Open Wire Endpoints** (zero client translation):
  - `/openai/*`: Standard OpenAI wire specification (`/v1/chat/completions`, `/v1/models`, `/v1/embeddings`)
  - `/anthropic/*`: Standard Anthropic Messages wire specification (`/v1/messages`)
  - `/genai/*`: Standard Google GenAI REST specification
  - `/bedrock/*`: Standard AWS Bedrock Converse & InvokeModel specification
  - `/mcp`: Unified Model Context Protocol (MCP) streamable gateway
- **Authentication**: All client requests authenticate using a Bifrost Virtual Key (`sk-bf-*`) passed via `Authorization: Bearer <key>` or `x-bf-vk: <key>`. Direct upstream keys are strictly rejected at the edge.

---

## 2. 2026 Normative Invariants & Breaking Changes (v2.0.0 GA)

Every consumer, agent, and operator configuring Bifrost MUST enforce these active invariants:

1. **Inversion of Empty Allow-Lists (`version: 2` Semantics)**:
   - `[]` (empty array) strictly means **DENY ALL**.
   - `["*"]` is strictly required to **ALLOW ALL**.
   - Applies to: provider key `models`, Virtual Key `allowed_models`, Virtual Key `key_ids`, and Virtual Key MCP `tools_to_execute`.
   - Mixing wildcards with literals (e.g. `["*", "gpt-4o"]`) is rejected with HTTP 400.
2. **`allowed_keys` Renamed to `key_ids`**:
   - Provider restriction in Virtual Keys uses `key_ids: ["*"]` or explicit key names. The legacy attribute `allowed_keys` is deprecated and purged.
3. **Consolidation of Cloud Deployment Maps**:
   - All provider-specific `deployments` maps are merged into the top-level `aliases` dictionary on each key.
4. **Deny-by-Default Virtual Keys**:
   - Virtual Keys with empty or missing `provider_configs` have zero access to any provider.
5. **Multi-Budget Structure**:
   - Singular `budget_id` is replaced by the `budgets` array supporting multi-window reset intervals (e.g., hourly, daily, monthly caps) with `calendar_aligned: true`.
6. **No Direct Provider Key Pass-Through**:
   - The HTTP gateway rejects raw upstream provider keys passed directly in headers.
7. **SSRF Hardening (v2.0.0)**:
   - Plugin `.so` downloads reject private, loopback, and link-local CIDRs unless explicitly listed in `server.plugin_download_private_allowlist`.

---

## 3. Common Expression Language (CEL) Routing Engine

Bifrost evaluates routing rules at microsecond speeds using Common Expression Language (CEL) expressions.

### A. CEL Context Variables Dictionary

| Variable | Type | Description | Example Expression |
|---|---|---|---|
| `model` | string | Target model identifier requested by caller | `model.startsWith('llama-')` |
| `provider` | string | Target upstream provider identifier | `provider == 'freellmapi'` |
| `budget_used` | float | Percentage of active budget consumed (0.0–100.0) | `budget_used > 85.0` |
| `tokens_used` | float | Percentage of token quota consumed (0.0–100.0) | `tokens_used > 90.0` |
| `request` | float | Percentage of request quota consumed (0.0–100.0) | `request > 80.0` |
| `request_body.max_tokens` | int | Max output tokens specified in payload | `request_body.max_tokens > 4000` |
| `request_body.temperature` | float | Sampling temperature requested | `request_body.temperature == 0.0` |
| `headers["x-tier"]` | string | Value of custom HTTP request header | `headers['x-tier'] == 'priority'` |
| `virtual_key_id` | string | ID of the Virtual Key executing the request | `virtual_key_id == 'vk-prod'` |

### B. Canonical Zero-Leak Routing: FreeLLMAPI ($0) Default with Pro Fallback
```json
{
  "routing_rules": [
    {
      "id": "rule-explicit-pro-override",
      "name": "Route Explicit Pro Tier Requests Directly to Pro/DeepSeek",
      "cel_expression": "headers['x-force-deepseek'] == 'true' || headers['x-tier'] == 'pro' || headers['x-routing-tier'] == 'pro'",
      "targets": [
        {
          "provider": "pro",
          "weight": 1.0
        }
      ],
      "fallbacks": ["freellmapi"],
      "priority": 0
    },
    {
      "id": "rule-freellm-zero-cost-universal",
      "name": "Prioritize FreeLLMAPI ($0) for All Models (Chat, Code, Reasoning) with Paid Failover",
      "cel_expression": "true",
      "targets": [
        {
          "provider": "freellmapi",
          "weight": 1.0
        }
      ],
      "fallbacks": ["pro"],
      "priority": 1
    }
  ]
}
```

---

## 4. Semantic Caching Architecture (Valkey / Redis)

Bifrost incorporates native vector caching to eliminate redundant inference calls:
- **Direct Cache (Exact Match):** Uses deterministic SHA-256 hash over prompt and hyper-parameters with `dimension: 1`.
- **Semantic Cache:** Generates embeddings and evaluates cosine similarity against previous prompts.

### A. Configuration in `config.json`
```json
"vector_store": {
  "enabled": true,
  "type": "redis",
  "config": {
    "addr": "env.VALKEY_ADDR",
    "password": "env.VALKEY_PASSWORD",
    "db": 0,
    "use_tls": false
  }
}
```

### B. Operational Parameters
- **Similarity Threshold:** Recommended `0.85` (values below 0.80 cause semantic false positives; above 0.90 reduce cache hit rates).
- **TTL:** Default 300 seconds; caller can override per-request via `x-bf-cache-ttl: 3600`.
- **Custom Cache Keys:** Caller can segregate cache namespaces via `x-bf-cache-key: tenant-namespace-id`.

---

## 5. Model Context Protocol (MCP) Gateway & Autonomous Agent Mode

Bifrost functions as an enterprise MCP Aggregator and Gateway:
1. **Unified Endpoint:** `POST /mcp` accepts standard JSON-RPC 2.0 requests and multiplexes to configured MCP servers (e.g. FreeLLMAPI MCP, filesystem, databases).
2. **Autonomous Agent Mode (`tools_to_auto_execute`):**
   - When configured, the Bifrost Go daemon intercepts LLM tool calls matching `tools_to_auto_execute`, executes them directly against the MCP client, feeds outputs back into the LLM context, and iterates autonomously up to `max_agent_depth` (default 10 rounds).
   - This relieves client SDKs and agents from building custom tool execution loops.
3. **Configuration Schema:**
   ```json
   "mcp": {
     "client_configs": [
       {
         "name": "freellmapi-mcp",
         "connection_type": "http",
         "connection_string": "http://freellmapi:3001/mcp",
         "tools_to_execute": ["*"],
         "tools_to_auto_execute": ["list_models", "provider_health", "usage_summary"]
       }
     ],
     "tool_manager_config": {
       "max_agent_depth": 10,
       "tool_execution_timeout": "30s"
     }
   }
   ```

---

## 6. Client-Agnostic Connection Patterns (Open Protocols)

### Pattern 1: Universal cURL (OpenAI-Compatible)
```bash
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${BIFROST_VIRTUAL_KEY}" \
  -d '{
    "model": "llama-3.3-70b-versatile",
    "messages": [
      {"role": "user", "content": "Explain deterministic software architecture."}
    ],
    "temperature": 0.2
  }'
```

### Pattern 2: Universal Python Client (Standard OpenAI SDK)
```python
import os
from openai import OpenAI

# Any Python agent, worker, or script connects without vendor lock-in
client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL", "http://localhost:8080/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "")
)

response = client.chat.completions.create(
    model="qwen2.5-coder-32b-instruct",
    messages=[{"role": "user", "content": "Refactor this function."}],
    temperature=0.0
)
print(response.choices[0].message.content)
```

### Pattern 3: Universal TypeScript / Node.js Streaming Client
```typescript
import OpenAI from "openai";

const ai = new OpenAI({
  baseURL: process.env.OPENAI_BASE_URL || "http://localhost:8080/v1",
  apiKey: process.env.OPENAI_API_KEY,
});

async function runInference(prompt: string) {
  const stream = await ai.chat.completions.create({
    model: "llama-3.3-70b-versatile",
    messages: [{ role: "user", content: prompt }],
    stream: true,
  });

  for await (const chunk of stream) {
    process.stdout.write(chunk.choices[0]?.delta?.content || "");
  }
}
```

### Pattern 4: Universal Anthropic Wire Protocol
```bash
curl -X POST http://localhost:8080/anthropic/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${BIFROST_VIRTUAL_KEY}" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello via Bifrost Gateway."}]
  }'
```

### Pattern 5: Generic Terminal & Coding Agent Environment Configuration
Any terminal agent or CLI tool adhering to standard environment variables connects immediately:
```bash
export OPENAI_BASE_URL="http://localhost:8080/v1"
export OPENAI_API_KEY="${BIFROST_VIRTUAL_KEY}"
export ANTHROPIC_BASE_URL="http://localhost:8080/anthropic"
export ANTHROPIC_API_KEY="${BIFROST_VIRTUAL_KEY}"
```

### Pattern 6: Dual-Tier Predictive Intent Routing & Zero-Leak CEL
Clients can pass intent headers to immediately route to Pro without testing FreeLLMAPI:
```typescript
// Client-side predictive dispatch for WhatsApp Bots or Autonomous Workers
const isTransactional = /comprar|precio|pago|ticket|reserva|orden|reclam/i.test(userText) || hasActiveTools;

const response = await fetch("http://bifrost:8080/v1/chat/completions", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${BIFROST_VIRTUAL_KEY}`,
    ...(isTransactional ? { "x-force-deepseek": "true", "x-tier": "pro" } : {})
  },
  body: JSON.stringify({
    model: isTransactional ? "deepseek-chat" : "llama-3.3-70b-versatile",
    messages: conversationMessages,
    temperature: 0.1
  })
});
```

---

## 6. Bifrost CLI (@maximhq/bifrost-cli v1.0.1) Operational Guide

The `@maximhq/bifrost-cli` utility serves as the administrative bridge for managing Virtual Keys, inspecting circuit breaker status, and performing real-time inference probes.

### A. Installation & Binary Architecture
The npm package installs a bootstrap downloader at `/usr/bin/bifrost` that fetches the compiled Go binary into `~/.bifrost/bin/bifrost` on its first invocation.

```bash
# Global installation and first-run native binary hydration
sudo npm install -g @maximhq/bifrost-cli
/usr/bin/bifrost --help >/dev/null 2>&1 || true

# Symlink native Go binary to global PATH
sudo ln -sf "$HOME/.bifrost/bin/bifrost" /usr/local/bin/bifrost
sudo ln -sf "$HOME/.bifrost/bin/bifrost" /usr/local/bin/bifrost-cli
```

### B. Common CLI Operations
```bash
# 1. Health check & cluster status probe
curl -s http://bifrost:8080/healthz

# 2. Virtual Keys listing via Management API
curl -s -H "Authorization: Bearer $BIFROST_ADMIN_KEY" \
  http://bifrost:8080/api/governance/virtual-keys

# 3. Test inference via drop-in curl with zero-leak routing
curl -s -X POST http://bifrost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PROD_VIRTUAL_KEY" \
  -d '{
    "model": "llama-3.3-70b-versatile",
    "messages": [{"role": "user", "content": "Ping Bifrost"}]
  }'
```

---

## 7. Error Handling & Wire Catalog

| HTTP Status | Wire Error Type | Root Cause | Gateway Behavior | Remediation Action |
|---|---|---|---|---|
| **400 Bad Request** | `missing_required_headers` | Mandated governance headers are absent. | Blocked at edge pre-hook. | Provide required headers. |
| **401 Unauthorized** | `unauthorized` | Missing, invalid, or expired Virtual Key. | Rejected immediately. | Provide valid `sk-bf-*` Virtual Key. |
| **402 Payment Required** | `payment_required` | Upstream provider credits exhausted. | Rotates key without backoff. | Replenish upstream account balance. |
| **403 Forbidden** | `model_not_allowed` | Model not permitted by Virtual Key allow-list. | Blocked by governance engine. | Update `allowed_models` to `["*"]` or add model. |
| **429 Too Many Requests**| `rate_limit_error` | Upstream rate limit reached. | Rotates to fallback upstream. | Bifrost failover redirects to Pro or sibling key. |
| **429 Too Many Requests**| `budget_exceeded` | Virtual Key budget cap reached. | Hard block by governance engine. | Increase budget allocation in `config.json`. |
| **502 Bad Gateway** | `upstream_credentials_exhausted` | All configured upstream keys failed. | Aborts retries; returns 502. | Verify upstream provider availability and keys. |
| **503 / 504 Timeout** | `gateway_timeout` | Upstream timeout or connection dropped. | Retries up to `max_retries`, then triggers fallbacks. | Check network connectivity to upstreams. |

---

## 8. Common Anti-Patterns

- **Anti-Pattern 1: Empty Array in Key Configuration**: Setting `{"models": []}`. In v2.0 semantics, this blocks all models. Use `["*"]`.
- **Anti-Pattern 2: Client Direct Upstream Key Bypass**: Sending raw provider keys directly to Bifrost. All requests require Virtual Keys.
- **Anti-Pattern 3: Unbounded Semantic Cache Threshold**: Setting cosine threshold to `<0.75` causes false positive cache hits. Keep between `0.85` and `0.90`.
- **Anti-Pattern 4: Premature Paid Routing & Missing Circuit Breakers**: Diverting coding or reasoning requests directly to commercial tiers like DeepSeek based on model name strings instead of utilizing FreeLLMAPI ($0 pool across 12 keys). Always enforce Inverted Zero-Leak CEL Routing (Priority 1: `true` -> FreeLLMAPI, Priority 0: explicit bypass `x-force-deepseek: true`) coupled with a 60s circuit breaker to eliminate both token expenditure leaks and cascading 429 timeouts.

# FreeLLMAPI — Developer, Agent & Client Usage Manual (v2026.09)

## 1. Architectural Surface & Wire Protocols

FreeLLMAPI (`tashfeenahmed/freellmapi`) is a local-first, multi-provider AI proxy and aggregation gateway. It coalesces 34+ free LLM provider tiers (635+ model endpoints) behind a single OpenAI-compatible API surface with automatic failover, per-key quota tracking, and AES-256-GCM encrypted key storage.

### Connection Architecture
- **Unified Base URL**: `http://<freellmapi-host>:3001/v1`
- **Native Wire Surfaces**:
  - `/v1/chat/completions`: Drop-in OpenAI Chat Completions (streaming SSE, tool calling, JSON schema, vision).
  - `/v1/completions`: Ghost-text autocomplete for IDEs and editor extensions.
  - `/v1/models`: Consolidated live model catalog reflecting active provider health.
  - `/v1/messages`: Anthropic Messages API wire protocol for Claude Code and Anthropic SDKs.
  - `/v1beta/*`: Google GenAI REST protocol for Gemini CLI.
  - `/mcp`: Model Context Protocol (MCP) JSON-RPC 2.0 / SSE server for AI agent introspection.
  - `/api/ping`: Lightweight unauthenticated liveness probe (HTTP 200 OK).
  - `/api/status`: Operational health, active provider connections, and cooldown counters.
- **Authentication**: Authenticate all `/v1/*` requests using the unified bearer token:
  ```http
  Authorization: Bearer freellmapi-<unified-key>
  ```

---

## 2. Smart Routing Strategies & Virtual Models

FreeLLMAPI implements dynamic multi-metric scoring across speed, intelligence, and recent success rates. In any request, the `model` parameter can specify either an explicit model ID (e.g. `gemini-2.5-flash`, `groq/llama-3.3-70b-versatile`) or a routing directive:

| Directive | Selection Logic | Best Use Case |
|---|---|---|
| `auto` | Traverses the user-defined fallback chain in priority order. | General-purpose tasks and scripts. |
| `auto:smart` | Ranks models by intelligence and reasoning benchmarks. | Complex multi-step reasoning, architectural planning. |
| `auto:fast` | Prioritizes minimal Time-To-First-Byte (TTFT) and high token throughput. | Real-time chat, autocomplete, interactive terminal loops. |
| `auto:reliable` | Filters strictly for providers with 100% success rate over the last 15 minutes. | Mission-critical automations, automated test execution. |
| `auto:balanced` | Blends throughput, intelligence, and headroom under quotas. | Standard default for coding agents. |
| `fusion` | Fans prompt out to 3 distinct models in parallel; a judge synthesizes the final response. | High-ambiguity queries and consensus-driven answers. |

### Sticky Sessions & Context Handoff
When a provider quota is exhausted mid-session (HTTP 429), FreeLLMAPI rotates to the next healthy provider in the chain. To prevent conversational discontinuity:
- Provide an `X-Session-Id: <uuid>` header to maintain sticky model affinity for up to 30 minutes.
- Enable `FREELLMAPI_CONTEXT_HANDOFF=on_model_switch` to inject a compact, non-intrusive system briefing informing the incoming model of the previous assistant context.

---

## 3. Full Method Matrix & Wire Endpoints

| Endpoint | HTTP Method | Request Wire Spec | Headers | Purpose |
|---|---|---|---|---|
| `/v1/chat/completions` | `POST` | OpenAI Chat Completion spec | `Authorization: Bearer freellmapi-*`, `X-Session-Id` | High-performance inference across 34 free provider pools |
| `/v1/completions` | `POST` | OpenAI Text Completion spec | `Authorization: Bearer freellmapi-*` | Code completion and ghost-text streaming |
| `/v1/models` | `GET` | None | `Authorization: Bearer freellmapi-*` | Live catalog of active models and quotas |
| `/v1/messages` | `POST` | Anthropic Messages spec | `x-api-key: freellmapi-*`, `anthropic-version` | Native wire bridge for Claude Code and Anthropic clients |
| `/v1beta/models/*` | `POST` | Google GenAI REST spec | `x-goog-api-key: freellmapi-*` | Native wire bridge for Gemini CLI |
| `/mcp` | `POST` / `SSE` | JSON-RPC 2.0 (MCP Protocol) | `Authorization: Bearer freellmapi-*` | Model Context Protocol gateway for coding agents |
| `/api/ping` | `GET` | None | None | Instant zero-overhead liveness probe (HTTP 200 OK) |
| `/api/status` | `GET` | None | None | Detailed provider health, quotas, and cooldowns |

---

## 4. Production Patterns & Verified Code Recipes

### Pattern 1: High-Performance cURL with Smart Routing & Session Persistence
```bash
curl -s -X POST http://localhost:3001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer freellmapi-prod-unified-token" \
  -H "X-Session-Id: task-infra-deploy-001" \
  -d '{
    "model": "auto:smart",
    "messages": [
      {"role": "system", "content": "You are a senior systems architect."},
      {"role": "user", "content": "Explain zero-downtime database migration patterns."}
    ],
    "temperature": 0.2,
    "stream": false
  }'
```

### Pattern 2: Python OpenAI SDK Drop-In Override with Streaming
```python
import os
from openai import OpenAI

client = OpenAI(
    base_url=os.environ.get("FREELLMAPI_BASE_URL", "http://localhost:3001/v1"),
    api_key=os.environ.get("FREELLMAPI_KEY", "freellmapi-prod-unified-token"),
    default_headers={"X-Session-Id": "python-worker-session"}
)

response_stream = client.chat.completions.create(
    model="auto:balanced",
    messages=[
        {"role": "system", "content": "You are an expert Go and TypeScript developer."},
        {"role": "user", "content": "Implement an exponential backoff retry loop in Go."}
    ],
    temperature=0.1,
    stream=True
)

for chunk in response_stream:
    delta = chunk.choices[0].delta.content or ""
    print(delta, end="", flush=True)
print()
```

### Pattern 3: Node.js / TypeScript Streaming Client with Tool Calling
```typescript
import OpenAI from "openai";

const freellm = new OpenAI({
  baseURL: process.env.FREELLMAPI_BASE_URL || "http://localhost:3001/v1",
  apiKey: process.env.FREELLMAPI_KEY || "freellmapi-prod-unified-token",
});

async function executeAgentToolCall() {
  const runner = await freellm.chat.completions.create({
    model: "auto:smart",
    messages: [
      { role: "user", content: "Check status of service api-gateway." }
    ],
    tools: [
      {
        type: "function",
        function: {
          name: "get_service_status",
          description: "Get real-time operational status of an infrastructure service",
          parameters: {
            type: "object",
            properties: {
              serviceName: { type: "string" }
            },
            required: ["serviceName"]
          }
        }
      }
    ]
  });

  const message = runner.choices[0].message;
  if (message.tool_calls && message.tool_calls.length > 0) {
    console.log("Rescued Tool Call:", JSON.stringify(message.tool_calls, null, 2));
  } else {
    console.log("Response:", message.content);
  }
}

executeAgentToolCall().catch(console.error);
```

### Pattern 4: Agent & Tool One-Command Auto-Configuration
FreeLLMAPI provides automated non-destructive CLI generators to wire environment variables and configuration files for upstream agents and CLI tools:
```bash
# Export the unified API key
export FREELLMAPI_API_KEY="freellmapi-prod-unified-token"

# Generate configuration for Anthropic-compatible wire protocols
npx freellmapi setup-claude --url http://localhost:3001 --dry-run
npx freellmapi setup-claude --url http://localhost:3001

# Generate configuration for OpenAI-compatible wire protocols
npx freellmapi setup-codex --url http://localhost:3001/v1
npx freellmapi setup-aider --url http://localhost:3001/v1

# Launch ephemeral zero-persistence session (no keys written to disk)
npx freellmapi launch
```

### Pattern 5: Model Context Protocol (MCP) Integration
FreeLLMAPI exposes a native Model Context Protocol (MCP) server at `/mcp` over HTTP/SSE, allowing coding agents and orchestrators to inspect active provider health, model quotas, and runtime latency:
```bash
# Register FreeLLMAPI MCP endpoint in an agent environment
# Endpoint: http://localhost:3001/mcp
curl -s -X POST http://localhost:3001/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer freellmapi-prod-unified-token" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
  }'
```

---

## 5. Error Catalog, Edge Cases & Remediation

| HTTP Status | Error Code | Root Cause | Gateway Behavior | Remediation Action |
|---|---|---|---|---|
| **400 Bad Request** | `invalid_model_directive` | Unrecognized routing strategy or invalid model name. | Request rejected before provider dispatch. | Use canonical `auto`, `auto:smart`, `auto:fast`, or valid model family name. |
| **401 Unauthorized** | `invalid_unified_key` | Missing or incorrect `Bearer freellmapi-...` token. | Request rejected immediately. | Check `Authorization: Bearer` header against unified key in dashboard. |
| **429 Too Many Requests** | `all_providers_exhausted` | All free provider pools exceeded daily/minute quotas simultaneously. | Keys placed in temporary cooldown; fails over down chain. | Add backup providers via `FREEAPI_CONFIG_JSON` or route via Bifrost failover. |
| **502 Bad Gateway** | `provider_upstream_error` | Upstream provider API returned 5xx or connection was severed. | Retried up to 3 times on alternative providers before failing. | Inspect `/api/status` for provider health; verify outbound DNS/network. |
| **503 Service Unavailable** | `no_healthy_keys` | Zero active API keys configured or decrypted in database. | Request rejected at routing layer. | Supply provider keys in dashboard or declare them via `FREEAPI_CONFIG_JSON`. |
| **504 Gateway Timeout** | `upstream_timeout` | Upstream provider took longer than configured request timeout. | Request terminated; provider marked for cooldown. | Increase timeout or switch routing directive to `auto:fast`. |

---

## 6. Common Anti-Patterns & Operational Gotchas

- **Anti-Pattern 1: Missing Encryption Key on Restart**:
  - Running container without persistent `ENCRYPTION_KEY`.
  - *Consequence*: Database decrypt fails; all stored provider keys become permanently unreadable.
  - *Fix*: Fix `ENCRYPTION_KEY` in Zerops environment variables and never rotate without `npm run rotate-encryption-key`.
- **Anti-Pattern 2: Binding Exclusively to Loopback in Containers**:
  - Setting `HOST_BIND=127.0.0.1` inside Docker or Zerops container.
  - *Consequence*: Container cannot receive traffic from sibling services (e.g. Bifrost or AGY).
  - *Fix*: Always set `PORT=3001` and bind to `0.0.0.0` for inter-service communication in Zerops private networks.
- **Anti-Pattern 3: Passing Raw Upstream Keys to Clients**:
  - Giving developers direct keys from Groq, Cerebras, or Google AI Studio.
  - *Consequence*: Bypasses central quota tracking, eliminates automatic failover, and exposes raw credentials.
  - *Fix*: Hand out only the unified `freellmapi-...` token; manage upstream keys centrally via declarative config.

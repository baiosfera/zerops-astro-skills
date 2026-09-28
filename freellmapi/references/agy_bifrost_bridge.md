# FreeLLMAPI, Bifrost & Agent Ecosystem — Integrated Bridge Manual (v2026.09)

## 1. Unified Single Front Door Gateway Topology

This manual establishes the operational contract connecting **Maxim AI Bifrost** (Central Enterprise AI Gateway & Single Front Door), **FreeLLMAPI** (Free Tier Inference Aggregator Upstream), and **Pro Provider Slot** (Commercial Upstream) inside Zerops ZCP.

### Architectural Layout:
1. **Central Front Door: Maxim AI Bifrost (`bifrost:8080`)**
   - Single point of entry for all incoming inference traffic across the ecosystem (`bifrost:8080/v1`).
   - Clients never bypass Bifrost to communicate directly with backend providers.
   - Adds negligible gateway latency (<100µs).
   - Enforces Virtual Keys (`sk-bf-*`), rate limits, semantic vector caching (Valkey/Redis), Prometheus metrics, and CEL adaptive routing.
2. **Upstream 1: FreeLLMAPI (`freellmapi:3001/v1`)**
   - Internal inference aggregator serving 34+ free tier providers (Cerebras, Groq, OpenCode, OpenRouter Free, HuggingFace, Ollama, Google AI Studio, Aisa One).
   - Manages dynamic sliding-window rate tracking, token quotas, and automatic 429 failover across free pools.
3. **Upstream 2: Pro Provider Slot (Commercial API)**
   - Configured in Bifrost as secondary upstream for guaranteed SLA and fallback when free tiers exhaust.
4. **Clients & Consumers (Agnostic AI Agents, CLI Tools & Microservices)**
   - Any AI agent, autonomous worker, or platform microservice connects exclusively to Bifrost's OpenAI-compatible (`/v1`), Anthropic-compatible (`/anthropic/v1`), or MCP (`/mcp`) endpoints.

---

## 2. Bifrost Configuration for FreeLLMAPI Upstream

In Bifrost's production declarative configuration file (`config.json` version 2), define `freellmapi` as an OpenAI-compatible custom provider:

```json
{
  "$schema": "https://www.getbifrost.ai/schema",
  "version": 2,
  "providers": {
    "freellmapi": {
      "keys": [
        {
          "name": "freellmapi-primary-pool",
          "value": "env.FREELLMAPI_UNIFIED_KEY",
          "models": ["*"],
          "weight": 1.0
        }
      ],
      "network_config": {
        "base_url": "http://freellmapi:3001/v1",
        "default_request_timeout_in_seconds": 120,
        "max_retries": 3,
        "retry_backoff_initial": 500,
        "retry_backoff_max": 3000
      },
      "custom_provider_config": {
        "base_provider_type": "openai",
        "allowed_requests": {
          "chat_completion": true,
          "chat_completion_stream": true
        }
      }
    },
    "openai-commercial": {
      "keys": [
        {
          "name": "openai-backup-key",
          "value": "env.OPENAI_API_KEY",
          "models": ["*"],
          "weight": 1.0
        }
      ]
    }
  },
  "governance": {
    "virtual_keys": [
      {
        "id": "vk-agent-pool",
        "name": "antigravity-agent-key",
        "value": "env.AGENT_VIRTUAL_KEY",
        "is_active": true,
        "provider_configs": [
          {
            "provider": "freellmapi",
            "allowed_models": ["*"],
            "key_ids": ["*"],
            "weight": 1.0
          },
          {
            "provider": "openai-commercial",
            "allowed_models": ["*"],
            "key_ids": ["*"],
            "weight": 0.0
          }
        ]
      }
    ],
    "routing_rules": [
      {
        "id": "rule-freellm-zero-cost-priority",
        "name": "Prioritize FreeLLMAPI with Paid Commercial Failover",
        "cel_expression": "true",
        "targets": [
          {
            "provider": "freellmapi",
            "weight": 1.0
          }
        ],
        "fallbacks": [
          "openai-commercial"
        ]
      }
    ]
  }
}
```

---

## 3. Client & Agent Open-Protocol Bridge

### Method A: Model Context Protocol (MCP) Server Registration
FreeLLMAPI natively exposes an MCP endpoint allowing upstream agents and orchestrators to introspect active providers, quotas, and model health in real-time:
```bash
# Test MCP endpoint connectivity
curl -s -X POST http://freellmapi:3001/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer freellmapi-prod-unified-token" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}'
```

### Method B: Environment Variable Redirection for Agents (Bifrost Front Door)
All agents, workers, and tools executing inside containers or workflows point exclusively to Bifrost:
```bash
# Point agents through Bifrost Gateway (Single Front Door)
export OPENAI_BASE_URL="http://bifrost:8080/v1"
export OPENAI_API_KEY="sk-bf-antigravity-key"

# For Anthropic wire protocol clients:
export ANTHROPIC_BASE_URL="http://bifrost:8080/anthropic/v1"
export ANTHROPIC_API_KEY="sk-bf-antigravity-key"
```

### Method C: Zero-Touch Declarative Ingestion via `setup-keys.sh`
To inject existing ecosystem credentials into FreeLLMAPI on startup without manual UI interaction:
1. Credentials from `/var/www/baiosfera/0ZEROPS-AGY/0zcp-123/apis/baiosfera_freellm.md` are mapped to `FREEAPI_CONFIG_JSON`.
2. FreeLLMAPI parses the configuration on boot and updates the encrypted SQLite database idempotently.

---

## 4. End-to-End Verification & Health Sensor

Test the complete chain from client through Bifrost down to FreeLLMAPI:

```bash
# 1. Verify FreeLLMAPI health probe
timeout 5s curl -s -f http://localhost:3001/api/ping || exit 1

# 2. Verify Bifrost health probe
timeout 5s curl -s -f http://localhost:8080/health || exit 1

# 3. Perform end-to-end inference request via Bifrost
curl -s -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-bf-antigravity-key" \
  -d '{
    "model": "auto:smart",
    "messages": [{"role": "user", "content": "ping"}]
  }'
```
A successful response will carry the header `x-routed-via: <provider>/<model>` confirming that FreeLLMAPI served the request through a healthy free tier.

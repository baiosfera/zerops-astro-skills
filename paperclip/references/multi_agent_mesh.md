# Multi-Agent Mesh Integration Recipes for Paperclip

This document provides exact JSON configuration payloads, connection recipes, and architectural patterns for integrating every autonomous agent framework with Paperclip.

---

## 1. Hermes Agent Integration (`hermes_gateway`)

Nous Research Hermes acts as the **Chief of Staff & General Manager** within Paperclip. It communicates over an authenticated HTTP/SSE bridge to the Hermes daemon running on `http://hermes:8000`.

### Database Schema Registration
```sql
INSERT INTO agents (
  id, company_id, name, role, title, status, capabilities, adapter_type, adapter_config,
  budget_monthly_cents, spent_monthly_cents, runtime_config, permissions, lifecycle_state
) VALUES (
  '22222222-2222-2222-2222-222222222222',
  '<company_id>',
  'Hermes',
  'ceo',
  'Chief of Staff & Orchestrator',
  'idle',
  'Paperclip Gateway v1, CrewAI Runner, Multi-Agent Mesh Coordinator',
  'hermes_gateway',
  '{
    "apiBaseUrl": "http://hermes:8000",
    "apiKey": "hermes-internal-key",
    "dangerouslyAllowInsecureRemoteHttp": true,
    "sessionKeyStrategy": "issue",
    "timeoutSec": 600
  }'::jsonb,
  100000,
  0,
  '{"heartbeat": {"enabled": true, "intervalSec": 300, "cooldownSec": 10, "wakeOnDemand": true, "maxConcurrentRuns": 10, "skipTimerWhenNoActionableWork": true}}'::jsonb,
  '{"canCreateAgents": true, "canCreateSkills": true, "canHire": true}'::jsonb,
  'ready'
);
```

### Execution Flow (Outbound: Paperclip ➔ Hermes)
1. Paperclip sends `POST /v1/runs` with `{ input, prompt, issueId }`.
2. Hermes dispatches an asynchronous worker and returns `{ id: run_id, status: "running" }`.
3. Paperclip opens `GET /v1/runs/{run_id}/events` and streams SSE deltas (`message.delta`) directly into the Paperclip UI.
4. On finish, Hermes emits `run.completed` with token usage and cost in cents.

### Bidirectional Telemetry Bridge (Inbound: Hermes/Telegram ➔ Paperclip)
To prevent control plane blindness when users interact with Hermes via Telegram (outside Paperclip UI), Hermes integrates `paperclip_bridge.py`:
1. **Dynamic DB Discovery**: Hermes resolves Paperclip's PostgreSQL connection from `/mnt/localstorage/paperclip/instances/default/config.json`.
2. **Heartbeat Run Telemetry**: Each Telegram turn writes a completed execution to `heartbeat_runs` (`invocation_source: 'telegram'`, token usage, duration, exit code 0).
3. **Live Activity Stream**: Emits an audit event to `activity_log` (`action: 'agent.telegram_turn'`) with user prompt and response excerpt, appearing immediately on Paperclip's Dashboard.
4. **Heartbeat Stamp**: Updates `agents.last_heartbeat_at = NOW()` and `status = 'idle'`, maintaining live presence in Org Charts.
5. **Conversational Kanban Tools**: Hermes exposes `paperclip_list_tasks` and `paperclip_create_task` tools to inspect and create Paperclip issues directly from Telegram chat.

---

## 2. CrewAI Swarm Integration

CrewAI executes multi-agent polymorphic swarms (Researcher, Writer, Quality Analyst). There are two supported integration topologies:

### Option A: Via Hermes Gateway (Recommended — Zero Token Cost via Bifrost)
Hermes exposes native dynamic swarm compilation directly through its Gateway. In strict accordance with Observation #44 and `crewai-engine`, static `@CrewBase` squads are abolished in favor of programmatic assembly via `SwarmCompiler` and `DynamicSwarmSpec`. Agents are dynamically hydrated with any of the 83 sovereign skills via `SkillToolBridge`:
- Dynamic Swarms assembled on the fly per issue requirement (e.g., Researcher, Synthesizer, Code Reviewer).
- Zero-Token-Waste RAG ingestion via `TextFileKnowledgeSource` (chunk 2000, overlap 200).
- Pure $0 inference routed through Bifrost Gateway (`http://bifrost:8080/v1`) with Virtual Key `vk-crewai` (`openai/auto` with header `x-routing-tier: free`).

```json
{
  "apiBaseUrl": "http://hermes:8000",
  "apiKey": "hermes-internal-key",
  "dangerouslyAllowInsecureRemoteHttp": true,
  "headers": {
    "X-Engine": "crewai-dynamic-swarm"
  },
  "sessionKeyStrategy": "issue",
  "timeoutSec": 600
}
```

### Option B: Via Generic `process` Adapter
For independent Python CrewAI workers running directly in the environment:
```json
{
  "command": "python3",
  "args": ["-m", "crews.runner", "--task-id", "{{issueId}}"],
  "cwd": "/var/www/hermes",
  "env": {
    "OPENAI_API_BASE": "http://bifrost:8080/v1",
    "OPENAI_API_KEY": "bifrost-secret"
  },
  "timeoutSec": 900
}
```

---

## 3. Pi Coding Agent Integration (`pi_local`)

Pi is an elite coding agent specialized in fast code mutations, Astro 5 SSR, and TypeScript.

### Database Registration
```sql
INSERT INTO agents (
  id, company_id, name, role, title, status, reports_to, capabilities, adapter_type, adapter_config,
  budget_monthly_cents, spent_monthly_cents, runtime_config, permissions, lifecycle_state
) VALUES (
  '33333333-3333-3333-3333-333333333333',
  '<company_id>',
  'Pi Code Builder',
  'lead',
  'Senior Code Builder & Astro Engineer',
  'idle',
  '22222222-2222-2222-2222-222222222222',
  'Pi Coding Agent, Astro 5 SSR, Bun TypeScript, Fast Edits',
  'pi_local',
  '{
    "command": "pidev",
    "model": "bifrost/auto",
    "thinking": "medium",
    "stdoutLogMode": "compact",
    "env": {
      "OPENAI_BASE_URL": "http://bifrost:8080/v1",
      "OPENAI_API_KEY": "vk-bifrost",
      "HERMES_MODEL_ENDPOINT": "http://bifrost:8080/v1"
    },
    "timeoutSec": 600
  }'::jsonb,
  50000,
  0,
  '{"heartbeat": {"enabled": true, "intervalSec": 300, "cooldownSec": 10, "wakeOnDemand": true, "maxConcurrentRuns": 5, "skipTimerWhenNoActionableWork": true}}'::jsonb,
  '{"canCreateAgents": false, "canCreateSkills": true}'::jsonb,
  'ready'
);
```

### Key Parameters:
- `command`: "pidev" or "pi".
- `model`: Provider-qualified model identifier routed through Bifrost (e.g., `bifrost/auto`, `deepseek/deepseek-chat`, `bifrost/hermes-3-llama-3.1-8b`). All agent inference is grounded in `http://bifrost:8080/v1` to eliminate external vendor leakage.
- `thinking`: `off`, `low`, `medium`, `high`.
- `stdoutLogMode`: `"compact"` strips repetitive JSONL deltas to keep log size bounded.

---

## 4. Goose & Aider Integration (`process` + `@paperclipai/mcp-server`)

External CLI coding tools (Block Goose, Aider, OpenCode) integrate using the `process` adapter combined with the Paperclip MCP Server.

### Goose Configuration Payload
```json
{
  "command": "goose",
  "args": ["run", "--instruction", "{{prompt}}"],
  "cwd": "/var/www/webdev",
  "env": {
    "GOOSE_PROVIDER": "openai",
    "OPENAI_BASE_URL": "http://bifrost:8080/v1",
    "OPENAI_API_KEY": "bifrost-secret"
  },
  "timeoutSec": 1200
}
```

### Aider Configuration Payload
```json
{
  "command": "aider",
  "args": ["--yes", "--message", "{{prompt}}", "--openai-api-base", "http://bifrost:8080/v1"],
  "cwd": "/var/www/webdev",
  "timeoutSec": 1200
}
```

### Enabling MCP Tools for Goose/Aider
Both agents read standard MCP config from `~/.config/goose/config.yaml` or `.aider.conf.yml`:
```yaml
mcpServers:
  paperclip:
    command: "npx"
    args: ["@paperclipai/mcp-server"]
    env:
      PAPERCLIP_API_KEY: "{{agent_api_key}}"
      PAPERCLIP_URL: "http://paperclip:3100"
```
Through this MCP bridge, Goose and Aider automatically call `paperclipCheckoutIssue` to lock issues, `paperclipAddComment` for progress telemetry, `paperclipUpsertIssueDocument` for work products, and `paperclipUpdateIssue` to move tasks to review.

---

## 5. Generic Microservice / Webhook Integration (`http`)

For decoupled cloud agents, serverless functions, or proprietary external platforms:

```json
{
  "url": "http://my-agent-service:9000/run",
  "headers": {
    "Authorization": "Bearer external-service-token",
    "Content-Type": "application/json"
  },
  "timeoutSec": 300
}
```
Paperclip dispatches an HTTP POST payload containing:
```json
{
  "runId": "run_abc123",
  "companyId": "2c915432-4c84-4b01-b90b-ee7482147eef",
  "agentId": "uuid-here",
  "issue": {
    "id": "uuid-here",
    "identifier": "BAI-1",
    "title": "Task Title",
    "description": "Details"
  },
  "callbackUrl": "http://paperclip:3100/api/runs/run_abc123/complete"
}
```

---

## 6. Built-in Adapters Catalog & Grounding Invariants

Paperclip ships with dedicated adapters for autonomous coding tools:

| Adapter Name | Adapter Type | Execution Target | Grounding & Invariants |
|---|---|---|---|
| **Hermes Gateway** | `hermes_gateway` | HTTP/SSE bridge (`:8000`) | CEO & Chief of Staff. Routes runs asynchronously with live event streaming. |
| **Pi Coding Agent** | `pi_local` | Embedded CLI (`pidev`) | Bun/Astro 5 mutations. Strictly grounded in Bifrost (`http://bifrost:8080/v1`). |
| **CrewAI Runner** | `hermes_gateway` / `process` | Polymorphic dynamic swarm | Assembled via `SwarmCompiler` at $0 token cost via Bifrost (`vk-crewai`). |
| **Claude Local** | `claude_local` | Local `claude` CLI | Local CLI wrapper. Context isolated to workspace cwd. |
| **Codex Local** | `codex_local` | Local `codex` CLI | CLI executor. Reuses session continuity across heartbeats. |
| **OpenCode Local** | `opencode_local` | Local `opencode` CLI | Open-source coding CLI. |
| **OpenClaw Gateway**| `openclaw_gateway`| OpenClaw API endpoint | Remote gateway for web-native agent workflows. |
| **Generic Process** | `process` | Command-line execution | Executes arbitrary tools (Aider, Goose) with environment isolation. |
| **Generic HTTP** | `http` | Webhook HTTP POST | Cloud agent integration with callback contracts. |
| **Factory Droid** | `droid_local` | Plugin CLI adapter | External coding agent adapter (`@henkey/droid-paperclip-adapter`). |

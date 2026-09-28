# Dual-RAG Skill Templates & Production Standards (v7.0 — Fractal CoHaLo)

The **Dual-RAG Pattern** decouples operational knowledge into modular reference manuals so that LLM agents load only the required context slice without degrading the attention window.

---

## 1. Canonical Router Skeleton: `SKILL.md` (Target: 180 to 450 tokens)

```markdown
---
name: <target_name>
description: "<Concise description of the exact capabilities and scope in an affirmative sentence>. Trigger: <trigger1>, <trigger2>, <intent_phrases>."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.0"
---

# <Target_Title> — <Descriptive_Subtitle>

## Activation Contract
Activate strictly when <clear operational trigger condition>. Unrelated operational requests route to their respective specialized skills.

## Hard Rules (Positive Guidance)
- **Rule 1 (Zero Deletion & Signal Integrity)**: Preserve all domain algorithms, schemas, endpoints, and parameters via lossless offloading to references/.
- **Rule 2 (Fractal CoHaLo Bounded Execution)**: Commands execute with deterministic timeouts (`timeout 10s`), max synchronous wait (`WaitMsBeforeAsync: 10000`), and clean process termination via `manage_task action="kill"` for lingering background tasks.
- **Rule 3 (Circuit Breakers & Sensors)**: Consecutive retries are bounded to a maximum of 2 attempts before escalating; state attestation requires physical sensors (exit code 0 / HTTP 200).

## Decision Gates

| Use Case / Requirement | Action / Pattern | Reference / Asset |
|---|---|---|
| Method Signatures & Types | Client setup, method matrices, schemas | [`references/usage.md`](references/usage.md) |
| Production Recipes & Examples | End-to-end production workflows | [`references/usage.md`](references/usage.md) |
| Physical Validation Sensor | Standard deterministic sensor checks | [`scripts/<target>-validate.sh`](scripts/<target>-validate.sh) |

## Critical Workflows / Execution Steps
1. Validate required parameters and consult [`references/usage.md`](references/usage.md).
2. **Process Hygiene & Bounded Execution (CoHaLo)**: Execute commands with `timeout 10s`, `WaitMsBeforeAsync: 10000`, and clean orphan tasks with `manage_task action="kill"`.
3. **Circuit Breakers (CoHaLo)**: Limit retries to 2 attempts on failure (HTTP 500/timeout) before human escalation.
4. **Sensor Attestation**: Verify physical sensor check (exit code 0 / HTTP 200) and format output deterministically.

## Output Contract
- Deterministic response or JSON artifact matching schemas in [`references/usage.md`](references/usage.md).
- Status verification metric and clean execution state.

## References
- [`references/usage.md`](references/usage.md) — Method matrices, type interfaces, production patterns, error handling, and domain specifications.
- [`scripts/<target>-validate.sh`](scripts/<target>-validate.sh) — Deterministic physical validation sensor (0 tokens, < 50ms).
```

---

## 2. Canonical Usage Manuals: `references/usage.md` (By Archetype)

### Archetype A: Code & SDK Frameworks
```markdown
# <Target> — Developer & Agent Usage Manual

## 1. Client Initialization & Setup
Configuration, connection options, and authentication across TypeScript / Python:

```typescript
import { createClient } from '<target-sdk>';

export const client = createClient({
  apiKey: process.env.TARGET_API_KEY!,
  timeout: 10000,
  maxRetries: 2,
});
```

## 2. Method Signatures & Type Interfaces

| Method / Endpoint | Parameters | Return Type | Description |
|---|---|---|---|
| `client.execute(params)` | `params: ExecParams` | `Promise<ExecResult>` | Primary execution operation |
| `client.status(id)` | `id: string` | `Promise<StatusResult>` | Status query operation |

### Type Definitions
```typescript
export interface ExecParams {
  id: string;
  mode?: 'sync' | 'async';
}

export interface ExecResult {
  success: boolean;
  code: number;
  data: Record<string, unknown>;
}
```

## 3. Production Patterns & Recipes
1. **Basic Execution Pattern**: Standard initialization, execution, and error handling.
2. **Async Polling / Webhook Pattern**: Webhook registration and payload processing.
3. **Batch Processing Pattern**: Concurrent batch worker with rate limiting.
4. **Resilient Retry Pattern**: Exponential backoff with jitter and 2-attempt circuit breaker.
5. **Streaming / High-Throughput Pattern**: Event-driven processing with backpressure.

## 4. Error Handling & Edge Cases

| Error Code | Root Cause | Remediation Strategy |
|---|---|---|
| `401 Unauthorized` | Invalid or expired credentials | Verify environment variable configuration |
| `429 TooManyRequests` | Rate limit ceiling reached | Apply exponential backoff with jitter |
| `502 BadGateway` | Upstream service restarting | Halt after 2 attempts; report failure |

## 5. Best Practices & Invariants
- Reference credentials by variable name (`$TARGET_API_KEY`), avoiding plaintext tokens.
- Bound all external operations with explicit timeouts (`timeout 10s`).
```

### Archetype B: Domain Engines & REST Calculation Motors
```markdown
# <Target> — Domain Engine & REST Calculation Manual

## 1. API Endpoints & Request Contracts
Base URL and authentication headers:
- Base URL: `https://api.<target>.example/v1`
- Auth Header: `Authorization: Bearer $TARGET_API_KEY`
- Rate Limits: 100 requests/minute

| Endpoint | HTTP Method | Description |
|---|---|---|
| `/calculate` | POST | Primary calculation engine |
| `/query` | GET | Lookup domain parameters |

## 2. Input Parameter Schemas & Tolerances

| Parameter | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `target_id` | String | Yes | Alphanumeric | Target resource identifier |
| `timestamp` | Number | Yes | Unix epoch (seconds) | Reference temporal anchor |
| `precision` | String | No | `high` / `standard` | Calculation accuracy level |

## 3. Response Schemas & Precision Rules
Outputs adhere strictly to validated numerical and astronomical models without truncation.

## 4. Error Handling & Failovers
Halt requests upon quota exhaustion and route to secondary engines with exit status logging.
```

---

## 3. Canonical Infrastructure & Ops Manual: `references/infra.md` (Platform Archetype Only)

> **Note:** Generate `references/infra.md` *strictly* for Infrastructure services or long-running Framework services. Domain calculation APIs and cognitive skills omit this file.

```markdown
# <Target> — Infrastructure & Deployment Manual

## 1. Zerops & Container Specifications
- **Service Type**: Native LXC (`type: nodejs@...`, `type: python@...`) or Docker VM (`type: docker@...`).
- **Scaling Mode**: Elastic autoscaling (`min < max`) for Native LXC; Fixed (`min == max`) for Docker VM.
- **Listening Ports**: Internal listening port (e.g. `3000/TCP`, `8000/TCP`) and public routing domain.

## 2. Environment Variables (.env Dictionary)

| Variable Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `PORT` | Number | Yes | `3000` | HTTP service listening port |
| `DATABASE_URL` | String | Yes | — | Upstream database connection string |
| `LOG_LEVEL` | String | No | `info` | Logging verbosity (`debug`, `info`, `warn`, `error`) |

## 3. Persistent Storage & Permission Shields
- **Mount Path**: `/mnt/<storageHostname>/<service>/`
- **FUSE Permission Safeguard**:
```bash
chmod -R 777 /mnt/<storageHostname>/<service>/
```

## 4. Lifecycle Commands (`zerops.yaml`)
```yaml
zerops:
  - setup: <hostname>
    build:
      base: nodejs@22
      prepareCommands:
        - sudo apt-get update && sudo apt-get install -y curl
      buildCommands:
        - npm ci
        - npm run build
      deployFiles:
        - dist/
        - package.json
        - node_modules/
    run:
      base: nodejs@22
      startCommands:
        - npm start
      healthCheck:
        httpGet:
          port: 3000
          path: /healthz
```

## 5. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)
- Execute commands with strict bounds: `timeout 10s curl -s -f http://localhost:3000/healthz`
- Circuit Breaker: On consecutive HTTP 500 or timeout errors, halt execution at 2 retries and report to human operator.
- Terminate lingering background tasks with `manage_task action="kill"`.
```

---

## 4. Canonical Physical Validation Sensor: `scripts/<target>-validate.sh` (Standard v3.0)

Every generated or refactored skill MUST include its own deterministic validation sensor at `scripts/<target>-validate.sh`.
The sensor executes in CPU native Bash (< 50ms), consumes **0 LLM tokens**, uses **in-memory AST parsing** (0 `__pycache__`), and enforces hard structural, syntactic, and budget contracts:

```bash
#!/usr/bin/env bash
# ==============================================================================
# Deterministic Physical Validation Sensor for Agent Skills (Standard v3.0)
# Zero LLM Tokens | Bounded Execution < 100ms | 100% Deterministic
# ==============================================================================
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_NAME="$(basename "$SKILL_DIR")"
ERRORS=0

echo "============================================================"
echo "  🔍 Validating Skill Integrity: [$SKILL_NAME]"
echo "============================================================"

# 1. Structural & Dual-RAG Packaging Integrity
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "❌ Missing required SKILL.md in $SKILL_DIR"
    ERRORS=$((ERRORS + 1))
else
    echo "✓ SKILL.md exists"
fi

# 2. Frontmatter Metadata Verification
if grep -q '^name: ' "$SKILL_DIR/SKILL.md" && \
   grep -q '^description: ' "$SKILL_DIR/SKILL.md" && \
   grep -q 'version: ' "$SKILL_DIR/SKILL.md"; then
    echo "✓ Valid YAML frontmatter metadata (name, description, version)"
else
    echo "❌ Malformed frontmatter in SKILL.md (missing name, description, or version)"
    ERRORS=$((ERRORS + 1))
fi

# 3. Dual-RAG References Non-Emptiness Check
if [ -d "$SKILL_DIR/references" ]; then
    for ref_file in "$SKILL_DIR/references/"*.md; do
        if [ -f "$ref_file" ]; then
            if [ ! -s "$ref_file" ]; then
                echo "❌ Empty reference file detected: $(basename "$ref_file")"
                ERRORS=$((ERRORS + 1))
            fi
        fi
    done
    echo "✓ All reference files in references/ are non-empty"
fi

# 4. Clean-Room Bytecode Hygiene Verification
if find "$SKILL_DIR" -name "__pycache__" -o -name "*.pyc" 2>/dev/null | grep -q .; then
    echo "❌ Clean-room hygiene error: bytecode cache detected (__pycache__ or *.pyc)"
    ERRORS=$((ERRORS + 1))
else
    echo "✓ Clean-room hygiene verified: zero bytecode cache in skill tree"
fi

# 5. Deterministic Syntax Compilation (Fail-Fast, Zero Disk Writes)
if [ -d "$SKILL_DIR/scripts" ]; then
    for sh_file in "$SKILL_DIR/scripts/"*.sh; do
        if [ -f "$sh_file" ]; then
            if bash -n "$sh_file" >/dev/null 2>&1; then
                echo "✓ Bash syntax valid: $(basename "$sh_file")"
            else
                echo "❌ Bash syntax error in $(basename "$sh_file")"
                ERRORS=$((ERRORS + 1))
            fi
        fi
    done
    for py_file in "$SKILL_DIR/scripts/"*.py; do
        if [ -f "$py_file" ]; then
            if python3 -c "import ast; ast.parse(open('$py_file').read())" >/dev/null 2>&1; then
                echo "✓ Python AST valid: $(basename "$py_file")"
            else
                echo "❌ Python syntax error in $(basename "$py_file")"
                ERRORS=$((ERRORS + 1))
            fi
        fi
    done
fi

# 6. Physical Link Integrity (Zero Broken Links)
while IFS= read -r link; do
    clean_path="${link#file://}"
    if [ -z "${clean_path#/}" ]; then
        continue
    fi
    if [ ! -e "$clean_path" ]; then
        echo "❌ Broken physical link in SKILL.md: $link (target does not exist)"
        ERRORS=$((ERRORS + 1))
    fi
done < <(grep -oE 'file:///[^ )"`]+' "$SKILL_DIR/SKILL.md" 2>/dev/null || true)
echo "✓ Physical file:/// links resolved and verified on filesystem"

# 7. Context Token Budget Guardrail (Router Protection)
WORD_COUNT=$(wc -w < "$SKILL_DIR/SKILL.md")
EST_TOKENS=$((WORD_COUNT * 13 / 10))
echo "• SKILL.md budget check: $WORD_COUNT words (~$EST_TOKENS tokens)"
if [ "$EST_TOKENS" -gt 2500 ]; then
    echo "❌ SKILL.md exceeds hard ceiling of 2500 tokens (~$EST_TOKENS tokens). Offload deep content to references/!"
    ERRORS=$((ERRORS + 1))
elif [ "$EST_TOKENS" -gt 750 ]; then
    echo "⚠️ Notice: SKILL.md exceeds ideal budget of 750 tokens (~$EST_TOKENS tokens). Consider offloading to references/."
else
    echo "✓ SKILL.md within router token budget (<750 tokens)"
fi

# 8. Positive Guidance Verification
if grep -inE "Do NOT activate|Queda terminantemente prohibido" "$SKILL_DIR/references/"*.md 2>/dev/null | grep -v 'grep -inE'; then
    echo "❌ Legacy negative directives detected in references"
    ERRORS=$((ERRORS + 1))
else
    echo "✓ Positive guidance verified: zero legacy negative directives in references"
fi

echo "------------------------------------------------------------"
if [ "$ERRORS" -eq 0 ]; then
    echo "✅ Skill [$SKILL_NAME] passed physical validation (exit code 0)."
    exit 0
else
    echo "❌ Skill [$SKILL_NAME] validation failed with $ERRORS error(s)."
    exit 1
fi
```

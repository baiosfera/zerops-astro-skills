#!/usr/bin/env python3
"""
Automated Dual-RAG Skill Scaffolder for Docu (v7.0).
Generates normative directory structure, SKILL.md router, references/usage.md,
optional references/infra.md based on functional archetype, and a deterministic physical sensor.
"""
import os
import sys
import argparse
import stat

SKILL_TEMPLATE = """---
name: {name}
description: "{description} Trigger: {triggers}."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.0"
---

# {title} — Architecture & Operational Manual

## Activation Contract
Activate strictly when {activation}. Unrelated operational requests route to their respective specialized skills.

## Hard Rules (Positive Guidance)
- **Rule 1 (Zero Deletion & Signal Integrity)**: Preserve all domain algorithms, schemas, endpoints, and parameters via lossless offloading to references/.
- **Rule 2 (Fractal CoHaLo Bounded Execution)**: Commands execute with deterministic timeouts (`timeout 10s`), max synchronous wait (`WaitMsBeforeAsync: 10000`), and clean process termination via `manage_task action="kill"` for lingering background tasks.
- **Rule 3 (Circuit Breakers & Sensors)**: Consecutive retries are bounded to a maximum of 2 attempts before escalating; state attestation requires physical sensors (exit code 0 / HTTP 200).

## Decision Gates

| Use Case / Requirement | Action / Pattern | Reference / Asset |
|---|---|---|
| Method Signatures & Types | Client setup, method matrices, schemas | [`references/usage.md`](references/usage.md) |
| Production Recipes & Examples | End-to-end production workflows | [`references/usage.md`](references/usage.md) |
{infra_gate}| Physical Validation Sensor | Standard deterministic sensor checks | [`scripts/{name}-validate.sh`](scripts/{name}-validate.sh) |

## Critical Workflows / Execution Steps
1. Validate required parameters and consult [`references/usage.md`](references/usage.md){infra_step_ref}.
2. **Process Hygiene & Bounded Execution (CoHaLo)**: Execute commands with `timeout 10s`, `WaitMsBeforeAsync: 10000`, and clean orphan tasks with `manage_task action="kill"`.
3. **Circuit Breakers (CoHaLo)**: Limit retries to 2 attempts on failure (HTTP 500/timeout) before human escalation.
4. **Sensor Attestation**: Verify physical sensor check (exit code 0 / HTTP 200) and format output deterministically.

## Output Contract
- Deterministic response or JSON artifact matching schemas in [`references/usage.md`](references/usage.md).
- Status verification metric and clean execution state.

## References
- [`references/usage.md`](references/usage.md) — Method matrices, type interfaces, production patterns, error handling, and domain specifications.
{infra_ref}- [`scripts/{name}-validate.sh`](scripts/{name}-validate.sh) — Deterministic physical validation sensor (0 tokens, < 50ms).
"""

USAGE_FRAMEWORK_TEMPLATE = """# {title} — Developer & Agent Usage Manual

## 1. Client Initialization & Setup
Configuration, connection options, and authentication across TypeScript and Python:

```typescript
import {{ createClient }} from '{name}';

export const client = createClient({{
  apiKey: process.env.{env_prefix}_API_KEY!,
  timeout: 10000,
  maxRetries: 2,
}});
```

## 2. Method Signatures & Type Interfaces

| Method / Endpoint | Parameters | Return Type | Description |
|---|---|---|---|
| `client.execute(params)` | `params: ExecParams` | `Promise<ExecResult>` | Primary execution operation |
| `client.status(id)` | `id: string` | `Promise<StatusResult>` | Status query operation |

### Type Definitions
```typescript
export interface ExecParams {{
  id: string;
  mode?: 'sync' | 'async';
  options?: Record<string, unknown>;
}}

export interface ExecResult {{
  success: boolean;
  code: number;
  data: Record<string, unknown>;
}}
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
- Reference credentials by variable name (`${env_prefix}_API_KEY`), avoiding plaintext tokens.
- Bound all external operations with explicit timeouts (`timeout 10s`).
"""

USAGE_DOMAIN_TEMPLATE = """# {title} — Domain Engine & REST Calculation Manual

## 1. API Endpoints & Request Contracts
Base URL and authentication headers:
- Base URL: `https://api.{name}.example/v1`
- Auth Header: `Authorization: Bearer ${env_prefix}_API_KEY`
- Rate Limits: 100 requests/minute (standard tier)

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

### Request Payload Schema
```json
{{
  "target_id": "item-123",
  "timestamp": 1716384000,
  "precision": "high"
}}
```

## 3. Response Schemas & Domain Output
```json
{{
  "status": "success",
  "computed_at": 1716384001,
  "result": {{
    "value": 42.0,
    "confidence": 0.99
  }}
}}
```

## 4. Error Status Codes & Failover Protocol

| Status Code | Description | Failover Action |
|---|---|---|
| `400 Bad Request` | Missing or invalid parameter | Validate payload against schema before retry |
| `429 Quota Exceeded` | Daily or burst rate limit hit | Pause requests; switch to secondary provider |
| `503 Service Unavailable` | Engine maintenance | Trigger circuit breaker; halt after 2 retries |

## 5. Domain Invariants & Precision Rules
- Anchor calculations to verified canonical ephemeris or reference datasets.
- Round output values strictly to domain precision standards.
"""

USAGE_COGNITIVE_TEMPLATE = """# {title} — Cognitive & Methodological Manual

## 1. Core State Machine & Phase Transitions

| Phase | Name | Pre-Condition | Action | Sensor / Attestation |
|---|---|---|---|---|
| `P0` | Inflow & Recall | Task initiated | Query LTM memory and context | Evidence retrieved |
| `P1` | Evaluation | Inputs collected | Verify constraints against rules | Decision matrix validated |
| `P2` | Execution | Decision made | Execute deterministic procedure | Output generated |
| `P3` | Attestation | Procedure complete | Run deterministic sensor | Exit code 0 |

## 2. Algorithmic Invariants & Rules
- **Rule 1 (Context Optimization)**: Preserve KV cache prefix stability and keep routers under 550 tokens.
- **Rule 2 (Deterministic Harness)**: Every transformation is attested by automated checks with 0 LLM tokens.
- **Rule 3 (Bounded Loops)**: Limit iteration cycles to 2 attempts before escalating to human operator.

## 3. Decision Matrices & Evaluation Formulas

| Scenario | Input Pattern | Recommended Route | Fallback Route |
|---|---|---|---|
| Standard Path | Valid parameters present | Direct Execution | Clarification Gate |
| Degraded Path | Missing optional parameters | Default Policy | Human Escalation |

## 4. Output Schemas & Quality Thresholds
Outputs must satisfy structural completeness, schema compliance, and zero informational loss.
"""

INFRA_TEMPLATE = """# {title} — Infrastructure & Deployment Manual

## 1. Service Specifications & Topology
- **Runtime Base**: Native LXC (`ubuntu` / `alpine`) or Docker VM.
- **Scaling Mode**: Elastic autoscaling (`min < max`) for Native LXC; Fixed (`min == max`) for Docker VM.
- **Internal Ports**: Primary application port (e.g. `3000/TCP`, `8000/TCP`).

## 2. Environment Variables (.env Dictionary)

| Variable Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `PORT` | Number | Yes | `3000` | Application listening port |
| `DATABASE_URL` | String | Yes | — | Database connection string |
| `LOG_LEVEL` | String | No | `info` | Logging verbosity (`debug`, `info`, `warn`, `error`) |

## 3. Persistent Storage & Permissions
- **Mount Path**: `/mnt/<storageHostname>/<service>/`
- **FUSE Permission Safeguard**:
```bash
chmod -R 777 /mnt/<storageHostname>/<service>/
```

## 4. Lifecycle Automation (`zerops.yaml`)
```yaml
zerops:
  - setup: {name}
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

## 5. Process Hygiene & Circuit Breakers (CoHaLo)
- Execute commands with strict bounds: `timeout 10s ...`
- Limit retries to 2 attempts on HTTP 500 or timeout errors before human escalation.
- Clean lingering processes using `manage_task action="kill"`.
"""

VALIDATOR_TEMPLATE = """#!/usr/bin/env bash
# ==============================================================================
# Deterministic Physical Validation Sensor for {name}
# Zero LLM Tokens | Bounded Execution < 100ms | 100% Deterministic
# ==============================================================================
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")/.." && pwd)"
SKILL_NAME="$(basename "$SKILL_DIR")"
ERRORS=0

echo "============================================================"
echo "  🔍 Validating Skill Integrity: [$SKILL_NAME]"
echo "============================================================"

# 1. Structural Integrity Check
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "❌ Missing required SKILL.md in $SKILL_DIR"
    ERRORS=$((ERRORS + 1))
else
    echo "✓ SKILL.md exists"
fi

# 2. Frontmatter Metadata Verification
if grep -q '^name: ' "$SKILL_DIR/SKILL.md" && \\
   grep -q '^description: ' "$SKILL_DIR/SKILL.md" && \\
   grep -q 'version: ' "$SKILL_DIR/SKILL.md"; then
    echo "✓ Valid YAML frontmatter metadata"
else
    echo "❌ Malformed frontmatter in SKILL.md"
    ERRORS=$((ERRORS + 1))
fi

# 3. Reference Files Non-Emptiness Check
if [ -d "$SKILL_DIR/references" ]; then
    for ref_file in "$SKILL_DIR/references/"*.md; do
        if [ -f "$ref_file" ]; then
            if [ ! -s "$ref_file" ]; then
                echo "❌ Empty reference file: $(basename "$ref_file")"
                ERRORS=$((ERRORS + 1))
            fi
        fi
    done
    echo "✓ Reference files in references/ are non-empty"
fi

# 4. Clean-Room Bytecode Hygiene (Zero __pycache__ or *.pyc)
if find "$SKILL_DIR" -name "__pycache__" -o -name "*.pyc" 2>/dev/null | grep -q .; then
    echo "❌ Bytecode cache detected (__pycache__ or *.pyc)"
    ERRORS=$((ERRORS + 1))
else
    echo "✓ Clean-room hygiene verified: zero bytecode cache"
fi

# 5. Script Syntax Verification (In-memory AST, zero disk writes)
if [ -d "$SKILL_DIR/scripts" ]; then
    for sh_file in "$SKILL_DIR/scripts/"*.sh; do
        if [ -f "$sh_file" ]; then
            if bash -n "$sh_file" >/dev/null 2>&1; then
                echo "✓ Bash syntax valid: $(basename "$sh_file")"
            else
                echo "❌ Bash syntax error: $(basename "$sh_file")"
                ERRORS=$((ERRORS + 1))
            fi
        fi
    done
    for py_file in "$SKILL_DIR/scripts/"*.py; do
        if [ -f "$py_file" ]; then
            if python3 -c "import ast; ast.parse(open('$py_file').read())" >/dev/null 2>&1; then
                echo "✓ Python AST valid: $(basename "$py_file")"
            else
                echo "❌ Python syntax error: $(basename "$py_file")"
                ERRORS=$((ERRORS + 1))
            fi
        fi
    done
fi

# 6. Physical Link Integrity (Zero Broken Links)
while IFS= read -r link; do
    clean_path="${{link#file://}}"
    if [ -z "${{clean_path#/}}" ]; then
        continue
    fi
    if [ ! -e "$clean_path" ]; then
        echo "❌ Broken physical link: $link"
        ERRORS=$((ERRORS + 1))
    fi
done < <(grep -oE 'file:///[^ )"`]+' "$SKILL_DIR/SKILL.md" 2>/dev/null || true)
echo "✓ Physical file:/// links resolved and verified"

# 7. Token Budget Guardrail (<= 550 recommended, <= 750 warning, <= 2500 error)
WORD_COUNT=$(wc -w < "$SKILL_DIR/SKILL.md")
EST_TOKENS=$((WORD_COUNT * 13 / 10))
echo "• SKILL.md word count: $WORD_COUNT (~$EST_TOKENS tokens)"
if [ "$EST_TOKENS" -gt 2500 ]; then
    echo "❌ SKILL.md exceeds hard ceiling of 2500 tokens (~$EST_TOKENS tokens)"
    ERRORS=$((ERRORS + 1))
elif [ "$EST_TOKENS" -gt 750 ]; then
    echo "⚠️ Notice: SKILL.md exceeds ideal budget of 750 tokens (~$EST_TOKENS tokens)"
else
    echo "✓ SKILL.md within recommended token budget"
fi

# 8. Structural References Integrity Verification
EMPTY_REFS=0
if [ -d "$SKILL_DIR/references" ]; then
    for ref_f in "$SKILL_DIR/references/"*.md; do
        if [ -f "$ref_f" ] && [ ! -s "$ref_f" ]; then
            echo "❌ Empty reference file: $(basename "$ref_f")"
            EMPTY_REFS=$((EMPTY_REFS + 1))
        fi
    done
fi
if [ "$EMPTY_REFS" -eq 0 ]; then
    echo "✓ Structural reference files non-empty and verified"
else
    ERRORS=$((ERRORS + 1))
fi

echo "------------------------------------------------------------"
if [ "$ERRORS" -eq 0 ]; then
    echo "✅ Skill [$SKILL_NAME] passed physical validation (exit code 0)."
    exit 0
else
    echo "❌ Skill [$SKILL_NAME] validation failed with $ERRORS error(s)."
    exit 1
fi
"""


def main():
    parser = argparse.ArgumentParser(description="Automated Dual-RAG Skill Scaffolder (v7.0)")
    parser.add_argument("slug", help="Unique skill identifier slug (e.g. my-skill)")
    parser.add_argument("triggers", help="Comma-separated trigger phrases (e.g. my-skill, query-skill)")
    parser.add_argument("description", help="Concise affirmative description of skill capabilities")
    parser.add_argument("--archetype", choices=["framework", "infra", "domain", "cognitive"], default="framework",
                        help="Functional archetype (framework, infra, domain, cognitive)")
    parser.add_argument("--with-infra", action="store_true", help="Force generation of references/infra.md")
    parser.add_argument("--base-dir", default="/var/www/.agents/skills", help="Base directory for skills")

    args = parser.parse_args()

    skill_dir = os.path.join(args.base_dir, args.slug)
    ref_dir = os.path.join(skill_dir, "references")
    assets_dir = os.path.join(skill_dir, "assets")
    scripts_dir = os.path.join(skill_dir, "scripts")

    os.makedirs(ref_dir, exist_ok=True)
    os.makedirs(assets_dir, exist_ok=True)
    os.makedirs(scripts_dir, exist_ok=True)

    title = args.slug.replace("-", " ").title()
    env_prefix = args.slug.replace("-", "_").upper()
    needs_infra = (args.archetype == "infra") or args.with_infra

    # 1. Format SKILL.md
    if needs_infra:
        infra_gate = "| Infrastructure & Deployment | Service specs, ports, lifecycle | [`references/infra.md`](references/infra.md) |\n"
        infra_step_ref = " or [`references/infra.md`](references/infra.md)"
        infra_ref = "- [`references/infra.md`](references/infra.md) — Service specs, ports, .env dictionary, and lifecycle automation.\n"
    else:
        infra_gate = ""
        infra_step_ref = ""
        infra_ref = ""

    skill_content = SKILL_TEMPLATE.format(
        name=args.slug,
        title=title,
        description=args.description.strip('"'),
        triggers=args.triggers.strip('"'),
        activation=f"operating with {args.slug} capabilities or intent",
        infra_gate=infra_gate,
        infra_step_ref=infra_step_ref,
        infra_ref=infra_ref
    )

    with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(skill_content)

    # 2. Format references/usage.md
    if args.archetype == "domain":
        usage_content = USAGE_DOMAIN_TEMPLATE.format(title=title, name=args.slug, env_prefix=env_prefix)
    elif args.archetype == "cognitive":
        usage_content = USAGE_COGNITIVE_TEMPLATE.format(title=title, name=args.slug)
    else:
        usage_content = USAGE_FRAMEWORK_TEMPLATE.format(title=title, name=args.slug, env_prefix=env_prefix)

    with open(os.path.join(ref_dir, "usage.md"), "w", encoding="utf-8") as f:
        f.write(usage_content)

    # 3. Format references/infra.md if needed
    if needs_infra:
        infra_content = INFRA_TEMPLATE.format(title=title, name=args.slug)
        with open(os.path.join(ref_dir, "infra.md"), "w", encoding="utf-8") as f:
            f.write(infra_content)

    # 4. Format scripts/<slug>-validate.sh
    validator_content = VALIDATOR_TEMPLATE.format(name=args.slug)
    val_path = os.path.join(scripts_dir, f"{args.slug}-validate.sh")
    with open(val_path, "w", encoding="utf-8") as f:
        f.write(validator_content)

    # Set executable permissions on validator
    st = os.stat(val_path)
    os.chmod(val_path, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    print(f"✅ Successfully scaffolded skill [{args.slug}] under archetype [{args.archetype}] at {skill_dir}")


if __name__ == "__main__":
    main()

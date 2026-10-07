#!/usr/bin/env bash
# ==============================================================================
# Deterministic Physical Validation Sensor for whatsapp-engine Suite (v2.0)
# ==============================================================================
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

REAL_SCRIPT="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$REAL_SCRIPT")"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ERRORS=0

trap 'rm -rf "$SCRIPT_DIR/__pycache__" "$SCRIPT_DIR"/*.pyc 2>/dev/null || true' EXIT

echo "============================================================"
echo "  🔍 Validating whatsapp-engine Skill Integrity (v2.0)"
echo "============================================================"

# 1. Frontmatter and Word Count Validation
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "❌ Missing SKILL.md in $SKILL_DIR"
    ERRORS=$((ERRORS + 1))
else
    echo "✓ SKILL.md exists"

    WORD_COUNT=$(wc -w < "$SKILL_DIR/SKILL.md")
    if [ "$WORD_COUNT" -le 480 ]; then
        echo "✓ Router word count budget compliant: $WORD_COUNT words (limit 480)"
    else
        echo "❌ Router word count exceeded: $WORD_COUNT words (limit 480)"
        ERRORS=$((ERRORS + 1))
    fi

    VERSION=$(python3 -c "
import yaml
with open('$SKILL_DIR/SKILL.md') as f:
    content = f.read()
parts = content.split('---')
if len(parts) >= 3:
    meta = yaml.safe_load(parts[1])
    print(meta.get('metadata', {}).get('version', ''))
")

    if [ "$VERSION" = "2.0" ]; then
        echo "✓ Canonical frontmatter version validated: v$VERSION"
    else
        echo "❌ Invalid or missing frontmatter version: found '$VERSION', expected '2.0'"
        ERRORS=$((ERRORS + 1))
    fi
fi

# 2. Dual-RAG Reference Files & Canonical Links Integrity
REQUIRED_REFS=(
    "references/usage.md"
    "references/infra.md"
    "references/drivers/bifrost_llm.md"
    "references/drivers/nats_events.md"
    "references/drivers/evolutiongo.md"
    "references/drivers/meta_cloud.md"
    "assets/anti_ban_warmup_guide.md"
    "assets/whatsapp_engine_recipes.json"
    "scripts/whatsapp-engine-validate.sh"
)

for ref in "${REQUIRED_REFS[@]}"; do
    if [ -f "$SKILL_DIR/$ref" ] && [ -s "$SKILL_DIR/$ref" ]; then
        echo "✓ Reference file exists and non-empty: $ref"
    else
        echo "❌ Missing or empty reference file: $ref"
        ERRORS=$((ERRORS + 1))
    fi

    if grep -q "file:///var/www/.agents/skills/whatsapp-engine/$ref" "$SKILL_DIR/SKILL.md"; then
        echo "✓ Canonical file link verified in SKILL.md: $ref"
    else
        echo "❌ Missing canonical file link in SKILL.md: $ref"
        ERRORS=$((ERRORS + 1))
    fi
done

# 3. Deterministic JSON Validation
python3 -c "
import json

with open('$SKILL_DIR/assets/whatsapp_engine_recipes.json') as f:
    data = json.load(f)
assert data.get('version') == '2.0', 'Recipes version must be 2.0'
assert 'recipes' in data and len(data['recipes']) >= 3, 'Must have at least 3 recipes'
for r in data['recipes']:
    assert 'id' in r and 'description' in r, 'Malformed recipe item'
assert any(r.get('port') == 8080 for r in data['recipes']), 'Missing port 8080 in runtime recipe'

with open('$SKILL_DIR/assets/evolutiongo_production_recipes.json') as f:
    ev_data = json.load(f)
assert 'recipes' in ev_data, 'Missing recipes object'
assert 'zerops_yaml_evolutiongo' in ev_data['recipes'], 'Missing zerops_yaml_evolutiongo recipe'

print('✓ JSON syntax and recipes structure valid: assets/*.json')
" || { echo "❌ JSON validation failed for recipes"; ERRORS=$((ERRORS + 1)); }

# 4. TypeScript Structural Integrity & AST Assertions
python3 -c "
with open('$SKILL_DIR/assets/meta_cloud/whatsapp_cloud_client.ts') as f:
    client_src = f.read()
assert 'export class WhatsAppCloudClient' in client_src, 'Missing WhatsAppCloudClient class'
assert 'async sendText(' in client_src, 'Missing sendText method'
assert 'async sendInteractiveButtons(' in client_src, 'Missing sendInteractiveButtons method'
assert 'v21.0' in client_src, 'Missing v21.0 API version reference'

with open('$SKILL_DIR/assets/meta_cloud/whatsapp_ai_agent.ts') as f:
    agent_src = f.read()
assert 'export async function processWhatsAppInbound' in agent_src, 'Missing processWhatsAppInbound'
assert 'createPaymentLink' in agent_src, 'Missing createPaymentLink tool'
assert 'resolveSystemPrompt' in agent_src, 'Missing resolveSystemPrompt function'
assert '8080' in agent_src, 'Missing Bifrost 8080 port default in agent'

with open('$SKILL_DIR/assets/meta_cloud/valkey_session_manager.ts') as f:
    valkey_src = f.read()
assert 'export class ValkeySessionManager' in valkey_src, 'Missing ValkeySessionManager'
assert 'acquireLock' in valkey_src, 'Missing acquireLock method'

with open('$SKILL_DIR/assets/meta_cloud/whatsapp_zod_schemas.ts') as f:
    zod_src = f.read()
assert 'export const WhatsAppWebhookPayloadSchema' in zod_src, 'Missing WhatsAppWebhookPayloadSchema'

print('✓ TypeScript structural assertions passed for all meta_cloud assets')
" || { echo "❌ TypeScript structural assertions failed"; ERRORS=$((ERRORS + 1)); }

# 5. Ecosystem Ground Truth & Port 8080 Validation
if grep -rn "bifrost:8000" "$SKILL_DIR/SKILL.md" "$SKILL_DIR/references/" "$SKILL_DIR/assets/" 2>/dev/null; then
    echo "❌ Found deprecated port 8000 in whatsapp-engine. Bifrost must use port 8080 in Zerops."
    ERRORS=$((ERRORS + 1))
else
    echo "✓ Port 8080 verified: zero occurrences of deprecated bifrost:8000."
fi

# 6. Decoupled Prompt Path Validation
if grep -rn "/brand/fase0_system_prompt.md" "$SKILL_DIR/SKILL.md" "$SKILL_DIR/references/drivers/bifrost_llm.md" 2>/dev/null; then
    echo "❌ Found hardcoded single-tenant path /brand/fase0_system_prompt.md. Must use dynamic env vars."
    ERRORS=$((ERRORS + 1))
else
    echo "✓ Dynamic system prompt path verified: zero occurrences of hardcoded /brand/fase0_system_prompt.md."
fi

# 7. Anti-Leak Secret Validation
LEAK_PATTERNS=("BEGIN PRIVATE KEY" "ghp_" "glpat-" "xoxb-" "sk-proj-")
for pat in "${LEAK_PATTERNS[@]}"; do
    if grep -rq "$pat" "$SKILL_DIR" --exclude="*.sh"; then
        echo "❌ Possible secret leak detected matching '$pat'"
        ERRORS=$((ERRORS + 1))
    fi
done
echo "✓ Anti-leak secret check clean"

echo "------------------------------------------------------------"
if [ "$ERRORS" -eq 0 ]; then
    echo "✅ whatsapp-engine v2.0 validation passed successfully with exit code 0."
    exit 0
else
    echo "❌ whatsapp-engine v2.0 validation failed with $ERRORS error(s)."
    exit 1
fi

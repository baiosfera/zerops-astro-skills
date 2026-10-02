#!/usr/bin/env bash
# ==============================================================================
# Deterministic Physical Validation Sensor for automation-engine Suite (v2.0)
# ==============================================================================
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ERRORS=0

echo "============================================================"
echo "  🔍 Validating automation-engine Skill Integrity (v2.0)"
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
    "assets/automation_zod_schemas.ts"
    "assets/circuit_breaker.ts"
    "assets/nats_jetstream_client.ts"
    "assets/bullmq_worker.ts"
    "assets/automation_engine_recipes.json"
    "scripts/automation-engine-validate.sh"
)

for ref in "${REQUIRED_REFS[@]}"; do
    if [ -f "$SKILL_DIR/$ref" ] && [ -s "$SKILL_DIR/$ref" ]; then
        echo "✓ Reference file exists and non-empty: $ref"
    else
        echo "❌ Missing or empty reference file: $ref"
        ERRORS=$((ERRORS + 1))
    fi

    if grep -q "file:///var/www/.agents/skills/automation-engine/$ref" "$SKILL_DIR/SKILL.md"; then
        echo "✓ Canonical file link verified: $ref"
    else
        echo "❌ Missing canonical file link in SKILL.md: $ref"
        ERRORS=$((ERRORS + 1))
    fi
done

# 3. Deterministic JSON Validation (No silent suppression)
python3 -c "
import json
with open('$SKILL_DIR/assets/automation_engine_recipes.json') as f:
    data = json.load(f)
assert data.get('version') == '2.0', 'Recipes version must be 2.0'
assert len(data.get('recipes', [])) >= 2, 'Must contain at least 2 recipes'
print('✓ JSON syntax and schema structure valid: assets/automation_engine_recipes.json')
" || { echo "❌ JSON validation failed"; ERRORS=$((ERRORS + 1)); }

# 4. TypeScript & JavaScript Asset Structural Integrity
for ts_file in "assets/automation_zod_schemas.ts" "assets/circuit_breaker.ts" "assets/nats_jetstream_client.ts" "assets/bullmq_worker.ts"; do
    python3 -c "
with open('$SKILL_DIR/$ts_file') as f:
    content = f.read()
assert len(content) > 100, 'File $ts_file is too small'
assert 'export ' in content, 'File $ts_file must have exports'
print('✓ Code structural assertion passed: $ts_file')
" || { echo "❌ Code structural error in $ts_file"; ERRORS=$((ERRORS + 1)); }
done

if [ -f "$SKILL_DIR/assets/directus_flow_transformer.js" ]; then
    node --check "$SKILL_DIR/assets/directus_flow_transformer.js" && echo "✓ JavaScript syntax valid: directus_flow_transformer.js" || { echo "❌ Syntax error in directus_flow_transformer.js"; ERRORS=$((ERRORS + 1)); }
fi

# 5. Zero Single-Tenant Debt Invariant (Banned Leak Scanner)
BANNED_LEAKS=("baiosfera" "total_cop" "0zcp-123" "sales-main")
for leak in "${BANNED_LEAKS[@]}"; do
    FOUND_LEAKS=$(grep -rn "$leak" "$SKILL_DIR" --exclude="*.bak*" --exclude="automation-engine-validate.sh" || true)
    if [ -n "$FOUND_LEAKS" ]; then
        echo "❌ Single-tenant leak detected for '$leak':"
        echo "$FOUND_LEAKS"
        ERRORS=$((ERRORS + 1))
    else
        echo "✓ Zero single-tenant leak for '$leak'"
    fi
done

echo "------------------------------------------------------------"
if [ "$ERRORS" -eq 0 ]; then
    echo "✅ automation-engine v2.0 validation passed successfully with exit code 0."
    exit 0
else
    echo "❌ automation-engine v2.0 validation failed with $ERRORS error(s)."
    exit 1
fi

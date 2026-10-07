#!/usr/bin/env bash
# ==============================================================================
# Deterministic Physical Validation Sensor for Listmonk Suite (v2.0)
# ==============================================================================
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

REAL_SCRIPT="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$REAL_SCRIPT")"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ERRORS=0

trap 'rm -rf "$SCRIPT_DIR/__pycache__" "$SCRIPT_DIR"/*.pyc 2>/dev/null || true' EXIT

echo "============================================================"
echo "  🔍 Validating Listmonk Skill Integrity (v2.0)"
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
    "assets/listmonk_client.ts"
    "assets/listmonk_production_recipes.json"
    "scripts/listmonk-validate.sh"
)

for ref in "${REQUIRED_REFS[@]}"; do
    if [ -f "$SKILL_DIR/$ref" ] && [ -s "$SKILL_DIR/$ref" ]; then
        echo "✓ Reference file exists and non-empty: $ref"
    else
        echo "❌ Missing or empty reference file: $ref"
        ERRORS=$((ERRORS + 1))
    fi

    if grep -q "file:///var/www/.agents/skills/listmonk/$ref" "$SKILL_DIR/SKILL.md"; then
        echo "✓ Canonical file link verified: $ref"
    else
        echo "❌ Missing canonical file link in SKILL.md: $ref"
        ERRORS=$((ERRORS + 1))
    fi
done

# 3. Deterministic JSON Validation
python3 -c "
import json
with open('$SKILL_DIR/assets/listmonk_production_recipes.json') as f:
    data = json.load(f)
assert data.get('version') == '2.0.0', 'Recipes version must be 2.0.0'
assert 'recipes' in data, 'Must have recipes dictionary'
assert 'zerops_yaml_static_binary' in data['recipes'], 'Missing static binary recipe'
assert 'horizontal_scaling_passive_replica' in data['recipes'], 'Missing passive scaling recipe'

yaml_content = data['recipes']['zerops_yaml_static_binary']['yaml']
assert 'v6.2.0' in yaml_content, 'Recipe must reference Listmonk v6.2.0'
assert 'search_path=listmonk,public' in yaml_content, 'Recipe must configure search_path=listmonk,public'
assert 'upload__provider: \"s3\"' in yaml_content, 'Recipe must configure S3 upload provider'

print('✓ JSON syntax and recipes structure valid: assets/listmonk_production_recipes.json')
" || { echo "❌ JSON validation failed for listmonk_production_recipes.json"; ERRORS=$((ERRORS + 1)); }

# 4. TypeScript Client Structural Integrity
python3 -c "
with open('$SKILL_DIR/assets/listmonk_client.ts') as f:
    content = f.read()
assert 'export class ListmonkClient' in content, 'Missing ListmonkClient export'
assert 'export interface TransactionalEmailRequest' in content, 'Missing TransactionalEmailRequest export'
assert 'altbody' in content, 'Client must support altbody parameter'
assert 'patchSubscriber' in content, 'Client must support patchSubscriber'
print('✓ Code structural assertion passed: assets/listmonk_client.ts')
" || { echo "❌ Code structural error in assets/listmonk_client.ts"; ERRORS=$((ERRORS + 1)); }

# 5. Zero Single-Tenant Debt Invariant (Banned Leak Scanner)
BANNED_LEAKS=("/mnt/baiostorage" "baiostorage" "baiosfera/0ZEROPS-AGY")
for leak in "${BANNED_LEAKS[@]}"; do
    FOUND_LEAKS=$(grep -rn "$leak" "$SKILL_DIR" --exclude="*.bak*" --exclude="listmonk-validate.sh" || true)
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
    echo "✅ Listmonk v2.0 validation passed successfully with exit code 0."
    exit 0
else
    echo "❌ Listmonk v2.0 validation failed with $ERRORS error(s)."
    exit 1
fi

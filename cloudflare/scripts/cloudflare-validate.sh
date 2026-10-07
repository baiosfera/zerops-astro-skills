#!/usr/bin/env bash
# ==============================================================================
# Deterministic Physical Validation Sensor for cloudflare Suite (v2.0)
# ==============================================================================
set -euo pipefail

REAL_SCRIPT="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$REAL_SCRIPT")"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ERRORS=0

echo "============================================================"
echo "  🔍 Validating cloudflare Skill Integrity (v2.0)"
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
    "assets/cloudflare_client.ts"
    "assets/dns_zod_schemas.ts"
    "assets/turnstile_validator.ts"
    "assets/cloudflare_production_recipes.json"
    "scripts/sync-dns.ts"
    "scripts/cloudflare-validate.sh"
)

for ref in "${REQUIRED_REFS[@]}"; do
    if [ -f "$SKILL_DIR/$ref" ] && [ -s "$SKILL_DIR/$ref" ]; then
        echo "✓ Reference file exists and non-empty: $ref"
    else
        echo "❌ Missing or empty reference file: $ref"
        ERRORS=$((ERRORS + 1))
    fi

    if grep -q "file:///var/www/.agents/skills/cloudflare/$ref" "$SKILL_DIR/SKILL.md"; then
        echo "✓ Canonical file link verified: $ref"
    else
        echo "❌ Missing canonical file link in SKILL.md: $ref"
        ERRORS=$((ERRORS + 1))
    fi
done

# 3. Deterministic JSON Validation (No silent suppression)
python3 -c "
import json
with open('$SKILL_DIR/assets/cloudflare_production_recipes.json') as f:
    data = json.load(f)
assert data.get('version') == '2.0', 'Recipes version must be 2.0'
assert 'rulesets' in data, 'Must contain rulesets definitions'
assert 'waf_acme_http01_bypass' in data['rulesets'], 'Must define ACME bypass'
print('✓ JSON syntax and Rulesets structure valid: assets/cloudflare_production_recipes.json')
" || { echo "❌ JSON validation failed for cloudflare_production_recipes.json"; ERRORS=$((ERRORS + 1)); }

# 4. TypeScript Code Structural Integrity
for ts_file in "assets/dns_zod_schemas.ts" "assets/cloudflare_client.ts" "assets/turnstile_validator.ts" "scripts/sync-dns.ts"; do
    python3 -c "
with open('$SKILL_DIR/$ts_file') as f:
    content = f.read()
assert len(content) > 100, 'File $ts_file is too small'
assert 'export ' in content or 'import ' in content, 'File $ts_file lacks export/import statements'
print('✓ Code structural assertion passed: $ts_file')
" || { echo "❌ Code structural error in $ts_file"; ERRORS=$((ERRORS + 1)); }
done

# 5. Anti-Leak & RFC 9989 Enforcement Scan
BANNED_LEAKS=("baiosfera" "0zcp-123" "sales-main" "directus-prod.app-123" "pct=100")
for leak in "${BANNED_LEAKS[@]}"; do
    FOUND_LEAKS=$(grep -rn "$leak" "$SKILL_DIR" --exclude="*.bak*" --exclude="cloudflare-validate.sh" || true)
    if [ -n "$FOUND_LEAKS" ]; then
        echo "❌ Prohibited pattern / leak detected for '$leak':"
        echo "$FOUND_LEAKS"
        ERRORS=$((ERRORS + 1))
    else
        echo "✓ Zero leak for '$leak'"
    fi
done

echo "------------------------------------------------------------"
if [ "$ERRORS" -eq 0 ]; then
    echo "✅ cloudflare v2.0 validation passed successfully with exit code 0."
    exit 0
else
    echo "❌ cloudflare v2.0 validation failed with $ERRORS error(s)."
    exit 1
fi

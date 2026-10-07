#!/usr/bin/env bash
# ==============================================================================
# Deterministic Physical Validation Sensor for Astro Skill Suite (v3.0)
# Zero Checklist Theater | Reality Over Compliance | Exit Code 0 Invariant
# ==============================================================================
set -euo pipefail

REAL_SCRIPT="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$REAL_SCRIPT")"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ERRORS=0

echo "============================================================"
echo "  🔍 Validating Astro Skill Suite Integrity (v3.0)"
echo "============================================================"

# 1. Manifest Budget & Frontmatter Verification
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "❌ Missing SKILL.md in $SKILL_DIR"
    ERRORS=$((ERRORS + 1))
else
    WORD_COUNT=$(wc -w < "$SKILL_DIR/SKILL.md")
    if [ "$WORD_COUNT" -le 480 ]; then
        echo "✓ Word budget compliant: $WORD_COUNT words (limit: 480 words)"
    else
        echo "❌ Word budget exceeded: $WORD_COUNT words > 480 words"
        ERRORS=$((ERRORS + 1))
    fi

    # Extract version with Python YAML parser
    VERSION=$(python3 -c "
import yaml
with open('$SKILL_DIR/SKILL.md') as f:
    content = f.read()
parts = content.split('---')
if len(parts) >= 3:
    meta = yaml.safe_load(parts[1])
    print(meta.get('metadata', {}).get('version', ''))
")

    if [ "$VERSION" = "3.0" ]; then
        echo "✓ Canonical frontmatter version validated: v$VERSION"
    else
        echo "❌ Invalid or missing frontmatter version: found '$VERSION', expected '3.0'"
        ERRORS=$((ERRORS + 1))
    fi
fi

# 2. Dual-RAG File & Hyperlink Integrity
for ref in "references/usage.md" "references/infra.md" "assets/astro_production_recipes.json" "assets/import_template.yaml" "assets/zerops_template.yaml" "scripts/astro-web-validate.sh"; do
    if [ -f "$SKILL_DIR/$ref" ] && [ -s "$SKILL_DIR/$ref" ]; then
        echo "✓ Reference file exists and non-empty: $ref"
    else
        echo "❌ Missing or empty reference file: $ref"
        ERRORS=$((ERRORS + 1))
    fi

    if grep -q "file:///var/www/.agents/skills/astro-web/$ref" "$SKILL_DIR/SKILL.md"; then
        echo "✓ Canonical file link verified: $ref"
    else
        echo "❌ Missing canonical file link in SKILL.md: $ref"
        ERRORS=$((ERRORS + 1))
    fi
done

# 3. Deterministic YAML Validation
for yml in "$SKILL_DIR/assets/import_template.yaml" "$SKILL_DIR/assets/zerops_template.yaml"; do
    if python3 -c "import yaml; yaml.safe_load(open('$yml'))"; then
        echo "✓ YAML syntax valid: $(basename "$yml")"
    else
        echo "❌ YAML syntax error in $yml"
        ERRORS=$((ERRORS + 1))
    fi
done

# 4. Deterministic JSON Validation
if python3 -m json.tool "$SKILL_DIR/assets/astro_production_recipes.json" > /tmp/astro_json_val.tmp; then
    echo "✓ JSON syntax valid: assets/astro_production_recipes.json"
    rm -f /tmp/astro_json_val.tmp
else
    echo "❌ JSON syntax error in assets/astro_production_recipes.json"
    ERRORS=$((ERRORS + 1))
fi

# 5. Zero Single-Tenant Debt Invariant (Banned Leak Scanner)
BANNED_LEAKS=("baiosfera" "sales-main" "gentle-astro-suite")
for leak in "${BANNED_LEAKS[@]}"; do
    FOUND_LEAKS=$(grep -rn "$leak" "$SKILL_DIR" --exclude="*.bak*" --exclude="astro-web-validate.sh" || true)
    if [ -n "$FOUND_LEAKS" ]; then
        echo "❌ Single-tenant leak detected for '$leak':"
        echo "$FOUND_LEAKS"
        ERRORS=$((ERRORS + 1))
    else
        echo "✓ Zero single-tenant leak for '$leak'"
    fi
done

# 6. Syntax Check of Embedded Code Recipes
python3 -c "
import json, yaml

with open('$SKILL_DIR/assets/astro_production_recipes.json') as f:
    data = json.load(f)

recipes = data.get('recipes', {})
for rname, rdata in recipes.items():
    if 'yaml' in rdata:
        yaml.safe_load(rdata['yaml'])
        print(f'✓ Validated YAML recipe: {rname}')
    if 'code' in rdata:
        assert len(rdata['code']) > 20, f'Recipe {rname} too short'
        assert 'export' in rdata['code'] or 'import' in rdata['code'], f'Recipe {rname} lacks export/import'
        print(f'✓ Validated code recipe: {rname}')
" || ERRORS=$((ERRORS + 1))

echo "------------------------------------------------------------"
if [ "$ERRORS" -eq 0 ]; then
    echo "✅ Astro Skill Suite v3.0 physically validated with exit code 0."
    exit 0
else
    echo "❌ Astro Skill Suite v3.0 validation failed with $ERRORS error(s)."
    exit 1
fi

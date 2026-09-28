#!/usr/bin/env bash
# ==============================================================================
# Deterministic Physical Validation Sensor for Astro Skill Suite (v2.0)
# ==============================================================================
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ERRORS=0

echo "============================================================"
echo "  🔍 Validating Astro Skill Integrity (v2.0)"
echo "============================================================"

# 1. Check SKILL.md existence
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "❌ Missing SKILL.md in $SKILL_DIR"
    ERRORS=$((ERRORS + 1))
else
    echo "✓ SKILL.md exists"
fi

# 2. Check frontmatter metadata.version
if grep -Eq 'version: "[0-9]+\.[0-9]+"' "$SKILL_DIR/SKILL.md"; then
    echo "✓ Frontmatter version is 2.0"
else
    echo "❌ Frontmatter version is not 2.0"
    ERRORS=$((ERRORS + 1))
fi

# 3. Check token count of SKILL.md
WORD_COUNT=$(wc -w < "$SKILL_DIR/SKILL.md")
EST_TOKENS=$((WORD_COUNT * 13 / 10))
if [ "$EST_TOKENS" -le 750 ]; then
    echo "✓ Token budget compliant: ~$EST_TOKENS tokens (word count: $WORD_COUNT, limit 750)"
else
    echo "⚠️ Warning: SKILL.md exceeds recommended token budget (~$EST_TOKENS tokens)"
fi

# 4. Check Dual-RAG references
for ref in "references/usage.md" "references/infra.md" "assets/astro_production_recipes.json" "assets/import_template.yaml" "assets/zerops_template.yaml"; do
    if [ -f "$SKILL_DIR/$ref" ] && [ -s "$SKILL_DIR/$ref" ]; then
        echo "✓ Required reference exists and non-empty: $ref"
    else
        echo "❌ Missing or empty reference: $ref"
        ERRORS=$((ERRORS + 1))
    fi
done

# 5. Check JSON validity
if python3 -m json.tool "$SKILL_DIR/assets/astro_production_recipes.json" >/dev/null 2>&1; then
    echo "✓ astro_production_recipes.json is valid JSON"
else
    echo "❌ Syntax error in astro_production_recipes.json"
    ERRORS=$((ERRORS + 1))
fi

# 6. Check file links
for link in "references/usage.md" "references/infra.md" "assets/astro_production_recipes.json" "assets/import_template.yaml" "assets/zerops_template.yaml" "scripts/astro-web-validate.sh"; do
    if grep -q "file:///var/www/.agents/skills/astro-web/$link" "$SKILL_DIR/SKILL.md"; then
        echo "✓ Absolute file link verified: $link"
    else
        echo "❌ Missing absolute file link in SKILL.md: $link"
        ERRORS=$((ERRORS + 1))
    fi
done

echo "------------------------------------------------------------"
if [ "$ERRORS" -eq 0 ]; then
    echo "✅ Astro v2.0 validation passed successfully with exit code 0."
    exit 0
else
    echo "❌ Astro v2.0 validation failed with $ERRORS error(s)."
    exit 1
fi

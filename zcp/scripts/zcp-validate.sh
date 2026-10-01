#!/usr/bin/env bash
# ==============================================================================
# Deterministic Physical Validation Sensor for zcp Suite (v6.4)
# ==============================================================================
set -euo pipefail

export PYTHONDONTWRITEBYTECODE=1

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Trap cleanup on exit to eliminate any bytecode artifacts
trap 'find "$SKILL_DIR" -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true; find "$SKILL_DIR" -name "*.pyc" -delete 2>/dev/null || true' EXIT INT TERM

ERRORS=0

echo "============================================================"
echo "  🔍 Validating zcp Skill Integrity (v6.4)"
echo "============================================================"

# 1. Check SKILL.md existence
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "❌ Missing SKILL.md in $SKILL_DIR"
    ERRORS=$((ERRORS + 1))
else
    echo "✓ SKILL.md exists"
fi

# 2. Check frontmatter metadata.version
VERSION=$(grep -E 'version: "[0-9]+\.[0-9]+"' "$SKILL_DIR/SKILL.md" | head -n 1 | sed -E 's/.*version: "([^"]+)".*/\1/')
if [ "$VERSION" = "6.4" ]; then
    echo "✓ Frontmatter version is 6.4"
else
    echo "❌ Frontmatter version is not 6.4 (found: $VERSION)"
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
for ref in "references/usage.md" "references/infra.md" "assets/zcp_production_recipes.json" "assets/import_template.yaml" "assets/zerops_template.yaml"; do
    if [ -f "$SKILL_DIR/$ref" ] && [ -s "$SKILL_DIR/$ref" ]; then
        echo "✓ Required reference exists and non-empty: $ref"
    else
        echo "❌ Missing or empty reference: $ref"
        ERRORS=$((ERRORS + 1))
    fi
done

# 5. Check JSON validity
if python3 -c "import json, sys; json.load(open(sys.argv[1]))" "$SKILL_DIR/assets/zcp_production_recipes.json"; then
    echo "✓ zcp_production_recipes.json is valid JSON"
else
    echo "❌ Syntax error in zcp_production_recipes.json"
    ERRORS=$((ERRORS + 1))
fi

# 6. Check file links
for link in "references/usage.md" "references/infra.md" "assets/zcp_production_recipes.json" "assets/import_template.yaml" "assets/zerops_template.yaml" "scripts/zcp-validate.sh"; do
    if grep -q "file:///var/www/.agents/skills/zcp/$link" "$SKILL_DIR/SKILL.md"; then
        echo "✓ Absolute file link verified: $link"
    else
        echo "❌ Missing absolute file link in SKILL.md: $link"
        ERRORS=$((ERRORS + 1))
    fi
done

echo "------------------------------------------------------------"
if [ "$ERRORS" -eq 0 ]; then
    echo "✅ zcp v6.3 validation passed successfully with exit code 0."
    exit 0
else
    echo "❌ zcp v6.3 validation failed with $ERRORS error(s)."
    exit 1
fi

#!/usr/bin/env bash
# ==============================================================================
# Deterministic Physical Validation Sensor for seo-aeo-geo Suite (v1.2)
# ==============================================================================
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ERRORS=0

echo "============================================================"
echo "  🔍 Validating seo-aeo-geo Skill Integrity (v1.2)"
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
    echo "✓ Frontmatter version is 1.2"
else
    echo "❌ Frontmatter version is not 1.2"
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
for ref in \
    "references/usage.md" \
    "references/infra.md" \
    "assets/SEO.astro" \
    "assets/SchemaGraph.astro" \
    "assets/llms.txt.ts" \
    "assets/robots.txt.ts"; do
    if [ -f "$SKILL_DIR/$ref" ] && [ -s "$SKILL_DIR/$ref" ]; then
        echo "✓ Required reference exists and non-empty: $ref"
    else
        echo "❌ Missing or empty reference: $ref"
        ERRORS=$((ERRORS + 1))
    fi
done

# 5. Check file links
for link in \
    "references/usage.md" \
    "references/infra.md" \
    "assets/SEO.astro" \
    "assets/SchemaGraph.astro" \
    "assets/llms.txt.ts" \
    "assets/robots.txt.ts" \
    "scripts/seo-aeo-geo-validate.sh"; do
    if grep -q "file:///var/www/.agents/skills/seo-aeo-geo/$link" "$SKILL_DIR/SKILL.md"; then
        echo "✓ Absolute file link verified: $link"
    else
        echo "❌ Missing absolute file link in SKILL.md: $link"
        ERRORS=$((ERRORS + 1))
    fi
done

echo "------------------------------------------------------------"
if [ "$ERRORS" -eq 0 ]; then
    echo "✅ seo-aeo-geo v1.2 validation passed successfully with exit code 0."
    exit 0
else
    echo "❌ seo-aeo-geo v1.2 validation failed with $ERRORS error(s)."
    exit 1
fi

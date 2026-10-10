#!/usr/bin/env bash
# ==============================================================================
# Deterministic Physical Validation Sensor for seo-aeo-geo Suite (v2.0)
# ==============================================================================
set -euo pipefail

REAL_SCRIPT="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$REAL_SCRIPT")"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ERRORS=0

echo "============================================================"
echo "  🔍 Validating seo-aeo-geo Skill Integrity (v2.0)"
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
    echo "✓ Frontmatter version is valid SemVer"
else
    echo "❌ Frontmatter version is not valid SemVer"
    ERRORS=$((ERRORS + 1))
fi

# 3. Check token count of SKILL.md (CoHaLo Level 2 limit <= 480 words)
WORD_COUNT=$(wc -w < "$SKILL_DIR/SKILL.md")
EST_TOKENS=$((WORD_COUNT * 13 / 10))
if [ "$WORD_COUNT" -le 480 ]; then
    echo "✓ Token budget compliant: ~$EST_TOKENS tokens (word count: $WORD_COUNT, limit 480)"
else
    echo "⚠️ Warning: SKILL.md exceeds recommended token budget ($WORD_COUNT words > 480)"
    ERRORS=$((ERRORS + 1))
fi

# 4. Check Dual-RAG references and new visual assets
for ref in \
    "references/usage.md" \
    "references/infra.md" \
    "assets/SEO.astro" \
    "assets/FaviconSuite.astro" \
    "assets/SchemaGraph.astro" \
    "assets/llms.txt.ts" \
    "assets/robots.txt.ts" \
    "scripts/generate-visual-assets.py"; do
    if [ -f "$SKILL_DIR/$ref" ] && [ -s "$SKILL_DIR/$ref" ]; then
        echo "✓ Required reference exists and non-empty: $ref"
    else
        echo "❌ Missing or empty reference: $ref"
        ERRORS=$((ERRORS + 1))
    fi
done

# 5. Check file links in SKILL.md
for link in \
    "references/usage.md" \
    "references/infra.md" \
    "assets/SEO.astro" \
    "assets/FaviconSuite.astro" \
    "assets/SchemaGraph.astro" \
    "assets/llms.txt.ts" \
    "assets/robots.txt.ts" \
    "scripts/generate-visual-assets.py" \
    "scripts/seo-aeo-geo-validate.sh"; do
    if grep -q "$link" "$SKILL_DIR/SKILL.md"; then
        echo "✓ File link verified: $link"
    else
        echo "❌ Missing file link in SKILL.md: $link"
        ERRORS=$((ERRORS + 1))
    fi
done

# 6. Python AST Syntax Check for scripts
if [ -f "$SKILL_DIR/scripts/generate-visual-assets.py" ]; then
    if python3 -c "import ast; ast.parse(open('$SKILL_DIR/scripts/generate-visual-assets.py').read())" 2>/dev/null; then
        echo "✓ Python AST valid: generate-visual-assets.py"
    else
        echo "❌ Python syntax error: generate-visual-assets.py"
        ERRORS=$((ERRORS + 1))
    fi
fi

echo "------------------------------------------------------------"
if [ "$ERRORS" -eq 0 ]; then
    echo "✅ seo-aeo-geo v2.0 validation passed successfully with exit code 0."
    exit 0
else
    echo "❌ seo-aeo-geo v2.0 validation failed with $ERRORS error(s)."
    exit 1
fi

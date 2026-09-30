#!/usr/bin/env bash
# ==============================================================================
# Deterministic Physical Validation Sensor for cohalo Architecture Suite (v8.3)
# Standard: CoHaLo SOTA / Zero Tokens / Bounded Execution < 100ms
# ==============================================================================
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
trap 'find "$SKILL_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true; find "$SKILL_DIR" -type f -name "*.pyc" -delete 2>/dev/null || true' EXIT
ERRORS=0

echo "============================================================"
echo "  🔍 Validating cohalo Architecture Skill Integrity (v8.3)"
echo "============================================================"

# 1. Check SKILL.md existence
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "❌ Missing SKILL.md in $SKILL_DIR"
    ERRORS=$((ERRORS + 1))
else
    echo "✓ SKILL.md exists"
fi

# 2. Check frontmatter metadata.version
if grep -Eq 'version: "8\.[2-9]"' "$SKILL_DIR/SKILL.md"; then
    echo "✓ Frontmatter version is 8.x (>= 8.2)"
else
    echo "❌ Frontmatter version is not 8.x (>= 8.2)"
    ERRORS=$((ERRORS + 1))
fi

# 3. Check Dual-RAG references presence and non-emptiness
for ref in \
    "references/context.md" \
    "references/context_engineering_caching.md" \
    "references/prompt_engineering_foundations.md" \
    "references/sota_reasoning_prompting.md" \
    "references/antipatterns_deprecations.md" \
    "references/harness.md" \
    "references/loops.md"; do
    if [ -f "$SKILL_DIR/$ref" ] && [ -s "$SKILL_DIR/$ref" ]; then
        echo "✓ Required reference exists and non-empty: $ref"
    else
        echo "❌ Missing or empty reference: $ref"
        ERRORS=$((ERRORS + 1))
    fi
done

# 4. Check SKILL.md token budget (Progressive Disclosure Nivel 2: <= 550 tokens, hard limit 700)
WORD_COUNT=$(wc -w < "$SKILL_DIR/SKILL.md")
EST_TOKENS=$(awk -v w="$WORD_COUNT" 'BEGIN { printf "%.0f", w * 1.3 }')
echo "Calculated SKILL.md word count: $WORD_COUNT, estimated tokens: ~$EST_TOKENS"
if [ "$EST_TOKENS" -gt 700 ]; then
    echo "❌ SKILL.md exceeds 700 tokens hard budget (~$EST_TOKENS tokens). Router bloat!"
    ERRORS=$((ERRORS + 1))
elif [ "$EST_TOKENS" -gt 550 ]; then
    echo "⚠️ Warning: SKILL.md slightly exceeds recommended 550 tokens budget (~$EST_TOKENS tokens)."
else
    echo "✓ SKILL.md complies with Progressive Disclosure Level 2 budget (<=550 tokens)"
fi

# 5. Check Positive Guidance compliance (Zero negative phrasing in Hard Rules)
if grep -qiE "(prohibido|no hagas|no inventes)" "$SKILL_DIR/SKILL.md"; then
    echo "❌ Detected legacy negative phrasing in SKILL.md router. Enforce Positive Guidance!"
    ERRORS=$((ERRORS + 1))
else
    echo "✓ Positive Guidance verified: Zero negative prohibitive phrasing in SKILL.md"
fi

# 6. Check file links integrity in SKILL.md
for link in \
    "references/context.md" \
    "references/context_engineering_caching.md" \
    "references/prompt_engineering_foundations.md" \
    "references/sota_reasoning_prompting.md" \
    "references/antipatterns_deprecations.md" \
    "references/harness.md" \
    "references/loops.md" \
    "scripts/cohalo-validate.sh"; do
    if grep -q "$link" "$SKILL_DIR/SKILL.md"; then
        echo "✓ File link verified: $link"
    else
        echo "❌ Missing link to $link in SKILL.md"
        ERRORS=$((ERRORS + 1))
    fi
done

# 7. Check Physical Links in SKILL.md (Zero 404s)
while IFS= read -r link; do
    clean_path="${link#file://}"
    if [ -z "${clean_path#/}" ]; then
        continue
    fi
    if [ ! -e "$clean_path" ]; then
        echo "❌ Broken physical link in SKILL.md: $link (target does not exist)"
        ERRORS=$((ERRORS + 1))
    fi
done < <(grep -oE 'file:///[^ )"`]+' "$SKILL_DIR/SKILL.md" || true)
echo "✓ Physical file:/// links resolved and verified on filesystem"

echo "------------------------------------------------------------"
if [ "$ERRORS" -eq 0 ]; then
    echo "✅ cohalo v8.2 validation passed successfully with exit code 0."
    exit 0
else
    echo "❌ cohalo v8.2 validation failed with $ERRORS error(s)."
    exit 1
fi

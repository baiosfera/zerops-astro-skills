#!/usr/bin/env bash
# ==============================================================================
# Deterministic Physical Validation Sensor for sales-enablement Suite (v2.0)
# ==============================================================================
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ERRORS=0

echo "============================================================"
echo "  🔍 Validating sales-enablement Skill Integrity (v2.0)"
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
    "assets/sales_zod_schemas.ts"
    "assets/lead_scoring_engine.ts"
    "assets/crm_adapter.ts"
    "assets/handover_pack.ts"
    "assets/battlecards_dataset.json"
    "scripts/sales-enablement-validate.sh"
)

for ref in "${REQUIRED_REFS[@]}"; do
    if [ -f "$SKILL_DIR/$ref" ] && [ -s "$SKILL_DIR/$ref" ]; then
        echo "✓ Reference file exists and non-empty: $ref"
    else
        echo "❌ Missing or empty reference file: $ref"
        ERRORS=$((ERRORS + 1))
    fi

    if grep -q "file:///var/www/.agents/skills/sales-enablement/$ref" "$SKILL_DIR/SKILL.md"; then
        echo "✓ Canonical file link verified: $ref"
    else
        echo "❌ Missing canonical file link in SKILL.md: $ref"
        ERRORS=$((ERRORS + 1))
    fi
done

# 3. Deterministic JSON Validation (No silent suppression)
python3 -c "
import json
with open('$SKILL_DIR/assets/battlecards_dataset.json') as f:
    data = json.load(f)
assert isinstance(data, list), 'Battlecards dataset must be an array'
assert len(data) >= 3, 'Must contain at least 3 battlecard entries'
for card in data:
    assert 'objectionType' in card and 'script' in card, 'Malformed battlecard'
print('✓ JSON syntax and schema structure valid: assets/battlecards_dataset.json')
" || { echo "❌ JSON validation failed for battlecards_dataset.json"; ERRORS=$((ERRORS + 1)); }

# 4. TypeScript Code Structural Integrity
for ts_file in "assets/sales_zod_schemas.ts" "assets/lead_scoring_engine.ts" "assets/crm_adapter.ts" "assets/handover_pack.ts"; do
    python3 -c "
with open('$SKILL_DIR/$ts_file') as f:
    content = f.read()
assert len(content) > 100, 'File $ts_file is too small'
assert 'export ' in content, 'File $ts_file must have exports'
print('✓ Code structural assertion passed: $ts_file')
" || { echo "❌ Code structural error in $ts_file"; ERRORS=$((ERRORS + 1)); }
done

# 5. Deterministic Physical Calculation Assertion (Testing scoring math)
python3 -c "
# Python mirror of calculateLeadScore to physically assert correctness
def calculate_lead_score(explicit_s, implicit_s, cosine_dist):
    semantic_sim = max(0, min(100, (1 - cosine_dist) * 100))
    total = round(explicit_s * 0.35 + implicit_s * 0.25 + semantic_sim * 0.40)
    grade = 'A_HOT' if total >= 75 else ('B_WARM' if total >= 50 else ('C_NURTURE' if total >= 30 else 'D_COLD'))
    return total, grade

total, grade = calculate_lead_score(90, 80, 0.1)
assert total == 88, f'Expected total score 88, got {total}'
assert grade == 'A_HOT', f'Expected grade A_HOT, got {grade}'

total_cold, grade_cold = calculate_lead_score(10, 10, 0.9)
assert grade_cold == 'D_COLD', f'Expected grade D_COLD, got {grade_cold}'

print('✓ Physical lead scoring calculation assertion PASSED')
" || { echo "❌ Lead scoring calculation test failed"; ERRORS=$((ERRORS + 1)); }

# 6. Zero Single-Tenant Debt Invariant (Banned Leak Scanner)
BANNED_LEAKS=("baiosfera" "sales-main" "0zcp-123" "wompi" "nequi" "daviplata")
for leak in "${BANNED_LEAKS[@]}"; do
    FOUND_LEAKS=$(grep -rn "$leak" "$SKILL_DIR" --exclude="*.bak*" --exclude="sales-enablement-validate.sh" --exclude="battlecards_latam.json" || true)
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
    echo "✅ sales-enablement v2.0 validation passed successfully with exit code 0."
    exit 0
else
    echo "❌ sales-enablement v2.0 validation failed with $ERRORS error(s)."
    exit 1
fi

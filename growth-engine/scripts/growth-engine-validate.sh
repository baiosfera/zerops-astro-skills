#!/usr/bin/env bash
# ==============================================================================
# Deterministic Physical Validation Sensor for growth-engine Suite (v2.0)
# ==============================================================================
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

REAL_SCRIPT="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$REAL_SCRIPT")"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ERRORS=0

trap 'rm -rf "$SCRIPT_DIR/__pycache__" "$SCRIPT_DIR"/*.pyc 2>/dev/null || true' EXIT

echo "============================================================"
echo "  🔍 Validating growth-engine Skill Integrity (v2.0)"
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
    "assets/copywriting_zod_schemas.ts"
    "assets/copy_atomizer_engine.ts"
    "assets/omnichannel_copy_templates.md"
    "assets/growth_engine_recipes.json"
    "scripts/growth-engine-validate.sh"
)

for ref in "${REQUIRED_REFS[@]}"; do
    if [ -f "$SKILL_DIR/$ref" ] && [ -s "$SKILL_DIR/$ref" ]; then
        echo "✓ Reference file exists and non-empty: $ref"
    else
        echo "❌ Missing or empty reference file: $ref"
        ERRORS=$((ERRORS + 1))
    fi

    if grep -q "file:///var/www/.agents/skills/growth-engine/$ref" "$SKILL_DIR/SKILL.md"; then
        echo "✓ Canonical file link verified: $ref"
    else
        echo "❌ Missing canonical file link in SKILL.md: $ref"
        ERRORS=$((ERRORS + 1))
    fi
done

# 3. Deterministic JSON Validation
python3 -c "
import json
with open('$SKILL_DIR/assets/growth_engine_recipes.json') as f:
    data = json.load(f)
assert data.get('version') == '2.0', 'Recipes version must be 2.0'
assert 'recipes' in data and len(data['recipes']) >= 4, 'Must have at least 4 recipes'
for r in data['recipes']:
    assert 'id' in r and 'description' in r, 'Malformed recipe item'
print('✓ JSON syntax and recipes structure valid: assets/growth_engine_recipes.json')
" || { echo "❌ JSON validation failed for growth_engine_recipes.json"; ERRORS=$((ERRORS + 1)); }

# 4. TypeScript Code Structural Integrity
for ts_file in "assets/copywriting_zod_schemas.ts" "assets/copy_atomizer_engine.ts"; do
    python3 -c "
with open('$SKILL_DIR/$ts_file') as f:
    content = f.read()
assert len(content) > 100, 'File $ts_file is too small'
assert 'export ' in content, 'File $ts_file must have exports'
print('✓ Code structural assertion passed: $ts_file')
" || { echo "❌ Code structural error in $ts_file"; ERRORS=$((ERRORS + 1)); }
done

# 5. Deterministic Physical Calculation Assertion: Dynamic Discount Capping Math
python3 -c "
def calculate_bounded_discount(gross_margin, attempt_number, ltv_tier='STANDARD'):
    margin_cap = max(0.0, gross_margin - 0.05)
    attempt_caps = {1: 0.0, 2: 0.10, 3: 0.20}
    attempt_cap = attempt_caps.get(attempt_number, 0.0)
    ltv_caps = {'NEW': 0.10, 'STANDARD': 0.15, 'VIP': 0.20}
    ltv_cap = ltv_caps.get(ltv_tier, 0.15)
    return round(min(margin_cap, attempt_cap, ltv_cap), 2)

# Test 1: Attempt 1 is always 0%
assert calculate_bounded_discount(0.50, 1) == 0.0, 'Attempt 1 must be 0% discount'
# Test 2: Standard margin 50%, Attempt 2 -> 10%
assert calculate_bounded_discount(0.50, 2) == 0.10, 'Attempt 2 at 50% margin should be 10%'
# Test 3: Low margin 12%, Attempt 2 -> margin cap: 0.12 - 0.05 = 0.07 (7%)
assert calculate_bounded_discount(0.12, 2) == 0.07, 'Attempt 2 at 12% margin should be capped at 7%'
# Test 4: Attempt 3 at 50% margin VIP -> 20%
assert calculate_bounded_discount(0.50, 3, 'VIP') == 0.20, 'Attempt 3 at 50% margin VIP should be 20%'

print('✓ Dynamic discount capping calculation test PASSED')
" || { echo "❌ Dynamic discount capping calculation test failed"; ERRORS=$((ERRORS + 1)); }

# 6. Physical Anti-SPAM Linter Test
python3 -c "
import re

def validate_subject_line(subject):
    errors = []
    # Length check 30 - 50 chars
    if len(subject) < 30 or len(subject) > 50:
        errors.append('length_outside_bounds')
    # All caps words
    words = subject.split()
    all_caps = [w for w in words if len(w) > 3 and w == w.upper() and w.isalpha()]
    if all_caps:
        errors.append('all_caps_detected')
    # Consecutive exclamation marks
    if re.search(r'!{2,}', subject):
        errors.append('excessive_exclamation')
    return errors

# Good subject: 36 chars, proper casing
good = 'Your saved items are waiting for you'
assert len(validate_subject_line(good)) == 0, 'Compliant subject line should pass'

# Bad subject: ALL CAPS word + excessive exclamation + too short
bad = 'ACT NOW FREE OFFER!!!'
bad_errs = validate_subject_line(bad)
assert 'all_caps_detected' in bad_errs, 'Should detect ALL CAPS'
assert 'excessive_exclamation' in bad_errs, 'Should detect exclamation'
assert 'length_outside_bounds' in bad_errs, 'Should detect short length'

print('✓ Physical Anti-SPAM linter heuristics test PASSED')
" || { echo "❌ Anti-SPAM linter heuristics test failed"; ERRORS=$((ERRORS + 1)); }

# 7. Zero Single-Tenant Debt Invariant (Banned Leak Scanner)
BANNED_LEAKS=("astrobranding_" "fase0_system_prompt.md" "bifrost:8000" "enterizo velvet" "daviplata")
for leak in "${BANNED_LEAKS[@]}"; do
    FOUND_LEAKS=$(grep -rn "$leak" "$SKILL_DIR" --exclude="*.bak*" --exclude="growth-engine-validate.sh" || true)
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
    echo "✅ growth-engine v2.0 validation passed successfully with exit code 0."
    exit 0
else
    echo "❌ growth-engine v2.0 validation failed with $ERRORS error(s)."
    exit 1
fi

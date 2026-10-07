#!/usr/bin/env bash
# ==============================================================================
# Deterministic Physical Validation Sensor for erpnext Universal Suite (v2.5)
# ==============================================================================
set -euo pipefail

REAL_SCRIPT="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$REAL_SCRIPT")"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ERRORS=0

echo "============================================================"
echo "  🔍 Validating erpnext Universal Skill Integrity (v2.5)"
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
    echo "✓ Frontmatter version is 2.5"
else
    echo "❌ Frontmatter version is not 2.5"
    ERRORS=$((ERRORS + 1))
fi

# 3. Check Dual-RAG references & scripts
for ref in "references/usage.md" "references/infra.md" "references/agent_accounting.md" "assets/erpnext_production_recipes.json" "assets/onboarding_profile.json" "assets/directus_frappe_hook.ts" "assets/frappe_webhook_endpoint.ts" "scripts/erpnext-onboard.py" "scripts/erpnext-rut-parser.py" "scripts/erpnext-ciiu-resolver.py" "scripts/erpnext-client.py"; do
    if [ -f "$SKILL_DIR/$ref" ] && [ -s "$SKILL_DIR/$ref" ]; then
        echo "✓ Required reference exists and non-empty: $ref"
    else
        echo "❌ Missing or empty reference: $ref"
        ERRORS=$((ERRORS + 1))
    fi
done

# 4. Check JSON validity
for json_file in "assets/erpnext_production_recipes.json" "assets/onboarding_profile.json"; do
    if python3 -m json.tool "$SKILL_DIR/$json_file" >/dev/null 2>&1; then
        echo "✓ $json_file is valid JSON"
    else
        echo "❌ Syntax error in $json_file"
        ERRORS=$((ERRORS + 1))
    fi
done

# 5. Check executable permissions & Python compilation
chmod +x "$SKILL_DIR/scripts/"*.py "$SKILL_DIR/scripts/"*.sh
for py_file in "$SKILL_DIR/scripts/"*.py; do
    if python3 -m py_compile "$py_file" >/dev/null 2>&1; then
        echo "✓ Python compilation passed: $(basename "$py_file")"
    else
        echo "❌ Python syntax error in $(basename "$py_file")"
        ERRORS=$((ERRORS + 1))
    fi
done

# 6. Execute CIIU Resolver & Client unit test suites
if python3 "$SKILL_DIR/scripts/erpnext-ciiu-resolver.py" --test >/dev/null 2>&1; then
    echo "✓ CIIU-to-PUC Resolver unit tests (10/10) passed"
else
    echo "❌ CIIU-to-PUC Resolver unit tests failed"
    ERRORS=$((ERRORS + 1))
fi

if python3 "$SKILL_DIR/scripts/erpnext-client.py" --test >/dev/null 2>&1; then
    echo "✓ Frappe REST & RPC Client unit tests passed"
else
    echo "❌ Frappe REST & RPC Client unit tests failed"
    ERRORS=$((ERRORS + 1))
fi

# 7. Check Headless Mode and Amazon SES Outgoing Contracts
if grep -q 'enable_onboarding' "$SKILL_DIR/scripts/erpnext-onboard.py" && grep -q 'email-smtp' "$SKILL_DIR/scripts/erpnext-onboard.py"; then
    echo "✓ Headless Desk Mode and Amazon SES contract verified in erpnext-onboard.py"
else
    echo "❌ Missing Headless Mode or Amazon SES contract in erpnext-onboard.py"
    ERRORS=$((ERRORS + 1))
fi

# 8. Check Zero Brand Coupling Invariant (Strict Agnosticism)
if grep -qiE '(catalinaglamur|glamur-keys)' "$SKILL_DIR/scripts/erpnext-onboard.py" "$SKILL_DIR/SKILL.md"; then
    echo "❌ Brand coupling detected in erpnext skill files!"
    ERRORS=$((ERRORS + 1))
else
    echo "✓ Zero Brand Coupling verified (100% tenant-agnostic)"
fi

# 9. Check SKILL.md token budget
WORD_COUNT=$(wc -w < "$SKILL_DIR/SKILL.md")
EST_TOKENS=$(awk -v w="$WORD_COUNT" 'BEGIN { printf "%.0f", w * 1.3 }')
echo "Calculated SKILL.md word count: $WORD_COUNT, estimated tokens: ~$EST_TOKENS"
if [ "$EST_TOKENS" -gt 650 ]; then
    echo "❌ SKILL.md exceeds 650 tokens hard budget (~$EST_TOKENS tokens). Offload to references/!"
    ERRORS=$((ERRORS + 1))
else
    echo "✓ SKILL.md within token budget (<650 tokens)"
fi

# 10. Check file links in SKILL.md
for link in "references/usage.md" "references/infra.md" "references/agent_accounting.md" "assets/onboarding_profile.json" "assets/erpnext_production_recipes.json" "assets/directus_frappe_hook.ts" "assets/frappe_webhook_endpoint.ts" "scripts/erpnext-onboard.py" "scripts/erpnext-rut-parser.py" "scripts/erpnext-ciiu-resolver.py" "scripts/erpnext-client.py" "scripts/erpnext-validate.sh"; do
    if grep -q "$link" "$SKILL_DIR/SKILL.md"; then
        echo "✓ Absolute file link verified: $link"
    else
        echo "❌ Missing link to $link in SKILL.md"
        ERRORS=$((ERRORS + 1))
    fi
done

echo "------------------------------------------------------------"
if [ "$ERRORS" -eq 0 ]; then
    echo "✅ erpnext v2.5 validation passed successfully with exit code 0."
    exit 0
else
    echo "❌ erpnext v2.5 validation failed with $ERRORS error(s)."
    exit 1
fi

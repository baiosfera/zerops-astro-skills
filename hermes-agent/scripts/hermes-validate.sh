#!/usr/bin/env bash
# ==============================================================================
# Hermes-Agent Dual-RAG Skill Physical Validation Sensor
# ==============================================================================
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=== [SENSOR] Validating Hermes-Agent Skill Structure ==="
echo "• Target Directory: $SKILL_DIR"

# 1. Check SKILL.md
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "❌ ERROR: SKILL.md missing!"
    exit 1
fi

if ! grep -q 'name: "hermes-agent"' "$SKILL_DIR/SKILL.md"; then
    echo "❌ ERROR: SKILL.md missing valid quoted frontmatter name!"
    exit 1
fi
echo "✓ SKILL.md frontmatter verified."

# 2. Check References
REQUIRED_REFS=("usage.md" "infra.md" "bridge_agy.md" "suite_integration.md")
for ref in "${REQUIRED_REFS[@]}"; do
    if [ ! -s "$SKILL_DIR/references/$ref" ]; then
        echo "❌ ERROR: references/$ref is missing or empty!"
        exit 1
    fi
    echo "✓ Reference verified: references/$ref"
done

# 3. Check Assets
REQUIRED_ASSETS=("config_production_template.yaml" "zerops_hermes_recipe.yaml" "hermes_tools_bundle.py")
for asset in "${REQUIRED_ASSETS[@]}"; do
    if [ ! -s "$SKILL_DIR/assets/$asset" ]; then
        echo "❌ ERROR: assets/$asset is missing or empty!"
        exit 1
    fi
    echo "✓ Asset verified: assets/$asset"
done

# 4. Compile Python tool bundle
if command -v python3 >/dev/null 2>&1; then
    python3 -m py_compile "$SKILL_DIR/assets/hermes_tools_bundle.py"
    echo "✓ Python compilation verified: assets/hermes_tools_bundle.py"
fi

echo "=== [SENSOR RESULT] Hermes-Agent Dual-RAG Skill PASSED (Exit 0) ==="
exit 0

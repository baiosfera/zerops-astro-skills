#!/usr/bin/env bash
set -eo pipefail

SKILL_DIR="/var/www/.agents/skills/bifrost"

echo "=== [Bifrost Dual-RAG Skill Validation Sensor] ==="

# 1. Check required files
FILES=(
  "${SKILL_DIR}/SKILL.md"
  "${SKILL_DIR}/references/usage.md"
  "${SKILL_DIR}/references/infra.md"
  "${SKILL_DIR}/assets/config_production_template.json"
  "${SKILL_DIR}/assets/zerops_bifrost_recipe.yaml"
)

for file in "${FILES[@]}"; do
  if [ ! -f "$file" ]; then
    echo "❌ Missing required file: $file"
    exit 1
  fi
  if [ ! -s "$file" ]; then
    echo "❌ Empty file detected: $file"
    exit 1
  fi
  echo "✅ Found: $(basename "$file") ($(wc -l < "$file") lines)"
done

# 2. Validate JSON syntax
if command -v jq >/dev/null 2>&1; then
  jq empty "${SKILL_DIR}/assets/config_production_template.json"
  echo "✅ JSON syntax valid: config_production_template.json"
fi

# 3. Validate Token / Word count of SKILL.md
WORDS=$(wc -w < "${SKILL_DIR}/SKILL.md")
echo "ℹ️  SKILL.md word count: $WORDS (budget: 150 - 600 words)"
if [ "$WORDS" -gt 650 ]; then
  echo "⚠️ Warning: SKILL.md exceeds ideal executive token budget ($WORDS words)"
fi

# 4. Check 2026 Invariant Keywords
grep -q '"version": 2' "${SKILL_DIR}/assets/config_production_template.json" || (echo "❌ Missing version 2 in config schema" && exit 1)
grep -Eq 'version: "[0-9]+\.[0-9]+"' "${SKILL_DIR}/SKILL.md" || (echo "❌ Missing version 2.1 in SKILL.md metadata" && exit 1)
grep -q 'custom_provider_config' "${SKILL_DIR}/assets/config_production_template.json" || (echo "❌ Missing custom_provider_config in config" && exit 1)
grep -q 'vector_store' "${SKILL_DIR}/assets/config_production_template.json" || (echo "❌ Missing vector_store in config" && exit 1)
grep -q '"mcp":' "${SKILL_DIR}/assets/config_production_template.json" || (echo "❌ Missing mcp in config" && exit 1)
grep -q 'key_ids' "${SKILL_DIR}/references/usage.md" || (echo "❌ Missing key_ids 2026 attribute" && exit 1)
grep -q 'health' "${SKILL_DIR}/references/infra.md" || (echo "❌ Missing /health probe" && exit 1)

echo "🎯 [SUCCESS]: All Bifrost skill sensors passed with exit code 0."
exit 0

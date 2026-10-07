#!/usr/bin/env bash
# ==============================================================================
# Deterministic Physical Sensor: freellmapi Skill Validator (v1.2)
# ==============================================================================
set -euo pipefail

REAL_SCRIPT="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$REAL_SCRIPT")"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"

echo "============================================================"
echo "  🔍 Validating Sovereign Skill: freellmapi"
echo "  Directory: $SKILL_DIR"
echo "============================================================"

# 1. Check SKILL.md existence
if [[ ! -f "$SKILL_MD" ]]; then
  echo "❌ FAIL: SKILL.md not found at $SKILL_MD" >&2
  exit 1
fi
echo "✅ PASS: SKILL.md exists"

# 2. Check frontmatter structure
if ! grep -q '^name: "freellmapi"' "$SKILL_MD"; then
  echo "❌ FAIL: Quoted name 'freellmapi' not found in frontmatter" >&2
  exit 1
fi
if ! grep -Eq 'version: "[0-9]+\.[0-9]+"' "$SKILL_MD"; then
  echo "❌ FAIL: Version 1.2 not found in SKILL.md frontmatter" >&2
  exit 1
fi
echo "✅ PASS: Valid YAML frontmatter name and version 1.2"

# 3. Check token count of SKILL.md (rough word count proxy: target 180-450, hard max 700)
WORD_COUNT=$(wc -w < "$SKILL_MD")
echo "ℹ️ INFO: Word count of SKILL.md is $WORD_COUNT words"
if [[ "$WORD_COUNT" -gt 700 ]]; then
  echo "❌ FAIL: SKILL.md word count ($WORD_COUNT) exceeds hard max 700 words" >&2
  exit 1
fi
echo "✅ PASS: Executive router brevity satisfied (<= 700 words)"

# 4. Check required references
REQUIRED_REFS=("usage.md" "infra.md" "agy_bifrost_bridge.md")
for ref in "${REQUIRED_REFS[@]}"; do
  REF_PATH="$SKILL_DIR/references/$ref"
  if [[ ! -f "$REF_PATH" ]]; then
    echo "❌ FAIL: Missing required reference: $REF_PATH" >&2
    exit 1
  fi
  echo "✅ PASS: Reference exists: references/$ref"
done

# 5. Check required assets
REQUIRED_ASSETS=("freellmapi_production_template.json" "zerops_freellmapi_recipe.yaml")
for asset in "${REQUIRED_ASSETS[@]}"; do
  ASSET_PATH="$SKILL_DIR/assets/$asset"
  if [[ ! -f "$ASSET_PATH" ]]; then
    echo "❌ FAIL: Missing required asset: $ASSET_PATH" >&2
    exit 1
  fi
  echo "✅ PASS: Asset exists: assets/$asset"
done

# 6. Check JSON syntax of production template
if command -v jq >/dev/null 2>&1; then
  jq empty "$SKILL_DIR/assets/freellmapi_production_template.json"
  echo "✅ PASS: JSON syntax valid for assets/freellmapi_production_template.json"
fi

# 7. Check clickable file:/// links standard
if ! grep -q 'file:///' "$SKILL_MD"; then
  echo "❌ FAIL: SKILL.md must use clickable file:/// absolute links" >&2
  exit 1
fi
echo "✅ PASS: Absolute file:/// links verified in SKILL.md"

echo "============================================================"
echo "  🎉 All physical sensor checks PASSED for freellmapi (exit 0)"
echo "============================================================"
exit 0

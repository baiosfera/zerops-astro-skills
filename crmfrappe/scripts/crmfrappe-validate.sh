#!/usr/bin/env bash
# ==============================================================================
# Deterministic Physical Validation Sensor: crmfrappe (v1.2)
# Enforces Supreme Directive v6.8, Fractal CoHaLo v6.7 & Token Budgets
# ==============================================================================
set -eo pipefail

SKILL_DIR="/var/www/.agents/skills/crmfrappe"
SKILL_FILE="${SKILL_DIR}/SKILL.md"
USAGE_FILE="${SKILL_DIR}/references/usage.md"
INFRA_FILE="${SKILL_DIR}/references/infra.md"
RECIPES_FILE="${SKILL_DIR}/assets/crmfrappe_production_recipes.json"
CLIENT_SCRIPT="${SKILL_DIR}/scripts/crmfrappe-client.py"
ONBOARD_SCRIPT="${SKILL_DIR}/scripts/crmfrappe-onboard.py"

echo "=== [1/8] Validating Directory Structure ==="
test -d "${SKILL_DIR}" || { echo "[ERROR] Skill directory missing"; exit 1; }
test -d "${SKILL_DIR}/references" || { echo "[ERROR] references/ directory missing"; exit 1; }
test -d "${SKILL_DIR}/assets" || { echo "[ERROR] assets/ directory missing"; exit 1; }
test -d "${SKILL_DIR}/scripts" || { echo "[ERROR] scripts/ directory missing"; exit 1; }
echo "[✓] Directory structure complete."

echo "=== [2/8] Validating Dual-RAG Files Presence ==="
test -s "${SKILL_FILE}" || { echo "[ERROR] SKILL.md missing or empty"; exit 1; }
test -s "${USAGE_FILE}" || { echo "[ERROR] references/usage.md missing or empty"; exit 1; }
test -s "${INFRA_FILE}" || { echo "[ERROR] references/infra.md missing or empty"; exit 1; }
test -s "${RECIPES_FILE}" || { echo "[ERROR] assets/crmfrappe_production_recipes.json missing or empty"; exit 1; }
test -s "${CLIENT_SCRIPT}" || { echo "[ERROR] scripts/crmfrappe-client.py missing or empty"; exit 1; }
test -s "${ONBOARD_SCRIPT}" || { echo "[ERROR] scripts/crmfrappe-onboard.py missing or empty"; exit 1; }
echo "[✓] All Dual-RAG files verified on disk."

echo "=== [3/8] Validating JSON Recipes Schema ==="
python3 -m json.tool "${RECIPES_FILE}" > /dev/null || { echo "[ERROR] Invalid JSON in recipes file"; exit 1; }
echo "[✓] JSON syntax in recipes is strictly valid."

echo "=== [4/8] Validating Python Scripts Syntax ==="
python3 -m py_compile "${CLIENT_SCRIPT}" || { echo "[ERROR] Syntax error in crmfrappe-client.py"; exit 1; }
python3 -m py_compile "${ONBOARD_SCRIPT}" || { echo "[ERROR] Syntax error in crmfrappe-onboard.py"; exit 1; }
echo "[✓] Python scripts compile without error."

echo "=== [5/8] Validating SKILL.md Token Budget & Frontmatter ==="
WORD_COUNT=$(wc -w < "${SKILL_FILE}")
EST_TOKENS=$(awk -v w="${WORD_COUNT}" 'BEGIN { printf "%.0f", w * 1.3 }')
echo "Calculated word count: ${WORD_COUNT}, estimated tokens: ~${EST_TOKENS}"

if [ "${EST_TOKENS}" -gt 700 ]; then
  echo "[ERROR] SKILL.md exceeds 700 tokens hard budget (~${EST_TOKENS} tokens). Offload to references/!"
  exit 1
fi

grep -q "^name: crmfrappe" "${SKILL_FILE}" || { echo "[ERROR] Frontmatter name != crmfrappe"; exit 1; }
grep -q "^description:" "${SKILL_FILE}" || { echo "[ERROR] Frontmatter description missing"; exit 1; }
grep -Eq 'version: "[0-9]+\.[0-9]+"' "${SKILL_FILE}" || { echo "[ERROR] Frontmatter version != 1.2"; exit 1; }
echo "[✓] SKILL.md conforms to Agent Skills specification and token limits."

echo "=== [6/8] Validating file:/// Markdown Link Integrity ==="
grep -q "file:///var/www/.agents/skills/crmfrappe" "${SKILL_FILE}" || {
  echo "[ERROR] SKILL.md lacks file:/// links for code-server / IDE navigation"; exit 1;
}
echo "[✓] Absolute file:/// links verified for 1-click navigation."

echo "=== [7/8] Validating Executable Bits ==="
chmod +x "${CLIENT_SCRIPT}" "${ONBOARD_SCRIPT}" "${SKILL_DIR}/scripts/crmfrappe-validate.sh"
test -x "${CLIENT_SCRIPT}" || { echo "[ERROR] crmfrappe-client.py not executable"; exit 1; }
test -x "${ONBOARD_SCRIPT}" || { echo "[ERROR] crmfrappe-onboard.py not executable"; exit 1; }
echo "[✓] Scripts marked as executable."

echo "=== [8/8] Testing Headless Onboarding CLI Interface ==="
python3 "${ONBOARD_SCRIPT}" --help > /dev/null || { echo "[ERROR] crmfrappe-onboard.py --help failed"; exit 1; }
echo "[✓] Headless onboarding CLI interface verified offline."

echo "=========================================================="
echo "🎉 ALL PHYSICAL SENSOR CHECKS PASSED FOR crmfrappe (v1.2)"
echo "=========================================================="
exit 0

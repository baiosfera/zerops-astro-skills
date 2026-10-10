#!/usr/bin/env bash
# ==============================================================================
# Research Skill Validation Harness & MCP Health Sensor (v8.2)
# ==============================================================================
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

REAL_SCRIPT="$(readlink -f "${BASH_SOURCE[0]}")"
SKILL_DIR="$(cd "$(dirname "$REAL_SCRIPT")/.." && pwd)"
trap 'find "$SKILL_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true; find "$SKILL_DIR" -type f -name "*.pyc" -delete 2>/dev/null || true' EXIT
ERRORS=0

echo "============================================================"
echo "  [Research v8.2] Sensor de Validación y Salud Epistémica"
echo "============================================================"

# 1. Validar integridad de archivos SSoT
echo "• Validando archivos contractuales..."
for f in "SKILL.md" "references/usage.md" "references/infra.md" "references/tools.md" "references/heuristics.md" "assets/research_query_matrix.json" "assets/subagent_prompt_contract.md"; do
    if [ -f "$SKILL_DIR/$f" ]; then
        echo "  ✓ $f presente ($(wc -l < "$SKILL_DIR/$f") líneas)"
    else
        echo "  ❌ FALTA archivo crítico: $f"
        ERRORS=$((ERRORS + 1))
    fi
done

# 2. Validar versión en Frontmatter (Dynamic SemVer)
echo "• Validando metadata.version en SKILL.md..."
if grep -Eq 'version: "(7\.[0-9]+|8\.[0-9]+)"' "$SKILL_DIR/SKILL.md"; then
    echo "  ✓ Versión SemVer validada en Frontmatter."
else
    echo "  ❌ Error: Falta versión 7.x/8.x en Frontmatter."
    ERRORS=$((ERRORS + 1))
fi

# 2.1 Validar Rule 7 (Action-First Execution Lockdown & Epistemic Receipt)
echo "• Validando Rule 7 (Action-First Lockdown & Epistemic Receipt)..."
if grep -q "Action-First Execution Lockdown" "$SKILL_DIR/SKILL.md" && grep -q "epistemic_attestation" "$SKILL_DIR/SKILL.md"; then
    echo "  ✓ Rule 7 y contrato de recibo <epistemic_attestation> validados."
else
    echo "  ❌ Error: Falta Rule 7 o contrato de recibo <epistemic_attestation> en SKILL.md."
    ERRORS=$((ERRORS + 1))
fi

# 2.2 Validar Rule 9 & Zero-Local Isolation Invariant
echo "• Validando Rule 9 & Zero-Local Isolation Invariant..."
if grep -q "Zero-Local Isolation & Mandatory Web Grounding" "$SKILL_DIR/SKILL.md" && grep -q "Zero-Local Isolation & Mandatory Web Grounding Invariant" "$SKILL_DIR/assets/subagent_prompt_contract.md"; then
    echo "  ✓ Rule 9 y Zero-Local Isolation Invariant validados físicamente en SKILL.md y contrato de subagente."
else
    echo "  ❌ Error: Falta Rule 9 o Zero-Local Isolation Invariant en SKILL.md o subagent_prompt_contract.md."
    ERRORS=$((ERRORS + 1))
fi

# 3. Validar Presupuesto de Tokens Dual-RAG
echo "• Validando Presupuesto de Tokens de Router Ejecutivo (CoHaLo)..."
WORD_COUNT=$(wc -w < "$SKILL_DIR/SKILL.md")
EST_TOKENS=$((WORD_COUNT * 13 / 10))
echo "  ℹ Conteo actual: $WORD_COUNT palabras (~$EST_TOKENS tokens)"
if [ "$EST_TOKENS" -le 1000 ]; then
    echo "  ✓ Presupuesto ejecutivo CoHaLo respetado (~$EST_TOKENS tokens <= 1000 tokens)."
else
    echo "  ⚠️ Warning: SKILL.md excede presupuesto recomendado (~$EST_TOKENS tokens)."
fi

# 4. Validar Autonomía del Contrato de Subagente (Zero Capping)
echo "• Validando autonomía del contrato de subagente..."
if grep -qiE "(extrae solo de 3 a 5|no consumas)" "$SKILL_DIR/assets/subagent_prompt_contract.md"; then
    echo "  ❌ Error: Cláusulas castradoras detectadas en subagent_prompt_contract.md."
    ERRORS=$((ERRORS + 1))
else
    echo "  ✓ Contrato de subagente validado: Libertad operativa total sin límites artificiales."
fi

# 5. Validar Zero-Mermaid Invariant en SKILL.md
echo "• Validando Zero-Mermaid Invariant en SKILL.md..."
if grep -q '```mermaid' "$SKILL_DIR/SKILL.md"; then
    echo "  ❌ Error: Se detectó diagrama Mermaid en SKILL.md. Debe residir en references/."
    ERRORS=$((ERRORS + 1))
else
    echo "  ✓ Zero-Mermaid Invariant validado en SKILL.md."
fi

# 6. Validar enlaces canónicos file:///
echo "• Validando enlaces canónicos en SKILL.md..."
for ref in "references/usage.md" "references/infra.md" "references/tools.md" "references/heuristics.md" "assets/subagent_prompt_contract.md" "assets/research_query_matrix.json" "scripts/research-validate.sh"; do
    if grep -q "$ref" "$SKILL_DIR/SKILL.md"; then
        echo "  ✓ Enlace hacia $ref validado."
    else
        echo "  ❌ Error: Falta enlace a $ref en SKILL.md."
        ERRORS=$((ERRORS + 1))
    fi
done

# 7. Validar JSON Schema de la matriz de consultas
echo "• Validando sintaxis de research_query_matrix.json..."
if jq empty "$SKILL_DIR/assets/research_query_matrix.json" 2>/dev/null; then
    ROULES_COUNT=$(jq '.routing_rules | length' "$SKILL_DIR/assets/research_query_matrix.json")
    ENGINES_COUNT=$(jq '.engines_catalog | map(length) | add' "$SKILL_DIR/assets/research_query_matrix.json")
    echo "  ✓ JSON válido: $ROULES_COUNT reglas de enrutamiento y $ENGINES_COUNT motores registrados."
else
    echo "  ❌ Error: JSON corrupto en research_query_matrix.json"
    ERRORS=$((ERRORS + 1))
fi

# 8. Validar memoria local Engram
echo "• Validando memoria semántica local Engram..."
if command -v engram &>/dev/null || [ -x "/var/www/.bin/engram" ]; then
    ENGRAM_BIN=$(command -v engram 2>/dev/null || echo "/var/www/.bin/engram")
    if $ENGRAM_BIN status &>/dev/null; then
        echo "  ✓ Engram LTM activo y operativo."
    else
        echo "  ⚠️ Engram presente pero no respondió a status."
    fi
else
    echo "  ⚠️ Binario engram no encontrado en PATH."
fi

# 9. Validar herramientas de scraping local
echo "• Validando motores de scraping local..."
if command -v python3 &>/dev/null; then
    echo "  ✓ Python 3 disponible para Crawl4AI."
fi
if command -v node &>/dev/null || command -v bun &>/dev/null; then
    echo "  ✓ Node/Bun disponible para Playwright / Puppeteer."
fi

# 10. Validar resolución física de enlaces file:///
echo "• Validando resolución física de enlaces file:///..."
LINK_ERRORS=0
while IFS= read -r link; do
    clean_path="${link#file://}"
    if [ -n "$clean_path" ] && [ ! -e "$clean_path" ]; then
        echo "  ❌ Enlace roto detectado: $link"
        LINK_ERRORS=$((LINK_ERRORS + 1))
    fi
done < <(grep -h -oE 'file:///[^ )"`]+' "$SKILL_DIR/SKILL.md" "$SKILL_DIR/references/"*.md 2>/dev/null || true)
if [ "$LINK_ERRORS" -eq 0 ]; then
    echo "  ✓ Enlaces físicos file:/// validados sin 404s."
else
    ERRORS=$((ERRORS + LINK_ERRORS))
fi

echo "============================================================"
if [ "$ERRORS" -eq 0 ]; then
    echo "  ✅ Validación EXITOSA: Skill Research v8.2 al 100% de integridad física."
    exit 0
else
    echo "  ❌ Validación FALLIDA con $ERRORS errores."
    exit 1
fi

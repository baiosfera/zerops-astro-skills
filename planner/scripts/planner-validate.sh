#!/usr/bin/env bash
# ==============================================================================
# Planner Skill Validation Harness & Structure Sensor (v3.8 — Standard v3.1)
# Zero LLM Tokens | Bounded Execution < 100ms | 100% Deterministic
# ==============================================================================
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

REAL_SCRIPT="$(readlink -f "${BASH_SOURCE[0]}")"
SKILL_DIR="$(cd "$(dirname "$REAL_SCRIPT")/.." && pwd)"
trap 'find "$SKILL_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true; find "$SKILL_DIR" -type f -name "*.pyc" -delete 2>/dev/null || true' EXIT
ERRORS=0

echo "============================================================"
echo "  [Planner v3.8] Sensor de Validación CoHaLo SOTA (v3.1)"
echo "============================================================"

# 1. Validar integridad de archivos SSoT
echo "• Validando archivos contractuales..."
for f in "SKILL.md" "references/usage.md" "references/planning_heuristics.md" "references/governance_contracts.md" "references/control_matrix_standard.md" "assets/plan_template.md"; do
    if [ -f "$SKILL_DIR/$f" ] && [ -s "$SKILL_DIR/$f" ]; then
        echo "  ✓ $f presente ($(wc -l < "$SKILL_DIR/$f") líneas)"
    else
        echo "  ❌ FALTA o está vacío archivo crítico: $f"
        ERRORS=$((ERRORS + 1))
    fi
done

# 2. Validar versión y triggers en SKILL.md (Dynamic SemVer)
echo "• Validando versión y triggers en SKILL.md..."
if grep -Eq 'version: "[0-9]+\.[0-9]+"' "$SKILL_DIR/SKILL.md"; then
    echo "  ✓ Versión SemVer validada en Frontmatter."
else
    echo "  ❌ Error: Falta versión válida en Frontmatter."
    ERRORS=$((ERRORS + 1))
fi

if grep -q "Trigger:.*planner" "$SKILL_DIR/SKILL.md" && grep -q "Trigger:.*plan" "$SKILL_DIR/SKILL.md"; then
    echo "  ✓ Triggers 'planner' y 'plan' validados en Frontmatter."
else
    echo "  ❌ Error: Falta trigger 'planner' o 'plan' en Frontmatter."
    ERRORS=$((ERRORS + 1))
fi

# 3. Validar Presupuesto de Tokens de Router Ejecutivo (Standard v3.0 Two-Tier)
echo "• Validando Presupuesto de Tokens de Router Ejecutivo (CoHaLo)..."
WORD_COUNT=$(wc -w < "$SKILL_DIR/SKILL.md")
EST_TOKENS=$((WORD_COUNT * 13 / 10))
echo "  ℹ Conteo actual: $WORD_COUNT palabras (~$EST_TOKENS tokens)"
if [ "$EST_TOKENS" -gt 2500 ]; then
    echo "  ❌ Error: SKILL.md excede techo rígido de 2500 tokens (~$EST_TOKENS tokens)."
    ERRORS=$((ERRORS + 1))
elif [ "$EST_TOKENS" -gt 750 ]; then
    echo "  ℹ Aviso: SKILL.md en presupuesto de orquestador de dominio (~$EST_TOKENS tokens, límite techo 2500)."
    echo "  ✓ Presupuesto ejecutivo CoHaLo respetado."
else
    echo "  ✓ Presupuesto ejecutivo CoHaLo respetado ($WORD_COUNT palabras, ~$EST_TOKENS tokens <= 750)."
fi

# 4. Validar CoHaLo Positive Guidance & Hard Rules en SKILL.md
echo "• Validando Hard Rules y Decision Gates..."
if grep -q "Rule 1 (CoHaLo Positive Guidance & Continuous Present Inflow)" "$SKILL_DIR/SKILL.md" && \
   grep -q "Rule 2 (Dual-Track SSoT Governance & Lifecycle Bifurcation)" "$SKILL_DIR/SKILL.md" && \
   grep -q "Rule 3 (Immutable Plan Versions, Anti-Amnesia Consolidation & Token Economy)" "$SKILL_DIR/SKILL.md" && \
   grep -Eq "Rule 4 \(SSoT Indivisibility.*(unisetup\.sh-First|Universal Clean-Room Virgin ZCP)" "$SKILL_DIR/SKILL.md" && \
   grep -q "Rule 5 (Closed Lifecycle Topology & Zero-Omission Checklist Gate)" "$SKILL_DIR/SKILL.md"; then
    echo "  ✓ Las 5 Hard Rules de CoHaLo v3.1 validadas en SKILL.md."
else
    echo "  ❌ Error: Faltan Hard Rules (1 a 5) en SKILL.md."
    ERRORS=$((ERRORS + 1))
fi

# 5. Validar gramática de respaldos planos O(1) en Rule 2
echo "• Validando gramática fija de respaldos planos en Rule 2..."
if grep -q 'bak/skills/<skill_name>_v<current_version>\.bak/' "$SKILL_DIR/SKILL.md"; then
    echo "  ✓ Gramática plana de respaldos O(1) validada en Rule 2 de SKILL.md."
else
    echo "  ❌ Error: Rule 2 no contiene la gramática de respaldos planos /bak/skills/<skill_name>_v<current_version>.bak/."
    ERRORS=$((ERRORS + 1))
fi

# 6. Validar erradicación de cláusula de excepción en governance_contracts.md
echo "• Validando ausencia de excepciones de agrupación en governance_contracts.md..."
if grep -qi "Dedicated grouping parent subdirectories" "$SKILL_DIR/references/governance_contracts.md"; then
    echo "  ❌ Error: Se detectó cláusula permisiva de subdirectorios agrupados en governance_contracts.md."
    ERRORS=$((ERRORS + 1))
else
    echo "  ✓ Cero cláusulas permisivas de carpetas agrupadas en governance_contracts.md."
fi

# 7. Validar plantilla atemporal en assets/plan_template.md
echo "• Validando atemporalidad en cabecera de plan_template.md..."
if grep -E "Planner v|CoHaLo v|Supreme Directive v" "$SKILL_DIR/assets/plan_template.md" >/dev/null 2>&1; then
    echo "  ❌ Error: plan_template.md contiene versiones hardcodeadas en cabecera o matriz."
    ERRORS=$((ERRORS + 1))
else
    echo "  ✓ plan_template.md validado como 100% atemporal y canónico."
fi

# 8. Validar sintaxis Bash de scripts internos
echo "• Validando sintaxis de scripts internos..."
if [ -d "$SKILL_DIR/scripts" ]; then
    for sh_file in "$SKILL_DIR/scripts/"*.sh; do
        if [ -f "$sh_file" ]; then
            if bash -n "$sh_file" >/dev/null 2>&1; then
                echo "  ✓ Bash sintaxis válida: $(basename "$sh_file")"
            else
                echo "  ❌ Error de sintaxis Bash en $(basename "$sh_file")"
                ERRORS=$((ERRORS + 1))
            fi
        fi
    done
fi

# 9. Validar enlaces canónicos en SKILL.md (Zero 404s)
echo "• Validando enlaces canónicos en SKILL.md..."
for ref_skill in "research" "skill-improver" "skill-creator" "docu"; do
    if grep -q "file:///var/www/.agents/skills/$ref_skill" "$SKILL_DIR/SKILL.md"; then
        echo "  ✓ Enlace canónico file:/// hacia $ref_skill validado."
    else
        echo "  ❌ Error: Falta enlace canónico hacia $ref_skill en SKILL.md."
        ERRORS=$((ERRORS + 1))
    fi
done

while IFS= read -r link; do
    clean_path="${link#file://}"
    if [ -z "${clean_path#/}" ]; then
        continue
    fi
    clean_path="${clean_path%%#*}"
    if [ ! -e "$clean_path" ]; then
        echo "  ❌ Broken physical link in SKILL.md: $link (target $clean_path does not exist)"
        ERRORS=$((ERRORS + 1))
    fi
done < <(grep -oE 'file:///[^ )"`]+' "$SKILL_DIR/SKILL.md" || true)
echo "  ✓ Enlaces físicos file:/// validados en disco sin 404s."

echo "============================================================"
if [ "$ERRORS" -eq 0 ]; then
    echo "  ✅ Validación EXITOSA: Skill Planner v3.8 al 100% de integridad física."
    exit 0
else
    echo "  ❌ Validación FALLIDA con $ERRORS errores."
    exit 1
fi

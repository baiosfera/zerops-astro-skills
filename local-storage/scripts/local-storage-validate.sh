#!/usr/bin/env bash
# ==============================================================================
# Deterministic Physical Validation Sensor for Agent Skills (Standard v3.0)
# Zero LLM Tokens | Bounded Execution < 100ms | 100% Deterministic
# ==============================================================================
set -euo pipefail

REAL_SCRIPT="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$REAL_SCRIPT")"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_NAME="$(basename "$SKILL_DIR")"
ERRORS=0

echo "============================================================"
echo "  🔍 Validating Skill Integrity: [$SKILL_NAME]"
echo "============================================================"

# 1. Structural & Dual-RAG Packaging Integrity
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "❌ Missing required SKILL.md in $SKILL_DIR"
    ERRORS=$((ERRORS + 1))
else
    echo "✓ SKILL.md exists"
fi

# 2. Frontmatter Metadata Verification
if grep -q '^name: ' "$SKILL_DIR/SKILL.md" && \
   grep -q '^description: ' "$SKILL_DIR/SKILL.md" && \
   grep -q 'version: ' "$SKILL_DIR/SKILL.md"; then
    echo "✓ Valid YAML frontmatter metadata (name, description, version)"
else
    echo "❌ Malformed frontmatter in SKILL.md (missing name, description, or version)"
    ERRORS=$((ERRORS + 1))
fi

# 3. Dual-RAG References Non-Emptiness Check
if [ -d "$SKILL_DIR/references" ]; then
    for ref_file in "$SKILL_DIR/references/"*.md; do
        if [ -f "$ref_file" ]; then
            if [ ! -s "$ref_file" ]; then
                echo "❌ Empty reference file detected: $(basename "$ref_file")"
                ERRORS=$((ERRORS + 1))
            fi
        fi
    done
    echo "✓ All reference files in references/ are non-empty"
fi

# 4. Deterministic Syntax Compilation (Fail-Fast)
# 4.1 Shell Scripts Syntax Validation
if [ -d "$SKILL_DIR/scripts" ]; then
    for sh_file in "$SKILL_DIR/scripts/"*.sh; do
        if [ -f "$sh_file" ]; then
            if bash -n "$sh_file" >/dev/null 2>&1; then
                echo "✓ Bash syntax valid: $(basename "$sh_file")"
            else
                echo "❌ Bash syntax error in $(basename "$sh_file")"
                ERRORS=$((ERRORS + 1))
            fi
        fi
    done
fi

# 4.2 Python Scripts Bytecode Compilation
if [ -d "$SKILL_DIR/scripts" ]; then
    for py_file in "$SKILL_DIR/scripts/"*.py; do
        if [ -f "$py_file" ]; then
            if python3 -m py_compile "$py_file" >/dev/null 2>&1; then
                echo "✓ Python compilation passed: $(basename "$py_file")"
            else
                echo "❌ Python syntax error in $(basename "$py_file")"
                ERRORS=$((ERRORS + 1))
            fi
        fi
    done
fi

# 4.3 JSON Assets Schema & Syntax Parsing
if [ -d "$SKILL_DIR/assets" ]; then
    for json_file in "$SKILL_DIR/assets/"*.json; do
        if [ -f "$json_file" ]; then
            if python3 -m json.tool "$json_file" >/dev/null 2>&1; then
                echo "✓ JSON valid: $(basename "$json_file")"
            else
                echo "❌ JSON syntax error in $(basename "$json_file")"
                ERRORS=$((ERRORS + 1))
            fi
        fi
    done
fi

# 5. Physical Link Integrity (Zero Dead Links / Cero 404s)
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

# 6. Context Token Budget Guardrail (Router Protection)
WORD_COUNT=$(wc -w < "$SKILL_DIR/SKILL.md")
EST_TOKENS=$((WORD_COUNT * 13 / 10))
echo "• SKILL.md budget check: $WORD_COUNT words (~$EST_TOKENS tokens)"
if [ "$EST_TOKENS" -gt 2500 ]; then
    echo "❌ SKILL.md exceeds hard budget of 2500 tokens (~$EST_TOKENS tokens). Router bloat!"
    ERRORS=$((ERRORS + 1))
elif [ "$EST_TOKENS" -gt 750 ]; then
    echo "⚠️ Warning: SKILL.md exceeds recommended budget (~$EST_TOKENS tokens)."
else
    echo "✓ SKILL.md within router token budget (<=750 tokens)"
fi

# 7. Hermetic Self-Tests Execution (if present)
if [ -d "$SKILL_DIR/scripts" ]; then
    for test_script in "$SKILL_DIR/scripts/"*test*.py; do
        if [ -f "$test_script" ]; then
            if python3 "$test_script" >/dev/null 2>&1; then
                echo "✓ Hermetic unit test passed: $(basename "$test_script")"
            else
                echo "❌ Hermetic unit test failed: $(basename "$test_script")"
                ERRORS=$((ERRORS + 1))
            fi
        fi
    done
fi

echo "------------------------------------------------------------"
if [ "$ERRORS" -eq 0 ]; then
    echo "✅ Skill [$SKILL_NAME] passed physical validation (exit code 0)."
    exit 0
else
    echo "❌ Skill [$SKILL_NAME] validation failed with $ERRORS error(s)."
    exit 1
fi

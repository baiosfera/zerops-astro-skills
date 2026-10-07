#!/usr/bin/env bash
# ==============================================================================
# Deterministic Physical Validation Sensor for object-storage Skill
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
    echo "❌ Malformed frontmatter in SKILL.md"
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
else
    echo "❌ Missing references/ directory in $SKILL_DIR"
    ERRORS=$((ERRORS + 1))
fi

# 4. Mandatory S3 Invariant Keywords Check
if grep -q "AWS_USE_PATH_STYLE_ENDPOINT" "$SKILL_DIR/SKILL.md" && \
   grep -q "storage_apiUrl" "$SKILL_DIR/SKILL.md"; then
    echo "✓ Critical S3 path-style and storage_apiUrl invariants present"
else
    echo "❌ Missing critical S3 invariants in SKILL.md"
    ERRORS=$((ERRORS + 1))
fi

echo "------------------------------------------------------------"
if [ "$ERRORS" -eq 0 ]; then
    echo "✅ Skill [$SKILL_NAME] passed physical validation (exit code 0)."
    exit 0
else
    echo "❌ Skill [$SKILL_NAME] failed physical validation with $ERRORS error(s)."
    exit 1
fi

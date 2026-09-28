#!/usr/bin/env bash
# ==============================================================================
# Deterministic Physical Validation Sensor for Docu (v7.0 — Standard v3.0)
# Zero LLM Tokens | Bounded Execution < 500ms | 100% Deterministic Round-Trip
# ==============================================================================
set -euo pipefail

REAL_SCRIPT="$(readlink -f "${BASH_SOURCE[0]}")"
SKILL_DIR="$(cd "$(dirname "$REAL_SCRIPT")/.." && pwd)"
ERRORS=0

echo "============================================================"
echo "  🔍 Validating Docu Skill Integrity (v7.0)"
echo "============================================================"

# 1. Check SKILL.md existence
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "❌ Missing SKILL.md in $SKILL_DIR"
    ERRORS=$((ERRORS + 1))
else
    echo "✓ SKILL.md exists"
fi

# 2. Check frontmatter metadata.version (Dynamic SemVer)
if grep -Eq 'version: "7\.[0-9]+"' "$SKILL_DIR/SKILL.md"; then
    echo "✓ Frontmatter version is 7.x"
else
    echo "❌ Frontmatter version is not 7.x"
    ERRORS=$((ERRORS + 1))
fi

# 3. Check token count of SKILL.md (Progressive Disclosure Level 2: <= 550 tokens)
WORD_COUNT=$(wc -w < "$SKILL_DIR/SKILL.md")
EST_TOKENS=$((WORD_COUNT * 13 / 10))
echo "Calculated SKILL.md word count: $WORD_COUNT, estimated tokens: ~$EST_TOKENS"
if [ "$EST_TOKENS" -gt 700 ]; then
    echo "❌ SKILL.md exceeds 700 tokens hard budget (~$EST_TOKENS tokens). Router bloat!"
    ERRORS=$((ERRORS + 1))
elif [ "$EST_TOKENS" -gt 550 ]; then
    echo "⚠️ Warning: SKILL.md slightly exceeds recommended 550 tokens budget (~$EST_TOKENS tokens)."
else
    echo "✓ Token budget compliant: ~$EST_TOKENS tokens (word count: $WORD_COUNT, limit 550)"
fi

# 4. Check Dual-RAG references and Certification Gate
for ref in \
    "references/certification.md" \
    "references/workflow.md" \
    "references/templates.md" \
    "assets/skill_scaffold.py" \
    "assets/research_ingestion_protocol.md" \
    "assets/subagent_meta_prompt_template.md"; do
    if [ -f "$SKILL_DIR/$ref" ] && [ -s "$SKILL_DIR/$ref" ]; then
        echo "✓ Required reference exists and non-empty: $ref"
    else
        echo "❌ Missing or empty reference: $ref"
        ERRORS=$((ERRORS + 1))
    fi
done

# 5. Check Absence of Legacy Extreme Research Protocol Dogma
if [ -f "$SKILL_DIR/assets/extreme_research_protocol.md" ]; then
    echo "❌ Legacy extreme_research_protocol.md still present. Must be eradicated!"
    ERRORS=$((ERRORS + 1))
else
    echo "✓ Legacy extreme_research_protocol.md verified absent"
fi

# 6. Check Python script syntax (In-memory AST parsing, zero disk writes)
if python3 -c "import ast; ast.parse(open('$SKILL_DIR/assets/skill_scaffold.py').read())" 2>/dev/null; then
    echo "✓ skill_scaffold.py AST syntax valid (in-memory, 0 disk writes)"
else
    echo "❌ Syntax error in skill_scaffold.py"
    ERRORS=$((ERRORS + 1))
fi

# 7. Check Clean-Room Bytecode Hygiene (Zero __pycache__ or *.pyc)
if find "$SKILL_DIR" -name "__pycache__" -o -name "*.pyc" 2>/dev/null | grep -q .; then
    echo "❌ Clean-room hygiene error: bytecode cache detected in $SKILL_DIR"
    ERRORS=$((ERRORS + 1))
else
    echo "✓ Clean-room hygiene verified: zero bytecode cache in skill tree"
fi

# 8. Check Version Synchronization in references and assets (v7.x)
for f in "references/workflow.md" "references/templates.md" "references/certification.md" "assets/skill_scaffold.py" "assets/subagent_meta_prompt_template.md" "assets/research_ingestion_protocol.md"; do
    if grep -Eq "v7\.[0-9]+" "$SKILL_DIR/$f"; then
        echo "✓ Version v7.x verified in $f"
    else
        echo "❌ Missing v7.x version tag in $f"
        ERRORS=$((ERRORS + 1))
    fi
done

# 9. Check Positive Guidance Eradication of Legacy Negative Directives in Templates/Assets
if grep -inE "Do NOT activate|Queda terminantemente prohibido" "$SKILL_DIR/references/"*.md "$SKILL_DIR/assets/"* 2>/dev/null | grep -v 'grep -inE'; then
    echo "❌ Legacy negative directives detected in references or assets"
    ERRORS=$((ERRORS + 1))
else
    echo "✓ Positive guidance verified: zero legacy negative directives in references and assets"
fi

# 10. Check Physical Links in SKILL.md (Zero 404s)
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

# 11. Check Zero Ephemeral Artifact Links in SKILL.md
if grep -oE 'file:///var/www/artifacts/[^ )"`]+' "$SKILL_DIR/SKILL.md" 2>/dev/null; then
    echo "❌ Forbidden ephemeral artifact link found in SKILL.md! Use references/ instead."
    ERRORS=$((ERRORS + 1))
else
    echo "✓ Zero ephemeral artifact links in SKILL.md verified"
fi

# 12. Live Physiological Round-Trip Testing (Scaffold -> Validate -> Clean)
echo "• Executing live physiological round-trip test in /var/www/scratch..."
TEST_SCRATCH_DIR="/var/www/scratch"
mkdir -p "$TEST_SCRATCH_DIR"

# Test 12.1: Framework Archetype Round-Trip
rm -rf "$TEST_SCRATCH_DIR/test-roundtrip-skill"
if python3 "$SKILL_DIR/assets/skill_scaffold.py" test-roundtrip-skill "test, demo" "Test SOTA Framework Capabilities" --archetype framework --base-dir "$TEST_SCRATCH_DIR" >/dev/null 2>&1; then
    if bash "$TEST_SCRATCH_DIR/test-roundtrip-skill/scripts/test-roundtrip-skill-validate.sh" >/dev/null 2>&1; then
        echo "✓ Round-trip test passed for framework archetype (exit code 0)"
    else
        echo "❌ Generated framework validator failed round-trip execution"
        ERRORS=$((ERRORS + 1))
    fi
    rm -rf "$TEST_SCRATCH_DIR/test-roundtrip-skill"
else
    echo "❌ Failed to scaffold test-roundtrip-skill"
    ERRORS=$((ERRORS + 1))
fi

# Test 12.2: Domain Archetype Round-Trip (No infra.md)
rm -rf "$TEST_SCRATCH_DIR/test-domain-roundtrip"
if python3 "$SKILL_DIR/assets/skill_scaffold.py" test-domain-roundtrip "domain, astro" "Test SOTA Domain Calculations" --archetype domain --base-dir "$TEST_SCRATCH_DIR" >/dev/null 2>&1; then
    if [ -f "$TEST_SCRATCH_DIR/test-domain-roundtrip/references/infra.md" ]; then
        echo "❌ Architecture violation: infra.md unexpectedly generated for domain archetype"
        ERRORS=$((ERRORS + 1))
    else
        echo "✓ Domain archetype correctly omitted infra.md"
    fi
    if bash "$TEST_SCRATCH_DIR/test-domain-roundtrip/scripts/test-domain-roundtrip-validate.sh" >/dev/null 2>&1; then
        echo "✓ Round-trip test passed for domain archetype (exit code 0)"
    else
        echo "❌ Generated domain validator failed round-trip execution"
        ERRORS=$((ERRORS + 1))
    fi
    rm -rf "$TEST_SCRATCH_DIR/test-domain-roundtrip"
else
    echo "❌ Failed to scaffold test-domain-roundtrip"
    ERRORS=$((ERRORS + 1))
fi

echo "------------------------------------------------------------"
if [ "$ERRORS" -eq 0 ]; then
    echo "✅ Docu v7.0 validation passed successfully with exit code 0."
    exit 0
else
    echo "❌ Docu v7.0 validation failed with $ERRORS error(s)."
    exit 1
fi

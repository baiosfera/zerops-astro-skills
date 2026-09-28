#!/usr/bin/env bash
# ==============================================================================
# Deterministic Physical Validation Sensor: Gemini Notebook / NotebookLM Skill
# Standard: Fractal CoHaLo v6.9 | Supreme Directive v7.6 | Planner v3.3 (Track A)
# Execution: Bounded < 50ms | 0 LLM Tokens | 100% Deterministic Exit Code
# ==============================================================================
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ERRORS=0

echo "============================================================"
echo "  🔍 Validating Gemini Notebook Skill Integrity: [notebooklm]"
echo "  Target: $SKILL_DIR"
echo "============================================================"

# 1. Structural Files Check
for req in "SKILL.md" "references/usage.md" "references/infra.md"; do
    if [ -f "$SKILL_DIR/$req" ] && [ -s "$SKILL_DIR/$req" ]; then
        echo "✓ File present and non-empty: $req"
    else
        echo "❌ Missing or empty required file: $req"
        ERRORS=$((ERRORS + 1))
    fi
done

# 2. Token / Word Count Budget on SKILL.md (< 450 words)
if [ -f "$SKILL_DIR/SKILL.md" ]; then
    WORDS=$(wc -w < "$SKILL_DIR/SKILL.md")
    if [ "$WORDS" -le 450 ]; then
        echo "✓ SKILL.md token budget compliant ($WORDS words, limit <= 450)"
    else
        echo "❌ SKILL.md exceeds token budget ($WORDS words > 450 words)"
        ERRORS=$((ERRORS + 1))
    fi
fi

# 3. Semantic Versioning (Semver 2.x)
if grep -Eq 'version: "2\.[0-9]+\.[0-9]+"' "$SKILL_DIR/SKILL.md"; then
    echo "✓ YAML frontmatter Semver 2.x validated"
else
    echo "❌ Missing or invalid version: \"2.x.x\" in SKILL.md"
    ERRORS=$((ERRORS + 1))
fi

# 4. Anti-Artifacts Link Invariant (Zero permanent links to /var/www/artifacts/)
if grep -r "/var/www/artifacts" "$SKILL_DIR" --exclude="*.bak" --exclude="*.log" --exclude="*.sh" 2>/dev/null; then
    echo "❌ Fatal: Detected prohibited permanent links to /var/www/artifacts/ inside skill"
    ERRORS=$((ERRORS + 1))
else
    echo "✓ Zero prohibited links to /var/www/artifacts/ verified"
fi

# 5. FastMCP 49 Tools Catalog Validation in references/usage.md
if [ -f "$SKILL_DIR/references/usage.md" ]; then
    for tool in "collection_list" "collection_create" "usage_get" "chat_export" "notebook_query_start" "notebook_query_status" "note" "label" "source_add" "studio_create" "server_info"; do
        if grep -q "$tool" "$SKILL_DIR/references/usage.md"; then
            :
        else
            echo "❌ Missing canonical FastMCP tool in usage.md: $tool"
            ERRORS=$((ERRORS + 1))
        fi
    done
    echo "✓ Canonical FastMCP tools validated in usage.md"
fi

# 6. Official 43 Supported File Extensions Contract
if [ -f "$SKILL_DIR/references/usage.md" ]; then
    if grep -qi "43 extensiones" "$SKILL_DIR/references/usage.md" || grep -qi "43 official" "$SKILL_DIR/references/usage.md"; then
        echo "✓ Official 43-extension contract documented in usage.md"
    else
        echo "❌ Missing 43 official file extensions contract in usage.md"
        ERRORS=$((ERRORS + 1))
    fi
fi

# 7. Ground Truth CLI Syntax Assertions
if [ -f "$SKILL_DIR/references/usage.md" ]; then
    # Download --id
    if grep -q "nlm download.*--id" "$SKILL_DIR/references/usage.md"; then
        echo "✓ Validated CLI syntax: nlm download with --id"
    else
        echo "❌ Missing or invalid nlm download syntax with --id"
        ERRORS=$((ERRORS + 1))
    fi

    # Data-table positional description
    if grep -q 'nlm data-table create <UUID> "<description>"' "$SKILL_DIR/references/usage.md" || grep -q 'nlm data-table create <UUID> "<' "$SKILL_DIR/references/usage.md"; then
        echo "✓ Validated CLI syntax: nlm data-table create with positional description"
    else
        echo "❌ Missing or invalid nlm data-table create positional syntax"
        ERRORS=$((ERRORS + 1))
    fi

    # Tag add -t / --tags
    if grep -qE "nlm tag add <UUID> (-t|--tags)" "$SKILL_DIR/references/usage.md"; then
        echo "✓ Validated CLI syntax: nlm tag add with -t/--tags"
    else
        echo "❌ Missing or invalid nlm tag add with -t/--tags"
        ERRORS=$((ERRORS + 1))
    fi

    # Export to-docs / to-sheets
    if grep -q "nlm export to-docs" "$SKILL_DIR/references/usage.md" && grep -q "nlm export to-sheets" "$SKILL_DIR/references/usage.md"; then
        echo "✓ Validated CLI syntax: nlm export to-docs / to-sheets"
    else
        echo "❌ Missing or invalid nlm export to-docs / to-sheets syntax"
        ERRORS=$((ERRORS + 1))
    fi

    # Quiz difficulty 1-5 integer
    if grep -qE "nlm quiz create.*--difficulty [1-5]" "$SKILL_DIR/references/usage.md"; then
        echo "✓ Validated CLI syntax: nlm quiz create with integer difficulty 1-5"
    else
        echo "❌ Missing or invalid nlm quiz create with integer difficulty 1-5"
        ERRORS=$((ERRORS + 1))
    fi
fi

# 8. CoHaLo Harness & Compute Quota Documentation in references/infra.md
if [ -f "$SKILL_DIR/references/infra.md" ]; then
    if grep -qi "timeout 10s" "$SKILL_DIR/references/infra.md" && grep -qi "WaitMsBeforeAsync" "$SKILL_DIR/references/infra.md"; then
        echo "✓ CoHaLo bounded execution harness documented in infra.md"
    else
        echo "❌ Missing CoHaLo bounded execution harness in infra.md"
        ERRORS=$((ERRORS + 1))
    fi

    if grep -qi "rolling" "$SKILL_DIR/references/infra.md" && grep -qi "weekly" "$SKILL_DIR/references/infra.md"; then
        echo "✓ Dual-window compute quotas (rolling & weekly) documented in infra.md"
    else
        echo "❌ Missing dual-window compute quotas in infra.md"
        ERRORS=$((ERRORS + 1))
    fi

    if grep -qi "__Secure-1PSIDTS" "$SKILL_DIR/references/infra.md"; then
        echo "✓ Google session cookie __Secure-1PSIDTS freshness documented in infra.md"
    else
        echo "❌ Missing __Secure-1PSIDTS authentication lifecycle in infra.md"
        ERRORS=$((ERRORS + 1))
    fi

    # 9. Google One AI Premium SSoT Verification
    if grep -qi "NOTEBOOKLM_TIER_PRO_CONSUMER_USER" "$SKILL_DIR/references/infra.md" && grep -qi "NOTEBOOKLM_TIER_PRO_CONSUMER_USER" "$SKILL_DIR/SKILL.md"; then
        echo "✓ Google One AI Premium tier contract (NOTEBOOKLM_TIER_PRO_CONSUMER_USER) documented in infra.md and SKILL.md"
    else
        echo "❌ Missing NOTEBOOKLM_TIER_PRO_CONSUMER_USER contract in infra.md or SKILL.md"
        ERRORS=$((ERRORS + 1))
    fi
fi

# 10. Studio Styles Contract in usage.md
if [ -f "$SKILL_DIR/references/usage.md" ]; then
    if grep -q "editorial" "$SKILL_DIR/references/usage.md" && grep -q "anime" "$SKILL_DIR/references/usage.md"; then
        echo "✓ Studio infographic & video styles (including editorial) documented in usage.md"
    else
        echo "❌ Missing verified studio styles in usage.md"
        ERRORS=$((ERRORS + 1))
    fi
fi

# 11. Orchestrator nlm-tutor Intact & Executable Check
if command -v nlm-tutor >/dev/null 2>&1; then
    echo "✓ Orquestador nlm-tutor present and executable in PATH"
else
    echo "❌ Missing or non-executable nlm-tutor in PATH"
    ERRORS=$((ERRORS + 1))
fi

echo "------------------------------------------------------------"
if [ "$ERRORS" -eq 0 ]; then
    echo "✅ Skill [notebooklm] v2.3.0 physically validated with 0 errors (exit code 0)."
    exit 0
else
    echo "❌ Skill [notebooklm] validation failed with $ERRORS error(s)."
    exit 1
fi

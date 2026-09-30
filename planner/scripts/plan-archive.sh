#!/usr/bin/env bash
# ==============================================================================
# plan-archive: Deterministic Plan Archival & Hygiene Utility
# Version: 1.0 (Track A/B Sovereign Lifecycle Governance)
# Zero LLM Tokens | Bounded Execution < 100ms | 100% Deterministic
#
# Usage:
#   plan-archive                     # Scans /var/www/artifacts, moves older versions to archive/
#   plan-archive <plan-path>         # Ensures <plan-path> is active, archives older versions of same stem
#   plan-archive <plan-path> --executed  # Marks plan as executed and moves to archive/
#   plan-archive --clean             # Removes stale superseded versions across all plans
# ==============================================================================
set -euo pipefail

ARTIFACTS_DIR="/var/www/artifacts"
ARCHIVE_DIR="${ARTIFACTS_DIR}/archive"

mkdir -p "$ARCHIVE_DIR"

MODE="auto"
TARGET_PLAN=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --executed)
            MODE="executed"
            shift
            ;;
        --clean)
            MODE="clean"
            shift
            ;;
        --help|-h)
            echo "Usage: plan-archive [plan_path] [--executed] [--clean]"
            echo "  --executed: Mark target plan as executed in archive/"
            echo "  --clean:    Move all superseded versions to archive/, leaving only latest active"
            exit 0
            ;;
        *)
            if [ -z "$TARGET_PLAN" ]; then
                TARGET_PLAN="$1"
            fi
            shift
            ;;
    esac
done

# If an explicit plan was provided
if [ -n "$TARGET_PLAN" ] && [ -f "$TARGET_PLAN" ]; then
    FNAME="$(basename "$TARGET_PLAN")"
    STEM=$(echo "$FNAME" | sed -E 's/_v[0-9]+.*$//')
    CURRENT_VER=$(echo "$FNAME" | grep -oE '_v[0-9]+([_\.][0-9]+)*' || echo "")

    if [ "$MODE" == "executed" ]; then
        DEST="${ARCHIVE_DIR}/${FNAME}"
        echo "📦 Archiving executed plan: $FNAME -> archive/$FNAME"
        mv -f "$TARGET_PLAN" "$DEST"
        exit 0
    fi

    # Normal mode: move older versions of this stem to archive/
    for f in "$ARTIFACTS_DIR"/${STEM}_v*.md; do
        [ -e "$f" ] || continue
        BNAME="$(basename "$f")"
        if [ "$BNAME" != "$FNAME" ]; then
            echo "📦 Archiving superseded version: $BNAME -> archive/$BNAME"
            mv -f "$f" "${ARCHIVE_DIR}/${BNAME}"
        fi
    done
    echo "✓ Active plan preserved in root: $FNAME"
    exit 0
fi

# Auto / Clean mode: scan all plan files in ARTIFACTS_DIR root
echo "============================================================"
echo "  🧹 Running Deterministic Plan Archival (plan-archive)"
echo "============================================================"

# Collect all stems
declare -A HIGHEST_VER
declare -A HIGHEST_FILE

for f in "$ARTIFACTS_DIR"/*_v[0-9]*.md; do
    [ -e "$f" ] || continue
    BNAME="$(basename "$f")"
    STEM=$(echo "$BNAME" | sed -E 's/_v[0-9]+.*$//')
    VER=$(echo "$BNAME" | grep -oE '_v[0-9]+' | sed 's/_v//')
    
    if [ -z "${HIGHEST_VER[$STEM]:-}" ] || [ "$VER" -gt "${HIGHEST_VER[$STEM]}" ]; then
        HIGHEST_VER[$STEM]="$VER"
        HIGHEST_FILE[$STEM]="$f"
    fi
done

ARCHIVED_COUNT=0
for f in "$ARTIFACTS_DIR"/*_v[0-9]*.md; do
    [ -e "$f" ] || continue
    BNAME="$(basename "$f")"
    STEM=$(echo "$BNAME" | sed -E 's/_v[0-9]+.*$//')
    
    if [ "$f" != "${HIGHEST_FILE[$STEM]}" ]; then
        echo "  → Archiving superseded: $BNAME -> archive/$BNAME"
        mv -f "$f" "${ARCHIVE_DIR}/${BNAME}"
        ARCHIVED_COUNT=$((ARCHIVED_COUNT + 1))
    else
        echo "  ✓ Keeping active: $BNAME"
    fi
done

echo "------------------------------------------------------------"
echo "✅ Plan hygiene complete: $ARCHIVED_COUNT superseded plan(s) moved to archive/."
exit 0

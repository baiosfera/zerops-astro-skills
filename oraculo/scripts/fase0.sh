#!/usr/bin/env bash
# ==============================================================================
# Oráculo Fast-Path Launcher: Fase 0 & Virtual Data Lakehouse
# Zero Tokens Exploration | Single-Command Invocator | Deterministic
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENGINE_SCRIPT="$SCRIPT_DIR/omni_engine.py"

if [ $# -lt 1 ]; then
    echo "Uso: bash $0 <ruta_archivo_consultante>"
    echo "Ejemplo: bash $0 /var/www/baiosfera/ASTROLOGÍA/DIAG/CATALINA_GLAMUR_AGY/Catalina.txt"
    exit 1
fi

CLIENT_FILE="$1"

if [ ! -f "$CLIENT_FILE" ]; then
    echo "❌ Error: Archivo de consultante no encontrado en: $CLIENT_FILE"
    exit 1
fi

echo "🚀 Iniciando Fase 0 (Extracción Federada + Data Lakehouse SSoT)..."
python3 "$ENGINE_SCRIPT" --file "$CLIENT_FILE"

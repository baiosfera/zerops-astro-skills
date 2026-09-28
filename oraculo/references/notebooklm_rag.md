# NotebookLM & Gemini RAG Operational Protocol (SSoT V4.0)

Esta guía define el protocolo de interacción asíncrona, ciclo de vida de artefactos y mapeo de fuentes teóricas para la interpretación astrológica mediante NotebookLM CLI (`nlm-mcp` / MCP `notebooklm`).

---

## 1. Ciclo de Vida de Artefactos (Generación, Descarga Local y Sanitización)
Para mantener limpios y desintoxicados los 10 cuadernos temáticos globales de la nube, toda consulta teórica sigue estrictamente este ciclo:

```
[1. Cuaderno Temático] ➔ nlm report create / studio_create (Genera Artefacto en la Nube)
                                     │
                                     ▼
[2. Polling Asíncrono] ➔ nlm studio status (Espera estado completed sin bloquear)
                                     │
                                     ▼
[3. Extracción Local]  ➔ Descarga en /DIAG/<ID>/notebooks/consult_<ID>_<fase>.md
                                     │
                                     ▼
[4. Purga en la Nube]  ➔ nlm studio delete <UUID> <ART_ID> (Elimina artefacto del cuaderno temático)
                                     │
                                     ▼
[5. Fase 11 - Entrega] ➔ Sube todos los .md de /DIAG/<ID>/notebooks/ al Cuaderno del Cliente
```

### Script de Ejecución por Fase:
```bash
# 1. Crear solicitud de reporte/briefing
ART_ID=$(nlm report create <UUID> -f "FAQ" --prompt "PROMPT_ANALITICO" -y --json | jq -r '.artifact_id')

# 2. Esperar completitud de forma no bloqueante
STATUS="unknown"
while [ "$STATUS" != "completed" ] && [ "$STATUS" != "error" ]; do
    sleep 3
    STATUS=$(nlm studio status <UUID> --json | jq -r ".[] | select(.artifact_id==\"$ART_ID\") | .status")
done

# 3. Descargar y guardar en la carpeta local del cliente
mkdir -p "/var/www/baiosfera/ASTROLOGÍA/DIAG/<ID>/notebooks"
nlm download report <UUID> --id "$ART_ID" -o "/var/www/baiosfera/ASTROLOGÍA/DIAG/<ID>/notebooks/consult_<ID>_<fase>.md"

# 4. Sanitización inmediata del cuaderno temático de origen
nlm studio delete <UUID> "$ART_ID" -y
```

---

## 2. Diccionario de Cuadernos Teóricos (UUIDs Canónicos)
Cuando se realicen consultas temáticas en Fases 1 a 9, enrutar a los siguientes UUIDs:

| Etiqueta Temática | Disciplina / Enfoque | Cuaderno UUID |
|---|---|---|
| `[NUMEROLOGIA]`, `[TANTRICA]`, `[PINACULOS]` | Numerología Pitagórica, Tántrica y Pináculos | `abfb2941-fe0d-462f-8937-2317b6050589` |
| `[GENERAL]`, `[KARMICA]`, `[DESCRIPTIVA]` | Astrología Kármica y General | `ec1e2b8b-c289-4a9d-8264-5990200a2594` |
| `[PSICOLOGICA]`, `[PERSONALIDAD]` | Astrología Psicológica y Arquetípica | `6f0edade-bc2f-4a46-9ec3-63dfa0b2bb6c` |
| `[NATAL]`, `[INTERPRETATIVA]` | Astrología Natal Tradicional y Moderna | `fef0b3a9-7980-408e-95fa-9fd1190fed29` |
| `[HINDU]` | Astrología Védica (Jyotish) y Nakshatras | `395df439-bfcf-4f41-8854-df9a773a8376` |
| `[CABALA]` | Mística Hebrea, Gematría y Árbol de la Vida | `52edc22f-298e-4cbe-8cf2-7765fa2cff58` |
| `[CHINA]` | Metafísica China y BaZi (4 Pilares) | `e8ca0237-e8d3-4a84-8124-a671c382659a` |
| `[VOCACIONAL]`, `[EMPRESARIAL]`, `[FINANCIERA]` | Astrobranding, Negocios y Timing Financiero | `f4955a1a-694d-4f27-b164-95cbd40bbdd3` |
| `[DISEÑO_UX]` | UX/UI, Psicología Gestalt y Visual | `a259ace3-d32c-4d36-81b2-3254798acba9` |
| `[BRANDING]` | Posicionamiento, Arquetipos y Thick Data | `a5549193-cd59-47d9-a0a2-f0580bef3221` |

---

## 3. Reglas Anti-Contaminación de Consultas
- Los prompts hacia NotebookLM deben ser **analíticos, fríos y conceptuales**.
- Solicitar estrictamente la teoría sin incorporar nombres propios o casos de estudio de los cursos de origen.
- Toda adaptación de tono pedagógico, metáforas y formato se aplica en la capa de síntesis final del LLM.

# Orchesbrand: Manual de Invocación Antigravity & Control de Estado

Este documento describe la operativa técnica para definir e invocar subagentes dinámicos dentro de Google Antigravity y supervisar el ciclo de vida de la suite de branding.

---

## 1. Protocolo de Invocación de Subagentes en Antigravity

Antigravity opera con subagentes dinámicos en tiempo de ejecución. El orquestador ejecuta el siguiente patrón:

```
1. Leer el archivo SKILL.md de la fase destino:
   target_prompt = view_file("/var/www/.agents/skills/<fase>/SKILL.md")

2. Registrar el subagente dinámico:
   define_subagent(
     name: "<fase>",
     description: "Worker especializado en <fase>",
     system_prompt: target_prompt,
     enable_mcp_tools: true,
     enable_write_tools: true
   )

3. Disparar la ejecución:
   invoke_subagent(
     Subagents: [{
       TypeName: "<fase>",
       Role: "Branding <Fase> Specialist",
       Prompt: "Ejecutar <fase> para la marca [MARCA] leyendo /var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/..."
     }]
   )
```

---

## 2. Manejo de Errores y Diagnóstico Forense

- Si un subagente devuelve un error o genera un JSON que no valida el schema:
  1. El orquestador lee el log del subagente.
  2. Identifica la clave faltante o tipo incorrecto.
  3. Re-invoca con instrucción de remediación explícita.
- Máximo 2 intentos antes del apagado seguro del circuito.

---

## 3. Arquitectura Desacoplada & Modos de Invocación

La fuente primaria y canónica de verdad es `astrobranding_<brand>.md` junto con `dev/verticals/<vertical>.json`.
- **Desacople y Aislamiento de Workspace:** `orchesbrand` v3.0 invoca `chroma-engine`, `fontgen-engine` y `envato-font-preview` escribiendo únicamente en `dev/workspaces/<vertical>/brand/` (o `--output-dir`), sin crear carpetas fantasmas globales.
- **Merge No Destructivo de `brandbook.json`:** Preserva `brand_architecture`, `voice_tone_and_messaging`, `lexicon` y `target_audience` mientras inyecta los tokens OKLCH y tipográficos validados.
- **CLI Soberano:**
  `orchesbrand --brand <BRAND> --vertical <slug> --project-dir /var/www/localstorage/<Project>/dev --phases chroma,fontgen,previews,brandbook --audit`


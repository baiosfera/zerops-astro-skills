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

La fuente primaria y canónica de verdad es `astrobranding_[MARCA].md` compilado por Oráculo en Fase 0 a partir de los shards del VirtualDataLake.
- **Desacople Total de Cascada:** La cascada entre fases es opcional y no bloqueante. Las skills (`fontgen`, `symbol`, `chroma`, `kinetic`, `brandbook`) pueden ser invocadas de forma aislada sin requerir que las fases precedentes se hayan ejecutado o completado.
- **Modo Interactivo (Brandview):** Brandview puede invocar o solicitar la ejecución de una fase particular cuando el usuario interactúa con la interfaz web.
- **Resiliencia de Manifiestos:** Cada fase genera su contrato de salida específico consumiendo directamente el SSoT y enriqueciendo los manifiestos preexistentes en `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/`.


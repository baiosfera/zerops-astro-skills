# Docu Reference Manual: Skill Certification & Invariance Gate (v7.0)

## 1. Concepto Fundamental & Justificación Arquitectónica
En el ciclo de vida de las habilidades de agente (Agent Skills), un antipatrón recurrente es la **mutación compulsiva** (*Gratuitous Churn*): la tendencia de los agentes a asumir que toda invocación de auditoría o mejora exige forzosamente reescribir o alterar archivos, incluso cuando la skill ya ha alcanzado un estado óptimo, robusto y antifrágil.

> **Principio de Invarianza Normativa:**
> Una skill que satisface al 100% los contratos estructurales, de contenido y de atestación física es un **activo definitivo e invariante**. Mantiene estrictamente 0 bytes de mutación en disco salvo evidencia demostrable de drift técnico externo, fallo de pruebas o deprecación de APIs.

---

## 2. Las Tres Modalidades Operativas de `docu`

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        DOCU LIFECYCLE ROUTER                           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         ▼                          ▼                          ▼
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│  SCAFFOLD MODE   │      │   PATCH MODE     │      │INVARIANCE / AUDIT│
│                  │      │                  │      │                  │
│ Nueva skill      │      │ Deriva técnica,  │      │ Evaluación       │
│ desde cero bajo  │      │ APIs deprecadas  │      │ contra los 5     │
│ 4 arquetipos.    │      │ o sensores en    │      │ criterios        │
│ Progressive      │      │ fallo (exit != 0)│      │ normativos.      │
│ Disclosure.      │      │                  │      │                  │
└──────────────────┘      └──────────────────┘      └─────────┬────────┘
                                                              │
                                       ┌──────────────────────┴───────┐
                                       ▼                              ▼
                             [Criterios Cumplidos]         [Criterios Violados]
                                       │                              │
                                       ▼                              ▼
                             CERTIFICADO ÓPTIMO             Transición a
                             (Cero Mutaciones)              Patch / Refactor
```

1. **Scaffold Mode (Construcción Inicial):** Generación de nuevas habilidades aplicando el estándar de 3 niveles de Progressive Disclosure y Positive Guidance estricto bajo el arquetipo correspondiente.
2. **Patch / Refactor Mode (Mantenimiento por Deriva):** Intervención quirúrgica y acotada triggered únicamente por:
   - Actualización de versiones upstream de bibliotecas o APIs.
   - Fallo en los sensores físicos deterministas (`exit code != 0`).
   - Violación del presupuesto de tokens en `SKILL.md` (> 700 tokens).
3. **Certification & Invariance Mode (Auditoría & Blindaje):** Inspección pasiva determinista. Si la skill cumple los 5 criterios de certificación a nivel superficial y profundo, se emite el dictamen de invariancia y se detiene el flujo con 0 mutaciones.

---

## 3. Los 5 Criterios Normativos de Certificación Invariante

Toda skill candidata a certificación debe aprobar formalmente la siguiente lista de verificación:

| Criterio | Nombre del Contrato | Verificación Determinista | Sensor de Atestación |
|---|---|---|---|
| **C1** | **Anatomía Canónica & Higiene Profunda** | Presencia de `SKILL.md`, `references/`, `assets/`, `scripts/`, cero `__pycache__` y esquemas JSON válidos. | `test -d references && test -d scripts && [ $(find . -name '__pycache__' \| wc -l) -eq 0 ]` |
| **C2** | **Presupuesto Nivel 2** | `SKILL.md` menor a 500 palabras (~550 tokens) sin advertencias. | `wc -w < SKILL.md` (Tokens <= 550) |
| **C3** | **Zero Deletion Invariant** | 100% de métodos, esquemas, tipos y matrices de error preservados en `references/`. | Inspección cruzada contra respaldo `bak/` |
| **C4** | **Arnés CoHaLo & Positive Guidance** | Sensor determinista `scripts/<skill>-validate.sh` presente, ejecutable y libre de directivas prohibitivas en plantillas. | `bash scripts/<skill>-validate.sh` $\to$ **`exit code 0`** |
| **C5** | **Paridad SSoT Soberana** | Espejo idéntico en Google Drive y compatibilidad con `unisetup.sh` (clean-room virgin ZCP). | `ssot-parity-check` $\to$ **`exit code 0`** |

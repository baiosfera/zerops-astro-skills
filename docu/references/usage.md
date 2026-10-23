# Docu — Dual-RAG Construction, Archetypes & Workflow Manual (v2.0)

Este manual documenta el flujo de trabajo de 8 pasos para la construcción, evolución y refactorización de skills Dual-RAG bajo Fractal CoHaLo v8.4.

---

## 1. La Tríada Epistémica y Desacople Arquitectónico

```text
[cohalo / 00-SUPREME-DIRECTIVE] ──(Fase F2)──> [research (12 Motores)] ──(Dossier Verbatim)──> [docu / meta-skill]
                                                                                                      │
                                                                           ┌──────────────────────────┴──────────────────────────┐
                                                                           ▼                                                     ▼
                                                                  [SKILL.md (<= 480 palabras)]                          [references/ (Usage & Infra)]
```

---

## 2. Los 4 Arquetipos Funcionales

| Arquetipo | Propósito Principal | Estructura Requerida |
|---|---|---|
| **Framework** | Frameworks frontend/backend (Astro, Next.js, FastAPI, Bun) | `SKILL.md` + `references/usage.md` + `infra.md` |
| **Infra** | Plataformas, bases de datos, colas (Zerops, Postgres, Valkey, NATS) | `SKILL.md` + `references/usage.md` + `infra.md` |
| **Domain** | Reglas de negocio y motores especializados (Oráculo, CRM, DIAN) | `SKILL.md` + `references/usage.md` + `infra.md` |
| **Cognitive** | Razonamiento, revisión, planificación (Codecraft, Planner, Docu) | `SKILL.md` + `references/usage.md` + `infra.md` |

---

## 3. Flujo de Trabajo de 8 Pasos (Ciclo de Vida)

1. **Ingestión de Hechos (F0)**: Triangulación con `research` y extracción de especificaciones verbatim.
2. **Clasificación de Arquetipo**: Selección del arquetipo normativo.
3. **Presupuesto de Router**: `SKILL.md` estrictamente $\le 480$ palabras (~550 tokens) enfocado en Positive Guidance y compuertas de decisión.
4. **Desacople Espacial (Dual-RAG)**: Reubicación de código, tablas de comandos y guías en `references/usage.md` y `references/infra.md`.
5. **Invariante de Cero Mutilación**: Preservación del 100% de firmas AST, APIs y contratos.
6. **Validación Física**: Verificación con sensores reales (`skills-suite-validate` exit code 0).
7. **Sincronización SSoT**: Paridad indivisible con Google Drive y GitHub.
8. **Reindexación**: Actualización del registro con `gentle-ai skill-registry refresh --force`.

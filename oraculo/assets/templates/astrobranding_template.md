# Especificación de Diseño AstroBranding (SSoT Semiótico): <NOMBRE_DE_MARCA> 🎨
*Puente estructurado de inteligencia semiótica sintetizado en Fases 10 y 11 — Destino: Suite de Diseño Orchesbrand*  
*Plantilla Agnóstica y Holística — Subordinada a los Arquetipos Astrológicos Maestros y Contratos de Orchesbrand*

---

## 1. 🌌 Génesis Astrológica & Autoridad Arquetípica
La carta natal se sintetiza en el núcleo psicológico de la marca y su territorio soberano de mercado:
- **Huella del Vehículo Comercial**: Compatibilidad entre la vibración caldea/pitagórica de la marca y el número conductor del fundador.
- **Arquetipo Rector de Marca (Primario)**: Arquetipo maestro dominante derivado de la síntesis natal (e.g. Arquitecto Soberano, Especialista Sabio, Alquimista, Gobernante).
- **Arquetipo Secundario (Balance)**: Arquetipo de balance derivado del Lagna Védico, Amatyakaraka y Tronco del Día BaZi.
- **Arquetipo de Sombra (Punto Ciego)**: Tensión subconsciente que la marca trasciende conscientemente (derivada de Desafíos activos o eje nodal).
- **Tensión Mitológica**: El conflicto sagrado central que la marca resuelve de forma única para su audiencia, transformando complejidad diagnóstica en orden práctico.
- **Manifiesto de Autoridad de Marca**: 2 a 3 párrafos articulando la voz soberana, no vendedora, de la marca en el mercado.

---

## 2. 🔤 Directivas Tipográficas Semióticas (Insumo para `fontgen` — Fase 1)
Directivas mapeadas al Arquetipo Rector. Descriptores morfológicos y semióticos puros; la selección de fuentes específicas la resuelve downstream `fontgen`.
- **Titulares / Display (Token Primario — Envato Elements)**:
  - *Categoría Morfológica*: Serif vs Sans-Serif, Neoclásica vs Brutalista/Moderna, Alto Contraste vs Monolineal.
  - *Expresión Arquetípica*: Atributos que reflejan la autoridad del Arquetipo Primario (dignidad lapidaria, precisión arquitectónica o herencia editorial).
  - *Jerarquía Óptica*: Distribución de pesos, proporciones, recomendaciones de tracking (compacto para titulares monolíticos).
- **Cuerpo de Texto / Lectura (Token Secundario — Google Fonts Variable)**:
  - *Categoría Morfológica*: Sans-Serif geométrica o humanista neutral, contraformas abiertas, altura de x amplia para cero fatiga cognitiva.
  - *Experiencia de Lectura*: Legibilidad sin esfuerzo en pantallas móviles, tablas de datos y reportes diagnósticos densos.
- **Acento / Micro-UI (Token Terciario — Monograma / Citas)**:
  - *Rol Estilístico*: Glifos distintivos, iniciales esculpidas o precisión monoespaciada para metadatos.

---

## 3. 📐 Directivas Vectoriales y Monocromáticas Estrictas (Insumo para `symbol` — Fase 2 B/N)
Directivas mapeadas a las compuertas de decisión en `symbol/SKILL.md`. Blanco y negro puro (`currentColor`, sin rellenos de color).
- **Geometría Sagrada y Familia Vectorial**:
  - *Sabio / Gobernante*: Geometría euclidiana simétrica (Círculos concéntricos, Octagrama, Flor de la vida, Escudo con monograma esculpido).
  - *Mago / Rebelde / Atleta*: Elipses orbitales cinéticas, espirales doradas dinámicas, sellos angulares.
  - *Inocente / Creador / Amante*: Geometría orgánica fluida, dibujo lineal continuo, armonía minimalista.
- **IDs Semánticos Obligatorios de Nodos para Animación Posterior**:
  - `#symbol-core`: Marca central del núcleo y gravedad del monograma.
  - `#symbol-orbit-1` y `#symbol-orbit-2`: Elipses orbitales cinéticas o arcos concéntricos.
  - `#symbol-geometry-star`: Polígonos de geometría sagrada, estrellas o sellos envolventes.
  - `#symbol-monogram`: Glifos vectoriales de las iniciales de la marca.
- **Parámetros de Lockup**: Guías estructurales para `symbolScale`, `symbolX`, `symbolY`, `brandY`, `sloganY`.

---

## 4. 🎨 Conceptos Cromáticos Semánticos (Insumo para `chroma` — Fase 3)
Fundamentos conceptuales para los 3 ecosistemas OKLCH completos. Directivas de color perceptivo semántico; los códigos HEX dependientes del dispositivo son resueltos downstream por `chroma`.
- **3 Ecosistemas Arquetípicos Diferenciados**:
  - *Ecosistema 1 (Esencia del Arquetipo Primario)*: Ej. Lujo Silencioso / Autoridad Soberana — Obsidiana Oscura & Mineral Puro.
  - *Ecosistema 2 (Esencia del Arquetipo Secundario)*: Ej. Sabiduría Profunda / Santuario Analítico — Índigo Nocturno & Perla Luminosa.
  - *Ecosistema 3 (Síntesis Alquímica)*: Ej. Transición Sagrada / Alto Impacto — Arcilla Profunda & Llama Dorada.
- **7 Tokens Semánticos Funcionales por Ecosistema (Modos Claro y Oscuro)**:
  - Definición de roles para: `primary`, `secondary`, `accent`, `background`, `surface`, `text_primary`, `text_muted`.
- **Mandato de Accesibilidad y Contraste**: Cumplimiento estricto WCAG 2.2 AAA ($\ge 7.0:1$) y APCA ($L_c \ge 75.0$) en ambos modos.

---

## 5. ⚡ Directivas de Animación Cinética y Micro-Audio (Insumo para `kinetic` — Fase 4)
Parámetros de diseño de movimiento a 60fps dirigidos a los IDs semánticos del SVG y síntesis de audio ADSR en Web Audio.

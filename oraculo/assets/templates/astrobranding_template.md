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
- **Fundamento Bioenergético (Medicina China TCM & BaZi — Shard 11 y Shard 04)**:
  - *Distribución Elemental*: Porcentajes exactos de Madera (Creatividad/Expansión), Fuego (Visibilidad/Pasión), Tierra (Estabilidad/Confianza), Metal (Estructura/Precisión) y Agua (Profundidad/Fluidez).
  - *Elemento Favorable (`Yong Shen`)*: El elemento bioenergético corrector que la paleta cromática debe amplificar para inducir equilibrio y autoridad en el receptor.
  - *Elemento Excesivo o Desafiante*: Tonalidades que deben calibrarse como acentos restringidos o matices secundarios para evitar fatiga perceptual.
- **Mandato de Accesibilidad y Contraste**: Cumplimiento estricto WCAG 2.2 AAA ($\ge 7.0:1$) y APCA ($L_c \ge 75.0$) en modos Claro y Oscuro para el ecosistema primario.

---

## 5. ⚡ Directivas de Animación Cinética y Micro-Audio (Insumo para `kinetic` — Fase 4)
Parámetros de diseño de movimiento a 60fps dirigidos a los IDs semánticos del SVG y síntesis de audio procedural en Web Audio API:
- **Tempo y Ritmo Energético (Derivado de Shadbala #1 y Modalidades)**:
  - *Velocidad & Duración*: Si predomina Aire/Marte: transiciones rápidas (0.4s - 0.7s) con eases agudos `power3.out`. Si predomina Tierra/Saturno: cadencia pausada, monumental (1.2s - 2.0s) con `sine.inOut` o `expo.out`.
  - *Coreografía de Capas*: Entrada escalonada (`stagger: 0.15`): primero el núcleo `#symbol-core`, luego los anillos cinéticos `#symbol-orbit-*`, seguidos del monograma `#symbol-monogram` y finalmente la firma tipográfica.
- **Micro-Interacciones Procedurales**:
  - *Hover State*: Resonancia armónica, micro-rotación orbital ($\le 15^\circ$) y expansión de radio del núcleo (+4%).
  - *Active / Click*: Pulso elástico y contracción dimensional instantánea.
- **Parámetros de Síntesis de Audio (ADSR en Web Audio API)**:
  - *Frecuencia Base*: Afinación modal acorde al elemento dominante (Agua: 432 Hz, Fuego: 528 Hz, Tierra: 136.1 Hz Ohm, Metal: 741 Hz, Aire: 639 Hz).
  - *Envolvente*: Attack: 0.02s, Decay: 0.15s, Sustain: 0.1, Release: 0.4s.

---

## 6. 📦 Consolidación de Tokens W3C DTCG (Insumo para `brandbook` — Fase 5)
Estructura canónica de tokens de diseño para exportación JSON W3C Design Tokens Community Group:
- **Estructura de Tokens**: Todo token debe declarar su valor (`$value`), tipo (`$type`: `color`, `dimension`, `fontFamily`, `fontWeight`, `duration`) y descripción de intención (`$description`).
- **Arquitectura de Capas DTCG**:
  1. *Global / Core*: Primitivas matemáticas en OKLCH y familias tipográficas puras.
  2. *Semántico / Alias*: Roles funcionales (`color.surface.brand`, `color.action.primary`, `typography.heading.display`).
  3. *Componente / Override*: Sobrescrituras para UI SaaS (`button.primary.background`, `card.surface.elevated`).
- **Showcase Interactivo**: Requisitos para el compilador de `index.html` con cambio en tiempo real entre los 3 Ecosistemas y alternancia Claro/Oscuro sin parpadeos de FOUC.

---

## 7. 🌍 Anclaje Geográfico & Expansión Comercial (Insumo de Shard 09 — ACG)
Líneas de poder astronómico y polos de atracción física para penetración de mercado y eventos de marca:
- **Líneas de Tracción Comercial (Mercurio MC / Júpiter MC)**: Coordenadas geográficas y ciudades de máxima proyección pública, contratos masivos y alianzas institucionales.
- **Líneas de Fidelización y Atracción Magnética (Venus DSC / Sol ASC)**: Regiones y polos culturales donde la identidad de marca genera fascinación natural y resonancia con clientes de alto valor.
- **Top 5 Ciudades de Anclaje de Marca**: Mapeo de ciudades globales donde convergen parans favorables para sedes corporativas, lanzamientos o servidores edge.

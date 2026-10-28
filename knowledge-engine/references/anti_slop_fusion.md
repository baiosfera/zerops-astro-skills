# Decoupled Anti-Slop Fusion Protocol

This document defines the 2-step transmutation protocol that merges upstream knowledge extracted from courses (via Google NotebookLM or `/var/www/baiosfera/PLAYBOOKS/`) with downstream brand identity systems (`brandbook.json`).

---

## 1. The Core Decoupling Thesis

Raw outputs from marketing courses or LLM summaries often default to generic clichés ("lleva tu negocio al siguiente nivel", "en el mundo competitivo de hoy", "una experiencia inolvidable") or carry the personal voice of the course instructor.

To preserve authentic brand differentiation across multiple Zerops projects, strategic knowledge must be handled through strict separation of concerns:
- **Upstream (The Skeleton)**: Universal conversion mechanics, psychological triggers, value equations, and structural sequencing.
- **Downstream (The Flesh & Voice)**: The unique lexical dictionary, tone of voice, OKLCH color palette, and philosophical boundaries of the active brand.

```
┌─────────────────────────────────┐
│   Google NotebookLM / Courses   │  <- High-Density Knowledge (Fórmulas, Heurísticas)
└────────────────┬────────────────┘
                 │
                 ▼ Step 1: Structural Extraction (Frameworks Only)
┌─────────────────────────────────┐
│   Logical Skeleton / Blueprint  │  <- Pure Wireframe & Variable Slots
└────────────────┬────────────────┘
                 │
                 ▼ Step 2: Lexical Transmutation (Local Brandbook Infusion)
┌─────────────────────────────────┐
│  /var/www/localstorage/<BRAND>  │  <- brandbook.json, Lexicon, Prohibited Words, OKLCH
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│   Physical Anti-Slop Linter     │  <- anti-slop-linter (Exit Code 0 Verification)
└─────────────────────────────────┘
```

---

## 2. Step 1: Upstream Structural Extraction

Query the relevant NotebookLM cluster or read the corresponding SSoT playbook in `/var/www/baiosfera/PLAYBOOKS/`.
Extract strictly the abstract formula, leaving variable slots for brand data:

### Example: Alex Hormozi Offer Skeleton
- **Formula**: `[Resultado Soñado] con [Mecanismo Único] garantizado en [Plazo], sin [Dolor/Fricción Principal].`
- **Componentes Requeridos**:
  * Variable A: Dream Outcome (Resultado final transformacional).
  * Variable B: Unique Mechanism (El método o activo propietario).
  * Variable C: Time Delay (Horizonte temporal tangible).
  * Variable D: Effort & Sacrifice Eliminator (Objeción o tarea odiada por el cliente).
  * Bonus Stack: 3 activos complementarios con valor percibido individual.
  * Risk Reversal: Tipo de garantía (incondicional o condicional cuantificable).

---

## 3. Step 2: Downstream Lexical Transmutation

Read the active project's brand definition from:
- `/var/www/localstorage/${PROJECT_NAME}/dev/brandbook.json`, or
- `/var/www/baiosfera/PROYECTOS/${PROJECT_NAME}/dev/brandbook.json`.

Extract the brand constraints:
1. **Pronoun & Addressing**: Form of address (`tú`, `vos`, `usted`).
2. **Lexical Tone**: Dominant emotional frequency (ej. hedonismo elegante y misterio en El Placer de Compartir; lujo silencioso y rigor artesanal en Catalina Glamur).
3. **Blacklisted Vocabulary**: Terms rejected by the brand's identity manual (ej. términos místicos o esotéricos en El Placer de Compartir; jerga barata o urgencia desesperada en Catalina Glamur).
4. **Visual & Design Tokens**: Tailwind CSS classes, OKLCH colors, and typography styles defined in the brandbook.

### Transmutation Rule:
Substitute each structural slot from Step 1 using exclusively the vocabulary and tonal frequency of Step 2. Verify that every headline, body paragraph, button label, and FAQ item reflects the specific worldview of the brand.

---

## 5. Sovereign Invariant: 100% Brand-Agnostic Playbooks (Zero-Brand Slop)

Playbooks compiled in `/var/www/baiosfera/PLAYBOOKS/` serve as the universal algorithmic foundation across all projects.

1. **Absolute Ban on Upstream Brand Names**:
   Never include names of academies, platforms, or commercial authors (e.g., `Platzi`, `DigitalMarketer`, `Velocity Media`, `Mindvalley`, `Carlos Muñoz`, etc.) within generated playbooks.
2. **Pure Algorithmic & Structural Content**:
   Playbooks must strictly contain mathematical conversion equations, psychological trigger frameworks, funnel schemas, and abstract wireframe contracts.
3. **Downstream Transmutation Integrity**:
   When downstream skills (`astro-web`, `frnt`, `bknd`) ingest a playbook, they must only receive universal frameworks to be transmuted with the active brand's tokens, guaranteeing 0 cross-brand contamination.

Before committing or integrating generated copy or landing page markup into Astro components, execute the physical anti-slop linter:

```bash
anti-slop-linter --brand "${PROJECT_NAME}" --file path/to/output.astro
```

The linter validates:
- **Zero Blacklisted AI Clichés**: Absence of generic LLM phrases.
- **Brand Lexicon Compliance**: Strict adherence to the brand's positive vocabulary and avoidance of forbidden words.
- **Format Integrity**: Presence of required structural elements (Hook, Proof, Mechanism, Offer, CTA).

# Decoupled Anti-Slop Fusion Protocol

This document defines the 2-step transmutation protocol that merges upstream knowledge compiled in **Baiosfera Knowledge Hub** (`/var/www/localstorage/knowledge_hub/02_PLAYBOOKS_MAESTROS/`, aliased at `/mnt/localstorage/playbooks/` and mirrored from `baiosfera:KNOWLEDGE_HUB/02_PLAYBOOKS_MAESTROS/`) with downstream brand identity systems (`brandbook.json`).

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

Read `INDEX.json` task routes and the canonical playbooks directly from `/mnt/localstorage/playbooks/` (`/var/www/localstorage/knowledge_hub/02_PLAYBOOKS_MAESTROS/`).
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
2. **Lexical Tone**: Dominant emotional frequency (e.g. refined editorial wit for an experiential brand; quiet luxury and artisanal rigor for a high-ticket studio).
3. **Blacklisted Vocabulary**: Terms rejected by the brand's identity manual (e.g. mystical clichés for a rationalist brand; cheap urgency or discount jargon for a luxury brand).
4. **Visual & Design Tokens**: Tailwind CSS classes, OKLCH colors, and typography styles defined in the brandbook.

### Transmutation Rule:
Substitute each structural slot from Step 1 using exclusively the vocabulary and tonal frequency of Step 2. Verify that every headline, body paragraph, button label, and FAQ item reflects the specific worldview of the brand.

---

## 4. Physical Verification Gate

Before committing or integrating generated copy or landing page markup into Astro components, execute the physical anti-slop linter:

```bash
anti-slop-linter --brand "${PROJECT_NAME}" --file path/to/output.astro
```

The linter validates:
- **Zero Blacklisted AI Clichés**: Absence of generic LLM phrases.
- **Brand Lexicon Compliance**: Strict adherence to the brand's positive vocabulary and avoidance of forbidden words.
- **Format Integrity**: Presence of required structural elements (Hook, Proof, Mechanism, Offer, CTA).

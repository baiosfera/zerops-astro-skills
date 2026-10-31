# `brand-play` — Usage Guide & Multi-Surface Transmutation Recipes

## 1. Slot Hydration Algorithm

The `brand-play` engine consumes universal, mathematical TYM (Type-YAML-Markdown) playbooks from `/var/www/baiosfera/PLAYBOOKS/` and hydratates all declared semantic slots (`{{SLOT}}`) using W3C DTCG tokens from `/var/www/localstorage/${PROJECT_NAME}/dev/brandbook.json`.

### Pipeline Execution Flow
1. **Source Ingestion**: Load the raw universal playbook from `/var/www/baiosfera/PLAYBOOKS/<cluster>_playbook.md`.
2. **Schema Separation**: Extract Frontmatter, `<system_dynamics>`, `<slots_contract>`, and `<modular_blocks>`.
3. **Token Resolution**: Read the active brandbook (`/var/www/localstorage/${PROJECT_NAME}/dev/brandbook.json`), resolving DTCG `$value` nodes matching the slot pointers.
4. **AST Replacement**: Execute replacement of all `{{SLOT}}` markers using strict coalescing fallbacks for non-required slots.
5. **Anti-Slop Linter**: Verify that zero unresolved `{{...}}` tags remain and no prohibited words from `communication_dictionary.prohibited_words_commercial_bias` leaked into the output.

---

## 2. Multi-Surface Transmutation Recipes

### Recipe A: Copywriting & Growth Engine (`growth-engine`)
- **Input Block**: `#mod-hero`, `#mod-mechanism`, `#mod-pricing`.
- **Target Contract**: `PillarContentInputSchema` in `growth-engine`.
- **Inference**: Bifrost Gateway (`http://bifrost:8080/v1/chat/completions`) with `x-tier: production` (temperature 0.2).
- **Anti-SPAM Linter**:
  - Subject lines strictly between 30 and 50 characters (4 to 7 words).
  - Maximum 1 emoji, zero ALL-CAPS words, zero multiple exclamation marks (`!!`).
  - Expected complaint rate $< 0.10\%$.

### Recipe B: Web Components & Landing Pages (`astro-web`)
- **Token Compilation**: Compiles `$type: "color"` and `$type: "fontFamily"` into Tailwind CSS v4 `@theme` block in `src/styles/global.css`:
  ```css
  @theme {
    --color-brand-primary: var(--brand-primary);
    --color-brand-canvas: var(--brand-canvas);
    --font-display: var(--brand-font-display);
    --font-body: var(--brand-font-body);
  }
  ```
- **Component Scaffolding**:
  - `#mod-hero` $\to$ `src/components/landing/HeroSection.astro`
  - `#mod-pricing` $\to$ `src/components/pricing/PricingTable.astro`
- **Server Islands (`server:defer`)**: Personalization blocks (e.g. VIP badge, attendee name) render with `server:defer` and SVG skeleton fallbacks, decrypted via `ASTRO_KEY`.

### Recipe C: Conversational Agent Flows (`whatsapp-engine`)
- **Worker Target**: Bun LXC `whatsappbot` (Evolution Go + NATS JetStream).
- **Conversational State Machine (4 Phases)**:
  1. *Fase 1 (Bienvenida)*: Natural tone matching `voice_tone_and_messaging.triad_of_voices`.
  2. *Fase 2 (Cualificación BANT)*: Diagnostic questions derived from `iceberg.patterns_adaptive`.
  3. *Fase 3 (Mecanismo & Ética)*: Ethical agreement and consent charter before pricing.
  4. *Fase 4 (Cierre & Reserva)*: Deposit link ($100.000 COP) with delayed confirmation.
- **Operator Lock**: Respects `#stop`, `#mute`, `#bot` commands with Valkey key locks (`EX 86400`).

### Recipe D: Transactional & Lifecycle Email (`email-marketing`)
- **React Email 3.0**: Renders modular email components with 100% inline CSS and compiled HTML footprint $< 85\text{ KB}$ (preventing Gmail clipping).
- **Deliverability Compliance**: Injects RFC 8058 `List-Unsubscribe: <https://...>, <mailto:...>` headers, DMARC `p=reject`/`p=quarantine`, and DKIM 2048-bit signatures.
- **Throttling**: Valkey/BullMQ queue limited to 10 dispatches/sec.

---

## 3. Anti-Slop Validation & CLI Usage

### CLI Commands
```bash
# Transmute a single playbook for active brand
brand-play transmute --playbook offers_pricing --brand elplacerdc --target web

# Transmute all 18 playbooks for active brand across all targets
brand-play transmute --all --brand elplacerdc --target all

# Run integrity validation
skills-suite-validate && ssot-parity-check
```

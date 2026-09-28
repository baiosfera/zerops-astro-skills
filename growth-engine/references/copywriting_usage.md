# Copywriting Vanguard & LatAm Neuro-Persuasion: Usage & Development Guide (v1.2)

> **SSoT Reference Document:** `.agents/skills/copywriting-vanguard/references/usage.md`  
> **Ámbito:** Frameworks de neuro-copywriting, psicología de compra en Colombia/LatAm, Linter Anti-SPAM 2025/2026, calibración de arquetipo de voz desde `brandbook.json` y motor de atomización omnicanal tipado con Zod.

---

## 1. Frameworks Canónicos de Copywriting de Alta Conversión

### 1.1. StoryBrand 2.0 (Donald Miller — SB7 Framework)
Estructura donde el cliente es el Héroe y la marca es el Guía que le muestra el camino:
1. **Un Personaje (El Héroe):** Define el deseo primario del cliente (tiempo, estatus, dinero, tranquilidad).
2. **Con un Problema (3 Capas Indivisibles):**
   * *Externo (El síntoma tangible):* "Nuestras prendas deportivas pierden soporte y elegancia tras pocas posturas."
   * *Interno (La emoción/frustración):* "Siento que tengo que sacrificar comodidad para lucir sofisticada."
   * *Filosófico (La injusticia):* "Nadie debería tener que elegir entre el alto rendimiento físico y la distinción de alta costura."
3. **Se encuentra con un Guía (Tu Marca):**
   * *Empatía:* "Entendemos la exigencia de tu ritmo de vida."
   * *Autoridad:* Pruebas medibles (textiles de autor, confección local de precisión, testimonios de clientas reales).
4. **Que le entrega un Plan de 3 Pasos:**
   * Paso 1: Explora la colección privada.
   * Paso 2: Elige tu silueta y talla perfecta con nuestra guía ergonómica.
   * Paso 3: Recibe en tu puerta con envío express y garantía de ajuste total.
5. **Y lo llama a la Acción:**
   * *Direct CTA:* "Descubrir la Colección", "Comprar ahora con PSE / Tarjeta".
   * *Transitional CTA:* "Ver Catálogo en WhatsApp", "Suscribirme al club exclusivo".
6. **Que le ayuda a Evitar el Fracaso (Stakes Negativos):** Seguir usando prendas genéricas que no reflejan tu estándar de excelencia.
7. **Y culmina en el Éxito (Visión de Victoria):** Sentir la seguridad y presencia que otorga una prenda de lujo silencioso.

---

## 2. Ecuación de Valor de Alex Hormozi ($100M Offers)

$$\text{Valor Percibido} = \frac{\text{Resultado Soñado} \times \text{Probabilidad Percibida de Éxito}}{\text{Demora de Tiempo} \times \text{Esfuerzo y Sacrificio}}$$

* **Numerador (Multiplicadores de Valor):**
  * *Resultado Soñado:* Elevar el estatus y resolver un dolor profundo.
  * *Probabilidad Percibida:* Casos de estudio en video, testimonios locales y garantías incondicionales de 30 días.
* **Denominador (Destructores de Valor — Minimizarlos a Cero):**
  * *Demora de Tiempo:* Entregar un *Quick Win* tangible en las primeras 24-48 horas (envío express inmediato).
  * *Esfuerzo y Sacrificio:* Cambios de talla sin costo a domicilio.

---

## 3. P.A.S.T.O.R. (Ray Edwards)
1. **P - Problem / Person:** Identificar a la persona exacta y su dolor con sus propias palabras.
2. **A - Amplify:** Amplificar el costo financiero y emocional de posponer la decisión.
3. **S - Story & Solution:** La historia del descubrimiento de la nueva tecnología textil o diseño.
4. **T - Transformation & Testimony:** Pruebas y testimonios de transformación real.
5. **O - Offer:** La propuesta irresistible (80% beneficios / 20% características).
6. **R - Response:** Instrucciones paso a paso sobre cómo responder de inmediato.

---

## 4. Linter Anti-SPAM 2025/2026 para Email Copywriting

Todo texto redactado para correo electrónico debe pasar por los siguientes filtros heurísticos antes de despacharse:

### 4.1. Taxonomía de Palabras Gatillo Prohibidas

| Categoría de Riesgo | Términos Prohibidos (Spam Triggers) | Alternativas Seguras Recomendadas |
| :--- | :--- | :--- |
| **Financiero / Dinero** | `GANA DINERO RÁPIDO`, `INGRESOS PASIVOS 100%`, `SIN COSTO`, `TOTALMENTE GRATIS`. | `Descubre la propuesta`, `Acceso incluido`, `Inversión estratégica`. |
| **Urgencia Artificial** | `URGENTE`, `ACTÚA AHORA MISMO`, `HAZ CLIC AQUÍ`, `ÚLTIMOS SEGUNDOS`, `NO LO DEJES PASAR`. | `Disponible hasta el viernes`, `Conoce los detalles`, `Revisa la disponibilidad`. |
| **Promesas Exageradas** | `100% GARANTIZADO`, `CURA DEFINITIVA`, `RESULTADOS MILAGROSOS`. | `Garantía de satisfacción de 30 días`, `Confección respaldada`. |
| **Patrones Engañosos** | `Re: Factura pendiente`, `Fwd: Confirmación urgente`, `COMPRA YA (ALL CAPS)`, `¡¡¡OFERTA!!!`. | Asuntos claros: `Confirmación de tu pedido #1024`, `Nueva colección disponible`. |

### 4.2. Reglas del Asunto (*Subject Line*)
* **Longitud Estricta:** Entre **30 y 50 caracteres** (aproximadamente **4 a 7 palabras**).
* **Emojis:** Máximo **1 emoji contextual** por asunto (prohibidas ristras `🔥💰🎉🚀`).
* **Preheader:** Entre **40 y 90 caracteres**, complementando el Asunto sin repetir palabras.
* **Ratio Texto / Imagen:** Mínimo **60% de texto HTML real** y máximo **40% de imágenes**. Prohibidos los correos de una sola imagen.

---

## 5. Calibración de Arquetipo de Voz desde `brandbook.json` (W3C DTCG)

El copywriter debe leer el campo `brand.archetype` y `brand.slogan` de `brandbook.json` para definir el vocabulario y tono de la marca:

```typescript
// Ejemplo de Mapeo de Arquetipos
const archetypeVoiceMap = {
  "La Gobernante / La Amante Sensorial": {
    tone: "Elegante, sobrio, sensorial, exclusivo, seguro, sin hype ni desesperación.",
    keywords: ["distinción", "autoría", "siluetas esculpidas", "confort absoluto", "lujo silencioso"],
    forbiddenJargon: ["ganga", "baratísimo", "oferta loca", "compra ya"]
  },
  "El Héroe / High Performance": {
    tone: "Enérgico, retador, técnico, enfocado en superación y métricas.",
    keywords: ["rendimiento", "resistencia", "precisión", "potencia", "disciplina"]
  },
  "El Sabio / Arquitecto": {
    tone: "Analítico, fundamentado, sereno, basado en primeros principios.",
    keywords: ["arquitectura", "sistemas", "determinismo", "estándar", "evidencia"]
  }
};
```

---

## 6. Invariante de Resguardo de Idioma (Español Natural)

* Toda la redacción en español debe ser **100% natural, fluida y libre de anglicismos técnicos** mezclados (no usar *"Athleisure"*, *"UI"*, *"Display Serif"*, *"Tokens"*, *"Tracking"* en correos para clientes finales).
* Esto garantiza que los clasificadores de Google/Gmail detecten **100% de coherencia en español**, eliminando los falsos positivos y avisos de *"Traducir al español"*.

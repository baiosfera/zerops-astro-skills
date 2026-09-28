# Sales Enablement & AI SDR / Closer: Usage & Development Guide (v1.0)

> **SSoT Reference Document:** `.agents/skills/sales-enablement/references/usage.md`  
> **Ámbito:** Calificación comercial (BANT/CHAMP), scoring híbrido con `pgvector` HNSW, battlecards dinámicas para Colombia y LatAm, y protocolos de handover en Directus 11+ CRM.

---

## 1. Metodologías de Calificación Comercial: BANT & CHAMP

### A. Calificación BANT (Ventas Transaccionales & Triaje Rápido)
1. **Budget (Presupuesto):**
   * Verificación de rangos en COP o USD. Clasificación en `confirmed`, `elastic`, `insufficient` o `unknown`.
2. **Authority (Autoridad de Decisión):**
   * Identificación del interlocutor: `sole_decision_maker`, `economic_buyer`, `influencer`, `champion` o `gatekeeper`.
3. **Need (Necesidad / Dolor Crítico):**
   * Evaluación de impacto financiero si el problema no se resuelve en 60 días (`critical_urgency`, `moderate`, `low_nice_to_have`).
4. **Timing (Ventana de Decisión):**
   * Plazo de implementación: `immediate` ($\le 15$ días), `short_term` (16–45 días), `medium_term` (46–90 días) o `long_term`.

### B. Calificación CHAMP (Ventas Consultivas B2B)
1. **Challenges (Desafíos):** Identificación del cuello de botella antes de discutir presupuestos.
2. **Authority (Autoridad & DMU):** Mapeo de comités y procesos legales/financieros.
3. **Money (Viabilidad de Inversión):** Cuantificación del retorno de inversión (ROI) frente al costo de inacción (COI).
4. **Prioritization (Prioridad Estratégica):** Posición del proyecto en el Top 3 de la compañía.

---

## 2. Algoritmo de Lead Scoring Híbrido (0–100)

$$\text{LeadScore} = (\text{Score}_{\text{explicit}} \times 0.35) + (\text{Score}_{\text{implicit}} \times 0.25) + (\text{Score}_{\text{semantic}} \times 0.40)$$

```typescript
export function calculateHybridLeadScore(params: {
  explicitScore: number;  // 0 - 100 (Firmografía, Presupuesto, Cargo)
  implicitScore: number;  // 0 - 100 (Velocidad en chat, Preguntas clave)
  semanticCosineDistance: number; // Distancia coseno devuelta por pgvector (<=>)
}): { totalScore: number; grade: "A_HOT" | "B_WARM" | "C_NURTURE" | "D_COLD" } {
  // Similitud coseno normalizada de 0 a 100
  const semanticSimilarity = Math.max(0, Math.min(100, (1 - params.semanticCosineDistance) * 100));

  const totalScore = Math.round(
    params.explicitScore * 0.35 +
    params.implicitScore * 0.25 +
    semanticSimilarity * 0.40
  );

  let grade: "A_HOT" | "B_WARM" | "C_NURTURE" | "D_COLD" = "D_COLD";
  if (totalScore >= 75) grade = "A_HOT";
  else if (totalScore >= 50) grade = "B_WARM";
  else if (totalScore >= 30) grade = "C_NURTURE";

  return { totalScore, grade };
}
```

---

## 3. Matriz de Battlecards para Colombia y Latinoamérica

```json
[
  {
    "objectionType": "price",
    "triggerKeywords": ["caro", "presupuesto", "rebaja", "descuento", "muy costoso"],
    "coreAngle": "Costo de Inacción (COI) & ROI acelerado",
    "script": "Entiendo totalmente. Sin embargo, al analizar que tu operación pierde X horas o ventas semanales sin este sistema, la solución se paga sola en menos de 45 días. ¿Te gustaría evaluar cómo estructuramos un plan piloto modular?",
    "proofPoints": ["ROI promedio en 45 días", "Opciones de pago diferido sin interés"]
  },
  {
    "objectionType": "trust",
    "triggerKeywords": ["estafa", "desconfianza", "seguro", "garantía", "no los conozco"],
    "coreAngle": "Prueba social local y pasarelas vigiladas",
    "script": "Es totalmente natural la precaución. Procesamos todos los pagos a través de Wompi / Bancolombia con supervisión de la Superfinanciera, y contamos con más de 250 empresas activas en el país. Puedes revisar nuestro NIT y casos de éxito en vivo.",
    "proofPoints": ["Cero fraude con Wompi PSE", "Casos de éxito documentados en Colombia"]
  },
  {
    "objectionType": "payment_methods",
    "triggerKeywords": ["pse", "nequi", "daviplata", "contra entrega", "tarjeta"],
    "coreAngle": "Flexibilidad total de rieles locales",
    "script": "Disponemos de todos los medios locales: PSE interbancario, Nequi, Daviplata, transferencias directas Bancolombia, tarjetas de crédito y Pago Contra Entrega en las principales ciudades.",
    "proofPoints": ["Acreditación inmediata en línea", "Generación de comprobante CUS"]
  }
]
```

---

## 4. Protocolo de Handover Híbrido hacia Directus CRM

```typescript
export async function executeHandoverToCloser(briefing: {
  leadId: string;
  contactName: string;
  contactPhone: string;
  score: number;
  grade: string;
  summary: string;
  recommendedOffer: string;
}) {
  const directusUrl = process.env.DIRECTUS_URL || "http://directus:8055";
  const token = process.env.DIRECTUS_SERVER_TOKEN;

  const res = await fetch(`${directusUrl}/items/crm_deals`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      lead_id: briefing.leadId,
      title: `Oportunidad Calificada: ${briefing.contactName} (Score: ${briefing.score})`,
      status: "pending_assignment",
      priority: briefing.grade === "A_HOT" ? "high" : "normal",
      notes: briefing.summary,
      phone: briefing.contactPhone,
      recommended_offer: briefing.recommendedOffer
    })
  });

  return await res.json();
}
```

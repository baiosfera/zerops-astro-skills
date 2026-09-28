---
name: "orders-fulfillment"
description: "Trigger: orders-fulfillment, mipaquete, skydropx, envia api, coordinadora dane, servientrega sisclinet, waybill generation, zpl pdf label, dane divipola 8 digits, domestic carrier logistics, atomic stock locking, pago contra entrega cod. Architect, develop, and automate domestic carrier fulfillment and multi-carrier aggregators (MiPaquete, Skydropx, Envia.com, Coordinadora, Servientrega), Cash on Delivery (COD) payouts, atomic inventory locking in Directus/PostgreSQL, 8-digit DANE Divipola address normalization, thermal shipping label generation (ZPL/PDF), and real-time webhook tracking."
license: "MIT"
metadata:
  author: "Gentleman Programming"
  version: "2.0"
  cohalo-standard: "6.7"
---

# `orders-fulfillment`: Domestic Multi-Carrier Logistics & Atomic Inventory Engine (v2.0)

## Activation Contract
Activate whenever developing, automating, or optimizing post-checkout order processing, domestic multi-carrier shipping aggregators (**MiPaquete.com**, **Skydropx**, **Envia.com**), direct carrier protocols (**Coordinadora Mercantil**, **Servientrega SISCLINET**), Cash on Delivery (COD / Recaudo) management, atomic stock reservations in Directus/PostgreSQL, **8-digit DANE Divipola** geolocation mapping, thermal label generation (ZPL / PDF), or real-time parcel tracking webhooks across Colombia and Latin America.

---

## Hard Rules & Technical Invariants

1. **Multi-Carrier Strategy Invariant:**
   - Always prioritize dynamic aggregators (MiPaquete / Skydropx) for instant self-serve onboarding, multi-carrier fallback (Coordinadora, Servientrega, Inter Rapidísimo, TCC, Envía), and unified Cash on Delivery (COD) payouts without requiring credit surety bonds (*pólizas de fianza*).
2. **Atomic Stock Locking Invariant:**
   - Orders MUST execute an atomic stock reservation in PostgreSQL/Directus with row-level locks (`FOR UPDATE`) before confirming payment or generating carrier shipping guides.
3. **DANE Divipola 8-Digit Geocoding:**
   - Shipping destination addresses MUST map to official 8-digit DANE Divipola codes (`DPTO` + `MPIO` + `POBLADO`) to prevent carrier dispatch rejections.
4. **Zero-Blindness / F1 Clarification Gate:**
   - Autodiscover logistics credentials (`MIPAQUETE_API_KEY`, `SKYDROPX_TOKEN`, `COORDINADORA_API_KEY`). If unconfigured, halt execution immediately to query for credentials.

---

## References & SSoT Documents

- [`references/usage.md`](file:///var/www/.agents/skills/orders-fulfillment/references/usage.md) — Multi-carrier quote and shipment creation (MiPaquete, Skydropx), COD workflows, DANE city lookup, and thermal label generation.
- [`references/infra.md`](file:///var/www/.agents/skills/orders-fulfillment/references/infra.md) — Zerops deployment topology, Valkey queue workers, environment variables, and third-party console onboarding runbooks.
- [`assets/logistics_unified_provider.ts`](file:///var/www/.agents/skills/orders-fulfillment/assets/logistics_unified_provider.ts) — Unified TypeScript provider with MiPaquete and Skydropx adapters and F1 Clarification Gate.
- [`assets/fulfillment_zod_schemas.ts`](file:///var/www/.agents/skills/orders-fulfillment/assets/fulfillment_zod_schemas.ts) — Strict Zod validation schemas for shipments and carrier webhooks.

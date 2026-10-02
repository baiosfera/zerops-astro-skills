# Email Marketing, React Email 3.0 & Deliverability Engine Manual (v2.0)

`email-marketing` is the sovereign email templating, multi-provider transactional dispatching, anti-SPAM deliverability, and automated marketing sequence engine for the Zerops stack. Under the strict **2026 Deliverability Standards (DMARCbis RFC 9989, DKIM 2048-bit, RFC 8058 One-Click Unsubscribe, Google/Yahoo Spam Rate < 0.10%)** and **$0 SaaS licensing** model, it decouples email dispatching across **Zoho ZeptoMail REST/SMTP**, **Amazon SES v2**, **Resend API**, **Listmonk (Self-Hosted in Zerops)**, and **Generic SMTP**.

---

## 1. 4D Comparative Architectural Matrix: Email Relays & Providers

| Email Provider | Service Type | Integration Protocol | Auth & Limits | Zerops Suitability |
|---|---|---|---|---|
| **Zoho ZeptoMail** | Dedicated Transactional | REST API v1.1 / SMTP 587 | Token `Zoho-enczapikey` / High LatAm reputation | **SSoT Transactional LatAm** |
| **Amazon SES v2** | High Scale Bulk / Trans. | AWS SDK v3 / SMTP | IAM SigV4 / 2048-bit DKIM / $0.10 x 1k | Mass newsletter & notifications |
| **Resend API** | Developer-First | REST HTTPS / SDK | Bearer Token / React Email native | Rapid onboarding & dev testing |
| **Listmonk** | Self-Hosted Newsletters | REST API Go in Zerops | HTTP Basic / Native PostgreSQL | **$0 SaaS for Mass Broadcasts** |
| **Generic SMTP** | Universal Fallback | RFC 5321 SMTP TLS | STARTTLS / Standard Auth | Universal fallback relay |

---

## 2. Deterministic Connection with `brandbook.json` (W3C DTCG SSoT)

All email templates must be dynamically styled using tokens from `brandbook.json` via [`assets/email_brandbook_bridge.ts`](file:///var/www/.agents/skills/email-marketing/assets/email_brandbook_bridge.ts):

```typescript
import { loadEmailBrandTokens } from "../assets/email_brandbook_bridge";

// 1. Load and transpile brand tokens to inline CSS-safe values
const brandbookPath = process.env.BRANDBOOK_PATH || "./brandbook.json";
const brand = loadEmailBrandTokens(brandbookPath);

// Ready-to-use inline styles:
// brand.palette.primary       ➔ Primary brand accent
// brand.palette.background    ➔ Obsidian / dark background
// brand.palette.surface       ➔ Surface container background
// brand.palette.secondary     ➔ Secondary brand accent
// brand.typography.display    ➔ Display heading font stack
// brand.typography.body       ➔ Body text font stack
// brand.monogramSvg           ➔ Vector monogram mark
```

---

## 3. HTML Hygiene & Email Rendering Invariants

### 3.1. Gmail 102 KB Clipping Threshold (< 85 KB Rule)
* **Rule:** Total compiled HTML file size MUST NOT exceed **85 KB**.
* **Hazard:** Emails over 102 KB trigger Gmail's *"[Message clipped] View entire message"*, hiding tracking pixels and footer unsubscribe buttons.
* **Prohibition of Base64:** Never embed images or fonts as Base64 data URIs (`data:image/...` or `data:font/...`) in HTML or `<style>` blocks. Base64 triggers Gmail to strip style tags and penalizes sender reputation.

### 3.2. CSS 100% Inline Compilation
Every visual style (colors, paddings, borders, buttons, backgrounds) MUST compile directly to inline `style="..."` attributes on `<table>`, `<tr>`, `<td>`, `<div>`, `<a>`, and `<button>` elements.

### 3.3. Progressive Enhancement Typography Stack
1. **Logo & Monogram:** Embedded as **pure SVG vectors or 2x Retina PNGs** in the email header.
2. **H1/H2 Display Headings:** `font-family: 'Rising', 'Playfair Display', Georgia, 'Times New Roman', serif;`
3. **Body Text & Buttons:** `font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;`

### 3.4. Bun SSR React Email 3.0 Streaming Quirk
In Bun 1.3+, `react-dom/server` resolves to `server.bun.js` which can emit incomplete HTML shells when `<Tailwind>` compiles asynchronously. To guarantee complete HTML generation:
- Use `await render(element)` directly in server runtime.
- For streaming contexts, ensure `await stream.allReady` completes before passing chunks to email transport.

---

## 4. Language Resguard & Anti-Translation Invariant

To prevent Gmail from displaying unwanted "Translate to Spanish" banners:
1. **HTML Root Attributes:** `<html lang="es" xml:lang="es" translate="no" class="notranslate">`.
2. **Google Meta Tag:** `<meta name="google" content="notranslate" />`.
3. **MIME Header:** `Content-Language: es` across SMTP transport and MIME parts.
4. **Natural Spanish Phrasing:** Avoid mixing English UI technical jargon in the subject line and body copy.

---

## 5. Multi-Provider Strategy Dispatcher with RFC 8058

```typescript
import {
  UnifiedEmailDispatcher,
  ListmonkProvider,
  ZeptoMailRestProvider,
  AwsSesV2Provider,
  ResendProvider,
  UnifiedEmailPayload
} from "../assets/email_dispatcher";

const dispatcher = new UnifiedEmailDispatcher();

// Automatic transactional dispatch resolving credentials from environment
export async function dispatchTransactionalEmail(payload: UnifiedEmailPayload) {
  return await dispatcher.dispatch(payload);
}
```

---

## 6. 2026 Deliverability & Anti-SPAM Compliance Standards

| Metric / Protocol | 2026 Requirement | Non-Compliance Consequence |
|---|---|---|
| **Spam Complaint Rate** | **< 0.10%** in Google Postmaster Tools | Warning at 0.10%, hard block at $\ge 0.30\%$ |
| **RFC 8058 One-Click** | `List-Unsubscribe` + `List-Unsubscribe-Post: List-Unsubscribe=One-Click` (DKIM signed) | Rejection or SPAM foldering in Yahoo/Gmail |
| **DMARCbis (RFC 9989)** | Policy `p=quarantine` or `p=reject` with strict alignment (`adkim=r; aspf=r;`) | Outright delivery rejection |
| **DKIM 2048-bit** | RSA 2048-bit cryptographic key length | SMTP 550 relay rejection |
| **Reverse DNS (PTR)** | Valid FCrDNS resolving between sending IP and FQDN | Perimeter block |

---

## 7. NATS JetStream Event Consumer for Reactive Emails

```typescript
import { connect, JSONCodec } from 'nats';
import { dispatchTransactionalEmail } from '../assets/email_dispatcher';

export async function startEmailEventConsumer() {
  const nc = await connect({ servers: process.env.NATS_URL || 'nats://nats:4222' });
  const jc = JSONCodec();
  const sub = nc.subscribe('events.orders.completed');

  for await (const msg of sub) {
    const order = jc.decode(msg.data) as any;
    await dispatchTransactionalEmail({
      to: [order.customer_email],
      subject: `Order Confirmation #${order.id}`,
      html: `<h1>Thank you for your purchase, ${order.customer_name}!</h1>`,
      tags: { category: 'order_receipt' }
    });
  }
}
```

---

## 8. 5 Production Patterns in Zerops

### Pattern 1: Multi-Provider Transactional Dispatcher with Dynamic Fallbacks
Resolves Listmonk or ZeptoMail for transactional orders and falls back to AWS SES v2 or Resend if primary limits are hit.

### Pattern 2: Throttled Bulk Broadcast Queue with BullMQ in Valkey
Enqueues mass marketing campaigns through `emailDispatchQueue`, enforcing a hard rate limit of `10 emails/sec`.

### Pattern 3: Automated Design Token Transpilation from `brandbook.json`
Reads master brand book tokens dynamically during React Email build phase to ensure 100% visual consistency.

### Pattern 4: RFC 8058 One-Click Unsubscribe Header Signing
Appends compliant `List-Unsubscribe` headers to commercial broadcasts, ensuring DKIM signature covers these headers.

### Pattern 5: NATS JetStream Reactive Email Consumer Worker
Background daemon in `aiworker` listening to `events.orders.completed` and `events.auth.magic_link` for instant asynchronous email delivery.

---

## 9. Anti-Patterns & Common Gotchas

1. **Exceeding 102 KB HTML Size**: Large templates get clipped in Gmail, breaking the unsubscribe link and causing spam complaints. Keep size below 85 KB.
2. **Embedding Base64 Images**: Base64 images trigger spam filters and cause Gmail to strip CSS styles. Always use HTTPS asset URLs.
3. **Missing One-Click Unsubscribe Headers**: Omitting RFC 8058 headers on marketing blasts causes Yahoo and Gmail to penalize sender domain reputation.

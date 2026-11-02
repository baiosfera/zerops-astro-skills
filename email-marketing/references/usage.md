# Email Marketing, React Email 3.0 & Deliverability Engine Manual (v3.0)

`email-marketing` is the sovereign email templating, multi-provider transactional dispatching, anti-SPAM deliverability, and automated marketing sequence engine for the Zerops stack. Under the strict **2026 Deliverability Standards (DMARCbis RFC 9989, DKIM 2048-bit, RFC 8058 One-Click Unsubscribe, Google/Yahoo Spam Rate < 0.10%)** and **$0 SaaS licensing** model, it decouples email dispatching across **Zoho ZeptoMail REST/SMTP**, **Amazon SES v2**, **Resend API**, **Listmonk (Self-Hosted in Zerops)**, and **Generic SMTP**.

---

## 1. 4D Comparative Architectural Matrix: Email Relays & Providers

| Email Provider | Service Type | Integration Protocol | Auth & Limits | Zerops Suitability |
|---|---|---|---|---|
| **Zoho ZeptoMail** | Dedicated Transactional | REST API v1.1 / SMTP 587 | Token `Zoho-enczapikey` / High LatAm reputation | **SSoT Transactional LatAm** |
| **Amazon SES v2** | High Scale Bulk / Trans. | AWS SDK v3 / SigV4 / SMTP | IAM SigV4 / 2048-bit DKIM / $0.10 x 1k | **Mass newsletter & notifications** |
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
// brand.palette.background    ➔ Dark container background
// brand.palette.surface       ➔ Surface container background
// brand.palette.secondary     ➔ Secondary brand accent
// brand.typography.display    ➔ Display heading font stack
// brand.typography.body       ➔ Body text font stack
// brand.monogramSvg           ➔ Pure vector monogram mark
```

---

## 3. HTML Hygiene & Email Rendering Invariants

### 3.1. Gmail 102 KB Clipping Threshold (< 85 KB Rule)
* **Rule:** Total compiled HTML file size MUST NOT exceed **85 KB**.
* **Hazard:** Emails over 102 KB trigger Gmail's *"[Message clipped] View entire message"*, hiding tracking pixels and footer unsubscribe buttons. This causes recipients to click "Report Spam" instead of unsubscribing, immediately threatening domain reputation.
* **Prohibition of Base64:** Never embed images or fonts as Base64 data URIs (`data:image/...` or `data:font/...`) in HTML or `<style>` blocks. Base64 triggers Gmail to strip style tags and penalizes sender reputation.

### 3.2. CSS 100% Inline Compilation
Every visual style (colors, paddings, borders, buttons, backgrounds) MUST compile directly to inline `style="..."` attributes on `<table>`, `<tr>`, `<td>`, `<div>`, `<a>`, and `<button>` elements.

### 3.3. Progressive Enhancement Typography Stack
1. **Logo & Monogram:** Embedded as pure SVG vectors or 2x Retina PNGs hosted on public CDN.
2. **H1/H2 Display Headings:** `font-family: 'Rising', 'Playfair Display', Georgia, 'Times New Roman', serif;`
3. **Body Text & Buttons:** `font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;`

### 3.4. Bun SSR React Email 3.0 Rendering Invariant
In Bun 1.3+, use `await render(element)` directly with minification enabled:
```typescript
import { render } from "@react-email/components";
import React from "react";
import { GenericTransactionalEmail } from "../assets/GenericTransactionalEmail";

export async function renderTemplateToHtml(props: any): Promise<string> {
  const html = await render(React.createElement(GenericTransactionalEmail, props), {
    pretty: false // Minifies output to guarantee total size stays under 85 KB
  });
  
  if (Buffer.byteLength(html, "utf8") > 85000) {
    throw new Error(`[Anti-Clipping Violation] Email HTML size (${Buffer.byteLength(html, "utf8")} bytes) exceeds 85 KB limit.`);
  }
  return html;
}
```

---

## 4. RFC 8058 One-Click Unsubscribe Endpoint Implementation

To satisfy Google and Yahoo mandatory sender requirements, implement the following HTTPS POST handler in Astro 5 or Hono/Elysia:

```typescript
// Astro 5 API Route: src/pages/api/v1/unsubscribe.ts
import type { APIRoute } from "astro";

export const prerender = false;

export const POST: APIRoute = async ({ request }) => {
  const url = new URL(request.url);
  const token = url.searchParams.get("token") || url.searchParams.get("id");
  
  if (!token) {
    return new Response(JSON.stringify({ error: "Missing unsubscribe token" }), {
      status: 400,
      headers: { "Content-Type": "application/json" }
    });
  }

  // RFC 8058 requires reading POST body containing 'List-Unsubscribe=One-Click'
  const contentType = request.headers.get("content-type") || "";
  if (contentType.includes("application/x-www-form-urlencoded")) {
    const rawBody = await request.text();
    if (!rawBody.includes("List-Unsubscribe=One-Click")) {
      return new Response(JSON.stringify({ error: "Invalid RFC 8058 payload" }), { status: 400 });
    }
  }

  // Atomically suppress recipient in database / Listmonk / Directus
  await suppressRecipientByToken(token);

  // Return immediate 200 OK without redirect or authentication challenge
  return new Response(JSON.stringify({ success: true, message: "Unsubscribed successfully" }), {
    status: 200,
    headers: { "Content-Type": "application/json" }
  });
};
```

---

## 5. Google Postmaster Tools & Spam Complaint Rate Mitigation

### 5.1. The 0.10% / 0.30% Thresholds
* **Calculation:** $\frac{\text{Reported Spam Complaints}}{\text{Emails Delivered to Inbox}} \times 100\%$
* **Target:** Maintain strictly **< 0.10%** across rolling 7-day windows.
* **Immediate Circuit Breaker:** If spam complaints reach 0.20%, throttle marketing broadcasts by 50% and execute list hygiene. If rate reaches 0.30%, halt marketing blasts entirely.

### 5.2. Automated Suppression on Hard Bounce / Complaint (SNS Webhook)
Connect Amazon SNS Event Destination to an endpoint:
```typescript
export async function handleSesEvent(eventPayload: any) {
  const { eventType, mail } = eventPayload;
  const recipient = mail.destination[0];

  if (eventType === "Bounce" && eventPayload.bounce?.bounceType === "Permanent") {
    console.warn(`[SES] Hard bounce detected for ${recipient}. Adding to suppression list.`);
    await addEmailToSuppressionList(recipient, "HARD_BOUNCE");
  } else if (eventType === "Complaint") {
    console.error(`[SES] Spam complaint detected for ${recipient}. Immediate suppression.`);
    await addEmailToSuppressionList(recipient, "COMPLAINT");
  }
}
```

---

## 6. Multi-Provider Strategy Dispatcher with Circuit Breaker

```typescript
import {
  UnifiedEmailDispatcher,
  getAutoConfiguredDispatcher,
  UnifiedEmailPayload
} from "../assets/email_dispatcher";

const dispatcher = getAutoConfiguredDispatcher();

export async function dispatchTransactionalEmail(payload: UnifiedEmailPayload) {
  return await dispatcher.send(payload);
}
```

---

## 7. Anti-Patterns & Common Gotchas

1. **Exceeding 102 KB HTML Size**: Large templates get clipped in Gmail, breaking the unsubscribe link and causing recipients to mark as spam. Keep size below 85 KB.
2. **Embedding Base64 Images**: Base64 images trigger spam filters and cause Gmail to strip CSS styles. Always use HTTPS asset URLs.
3. **Missing RFC 8058 Headers**: Omitting RFC 8058 headers on marketing blasts causes Yahoo and Gmail to penalize sender domain reputation.
4. **Missing One-Click POST Receiver**: Having the headers in outgoing email but returning 404 or a login page on the POST endpoint violates RFC 8058 §4.
5. **Ignoring Custom MAIL FROM on SES**: Sending with default `MAIL FROM: ...@amazonses.com` breaks DMARC SPF alignment under `aspf=r`. Always configure `mail.yourdomain.com`.

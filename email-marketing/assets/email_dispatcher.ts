/**
 * @file email_dispatcher.ts
 * @description Motor Unificado de Despacho de Correo Electrónico (Multi-Provider Strategy)
 * con cumplimiento estricto de normas Anti-SPAM y Entregabilidad 2025/2026 (RFC 8058, RFC 9989 DMARCbis,
 * límite de peso HTML < 85 KB, CSS 100% Inline y Resguardo de Idioma con Google notranslate).
 * @version 2.1.0
 */

import { Resend } from "resend";
import { SESv2Client, SendEmailCommand } from "@aws-sdk/client-sesv2";
import nodemailer, { Transporter } from "nodemailer";
import { render, toPlainText } from "@react-email/components";
import React from "react";
import { WelcomeLatAmEmail } from "./WelcomeLatAmEmail";

export interface UnifiedEmailAttachment {
  filename: string;
  content: string | Buffer;
  contentType?: string;
}

export interface UnifiedEmailPayload {
  from?: string;
  to: string[];
  cc?: string[];
  bcc?: string[];
  replyTo?: string;
  subject: string;
  html?: string;
  text?: string;
  language?: string; // Por defecto "es"
  userName?: string;
  discountCode?: string;
  discountValue?: string;
  shopUrl?: string;
  unsubscribeUrl?: string;
  unsubscribeMailto?: string;
  tags?: Record<string, string>;
  attachments?: UnifiedEmailAttachment[];
}

export interface DispatchResult {
  provider: "resend" | "aws-ses" | "zeptomail-rest" | "generic-smtp" | "mock-sandbox";
  messageId: string;
  success: boolean;
  timestamp: string;
}

export interface IEmailProvider {
  name: "resend" | "aws-ses" | "zeptomail-rest" | "generic-smtp" | "mock-sandbox";
  send(payload: UnifiedEmailPayload): Promise<DispatchResult>;
}

/**
 * Validador de Higiene HTML y Límite de Peso Anti-Clipping (Gmail 102 KB Limit)
 */
export function validateEmailPayloadHygiene(html: string, subject: string): void {
  const byteLength = Buffer.byteLength(html, "utf8");
  
  // 1. Alerta de Límite de Peso de Gmail (102 KB)
  if (byteLength > 102400) {
    throw new Error(
      `[EmailHygieneViolation] El tamaño del HTML (${(byteLength / 1024).toFixed(2)} KB) supera el límite crítico de 102 KB de Gmail. ` +
      `Gmail recortará el mensaje ("[Message clipped]"), rompiendo el píxel de tracking y el botón de desuscripción. Reduzca el HTML a < 85 KB.`
    );
  }

  if (byteLength > 87040) {
    console.warn(
      `[EmailHygieneWarning] El HTML pesa ${(byteLength / 1024).toFixed(2)} KB. Se recomienda mantenerlo por debajo de 85 KB para evitar riesgos de recorte con tracking tokens.`
    );
  }

  // 2. Prohibición de Base64 Data URIs (Causa eliminación de CSS y bloqueos)
  if (html.includes("data:image/") || html.includes("data:font/")) {
    throw new Error(
      `[EmailHygieneViolation] Se detectaron URIs en Base64 (data:image/ o data:font/) en el HTML del correo. ` +
      `Gmail y Outlook eliminan bloques <style> que contengan Base64 y bloquean imágenes inline. Todas las imágenes deben alojarse en CDN HTTPS y las tipografías deben usar fallbacks de sistema.`
    );
  }

  // 3. Validación de Longitud de Asunto (Anti-Spam 2026: 30 a 60 caracteres)
  if (subject.length > 70) {
    console.warn(
      `[EmailHygieneWarning] El asunto '${subject}' tiene ${subject.length} caracteres. Los clientes móviles truncan asuntos de más de 55 caracteres y aumenta el riesgo de penalización SPAM.`
    );
  }
}

// 1. Resend API Provider
export class ResendProvider implements IEmailProvider {
  public name = "resend" as const;
  private client: Resend;
  private defaultFrom: string;

  constructor(apiKey: string, defaultFrom: string = "Baiosfera <hola@baiosfera.com>") {
    this.client = new Resend(apiKey);
    this.defaultFrom = defaultFrom;
  }

  async send(payload: UnifiedEmailPayload): Promise<DispatchResult> {
    const html = payload.html || await render(
      React.createElement(WelcomeLatAmEmail, {
        userName: payload.userName || "Amigo",
        discountCode: payload.discountCode || "BIENVENIDO10",
        discountValue: payload.discountValue || "10%",
        shopUrl: payload.shopUrl || "https://mitienda.com",
        unsubscribeUrl: payload.unsubscribeUrl || "https://mitienda.com/api/unsubscribe"
      })
    );
    const text = payload.text || toPlainText(html);

    validateEmailPayloadHygiene(html, payload.subject);

    const headers: Record<string, string> = {
      "Content-Language": payload.language || "es",
    };

    if (payload.unsubscribeUrl || payload.unsubscribeMailto) {
      const unsub = [];
      if (payload.unsubscribeUrl) unsub.push(`<${payload.unsubscribeUrl}>`);
      if (payload.unsubscribeMailto) unsub.push(`<mailto:${payload.unsubscribeMailto}>`);
      headers["List-Unsubscribe"] = unsub.join(", ");
      headers["List-Unsubscribe-Post"] = "List-Unsubscribe=One-Click";
    }

    const { data, error } = await this.client.emails.send({
      from: payload.from || this.defaultFrom,
      to: payload.to,
      cc: payload.cc,
      bcc: payload.bcc,
      reply_to: payload.replyTo,
      subject: payload.subject,
      html,
      text,
      headers,
      attachments: payload.attachments?.map(att => ({
        filename: att.filename,
        content: typeof att.content === "string" ? Buffer.from(att.content, "base64") : att.content,
        content_type: att.contentType
      }))
    });

    if (error || !data) {
      throw new Error(`Resend send failed: ${error?.message || "Unknown error"}`);
    }

    return {
      provider: "resend",
      messageId: data.id,
      success: true,
      timestamp: new Date().toISOString()
    };
  }
}

// 2. AWS SES v2 Provider
export class AwsSesV2Provider implements IEmailProvider {
  public name = "aws-ses" as const;
  private client: SESv2Client;
  private defaultFrom: string;
  private configurationSetName?: string;

  constructor(options: { region?: string; defaultFrom?: string; configurationSetName?: string } = {}) {
    this.client = new SESv2Client({ region: options.region || process.env.AWS_REGION || "us-east-1" });
    this.defaultFrom = options.defaultFrom || process.env.AWS_SES_DEFAULT_FROM || "Baiosfera <hola@baiosfera.com>";
    this.configurationSetName = options.configurationSetName || process.env.AWS_SES_CONFIGURATION_SET;
  }

  async send(payload: UnifiedEmailPayload): Promise<DispatchResult> {
    const html = payload.html || await render(
      React.createElement(WelcomeLatAmEmail, {
        userName: payload.userName || "Amigo",
        discountCode: payload.discountCode || "BIENVENIDO10",
        discountValue: payload.discountValue || "10%",
        shopUrl: payload.shopUrl || "https://mitienda.com",
        unsubscribeUrl: payload.unsubscribeUrl || "https://mitienda.com/api/unsubscribe"
      })
    );
    const text = payload.text || toPlainText(html);

    validateEmailPayloadHygiene(html, payload.subject);

    const headers = [
      { Name: "Content-Language", Value: payload.language || "es" }
    ];

    if (payload.unsubscribeUrl || payload.unsubscribeMailto) {
      const unsub = [];
      if (payload.unsubscribeUrl) unsub.push(`<${payload.unsubscribeUrl}>`);
      if (payload.unsubscribeMailto) unsub.push(`<mailto:${payload.unsubscribeMailto}>`);
      headers.push(
        { Name: "List-Unsubscribe", Value: unsub.join(", ") },
        { Name: "List-Unsubscribe-Post", Value: "List-Unsubscribe=One-Click" }
      );
    }

    const command = new SendEmailCommand({
      FromEmailAddress: payload.from || this.defaultFrom,
      Destination: {
        ToAddresses: payload.to,
        CcAddresses: payload.cc,
        BccAddresses: payload.bcc
      },
      ReplyToAddresses: payload.replyTo ? [payload.replyTo] : undefined,
      ConfigurationSetName: this.configurationSetName,
      Content: {
        Simple: {
          Subject: { Data: payload.subject, Charset: "UTF-8" },
          Body: {
            Html: { Data: html, Charset: "UTF-8" },
            Text: { Data: text, Charset: "UTF-8" }
          },
          Headers: headers
        }
      }
    });

    const response = await this.client.send(command);
    return {
      provider: "aws-ses",
      messageId: response.MessageId || "ses-ok",
      success: true,
      timestamp: new Date().toISOString()
    };
  }
}

// 3. Zoho ZeptoMail REST Provider
export class ZeptoMailRestProvider implements IEmailProvider {
  public name = "zeptomail-rest" as const;
  private apiKey: string;
  private defaultFromAddress: string;
  private defaultFromName: string;
  private bounceAddress?: string;

  constructor(options: {
    apiKey: string;
    defaultFromAddress?: string;
    defaultFromName?: string;
    bounceAddress?: string;
  }) {
    this.apiKey = options.apiKey;
    this.defaultFromAddress = options.defaultFromAddress || process.env.ZEPTOMAIL_DEFAULT_FROM_EMAIL || "hola@baiosfera.com";
    this.defaultFromName = options.defaultFromName || "Baiosfera";
    this.bounceAddress = options.bounceAddress || process.env.ZEPTOMAIL_BOUNCE_ADDRESS;
  }

  async send(payload: UnifiedEmailPayload): Promise<DispatchResult> {
    const html = payload.html || await render(
      React.createElement(WelcomeLatAmEmail, {
        userName: payload.userName || "Amigo",
        discountCode: payload.discountCode || "BIENVENIDO10",
        discountValue: payload.discountValue || "10%",
        shopUrl: payload.shopUrl || "https://mitienda.com",
        unsubscribeUrl: payload.unsubscribeUrl || "https://mitienda.com/api/unsubscribe"
      })
    );
    const text = payload.text || toPlainText(html);

    validateEmailPayloadHygiene(html, payload.subject);

    const mimeHeaders: Record<string, string> = {
      "Content-Language": payload.language || "es"
    };

    if (payload.unsubscribeUrl || payload.unsubscribeMailto) {
      const unsub = [];
      if (payload.unsubscribeUrl) unsub.push(`<${payload.unsubscribeUrl}>`);
      if (payload.unsubscribeMailto) unsub.push(`<mailto:${payload.unsubscribeMailto}>`);
      mimeHeaders["List-Unsubscribe"] = unsub.join(", ");
      mimeHeaders["List-Unsubscribe-Post"] = "List-Unsubscribe=One-Click";
    }

    const authHeader = this.apiKey.startsWith("Zoho-enczapikey ")
      ? this.apiKey
      : `Zoho-enczapikey ${this.apiKey.trim()}`;

    const bodyPayload: any = {
      from: {
        address: this.defaultFromAddress,
        name: this.defaultFromName
      },
      to: payload.to.map(email => ({
        email_address: { address: email, name: email.split("@")[0] }
      })),
      subject: payload.subject,
      htmlbody: html,
      textbody: text,
      track_clicks: true,
      track_opens: true
    };

    if (this.bounceAddress) bodyPayload.bounce_address = this.bounceAddress;
    if (Object.keys(mimeHeaders).length > 0) bodyPayload.mime_headers = mimeHeaders;
    if (payload.replyTo) {
      bodyPayload.reply_to = [{ address: payload.replyTo, name: "Atención" }];
    }
    if (payload.attachments && payload.attachments.length > 0) {
      bodyPayload.attachments = payload.attachments.map(att => ({
        name: att.filename,
        content: typeof att.content === "string" ? att.content : att.content.toString("base64"),
        mime_type: att.contentType || "application/octet-stream"
      }));
    }

    const res = await fetch("https://api.zeptomail.com/v1.1/email", {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": authHeader
      },
      body: JSON.stringify(bodyPayload)
    });

    const resData = await res.json();
    if (!res.ok) {
      throw new Error(`ZeptoMail failed (${res.status}): ${JSON.stringify(resData)}`);
    }

    return {
      provider: "zeptomail-rest",
      messageId: resData?.data?.[0]?.message_id || resData?.request_id || "zeptomail-sent",
      success: true,
      timestamp: new Date().toISOString()
    };
  }
}

// 4. Generic SMTP Provider (Nodemailer)
export class GenericSmtpProvider implements IEmailProvider {
  public name = "generic-smtp" as const;
  private transporter: Transporter;
  private defaultFrom: string;

  constructor(options: {
    host: string;
    port: number;
    secure?: boolean;
    user: string;
    pass: string;
    defaultFrom: string;
  }) {
    this.defaultFrom = options.defaultFrom;
    this.transporter = nodemailer.createTransport({
      host: options.host,
      port: options.port,
      secure: options.secure ?? (options.port === 465),
      auth: {
        user: options.user,
        pass: options.pass
      }
    });
  }

  async send(payload: UnifiedEmailPayload): Promise<DispatchResult> {
    const html = payload.html || await render(
      React.createElement(WelcomeLatAmEmail, {
        userName: payload.userName || "Amigo",
        discountCode: payload.discountCode || "BIENVENIDO10",
        discountValue: payload.discountValue || "10%",
        shopUrl: payload.shopUrl || "https://mitienda.com",
        unsubscribeUrl: payload.unsubscribeUrl || "https://mitienda.com/api/unsubscribe"
      })
    );
    const text = payload.text || toPlainText(html);

    validateEmailPayloadHygiene(html, payload.subject);

    const headers: Record<string, string> = {
      "Content-Language": payload.language || "es"
    };

    if (payload.unsubscribeUrl || payload.unsubscribeMailto) {
      const unsub = [];
      if (payload.unsubscribeUrl) unsub.push(`<${payload.unsubscribeUrl}>`);
      if (payload.unsubscribeMailto) unsub.push(`<mailto:${payload.unsubscribeMailto}>`);
      headers["List-Unsubscribe"] = unsub.join(", ");
      headers["List-Unsubscribe-Post"] = "List-Unsubscribe=One-Click";
    }

    const info = await this.transporter.sendMail({
      from: payload.from || this.defaultFrom,
      to: payload.to.join(", "),
      cc: payload.cc?.join(", "),
      bcc: payload.bcc?.join(", "),
      replyTo: payload.replyTo,
      subject: payload.subject,
      html,
      text,
      headers,
      attachments: payload.attachments?.map(att => ({
        filename: att.filename,
        content: att.content,
        contentType: att.contentType
      }))
    });

    return {
      provider: "generic-smtp",
      messageId: info.messageId,
      success: true,
      timestamp: new Date().toISOString()
    };
  }
}

// 5. Mock Sandbox Provider (For explicit demo / sandbox execution only)
export class MockSandboxProvider implements IEmailProvider {
  public name = "mock-sandbox" as const;

  async send(payload: UnifiedEmailPayload): Promise<DispatchResult> {
    const msgId = `mock_${Math.random().toString(36).substring(2, 12)}`;
    console.warn(`[MOCK SANDBOX ACTIVE] Simulating email delivery to: ${payload.to.join(", ")} | Subject: ${payload.subject} | ID: ${msgId}`);
    return {
      provider: "mock-sandbox",
      messageId: msgId,
      success: true,
      timestamp: new Date().toISOString()
    };
  }
}

// Factory resolver: Automatically picks provider from environment or throws F1 Clarification Gate error
export function getAutoConfiguredDispatcher(): IEmailProvider {
  if (process.env.ZEPTOMAIL_SEND_MAIL_TOKEN && process.env.ZEPTOMAIL_SEND_MAIL_TOKEN.trim() !== "") {
    return new ZeptoMailRestProvider({ apiKey: process.env.ZEPTOMAIL_SEND_MAIL_TOKEN });
  }

  if (process.env.AWS_ACCESS_KEY_ID && process.env.AWS_SECRET_ACCESS_KEY) {
    return new AwsSesV2Provider();
  }

  if (process.env.RESEND_API_KEY && process.env.RESEND_API_KEY.trim() !== "") {
    return new ResendProvider(process.env.RESEND_API_KEY);
  }

  if (process.env.SMTP_HOST && process.env.SMTP_USER && process.env.SMTP_PASSWORD) {
    return new GenericSmtpProvider({
      host: process.env.SMTP_HOST,
      port: parseInt(process.env.SMTP_PORT || "587", 10),
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASSWORD,
      defaultFrom: process.env.SMTP_DEFAULT_FROM || "Baiosfera <hola@baiosfera.com>"
    });
  }

  if (process.env.ALLOW_MOCK_DISPATCH === "true") {
    return new MockSandboxProvider();
  }

  throw new Error(
    `[F1 CLARIFICATION GATE - email-marketing]\n` +
    `No active email credentials detected in zerops_env / process.env.\n` +
    `Supported providers:\n` +
    `• Zoho ZeptoMail: ZEPTOMAIL_SEND_MAIL_TOKEN\n` +
    `• AWS SES v2: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION\n` +
    `• Resend: RESEND_API_KEY\n` +
    `• Generic SMTP: SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD\n\n` +
    `Action required: Configure variables in Zerops or provide credentials in the prompt.`
  );
}

// Backward-compatible export
export async function sendResendEmail(params: UnifiedEmailPayload) {
  const dispatcher = getAutoConfiguredDispatcher();
  return await dispatcher.send(params);
}

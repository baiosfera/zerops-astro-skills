export class WhatsAppCloudClient {
  private baseUrl = "https://graph.facebook.com/v21.0";

  constructor(
    private phoneNumberId: string,
    private accessToken: string
  ) {}

  private async post(payload: unknown): Promise<{ messageId: string }> {
    const res = await fetch(`${this.baseUrl}/${this.phoneNumberId}/messages`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${this.accessToken}`
      },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const err = await res.text();
      throw new Error(`[WhatsApp Cloud API Error] HTTP ${res.status}: ${err}`);
    }

    const json = (await res.json()) as { messages: [{ id: string }] };
    return { messageId: json.messages[0].id };
  }

  async sendText(to: string, text: string) {
    return this.post({
      messaging_product: "whatsapp",
      recipient_type: "individual",
      to,
      type: "text",
      text: { body: text }
    });
  }

  async sendInteractiveButtons(to: string, bodyText: string, buttons: Array<{ id: string; title: string }>) {
    return this.post({
      messaging_product: "whatsapp",
      recipient_type: "individual",
      to,
      type: "interactive",
      interactive: {
        type: "button",
        body: { text: bodyText },
        action: {
          buttons: buttons.map((b) => ({ type: "reply", reply: { id: b.id, title: b.title } }))
        }
      }
    });
  }
}

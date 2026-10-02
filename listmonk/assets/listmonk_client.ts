/**
 * Listmonk API Client (v2.0)
 * Sovereign TypeScript SDK for Listmonk v6.2.0 REST API in Zerops.
 * Supports bot token headers (Authorization: token ...), transactional emails,
 * and granular subscriber mutations over internal Zerops DNS.
 */

export interface ListmonkClientConfig {
  baseUrl?: string; // Defaults to process.env.LISTMONK_URL or "http://listmonk:9000"
  apiToken?: string; // Preferred bot token: Authorization: token <token>
  username?: string; // Fallback HTTP Basic Auth username
  password?: string; // Fallback HTTP Basic Auth password
  timeoutMs?: number;
}

export interface TransactionalEmailRequest {
  subscriber_email?: string;
  subscriber_id?: number;
  subscriber_emails?: string[];
  subscriber_mode?: "default" | "fallback" | "external";
  template_id: number;
  from_email?: string;
  subject?: string;
  data?: Record<string, any>;
  headers?: Array<Record<string, string>>;
  content_type?: "html" | "markdown" | "plain";
  altbody?: string; // Plaintext representation for multipart MIME
}

export interface SubscriberPayload {
  email: string;
  name?: string;
  status?: "enabled" | "disabled" | "blocklisted";
  lists?: number[];
  attribs?: Record<string, any>;
  preconfirm_subscriptions?: boolean;
}

export interface ListmonkApiResponse<T = any> {
  data: T;
  message?: string;
}

export class ListmonkClient {
  private baseUrl: string;
  private authHeader: string;
  private timeoutMs: number;

  constructor(config: ListmonkClientConfig = {}) {
    this.baseUrl = (config.baseUrl || process.env.LISTMONK_URL || "http://listmonk:9000").replace(/\/$/, "");
    this.timeoutMs = config.timeoutMs || 10000;

    const token = config.apiToken || process.env.LISTMONK_API_TOKEN;
    if (token) {
      this.authHeader = `token ${token}`;
    } else {
      const user = config.username || process.env.LISTMONK_USER || "admin";
      const pass = config.password || process.env.LISTMONK_PASSWORD || "admin";
      const encoded = Buffer.from(`${user}:${pass}`).toString("base64");
      this.authHeader = `Basic ${encoded}`;
    }
  }

  private async request<T>(path: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${path}`;
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      "Authorization": this.authHeader,
      ...((options.headers as Record<string, string>) || {})
    };

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), this.timeoutMs);

    try {
      const res = await fetch(url, {
        ...options,
        headers,
        signal: controller.signal
      });

      if (!res.ok) {
        const errorBody = await res.text().catch(() => "");
        throw new Error(`[listmonk] HTTP ${res.status} on ${options.method || "GET"} ${path}: ${errorBody}`);
      }

      return (await res.json()) as T;
    } finally {
      clearTimeout(timeout);
    }
  }

  /**
   * Dispatches high-throughput transactional emails via POST /api/tx
   */
  async sendTransactional(payload: TransactionalEmailRequest): Promise<ListmonkApiResponse<boolean>> {
    return this.request<ListmonkApiResponse<boolean>>("/api/tx", {
      method: "POST",
      body: JSON.stringify({
        subscriber_mode: payload.subscriber_mode || "external",
        ...payload
      })
    });
  }

  /**
   * Creates a new subscriber or updates lists
   */
  async createSubscriber(payload: SubscriberPayload): Promise<ListmonkApiResponse<any>> {
    return this.request<ListmonkApiResponse<any>>("/api/subscribers", {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }

  /**
   * Partially updates an existing subscriber's profile or attributes (v6.1+)
   */
  async patchSubscriber(id: number, patch: Partial<SubscriberPayload>): Promise<ListmonkApiResponse<any>> {
    return this.request<ListmonkApiResponse<any>>(`/api/subscribers/${id}`, {
      method: "PATCH",
      body: JSON.stringify(patch)
    });
  }

  /**
   * Queries subscribers with arbitrary SQL expressions
   */
  async querySubscribers(query: string, page = 1, perPage = 50): Promise<ListmonkApiResponse<any>> {
    const params = new URLSearchParams({
      query,
      page: page.toString(),
      per_page: perPage.toString()
    });
    return this.request<ListmonkApiResponse<any>>(`/api/subscribers?${params.toString()}`);
  }

  /**
   * Health check asserting container responsiveness
   */
  async health(): Promise<boolean> {
    try {
      const res = await this.request<any>("/api/config");
      return !!res.data;
    } catch {
      return false;
    }
  }
}

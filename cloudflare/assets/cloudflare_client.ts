import { z } from "zod";
import {
  CloudflareApiResponseSchema,
  CloudflareDnsRecordInput,
  CloudflareDnsRecordInputSchema,
  CloudflareDnsRecord,
  CloudflareDnsRecordSchema,
} from "./dns_zod_schemas";

export interface CloudflareClientConfig {
  apiToken: string;
  zoneId?: string;
}

export interface DnsSyncSummary {
  created: number;
  updated: number;
  untouched: number;
}

export class CloudflareV4Client {
  private readonly baseUrl = "https://api.cloudflare.com/client/v4";
  private readonly headers: Record<string, string>;

  constructor(private readonly config: CloudflareClientConfig) {
    if (!config.apiToken) {
      throw new Error(
        `[F1 CLARIFICATION GATE - cloudflare]\n` +
        `CLOUDFLARE_API_TOKEN is missing in environment.\n` +
        `Please configure CLOUDFLARE_API_TOKEN in Zerops environment.`
      );
    }
    this.headers = {
      Authorization: `Bearer ${config.apiToken}`,
      "Content-Type": "application/json",
    };
  }

  private async request<TSchema extends z.ZodTypeAny>(
    endpoint: string,
    options: RequestInit = {},
    schema: TSchema
  ): Promise<z.infer<TSchema>> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      ...options,
      headers: {
        ...this.headers,
        ...options.headers,
      },
    });

    const data = await response.json();
    const wrapped = CloudflareApiResponseSchema(schema).safeParse(data);

    if (!wrapped.success || !wrapped.data.success) {
      const errorMsg = wrapped.success
        ? wrapped.data.errors.map((e) => `[${e.code}] ${e.message}`).join(", ")
        : JSON.stringify(wrapped.error.format());
      throw new Error(`Cloudflare API Error (${response.status} on ${endpoint}): ${errorMsg}`);
    }

    return wrapped.data.result;
  }

  /** Resolves Zone ID for a domain name */
  async getZoneId(domain: string): Promise<string> {
    if (this.config.zoneId) return this.config.zoneId;

    const schema = z.array(z.object({ id: z.string(), name: z.string() }));
    const result = await this.request(`/zones?name=${encodeURIComponent(domain)}`, {}, schema);

    if (!result || result.length === 0) {
      throw new Error(`Zone for domain '${domain}' not found in Cloudflare account.`);
    }
    return result[0].id;
  }

  /** Lists all DNS records for a zone */
  async listDnsRecords(zoneId: string): Promise<CloudflareDnsRecord[]> {
    return this.request(
      `/zones/${zoneId}/dns_records?per_page=100`,
      { method: "GET" },
      z.array(CloudflareDnsRecordSchema)
    );
  }

  /** Creates a DNS record */
  async createDnsRecord(zoneId: string, record: CloudflareDnsRecordInput): Promise<CloudflareDnsRecord> {
    return this.request(
      `/zones/${zoneId}/dns_records`,
      {
        method: "POST",
        body: JSON.stringify(record),
      },
      CloudflareDnsRecordSchema
    );
  }

  /** Updates an existing DNS record */
  async updateDnsRecord(
    zoneId: string,
    recordId: string,
    record: Partial<CloudflareDnsRecordInput>
  ): Promise<CloudflareDnsRecord> {
    return this.request(
      `/zones/${zoneId}/dns_records/${recordId}`,
      {
        method: "PATCH",
        body: JSON.stringify(record),
      },
      CloudflareDnsRecordSchema
    );
  }

  /** Deletes a DNS record by ID */
  async deleteDnsRecord(zoneId: string, recordId: string): Promise<{ id: string }> {
    return this.request(
      `/zones/${zoneId}/dns_records/${recordId}`,
      { method: "DELETE" },
      z.object({ id: z.string() })
    );
  }

  /** Idempotently synchronizes a single DNS record */
  async syncDnsRecord(zoneId: string, desired: CloudflareDnsRecordInput): Promise<CloudflareDnsRecord> {
    const existingRecords = await this.listDnsRecords(zoneId);
    const existing = existingRecords.find(
      (r) => r.type === desired.type && (r.name === desired.name || r.name.startsWith(`${desired.name}.`))
    );

    if (!existing) {
      console.log(`[Cloudflare DNS] Creating [${desired.type}] ${desired.name} -> ${desired.content}`);
      return this.createDnsRecord(zoneId, desired);
    }

    const needsUpdate =
      existing.content !== desired.content ||
      existing.proxied !== desired.proxied ||
      (desired.ttl && existing.ttl !== desired.ttl) ||
      (desired.priority !== undefined && existing.priority !== desired.priority);

    if (needsUpdate) {
      console.log(`[Cloudflare DNS] Updating [${desired.type}] ${desired.name} -> ${desired.content} (Proxy: ${desired.proxied})`);
      return this.updateDnsRecord(zoneId, existing.id, desired);
    }

    console.log(`[Cloudflare DNS] In Sync [${desired.type}] ${desired.name}`);
    return existing;
  }

  /** Synchronizes a collection of desired DNS records */
  async syncDnsRecords(
    zoneId: string,
    desiredList: CloudflareDnsRecordInput[],
    baseDomain: string
  ): Promise<DnsSyncSummary> {
    const existingRecords = await this.listDnsRecords(zoneId);
    let created = 0;
    let updated = 0;
    let untouched = 0;

    for (const desired of desiredList) {
      const matchName = desired.name === "@" ? baseDomain : (desired.name.includes(".") ? desired.name : `${desired.name}.${baseDomain}`);
      const existing = existingRecords.find(
        (r) => r.type === desired.type && (r.name === matchName || r.name === desired.name)
      );

      if (!existing) {
        await this.createDnsRecord(zoneId, desired);
        created++;
      } else {
        const needsUpdate =
          existing.content !== desired.content ||
          existing.proxied !== desired.proxied ||
          (desired.ttl && existing.ttl !== desired.ttl) ||
          (desired.priority !== undefined && existing.priority !== desired.priority);

        if (needsUpdate) {
          await this.updateDnsRecord(zoneId, existing.id, desired);
          updated++;
        } else {
          untouched++;
        }
      }
    }

    return { created, updated, untouched };
  }

  /** Enforces Full (Strict) SSL/TLS encryption */
  async setSslMode(zoneId: string, mode: "strict" | "full" | "off" = "strict"): Promise<void> {
    const schema = z.object({ id: z.string(), value: z.string() });
    await this.request(
      `/zones/${zoneId}/settings/ssl`,
      {
        method: "PATCH",
        body: JSON.stringify({ value: mode }),
      },
      schema
    );
  }

  async setSslModeStrict(zoneId: string): Promise<void> {
    return this.setSslMode(zoneId, "strict");
  }

  /** Enforces Always Use HTTPS redirect */
  async setAlwaysUseHttps(zoneId: string, enabled = true): Promise<void> {
    const schema = z.object({ id: z.string(), value: z.string() });
    await this.request(
      `/zones/${zoneId}/settings/always_use_https`,
      {
        method: "PATCH",
        body: JSON.stringify({ value: enabled ? "on" : "off" }),
      },
      schema
    );
  }

  async enableAlwaysUseHttps(zoneId: string): Promise<void> {
    return this.setAlwaysUseHttps(zoneId, true);
  }

  /** Purges Cloudflare Edge Cache */
  async purgeCache(zoneId: string, options: { purge_everything?: boolean; files?: string[] }): Promise<{ id: string }> {
    return this.request(
      `/zones/${zoneId}/purge_cache`,
      {
        method: "POST",
        body: JSON.stringify(options),
      },
      z.object({ id: z.string() })
    );
  }
}

export function getAutoConfiguredCloudflareClient(): CloudflareV4Client {
  const apiToken = process.env.CLOUDFLARE_API_TOKEN || "";
  const zoneId = process.env.CLOUDFLARE_ZONE_ID;
  return new CloudflareV4Client({ apiToken, zoneId });
}

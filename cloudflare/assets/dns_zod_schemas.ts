import { z } from "zod";

export const DnsRecordTypeSchema = z.enum([
  "A",
  "AAAA",
  "CNAME",
  "TXT",
  "MX",
  "NS",
  "SRV",
  "CAA",
]);
export type DnsRecordType = z.infer<typeof DnsRecordTypeSchema>;

export const CloudflareDnsRecordInputSchema = z.object({
  type: DnsRecordTypeSchema,
  name: z.string().min(1).describe("Record name or FQDN (e.g. api, @, _dmarc)"),
  content: z.string().min(1).describe("Record value (IP address, target FQDN, or TXT content)"),
  ttl: z.number().int().min(1).max(86400).default(1).describe("1 = Automatic TTL"),
  proxied: z.boolean().default(false).describe("Cloudflare proxy status"),
  priority: z.number().int().optional().describe("Required for MX and SRV records"),
  comment: z.string().optional().describe("Operational description"),
});
export type CloudflareDnsRecordInput = z.infer<typeof CloudflareDnsRecordInputSchema>;

export const CloudflareDnsRecordSchema = CloudflareDnsRecordInputSchema.extend({
  id: z.string().min(1),
  zone_id: z.string().min(1),
  zone_name: z.string(),
  created_on: z.string(),
  modified_on: z.string(),
});
export type CloudflareDnsRecord = z.infer<typeof CloudflareDnsRecordSchema>;

export const CloudflareApiResponseSchema = <T extends z.ZodTypeAny>(resultSchema: T) =>
  z.object({
    success: z.boolean(),
    errors: z.array(z.object({ code: z.number(), message: z.string() })),
    messages: z.array(z.string()),
    result: resultSchema,
  });

/**
 * RFC 9989 DMARCbis Schema (Obsoleting RFC 7489)
 * Note: 'pct' tag is obsoleted in RFC 9989 and intentionally omitted.
 */
export const DmarcRecordRfc9989Schema = z.object({
  v: z.literal("DMARC1"),
  p: z.enum(["none", "quarantine", "reject"]),
  sp: z.enum(["none", "quarantine", "reject"]).optional(),
  np: z.enum(["none", "quarantine", "reject"]).optional().describe("Non-existent subdomain policy (RFC 9989)"),
  t: z.enum(["y", "n"]).optional().describe("Testing mode indicator (RFC 9989)"),
  rua: z.string().url().or(z.string().regex(/^mailto:/)).optional(),
  ruf: z.string().url().or(z.string().regex(/^mailto:/)).optional(),
  adkim: z.enum(["r", "s"]).default("r"),
  aspf: z.enum(["r", "s"]).default("r"),
  fo: z.enum(["0", "1", "d", "s"]).default("0"),
  ri: z.number().int().min(3600).default(86400),
});
export type DmarcRecordRfc9989 = z.infer<typeof DmarcRecordRfc9989Schema>;

export const TurnstileVerifyResponseSchema = z.object({
  success: z.boolean(),
  "error-codes": z.array(z.string()).default([]),
  challenge_ts: z.string().optional(),
  hostname: z.string().optional(),
  action: z.string().optional(),
  cdata: z.string().optional(),
  metadata: z.record(z.unknown()).optional(),
});
export type TurnstileVerifyResponse = z.infer<typeof TurnstileVerifyResponseSchema>;

export const DesiredDnsTopologySchema = z.object({
  baseDomain: z.string().min(1),
  zoneId: z.string().optional(),
  sslMode: z.enum(["strict", "full", "off"]).default("strict"),
  alwaysUseHttps: z.boolean().default(true),
  records: z.array(CloudflareDnsRecordInputSchema),
});
export type DesiredDnsTopology = z.infer<typeof DesiredDnsTopologySchema>;

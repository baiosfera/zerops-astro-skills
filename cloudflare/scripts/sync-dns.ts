#!/usr/bin/env bun
import { getAutoConfiguredCloudflareClient } from "../assets/cloudflare_client";
import { CloudflareDnsRecordInput } from "../assets/dns_zod_schemas";

async function main() {
  console.log("============================================================");
  console.log("  🌐 Cloudflare & Zerops DNS Declarative Synchronizer (v1.0)");
  console.log("============================================================");

  const baseDomain = process.env.CLOUDFLARE_BASE_DOMAIN;
  if (!baseDomain) {
    console.error("❌ Error: CLOUDFLARE_BASE_DOMAIN is not set in environment.");
    process.exit(1);
  }

  const client = getAutoConfiguredCloudflareClient();
  const zoneId = await client.getZoneId(baseDomain);
  console.log(`• Connected to Zone: ${baseDomain} (Zone ID: ${zoneId})`);

  // Target Zerops Ingress / Subdomains from environment or defaults
  const astroTarget = process.env.ASTRO_SUBDOMAIN || process.env.ZEROPS_SUBDOMAIN || `@`;
  const directusTarget = process.env.DIRECTUS_SUBDOMAIN || `api`;
  const evolutionTarget = process.env.EVOLUTION_SUBDOMAIN || `wa`;
  const sgtmTarget = process.env.SGTM_SUBDOMAIN || `sgtm`;

  // Zerops Dedicated IPv4 if configured
  const dedicatedIpv4 = process.env.ZEROPS_DEDICATED_IPV4;
  const dedicatedIpv6 = process.env.ZEROPS_DEDICATED_IPV6;

  const desiredRecords: CloudflareDnsRecordInput[] = [];

  // 1. Frontend Apex & WWW
  if (dedicatedIpv4) {
    desiredRecords.push({
      type: "A",
      name: "@",
      content: dedicatedIpv4,
      proxied: true,
      comment: "Astro Frontend Apex - Zerops Dedicated IPv4",
    });
  }
  if (dedicatedIpv6) {
    desiredRecords.push({
      type: "AAAA",
      name: "@",
      content: dedicatedIpv6,
      proxied: true,
      comment: "Astro Frontend Apex - Zerops Dedicated IPv6",
    });
  }

  desiredRecords.push({
    type: "CNAME",
    name: "www",
    content: baseDomain,
    proxied: true,
    comment: "Astro Frontend WWW Canonical Alias",
  });

  // 2. Directus CMS API
  if (process.env.DIRECTUS_SUBDOMAIN) {
    desiredRecords.push({
      type: "CNAME",
      name: "api",
      content: process.env.DIRECTUS_SUBDOMAIN,
      proxied: true,
      comment: "Directus Headless CMS API - Zerops Routing",
    });
  }

  // 3. Evolution API / WhatsApp Gateway
  if (process.env.EVOLUTION_SUBDOMAIN) {
    desiredRecords.push({
      type: "CNAME",
      name: "wa",
      content: process.env.EVOLUTION_SUBDOMAIN,
      proxied: true,
      comment: "Evolution API Sovereign WhatsApp Gateway",
    });
  }

  // 4. Server-Side GTM (sGTM)
  if (process.env.SGTM_SUBDOMAIN) {
    desiredRecords.push({
      type: "CNAME",
      name: "sgtm",
      content: process.env.SGTM_SUBDOMAIN,
      proxied: true,
      comment: "Server-Side Google Tag Manager Tracking",
    });
  }

  // 5. Email Deliverability Authentication (SPF, DKIM, DMARCbis)
  desiredRecords.push({
    type: "TXT",
    name: "@",
    content: "v=spf1 include:zeptomail.net include:amazonses.com ~all",
    proxied: false,
    comment: "Unified SPF Policy for ZeptoMail and Amazon SES v2",
  });

  desiredRecords.push({
    type: "TXT",
    name: "_dmarc",
    content: `v=DMARC1; p=quarantine; pct=100; rua=mailto:dmarc-reports@${baseDomain}; sp=quarantine`,
    proxied: false,
    comment: "DMARCbis RFC 9989 Policy with Quarantine Enforcement",
  });

  console.log(`• Synchronizing ${desiredRecords.length} desired DNS records...`);
  const result = await client.syncDnsRecords(zoneId, desiredRecords, baseDomain);

  console.log(`  ✅ Created: ${result.created}`);
  console.log(`  ✅ Updated: ${result.updated}`);
  console.log(`  ✅ Untouched (in-sync): ${result.untouched}`);

  // Enforce SSL Full Strict mode and Always Use HTTPS
  console.log("• Enforcing Cloudflare SSL/TLS Full Strict mode & Always Use HTTPS...");
  await client.setSslModeStrict(zoneId);
  await client.enableAlwaysUseHttps(zoneId);
  console.log("  ✅ SSL/TLS configured to Full (strict)");

  console.log("============================================================");
  console.log("  🎉 DNS & Edge CDN Synchronization Completed Successfully");
  console.log("============================================================");
}

main().catch((err) => {
  console.error("❌ Fatal Error:", err.message);
  process.exit(1);
});

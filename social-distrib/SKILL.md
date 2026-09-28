---
name: social-distrib
description: "Trigger: social-distrib, instagram graph api, tiktok content posting, linkedin posts api, x twitter api v2, bullmq social, peak hours scheduling, social media auto posting. Architect, schedule, and automate multi-platform social media distribution across Instagram (Reels & Carousels), TikTok, LinkedIn (PDF Carousels), and X with LatAm GMT-5 peak timing optimization and BullMQ rate limiting on Valkey 7.2 and Directus 11+."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.1"
---

# Social Distribution — Multi-Platform Auto-Publishing Engine (v1.1.0)

## Activation Contract
Activate whenever developing, automating, or operating technical publishing pipelines across social networks (**Instagram Graph API**, **TikTok Content Posting API**, **LinkedIn API**, **X API v2**), queue scheduling with BullMQ on Valkey 7.2, GMT-5 LatAm peak posting optimization, or rate-limit throttling.

---

## Hard Rules & Technical Invariants

1. **Rate Limit & Backoff Invariant:**
   - Every social API invocation MUST pass through BullMQ workers with exponential backoff and jitter to comply strictly with platform rate limits.
2. **Media Pre-Validation Invariant:**
   - Video aspect ratios (9:16 for Reels/TikTok), image dimensions (1:1 / 4:5 for IG), and container formats (MP4 H.264 / AAC) MUST be validated before queuing publishing jobs.
3. **Decoupled Architecture Boundary:**
   - `social-distrib` handles technical dispatch, OAuth token refresh, and scheduling only. Copy and creative assets are provided by upstream skills.

---

## References & SSoT Documents

- [`references/usage.md`](file:///var/www/.agents/skills/social-distrib/references/usage.md) — API client implementation, OAuth2 token management, and webhook verification.
- [`references/infra.md`](file:///var/www/.agents/skills/social-distrib/references/infra.md) — Valkey BullMQ queue topology, SeaweedFS media mounts, and environment configuration.
- [`assets/social_publishers_client.ts`](file:///var/www/.agents/skills/social-distrib/assets/social_publishers_client.ts) — TypeScript API clients for Meta Graph, TikTok, LinkedIn, and X.
- [`assets/social_bullmq_workers.ts`](file:///var/www/.agents/skills/social-distrib/assets/social_bullmq_workers.ts) — Background workers handling scheduled dispatches.

---
name: video-worker
description: "Trigger: video-worker, render video, html to video, motion graphics, video queue, bullmq video, nats video, ephemeral worker zerops, remotion, timesnap, playwright video. Sovereign Ephemeral Video Rendering Worker & Queue Engine in Zerops."
license: MIT
metadata:
  author: "gentleman-programming"
  version: "2.1"
---

# `video-worker` — Sovereign Ephemeral Video Rendering Engine (v2.1)

## Activation Contract
Rendering decoupled, asynchronous, ephemeral video on Zerops under Fractal CoHaLo v8.4. Processes HTML/CSS/Canvas templates and FFmpeg cinematic composition via Valkey 7.2 (BullMQ) or NATS 2.12 JetStream queues.

## Core Directives & Invariants
- **Ephemeral Lifecycle & Zero Cost**: The `videoworker` service (`ubuntu/nodejs@22`) is provisioned on-demand via `recipes/steps/08-video-worker.yaml`. Once MP4 exports are uploaded to persistent Object Storage, destroy the service with `zerops_delete` or `zcli service delete videoworker` to maintain zero idle costs.
- **Deterministic Virtual Clock**: Control time progression explicitly (`timesnap`, intercepted `requestAnimationFrame`, or GSAP `timeline.seek(t)`). Never record real-time CSS `@keyframes` on CPU containers; missing hardware acceleration freezes frames.
- **Direct Memory Pipes to FFmpeg**: Stream capture buffers directly to FFmpeg `stdin` (`image2pipe`, `yuv420p`, `libx264`). Never write sequences of thousands of PNG files to disk, which exhausts container I/O.
- **Mobile Safe Areas (65% Central)**: Vertical renders (9:16, 1080x1920) must confine typography, badges, and logos within the central 65% safe area to prevent mobile viewport clipping. Always generate dual formats: 9:16 (mobile) and 16:9 (desktop).
- **Brand Agnosticism & Font Declarations**: Inject OpenType stylistic sets (`ss01`–`ss05`) and PUA glyphs from brand `.otf`/`.ttf` fonts via environment variables.
- **Conversion Decoupling**: Video serves exclusively as visual atmosphere and B-roll. All interactive CTAs must reside in the native web DOM (`<button>`, `<a>`).

## Decision Gates & References
- **Queue Pipeline & Memory Pipes**: [`usage.md`](file:///var/www/zerops-astro-skills/video-worker/references/usage.md) — FFmpeg memory pipes, virtual clock determinism, and anti-patterns.
- **Ephemeral Topology & Zero-Cost Purge**: [`infra.md`](file:///var/www/zerops-astro-skills/video-worker/references/infra.md) — Provisioning recipes, resource quotas, and deletion protocols.

## Output Contract
High-resolution MP4 video (H.264/AAC, yuv420p, +faststart), validated safe areas, and immediate teardown of ephemeral worker resources.

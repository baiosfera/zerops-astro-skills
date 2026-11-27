---
name: astro-web
description: "Trigger: astro-web, astro 5, astro ssr, server islands, content layer, astro actions, craft anti-slop, brandbook tokens. Astro 5 SSR on Bun with Decoupled Lego Backend & Brandbook Tokens in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "3.3"
---

# Astro 5 — High-Performance SSR & Disruptive Vibecoding Craft (v3.3)

## Activation Contract
Activate when architecting or optimizing Astro 5 SSR on Zerops: Server Islands (`server:defer`), Astro Actions, Content Layer API, `DESIGN.md` & `brandbook.json` tokens, Anti-Slop Craft Gates, GSAP/Lenis 60fps motion, or decoupled backends (`nats`, `valkey`, `postgresql`, `objectstorage`).

## Hard Rules & Positive Guidance
- **Host, Ports & Keys**: Bind `HOST: "0.0.0.0"` and `PORT: "4321"` (or service port). Prefix public vars `PUBLIC_`, isolate server secrets via `astro:env/server`, and share identical `ASTRO_KEY` across rolling replicas.
- **Runtime & Base Selection**: Run SSR on `ubuntu/bun@1.4` (`bun@1.3.9+` glibc parity); deploy `[.]` on ZCP containers and inject `NODE_OPTIONS="--max-old-space-size=1024"` in build envs when bundling React islands + variable fonts.
- **Craft Floor (`PB19` + `DESIGN.md` Before UI Code)**: Read `19_web_design_systems_craft_and_vibecoding.md`, `{ws_dir}/brand/DESIGN.md`, `design-taste-frontend`, and `impeccable/reference/craft-floor.md` before writing components. Keep each brand's own visual world without cloning reference URLs or falling into uniform cards, gradient text, uppercase hero eyebrows, or arbitrary `0px` corners.
- **Verified Self-Hosted Fonts Only**: Load real `@fontsource-variable/*` packages from `web_ready_bridge.fontsource_packages` (or physically present `public/fonts/*.woff2`) with CLS-0 fallback overrides; exclude overused AI faces (`Inter`, `Fraunces`, `Instrument Serif`, `Plus Jakarta Sans`, `Space Grotesk`, `DM Sans`, `Outfit`, `Syne`).
- **Hero Punch & Above-the-Fold Proof**: Deliver a `6–14`-word `H1` (optional focal italic/weight contrast), `<= 26`-word subtitle, zero acronyms in parentheses in H1, immediate interactive proof or human anchor above the fold, `PB06` Direct-Answer below the fold, and compact consent UI that never covers hero CTAs.
- **Dynamic Ads-First SSR (`/[vertical]/lp/[slug].astro`)**: Hydrate validated `CampaignLandingSpec` JSONs inheriting `[data-brand]` tokens, defaulting to `X-Robots-Tag: noindex, follow` (unless `seo_cluster_id` is set), gating `ViewContent` to acquisition routes, and rendering `<InteractiveProofCalculator />` strictly when `lead_magnet.mechanism !== "none"`.
- **Lazy 60fps Motion & Physical Craft Gate**: Load `GSAP + ScrollTrigger` (+ optional `Lenis` via `gsap.ticker`) inside `requestIdleCallback` with Astro View Transitions teardown and `prefers-reduced-motion`; validate with `impeccable detect`, `anti-slop-linter`, and batched desktop/mobile browser captures.

## Decision Gates

| Objective | Strategy | Reference |
|---|---|---|
| Architecture Matrix & Actions | Astro 5 SSR, Server Islands, Actions, NATS | [`references/usage.md`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| Craft, Fonts, Hero & Motion | `PB19`, `DESIGN.md`, `@fontsource-variable`, GSAP/Lenis | [`references/usage.md#7-anti-slop`](file:///var/www/.agents/skills/astro-web/references/usage.md#7-anti-slop) |
| Admin & Mobile UX | Standalone CSS, `path: "/"`, prefetch guard | [`references/usage.md#11-admin-invariants`](file:///var/www/.agents/skills/astro-web/references/usage.md#11-admin-invariants) |
| Topology & Lifecycle | Bun, NATS 2.12, Valkey 7.2, Postgres 18 | [`references/infra.md`](file:///var/www/.agents/skills/astro-web/references/infra.md) |

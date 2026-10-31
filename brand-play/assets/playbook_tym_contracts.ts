/**
 * playbook_tym_contracts.ts — Formal Type Definitions for Canonical TYM Playbooks
 * Standard: TYM (Type-YAML-Markdown) v1.0
 * Architecture: Fractal CoHaLo & Sovereign Brand-Play Transmutation
 */

export interface PlaybookMetadata {
  id: string;
  slug: string;
  cluster: string;
  version: string;
  title: string;
  authoritative_sources_count: number;
  system_dynamics_paradigm: "meadows_mit_four_layers";
  token_budget_target: number;
  zero_brand_slop_attested: boolean;
  updated_at: string;
}

export interface IcebergModel {
  events_reactive: string[];
  patterns_adaptive: string[];
  structures_systemic: string[];
  mental_models_transformative: string[];
}

export interface StockAndFlow {
  id: string;
  stock_name: string;
  inflows: string[];
  outflows: string[];
  equilibrium_heuristic: string;
}

export interface LeveragePoint {
  meadows_rank: number; // 1 to 12
  leverage_name: string;
  system_intervention: string;
}

export interface SystemDynamicsEngine {
  iceberg: IcebergModel;
  stocks_and_flows: StockAndFlow[];
  leverage_points?: LeveragePoint[];
}

export type SlotKind =
  | "string"
  | "color_hex"
  | "color_oklch"
  | "typography_family"
  | "price_currency"
  | "url_absolute"
  | "array_strings";

export interface SlotDefinition {
  key: string;
  kind: SlotKind;
  json_pointer: string; // RFC 6901 pointer into brandbook.json
  required: boolean;
  fallback_value: string | string[];
  description?: string;
}

export interface SlotsContract {
  brand_slots: SlotDefinition[];
}

export type ModularBlockKind =
  | "hero_hook"
  | "causal_mechanism"
  | "pricing_table"
  | "objection_antidote"
  | "guarantee_charter"
  | "faq_accordion"
  | "cta_cluster"
  | "whatsapp_qualification"
  | "email_transactional";

export type TargetAdapter =
  | "growth-engine"
  | "astro-web"
  | "whatsapp-engine"
  | "email-marketing";

export interface ModularBlock {
  anchor_id: string; // e.g. #mod-hero, #mod-mechanism
  kind: ModularBlockKind;
  title: string;
  causal_rationale: string;
  unhydrated_template: string; // Plain text with {{SLOT}} tags
  target_adapters: TargetAdapter[];
}

export interface CanonicalPlaybookTYM {
  metadata: PlaybookMetadata;
  system_dynamics: SystemDynamicsEngine;
  slots_contract: SlotsContract;
  modular_blocks: ModularBlock[];
  downstream_transmutation_rules: Record<string, string>;
}

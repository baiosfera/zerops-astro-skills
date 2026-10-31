/**
 * slot_hydrator.ts — Deterministic Semantic Slot Hydrator for Canonical TYM Playbooks
 * Standard: W3C DTCG Token Ingestion & RFC 6901 JSON Pointer Resolution
 */

import type { SlotDefinition, SlotsContract } from "./playbook_tym_contracts";

export interface HydrationResult {
  hydratedContent: string;
  resolvedSlots: Record<string, string>;
  unresolvedRequiredSlots: string[];
  unresolvedOptionalSlots: string[];
  prohibitedWordViolations: string[];
}

/**
 * Resolves an RFC 6901 JSON pointer (e.g. /design_system/color/primary) from an object.
 */
export function resolveJsonPointer(obj: any, pointer: string): any {
  if (!pointer || pointer === "/" || pointer === "") return obj;
  const parts = pointer.replace(/^\//, "").split("/").map(part => part.replace(/~1/g, "/").replace(/~0/g, "~"));
  let current = obj;
  for (const part of parts) {
    if (current === null || current === undefined || typeof current !== "object") {
      return undefined;
    }
    current = current[part];
  }
  // If DTCG node with $value, extract it
  if (current && typeof current === "object" && "$value" in current) {
    return current["$value"];
  }
  return current;
}

/**
 * Hydrates all {{SLOT}} instances in template text using the brandbook object and slots contract.
 */
export function hydrateTemplate(
  templateText: string,
  brandbook: Record<string, any>,
  slotsContract: SlotsContract,
  prohibitedWords: string[] = []
): HydrationResult {
  const resolvedSlots: Record<string, string> = {};
  const unresolvedRequiredSlots: string[] = [];
  const unresolvedOptionalSlots: string[] = [];

  // Build slot lookup
  const slotMap = new Map<string, SlotDefinition>();
  for (const slot of slotsContract.brand_slots) {
    slotMap.set(slot.key, slot);
  }

  // Pre-resolve all slots
  for (const slot of slotsContract.brand_slots) {
    let val = resolveJsonPointer(brandbook, slot.json_pointer);
    if (val === undefined || val === null || val === "") {
      if (slot.required && (slot.fallback_value === undefined || slot.fallback_value === null)) {
        unresolvedRequiredSlots.push(slot.key);
      } else {
        val = slot.fallback_value;
        if (val === undefined) {
          unresolvedOptionalSlots.push(slot.key);
        }
      }
    }
    if (val !== undefined && val !== null) {
      resolvedSlots[slot.key] = Array.isArray(val) ? val.join(", ") : String(val);
    }
  }

  // Replace {{SLOT}} in templateText
  const slotRegex = /\{\{([A-Z0-9_]+)\}\}/g;
  const hydratedContent = templateText.replace(slotRegex, (match, slotKey) => {
    if (slotKey in resolvedSlots) {
      return resolvedSlots[slotKey];
    }
    // Check if slot definition exists
    const slotDef = slotMap.get(slotKey);
    if (slotDef && slotDef.fallback_value !== undefined) {
      return String(slotDef.fallback_value);
    }
    return match; // Leave untouched for linter to detect
  });

  // Anti-Slop Linter: Check for remaining {{...}} tags
  const remainingSlots = hydratedContent.match(/\{\{([A-Z0-9_]+)\}\}/g) || [];
  for (const m of remainingSlots) {
    const key = m.replace(/[\{\}]/g, "");
    if (!unresolvedRequiredSlots.includes(key) && !unresolvedOptionalSlots.includes(key)) {
      unresolvedOptionalSlots.push(key);
    }
  }

  // Check prohibited words
  const prohibitedWordViolations: string[] = [];
  const contentLower = hydratedContent.toLowerCase();
  for (const word of prohibitedWords) {
    if (word && word.length > 2 && contentLower.includes(word.toLowerCase())) {
      prohibitedWordViolations.push(word);
    }
  }

  return {
    hydratedContent,
    resolvedSlots,
    unresolvedRequiredSlots,
    unresolvedOptionalSlots,
    prohibitedWordViolations
  };
}

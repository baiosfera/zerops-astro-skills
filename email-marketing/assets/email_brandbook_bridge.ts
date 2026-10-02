/**
 * @file email_brandbook_bridge.ts
 * @description Ingests and transpiles Design Tokens (W3C DTCG)
 * from brandbook.json into email template palettes with inline styling.
 * @version 2.0.0
 */

import { readFileSync, existsSync } from "node:fs";

export interface EmailBrandPalette {
  primary: string;
  secondary: string;
  accent: string;
  background: string;
  surface: string;
  textPrimary: string;
  textMuted: string;
  border: string;
}

export interface EmailTypographyStack {
  display: string;
  body: string;
  googleFontImportUrl?: string;
}

export interface EmailBrandTokens {
  brandName: string;
  slogan: string;
  archetype: string;
  palette: EmailBrandPalette;
  typography: EmailTypographyStack;
  monogramSvg?: string;
  logoSvg?: string;
}

/**
 * Loads and transpiles a brandbook.json (W3C DTCG) file for email usage
 */
export function loadEmailBrandTokens(brandbookPath: string): EmailBrandTokens {
  if (!existsSync(brandbookPath)) {
    throw new Error(`[EmailBrandBridge] brandbook.json not found at: ${brandbookPath}`);
  }

  const raw = readFileSync(brandbookPath, "utf-8");
  const data = JSON.parse(raw);

  const brandName = data.brand?.name?.$value || data.name || "Brand";
  const slogan = data.brand?.slogan?.$value || "";
  const archetype = data.brand?.archetype?.$value || "Sovereign / Enterprise";

  // Color Transpilation
  const darkColors = data.color?.dark || data.color?.light || {};
  const palette: EmailBrandPalette = {
    primary: darkColors.primary?.hex || "#2563eb",
    secondary: darkColors.secondary?.hex || "#059669",
    accent: darkColors.accent?.hex || "#3b82f6",
    background: darkColors.background?.hex || "#0f172a",
    surface: darkColors.surface?.hex || "#1e293b",
    textPrimary: darkColors.text_primary?.hex || "#f8fafc",
    textMuted: darkColors.text_muted?.hex || "#94a3b8",
    border: "#334155",
  };

  // Safe Email Typography Stacks
  const fontDisplayRaw = data.typography?.display?.$value || "Inter";
  const fontBodyRaw = data.typography?.body?.$value || "Inter";

  const typography: EmailTypographyStack = {
    display: `'${fontDisplayRaw}', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`,
    body: `'${fontBodyRaw}', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`,
    googleFontImportUrl: "https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap",
  };

  // SVG Vectors
  const monogramSvg = data.vectors?.monogram?.svg_raw || undefined;
  const logoSvg = data.vectors?.logo_primary?.svg_raw || undefined;

  return {
    brandName,
    slogan,
    archetype,
    palette,
    typography,
    monogramSvg,
    logoSvg,
  };
}

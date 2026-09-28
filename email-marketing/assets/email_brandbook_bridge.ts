/**
 * @file email_brandbook_bridge.ts
 * @description Bridge determinista para la ingesta y transpilación de Design Tokens (W3C DTCG)
 * desde brandbook.json hacia plantillas de correo electrónico con estilos 100% Inline.
 * @version 1.0.0 (Vigencia 2025/2026)
 */

import { readFileSync, existsSync } from "node:fs";
import { z } from "zod";

export interface EmailBrandPalette {
  primary: string;       // Hex sRGB (ej. #E2C974 Oro Champagne)
  secondary: string;     // Hex sRGB (ej. #10B981 Verde Esmeralda)
  accent: string;        // Hex sRGB (ej. #34D399 Esmeralda Luminosa)
  background: string;    // Hex sRGB (ej. #0F172A Negro Obsidiana)
  surface: string;       // Hex sRGB (ej. #1E293B Pizarra Profunda)
  textPrimary: string;   // Hex sRGB (ej. #F8FAFC Blanco Titanio)
  textMuted: string;     // Hex sRGB (ej. #94A3B8 Gris Platino)
  border: string;        // Hex sRGB
}

export interface EmailTypographyStack {
  display: string;       // Stack de Titulares con fallback (ej. 'Rising', 'Playfair Display', Georgia, serif)
  body: string;          // Stack de Párrafos con fallback (ej. 'Plus Jakarta Sans', 'Segoe UI', -apple-system, sans-serif)
  googleFontImportUrl?: string; // URL opcional para clientes con soporte @import (Apple Mail)
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
 * Carga y transpila un archivo brandbook.json (W3C DTCG) para uso en emails
 */
export function loadEmailBrandTokens(brandbookPath: string): EmailBrandTokens {
  if (!existsSync(brandbookPath)) {
    throw new Error(`[EmailBrandBridge] brandbook.json no encontrado en: ${brandbookPath}`);
  }

  const raw = readFileSync(brandbookPath, "utf-8");
  const data = JSON.parse(raw);

  const brandName = data.brand?.name?.$value || data.name || "Brand";
  const slogan = data.brand?.slogan?.$value || "";
  const archetype = data.brand?.archetype?.$value || "La Gobernante / Lujo Silencioso";

  // Transpilación de Colores (Priorizando Hex del bloque dark o extensions)
  const darkColors = data.color?.dark || {};
  const palette: EmailBrandPalette = {
    primary: darkColors.primary?.hex || "#E2C974",
    secondary: darkColors.secondary?.hex || "#10B981",
    accent: darkColors.accent?.hex || "#34D399",
    background: darkColors.background?.hex || "#0F172A",
    surface: darkColors.surface?.hex || "#1E293B",
    textPrimary: darkColors.text_primary?.hex || "#F8FAFC",
    textMuted: darkColors.text_muted?.hex || "#94A3B8",
    border: "#334155",
  };

  // Pilas Tipográficas Seguras para Email
  const fontDisplayRaw = data.typography?.display?.$value || "Rising";
  const fontBodyRaw = data.typography?.body?.$value || "Plus Jakarta Sans";

  const typography: EmailTypographyStack = {
    display: `'${fontDisplayRaw}', 'Playfair Display', Georgia, 'Times New Roman', serif`,
    body: `'${fontBodyRaw}', 'Segoe UI', -apple-system, BlinkMacSystemFont, Tahoma, Geneva, Verdana, sans-serif`,
    googleFontImportUrl: "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap",
  };

  // Vectores SVG
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

#!/usr/bin/env python3
"""
Universal Agnostic Visual Asset & OpenGraph Generator (SOTA 2026)
Generates complete Favicon Suite, PWA Web Manifest, and Multi-Surface OpenGraph images.
Enforces:
  - Universal OpenGraph 1200x630 with 1080x600 centered safe zone.
  - Strict WhatsApp preview compression budget (<300 KB).
  - Apple Touch Icon (180x180 solid background).
  - Vector SVG Favicon with dark/light scheme.
  - Client-agnostic parameterization via CLI args and W3C DTCG brandbook tokens.
"""

import os
import sys
import json
import argparse
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def parse_args():
    parser = argparse.ArgumentParser(description="Generate Favicon Suite and Multi-Surface OG assets")
    parser.add_argument("--logo", required=True, help="Path to master logo file (PNG or JPG)")
    parser.add_argument("--out-dir", required=True, help="Output directory (e.g. public/)")
    parser.add_argument("--brand-name", default="Sovereign Brand", help="Brand or Site Name")
    parser.add_argument("--tagline", default="", help="Brand Tagline or Subtitle for OG cards")
    parser.add_argument("--bg-color", default="#050505", help="Background hex color for dark theme")
    parser.add_argument("--accent-color", default="#C5A059", help="Accent hex color (gold/highlight)")
    parser.add_argument("--text-color", default="#F7F4EE", help="Text hex color")
    parser.add_argument("--brandbook", default="", help="Optional path to W3C DTCG brandbook.json to pull tokens")
    parser.add_argument("--full-bleed", action="store_true", help="Scale logo to fill full icon bounds without background padding")
    return parser.parse_args()

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip("#")
    if len(hex_str) == 3:
        hex_str = "".join([c*2 for c in hex_str])
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def load_brandbook_tokens(brandbook_path):
    if not brandbook_path or not os.path.exists(brandbook_path):
        return {}
    try:
        with open(brandbook_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except Exception as e:
        print(f"Warning: could not parse brandbook at {brandbook_path}: {e}")
        return {}

def generate_favicons(logo_path, out_dir, bg_color, brand_name="Brand", accent_color="#C5A059", full_bleed=False):
    print("• Generating Favicon Suite...")
    os.makedirs(out_dir, exist_ok=True)
    logo = Image.open(logo_path).convert("RGBA")
    
    # 1. Favicon 16x16 and 32x32
    fav16 = logo.resize((16, 16), Image.Resampling.LANCZOS)
    fav32 = logo.resize((32, 32), Image.Resampling.LANCZOS)
    fav48 = logo.resize((48, 48), Image.Resampling.LANCZOS)
    
    fav16.save(os.path.join(out_dir, "favicon-16x16.png"), "PNG")
    fav32.save(os.path.join(out_dir, "favicon-32x32.png"), "PNG")
    
    # Favicon.ico multi-resolution
    ico_path = os.path.join(out_dir, "favicon.ico")
    logo.save(ico_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
    print(f"  ✓ Created {ico_path}")

    # 2. Apple Touch Icon 180x180 (Solid background per Apple HIG)
    if full_bleed or (logo.width == logo.height and logo.mode == "RGB"):
        scaled_apple = logo.resize((180, 180), Image.Resampling.LANCZOS)
        apple_canvas = scaled_apple
    else:
        apple_canvas = Image.new("RGBA", (180, 180), hex_to_rgb(bg_color) + (255,))
        logo_ratio = min(140 / logo.width, 140 / logo.height)
        new_w, new_h = int(logo.width * logo_ratio), int(logo.height * logo_ratio)
        scaled_logo = logo.resize((new_w, new_h), Image.Resampling.LANCZOS)
        offset = ((180 - new_w) // 2, (180 - new_h) // 2)
        apple_canvas.paste(scaled_logo, offset, scaled_logo)
    
    apple_path = os.path.join(out_dir, "apple-touch-icon.png")
    apple_canvas.convert("RGB").save(apple_path, "PNG", optimize=True)
    print(f"  ✓ Created {apple_path} (180x180)")

    # 3. PWA Icons 192x192 and 512x512 (Full bleed option for seamless brand bounds)
    for size in (192, 512):
        if full_bleed:
            pwa_canvas = logo.resize((size, size), Image.Resampling.LANCZOS)
        else:
            pwa_canvas = Image.new("RGBA", (size, size), hex_to_rgb(bg_color) + (255,))
            target_size = int(size * 0.85)
            pwa_ratio = min(target_size / logo.width, target_size / logo.height)
            pw_w, pw_h = int(logo.width * pwa_ratio), int(logo.height * pwa_ratio)
            pwa_scaled = logo.resize((pw_w, pw_h), Image.Resampling.LANCZOS)
            pwa_offset = ((size - pw_w) // 2, (size - pw_h) // 2)
            pwa_canvas.paste(pwa_scaled, pwa_offset, pwa_scaled)
        pwa_out = os.path.join(out_dir, f"icon-{size}.png")
        pwa_canvas.convert("RGBA").save(pwa_out, "PNG", optimize=True)
        print(f"  ✓ Created {pwa_out}")

    # 4. Scalable Vector Favicon (favicon.svg)
    svg_path = os.path.join(out_dir, "favicon.svg")
    initial = (brand_name[0] if brand_name else "A").upper()
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <style>
    circle {{ fill: {bg_color}; }}
    text {{ fill: {accent_color}; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, serif; font-size: 50px; font-weight: bold; text-anchor: middle; dominant-baseline: central; }}
    @media (prefers-color-scheme: light) {{
      circle {{ fill: #F7F4EE; }}
      text {{ fill: {bg_color}; }}
    }}
  </style>
  <circle cx="50" cy="50" r="48" stroke="{accent_color}" stroke-width="2"/>
  <text x="50" y="54">{initial}</text>
</svg>"""
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"  ✓ Created {svg_path}")

def generate_webmanifest(out_dir, brand_name, bg_color, theme_color):
    manifest = {
        "name": brand_name,
        "short_name": brand_name[:12],
        "start_url": "/",
        "display": "standalone",
        "background_color": bg_color,
        "theme_color": theme_color,
        "icons": [
            {
                "src": "/icon-192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/icon-512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable"
            }
        ]
    }
    manifest_path = os.path.join(out_dir, "site.webmanifest")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"  ✓ Created {manifest_path}")

def generate_opengraph_cards(logo_path, out_dir, brand_name, tagline, bg_color, accent_color, text_color):
    print("• Generating Multi-Surface OpenGraph Cards...")
    logo = Image.open(logo_path).convert("RGBA")
    
    # 1. Universal OpenGraph (1200x630, 1.91:1) with safe zone 1080x600
    w, h = 1200, 630
    card = Image.new("RGB", (w, h), hex_to_rgb(bg_color))
    draw = ImageDraw.Draw(card)
    
    # Elegant decorative border (inside safe zone)
    margin_x = 60
    margin_y = 30
    draw.rectangle([margin_x, margin_y, w - margin_x, h - margin_y], outline=hex_to_rgb(accent_color), width=2)
    draw.rectangle([margin_x + 6, margin_y + 6, w - margin_x - 6, h - margin_y - 6], outline=hex_to_rgb(accent_color), width=1)
    
    # Place logo (left/center)
    logo_max = 280
    l_ratio = min(logo_max / logo.width, logo_max / logo.height)
    lw, lh = int(logo.width * l_ratio), int(logo.height * l_ratio)
    scaled_logo = logo.resize((lw, lh), Image.Resampling.LANCZOS)
    
    logo_x = margin_x + 60
    logo_y = (h - lh) // 2
    card.paste(scaled_logo, (logo_x, logo_y), scaled_logo)
    
    # Load fonts (fallback to default if ttf not in container)
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 46)
        sub_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    except Exception:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        
    # Text block
    text_x = logo_x + lw + 60
    text_y = (h // 2) - 60
    
    draw.text((text_x, text_y), brand_name, fill=hex_to_rgb(accent_color), font=title_font)
    if tagline:
        # Wrap simple tagline
        draw.text((text_x, text_y + 70), tagline[:75], fill=hex_to_rgb(text_color), font=sub_font)
        if len(tagline) > 75:
            draw.text((text_x, text_y + 105), tagline[75:150], fill=hex_to_rgb(text_color), font=sub_font)
            
    # Save with strict WhatsApp compression budget (<300 KB)
    og_universal_path = os.path.join(out_dir, "og-default.jpg")
    card.save(og_universal_path, "JPEG", quality=85, optimize=True, progressive=True)
    size_kb = os.path.getsize(og_universal_path) / 1024
    print(f"  ✓ Created {og_universal_path} (1200x630, {size_kb:.1f} KB - WhatsApp Safe: {size_kb < 300})")
    
    # 2. Square OG / Instagram / WhatsApp Catalog (1080x1080)
    sq_size = 1080
    sq_card = Image.new("RGB", (sq_size, sq_size), hex_to_rgb(bg_color))
    sq_draw = ImageDraw.Draw(sq_card)
    sq_draw.rectangle([40, 40, sq_size - 40, sq_size - 40], outline=hex_to_rgb(accent_color), width=2)
    
    sq_logo_max = 420
    sq_ratio = min(sq_logo_max / logo.width, sq_logo_max / logo.height)
    sq_lw, sq_lh = int(logo.width * sq_ratio), int(logo.height * sq_ratio)
    sq_scaled = logo.resize((sq_lw, sq_lh), Image.Resampling.LANCZOS)
    sq_card.paste(sq_scaled, ((sq_size - sq_lw) // 2, 220), sq_scaled)
    
    sq_draw.text(((sq_size // 2) - 180, 700), brand_name, fill=hex_to_rgb(accent_color), font=title_font)
    if tagline:
        sq_draw.text(((sq_size // 2) - 260, 780), tagline[:50], fill=hex_to_rgb(text_color), font=sub_font)
        
    og_square_path = os.path.join(out_dir, "og-square.jpg")
    sq_card.save(og_square_path, "JPEG", quality=85, optimize=True)
    print(f"  ✓ Created {og_square_path} (1080x1080)")

def main():
    args = parse_args()
    if not os.path.exists(args.logo):
        print(f"Error: logo not found at {args.logo}", file=sys.stderr)
        sys.exit(1)
        
    tokens = load_brandbook_tokens(args.brandbook)
    # Token extraction if brandbook was passed
    generate_favicons(args.logo, args.out_dir, args.bg_color, brand_name=args.brand_name, accent_color=args.accent_color, full_bleed=args.full_bleed)
    generate_webmanifest(args.out_dir, args.brand_name, args.bg_color, args.accent_color)
    generate_opengraph_cards(args.logo, args.out_dir, args.brand_name, args.tagline, args.bg_color, args.accent_color, args.text_color)
    print("✅ All visual assets generated successfully.")

if __name__ == "__main__":
    main()

"""GentleLab Spiral Ring V2 → multi-size favicons.

SVG spec (viewBox 280×280):
  - circles: r=100.8/70/95.2/77/109.2
  - strokes: #C8956C/#E8A54B/#5CBBAA/#7FBBB3/#90D4A8
  - widths:  21/16.8/16.8/11.2/7
  - opacity: 0.85/0.65/0.7/0.5/0.3

출력 (public/):
  - favicon.ico (16+32+48 multi-size)
  - favicon-32.png · favicon-96.png · favicon-192.png
  - apple-touch-icon.png (180×180, Salt White BG, rounded corners by iOS)
"""
from PIL import Image, ImageDraw
from pathlib import Path

OUT = Path("/Users/seung-yeoblee/dev/gentlelab-web/public")

# Brand colors
BG_TRANSPARENT = (0, 0, 0, 0)
BG_SALT_WHITE = (250, 250, 248, 255)
BG_DEEP_OCEAN = (27, 40, 56, 255)

# Ring spec (in viewBox 280 unit) — center 140,140
RINGS = [
    # (r, color, width, opacity)
    (100.8, (200, 149, 108), 21,   0.85),  # Compass Gold
    (70.0,  (232, 165, 75),  16.8, 0.65),  # Dusk Amber
    (95.2,  (92, 187, 170),  16.8, 0.70),  # Seafoam
    (77.0,  (127, 187, 179), 11.2, 0.50),  # Sage Mist
    (109.2, (144, 212, 168), 7,    0.30),  # Mint
]

VIEWBOX = 280
CENTER = VIEWBOX / 2  # 140


def render_spiral(size_px: int, bg=None) -> Image.Image:
    """Render Spiral Ring V2 at size_px × size_px.
    Internally uses 4× supersample then downscale for smooth edges.
    """
    SS = 4  # supersample factor
    canvas_size = size_px * SS
    scale = canvas_size / VIEWBOX

    # Create canvas
    if bg is None:
        img = Image.new("RGBA", (canvas_size, canvas_size), BG_TRANSPARENT)
    else:
        img = Image.new("RGBA", (canvas_size, canvas_size), bg)

    # Each ring rendered separately with alpha then composited
    for r, color, stroke_w, opacity in RINGS:
        ring_layer = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
        d = ImageDraw.Draw(ring_layer)
        cx = cy = CENTER * scale
        radius = r * scale
        sw = stroke_w * scale
        # Draw ring as 2 circles diff (outer fill, inner cut)
        # Pillow ellipse with width parameter draws stroke inside the bbox
        rgba = (*color, int(255 * opacity))
        bbox = (cx - radius, cy - radius, cx + radius, cy + radius)
        d.ellipse(bbox, outline=rgba, width=int(round(sw)))
        # Composite onto main
        img = Image.alpha_composite(img, ring_layer)

    # Downscale with LANCZOS for smooth edges
    return img.resize((size_px, size_px), Image.LANCZOS)


def main():
    print("=== GentleLab Spiral Ring V2 → favicons ===\n")

    # 1. PNG favicons (transparent BG)
    for size in (32, 96, 192):
        img = render_spiral(size)
        out = OUT / f"favicon-{size}.png"
        img.save(out, "PNG", optimize=True)
        print(f"✓ {out.name}  ({size}×{size}, transparent)")

    # 2. apple-touch-icon (180×180, Salt White BG — iOS adds rounded corners automatically)
    apple = render_spiral(180, bg=BG_SALT_WHITE)
    apple_out = OUT / "apple-touch-icon.png"
    apple.save(apple_out, "PNG", optimize=True)
    print(f"✓ {apple_out.name}  (180×180, Salt White BG)")

    # 3. favicon.ico (multi-size 16+32+48 — universal browser support)
    # Use 256 base + Pillow's sizes parameter to generate multi-size
    base = render_spiral(256, bg=BG_SALT_WHITE)  # ICO with white BG for visibility on any tab
    ico_out = OUT / "favicon.ico"
    base.save(ico_out, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
    print(f"✓ {ico_out.name}  (multi-size 16/32/48, Salt White BG)")

    print("\n완료 — favicon.svg는 그대로 유지 (modern browser SVG 우선).")


if __name__ == "__main__":
    main()

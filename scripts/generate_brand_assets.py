#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
BRAND_DIR = ROOT / "assets" / "brand"

BG = (242, 245, 251, 255)
PANEL = (255, 255, 255, 242)
LINE = (32, 61, 112, 38)
TEXT = (15, 23, 40, 255)
MUTED = (78, 92, 116, 255)
ACCENT = (18, 115, 255, 255)
ACCENT_DARK = (3, 83, 216, 255)
SUCCESS = (20, 184, 107, 255)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = ["DejaVuSans-Bold.ttf", "Arial Bold.ttf"] if bold else ["DejaVuSans.ttf", "Arial.ttf"]
    for name in names:
        try:
            return ImageFont.truetype(name, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_grid(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], step: int, color: tuple[int, int, int, int]) -> None:
    left, top, right, bottom = box
    for x in range(left, right + 1, step):
        draw.line((x, top, x, bottom), fill=color, width=1)
    for y in range(top, bottom + 1, step):
        draw.line((left, y, right, y), fill=color, width=1)


def draw_mark(draw: ImageDraw.ImageDraw, origin: tuple[int, int], size: int, panel: bool) -> None:
    x, y = origin
    inset = max(10, size // 14)
    radius = size // 6
    if panel:
        draw.rounded_rectangle((x, y, x + size, y + size), radius=radius, fill=PANEL, outline=(32, 61, 112, 46), width=3)

    inner = (x + inset, y + inset, x + size - inset, y + size - inset)
    draw_grid(draw, inner, max(18, size // 6), LINE)

    base_y = y + size - inset
    left = x + inset
    right = x + size - inset
    draw.line((left, base_y, right, base_y), fill=(32, 61, 112, 90), width=max(2, size // 48))
    draw.line((left, y + inset, left, base_y), fill=(32, 61, 112, 90), width=max(2, size // 48))

    points = [
        (x + size * 0.22, y + size * 0.72),
        (x + size * 0.39, y + size * 0.58),
        (x + size * 0.54, y + size * 0.64),
        (x + size * 0.71, y + size * 0.37),
        (x + size * 0.84, y + size * 0.23),
    ]
    draw.line(points, fill=ACCENT, width=max(5, size // 24), joint="curve")

    for px, py in points[:-1]:
        radius = max(5, size // 40)
        draw.ellipse((px - radius, py - radius, px + radius, py + radius), fill=PANEL, outline=ACCENT_DARK, width=3)

    focus = points[-1]
    focus_radius = max(8, size // 28)
    draw.ellipse(
        (focus[0] - focus_radius, focus[1] - focus_radius, focus[0] + focus_radius, focus[1] + focus_radius),
        fill=SUCCESS,
        outline=ACCENT_DARK,
        width=4,
    )

    for bar_x in [x + size * 0.18, x + size * 0.31, x + size * 0.44]:
        top = y + size * 0.8
        bar_top = top - size * (0.12 + ((bar_x - x) / size) * 0.16)
        draw.rounded_rectangle(
            (bar_x, bar_top, bar_x + size * 0.07, top),
            radius=max(4, size // 48),
            fill=(18, 115, 255, 40),
            outline=(18, 115, 255, 80),
            width=2,
        )


def write_mark_svg() -> None:
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" role="img" aria-labelledby="title desc">
  <title id="title">DeepSeek V4 Benchmark logo mark</title>
  <desc id="desc">Rounded benchmark grid with an ascending blue line and green terminal point.</desc>
  <rect x="8" y="8" width="240" height="240" rx="42" fill="#ffffff" stroke="rgba(32,61,112,0.18)" stroke-width="3"/>
  <g stroke="rgba(32,61,112,0.18)" stroke-width="1">
    <path d="M48 48V208"/>
    <path d="M82 48V208"/>
    <path d="M116 48V208"/>
    <path d="M150 48V208"/>
    <path d="M184 48V208"/>
    <path d="M208 48V208"/>
    <path d="M48 48H208"/>
    <path d="M48 82H208"/>
    <path d="M48 116H208"/>
    <path d="M48 150H208"/>
    <path d="M48 184H208"/>
    <path d="M48 208H208"/>
  </g>
  <g stroke="#0353d8" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <polyline points="56,176 100,142 138,156 182,96 214,58"/>
  </g>
  <g fill="#ffffff" stroke="#0353d8" stroke-width="4">
    <circle cx="56" cy="176" r="7"/>
    <circle cx="100" cy="142" r="7"/>
    <circle cx="138" cy="156" r="7"/>
    <circle cx="182" cy="96" r="7"/>
  </g>
  <circle cx="214" cy="58" r="10" fill="#14b86b" stroke="#0353d8" stroke-width="4"/>
  <g fill="rgba(18,115,255,0.12)" stroke="rgba(18,115,255,0.3)" stroke-width="2">
    <rect x="56" y="140" width="18" height="52" rx="5"/>
    <rect x="88" y="126" width="18" height="66" rx="5"/>
    <rect x="120" y="112" width="18" height="80" rx="5"/>
  </g>
</svg>
"""
    (BRAND_DIR / "logo-mark.svg").write_text(svg, encoding="utf-8")
    (BRAND_DIR / "favicon.svg").write_text(svg, encoding="utf-8")


def write_wordmark_svg() -> None:
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 320" role="img" aria-labelledby="title desc">
  <title id="title">DeepSeek V4 Benchmark wordmark</title>
  <desc id="desc">Technical wordmark with a benchmark grid mark and stacked title.</desc>
  <defs>
    <linearGradient id="line" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1273ff"/>
      <stop offset="100%" stop-color="#0353d8"/>
    </linearGradient>
  </defs>
  <rect width="960" height="320" rx="36" fill="rgba(255,255,255,0.84)"/>
  <g transform="translate(24 32) scale(1)">
    <rect x="8" y="8" width="240" height="240" rx="42" fill="#ffffff" stroke="rgba(32,61,112,0.18)" stroke-width="3"/>
    <g stroke="rgba(32,61,112,0.18)" stroke-width="1">
      <path d="M48 48V208"/>
      <path d="M82 48V208"/>
      <path d="M116 48V208"/>
      <path d="M150 48V208"/>
      <path d="M184 48V208"/>
      <path d="M208 48V208"/>
      <path d="M48 48H208"/>
      <path d="M48 82H208"/>
      <path d="M48 116H208"/>
      <path d="M48 150H208"/>
      <path d="M48 184H208"/>
      <path d="M48 208H208"/>
    </g>
    <polyline points="56,176 100,142 138,156 182,96 214,58" fill="none" stroke="url(#line)" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
    <g fill="#ffffff" stroke="#0353d8" stroke-width="4">
      <circle cx="56" cy="176" r="7"/>
      <circle cx="100" cy="142" r="7"/>
      <circle cx="138" cy="156" r="7"/>
      <circle cx="182" cy="96" r="7"/>
    </g>
    <circle cx="214" cy="58" r="10" fill="#14b86b" stroke="#0353d8" stroke-width="4"/>
  </g>
  <text x="308" y="128" fill="#0f1728" font-size="76" font-weight="700" letter-spacing="-2" font-family="'Avenir Next Condensed','Avenir Next','Segoe UI Variable',sans-serif">DEEPSEEK V4</text>
  <text x="308" y="200" fill="#0353d8" font-size="76" font-weight="700" letter-spacing="-2" font-family="'Avenir Next Condensed','Avenir Next','Segoe UI Variable',sans-serif">BENCHMARK</text>
  <text x="312" y="244" fill="#4e5c74" font-size="24" font-weight="600" letter-spacing="8" font-family="'IBM Plex Mono','SFMono-Regular',monospace">PUBLIC MODEL SNAPSHOT</text>
  <path d="M312 228H802" stroke="rgba(32,61,112,0.18)" stroke-width="3"/>
</svg>
"""
    (BRAND_DIR / "logo-wordmark.svg").write_text(svg, encoding="utf-8")


def draw_wrapped_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    start: tuple[int, int],
    font_obj: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    fill: tuple[int, int, int, int],
    max_width: int,
    line_gap: int,
) -> int:
    x, y = start
    lines: list[str] = []
    for paragraph in text.splitlines():
        current = ""
        for word in paragraph.split():
            candidate = word if not current else f"{current} {word}"
            if draw.textlength(candidate, font=font_obj) <= max_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        if not paragraph:
            lines.append("")

    for line in lines:
        draw.text((x, y), line, font=font_obj, fill=fill)
        y += line_gap

    return y


def create_png_assets() -> None:
    logo = Image.new("RGBA", (512, 512), BG)
    draw = ImageDraw.Draw(logo)
    draw_mark(draw, (28, 28), 456, panel=True)
    logo.save(BRAND_DIR / "logo-mark.png")
    logo.resize((256, 256), Image.Resampling.LANCZOS).save(BRAND_DIR / "favicon.png")
    logo.resize((180, 180), Image.Resampling.LANCZOS).save(BRAND_DIR / "apple-touch-icon.png")
    logo.resize((192, 192), Image.Resampling.LANCZOS).save(BRAND_DIR / "icon-192.png")
    logo.resize((512, 512), Image.Resampling.LANCZOS).save(BRAND_DIR / "icon-512.png")

    card = Image.new("RGBA", (1200, 630), BG)
    draw = ImageDraw.Draw(card)
    draw.rounded_rectangle((24, 24, 1176, 606), radius=36, fill=PANEL, outline=(32, 61, 112, 44), width=4)
    draw_mark(draw, (70, 120), 260, panel=True)

    headline_font = font(76, bold=True)
    body_font = font(28)
    micro_font = font(22)

    draw.text((390, 148), "DEEPSEEK V4", font=headline_font, fill=TEXT)
    draw.text((390, 230), "BENCHMARK", font=headline_font, fill=ACCENT_DARK)
    line_y = draw_wrapped_text(
        draw,
        "Public comparison snapshot vs GPT-5.4, Claude Opus 4.6, and Gemini 3.1 Pro.",
        (392, 334),
        body_font,
        MUTED,
        700,
        42,
    )
    draw_wrapped_text(
        draw,
        "Official model cards, API docs, and launch posts only.",
        (392, line_y + 16),
        body_font,
        MUTED,
        700,
        42,
    )
    draw.line((392, 428, 1030, 428), fill=(32, 61, 112, 48), width=3)
    draw.text((392, 478), "Updated 2026-04-24", font=micro_font, fill=ACCENT_DARK)
    draw.text((392, 516), "deepseekv4benchmark.lol", font=micro_font, fill=MUTED)
    card.save(BRAND_DIR / "social-card.png")


def main() -> None:
    BRAND_DIR.mkdir(parents=True, exist_ok=True)
    write_mark_svg()
    write_wordmark_svg()
    create_png_assets()
    print(f"Brand assets generated in {BRAND_DIR}")


if __name__ == "__main__":
    main()

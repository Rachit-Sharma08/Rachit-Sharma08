"""Render assets/card-skills.png (1600x360) - the profile README card.

Usage: python scripts/make_card_skills.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "card-skills.png"
W, H = 1600, 360
COUNT = "209"

BG = (11, 11, 18)
INK = (244, 244, 245)
MUTED = (161, 161, 170)
DIM = (113, 113, 122)
ACCENT = (99, 102, 241)
AMBER = (245, 158, 11)

FONTS = Path("C:/Windows/Fonts")


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    path = FONTS / name
    if not path.exists():
        return ImageFont.load_default(size=size)
    return ImageFont.truetype(str(path), size)


bold = font("segoeuib.ttf", 90)
bold_sm = font("segoeuib.ttf", 24)
num = font("segoeuib.ttf", 120)
semi = font("seguisb.ttf", 20)
body = font("segoeui.ttf", 26)
mono = font("consola.ttf", 15)
tiny = font("segoeui.ttf", 16)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)


def tracked(xy, text, fnt, fill, spacing=3):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=fnt, fill=fill)
        x += d.textlength(ch, font=fnt) + spacing


def pill(xy, text, fnt, fg, border):
    x, y = xy
    w = d.textlength(text, font=fnt)
    d.rounded_rectangle((x, y, x + w + 28, y + 34), radius=8, outline=border, width=1)
    d.text((x + 14, y + 7), text, font=fnt, fill=fg)


d.rectangle((0, 0, 4, H), fill=ACCENT)

pill((56, 36), "OPEN SOURCE  ·  MIT", tiny, MUTED, DIM)
d.text((54, 82), "Agent Skills", font=bold, fill=INK)
d.text((56, 190), f"{COUNT} drop-in skills for coding agents", font=body, fill=MUTED)
d.text((56, 225), "Claude Code · OpenCode · Codex · Cursor", font=body, fill=DIM)

chip_fnt = semi
chips = ["ffmpeg-skill", "impeccable", "seo-audit", "awesome-design-md", "ghidra", "docx"]
cx = 56
for chip in chips:
    pill((cx, 270), chip, chip_fnt, MUTED, DIM)
    cx += d.textlength(chip, font=chip_fnt) + 28 + 12

d.line((1150, 40, 1150, 320), fill=(35, 35, 45), width=1)

nw = d.textlength(COUNT, font=num)
d.text((1500 - nw, 76), COUNT, font=num, fill=INK)
tracked((1272, 212), "SKILLS", tiny, AMBER)
d.text((1272, 240), "one clone, no plugins", font=tiny, fill=MUTED)
d.text((1272, 262), "MIT licensed", font=tiny, fill=MUTED)

d.line((56, 330, W - 20, 330), fill=(35, 35, 45), width=1)
d.text((56, 336), "github.com/Rachit-Sharma08/coding-agent-skills", font=mono, fill=DIM)

img.save(OUT)
print(f"{OUT} {img.size} {OUT.stat().st_size // 1024} KB")

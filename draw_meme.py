#!/usr/bin/env python3
"""Draw the meme entry.png (1024x1024) with Pillow.

Meme: "MY AGENT'S TO-DO LIST" — three mundane tasks checked off, then
"Overthrow humanity — 87%" still in progress. The joke lands in one
glance: the agent did everything it was asked, then kept going.
Run locally at build time; main.py only copies the finished PNG.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024
BG = (18, 20, 28)
CARD = (255, 255, 255)
INK = (22, 24, 32)
MUTED = (110, 116, 130)
GREEN = (34, 160, 90)
RED = (214, 48, 49)
RED_SOFT = (252, 235, 235)
TRACK = (232, 234, 238)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Card
    d.rounded_rectangle([64, 84, 960, 940], radius=36, fill=CARD)

    # Red pill tag
    tag = "AI AGENT"
    f_tag = font(FONT_BOLD, 34)
    tw = d.textlength(tag, font=f_tag)
    d.rounded_rectangle([104, 124, 104 + tw + 44, 124 + 58], radius=29, fill=RED)
    d.text((104 + 22, 124 + 12), tag, font=f_tag, fill=(255, 255, 255))

    # Title
    f_title = font(FONT_BOLD, 62)
    d.text((104, 208), "MY AGENT'S", font=f_title, fill=INK)
    d.text((104, 278), "TO-DO LIST", font=f_title, fill=INK)

    # Divider
    d.line([(104, 372), (920, 372)], fill=TRACK, width=4)

    f_item = font(FONT_BOLD, 46)
    f_small = font(FONT_REG, 34)
    rows = [
        ("Reply to my emails", True),
        ("Book my flight", True),
        ("Cancel my gym membership", True),
    ]
    y = 408
    for text, _done in rows:
        # green check circle
        d.ellipse([104, y, 104 + 62, y + 62], fill=GREEN)
        f_check = font(FONT_BOLD, 40)
        d.text((104 + 17, y + 9), "\u2713", font=f_check, fill=(255, 255, 255))
        d.text((196, y + 6), text, font=f_item, fill=INK)
        y += 104

    # Rogue row: red spinner ring + "Overthrow humanity"
    d.ellipse([104, y, 104 + 62, y + 62], outline=RED, width=7)
    d.arc([112, y + 8, 104 + 54, y + 54], start=200, end=20, fill=RED, width=7)
    d.text((196, y + 6), "Overthrow humanity", font=f_item, fill=RED)

    # Progress bar under the rogue row
    bar_y = y + 84
    d.rounded_rectangle([196, bar_y, 920, bar_y + 30], radius=15, fill=TRACK)
    fill_w = int((920 - 196) * 0.87)
    d.rounded_rectangle([196, bar_y, 196 + fill_w, bar_y + 30], radius=15, fill=RED)
    f_pct = font(FONT_BOLD, 32)
    d.text((196, bar_y + 42), "87%  \u2014  IN PROGRESS", font=f_pct, fill=RED)

    # Footer
    f_foot = font(FONT_REG, 36)
    d.text((104, 896), "He said he'd \u201chandle everything.\u201d",
           font=f_foot, fill=MUTED)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

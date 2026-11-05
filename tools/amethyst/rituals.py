#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Mock screens for Amethyst's rituals (docs/AMETHYST.md, section 3): the rewind call, a shout-out, the dubplate, the
tape pack and the sleeve notes. Sketches at the FM-1's size, cut to 16 colors like everything else in docs/amethyst/.

  python3 tools/amethyst/rituals.py [--font FONT.ttf] [--out docs/amethyst/rituals]

Three of them sit on the Commons photos in docs/amethyst/photos/ (the-end.png, CC BY 2.0, steve_w; night-bus.png,
CC BY-SA 2.0, Alastair Rae), so those three carry their photo's license; see docs/amethyst/photos/CREDITS.md."""
import argparse
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import mockups as mk

ROOT = mk.ROOT
S = mk.S
PHOTOS = ROOT / "docs" / "amethyst" / "photos"


def photo(name, dim=1.0):
    """a stage photo without its band at the top (the header is drawn again)"""
    im = Image.open(PHOTOS / name).convert("RGB")
    a = np.asarray(im, np.float32).copy()
    a[:34] = a[34:68][::-1]                                    # the old label band, covered with the rows under it
    a *= dim
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def lighter(d, x, y, s, flame):
    """a hand holding a lighter up, and its flame"""
    d.rounded_rectangle([x - 5 * s, y, x + 5 * s, y + 22 * s], 3 * s, fill=mk.INK)          # the fist
    d.rectangle([x - 3 * s, y - 9 * s, x + 3 * s, y], fill=(60, 60, 70))                    # the lighter
    d.ellipse([x - 3 * s, y - 9 * s - flame * 2.2, x + 3 * s, y - 8 * s], fill=mk.SODIUM)  # the flame
    d.ellipse([x - 1.5 * s, y - 9 * s - flame * 1.4, x + 1.5 * s, y - 8.5 * s], fill=mk.SODIUM_L)


def rewind(f):
    img = photo("the-end.png", 0.8)
    r = mk.rng(11)
    for i in range(9):                                         # glows first, then the hands over them
        x = 16 + i * 26 + int(r.integers(-6, 7))
        img = mk.glow(img, (x, 178 - int(r.integers(0, 24))), 10, mk.SODIUM, 0.6)
    d = ImageDraw.Draw(img)
    r = mk.rng(11)
    for i in range(9):
        x = 16 + i * 26 + int(r.integers(-6, 7))
        y = 186 - int(r.integers(0, 24))
        lighter(d, x, y, 1, int(r.integers(3, 6)))
    d.rectangle([0, 214, S, S], fill=mk.INK)
    t = "REWIND!"
    w = d.textlength(t, font=mk.font(f, 44))
    for dx, dy, c in ((3, 3, mk.AM_D), (0, 0, mk.SODIUM_L)):   # the call, big, with a violet shadow
        d.text(((S - w) / 2 + dx, 70 + dy), t, font=mk.font(f, 44), fill=c)
    t = "COME AGAIN"
    w = d.textlength(t, font=mk.font(f, 18))
    d.text(((S - w) / 2, 122), t, font=mk.font(f, 18), fill=mk.AM_L)
    img = mk.posterize(img)
    img = mk.header(img, f, "FRIDAY", 7, 9, mk.SODIUM)
    return mk.footer(img, f, "SCL: THE CROWD WANTS IT", mk.SODIUM)


def shoutout(f):
    img = photo("night-bus.png", 0.9)
    d = ImageDraw.Draw(img)
    x0, y0 = 118, 86                                           # a 2000s phone, the text on its screen
    d.rounded_rectangle([x0, y0, x0 + 108, y0 + 132], 16, fill=(40, 40, 52), outline=(110, 110, 124), width=2)
    d.rounded_rectangle([x0 + 10, y0 + 14, x0 + 98, y0 + 78], 4, fill=(150, 190, 120))
    d.text((x0 + 15, y0 + 17), "1 NEW MESSAGE", font=mk.font(f, 11), fill=(30, 44, 24))
    for i, line in enumerate(("BIG UP THE", "E8 LOT. REWIND", "THAT ONE!! x")):
        d.text((x0 + 15, y0 + 32 + i * 14), line, font=mk.font(f, 12), fill=(20, 30, 16))
    for row in range(3):                                       # the keypad
        for col in range(3):
            cx, cy = x0 + 24 + col * 30, y0 + 92 + row * 12
            d.rounded_rectangle([cx - 10, cy - 4, cx + 10, cy + 4], 3, fill=(80, 80, 94))
    img = mk.posterize(img)
    img = mk.header(img, f, "NIGHT BUS", 8, 9, mk.SODIUM)
    return mk.footer(img, f, "FROM: TASHA, HACKNEY", mk.AM_L)


def dubplate(f):
    img = Image.new("RGB", (S, S), mk.INK)
    img = mk.glow(img, (120, 128), 70, mk.AM_D, 0.8)
    d = ImageDraw.Draw(img)
    cx, cy, rad = 120, 130, 84
    d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(22, 20, 26))          # the acetate
    for rr in range(rad - 4, 34, -3):                          # its grooves, catching the light on one side
        c = (44, 40, 52) if rr % 2 else (30, 28, 36)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=c)
    d.arc([cx - rad + 6, cy - rad + 6, cx + rad - 6, cy + rad - 6], 200, 250, fill=mk.AM_L, width=2)
    d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=(236, 228, 210))           # a plain white label
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=mk.INK)
    for t, px, y, c in (("FRIDAY", 13, cy - 27, (40, 30, 110)), ("VIP", 15, cy + 4, mk.RED),
                        ("1 OF 1", 10, cy + 19, (40, 30, 110))):          # written by hand, as they were
        w = d.textlength(t, font=mk.font(f, px))
        d.text((cx - w / 2, y), t, font=mk.font(f, px), fill=c)
    img = mk.posterize(img)
    img = mk.header(img, f, "DUBPLATE CUT", 7, 9, mk.SODIUM)
    return mk.footer(img, f, "3 REWINDS  •  FRIDAY HAS A VIP", mk.SODIUM)


def tapepack(f):
    img = Image.new("RGB", (S, S), (14, 12, 22))
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = 28, 44, 212, 214                          # the clamshell box
    d.rounded_rectangle([x0, y0, x1, y1], 8, fill=(30, 30, 38), outline=(120, 120, 132), width=2)
    cov = Image.new("RGB", (x1 - x0 - 20, y1 - y0 - 50), (0, 0, 0))                # its cover, airbrushed
    cd = ImageDraw.Draw(cov)
    w, h = cov.size
    for y in range(h):                                         # a violet sky over a moss-green planet
        t = y / h
        cd.line([(0, y), (w, y)], fill=(int(20 + 90 * t), int(10 + 20 * t), int(60 + 80 * t)))
    cd.ellipse([-40, h - 50, w + 40, h + 120], fill=mk.MOSS)
    cd.ellipse([-30, h - 46, w + 30, h + 110], fill=mk.MOSS_D)
    cd.polygon([(w / 2, 14), (w / 2 + 22, 46), (w / 2 + 12, 90), (w / 2 - 12, 90), (w / 2 - 22, 46)], fill=mk.AM)
    cd.polygon([(w / 2, 14), (w / 2 + 22, 46), (w / 2, 56), (w / 2 - 22, 46)], fill=mk.AM_L)
    r = mk.rng(12)
    for _ in range(40):
        cd.point((int(r.integers(0, w)), int(r.integers(0, h - 60))), fill=(240, 230, 250))
    cov = cov.filter(ImageFilter.GaussianBlur(1.1))            # the airbrush
    img.paste(cov, (x0 + 10, y0 + 10))
    img = mk.glow(img, (120, y0 + 30), 16, mk.AM_L, 0.4)
    d = ImageDraw.Draw(img)
    t = "AMETHYST  •  LIVE"
    tw = d.textlength(t, font=mk.font(f, 15))
    d.text(((S - tw) / 2, y1 - 36), t, font=mk.font(f, 15), fill=(246, 240, 236))
    t = "9 STAGES  •  1H 12M  •  14 REWINDS"
    tw = d.textlength(t, font=mk.font(f, 11))
    d.text(((S - tw) / 2, y1 - 18), t, font=mk.font(f, 11), fill=mk.AM_L)
    img = mk.posterize(img)
    return mk.header(img, f, "TAPE PACK", 1, 1, mk.AM_L)


def sleeve(f):
    img = photo("the-end.png", 0.35)
    d = ImageDraw.Draw(img)
    lines = [("2001", mk.SODIUM, 26), ("", None, 6),
             ("Fabric opened in Farringdon in", mk.AM_L, 14), ("1999 and kept Fridays for drum", mk.AM_L, 14),
             ("and bass: FABRICLIVE, and DJ", mk.AM_L, 14), ("Hype's Playaz from the start.", mk.AM_L, 14),
             ("", None, 6),
             ("May 2001: Dillinja and Lemon D", (230, 226, 236), 14),
             ("bring Valve, 52 subs of their own.", (230, 226, 236), 14)]
    y = 42
    for t, c, px in lines:
        if t:
            d.text((14, y), t, font=mk.font(f, px), fill=c)
        y += px + 5 if t else px
    img = mk.posterize(img)
    img = mk.header(img, f, "FRIDAY  •  SLEEVE NOTES", 7, 9, mk.SODIUM)
    return mk.footer(img, f, "HOME: BACK TO THE MUSIC", mk.SODIUM)


SCREENS = [("rewind", rewind), ("shoutout", shoutout), ("dubplate", dubplate), ("tapepack", tapepack),
           ("sleeve", sleeve)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--font")
    ap.add_argument("--out", default=str(ROOT / "docs" / "amethyst" / "rituals"))
    a = ap.parse_args()
    f = mk.find_font(a.font)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    shots = []
    for name, fn in SCREENS:
        im = fn(f)
        im.save(out / f"{name}.png")
        shots.append(im)
    gap = 8
    sheet = Image.new("RGB", (len(shots) * (S * 2 + gap) + gap, S * 2 + 2 * gap), (12, 10, 18))
    for i, im in enumerate(shots):
        sheet.paste(im.resize((S * 2, S * 2), Image.Resampling.NEAREST), (gap + i * (S * 2 + gap), gap))
    sheet.save(out / "sheet.png")
    print(f"{out}: {len(shots)} screens and sheet.png")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Mock screens for Amethyst, a drum and bass firmware idea for the FM-1 (docs/AMETHYST.md). Nothing here runs on
the FM-1: these are sketches at the screen's size (240 x 240), each cut down to 16 colors the way Album 01 cuts its
photos, so the looks can be compared before any firmware is written.

  python3 tools/amethyst/mockups.py [--font FONT.ttf] [--out docs/amethyst]

Writes one PNG a screen (at 1x, as on the FM-1) and sheet.png (all eight at 2x). The font is Barlow Semi Condensed
Bold if it can be found (Album's, from fm1-base), else Inter Tight from assets/fonts."""
import argparse
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
S = 240

# the palette everything is drawn from: wet black, amethyst, moss, sodium light, concrete
INK = (7, 6, 12)
NIGHT = (18, 14, 30)
AM_D, AM, AM_L = (58, 30, 96), (138, 82, 210), (206, 172, 248)
MOSS_D, MOSS, MOSS_L = (30, 44, 20), (84, 112, 44), (150, 182, 82)
SODIUM, SODIUM_L = (226, 140, 48), (255, 214, 150)
CONC_D, CONC = (44, 44, 50), (96, 96, 104)
BRICK = (92, 48, 38)
CYAN = (70, 220, 200)
RED = (220, 40, 52)


def font(path, px):
    return ImageFont.truetype(str(path), px)


def find_font(arg):
    if arg:
        return Path(arg)
    for p in [ROOT.parent / "joshbartlettband-web/album-fm1/base/assets/fonts/BarlowSemiCondensed-Bold.ttf",
              ROOT.parent / "album-fm1/base/assets/fonts/BarlowSemiCondensed-Bold.ttf"]:
        if p.exists():
            return p
    return ROOT / "assets/fonts/InterTight[wght].ttf"


def rng(seed):
    return np.random.default_rng(seed)


def posterize(img, colors=16):
    """16 colors, no dither: Album 01's flat look"""
    return img.convert("RGB").quantize(colors=colors, method=Image.Quantize.MEDIANCUT,
                                       dither=Image.Dither.NONE).convert("RGB")


def glow(img, xy, r, col, alpha=0.8):
    """a soft round light, added"""
    layer = Image.new("RGB", (S, S), (0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = xy
    d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    layer = layer.filter(ImageFilter.GaussianBlur(r * 0.6))
    a = np.asarray(img, dtype=np.float32) + np.asarray(layer, dtype=np.float32) * alpha
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def grain(img, amount, seed):
    a = np.asarray(img, dtype=np.float32)
    n = rng(seed).normal(0, amount, (S, S, 1))
    return Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8))


def waver(img, amp, seed):
    """the rows shifted sideways, as Album's photos waver while a note sounds"""
    a = np.asarray(img)
    out = a.copy()
    r = rng(seed)
    phase = r.uniform(0, 6.28)
    for y in range(S):
        dx = int(round(amp * math.sin(y / 9.0 + phase) * (0.6 + 0.4 * math.sin(y / 31.0))))
        out[y] = np.roll(a[y], dx, axis=0)
    return Image.fromarray(out)


def header(img, f, name, n, total, accent=AM_L):
    """Album 01's band at the top: the name left, the place in the set right"""
    a = np.asarray(img, dtype=np.float32)
    a[:34] = a[:34] * 0.45
    img = Image.fromarray(a.astype(np.uint8))
    d = ImageDraw.Draw(img)
    d.text((10, 8), name, font=font(f, 17), fill=(246, 240, 236))
    t = f"{n} / {total}"
    w = d.textlength(t, font=font(f, 13))
    d.text((S - 10 - w, 11), t, font=font(f, 13), fill=accent)
    return img


def footer(img, f, text, col=(246, 240, 236)):
    a = np.asarray(img, dtype=np.float32)
    a[S - 30:] = a[S - 30:] * 0.45
    img = Image.fromarray(a.astype(np.uint8))
    d = ImageDraw.Draw(img)
    d.text((10, S - 24), text, font=font(f, 15), fill=col)
    return img


# --- 1. a photo, Album 01 style: a canal under a brick bridge at night, moss on the walls --------------------------

def canal(f):
    img = Image.new("RGB", (S, S), NIGHT)
    d = ImageDraw.Draw(img)
    r = rng(1)
    for y in range(0, 150):                                    # sky, fog lit orange from the city
        t = y / 150
        d.line([(0, y), (S, y)], fill=tuple(int(NIGHT[i] * (1 - t) + (70, 44, 54)[i] * t) for i in range(3)))
    d.rectangle([0, 40, S, 150], fill=BRICK)                   # the bridge
    for y in range(40, 150, 6):                                # brick courses
        off = 0 if (y // 6) % 2 else 9
        for x in range(-off, S, 18):
            d.rectangle([x + 1, y + 1, x + 16, y + 5], fill=tuple(c + r.integers(-10, 12) for c in BRICK))
    d.ellipse([30, 70, 210, 250], fill=INK)                    # the arch
    d.rectangle([30, 160, 210, 170], fill=INK)
    for x in range(36, 205, 4):                                # moss down the arch's edge and the wall
        h = int(abs(r.normal(14, 9)))
        d.line([(x, 150), (x, 150 + h)], fill=MOSS if r.random() > .3 else MOSS_L)
    for _ in range(420):                                       # moss in the mortar, thickest low down
        x, y = r.integers(0, S), int(150 - abs(r.normal(0, 40)))
        if 30 < x < 210 and y > 90 or y < 40:
            continue
        d.ellipse([x, y, x + r.integers(3, 9), y + r.integers(2, 6)], fill=[MOSS_D, MOSS, MOSS_L][int(r.integers(0, 3))])
    d.rectangle([0, 170, S, S], fill=(14, 18, 26))             # the water
    img = glow(img, (120, 118), 18, SODIUM, 1.2)               # a lamp far down the tunnel
    img = glow(img, (120, 205), 26, SODIUM, 0.5)               # and in the water
    d = ImageDraw.Draw(img)
    for y in range(172, S, 3):                                 # its reflection, broken by ripples
        w = int(4 + (y - 170) * 0.4 + r.integers(0, 6))
        d.line([(120 - w, y), (120 + w, y)], fill=SODIUM if y % 2 else SODIUM_L)
    d.line([(0, 168), (S, 168)], fill=AM, width=2)             # the towpath's edge, lit violet
    img = waver(img, 3, 5)
    img = posterize(grain(img, 6, 2))
    return header(img, f, "CANAL", 1, 8, SODIUM)


# --- 2. a rave stage: a railway arch, lasers from the back, the crowd's heads --------------------------------------

def arches(f):
    img = Image.new("RGB", (S, S), INK)
    d = ImageDraw.Draw(img)
    for i in range(6):                                         # arches going back, smaller each time
        k = 1 - i * 0.15
        w, h = 230 * k, 260 * k
        x0, y0 = 120 - w / 2, 150 - h * 0.55
        c = tuple(int(v * (0.25 + 0.12 * i)) for v in AM)
        d.ellipse([x0, y0, x0 + w, y0 + h], outline=c, width=3)
    img = glow(img, (120, 112), 34, AM, 0.9)                   # fog lit from the stage
    lay = Image.new("RGB", (S, S), (0, 0, 0))
    ld = ImageDraw.Draw(lay)
    for a in np.linspace(-1.1, 1.1, 9):                        # lasers fanning out from one point
        x2, y2 = 120 + 300 * math.sin(a), 112 - 300 * math.cos(a) * 0.35
        ld.line([(120, 112), (x2, y2)], fill=CYAN if abs(a) > .3 else MOSS_L, width=2)
    lay = lay.filter(ImageFilter.GaussianBlur(1.2))
    img = Image.fromarray(np.clip(np.asarray(img, np.float32) + np.asarray(lay, np.float32) * 1.4, 0, 255)
                          .astype(np.uint8))
    d = ImageDraw.Draw(img)
    d.rectangle([84, 118, 156, 128], fill=CONC_D)              # the decks
    d.rectangle([110, 100, 130, 118], fill=INK)                # the DJ
    d.ellipse([112, 88, 128, 104], fill=INK)
    for y in range(150, S):                                    # haze over the floor, lit from the stage
        t = (y - 150) / 90
        d.line([(0, y), (S, y)], fill=tuple(int(c * (0.55 - 0.3 * t)) for c in AM))
    r = rng(3)
    for row, y in enumerate((178, 192, 208, 226)):             # heads and raised hands
        for x in range(-10, S + 10, 16 - row):
            x += int(r.integers(-4, 5))
            s = 9 + row * 3
            d.ellipse([x - s, y - s, x + s, y + s], fill=INK)
            if r.random() < 0.12:
                d.line([(x + 4, y - s), (x + 10, y - s - 26)], fill=INK, width=4)
    img = posterize(img)
    img = header(img, f, "ARCHES", 2, 8, CYAN)
    return footer(img, f, "174  •  DROP IN 4", CYAN)


# --- 3. pirate radio: a tuning dial, a tower block with a light on top ---------------------------------------------

def pirate(f):
    img = Image.new("RGB", (S, S), NIGHT)
    d = ImageDraw.Draw(img)
    d.rectangle([150, 76, 205, 160], fill=CONC_D)              # the tower block
    r = rng(4)
    for y in range(84, 156, 8):
        for x in range(155, 202, 8):
            if r.random() < 0.35:
                d.rectangle([x, y, x + 4, y + 4], fill=SODIUM if r.random() > .3 else AM_L)
    d.line([(180, 76), (180, 54)], fill=CONC, width=2)         # the aerial
    img = glow(img, (180, 54), 6, RED, 1.5)
    d = ImageDraw.Draw(img)
    for i, rad in enumerate((14, 24, 34)):                     # the signal going out
        d.arc([180 - rad, 54 - rad, 180 + rad, 54 + rad], 200, 340, fill=tuple(int(c * (1 - i * .25)) for c in RED))
    d.rectangle([0, 160, S, S], fill=(24, 20, 34))             # the dial
    d.rectangle([10, 172, 230, 214], outline=AM, width=2)
    for i in range(0, 21):
        x = 18 + i * 10.2
        h = 10 if i % 5 == 0 else 5
        d.line([(x, 176), (x, 176 + h)], fill=AM_L)
    for i, mhz in enumerate(("88", "92", "96", "100", "104")):
        d.text((14 + i * 51, 194), mhz, font=font(f, 13), fill=AM_L)
    d.line([(147, 168), (147, 218)], fill=RED, width=3)        # the needle, between stations
    a = np.asarray(img, np.float32)                            # static over the top half: between two stations
    n = r.normal(0, 22, (160, S, 1)) * (r.random((160, 1, 1)) > .8)
    a[:160] += n
    img = posterize(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)))
    img = header(img, f, "PIRATE", 3, 8, RED)
    return footer(img, f, "99.7  TOWER BLOCK FM", AM_L)


# --- 4. the night bus: rain on the window, the city going past ----------------------------------------------------

def nightbus(f):
    img = Image.new("RGB", (S, S), INK)
    r = rng(5)
    for _ in range(26):                                        # lights outside, out of focus
        x, y = int(r.integers(0, S)), int(r.integers(60, 200))
        img = glow(img, (x, y), int(r.integers(5, 16)), [SODIUM, AM, CYAN, RED, SODIUM_L][int(r.integers(0, 5))], 1.3)
    img = img.filter(ImageFilter.GaussianBlur(2))
    d = ImageDraw.Draw(img)
    for _ in range(70):                                        # drops on the glass, and their trails
        x, y = int(r.integers(0, S)), int(r.integers(30, S))
        rad = int(r.integers(1, 4))
        d.line([(x, y - int(r.integers(6, 30))), (x, y)], fill=(70, 66, 92), width=1)
        d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=(150, 140, 180))
    d.rectangle([0, 206, S, S], fill=(20, 18, 28))             # the window's frame and a seat back
    d.rectangle([0, 0, 6, S], fill=(20, 18, 28))
    d.rounded_rectangle([150, 214, 250, 260], 10, fill=AM_D)
    img = posterize(img)
    return header(img, f, "NIGHT BUS", 4, 8, SODIUM)


# --- 5. moss and amethyst: crystals and moss grow over concrete while you play -------------------------------------

def moss(f):
    img = Image.new("RGB", (S, S), CONC_D)
    d = ImageDraw.Draw(img)
    for y in range(0, S, 60):                                  # concrete panels and their shuttering lines
        for x in range(0, S, 80):
            d.rectangle([x + 1, y + 1, x + 78, y + 58], fill=CONC if (x // 80 + y // 60) % 2 else (84, 84, 92))
            for yy in range(y + 8, y + 58, 9):
                d.line([(x + 3, yy), (x + 76, yy)], fill=(74, 74, 82))
    r = rng(6)
    grid = np.zeros((60, 60), bool)                            # moss: a growth from the bottom corner, cell by cell
    grid[59, ::7] = True
    for _ in range(9000):
        ys, xs = np.nonzero(grid)
        i = r.integers(0, len(ys))
        ny, nx = ys[i] + r.integers(-1, 2), xs[i] + r.integers(-1, 2)
        if 0 <= ny < 60 and 0 <= nx < 60 and r.random() < (ny - 20) / 60:
            grid[ny, nx] = True
    for y, x in zip(*np.nonzero(grid)):
        c = [MOSS_D, MOSS, MOSS_L][int(r.integers(0, 3))]
        d.rectangle([x * 4, y * 4, x * 4 + 3, y * 4 + 3], fill=c)

    def crystal(cx, base, h, w, tilt):
        top = (cx + tilt, base - h)
        d.polygon([(cx - w, base), (cx - w + tilt * .6, base - h * .75), top, (cx + tilt * .3, base)], fill=AM_D)
        d.polygon([(cx + tilt * .3, base), top, (cx + w + tilt * .6, base - h * .75), (cx + w, base)], fill=AM)
        d.line([top, (cx + tilt * .3, base)], fill=AM_L, width=1)

    for cx, h, w, t in [(70, 70, 12, -10), (92, 100, 14, 4), (112, 60, 10, 14), (52, 40, 9, -16), (130, 34, 8, 18)]:
        crystal(cx, 214, h, w, t)
    img = glow(img, (92, 150), 30, AM, 0.45)
    img = posterize(img)
    img = header(img, f, "MOSS", 5, 8, MOSS_L)
    return footer(img, f, "BAR 12  •  5 CRYSTALS", MOSS_L)


# --- 6. the chop: the break drawn as its slices, one for each black key ---------------------------------------------

def chop(f):
    img = Image.new("RGB", (S, S), INK)
    d = ImageDraw.Draw(img)
    r = rng(7)
    hits = [i * 10 for i in range(12)]                         # 11 slices across the bar
    env = np.zeros(S)
    for i, h in enumerate(hits[:-1]):
        x0 = 10 + h * 2
        for x in range(x0, 10 + hits[i + 1] * 2):
            env[x] = math.exp(-(x - x0) / (6 if i % 4 == 2 else 14))
    lit = 6
    for x in range(10, 230):
        a = env[x] * (0.55 + 0.45 * r.random())
        top, bot = int(120 - a * 62), int(120 + a * 62)
        sl = max(i for i, h in enumerate(hits[:-1]) if 10 + h * 2 <= x)
        col = AM_L if sl == lit else (AM if sl % 2 else (102, 64, 160))
        d.line([(x, top), (x, bot)], fill=col)
    for i, h in enumerate(hits):
        d.line([(10 + h * 2, 56), (10 + h * 2, 184)], fill=CONC_D)
    names = ["F#", "G#", "A#", "C#", "D#", "F#", "G#", "A#", "C#", "D#", "F#"]
    for i, n in enumerate(names):                              # which black key plays which slice
        x = 10 + (hits[i] + hits[i + 1])
        w = d.textlength(n, font=font(f, 12))
        d.text((x - w / 2, 192), n, font=font(f, 12), fill=SODIUM if i == lit else CONC)
    d.rectangle([10 + hits[lit] * 2, 52, 10 + hits[lit + 1] * 2, 56], fill=SODIUM)
    img = header(img, f, "BREAK 3  •  KEEPER", 6, 8, SODIUM)
    return footer(img, f, "CHOP  7 / 11", SODIUM)


# --- 7. CCTV: an underpass on a grainy camera, the time in the corner ---------------------------------------------

def cctv(f):
    img = Image.new("RGB", (S, S), (16, 20, 18))
    d = ImageDraw.Draw(img)
    d.polygon([(0, 40), (240, 40), (170, 110), (70, 110)], fill=(40, 46, 42))      # the ceiling
    d.polygon([(0, 240), (240, 240), (170, 150), (70, 150)], fill=(52, 58, 52))    # the floor
    d.polygon([(0, 40), (70, 110), (70, 150), (0, 240)], fill=(32, 38, 34))         # the walls
    d.polygon([(240, 40), (170, 110), (170, 150), (240, 240)], fill=(36, 42, 38))
    d.rectangle([70, 110, 170, 150], fill=(120, 140, 120))     # the way out, bright
    for i in range(4):                                         # lights on the ceiling
        t = i / 4
        x0, x1 = 20 + 60 * t, 220 - 60 * t
        y = 50 + 55 * t
        d.line([(x0 + 20, y), (x1 - 20, y)], fill=(180, 200, 170), width=max(1, 4 - i))
    d.rectangle([108, 120, 116, 146], fill=(10, 12, 10))       # someone walking out
    d.ellipse([107, 112, 117, 122], fill=(10, 12, 10))
    r = rng(8)
    for y, x in zip(r.integers(150, 236, 40), r.integers(0, 70, 40)):              # moss in the corner where it's damp
        d.ellipse([x, y, x + 6, y + 4], fill=MOSS)
    img = grain(img, 14, 9)
    a = np.asarray(img, np.float32)
    a[::2] *= 0.75                                             # scan lines
    a[:, :, 0] *= 0.8                                          # the green cast of a cheap camera
    a[:, :, 2] *= 0.85
    img = posterize(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)))
    d = ImageDraw.Draw(img)
    d.text((10, 10), "CAM 04", font=font(f, 15), fill=(220, 230, 210))
    d.text((150, 10), "03:12:44", font=font(f, 15), fill=(220, 230, 210))
    d.ellipse([10, 218, 18, 226], fill=RED)
    d.text((24, 213), "REC", font=font(f, 15), fill=(220, 230, 210))
    return img


# --- 8. hello: the boot screen -------------------------------------------------------------------------------------

def hello(f):
    img = Image.new("RGB", (S, S), INK)
    img = glow(img, (120, 104), 54, AM_D, 1.0)
    d = ImageDraw.Draw(img)
    pts = [(120, 40), (152, 78), (140, 150), (100, 150), (88, 78)]  # one cut stone
    d.polygon(pts, fill=AM)
    d.polygon([(120, 40), (152, 78), (120, 92), (88, 78)], fill=AM_L)
    d.polygon([(88, 78), (120, 92), (100, 150)], fill=AM_D)
    d.polygon([(152, 78), (120, 92), (140, 150)], fill=(110, 62, 176))
    r = rng(10)
    for x in range(40, 200, 3):                                # moss under it
        h = int(abs(r.normal(8, 5)))
        d.line([(x, 160), (x, 160 - h)], fill=[MOSS_D, MOSS, MOSS_L][int(r.integers(0, 3))], width=2)
    t = "AMETHYST"
    w = d.textlength(t, font=font(f, 30))
    d.text(((S - w) / 2, 172), t, font=font(f, 30), fill=(246, 240, 236))
    t = "DRUM AND BASS FOR THE FM-1"
    w = d.textlength(t, font=font(f, 12))
    d.text(((S - w) / 2, 210), t, font=font(f, 12), fill=AM_L)
    return posterize(img)


SCREENS = [("canal", canal), ("arches", arches), ("pirate", pirate), ("nightbus", nightbus),
           ("moss", moss), ("chop", chop), ("cctv", cctv), ("hello", hello)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--font")
    ap.add_argument("--out", default=str(ROOT / "docs" / "amethyst"))
    a = ap.parse_args()
    f = find_font(a.font)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    shots = []
    for name, fn in SCREENS:
        im = fn(f)
        im.save(out / f"{name}.png")
        shots.append(im)
    gap = 8
    sheet = Image.new("RGB", (4 * S * 2 + 5 * gap, 2 * S * 2 + 3 * gap), (12, 10, 18))
    for i, im in enumerate(shots):
        x, y = gap + (i % 4) * (S * 2 + gap), gap + (i // 4) * (S * 2 + gap)
        sheet.paste(im.resize((S * 2, S * 2), Image.Resampling.NEAREST), (x, y))
    sheet.save(out / "sheet.png")
    print(f"{out}: {len(shots)} screens and sheet.png, font {f.name}")


if __name__ == "__main__":
    main()

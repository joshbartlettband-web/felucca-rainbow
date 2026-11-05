#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Mock screens in kipatchi's look for Amethyst: overgrown steampunk (moss and verdigris over brass and copper, after
the way Amon Tobin's records feel) on a retro-futurist grunge display (lettered panels, two-line labels, circuit
traces, torn paper notes). Sketches at the FM-1's size, cut to 16 colors. See docs/AMETHYST.md, section 6.

  python3 tools/amethyst/overgrown.py [--font FONT.ttf] [--out docs/amethyst/overgrown]

The hello's four panels use the Commons photos in docs/amethyst/photos/ (credits in CREDITS.md there); its file
carries the strictest of their licenses, CC BY-SA 2.0."""
import argparse
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import mockups as mk

ROOT = mk.ROOT
S = mk.S
PHOTOS = ROOT / "docs" / "amethyst" / "photos"
BRASS, BRASS_D = (176, 150, 70), (104, 84, 36)
COPPER, COPPER_D = (184, 110, 56), (100, 54, 28)
VERDI, VERDI_L = (60, 146, 126), (130, 200, 176)
PAPER, PAPER_D = (214, 196, 160), (150, 128, 96)
OFF = (232, 222, 204)


def poster(img, keep):
    """16 colors with a few kept, as Album's photos keep theirs: 16 - len(keep) found by median cut, then each pixel
    to its nearest"""
    q = img.convert("RGB").quantize(colors=16 - len(keep), method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    pal = np.array(q.getpalette()[:3 * (16 - len(keep))]).reshape(-1, 3)
    pal = np.vstack([pal, np.array(keep)]).astype(np.int32)
    px = np.asarray(img.convert("RGB")).reshape(-1, 3).astype(np.int32)
    idx = ((px[:, None, :] - pal[None, :, :]) ** 2).sum(2).argmin(1)
    return Image.fromarray(pal[idx].reshape(S, S, 3).astype(np.uint8))


def grunge(img, seed, amount=6):
    """grain, a few scratches, the corners darker"""
    r = mk.rng(seed)
    a = np.asarray(img, np.float32)
    a += r.normal(0, amount, (S, S, 1))
    yy, xx = np.mgrid[0:S, 0:S]
    a *= (1 - 0.3 * (((xx - S / 2) ** 2 + (yy - S / 2) ** 2) / (S * S / 2)))[..., None]
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    for _ in range(14):
        x, y = int(r.integers(0, S)), int(r.integers(0, S))
        d.line([(x, y), (x + int(r.integers(-30, 30)), y + int(r.integers(10, 60)))], fill=(150, 140, 120), width=1)
    return img


def label(d, f, x, y, title, sub, w=None):
    """the two-line label in a panel's corner: a bold name, a small line under it"""
    tw = max(d.textlength(title, font=mk.font(f, 14)), d.textlength(sub, font=mk.font(f, 9))) + 10
    d.rectangle([x, y, x + (w or tw), y + 29], fill=(14, 12, 12), outline=(90, 80, 64))
    d.text((x + 5, y + 2), title, font=mk.font(f, 14), fill=OFF)
    d.text((x + 5, y + 17), sub, font=mk.font(f, 9), fill=PAPER)


def letter(d, f, x, y, ch):
    d.rectangle([x, y, x + 13, y + 14], fill=PAPER)
    d.text((x + 3, y), ch, font=mk.font(f, 12), fill=(20, 16, 12))


def note(img, f, x, y, lines, angle, seed):
    """a torn paper note, written on by hand, at an angle"""
    r = mk.rng(seed)
    w = 12 + max(int(ImageDraw.Draw(img).textlength(t, font=mk.font(f, 11))) for t in lines)
    h = 10 + 13 * len(lines)
    tile = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    edge = [(0, 0)] + [(i, int(r.integers(0, 3))) for i in range(4, w, 4)] + [(w, 0), (w, h)] + \
           [(i, h - int(r.integers(0, 4))) for i in range(w - 4, 0, -4)] + [(0, h)]
    td.polygon(edge, fill=PAPER + (255,))
    for i, t in enumerate(lines):
        td.text((6, 4 + i * 13), t, font=mk.font(f, 11), fill=(50, 36, 24, 255))
    tile = tile.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    img.paste(tile, (x, y), tile)
    return img


def traces(d, seed, box, col=COPPER_D):
    """circuit-board traces: lines that turn at right angles and end in a pad"""
    r = mk.rng(seed)
    x0, y0, x1, y1 = box
    for _ in range(18):
        x, y = int(r.integers(x0, x1)), int(r.integers(y0, y1))
        pts = [(x, y)]
        for _ in range(3):
            if r.random() < 0.5:
                x = int(np.clip(x + r.integers(-30, 31), x0, x1))
            else:
                y = int(np.clip(y + r.integers(-30, 31), y0, y1))
            pts.append((x, y))
        d.line(pts, fill=col, width=1)
        d.ellipse([x - 2, y - 2, x + 2, y + 2], outline=BRASS, width=1)


def gear(d, cx, cy, r_out, teeth, col, dark, hole=0.35, rot=0.0):
    pts = []
    for i in range(teeth * 2):
        a = rot + i * math.pi / teeth
        rr = r_out if i % 2 == 0 else r_out * 0.82
        for da in (-0.5, 0.5):
            aa = a + da * math.pi / teeth * 0.9
            pts.append((cx + rr * math.cos(aa), cy + rr * math.sin(aa)))
    d.polygon(pts, fill=col, outline=dark)
    ri = r_out * 0.62
    d.ellipse([cx - ri, cy - ri, cx + ri, cy + ri], outline=dark, width=2)
    for k in range(5):                                         # spokes
        a = rot + k * 2 * math.pi / 5
        d.line([(cx, cy), (cx + ri * math.cos(a), cy + ri * math.sin(a))], fill=dark, width=3)
    rh = r_out * hole * 0.5
    d.ellipse([cx - rh, cy - rh, cx + rh, cy + rh], fill=mk.INK)


def moss_on(d, seed, box, n):
    """moss in clumps, with verdigris where it meets the metal"""
    r = mk.rng(seed)
    x0, y0, x1, y1 = box
    for _ in range(n):
        x, y = int(r.integers(x0, x1)), int(r.integers(y0, y1))
        s = int(r.integers(2, 6))
        c = [mk.MOSS_D, mk.MOSS, mk.MOSS_L, VERDI, mk.MOSS][int(r.integers(0, 5))]
        d.ellipse([x - s, y - s, x + s, y + s * 0.7], fill=c)


def clockwork(f):
    img = Image.new("RGB", (S, S), (20, 16, 14))
    d = ImageDraw.Draw(img)
    traces(d, 21, (0, 0, S, S), (60, 40, 26))
    gear(d, 70, 92, 58, 14, BRASS, BRASS_D, rot=0.2)
    gear(d, 160, 70, 40, 11, COPPER, COPPER_D, rot=0.5)
    gear(d, 172, 160, 50, 13, (120, 112, 90), (60, 54, 40), rot=0.1)
    gear(d, 92, 182, 30, 9, COPPER, COPPER_D, rot=0.9)
    r = mk.rng(22)
    for _ in range(6):                                         # wires, hanging loose
        x0 = int(r.integers(0, S))
        d.line([(x0, 0), (x0 + int(r.integers(-40, 40)), 120), (int(r.integers(0, S)), S)],
               fill=[(150, 40, 40), (40, 90, 60), (160, 120, 40)][int(r.integers(0, 3))], width=2)
    moss_on(d, 23, (0, 120, S, S), 260)                        # moss climbing up from the bottom
    moss_on(d, 24, (20, 40, 130, 150), 70)                     # and over the big gear
    for cx, h, w, t in [(150, 70, 11, -6), (168, 98, 13, 3), (186, 58, 10, 10)]:   # amethyst growing out of it
        top = (cx + t, 214 - h)
        d.polygon([(cx - w, 214), top, (cx + t * .3, 214)], fill=mk.AM_D)
        d.polygon([(cx + t * .3, 214), top, (cx + w, 214)], fill=mk.AM)
        d.line([top, (cx + t * .3, 214)], fill=mk.AM_L, width=1)
    img = mk.glow(img, (168, 168), 26, mk.AM, 0.35)
    img = grunge(img, 25)
    img = poster(img, [mk.AM, mk.AM_L, mk.AM_D, VERDI, mk.MOSS_L])
    d = ImageDraw.Draw(img)
    letter(d, f, 220, 6, "A")
    label(d, f, 8, 202, "CLOCKWORK", "OVERGROWN, STILL TURNING")
    return note(img, f, 8, 8, ["the machine", "under the moss", "still keeps time"], 4, 26)


def roof(f):
    img = Image.new("RGB", (S, S), (16, 14, 20))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, S, 120], fill=(24, 22, 34))
    traces(d, 31, (0, 0, S, 120), (54, 44, 70))
    d.rectangle([20, 70, 110, 240], fill=(40, 38, 46))         # the tower block, its lit windows
    r = mk.rng(32)
    for y in range(80, 236, 9):
        for x in range(26, 104, 9):
            if r.random() < 0.3:
                d.rectangle([x, y, x + 4, y + 4], fill=mk.SODIUM)
    d.line([(64, 70), (64, 26)], fill=(120, 120, 128), width=2)  # the aerial, wired up by hand
    for k in range(4):
        d.line([(54, 34 + k * 8), (74, 34 + k * 8)], fill=(120, 120, 128), width=1)
    d.line([(64, 40), (130, 150), (180, 168)], fill=(150, 40, 40), width=2)
    img = mk.glow(img, (64, 26), 7, mk.RED, 1.5)
    d = ImageDraw.Draw(img)
    x0, y0 = 128, 128                                          # the ON AIR box, wires coming out of it
    img = mk.glow(img, (x0 + 50, y0 + 22), 34, mk.RED, 0.5)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0, y0, x0 + 100, y0 + 44], 5, fill=(60, 16, 20), outline=COPPER, width=2)
    d.text((x0 + 12, y0 + 6), "ON AIR", font=mk.font(f, 26), fill=(255, 96, 96))
    for i in range(0, 110, 2):                                 # a waveform, on a scrap of screen
        h = int(8 * abs(math.sin(i * 0.31)) * (1 + math.sin(i * 0.07)))
        d.line([(124 + i, 196 - h), (124 + i, 196 + h)], fill=VERDI_L)
    moss_on(d, 33, (20, 200, 110, 240), 60)
    img = grunge(img, 34)
    img = poster(img, [(255, 96, 96), (60, 16, 20), mk.RED, VERDI_L, mk.SODIUM])
    d = ImageDraw.Draw(img)
    letter(d, f, 220, 6, "B")
    label(d, f, 124, 8, "ROOF", "STILL BROADCASTING, 1992")
    return note(img, f, 140, 60, ["London, 3 AM.", "Still on air."], -6, 35)


def hello(f):
    img = Image.new("RGB", (S, S), (18, 14, 12))
    d = ImageDraw.Draw(img)
    traces(d, 41, (0, 0, S, S))
    panels = [("night-bus.png", "A", "NIGHT BUS", "THE N-ROUTE HOME"), ("the-end.png", "B", "FRIDAY", "THE DOORS AT 3 AM"),
              ("heygate.png", "C", "ROOF", "STILL BROADCASTING"), ("abney-park.png", "D", "MOSS", "OVERGROWN")]
    boxes = [(6, 6, 116, 112), (124, 6, 234, 112), (6, 120, 116, 226), (124, 120, 234, 226)]
    for (name, ch, t, sub), (x0, y0, x1, y1) in zip(panels, boxes):
        ph = Image.open(PHOTOS / name).convert("RGB").crop((0, 40, 240, 240)).resize((x1 - x0, y1 - y0))
        img.paste(ph, (x0, y0))
        d.rectangle([x0, y0, x1, y1], outline=(110, 96, 70), width=2)
    img = grunge(img, 42, 5)
    img = poster(img, [mk.MOSS_L, mk.SODIUM, mk.AM_L])
    d = ImageDraw.Draw(img)
    for (name, ch, t, sub), (x0, y0, x1, y1) in zip(panels, boxes):
        letter(d, f, x1 - 15, y0 + 2, ch)
        d.rectangle([x0 + 2, y1 - 24, x1 - 2, y1 - 2], fill=(14, 12, 12))
        d.text((x0 + 5, y1 - 24), t, font=mk.font(f, 12), fill=OFF)
        d.text((x0 + 5, y1 - 12), sub, font=mk.font(f, 8), fill=PAPER)
    img = note(img, f, 64, 34, ["London pirate radio,", "rainy alleys at 3 AM.", "AMETHYST"], -4, 43)
    d = ImageDraw.Draw(img)
    t = "JOSH & KIPATCHI"
    w = d.textlength(t, font=mk.font(f, 10))
    d.text(((S - w) / 2, 228), t, font=mk.font(f, 10), fill=PAPER)
    return img


SCREENS = [("hello", hello), ("clockwork", clockwork), ("roof", roof)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--font")
    ap.add_argument("--out", default=str(ROOT / "docs" / "amethyst" / "overgrown"))
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

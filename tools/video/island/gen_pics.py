#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""The island film's pictures: the cast's 48 x 48 art (tools/gen_kid_art.py) and the toy's 5 x 7 font (kid.c KID_FONT)
as pics.js, for world.js to build its voxel friends and letters from.
  python3 tools/video/island/gen_pics.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import gen_kid_art as g                                       # noqa: E402

# the films' cast: the key world.js uses, the friend's name (a stand-in's too), and a hat from the toy's (a costume), if any
CAST = {"STAR": "STAR", "DUCKY": "DUCKY", "KITTY": "KITTY", "BUNNY": "BUNNY", "ELEPHANT": "ELEPHANT", "BEAR": "BEAR",
        "FROG": "FROG", "APRIL": "APRIL", "OWL": "OWL", "PEACOCK": "PEACOCK", "BEATBOT": "BEAT BOT", "SHEEP": "SHEEP",
        # Halloween (halloween.mjs): the spooky friends, and the first film's friends in costume
        "PUMPKIN": "PUMPKIN", "GHOST": "GHOST", "BAT": "BAT", "SPIDER": "SPIDER", "WOLF": "WOLF", "SKELETON": "SKELETON",
        "SLIMY": "SLIMY", "FLYTRAP": "FLYTRAP", "SCIENTIST": "SCIENTIST",
        "DUCKY_WIZARD": ("DUCKY", "WIZARD"), "KITTY_WIZARD": ("KITTY", "WIZARD"), "BUNNY_TOPHAT": ("BUNNY", "TOP HAT"),
        "FROG_CROWN": ("FROG", "CROWN"), "APRIL_WESTERN": ("APRIL", "WESTERN"),
        # The Bear and the Balloon (honey.mjs): Bear, Bear covered in mud, the bees' Bee, the Butterfly, and Robin (kid())
        "BEE": "BEE", "BUTTERFLY": "BUTTERFLY", "BEAR_MUD": "BEAR MUD", "ROBIN": "ROBIN"}


def kid():
    """Robin, a child in a yellow smock: drawn for the films in the toy's way (gen_kid_art.Pic), not one of the toy's friends"""
    p = g.Pic()
    p.rect(18, 39, 21, 43, "tan"); p.rect(26, 39, 29, 43, "tan")                 # legs
    p.ell(19, 44, 3, 2, "red"); p.ell(28, 44, 3, 2, "red")                        # shoes
    p.rect(16, 34, 31, 39, "blue"); p.rect(23, 37, 24, 39, "dblue")               # shorts
    p.poly([(17, 23), (30, 23), (34, 36), (13, 36)], "yellow")                    # the smock
    p.poly([(27, 23), (30, 23), (34, 36), (30, 36)], "dyellow")
    p.poly([(17, 25), (11, 33), (13, 35), (18, 29)], "yellow"); p.ell(12, 35, 2, 2, "tan")   # arms, hands
    p.poly([(30, 25), (36, 33), (34, 35), (29, 29)], "dyellow"); p.ell(35, 35, 2, 2, "tan")
    p.rect(20, 23, 27, 25, "white")                                               # a collar
    p.ball(24, 14, 11, 10, "tan", "dtan")                                         # head
    p.ell(24, 8, 11, 6, "brown")                                                  # hair, with a fringe
    p.poly([(13, 9), (14, 14), (17, 10), (20, 13), (23, 9), (26, 13), (29, 10), (32, 13), (35, 9), (35, 6), (13, 6)], "brown")
    p.eye(20, 15, 3); p.eye(28, 15, 3)
    p.smile(24, 20, 2)
    p.cheek(16, 19); p.cheek(32, 19)
    return p.done()


def bear_mud():
    """the Bear, rolled in mud: a little black cloud (its eyes and cheeks still its own)"""
    p = dict(g.FRIENDS)["BEAR"]()
    mud = {g.C["brown"]: (70, 56, 52), g.C["dbrown"]: (44, 34, 32), g.C["tan"]: (98, 82, 74), g.C["dtan"]: (80, 64, 58)}
    im = p.im
    for y in range(im.height):
        for x in range(im.width):
            r, gg, b, a = im.getpixel((x, y))
            if a and (r, gg, b) in mud:
                im.putpixel((x, y), mud[(r, gg, b)] + (255,))
    return p


def with_hat(name, im, hat):
    """the picture with a hat of the toy's on, as kid.c draws it (KID_HAT_AT): HAT_UP rows of headroom over it"""
    sprite = g.hat_sprite(dict(g.HATS)[hat])
    cx, y, hw = g.hat_anchor(name, im)
    hh = g.HAT_H * hw // g.HAT_W
    out = g.Image.new("RGBA", (g.N, g.N + g.HAT_UP), (0, 0, 0, 0))
    out.paste(im, (0, g.HAT_UP))
    for ry in range(-g.HAT_UP, g.N):
        for rx in range(g.N):
            hx, hy = rx - (cx - hw // 2), ry - (y - hh)
            if 0 <= hx < hw and 0 <= hy < hh:
                px = sprite.getpixel((hx * g.HAT_W // hw, hy * g.HAT_W // hw))
                if px[3]:
                    out.putpixel((rx, ry + g.HAT_UP), px)
    return out


def main():
    fn = dict(g.FRIENDS + list(g.STAND_INS.values()) + [("ROBIN", kid), ("BEAR MUD", bear_mud)])
    shimmer = [g.C[k] for k in g.SHIMMER]
    out = {}
    for key, who in CAST.items():
        name, hat = (who, None) if isinstance(who, str) else who
        im = fn[name]().im
        if hat:
            im = with_hat(name, im, hat)
        w, h = im.size
        pal, idx = [], []
        for y in range(h):
            for x in range(w):
                r, gg, b, a = im.getpixel((x, y))
                if not a:
                    idx.append(0)
                    continue
                if (r, gg, b) not in pal:
                    pal.append((r, gg, b))
                idx.append(pal.index((r, gg, b)) + 1)
        out[key] = {"w": w, "h": h, "pal": ["#%02x%02x%02x" % c for c in pal], "px": "".join(chr(48 + i) for i in idx),
                    "shim": [pal.index(c) + 1 for c in shimmer if c in pal]}
    src = (ROOT / "firmware/src/kid.c").read_text()
    i = src.index("static const uint8_t KID_FONT[][7] = {")
    j = src.index("/* accented", i)
    rows = re.findall(r"\{((?:0x[0-9A-F]{2}, ){6}0x[0-9A-F]{2})\}", src[i:j])
    font = {ch: [int(v, 16) for v in r.split(", ")] for ch, r in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ13#!58-?794", rows)}
    # a few the toy has no need of, in its style, for the films' captions and credits
    font.update({"0": [0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E], "2": [0x0E, 0x11, 0x01, 0x02, 0x04, 0x08, 0x1F],
                 "6": [0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E], ".": [0, 0, 0, 0, 0, 0x0C, 0x0C],
                 ",": [0, 0, 0, 0, 0x0C, 0x04, 0x08], "'": [0x04, 0x04, 0x08, 0, 0, 0, 0]})
    dest = Path(__file__).with_name("pics.js")
    dest.write_text("export const PICS = " + json.dumps(out) + ";\nexport const FONT = " + json.dumps(font) +
                    ';\nexport const OUTLINE = "#341a3a";\n')
    print(f"{len(out)} pictures, {len(font)} letters -> {dest}")


if __name__ == "__main__":
    main()

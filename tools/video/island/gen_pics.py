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

CAST = {"STAR": "STAR", "DUCKY": "DUCKY", "KITTY": "KITTY", "BUNNY": "BUNNY", "ELEPHANT": "ELEPHANT", "BEAR": "BEAR",
        "FROG": "FROG", "APRIL": "APRIL", "OWL": "OWL", "PEACOCK": "PEACOCK", "BEATBOT": "BEAT BOT", "SHEEP": "SHEEP"}


def main():
    fn = dict(g.FRIENDS)
    shimmer = [g.C[k] for k in g.SHIMMER]
    out = {}
    for key, name in CAST.items():
        im = fn[name]().im
        pal, idx = [], []
        for y in range(48):
            for x in range(48):
                r, gg, b, a = im.getpixel((x, y))
                if not a:
                    idx.append(0)
                    continue
                if (r, gg, b) not in pal:
                    pal.append((r, gg, b))
                idx.append(pal.index((r, gg, b)) + 1)
        out[key] = {"pal": ["#%02x%02x%02x" % c for c in pal], "px": "".join(chr(48 + i) for i in idx),
                    "shim": [pal.index(c) + 1 for c in shimmer if c in pal]}
    src = (ROOT / "firmware/src/kid.c").read_text()
    i = src.index("static const uint8_t KID_FONT[][7] = {")
    j = src.index("/* accented", i)
    rows = re.findall(r"\{((?:0x[0-9A-F]{2}, ){6}0x[0-9A-F]{2})\}", src[i:j])
    font = {ch: [int(v, 16) for v in r.split(", ")] for ch, r in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ13#!58-?794", rows)}
    dest = Path(__file__).with_name("pics.js")
    dest.write_text("export const PICS = " + json.dumps(out) + ";\nexport const FONT = " + json.dumps(font) +
                    ';\nexport const OUTLINE = "#341a3a";\n')
    print(f"{len(out)} pictures, {len(font)} letters -> {dest}")


if __name__ == "__main__":
    main()

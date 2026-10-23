# SPDX-License-Identifier: GPL-3.0-only
"""ALBUM's photos: phone photos, made smaller, never repainted.

  python3 photo.py add PHONE.jpg NAME [--y 0.5]   crop square (--y: 0 keeps the top, 1 the bottom), drop the
                                                   metadata (place, time, phone), save photos/NAME.jpg at 960 px
  python3 photo.py build                           every photos/*.jpg to 60 x 60 RGB565 in src/photos.c, and a
                                                   preview of each as the FM-1 shows it (stretched, smoothed)
                                                   in build/preview/
"""
import pathlib
import sys

import numpy as np
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
SIZE = 60                      # 7,200 bytes a photo
SCREEN = 240


def add(src, name, y=0.5):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    w, h = im.size
    s = min(w, h)
    left, top = (w - s) // 2, round((h - s) * y)
    im = im.crop((left, top, left + s, top + s)).resize((960, 960), Image.LANCZOS)
    out = ROOT / "photos" / f"{name}.jpg"
    out.parent.mkdir(exist_ok=True)
    im.save(out, quality=92)   # a fresh image: no EXIF, no GPS
    print(out)


def to565(a):
    a = a.astype(np.uint32)
    return ((a[..., 0] * 31 + 127) // 255) << 11 | ((a[..., 1] * 63 + 127) // 255) << 5 | ((a[..., 2] * 31 + 127) // 255)


def from565(p):
    r, g, b = (p >> 11) & 31, (p >> 5) & 63, p & 31
    return np.stack([r * 255 // 31, g * 255 // 63, b * 255 // 31], -1).astype(np.uint8)


def build():
    photos = sorted((ROOT / "photos").glob("*.jpg"))
    prev = ROOT / "build" / "preview"
    prev.mkdir(parents=True, exist_ok=True)
    lines = ["/* SPDX-License-Identifier: GPL-3.0-only */",
             "/* Made by tools/photo.py from the photos folder: do not edit. 60 x 60 RGB565, row by row. */",
             "#include <stdint.h>", ""]
    for p in photos:
        small = Image.open(p).convert("RGB").resize((SIZE, SIZE), Image.LANCZOS, reducing_gap=3.0)
        px = to565(np.asarray(small))
        sym = "PHOTO_" + "".join(c if c.isalnum() else "_" for c in p.stem.upper())
        lines.append(f"const uint16_t {sym}[{SIZE * SIZE}] = {{")
        flat = px.ravel()
        for i in range(0, len(flat), 12):
            lines.append("    " + ", ".join(f"0x{v:04X}" for v in flat[i:i + 12]) + ",")
        lines.append("};")
        lines.append("")
        Image.fromarray(from565(px)).resize((SCREEN, SCREEN), Image.BILINEAR).save(prev / f"{p.stem}.png")
        print(f"{p.name}: {sym}, {SIZE * SIZE * 2:,} bytes")
    (ROOT / "src" / "photos.c").write_text("\n".join(lines))


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "add":
        y = float(sys.argv[sys.argv.index("--y") + 1]) if "--y" in sys.argv else 0.5
        add(sys.argv[2], sys.argv[3], y)
    elif len(sys.argv) == 2 and sys.argv[1] == "build":
        build()
    else:
        print(__doc__)

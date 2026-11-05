#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""The photos from commons_fetch.py as they would look on the FM-1: through Album 01's own photo code
(album/tools/photos.py, MIT, Hausway, from a clone of album-fm1 with its fm1-base submodule), square, 240 px,
16 colors with Amethyst's violet and moss kept, and the size each would take (4 bits a pixel, LZ4 in 16-row bands).
The daytime ones are turned to night first (night(), below).

  python3 tools/amethyst/commons_preview.py DOWNLOADS OUT [ALBUM_CLONE]

Writes OUT/<stage>.png, OUT/sheet.png and OUT/photos.json (name, size, license, author, date, page)."""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
ALBUM = Path(sys.argv[3] if len(sys.argv) > 3 else Path(__file__).resolve().parents[3] / "joshbartlettband-web/album-fm1") / "album" / "tools"
sys.path.insert(0, str(ALBUM.parents[1] / "base" / "tools")); sys.path.insert(0, str(ALBUM))
import photos as ph, lz4blk
dl, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(exist_ok=True)
FONT = str(ALBUM.parents[1] / "base/assets/fonts/BarlowSemiCondensed-Bold.ttf")
meta = json.load(open(dl / "meta.json"))
# name on the screen, crop as (x, y, size) fractions of the photo, colours to keep
PLAN = {
 "The-End": ("THE END", None, ["#8A52D2", "#E28C30"]),
 "Outside-Turnmills": ("TURNMILLS", None, ["#8A52D2", "#E28C30"]),
 "Sound-System": ("SOUND SYSTEM", None, ["#8A52D2", "#54702C"]),
 "Heygate": ("HEYGATE", None, ["#8A52D2", "#54702C"]),
 "London-Night-bus-N8": ("N8", None, ["#E28C30", "#8A52D2"]),
 "Barbican": ("CONSERVATORY", None, ["#54702C", "#96B652", "#8A52D2"]),
 "Abney-Park": ("ABNEY PARK", None, ["#54702C", "#96B652", "#8A52D2"]),
 "Night-Bus": ("NIGHT BUS", None, ["#E28C30", "#8A52D2"]),
 "Latimer-Road": ("LATIMER ROAD", None, ["#8A52D2", "#E28C30"]),
}
NIGHT = {"The-End", "Outside-Turnmills", "Sound-System", "Heygate", "Barbican", "Abney-Park"}
def night(img):
    """day for night, as film crews did it: everything darker and violet, the sky darkest; only warm, bright things
    (windows, lamps, brick in the sun) stay lit, in sodium orange; greens kept as moss"""
    a = np.asarray(img, np.float32) / 255
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = 0.3 * r + 0.59 * g + 0.11 * b
    h = a.shape[0]
    sky = np.clip((b - r) * 4 + 0.5, 0, 1) * np.clip(lum * 2 - 0.6, 0, 1) * np.linspace(1, 0.2, h)[:, None]
    warm = np.clip((r - b) * 3, 0, 1) * np.clip(lum * 2.2 - 1.1, 0, 1)
    green = np.clip((g - (r + b) / 2) * 7, 0, 1)
    base = lum[..., None] ** 1.6 * np.array([0.42, 0.34, 0.62])          # violet night
    base = base * (1 - green[..., None] * 0.6) + green[..., None] * lum[..., None] ** 1.05 * np.array([0.36, 0.66, 0.24])
    base = base * (1 - sky[..., None]) + sky[..., None] * np.array([0.07, 0.05, 0.14])
    base = base + warm[..., None] * np.array([0.95, 0.55, 0.18])
    return Image.fromarray(np.clip(base * 255, 0, 255).astype(np.uint8))
shots, rows = [], []
for m in meta:
    key = next(k for k in PLAN if m["file"].startswith(k))
    name, crop, keep = PLAN[key]
    img = Image.open(dl / m["file"]).convert("RGB")
    w, h = img.size; s = min(w, h)
    img = img.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s)).resize((240, 240), Image.LANCZOS)
    if key in NIGHT:
        img = night(img)
    img = ImageEnhance.Color(img).enhance(1.25)
    px = np.asarray(img)
    pal = ph.palette_for(px, [ph.hexrgb(c) for c in keep])
    idx = ph.reduce(img, pal, False)
    packed = ph.pack(idx)
    size = sum(len(lz4blk.compress(packed[i:i + 1920])) for i in range(0, len(packed), 1920))
    im = Image.fromarray(pal[idx])
    a = np.asarray(im, np.float32); a[:34] *= 0.45; im = Image.fromarray(a.astype(np.uint8))
    d = ImageDraw.Draw(im)
    d.text((10, 8), name, font=ImageFont.truetype(FONT, 17), fill=(246, 240, 236))
    lic = m["license"].replace("Public domain", "PD")
    t = f"{m['date'][:4]}  {lic}"
    tw = d.textlength(t, font=ImageFont.truetype(FONT, 12))
    d.text((230 - tw, 12), t, font=ImageFont.truetype(FONT, 12), fill=(206, 172, 248))
    im.save(out / (key.lower() + ".png")); shots.append(im)
    rows.append((name, m, size)); print(f"{name:14} {size:6} B  {m['license']:14} {m['artist'][:40]}  {m['date']}  {m['page']}")
S, gap, n = 240, 8, len(shots)
cols = 3 if n == 9 else 4
sheet = Image.new("RGB", (cols * (S * 2 + gap) + gap, ((n + cols - 1) // cols) * (S * 2 + gap) + gap), (12, 10, 18))
for i, im in enumerate(shots):
    sheet.paste(im.resize((S * 2, S * 2), Image.NEAREST), (gap + (i % cols) * (S * 2 + gap), gap + (i // cols) * (S * 2 + gap)))
sheet.save(out / "sheet.png")
json.dump([{"name": r[0], "bytes": r[2], **r[1]} for r in rows], open(out / "photos.json", "w"), indent=1)

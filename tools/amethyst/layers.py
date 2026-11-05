#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Amethyst's stages as layers (docs/AMETHYST.md, section 6): the venue's photo and name in the middle, and over it
dark moss that crawls up as the jam goes on and glows on every kick, lasers after the drop, and kipatchi's brass
frame. Each stage comes out as a short animated GIF at the FM-1's size, cut to one 16-color palette for all its
frames (as the FM-1 would hold it), and a still for the sheet.

  python3 tools/amethyst/layers.py [--src docs/amethyst/gemini] [--out docs/amethyst/layers]

The pictures in --src are Gemini's changes of the Commons photos and Gemini's layers on black (see PROMPTS.md
there). Layers on black are keyed by brightness: black is see-through."""
import argparse
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import mockups as mk

ROOT = mk.ROOT
S = mk.S
FRAMES, FPS, BPM = 36, 12, 174
OFF, PAPER = (236, 228, 210), (214, 196, 160)


def load(src, name, crop=0):
    im = Image.open(src / name).convert("RGB")
    if crop:
        w, h = im.size
        im = im.crop((crop, crop, w - crop, h - crop))
    return np.asarray(im.resize((S, S), Image.Resampling.LANCZOS), np.float32)


def key(layer, lo=14, hi=70):
    """how see-through a layer on black is: black 0, bright 1"""
    lum = layer @ np.array([0.3, 0.59, 0.11], np.float32)
    return np.clip((lum - lo) / (hi - lo), 0, 1)[..., None]


def crawl_mask(t, seed):
    """where the moss has reached at time t (0..1): up from the bottom and in from the corners, ragged"""
    r = mk.rng(seed)
    noise = Image.fromarray((r.random((30, 30)) * 255).astype(np.uint8)).resize((S, S), Image.Resampling.BICUBIC)
    noise = np.asarray(noise, np.float32) / 255
    yy, xx = np.mgrid[0:S, 0:S] / S
    reach = (1 - yy) * 0.8 + np.minimum(xx, 1 - xx) * 0.4 + noise * 0.25
    m = np.clip((t * 1.05 - reach) * 8 + 0.5, 0, 1)
    return m[..., None]


def kick(frame):
    """1 on the kick, falling away: a kick every beat at BPM"""
    beat = FPS * 60 / BPM
    ph = (frame % beat) / beat
    return math.exp(-ph * 5)


def label(img, f, title, sub, y=None):
    """the venue's name in the middle band, kipatchi's two-line label"""
    d = ImageDraw.Draw(img)
    tw = max(d.textlength(title, font=mk.font(f, 22)), d.textlength(sub, font=mk.font(f, 10))) + 16
    x = (S - tw) / 2
    y = y if y is not None else 16
    d.rectangle([x, y, x + tw, y + 42], fill=(12, 10, 10), outline=(110, 96, 70))
    d.text((x + 8, y + 3), title, font=mk.font(f, 22), fill=OFF)
    d.text((x + 8, y + 28), sub, font=mk.font(f, 10), fill=PAPER)


def stage(src, f, cfg):
    base = load(src, cfg["photo"])
    moss = load(src, "layer-moss.jpg", crop=40)
    lasers = load(src, "layer-lasers.jpg") if cfg.get("lasers") else None
    frame_l = load(src, "layer-frame.jpg") if cfg.get("frame") else None
    mk_moss = key(moss)
    glow_pts = np.clip((moss.max(2) - 150) / 80, 0, 1)[..., None]        # the moss's brightest points
    shots = []
    for i in range(FRAMES):
        t = 0.05 + 0.95 * i / (FRAMES - 1)                     # the jam goes on: the moss climbs
        k = kick(i)
        a = base * (0.82 + 0.18 * k * cfg.get("pulse", 1))     # the room breathes on the kick
        m = mk_moss * crawl_mask(t, cfg.get("seed", 1))
        a = a * (1 - m) + moss * m
        a += glow_pts * m * k * np.array([150, 90, 220], np.float32) * 1.2      # the moss glows on the kick
        a += m * (1 - glow_pts) * np.array([-10, 8, -10], np.float32)            # and stays green where it's dark
        if lasers is not None and i >= FRAMES // 2:            # after the drop
            flick = 0.7 + 0.3 * math.sin(i * 1.7)
            a += lasers * key(lasers, 10, 60) * flick * 0.55 * np.array([0.9, 0.8, 1.1], np.float32)
        if frame_l is not None:
            fk = key(frame_l, 20, 60)
            a = a * (1 - fk) + frame_l * fk
        if cfg.get("aerial"):                                  # the pirate aerial's light
            x, y = cfg["aerial"]
            yy, xx = np.mgrid[0:S, 0:S]
            g = np.exp(-((xx - x) ** 2 + (yy - y) ** 2) / (2 * 6 ** 2))[..., None]
            a += g * (0.4 + 0.6 * (i % 6 < 3)) * np.array([255, 40, 50], np.float32)
        shots.append(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)))
    # one palette for every frame, from the middle and the last, so nothing flickers
    ref = Image.new("RGB", (S, S * 2))
    ref.paste(shots[FRAMES // 2], (0, 0))
    ref.paste(shots[-1], (0, S))
    keep = [mk.AM, mk.AM_L, mk.MOSS, mk.MOSS_L, mk.SODIUM, (255, 60, 70)]   # what the 16 colors must not lose
    q = ref.quantize(colors=16 - len(keep), method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    pal = np.vstack([np.array(q.getpalette()[:3 * (16 - len(keep))]).reshape(-1, 3), keep]).astype(np.int32)
    out = []
    for im in shots:
        px = np.asarray(im).reshape(-1, 3).astype(np.int32)
        idx = ((px[:, None, :] - pal[None, :, :]) ** 2).sum(2).argmin(1)
        q = Image.fromarray(pal[idx].reshape(S, S, 3).astype(np.uint8))
        label(q, f, cfg["title"], cfg["sub"], cfg.get("label_y"))
        out.append(q)
    return out


STAGES = [
    {"name": "the-end", "photo": "the-end-moss.jpg", "title": "THE END", "sub": "WEST CENTRAL STREET  •  FRIDAY",
     "lasers": True, "seed": 3},
    {"name": "turnmills", "photo": "turnmills-moss.jpg", "title": "TURNMILLS", "sub": "CLERKENWELL  •  DARKSIDE",
     "frame": True, "seed": 5, "label_y": 34},
    {"name": "heygate", "photo": "heygate-roof.jpg", "title": "HEYGATE", "sub": "ELEPHANT AND CASTLE  •  ROOF",
     "aerial": (65, 24), "seed": 7, "label_y": 186},
    {"name": "night-bus", "photo": "nightbus-moss.jpg", "title": "NIGHT BUS", "sub": "3 AM, THE WAY HOME",
     "seed": 9, "label_y": 186},
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--font")
    ap.add_argument("--src", default=str(ROOT / "docs" / "amethyst" / "gemini"))
    ap.add_argument("--out", default=str(ROOT / "docs" / "amethyst" / "layers"))
    a = ap.parse_args()
    f, src, out = mk.find_font(a.font), Path(a.src), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    stills = []
    for cfg in STAGES:
        frames = stage(src, f, cfg)
        frames[0].save(out / f"{cfg['name']}.gif", save_all=True, append_images=frames[1:], duration=1000 // FPS,
                       loop=0, optimize=True)
        stills.append((frames[FRAMES // 4], frames[-1]))
    gap = 8
    sheet = Image.new("RGB", (len(stills) * (S * 2 + gap) + gap, 2 * (S * 2 + gap) + gap), (12, 10, 18))
    for i, (early, late) in enumerate(stills):                 # each stage early in the jam, then late
        x = gap + i * (S * 2 + gap)
        sheet.paste(early.resize((S * 2, S * 2), Image.Resampling.NEAREST), (x, gap))
        sheet.paste(late.resize((S * 2, S * 2), Image.Resampling.NEAREST), (x, S * 2 + 2 * gap))
    sheet.save(out / "sheet.png")
    print(f"{out}: {len(stills)} stages, a GIF each, and sheet.png")


if __name__ == "__main__":
    main()

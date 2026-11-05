#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Ask Gemini's image model for one picture: a new one from words, or a change to a picture you give it. Used to try
layers and changes for Amethyst's stages (docs/AMETHYST.md, section 6). Whatever comes back is a sketch: check it,
credit it as AI-made, and keep the license of any photo it started from.

  python3 tools/amethyst/gemini_image.py OUT.png "what to make" [IN.jpg ...] [--model gemini-3-pro-image] [--square]

Needs GEMINI_API_KEY, or a proxy that adds the key (any placeholder value is sent then)."""
import argparse
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.request

API = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("prompt")
    ap.add_argument("inputs", nargs="*")
    ap.add_argument("--model", default="gemini-3-pro-image")
    ap.add_argument("--square", action="store_true", help="ask for a 1:1 picture")
    a = ap.parse_args()
    parts = []
    for path in a.inputs:
        mime = mimetypes.guess_type(path)[0] or "image/jpeg"
        parts.append({"inline_data": {"mime_type": mime, "data": base64.b64encode(open(path, "rb").read()).decode()}})
    parts.append({"text": a.prompt})
    cfg = {"responseModalities": ["IMAGE", "TEXT"]}
    if a.square:
        cfg["imageConfig"] = {"aspectRatio": "1:1"}
    body = json.dumps({"contents": [{"role": "user", "parts": parts}], "generationConfig": cfg}).encode()
    req = urllib.request.Request(API.format(model=a.model), data=body, method="POST", headers={
        "Content-Type": "application/json", "x-goog-api-key": os.environ.get("GEMINI_API_KEY", "placeholder")})
    for attempt in range(3):
        try:
            d = json.load(urllib.request.urlopen(req, timeout=300))
            break
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:400]
            if e.code in (429, 500, 503) and attempt < 2:
                time.sleep(15 * (attempt + 1))
                continue
            sys.exit(f"gemini_image: HTTP {e.code}: {msg}")
    for c in d.get("candidates", []):
        for p in c.get("content", {}).get("parts", []):
            blob = p.get("inline_data") or p.get("inlineData")
            if blob:
                open(a.out, "wb").write(base64.b64decode(blob["data"]))
                print(f"{a.out}: {blob.get('mime_type') or blob.get('mimeType')}")
                return
            if p.get("text"):
                print("model said:", p["text"][:300])
    sys.exit("gemini_image: no picture came back: " + json.dumps(d)[:400])


if __name__ == "__main__":
    main()

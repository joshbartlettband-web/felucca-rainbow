#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Download photos from Wikimedia Commons at 720 px, with their license, author and date, for trying them as
Amethyst's stages (docs/AMETHYST.md, section 6). Keep the downloads out of the repo: only the 240 px results of
commons_preview.py go in, with their credits.

  python3 tools/amethyst/commons_fetch.py DIR "File:Night Bus (254241945).jpg" ...

Writes DIR/<name>.jpg and DIR/meta.json. Commons answers 429 to a fast client, so this waits between files."""
import json, sys, time, urllib.parse, urllib.request, re
API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "amethyst-research/0.1 (FM-1 firmware design notes)"}
out_dir = sys.argv[1]
titles = sys.argv[2:]
import os
meta = json.load(open(f'{out_dir}/meta.json')) if os.path.exists(f'{out_dir}/meta.json') else []
for t in titles:
    q = {"action": "query", "titles": t, "prop": "imageinfo", "iiprop": "url|extmetadata", "iiurlwidth": 720,
         "iiextmetadatafilter": "LicenseShortName|Artist|DateTimeOriginal|LicenseUrl", "format": "json"}
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(q), headers=UA)
    for i in range(6):
        try:
            d = json.load(urllib.request.urlopen(req, timeout=30)); break
        except Exception as e:
            time.sleep(10 * (i + 1))
    p = next(iter(d["query"]["pages"].values()))
    ii = p["imageinfo"][0]; m = ii["extmetadata"]
    g = lambda k: re.sub("<[^>]+>", "", m.get(k, {}).get("value", "")).strip()
    name = re.sub(r"[^A-Za-z0-9]+", "-", t[5:].rsplit(".", 1)[0])[:40].strip("-") + ".jpg"
    data = None
    for i in range(4):
        try:
            data = urllib.request.urlopen(urllib.request.Request(ii["thumburl"], headers=UA), timeout=60).read(); break
        except Exception:
            time.sleep(10 * (i + 1))
    if data is None:
        print(f"{t}: not downloaded (Commons asked us to slow down); try again later")
        continue
    open(f"{out_dir}/{name}", "wb").write(data)
    meta.append({"title": t, "file": name, "license": g("LicenseShortName"), "artist": g("Artist"),
                 "date": g("DateTimeOriginal")[:10], "page": ii["descriptionurl"]})
    print(name, "|", meta[-1]["license"], "|", meta[-1]["artist"][:40], "|", meta[-1]["date"])
    time.sleep(6)
json.dump(meta, open(f"{out_dir}/meta.json", "w"), indent=1)

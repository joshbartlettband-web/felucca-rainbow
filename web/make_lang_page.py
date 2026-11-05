#!/usr/bin/env python3
"""Rainbow mode's page in another language: web/make_lang_page.py LL OUT.html
The words are PAGE in tools/lang/LL.py; the look is landing/pt/index.html's (its <style>). The songs are the ones its
FOLLOW plays (SONGS), as the screen shows them. The workflow fills in @SITE@ and @REPO@."""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import gen_kid_lang  # noqa: E402


def main(code, out):
    L = gen_kid_lang.lang(code)
    P = L.PAGE
    pt = (ROOT / "landing" / "pt" / "index.html").read_text(encoding="utf-8")
    style = re.search(r"<style>.*?</style>", pt, re.S).group(0)
    icon = re.search(r'<link rel="icon"[^>]*>', pt).group(0)
    e = html.escape
    songs = [n for n, *_ in L.SOLFA_SONGS] + [n for n, _ in L.SONGS]
    facts = "\n".join(f"    <li>{e(f)}</li>" for f in P["facts"])
    page = f"""<!doctype html>
<!-- SPDX-License-Identifier: GPL-3.0-only
     Made by web/make_lang_page.py from tools/lang/{code}.py. Do not edit: edit that. -->
<html lang="{P['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(P['title'])}</title>
<meta name="description" content="{e(P['lede'])}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(P['title'])}">
<meta property="og:description" content="{e(P['lede'])}">
<meta property="og:image" content="@SITE@/card.png">
{icon}
{style}
</head>
<body>
<div class="stripe"></div>
<main>
  <section>
    <h1><span>R</span><span>a</span><span>i</span><span>n</span><span>b</span><span>o</span><span>w</span> mode</h1>
    <p class="lede">{e(P['lede'])}</p>
    <div class="buttons">
      <a class="btn" href="webapp/try/">{e(P['try'])}</a>
      <a class="btn alt" href="webapp/installer/">{e(P['install'])}</a>
      <a class="btn alt" href="../" lang="en">In English</a>
    </div>
    <p class="lede" style="font-size:1rem;margin:0">{e(P['note'])}</p>
  </section>

  <h2>{e(P['inside'])}</h2>
  <ul class="facts">
{facts}
  </ul>

  <h2>{e(P['songs'])}</h2>
  <p class="lede" style="font-size:1rem">{e(", ".join(songs))}</p>
  <p style="color:var(--soft);font-size:.95rem">{e(P['source'])}</p>
</main>
<footer>
  <p>{e(P['footer'])} <a href="https://github.com/hugelton/Felucca">Felucca</a> · <a href="https://github.com/@REPO@">github.com/@REPO@</a></p>
</footer>
</body>
</html>
"""
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(page, encoding="utf-8")
    print(f"page: {code} -> {out}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

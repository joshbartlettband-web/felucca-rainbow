#!/usr/bin/env python3
""""Other projects by Josh": the menu at the top of the landing page and the moving pictures at the bottom. The same
script (and the same landing/more/*.gif) lives in all three repos: Double Rainbow, Rainbow mode and Fretbound.
  python3 tools/landing/more.py landing/index.html THIS_SLUG
Fills <!--MORE-TOP-->...<!--/MORE-TOP--> and <!--MORE-BOTTOM-->...<!--/MORE-BOTTOM--> with the other two projects.
Run it again after changing PROJECTS; it replaces what it wrote before. Styles are self-contained (class jbm-*), so
the block sits on any of the three pages without touching their own CSS."""
import re
import sys
from pathlib import Path

PROJECTS = [
    ("double-rainbow", "Double Rainbow", "https://joshbartlettband-web.github.io/Double-Rainbow/",
     "Firmware for the M-VAVE FM-1. 24 sounds got out of the Keeper's jars, and each one is a real synth engine you "
     "learn by playing. For ages ten and up.", "Synth characters for the FM-1, ten and up"),
    ("rainbow-mode", "Rainbow mode", "https://joshbartlettband-web.github.io/felucca-rainbow/",
     "A music toy for little hands on the M-VAVE FM-1. 94 friends, 21 beats and a color for every note.",
     "A music toy for little hands, on the FM-1"),
    ("fretbound", "Fretbound", "https://joshbartlettband-web.github.io/Fretbound/",
     "An ear-training game for guitarists. A rival plays a phrase and you play it back on the fretboard. "
     "It runs in your browser.", "Ear training for guitarists, in your browser"),
]

STYLE = """<style>
  .jbm-top { max-width: 940px; margin: 0 auto; padding: 10px 16px 0; display: flex; justify-content: flex-end; position: relative; z-index: 5; }
  .jbm-top details { position: relative; background: none; padding: 0; margin: 0; border-radius: 0; }
  .jbm-top summary { list-style: none; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; min-height: 40px;
    padding: 0 14px; border-radius: 999px; font: 600 15px/1 system-ui, -apple-system, "Segoe UI", sans-serif;
    color: #f6ead2; background: rgba(255, 255, 255, .08); box-shadow: inset 0 0 0 1px rgba(255, 255, 255, .18); }
  .jbm-top summary::-webkit-details-marker { display: none; }
  .jbm-top summary::after { content: ""; width: 7px; height: 7px; border: solid currentColor; border-width: 0 2px 2px 0;
    transform: translateY(-2px) rotate(45deg); transition: transform .15s; }
  .jbm-top details[open] summary::after { transform: translateY(1px) rotate(-135deg); }
  .jbm-top summary:focus-visible, .jbm-top a:focus-visible, .jbm-bottom a:focus-visible { outline: 3px solid #3fe0c5; outline-offset: 3px; }
  .jbm-top ul { position: absolute; right: 0; top: calc(100% + 8px); width: min(320px, calc(100vw - 32px)); margin: 0; padding: 8px;
    list-style: none; background: #1b1430; border-radius: 16px; box-shadow: 0 12px 40px rgba(0, 0, 0, .5), inset 0 0 0 1px rgba(255, 255, 255, .12); }
  .jbm-top li a { display: flex; gap: 12px; align-items: center; padding: 8px; border-radius: 12px; text-decoration: none; color: #f6ead2; }
  .jbm-top li a:hover { background: rgba(255, 255, 255, .08); }
  .jbm-top li img { width: 52px; height: 52px; object-fit: cover; object-position: center; border-radius: 10px; flex: none; image-rendering: pixelated; }
  .jbm-top li b { display: block; font: 700 16px/1.25 system-ui, -apple-system, "Segoe UI", sans-serif; }
  .jbm-top li span { display: block; font: 13px/1.35 system-ui, -apple-system, "Segoe UI", sans-serif; color: #c9bcd9; }
  .jbm-bottom { max-width: 940px; margin: 64px auto 0; padding: 0 16px; }
  .jbm-bottom h2 { margin: 0 0 14px; }
  .jbm-bottom ul { display: grid; gap: 16px; margin: 0; padding: 0; list-style: none; }
  .jbm-bottom a { display: grid; grid-template-columns: 120px 1fr; gap: 16px; align-items: center; padding: 12px; border-radius: 18px;
    text-decoration: none; color: inherit; background: rgba(255, 255, 255, .06); box-shadow: inset 0 0 0 1px rgba(255, 255, 255, .1); }
  .jbm-bottom a:hover { background: rgba(255, 255, 255, .1); }
  .jbm-bottom img { width: 120px; height: 120px; object-fit: cover; object-position: center; border-radius: 12px; image-rendering: pixelated; }
  .jbm-bottom b { display: block; font-size: 1.15rem; }
  .jbm-bottom span { display: block; font-size: .95rem; line-height: 1.4; opacity: .85; }
  .jbm-bottom em { display: block; margin-top: 6px; font-style: normal; font-weight: 700; font-size: .95rem; color: #3fe0c5; }
  @media (min-width: 640px) {
    .jbm-bottom ul { grid-template-columns: repeat(2, 1fr); }
    .jbm-bottom a { grid-template-columns: 1fr; align-items: start; }
    .jbm-bottom img { width: 100%; height: auto; aspect-ratio: 1; }
  }
</style>"""

SCRIPT = """<script>
  // the menu closes on a click outside it or on Escape
  (function () {
    var d = document.querySelector(".jbm-top details");
    if (!d) return;
    document.addEventListener("click", function (e) { if (d.open && !d.contains(e.target)) d.open = false; });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && d.open) { d.open = false; d.querySelector("summary").focus(); } });
  })();
</script>"""


def others(me):
    return [p for p in PROJECTS if p[0] != me]


def top(me):
    items = "\n".join(
        f'      <li><a href="{url}"><img src="more/{slug}.gif" width="52" height="52" alt=""><span><b>{name}</b>'
        f'<span>{short}</span></span></a></li>'
        for slug, name, url, line, short in others(me))
    return (f"\n{STYLE}\n<nav class=\"jbm-top\" aria-label=\"Other projects by Josh\">\n  <details>\n"
            f"    <summary>Other projects by Josh</summary>\n    <ul>\n{items}\n    </ul>\n  </details>\n</nav>\n")


def bottom(me):
    items = "\n".join(
        f'    <li><a href="{url}"><img src="more/{slug}.gif" width="240" height="240" loading="lazy" '
        f'alt="{name}, a few of its screens"><div><b>{name}</b><span>{line}</span><em>Take a look</em></div></a></li>'
        for slug, name, url, line, short in others(me))
    return (f"\n<section class=\"jbm-bottom\" aria-labelledby=\"jbm-h\">\n  <h2 id=\"jbm-h\">Other projects by Josh</h2>\n"
            f"  <ul>\n{items}\n  </ul>\n</section>\n{SCRIPT}\n")


def fill(html, tag, body):
    pat = re.compile(rf"<!--{tag}-->.*?<!--/{tag}-->", re.S)
    if len(pat.findall(html)) != 1:
        sys.exit(f"more.py: the page needs exactly one <!--{tag}--><!--/{tag}--> pair")
    return pat.sub(lambda m: f"<!--{tag}-->{body}<!--/{tag}-->", html)


def main():
    path, me = Path(sys.argv[1]), sys.argv[2]
    if me not in [p[0] for p in PROJECTS]:
        sys.exit(f"more.py: no project {me!r}")
    html = path.read_text()
    html = fill(html, "MORE-TOP", top(me))
    html = fill(html, "MORE-BOTTOM", bottom(me))
    path.write_text(html)
    print(f"{path}: linked {', '.join(p[1] for p in others(me))}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""A FOLLOW song from a Wikipedia article's score: tools/wiki_song.py LANG "Article title" [BLOCK] [NAME]
Fetches the article's wikitext, renders its <score> (LilyPond) to MIDI with repeats written out, reads the tune back
(the top note of the highest part), plays a score that repeats itself whole once, and moves it to fit the keys at OCT 0
(F3 .. G5) with the fewest black keys. Prints the line for tools/lang/LANG.py's SONGS. Needs lilypond and mido
(pip install mido); only for adding songs, the build does not use it."""
import glob
import re
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request

import mido

NAMES = "C CS D DS E F FS G GS A AS B".split()


def wikitext(lang, title):
    url = f"https://{lang}.wikipedia.org/w/index.php?title={urllib.parse.quote(title.replace(' ', '_'))}&action=raw"
    req = urllib.request.Request(url, headers={"User-Agent": "rainbow-mode-build/1.0 (children's song sourcing)"})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8")


def lilypond(attrs, body):
    body = body.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    body = re.sub(r"\\repeat\s+(volta|percent|segno)", r"\\unfoldRepeats \\repeat \1", body)
    if "raw" in attrs:                                     # (a whole LilyPond file: give its \score a \midi)
        if "\\midi" not in body:
            at = [m.start() for m in re.finditer(r"\\layout\s*\{", body)]
            i = at[-1] if at else body.rfind("}")
            body = body[:i] + "\\midi { }\n" + body[i:]
        return body
    top = re.findall(r'\\language\s+"[a-z]+"', body)
    body = re.sub(r'\\language\s+"[a-z]+"', "", body)
    return "\n".join(top) + "\n\\score { " + body + "\n\\layout { } \\midi { } }\n"


def tune(midi_path):
    best = None
    for tr in mido.MidiFile(midi_path).tracks:
        t, at = 0, {}
        for msg in tr:
            t += msg.time
            if msg.type == "note_on" and msg.velocity > 0:
                at.setdefault(t, []).append(msg.note)
        if len(at) < 8:
            continue
        seq = [max(at[k]) for k in sorted(at)]
        if best is None or sum(seq) / len(seq) > best[0]:
            best = (sum(seq) / len(seq), seq)
    return best[1] if best else []


def fit(seq):
    while len(seq) % 2 == 0 and seq and seq[:len(seq) // 2] == seq[len(seq) // 2:]:
        seq = seq[:len(seq) // 2]
    opts = [(sum((x + sh) % 12 in (1, 3, 6, 8, 10) for x in seq), abs(sh), sh) for sh in range(-12, 13)
            if min(seq) + sh >= 53 and max(seq) + sh <= 79]
    if not opts:
        raise SystemExit(f"wiki_song: {min(seq)} .. {max(seq)} does not fit the keys")
    sh = min(opts)[2]
    return sh, [x + sh for x in seq]


def main(lang, title, block=0, name=None):
    scores = re.findall(r"<score([^>]*)>(.*?)</score>", wikitext(lang, title), re.S)
    if not scores:
        raise SystemExit(f"wiki_song: {title}: no score")
    with tempfile.TemporaryDirectory() as d:
        open(f"{d}/s.ly", "w").write(lilypond(*scores[block]))
        subprocess.run(["lilypond", "-dno-print-pages", "-o", f"{d}/s", f"{d}/s.ly"], capture_output=True, timeout=120)
        mids = glob.glob(f"{d}/*.mid*")
        if not mids:
            raise SystemExit(f"wiki_song: {title}: LilyPond made no MIDI")
        sh, seq = fit(tune(mids[0]))
    moved = f", moved {sh:+d}" if sh else ""
    print(f"    # {title} ({lang}.wikipedia.org, its score{moved})")
    print(f'    ("{name or title.upper()[:14]}", "{" ".join(NAMES[x % 12] + str(x // 12 - 1) for x in seq)}"),')


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], a[1], int(a[2]) if len(a) > 2 else 0, a[3] if len(a) > 3 else None)

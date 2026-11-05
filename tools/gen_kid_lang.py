#!/usr/bin/env python3
"""Rainbow mode in another language: kid.c with the screen's words, the songs and the note names of tools/lang/LANG.py.
  gen_kid_lang.py LANG OUT.c        (build.py --lang LANG; then felucca.c includes OUT.c, kid_lang.c, for kid.c)
kid.c stays the English source. Each word to translate is one of its string literals, exactly ("BIG", "YES!", a card
with its \\n), and must be there, or this stops: a literal that changed in kid.c is a translation to look at again.
The accented capitals become the bytes kid.c's font has (\\200 .. \\213, its KID_FONT after 4); gen_kid_art.py uses enc()
for the friends' and the hats' names. FOLLOW's songs are replaced by the language's own.
A language written in kana (SCRIPT = "kana": Japanese) gets 7 px letters on an 8 px step (KID_ADV 8): each kana it uses
is a byte from \200 up, in the order of their code points, drawn from tools/fonts/misaki_kana.bdf (Misaki Gothic 2nd,
Num Kadoma's free 8x8 font) into KID_KANA; the capitals and digits stay, centred in the wider step."""
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACCENTS = "ÁÀÂÃÇÉÊÍÓÔÕÚÈËÎÏÌÑÒÙÛÜÄÖÅÆØ"   # kid.c KID_FONT 37 .., bytes 0x80 .. 0x9A
SOLFA = {"do": 0, "re": 2, "mi": 4, "fa": 5, "sol": 7, "la": 9, "si": 11}
KEYS = ["F3", "FS3", "G3", "GS3", "A3", "AS3", "B3", "C4", "CS4", "D4", "DS4", "E4", "F4", "FS4", "G4", "GS4", "A4",
        "AS4", "B4", "C5", "CS5", "D5", "DS5", "E5", "F5", "FS5", "G5"]   # kid.c K_*: key 0 is F3 (MIDI 53)


ADV = 6                                  # a letter's step at scale 1 (kid.c KID_ADV)
KANA = {}                                # a kana language's letters: character -> byte (from 0x80)


def lang(code):
    global ADV, KANA
    p = ROOT / "tools" / "lang" / f"{code}.py"
    if not p.exists():
        raise SystemExit(f"gen_kid_lang: no tools/lang/{code}.py")
    spec = importlib.util.spec_from_file_location(f"lang_{code}", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    ADV, KANA = 6, {}
    if getattr(m, "SCRIPT", "") == "kana":
        ADV = 8
        texts = list(m.WORDS.values()) + list(m.NAMES.values()) + list(m.HATS.values()) + \
            [n for n, *_ in m.SOLFA_SONGS + m.SONGS] + "".join(getattr(m, "SUBS", {}).values()).split('"')
        used = sorted({ch for t in texts for ch in t if ord(ch) > 0x7f})
        if len(used) > 128:
            raise SystemExit(f"gen_kid_lang: {code}: {len(used)} kana, 128 at most")
        KANA = {ch: 0x80 + i for i, ch in enumerate(used)}
    return m


def kana_glyphs():
    """KID_KANA: each kana's 7 rows of 7 px (the left one bit 6), from the BDF, its baseline under the 7th row"""
    bdf = (ROOT / "tools" / "fonts" / "misaki_kana.bdf").read_text(encoding="latin-1")
    font = {}
    for c in re.findall(r"STARTCHAR.*?ENDCHAR", bdf, re.S):
        e = int(re.search(r"ENCODING (\d+)", c).group(1))
        w, h, xo, yo = map(int, re.search(r"BBX (-?\d+) (-?\d+) (-?\d+) (-?\d+)", c).groups())
        rows = [0] * 7
        for r, hexrow in enumerate(re.search(r"BITMAP\n(.*)", c, re.S).group(1).split()[:h]):
            y = 7 - (yo + h) + r
            if 0 <= y < 7:
                rows[y] = (int(hexrow, 16) >> (1 + xo)) & 0x7f
        font[chr(e)] = rows
    out = []
    for ch, b in sorted(KANA.items(), key=lambda kv: kv[1]):
        if ch not in font:
            raise SystemExit(f"gen_kid_lang: {ch!r} is not in tools/fonts/misaki_kana.bdf")
        out.append("    {" + ", ".join(f"0x{v:02X}" for v in font[ch]) + "},   /* \\%03o %s */" % (b, ch))
    return out


def enc(s):
    """a word as kid.c's band can draw it: capitals, digits, space # ! ? - (and \\n in a card); accents as octal bytes"""
    if "\\n" in s:                        # (a card: its lines, the \n between them kept as kid.c writes it)
        return "\\n".join(enc(x) for x in s.split("\\n"))
    out = []
    for ch in s:
        if ch in KANA:
            out.append("\\%03o" % KANA[ch])
        elif KANA and ord(ch) > 0x7f:
            raise SystemExit(f"gen_kid_lang: {s!r}: {ch!r} is not one of the kana")
        elif ch in ACCENTS:
            out.append("\\%03o" % (0x80 + ACCENTS.index(ch)))
        elif re.fullmatch(r"[A-Z0-9 #!?\-_=]", ch):
            out.append(ch)
        else:
            raise SystemExit(f"gen_kid_lang: {s!r}: {ch!r} is not in the band's font")
    return "".join(out)


def shown(s):
    """how long a word is on the screen (an accented capital is one byte)"""
    return len(s)


ONE_LINE = {"KICK", "SNARE", "CLAP", "HI-HAT", "OPEN HAT", "RIM", "COWBELL", "CYMBAL", "TOM", "CONGA", "CLAVE", "CYM",
            "SHAKER"}                     # (kid_drum_word: the band says them on one line, so 13 letters at most)
WRITE_WORDS = {"NO BEAT", "NEW SONG", "WRITE", "LOOP", "DANCE", "MARCH", "SPOOKY", "ROCK", "DISCO", "HIP HOP", "TRAIN",
               "SAMBA", "REGGAE", "LULLABY", "HOEDOWN", "LOFI", "ACID", "POLKA"}   # (kid.c KID_BEATS: the beats' names)


def fits(code, src, en, tr):
    """does a word fit across the screen (240 px, 6 px a letter at scale 1) where kid.c draws it"""
    n = shown(tr)
    m = re.search(r'\{"%s", (\d+), \d+, (\d)\}' % re.escape(en), src)     # (the name screen's lines: x, y, scale)
    if m:
        ok = n * ADV * int(m[2]) - int(m[2]) <= 238 - int(m[1])
    elif en in WRITE_WORDS and n * ADV * 2 - 2 > 176:                          # (WRITE: beside the friend, scale 2)
        ok = False
    elif en in ("HI!", "HI"):                                                  # (the hello: scale 4 at the smallest
        ok = n * ADV * 4 - 4 <= 228 if en == "HI!" else n * ADV * 7 - 7 <= 232   #  alone, 7 with a name)
    elif n * ADV * 3 - 3 <= 232:                                               # (the band: scale 3 at the smallest)
        ok = True
    else:                                                                      # (or two lines, split at a space)
        cuts = [i for i, ch in enumerate(tr) if ch == " "]                     #  as kid.c: the one nearest the middle
        cut = min(cuts, key=lambda i: abs(i - n // 2)) if cuts else 0
        ok = bool(cut) and en not in ONE_LINE and 'kid_band_word("%s"' % en not in src and \
            max(shown(tr[:cut]), shown(tr[cut + 1:])) * ADV * 3 - 3 <= 232
    if not ok:
        raise SystemExit(f"gen_kid_lang: {code}: {tr!r} (for {en!r}) is too wide for the screen")


def solfa_keys(text, shift):
    keys = []
    for w in text.replace("/", " ").split():
        m = re.fullmatch(r"(do|re|mi|fa|sol|la|si|DO|RE|MI|FA|SOL|LA|SI)(#|b)?", w)
        if not m:
            raise SystemExit(f"gen_kid_lang: {w!r} is not a note (do re mi .. si, # or b; capitals: the high octave)")
        n = 60 + SOLFA[m[1].lower()] + (12 if m[1].isupper() else 0) + {"#": 1, "b": -1, None: 0}[m[2]] + shift
        keys.append(n - 53)
    return keys


def note_keys(text):
    keys = []
    for w in text.split():
        m = re.fullmatch(r"([A-G])(S?)([0-9])", w)
        if not m:
            raise SystemExit(f"gen_kid_lang: {w!r} is not a note (C4, FS3 ..)")
        n = 12 * (int(m[3]) + 1) + {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[m[1]] + (m[2] == "S")
        keys.append(n - 53)
    return keys


def song_line(name, keys):
    if not keys or min(keys) < 0 or max(keys) > 26:
        raise SystemExit(f"gen_kid_lang: {name}: a note off the keys (F3 .. G5)")
    toks = [f"K_{KEYS[k]}" for k in keys]
    head = '    {"%s", ' % enc(name)
    lines, line = [], head
    for t in toks:
        if len(line) + len(t) + 1 > 116:
            lines.append(line.rstrip())
            line = " " * len(head)
        line += t + " "
    return "\n".join(lines + [line.rstrip() + "},"])


def main(code, out):
    L = lang(code)
    src = (ROOT / "firmware" / "src" / "kid.c").read_text()
    for en, tr in L.WORDS.items():
        lit = '"' + en + '"'
        if lit not in src:
            raise SystemExit(f"gen_kid_lang: {code}: {lit} is not in kid.c any more")
        if "\\n" in en:                    # a card: up to 3 lines of 17 (13 kana)
            ls, most = tr.split("\\n"), 17 if ADV == 6 else 220 // (2 * ADV)
            if len(ls) > 3 or max(shown(x) for x in ls) > most:
                raise SystemExit(f"gen_kid_lang: {code}: {tr!r}: a card has 3 lines of {most} at most")
        else:
            fits(code, src, en, tr)
        src = src.replace(lit, '"' + enc(tr) + '"')
    for a, b in getattr(L, "SUBS", {}).items():    # (whole pieces of code to swap, each exactly once: H for B)
        if src.count(a) != 1:
            raise SystemExit(f"gen_kid_lang: {code}: {a!r} is in kid.c {src.count(a)} times, not once")
        src = src.replace(a, re.sub(r'"([^"]*)"', lambda m: '"' + enc(m[1]) + '"', b))
    i = src.index("static const kid_song_t KID_SONGS[] = {")
    j = src.index("\n};", i)
    songs = [song_line(n, solfa_keys(t, sh)) for n, sh, _, t in L.SOLFA_SONGS] + \
            [song_line(n, note_keys(t)) for n, t in L.SONGS]
    for n, *_ in L.SOLFA_SONGS + L.SONGS:
        if shown(n) > 14 * 6 // ADV:
            raise SystemExit(f"gen_kid_lang: {code}: the song {n!r}: {14 * 6 // ADV} letters at most")
    src = src[:i] + "static const kid_song_t KID_SONGS[] = {\n" + "\n".join(songs) + src[j:]
    head = (f"/* generated by tools/gen_kid_lang.py from firmware/src/kid.c and tools/lang/{code}.py: Rainbow mode in "
            f"this language. Do not edit: edit those. */\n#define KID_DOREMI_FIRST {1 if L.DOREMI else 0}\n")
    if KANA:                                       # (its letters: kana, 7 px on an 8 px step)
        head += (f"#define KID_ADV {ADV}\n#define KID_KANA_N {len(KANA)}\n"
                 "static const uint8_t KID_KANA[KID_KANA_N][7] = {   /* tools/fonts/misaki_kana.bdf: Misaki Gothic 2nd, "
                 "(C) Num Kadoma, free */\n" + "\n".join(kana_glyphs()) + "\n};\n")
    Path(out).write_text(head + src)
    print(f"kid lang: {code}, {len(L.WORDS)} words, {len(songs)} songs -> {out}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

#!/usr/bin/env python3
"""Rainbow mode in another language: kid.c with the screen's words, the songs and the note names of tools/lang/LANG.py.
  gen_kid_lang.py LANG OUT.c        (build.py --lang LANG; then felucca.c includes OUT.c, kid_lang.c, for kid.c)
kid.c stays the English source. Each word to translate is one of its string literals, exactly ("BIG", "YES!", a card
with its \\n), and must be there, or this stops: a literal that changed in kid.c is a translation to look at again.
The accented capitals become the bytes kid.c's font has (\\200 .. \\213, its KID_FONT after 4); gen_kid_art.py uses enc()
for the friends' and the hats' names. FOLLOW's songs are replaced by the language's own. NAME_ALPHABET: the letters the
grown-ups' NAME turns through (a space first; the default is A to Z), all of them in the script's byte table.
A language with letters of its own sets SCRIPT (SCRIPTS below says what each does). Its letters are bytes from \\200 up, in the
order of their code points, drawn into kid.c's KID_KANA table (the name is from the first, kana, build):
  "kana" (Japanese): 7 px letters on an 8 px step (KID_ADV 8), drawn from tools/fonts/misaki_kana.bdf (Misaki Gothic 2nd,
    Num Kadoma's free 8x8 font); the capitals and digits stay, centred in the wider step.
  "cyrillic" (Russian): the 6 px step as it is: 5 x 7 capitals, CYR below."""
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACCENTS = "ÁÀÂÃÇÉÊÍÓÔÕÚÈËÎÏÌÑÒÙÛÜÄÖÅÆØ"   # kid.c KID_FONT 37 .., bytes 0x80 .. 0x9A
SOLFA = {"do": 0, "re": 2, "mi": 4, "fa": 5, "sol": 7, "la": 9, "si": 11}
KEYS = ["F3", "FS3", "G3", "GS3", "A3", "AS3", "B3", "C4", "CS4", "D4", "DS4", "E4", "F4", "FS4", "G4", "GS4", "A4",
        "AS4", "B4", "C5", "CS5", "D5", "DS5", "E5", "F5", "FS5", "G5"]   # kid.c K_*: key 0 is F3 (MIDI 53)


DEFAULT_ADV = 6                          # a letter's step at scale 1 in kid.c (KID_ADV)
ADV = DEFAULT_ADV                        # ... in this language
SCRIPT = ""                              # this language's SCRIPT ("", "kana", "cyrillic")
LETTERS = {}                             # its own letters (kana, Cyrillic): character -> byte (from 0x80)

CYR = {                                  # 5 x 7 Cyrillic capitals, as kid.c's KID_FONT: a row a byte, bit 4 the left column
    "А": [0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11], "Б": [0x1F, 0x10, 0x10, 0x1E, 0x11, 0x11, 0x1E],
    "В": [0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E], "Г": [0x1F, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10],
    "Д": [0x0F, 0x09, 0x09, 0x09, 0x09, 0x1F, 0x11], "Е": [0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F],
    "Ё": [0x0A, 0x00, 0x1F, 0x10, 0x1E, 0x10, 0x1F], "Ж": [0x15, 0x15, 0x15, 0x0E, 0x15, 0x15, 0x15],
    "З": [0x1E, 0x01, 0x01, 0x0E, 0x01, 0x01, 0x1E], "И": [0x11, 0x11, 0x13, 0x15, 0x19, 0x11, 0x11],
    "Й": [0x0A, 0x04, 0x11, 0x13, 0x15, 0x19, 0x11], "К": [0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11],
    "Л": [0x0F, 0x09, 0x09, 0x09, 0x09, 0x11, 0x11], "М": [0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11],
    "Н": [0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11], "О": [0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E],
    "П": [0x1F, 0x11, 0x11, 0x11, 0x11, 0x11, 0x11], "Р": [0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10],
    "С": [0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E], "Т": [0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04],
    "У": [0x11, 0x11, 0x0A, 0x04, 0x08, 0x10, 0x10], "Ф": [0x04, 0x0E, 0x15, 0x15, 0x15, 0x0E, 0x04],
    "Х": [0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11], "Ц": [0x11, 0x11, 0x11, 0x11, 0x11, 0x1F, 0x01],
    "Ч": [0x11, 0x11, 0x11, 0x0F, 0x01, 0x01, 0x01], "Ш": [0x15, 0x15, 0x15, 0x15, 0x15, 0x15, 0x1F],
    "Щ": [0x15, 0x15, 0x15, 0x15, 0x15, 0x1F, 0x01], "Ъ": [0x18, 0x08, 0x08, 0x0E, 0x09, 0x09, 0x0E],
    "Ы": [0x11, 0x11, 0x11, 0x1D, 0x15, 0x15, 0x1D], "Ь": [0x10, 0x10, 0x10, 0x1E, 0x11, 0x11, 0x1E],
    "Э": [0x1E, 0x01, 0x01, 0x0F, 0x01, 0x01, 0x1E], "Ю": [0x12, 0x15, 0x15, 0x1D, 0x15, 0x15, 0x12],
    "Я": [0x0F, 0x11, 0x11, 0x0F, 0x05, 0x09, 0x11],
}


def lang(code):
    global ADV, SCRIPT, LETTERS
    p = ROOT / "tools" / "lang" / f"{code}.py"
    if not p.exists():
        raise SystemExit(f"gen_kid_lang: no tools/lang/{code}.py")
    spec = importlib.util.spec_from_file_location(f"lang_{code}", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    ADV, SCRIPT, LETTERS = DEFAULT_ADV, getattr(m, "SCRIPT", ""), {}
    if SCRIPT:
        if SCRIPT not in SCRIPTS:
            raise SystemExit(f"gen_kid_lang: {code}: SCRIPT {SCRIPT!r} is not one of {', '.join(SCRIPTS)}")
        ADV = SCRIPTS[SCRIPT][0]
        texts = list(m.WORDS.values()) + list(m.NAMES.values()) + list(m.HATS.values()) + \
            [n for n, *_ in m.SOLFA_SONGS + m.SONGS] + "".join(getattr(m, "SUBS", {}).values()).split('"') + \
            [getattr(m, "NAME_ALPHABET", "")]       # (all of the name's letters, so each keeps its byte: a kept name is bytes)
        used = sorted({ch for t in texts for ch in t if ord(ch) > 0x7f})
        if len(used) > 128:
            raise SystemExit(f"gen_kid_lang: {code}: {len(used)} letters, 128 at most")
        LETTERS = {ch: 0x80 + i for i, ch in enumerate(used)}
    return m


def glyph_line(ch, b, rows):
    return "    {" + ", ".join(f"0x{v:02X}" for v in rows) + "},   /* \\%03o %s */" % (b, ch)


def kana_glyphs():
    """KID_KANA of a kana language: each kana's 7 rows of 7 px (the left one bit 6), from the BDF, its baseline under
    the 7th row"""
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
    for ch, b in sorted(LETTERS.items(), key=lambda kv: kv[1]):
        if ch not in font:
            raise SystemExit(f"gen_kid_lang: {ch!r} is not in tools/fonts/misaki_kana.bdf")
        out.append(glyph_line(ch, b, font[ch]))
    return out


def cyrillic_glyphs():
    """KID_KANA of a Cyrillic language: each letter's 7 rows of 5 px, from CYR"""
    out = []
    for ch, b in sorted(LETTERS.items(), key=lambda kv: kv[1]):
        if ch not in CYR:
            raise SystemExit(f"gen_kid_lang: {ch!r} is not in CYR (the Cyrillic capitals)")
        out.append(glyph_line(ch, b, CYR[ch]))
    return out


# SCRIPT: (a letter's step, its glyphs' function, where they come from: the comment on KID_KANA)
SCRIPTS = {
    "kana": (8, kana_glyphs, "tools/fonts/misaki_kana.bdf: Misaki Gothic 2nd, (C) Num Kadoma, free"),
    "cyrillic": (DEFAULT_ADV, cyrillic_glyphs, "tools/gen_kid_lang.py CYR: 5 x 7 Cyrillic capitals"),
}


def enc(s):
    """a word as kid.c's band can draw it: capitals, digits, space # ! ? - (and \\n in a card); accents as octal bytes"""
    if "\\n" in s:                        # (a card: its lines, the \n between them kept as kid.c writes it)
        return "\\n".join(enc(x) for x in s.split("\\n"))
    out = []
    for ch in s:
        if ch in LETTERS:
            out.append("\\%03o" % LETTERS[ch])
        elif LETTERS and ord(ch) > 0x7f:
            raise SystemExit(f"gen_kid_lang: {s!r}: {ch!r} is not one of the {SCRIPT} letters")
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
               "SAMBA", "REGGAE", "LULLABY", "HOEDOWN", "LOFI", "ACID", "POLKA", "BOSSA", "FUNK", "SKA", "TRAP", "SALSA",
               "SHUFFLE", "BREAK"}   # (kid.c KID_BEATS: the beats' names)


def fits(code, src, en, tr):
    """does a word fit across the screen (240 px, 6 px a letter at scale 1) where kid.c draws it"""
    n = shown(tr)
    m = re.search(r'\{"%s", (\d+), \d+, (\d)\}' % re.escape(en), src)     # (the name screen's lines: x, y, scale)
    if m:
        ok = n * ADV * int(m[2]) - int(m[2]) <= 238 - int(m[1])
    elif en in WRITE_WORDS and n * ADV * 2 - 2 > 176:                          # (WRITE: beside the friend, scale 2)
        ok = False
    elif en in ("HI!", "HI"):                                                  # (the hello: scale 4 at the smallest
        ok = n * ADV * 4 - 4 <= (228 if en == "HI!" else 236)   #  alone, 7 with a name, smaller as it needs: kid_hello_fit)
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


def song_line(name, keys, pic):
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
    return "\n".join(lines + [line.rstrip() + f", KID_PIC_{re.sub(r'[^A-Z0-9]', '_', pic)}}},"])


def main(code, out):
    L = lang(code)
    src = (ROOT / "firmware" / "src" / "kid.c").read_text()
    for en, tr in L.WORDS.items():
        lit = '"' + en + '"'
        if lit not in src:
            raise SystemExit(f"gen_kid_lang: {code}: {lit} is not in kid.c any more")
        if "\\n" in en:                    # a card: up to 3 lines of 17 (13 kana)
            ls, most = tr.split("\\n"), 17 if ADV == DEFAULT_ADV else 220 // (2 * ADV)
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
    art = (ROOT / "tools" / "gen_kid_art.py").read_text()
    friends = re.findall(r'^\s*\("([A-Z][A-Z -]*)", ', art, re.M) + \
        re.findall(r'\("([A-Z][A-Z -]*)", ', art[art.index("STAND_INS = {"):art.index("\n}", art.index("STAND_INS = {"))])
    pics = getattr(L, "SONG_PICS", {})                 # each song's picture: a friend (gen_kid_art.py FRIENDS), so a child
    for n, *_ in L.SOLFA_SONGS + L.SONGS:             # who can't read yet knows the song (kid.c kid_band_icon)
        if pics.get(n) not in friends:
            raise SystemExit(f"gen_kid_lang: {code}: the song {n!r} needs a friend's picture in SONG_PICS ({pics.get(n)!r})")
    if len(set(pics[n] for n, *_ in L.SOLFA_SONGS + L.SONGS)) < len(L.SOLFA_SONGS + L.SONGS):
        raise SystemExit(f"gen_kid_lang: {code}: two songs with the same picture")
    songs = [song_line(n, solfa_keys(t, sh), pics[n]) for n, sh, _, t in L.SOLFA_SONGS] + \
            [song_line(n, note_keys(t), pics[n]) for n, t in L.SONGS]
    for n, *_ in L.SOLFA_SONGS + L.SONGS:
        if shown(n) > 14 * DEFAULT_ADV // ADV:
            raise SystemExit(f"gen_kid_lang: {code}: the song {n!r}: {14 * DEFAULT_ADV // ADV} letters at most")
    src = src[:i] + "static const kid_song_t KID_SONGS[] = {\n" + "\n".join(songs) + src[j:]
    head = (f"/* generated by tools/gen_kid_lang.py from firmware/src/kid.c and tools/lang/{code}.py: Rainbow mode in "
            f"this language. Do not edit: edit those. */\n#define KID_DOREMI_FIRST {1 if L.DOREMI else 0}\n")
    abc = getattr(L, "NAME_ALPHABET", "")           # the letters of the grown-ups' NAME (kid.c KID_NAME_ABC): a space, then these
    if abc:
        head += f'#define KID_NAME_ABC " {enc(abc)}"\n'
    if LETTERS:                                    # (its own letters: a table of them, and the step when it is not 6 px)
        _, glyphs, source = SCRIPTS[SCRIPT]
        head += ((f"#define KID_ADV {ADV}\n" if ADV != DEFAULT_ADV else "") + f"#define KID_KANA_N {len(LETTERS)}\n"
                 f"static const uint8_t KID_KANA[KID_KANA_N][7] = {{   /* {source} */\n" + "\n".join(glyphs()) + "\n};\n")
    Path(out).write_text(head + src)
    print(f"kid lang: {code}, {len(L.WORDS)} words, {len(songs)} songs -> {out}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

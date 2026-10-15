#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Rainbow mode's friends: 40 pixel-art pictures (run by tools/build.py generate()).

  gen_kid_art.py OUT.h [--png SHEET.png]

Each friend is drawn from shapes (no antialiasing) on a roomy canvas, then outlined (every empty pixel that
touches the picture becomes the outline colour), trimmed, centred across a 48 x 48 grid and stood on its
bottom row. A picture that would not fit stops the build: nothing is ever cut off. At most 15 colours per picture (index 0 = see-through); the
header stores 4 bits per pixel and a 16-entry RGB565 palette per picture, in the order of FRIENDS below
(firmware/src/kid.c matches its sounds to the same order). --png writes a contact sheet for checking by eye.
KID_NAME in the environment (a GitHub secret in the workflow) is the name the power-up hello greets: capitals,
spaces and at most 10 letters are kept, "!" is added. Without it the hello is a plain HI!, so the name is never
in the source.
"""
import os
import re
import sys
from PIL import Image, ImageDraw

N = 48                           # a picture: N x N, shapes at most N - 2 across (the outline round them)
W = 72                           # the drawing canvas: room on every side, so nothing is cut while drawing
OFF = 12                         # design coordinates (about 0 .. 47) sit this far into the canvas
OUT = (52, 26, 58)               # the outline: a dark plum, softer than black
C = dict(
    white=(255, 255, 255), black=(28, 20, 36), cream=(255, 244, 214), grey=(176, 180, 200), dgrey=(96, 98, 120),
    yellow=(255, 216, 46), dyellow=(236, 166, 24), gold=(255, 178, 30), orange=(255, 132, 36), dorange=(214, 88, 24),
    red=(236, 52, 64), dred=(170, 24, 48), pink=(255, 138, 196), dpink=(222, 92, 162), lpink=(255, 200, 226),
    hpink=(236, 64, 150), blue=(56, 128, 244), dblue=(30, 70, 170), lblue=(150, 206, 255), mblue=(96, 160, 236),
    navy=(30, 36, 90), teal=(36, 196, 190), green=(70, 200, 90), dgreen=(36, 130, 64), lime=(176, 232, 70),
    dlime=(112, 180, 40), lgreen=(214, 252, 170), purple=(150, 88, 226), dpurple=(104, 56, 180),
    lpurple=(204, 164, 255), brown=(150, 92, 46), dbrown=(84, 50, 32), tan=(226, 176, 112), dtan=(186, 128, 70),
    silver=(214, 220, 236), dwhite=(204, 212, 238), sky=(150, 206, 255), glass=(212, 236, 255),
    mint=(110, 230, 196), dmint=(52, 176, 148),
)


class Pic:
    """draw in design coordinates (0 .. 47, a little past is fine); done() outlines, trims and places it"""

    def __init__(self):
        self.im = Image.new("RGBA", (W, W), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def _c(self, c):
        return C[c] + (255,) if c else (0, 0, 0, 0)

    def ell(self, cx, cy, rx, ry, c):
        self.d.ellipse([cx - rx + OFF, cy - ry + OFF, cx + rx + OFF, cy + ry + OFF], fill=self._c(c))

    def ball(self, cx, cy, rx, ry, c, dark):      # a shaded round shape: the dark side down and to the right
        self.ell(cx, cy, rx, ry, dark)
        self.ell(cx - 1, cy - 1, rx - 1, ry - 1, c)

    def rect(self, x0, y0, x1, y1, c):
        self.d.rectangle([x0 + OFF, y0 + OFF, x1 + OFF, y1 + OFF], fill=self._c(c))

    def poly(self, pts, c):
        self.d.polygon([(x + OFF, y + OFF) for x, y in pts], fill=self._c(c))

    def line(self, pts, c, w=2):
        self.d.line([(x + OFF, y + OFF) for x, y in pts], fill=self._c(c), width=w)

    def pie(self, cx, cy, r, a0, a1, c):
        self.d.pieslice([cx - r + OFF, cy - r + OFF, cx + r + OFF, cy + r + OFF], a0, a1, fill=self._c(c))

    def px(self, x, y, c):
        self.im.putpixel((x + OFF, y + OFF), self._c(c))

    def eye(self, x, y, r=4):                     # a big shiny eye: white, a dark pupil low, a white spark
        self.ell(x, y, r, r + 1, "white")
        self.ell(x, y + 1, r - 1, r, "black")
        self.rect(x - 1, y - 1, x, y, "white")

    def dot_eye(self, x, y):                      # a small solid eye (ducks, a robot's lamp), with a spark
        self.ell(x, y, 2, 3, "black")
        self.px(x - 1, y - 1, "white")

    def smile(self, x, y, w=3, c="black"):
        self.line([(x - w, y), (x - w + 1, y + 1), (x + w - 1, y + 1), (x + w, y)], c, 1)
        self.line([(x - w + 1, y + 1), (x + w - 1, y + 1)], c, 1)

    def cheek(self, x, y):
        self.ell(x, y, 2, 1, "pink")

    def done(self):
        """outline, trim to the outline, then centre it across and stand it on the bottom row"""
        src = self.im.copy()
        for y in range(W):
            for x in range(W):
                if src.getpixel((x, y))[3]:
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < W and 0 <= yy < W and src.getpixel((xx, yy))[3]:
                        self.im.putpixel((x, y), OUT + (255,))
                        break
        x0, y0, x1, y1 = self.im.getbbox()
        w, h = x1 - x0, y1 - y0
        if w > N or h > N:
            raise SystemExit(f"a picture is {w} x {h}: {N} x {N} at most (it would be cut)")
        if min(x0, y0) == 0 or x1 == W or y1 == W:
            raise SystemExit("a picture reaches the edge of the drawing canvas (it would be cut)")
        out = Image.new("RGBA", (N, N), (0, 0, 0, 0))
        out.paste(self.im.crop((x0, y0, x1, y1)), ((N - w) // 2, N - h))
        self.im = out
        return self


# ---------------------------------------------------------------- the friends
SHADE = dict(gold="dyellow", lpurple="purple", yellow="dyellow", pink="dpink", lblue="mblue", white="dwhite", lime="dlime", red="dred",
             blue="dblue", orange="dorange", green="dgreen", purple="dpurple", tan="dtan", brown="dbrown")


def ducky(body, wing, extra=None):
    def f():
        p = Pic()
        p.poly([(38, 30), (45, 20), (43, 36)], SHADE[body])          # tail, up at the back
        p.ball(26, 37, 17, 10, body, SHADE[body])                   # body
        p.ball(19, 19, 10, 10, body, SHADE[body])                   # head
        p.ell(7, 22, 6, 3, "orange")                                # beak
        p.rect(3, 23, 10, 24, "dorange")
        p.ell(28, 34, 9, 5, wing)                                   # wing
        p.ell(27, 32, 8, 3, body)
        p.dot_eye(17, 17)
        p.cheek(22, 23)
        if extra:
            extra(p)
        return p.done()
    return f


def goldcrown(p):                      # the secret friend's crown, and sparkles round it
    crown(p)
    for x, y in ((2, 8), (30, 4), (33, 15), (40, 36), (2, 36)):
        p.px(x, y, "white"); p.px(x - 1, y, "yellow"); p.px(x + 1, y, "yellow"); p.px(x, y - 1, "yellow"); p.px(x, y + 1, "yellow")


def bow(p):
    p.poly([(12, 7), (18, 10), (12, 13)], "hpink"); p.poly([(24, 7), (18, 10), (24, 13)], "hpink")
    p.ell(18, 10, 2, 2, "red")


def bucket_shades(p):                  # shades, and a rainbow bucket hat (asked for at home)
    p.rect(11, 14, 25, 15, "black")
    p.ell(15, 17, 4, 3, "black"); p.ell(23, 17, 3, 3, "black")
    p.px(13, 16, "lblue"); p.px(21, 16, "lblue")
    for y, (x0, x1), c in ((2, (14, 24), "red"), (3, (13, 25), "red"), (4, (12, 26), "orange"), (5, (12, 26), "orange"),
                           (6, (11, 27), "yellow"), (7, (11, 27), "green"), (8, (11, 27), "blue"), (9, (11, 27), "blue"),
                           (10, (11, 27), "purple")):
        p.rect(x0, y, x1, y, c)
    for y, (x0, x1) in ((11, (8, 30)), (12, (7, 31)), (13, (6, 32))):   # the brim, sloping down all round
        p.rect(x0, y, x1, y, "purple")


def axolotl():
    p = Pic()
    p.poly([(34, 32), (45, 25), (45, 43)], "lpink")              # tail fin
    p.ball(29, 35, 12, 7, "pink", "dpink")                       # body
    p.ell(22, 43, 3, 3, "dpink"); p.ell(35, 43, 3, 3, "dpink")   # legs
    for (ax, ay), (tx, ty) in (((10, 14), (4, 8)), ((8, 19), (2, 17)), ((10, 24), (4, 27)),
                               ((30, 14), (36, 8)), ((32, 19), (38, 17)), ((30, 24), (36, 27))):   # frilly gills
        p.line([(ax, ay), (tx, ty)], "hpink", 3)
        p.ell(tx, ty, 2, 2, "hpink")
    p.ball(20, 19, 13, 11, "pink", "dpink")                      # head
    p.eye(14, 17, 3); p.eye(26, 17, 3)
    p.smile(20, 24, 4)
    p.cheek(10, 23); p.cheek(30, 23)
    return p.done()


def unicorn():
    p = Pic()
    p.poly([(14, 46), (16, 30), (32, 30), (36, 46)], "dwhite")   # neck
    p.poly([(16, 46), (17, 31), (30, 31), (33, 46)], "white")
    p.ball(23, 24, 11, 10, "white", "dwhite")                    # head
    p.ball(12, 31, 8, 6, "white", "dwhite")                      # snout
    p.ell(8, 33, 4, 3, "lpink")
    p.rect(6, 32, 7, 33, "dpink"); p.rect(10, 32, 11, 33, "dpink")
    p.poly([(20, 15), (26, 1), (29, 16)], "gold")                # horn, with two stripes
    p.line([(21, 12), (27, 10)], "yellow"); p.line([(23, 7), (27, 6)], "yellow")
    p.poly([(27, 16), (31, 9), (34, 19)], "white")               # ear
    for i, c in enumerate(("red", "orange", "yellow", "green", "blue", "purple")):   # rainbow mane
        p.ell(34 + i // 2, 18 + i * 4, 5, 3, c)
    p.eye(20, 22, 3)
    p.cheek(17, 28)
    return p.done()


def giraffe():
    p = Pic()
    p.rect(25, 16, 34, 44, "dyellow")                            # neck
    p.rect(25, 16, 32, 44, "yellow")
    for x, y in ((28, 22), (31, 29), (27, 35), (31, 41)):        # big spots
        p.ell(x, y, 3, 2, "brown")
    p.rect(34, 18, 37, 42, "brown")                              # mane
    p.ball(21, 14, 11, 8, "yellow", "dyellow")                   # head
    p.ell(11, 17, 6, 5, "tan")                                   # muzzle
    p.rect(8, 15, 9, 16, "dbrown"); p.rect(12, 15, 13, 16, "dbrown")
    p.rect(18, 3, 20, 8, "brown"); p.rect(25, 3, 27, 8, "brown")  # ossicones, thick
    p.ell(19, 3, 2, 2, "dbrown"); p.ell(26, 3, 2, 2, "dbrown")
    p.ell(32, 9, 4, 2, "yellow")                                 # ear
    p.eye(21, 12, 3)
    p.smile(13, 20, 2)
    return p.done()


def goo(main, dark, light):
    def f():
        p = Pic()
        for x, h in ((9, 5), (17, 7), (31, 6), (39, 4)):        # drips
            p.rect(x - 2, 38, x + 2, 38 + h, main); p.ell(x, 38 + h, 2, 2, main)
        p.ball(24, 30, 19, 13, main, dark)                       # the blob
        p.ell(24, 20, 13, 11, main)
        p.ell(16, 14, 4, 3, light)                               # shine
        p.ell(13, 16, 1, 1, "white")
        p.eye(18, 24, 4); p.eye(30, 24, 4)
        p.pie(24, 30, 6, 0, 180, "black")                       # a big grin
        p.ell(24, 34, 3, 1, "hpink")
        p.cheek(11, 30); p.cheek(37, 30)
        return p.done()
    return f


def bluepup():                                                   # a blue heeler pup (original design)
    p = Pic()
    p.poly([(7, 2), (18, 14), (5, 20)], "navy")                  # ears
    p.poly([(41, 2), (30, 14), (43, 20)], "navy")
    p.poly([(9, 8), (14, 14), (8, 17)], "tan"); p.poly([(39, 8), (34, 14), (40, 17)], "tan")
    p.ball(24, 27, 17, 15, "mblue", "blue")                      # head
    p.ell(24, 14, 5, 3, "navy")                                  # a dark patch on top
    p.ell(15, 25, 6, 6, "navy"); p.ell(33, 25, 6, 6, "navy")     # eye patches
    p.ell(24, 36, 11, 7, "cream")                                # muzzle
    p.eye(15, 25, 4); p.eye(33, 25, 4)
    p.ell(24, 32, 3, 2, "black")                                 # nose
    p.smile(24, 37, 4)
    p.ell(26, 41, 2, 2, "hpink")                                 # tongue
    return p.done()


def monster(main, dark, nose, cookie=False):
    def f():
        p = Pic()
        for x, y in ((9, 10), (15, 6), (23, 4), (31, 5), (38, 9), (42, 16), (6, 18)):   # fur tufts
            p.ell(x, y, 4, 4, main)
        p.ball(24, 26, 19, 19, main, dark)
        p.ell(16, 14, 6, 6, "white"); p.ell(31, 14, 6, 6, "white")   # googly eyes on top
        p.ell(17, 15, 3, 3, "black"); p.ell(30, 15, 3, 3, "black")
        p.rect(15, 13, 16, 14, "white"); p.rect(28, 13, 29, 14, "white")
        if nose:
            p.ell(24, 24, 5, 4, nose)
            p.px(22, 22, "white")
        p.pie(24, 29, 11, 0, 180, "black")                       # a big happy mouth
        p.ell(24, 37, 6, 2, "red")
        if cookie:
            p.ball(38, 37, 7, 7, "tan", "dtan")
            for x, y in ((35, 35), (39, 38), (36, 40), (41, 34)):
                p.ell(x, y, 1, 1, "dbrown")
        return p.done()
    return f


def doggy():                                                     # April: brown and black Aussie / shepherd mix
    p = Pic()
    p.poly([(8, 2), (18, 12), (6, 20)], "dbrown")                # tall ears
    p.poly([(40, 2), (30, 12), (42, 20)], "dbrown")
    p.poly([(10, 7), (15, 12), (9, 16)], "tan"); p.poly([(38, 7), (33, 12), (39, 16)], "tan")
    p.ball(24, 26, 16, 15, "brown", "dbrown")                    # head
    p.ell(24, 17, 10, 8, "black")                                # dark saddle on top
    p.ell(24, 35, 10, 8, "tan")                                  # muzzle
    p.eye(16, 24, 4); p.eye(32, 24, 4)
    p.ell(16, 18, 2, 1, "tan"); p.ell(32, 18, 2, 1, "tan")       # eyebrow dots
    p.ell(24, 31, 4, 3, "black")                                 # nose
    p.px(23, 30, "grey")
    p.smile(24, 37, 4)
    p.ell(26, 41, 2, 3, "hpink")
    return p.done()


def scissors():
    p = Pic()
    p.poly([(21, 27), (43, 4), (45, 7), (25, 29)], "dwhite")      # blades, thick
    p.poly([(21, 21), (43, 44), (41, 46), (19, 25)], "dwhite")
    p.line([(25, 26), (43, 6)], "silver"); p.line([(24, 22), (42, 42)], "silver")
    p.ell(22, 24, 2, 2, "dgrey")
    for cx, cy in ((11, 12), (11, 36)):                           # handles, chunky rings
        p.ell(cx, cy, 9, 9, "hpink")
        p.ell(cx, cy, 4, 4, None)
    p.poly([(16, 16), (23, 22), (21, 25), (14, 20)], "hpink")
    p.poly([(16, 32), (23, 26), (21, 23), (14, 28)], "hpink")
    return p.done()


def ghost():
    p = Pic()
    p.ball(24, 20, 16, 16, "white", "dwhite")
    p.rect(8, 20, 40, 38, "white"); p.rect(38, 20, 40, 38, "dwhite")
    for i, x in enumerate(range(8, 41, 8)):                      # wavy hem
        p.ell(x + 4, 39, 4, 4 if i % 2 else 3, "white")
    p.ell(6, 26, 3, 3, "white")                                  # waving arms
    p.ell(42, 28, 3, 3, "white")
    p.ell(17, 18, 3, 5, "black"); p.ell(31, 18, 3, 5, "black")
    p.rect(16, 15, 17, 16, "white"); p.rect(30, 15, 31, 16, "white")
    p.ell(24, 30, 4, 4, "black"); p.ell(24, 31, 2, 2, "red")    # an "Ooo!" mouth
    p.cheek(11, 25); p.cheek(37, 25)
    return p.done()


def webhero():                                                   # a masked web hero (original design)
    import math
    p = Pic()
    p.ball(24, 24, 18, 21, "red", "dred")
    for a in range(0, 360, 45):                                  # the web: a few strong lines
        x = 24 + 22 * math.cos(math.radians(a)); y = 24 + 24 * math.sin(math.radians(a))
        p.line([(24, 24), (x, y)], "dred", 1)
    for r in (8, 15):
        p.d.ellipse([24 - r + OFF, 24 - r * 1.15 + OFF, 24 + r + OFF, 24 + r * 1.15 + OFF], outline=C["dred"] + (255,))
    p.poly([(7, 15), (21, 20), (21, 29), (9, 27)], "black")      # big eye shapes
    p.poly([(41, 15), (27, 20), (27, 29), (39, 27)], "black")
    p.poly([(10, 18), (19, 22), (19, 27), (11, 25)], "white")
    p.poly([(38, 18), (29, 22), (29, 27), (37, 25)], "white")
    im = p.im                                                    # keep only the head
    for y in range(W):
        for x in range(W):
            if ((x - 24 - OFF) / 18.5) ** 2 + ((y - 24 - OFF) / 21.5) ** 2 > 1:
                im.putpixel((x, y), (0, 0, 0, 0))
    return p.done()


def butterfly():
    p = Pic()
    p.ball(13, 15, 11, 11, "purple", "dpurple"); p.ball(36, 15, 11, 11, "purple", "dpurple")
    p.ball(14, 34, 9, 8, "hpink", "dpink"); p.ball(35, 34, 9, 8, "hpink", "dpink")
    p.ell(12, 14, 5, 5, "lpurple"); p.ell(36, 14, 5, 5, "lpurple")
    p.ell(14, 35, 3, 3, "yellow"); p.ell(35, 35, 3, 3, "yellow")
    p.ell(24, 26, 3, 15, "dbrown")
    p.ell(24, 11, 4, 4, "dbrown")
    p.line([(22, 8), (17, 1)], "dbrown"); p.line([(26, 8), (31, 1)], "dbrown")
    p.ell(17, 1, 2, 2, "hpink"); p.ell(31, 1, 2, 2, "hpink")
    p.px(23, 10, "white"); p.px(26, 10, "white")
    return p.done()


def kitty():
    p = Pic()
    p.poly([(6, 3), (18, 12), (6, 22)], "orange"); p.poly([(42, 3), (30, 12), (42, 22)], "orange")
    p.poly([(9, 9), (14, 13), (9, 18)], "lpink"); p.poly([(39, 9), (34, 13), (39, 18)], "lpink")
    p.ball(24, 27, 18, 16, "orange", "dorange")
    for y in (14, 18):                                           # stripes
        p.rect(19, y, 29, y + 1, "dorange")
    p.ell(24, 35, 9, 6, "cream")
    p.eye(16, 26, 4); p.eye(32, 26, 4)
    p.poly([(21, 31), (27, 31), (24, 34)], "hpink")
    p.smile(24, 36, 3)
    for y in (32, 36):                                           # whiskers, 2 px
        p.line([(2, y - 2), (10, y)], "dbrown"); p.line([(38, y), (46, y - 2)], "dbrown")
    return p.done()


def frog():
    p = Pic()
    p.ball(24, 32, 20, 13, "green", "dgreen")
    p.ball(13, 16, 8, 8, "green", "dgreen"); p.ball(35, 16, 8, 8, "green", "dgreen")
    p.eye(12, 15, 4); p.eye(34, 15, 4)
    p.ell(24, 37, 12, 6, "lime")
    p.line([(10, 29), (24, 34), (38, 29)], "dgreen", 2)
    p.cheek(8, 31); p.cheek(40, 31)
    p.ell(9, 45, 5, 2, "dgreen"); p.ell(39, 45, 5, 2, "dgreen")
    return p.done()


def robot():
    p = Pic()
    p.rect(23, 3, 25, 8, "dgrey"); p.ell(24, 3, 3, 2, "red")
    p.rect(8, 9, 40, 34, "dwhite"); p.rect(8, 9, 38, 32, "silver")
    p.rect(3, 16, 7, 26, "dgrey"); p.rect(41, 16, 45, 26, "dgrey")
    p.rect(11, 12, 37, 30, "lblue")
    p.ell(17, 19, 4, 4, "white"); p.ell(31, 19, 4, 4, "white")
    p.ell(17, 20, 2, 2, "blue"); p.ell(31, 20, 2, 2, "blue")
    for i, c in enumerate(("red", "yellow", "green", "blue", "purple")):   # a light-up smile
        p.rect(14 + i * 4, 25, 16 + i * 4, 27, c)
    p.rect(14, 36, 34, 45, "silver")
    p.ell(24, 40, 3, 3, "hpink")
    p.rect(16, 34, 32, 35, "dgrey")
    return p.done()


def rainbow():
    p = Pic()
    for i, c in enumerate(("red", "orange", "yellow", "green", "blue", "purple")):
        p.pie(24, 32, 21 - i * 3, 180, 360, c)
    p.pie(24, 32, 5, 180, 360, None)                             # the arch's hole
    p.rect(-2, 33, 50, 40, None)
    for cx in (9, 39):                                           # clouds at the ends, with faces
        p.ball(cx, 34, 6, 5, "white", "dwhite"); p.ell(cx - 4, 37, 3, 3, "white"); p.ell(cx + 4, 37, 3, 3, "white")
        p.ell(cx - 2, 34, 1, 1, "black"); p.ell(cx + 2, 34, 1, 1, "black"); p.px(cx, 37, "hpink")
    return p.done()


def crown(p):
    p.poly([(11, 12), (13, 6), (16, 9), (19, 4), (22, 9), (25, 6), (27, 12)], "gold")
    p.rect(11, 11, 27, 13, "gold")
    p.ell(19, 9, 1, 1, "red"); p.ell(14, 11, 1, 1, "lblue"); p.ell(24, 11, 1, 1, "lblue")


def redpup():                                                    # a red heeler pup (original design)
    p = Pic()
    p.poly([(7, 2), (18, 14), (5, 20)], "dorange")               # ears
    p.poly([(41, 2), (30, 14), (43, 20)], "dorange")
    p.poly([(9, 8), (14, 14), (8, 17)], "cream"); p.poly([(39, 8), (34, 14), (40, 17)], "cream")
    p.ball(24, 27, 17, 15, "orange", "dorange")                  # head
    p.ell(24, 14, 5, 3, "dorange")
    p.ell(15, 25, 6, 6, "dorange"); p.ell(33, 25, 6, 6, "dorange")
    p.ell(24, 36, 11, 7, "cream")
    p.eye(15, 25, 4); p.eye(33, 25, 4)
    p.ell(24, 32, 3, 2, "black")
    p.smile(24, 37, 4)
    p.ell(26, 41, 2, 2, "hpink")
    return p.done()


def yellowbird():                                                # a big yellow bird (original design)
    p = Pic()
    for i in range(7):                                           # feathery body
        p.ell(10 + i * 5, 34 + (i % 2) * 2, 6, 9, "dyellow" if i % 2 else "yellow")
    p.ball(24, 18, 13, 13, "yellow", "dyellow")                  # head
    for x in (16, 22, 28):                                       # a tuft of feathers on top
        p.ell(x, 5, 2, 4, "yellow")
    p.eye(19, 16, 4); p.eye(29, 16, 4)
    p.poly([(16, 23), (33, 23), (24, 31)], "orange")             # a big beak
    p.rect(17, 23, 32, 24, "dorange")
    return p.done()


def slimy():                                                     # a green slime ghost (original design)
    p = Pic()
    p.ball(24, 22, 17, 16, "lime", "dlime")
    p.poly([(8, 24), (40, 24), (36, 44), (24, 38), (12, 44)], "lime")   # a wispy tail
    p.ell(6, 30, 4, 3, "lime"); p.ell(42, 30, 4, 3, "lime")      # little arms
    p.eye(17, 18, 4); p.eye(31, 18, 4)
    p.pie(24, 26, 9, 0, 180, "black")                            # a goofy grin, tongue out
    p.ell(27, 33, 3, 3, "hpink")
    p.ell(13, 10, 3, 2, "lgreen")
    return p.done()


def bunny():
    p = Pic()
    p.ell(16, 10, 4, 11, "white"); p.ell(32, 10, 4, 11, "white")  # long ears
    p.ell(16, 11, 2, 8, "lpink"); p.ell(32, 11, 2, 8, "lpink")
    p.ball(24, 30, 16, 14, "white", "dwhite")
    p.eye(17, 28, 4); p.eye(31, 28, 4)
    p.poly([(21, 34), (27, 34), (24, 37)], "hpink")
    p.smile(24, 39, 3)
    p.rect(22, 40, 26, 43, "white")                              # two front teeth
    p.line([(24, 40), (24, 43)], "dwhite", 1)
    p.cheek(11, 35); p.cheek(37, 35)
    return p.done()


def panda():
    p = Pic()
    p.ell(9, 10, 6, 6, "black"); p.ell(39, 10, 6, 6, "black")    # ears
    p.ball(24, 27, 18, 16, "white", "dwhite")
    p.ell(15, 25, 6, 7, "black"); p.ell(33, 25, 6, 7, "black")   # eye patches
    p.eye(15, 25, 3); p.eye(33, 25, 3)
    p.ell(24, 33, 4, 3, "black")
    p.smile(24, 37, 3)
    p.cheek(9, 33); p.cheek(39, 33)
    return p.done()


def penguin():
    p = Pic()
    p.ball(24, 26, 16, 19, "navy", "black")                      # body
    p.ell(24, 30, 11, 14, "white")                               # white tummy
    p.ell(24, 17, 12, 9, "white")                                # face
    p.ell(7, 30, 4, 9, "navy"); p.ell(41, 30, 4, 9, "navy")      # flippers
    p.eye(19, 16, 3); p.eye(29, 16, 3)
    p.poly([(20, 21), (28, 21), (24, 26)], "orange")
    p.ell(17, 45, 5, 2, "orange"); p.ell(31, 45, 5, 2, "orange")  # feet
    p.cheek(14, 21); p.cheek(34, 21)
    return p.done()


def owl():
    p = Pic()
    p.poly([(8, 4), (16, 12), (8, 16)], "brown"); p.poly([(40, 4), (32, 12), (40, 16)], "brown")   # ear tufts
    p.ball(24, 26, 17, 19, "brown", "dbrown")
    p.ell(24, 33, 11, 11, "tan")                                 # tummy
    for x, y in ((19, 30), (29, 30), (24, 36), (19, 41), (29, 41)):
        p.poly([(x - 2, y), (x + 2, y), (x, y + 2)], "dtan")     # feathers
    p.ell(16, 18, 7, 7, "cream"); p.ell(32, 18, 7, 7, "cream")   # big eye rings
    p.eye(16, 18, 4); p.eye(32, 18, 4)
    p.poly([(22, 22), (26, 22), (24, 27)], "orange")
    p.ell(6, 30, 3, 9, "dbrown"); p.ell(42, 30, 3, 9, "dbrown")  # wings
    return p.done()


def bee():
    p = Pic()
    p.ell(14, 10, 8, 7, "lblue"); p.ell(32, 10, 8, 7, "lblue")   # wings
    p.ell(14, 10, 5, 4, "white"); p.ell(32, 10, 5, 4, "white")
    p.ball(24, 28, 19, 15, "yellow", "dyellow")                  # round body
    for x in (14, 24, 34):                                       # stripes
        p.rect(x - 2, 15, x + 2, 42, "black")
    p.ball(13, 28, 9, 9, "yellow", "dyellow")                    # face
    p.eye(10, 26, 3); p.eye(17, 26, 3)
    p.smile(13, 32, 2)
    p.cheek(7, 31)
    p.poly([(42, 26), (47, 28), (42, 30)], "black")              # stinger
    return p.done()


def ladybug():
    p = Pic()
    p.ball(24, 29, 19, 15, "red", "dred")                        # shell
    p.rect(23, 14, 25, 44, "black")                              # the line down the back
    for x, y in ((14, 24), (34, 24), (12, 35), (36, 35), (19, 41), (29, 41)):
        p.ell(x, y, 3, 3, "black")
    p.ball(24, 11, 11, 8, "black", "black")                      # head
    p.eye(19, 11, 3); p.eye(29, 11, 3)
    p.line([(18, 6), (14, 3)], "black"); p.line([(30, 6), (34, 3)], "black")   # antennae
    p.ell(14, 3, 2, 2, "black"); p.ell(34, 3, 2, 2, "black")
    return p.done()


def dino():
    p = Pic()
    p.poly([(36, 34), (47, 44), (34, 44)], "dgreen")             # tail
    for x, y in ((14, 6), (22, 3), (30, 6), (36, 12)):           # spikes on top
        p.poly([(x - 3, y + 6), (x, y), (x + 3, y + 6)], "orange")
    p.ball(24, 32, 15, 13, "green", "dgreen")                    # body
    p.ball(18, 18, 14, 11, "green", "dgreen")                    # big head
    p.ell(24, 36, 8, 7, "lime")                                  # tummy
    p.eye(19, 15, 4)
    p.pie(14, 22, 8, 0, 180, "black")                            # a toothy grin
    p.poly([(9, 22), (11, 25), (13, 22)], "white"); p.poly([(15, 22), (17, 25), (19, 22)], "white")
    p.ell(14, 45, 4, 2, "dgreen"); p.ell(30, 45, 4, 2, "dgreen")
    return p.done()


def whale():
    p = Pic()
    p.poly([(38, 26), (47, 16), (47, 34)], "blue")               # tail
    p.ball(22, 30, 20, 13, "blue", "dblue")
    p.ell(20, 36, 15, 6, "lblue")                                # belly
    p.ell(14, 26, 3, 4, "white"); p.ell(14, 27, 2, 3, "black")   # eye
    p.px(13, 25, "white")
    p.smile(10, 33, 4)
    p.cheek(18, 31)
    p.line([(22, 16), (22, 9)], "lblue", 3)                      # a spout of water
    p.ell(18, 7, 3, 3, "lblue"); p.ell(26, 7, 3, 3, "lblue"); p.ell(22, 5, 3, 3, "lblue")
    return p.done()


def octopus():
    p = Pic()
    for i, x in enumerate((6, 13, 20, 28, 35, 42)):              # legs, curling
        p.ell(x, 38, 3, 8, "purple"); p.ell(x + (2 if i < 3 else -2), 45, 3, 2, "purple")
    p.ball(24, 20, 17, 17, "purple", "dpurple")
    p.ell(17, 11, 4, 3, "lpurple")
    p.eye(17, 21, 4); p.eye(31, 21, 4)
    p.smile(24, 29, 4)
    p.cheek(11, 27); p.cheek(37, 27)
    return p.done()


def fish():
    p = Pic()
    p.poly([(34, 24), (47, 12), (47, 38)], "orange")             # tail
    p.ball(21, 25, 19, 14, "orange", "dorange")
    p.rect(14, 12, 18, 38, "white"); p.rect(26, 13, 30, 37, "white")   # clownfish stripes
    p.poly([(16, 11), (26, 3), (30, 12)], "dorange")             # fin
    p.eye(9, 22, 4)
    p.smile(6, 30, 2)
    p.cheek(13, 29)
    return p.done()


def turtle():
    p = Pic()
    p.ball(8, 28, 8, 7, "lime", "dlime")                         # head
    p.eye(7, 26, 3)
    p.smile(6, 32, 2)
    p.ell(14, 41, 4, 4, "lime"); p.ell(34, 41, 4, 4, "lime")     # legs
    p.ball(25, 30, 18, 13, "green", "dgreen")                    # shell
    for x, y in ((18, 26), (30, 26), (24, 34), (14, 34), (36, 34)):
        p.ell(x, y, 4, 3, "dgreen")
    p.rect(8, 38, 43, 40, "dlime")                               # its rim
    return p.done()


def icecream():
    p = Pic()
    p.poly([(12, 26), (36, 26), (24, 45)], "tan")                # cone
    for y in (31, 36, 41):                                       # its waffle lines, inside the cone
        half = (45 - y) * 12 // 19
        p.rect(24 - half + 1, y, 24 + half - 1, y, "dtan")
    p.ball(24, 24, 13, 7, "lpink", "pink")                       # a scoop of strawberry
    p.ball(24, 14, 11, 9, "cream", "tan")                        # and one of vanilla
    for x, y in ((18, 12), (26, 9), (30, 16), (20, 20)):         # sprinkles
        p.rect(x, y, x + 2, y, "hpink")
    p.ell(24, 5, 3, 3, "red")                                    # a cherry
    p.eye(20, 15, 3); p.eye(28, 15, 3)
    p.smile(24, 21, 2)
    return p.done()


def cupcake():
    p = Pic()
    p.poly([(9, 28), (39, 28), (35, 46), (13, 46)], "lblue")     # the cup
    for x in (14, 20, 26, 32):
        p.rect(x, 29, x + 1, 45, "mblue")
    p.ball(24, 24, 17, 8, "pink", "dpink")                       # frosting
    p.ball(24, 15, 12, 8, "pink", "dpink")
    p.ell(24, 6, 4, 4, "red")                                    # a cherry
    for x, y in ((14, 22), (30, 20), (22, 13), (34, 26)):
        p.rect(x, y, x + 2, y, "yellow")
    p.eye(19, 36, 3); p.eye(29, 36, 3)
    p.smile(24, 42, 2)
    return p.done()


def rocket():
    p = Pic()
    p.poly([(14, 34), (6, 44), (14, 44)], "red"); p.poly([(34, 34), (42, 44), (34, 44)], "red")   # fins
    p.poly([(24, 2), (33, 12), (15, 12)], "red")                 # nose
    p.ball(24, 27, 10, 17, "white", "dwhite")
    p.rect(14, 12, 34, 40, "white"); p.rect(32, 12, 34, 40, "dwhite")
    p.ell(24, 22, 6, 6, "dblue"); p.ell(24, 22, 4, 4, "lblue")   # a round window
    p.px(22, 20, "white")
    p.poly([(18, 41), (30, 41), (24, 45)], "orange")             # flame
    p.poly([(21, 41), (27, 41), (24, 44)], "yellow")
    return p.done()


def strawberry():
    p = Pic()
    p.poly([(4, 14), (44, 14), (24, 44)], "red")
    p.ball(24, 20, 20, 12, "red", "dred")
    for x, y in ((12, 20), (20, 26), (30, 25), (36, 18), (24, 34), (16, 30), (31, 33)):   # seeds
        p.rect(x, y, x + 1, y + 1, "yellow")
    p.poly([(12, 9), (24, 4), (36, 9), (30, 13), (24, 10), (18, 13)], "green")   # leaves
    p.rect(23, 2, 25, 7, "dgreen")
    p.eye(18, 22, 3); p.eye(30, 22, 3)
    p.smile(24, 29, 3)
    return p.done()


def star():
    import math
    p = Pic()
    pts = []
    for i in range(10):
        r = 23 if i % 2 == 0 else 10
        a = math.radians(-90 + i * 36)
        pts.append((24 + r * math.cos(a), 25 + r * math.sin(a)))
    p.poly([(x + 1, y + 1) for x, y in pts], "dyellow")
    p.poly(pts, "yellow")
    p.eye(19, 24, 3); p.eye(29, 24, 3)
    p.smile(24, 31, 3)
    p.cheek(15, 30); p.cheek(33, 30)
    return p.done()


# friends suggested by r/MVaveFM1's u/veecheech (CREDITS.md): a T-Rex, a skeleton, RANCHER and RODEO, a vacuum
def trex():                                                      # a T-Rex, side on (original design)
    p = Pic()
    p.poly([(34, 26), (45, 37), (44, 41), (32, 38)], "dorange")  # tail
    p.rect(19, 34, 25, 46, "dorange"); p.rect(30, 34, 36, 46, "dorange")   # legs
    p.ell(21, 46, 5, 2, "dorange"); p.ell(34, 46, 5, 2, "dorange")         # feet
    p.ball(28, 30, 13, 11, "orange", "dorange")                  # body
    p.ell(25, 34, 7, 6, "cream")                                 # tummy
    for x in (24, 30, 36):                                       # stripes on the back
        p.poly([(x - 2, 20), (x + 2, 20), (x, 25)], "dorange")
    p.ball(16, 15, 14, 11, "orange", "dorange")                  # big head
    p.pie(10, 20, 8, 0, 180, "dred")                             # a wide-open roar
    p.rect(2, 20, 17, 20, "dred")
    for x in (4, 8, 12, 16):                                     # teeth, top and bottom
        p.poly([(x - 1, 20), (x + 1, 20), (x, 23)], "white")
    for x in (6, 10, 14):
        p.poly([(x - 1, 27), (x + 1, 27), (x, 24)], "white")
    p.ell(10, 25, 3, 1, "hpink")                                  # tongue
    p.eye(19, 11, 4)
    p.rect(14, 5, 24, 6, "dorange")                              # a cross brow (it is pretend-scary)
    p.ell(6, 10, 1, 1, "dorange")                                # nostril
    p.ell(15, 30, 3, 2, "dorange"); p.px(12, 31, "white")         # a tiny arm, with a claw
    return p.done()


def skeleton():                                                  # a dapper skeleton (original design)
    p = Pic()
    p.rect(13, 31, 35, 45, "black")                              # a black suit with pinstripes
    for x in (17, 22, 27, 32):
        p.line([(x, 33), (x, 45)], "dgrey", 1)
    p.line([(13, 33), (5, 42)], "black", 4); p.line([(35, 33), (43, 42)], "black", 4)   # arms
    p.ell(5, 43, 2, 2, "white"); p.ell(43, 43, 2, 2, "white")    # bony hands
    p.poly([(24, 33), (14, 29), (17, 33), (14, 37)], "purple")   # a bat bow tie
    p.poly([(24, 33), (34, 29), (31, 33), (34, 37)], "purple")
    p.ell(24, 33, 2, 2, "dpurple")
    p.ball(24, 15, 15, 14, "white", "dwhite")                    # the skull
    p.ell(17, 13, 5, 6, "black"); p.ell(31, 13, 5, 6, "black")   # big round eye holes
    p.ell(16, 11, 1, 2, "white"); p.ell(30, 11, 1, 2, "white")   # .. with a twinkle
    p.poly([(24, 18), (22, 21), (26, 21)], "black")              # nose
    p.line([(13, 24), (17, 26), (31, 26), (35, 24)], "black", 1) # a stitched grin
    for x in (16, 20, 24, 28, 32):
        p.line([(x, 24), (x, 28)], "black", 1)
    return p.done()


def cowkid(hat, hatd, hair, scarf, shirt, spots=False, braid=False):
    def f():                                                     # RANCHER or RODEO (original designs)
        p = Pic()
        p.rect(8, 38, 40, 47, shirt)                             # shoulders
        if spots:
            for x, y in ((12, 42), (20, 45), (33, 41), (38, 45)):
                p.ell(x, y, 2, 2, "black")
        else:
            for x in (12, 18, 30, 36):                           # a check shirt
                p.line([(x, 38), (x, 47)], "dorange", 1)
            p.line([(8, 43), (40, 43)], "dorange", 1)
        p.poly([(15, 35), (33, 35), (24, 45)], scarf)            # a neckerchief
        if braid:
            for y in range(24, 44, 4):                           # a long braid over the shoulder
                p.ell(39, y, 3, 3, hair)
            p.ell(39, 45, 2, 2, "yellow")
        p.ball(24, 25, 13, 12, "tan", "dtan")                    # face
        p.rect(11, 15, 37, 19, hair)                             # hair under the hat
        p.eye(19, 24, 3); p.eye(29, 24, 3)
        p.smile(24, 31, 4)
        p.cheek(14, 29); p.cheek(34, 29)
        if braid:
            for x, y in ((16, 28), (18, 29), (30, 29), (32, 28)):   # freckles
                p.px(x, y, "dtan")
        p.ell(24, 14, 22, 3, hat)                                # the brim, wide
        p.ell(24, 15, 22, 2, hatd)
        p.poly([(13, 13), (15, 2), (24, 5), (33, 2), (35, 13)], hat)   # the crown, dented on top
        p.rect(14, 10, 34, 12, hatd)                             # the band
        return p.done()
    return f


def vacuum():                                                    # an upright vacuum cleaner (original design)
    p = Pic()
    p.rect(22, 3, 26, 12, "dgrey"); p.rect(17, 2, 31, 4, "dgrey")   # the handle
    p.ball(24, 22, 13, 13, "purple", "dpurple")                  # the bag
    p.ell(24, 24, 9, 8, "lpurple")                               # .. its face
    p.eye(20, 22, 3); p.eye(28, 22, 3)
    p.smile(24, 28, 3)
    p.cheek(17, 27); p.cheek(31, 27)
    p.rect(8, 36, 40, 42, "silver"); p.rect(8, 41, 40, 42, "dgrey")  # the floor head
    p.rect(10, 35, 38, 36, "red")                                # a red stripe
    p.ell(12, 44, 2, 2, "black"); p.ell(36, 44, 2, 2, "black")   # wheels
    for x, y, r in ((4, 42, 2), (2, 38, 1), (44, 43, 1)):        # dust puffs it is about to eat
        p.ell(x, y, r, r, "grey")
    return p.done()


def spacehero():                                                 # a space hero in a bubble helmet (original design)
    p = Pic()
    p.rect(5, 36, 43, 46, "white")                               # the suit's shoulders
    p.rect(5, 44, 43, 46, "dwhite")
    p.rect(16, 37, 32, 46, "green")                              # the chest panel, its buttons
    p.rect(16, 37, 32, 38, "dgreen")
    for x, c in ((20, "red"), (24, "blue"), (28, "yellow")):
        p.ell(x, 42, 1, 1, c)
    p.rect(5, 36, 9, 46, "purple"); p.rect(39, 36, 43, 46, "purple")   # purple stripes down the arms
    p.ell(24, 21, 21, 20, "lblue")                               # the glass dome
    p.ell(24, 21, 19, 18, "glass")
    p.ball(24, 21, 14, 14, "lpurple", "purple")                  # the hood round the face
    p.ell(24, 23, 10, 11, "tan")                                 # the face
    p.eye(19, 21, 3); p.eye(29, 21, 3)
    p.rect(15, 15, 22, 16, "dbrown"); p.rect(26, 15, 33, 16, "dbrown")  # brave brows
    p.smile(24, 28, 3)
    p.line([(9, 14), (12, 9), (16, 6)], "white", 2)              # the glass's shine
    return p.done()


# drum kits (Felucca's model kits: kid.c KID_SOUND's kit)
def beatbot():                                                   # a drum machine with a face (original design)
    p = Pic()
    p.rect(4, 10, 44, 44, "dgrey"); p.rect(4, 10, 44, 12, "grey")   # the box
    p.rect(9, 14, 39, 24, "lgreen")                              # its screen, a face on it
    p.dot_eye(18, 18); p.dot_eye(30, 18)
    p.smile(24, 21, 3, "dgreen")
    for i, c in enumerate(("red", "orange", "yellow", "green", "blue", "purple", "hpink", "teal")):
        x, y = 9 + (i % 4) * 8, 28 + (i // 4) * 8                 # eight pads in their colors
        p.rect(x, y, x + 5, y + 5, c)
    p.rect(22, 3, 25, 9, "grey"); p.ell(24, 3, 3, 2, "red")      # an antenna
    return p.done()


def toydrum():                                                   # a toy marching drum, sticks crossed (original design)
    p = Pic()
    p.line([(7, 4), (22, 18)], "tan", 3); p.line([(41, 4), (26, 18)], "tan", 3)   # drumsticks
    p.ell(7, 4, 3, 3, "white"); p.ell(41, 4, 3, 3, "white")
    p.rect(6, 20, 42, 42, "red")                                 # the shell
    for i in range(4):                                           # its cords, zigzag
        x = 6 + i * 9
        p.line([(x, 23), (x + 4, 39)], "yellow", 1); p.line([(x + 9, 23), (x + 4, 39)], "yellow", 1)
    p.ell(24, 20, 18, 5, "white"); p.ell(24, 20, 16, 3, "cream")    # the head on top
    p.rect(6, 40, 42, 43, "blue"); p.rect(6, 21, 42, 23, "blue")    # the rims
    p.eye(17, 30, 3); p.eye(31, 30, 3)
    p.smile(24, 36, 3)
    return p.done()


def bongo():                                                     # two bongos side by side (original design)
    p = Pic()
    for cx, w, h in ((14, 11, 26), (35, 9, 22)):
        top = 46 - h
        p.poly([(cx - w, top), (cx + w, top), (cx + w - 3, 45), (cx - w + 3, 45)], "brown")
        p.rect(cx - w, top + 6, cx + w, top + 8, "dbrown")       # a band round it
        p.ell(cx, top, w, 3, "cream")                            # its head
    p.rect(24, 30, 26, 34, "dbrown")                             # joined in the middle
    p.eye(10, 33, 3); p.eye(18, 33, 3)                           # the big one's face
    p.smile(14, 40, 3)
    p.cheek(8, 38); p.cheek(20, 38)
    return p.done()


def monkey():                                                    # a cymbal monkey toy (original design)
    p = Pic()
    p.line([(16, 39), (8, 36)], "brown", 3); p.line([(32, 39), (40, 36)], "brown", 3)   # arms out
    p.ell(6, 36, 4, 9, "gold"); p.ell(6, 36, 1, 3, "dorange")    # a cymbal in each hand
    p.ell(42, 36, 4, 9, "gold"); p.ell(42, 36, 1, 3, "dorange")
    p.ell(11, 20, 5, 5, "brown"); p.ell(37, 20, 5, 5, "brown")   # ears
    p.ell(11, 20, 3, 3, "tan"); p.ell(37, 20, 3, 3, "tan")
    p.rect(14, 36, 34, 46, "red")                                # a little red jacket
    p.ball(24, 22, 12, 12, "brown", "dbrown")                    # the head
    p.ell(24, 26, 8, 7, "tan")                                   # the face
    p.eye(20, 20, 3); p.eye(28, 20, 3)
    p.ell(24, 29, 4, 2, "black"); p.ell(24, 29, 2, 1, "hpink")   # a big "ooh"
    p.rect(17, 8, 31, 11, "red"); p.rect(22, 5, 26, 8, "red")    # a fez
    return p.done()


# ALGORITHM's modes, as pictures for children who do not read yet (kid.c KID_ICON_*, in the order of KM_*)
def icon_one():                                                  # one friend: a smiling face
    p = Pic()
    p.ball(24, 24, 18, 18, "yellow", "dyellow")
    p.eye(17, 20, 4); p.eye(31, 20, 4)
    p.smile(24, 31, 6)
    p.cheek(12, 29); p.cheek(36, 29)
    return p.done()


def icon_choir():                                                # three friends singing, notes over them
    p = Pic()
    for x, y, c, d in ((12, 30, "pink", "dpink"), (36, 30, "lblue", "mblue"), (24, 34, "yellow", "dyellow")):
        p.ball(x, y, 9, 9, c, d)
        p.dot_eye(x - 4, y - 2); p.dot_eye(x + 4, y - 2)
        p.ell(x, y + 5, 3, 3, "black")                           # singing: an open mouth
    for x, y in ((14, 8), (32, 6)):                              # notes
        p.ell(x, y + 8, 3, 2, "purple"); p.rect(x + 2, y, x + 3, y + 8, "purple"); p.rect(x + 2, y, x + 6, y + 1, "purple")
    return p.done()


def icon_strum():                                                # a harp with its strings
    p = Pic()
    p.poly([(8, 44), (12, 4), (18, 4), (14, 44)], "gold")       # the pillar
    p.poly([(12, 4), (40, 26), (42, 32), (14, 10)], "gold")      # the neck, curving down
    p.rect(10, 42, 42, 46, "dorange")                            # the base
    p.poly([(36, 28), (44, 30), (44, 44), (38, 44)], "dorange")  # the sound box
    for i in range(6):                                           # strings, each its color
        x = 16 + i * 4
        p.line([(x, 8 + i * 3), (x, 41)], ["red", "orange", "yellow", "green", "blue", "purple"][i], 1)
    p.ell(30, 12, 2, 2, "white"); p.ell(36, 8, 1, 1, "white")    # sparkles
    return p.done()


def icon_accordion():                                            # an accordion: two boxes, the bellows between
    p = Pic()
    p.rect(2, 12, 12, 40, "red"); p.rect(2, 12, 12, 14, "dred")   # the left box, its buttons
    for y in (18, 24, 30):
        p.ell(7, y, 2, 2, "white")
    for i in range(6):                                           # the bellows: folds, light and dark
        x = 13 + i * 4
        p.poly([(x, 10), (x + 2, 14), (x + 2, 38), (x, 42)], "lpurple" if i % 2 else "purple")
        p.poly([(x + 2, 14), (x + 4, 10), (x + 4, 42), (x + 2, 38)], "purple" if i % 2 else "dpurple")
    p.rect(37, 12, 46, 40, "red"); p.rect(37, 12, 46, 14, "dred")   # the right box: piano keys
    for y in range(16, 40, 4):
        p.rect(39, y, 46, y + 2, "white")
    p.rect(2, 40, 46, 42, "dred")
    return p.done()


def icon_guess():                                                # a speech bubble: a note and a question
    p = Pic()
    p.ell(24, 20, 21, 17, "white")
    p.poly([(12, 32), (20, 34), (8, 44)], "white")               # its tail
    p.ell(14, 26, 4, 3, "blue"); p.rect(17, 10, 18, 26, "blue"); p.rect(17, 10, 23, 12, "blue")   # a note
    p.ell(33, 14, 6, 6, "orange"); p.ell(33, 14, 3, 3, "white")  # a "?"
    p.rect(27, 12, 30, 16, "white")
    p.rect(32, 19, 35, 25, "orange")
    p.ell(33, 30, 2, 2, "orange")
    return p.done()


def icon_follow():                                               # piano keys, one lit, an arrow down to it
    p = Pic()
    p.rect(2, 22, 46, 46, "white")
    for x in range(8, 46, 8):                                    # the white keys' edges
        p.line([(x, 22), (x, 46)], "dgrey", 1)
    p.rect(17, 22, 22, 46, "yellow")                             # the lit key
    for x in (6, 14, 30, 38):                                    # black keys
        p.rect(x, 22, x + 4, 36, "black")
    p.poly([(19, 18), (12, 10), (16, 10), (16, 2), (22, 2), (22, 10), (26, 10)], "green")   # an arrow
    return p.done()


def icon_chords():                                               # piano keys, a chord of three lit in their colors
    p = Pic()
    p.rect(2, 22, 46, 46, "white")
    for x in range(8, 46, 8):                                    # the white keys' edges
        p.line([(x, 22), (x, 46)], "dgrey", 1)
    for x, c in ((1, "red"), (17, "yellow"), (33, "teal")):      # C, E and G, lit
        p.rect(x + 2, 37, x + 6, 46, c)
    for x in (6, 14, 30, 38):                                    # black keys
        p.rect(x, 22, x + 4, 36, "black")
    for x, y, c in ((12, 9, "red"), (24, 5, "yellow"), (36, 9, "teal")):   # three notes above, a chord
        p.ell(x, y + 6, 4, 3, c)
    return p.done()


def icon_copy():                                                 # two bubbles with the same notes, one answering the other
    p = Pic()
    def note(x, y, c):
        p.ell(x, y, 3, 2, c); p.rect(x + 2, y - 8, x + 3, y, c)
        p.rect(x + 2, y - 8, x + 6, y - 7, c)
    p.ball(15, 14, 13, 11, "lpurple", "purple")                  # the friend's bubble, up and left
    note(8, 17, "red"); note(17, 16, "dblue")
    p.ball(33, 34, 13, 11, "lgreen", "green")                    # the answer, down and right
    note(26, 37, "red"); note(35, 36, "dblue")
    return p.done()


# the Prophet-style friends (sounds after the Sequential Prophet-5's classic patches, made on Felucca's engines)
def elephant():                                                  # brass: an elephant's trumpet
    p = Pic()
    p.ell(9, 22, 7, 11, "grey"); p.ell(39, 22, 7, 11, "grey")    # big ears
    p.ell(9, 22, 4, 8, "lpink"); p.ell(39, 22, 4, 8, "lpink")
    p.ball(24, 22, 14, 14, "grey", "dgrey")                      # head
    p.rect(21, 28, 27, 40, "grey")                               # the trunk, curling up at the end
    p.ell(26, 41, 5, 3, "grey"); p.ell(31, 38, 3, 3, "grey")
    for y in (31, 34, 37):                                       # its wrinkles
        p.line([(22, y), (26, y)], "dgrey", 1)
    p.px(31, 37, "dgrey")
    p.poly([(15, 32), (19, 30), (17, 38)], "cream"); p.poly([(33, 32), (29, 30), (31, 38)], "cream")   # tusks
    p.eye(18, 20, 3); p.eye(30, 20, 3)
    p.cheek(13, 27); p.cheek(35, 27)
    for x in (14, 24, 34):                                       # a tuft of hair
        p.line([(x, 8), (24, 11)], "dgrey", 1)
    return p.done()


def racecar():                                                   # the sync lead's zoom: a race car and its driver, side on
    p = Pic()                                                    # (no face on the car: that is someone else's film)
    p.poly([(2, 30), (8, 22), (20, 20), (26, 12), (36, 12), (40, 20), (46, 22), (46, 34), (2, 34)], "teal")
    p.poly([(28, 14), (35, 14), (38, 20), (25, 20)], "glass")    # the window
    p.ell(31, 17, 4, 4, "yellow")                                # the driver: a helmet with a visor
    p.rect(30, 16, 34, 18, "navy"); p.px(33, 16, "white")
    p.rect(2, 27, 46, 29, "white")                               # a racing stripe
    p.ell(15, 25, 4, 3, "white"); p.ell(15, 25, 2, 1, "teal")    # a number ring
    p.rect(42, 14, 46, 16, "navy"); p.rect(43, 16, 44, 22, "navy")   # the spoiler
    p.rect(2, 24, 4, 26, "yellow")                               # a headlight
    p.ball(12, 36, 7, 7, "black", "dgrey"); p.ball(36, 36, 7, 7, "black", "dgrey")   # wheels
    p.ell(12, 36, 3, 3, "silver"); p.ell(36, 36, 3, 3, "silver")
    return p.done()


def jellyfish():                                                 # strings: a slow, floating jellyfish
    import math
    p = Pic()
    p.ball(24, 22, 19, 16, "lpurple", "purple")                  # the bell
    p.rect(3, 29, 45, 40, "")                                    # (its flat underside)
    for x0, c in ((12, "purple"), (36, "purple"), (17, "lpurple"), (31, "lpurple")):   # wavy tentacles
        p.line([(x0 + 1.6 * math.sin((y - 30) / 2.6 + x0), y) for y in range(30, 46)], c, 2)
    for x0 in (21, 27):                                          # two frilly arms in the middle, swaying together
        p.line([(x0 + 1.2 * math.sin((y - 30) / 1.5), y) for y in range(30, 44)], "pink", 3)
    for x in range(8, 41, 8):                                    # a scalloped hem
        p.ell(x, 29, 4, 3, "lpurple")
    for x, y, r in ((14, 13, 2), (31, 10, 2), (37, 17, 1), (22, 9, 1)):   # spots
        p.ell(x, y, r, r, "lpink")
    p.eye(18, 21, 3); p.eye(30, 21, 3)
    p.smile(24, 26, 2)
    p.cheek(12, 25); p.cheek(36, 25)
    return p.done()


def bear():                                                      # bass: a big, round bear
    p = Pic()
    p.ball(10, 10, 6, 6, "brown", "dbrown"); p.ball(38, 10, 6, 6, "brown", "dbrown")   # ears
    p.ell(10, 10, 3, 3, "tan"); p.ell(38, 10, 3, 3, "tan")
    p.ball(24, 26, 19, 18, "brown", "dbrown")                    # head
    p.ell(24, 33, 9, 7, "tan")                                   # muzzle
    p.ell(24, 29, 4, 3, "black")                                 # nose
    p.px(23, 28, "white")
    p.line([(24, 32), (24, 35)], "black", 1)
    p.smile(24, 36, 3)
    p.eye(15, 22, 3); p.eye(33, 22, 3)
    p.cheek(11, 30); p.cheek(37, 30)
    return p.done()


def snowman():                                                   # glassy bells: a snowman
    p = Pic()
    p.ball(24, 38, 13, 9, "white", "dwhite")                     # body
    p.ball(24, 21, 9, 8, "white", "dwhite")                      # head
    p.rect(15, 11, 33, 13, "black"); p.rect(18, 4, 30, 12, "black")   # a top hat
    p.rect(18, 9, 30, 10, "red")
    p.rect(15, 28, 33, 31, "red"); p.rect(28, 29, 32, 37, "red")  # a scarf
    p.rect(29, 35, 32, 37, "dred")
    p.eye(20, 19, 2); p.eye(28, 19, 2)
    p.poly([(23, 22), (25, 21), (33, 24)], "orange")              # a carrot nose
    p.smile(24, 26, 2)
    p.ell(24, 35, 1, 1, "black"); p.ell(24, 40, 1, 1, "black")    # coal buttons
    p.line([(12, 35), (3, 29)], "dbrown", 2); p.line([(36, 35), (45, 29)], "dbrown", 2)   # stick arms
    return p.done()


def crab():                                                      # clav: a snappy crab
    p = Pic()
    for x in (8, 13, 35, 40):                                    # legs
        p.line([(x + (6 if x < 24 else -6), 34), (x, 42)], "dred", 2)
    p.ball(24, 32, 16, 10, "red", "dred")                        # body
    p.line([(19, 24), (17, 14)], "dred", 2); p.line([(29, 24), (31, 14)], "dred", 2)   # eye stalks
    p.eye(17, 12, 3); p.eye(31, 12, 3)
    p.line([(12, 30), (8, 24)], "dred", 2); p.line([(36, 30), (40, 24)], "dred", 2)   # arms
    p.ball(7, 20, 5, 5, "red", "dred"); p.ball(41, 20, 5, 5, "red", "dred")   # claws, open
    p.poly([(3, 14), (7, 19), (2, 19)], ""); p.poly([(45, 14), (41, 19), (46, 19)], "")
    p.smile(24, 34, 4)
    p.cheek(15, 33); p.cheek(33, 33)
    return p.done()


def wolf():                                                      # a howl: a wolf, nose to the moon
    p = Pic()
    p.poly([(9, 2), (19, 14), (6, 18)], "grey"); p.poly([(39, 2), (29, 14), (42, 18)], "grey")   # ears
    p.poly([(11, 8), (16, 14), (9, 15)], "lpink"); p.poly([(37, 8), (32, 14), (39, 15)], "lpink")
    p.ball(24, 26, 17, 15, "grey", "dgrey")                      # head
    p.poly([(7, 30), (24, 44), (41, 30), (24, 34)], "dwhite")    # a ruff
    p.ell(24, 33, 9, 7, "cream")                                 # muzzle
    p.pie(24, 34, 5, 0, 180, "black")                            # howling: an open "ooo"
    p.ell(24, 36, 2, 1, "hpink")
    p.ell(24, 28, 3, 2, "black")                                 # nose
    p.line([(13, 20), (19, 22)], "dgrey", 1); p.line([(35, 20), (29, 22)], "dgrey", 1)
    p.eye(17, 23, 3); p.eye(31, 23, 3)
    return p.done()


def camel():                                                     # a big, loping lead: a camel, side on
    p = Pic()
    for x, c in ((17, "dtan"), (33, "dtan"), (22, "tan"), (38, "tan")):   # legs, the far ones darker, and hooves
        p.rect(x, 35, x + 3, 45, c)
        p.rect(x, 44, x + 3, 45, "dbrown")
    p.line([(43, 28), (45, 36)], "dtan", 2)                      # a tail with a tuft
    p.ell(45, 37, 1, 2, "dbrown")
    p.ball(25, 18, 6, 9, "tan", "dtan"); p.ball(38, 19, 5, 8, "tan", "dtan")   # two tall humps
    p.ball(31, 30, 13, 7, "tan", "dtan")                         # body
    p.line([(31, 23), (32, 26)], "dtan", 1)                      # (the dip between them)
    p.ell(23, 13, 2, 2, "cream"); p.ell(37, 15, 1, 2, "cream")    # a shine on each
    p.poly([(10, 17), (16, 16), (21, 30), (16, 33)], "tan")      # neck
    p.ball(11, 13, 8, 6, "tan", "dtan")                          # head
    p.ell(6, 16, 4, 4, "cream")                                  # muzzle
    p.px(3, 14, "dbrown")                                        # nostril
    p.smile(6, 18, 2)
    p.ell(16, 7, 2, 3, "dtan")                                   # ear
    p.eye(12, 11, 3)
    p.line([(10, 6), (11, 7)], "black", 1); p.line([(13, 5), (13, 7)], "black", 1)   # long lashes
    p.cheek(15, 16)
    return p.done()


# the acid friends (a 303's squelch on ANALOG's ACID; the Scientist voiced like a TD-3's classic setting)
def scientist():                                                 # a young scientist: goggles, a lab coat, a bubbling flask
    p = Pic()
    p.rect(12, 30, 36, 46, "white"); p.rect(34, 30, 36, 46, "dwhite")   # the lab coat
    p.poly([(21, 30), (24, 36), (27, 30)], "teal")               # a shirt at the collar
    p.ball(24, 18, 12, 12, "tan", "dtan")                        # face
    p.ell(24, 8, 12, 6, "dbrown"); p.ell(13, 14, 3, 6, "dbrown"); p.ell(35, 14, 3, 6, "dbrown")   # hair
    p.rect(12, 14, 36, 16, "black")                              # the goggles' strap
    for x in (18, 30):                                           # the goggles, eyes behind the glass
        p.ell(x, 16, 6, 6, "silver"); p.ell(x, 16, 4, 4, "glass")
        p.ell(x, 17, 2, 2, "black"); p.px(x - 1, 16, "white")
    p.smile(24, 24, 2)
    p.cheek(15, 22); p.cheek(33, 22)
    p.poly([(40, 26), (44, 26), (43, 31), (47, 42), (37, 42), (41, 31)], "glass")   # the flask
    p.poly([(39, 36), (45, 36), (47, 42), (37, 42)], "lime")     # its green potion
    p.ell(41, 22, 2, 2, "lgreen"); p.ell(44, 18, 1, 1, "lgreen")  # bubbles
    p.ell(38, 38, 3, 3, "tan")                                   # the hand holding it
    return p.done()


def flytrap():                                                   # a Venus flytrap, side on: its trap open, in a pot
    p = Pic()
    p.poly([(14, 37), (34, 37), (31, 46), (17, 46)], "dorange"); p.rect(13, 35, 35, 38, "orange")   # the pot
    p.line([(24, 35), (21, 30), (14, 26)], "dgreen", 3)          # a stem curving up to the trap
    p.ell(30, 31, 5, 2, "green")                                 # a leaf
    for x, y in ((22, 4), (28, 3), (34, 4), (40, 7)):            # spines along the top jaw's rim
        p.poly([(x - 1, y + 2), (x + 1, y + 2), (x + 3, y - 2)], "lime")
    for x, y in ((22, 32), (28, 33), (34, 31), (40, 28)):        # .. and the bottom one's
        p.poly([(x - 1, y - 2), (x + 1, y - 2), (x + 3, y + 2)], "lime")
    p.poly([(6, 18), (8, 10), (16, 4), (28, 3), (42, 7), (36, 11), (22, 14)], "green")      # the top jaw, tipped up
    p.poly([(6, 20), (22, 23), (40, 27), (36, 31), (24, 34), (12, 30)], "green")            # the bottom jaw
    p.poly([(10, 17), (22, 13), (38, 9), (35, 11), (22, 15)], "hpink")                      # their pink insides
    p.poly([(10, 21), (22, 24), (38, 28), (35, 26), (22, 22)], "hpink")
    for x, y in ((27, 14), (33, 12)):                            # green bristles over the gap, as a real one has
        p.poly([(x - 1, y), (x + 1, y), (x + 1, y + 4)], "lime")
    for x, y in ((27, 24), (33, 26)):
        p.poly([(x - 1, y), (x + 1, y), (x + 1, y - 4)], "lime")
    p.eye(18, 9, 3)                                              # an eye on top
    p.cheek(12, 13)
    return p.done()


def sunflower():                                                 # a sunflower, smiling
    p = Pic()
    import math
    p.line([(24, 30), (24, 44)], "dgreen", 3)                    # stem and leaves
    p.ell(17, 36, 6, 3, "green"); p.ell(31, 39, 6, 3, "green")
    for i in range(12):                                          # oval petals all round
        a = i * math.pi / 6 + (math.pi / 12 if i % 2 else 0)
        cx, cy = 24 + 10.5 * math.cos(a), 16 + 10.5 * math.sin(a)
        p.poly([(cx + 6 * math.cos(t) * math.cos(a) - 2.6 * math.sin(t) * math.sin(a),
                 cy + 6 * math.cos(t) * math.sin(a) + 2.6 * math.sin(t) * math.cos(a)) for t in [k * math.pi / 8 for k in range(16)]],
               "gold" if i % 2 else "yellow")
    p.ball(24, 16, 8, 8, "brown", "dbrown")                      # the seedy middle, its face
    for x, y in ((19, 11), (29, 11), (24, 9)):
        p.px(x, y, "dbrown")
    p.eye(21, 15, 2); p.eye(27, 15, 2)
    p.smile(24, 19, 2, "black")
    p.cheek(18, 18); p.cheek(30, 18)
    return p.done()


# designed at home: Spider Mom and Dragon Duck
def spidermom():                                                 # a masked web hero, rainbow instead of red, and long
    import math                                                  # dark brown hair (an idea from home)
    p = Pic()
    p.ball(24, 21, 21, 19, "dbrown", "black")                    # long hair behind the head, down to the shoulders
    p.rect(3, 21, 13, 45, "dbrown"); p.rect(35, 21, 45, 45, "dbrown")
    p.line([(7, 23), (6, 43)], "brown", 1); p.line([(41, 23), (42, 43)], "brown", 1)   # a shine in it
    m = Pic()                                                    # the mask, drawn on its own and kept round
    rain = ["red", "orange", "yellow", "green", "blue", "purple"]
    for i, c in enumerate(rain):
        m.rect(4, 2 if i == 0 else 8 + round(i * 6.3), 44, 7 + round((i + 1) * 6.3), c)   # (red starts under the bangs)
    for a in range(0, 360, 45):                                  # the web: lines out from the middle, and rings
        m.line([(24, 24), (24 + 22 * math.cos(math.radians(a)), 24 + 24 * math.sin(math.radians(a)))], "black", 1)
    for r in (8, 15):
        m.d.ellipse([24 - r + OFF, 24 - r * 1.15 + OFF, 24 + r + OFF, 24 + r * 1.15 + OFF], outline=C["black"] + (255,))
    m.poly([(7, 15), (21, 20), (21, 29), (9, 27)], "black")      # the big eyes
    m.poly([(41, 15), (27, 20), (27, 29), (39, 27)], "black")
    m.poly([(10, 18), (19, 22), (19, 27), (11, 25)], "white")
    m.poly([(38, 18), (29, 22), (29, 27), (37, 25)], "white")
    for y in range(W):
        for x in range(W):
            if ((x - 24 - OFF) / 17.5) ** 2 + ((y - 24 - OFF) / 20.5) ** 2 > 1:
                m.im.putpixel((x, y), (0, 0, 0, 0))
    p.im.alpha_composite(m.im)
    p.pie(24, 11, 11, 205, 335, "dbrown")                        # the hair over the top of the mask
    return p.done()


def dragonduck():                                                # a duck that is also a little dragon
    p = Pic()
    p.poly([(28, 30), (33, 12), (38, 18), (43, 10), (45, 24), (40, 30)], "purple")   # a bat wing, up
    p.line([(33, 13), (36, 28)], "dpurple", 1); p.line([(43, 11), (41, 28)], "dpurple", 1)
    p.poly([(38, 30), (45, 20), (43, 36)], "dgreen")             # tail
    for x, y in ((24, 27), (31, 27)):                             # spikes down the back
        p.poly([(x - 2, y + 2), (x + 2, y + 2), (x, y - 3)], "orange")
    p.ball(26, 37, 17, 10, "green", "dgreen")                    # body
    p.ell(26, 40, 10, 5, "lime")                                 # a pale belly
    p.poly([(13, 11), (15, 3), (18, 10)], "cream"); p.poly([(20, 10), (23, 3), (25, 11)], "cream")   # two little horns
    p.ball(19, 19, 10, 10, "green", "dgreen")                    # head
    p.ell(7, 22, 6, 3, "orange")                                 # beak
    p.rect(3, 23, 10, 24, "dorange")
    p.ell(3, 18, 2, 1, "yellow"); p.ell(5, 16, 1, 1, "red")      # a puff of fire
    p.dot_eye(17, 17)
    p.cheek(22, 23)
    return p.done()


# the stand-ins: original friends shown in place of the look-alikes when the grown-ups' LOOK-ALIKES is off (kid.c),
# with the same sound, sky and beat
def spottypup():                                                 # a white pup with a brown patch and floppy ears
    p = Pic()
    p.ell(9, 22, 6, 12, "brown"); p.ell(39, 22, 6, 12, "brown")  # floppy ears
    p.ball(24, 26, 17, 16, "white", "dwhite")                    # head
    p.ell(31, 22, 7, 6, "tan")                                   # a patch round one eye
    p.ell(24, 36, 9, 6, "cream")
    p.eye(17, 23, 4); p.eye(31, 23, 4)
    p.ell(24, 32, 3, 2, "black")
    p.smile(24, 37, 3)
    p.ell(24, 41, 2, 2, "hpink")
    p.ell(15, 33, 2, 1, "dbrown"); p.ell(36, 33, 1, 1, "dbrown")  # freckles
    return p.done()


def fox():                                                       # a fox: black-tipped ears, a white chin
    p = Pic()
    p.poly([(5, 0), (19, 13), (4, 18)], "orange"); p.poly([(43, 0), (29, 13), (44, 18)], "orange")
    p.poly([(5, 0), (9, 4), (4, 6)], "black"); p.poly([(43, 0), (39, 4), (44, 6)], "black")
    p.ball(24, 24, 18, 14, "orange", "dorange")                  # head
    p.poly([(6, 26), (24, 43), (42, 26), (24, 32)], "white")     # white cheeks to a pointed chin
    p.eye(16, 21, 3); p.eye(32, 21, 3)
    p.ell(24, 36, 3, 2, "black")
    p.smile(24, 40, 2)
    return p.done()


def fuzzy():                                                     # a one-eyed fuzzy monster with little horns
    p = Pic()
    p.poly([(12, 10), (15, 3), (19, 9)], "cream"); p.poly([(29, 9), (33, 3), (36, 10)], "cream")   # horns
    for x, y in ((6, 20), (8, 34), (40, 20), (40, 34), (14, 40), (34, 40), (24, 41)):   # fur tufts
        p.ell(x, y, 4, 4, "red")
    p.ball(24, 26, 18, 18, "red", "dred")
    p.ell(24, 19, 9, 9, "white"); p.ell(24, 21, 5, 6, "black"); p.rect(21, 17, 23, 19, "white")   # the one big eye
    p.pie(24, 31, 9, 0, 180, "black")                            # a toothy grin
    p.rect(19, 31, 21, 33, "white"); p.rect(27, 31, 29, 33, "white")
    p.cheek(11, 30); p.cheek(37, 30)
    return p.done()


def bigblue():                                                   # a tall blue monster with curly horns
    p = Pic()
    p.poly([(12, 15), (7, 3), (19, 11)], "cream")                # short horns
    p.poly([(36, 15), (41, 3), (29, 11)], "cream")
    p.ball(24, 28, 17, 18, "mblue", "blue")
    for x in (18, 24, 30):                                       # a shaggy fringe
        p.poly([(x - 4, 11), (x + 4, 11), (x, 18)], "navy")
    p.ell(24, 40, 10, 5, "lblue")                                # tummy
    p.eye(17, 22, 4); p.eye(31, 22, 4)
    p.rect(14, 15, 20, 16, "navy"); p.rect(28, 15, 34, 16, "navy")   # bushy brows
    p.pie(24, 30, 8, 0, 180, "navy")                             # a wide grin, two teeth
    p.rect(19, 30, 21, 32, "white"); p.rect(27, 30, 29, 32, "white")
    return p.done()


def spider():                                                    # a friendly spider: round, eight legs, two big eyes
    p = Pic()
    for y, dx in ((18, 0), (25, 2), (32, 2), (39, 0)):          # legs
        p.line([(14, y - 4), (6 - dx, y - 8), (2, y)], "dpurple", 2)
        p.line([(34, y - 4), (42 + dx, y - 8), (46, y)], "dpurple", 2)
    p.ball(24, 28, 14, 14, "purple", "dpurple")
    p.ell(18, 21, 4, 3, "lpurple")
    p.eye(19, 26, 4); p.eye(29, 26, 4)
    p.smile(24, 35, 3)
    p.cheek(13, 33); p.cheek(35, 33)
    p.line([(24, 14), (24, 2)], "silver", 1)                     # its thread
    return p.done()


def pumpkin():                                                   # a smiling pumpkin (the spooky beat, not scary)
    p = Pic()
    p.rect(22, 3, 26, 11, "dgreen")                              # stem and a leaf
    p.ell(31, 7, 5, 3, "green")
    for x, c in ((13, "dorange"), (35, "dorange"), (18, "orange"), (30, "orange"), (24, "orange")):
        p.ell(x, 28, 10, 15, c)
    p.line([(18, 15), (18, 41)], "dorange", 1); p.line([(30, 15), (30, 41)], "dorange", 1)
    p.poly([(14, 22), (20, 22), (17, 17)], "yellow"); p.poly([(28, 22), (34, 22), (31, 17)], "yellow")   # eyes
    p.poly([(11, 30), (37, 30), (31, 37), (17, 37)], "yellow")   # a big grin
    p.rect(21, 30, 23, 32, "orange"); p.rect(26, 35, 28, 37, "orange")
    return p.done()


def chick():                                                     # a baby chick, just hatched
    p = Pic()
    p.ball(24, 22, 14, 13, "yellow", "dyellow")
    p.ell(14, 10, 2, 4, "yellow"); p.ell(19, 8, 2, 4, "yellow")  # a tuft
    p.ell(9, 24, 4, 6, "dyellow"); p.ell(39, 24, 4, 6, "dyellow")   # little wings
    p.eye(18, 20, 3); p.eye(30, 20, 3)
    p.poly([(21, 25), (27, 25), (24, 29)], "orange")
    p.cheek(13, 27); p.cheek(35, 27)
    p.pie(24, 34, 15, 0, 180, "cream")                           # in its eggshell
    p.poly([(9, 34), (14, 30), (19, 34), (24, 30), (29, 34), (34, 30), (39, 34)], "cream")
    p.ell(16, 40, 2, 1, "tan"); p.ell(31, 42, 2, 1, "tan")
    return p.done()


def bat():                                                       # a little bat, wings out
    p = Pic()
    p.poly([(16, 20), (2, 12), (5, 22), (2, 32), (9, 28), (12, 34), (18, 30)], "purple")   # wings
    p.poly([(32, 20), (46, 12), (43, 22), (46, 32), (39, 28), (36, 34), (30, 30)], "purple")
    p.poly([(15, 14), (18, 4), (22, 13)], "dpurple"); p.poly([(26, 13), (30, 4), (33, 14)], "dpurple")   # ears
    p.ball(24, 25, 11, 12, "dpurple", "navy")
    p.ell(24, 30, 6, 5, "lpurple")
    p.eye(20, 22, 3); p.eye(28, 22, 3)
    p.poly([(21, 29), (23, 29), (22, 32)], "white"); p.poly([(25, 29), (27, 29), (26, 32)], "white")   # tiny fangs
    p.cheek(16, 28); p.cheek(32, 28)
    return p.done()


def horse():                                                     # a horse's head with a mane
    p = Pic()
    for y in range(4, 36, 6):                                    # the mane
        p.ell(34, y + 4, 5, 4, "dbrown")
    p.poly([(15, 4), (19, 12), (13, 12)], "brown"); p.poly([(27, 3), (31, 12), (24, 12)], "brown")   # ears
    p.ball(22, 18, 12, 11, "brown", "dbrown")                    # head
    p.ball(20, 34, 10, 10, "brown", "dbrown")                    # long nose
    p.ell(19, 38, 8, 6, "tan")
    p.ell(15, 38, 1, 1, "dbrown"); p.ell(23, 38, 1, 1, "dbrown")   # nostrils
    p.rect(17, 6, 22, 14, "white")                               # a blaze
    p.eye(14, 18, 3); p.eye(28, 18, 3)
    p.smile(19, 42, 2)
    return p.done()


def cactus():                                                    # a cactus in a western hat
    p = Pic()
    p.ball(24, 32, 8, 15, "green", "dgreen")                     # trunk
    p.rect(7, 22, 12, 34, "green"); p.ell(9, 22, 3, 3, "green"); p.rect(10, 31, 18, 35, "green")   # arms
    p.rect(36, 18, 41, 30, "green"); p.ell(38, 18, 3, 3, "green"); p.rect(30, 27, 38, 31, "green")
    p.rect(14, 44, 34, 46, "dtan")                               # sand
    p.rect(10, 12, 38, 14, "brown"); p.ell(24, 10, 9, 6, "brown")   # the hat
    p.rect(15, 11, 33, 12, "red")
    p.ell(31, 18, 3, 3, "pink"); p.ell(31, 18, 1, 1, "yellow")    # a flower on the brim
    p.eye(20, 24, 3); p.eye(28, 24, 3)
    p.smile(24, 31, 3)
    for x, y in ((18, 37), (30, 40), (22, 43), (11, 28), (38, 24)):   # prickles
        p.px(x, y, "lgreen")
    return p.done()


def rainbowmom():                                                # Spider Mom's stand-in: long hair and a rainbow headband
    p = Pic()
    p.ball(24, 22, 19, 19, "brown", "dbrown")                    # hair, down to the shoulders
    p.rect(5, 22, 43, 42, "brown"); p.rect(39, 22, 43, 42, "dbrown")
    p.ball(24, 26, 13, 14, "tan", "dtan")                        # face
    p.pie(24, 18, 13, 180, 360, "brown")                         # a side-swept fringe
    rain = ["red", "orange", "yellow", "green", "blue", "purple"]
    for i, c in enumerate(rain):                                 # the rainbow headband, an arch over the head
        r = 19 - i
        p.d.arc([24 - r + OFF, 18 - r + OFF, 24 + r + OFF, 18 + r + OFF], 195, 345, fill=C[c] + (255,), width=1)
    p.eye(19, 26, 3); p.eye(29, 26, 3)
    p.smile(24, 33, 3)
    p.cheek(15, 31); p.cheek(33, 31)
    return p.done()


def alien():                                                     # a little green alien with antennae
    p = Pic()
    p.line([(17, 12), (12, 4)], "dlime", 2); p.line([(31, 12), (36, 4)], "dlime", 2)
    p.ell(12, 4, 3, 3, "pink"); p.ell(36, 4, 3, 3, "pink")
    p.ball(24, 24, 16, 14, "lime", "dlime")                      # head
    p.ell(16, 23, 5, 6, "black"); p.ell(32, 23, 5, 6, "black")   # big eyes
    p.rect(14, 20, 15, 21, "white"); p.rect(30, 20, 31, 21, "white")
    p.smile(24, 31, 2)
    p.rect(13, 37, 35, 45, "silver")                             # a silver suit
    p.rect(13, 37, 35, 38, "lblue")
    p.ell(24, 41, 3, 3, "pink")
    return p.done()


# a second batch designed at home: Spider Grandma, Night Light (after a night light), Green Queen, King Axolotl,
# Fairy Monster and Morning Glory
def web_face(p, cx, cy, rx, ry, colour):                         # a web hero's mask in one colour, its web and big eyes
    import math
    m = Pic()
    sx, sy = rx / 17.5, ry / 20.5
    q = lambda pts: [(cx + (x - 24) * sx, cy + (y - 24) * sy) for x, y in pts]
    m.rect(0, 0, 47, 47, colour)
    for a in range(0, 360, 45):
        m.line([(cx, cy), (cx + (rx + 4) * math.cos(math.radians(a)), cy + (ry + 4) * math.sin(math.radians(a)))], "black", 1)
    for r in (0.45, 0.85):
        m.d.ellipse([cx - rx * r + OFF, cy - ry * r + OFF, cx + rx * r + OFF, cy + ry * r + OFF], outline=C["black"] + (255,))
    m.poly(q([(7, 15), (21, 20), (21, 29), (9, 27)]), "black"); m.poly(q([(41, 15), (27, 20), (27, 29), (39, 27)]), "black")
    m.poly(q([(10, 18), (19, 22), (19, 27), (11, 25)]), "white"); m.poly(q([(38, 18), (29, 22), (29, 27), (37, 25)]), "white")
    for y in range(W):
        for x in range(W):
            if ((x - cx - OFF) / rx) ** 2 + ((y - cy - OFF) / ry) ** 2 > 1:
                m.im.putpixel((x, y), (0, 0, 0, 0))
    p.im.alpha_composite(m.im)


def spidergrandma():                                             # a web hero with silver curls: a green mask, a bun, pearls
    p = Pic()
    for x, y in ((9, 16), (7, 23), (8, 30), (39, 16), (41, 23), (40, 30), (14, 11), (34, 11)):   # curls round the mask
        p.ball(x, y, 5, 5, "silver", "grey")
    p.ball(24, 6, 7, 5, "silver", "grey")                       # the bun on top
    web_face(p, 24, 25, 15, 17, "green")
    p.pie(24, 14, 9, 200, 340, "silver")                         # the curls over the top of the mask
    for i, x in enumerate(range(13, 36, 3)):                      # pearls
        p.ell(x, 43 + (1 if 16 < x < 32 else 0), 1, 1, "white")
    return p.done()


def axo_sit(body, shade, gill, gill_dark, frills=False):         # a round sitting axolotl, as the night light
    def gills(p):
        if frills:                                               # feathery gills (KING AXOLOTL)
            for (ax, ay), (tx, ty) in (((14, 10), (8, 4)), ((11, 14), (5, 10)), ((11, 19), (5, 19))):
                for sgn in (1, -1):
                    a, t = (ax if sgn > 0 else 48 - ax, ay), (tx if sgn > 0 else 48 - tx, ty)
                    p.line([a, t], gill, 3)
                    p.ell(t[0], t[1], 2, 2, gill_dark)
            return
        for tri in (((16, 9), (20, 8), (15, 3)), ((12, 11), (15, 9), (5, 4)), ((10, 17), (11, 12), (3, 11))):
            p.poly(list(tri), gill)
            p.poly([(48 - x, y) for x, y in tri], gill)
    def f(p, under=None, over=None):
        gills(p)
        if under:
            under(p)
        p.ball(24, 35, 11, 10, body, shade)                      # body
        p.ell(16, 43, 3, 2, body); p.ell(32, 43, 3, 2, body)     # feet
        p.ball(24, 18, 14, 11, body, shade)                      # the big round head
        p.ell(18, 17, 2, 2, "black"); p.ell(30, 17, 2, 2, "black")   # eyes, shiny
        p.px(17, 16, "white"); p.px(29, 16, "white")
        p.px(22, 21, "black"); p.px(26, 21, "black")             # two little nostrils
        p.line([(15, 22), (17, 24), (20, 24), (24, 25), (28, 24), (31, 24), (33, 22)], "black", 1)   # a wide, wavy smile
        if over:
            over(p)
        return p.done()
    return f


def nightlight():                                                # the night light: white, mint gills, hugging a mint egg
    p = Pic()
    def egg(p):
        p.ball(24, 37, 6, 8, "mint", "dmint")
        p.ell(17, 35, 3, 2, "white"); p.ell(31, 38, 3, 2, "white")   # hands round it
    return axo_sit("white", "dwhite", "mint", "dmint")(p, over=egg)


def greenqueen():                                                # the night light as GREEN QUEEN: a gold crown, a rainbow cape
    p = Pic()
    def cape(p):
        for i, c in enumerate(["red", "orange", "yellow", "green", "blue", "purple"]):
            x0 = 8 + i * 5
            p.poly([(max(x0, 12 - (x0 < 24) * 0), 26), (x0 + 5, 26), (x0 + 5 + (i - 2.5) * 0.8, 46), (x0 + (i - 2.5) * 0.8, 46)], c)
    def crown(p):
        p.poly([(17, 9), (17, 3), (20, 6), (24, 1), (28, 6), (31, 3), (31, 9)], "gold")
        p.rect(17, 8, 31, 9, "dyellow")
        p.px(24, 5, "red")
        p.ell(24, 37, 5, 6, "lgreen")                            # a pale belly
        p.ell(18, 34, 2, 2, "green"); p.ell(30, 34, 2, 2, "green")   # hands
    return axo_sit("green", "dgreen", "lime", "dlime")(p, under=cape, over=crown)


def kingaxolotl():                                               # a green axolotl on a rainbow throne, in a crown and green and red robes
    p = Pic()
    def throne(p):
        for i, c in enumerate(["red", "orange", "yellow", "green", "blue", "purple"]):
            r = 22 - i * 2
            p.pie(24, 26, r, 180, 360, c)
        p.pie(24, 26, 11, 180, 360, None)
        p.rect(5, 30, 43, 33, "gold"); p.rect(7, 34, 41, 45, "dyellow")   # the seat
    def robe(p):
        p.ball(24, 37, 12, 9, "red", "dred")                      # a red robe, round over the body
        p.poly([(21, 29), (27, 29), (29, 45), (19, 45)], "green")  # green down the front
        p.ell(24, 29, 9, 2, "white")                              # a fur collar
        p.ell(14, 37, 3, 2, "green"); p.ell(34, 37, 3, 2, "green")   # the hands
        p.poly([(17, 9), (17, 3), (20, 6), (24, 1), (28, 6), (31, 3), (31, 9)], "gold")   # crown
        p.px(20, 7, "red"); p.px(28, 7, "red")
    return axo_sit("green", "dgreen", "red", "dred", frills=True)(p, under=throne, over=robe)


def fairymonster():                                              # a pink fairy monster: pigtails, little wings, a star wand
    p = Pic()
    p.ell(8, 26, 6, 9, "glass"); p.ell(40, 26, 6, 9, "glass")    # wings
    p.ell(9, 7, 5, 5, "lpurple"); p.ell(39, 7, 5, 5, "lpurple")  # pigtails, tied up high
    p.ell(13, 10, 2, 2, "yellow"); p.ell(35, 10, 2, 2, "yellow")
    for x, y in ((10, 26), (38, 26), (12, 36), (36, 36), (18, 41), (30, 41), (24, 42)):   # fluff
        p.ell(x, y, 4, 4, "pink")
    p.ball(24, 27, 15, 16, "pink", "dpink")
    p.pie(24, 18, 12, 180, 360, "lpurple")                       # the hair
    p.ell(24, 13, 5, 3, "lpurple")
    p.eye(19, 25, 4); p.eye(29, 25, 4)
    p.ell(24, 30, 2, 2, "hpink")                                 # a round nose
    p.smile(24, 34, 4)
    p.line([(35, 37), (40, 23)], "white", 1)                     # the wand, and its star
    import math
    p.poly([(40 + (4 if k % 2 == 0 else 1.8) * math.cos(math.pi / 2 + k * math.pi / 5),
             20 - (4 if k % 2 == 0 else 1.8) * math.sin(math.pi / 2 + k * math.pi / 5)) for k in range(10)], "yellow")
    return p.done()


def morningglory():                                              # a morning glory vine: heart leaves, purple trumpet flowers
    import math
    p = Pic()
    pts = [(20 + 7 * math.sin(t / 5), 45 - t) for t in range(0, 36)]   # the vine, curling up
    p.line(pts, "dgreen", 2)
    def leaf(x, y, flip):                                        # a heart-shaped leaf, its point away from the vine
        d = -1 if flip else 1
        p.ell(x, y - 2, 3, 3, "green"); p.ell(x + 4 * d, y - 2, 3, 3, "green")
        p.poly([(x - 3 * (d > 0) - 0 * d, y - 1), (x + 7 * (d > 0) - 0, y - 1), (x + 2 * d, y + 5)], "green")
        p.line([(x + 2 * d, y - 3), (x + 2 * d, y + 3)], "dgreen", 1)
    leaf(28, 39, False); leaf(11, 31, True); leaf(29, 24, False); leaf(9, 13, True)
    def flower(cx, cy, r, face=False):
        p.ell(cx, cy, r, r, "purple")
        for i in range(5):                                       # five pale stripes from the middle
            a = i * 2 * math.pi / 5 - math.pi / 2
            p.line([(cx, cy), (cx + (r - 1) * math.cos(a), cy + (r - 1) * math.sin(a))], "lpurple", 1)
        p.ell(cx, cy, r // 3, r // 3, "white")
        if face:
            p.ell(cx, cy + 1, r // 2 + 1, r // 2, "white")
            p.ell(cx - 3, cy, 1, 2, "black"); p.ell(cx + 3, cy, 1, 2, "black")
            p.smile(cx, cy + 3, 2)
    flower(34, 32, 6); flower(14, 22, 5)
    flower(30, 13, 9, True)
    return p.done()


def greengranny():                                               # Spider Grandma's stand-in: silver curls, glasses, a green cardigan
    p = Pic()
    p.rect(10, 38, 38, 45, "green"); p.poly([(20, 38), (28, 38), (24, 45)], "white")   # cardigan, a white blouse
    for x, y in ((10, 18), (9, 26), (38, 18), (39, 26), (14, 11), (34, 11), (24, 8)):   # silver curls
        p.ball(x, y, 6, 6, "silver", "grey")
    p.ball(24, 6, 6, 4, "silver", "grey")                       # a bun
    p.ball(24, 25, 13, 14, "tan", "dtan")                        # face
    p.pie(24, 18, 11, 195, 345, "silver")
    for x in (18, 30):                                           # round glasses
        p.d.ellipse([x - 5 + OFF, 20 + OFF, x + 5 + OFF, 30 + OFF], outline=C["dgreen"] + (255,), width=1)
    p.line([(23, 25), (25, 25)], "dgreen", 1)
    p.ell(18, 25, 2, 2, "black"); p.ell(30, 25, 2, 2, "black")
    p.smile(24, 33, 3)
    p.cheek(13, 31); p.cheek(35, 31)
    for x in range(15, 34, 3):                                   # pearls
        p.ell(x, 40 + (1 if 18 < x < 30 else 0), 1, 1, "white")
    return p.done()


def pixie():                                                     # Fairy Monster's stand-in: a pixie in a leaf hat
    p = Pic()
    p.ell(9, 30, 6, 9, "lpurple"); p.ell(39, 30, 6, 9, "lpurple")   # wings
    p.poly([(14, 34), (34, 34), (38, 46), (10, 46)], "green")    # a leaf dress
    p.line([(24, 34), (24, 46)], "dgreen", 1)
    p.ball(24, 24, 11, 11, "tan", "dtan")                        # face
    p.poly([(12, 22), (6, 16), (14, 19)], "tan"); p.poly([(36, 22), (42, 16), (34, 19)], "tan")   # pointed ears
    p.poly([(11, 17), (37, 17), (34, 8), (30, 3), (42, 1), (26, 6), (18, 8)], "dgreen")   # a pointed leaf hat
    p.rect(11, 15, 37, 18, "green")
    p.eye(20, 24, 3); p.eye(28, 24, 3)
    p.smile(24, 30, 3)
    p.cheek(16, 29); p.cheek(32, 29)
    return p.done()


# a third batch designed at home: Grouch, Tiger Cub, Raccoon and Goldenrod
def trash_can(p, y0=27):                                         # a ridged silver can, its rim at y0
    p.rect(10, y0 + 3, 38, 45, "silver")
    for x in range(13, 37, 5):
        p.line([(x, y0 + 4), (x, 44)], "grey", 1)
    p.rect(8, y0, 40, y0 + 3, "grey")


def grouch():                                                    # a grumpy green furry monster in a can, its lid on its head
    p = Pic()
    for x, y in ((12, 18), (36, 18), (14, 26), (34, 26), (18, 10), (30, 10)):   # fur
        p.ell(x, y, 4, 4, "green")
    p.ball(24, 19, 12, 11, "green", "dgreen")
    p.poly([(9, 8), (30, 2), (39, 6), (16, 11)], "grey")         # the lid, tipped up on its head
    p.rect(22, 2, 26, 4, "silver")
    p.line([(13, 13), (24, 17), (35, 13)], "dbrown", 3)          # one big, cross eyebrow
    p.ell(19, 19, 3, 3, "white"); p.ell(29, 19, 3, 3, "white")
    p.ell(19, 20, 1, 2, "black"); p.ell(29, 20, 1, 2, "black")
    p.line([(18, 26), (20, 24), (28, 24), (30, 26)], "black", 1)   # a frown
    trash_can(p)
    p.ell(11, 28, 3, 2, "green"); p.ell(37, 28, 3, 2, "green")   # hands on the rim
    return p.done()


def tigercub():                                                  # a tiger cub in a red zip-up sweater
    p = Pic()
    p.ball(24, 39, 13, 8, "red", "dred")                         # the sweater
    p.line([(24, 32), (24, 46)], "gold", 1)                      # its zip
    p.ell(11, 41, 3, 3, "orange"); p.ell(37, 41, 3, 3, "orange")   # paws
    p.ell(12, 8, 5, 5, "orange"); p.ell(36, 8, 5, 5, "orange")   # round ears
    p.ell(12, 8, 2, 2, "lpink"); p.ell(36, 8, 2, 2, "lpink")
    p.ball(24, 19, 15, 13, "orange", "dorange")                  # head
    for x0, y0, x1, y1 in ((21, 7, 22, 11), (26, 7, 27, 11), (9, 17, 13, 18), (35, 17, 39, 18), (9, 21, 12, 22), (36, 21, 39, 22)):
        p.rect(x0, y0, x1, y1, "black")                          # stripes
    p.ell(24, 25, 7, 5, "cream")                                 # muzzle
    p.eye(18, 18, 3); p.eye(30, 18, 3)
    p.ell(24, 23, 2, 1, "hpink")
    p.smile(24, 27, 3)
    return p.done()


def raccoon():                                                   # a raccoon with a collection, a box of treasures
    p = Pic()
    for i, c in enumerate(["grey", "black", "grey", "black", "grey"]):   # a ringed tail
        p.ell(40, 40 - i * 4, 4, 3, c)
    p.ball(24, 37, 12, 9, "grey", "dgrey")                       # body
    p.poly([(9, 12), (12, 2), (18, 8)], "grey"); p.poly([(39, 12), (36, 2), (30, 8)], "grey")   # ears
    p.ball(24, 17, 14, 11, "grey", "dgrey")                      # head
    p.poly([(9, 15), (24, 18), (39, 15), (36, 22), (24, 21), (12, 22)], "black")   # the mask
    p.ell(18, 18, 2, 2, "white"); p.ell(30, 18, 2, 2, "white")
    p.px(18, 18, "black"); p.px(30, 18, "black")
    p.ell(24, 24, 6, 4, "white")                                 # muzzle
    p.ell(24, 22, 2, 1, "black")
    p.smile(24, 25, 2)
    p.rect(13, 34, 33, 45, "tan"); p.rect(13, 34, 33, 35, "dtan")   # its box of treasures
    for x, y, c in ((16, 32, "blue"), (20, 31, "red"), (25, 32, "yellow"), (30, 31, "green"), (18, 33, "purple"), (27, 33, "pink")):
        p.ell(x, y, 2, 2, c)
    p.ell(11, 38, 3, 2, "dgrey"); p.ell(35, 38, 3, 2, "dgrey")   # paws holding it
    return p.done()


def goldenrod():                                                 # goldenrod (a prairie flower): golden plumes on tall stems
    import math
    p = Pic()
    for x0, x1, top in ((24, 24, 14), (24, 12, 22), (24, 37, 20)):   # three stems
        p.line([(x0, 46), (x1, top)], "dgreen", 2)
    for x, y, d in ((20, 36, -1), (29, 32, 1), (17, 26, -1), (30, 24, 1)):   # long, narrow leaves
        p.poly([(x, y), (x + 9 * d, y - 4), (x + 1 * d, y + 2)], "green")
    def plume(cx, cy, w, h):                                     # an arching spray of little yellow flowers
        for i in range(0, 40):
            a = i * 2.39996
            r = math.sqrt(i / 40)
            x, y = cx + w * r * math.cos(a), cy + h * r * math.sin(a)
            p.ell(x, y, 1, 1, "yellow" if i % 3 else "gold")
    plume(12, 18, 6, 6); plume(37, 16, 6, 6)
    p.ball(24, 11, 10, 9, "yellow", "gold")                      # the big plume, with a face
    for x, y in ((17, 5), (22, 3), (28, 3), (32, 7), (15, 10), (33, 12)):
        p.ell(x, y, 2, 2, "gold")
    p.eye(20, 11, 2); p.eye(28, 11, 2)
    p.smile(24, 15, 2)
    p.cheek(16, 14); p.cheek(32, 14)
    return p.done()


def alleycat():                                                  # Grouch's stand-in: a grey alley cat, smiling out of a can
    p = Pic()
    p.poly([(11, 13), (13, 2), (20, 9)], "grey"); p.poly([(37, 13), (35, 2), (28, 9)], "grey")
    p.poly([(13, 10), (14, 5), (17, 8)], "lpink"); p.poly([(35, 10), (34, 5), (31, 8)], "lpink")
    p.ball(24, 18, 13, 11, "grey", "dgrey")
    p.eye(19, 17, 3); p.eye(29, 17, 3)
    p.poly([(22, 21), (26, 21), (24, 23)], "hpink")
    p.smile(24, 24, 2)
    for y in (21, 24):
        p.line([(6, y - 1), (13, y)], "dgrey", 1); p.line([(35, y), (42, y - 1)], "dgrey", 1)
    trash_can(p)
    p.ell(11, 28, 3, 2, "grey"); p.ell(37, 28, 3, 2, "grey")
    return p.done()


def lioncub():                                                   # Tiger Cub's stand-in: a lion cub with a fluffy mane
    p = Pic()
    p.ball(24, 39, 12, 8, "gold", "dyellow")
    for i in range(10):                                          # the mane
        import math
        a = i * math.pi / 5
        p.ell(24 + 15 * math.cos(a), 20 + 13 * math.sin(a), 5, 5, "dorange")
    p.ball(24, 20, 13, 12, "gold", "dyellow")
    p.ell(24, 26, 6, 4, "cream")
    p.eye(19, 19, 3); p.eye(29, 19, 3)
    p.ell(24, 24, 2, 1, "dbrown")
    p.smile(24, 28, 2)
    return p.done()


def squirrel():                                                  # Raccoon's stand-in: a squirrel with an acorn
    p = Pic()
    p.ball(36, 24, 9, 16, "orange", "dorange")                   # a big bushy tail
    p.ball(22, 36, 10, 9, "orange", "dorange")
    p.ell(22, 38, 6, 6, "cream")
    p.poly([(14, 10), (15, 3), (19, 9)], "orange"); p.poly([(26, 9), (29, 3), (30, 10)], "orange")
    p.ball(22, 18, 11, 10, "orange", "dorange")
    p.eye(18, 17, 3); p.eye(26, 17, 3)
    p.ell(22, 22, 1, 1, "dbrown")
    p.smile(22, 24, 2)
    p.ell(22, 33, 3, 3, "brown"); p.rect(19, 30, 25, 31, "dbrown")   # the acorn
    return p.done()


# friends that play real recordings (SAMPLE: the piano, flute and sax sets Felucca carries)
def pianopal():                                                  # an upright piano with a face above its keys
    p = Pic()
    p.rect(5, 9, 43, 41, "dbrown"); p.rect(6, 10, 42, 40, "brown")   # the case
    p.rect(8, 12, 40, 26, "cream")                               # the music stand, a face
    p.eye(17, 19, 3); p.eye(31, 19, 3)
    p.smile(24, 24, 3)
    p.cheek(11, 23); p.cheek(37, 23)
    p.rect(7, 28, 41, 38, "white")                               # the keys
    for x in range(9, 40, 4):
        p.rect(x, 28, x, 38, "grey")
    for x in (10, 14, 22, 26, 30, 38):
        p.rect(x, 28, x + 1, 33, "black")
    p.rect(8, 41, 11, 45, "dbrown"); p.rect(37, 41, 40, 45, "dbrown")   # legs
    return p.done()


def flutebird():                                                 # a blue bird playing a silver flute
    p = Pic()
    p.poly([(36, 30), (45, 24), (43, 38)], "dblue")              # tail
    p.ball(24, 30, 15, 13, "blue", "dblue")                      # body
    p.ell(24, 33, 8, 7, "lblue")                                 # belly
    p.ball(20, 16, 11, 10, "blue", "dblue")                      # head
    p.poly([(8, 16), (3, 18), (8, 20)], "orange")                # beak
    p.dot_eye(15, 14)
    p.cheek(21, 20)
    p.line([(4, 28), (26, 22)], "silver", 3)                     # the flute, held across
    p.line([(4, 28), (26, 22)], "dgrey", 1)
    for x, y in ((10, 26), (14, 25), (18, 24), (22, 23)):
        p.px(x, y, "black")
    p.ell(26, 24, 3, 2, "lblue")                                 # a wing holding it
    p.line([(20, 42), (20, 46)], "orange", 1); p.line([(28, 42), (28, 46)], "orange", 1)   # legs
    return p.done()


def saxcat():                                                    # a cat with a golden saxophone
    p = Pic()
    p.poly([(11, 13), (13, 2), (20, 9)], "grey"); p.poly([(37, 13), (35, 2), (28, 9)], "grey")   # ears
    p.poly([(13, 10), (14, 5), (17, 8)], "lpink"); p.poly([(35, 10), (34, 5), (31, 8)], "lpink")
    p.ball(24, 18, 13, 11, "grey", "dgrey")                      # head
    p.eye(19, 17, 3); p.eye(29, 17, 3)
    p.poly([(22, 21), (26, 21), (24, 23)], "hpink")
    p.ball(24, 37, 11, 9, "grey", "dgrey")                       # body
    p.line([(31, 26), (35, 38), (34, 44)], "gold", 4)            # the sax: a gold tube,
    p.poly([(31, 43), (40, 43), (38, 47), (30, 47)], "dyellow")   # its bell,
    p.line([(31, 27), (27, 24)], "gold", 3)                      # and its neck to the mouth
    p.px(33, 32, "dyellow"); p.px(34, 36, "dyellow"); p.px(34, 40, "dyellow")
    return p.done()



# ---------------------------------------------------------------- friends in sets: the farm, the sea, bugs, dinosaurs,
# food and things that go. The vehicles have no faces (a driver smiles from the window), so they are no one's film or show.
def cow():
    p = Pic()
    p.ell(7, 17, 5, 3, "white"); p.ell(41, 17, 5, 3, "white")    # ears
    p.ell(7, 17, 3, 1, "pink"); p.ell(41, 17, 3, 1, "pink")
    p.poly([(14, 11), (11, 2), (19, 9)], "cream"); p.poly([(34, 11), (37, 2), (29, 9)], "cream")   # horns
    p.ball(24, 24, 17, 16, "white", "dwhite")
    p.ell(14, 14, 6, 4, "black")                                 # spots
    p.ell(34, 24, 6, 6, "black")
    p.eye(17, 24, 3); p.eye(33, 24, 3)
    p.ball(24, 35, 11, 7, "pink", "dpink")                        # muzzle
    p.ell(20, 35, 1, 2, "dpink"); p.ell(28, 35, 1, 2, "dpink")
    p.smile(24, 40, 3)
    return p.done()


def pig():
    p = Pic()
    p.poly([(6, 5), (18, 9), (9, 18)], "pink"); p.poly([(42, 5), (30, 9), (39, 18)], "pink")   # ears
    p.poly([(9, 8), (14, 10), (10, 14)], "dpink"); p.poly([(39, 8), (34, 10), (38, 14)], "dpink")
    p.ball(24, 26, 19, 17, "pink", "dpink")
    p.ball(24, 32, 9, 7, "lpink", "dpink")                        # snout
    p.ell(21, 32, 1, 3, "dpink"); p.ell(27, 32, 1, 3, "dpink")
    p.eye(15, 22, 3); p.eye(33, 22, 3)
    p.cheek(10, 30); p.cheek(38, 30)
    p.smile(24, 41, 3)
    return p.done()


def sheep():
    p = Pic()
    for x, y, r in ((11, 16, 7), (20, 9, 8), (31, 9, 8), (38, 17, 7), (9, 29, 6), (39, 29, 6), (14, 38, 6), (34, 38, 6)):
        p.ball(x, y, r, r, "white", "dwhite")                     # the wool
    p.ball(24, 26, 15, 14, "white", "dwhite")
    p.rect(15, 41, 18, 46, "dgrey"); p.rect(30, 41, 33, 46, "dgrey")   # hooves
    p.ell(11, 27, 5, 3, "dgrey"); p.ell(37, 27, 5, 3, "dgrey")    # ears
    p.ball(24, 28, 10, 12, "dgrey", "black")                      # the face
    p.eye(19, 25, 3); p.eye(29, 25, 3)
    p.ell(24, 33, 3, 2, "pink")
    p.smile(24, 37, 2, "white")
    return p.done()


def shark():
    p = Pic()
    p.poly([(36, 24), (47, 11), (44, 25), (47, 38)], "blue")      # tail
    p.poly([(18, 18), (25, 4), (31, 18)], "blue")                 # the fin on its back
    p.ball(22, 28, 20, 12, "blue", "dblue")
    p.ell(19, 34, 15, 5, "white")                                 # belly
    p.eye(10, 25, 3)
    p.rect(5, 31, 18, 31, "black")                                # a wide smile, with teeth
    for x in (7, 10, 13, 16):
        p.poly([(x - 1, 31), (x + 1, 31), (x, 34)], "white")
    for x in (19, 22, 25):                                        # gills
        p.line([(x, 25), (x, 29)], "dblue", 1)
    p.poly([(27, 34), (36, 38), (28, 40)], "dblue")               # a side fin
    p.cheek(12, 29)
    return p.done()


def seahorse():
    p = Pic()
    p.poly([(31, 14), (41, 21), (32, 30)], "yellow")              # the fin on its back
    p.line([(26, 33), (27, 38), (31, 41), (36, 39), (37, 34), (33, 32), (31, 35)], "orange", 4)   # the curled tail
    p.ball(24, 24, 9, 12, "orange", "dorange")                    # chest
    p.ell(19, 26, 4, 8, "yellow")                                 # its pale belly
    for y in (18, 23, 28):
        p.line([(25, y), (32, y)], "dorange", 1)
    p.ball(21, 11, 8, 7, "orange", "dorange")                     # head
    p.rect(6, 8, 14, 12, "orange"); p.rect(6, 12, 14, 12, "dorange")   # snout
    p.poly([(20, 5), (24, 0), (26, 6)], "dorange"); p.poly([(25, 6), (30, 2), (30, 9)], "dorange")   # crest
    p.eye(19, 10, 3)
    p.cheek(17, 15)
    return p.done()


def starfish():
    import math
    p = Pic()
    tips = [(24 + 18 * math.cos(math.radians(a)), 26 + 18 * math.sin(math.radians(a))) for a in (-90, -18, 54, 126, 198)]
    for x, y in tips:
        p.line([(24, 26), (x, y)], "orange", 10)
        p.ell(x, y, 5, 5, "orange")
    p.ball(24, 26, 11, 11, "orange", "dorange")
    for (x, y) in tips:                                           # a row of dots along each arm
        for t in (0.45, 0.7, 0.92):
            p.px(round(24 + (x - 24) * t), round(26 + (y - 26) * t), "yellow")
    p.eye(20, 24, 3); p.eye(29, 24, 3)
    p.smile(24, 31, 3)
    p.cheek(16, 30); p.cheek(33, 30)
    return p.done()


def snail():
    p = Pic()
    p.ball(24, 40, 21, 6, "lime", "dlime")                        # the foot
    p.ell(7, 30, 5, 10, "lime")                                   # neck and head
    p.line([(5, 22), (3, 12)], "dlime", 2); p.line([(11, 22), (13, 12)], "dlime", 2)   # eyestalks
    p.eye(3, 11, 3); p.eye(13, 11, 3)
    p.ball(29, 24, 15, 15, "orange", "dorange")                   # the shell, a swirl
    p.ell(28, 23, 10, 10, "tan")
    p.ell(28, 23, 6, 6, "orange")
    p.ell(28, 23, 2, 2, "dorange")
    p.smile(8, 35, 2)
    p.cheek(11, 32)
    return p.done()


def caterpillar():
    p = Pic()
    for i, (x, y) in enumerate(((38, 37), (31, 33), (25, 37), (19, 33))):
        p.rect(x - 1, y + 4, x + 1, y + 8, "dgreen")             # little feet
        p.ball(x, y, 6, 6, "lime" if i % 2 else "green", "dlime" if i % 2 else "dgreen")
    p.rect(11, 38, 13, 43, "dgreen")
    p.ball(11, 31, 10, 10, "green", "dgreen")                     # the head
    p.line([(7, 21), (4, 11)], "dgreen", 1); p.line([(16, 21), (19, 11)], "dgreen", 1)   # antennae
    p.ell(4, 10, 2, 2, "red"); p.ell(19, 10, 2, 2, "red")
    p.eye(7, 29, 3); p.eye(16, 29, 3)
    p.smile(11, 36, 3)
    p.cheek(3, 35); p.cheek(19, 35)
    return p.done()


def firefly():
    p = Pic()
    p.ball(32, 33, 9, 8, "yellow", "gold")                        # the glowing end
    p.ell(30, 32, 4, 3, "white")
    p.ell(30, 28, 12, 5, "glass")                                 # a wing
    p.ball(22, 26, 8, 7, "dgrey", "black")
    p.ball(12, 21, 8, 8, "dgrey", "black")                        # the head
    p.line([(10, 14), (5, 6)], "black", 1); p.line([(15, 14), (18, 6)], "black", 1)
    p.ell(5, 5, 1, 1, "yellow"); p.ell(18, 5, 1, 1, "yellow")
    p.eye(9, 20, 3)
    p.smile(12, 26, 2, "white")
    for x in (18, 23, 28):                                        # legs
        p.line([(x, 31), (x - 2, 38)], "black", 1)
    for x, y in ((42, 24), (44, 38), (30, 43), (41, 46)):         # it glows: sparkles
        p.px(x, y, "white"); p.px(x - 1, y, "yellow"); p.px(x + 1, y, "yellow"); p.px(x, y - 1, "yellow"); p.px(x, y + 1, "yellow")
    return p.done()


def triceratops():
    p = Pic()
    p.poly([(34, 28), (47, 38), (41, 40), (32, 36)], "dgreen")    # tail
    p.rect(19, 36, 24, 46, "dgreen"); p.rect(31, 36, 36, 46, "dgreen")   # legs
    p.ball(29, 31, 14, 10, "green", "dgreen")                     # body
    p.ell(27, 35, 8, 5, "lgreen")
    p.ball(16, 18, 12, 12, "orange", "dorange")                   # the frill
    for x, y in ((10, 8), (16, 6), (22, 8), (26, 14)):
        p.ell(x, y, 2, 2, "yellow")
    p.ball(12, 29, 10, 8, "green", "dgreen")                      # head
    p.poly([(7, 21), (10, 10), (13, 21)], "cream")                # brow horns
    p.poly([(14, 21), (18, 12), (18, 22)], "cream")
    p.poly([(2, 30), (5, 24), (7, 31)], "cream")                  # nose horn
    p.eye(11, 26, 3)
    p.smile(9, 34, 2)
    p.cheek(15, 33)
    return p.done()


def stegosaurus():
    p = Pic()
    for x, h in ((13, 9), (19, 12), (26, 13), (33, 11), (38, 8)):   # the plates on its back
        p.poly([(x - 4, 24), (x, 24 - h), (x + 4, 24)], "orange")
        p.px(x, 24 - h + 3, "yellow")
    p.poly([(38, 30), (46, 36), (39, 40)], "green")               # tail
    for y, x in ((28, 45), (34, 45)):
        p.poly([(x - 3, y + 1), (x, y - 3), (x, y + 4)], "cream")
    p.rect(14, 38, 19, 46, "dgreen"); p.rect(31, 38, 36, 46, "dgreen")
    p.ball(26, 31, 17, 10, "green", "dgreen")
    p.ell(25, 36, 10, 4, "lgreen")
    p.ball(8, 35, 7, 6, "green", "dgreen")                        # small head
    p.eye(7, 33, 3)
    p.smile(6, 38, 2)
    p.cheek(11, 37)
    return p.done()


def pizza():
    p = Pic()
    p.poly([(5, 10), (43, 10), (24, 46)], "yellow")               # the cheese
    p.rect(4, 4, 44, 11, "dtan"); p.rect(4, 4, 44, 9, "tan")      # the crust
    p.ell(4, 7, 2, 3, "tan"); p.ell(44, 7, 2, 3, "tan")
    for x, y in ((13, 17), (33, 17), (24, 28)):                   # pepperoni
        p.ball(x, y, 4, 4, "red", "dred")
    for x, y in ((22, 15), (14, 24), (33, 25), (24, 37)):         # little green peppers
        p.rect(x, y, x + 2, y + 1, "green")
    p.eye(18, 23, 3); p.eye(30, 23, 3)
    p.smile(24, 31, 3)
    return p.done()


def donut():
    p = Pic()
    p.ball(24, 27, 22, 17, "tan", "dtan")
    p.ball(24, 25, 20, 15, "hpink", "dpink")                      # the icing
    p.ell(24, 20, 6, 4, "")                                       # the hole
    for x, y, c in ((12, 22, "yellow"), (17, 15, "white"), (31, 15, "lblue"), (38, 22, "yellow"), (14, 30, "lime"),
                    (35, 31, "white"), (24, 11, "lblue"), (40, 28, "lime")):
        p.rect(x, y, x + 2, y, c)
    p.eye(17, 29, 3); p.eye(31, 29, 3)
    p.smile(24, 35, 3)
    p.cheek(11, 33); p.cheek(37, 33)
    return p.done()


def banana():
    p = Pic()
    p.rect(17, 2, 21, 6, "dbrown")                                # the stem
    p.poly([(15, 6), (26, 6), (33, 15), (38, 28), (34, 41), (22, 45), (11, 43), (20, 37), (22, 25), (16, 14)], "yellow")
    p.poly([(26, 6), (33, 15), (38, 28), (34, 41), (22, 45), (26, 40), (30, 28), (28, 15)], "dyellow")
    p.dot_eye(19, 22); p.dot_eye(28, 22)
    p.smile(24, 29, 2)
    p.cheek(17, 28); p.cheek(30, 28)
    return p.done()


def train():
    p = Pic()
    p.ell(10, 6, 4, 3, "white"); p.ell(16, 4, 3, 2, "white")      # puffs of steam
    p.rect(8, 11, 13, 21, "black"); p.rect(6, 9, 15, 12, "dgrey")   # the smokestack
    p.rect(4, 36, 45, 39, "black")
    p.rect(4, 21, 28, 36, "blue"); p.rect(4, 21, 28, 22, "mblue")   # the boiler
    for x in (11, 20):
        p.rect(x, 21, x + 1, 36, "yellow")
    p.ell(4, 28, 2, 3, "yellow")                                  # a lamp
    p.rect(28, 12, 44, 36, "red"); p.rect(26, 9, 46, 13, "dred")  # the cab
    p.rect(32, 17, 41, 28, "glass")
    p.ell(36, 25, 3, 3, "tan"); p.rect(32, 21, 40, 22, "navy")    # the driver, in a cap
    p.rect(34, 27, 38, 27, "black")
    for x in (10, 24, 38):                                        # wheels
        p.ball(x, 40, 5, 5, "black", "dgrey")
        p.ell(x, 40, 2, 2, "silver")
    return p.done()


def firetruck():
    p = Pic()
    p.rect(3, 16, 31, 18, "silver")                               # the ladder
    for x in range(5, 31, 4):
        p.rect(x, 16, x, 21, "dgrey")
    p.rect(2, 22, 32, 37, "red"); p.rect(2, 29, 32, 30, "white")
    p.rect(33, 15, 46, 37, "red"); p.rect(33, 15, 46, 16, "dred")
    p.rect(36, 18, 45, 27, "glass")
    p.ell(41, 25, 3, 3, "tan"); p.rect(37, 19, 45, 21, "yellow")  # the firefighter, in a helmet
    p.rect(38, 11, 43, 14, "dgrey"); p.rect(39, 9, 42, 11, "hpink")   # the lights
    p.rect(3, 33, 32, 35, "dred")
    for x in (12, 38):
        p.ball(x, 41, 6, 6, "black", "dgrey")
        p.ell(x, 41, 2, 2, "silver")
    return p.done()


def schoolbus():
    p = Pic()
    p.rect(3, 13, 45, 37, "yellow"); p.rect(3, 13, 45, 15, "dyellow")
    for i, x in enumerate((5, 13, 21, 29)):                       # windows, a friend in each
        p.rect(x, 18, x + 6, 27, "glass")
        p.ell(x + 3, 25, 2, 2, ("tan", "pink", "dtan", "lpink")[i])
    p.rect(37, 18, 45, 28, "glass")
    p.ell(41, 25, 3, 3, "tan")
    p.rect(3, 30, 45, 31, "black")
    p.rect(3, 34, 45, 35, "dyellow")
    p.ell(3, 24, 2, 2, "red")
    for x in (12, 37):
        p.ball(x, 41, 6, 6, "black", "dgrey")
        p.ell(x, 41, 2, 2, "silver")
    return p.done()


def helicopter():
    p = Pic()
    p.rect(5, 4, 43, 5, "dgrey"); p.rect(22, 5, 25, 11, "grey")   # the rotor
    p.ball(20, 23, 17, 12, "red", "dred")
    p.poly([(32, 20), (47, 15), (47, 21), (32, 27)], "red")       # the tail
    p.rect(44, 11, 45, 22, "dgrey")
    p.ell(12, 21, 9, 7, "glass")                                  # the cockpit, a pilot in it
    p.ell(11, 22, 3, 3, "tan"); p.rect(8, 19, 14, 20, "navy")
    p.rect(21, 17, 29, 23, "glass")
    p.rect(6, 37, 34, 38, "dgrey")                                # the skids
    p.rect(13, 32, 14, 37, "dgrey"); p.rect(27, 32, 28, 37, "dgrey")
    p.ell(5, 37, 2, 1, "dgrey")
    return p.done()


STAND_INS = {                    # the look-alike's name: the stand-in's name and picture
    "BLUE PUP": ("SPOTTY PUP", spottypup),
    "RED PUP": ("FOX", fox),
    "RED MONSTER": ("FUZZY", fuzzy),
    "BLUE MONSTER": ("BIG BLUE", bigblue),
    "WEB HERO": ("SPIDER", spider),
    "SLIMY": ("PUMPKIN", pumpkin),
    "YELLOW BIRD": ("CHICK", chick),
    "SKELETON": ("BAT", bat),
    "RANCHER": ("HORSE", horse),
    "RODEO": ("CACTUS", cactus),
    "SPACE HERO": ("ALIEN", alien),
    "SPIDER MOM": ("RAINBOW MOM", rainbowmom),
    "SPIDER GRANDMA": ("GREEN GRANNY", greengranny),
    "FAIRY MONSTER": ("PIXIE", pixie),
    "GROUCH": ("ALLEY CAT", alleycat),
    "TIGER CUB": ("LION CUB", lioncub),
    "RACCOON": ("SQUIRREL", squirrel),
}

ICONS = [icon_one, icon_choir, icon_strum, icon_accordion, icon_guess, icon_follow, icon_chords, icon_copy]


# order = the firmware's (kid.c KID_SOUND)
FRIENDS = [
    ("DUCKY", ducky("yellow", "dyellow")),
    ("PINK DUCKY", ducky("pink", "dpink", bow)),
    ("COOL DUCKY", ducky("green", "lime", bucket_shades)),
    ("AXOLOTL", axolotl),
    ("UNICORN", unicorn),
    ("GIRAFFE", giraffe),
    ("GOO", goo("pink", "dpink", "lpink")),
    ("GOOBERT", goo("mblue", "blue", "lblue")),
    ("BLUE PUP", bluepup),
    ("RED MONSTER", monster("red", "dred", "orange")),
    ("BLUE MONSTER", monster("blue", "dblue", None, True)),
    ("APRIL", doggy),
    ("SCISSORS", scissors),
    ("GHOST", ghost),
    ("WEB HERO", webhero),
    ("BUTTERFLY", butterfly),
    ("KITTY", kitty),
    ("FROG", frog),
    ("ROBOT", robot),
    ("RAINBOW", rainbow),
    ("PRINCESS DUCKY", ducky("lpurple", "purple", crown)),
    ("RED PUP", redpup),
    ("YELLOW BIRD", yellowbird),
    ("SLIMY", slimy),
    ("BUNNY", bunny),
    ("PANDA", panda),
    ("PENGUIN", penguin),
    ("OWL", owl),
    ("BEE", bee),
    ("LADYBUG", ladybug),
    ("DINO", dino),
    ("WHALE", whale),
    ("OCTOPUS", octopus),
    ("FISH", fish),
    ("TURTLE", turtle),
    ("ICE CREAM", icecream),
    ("CUPCAKE", cupcake),
    ("ROCKET", rocket),
    ("STRAWBERRY", strawberry),
    ("STAR", star),
    ("T-REX", trex),
    ("SKELETON", skeleton),
    ("RANCHER", cowkid("brown", "dbrown", "dbrown", "red", "yellow")),
    ("RODEO", cowkid("red", "dred", "orange", "yellow", "white", spots=True, braid=True)),
    ("VACUUM", vacuum),
    ("SPACE HERO", spacehero),
    ("BEAT BOT", beatbot),
    ("TOY DRUM", toydrum),
    ("BONGO", bongo),
    ("MONKEY", monkey),
    ("ELEPHANT", elephant),
    ("RACE CAR", racecar),
    ("JELLYFISH", jellyfish),
    ("BEAR", bear),
    ("SNOWMAN", snowman),
    ("CRAB", crab),
    ("WOLF", wolf),
    ("CAMEL", camel),
    ("SCIENTIST", scientist),
    ("FLYTRAP", flytrap),
    ("SUNFLOWER", sunflower),
    ("SPIDER MOM", spidermom),
    ("DRAGON DUCK", dragonduck),
    ("SPIDER GRANDMA", spidergrandma),
    ("NIGHT LIGHT", nightlight),
    ("GREEN QUEEN", greenqueen),
    ("KING AXOLOTL", kingaxolotl),
    ("FAIRY MONSTER", fairymonster),
    ("MORNING GLORY", morningglory),
    ("GROUCH", grouch),
    ("TIGER CUB", tigercub),
    ("RACCOON", raccoon),
    ("GOLDENROD", goldenrod),
    ("PIANO PAL", pianopal),
    ("FLUTE BIRD", flutebird),
    ("SAX CAT", saxcat),
    ("COW", cow),
    ("PIG", pig),
    ("SHEEP", sheep),
    ("SHARK", shark),
    ("SEAHORSE", seahorse),
    ("STARFISH", starfish),
    ("SNAIL", snail),
    ("CATERPILLAR", caterpillar),
    ("FIREFLY", firefly),
    ("TRICERATOPS", triceratops),
    ("STEGOSAURUS", stegosaurus),
    ("PIZZA", pizza),
    ("DONUT", donut),
    ("BANANA", banana),
    ("TRAIN", train),
    ("FIRE TRUCK", firetruck),
    ("SCHOOL BUS", schoolbus),
    ("HELICOPTER", helicopter),
    ("GOLD DUCKY", ducky("gold", "dyellow", goldcrown)),       # the secret friend (50 stars): always the last
]
SECRET_FRIEND = "GOLD DUCKY"


# the treble clef of the staff (kid.c): 16 x 46, the G clef (U+1D11E) of the FreeSerif font (GNU FreeFont, GPL-3.0 or
# later with the font exception), scaled down and thresholded, as plain rows here so the build needs no font
CLEF = [
    "........###.....",
    "........####....",
    ".......#####....",
    ".......#####....",
    "......###..##...",
    "......##...##...",
    "......##...##...",
    "......##...##...",
    "......#....##...",
    "......#...###...",
    "......#...###...",
    "......#..###....",
    "......######....",
    ".......#####....",
    "......#####.....",
    ".....#####......",
    "....######......",
    "...######.......",
    "...######.......",
    "..####..#.......",
    ".#####..#.......",
    ".####...##......",
    "####....#####...",
    "###...########..",
    "###...#########.",
    "##...#####.#####",
    "##...##..#...###",
    "##...##..##...##",
    "##...##...#...##",
    "##...##...#...##",
    ".##...#...#...##",
    "..#....#..#...##",
    "..##......##.##.",
    "...##......###..",
    ".....########...",
    "........#..#....",
    "...........##...",
    "...........##...",
    "............#...",
    ".....###....#...",
    "....#####...#...",
    "...######...#...",
    "...######...#...",
    "....####...##...",
    "....###...##....",
    "......#####.....",
]


def rle(idx):                          # a picture's colour indexes (N x N) as kid.c's runs (KID_RLE)
    lens, body = [], bytearray()
    for y in range(N):
        r = idx[y * N:(y + 1) * N]
        while r and r[-1] == 0:
            r.pop()
        row, i = bytearray(), 0
        while i < len(r):
            j = i
            while j < len(r) and r[j] == r[i] and j - i < 16:
                j += 1
            row.append(r[i] << 4 | (j - i - 1))
            i = j
        lens.append(len(row))
        body += row
    return bytes(lens) + bytes(body)


def rgb565(c):
    r, g, b = c[:3]
    return ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)


# ------------------------------------------------------------------ the hats
# Ten small hats any friend can wear (kid.c: HOME held 1 s, then KNOB 4). Each is drawn like a friend, then cropped to its
# own size and kept in a HAT_W x HAT_H box (bottom, centre); the friend's picture says where its head top is (hat_anchor).
HAT_W, HAT_H = 22, 16


def hat_party():
    p = Pic()
    p.poly([(24, 20), (17, 31), (31, 31)], "red")
    for x0, x1, y in ((22, 26, 24), (20, 28, 28)):
        p.rect(x0, y, x1, y + 1, "yellow")
    p.ell(24, 20, 2, 2, "yellow")
    p.rect(17, 30, 31, 31, "hpink")
    return p.done()


def hat_crown():
    p = Pic()
    p.poly([(16, 31), (16, 22), (20, 26), (24, 20), (28, 26), (32, 22), (32, 31)], "gold")
    p.rect(16, 28, 32, 31, "dyellow")
    p.px(24, 24, "red"); p.px(19, 29, "blue"); p.px(29, 29, "green")
    p.px(16, 21, "yellow"); p.px(24, 19, "yellow"); p.px(32, 21, "yellow")
    return p.done()


def hat_top():
    p = Pic()
    p.rect(18, 22, 30, 29, "black")
    p.rect(18, 26, 30, 27, "red")
    p.rect(15, 30, 33, 31, "black")
    p.rect(20, 23, 21, 24, "dgrey")
    return p.done()


def hat_bucket():
    p = Pic()
    for i, c in enumerate(["red", "orange", "yellow", "green", "blue"]):
        p.rect(18 - (i == 0) * -1, 22 + i * 2, 30 + (i == 0) * -1, 23 + i * 2, c)
    p.rect(15, 32, 33, 33, "purple")
    p.rect(18, 22, 30, 22, "red")
    return p.done()


def hat_wizard():
    p = Pic()
    p.poly([(26, 19), (19, 31), (31, 31), (29, 25)], "purple")
    p.poly([(26, 19), (30, 20), (28, 24)], "purple")
    p.rect(15, 30, 33, 32, "dpurple")
    p.px(24, 27, "yellow"); p.px(27, 25, "yellow"); p.px(22, 29, "yellow")
    return p.done()


def hat_beanie():
    p = Pic()
    p.ell(24, 27, 8, 5, "red")
    p.rect(16, 28, 32, 31, "white")
    for x in range(17, 32, 2):
        p.px(x, 29, "grey")
    p.ell(24, 21, 2, 2, "white")
    return p.done()


def hat_western():
    p = Pic()
    p.poly([(19, 30), (20, 23), (22, 25), (26, 25), (28, 23), (29, 30)], "brown")
    p.poly([(15, 28), (17, 31), (31, 31), (33, 28), (32, 32), (16, 32)], "dbrown")
    p.rect(20, 28, 28, 29, "dbrown")
    p.px(24, 23, "dbrown")
    return p.done()


def hat_chef():
    p = Pic()
    p.ell(19, 24, 4, 4, "white"); p.ell(24, 22, 5, 4, "white"); p.ell(29, 24, 4, 4, "white")
    p.rect(18, 26, 30, 31, "white")
    p.rect(18, 30, 30, 31, "dwhite")
    return p.done()


def hat_prop():
    p = Pic()
    p.pie(24, 31, 8, 180, 360, "blue")
    p.pie(24, 31, 8, 225, 270, "red"); p.pie(24, 31, 8, 270, 315, "yellow")
    p.rect(15, 30, 33, 31, "dblue")
    p.rect(23, 21, 24, 23, "grey")
    p.rect(18, 20, 30, 20, "red")
    return p.done()


def hat_star():                         # the secret hat (10 stars): a big gold star
    import math
    p = Pic()
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36)
        r = 6.5 if i % 2 == 0 else 2.8
        pts.append((round(24 + r * math.cos(a)), round(25 + r * math.sin(a))))
    p.poly(pts, "gold")
    p.rect(22, 30, 26, 31, "dyellow")                                # (a small base: the star sits on the head)
    p.px(24, 25, "yellow")
    return p.done()


def hat_flowers():
    p = Pic()
    p.rect(15, 29, 33, 31, "green")
    for x, c in ((17, "pink"), (21, "yellow"), (26, "white"), (30, "hpink")):
        p.ell(x, 28, 2, 2, c)
        p.px(x, 28, "gold")
    p.px(18, 26, "lgreen"); p.px(24, 25, "lgreen"); p.px(29, 26, "lgreen")
    return p.done()


HATS = [("PARTY", hat_party), ("CROWN", hat_crown), ("TOP HAT", hat_top), ("BUCKET", hat_bucket), ("WIZARD", hat_wizard),
        ("BEANIE", hat_beanie), ("WESTERN", hat_western), ("CHEF", hat_chef), ("PROPELLER", hat_prop), ("FLOWERS", hat_flowers),
        ("STAR", hat_star)]                 # (the last is the secret one)


def hat_sprite(f):                      # the hat cropped, in a HAT_W x HAT_H box, bottom and centre
    im = f().im
    x0, y0, x1, y1 = im.getbbox()
    w, h = x1 - x0, y1 - y0
    if w > HAT_W or h > HAT_H:
        raise SystemExit(f"a hat is {w} x {h}: {HAT_W} x {HAT_H} at most")
    out = Image.new("RGBA", (HAT_W, HAT_H), (0, 0, 0, 0))
    out.paste(im.crop((x0, y0, x1, y1)), ((HAT_W - w) // 2, HAT_H - h))
    return out


# where a friend wears a hat: (centre x, the row its hat's bottom edge sits on, hat width): the head top of its picture,
# found from the picture (the topmost rows' middle), and the overrides below for a picture that is not a head up top
HAT_AT = {}   # name -> (x, y, w)


def hat_anchor(name, im):
    px = im.load()
    rows = [y for y in range(N) if any(px[x, y][3] for x in range(N))]
    top = rows[0]
    if name in HAT_AT:
        return HAT_AT[name]
    xs = [x for y in range(top, min(top + 5, N)) for x in range(N) if px[x, y][3]]
    cx = (min(xs) + max(xs)) // 2
    span = [x for x in range(N) if px[x, min(top + 8, N - 1)][3]]
    w = max(10, min(20, (max(span) - min(span)) * 3 // 4 if span else 16))
    hh = HAT_H * w // HAT_W
    return cx, max(top + 4, hh + 1), w


hat_anchors = []


def main(out, png=None):
    names = [n for n, _ in FRIENDS]
    for k in STAND_INS:
        if k not in names:
            raise SystemExit(f"STAND_INS: {k} is not a friend")
    for name, _ in FRIENDS + list(STAND_INS.values()):   # the band shows the name: one line at scale 4 or 3, or two at 3
        if not re.fullmatch(r"[A-Z-]+( [A-Z-]+)*", name):
            raise SystemExit(f"{name!r}: capitals, hyphens and single spaces only (the band's font)")
        if len(name) * 18 - 3 > 232 and (" " not in name or len(name) > 15 or
                                          max(len(w) for w in name.split(" ", 1)) * 18 - 3 > 232):
            raise SystemExit(f"{name}: too long for the band, even on two lines")
    pics = []
    for name, f in FRIENDS + list(STAND_INS.values()):  # (the stand-ins after the friends: KID_N .. KID_NART - 1)
        try:
            pics.append((name, f().im))
        except SystemExit as e:
            raise SystemExit(f"{name}: {e}")
    hello = re.sub(r"[^A-Z ]", "", os.environ.get("KID_NAME", "").upper()).strip()[:10]
    hello = hello + "!" if hello else ""
    lines = ["/* generated by tools/gen_kid_art.py: Rainbow mode's friends */",
             f"#define KID_N {len(FRIENDS)}", f"#define KID_SECRET_FR {[n for n, _ in FRIENDS].index(SECRET_FRIEND)}", f"#define KID_NART {len(pics)}", f"#define KID_PW {N}",
             "static const char *const KID_NAME[KID_NART] = {" + ", ".join(f'"{n}"' for n, _ in pics) + "};",
             "/* a look-alike's stand-in (its picture and name, KID_N ..), 0 none: the grown-ups' LOOK-ALIKES (kid.c) */",
             "static const uint8_t KID_ALT[KID_N] = {" + ", ".join(
                 str(len(FRIENDS) + list(STAND_INS).index(n)) if n in STAND_INS else "0" for n in names) + "};",
             f'#define KID_HELLO_NAME "{hello}"', f"#define KID_HELLO_SC {5 if len(hello) <= 8 else 4}",
             "static const uint16_t KID_PAL[KID_NART][16] = {"]
    data = []
    for name, im in pics:
        cols = []
        idx = []
        for y in range(N):
            for x in range(N):
                p = im.getpixel((x, y))
                if not p[3]:
                    idx.append(0)
                    continue
                c = p[:3]
                if c not in cols:
                    cols.append(c)
                idx.append(cols.index(c) + 1)
        if len(cols) > 15:
            raise SystemExit(f"{name}: {len(cols)} colours, 15 at most")
        pal = [0] + [rgb565(c) for c in cols] + [0] * (15 - len(cols))
        lines.append("    {" + ", ".join(f"0x{v:04X}" for v in pal) + "},")
        data.append(rle(idx))
    lines.append("};")
    at, n = [], 0
    for d in data:
        at.append(n)
        n += len(d)
    if n > 0xFFFF:
        raise SystemExit(f"kid art: {n} B of runs, KID_RLE_AT is 16-bit")
    lines.append("/* each picture: its 48 rows' lengths in bytes, then the rows, a byte a run (colour << 4 | length - 1),")
    lines.append(" * a row's clear end left off; kid.c kid_row decodes a row */")
    lines.append("static const uint16_t KID_RLE_AT[KID_NART] = {" + ", ".join(map(str, at)) + "};")
    lines.append(f"static const uint8_t KID_RLE[{n}] = {{")
    for d in data:
        lines.append("    " + ",".join(str(b) for b in d) + ",")
    lines.append("};")
    rle_bytes = n
    icons = []
    for f in ICONS:
        im, cols, idx = f().im, [], []
        for y in range(N):
            for x in range(N):
                q = im.getpixel((x, y))
                if not q[3]:
                    idx.append(0)
                    continue
                if q[:3] not in cols:
                    cols.append(q[:3])
                idx.append(cols.index(q[:3]) + 1)
        if len(cols) > 15:
            raise SystemExit(f"{f.__name__}: {len(cols)} colours, 15 at most")
        icons.append(([0] + [rgb565(c) for c in cols] + [0] * (15 - len(cols)),
                      bytes((idx[i] << 4) | idx[i + 1] for i in range(0, len(idx), 2))))
    lines.append(f"#define KID_ICON_N {len(icons)}")
    lines.append("static const uint16_t KID_ICON_PAL[KID_ICON_N][16] = {")
    for pal, _ in icons:
        lines.append("    {" + ", ".join(f"0x{v:04X}" for v in pal) + "},")
    lines.append("};")
    lines.append(f"static const uint8_t KID_ICON_PIX[KID_ICON_N][{N * N // 2}] = {{")
    for _, d in icons:
        lines.append("    {" + ",".join(str(b) for b in d) + "},")
    lines.append("};")
    hat_data = []                                                # the hats, 4 bits a pixel, each with its own palette
    for _, f in HATS:
        him, cols, hidx = hat_sprite(f), [], []
        for y in range(HAT_H):
            for x in range(HAT_W):
                q = him.getpixel((x, y))
                if not q[3]:
                    hidx.append(0)
                    continue
                if q[:3] not in cols:
                    cols.append(q[:3])
                hidx.append(cols.index(q[:3]) + 1)
        if len(cols) > 15:
            raise SystemExit(f"a hat has {len(cols)} colours, 15 at most")
        hat_data.append(([0] + [rgb565(c) for c in cols] + [0] * (15 - len(cols)),
                         bytes((hidx[i] << 4) | hidx[i + 1] for i in range(0, len(hidx), 2))))
    lines.append(f"#define KID_HAT_N {len(HATS)}")
    lines.append(f"#define KID_HAT_W {HAT_W}")
    lines.append(f"#define KID_HAT_H {HAT_H}")
    lines.append("static const char *const KID_HAT_NAME[KID_HAT_N] = {" + ", ".join(f'"{n}"' for n, _ in HATS) + "};")
    lines.append("static const uint16_t KID_HAT_PAL[KID_HAT_N][16] = {")
    for pal, _ in hat_data:
        lines.append("    {" + ", ".join(f"0x{v:04X}" for v in pal) + "},")
    lines.append("};")
    lines.append(f"static const uint8_t KID_HAT_PIX[KID_HAT_N][{HAT_W * HAT_H // 2}] = {{")
    for _, d in hat_data:
        lines.append("    {" + ",".join(str(b) for b in d) + "},")
    lines.append("};")
    anchors = [hat_anchor(n, im) for n, im in pics]
    lines.append("/* where each picture's head top is: the hat's centre x, the row its bottom sits on, and its width (kid.c kid_hat) */")
    lines.append("static const uint8_t KID_HAT_AT[KID_NART][3] = {" + ", ".join("{%d, %d, %d}" % a for a in anchors) + "};")
    hat_anchors[:] = anchors
    lines.append(f"#define KID_CLEF_W {len(CLEF[0])}")
    lines.append(f"#define KID_CLEF_H {len(CLEF)}")
    lines.append(f"static const uint16_t KID_CLEF[{len(CLEF)}] = {{    /* bit 15 the left column */")
    lines.append("    " + ", ".join(f"0x{sum(1 << (15 - x) for x, c in enumerate(r) if c == '#'):04X}" for r in CLEF))
    lines.append("};")
    open(out, "w").write("\n".join(lines) + "\n")
    print(f"kid art: {len(FRIENDS)} friends and {len(STAND_INS)} stand-ins, {rle_bytes} B of runs (from {len(data) * N * N // 2})")
    if png:
        cols = 5
        sheet = Image.new("RGB", (cols * (N * 4 + 8), ((len(pics) + cols - 1) // cols) * (N * 4 + 8)), (120, 200, 255))
        for i, (_, im) in enumerate(pics):
            big = im.resize((N * 4, N * 4), Image.NEAREST)
            x, y = (i % cols) * (N * 4 + 8) + 4, (i // cols) * (N * 4 + 8) + 4
            ImageDraw.Draw(sheet).rectangle([x, y, x + N * 4 - 1, y + N * 4 - 1], outline=(90, 160, 220))
            sheet.paste(big, (x, y), big)
        sheet.save(png)
        hs = Image.new("RGB", (cols * (N * 4 + 8), ((len(pics) + cols - 1) // cols) * (N * 4 + 8)), (120, 200, 255))
        for i, (_, im) in enumerate(pics):                       # every picture in a hat, to check where they sit
            big = im.copy()
            cx, by, w = hat_anchors[i]
            hat = hat_sprite(HATS[i % len(HATS)][1])
            hh = HAT_H * w // HAT_W
            hat = hat.resize((w, hh), Image.NEAREST)
            big.alpha_composite(hat, (cx - w // 2, by - hh)) if cx - w // 2 >= 0 and by - hh >= 0 else None
            big = big.resize((N * 4, N * 4), Image.NEAREST)
            x, y = (i % cols) * (N * 4 + 8) + 4, (i // cols) * (N * 4 + 8) + 4
            hs.paste(big, (x, y), big)
        hs.save(png.replace(".png", "-hats.png"))
        row = Image.new("RGB", (len(ICONS) * (N * 4 + 8), N * 4 + 8), (150, 110, 230))
        for i, f in enumerate(ICONS):
            big = f().im.resize((N * 4, N * 4), Image.NEAREST)
            row.paste(big, (i * (N * 4 + 8) + 4, 4), big)
        row.save(png.replace(".png", "-icons.png"))


if __name__ == "__main__":
    a = sys.argv[1:]
    png = a[a.index("--png") + 1] if "--png" in a else None
    main(a[0], png)

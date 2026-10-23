# Album

A firmware for the M-VAVE FM-1 made like a record: twelve patches, each one a photo from Josh's phone and a sound
to go with it. The first album takes after My Bloody Valentine's *m b v* (2013). If it works, there could be more,
each its own album.

Nothing has been put on an FM-1 yet. This folder is the sound and the photos, worked out one patch at a time.

## The rules

- Nothing tinny or harsh. Every oscillator is band-limited so high notes don't fold back as whistles, every voice
  goes through a warm low-pass that darkens the high notes, and loud parts saturate softly, like tape.
- Photos are Josh's own, made smaller and nothing else. No AI repainting, and no Gemini anywhere in this project.
- Twelve great patches, no more. Sound first, features later.
- The sound is written from scratch. Felucca (Leo Kuroshita, Hügelton Instruments, GPL-3.0) will only start the chip
  and run the screen, keys, knobs and USB.

## The patches

| # | Photo | Patch | What it is |
|---|-------|-------|------------|
| 1 | Wing over the cloud deck, Pixel 9a, October 10, 2026 | WING | Slow and airy, a long arm bend, a little cabin hush |

## How it works

`src/album.c` is the GLIDE voice, after Kevin Shields' glide guitar: each note is four saws a few cents apart, each
wandering on its own, and one shared tremolo arm bends every held note down and back, as one guitar would.
`src/verb.c` is a big, dark reverb whose tail loses its highs first. `src/patches.c` holds the patches. It is all
integer math, as the FM-1 needs, so the recordings below come from the same code the FM-1 will run.

## Hearing a patch on a computer

```
cd host
cc -O2 -I../src -o render render.c ../src/album.c ../src/verb.c ../src/patches.c
./render 0 wing.wav          # patch number, file
python3 check.py wing.wav    # level, and how much sits up where sounds turn harsh
```

## Adding a photo

```
python3 tools/photo.py add PHONE.jpg 02-name --y 0.5   # square crop (--y 0 keeps the top), metadata dropped
python3 tools/photo.py build                           # 60 x 60 for the FM-1 (7,200 bytes), previews in build/
```

The screen is 240 x 240, so a 60 x 60 photo is stretched four times and smoothed. Twelve photos come to 86,400 bytes.

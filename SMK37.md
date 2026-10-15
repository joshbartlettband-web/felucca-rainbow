# Rainbow mode on the M-Vave SMK-37

Rainbow mode (see [RAINBOW.md](RAINBOW.md)) also builds for the M-Vave SMK-37, a 37-key controller with the same
chip as the FM-1. The FM-1 build is unchanged; everything for the SMK-37 is behind `BOARD_SMK37`.

Until this project's releases include SMK-37 packages, unofficial builds can be installed with the web installer: https://genkigenki.github.io/smk37/

## Supported models

- **SMK-37 Pro**: the default build (package identity `SMK-37 Pro_900`).
- **SMK-37 Elite**: `MODEL=elite` (identity `SMK-37 Elite_900`).
- **MKE-P37**: `MODEL=mke` (identity `MKE-P37_900`).
- **Starrykey 37 Play**: uses the SMK-37 Pro build.

All of them are the same hardware; each build carries its model's name, and the installer refuses a package made
for another model.

## Controls (the toy)

| SMK-37 | Does |
| --- | --- |
| Keys F3..G5 (the middle 27) | the FM-1's 27 keys: the friend sings, the letter shows |
| Keys C3..E3 and G#5..C6 (the outer 10) | more notes; the friend hops |
| 16 pads | the white keys F3..G5 (low notes on the bottom row), in their note colours; bright while held or while FOLLOW, GUESS or CHORDS light the key |
| K1 | volume (never above the grown-ups' VOLUME) |
| K2 / K3 / K4 | beat speed / how the keys play / next friend |
| K5..K8 and faders 1..4 | BIG/SMALL, DAY/NIGHT, ECHO, WIGGLE (a fader takes over once it moves) |
| Pitch wheel | a slide, up to 2 semitones |
| Mod wheel | more wiggle |
| FX, SCALE, CHORD, NOTE REPEAT, PARA, GLOBE | HICCUP, BACKWARDS, SLEEPY, SQUEAKY, GIANT, FREEZE |
| ARP / SEQ / SEQ PLAY / SEQ REC | sparkle / next beat (or song, lesson) / beat on-off / next sky |
| PATCH (HOME) | a surprise friend |
| BT (SAVE) | WRITE your own song, and back |
| OCTAVE- / OCTAVE+ | bigger / smaller |
| KNOB BANK | a surprise friend |
| FADER BANK | the next sky |
| < / > | the friend before / after |

All keys and pads play at one fixed velocity. No menu opens from the toy.

Grown-ups: PATCH held 1 s, then OCTAVE- / OCTAVE+ sets the VOLUME cap (PRESETS or < > the look-alikes);
PATCH + BT held 3 s opens the full Felucca until the next power-on.

The SMK-37's TRS jack is a MIDI output and this build does not use it; there is no TRS MIDI IN. MIDI works over USB.

## Build

See [BUILDING.md](BUILDING.md) for the toolchain.

```sh
BOARD=smk37 ./build.sh                 # build/rainbow-smk37.fwsc (SMK-37 Pro, Starrykey 37 Play)
BOARD=smk37 MODEL=elite ./build.sh     # build/rainbow-smk37-elite.fwsc
BOARD=smk37 MODEL=mke ./build.sh       # build/rainbow-smk37-mke.fwsc
./build.sh                             # the FM-1 build again before tests/run_tests.sh (the tests use its files)
```

## Install

Connect the keyboard by USB and run, with the package for your model:

```sh
python3 tools/fm1_install.py build/rainbow-smk37.fwsc
```

`fm1_install.py` needs `mido` and `python-rtmidi` (`pip3 install mido python-rtmidi`). It checks that the package
is for the connected model.

## Going back to the stock firmware

Install M-Vave's firmware package for your model with M-Vave's updater, M-UPGRADE. It works directly, because
the installed package keeps the keyboard's model name. `tools/fm1_install.py` can also install the stock SMK-37 Pro
V016 package.

## Safety

- Back up first: have M-Vave's stock package for your model and M-UPGRADE ready before you install.
- Keep the USB cable connected until the install has finished and the keyboard has restarted.
- The first start clears the stock firmware's settings, and any other firmware's data, in the shared data area.
- The firmware never writes the keyboard's calibration, Bluetooth pairing or key areas; the flash map refuses
  them at compile time and again in the flash driver.
- Installing other firmware is at your own risk.

# The FM-1 Transporter build for FM-1 Rescue

The firmware for the Transporter mode of [FM-1 Rescue](../android/README.md):
[FM-1-transporter](https://github.com/kurogedelic/FM-1-transporter) by kurogedelic (MIT), for a Seeed XIAO RP2040.
It wakes an FM-1's boot mode electrically (USB_KEY at power-on), so it reaches a unit that never shows up on USB
by itself.

The difference from the upstream build: **it carries no JieLi code.** Upstream embeds `wl82loader.bin` at build
time. This build leaves it out, and FM-1 Rescue uploads the loader at run time with the Transporter's own `memw`
and `jump` commands. The app downloads the loader from jl-uboot-tool and checks its sha256 first.
`0001-host-provided-loader.patch` makes `jump 0x1C02000 1` mark the loader as running, the same state the embedded
upload leaves, and changes nothing else.

- `build.sh WORK OUT` builds it: upstream at a pinned commit, Pico SDK 2.2.0, `PICO_BOARD=seeed_xiao_rp2040`. The
  workflow `.github/workflows/fm1-rescue.yml` runs it and publishes `fm1-transporter.uf2` and its license notices
  in the `fm1-rescue-test` prerelease, next to the app.
- Putting it on the XIAO: hold the XIAO's **B** (boot) button while connecting it, and it appears as a USB drive
  (RPI-RP2). Copy `fm1-transporter.uf2` onto it. A phone's Files app can do this through the OTG adapter. The XIAO
  restarts as the Transporter.

## Wiring

| XIAO RP2040 | FM-1 (a USB-C breakout plugged into it) |
|---|---|
| D6 (GP0) | D+ |
| D7 (GP1) | D- |
| GND | GND |

**Do not connect 5V/VBUS**: the FM-1 runs on its battery. If nothing happens, check D+ and D- are not swapped.
Some breakouts wire only one side of the plug, so turn the plug over.

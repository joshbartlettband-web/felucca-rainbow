#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-only
# Build the FM-1 Transporter firmware for FM-1 Rescue: kurogedelic/FM-1-transporter at a pinned commit, for the
# Seeed XIAO RP2040, WITHOUT JieLi's wl82loader.bin (the phone uploads it at run time), with
# 0001-host-provided-loader.patch. Output: OUT/fm1-transporter.uf2 and OUT/fm1-transporter-LICENSES.txt.
#   transporter/build.sh WORK_DIR OUT_DIR        (needs git, cmake, python3, arm-none-eabi-gcc with newlib)
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
WORK=$(mkdir -p "$1" && cd "$1" && pwd)
OUT=$(mkdir -p "$2" && cd "$2" && pwd)
TRANSPORTER_COMMIT=a632d923203170e3a08565f4056dbb3fd3d65ca5
PICO_SDK_TAG=2.2.0

if [ ! -d "$WORK/pico-sdk" ]; then
    git clone -q --depth 1 --branch "$PICO_SDK_TAG" https://github.com/raspberrypi/pico-sdk.git "$WORK/pico-sdk"
    git -C "$WORK/pico-sdk" submodule update -q --init --depth 1 lib/tinyusb
fi
rm -rf "$WORK/fm1t"
git init -q "$WORK/fm1t"
git -C "$WORK/fm1t" remote add origin https://github.com/kurogedelic/FM-1-transporter.git
git -C "$WORK/fm1t" fetch -q --depth 1 origin "$TRANSPORTER_COMMIT"
git -C "$WORK/fm1t" checkout -q FETCH_HEAD
git -C "$WORK/fm1t" submodule update -q --init --depth 1
git -C "$WORK/fm1t" apply "$HERE/0001-host-provided-loader.patch"

cmake -S "$WORK/fm1t" -B "$WORK/fm1t/build" -DPICO_SDK_PATH="$WORK/pico-sdk" -DPICO_BOARD=seeed_xiao_rp2040 \
      -DFM1T_LOADER_BIN=/nonexistent/wl82loader.bin >"$WORK/cmake.log" 2>&1
cmake --build "$WORK/fm1t/build" --target fm1_transporter -j4 >"$WORK/build.log" 2>&1 || { tail -40 "$WORK/build.log"; exit 1; }
cp "$WORK/fm1t/build/fm1_transporter.uf2" "$OUT/fm1-transporter.uf2"
{
    echo "fm1-transporter.uf2: FM-1 Transporter (https://github.com/kurogedelic/FM-1-transporter, commit $TRANSPORTER_COMMIT)"
    echo "for the Seeed XIAO RP2040, built without JieLi's wl82loader.bin, with FM-1 Rescue's"
    echo "transporter/0001-host-provided-loader.patch. It contains the following software:"
    for f in "$WORK/fm1t/LICENSE" "$WORK/fm1t/lib/Pico-PIO-USB/LICENSE" "$WORK/pico-sdk/LICENSE.TXT" "$WORK/pico-sdk/lib/tinyusb/LICENSE"; do
        echo; echo "==== ${f#$WORK/} ===="; cat "$f"
    done
} >"$OUT/fm1-transporter-LICENSES.txt"
python3 - "$OUT/fm1-transporter.uf2" <<'PY'
import sys
b = open(sys.argv[1], "rb").read()
assert len(b) % 512 == 0 and b[:4] == b"UF2\n", "not a UF2 file"
print(f"{sys.argv[1]}: {len(b)} bytes, {len(b) // 512} UF2 blocks")
PY

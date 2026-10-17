#!/bin/sh
# The browser build without Emscripten, for recording the tour where emsdk cannot be installed: plain clang and
# wasi-libc (Debian/Ubuntu: apt install clang lld wasi-libc libclang-rt-18-dev-wasm32). It makes the same
# build/emu/felucca.wasm as web/emu/build.sh (no imports; web/emu/kid_test.mjs passes on it). Run after the
# generate step (build/gen). The site is still built with Emscripten (.github/workflows/rainbow.yml).
set -e
cd "$(dirname "$0")/../.."
[ -f build/gen/felucca_tables.h ] || { echo "run the generate step first (build/gen)"; exit 1; }
VERSION=$(sed -n 's/^#define FELUCCA_VERSION "\([^"]*\)".*/\1/p' firmware/src/felucca.c)
mkdir -p build/emu build/wasishim/sys
cat > build/wasishim/sys/wait.h <<'H'
#pragma once
/* the browser build never forks (tests/hostsim.c's helpers); stubs, as Emscripten has */
static inline int pipe(int *f) { (void)f; return -1; }
static inline int fork(void) { return -1; }
static inline int waitpid(int p, int *s, int o) { (void)p; (void)s; (void)o; return -1; }
#define WIFEXITED(s) 0
#define WEXITSTATUS(s) 0
H
clang --target=wasm32-wasi -isystem build/wasishim -isystem /usr/include/wasm32-wasi -L/usr/lib/wasm32-wasi \
    -O2 -ffp-contract=off -std=gnu99 -w "-DFELUCCA_VERSION=\"$VERSION\"" -Ibuild/gen -Ifirmware/src \
    -mexec-model=reactor -Wl,--export-dynamic -Wl,-z,stack-size=1048576 -Wl,--initial-memory=33554432 \
    -o build/emu/felucca.wasm web/emu/felucca_web.c -lm
echo "clang: build/emu/felucca.wasm ($(wc -c < build/emu/felucca.wasm | tr -d ' ') B, $VERSION)"
